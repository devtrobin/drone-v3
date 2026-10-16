"""Collect unchanged primary technical references for the running gear."""
from pathlib import Path
import urllib.request,hashlib,json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'Composants/direction-et-transmission/notices'
DOCS=[
 ('FEETECH-FT90M-fiche-historique-miroir.pdf','https://www.gotronic.fr/pj2-ft90m-2907.pdf'),
 ('Tamiya-TT01R-notice-constructeur.pdf','https://www.tamiya.com/cms/english/rc/rcmanual/tt01r.pdf'),
 ('Tamiya-TT01-notice-constructeur.pdf','https://www.tamiya.com/cms/english/rc/rcmanual/tt01.pdf'),
 ('KHK-engrenages-acier-SS.pdf','https://khkgears.net/pdf/ss.pdf'),
 ('KHK-guide-technique-engrenages.pdf','https://khkgears.net/pdf/spur-tech.pdf'),
 ('SMB-MR115ZZ-fiche-technique.pdf','https://www.smbbearings.com/firebrick/ckeditor/plugins/upload/Uploads/Documents/bearingpdfs/MR115ZZ-miniature-bearing-5x11x4mm.pdf'),
]

def main():
 OUT.mkdir(parents=True,exist_ok=True);manifest=[]
 for filename,url in DOCS:
  path=OUT/filename
  try:
   if not path.exists():
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=60) as r:data=r.read()
    assert data.startswith(b'%PDF'),filename
    path.write_bytes(data)
   manifest.append({'file':filename,'url':url,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'modified':False})
   print(filename,path.stat().st_size,flush=True)
  except Exception as e:
   print('ERROR',filename,str(e),flush=True)
   manifest.append({'file':filename,'url':url,'download_error':str(e)})
 register=OUT/'assets.json'
 old=json.loads(register.read_text(encoding='utf-8')) if register.exists() else {}
 errors=old.get('unavailable_primary_documents',[])
 for entry in old.get('documents',[]):
  if 'download_error' in entry and entry not in errors:errors.append(entry)
 register.write_text(json.dumps({'collected_on':'2026-10-13','documents':manifest,'unavailable_primary_documents':errors},indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
