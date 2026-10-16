"""Check the deliverable, source integrity, CAD controls, links and calculations."""
from pathlib import Path
import json,hashlib,re,math,subprocess,sys,py_compile
import pymupdf
from build_harness_data import PARTS
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants';COMMON=BASE/'faisceau-puissance'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def links(p):
    for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
        if target.startswith(('https:','http:','#')):continue
        assert (p.parent/target.split('#')[0]).exists(),(p,target)
def main():
    sys.stdout.reconfigure(encoding='utf-8');paths=[COMMON,*[BASE/i['folder'] for i in PARTS]];archives=0;pdfsources=0
    (COMMON/'validation-dossier.json').write_text(json.dumps(dict(all_passed=False,status='verification en cours'),indent=2)+'\n',encoding='utf-8')
    for root in paths:
        for p in root.rglob('*.json'):read(p)
        for p in root.rglob('*.md'):links(p)
    for p in [ROOT/'ReadMe.md',BASE/'README.md']:
        links(p);assert 'faisceau-puissance/README.md' in p.read_text(encoding='utf-8')
    for p in [BASE/'cosses-puissance/README.md',BASE/'maintien-faisceau/README.md']:links(p)
    for folder in ['cable-puissance-12awg','connecteurs-alimentation','protection-branches-moteurs','distribution-alimentation','repartition-moteurs','protection-surintensite']:
        p=BASE/folder/'integration.md'
        if not p.exists():p=BASE/folder/'README.md'
        links(p);assert 'faisceau-puissance' in p.read_text(encoding='utf-8')
    assets=read(COMMON/'assets.json')['assets'];assert len({a['file'] for a in assets})==len(assets)
    for a in assets:
        if 'sha256' not in a:continue
        p=COMMON/a['file'];assert p.stat().st_size==a['bytes'] and sha(p)==a['sha256']
        if a['status']=='downloaded':archives+=1
        if p.suffix=='.pdf':assert p.read_bytes().startswith(b'%PDF');pdfsources+=1
    cat=read(COMMON/'3D/catalogue.json');assert cat['model_count']==len(cat['models'])==14 and cat['folder_count']==8
    for m in cat['models']:
        out=BASE/m['folder']/'3D';p=out/m['file'];assert sha(p)==m['sha256'] and p.stat().st_size==m['bytes']
        assert sha(out/m['preview']['file'])==m['preview']['sha256'] and sha(ROOT/m['generator'])==m['generator_sha256']
        assert m['validation']['valid_after_reimport'] and m['validation']['bbox_error_mm']<.01 and m['validation']['volume_relative_error']<1e-4
        assert not m['native_vendor_cad'] and not m['hardware_measured']
        assert read(out/p.with_suffix('.json').name)['sha256']==m['sha256']
        ignored=subprocess.run(['git','check-ignore',str(p.relative_to(ROOT))],cwd=ROOT,capture_output=True);assert ignored.returncode==1,(p,ignored.stdout)
    for item in PARTS:
        src=read(BASE/item['folder']/'sources.json');assert not src['selection']['amazon_FR_verified'] and src['selection']['price_EUR_TTC'] is None
        assert (BASE/item['folder']/'3D/provenance.json').exists()
    fc=read(COMMON/'3D/validation-freecad.json');assert fc['all_passed'] and len(fc['checks'])==14
    for c in fc['checks']:
        assert c['valid'] and c['solids_closed'] and sha(BASE/c['folder']/'3D'/c['file'])==c['sha256'] and c['bbox_error_mm']<.01
    meta=COMMON/'notices/notice-faisceau-puissance-v3.json';m=read(meta);assert m['visual_review_complete'] and m['pages']==8 and sha(meta.with_suffix('.pdf'))==m['sha256']
    doc=pymupdf.open(meta.with_suffix('.pdf'));assert len(doc)==8 and all(len(p.get_text())>600 for p in doc)
    assert sum(1 for p in doc for a in p.links() if a.get('uri'))>=8
    calc=read(COMMON/'calculs.json');I=40+25/(6.4*.9)+.05;assert math.isclose(calc['main_current_study_A'],I)
    for row in calc['loops']:
        R=2*row['one_way_length_m']*.01724/6;assert math.isclose(row['loop_resistance_ohm'],R)
        assert math.isclose(row['drop_V'],I*R) and math.isclose(row['loss_W'],I*I*R)
    for c in calc['stud_passages']:assert c['hole_mm']>c['stud_major_nominal_mm']
    bom=read(COMMON/'nomenclature.json');assert len(bom['parts'])==8 and len(bom['connections'])==9 and bom['exact_total_EUR'] is None
    lookup={p['id']:p for p in bom['parts']};assert lookup['klauke95r5']['quantity']==5 and lookup['klauke95r5']['mandatory']==4
    assert lookup['ancor309203']['quantity']==2 and lookup['klauke95r4']['quantity']==2 and lookup['ancor312303']['quantity']==3
    assert lookup['teatum8']['reference'].endswith('(NB11802001)') and '111-01919' in lookup['htt18r']['reference']
    assert '4,7' in lookup['auprotec6']['spec'] and '+70' in lookup['auprotec6']['spec']
    for name in ['collect_harness_refs.py','collect_harness_more.py','inspect_harness_refs.py','build_harness_step.py','build_harness_data.py',
        'harness_text.py','validate_harness_freecad.py','build_harness_pdf.py','verify_harness_package.py']:
        py_compile.compile(str(ROOT/'tools'/name),doraise=True)
    report=dict(checked_on='2026-10-14',all_passed=True,component_dossiers=8,STEP_models=14,FreeCAD_headless_valid=True,
        original_archives=archives,pdf_source_documents=pdfsources,pdf_notice_pages=8,pdf_visual_review_complete=True,
        hashes_links_calculations_valid=True,STEP_not_ignored=True,source_dimensions_distinguished_from_estimates=True,
        current_qualified=False,hardware_tested=False,actual_cut_list_validated=False,battery_interface_final=False,
        exact_Amazon_FR_offers_verified=False,price_FR_TTC_confirmed=False,tool_and_conductor_pairing_qualified=False)
    (COMMON/'validation-dossier.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS:8 dossiers;14STEP/FreeCAD;8pagesPDF;'+str(pdfsources)+'PDFsources;hashes/links/calculations;STEPnotignored',flush=True)
if __name__=='__main__':main()
