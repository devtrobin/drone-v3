"""Independent FreeCAD import of the three current support-camera STEP files."""
from pathlib import Path
import hashlib,json
import FreeCAD,Part

ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Composants/support-camera/3D'
rows=[]
for m in json.loads((B/'provenance.json').read_text(encoding='utf-8'))['models']:
    path=B/m['file'];s=Part.read(str(path));bb=s.BoundBox
    bounds=dict(zip(['xmin','xmax','ymin','ymax','zmin','zmax'],[bb.XMin,bb.XMax,bb.YMin,bb.YMax,bb.ZMin,bb.ZMax]))
    error=max(abs(bounds[k]-m['bounds_mm'][k]) for k in bounds)
    passed=s.isValid() and all(x.isValid() and x.isClosed() for x in s.Solids) and len(s.Solids)==m['validation']['solids'] and error<.01
    rows.append(dict(file=path.name,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),passed=passed,solids=len(s.Solids),bounds_mm=bounds,max_bbox_error_mm=error))
    print(path.name,passed,len(s.Solids),flush=True)
result=dict(all_passed=all(r['passed'] for r in rows),FreeCAD_version=FreeCAD.Version(),models=rows,hardware_tested=False,GUI_test=False)
(B/'validation-freecad.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
assert result['all_passed']
