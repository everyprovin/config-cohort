# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
import hashlib
import json
import re
from datetime import datetime, timezone


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise gl.vm.UserError('[EXPECTED] '+message)


def _canonical(value) -> str:
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)


def _now() -> int:
    value=datetime.fromisoformat(gl.message_raw['datetime'].replace('Z','+00:00'))
    if value.tzinfo is None:
        value=value.replace(tzinfo=timezone.utc)
    delta=value.astimezone(timezone.utc)-datetime(1970,1,1,tzinfo=timezone.utc)
    return delta.days*86400+delta.seconds


def _identifier(value) -> None:
    _require(isinstance(value,str) and re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,23}',value) is not None,'invalid ASCII identifier')


def _source_locator(url: str,digest: str) -> None:
    pattern=r'https://raw\.githubusercontent\.com/[A-Za-z0-9-]{1,39}/[A-Za-z0-9_.-]{1,100}/[0-9a-f]{40}/([A-Za-z0-9_.~/-]+)'
    match=re.fullmatch(pattern,url) if isinstance(url,str) and len(url)<=512 else None
    _require(match is not None and all(part not in ('','.','..') for part in url.split('/')[3:]) and url.endswith('/profile05/projects/config-cohort/fixtures/policy.json'),'commit-pinned project source required')
    _require(isinstance(digest,str) and re.fullmatch(r'[0-9a-f]{64}',digest) is not None,'invalid SHA256')


def _unique_pairs(pairs: list) -> dict:
    result={}
    for key,value in pairs:
        _require(key not in result,'duplicate JSON key')
        result[key]=value
    return result


def _parse_json(body: bytes):
    _require(1<=len(body)<=32768,'source byte bound')
    try:
        return json.loads(body.decode('utf-8'),object_pairs_hook=_unique_pairs)
    except (ValueError,UnicodeError,RecursionError):
        raise gl.vm.UserError('[SOURCE] invalid UTF-8 JSON')


def _fetch(url: str,digest: str) -> dict:
    response=gl.nondet.web.get(url,headers={'Accept':'application/json'})
    if response.status!=200 or response.body is None or not 1<=len(response.body)<=32768:
        raise gl.vm.UserError('[SOURCE] source unavailable or oversized')
    if hashlib.sha256(response.body).hexdigest()!=digest:
        raise gl.vm.UserError('[SOURCE] source byte SHA256 mismatch')
    return _validate(_parse_json(response.body))


def _validate(value) -> dict:
    _require(isinstance(value,dict) and set(value)=={'schema','variables','clauses'} and value['schema']=='ConfigCohort-policy-v1','policy schema fields')
    variables=value['variables'];clauses=value['clauses']
    _require(isinstance(variables,list) and 1<=len(variables)<=12,'variable count 1..12')
    _require(isinstance(clauses,list) and 1<=len(clauses)<=24,'clause count 1..24')
    names=set()
    for variable in variables:
        _require(isinstance(variable,dict) and set(variable)=={'id','baseline','flip_weight'},'variable fields')
        _identifier(variable['id'])
        _require(variable['id'] not in names,'duplicate variable ID');names.add(variable['id'])
        _require(type(variable['baseline']) is bool,'baseline must be Boolean')
        _require(type(variable['flip_weight']) is int and 1<=variable['flip_weight']<=1000000,'flip weight 1..1000000')
    seen=set()
    for clause in clauses:
        _require(isinstance(clause,list) and 1<=len(clause)<=12,'clause size 1..12')
        clause_variables=set()
        for literal in clause:
            _require(isinstance(literal,str) and 1<=len(literal)<=25,'literal must be string')
            name=literal[1:] if literal.startswith('!') else literal
            _require(name in names,'unknown literal variable')
            _require(name not in clause_variables,'duplicate or contradictory literal');clause_variables.add(name)
        key=tuple(sorted(clause))
        _require(key not in seen,'duplicate clause');seen.add(key)
    return {'schema':value['schema'],'variables':sorted(variables,key=lambda item:item['id']),'clauses':clauses}


def _compare(policy: dict,assignment: dict) -> dict:
    variables=policy['variables']
    _require(isinstance(assignment,dict) and set(assignment)==set(item['id'] for item in variables) and all(type(v) is bool for v in assignment.values()),'complete Boolean assignment required')
    clauses=[];violations=[]
    for index,clause in enumerate(policy['clauses']):
        # Build each literal witness explicitly so negation and positive values cannot alias.
        witnesses=[]
        for literal in clause:
            satisfied=(not assignment[literal[1:]]) if literal.startswith('!') else assignment[literal]
            if satisfied:
                witnesses.append(literal)
        clauses.append({'index':index,'satisfied_by':witnesses})
        if not witnesses:
            violations.append(index)
    flips=[v['id'] for v in variables if assignment[v['id']]!=v['baseline']]
    return {'satisfied':not violations,'violated_clauses':violations,'clauses':clauses,'flips':flips,'flip_cost':sum(v['flip_weight'] for v in variables if v['id'] in flips)}


def _derive(policy: dict) -> dict:
    variables=policy['variables'];n=len(variables);best=None;models=0
    for code in range(1<<n):
        assignment={v['id']:bool((code>>(n-1-i))&1) for i,v in enumerate(variables)}
        valid=True
        for clause in policy['clauses']:
            if not any((not assignment[literal[1:]]) if literal.startswith('!') else assignment[literal] for literal in clause):
                valid=False;break
        if not valid:
            continue
        models+=1
        cost=sum(v['flip_weight'] for v in variables if assignment[v['id']]!=v['baseline'])
        candidate=(cost,code)
        if best is None or candidate<best:
            best=candidate
    if best is None:
        return {'decision':'UNSAT','assignment':None,'bits':None,'flip_cost':None,'flips':[],'model_count':0,'examined':1<<n,'clauses':[]}
    cost,code=best
    assignment={v['id']:bool((code>>(n-1-i))&1) for i,v in enumerate(variables)}
    comparison=_compare(policy,assignment)
    return {'decision':'SAT','assignment':assignment,'bits':''.join('1' if assignment[v['id']] else '0' for v in variables),'flip_cost':cost,'flips':comparison['flips'],'model_count':models,'examined':1<<n,'clauses':comparison['clauses']}

def _capture(url: str,digest: str,binding: dict) -> dict:
    def leader() -> dict:
        source=_fetch(url,digest)
        return {'binding':binding,'source_sha256':digest,'source':source,'result':None if binding['operation']=='lock' else _derive(source)}
    def validator(proposed: gl.vm.Result) -> bool:
        if not isinstance(proposed,gl.vm.Return):
            return False
        try:
            return _canonical(leader())==_canonical(proposed.calldata)
        except Exception:
            return False
    return gl.vm.run_nondet_unsafe(leader,validator)


class ConfigCohort(gl.Contract):
    records: TreeMap[str,str]

    def __init__(self):
        pass

    def _record(self,record_id: str) -> dict:
        _require(record_id in self.records,'unknown record')
        return json.loads(self.records[record_id])

    def _owner_revision(self,record: dict,expected_revision: int) -> None:
        _require(gl.message.sender_address.as_hex.lower()==record['owner'],'owner only')
        _require(type(expected_revision) is int and expected_revision==record['revision'],'stale revision')

    def _binding(self,record: dict,operation: str) -> dict:
        return {'protocol':'ConfigCohort-v1','chain_id':int(gl.message.chain_id),'contract':gl.message.contract_address.as_hex.lower(),'owner':record['owner'],'record_id':record['record_id'],'source_url':record['source_url'],'source_sha256':record['source_sha256'],'revision':record['revision'],'operation':operation,'observed_at':_now()}

    @gl.public.write
    def lock_source(self,record_id: str,source_url: str,source_sha256: str) -> None:
        _identifier(record_id);_source_locator(source_url,source_sha256)
        _require(record_id not in self.records,'record ID already used')
        record={'record_id':record_id,'owner':gl.message.sender_address.as_hex.lower(),'source_url':source_url,'source_sha256':source_sha256,'status':'LOCKED','revision':0,'locked_at':_now(),'derived_at':0,'confirmed_at':0,'revoked_at':0,'reason':'','result':None,'certificate_id':''}
        packet=_capture(source_url,source_sha256,self._binding(record,'lock'))
        record['source']=packet['source'];record['last_capture']=packet
        self.records[record_id]=_canonical(record)

    @gl.public.write
    def derive(self,record_id: str,expected_revision: int) -> dict:
        record=self._record(record_id);self._owner_revision(record,expected_revision)
        _require(record['status']=='LOCKED','record not locked')
        packet=_capture(record['source_url'],record['source_sha256'],self._binding(record,'derive'))
        _require(_canonical(packet['source'])==_canonical(record['source']),'source snapshot mismatch')
        record['result']=packet['result'];record['last_capture']=packet;record['status']='DERIVED';record['revision']=1;record['derived_at']=_now()
        self.records[record_id]=_canonical(record)
        return record['result']

    @gl.public.write
    def confirm(self,record_id: str,expected_revision: int) -> None:
        record=self._record(record_id);self._owner_revision(record,expected_revision)
        _require(record['status']=='DERIVED','record not derived')
        _require(record['result']['decision']=='SAT','no satisfiable model to confirm')
        packet=_capture(record['source_url'],record['source_sha256'],self._binding(record,'confirm'))
        _require(_canonical(packet['source'])==_canonical(record['source']) and _canonical(packet['result'])==_canonical(record['result']),'derived snapshot mismatch')
        record['last_capture']=packet;record['status']='CONFIRMED';record['revision']=2;record['confirmed_at']=_now()
        record['certificate_id']=hashlib.sha256(_canonical(packet).encode('utf-8')).hexdigest()
        self.records[record_id]=_canonical(record)

    @gl.public.write
    def revoke(self,record_id: str,expected_revision: int,reason: str) -> None:
        record=self._record(record_id);self._owner_revision(record,expected_revision)
        _require(record['status']!='REVOKED','record already revoked')
        _require(isinstance(reason,str) and 1<=len(reason)<=200 and reason==reason.strip(),'reason required 1..200 characters')
        record['status']='REVOKED';record['revision']+=1;record['reason']=reason;record['revoked_at']=_now()
        self.records[record_id]=_canonical(record)

    @gl.public.view
    def get_record(self,record_id: str) -> dict:
        return self._record(record_id)

    @gl.public.view
    def get_configuration(self) -> dict:
        return {'protocol':'ConfigCohort-v1','max_variables':12,'max_clauses':24,'max_source_bytes':32768,'max_flip_weight':1000000,'real_infrastructure_modified':False}

    @gl.public.view
    def compare_assignment(self,record_id: str,assignment_json: str) -> dict:
        _require(isinstance(assignment_json,str) and len(assignment_json)<=4096,'assignment byte bound')
        record=self._record(record_id)
        return _compare(record['source'],_parse_json(assignment_json.encode('utf-8')))

