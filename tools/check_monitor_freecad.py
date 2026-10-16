"""Independent FreeCAD STEP import, validity, closure and bounds check (no GUI)."""
from pathlib import Path
import hashlib,json,sys,time
import FreeCAD,Part
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Composants/carte-surveillance-electrique'
def main():
    rows=[];meta=json.loads((B/'3D/provenance.json').read_text(encoding='utf-8'))
    for m in meta['models']:
        t=time.time();path=B/'3D'/m['file'];s=Part.read(str(path));bb=s.BoundBox
        actual=dict(zip(['xmin','xmax','ymin','ymax','zmin','zmax'],[bb.XMin,bb.XMax,bb.YMin,bb.YMax,bb.ZMin,bb.ZMax]))
        bberr=max(abs(actual[k]-m['bounds_mm'][k]) for k in actual)
        r=dict(file=path.name,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),valid=s.isValid(),all_solids_closed=all(x.isClosed() and x.isValid() for x in s.Solids),solids=len(s.Solids),
               expected_solids=m['validation']['solids'],bounds_mm=actual,bbox_max_difference_mm=bberr,elapsed_s=time.time()-t)
        r['passed']=r['valid'] and r['all_solids_closed'] and r['solids']==r['expected_solids'] and bberr<.01
        rows.append(r);print(path.name,r['passed'],len(s.Solids),flush=True)
    result=dict(FreeCAD_version=FreeCAD.Version(),all_passed=all(x['passed'] for x in rows),models=rows,GUI_open_test=False,hardware_tested=False)
    (B/'3D/validation-freecad.json').write_text(json.dumps(result,indent=2),encoding='utf-8');assert result['all_passed']
if __name__=='__main__':main()
