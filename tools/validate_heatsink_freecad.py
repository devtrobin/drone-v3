"""Independent FreeCAD STEP check; does not claim a GUI/CAD View test."""
from pathlib import Path
import FreeCAD,Part,json,time,sys,hashlib
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'Composants/dissipateur-relais/3D'
def main():
    sys.stdout.reconfigure(encoding='utf-8');data=json.loads((OUT/'catalogue.json').read_text(encoding='utf-8'));checks=[]
    for m in data['models']:
        p=OUT/m['file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==m['sha256']
        start=time.perf_counter();s=Part.read(str(p));seconds=time.perf_counter()-start;b=s.optimalBoundingBox()
        actual=dict(xmin=b.XMin,xmax=b.XMax,ymin=b.YMin,ymax=b.YMax,zmin=b.ZMin,zmax=b.ZMax)
        error=max(abs(v-m['bounds_mm'][k]) for k,v in actual.items())
        passed=s.isValid() and all(sol.isClosed() for sol in s.Solids) and len(s.Solids)==m['validation']['solids'] and error<.01
        checks.append(dict(file=m['file'],passed=passed,valid=s.isValid(),solids=len(s.Solids),faces=len(s.Faces),bbox_error_mm=error,seconds=seconds,sha256=m['sha256']))
        print('FREECAD',p.name,'PASS' if passed else 'FAIL',flush=True)
    result=dict(method='FreeCAD Part.read; headless',version=FreeCAD.Version(),checked_on='2026-10-13',
        all_passed=all(c['passed'] for c in checks),GUI_tested=False,VSCode_CAD_View_tested=False,checks=checks)
    (OUT/'validation-freecad.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');assert result['all_passed']
if __name__=='__main__':main()
