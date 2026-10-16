"""Call the anonymous manufacturer CAD read endpoints exposed by its public button."""
from collect_motor_splitter_refs import BASE,fetch
import json,sys
def main():
    sys.stdout.reconfigure(encoding='utf-8');p=BASE/'assets.json';d=json.loads(p.read_text(encoding='utf-8'));old={a['file']:a for a in d['assets']}
    query='?part_number=UD-80A&check_availability=0&brand=ERIFLEX'
    for kind in ['viewer','options']:
        rec=fetch(('sources-web/nVent-CAD-'+kind+'.json','https://www.nvent.com/en-us/api/traceparts/'+kind+query));old[rec['file']]=rec
        print(kind,rec['status'],rec.get('bytes',rec.get('error')),flush=True)
        if rec.get('status')=='downloaded':
            try:
                result=json.loads((BASE/rec['file']).read_text(encoding='utf-8'));print('PUBLIC_CAD_RESPONSE',result,flush=True)
            except ValueError:print('not JSON',flush=True)
    d['assets']=list(old.values());p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
