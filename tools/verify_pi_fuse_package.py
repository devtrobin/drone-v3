"""Check exact files, local references, FreeCAD report and reviewed PDF."""
from pathlib import Path
import hashlib,json,re,sys,subprocess,py_compile
import pymupdf
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/protection-branche-pi'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    sys.stdout.reconfigure(encoding='utf-8');count=0
    for p in BASE.rglob('*.json'):json.loads(p.read_text(encoding='utf-8'))
    for a in json.loads((BASE/'assets.json').read_text(encoding='utf-8'))['assets']:
        if 'sha256' not in a:continue
        p=BASE/a['file'];assert p.exists() and sha(p)==a['sha256'] and p.stat().st_size==a['bytes'];count+=1
        if p.suffix=='.pdf':assert p.read_bytes().startswith(b'%PDF')
    for p in BASE.rglob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            if link.startswith(('http:','https:','#')):continue
            assert (p.parent/link.split('#')[0]).exists(),(p,link)
    cat=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'));assert cat['model_count']==6
    for m in cat['models']:
        folder=ROOT/'Composants'/m['folder']/'3D';p=folder/m['file']
        assert sha(p)==m['sha256'] and sha(folder/m['preview']['file'])==m['preview']['sha256']
        assert m['validation']['valid_after_reimport'] and not m['validation']['pairwise_material_overlaps']
        assert m['generator_sha256']==sha(ROOT/m['generator'])
        ignored=subprocess.run(['git','check-ignore',str(p.relative_to(ROOT))],cwd=ROOT,capture_output=True)
        assert ignored.returncode==1,('STEP ignored or git error',p,ignored.stdout)
    fc=json.loads((BASE/'3D/validation-freecad.json').read_text(encoding='utf-8'));assert fc['all_passed'] and len(fc['checks'])==6
    for c in fc['checks']:assert sha(ROOT/'Composants'/c['folder']/'3D'/c['file'])==c['sha256']
    meta_path=BASE/'notices/notice-protection-branche-pi-v3.json';meta=json.loads(meta_path.read_text(encoding='utf-8'))
    assert meta['sha256']==sha(meta_path.with_suffix('.pdf')) and meta['pages']==5 and meta['visual_review_complete']
    doc=pymupdf.open(meta_path.with_suffix('.pdf'));assert len(doc)==5 and all(len(p.get_text())>200 for p in doc)
    for name in ['collect_pi_fuse_refs.py','inspect_pi_fuse_refs.py','build_pi_fuse_data.py','build_pi_fuse_step.py','build_pi_fuse_pdf.py','validate_pi_fuse_freecad.py','verify_pi_fuse_package.py']:
        py_compile.compile(str(ROOT/'tools'/name),doraise=True)
    report=dict(checked_on='2026-10-14',all_passed=True,archives_and_local_references=count,step_models=6,
        pdf_pages=5,pdf_visual_review_complete=True,local_links_valid=True,source_and_cad_hashes_valid=True,
        step_not_ignored=True,freecad_headless_imports_valid=True,hardware_tested=False,prospective_fault_current_validated=False,amazon_fr_offers_confirmed=False)
    (BASE/'validation-dossier.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS',count,'archives/references, 6 STEP/previews/FreeCAD checks, 5 PDF pages reviewed, JSON, links; STEP not ignored',flush=True)
if __name__=='__main__':main()
