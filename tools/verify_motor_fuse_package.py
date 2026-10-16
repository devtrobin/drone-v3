"""Verify motor fuse artifacts, links, provenance and independent CAD reports."""
from pathlib import Path
import hashlib,json,re,sys,subprocess,py_compile,math
import pymupdf
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/protection-branches-moteurs'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check_links(p):
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
        if a.get('origin'):assert sha(ROOT/a['origin'])==a['sha256']
    for p in BASE.rglob('*.md'):check_links(p)
    for relative in ['Composants/README.md','ReadMe.md','Composants/distribution-alimentation/integration.md',
        'Composants/protection-surintensite/integration.md','Composants/protection-batterie/integration.md']:check_links(ROOT/relative)
    cat=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'));assert cat['model_count']==5
    for m in cat['models']:
        folder=ROOT/'Composants'/m['folder']/'3D';p=folder/m['file']
        assert sha(p)==m['sha256'] and sha(folder/m['preview']['file'])==m['preview']['sha256']
        assert m['validation']['valid_after_reimport'] and not m['validation']['pairwise_material_overlaps']
        assert m['generator_sha256']==sha(ROOT/m['generator'])
        assert m['reused_geometry_generator_sha256']==sha(ROOT/m['reused_geometry_generator'])
        ignored=subprocess.run(['git','check-ignore',str(p.relative_to(ROOT))],cwd=ROOT,capture_output=True)
        assert ignored.returncode==1,('STEP ignored or Git error',p,ignored.stdout)
    fc=json.loads((BASE/'3D/validation-freecad.json').read_text(encoding='utf-8'));assert fc['all_passed'] and len(fc['checks'])==5
    for c in fc['checks']:assert sha(ROOT/'Composants'/c['folder']/'3D'/c['file'])==c['sha256']
    mp=BASE/'notices/notice-protection-branches-moteurs-v3.json';meta=json.loads(mp.read_text(encoding='utf-8'))
    assert sha(mp.with_suffix('.pdf'))==meta['sha256'] and meta['pages']==5 and meta['visual_review_complete']
    doc=pymupdf.open(mp.with_suffix('.pdf'));assert len(doc)==5 and all(len(p.get_text())>200 for p in doc)
    calc=json.loads((BASE/'calculs.json').read_text(encoding='utf-8'))
    assert calc['derating_A']['25'][1]<20<calc['derating_A']['30'][1]
    assert math.isclose(calc['two_fuses_at20A_loss_W'],1.576) and math.isclose(calc['example_added_4mm2_loop']['loss20A_W'],.7)
    assert [r['current_A'] for r in calc['time_current_table']]==[33,40.5,48,60,105,180]
    for file in ['collect_motor_fuse_refs.py','build_motor_fuse_data.py','build_motor_fuse_step.py','inspect_motor_fuse_sources.py',
        'build_motor_fuse_pdf.py','validate_motor_fuse_freecad.py','verify_motor_fuse_package.py','build_battery_protection_docs.py','build_distribution_data.py']:
        py_compile.compile(str(ROOT/'tools'/file),doraise=True)
    report=dict(checked_on='2026-10-14',all_passed=True,archives=archives,step_models=5,pdf_pages=5,pdf_visual_review_complete=True,
        links_and_hashes_valid=True,step_not_ignored=True,freecad_headless_valid=True,calculation_examples_consistent=True,
        hardware_tested=False,original_ESC16AWG_protection_validated=False,prospective_fault_current_validated=False,
        selectivity_validated=False,amazon_fr_offers_confirmed=False)
    (BASE/'validation-dossier.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS',archives,'archives,5STEP/previews/FreeCADchecks,5reviewedPDFpages,links,provenance andcalculationexamples; STEPnotignored',flush=True)
if __name__=='__main__':main()
