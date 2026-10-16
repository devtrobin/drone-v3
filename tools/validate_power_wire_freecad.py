"""Independent FreeCAD checks of six wire STEP files, including 680 strands."""
from pathlib import Path
import FreeCAD,Part,json,hashlib,time,sys
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/cable-puissance-12awg'
def main():
    sys.stdout.reconfigure(encoding='utf-8');cat=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'));checks=[]
    for m in cat['models']:
        p=BASE/'3D'/m['file'];t=time.perf_counter();s=Part.read(str(p));b=s.optimalBoundingBox()
        bounds=dict(xmin=b.XMin,xmax=b.XMax,ymin=b.YMin,ymax=b.YMax,zmin=b.ZMin,zmax=b.ZMax)
        error=max(abs(v-m['bounds_mm'][k]) for k,v in bounds.items());closed=all(a.isClosed() for a in s.Solids)
        strands=[a for a in s.Solids if abs(a.Volume-3.141592653589793*.04**2*25)<1e-6] if m['strand_packing'] else []
        passed=s.isValid() and closed and len(s.Solids)==m['validation']['solids'] and error<.01 and (not m['strand_packing'] or len(strands)==680)
        checks.append(dict(file=m['file'],sha256=hashlib.sha256(p.read_bytes()).hexdigest(),passed=passed,valid=s.isValid(),solids_closed=closed,
            solids=len(s.Solids),faces=len(s.Faces),bbox_error_mm=error,strands_count_verified=len(strands) if m['strand_packing'] else None,seconds=time.perf_counter()-t))
        print('FREECAD',p.name,'PASS' if passed else 'FAIL',len(s.Solids),'solids',round(error,6),'mm',flush=True)
    report=dict(checked_on='2026-10-14',all_passed=all(c['passed'] for c in checks),mode='headless',FreeCAD_version=FreeCAD.Version(),
        GUI_tested=False,hardware_tested=False,checks=checks)
    (BASE/'3D/validation-freecad.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');assert report['all_passed']
if __name__=='__main__':main()
