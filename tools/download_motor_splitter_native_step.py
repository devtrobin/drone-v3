"""Download the STEP AP214 option offered by the manufacturer, preserving bytes."""
from collect_motor_splitter_refs import BASE,fetch
from pathlib import Path
import json,sys,zipfile,hashlib
def main():
    sys.stdout.reconfigure(encoding='utf-8');manifest=BASE/'assets.json';d=json.loads(manifest.read_text(encoding='utf-8'));old={a['file']:a for a in d['assets']}
    opts=json.loads((BASE/'sources-web/nVent-CAD-options.json').read_text(encoding='utf-8'))['options']
    url=next(k for k,v in opts.items() if v=='STEP AP214');url='https:'+url if url.startswith('//') else url
    rec=fetch(('3D/originaux/nVent-UD80A-AP214-telechargement.bin',url));old[rec['file']]=rec
    print('DOWNLOAD',rec['status'],rec.get('bytes',rec.get('error')),flush=True)
    if rec.get('status')=='downloaded':
        p=BASE/rec['file'];b=p.read_bytes();print('format',b[:50],flush=True)
        records=[]
        if b.startswith(b'ISO-10303-21;'):records=[(p.name,b)]
        elif zipfile.is_zipfile(p):
            with zipfile.ZipFile(p) as z:
                print('zip entries',z.namelist(),flush=True)
                records=[(n,z.read(n)) for n in z.namelist() if Path(n).suffix.lower() in ['.stp','.step']]
        elif b.startswith(b'{'):
            info=json.loads(b);print('JSON_RESPONSE',info,flush=True)
        for n,data in records:
            assert data.lstrip().startswith(b'ISO-10303-21;');target=BASE/'3D/eriflex-ud80a-officiel.step';target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
            a=dict(file=str(target.relative_to(BASE)).replace('\\','/'),url=url,checked_on='2026-10-14',status='manufacturer_CAD_unchanged',archive_entry=n,modified=False,bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
            old[a['file']]=a;print('STEP preserved',len(data),'bytes',flush=True)
    d['assets']=list(old.values());manifest.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
