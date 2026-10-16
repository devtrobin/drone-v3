"""Archive maker sources and public purchase/review references for Active Cooler."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,json,hashlib,re,sys
import pymupdf
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/refroidissement-raspberry-pi-5'
MAKER='https://www.raspberrypi.com/products/active-cooler/'
PORTAL='https://pip.raspberrypi.com/categories/993-raspberry-pi-active-cooler'
TASKS=[
 ('sources-web/RaspberryPi-produit.html',MAKER),('sources-web/RaspberryPi-portail.html',PORTAL),
 ('notices/RaspberryPi-ActiveCooler-fiche-actuelle-originale.pdf','https://pip.raspberrypi.com/documents/RP-008188-DS-active-cooler-product-brief.pdf'),
 ('notices/RaspberryPi-ActiveCooler-plan-reference-original.pdf','https://datasheets.raspberrypi.com/cooling/raspberry-pi-active-cooler-mechanical-drawing.pdf'),
 ('notices/RaspberryPi-ActiveCooler-fiche-historique-originale.pdf','https://datasheets.raspberrypi.com/cooling/raspberry-pi-active-cooler-product-brief.pdf'),
 ('sources-web/RaspberryPi-thermique-2023.html','https://www.raspberrypi.com/news/heating-and-cooling-raspberry-pi-5/'),
 ('sources-web/RaspberryPi-doc-materiel.html','https://www.raspberrypi.com/documentation/computers/raspberry-pi.html'),
 ('sources-web/Amazon-FR-recherche.html','https://www.amazon.fr/s?k=Raspberry+Pi+Active+Cooler+SC1148'),
 ('sources-web/Geerling-mesures-2024.html','https://www.jeffgeerling.com/blog/2024/water-cooling-overkill-pi-5/'),
 ('sources-web/Forum-bruit.html','https://forums.raspberrypi.com/viewtopic.php?p=2179285'),
 ('sources-web/Forum-boitier.html','https://forums.raspberrypi.com/viewtopic.php?t=367026'),
 ('sources-web/YouTube-Geerling.html','https://www.youtube.com/watch?v=nBtOEmUqASQ'),
 ('sources-web/Olimex-produit.html','https://www.olimex.com/Products/RaspberryPi/RPi5-ACOOL/'),
]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fetch(task):
    name,url=task;p=BASE/name;p.parent.mkdir(parents=True,exist_ok=True);rec=dict(file=name,url=url,checked_on='2026-10-14',original_unmodified=True)
    try:
        if p.exists():b=p.read_bytes();final=url
        else:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=25) as r:b=r.read();final=r.geturl()
        if name.endswith('.pdf'):assert b.startswith(b'%PDF'),'not a PDF'
        p.write_bytes(b);status='downloaded' if b else 'empty_response'
        if any(t in b for t in [b'validateCaptcha',b'bm-verify',b'challenge-platform']):status='challenge_html'
        rec.update(status=status,bytes=len(b),sha256=sha(p),final_url=final)
    except Exception as e:rec.update(status='unavailable',error=str(e))
    return rec
def main():
    sys.stdout.reconfigure(encoding='utf-8');BASE.mkdir(parents=True,exist_ok=True)
    with ThreadPoolExecutor(max_workers=5) as pool:records=list(pool.map(fetch,TASKS))
    # Follow the actual current portal PDF links; do not infer revision numbers.
    portal=BASE/'sources-web/RaspberryPi-portail.html';extra=[]
    if portal.exists():
        s=portal.read_text(encoding='utf-8',errors='replace');urls=re.findall(r'href=[\"\']([^\"\']+)[\"\']',s)
        for u in dict.fromkeys(urls):
            if 'active-cooler' in u and ('mechanical' in u or 'product-brief' in u) and '/documents/' in u:
                u=urllib.request.urljoin(PORTAL,u)
                if u not in [r['url'] for r in records]:extra.append(('notices/portail-'+('plan' if 'mechanical' in u else 'fiche')+'-original.pdf',u))
    if extra:
        with ThreadPoolExecutor(max_workers=4) as pool:records+=list(pool.map(fetch,extra))
    # Maker photos from product HTML, retaining their exact downloaded bytes.
    maker=BASE/'sources-web/RaspberryPi-produit.html'
    if maker.exists():
        s=maker.read_text(encoding='utf-8',errors='replace')
        urls=list(dict.fromkeys(re.findall(r'https://assets\.raspberrypi\.com/[^\s\"<>]+',s)))
        urls=[u.replace('&amp;','&') for u in urls if re.search(r'\.(?:jpg|jpeg|png)(?:\?|$)',u,re.I)]
        for i,u in enumerate(urls[:5]):records.append(fetch((f'photos/RaspberryPi-original-{i+1}{".png" if ".png" in u else ".jpg"}',u)))
    (BASE/'assets.json').write_text(json.dumps(dict(checked_on='2026-10-14',assets=records),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for r in records:print(r['file'],r['status'],r.get('bytes',r.get('error')),flush=True)
    tmp=ROOT/'tools/temp/pi-cooler-review/sources';tmp.mkdir(parents=True,exist_ok=True)
    for r in records:
        if r['status']=='downloaded' and r['file'].endswith('.pdf'):
            doc=pymupdf.open(BASE/r['file']);print('PDF',r['file'],len(doc),'pages',flush=True)
            for i,page in enumerate(doc):
                print('TEXT',i+1,page.get_text()[:2400].replace('\n',' | '),flush=True)
                if 'plan' in r['file'] or i in (1,2,3):page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(tmp/f'{Path(r["file"]).stem}-p{i+1}.png')
                # Extract original embedded photos intact (no edits).
                if 'fiche-actuelle' in r['file'] and i in (0,1):
                    for j,im in enumerate(page.get_images(full=True)):
                        obj=doc.extract_image(im[0])
                        if obj['width']>300 and obj['height']>300:
                            path=BASE/f'photos/RaspberryPi-fiche-p{i+1}-{j+1}.{obj["ext"]}';path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(obj['image'])
                            records.append(dict(file=str(path.relative_to(BASE)).replace('\\','/'),source_document=r['file'],source_pdf_page=i+1,
                                original_unmodified=True,status='extracted_original',bytes=path.stat().st_size,sha256=sha(path)))
    (BASE/'assets.json').write_text(json.dumps(dict(checked_on='2026-10-14',assets=records),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
