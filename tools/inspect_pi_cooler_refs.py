from pathlib import Path
import pymupdf,json,re,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/refroidissement-raspberry-pi-5';TMP=ROOT/'tools/temp/pi-cooler-review/sources'
def main():
    sys.stdout.reconfigure(encoding='utf-8')
    d=pymupdf.open(BASE/'notices/RaspberryPi-ActiveCooler-plan-reference-original.pdf')
    d[0].get_pixmap(matrix=pymupdf.Matrix(4,4),clip=pymupdf.Rect(66,60,282,250)).save(TMP/'plan-zoom.png')
    d=pymupdf.open(BASE/'notices/RaspberryPi-ActiveCooler-fiche-actuelle-originale.pdf')
    for i in (4,5):d[i].get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(TMP/f'fiche-p{i+1}.png')
    pd=pymupdf.open(ROOT/'Composants/raspberry-pi-5/notices/Raspberry-Pi-5-plan-mecanique.pdf')
    pd[0].get_pixmap(matrix=pymupdf.Matrix(2,2)).save(TMP/'Pi5-plan-reference.png')
    # Match actual public PIP destinations to archives, record declared update dates.
    s=(BASE/'sources-web/RaspberryPi-portail.html').read_text(encoding='utf-8');s=re.sub(r'<[^>]+>',' ',s);s=re.sub(r'\s+',' ',s)
    for word in ['mechanical-drawing','product-brief']:
        x=s.find(word);print('PORTAL',s[x:x+220])
    for p in (BASE/'sources-web').glob('*.html'):
        if 'Geerling' in p.name or 'Olimex' in p.name:
            s=re.sub(r'<(?:script|style).*?</(?:script|style)>','',p.read_text(encoding='utf-8'),flags=re.S)
            s=re.sub(r'<[^>]+>',' ',s);s=re.sub(r'\s+',' ',s)
            for word in ['rpm','dBa','EUR','euro','Price','stock','VAT']:
                m=re.search(word,s,re.I)
                if m:print(p.name,word,s[max(0,m.start()-80):m.start()+250])
if __name__=='__main__':main()
