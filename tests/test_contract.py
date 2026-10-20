"""Actual pinned SDK integration; only external HTTP is fixture-controlled."""
import copy, hashlib, json, re
from pathlib import Path
import pytest
from gltest.direct import create_address

ROOT=Path(__file__).parents[1]
SOURCE=json.loads((ROOT/'fixtures/source.json').read_text())
BODY=(ROOT/'fixtures/policy.json').read_bytes().decode('utf-8')

def deploy(vm,build):
    vm.warp('2026-10-21T00:00:00Z')
    c=build(str(ROOT/'contract.py'),sdk_version='v0.2.12')
    assert hasattr(c,'lock_source'),'lock_source API not implemented'
    return c

def serve(vm,body=BODY,status=200):
    vm.mock_web(re.escape(SOURCE['test_url']),{'status':status,'body':body})

def lock(vm,c,body=BODY):
    serve(vm,body)
    c.lock_source('demo',SOURCE['test_url'],hashlib.sha256(body.encode()).hexdigest())

def test_owner_revision_revoke_and_permanent_ids(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy);lock(direct_vm,c)
    outsider=create_address('outsider')
    with direct_vm.prank(outsider):
        with direct_vm.expect_revert('owner only'):c.derive('demo',0)
        with direct_vm.expect_revert('owner only'):c.revoke('demo',0,'withdraw')
    with direct_vm.expect_revert('stale revision'):c.derive('demo',1)
    c.derive('demo',0)
    with direct_vm.prank(outsider):
        with direct_vm.expect_revert('owner only'):c.confirm('demo',1)
    with direct_vm.expect_revert('stale revision'):c.confirm('demo',0)
    c.confirm('demo',1)
    d=c.get_record('demo')
    assert d['status']=='CONFIRMED' and d['revision']==2 and len(d['certificate_id'])==64
    direct_vm.clear_mocks();c.revoke('demo',2,'Synthetic certificate withdrawn')
    d=c.get_record('demo');assert d['status']=='REVOKED' and d['revision']==3
    with direct_vm.expect_revert():c.confirm('demo',3)
    with direct_vm.expect_revert():c.revoke('demo',3,'again')
    with direct_vm.expect_revert('already used'):lock(direct_vm,c)

def test_fresh_independent_validator_rejects_changed_bytes_and_forged_binding(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy);lock(direct_vm,c);c.derive('demo',0)
    assert direct_vm.run_validator() is True
    packet=copy.deepcopy(c.get_record('demo')['last_capture'])
    packet['binding']['record_id']='another'
    assert direct_vm.run_validator(leader_result=packet) is False
    packet=copy.deepcopy(c.get_record('demo')['last_capture'])
    packet['result']=None
    assert direct_vm.run_validator(leader_result=packet) is False
    direct_vm.clear_mocks();serve(direct_vm,BODY+' ')
    assert direct_vm.run_validator() is False

def test_confirmation_rechecks_source_and_failed_write_preserves_revision(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy);lock(direct_vm,c);c.derive('demo',0)
    direct_vm.clear_mocks();serve(direct_vm,'gone',404)
    with direct_vm.expect_revert('SOURCE'):c.confirm('demo',1)
    assert c.get_record('demo')['status']=='DERIVED' and c.get_record('demo')['revision']==1

@pytest.mark.parametrize('url',[
 'https://raw.githubusercontent.com/a/b/main/profile05/projects/config-cohort/fixtures/policy.json',
 'https://raw.githubusercontent.com/a/b/'+'0'*40+'/profile05/projects/other/fixtures/policy.json',
 'https://raw.githubusercontent.com/a/b/'+'0'*40+'/x/../profile05/projects/config-cohort/fixtures/policy.json',
 'https://raw.githubusercontent.com/a/b/'+'0'*40+'/profile05/projects/config-cohort/fixtures/policy.json?raw=1',
 'http://raw.githubusercontent.com/a/b/'+'0'*40+'/profile05/projects/config-cohort/fixtures/policy.json',
])
def test_rejects_mutable_cross_project_or_noncanonical_source(direct_vm,direct_deploy,url):
    c=deploy(direct_vm,direct_deploy)
    with direct_vm.expect_revert('commit-pinned'):c.lock_source('demo',url,'0'*64)

@pytest.mark.parametrize('body',['x','[]','{}','{'+(' '*32768)+'}', '\ufeff{}'],ids=['invalid','array','empty','oversize','bom'])
def test_rejects_malformed_or_oversized_source(direct_vm,direct_deploy,body):
    c=deploy(direct_vm,direct_deploy)
    with direct_vm.expect_revert():lock(direct_vm,c,body)

def test_digest_and_unknown_record_errors(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy);serve(direct_vm)
    with direct_vm.expect_revert('SOURCE'):c.lock_source('demo',SOURCE['test_url'],'0'*64)
    with direct_vm.expect_revert('unknown record'):c.get_record('missing')
    with direct_vm.expect_revert():c.lock_source('bad id',SOURCE['test_url'],SOURCE['sha256'])

def test_exact_weighted_optimum_with_literal_witnesses(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy);lock(direct_vm,c)
    out=c.derive('demo',0)
    assert out['decision']=='SAT' and out['assignment']=={'audit':False,'cache':True,'preview':False,'telemetry':False}
    assert out['bits']=='0100' and out['flip_cost']==3 and out['flips']==['cache','preview']
    assert out['examined']==16 and out['model_count']==7
    assert out['clauses']==[{'index':0,'satisfied_by':['cache']},{'index':1,'satisfied_by':['!preview']},{'index':2,'satisfied_by':['!telemetry']},{'index':3,'satisfied_by':['!telemetry']}]
    assert direct_vm.run_validator() is True
    bad=c.compare_assignment('demo',json.dumps({'audit':False,'cache':False,'preview':True,'telemetry':False}))
    assert bad['satisfied'] is False and bad['violated_clauses']==[0,1] and bad['flip_cost']==0
    c.confirm('demo',1);assert direct_vm.run_validator() is True

def test_false_before_true_ascii_lex_tie_and_sorted_variables(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy)
    p={'schema':'ConfigCohort-policy-v1','variables':[{'id':'b','baseline':False,'flip_weight':1},{'id':'A','baseline':False,'flip_weight':1}], 'clauses':[['b','A']]}
    lock(direct_vm,c,json.dumps(p));out=c.derive('demo',0)
    assert out['assignment']=={'A':False,'b':True} and out['bits']=='01' and out['flip_cost']==1

def test_unsat_has_no_model_and_cannot_confirm(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy)
    p={'schema':'ConfigCohort-policy-v1','variables':[{'id':'x','baseline':False,'flip_weight':1}], 'clauses':[['x'],['!x']]}
    lock(direct_vm,c,json.dumps(p));out=c.derive('demo',0)
    assert out=={'decision':'UNSAT','assignment':None,'bits':None,'flip_cost':None,'flips':[],'model_count':0,'examined':2,'clauses':[]}
    with direct_vm.expect_revert('no satisfiable'):c.confirm('demo',1)

@pytest.mark.parametrize('change', ['unknown','bool_weight','zero_weight','duplicate_id','duplicate_clause','duplicate_literal','tautology','unknown_literal','empty_clause','nonbool_baseline','too_many_vars','too_many_clauses','bad_schema'])
def test_strict_policy_boundaries(direct_vm,direct_deploy,change):
    p=json.loads(BODY)
    if change=='unknown':p['extra']=0
    if change=='bool_weight':p['variables'][0]['flip_weight']=True
    if change=='zero_weight':p['variables'][0]['flip_weight']=0
    if change=='duplicate_id':p['variables'][1]['id']=p['variables'][0]['id']
    if change=='duplicate_clause':p['clauses'].append(list(reversed(p['clauses'][0])))
    if change=='duplicate_literal':p['clauses'][0]=['cache','cache']
    if change=='tautology':p['clauses'][0]=['cache','!cache']
    if change=='unknown_literal':p['clauses'][0]=['missing']
    if change=='empty_clause':p['clauses'][0]=[]
    if change=='nonbool_baseline':p['variables'][0]['baseline']=0
    if change=='too_many_vars':p['variables']=[{'id':'x'+str(i),'baseline':False,'flip_weight':1} for i in range(13)]
    if change=='too_many_clauses':p['clauses']=[['cache']]*25
    if change=='bad_schema':p['schema']='other'
    c=deploy(direct_vm,direct_deploy)
    with direct_vm.expect_revert():lock(direct_vm,c,json.dumps(p))

def test_duplicate_json_keys_and_incomplete_manual_assignment(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy)
    with direct_vm.expect_revert('duplicate'):lock(direct_vm,c,BODY.replace('"baseline": false','"baseline": false, "baseline": true',1))
    direct_vm.clear_mocks();lock(direct_vm,c)
    with direct_vm.expect_revert():c.compare_assignment('demo','{"audit":true}')
    with direct_vm.expect_revert():c.compare_assignment('demo','{"audit":true,"audit":false}')

def test_twelve_variable_bound_examines_all_assignments(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy)
    p={'schema':'ConfigCohort-policy-v1','variables':[{'id':'v'+str(i).zfill(2),'baseline':False,'flip_weight':1} for i in range(12)],'clauses':[['v00']]}
    lock(direct_vm,c,json.dumps(p));out=c.derive('demo',0)
    assert out['examined']==4096 and out['model_count']==2048 and out['flip_cost']==1 and out['bits']=='100000000000'


def test_fixture_metadata_locks_exact_bytes_without_newline_normalization(direct_vm,direct_deploy):
    raw=(ROOT/'fixtures/policy.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==SOURCE['sha256']
    c=deploy(direct_vm,direct_deploy);serve(direct_vm,raw.decode('utf-8'))
    c.lock_source('exactbytes',SOURCE['test_url'],SOURCE['sha256'])
    assert c.get_record('exactbytes')['source_sha256']==SOURCE['sha256']
