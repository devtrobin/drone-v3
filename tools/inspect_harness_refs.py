"""Inspect public maker pages/specifications without printing session attributes."""
from pathlib import Path
import re,html,sys,json
import pymupdf
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/faisceau-puissance'
def main():
    sys.stdout.reconfigure(encoding='utf-8')
    p=BASE/'sources-web/AUPROTEC-FLRYB6.html'
    s=p.read_text(encoding='utf-8',errors='replace')
    clean=re.sub(r'<(?:script|style).*?</(?:script|style)>','',s,flags=re.S);clean=html.unescape(re.sub('<[^>]+>',' ',clean));clean=re.sub(r'\s+',' ',clean)
    for token in ['Technische','Nennquerschnitt','Temperatur','Außendurchmesser','Leiter','6,0','4,1','4,4']:
        m=re.search(re.escape(token),clean,re.I)
        if m:print('AUPROTEC',token,clean[max(0,m.start()-80):m.start()+1100])
    for u in sorted(set(re.findall(r'href=[\"\']([^\"\']+/p/\d+)[\"\']',s))):
        if '6-0-mm2' in u:print('PRODUCT_VARIANT',u)
    for p in (BASE/'sources-web').glob('Amazon-COM*.html'):
        s=p.read_text(encoding='utf-8',errors='replace');m=re.search(r'id="productTitle"[^>]*>(.*?)</span>',s,re.S)
        print('AMAZON_TITLE',p.name,html.unescape(m[1].strip()) if m else 'unavailable')
    for p in (BASE/'notices').glob('*ATUM*.pdf'):
        doc=pymupdf.open(p)
        for i,page in enumerate(doc):
            text=page.get_text()
            if '8/2' in text:print('ATUM',p.name,'page',i+1,text[:3500].replace('\n',' | '))
if __name__=='__main__':main()
