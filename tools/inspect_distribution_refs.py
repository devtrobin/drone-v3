"""Read and render only relevant pages of archived original documents."""
from pathlib import Path
import pymupdf,sys,json
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/distribution-alimentation'
OUT=ROOT/'tools/temp/distribution-review/sources'
def main():
    sys.stdout.reconfigure(encoding='utf-8');OUT.mkdir(parents=True,exist_ok=True);pages=[]
    for name in ['BlueSea-certificat-IMCI-BusBars.pdf','BlueSea-declaration-BusBars.pdf','BlueSea-catalogue-2024-miroir-PrimeMarine.pdf']:
        doc=pymupdf.open(BASE/'notices'/name)
        for i,page in enumerate(doc):
            txt=page.get_text()
            if len(doc)==1 or (i==99 and 'catalogue' in name) or ('MiniBus 100A Common' in txt and '2315' in txt):
                print(name,'PDF PAGE',i+1,txt[:11000],flush=True)
                fn=f'{Path(name).stem}-p{i+1}.png';page.get_pixmap(matrix=pymupdf.Matrix(1.7,1.7)).save(OUT/fn)
                pages.append(dict(file=name,page=i+1,render=str((OUT/fn).relative_to(ROOT)).replace('\\','/')))
    (OUT/'pages.json').write_text(json.dumps(pages,indent=2),encoding='utf-8')
if __name__=='__main__':main()
