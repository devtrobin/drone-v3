from collect_final_components_refs import ROOT,BASE,get
from pathlib import Path
import json,urllib.request,sys,re,html,pymupdf
BN='https://bntechgo.com/bntechgo-18-gauge-silicone-wire-kit-ultra-flexible-20-ft-black-and-red-each-color-10-ft-high-temp-200-c-600v-18-awg-silicone-wire-150-strands-of-tinned-copper-wire-stranded-wire-stranded-wire-for-model-battery/'
def main():
 sys.stdout.reconfigure(encoding='utf-8')
 entries=[('liaisons-alimentation-surveillance','BNTECHGO-18AWG',BN,'html'),
  ('liaisons-alimentation-surveillance','WAGO-413-FR','https://www.gotronic.fr/pj2-fiche-technique-wg413-3763.pdf','pdf'),
  ('liaisons-alimentation-surveillance','JST-rallonge-Intermodel','https://www.intermodel.fr/cordons-et-prises-de-charge/548-rallonge-pour-prise-equilibrage-2s-intermodel-rallonge-2s-rallonge-prise-equilibrage-2s.html','html'),
  ('coupure-manuelle','Klauke-95R6','https://www.buerklin.com/en/p/klauke/cable-lugs/95r6/07F2055/','html')]
 for a in entries:
  folder,e=get(a);p=BASE/folder/'sources.json';v=json.loads(p.read_text(encoding='utf-8'));v['sources'].append(e);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(e,flush=True)
  if e['status']=='archived' and a[1]=='BNTECHGO-18AWG':
   txt=(BASE/folder/e['file']).read_text(encoding='utf-8')
   for n in re.findall(r'<img[^>]+>',txt):
    if 'sw-18-3' in n:print('BNIMAGE',n[:1500])
  if e['status']=='archived' and a[3]=='pdf':
   d=pymupdf.open(BASE/folder/e['file']);d[1].get_pixmap(matrix=pymupdf.Matrix(2,2)).save(ROOT/'tools/temp/final-components/WAGO-413-FR-p2.png');print('413DIMS',' '.join(d[i].get_text() for i in range(min(4,len(d)))))[-1000:] if False else None
 assets=[('maintien-batterie','photos/BENECREAT-feuilles.jpg','https://m.media-amazon.com/images/I/51Dsi5gU-WL._AC_SL1500_.jpg'),
 ('maintien-batterie','photos/BENECREAT-cotes.jpg','https://m.media-amazon.com/images/I/51-g3Ym4j+L._AC_SL1500_.jpg'),
 ('coupure-manuelle','photos/ED80-1-achat.jpg','https://www.partsandgo.fr/84161-large_default/arret-d-urgence.jpg')]
 for folder,rel,url in assets:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=30) as r:data=r.read()
  dst=BASE/folder/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(data)
  import hashlib
  p=BASE/folder/'sources.json';v=json.loads(p.read_text(encoding='utf-8'));v['sources'].append(dict(url=url,file=rel,status='archived',sha256=hashlib.sha256(data).hexdigest(),original_unmodified=True));p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 for folder in ['connecteurs-commande','liaisons-alimentation-surveillance']:
  p=BASE/folder/'sources.json';v=json.loads(p.read_text(encoding='utf-8'))
  for e in v['sources']:
   if e.get('status')=='archived' and e.get('bytes')==0:e['status']='unavailable';e['error']='Empty response';(BASE/folder/e['file']).unlink(missing_ok=True);e.pop('file',None)
  p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 d=pymupdf.open(BASE/'faisceau-puissance/notices/Klauke-catalogue-via-PowerCables.pdf')
 d[13].get_pixmap(matrix=pymupdf.Matrix(2,2)).save(ROOT/'tools/temp/final-components/Klauke-p14.png')
 print('KLAUKE',d[13].get_text()[:4500])
if __name__=='__main__':main()
