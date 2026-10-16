"""Read-only extraction and rendering of relevant original reference pages."""
from pathlib import Path
import pymupdf,sys
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/protection-branches-moteurs'
TMP=ROOT/'tools/temp/motor-fuse-review/sources'
def main():
    sys.stdout.reconfigure(encoding='utf-8');TMP.mkdir(parents=True,exist_ok=True)
    d=pymupdf.open(BASE/'notices/Littelfuse-ATO-fiche-originale-via-RSP.pdf')
    for i in [1,2]:
        p=d[i];p.get_pixmap(matrix=pymupdf.Matrix(1.6,1.6)).save(TMP/f'ATO2022-page-{i+1}.png')
        print('ATO2022 page',i+1,p.get_text(),flush=True)
if __name__=='__main__':main()
