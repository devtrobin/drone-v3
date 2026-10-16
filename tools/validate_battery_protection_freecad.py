"""Validate the three models with installed FreeCAD without a GUI."""
from pathlib import Path
import FreeCAD,Part,json,time,hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'Composants/protection-batterie/3D'
def main():
    sys.stdout.reconfigure(encoding='utf-8')
    cat=json.loads((OUT/'catalogue.json').read_text(encoding='utf-8'));checks=[]
    for m in cat['models']:
        p=ROOT/'Composants'/m['folder']/'3D'/m['file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==m['sha256']
        start=time.perf_counter();s=Part.read(str(p));elapsed=time.perf_counter()-start;b=s.optimalBoundingBox()
        values=dict(xmin=b.XMin,xmax=b.XMax,ymin=b.YMin,ymax=b.YMax,zmin=b.ZMin,zmax=b.ZMax)
        error=max(abs(v-m['bounds_mm'][k]) for k,v in values.items())
        passed=s.isValid() and all(x.isClosed() for x in s.Solids) and len(s.Solids)==m['validation']['solids'] and error<.01
        checks.append(dict(file=m['file'],sha256=m['sha256'],passed=passed,valid=s.isValid(),solids=len(s.Solids),faces=len(s.Faces),bbox_error_mm=error,seconds=elapsed))
        print('FREECAD',p.name,'PASS' if passed else 'FAIL',flush=True)
    result=dict(method='FreeCAD Part.read, headless',version=FreeCAD.Version(),checked_on='2026-10-13',GUI_tested=False,VSCode_CAD_View_tested=False,
        all_passed=all(x['passed'] for x in checks),checks=checks)
    (OUT/'validation-freecad.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');assert result['all_passed']
if __name__=='__main__':main()
