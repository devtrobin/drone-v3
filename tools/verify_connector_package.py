"""Package checks: source hashes, links, CAD import results, dimensions, PDF and Git."""
from pathlib import Path
import json,hashlib,re,math,subprocess,py_compile,sys
import pymupdf
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/connecteurs-alimentation'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def links(p):
    for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
        if link.startswith(('http:','https:','#')):continue
        assert (p.parent/link.split('#')[0]).exists(),(p,link)
def main():
    sys.stdout.reconfigure(encoding='utf-8');archives=0
    for p in BASE.rglob('*.json'):json.loads(p.read_text(encoding='utf-8'))
    for a in json.loads((BASE/'assets.json').read_text(encoding='utf-8'))['assets']:
        if 'sha256' not in a:continue
        p=BASE/a['file'];assert sha(p)==a['sha256'] and p.stat().st_size==a['bytes'];archives+=1
        if p.suffix=='.pdf':assert p.read_bytes().startswith(b'%PDF')
    for p in BASE.rglob('*.md'):links(p)
    for f in ['Composants/README.md','ReadMe.md','Composants/protection-branches-moteurs/integration.md',
        'Composants/repartition-moteurs/integration.md','Composants/batterie/README.md']:links(ROOT/f)
    cat=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'));assert cat['model_count']==len(cat['models'])==8
    for m in cat['models']:
        step=BASE/'3D'/m['file'];assert sha(step)==m['sha256'] and step.stat().st_size==m['bytes']
        assert sha(BASE/'3D'/m['preview']['file'])==m['preview']['sha256']
        assert sha(ROOT/m['generator'])==m['generator_sha256']
        assert not m['native_vendor_cad'] and not m['hardware_measured'] and m['validation']['valid_after_reimport']
        assert m['validation']['bbox_error_mm']<.01 and m['validation']['volume_relative_error']<1e-4
        ignored=subprocess.run(['git','check-ignore',str(step.relative_to(ROOT))],cwd=ROOT,capture_output=True);assert ignored.returncode==1
    dims={m['file']:m['bounds_mm'] for m in cat['models']}
    for name,length in [('amass-xt60h-f-detaille.step',24.95),('amass-xt60h-m-detaille.step',23.85)]:
        b=dims[name];assert math.isclose(b['zmax']-b['zmin'],length,abs_tol=1e-5)
        assert math.isclose(b['xmax']-b['xmin'],16.4,abs_tol=1e-5) and math.isclose(b['ymax']-b['ymin'],9.2,abs_tol=1e-5)
    pair=next(m for m in cat['models'] if 'accouplee' in m['file']);assert pair['mating_overlap_check']==[]
    wired=next(m for m in cat['models'] if 'cable' in m['file'])
    assert len(wired['wire_continuity_checks'])==2
    for c in wired['wire_continuity_checks']:
        assert c['core_solids']==c['jacket_solids']==1 and c['core_material_samples']>=120 and c['jacket_material_samples']>=120 and c['bond_gap_mm']==0
    fc=json.loads((BASE/'3D/validation-freecad.json').read_text(encoding='utf-8'));assert fc['all_passed'] and len(fc['checks'])==8
    for c in fc['checks']:assert sha(BASE/'3D'/c['file'])==c['sha256'] and c['valid'] and c['solids_closed']
    meta=BASE/'notices/notice-connecteurs-xt60h-v3.json';m=json.loads(meta.read_text(encoding='utf-8'))
    assert m['pages']==4 and m['visual_review_complete'] and sha(meta.with_suffix('.pdf'))==m['sha256']
    doc=pymupdf.open(meta.with_suffix('.pdf'));assert len(doc)==4 and all(len(p.get_text())>600 for p in doc)
    calc=json.loads((BASE/'calculs.json').read_text(encoding='utf-8'))
    assert math.isclose(calc['common_battery_current_scenario_A'],40+25/(6.4*.9)+.05)
    for r in calc['contact_loss_examples']:
        assert math.isclose(r['loop_drop_V'],2*r['current_A']*r['resistance_per_pole_assumed_ohm'])
        assert math.isclose(r['loop_loss_W'],2*r['current_A']**2*r['resistance_per_pole_assumed_ohm'])
    bom=json.loads((BASE/'nomenclature.json').read_text(encoding='utf-8'));assert bom['vehicle_need'][0]['quantity']==2 and bom['vehicle_need'][1]['additional_quantity']==0
    for name in ['collect_connector_refs.py','build_connector_data.py','build_connector_step.py','validate_connector_freecad.py',
        'build_connector_pdf.py','verify_connector_package.py','build_motor_fuse_data.py']:py_compile.compile(str(ROOT/'tools'/name),doraise=True)
    report=dict(checked_on='2026-10-14',all_passed=True,archives=archives,models=8,native_vendor_CAD=False,
        colours_and_roundtrip_valid=True,FreeCAD_headless_valid=True,GUI_import_tested=False,STEP_not_ignored=True,
        links_and_hashes_valid=True,current_envelopes_match_catalogue_2026=True,mated_pair_no_volume_overlap=True,
        illustrative_wires_continuity_sampled=True,pdf_pages=4,pdf_visual_review_complete=True,hardware_tested=False,
        actual_lot_dimensions_verified=False,Amazon_FR_availability_confirmed=False,prices_confirmed=False,
        individual_current_limit_enforced=False,wiring_and_faults_qualified=False,common_battery_XT60_qualified=False)
    (BASE/'validation-dossier.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS',archives,'archives;8STEP/FreeCAD;4PDFpages;links/hashes/dimensions/calculations;STEPnotignored',flush=True)
def contact_sheet():
    cat=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'));canvas=Image.new('RGB',(2080,846),'white')
    for i,m in enumerate(cat['models']):
        im=Image.open(BASE/'3D'/m['preview']['file']);im.thumbnail((520,423));canvas.paste(im,((i%4)*520,(i//4)*423))
    p=ROOT/'tools/temp/connectors-review/contact-sheet.png';p.parent.mkdir(parents=True,exist_ok=True);canvas.save(p);print(p)
if __name__=='__main__':
    if '--contact-sheet' in sys.argv:contact_sheet()
    else:main()
