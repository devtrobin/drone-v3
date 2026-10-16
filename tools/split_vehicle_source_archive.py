"""Preserve original exports in two ZIPs, each below GitHub's file limit."""
from pathlib import Path
import zipfile,hashlib,json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'Assemblage';BUILD=OUT/'preparation'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    source=OUT/'sources-step-detaillees-originales.zip'
    with zipfile.ZipFile(source) as original:
        manifest=json.loads(original.read('provenance.json'))
        all_names=original.namelist()
        full=[n for n in all_names if n=='drone-v3-complet-detaille.step']
        if not full:return
        rows=[]
        for filename,names in [('sources-step-detaillees-originales.zip',[n for n in all_names if n not in full]),('sources-step-complet-original.zip',full)]:
            path=BUILD/filename
            with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as target:
                for name in names:
                    data=original.read(name)
                    if name.endswith('.step'):
                        expected=next(r for r in manifest['models'] if r['file']==name)
                        assert hashlib.sha256(data).hexdigest()==expected['sha256']
                    target.writestr(name,data)
            with zipfile.ZipFile(path) as z:assert z.testzip() is None
            assert path.stat().st_size<100*1024*1024
            rows.append(dict(file=filename,bytes=path.stat().st_size,sha256=sha(path),members=names))
    (BUILD/'archives.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
    print('ARCHIVES',[(r['file'],r['bytes']) for r in rows])
if __name__=='__main__':main()
