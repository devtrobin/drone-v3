"""Verify local links, assets, STEP hashes and independent import reports."""
from pathlib import Path
import json,hashlib,re,sys,subprocess,py_compile
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/protection-surintensite'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    sys.stdout.reconfigure(encoding='utf-8')
    for p in BASE.rglob('*.json'):json.loads(p.read_text(encoding='utf-8'))
    manifest=json.loads((BASE/'assets.json').read_text(encoding='utf-8'))['assets'];count=0
    for a in manifest:
        if 'sha256' not in a:continue
        p=BASE/a['file'];assert p.exists() and sha(p)==a['sha256'] and p.stat().st_size==a['bytes'];count+=1
        if 'source_file' in a:assert sha(BASE/a['source_file'])==a['source_sha256']
    for p in BASE.rglob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            if link.startswith(('http:','https:','#')):continue
            assert (p.parent/link.split('#')[0]).exists(),(p,link)
    cat=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'));assert cat['model_count']==4
    for m in cat['models']:
        folder=ROOT/'Composants'/m['folder']/'3D';p=folder/m['file']
        assert sha(p)==m['sha256'] and sha(folder/m['preview']['file'])==m['preview']['sha256']
        ignored=subprocess.run(['git','check-ignore',str(p.relative_to(ROOT))],cwd=ROOT,capture_output=True)
        assert ignored.returncode==1,('STEP ignored or git error',p,ignored.stdout)
    fc=json.loads((BASE/'3D/validation-freecad.json').read_text(encoding='utf-8'));assert fc['all_passed']
    for check in fc['checks']:assert sha(ROOT/'Composants'/check['folder']/'3D'/check['file'])==check['sha256']
    p=BASE/'notices/notice-fusible-principal-v3.json';meta=json.loads(p.read_text(encoding='utf-8'))
    assert meta['sha256']==sha(p.with_suffix('.pdf')) and meta['pages']==5
    for name in ['collect_overcurrent_refs.py','build_overcurrent_data.py','build_overcurrent_step.py','build_overcurrent_pdf.py','validate_overcurrent_freecad.py','verify_overcurrent_package.py']:
        py_compile.compile(str(ROOT/'tools'/name),doraise=True)
    print('PASS',count,'archives, 4 STEP hashes/previews/FreeCAD checks, JSON, local links, syntax; STEP not ignored')
if __name__=='__main__':main()
