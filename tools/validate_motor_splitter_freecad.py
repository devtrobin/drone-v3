"""Independent headless FreeCAD checks for every delivered splitter STEP."""
from pathlib import Path
import FreeCAD,Part,json,hashlib,time,sys
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/repartition-moteurs'
def main():
    sys.stdout.reconfigure(encoding='utf-8');cat=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'));checks=[]
    for m in cat['models']:
        p=BASE/'3D'/m['file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==m['sha256'];t=time.perf_counter();s=Part.read(str(p));seconds=time.perf_counter()-t;b=s.optimalBoundingBox()
        bounds=dict(xmin=b.XMin,xmax=b.XMax,ymin=b.YMin,ymax=b.YMax,zmin=b.ZMin,zmax=b.ZMax)
        error=max(abs(v-m['bounds_mm'][k]) for k,v in bounds.items());valid=s.isValid();closed=all(a.isClosed() for a in s.Solids)
        passed=valid and closed and len(s.Solids)==m['validation']['solids'] and error<.01
        checks.append(dict(file=m['file'],sha256=m['sha256'],passed=passed,valid=valid,solids_closed=closed,solids=len(s.Solids),faces=len(s.Faces),bbox_error_mm=error,seconds=seconds));print('FREECAD',p.name,'PASS' if passed else 'FAIL',flush=True)
    report=dict(method='FreeCAD Part.read, headless',version=FreeCAD.Version(),checked_on='2026-10-14',GUI_tested=False,VSCode_CAD_View_tested=False,all_passed=all(c['passed'] for c in checks),checks=checks)
    (BASE/'3D/validation-freecad.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');assert report['all_passed']
if __name__=='__main__':main()
