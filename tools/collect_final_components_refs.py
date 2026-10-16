"""Public component references; never submits forms or places an order."""
from pathlib import Path
import urllib.request,json,hashlib,sys,re,html
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants'
SOURCES=[
 ('connecteurs-commande','Pololu-1925','https://www.pololu.com/product/1925','html'),
 ('connecteurs-commande','Pololu-1925-images','https://www.pololu.com/product/1925/pictures','html'),
 ('connecteurs-commande','Amazon-JR-recherche','https://www.amazon.fr/s?k=connecteur+servo+JR+sertir','html'),
 ('liaisons-alimentation-surveillance','JST-XH-catalogue','https://order.jst-mfg.com/InternetShop/app/pdf_show.php?kbn=1&key=eXH.pdf','pdf'),
 ('liaisons-alimentation-surveillance','JST-XH-famille','https://www.jst-mfg.com/product/index.php?series=277','html'),
 ('liaisons-alimentation-surveillance','WAGO-221-413','https://www.mouser.com/datasheet/2/737/Data_Sheet221_413_-1928674.pdf','pdf'),
 ('liaisons-alimentation-surveillance','WAGO-221-415','https://www.mouser.com/datasheet/2/737/Data_Sheet221_415_-1928675.pdf','pdf'),
 ('liaisons-alimentation-surveillance','DigiKey-221-415','https://www.digikey.fr/fr/products/detail/wago-corporation/221-415/13549457','html'),
 ('liaisons-alimentation-surveillance','Amazon-WAGO-recherche','https://www.amazon.fr/s?k=WAGO+221-413+221-415','html'),
 ('maintien-batterie','GEPRC-sangle','https://geprc.com/product/geprc-new-version-battery-strap5pcs/','html'),
 ('maintien-batterie','BENECREAT-Amazon','https://www.amazon.fr/dp/B08KFTBDF2','html'),
 ('maintien-batterie','Merefsa-silicone','https://www.merefsa.com/fr/produits/elastomere-de-silicone_kgr/plaques-et-feuilles-en-silicone-compact_pid18/articles/plaque-silicone-bleu-alimentaire-60-sh-5-400-mm-x-400-mm-x-2mm-0.3-epaisseur_id-PPLSBL60400020.html','html'),
 ('coupure-manuelle','Albright-ED80','https://www.albrightinternational.com/products/ed80-2/','html'),
 ('coupure-manuelle','Albright-ED80-fiche','https://www.albrightinternational.com/wpcms/wp-content/uploads/2024/10/ED80-Data-Sheet.pdf','pdf'),
 ('coupure-manuelle','PartsGo-ED80-recherche','https://www.partsandgo.fr/fr/arrets-d-urgence/52666-arret-d-urgence.html','html'),
 ('coupure-manuelle','BlueSea-6006-ecarte','https://www.bluesea.com/products/6006','html'),
]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def get(a):
 folder,name,url,ext=a;b=BASE/folder;b.mkdir(parents=True,exist_ok=True)
 dst=b/('notices' if ext=='pdf' else 'sources')/(name+'-original.'+ext);dst.parent.mkdir(parents=True,exist_ok=True)
 entry=dict(id=name,url=url,accessed='2026-10-14',original_unmodified=True)
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=35) as r:data=r.read()
  if not data:raise ValueError('Empty response')
  txt=data.decode('utf-8',errors='replace')
  if ext=='pdf' and not data.startswith(b'%PDF'):raise ValueError('Non-PDF response')
  if ext=='html' and any(k in txt.lower() for k in ['enter the characters you see below','validatecaptcha','robot check']):raise ValueError('Page unavailable: verification')
  dst.write_bytes(data);entry.update(file=dst.relative_to(b).as_posix(),sha256=sha(dst),bytes=len(data),status='archived')
  if ext=='html':
   (dst.with_suffix('.txt')).write_text(html.unescape(re.sub('<[^>]+>',' ',txt)),encoding='utf-8')
   if name in ['Pololu-1925-images','GEPRC-sangle','Albright-ED80','PartsGo-ED80-recherche','Merefsa-silicone']:
    links=[dict(href=html.unescape(a),text=html.unescape(re.sub('<[^>]+>','',b)).strip()) for a,b in re.findall(r'<a[^>]+href=[\"\']([^\"\']+)[\"\'][^>]*>(.*?)</a>',txt,re.S)]
    imgs=[{k:html.unescape(v) for k,v in re.findall(r'([\w-]+)=[\"\']([^\"\']*)[\"\']',tag)} for tag in re.findall(r'<img[^>]+>',txt)]
    tmp=ROOT/'tools/temp/final-components';tmp.mkdir(parents=True,exist_ok=True)
    (tmp/(name+'-links.json')).write_text(json.dumps(dict(links=links,images=imgs),ensure_ascii=False,indent=2),encoding='utf-8')
 except Exception as e:entry.update(status='unavailable',error=str(e))
 return folder,entry
def main():
 sys.stdout.reconfigure(encoding='utf-8');groups={}
 with ThreadPoolExecutor(max_workers=6) as pool:
  for folder,e in pool.map(get,SOURCES):groups.setdefault(folder,[]).append(e);print(e['id'],e['status'],e.get('bytes',e.get('error')),flush=True)
 for folder,entries in groups.items():
  (BASE/folder/'sources.json').write_text(json.dumps(dict(accessed='2026-10-14',sources=entries),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
