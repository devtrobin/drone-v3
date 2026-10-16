"""Archive public, observed product images and original reference PDFs.

Amazon observation below is a curated transcription from the visible product
page, not a raw account/browser dump. No private delivery address is stored.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request, json, hashlib, sys

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'Composants/fixations-raspberry-pi-5'
URL = 'https://www.amazon.fr/dp/B0DCS5C7SN'
ITEMS = [
 ('photos/Ewwtrey-kit-original.jpg','https://m.media-amazon.com/images/I/813e8a4aQJL._SL1500_.jpg','Amazon : photo du kit et étiquette'),
 ('photos/Ewwtrey-longueurs-original.jpg','https://m.media-amazon.com/images/I/61+JroRRcWL._SL1500_.jpg','Amazon : illustration des longueurs et quantités'),
 ('photos/Ewwtrey-pieces-original.jpg','https://m.media-amazon.com/images/I/81rvYkQkITL._SL1500_.jpg','Amazon : pièces et publicité matière'),
 ('photos/Ewwtrey-details-original.jpg','https://m.media-amazon.com/images/I/71f-laBg2eL._SL1500_.jpg','Amazon : détails des formes, photo commerciale'),
 ('notices/RaspberryPi-5-plan-mecanique-original.pdf','https://datasheets.raspberrypi.com/rpi5/raspberry-pi-5-mechanical-drawing.pdf','Raspberry Pi Ltd : plan mécanique de référence, non destiné à la production'),
 ('notices/Essentra-filetages-plastiques-reference-original.pdf','https://essentracomponents.bynder.com/m/6e2e9b888468b393/original/2685970-pdf.pdf','Essentra : autre fabricant, exemple de filetages métriques ; ne cote pas le kit Ewwtrey'),
]

def fetch(item):
 rel,url,desc=item;p=BASE/rel;p.parent.mkdir(parents=True,exist_ok=True)
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=35) as response:
   data=response.read();mime=response.headers.get('Content-Type','');final=response.geturl()
  if not data: raise ValueError('empty response')
  if p.suffix=='.pdf' and not data.startswith(b'%PDF'): raise ValueError('not a PDF')
  if p.suffix=='.jpg' and not data.startswith(b'\xff\xd8'): raise ValueError('not a JPEG')
  p.write_bytes(data)
  return dict(file=rel,url=url,final_url=final,description=desc,status='downloaded',bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),mime=mime,original_unchanged=True)
 except Exception as e:
  return dict(file=None,requested_file=rel,url=url,description=desc,status='unavailable',error=str(e))

def main():
 sys.stdout.reconfigure(encoding='utf-8');BASE.mkdir(parents=True,exist_ok=True)
 with ThreadPoolExecutor(max_workers=6) as pool:assets=list(pool.map(fetch,ITEMS))
 (BASE/'assets.json').write_text(json.dumps(dict(checked_on='2026-10-14',assets=assets),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 obs=dict(observed_on='2026-10-14',source_url=URL,method='Chrome, page publique affichée, variante Noir M2.5 sélectionnée',
  brand='Ewwtrey',manufacturer='DJJRX',manufacturer_part='260018',asin='B0DCS5C7SN',variant='Noir M2.5',
  material_advertised='Nylon ; grade et renforcement non publiés',quantity_advertised=335,
  price_eur_vat_included=9.98,stock_display='En stock',seller='QianHaiDian',fulfilled_by='Amazon',
  shipping_display='Livraison gratuite dans la session Prime consultée ; autres sessions à revalider',
  delivery_display='15 octobre 2026, prévision affichée le 14 octobre ; non garantie',
  item_dimensions_cm=[17,9.7,1.8],item_weight_g=90,
  dimensions_scope='Dimensions du lot/boîte et masse de l’article ; pas des pièces individuelles, aucun poids embarqué déduit',
  rating=4.6,global_ratings=871,rating_scope='Famille multivariantes M2.5 / M3 / M4 et couleurs ; pas uniquement ce kit noir',
  purchase_made=False,cart_modified=False,
  uncertainties=['Aucune notice PDF ni CAO native propre au kit trouvée','Pas, tolérances, profondeur de taraudage, couple et températures admissibles non publiés',
    'Les images haute définition confirment des corps MF et FF hexagonaux ; surplats réel à mesurer'],
  reviews=[
   dict(author='Gallimard',date='2026-09-27',variant='Noir M2.5',stars=5,verified_purchase_display=True,summary='Retour bref : utile pour son projet, sans mesures ni type de Pi indiqué.',url='https://www.amazon.fr/portal/customer-reviews/srp/-/RVVUFD9D8AD8U/'),
   dict(author='RL',date='2026-05-24',variant='Noir M2.5',stars=5,verified_purchase_display=True,summary='Rapporte une utilisation pour empiler des circuits au laboratoire et un vissage précis ; aucun contrôle dimensionnel publié.',url='https://www.amazon.fr/portal/customer-reviews/srp/-/R2ETNH017T6C07/'),
   dict(author='Ronny Grawitz',date='2026-09-26',variant='Noir M2.5',stars=5,verified_purchase_display=True,summary='Apprécie les différentes hauteurs et la fixation surélevée de cartes. Aucune qualification sous vibrations ni dans ce robot.',url=URL),
   dict(author='decaidronaftalene',date='2024-12-22',variant='Blanc M2.5 : autre couleur',stars=5,verified_purchase_display=True,summary='Décrit un montage DAC avec Raspberry Pi et Volumio ; apprécie assortiment et vissage. Variante blanche, modèle du Pi inconnu.',url='https://www.amazon.fr/portal/customer-reviews/B0DCS45XHS/')])
 (BASE/'observation-amazon.json').write_text(json.dumps(obs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 for a in assets: print(a['status'],a.get('file') or a['requested_file'],a.get('bytes',0),flush=True)

if __name__=='__main__':main()
