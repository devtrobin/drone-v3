from pathlib import Path
import json,sys,hashlib,re,subprocess
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants'
FOLDERS=['connecteurs-commande','liaisons-alimentation-surveillance','maintien-batterie','coupure-manuelle']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 sys.stdout.reconfigure(encoding='utf-8');checks=[];steps=[];ncomp=0
 def check(name,passed,**data):checks.append(dict(check=name,passed=bool(passed),**data))
 for folder in FOLDERS:
  b=BASE/folder;cat=json.loads((b/'3D/catalogue.json').read_text(encoding='utf-8'));fc=json.loads((b/'3D/validation-freecad.json').read_text(encoding='utf-8'))
  check(folder+' FreeCAD',fc['all_passed'] and len(fc['checks'])==len(cat['models']))
  for m in cat['models']:
   p=BASE/m['relative_step_path'];steps.append(p)
   check(m['file']+' hash',p.exists() and sha(p)==m['sha256'])
   for ext in ['.json','.png']:check(m['file']+ext,p.with_suffix(ext).exists())
   check(m['file']+' quadrature',m['validation']['volume_relative_error']<1e-4)
  sources=json.loads((b/'sources.json').read_text(encoding='utf-8'))['sources']
  for e in sources:
   if e.get('status')=='archived':check(folder+' source '+e.get('id',e['file']), (b/e['file']).exists() and sha(b/e['file'])==e['sha256'])
  n=json.loads((b/'nomenclature.json').read_text(encoding='utf-8'));ncomp+=len(n['parts'])
  for a in n['parts']:
   p=b/a['id'];check(a['id']+' component docs',all((p/rel).exists() for rel in ['README.md','notice.md','cotes.md','avis-utilisateurs.md','selection.json','3D/README.md']))
  pdf=b/'notices'/f'notice-{folder}-v3.pdf';m=json.loads(pdf.with_suffix('.json').read_text(encoding='utf-8'))
  check(folder+' PDFhash',sha(pdf)==m['sha256']);check(folder+' visualreview',m['visual_review_complete']);check(folder+' PDFpages',m['pages']>=5)
  for p in b.rglob('*.md'):
   for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
    if link.startswith(('https:','http:','#','mailto:')):continue
    target=p.parent/link.split('#')[0];check(str(p.relative_to(BASE))+' link '+link,target.exists())
 rels=[str(p.relative_to(ROOT)) for p in steps]
 r=subprocess.run(['git','--no-optional-locks','check-ignore','--stdin'],input='\n'.join(rels)+'\n',text=True,capture_output=True,cwd=ROOT)
 check('STEP not gitignored',r.returncode==1 and not r.stdout.strip(),stdout=r.stdout,stderr=r.stderr)
 check('25 STEP',len(steps)==25);check('10 component folders',ncomp==10)
 # Procurement allocation, declared diagram deferral and no new board design.
 command=json.loads((BASE/FOLDERS[0]/'nomenclature.json').read_text(encoding='utf-8'))
 links=json.loads((BASE/FOLDERS[1]/'nomenclature.json').read_text(encoding='utf-8'))
 wago413=sum(a['qty'] for a in links['parts'] if a['id']=='wago-221-413')+sum(a['quantity'] for a in command['additional_parts'] if '221-413' in a['ref'])
 check('three WAGO413 counted exactly once',wago413==3)
 check('deferredscope',all('Visserie restante' in json.loads((BASE/f/'nomenclature.json').read_text(encoding='utf-8'))['excluded'] for f in FOLDERS))
 report=dict(checked_on='2026-10-14',all_passed=all(c['passed'] for c in checks),checks=checks,step_count=len(steps),component_count=ncomp,total_STEP_bytes=sum(p.stat().st_size for p in steps),purchase_made=False,hardware_tested=False)
 out=BASE/'verification-ensembles-avant-chassis.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 bad=[c for c in checks if not c['passed']];print('PACKAGE',len(checks),'checks',len(bad),'failures',len(steps),'STEP',ncomp,'components')
 for c in bad:print(c)
 assert report['all_passed']
if __name__=='__main__':main()
