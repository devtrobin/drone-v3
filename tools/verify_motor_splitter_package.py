"""Verify original vendor CAD, derived models, references, PDF and project links."""
from pathlib import Path
import json,hashlib,re,math,zipfile,subprocess,py_compile,sys
import pymupdf
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/repartition-moteurs'
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
        p=BASE/a['file'];assert p.exists() and sha(p)==a['sha256'] and p.stat().st_size==a['bytes'];archives+=1
        if p.suffix=='.pdf':assert p.read_bytes().startswith(b'%PDF')
    original=BASE/'3D/eriflex-ud80a-officiel.step';archive=BASE/'3D/originaux/nVent-UD80A-AP214-telechargement.bin'
    with zipfile.ZipFile(archive) as z:assert z.read('E10106602.step')==original.read_bytes()
    for p in BASE.rglob('*.md'):links(p)
    for f in ['Composants/README.md','ReadMe.md','Composants/protection-branches-moteurs/integration.md','Composants/protection-branches-moteurs/recherche-technique.md',
        'Composants/distribution-alimentation/integration.md','Composants/protection-surintensite/integration.md','Composants/protection-batterie/integration.md']:links(ROOT/f)
    cat=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'));assert cat['model_count']==5 and cat['original_preserved']
    for m in cat['models']:
        step=BASE/'3D'/m['file'];assert sha(step)==m['sha256'] and sha(BASE/'3D'/m['preview']['file'])==m['preview']['sha256']
        assert m['validation']['valid_after_reimport'] and m['native_vendor_cad']
        if 'generator' in m:
            assert sha(ROOT/m['generator'])==m['generator_sha256'] and m['original_sha256']==sha(original)
            assert m['validation']['bbox_error_mm']<.01 and m['validation']['volume_relative_error']<1e-4
        ignored=subprocess.run(['git','check-ignore',str(step.relative_to(ROOT))],cwd=ROOT,capture_output=True);assert ignored.returncode==1
    fc=json.loads((BASE/'3D/validation-freecad.json').read_text(encoding='utf-8'));assert fc['all_passed'] and len(fc['checks'])==5
    for c in fc['checks']:assert sha(BASE/'3D'/c['file'])==c['sha256']
    meta=BASE/'notices/notice-repartition-moteurs-v3.json';m=json.loads(meta.read_text(encoding='utf-8'))
    assert m['pages']==4 and m['visual_review_complete'] and sha(meta.with_suffix('.pdf'))==m['sha256']
    doc=pymupdf.open(meta.with_suffix('.pdf'));assert len(doc)==4 and all(len(p.get_text())>200 for p in doc)
    calc=json.loads((BASE/'calculs.json').read_text(encoding='utf-8'));rows={r['ambient_C']:r for r in calc['derating']}
    assert math.isclose(rows[60]['computed_IEC_allowance_A'],60) and math.isclose(rows[65]['computed_IEC_allowance_A'],53.6)
    assert not rows[75]['scenario40A_within_nominal'] and calc['ESC16AWG_nominal_mm2']<calc['small_output_min_mm2']<calc['holder_12AWG_nominal_mm2']
    for name in ['collect_motor_splitter_refs.py','collect_motor_splitter_details.py','inspect_motor_splitter_refs.py','find_motor_splitter_cad.py',
        'collect_motor_splitter_cad_options.py','download_motor_splitter_native_step.py','build_motor_splitter_step.py','validate_motor_splitter_freecad.py',
        'build_motor_splitter_data.py','build_motor_splitter_pdf.py','verify_motor_splitter_package.py','build_motor_fuse_data.py','build_battery_protection_docs.py','build_distribution_data.py']:
        py_compile.compile(str(ROOT/'tools'/name),doraise=True)
    report=dict(checked_on='2026-10-14',all_passed=True,archives=archives,native_STEP_matches_original_ZIP=True,step_models=5,
        freecad_headless_imports_valid=True,step_not_ignored=True,provenance_and_links_valid=True,pdf_pages=4,pdf_visual_review_complete=True,
        example_calculations_consistent=True,manufacturer_assembly_overlap_preserved=True,hardware_tested=False,
        wiring_qualified=False,large_terminal_IEC_UL_difference_resolved_on_received_lot=False,Amazon_fr_exact_offer_confirmed=False,
        RS_France_price_observed_TTC_EUR=21.13,shipping_included=False)
    (BASE/'validation-dossier.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print('PASS',archives,'archives; nativeSTEPintact,5STEP/FreeCADchecks,4PDFpagesreviewed,links/hashes/calculations; STEPnotignored',flush=True)
if __name__=='__main__':main()
