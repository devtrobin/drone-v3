"""Extract relevant original reference pages without modifying their PDFs."""
from pathlib import Path
import pymupdf,json,sys,re
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/protection-branche-pi';TMP=ROOT/'tools/temp/pi-fuse-review/sources'
def main():
    sys.stdout.reconfigure(encoding='utf-8');TMP.mkdir(parents=True,exist_ok=True);records=[]
    paths=[BASE/'notices/Littelfuse-ATO-fiche-originale-via-RSP.pdf',BASE/'notices/Littelfuse-catalogue-aftermarket-2013-via-RS.pdf',
           ROOT/'Composants/distribution-alimentation/notices/BlueSea-catalogue-2024-miroir-PrimeMarine.pdf']
    for path in paths:
        doc=pymupdf.open(path);print(path.name,'PAGES',len(doc),flush=True)
        for i,page in enumerate(doc):
            text=page.get_text()
            match=(len(doc)<=4) or ('BlueSea' in path.name and '5065' in text and 'Pigtails' in text) or ('2013' in path.name and 'ATO7.5BP' in text)
            if not match:continue
            fn=f'{path.stem}-p{i+1}.png';page.get_pixmap(matrix=pymupdf.Matrix(1.7,1.7)).save(TMP/fn)
            records.append(dict(file=str(path.relative_to(ROOT)).replace('\\','/'),page=i+1,render=str((TMP/fn).relative_to(ROOT)).replace('\\','/')))
            print('PAGE',i+1,text[:7500],flush=True)
    (TMP/'pages.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')
    source=BASE/'sources-web/Skysat-5065.html'
    if source.exists():
        txt=source.read_text(encoding='utf-8');plain=re.sub(r'<[^>]+>',' ',txt)
        for term in ['38 x 25','priceCurrency','5065-BSS']:
            pos=txt.find(term);print('SKYSAT',term,txt[max(0,pos-80):pos+150],flush=True)
if __name__=='__main__':main()
