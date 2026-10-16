from pathlib import Path
import urllib.request,re,html,json,sys,hashlib
import pymupdf
from concurrent.futures import ThreadPoolExecutor
from collect_final_components_refs import ROOT,BASE,get
def text(s):return html.unescape(re.sub('<[^>]+>',' ',s)).strip()
def main():
 sys.stdout.reconfigure(encoding='utf-8')
 assets=[
 ('connecteurs-commande','photos/JR-boitier-cotes.jpg','https://a.pololu-files.com/picture/0J9699.1200.jpg'),
 ('connecteurs-commande','photos/JR-capot-cotes.jpg','https://a.pololu-files.com/picture/0J9700.1200.jpg'),
 ('connecteurs-commande','photos/JR-assemble.jpg','https://a.pololu-files.com/picture/0J3444.1200.jpg'),
 ('maintien-batterie','photos/GEPRC-jaune-bleu.jpg','https://geprc.com/wp-content/uploads/2022/05/6.jpg'),
 ('maintien-batterie','photos/GEPRC-detail.jpg','https://geprc.com/wp-content/uploads/2022/05/5-1.jpg'),
 ('coupure-manuelle','photos/Albright-ED80.jpg','https://www.albrightinternational.com/wpcms/wp-content/uploads/2016/07/ED80.jpg')]
 def image(a):
  folder,rel,url=a;p=BASE/folder/rel;p.parent.mkdir(parents=True,exist_ok=True)
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=25) as r:data=r.read()
   if not data.startswith(b'\xff\xd8'):raise ValueError('not jpeg')
   p.write_bytes(data);return folder,dict(url=url,file=rel,sha256=hashlib.sha256(data).hexdigest(),status='archived',original_unmodified=True)
  except Exception as e:return folder,dict(url=url,status='unavailable',error=str(e))
 with ThreadPoolExecutor(max_workers=6) as ex:
  for folder,e in ex.map(image,assets):
   src=BASE/folder/'sources.json';a=json.loads(src.read_text(encoding='utf-8'));a['sources'].append(e);src.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(folder,e,flush=True)
 for a in [
  ('liaisons-alimentation-surveillance','JST-XH-catalogue-public','https://www.jst-mfg.com/product/pdf/eng/eXH.pdf','pdf'),
  ('liaisons-alimentation-surveillance','WAGO-221-notice','https://www.wiska.com/files/2/document_7a8d1577378a637c2bc1b426459d7abf.pdf','pdf'),
  ('coupure-manuelle','PartsGo-ED80-liste','https://www.partsandgo.fr/fr/s/4/pieces-detachees-nacelles?order=product.price.asc&page=3','html'),
 ]:
  folder,e=get(a);src=BASE/folder/'sources.json';v=json.loads(src.read_text(encoding='utf-8'));v['sources'].append(e);src.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(e,flush=True)
 s=(BASE/'maintien-batterie/sources/BENECREAT-Amazon-original.html').read_text(encoding='utf-8')
 for key in ['productTitle','availability','priceToPay','corePriceDisplay','feature-bullets','landingImage']:
  hit=re.search(r'.{0,40}(?:id|class)=[\"\'][^\"\']*'+key+r'[^\"\']*[\"\'].{0,2200}',s,re.S)
  if hit:print('AMAZON',key,text(hit[0])[:1300],flush=True)
 print('AMAZONIMAGES',re.findall(r'"hiRes"\s*:\s*"([^"]+)"',s)[:7],flush=True)
 for folder,rel,pages in [('coupure-manuelle','Albright-ED80-fiche-original.pdf',[0]),('liaisons-alimentation-surveillance','JST-XH-catalogue-public-original.pdf',[2,3,4]),('liaisons-alimentation-surveillance','WAGO-221-notice-original.pdf',[0,3])]:
  p=BASE/folder/'notices'/rel
  if not p.exists():continue
  d=pymupdf.open(p)
  for i in pages:
   if i>=len(d):continue
   out=ROOT/'tools/temp/final-components'/(p.stem+f'-p{i+1}.png');d[i].get_pixmap(matrix=pymupdf.Matrix(2,2)).save(out)
  print('PDF',rel,len(d));print('\n'.join(d[i].get_text()[:5000] for i in pages if i<len(d)))
if __name__=='__main__':main()
