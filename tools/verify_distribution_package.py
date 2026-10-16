"""Verify deliverable links, archived originals and current CAD/PDF reports."""
from pathlib import Path
import hashlib,json,re,sys,subprocess,py_compile
import pymupdf
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/distribution-alimentation'
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
    cat=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'));assert cat['model_count']==5
    for m in cat['models']:
        folder=ROOT/'Composants'/m['folder']/'3D';p=folder/m['file']
        assert sha(p)==m['sha256'] and sha(folder/m['preview']['file'])==m['preview']['sha256']
        assert m['validation']['valid_after_reimport'] and not m['validation']['pairwise_material_overlaps']
        assert m['validation'].get('visible_thread_verified',False) or '/capot-' in m['folder']
        ignored=subprocess.run(['git','check-ignore',str(p.relative_to(ROOT))],cwd=ROOT,capture_output=True)
        assert ignored.returncode==1,('STEP ignored or git error',p,ignored.stdout)
    fc=json.loads((BASE/'3D/validation-freecad.json').read_text(encoding='utf-8'));assert fc['all_passed']
    for c in fc['checks']:assert sha(ROOT/'Composants'/c['folder']/'3D'/c['file'])==c['sha256']
    meta_path=BASE/'notices/notice-distribution-alimentation-v3.json';pdfmeta=json.loads(meta_path.read_text(encoding='utf-8'))
    assert pdfmeta['sha256']==sha(meta_path.with_suffix('.pdf')) and pdfmeta['pages']==5 and pdfmeta['visual_review_complete']
    doc=pymupdf.open(meta_path.with_suffix('.pdf'));assert len(doc)==5 and all(len(p.get_text())>200 for p in doc)
    for name in ['collect_distribution_refs.py','inspect_distribution_refs.py','build_distribution_data.py','build_distribution_step.py',
                 'build_distribution_pdf.py','validate_distribution_freecad.py','verify_distribution_package.py']:
        py_compile.compile(str(ROOT/'tools'/name),doraise=True)
    result=dict(checked_on='2026-10-14',all_passed=True,archived_files=count,step_models=5,pdf_pages=5,
        local_links_valid=True,source_hashes_valid=True,step_not_ignored=True,freecad_headless_imports_valid=True,
        pdf_visual_review_complete=True,hardware_tested=False,amazon_fr_offer_confirmed=False)
    (BASE/'validation-dossier.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('PASS',count,'archives, 5 STEP/current previews/FreeCAD checks, 5 PDF pages reviewed, JSON, links; STEP not ignored',flush=True)
if __name__=='__main__':main()
