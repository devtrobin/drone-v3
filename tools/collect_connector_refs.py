"""Archive public XT60H source documents without purchase or authentication."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,json,hashlib,sys,re
import pymupdf
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/connecteurs-alimentation'
TASKS=[
 ('notices/AMASS-XT60H-F-M-V1.2-via-Shoptronica.pdf','https://www.shoptronica.com/ficheros/XT60H.pdf'),
 ('notices/AMASS-XT60H-M-V1.2-via-Marutsu.pdf','https://www.marutsu.co.jp/contents/shop/marutsu/datasheet/XT60H-M.pdf'),
 ('notices/AMASS-XT60H-F-2023C0-via-LCSC.pdf','https://datasheet.lcsc.com/lcsc/2409041651_Changzhou-Amass-Elec-XT60H-F-Z-G-Y_C30170204.pdf'),
 ('notices/AMASS-catalogue-3G-2024-original.pdf','https://www.china-amass.com/public/upload/20240620/94b600a6a4c042646bc89646abc8ea85.pdf'),
 ('notices/AMASS-catalogue-XT-2026-original.pdf','https://www.china-amass.com/public/upload/20260207/7fa24f5a6f35ec66c7a115c07a34ab06.pdf'),
 ('photos/AMASS-plan-page-produit.png','https://www.china-amass.com/ueditor/php/upload/image/20241112/1731400363441838.png'),
 ('sources-web/AMASS-XT60H.html','https://www.china-amass.com/biao/283.html'),
 ('sources-web/AMASS-telechargements.html','https://www.china-amass.com/download/'),
 ('sources-web/Amazon-FR-B074PN6N4K.html','https://www.amazon.fr/dp/B074PN6N4K'),
 ('sources-web/Amazon-COM-B074PN6N4K.html','https://www.amazon.com/dp/B074PN6N4K'),
 ('sources-web/TME-F.html','https://www.tme.eu/fr/details/xt60h-f/connecteurs-dc/amass/'),
 ('sources-web/RCCrawler-utilisateurs.html','https://www.rccrawler.com/forums/threads/genuine-connectors.619280/'),
 ('sources-web/DashCamTalk-cables.html','https://dashcamtalk.com/forum/threads/7500-mah-96-wh-blackboxmycar-powercell-8-blackvue-b-130x-thinkware-ivolt-xtra-bab-95.48162/page-2'),
]
def fetch(task):
    name,url=task;p=BASE/name;p.parent.mkdir(parents=True,exist_ok=True)
    rec=dict(file=name,url=url,checked_on='2026-10-14',modified=False)
    try:
        if p.exists():
            blob=p.read_bytes();final=url
            if name.endswith('.pdf'):assert blob.startswith(b'%PDF')
            challenged=any(t in blob for t in [b'validateCaptcha',b'bm-verify',b'challenge-platform'])
            return dict(rec,status='downloaded' if not challenged else 'challenge_html',bytes=len(blob),sha256=hashlib.sha256(blob).hexdigest(),final_url=final)
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as r:blob=r.read();final=r.geturl()
        if name.endswith('.pdf'):assert blob.startswith(b'%PDF'),'response is not PDF'
        if name.endswith('.png'):assert blob.startswith(b'\x89PNG'),'response is not PNG'
        p.write_bytes(blob)
        status='downloaded' if blob else 'empty_response'
        if any(t in blob for t in [b'validateCaptcha',b'bm-verify',b'challenge-platform']):status='challenge_html'
        rec.update(status=status,bytes=len(blob),sha256=hashlib.sha256(blob).hexdigest(),final_url=final)
    except Exception as e:rec.update(status='unavailable',error=str(e))
    return rec
def main():
    sys.stdout.reconfigure(encoding='utf-8');BASE.mkdir(parents=True,exist_ok=True)
    with ThreadPoolExecutor(max_workers=5) as pool:records=list(pool.map(fetch,TASKS))
    html=BASE/'sources-web/AMASS-XT60H.html'
    if html.exists():
        paths=list(dict.fromkeys(re.findall(r'(?:src|href)=[\"\']([^\"\']+)',html.read_text(encoding='utf-8',errors='replace'))))
        images=[p for p in paths if 'upload' in p and p.lower().endswith(('.jpg','.jpeg','.png')) and '1731400363441838' not in p]
        for i,path in enumerate(images[:4]):
            url=path if path.startswith('http') else 'https://www.china-amass.com'+path
            records.append(fetch((f'photos/AMASS-produit-{i+1}{Path(path).suffix}',url)))
    source=ROOT/'Composants/moteur/photos/04-variateur-cables.jpg'
    target=BASE/'photos/Hobbywing-WP16BL30-G2-contacts-originaux.jpg';target.write_bytes(source.read_bytes())
    records.append(dict(file=str(target.relative_to(BASE)).replace('\\','/'),status='copied_original',modified=False,bytes=target.stat().st_size,
        sha256=hashlib.sha256(target.read_bytes()).hexdigest(),url='https://www.hobbywing.com/en/uploads/image/20250320/11fe634ae7e7736d36fcc3684c4a2eb6.jpg',
        source_local=str(source.relative_to(ROOT)).replace('\\','/'),checked_on='2026-10-14'))
    (BASE/'assets.json').write_text(json.dumps(dict(checked_on='2026-10-14',assets=records),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    tmp=ROOT/'tools/temp/connectors-review/sources';tmp.mkdir(parents=True,exist_ok=True)
    for a in records:
        print(a['file'],a['status'],a.get('bytes',a.get('error')),flush=True)
        if a['file'].endswith('.pdf') and a['status']=='downloaded':
            doc=pymupdf.open(BASE/a['file']);sel=[14] if '2026' in a['file'] else [12] if 'catalogue' in a['file'] else list(range(len(doc)))
            for i in sel:
                doc[i].get_pixmap(matrix=pymupdf.Matrix(2,2)).save(tmp/f'{Path(a["file"]).stem}-p{i+1}.png')
                print('PDF_TEXT',Path(a['file']).name,i+1,doc[i].get_text()[:3800].replace('\n',' | '),flush=True)
if __name__=='__main__':main()
