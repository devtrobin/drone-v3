from collect_final_components_refs import BASE,get
import json,sys,urllib.request,hashlib
def main():
 sys.stdout.reconfigure(encoding='utf-8')
 folder,e=get(('liaisons-alimentation-surveillance','GoTronic-WAGO-achat','https://www.gotronic.fr/cat-bornes-de-connexion-wago-0-5-a-2-5-mm2.htm','html'))
 p=BASE/folder/'sources.json';v=json.loads(p.read_text(encoding='utf-8'));v['sources'].append(e)
 rel='photos/BNTECHGO-18AWG-construction.jpg';url='https://cdn11.bigcommerce.com/s-clng77kigt/images/stencil/1280x1280/products/846/17494/18_Awg__41727.1576570492.jpg?c=2'
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as r:data=r.read()
 dst=BASE/folder/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(data);v['sources'].append(dict(url=url,file=rel,status='archived',sha256=hashlib.sha256(data).hexdigest(),original_unmodified=True))
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(e)
 # Curated public offer record; no account/browser delivery information.
 p=BASE/'maintien-batterie/observation-amazon.json'
 obs=dict(observed_on='2026-10-14',source_url='https://www.amazon.fr/dp/B08KFTBDF2',method='Public unauthenticated HTML fetched directly',
  brand='BENECREAT',asin='B08KFTBDF2',title='2 pièces plaque de silicone blanc200x200x2mm',variant='Blanc,2mm,200x200mm',
  price_eur_vat_included=11.99,stock_display='En stock',seller='BENECREAT FR BOUTIQUE',fulfilled_by='Amazon',shipping_FR_confirmed=False,
  purchase_made=False,cart_modified=False,Shore_hardness=None,friction_coefficient=None,hardware_tested=False)
 p.write_text(json.dumps(obs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
