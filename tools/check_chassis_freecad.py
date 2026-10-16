"""Independent FreeCAD import, integrity and closure of the A2-R1 STEP files."""
from pathlib import Path
import hashlib,json
import FreeCAD,Part

ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Composants/chassis';O=B/'3D'
manifest=json.loads((O/'provenance.json').read_text(encoding='utf-8'))
expected={m['file']:m for m in manifest['models']};rows=[]
for path in sorted(O.glob('*.step')):
    s=Part.read(str(path));passed=s.isValid() and len(s.Solids)>0 and all(q.isValid() and q.isClosed() for q in s.Solids)
    row=dict(file=path.name,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),passed=passed,solids=len(s.Solids),volume_mm3=s.Volume)
    if path.name in expected:
        m=expected[path.name];b=s.BoundBox;bounds=dict(zip(['xmin','xmax','ymin','ymax','zmin','zmax'],[b.XMin,b.XMax,b.YMin,b.YMax,b.ZMin,b.ZMax]))
        error=max(abs(bounds[k]-m['bounds_mm'][k]) for k in bounds)
        row.update(bounds_mm=bounds,max_bbox_error_mm=error)
        row['passed']=passed and error<.01 and len(s.Solids)==m['validation']['solids']
    rows.append(row);print(path.name,row['passed'],len(s.Solids),flush=True)
result=dict(all_passed=all(r['passed'] for r in rows),FreeCAD_version=FreeCAD.Version(),models=rows,hardware_tested=False,GUI_test=False)
(O/'validation-freecad.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
assert result['all_passed']
