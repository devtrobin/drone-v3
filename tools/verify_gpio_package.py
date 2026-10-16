"""Artifact checks: links, native sources, geometry evidence and electrical table."""
from pathlib import Path
import json,re,hashlib,subprocess,math,zipfile,sys,py_compile
import pymupdf
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/connecteur-gpio';OUT=BASE/'3D'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def links(p):
 n=0
 for t in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
  if t.startswith(('https:','http:','#')):continue
  assert (p.parent/t.split('#')[0]).exists(),(str(p),t);n+=1
 return n
def main():
 sys.stdout.reconfigure(encoding='utf-8');report=BASE/'validation-dossier.json'
 report.write_text('{"all_passed":false,"status":"verification en cours"}\n',encoding='utf-8')
 for p in BASE.rglob('*.json'):read(p)
 nlinks=sum(links(p) for p in BASE.rglob('*.md'))
 for p in [ROOT/'Composants/README.md',ROOT/'ReadMe.md',ROOT/'Composants/raspberry-pi-5/integration.md']:
  nlinks+=links(p);assert 'connecteur-gpio' in p.read_text(encoding='utf-8')
 assets=read(BASE/'assets.json')['assets'];assert len({a['file'] for a in assets})==len(assets)
 archived=0
 for a in assets:
  if 'sha256' not in a:continue
  p=BASE/a['file'];assert p.stat().st_size==a['bytes'] and sha(p)==a['sha256']
  if a['status']=='downloaded':archived+=1
  if p.suffix=='.pdf':assert p.read_bytes().startswith(b'%PDF')
 native=read(OUT/'source-native.json')
 assert native['native_vendor_cad'] and not native['geometry_modified'] and native['valid']
 assert sha(OUT/native['file'])==native['sha256'] and sha(OUT/native['archive'])==native['archive_sha256']
 with zipfile.ZipFile(OUT/native['archive']) as z:assert z.read(native['source_zip_member'])==(OUT/native['file']).read_bytes()
 cat=read(OUT/'catalogue.json');prov=read(OUT/'provenance.json');assert cat['model_count']==len(cat['models'])==4
 assert prov['models']==cat['models'] and prov['source_manifest_sha256']==sha(BASE/'assets.json')
 for m in cat['models']:
  p=OUT/m['file'];assert p.stat().st_size==m['bytes'] and sha(p)==m['sha256']
  assert sha(OUT/m['preview']['file'])==m['preview']['sha256'] and sha(ROOT/m['generator'])==m['generator_sha256']
  assert read(p.with_suffix('.json'))==m and m['source_manifest_sha256']==sha(BASE/'assets.json')
  v=m['validation'];assert v['valid_after_reimport'] and v['bbox_error_mm']<.01 and v['volume_relative_error']<1e-4
  assert m['unit']=='mm' and not m['hardware_measured']
  assert subprocess.run(['git','check-ignore',str(p.relative_to(ROOT))],cwd=ROOT,capture_output=True).returncode==1
 params=cat['models'][-1]['parameters'];assert len(params['populated_pins'])==15 and len(params['wire_continuity'])==15
 assert all(r['contact_housing_overlap_mm3']<1e-6 for r in params['contact_housing_reconstruction_overlap'])
 assert all(r['overlap_mm3']<1e-6 for r in params['wire_close_pair_checks'])
 for c in params['wire_continuity']:
  assert c['core_solids']==c['sheath_solids']==1 and c['centreline_probes']==65 and c['sheath_probes']==61
  assert 2.54<=c['stripped_length_study_mm']<=3.17
 fc=read(OUT/'validation-freecad.json');assert fc['all_passed'] and len(fc['checks'])==4
 lookup={m['file']:m for m in cat['models']}
 for c in fc['checks']:
  assert c['passed'] and c['valid'] and c['solids_closed'] and c['sha256']==lookup[c['file']]['sha256']
  assert c['bbox_error_mm']<.01 and c['volume_relative_error']<1e-4
 pins=read(BASE/'brochage.json');assert len(pins['pins'])==15 and len(pins['unused_pins'])==25
 assert len({p['physical_pin'] for p in pins['pins']})==15
 signals={p['signal']:p['physical_pin'] for p in pins['pins']}
 assert signals['PWM_ESC_G']==32 and signals['PWM_ESC_D']==33 and signals['PWM_SERVO']==12
 assert signals['WARN1']==11 and signals['WARN2']==13 and signals['DONE']==15
 assert not pins['ESC_3V3_input_validated'] and pins['servo_BEC6V_not_connected_to_GPIO']
 bom=read(BASE/'nomenclature.json');assert [p['quantity'] for p in bom['parts']]==[1,20,1]
 assert math.isclose(sum(p['quantity']*p['observed_USD_unit_price'] for p in bom['parts']),37.90)
 assert bom['french_total_EUR_TTC'] is None and not bom['purchased']
 calc=read(BASE/'calculs.json');R=.01724/.326*.15*(1/2+1/4);assert math.isclose(calc['wire_loop_R_ohm'],R)
 for c in calc['rows']:
  assert math.isclose(c['loop_resistance_ohm'],R+c['contact_resistance_assumed_ohm']*.75)
  assert math.isclose(c['drop_V'],5*c['loop_resistance_ohm']) and math.isclose(c['loss_W'],25*c['loop_resistance_ohm'])
 assert math.isclose(calc['planar_gap_study_mm'],.7227) and not calc['installed_fit_verified']
 meta=BASE/'notices/notice-connecteur-gpio-v3.json';m=read(meta)
 assert m['visual_review_complete'] and m['visually_reviewed_pages']==list(range(1,7)) and m['pages']==6
 assert m['sha256']==sha(meta.with_suffix('.pdf'))
 pdf=pymupdf.open(meta.with_suffix('.pdf'));assert len(pdf)==6 and all(len(p.get_text())>600 for p in pdf)
 assert sum(1 for p in pdf for a in p.links() if a.get('uri'))>=8
 for filename in ['collect_gpio_refs.py','collect_gpio_more.py','inspect_gpio_refs.py','prepare_gpio_native.py',
                  'build_gpio_step.py','build_gpio_data.py','build_gpio_pdf.py','validate_gpio_freecad.py','verify_gpio_package.py']:
  py_compile.compile(str(ROOT/'tools'/filename),doraise=True)
 result=dict(checked_on='2026-10-14',all_passed=True,native_housing_original_preserved=True,STEP_models=4,
  FreeCAD_headless_valid=True,STEP_not_ignored=True,archive_files_hash_verified=archived,local_links_verified=nlinks,
  notice_pages=6,notice_visual_review_complete=True,populated_contacts=15,wire_continuity_verified=True,
  wire_and_contact_geometry_collisions_checked=True,Amazon_exact_offer_verified=False,price_EUR_TTC=None,
  hardware_tested=False,Pi_5A_qualified=False,ESC_3V3_input_qualified=False,installed_fit_verified=False,
  RC_end_connectors_final=False)
 report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
