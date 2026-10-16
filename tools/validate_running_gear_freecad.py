"""Read the generated STEP catalogue with the installed FreeCAD Python runtime.

Run: D:/FreeCAD/bin/python.exe tools/validate_running_gear_freecad.py
This is a real headless FreeCAD/Part STEP import, not a GUI performance test.
It leaves existing STEP files unchanged and writes a machine-readable report.
"""
from pathlib import Path
import hashlib,json,sys,time
import FreeCAD,Part

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'Composants/direction-et-transmission/3D'


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    catalog=json.loads((OUT/'catalogue.json').read_text(encoding='utf-8'))
    checks=[]
    for item in catalog['models']:
        path=ROOT/'Composants'/item['folder']/'3D'/item['file']
        assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256']
        start=time.perf_counter();shape=Part.read(str(path));elapsed=time.perf_counter()-start
        # BoundBox can include distant BSpline control poles of trimmed
        # helical surfaces. Compare actual surface extrema, not pole bounds.
        bb=shape.optimalBoundingBox()
        bounds={'xmin':bb.XMin,'xmax':bb.XMax,'ymin':bb.YMin,'ymax':bb.YMax,'zmin':bb.ZMin,'zmax':bb.ZMax}
        error=max(abs(v-item['bounds_mm'][k]) for k,v in bounds.items())
        passed=(shape.isValid() and not shape.isNull() and
                len(shape.Solids)==item['validation']['solids'] and error<.01)
        result=dict(file=str(path.relative_to(ROOT)).replace('\\','/'),sha256=item['sha256'],
            valid=shape.isValid(),closed_solids=all(s.isClosed() for s in shape.Solids),
            solids=len(shape.Solids),faces=len(shape.Faces),bbox_error_mm=error,
            import_seconds=elapsed,bytes=path.stat().st_size,passed=passed)
        checks.append(result)
        print('FREECAD',path.name,'PASS' if passed else 'FAIL',round(elapsed,3),'s',flush=True)
    report=dict(checked_on='2026-10-13',method='FreeCAD Part.read, headless STEP import',
        version=FreeCAD.Version(),bbox_method='Part.Shape.optimalBoundingBox',
        GUI_tested=False,VSCode_CAD_View_tested=False,
        files=len(checks),all_passed=all(x['passed'] and x['closed_solids'] for x in checks),checks=checks)
    (OUT/'validation-freecad.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    assert report['all_passed'],'One or more STEP files failed FreeCAD import validation'
    print('FREECAD DONE',len(checks),'valid STEP files',flush=True)


if __name__=='__main__':
    main()
