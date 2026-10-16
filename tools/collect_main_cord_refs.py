"""Public manufacturer evidence; no login, purchases or private form submissions."""
from pathlib import Path
import sys,json,urllib.request,re,html,hashlib,concurrent.futures,zipfile,io,shutil
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/cordon-principal-batterie'
TE='https://www.te.com/en/product-130191.html'
BN='https://bntechgo.com/bntechgo-12-gauge-silicone-wire-kit-ultra-flexible-20-ft-black-and-red-each-color-10-ft-high-temp-200-c-600v-12-awg-silicone-wire-680-strands-of-tinned-copper-wire-stranded-wire-stranded-wire-for-model-battery/'
DRAW='https://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocFormat=pdf&DocLang=English&DocNm=130191&DocType=Customer+Drawing&PartCntxt=130191'
QRG='https://www.te.com/content/dam/te-com/documents/appliances/global/solistrand-terminals-and-splices-qrg.pdf'
TOOL='https://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocFormat=pdf&DocLang=English&DocNm=408-1216&DocType=Specification+Or+Standard&PartCntxt=49935'
def fetch(url):
 req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
 with urllib.request.urlopen(req,timeout=35) as r:return r.read(),r.geturl(),r.headers.get('Content-Type','')
def main():
 sys.stdout.reconfigure(encoding='utf-8');(BASE/'notices').mkdir(parents=True,exist_ok=True);(BASE/'references').mkdir(exist_ok=True)
 sources=[('te-drawing',DRAW,'notices/TE-130191-plan-A3-original.pdf'),('te-qrg',QRG,'notices/TE-SOLISTRAND-guide-original.pdf'),('te-tool',TOOL,'notices/TE-49935-notice-408-1216-original.pdf'),('te-product',TE,'references/TE-130191-page.html'),('bn-product',BN,'references/BNTECHGO-12awg-page.html'),('amazon-wire','https://www.amazon.fr/dp/B01ABOPMEI','references/Amazon-FR-B01ABOPMEI.html'),('amazon-plug','https://www.amazon.fr/dp/B074PN6N4K','references/Amazon-FR-B074PN6N4K.html'),('digikey-lug','https://www.digikey.fr/fr/products/detail/te-connectivity-amp-connectors/130191/1864623','references/DigiKey-130191-page.html')]
 assets=[]
 def get(item):
  ident,url,rel=item;entry=dict(id=ident,url=url,checked_on='2026-10-15')
  try:
   data,final,mime=fetch(url)
   if not data:raise ValueError('Empty HTTP response')
   if rel.endswith('.pdf') and not data.startswith(b'%PDF'):raise ValueError('Response is not PDF')
   p=BASE/rel;p.write_bytes(data);entry.update(local=rel,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),final_url=final,mime=mime,status='downloaded_original')
  except Exception as e:entry.update(status='not_downloaded',error=str(e))
  return entry
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
  for a in ex.map(get,sources):assets.append(a);print(a['id'],a['status'],a.get('bytes',a.get('error')),flush=True)
 # Manufacturer native CAD URL is read from the product page, never guessed.
 p=BASE/'references/TE-130191-page.html'
 if p.exists():
  s=html.unescape(p.read_text(encoding='utf-8',errors='replace'))
  urls=re.findall(r'(?:href|url)=["\']([^"\']+)["\']',s)
  candidates=[u for u in urls if '3d_stp' in u and '130191' in u]
  if not candidates:
   candidates=re.findall(r'https[^"<>\s]+(?:3d_stp)[^"<>\s]*',s)
  for u in candidates[:1]:
   if u.startswith('/'):u='https://www.te.com'+u
   a=get(('te-native-cad',u,'references/TE-130191-native-step.zip'));assets.append(a);print(a,flush=True)
   if a['status']=='downloaded_original':
    try:
     z=zipfile.ZipFile(BASE/a['local']);names=[n for n in z.namelist() if n.lower().endswith(('.stp','.step'))]
     for n in names:
      dest=BASE/'references/TE-130191-native-original.step';dest.write_bytes(z.read(n));assets.append(dict(id='te-native-extracted',archive=a['local'],archive_member=n,local=str(dest.relative_to(BASE)),bytes=dest.stat().st_size,sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),status='extracted_unchanged'))
    except Exception as e:print('native CAD unavailable',e)
 # Keep exact copies of already archived shared evidence, with origin paths.
 for origin,rel in [('connecteurs-alimentation/notices/AMASS-catalogue-XT-2026-original.pdf','notices/AMASS-catalogue-XT-2026-original.pdf'),('connecteurs-alimentation/notices/AMASS-XT60H-F-M-V1.2-via-Shoptronica.pdf','notices/AMASS-XT60H-V1.2-original.pdf')]:
  src=ROOT/'Composants'/origin
  if src.exists():
   dest=BASE/rel;shutil.copyfile(src,dest);assets.append(dict(id=Path(rel).stem,local=rel,copied_from='../'+origin,sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),bytes=dest.stat().st_size,status='copied_original_unchanged'))
 (BASE/'assets.json').write_text(json.dumps(dict(checked_on='2026-10-15',assets=assets),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 if p.exists():
  for m in re.finditer(r'.{0,80}3d_stp.{0,280}',p.read_text(encoding='utf-8',errors='replace')):print('CAD_LINK',m.group(0))
if __name__=='__main__':main()
