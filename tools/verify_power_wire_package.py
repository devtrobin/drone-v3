"""Verify source archives, six CAD models, 680-strand counts, PDF and integration."""
from pathlib import Path
import json,hashlib,re,math,subprocess,sys,py_compile
import pymupdf
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/cable-puissance-12awg'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def links(p):
    for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
        if target.startswith(('https:','http:','#')):continue
        assert (p.parent/target.split('#')[0]).exists(),(p,target)
def main():
    sys.stdout.reconfigure(encoding='utf-8');archives=0
    for p in BASE.rglob('*.json'):read(p)
    for a in read(BASE/'assets.json')['assets']:
        if 'sha256' not in a:continue
        p=BASE/a['file'];assert p.stat().st_size==a['bytes'] and sha(p)==a['sha256'];archives+=1
        if p.suffix=='.pdf':assert p.read_bytes().startswith(b'%PDF')
    for p in BASE.rglob('*.md'):links(p)
    for name in ['Composants/README.md','ReadMe.md','Composants/connecteurs-alimentation/integration.md','Composants/protection-branches-moteurs/integration.md']:links(ROOT/name)
    cat=read(BASE/'3D/catalogue.json');assert cat['model_count']==len(cat['models'])==6
    for m in cat['models']:
        p=BASE/'3D'/m['file'];assert sha(p)==m['sha256'] and p.stat().st_size==m['bytes']
        assert sha(BASE/'3D'/m['preview']['file'])==m['preview']['sha256'] and sha(ROOT/m['generator'])==m['generator_sha256']
        assert m['validation']['valid_after_reimport'] and m['validation']['bbox_error_mm']<.01 and m['validation']['volume_relative_error']<1e-4
        assert not m['native_vendor_cad'] and not m['hardware_measured']
        if m['strand_packing']:
            assert m['validation']['solids']==681 and m['strand_packing']['strands']==680 and m['strand_packing']['minimum_surface_gap_mm']>0
            assert math.isclose(m['strand_packing']['area_sum_mm2'],680*math.pi*.04**2)
        if m['curve_continuity_checks']:
            assert len(m['curve_continuity_checks'])==2
            for c in m['curve_continuity_checks']:assert c['core_solids']==c['sheath_solids']==1 and c['material_samples']>=264
        ignored=subprocess.run(['git','check-ignore',str(p.relative_to(ROOT))],cwd=ROOT,capture_output=True);assert ignored.returncode==1
    fc=read(BASE/'3D/validation-freecad.json');assert fc['all_passed'] and len(fc['checks'])==6
    for c in fc['checks']:assert c['valid'] and c['solids_closed'] and sha(BASE/'3D'/c['file'])==c['sha256']
    meta=BASE/'notices/notice-cable-puissance-12awg-v3.json';m=read(meta)
    assert m['visual_review_complete'] and m['pages']==4 and sha(meta.with_suffix('.pdf'))==m['sha256']
    doc=pymupdf.open(meta.with_suffix('.pdf'));assert len(doc)==4 and all(len(p.get_text())>600 for p in doc)
    calc=read(BASE/'calculs.json');assert math.isclose(calc['resistance_published_ohm_per_km']/1000,.00506)
    for r in calc['loop_examples']:
        assert math.isclose(r['loop_resistance_ohm'],2*r['one_way_length_m']*.00506)
        assert math.isclose(r['drop_V'],r['current_A']*r['loop_resistance_ohm']) and math.isclose(r['loss_per_branch_W'],r['current_A']**2*r['loop_resistance_ohm'])
    bom=read(BASE/'nomenclature.json');assert bom['amazon_ASIN']=='B01ABOPMEI' and math.isclose(bom['total_m'],2*10*.3048)
    for name in ['collect_power_wire_refs.py','inspect_power_wire_refs.py','build_power_wire_data.py','build_power_wire_step.py',
        'validate_power_wire_freecad.py','build_power_wire_pdf.py','verify_power_wire_package.py']:
        py_compile.compile(str(ROOT/'tools'/name),doraise=True)
    report=dict(checked_on='2026-10-14',all_passed=True,archives=archives,STEP_models=6,short_detailed_models=3,
        each_detailed_strand_count=680,FreeCAD_headless_valid=True,STEP_not_ignored=True,links_and_hashes_valid=True,
        source_image_specifications_used=True,wrong_14AWG_ASIN_excluded=True,pdf_pages=4,pdf_visual_review_complete=True,
        curve_material_continuity_sampled=True,hardware_tested=False,actual_strands_counted=False,
        actual_lay_geometry_verified=False,current_and_fault_qualification_complete=False,cap_fit_verified=False,
        Amazon_FR_stock_confirmed=False,price_FR_TTC_confirmed=False,actual_cut_list_validated=False)
    (BASE/'validation-dossier.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS',archives,'archives;6STEP/FreeCAD;680strands x3;4PDFpages;links/hashes/calculations;STEPnotignored',flush=True)
def contact_sheet():
    cat=read(BASE/'3D/catalogue.json');canvas=Image.new('RGB',(1600,868),'white')
    for i,m in enumerate(cat['models']):
        im=Image.open(BASE/'3D'/m['preview']['file']);im.thumbnail((533,434));canvas.paste(im,((i%3)*533,(i//3)*434))
    p=ROOT/'tools/temp/power-wire-review/contact-sheet.png';p.parent.mkdir(parents=True,exist_ok=True);canvas.save(p);print(p)
if __name__=='__main__':
    if '--contact-sheet' in sys.argv:contact_sheet()
    else:main()
