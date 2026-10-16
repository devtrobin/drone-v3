"""Verify SC1148 deliverables, archival integrity and existing CAD evidence."""
from pathlib import Path
import hashlib,json,math,re,subprocess,sys,py_compile
import pymupdf

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'Composants/refroidissement-raspberry-pi-5'
OUT=BASE/'3D'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def links(p):
    count=0
    for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
        if target.startswith(('http:','https:','#')):continue
        assert (p.parent/target.split('#')[0]).exists(),(str(p),target)
        count+=1
    return count
def main():
    sys.stdout.reconfigure(encoding='utf-8')
    report=BASE/'validation-dossier.json'
    dump(report,dict(all_passed=False,status='verification en cours'))
    for p in BASE.rglob('*.json'):read(p)
    local_links=sum(links(p) for p in BASE.rglob('*.md'))
    for p in [ROOT/'ReadMe.md',ROOT/'Composants/README.md',
              ROOT/'Composants/raspberry-pi-5/README.md',ROOT/'Composants/raspberry-pi-5/integration.md']:
        local_links+=links(p)
        assert 'refroidissement-raspberry-pi-5' in p.read_text(encoding='utf-8')
    for line in (OUT/'README.md').read_text(encoding='utf-8').splitlines():
        if line.startswith('|'):assert line.count('|')==5,line
    assets=read(BASE/'assets.json')['assets']
    assert len({a['file'] for a in assets})==len(assets)
    archived=0;pdf_originals=[]
    for a in assets:
        if 'sha256' not in a:continue
        p=BASE/a['file']
        assert p.stat().st_size==a['bytes'] and sha(p)==a['sha256'],a['file']
        archived+=1
        if p.suffix=='.pdf':
            assert p.read_bytes().startswith(b'%PDF')
            pdf_originals.append(a['sha256'])
    assert len(pdf_originals)==5 and len(set(pdf_originals))==2
    offer=read(BASE/'achat-amazon.json')
    assert offer['manufacturer_part']=='SC1148' and offer['ASIN']=='B0CLXZBR5P'
    assert offer['price_displayed_EUR']==6.99 and offer['VAT_included_page_statement']
    assert '5 exemplaire' in offer['availability_displayed'] and 'Raspberry Pi' in offer['title']
    assert sha(BASE/offer['source_file'])==offer['source_sha256']
    assert not offer['order_made'] and not offer['shipping_cost_guaranteed']
    cat=read(OUT/'catalogue.json');prov=read(OUT/'provenance.json')
    assert cat['model_count']==len(cat['models'])==4 and prov['models']==cat['models']
    assert prov['source_manifest_sha256']==sha(BASE/'assets.json') and not prov['native_vendor_cad']
    for m in cat['models']:
        p=OUT/m['file'];assert p.stat().st_size==m['bytes'] and sha(p)==m['sha256']
        assert p.read_bytes().startswith(b'ISO-10303-21;')
        assert sha(OUT/m['preview']['file'])==m['preview']['sha256']
        assert sha(ROOT/m['generator'])==m['generator_sha256']
        assert sha(BASE/'assets.json')==m['source_manifest_sha256']
        assert read(p.with_suffix('.json'))==m
        v=m['validation']
        assert v['valid_after_reimport'] and v['bbox_error_mm']<.01 and v['volume_relative_error']<1e-4
        assert not m['native_vendor_cad'] and not m['hardware_measured'] and m['unit']=='mm'
        assert len(m['estimates_and_limitations'])>=10 and m['parameters']['physical_pair_overlaps']==[]
        ignored=subprocess.run(['git','check-ignore',str(p.relative_to(ROOT))],cwd=ROOT,capture_output=True)
        assert ignored.returncode==1,(str(p),ignored.stdout)
    mainmodel=cat['models'][0];params=mainmodel['parameters']
    cables=params['cable_continuity_checks']
    assert cables==mainmodel['wire_continuity_checks'] and len(cables)==4
    for c in cables:
        assert c['core_solids']==c['sheath_solids']==1 and c['curve_spans']==2
        assert c['material_samples']==192 and c['centreline_samples']==82 and c['tangent_continuity']
    assert len(params['cable_pair_overlap_checks'])==6
    assert all(c['overlap_mm3']==0 for c in params['cable_pair_overlap_checks'])
    light=cat['models'][3]
    assert light['bytes']<3_000_000 and len(light['parameters']['omitted_details'])==3
    fc=read(OUT/'validation-freecad.json')
    assert fc['all_passed'] and len(fc['checks'])==4 and fc['mode']=='headless'
    modelmap={m['file']:m for m in cat['models']}
    for c in fc['checks']:
        m=modelmap[c['file']]
        assert c['passed'] and c['valid'] and c['solids_closed'] and c['sha256']==m['sha256']
        assert c['solids']==m['validation']['solids'] and c['bbox_error_mm']<.01 and c['volume_relative_error']<1e-4
    meta=BASE/'notices/notice-active-cooler-pi5-v3.json';pdfmeta=read(meta)
    assert pdfmeta['visual_review_complete'] and pdfmeta['visually_reviewed_pages']==list(range(1,7))
    assert pdfmeta['sha256']==sha(meta.with_suffix('.pdf')) and pdfmeta['pages']==6
    pdf=pymupdf.open(meta.with_suffix('.pdf'))
    assert len(pdf)==6 and all(len(p.get_text())>600 for p in pdf)
    assert sum(1 for p in pdf for a in p.links() if a.get('uri'))>=8
    for p in pdfmeta['renders']:assert (ROOT/p['render']).exists()
    calc=read(BASE/'calculs.json')
    assert calc['example_only'] and not calc['rated_fan_current_claimed'] and calc['measured_fan_current_A'] is None
    for r in calc['current_examples']:
        P=5*r['fan_current_example_A']
        assert math.isclose(r['fan_power_W'],P) and math.isclose(r['energy20min_Wh'],P/3)
        assert math.isclose(r['energy45min_Wh'],P*.75)
    src=read(BASE/'sources.json')
    assert src['electrical']['current_active_cooler_not_published_in_brief']
    assert src['electrical']['case_fan_60mA_not_transferred_to_ActiveCooler']
    assert not src['mechanical_reference_mm']['production_dimensions'] and not src['hardware_tested']
    bom=read(BASE/'nomenclature.json')
    assert bom['quantity']==1 and bom['price_displayed_EUR']==6.99 and not bom['purchase_made']
    for name in ['collect_pi_cooler_refs.py','collect_pi_cooler_more.py','inspect_pi_cooler_refs.py',
                 'inspect_pi_cooler_purchase.py','build_pi_cooler_step.py','validate_pi_cooler_freecad.py',
                 'build_pi_cooler_data.py','pi_cooler_text.py','build_pi_cooler_pdf.py','verify_pi_cooler_package.py']:
        py_compile.compile(str(ROOT/'tools'/name),doraise=True)
    result=dict(checked_on='2026-10-14',all_passed=True,STEP_models=4,FreeCAD_headless_valid=True,
        STEP_not_ignored=True,archival_files_hash_verified=archived,PDF_source_files=5,unique_PDF_source_contents=2,
        notice_pages=6,notice_visual_review_complete=True,local_links_verified=local_links,
        cable_continuity_verified=True,source_dimensions_distinguished_from_estimates=True,
        Amazon_FR_offer_observed=True,price_displayed_EUR=6.99,purchase_made=False,
        shipping_final=False,hardware_tested=False,installed_fit_verified=False,video1080p60_qualified=False)
    dump(report,result);print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
