from pathlib import Path
import json,re,html,sys,pymupdf
from collect_final_components_refs import BASE,ROOT,get
def clean(s):return ' '.join(html.unescape(re.sub('<[^>]+>',' ',s)).split())
def main():
 sys.stdout.reconfigure(encoding='utf-8')
 for folder,name,url,ext in [
 ('connecteurs-commande','Opencircuit-1925','https://opencircuit.fr/produit/jr-connector-pack-male','html'),
 ('coupure-manuelle','PartsGo-ED80-1','https://www.partsandgo.fr/fr/arrets-d-urgence/52668-arret-d-urgence.html','html'),
 ('liaisons-alimentation-surveillance','WAGO-221-415-public','https://m.media-amazon.com/images/I/B1tUMAUMH7L.pdf','pdf'),
 ('liaisons-alimentation-surveillance','WAGO-221-413-public','https://m.media-amazon.com/images/I/91VkNZV%2BTHL.pdf','pdf')]:
  _,e=get((folder,name,url,ext));p=BASE/folder/'sources.json';a=json.loads(p.read_text(encoding='utf-8'));a['sources'].append(e);p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(e,flush=True)
  if e['status']!='archived':continue
  src=BASE/folder/e['file']
  if ext=='pdf':
   d=pymupdf.open(src)
   for i in range(min(4,len(d))):
    if i in [0,1,3]:d[i].get_pixmap(matrix=pymupdf.Matrix(2,2)).save(ROOT/'tools/temp/final-components'/(name+f'-p{i+1}.png'))
   print('PDFTEXT',name,' '.join(d[i].get_text() for i in range(min(4,len(d))))[:4000])
  elif name=='PartsGo-ED80-1':
   txt=src.read_text(encoding='utf-8');
   for pattern in [r'<h1.*?</h1>',r'<div class="product-prices".*?</div>',r'<div id="product-description-short.*?</div>',r'<div class="product-availability".*?</div>']:
    print(name,[clean(x) for x in re.findall(pattern,txt,re.S)])
   print('META',[(k,v) for k,v in re.findall(r'<meta[^>]+(?:itemprop|property)="([^"]+)"[^>]+content="([^"]+)"',txt) if k in ['price','availability','og:image','priceCurrency']])
  else:
   txt=src.read_text(encoding='utf-8');plain=clean(txt)
   for k in ['Excl.','Rupture','stock','livraison']: 
    i=plain.find(k);print(name,k,plain[max(0,i-80):i+200])
if __name__=='__main__':main()
