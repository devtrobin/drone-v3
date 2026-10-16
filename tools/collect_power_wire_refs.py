"""Archive public BNTECHGO wire sources and comparison datasheets."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,json,hashlib,sys,re
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/cable-puissance-12awg'
MAKER='https://bntechgo.com/bntechgo-12-gauge-silicone-wire-kit-ultra-flexible-20-ft-black-and-red-each-color-10-ft-high-temp-200-c-600v-12-awg-silicone-wire-680-strands-of-tinned-copper-wire-stranded-wire-stranded-wire-for-model-battery/'
TASKS=[('sources-web/BNTECHGO-SW12G68008F10C2.html',MAKER),
 ('sources-web/Amazon-FR-B01AO7586O.html','https://www.amazon.fr/dp/B01AO7586O'),
 ('sources-web/Amazon-COM-B01AO7586O.html','https://www.amazon.com/dp/B01AO7586O'),
 ('sources-web/Amazon-FR-B01ABOPMEI.html','https://www.amazon.fr/dp/B01ABOPMEI'),
 ('sources-web/Amazon-COM-B01ABOPMEI.html','https://www.amazon.com/dp/B01ABOPMEI'),
 ('sources-web/RCTech-utilisateurs.html','https://www.rctech.net/forum/radio-electronics/1131751-where-buy-silicone-copper-wire.html'),
 ('sources-web/Newegg-dimensions.html','https://www.newegg.com/p/0PY-012A-00082'),
 ('notices/HingTak-catalogue-silicone-comparaison.pdf','https://www.hingtak.com/assets/catalogs/catalog-flexible-silicone-008.pdf'),
 ('notices/Junhao-catalogue-comparaison.pdf','https://en.junhaodx.com/Catalogue.pdf'),
 ('notices/ModalAI-MCBL00110-v4-cable-BNTECHGO-XT60.pdf','https://storage.googleapis.com/modalai_public/modal_drawings/MCBL-00110%20Drawing%20v4.pdf')]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fetch(task):
    name,url=task;p=BASE/name;p.parent.mkdir(parents=True,exist_ok=True);rec=dict(file=name,url=url,modified=False,checked_on='2026-10-14')
    try:
        if p.exists():b=p.read_bytes();final=url
        else:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as r:b=r.read();final=r.geturl()
        if name.endswith('.pdf'):assert b.startswith(b'%PDF'),'not a PDF'
        p.write_bytes(b);status='downloaded' if b else 'empty_response'
        if any(t in b for t in [b'validateCaptcha',b'bm-verify',b'challenge-platform']):status='challenge_html'
        rec.update(status=status,bytes=len(b),sha256=sha(p),final_url=final)
    except Exception as e:rec.update(status='unavailable',error=str(e))
    return rec
def main():
    sys.stdout.reconfigure(encoding='utf-8');BASE.mkdir(parents=True,exist_ok=True)
    with ThreadPoolExecutor(max_workers=5) as pool:records=list(pool.map(fetch,TASKS))
    page=BASE/'sources-web/BNTECHGO-SW12G68008F10C2.html'
    if page.exists():
        urls=list(dict.fromkeys(re.findall(r'https://cdn11\.bigcommerce\.com/[^\s\"<>]+',page.read_text(encoding='utf-8',errors='replace'))))
        urls=[u.replace('&amp;','&') for u in urls if any(n in u for n in ['sw-12-1-1','sw-12-2-1','sw-12-3','sw-12-4']) and '.jpg' in u]
        for i,url in enumerate(urls[:5]):records.append(fetch((f'photos/BNTECHGO-original-{i+1}.jpg',url)))
    (BASE/'assets.json').write_text(json.dumps(dict(checked_on='2026-10-14',assets=records),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for r in records:print(r['file'],r['status'],r.get('bytes',r.get('error')),flush=True)
if __name__=='__main__':main()
