"""Read saved variant data and source PDFs without printing page/session content."""
from pathlib import Path
import re,json,sys
import pymupdf
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/cable-puissance-12awg'
def main():
    sys.stdout.reconfigure(encoding='utf-8')
    for p in (BASE/'sources-web').glob('Amazon-COM*.html'):
        html=p.read_text(encoding='utf-8',errors='replace')
        title=re.search(r'id="productTitle"[^>]*>(.*?)</span>',html,re.S)
        print('TITLE',p.name,re.sub('<[^>]+>',' ',title[1]).strip() if title else 'not available')
        for key in ['dimensionValuesDisplayData','asinVariationValues']:
            matches=list(re.finditer('"'+key+'"\\s*:\\s*',html))
            if matches:
                try:obj,end=json.JSONDecoder().raw_decode(html[matches[0].end():]);print(key,json.dumps(obj,ensure_ascii=False)[:6500])
                except Exception as e:print(key,'parse error',str(e))
    for p in (BASE/'notices').glob('*.pdf'):
        doc=pymupdf.open(p)
        for i,page in enumerate(doc):
            text=page.get_text()
            if '680' in text:
                print('PDF',p.name,'page',i+1,text[:3500].replace('\n',' | '))
                out=ROOT/'tools/temp/power-wire-review';out.mkdir(parents=True,exist_ok=True)
                page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(out/f'{p.stem}-p{i+1}.png')
if __name__=='__main__':main()
