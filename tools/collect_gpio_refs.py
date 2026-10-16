"""Archive connector, crimp, wire and Pi sources without modifying originals."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,urllib.parse,json,hashlib,re,sys
import pymupdf
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/connecteur-gpio'
TASKS=[
 ('sources-web/Molex-boitier.html','https://www.molex.com/en-us/products/part-detail/0022552401'),
 ('sources-web/Molex-contact.html','https://www.molex.com/en-us/products/part-detail/0016020103'),
 ('sources-web/Adafruit-fil-3175.html','https://www.adafruit.com/product/3175'),
 ('sources-web/DigiKey-boitier.html','https://www.digikey.fr/fr/products/detail/molex/0022552401/171975'),
 ('sources-web/DigiKey-contact.html','https://www.digikey.fr/fr/products/detail/molex/0016020103/115063'),
 ('sources-web/Amazon-recherche-boitier.html','https://www.amazon.fr/s?k=Molex+22-55-2401'),
 ('sources-web/Amazon-recherche-contact.html','https://www.amazon.fr/s?k=Molex+16-02-0103'),
 ('sources-web/Amazon-recherche-fil.html','https://www.amazon.fr/s?k=Adafruit+3175'),
 ('notices/Molex-boitier-fiche-originale-2015.pdf','https://www.farnell.com/datasheets/1928032.pdf'),
 ('notices/Molex-contact-fiche-originale-2013.pdf','https://www.farnell.com/datasheets/1711811.pdf'),
 ('notices/Molex-boitier-plan-lien-source.pdf','https://www.molex.com/pdm_docs/sd/022552401_sd.pdf'),
 ('notices/Molex-SL-specification-lien-source.pdf','https://www.molex.com/pdm_docs/ps/PS-70058.pdf'),
 ('notices/Molex-boitier-plan-original.pdf','https://www.molex.com/pdm_docs/sd/704500026_sd.pdf'),
 ('notices/Molex-contact-plan-original.pdf','https://www.molex.com/pdm_docs/sd/700580002_sd.pdf'),
 ('notices/Molex-SL-specification-originale.pdf','https://www.molex.com/pdm_docs/ps/700580001_ps.pdf'),
 ('notices/Molex-sertissage-outil-original.pdf','https://www.molex.com/pdm_docs/ats/ATS-638118700.pdf'),
 ('sources-web/Pi-GPIO.html','https://www.raspberrypi.com/documentation/computers/raspberry-pi.html'),
]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fetch(item):
 name,url=item;p=BASE/name;p.parent.mkdir(parents=True,exist_ok=True)
 rec=dict(file=name,url=url,checked_on='2026-10-14',original_unmodified=True)
 try:
  if p.exists():b=p.read_bytes();final=url
  else:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=18) as r:b=r.read();final=r.geturl()
  if p.suffix=='.pdf':assert b.startswith(b'%PDF'),'Response is not PDF'
  p.write_bytes(b)
  rec.update(bytes=len(b),sha256=sha(p),final_url=final,status='downloaded' if b else 'empty_response')
  if any(t in b for t in [b'validateCaptcha',b'bm-verify',b'challenge-platform']):rec['status']='challenge_html'
 except Exception as e:rec.update(status='unavailable',error=str(e))
 return rec
def main():
 sys.stdout.reconfigure(encoding='utf-8');BASE.mkdir(parents=True,exist_ok=True)
 with ThreadPoolExecutor(max_workers=5) as pool:records=list(pool.map(fetch,TASKS))
 for rec in records:print(rec['file'],rec['status'],rec.get('bytes',rec.get('error')),flush=True)
 extra=[]
 # Follow only observed document URLs, so revisions are not inferred.
 for label in ['Molex-boitier','Molex-contact','DigiKey-boitier','DigiKey-contact']:
  p=BASE/('sources-web/'+label+'.html')
  if not p.exists():continue
  s=p.read_text(encoding='utf-8',errors='replace')
  matches=list(dict.fromkeys(re.findall(r'https?://[^\s"<>]+',s)))
  for u in matches:
   u=u.replace('&amp;','&')
   if any(t in u for t in ['pdm_docs/sd/','pdm_docs/ps/','pdm_docs/3d/','pdm_docs/ats/']):
    if u not in [r['url'] for r in records] and u.lower().endswith(('.pdf','.stp','.step','.zip')):
     extra.append(('notices/'+Path(urllib.parse.urlparse(u).path).name,u))
  print('OBSERVED',label,[(Path(urllib.parse.urlparse(u).path).name,u) for u in matches if 'pdm_docs/' in u][:12],flush=True)
 if extra:
  with ThreadPoolExecutor(max_workers=4) as pool:records+=list(pool.map(fetch,list(dict.fromkeys(extra))))
 (BASE/'assets.json').write_text(json.dumps(dict(checked_on='2026-10-14',assets=records),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 tmp=ROOT/'tools/temp/gpio-review/sources';tmp.mkdir(parents=True,exist_ok=True)
 for r in records:
  if r['status']=='downloaded' and r['file'].endswith('.pdf'):
   doc=pymupdf.open(BASE/r['file']);print('PDF',r['file'],len(doc),flush=True)
   for i,page in enumerate(doc):
    print('PAGE',i+1,page.get_text()[:2100].replace('\n',' | '),flush=True)
    if 'plan' in r['file']:page.get_pixmap(matrix=pymupdf.Matrix(1.6,1.6)).save(tmp/(Path(r['file']).stem+f'-{i+1}.png'))
if __name__=='__main__':main()
