"""Independent FreeCAD headless import and shape checks."""
from pathlib import Path
import FreeCAD,Part,json,hashlib,time,sys
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/connecteurs-alimentation'
def main():
    sys.stdout.reconfigure(encoding='utf-8');cat=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'));checks=[]
    for m in cat['models']:
        p=BASE/'3D'/m['file'];t=time.perf_counter();s=Part.read(str(p));b=s.optimalBoundingBox()
        bounds=dict(xmin=b.XMin,xmax=b.XMax,ymin=b.YMin,ymax=b.YMax,zmin=b.ZMin,zmax=b.ZMax)
        error=max(abs(v-m['bounds_mm'][k]) for k,v in bounds.items());closed=all(a.isClosed() for a in s.Solids)
        passed=s.isValid() and closed and len(s.Solids)==m['validation']['solids'] and error<.01
        checks.append(dict(file=m['file'],sha256=hashlib.sha256(p.read_bytes()).hexdigest(),passed=passed,valid=s.isValid(),
            solids_closed=closed,solids=len(s.Solids),faces=len(s.Faces),bbox_error_mm=error,seconds=time.perf_counter()-t))
        print('FREECAD',p.name,'PASS' if passed else 'FAIL',len(s.Solids),'solids',round(error,5),'mm',flush=True)
    report=dict(checked_on='2026-10-14',all_passed=all(c['passed'] for c in checks),mode='headless independent import',
        FreeCAD_version=FreeCAD.Version(),hardware_tested=False,GUI_tested=False,checks=checks)
    (BASE/'3D/validation-freecad.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');assert report['all_passed']
if __name__=='__main__':main()
