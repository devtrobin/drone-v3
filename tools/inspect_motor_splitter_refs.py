"""Read and render all archived reference PDFs; summarize public download links."""
from pathlib import Path
import pymupdf,re,sys
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/repartition-moteurs';TMP=ROOT/'tools/temp/motor-splitter-review/sources'
def main():
    sys.stdout.reconfigure(encoding='utf-8');TMP.mkdir(parents=True,exist_ok=True)
    for path in sorted((BASE/'notices').glob('*.pdf')):
        doc=pymupdf.open(path);txt='\n'.join(p.get_text() for p in doc)
        (TMP/(path.stem+'.txt')).write_text(txt,encoding='utf-8')
        print(path.name,len(doc),'pages',flush=True)
        if len(doc)<=5:
            for i,p in enumerate(doc):p.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(TMP/f'{path.stem}-p{i+1}.png')
        matches=[line for line in txt.splitlines() if re.search(r'UD.?80|569010|orque|Nm|N.m|strip|dénud|CAD',line,re.I)]
        print('\n'.join(matches[:35]),flush=True)
    for path in (BASE/'sources-web').glob('*.html'):
        if 'nVent' in path.name or 'Graybar' in path.name:
            txt=path.read_text(encoding='utf-8',errors='ignore')
            links=list(dict.fromkeys(re.findall(r'(?:src|href)=["\']([^"\']+)["\']',txt)))
            print('LINKS',path.name,'\n'.join(s for s in links if re.search(r'pdf|\.step|\.stp|\.igs|\.dxf|\.jpg|\.png|instruction|drawing|CAD',s,re.I))[:14000],flush=True)
if __name__=='__main__':main()
