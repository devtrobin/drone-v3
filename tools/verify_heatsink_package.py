"""Verify delivered references, hashes and local documentation links."""
from pathlib import Path
import json,hashlib,re,sys,subprocess,py_compile
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/dissipateur-relais'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    sys.stdout.reconfigure(encoding='utf-8')
    for p in BASE.rglob('*.json'):json.loads(p.read_text(encoding='utf-8'))
    assets=json.loads((BASE/'assets.json').read_text(encoding='utf-8'))['assets'];count=0
    for a in assets:
        if 'sha256' not in a:continue
        p=BASE/a['file'];assert p.exists() and sha(p)==a['sha256'] and p.stat().st_size==a['bytes'],p;count+=1
    for p in BASE.rglob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            if link.startswith(('http:','https:','#')):continue
            target=p.parent/link.split('#')[0];assert target.exists(),(p,link)
    catalog=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'))
    assert catalog['model_count']==5
    for m in catalog['models']:
        p=BASE/'3D'/m['file'];assert sha(p)==m['sha256']
        assert sha(BASE/'3D'/m['preview']['file'])==m['preview']['sha256']
        result=subprocess.run(['git','check-ignore',str(p.relative_to(ROOT))],cwd=ROOT,capture_output=True)
        assert result.returncode==1,('STEP ignored or git error',p,result.stdout,result.stderr)
    fc=json.loads((BASE/'3D/validation-freecad.json').read_text(encoding='utf-8'));assert fc['all_passed']
    for check in fc['checks']:assert sha(BASE/'3D'/check['file'])==check['sha256']
    notice=BASE/'notices/notice-dissipateur-relais-v3.json';data=json.loads(notice.read_text(encoding='utf-8'))
    assert data['sha256']==sha(notice.with_suffix('.pdf')) and data['pages']==4
    for script in ['collect_heatsink_refs.py','build_heatsink_data.py','build_heatsink_step.py','build_heatsink_pdf.py','validate_heatsink_freecad.py','verify_heatsink_package.py','build_battery_protection_docs.py']:
        py_compile.compile(str(ROOT/'tools'/script),doraise=True)
    print('PASS',count,'original assets, 5 STEP hashes and previews, FreeCAD validations, JSON, local links, syntax, STEP not ignored')
if __name__=='__main__':main()
