"""Read every power STEP with real headless FreeCAD, preserving the originals."""
from pathlib import Path
import FreeCAD,Part,json,hashlib,time,sys

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'Composants/alimentation/3D'


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    catalog=json.loads((OUT/'catalogue.json').read_text(encoding='utf-8'))
    checks=[]
    for item in catalog['models']:
        path=ROOT/'Composants'/item['folder']/'3D'/item['file']
        assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256']
        start=time.perf_counter();shape=Part.read(str(path));seconds=time.perf_counter()-start
        b=shape.optimalBoundingBox()
        bounds=dict(xmin=b.XMin,xmax=b.XMax,ymin=b.YMin,ymax=b.YMax,zmin=b.ZMin,zmax=b.ZMax)
        error=max(abs(v-item['bounds_mm'][k]) for k,v in bounds.items())
        valid=shape.isValid() and not shape.isNull()
        closed=all(s.isClosed() for s in shape.Solids)
        passed=valid and closed and len(shape.Solids)==item['validation']['solids'] and error<.01
        checks.append(dict(folder=item['folder'],file=item['file'],bytes=path.stat().st_size,
            sha256=item['sha256'],valid=valid,closed_solids=closed,solids=len(shape.Solids),
            faces=len(shape.Faces),bbox_error_mm=error,import_seconds=seconds,passed=passed))
        print('FREECAD',path.name,'PASS' if passed else 'FAIL',round(seconds,3),'s',flush=True)
    report=dict(checked_on='2026-10-13',method='FreeCAD Part.read, optimalBoundingBox; headless',
        version=FreeCAD.Version(),GUI_tested=False,VSCode_CAD_View_tested=False,
        files=len(checks),all_passed=all(x['passed'] for x in checks),checks=checks)
    (OUT/'validation-freecad.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    assert report['all_passed'],'STEP failed FreeCAD checks'


if __name__=='__main__':main()
