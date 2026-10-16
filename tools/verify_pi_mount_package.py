"""Dossier consistency: links, source/CAD hashes, inventory, PDF and Git rules."""
from pathlib import Path
import json,re,hashlib,sys,subprocess
import pymupdf

ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/fixations-raspberry-pi-5'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 sys.stdout.reconfigure(encoding='utf-8');checks=[]
 def check(name,passed,detail=None):
  checks.append(dict(check=name,passed=bool(passed),detail=detail));assert passed,(name,detail)
 nom=read(BASE/'nomenclature.json');cat=read(BASE/'3D/catalogue.json');fc=read(BASE/'3D/validation-freecad.json');meta=read(BASE/'notices/notice-fixations-pi-5-v3.json')
 check('inventory_335',sum(x['bought_in_one_kit'] for x in nom['parts'])==335)
 check('allocation_20',sum(x['used_in_study'] for x in nom['parts'])==20)
 check('reserves_315',sum(x['reserve'] for x in nom['parts'])==315)
 check('full_kit_cost',nom['kit']['price_eur_vat_included']==9.98 and nom['kit']['quantity_to_buy']==1)
 check('chassis_deferred',read(BASE/'calculs.json')['chassis_final_component'] and not nom['final_height_selected'])
 check('STEP_count',len(cat['models'])==15 and len(list((BASE/'3D').glob('*.step')))==15)
 check('FreeCAD_all',fc['all_passed'] and len(fc['checks'])==15)
 for m in cat['models']:
  p=BASE/'3D'/m['file'];check('CAD_hash_'+m['file'],sha(p)==m['sha256'])
  check('preview_hash_'+m['file'],sha(BASE/'3D'/m['preview']['file'])==m['preview']['sha256'])
  check('dated_metadata_'+m['file'],m['generated_on']=='2026-10-14')
  check('closed_solids_'+m['file'],next(x for x in fc['checks'] if x['file']==m['file'])['solids_closed'])
 for a in read(BASE/'assets.json')['assets']:
  check('source_'+a['file'],a['status']=='downloaded' and sha(BASE/a['file'])==a['sha256'])
 for path in BASE.rglob('*.json'):read(path)
 for path in [*BASE.rglob('*.md'),ROOT/'Composants/README.md',ROOT/'ReadMe.md']:
  for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
   link=link.strip('<>');link=link.split('#')[0]
   if not link or re.match(r'^[a-zA-Z]+:',link):continue
   check('link_'+str(path.relative_to(ROOT))+'_'+link,(path.parent/link).exists())
 pdf=BASE/'notices/notice-fixations-pi-5-v3.pdf';doc=pymupdf.open(pdf)
 check('PDF_6_pages',len(doc)==6)
 check('PDF_hash',sha(pdf)==meta['sha256'])
 check('PDF_visual_review',meta['visual_review_complete'])
 check('PDF_no_body_footer_collision',all(p['body_bottom_pt']<767 for p in meta['renders']),[p['body_bottom_pt'] for p in meta['renders']])
 urls=[link['uri'] for page in doc for link in page.get_links() if 'uri' in link]
 check('PDF_Amazon_link','https://www.amazon.fr/dp/B0DCS5C7SN' in urls)
 check('PDF_original_plan_link','https://datasheets.raspberrypi.com/rpi5/raspberry-pi-5-mechanical-drawing.pdf' in urls)
 check('no_candidate_STEP',not list((BASE/'3D').glob('*.candidate')))
 files=[str(p.relative_to(ROOT)).replace('\\','/') for p in BASE.rglob('*') if p.is_file()]
 proc=subprocess.run(['git','--no-optional-locks','check-ignore',*files],cwd=ROOT,capture_output=True,text=True)
 check('component_not_gitignored',proc.returncode==1 and not proc.stdout.strip(),proc.stdout.strip())
 result=dict(checked_on='2026-10-14',all_passed=all(c['passed'] for c in checks),checks=checks,
  hardware_tested=False,GUI_tested=False,chassis_authored=False)
 (BASE/'validation-dossier.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('PACKAGE PASS',len(checks),'checks, 15 STEP, 6 PDF pages',flush=True)

if __name__=='__main__':main()
