"""Contact sheets are for actual visual inspection, never automatic approval."""
from pathlib import Path
import json,sys,hashlib
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];TMP=ROOT/'tools/temp/final-components/pdf'
FOLDERS=['connecteurs-commande','liaisons-alimentation-surveillance','maintien-batterie','coupure-manuelle']
def main():
 sys.stdout.reconfigure(encoding='utf-8')
 for folder in FOLDERS:
  paths=sorted((TMP/folder).glob('page-*.png'))
  for start in range(0,len(paths),4):
   batch=paths[start:start+4];canvas=Image.new('RGB',(1320,1900),'#cfd8df');draw=ImageDraw.Draw(canvas)
   font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
   for j,path in enumerate(batch):
    im=Image.open(path).convert('RGB');im.thumbnail((630,891));x=(j%2)*660+15;y=(j//2)*950+40
    canvas.paste(im,(x,y));draw.text((x,y-27),folder+' - '+path.stem,font=font,fill='#172534')
   out=TMP/(folder+f'-review-{start//4+1}.jpg');canvas.save(out,quality=94);print(out)
 if '--accept-reviewed' in sys.argv:
  for folder in FOLDERS:
   p=ROOT/'Composants'/folder/'notices'/f'notice-{folder}-v3.json';m=json.loads(p.read_text(encoding='utf-8'))
   pdf=p.with_suffix('.pdf');assert hashlib.sha256(pdf.read_bytes()).hexdigest()==m['sha256']
   m.update(visual_review_complete=True,visual_review_date='2026-10-14',visual_review_method='Rendered every final page and viewed all contact sheets, with full page checks for layout issues.')
   p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  print('VISUAL REVIEW registered for all four current PDF hashes')
if __name__=='__main__':main()
