"""Archive public manufacturer evidence for the supply correction. No purchase."""
from pathlib import Path
import sys, json, hashlib, urllib.request, concurrent.futures, re, html
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'Composants/verification-alimentation'
SOURCES = [
 ('jlln', 'https://www.littelfuse.com/assetdocs/jlln-datasheet?assetguid=3a7bc9bf-d932-4401-bdc7-b39f302195cf', 'notices/Littelfuse-JLLN-original-2025.pdf'),
 ('klkd', 'https://www.littelfuse.com/assetdocs/klkd-fuse-datasheet?assetguid=7b52eebb-c7cc-43df-a8da-9682a338e0f6', 'notices/Littelfuse-KLKD-original-2025.pdf'),
 ('lf-catalog', 'https://www.littelfuse.com/de/assetdocs/powr-gard-catalog?assetguid=85d36235-a32b-4608-bfed-f9878aa43af0', 'notices/Littelfuse-catalogue-original.pdf'),
 ('lf-csa', 'https://www.littelfuse.com/assetdocs/csa-6225-01-007316?assetguid=203ad805-7e22-463f-997a-2431bbdfbbd1', 'notices/Littelfuse-supports-certificat-CSA-original.pdf'),
 ('blue-table', 'https://catalog2015.bluesea.com/files/common/downloads/page0140.pdf', 'notices/Blue-Sea-table-ampacite-originale.pdf'),
 ('lapp-black', 'https://e.lapp.com/jp/p/temperature-resistant-cables/oelflex-heat-180-sif-1x6-bk-0054001', 'references/LAPP-0054001.html'),
 ('lapp-red', 'https://e.lapp.com/jp/p/temperature-resistant-cables/oelflex-heat-180-sif-1x6-rd-0054104', 'references/LAPP-0054104.html'),
 ('pololu-5571', 'https://www.pololu.com/product/5571', 'references/Pololu-5571.html'),
 ('charge-cable', 'https://www.rcteam.com/products/beez2b-charging-cable-xt60-to-ec5-beec1067', 'references/Beez2B-BEEC1067.html'),
 ('charge-stock', 'https://www.rcteam.com/products/beez2b-charging-cable-xt60-to-ec5-beec1067.js', 'references/Beez2B-BEEC1067-stock.json'),
 ('ic5-ec5', 'https://www.spektrumrc.com/product/connector-ic5-device-w-4-10awg-wires/SPMXCA510.html', 'references/Spektrum-IC5.html'),
]
def fetch(item):
 ident, url, rel = item
 entry = dict(id=ident, url=url, checked_on='2026-10-15', local=rel)
 try:
  req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req, timeout=30) as response:
   data=response.read(); final=response.geturl(); mime=response.headers.get('Content-Type','')
  if not data or (rel.endswith('.pdf') and not data.startswith(b'%PDF')):
   raise ValueError('Not the expected document')
  path=BASE/rel; path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(data)
  entry.update(status='archived_original',bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),final_url=final,mime=mime)
 except Exception as error:
  entry.update(status='not_archived',error=str(error)); entry.pop('local',None)
 return entry
def main():
 sys.stdout.reconfigure(encoding='utf-8'); BASE.mkdir(parents=True,exist_ok=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
  assets=list(executor.map(fetch,SOURCES))
 for entry in assets: print(entry['id'],entry['status'],entry.get('bytes',entry.get('error')),flush=True)
 stock=BASE/'references/Beez2B-BEEC1067-stock.json'
 if stock.exists():
  product=json.loads(stock.read_text(encoding='utf-8'))
  print('CHARGE_PRODUCT',json.dumps({k:product.get(k) for k in ['title','price','available','variants','images']},ensure_ascii=False),flush=True)
  for index,url in enumerate(product.get('images',[])[:2]):
   if url.startswith('//'):url='https:'+url
   assets.append(fetch((f'charge-photo-{index+1}',url,f'references/Beez2B-photo-{index+1}.jpg')))
 page=BASE/'references/Pololu-5571.html'
 if page.exists():
  content=html.unescape(page.read_text(encoding='utf-8',errors='replace'))
  for url in dict.fromkeys(re.findall(r'(?:src|href)=["\']([^"\']+)["\']',content)):
   if ('pololu-files' in url and ('dropout' in url.lower() or '.pdf' in url.lower() or '.step' in url.lower())):
    print('POLOLU_ASSET',url,flush=True)
 (BASE/'assets.json').write_text(json.dumps(dict(checked_on='2026-10-15',assets=assets),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__': main()
