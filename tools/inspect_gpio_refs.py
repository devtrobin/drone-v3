from pathlib import Path
import sys,json,re,pymupdf
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/connecteur-gpio'
sys.stdout.reconfigure(encoding='utf-8')
doc=pymupdf.open(BASE/'notices/Molex-boitier-fiche-originale-2015.pdf')
print('PDF_LINKS',[(a.get('uri'),a.get('from')) for p in doc for a in p.links() if 'uri' in a][:7])
for name in ['validation-versions-travail.json','provenance.json']:
 d=json.loads((ROOT/'Composants/raspberry-pi-5/3D'/name).read_text(encoding='utf-8'))
 print('PI_KEYS',name,list(d))
 if name.startswith('validation'):
  for item in d['kept']:
   bb=item['bounds_mm'];sz=[bb[1]-bb[0],bb[3]-bb[2],bb[5]-bb[4]]
   if max(sz)>45 or ('header' in item['name'].lower()):print('PI_MAIN',item['index'],item['name'],bb)
PY=''
