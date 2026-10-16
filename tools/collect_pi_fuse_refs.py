"""Archive public references for the Pi-branch fuse; no purchase or form posting."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,json,hashlib,sys
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/protection-branche-pi'
TASKS=[
 ('notices/Littelfuse-ATO-aftermarket-2022.pdf','https://www.mouser.com/datasheet/2/240/media-3323444.pdf'),
 ('notices/Littelfuse-ATO-aftermarket-2022-source-fabricant.pdf','https://www.littelfuse.cn/assetdocs/littelfuse-datasheet-ato?assetguid=bba6ed2a-96e5-4b07-ab5d-0e8d267c0bd1'),
 ('notices/Littelfuse-ATO-fiche-originale-via-RSP.pdf','https://rspsupply.com/images/downloads/Littelfuse/0/Littelfuse%200ATO020.VP/Specification%20Document.pdf'),
 ('notices/Littelfuse-catalogue-aftermarket-2013-via-RS.pdf','https://docs.rs-online.com/d38b/0900766b813f0619.pdf'),
 ('notices/BlueSea-porte-fusibles-catalogue-2015.pdf','https://catalog2015.bluesea.com/files/common/downloads/page0043.pdf'),
 ('notices/Littelfuse-FHM-comparaison-2020.pdf','https://xonstorage.z8.web.core.windows.net/pdf/littelfuse_0fhm0002lxn_apr22_xonlink.pdf'),
 ('sources-web/BlueSea-5065.html','https://www.bluesea.com/products/5065/Waterproof_In-Line_ATO_ATC_Fuse_holder'),
 ('sources-web/Pololu-2813.html','https://www.pololu.com/product/2813'),
 ('sources-web/Amazon-FR-5065.html','https://www.amazon.fr/dp/B004ZIUA62'),
 ('sources-web/Amazon-US-5065.html','https://www.amazon.com/dp/B004ZIUA62'),
 ('sources-web/Amazon-FR-fusible-recherche.html','https://www.amazon.fr/s?k=Littelfuse+ATO7.5BP'),
 ('sources-web/PKYS-5065-mesures.html','https://shop.pkys.com/Blue-Sea-5065--Waterproof-In-Line-Fuse-Holder-for-ATOATC-Fuses_p_2716.html'),
 ('sources-web/Forum-SailboatOwners-5065.html','https://forums.sailboatowners.com/threads/what-are-you-using-as-a-bilge-pump-fuse-holder.162517/'),
 ('sources-web/Skysat-5065.html','https://skysat.fr/en-gb/products/blue-sea-waterproof-inline-ato-atc-fuse-holder'),
 ('porte-fusible/photos/Amazon-5065-original.jpg','https://m.media-amazon.com/images/I/51mfLfEM4UL._AC_SL1000_.jpg'),
]
def fetch(task):
    filename,url=task;p=BASE/filename;p.parent.mkdir(parents=True,exist_ok=True)
    rec=dict(file=filename,url=url,checked_on='2026-10-14',modified=False)
    try:
        if p.exists():
            data=p.read_bytes();final=url
            if (BASE/'assets.json').exists():
                prior=next((a for a in json.loads((BASE/'assets.json').read_text(encoding='utf-8'))['assets'] if a['file']==filename),None)
                if prior and prior.get('sha256')==hashlib.sha256(data).hexdigest():return prior
        else:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=24) as resp:data=resp.read();final=resp.geturl()
            if filename.endswith('.pdf'):assert data.startswith(b'%PDF'),'not a PDF'
            p.write_bytes(data)
        rec.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),final_url=final,
            status='challenge_html' if b'bm-verify' in data or b'validateCaptcha' in data else 'downloaded')
    except Exception as e:rec.update(status='unavailable',error=str(e))
    return rec
def main():
    sys.stdout.reconfigure(encoding='utf-8');BASE.mkdir(parents=True,exist_ok=True)
    with ThreadPoolExecutor(max_workers=5) as pool:records=list(pool.map(fetch,TASKS))
    old=json.loads((BASE/'assets.json').read_text(encoding='utf-8'))['assets'] if (BASE/'assets.json').exists() else []
    indexed={a['file']:a for a in old};indexed.update({a['file']:a for a in records})
    (BASE/'assets.json').write_text(json.dumps(dict(checked_on='2026-10-14',assets=list(indexed.values())),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for a in records:print(a['file'],a.get('bytes',a.get('error')),flush=True)
if __name__=='__main__':main()
