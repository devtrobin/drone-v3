"""Archive public MiniBus documents unchanged; no shopping or form submission."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,json,hashlib,sys,re,html
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/distribution-alimentation'
TASKS=[
 ('sources-web/BlueSea-2315.html','https://www.bluesea.com/products/2315/Common_100A_Mini_BusBar_-_4_Gang_with_Cover'),
 ('sources-web/BlueSea-2305.html','https://www.bluesea.com/products/2305/Common_100A_Mini_BusBar_-_4_Gang'),
 ('sources-web/BlueSea-2713.html','https://www.bluesea.com/products/2713/MiniBus_BusBar_Cover_for_PN_2304_and_2305'),
 ('sources-web/BlueSea-rating.html','https://www.bluesea.com/support/articles/506/How_a_BusBar_Should_be_Rated'),
 ('sources-web/BlueSea-installation.html','https://www.bluesea.com/support/articles/497/Application_Steps_Which_Improve_Busbar_Performance'),
 ('sources-web/Amazon-FR-B000OTJ8A0.html','https://www.amazon.fr/dp/B000OTJ8A0'),
 ('sources-web/Amazon-US-B000OTJ8A0.html','https://www.amazon.com/dp/B000OTJ8A0'),
 ('sources-web/HodgesMarine-2315.html','https://www.hodgesmarine.com/blu2315-blue-sea-2315-minibus-100-ampere-common-busbar-4-x.html'),
 ('sources-web/Desertcart-2315.html','https://www.desertcart.in/products/6640266-blue-sea-systems-2315-100-amp-mini-busbar-with-4'),
 ('sources-web/forum-R3Owners.html','https://www.r3owners.net/threads/tidy-up-your-battery-terminals.44398/page-2'),
 ('notices/BlueSea-2315-plan-original.jpg','https://d2pyqm2yd3fw2i.cloudfront.net/files/resources/dimensioned_drawing/2315.jpg'),
 ('notices/BlueSea-2305-plan-original.jpg','https://d2pyqm2yd3fw2i.cloudfront.net/files/resources/dimensioned_drawing/2305.jpg'),
 ('photos/BlueSea-2315-miniature-originale.png','https://dh778tpvmt77t.cloudfront.net/images/products/180px_thumbnails/2315.png'),
 ('photos/Amazon-2315-vue-originale.jpg','https://m.media-amazon.com/images/I/51pMZgmXn8L._AC_SL1000_.jpg'),
 ('photos/Amazon-2315-seconde-vue-originale.jpg','https://m.media-amazon.com/images/I/21ZlOFyEezL._AC_.jpg'),
 ('notices/BlueSea-certificat-IMCI-BusBars.pdf','https://d2pyqm2yd3fw2i.cloudfront.net/files/resources/ce_certificate/IMCI_BusBars.pdf'),
 ('notices/BlueSea-declaration-BusBars.pdf','https://d2pyqm2yd3fw2i.cloudfront.net/files/resources/declaration_of_conformity/BusBars.pdf'),
 ('notices/BlueSea-catalogue-2024-miroir-PrimeMarine.pdf','https://primemarine.com.pl/pli/141_Katalog%20BlueSea.pdf'),
]
def fetch(task):
    filename,url=task;p=BASE/filename;p.parent.mkdir(parents=True,exist_ok=True)
    record=dict(file=filename,url=url,checked_on='2026-10-14',modified=False)
    try:
        if p.exists():
            data=p.read_bytes();final=url
            if (BASE/'assets.json').exists():
                old=next((a for a in json.loads((BASE/'assets.json').read_text(encoding='utf-8'))['assets'] if a['file']==filename),None)
                if old and old.get('sha256')==hashlib.sha256(data).hexdigest():return old
        else:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=22) as r:
                data=r.read();final=r.geturl()
            if filename.endswith('.pdf'):assert data.startswith(b'%PDF'),'not a PDF'
            if filename.endswith('.dxf'):assert b'SECTION' in data[:500],'not a DXF'
            p.write_bytes(data)
        record.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),final_url=final,
            status='challenge_html' if b'bm-verify' in data or b'validateCaptcha' in data else 'downloaded')
    except Exception as exc:record.update(status='unavailable',error=str(exc))
    return record
def main():
    sys.stdout.reconfigure(encoding='utf-8');BASE.mkdir(parents=True,exist_ok=True)
    with ThreadPoolExecutor(max_workers=5) as pool:records=list(pool.map(fetch,TASKS))
    old=json.loads((BASE/'assets.json').read_text(encoding='utf-8'))['assets'] if (BASE/'assets.json').exists() else []
    indexed={a['file']:a for a in old};indexed.update({a['file']:a for a in records})
    (BASE/'assets.json').write_text(json.dumps(dict(checked_on='2026-10-14',assets=list(indexed.values())),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for a in records:print(a['file'],a.get('bytes',a.get('error')),flush=True)
    for filename in ['BlueSea-2315.html','BlueSea-2305.html','BlueSea-2713.html']:
        p=BASE/'sources-web'/filename
        if p.exists():
            urls=set(html.unescape(u) for u in re.findall(r'(?:href|src|content)=[\"\x27]([^\"\x27]+)',p.read_text(encoding='utf-8')))
            print(filename,'LINKS',[u for u in sorted(urls) if any(k in u for k in ['.dxf','.pdf','2315.','2305.','2713.','hi_res'])],flush=True)
if __name__=='__main__':main()
