"""File integrity, independent CAD results, exact quantities, PDF and Git inclusion."""
from pathlib import Path
import sys,json,hashlib,re,urllib.parse,subprocess
import pymupdf
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/cordon-principal-batterie';checks=[]
def check(label,value,detail=None):
 checks.append(dict(check=label,passed=bool(value),detail=detail))
 if not value:print('FAIL',label,detail,flush=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 sys.stdout.reconfigure(encoding='utf-8')
 select=json.loads((BASE/'selection-active.json').read_text(encoding='utf-8'));nom=json.loads((BASE/'nomenclature.json').read_text(encoding='utf-8'))
 check('User choice applied: factory IC5 2S G1',select['user_choice']=='factory_stronger_connector_2S' and select['active_battery']['ref']=='SPMX50002S30H5' and select['active_battery']['generation']=='G1')
 check('Selected battery exact current offer available',select['active_battery']['offer_available'] and select['active_battery']['offer_price_EUR']==49.99)
 check('OEM cord already includes both wires',nom['parts'][0]['ref']=='SPMXCA510' and nom['parts'][0]['qty']==1 and len(nom['parts'])==3)
 check('Legacy parts excluded from active purchase',nom['legacy_parts_not_to_add_to_active_purchase'])
 check('No false electrical qualification',not select['hardware_tested'] and not select['fuse_coordination_validated'] and select['standalone_connector_current_rating_not_found'])
 assets=json.loads((BASE/'assets.json').read_text(encoding='utf-8'))
 for a in assets['assets']:
  if a.get('local'):
   p=BASE/a['local'];check('Archived source exists: '+a['id'],p.is_file())
   if p.is_file():check('Archived SHA256: '+a['id'],sha(p)==a['sha256'])
 cat=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'));fc=json.loads((BASE/'3D/validation-freecad.json').read_text(encoding='utf-8'))
 check('11 CAD files, 3 active IC5',cat['model_count']==11 and sum(m.get('version')=='IC5_active' for m in cat['models'])==3)
 check('Independent FreeCAD pass for all final files',fc['all_passed'] and len(fc['checks'])==11)
 table={a['relative_step_path']:a for a in fc['checks']}
 for m in cat['models']:
  p=ROOT/'Composants'/m['relative_step_path'];check('STEP exists: '+m['file'],p.is_file())
  check('STEP SHA256: '+m['file'],sha(p)==m['sha256'])
  check('FreeCAD exact final SHA256: '+m['file'],table[m['relative_step_path']]['sha256']==sha(p) and table[m['relative_step_path']]['passed'])
  meta=json.loads(p.with_suffix('.json').read_text(encoding='utf-8'));check('STEP metadata consistent: '+m['file'],meta['sha256']==m['sha256'] and meta['validation']['solids']==m['validation']['solids'])
  png=p.with_suffix('.png');check('Preview exists: '+m['file'],png.is_file());check('Preview SHA256: '+m['file'],sha(png)==m['preview']['sha256'])
  check('CAD volume and envelope roundtrip: '+m['file'],m['validation']['volume_relative_error']<1e-4 and m['validation']['bbox_error_mm']<.01)
  check('Named coloured solids: '+m['file'],m['validation']['colors']>=1 and m['validation']['solids']>0)
  if m.get('version')=='IC5_active':check('IC5 body dimension estimates disclosed: '+m['file'],not m['native_vendor_cad'] and not m['hardware_measured'])
  if m['file']=='cordon-principal-ic5-10awg-etude.step':
   for row in m['wire_continuity_checks']:
    check('Continuous wire and termination: '+row['pole'],row['core_radial_samples']>=1800 and row['jacket_radial_samples']>=1800 and max(row['bonds'].values())<1e-6)
    check('Installed wire fits below OEM initial length: '+row['pole'],row['core_path_length_mm']<101.6)
   check('Independent sleeve and eyelet clearance probes present',len(table[m['relative_step_path']]['material_probes'])==34)
 # All relative Markdown targets in newly created directories must resolve.
 for folder in [BASE,ROOT/'Composants/batterie/spektrum-g1-ic5']:
  for p in folder.rglob('*.md'):
   s=re.sub(r'```[\s\S]*?```','',p.read_text(encoding='utf-8'))
   for dest in re.findall(r'\]\(([^)]+)\)',s):
    if dest.startswith(('http:','https:','#','mailto:')):continue
    path=urllib.parse.unquote(dest.split('#')[0]);check('Local link: '+str(p.relative_to(ROOT))+' -> '+dest,(p.parent/path).exists())
 paths=[str((ROOT/'Composants'/m['relative_step_path']).relative_to(ROOT)).replace('\\','/') for m in cat['models']]
 result=subprocess.run(['git','--no-optional-locks','check-ignore','--stdin'],cwd=ROOT,input='\n'.join(paths)+'\n',encoding='utf-8',capture_output=True)
 check('All final STEP eligible for Git inclusion',result.returncode==1 and not result.stdout.strip(),dict(returncode=result.returncode,output=result.stdout,error=result.stderr))
 pdf=BASE/'notices/notice-cordon-principal-batterie-v3.pdf';d=pymupdf.open(pdf);meta=json.loads(pdf.with_suffix('.json').read_text(encoding='utf-8'))
 check('Eight notice pages',len(d)==8);check('Notice SHA256',sha(pdf)==meta['sha256']);check('PDF all pages visually inspected',meta['visual_review_complete'] and len(meta.get('reviewed_pages',[]))==8)
 for i,page in enumerate(d):
  text=page.get_text();check('Page has readable text '+str(i+1),len(text)>400 and '\ufffd' not in text)
  check('Page layout stays within paper '+str(i+1),all(b[0]>=0 and b[1]>=0 and b[2]<=page.rect.width+.1 and b[3]<=page.rect.height+.1 for b in page.get_text('blocks')))
  check('Rendered page exists '+str(i+1),(ROOT/meta['renders'][i]['render']).is_file())
 report=dict(checked_on='2026-10-15',checks_count=len(checks),all_passed=all(c['passed'] for c in checks),checks=checks,purchased=False,hardware_tested=False,GUI_tested=False,CADView_tested=False,remaining=['temperature/current and fuse coordination','select and verify separate IC5 charge lead','measure connector and wire lot','final chassis/camera/monitoring board phase'])
 (BASE/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PACKAGE',len(checks),'checks','PASS' if report['all_passed'] else 'FAIL',flush=True);assert report['all_passed']
if __name__=='__main__':main()
