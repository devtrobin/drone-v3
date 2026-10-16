from collect_gpio_refs import fetch,BASE,ROOT
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,sys,pymupdf,zipfile
TASKS=[
 ('notices/Molex-sertissage-notice-actuelle-revE.pdf','https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/applicationtoolingspecificationpdf/638/63811/ATS-638118700-001.pdf'),
]
sys.stdout.reconfigure(encoding='utf-8')
with ThreadPoolExecutor(max_workers=4) as pool:r=list(pool.map(fetch,TASKS))
p=BASE/'assets.json';d=json.loads(p.read_text(encoding='utf-8'));d['assets']=[a for a in d['assets'] if a['file'] not in {x['file'] for x in r}]+r
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
tmp=ROOT/'tools/temp/gpio-review/sources';tmp.mkdir(parents=True,exist_ok=True)
for a in r:
 print(a['file'],a['status'],a.get('bytes',a.get('error')),flush=True)
 if a['status']!='downloaded':continue
 if a['file'].endswith('.pdf'):
  doc=pymupdf.open(BASE/a['file'])
  for i,page in enumerate(doc):
   print('PAGE',i+1,page.get_text()[:2400].replace('\n',' | '),flush=True)
   page.get_pixmap(matrix=pymupdf.Matrix(1.6,1.6)).save(tmp/(Path(a['file']).stem+f'-{i+1}.png'))
 if a['file'].endswith('.zip'):
  with zipfile.ZipFile(BASE/a['file']) as z:print('CAD_MEMBERS',z.namelist(),flush=True)
