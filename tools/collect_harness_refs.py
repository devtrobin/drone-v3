"""Collect public references for the final power-harness components; no purchases."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,hashlib,urllib.request,re,sys
import pymupdf
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/faisceau-puissance'
KLAUKE='https://www.klauke.com/gb/en/tubular-cable-lugs-cu-standard-type-4959'
AUPROTEC='https://auprotec.de/de/elektrik/fahrzeugleitungen-einadrig/flry-b-leitung/6-00-mm2-flry-b-leitung/flry-b-6-0-mm2-batteriekabel-rot-6m-ring/p/044906'
TASKS=[
 ('sources-web/Klauke-95R.html',KLAUKE),('sources-web/AUPROTEC-FLRYB6.html',AUPROTEC),
 ('sources-web/Ancor-catalogue-page24.html','https://docs.navico.com/view/362211770/24/'),
 ('sources-web/Ancor-catalogue-page25.html','https://docs.navico.com/view/362211770/25/'),
 ('notices/Ancor-catalogue-2020-original.pdf','https://www.projectk.co.jp/marine/pdf/2020_ancor_catalog.pdf'),
 ('notices/Klauke-catalogue-2019-original.pdf','https://www.klauke.com/Media/Default/Downloads/CatalogsBrochures/KATHAUPT19GB_06_19_I_GB_web.pdf'),
 ('notices/HT-isolation-catalogue-2026-original.pdf','https://www.hellermanntyton.com/binaries/content/assets/downloads/com/product_catalogue/ht_insulation_2026_com.pdf'),
 ('notices/HT-T18R-11101919-fiche-originale.pdf','https://www.hellermanntyton.com/shared/assets/TDS_111-01919_com.pdf'),
 ('notices/HT-T18R-plan-original.pdf','https://www.hellermanntyton.com/shared/assets/CAD_10-0585-001-CSC.pdf'),
 ('sources-web/HT-T18R.html','https://www.hellermanntyton.com/products/cable-ties-inside-serrated/t18r/111-01919'),
 ('sources-web/HT-MB2.html','https://www.hellermanntyton.com/au/products/cable-tie-mounts/mb2/151-28210'),
 ('sources-web/HT-HISA9.html','https://www.hellermanntyton.com/products/heat-shrink-tubing/his-a-9-3/308-10900'),
 ('sources-web/Amazon-FR-Ancor312303.html','https://www.amazon.fr/s?k=Ancor+312303'),
 ('sources-web/Amazon-FR-Ancor309203.html','https://www.amazon.fr/s?k=Ancor+309203'),
 ('sources-web/Amazon-FR-Klauke95R.html','https://www.amazon.fr/s?k=Klauke+95R4+95R5'),
 ('sources-web/Amazon-FR-HISA9.html','https://www.amazon.fr/s?k=HellermannTyton+308-10900'),
 ('sources-web/Amazon-FR-MB2.html','https://www.amazon.fr/s?k=HellermannTyton+151-28210'),
 ('sources-web/Amazon-FR-T18R.html','https://www.amazon.fr/s?k=HellermannTyton+111-01919'),
 ('sources-web/Amazon-COM-AUPROTEC6.html','https://www.amazon.com/dp/B00HDGB6GG'),
 ('sources-web/Amazon-FR-AUPROTEC6.html','https://www.amazon.fr/dp/B00HDGB6GG'),
 ('sources-web/TE-ATUM8.html','https://www.te.com/en/product-NB11802001.html'),
 ('notices/TE-ATUM-guide-2015-original.pdf','https://www.te.com/content/dam/te-com/documents/energy/jpn/heat_shrink_tubing_2015-03_rev.pdf'),
 ('notices/Klauke-cosses-catalogue-via-IEP.pdf','https://www.iep.com.my/wp-content/uploads/2020/10/Klauke-cable-lugs.pdf'),
 ('notices/HT-MB2-15128210-fiche-originale.pdf','https://www.hellermanntyton.com/shared/assets/TDS_151-28210_com.pdf'),
 ('sources-web/Amazon-FR-ATUM8.html','https://www.amazon.fr/s?k=Raychem+ATUM-8%2F2-0-STK'),
 ('notices/HT-MB2-plan-original.pdf','https://www.hellermanntyton.com/shared/assets/CAD_141622.pdf'),
 ('notices/HT-MB2-fiche-AU-originale.pdf','https://www.hellermanntyton.com/shared/assets/TDS_151-28210_com_au.pdf'),
 ('notices/TE-ATUM-plan-A2-original.pdf','https://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocFormat=pdf&DocLang=English&DocNm=ATUM_4_to_RATIO_STANDARD_SIZES&DocType=Customer+Drawing&PartCntxt=NB11802001'),
 ('notices/TE-ATUM-fiche-2024-originale.pdf','https://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocFormat=pdf&DocLang=English&DocNm=atum-tubing&DocType=Data+Sheet&PartCntxt=NB11802001'),
 ('photos/Klauke-logo-UL-original.jpg','https://cdn.klauke.com/resources/images/a6c5ac55-b8af-4cf2-9cd8-73b2bacc4fab'),
]
def fetch(task):
    name,url=task;p=BASE/name;p.parent.mkdir(parents=True,exist_ok=True);rec=dict(file=name,url=url,checked_on='2026-10-14',modified=False)
    try:
        if p.exists():b=p.read_bytes();final=url
        else:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=25) as r:b=r.read();final=r.geturl()
        if name.endswith('.pdf'):assert b.startswith(b'%PDF'),'response is not a PDF'
        p.write_bytes(b);status='downloaded' if b else 'empty_response'
        if any(t in b for t in [b'validateCaptcha',b'bm-verify',b'challenge-platform']):status='challenge_html'
        rec.update(status=status,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),final_url=final)
    except Exception as e:rec.update(status='unavailable',error=str(e))
    return rec
def main():
    sys.stdout.reconfigure(encoding='utf-8');BASE.mkdir(parents=True,exist_ok=True)
    with ThreadPoolExecutor(max_workers=6) as pool:records=list(pool.map(fetch,TASKS))
    # Public PDF/CAD/image URLs observed in maker pages, not guessed names.
    details=[]
    for name,stem in [('sources-web/HT-MB2.html','HT-MB2'),('sources-web/HT-HISA9.html','HT-HISA9')]:
        p=BASE/name
        if not p.exists():continue
        html=p.read_text(encoding='utf-8',errors='replace')
        urls=list(dict.fromkeys(re.findall(r'(?:href|data-download-url|src)=[\"\']([^\"\']+)',html)))
        relevant=[u for u in urls if 'shared/assets/' in u and any(t in u for t in ['TDS_','CAD_'])]
        for i,u in enumerate(relevant[:5]):
            url=u if u.startswith('http') else 'https://www.hellermanntyton.com'+u
            details.append((f'notices/{stem}-original-{i+1}{Path(u).suffix}',url))
        cad=[u for u in urls if any(u.lower().endswith(t) for t in ['.step','.stp','.zip'])]
        print('CAD_LINKS',stem,cad[:6],flush=True)
    if details:
        with ThreadPoolExecutor(max_workers=5) as pool:records+=list(pool.map(fetch,details))
    (BASE/'assets.json').write_text(json.dumps(dict(checked_on='2026-10-14',assets=records),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for a in records:print(a['file'],a['status'],a.get('bytes',a.get('error')),flush=True)
    tmp=ROOT/'tools/temp/harness-review/sources';tmp.mkdir(parents=True,exist_ok=True)
    for a in records:
        if not a['file'].endswith('.pdf') or a['status']!='downloaded':continue
        doc=pymupdf.open(BASE/a['file'])
        for i,page in enumerate(doc):
            text=page.get_text()
            wanted='95R4' in text or ('312303' in text and i==25) or ('309203' in text and i==26) or ('HIS-A-9/3' in text) or len(doc)==1
            if wanted:
                print('PDF_TEXT',Path(a['file']).name,'page',i+1,text[:2000].replace('\n',' | '),flush=True)
                if ('95R4' in text or len(doc)==1 or 'HIS-A-9/3' in text):page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(tmp/f'{Path(a["file"]).stem}-p{i+1}.png')
if __name__=='__main__':main()
