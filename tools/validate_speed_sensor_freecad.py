"""Independent headless FreeCAD import and geometry checks of the five STEP files."""
from pathlib import Path
import hashlib,json,sys,time
import FreeCAD,Part

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'Composants/capteurs-vitesse'
sys.stdout.reconfigure(encoding='utf-8')
cat=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'))
checks=[]
for m in cat['models']:
    p=ROOT/m['relative_step_path'];start=time.perf_counter()
    s=Part.read(str(p));b=s.optimalBoundingBox()
    bounds=dict(xmin=b.XMin,xmax=b.XMax,ymin=b.YMin,ymax=b.YMax,zmin=b.ZMin,zmax=b.ZMax)
    error=max(abs(v-m['bounds_mm'][k]) for k,v in bounds.items())
    volume=m['validation']['volume_after_default_quadrature_mm3']
    ve=abs(s.Volume-volume)/volume
    closed=all(a.isClosed() for a in s.Solids)
    passed=s.isValid() and closed and len(s.Solids)==m['validation']['solids'] and error<.01 and ve<1e-4
    result=dict(file=m['file'],relative_step_path=m['relative_step_path'],sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                passed=passed,valid=s.isValid(),closed_solids=closed,solids=len(s.Solids),faces=len(s.Faces),
                bounds_mm=bounds,bbox_error_mm=error,volume_mm3=s.Volume,volume_relative_error=ve,
                seconds=time.perf_counter()-start)
    checks.append(result);print('FreeCAD',m['file'],'PASS' if passed else 'FAIL',len(s.Solids),'solids',flush=True)
report=dict(checked_on='2026-10-15',mode='headless',FreeCAD_version=FreeCAD.Version(),GUI_tested=False,CADView_tested=False,
            hardware_tested=False,all_passed=all(c['passed'] for c in checks),checks=checks)
(BASE/'3D/validation-freecad.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert report['all_passed'],checks
