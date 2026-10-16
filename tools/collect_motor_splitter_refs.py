"""Download public exact-product references; no purchase, login or messages."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,json,hashlib,sys
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/repartition-moteurs'
GRAY='https://static.graybarcanada.com/Products/Enclosures/Enclosure%2C%20Industrial/ERI569010/Files/'
TASKS=[
 ('notices/nVent-UD80A-fiche-FR-2023-via-RS.pdf','https://docs.rs-online.com/e8ac/A700000010539200.pdf'),
 ('notices/nVent-UD80A-fiche-EN-2023-via-RS.pdf','https://docs.rs-online.com/0b1d/A700000010539216.pdf'),
 ('notices/nVent-UD80A-fiche-FR-2020-via-Sonepar.pdf','https://res.cloudinary.com/sonepar-fr/raw/upload/s--hVva9jzD--/v1/documents/3058/569010_FICHE.pdf'),
 ('notices/nVent-UD-distribution-catalogue.pdf','https://www.nvent.com/sites/default/files/dam/h85126-en.pdf'),
 ('notices/Graybar-UD80A-document-1.pdf',GRAY+'ERI569010_Files_1.pdf'),
 ('notices/Graybar-UD80A-document-2.pdf',GRAY+'ERI569010_Files_2.pdf'),
 ('notices/Graybar-UD80A-document-3.pdf',GRAY+'ERI569010_Files_3.pdf'),
 ('sources-web/nVent-UD80A.html','https://www.nvent.com/en-us/ERIFLEX/products/EFSUD-80A'),
 ('sources-web/RS-FR-569010.html','https://fr.rs-online.com/web/p/blocs-de-distribution/2776180'),
 ('sources-web/Amazon-FR-recherche.html','https://www.amazon.fr/s?k=Eriflex+UD-80A+569010'),
 ('sources-web/Graybar-569010.html','https://www.graybarcanada.com/item/eri569010'),
 ('sources-web/Iconopower-avis.html','https://www.iconopower.com/Single_Pole_Distribution_Block_p/569010.htm'),
 ('photos/RS-569010-original.jpg','https://media.rs-online.com/f_auto%2Cq_auto%2Cbo_1.5px_solid_white%2Cb_auto%2Cc_pad%2Cdpr_2%2Ch_399%2Cw_710/c_pad%2Ch_399%2Cw_710/Y2776180-01?pgw=1'),
]
def fetch(task):
    name,url=task;p=BASE/name;p.parent.mkdir(parents=True,exist_ok=True)
    rec=dict(file=name,url=url,checked_on='2026-10-14',modified=False)
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as resp:data=resp.read();final=resp.geturl()
        if name.endswith('.pdf'):assert data.startswith(b'%PDF'),'response is not a PDF'
        p.write_bytes(data);status='downloaded'
        if not data:status='empty_response'
        elif any(s in data for s in [b'validateCaptcha',b'bm-verify',b'challenge-platform']):status='challenge_html'
        rec.update(status=status,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),final_url=final)
    except Exception as e:rec.update(status='unavailable',error=str(e))
    return rec
def main():
    sys.stdout.reconfigure(encoding='utf-8');BASE.mkdir(parents=True,exist_ok=True)
    with ThreadPoolExecutor(max_workers=5) as pool:records=list(pool.map(fetch,TASKS))
    (BASE/'assets.json').write_text(json.dumps(dict(checked_on='2026-10-14',assets=records),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for a in records:print(a['file'],a['status'],a.get('bytes',a.get('error')),flush=True)
if __name__=='__main__':main()
