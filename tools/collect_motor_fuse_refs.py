"""Archive public sources and reuse unchanged reference documents already obtained."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,json,hashlib,sys
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/protection-branches-moteurs'
TASKS=[
 ('notices/Littelfuse-ATO-aftermarket-2022-fabricant.pdf','https://www.littelfuse.com/assetdocs/littelfuse-datasheet-ato?assetguid=bba6ed2a-96e5-4b07-ab5d-0e8d267c0bd1'),
 ('sources-web/BlueSea-5065.html','https://www.bluesea.com/products/5065'),
 ('sources-web/Hobbywing-WP16BL30-G2.html','https://www.hobbywing.com/en/products/quicrun-wp-16bl30-g2'),
 ('sources-web/Amazon-FR-5065.html','https://www.amazon.fr/dp/B004ZIUA62'),
 ('sources-web/Amazon-US-5065.html','https://www.amazon.com/dp/B004ZIUA62'),
 ('sources-web/Amazon-FR-ATO30BP-recherche.html','https://www.amazon.fr/s?k=Littelfuse+ATO30BP'),
 ('sources-web/DigiKey-0ATO030-V.html','https://www.digikey.com/en/products/detail/littelfuse-inc/0ATO030-V/2519124'),
 ('sources-web/CanadianTire-ATO30BP.html','https://www.canadiantire.ca/en/pdp/littelfuse-ato-blade-fuse-5-pk-0201571p.0201581.html'),
 ('sources-web/Forum-SailboatOwners-5065.html','https://forums.sailboatowners.com/threads/what-are-you-using-as-a-bilge-pump-fuse-holder.162517/'),
]
COPIES=[
 ('notices/Littelfuse-ATO-fiche-originale-via-RSP.pdf','Composants/protection-branche-pi/notices/Littelfuse-ATO-fiche-originale-via-RSP.pdf','https://rspsupply.com/images/downloads/Littelfuse/0/Littelfuse%200ATO020.VP/Specification%20Document.pdf'),
 ('notices/Littelfuse-catalogue-aftermarket-2013-via-RS.pdf','Composants/protection-branche-pi/notices/Littelfuse-catalogue-aftermarket-2013-via-RS.pdf','https://docs.rs-online.com/d38b/0900766b813f0619.pdf'),
 ('porte-fusible/photos/Amazon-5065-original.jpg','Composants/protection-branche-pi/porte-fusible/photos/Amazon-5065-original.jpg','https://m.media-amazon.com/images/I/51mfLfEM4UL._AC_SL1000_.jpg'),
]
def sha(data):return hashlib.sha256(data).hexdigest()
def fetch(task):
    name,url=task;p=BASE/name;p.parent.mkdir(parents=True,exist_ok=True)
    rec=dict(file=name,url=url,checked_on='2026-10-14',modified=False)
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as resp:data=resp.read();final=resp.geturl()
        if name.endswith('.pdf'):assert data.startswith(b'%PDF'),'response is not a PDF'
        p.write_bytes(data)
        status='downloaded'
        if not data:status='empty_response'
        elif any(s in data for s in [b'validateCaptcha',b'bm-verify',b'challenge-platform']):status='challenge_html'
        elif len(data)<5000 and ('Amazon' in name or 'BlueSea' in name):status='unusable_short_response'
        rec.update(status=status,bytes=len(data),sha256=sha(data),final_url=final)
    except Exception as e:rec.update(status='unavailable',error=str(e))
    return rec
def main():
    sys.stdout.reconfigure(encoding='utf-8');BASE.mkdir(parents=True,exist_ok=True)
    with ThreadPoolExecutor(max_workers=5) as pool:records=list(pool.map(fetch,TASKS))
    for name,origin,url in COPIES:
        data=(ROOT/origin).read_bytes();p=BASE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
        records.append(dict(file=name,url=url,checked_on='2026-10-14',status='unchanged_local_copy',origin=origin,modified=False,bytes=len(data),sha256=sha(data)))
    (BASE/'assets.json').write_text(json.dumps(dict(checked_on='2026-10-14',assets=records),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for a in records:print(a['file'],a['status'],a.get('bytes',a.get('error')),flush=True)
if __name__=='__main__':main()
