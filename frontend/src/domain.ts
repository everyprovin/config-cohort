export type ChainRecord={record_id:string;owner:string;status:string;revision:number;source:unknown;result:any;certificate_id:string;source_url:string;source_sha256:string};
export const ascii=(a:string,b:string)=>a<b?-1:a>b?1:0;
function fields(value:any,keys:string[]):void{if(!value||typeof value!=='object'||Array.isArray(value)||Object.keys(value).sort(ascii).join('|')!==[...keys].sort(ascii).join('|'))throw Error('Unexpected schema fields.');}
const id=(s:unknown):s is string=>typeof s==='string'&&/^[A-Za-z][A-Za-z0-9_]{0,23}$/.test(s);
const integer=(v:unknown,min:number,max:number)=>typeof v==='number'&&Number.isInteger(v)&&v>=min&&v<=max;
const canonical=(value:any):string=>value&&typeof value==='object'?(Array.isArray(value)?'['+value.map(canonical).join(',')+']':'{'+Object.keys(value).sort(ascii).map(k=>JSON.stringify(k)+':'+canonical(value[k])).join(',')+'}'):JSON.stringify(value);

export type Policy={schema:string;variables:{id:string;baseline:boolean;flip_weight:number}[];clauses:string[][]};
export type Recommendation={decision:'SAT'|'UNSAT';assignment:Record<string,boolean>|null;bits:string|null;flip_cost:number|null;flips:string[];model_count:number;examined:number;clauses:{index:number;satisfied_by:string[]}[]};
export function validatePolicy(value:unknown):Policy{
 const p=value as Policy;fields(p,['schema','variables','clauses']);
 if(p.schema!=='ConfigCohort-policy-v1'||!Array.isArray(p.variables)||p.variables.length<1||p.variables.length>12||!Array.isArray(p.clauses)||p.clauses.length<1||p.clauses.length>24)throw Error('Policy schema or bounds.');
 const names=new Set<string>();for(const v of p.variables){fields(v,['id','baseline','flip_weight']);if(!id(v.id)||names.has(v.id)||typeof v.baseline!=='boolean'||!integer(v.flip_weight,1,1000000))throw Error('Variable ID, baseline or positive flip weight invalid.');names.add(v.id);}
 const seen=new Set<string>();for(const clause of p.clauses){if(!Array.isArray(clause)||clause.length<1||clause.length>12)throw Error('Clause bound.');const used=new Set<string>();for(const literal of clause){if(typeof literal!=='string')throw Error('Literal must be a string.');const name=literal.startsWith('!')?literal.slice(1):literal;if(!names.has(name)||used.has(name))throw Error('Unknown, duplicate or contradictory literal.');used.add(name);}const key=[...clause].sort(ascii).join('|');if(seen.has(key))throw Error('Duplicate clause.');seen.add(key);}
 return {schema:p.schema,variables:p.variables.map(v=>({...v})).sort((a,b)=>ascii(a.id,b.id)),clauses:p.clauses.map(c=>[...c])};
}
export function compare(p:Policy,assignment:Record<string,boolean>){
 if(!assignment||typeof assignment!=='object'||Array.isArray(assignment)||Object.keys(assignment).length!==p.variables.length||p.variables.some(v=>typeof assignment[v.id]!=='boolean'))throw Error('Complete Boolean assignment required.');
 const clauses=p.clauses.map((clause,index)=>({index,satisfied_by:clause.filter(l=>l.startsWith('!')?!assignment[l.slice(1)]:assignment[l])}));
 const violated_clauses=clauses.filter(c=>!c.satisfied_by.length).map(c=>c.index),flips=p.variables.filter(v=>assignment[v.id]!==v.baseline).map(v=>v.id);
 return {satisfied:violated_clauses.length===0,violated_clauses,clauses,flips,flip_cost:p.variables.filter(v=>flips.includes(v.id)).reduce((a,v)=>a+v.flip_weight,0)};
}
export function recommend(p:Policy):Recommendation{
 const n=p.variables.length;let best:Recommendation|null=null,model_count=0;
 for(let mask=0;mask<2**n;mask++){const assignment=Object.fromEntries(p.variables.map((v,i)=>[v.id,!!((mask>>(n-1-i))&1)]));const c=compare(p,assignment);if(!c.satisfied)continue;model_count++;if(!best||c.flip_cost<best.flip_cost!){best={decision:'SAT',assignment,bits:p.variables.map(v=>assignment[v.id]?'1':'0').join(''),flip_cost:c.flip_cost,flips:c.flips,model_count:0,examined:2**n,clauses:c.clauses};}}
 return best?{...best,model_count}:{decision:'UNSAT',assignment:null,bits:null,flip_cost:null,flips:[],model_count:0,examined:2**n,clauses:[]};
}
export function assertChainResult(p:Policy,result:unknown):void{if(canonical(recommend(p))!==canonical(result))throw Error('Chain result inconsistent with its policy source.');}
export function canConfirm(r:any,account:string):boolean{return !!account&&r?.owner?.toLowerCase()===account.toLowerCase()&&r?.status==='DERIVED'&&r?.result?.decision==='SAT';}
