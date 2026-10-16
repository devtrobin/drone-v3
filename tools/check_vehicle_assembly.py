"""Independent FreeCAD import of the detailed V3 assembly and its four zones."""
from pathlib import Path
import ast,hashlib,json,sys,time
import FreeCAD,Part

ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Assemblage'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
d=json.loads((B/'provenance.json').read_text(encoding='utf-8'));rows=[];total=0
for m in d['models']:
    p=B/m['file'];assert sha(p)==m['sha256'] and p.stat().st_size==m['bytes']
    start=time.perf_counter();s=Part.read(str(p))
    closed=all(q.isClosed() for q in s.Solids);valid=s.isValid();count=len(s.Solids)
    assert valid and closed and count>0,m['file']
    if 'complet-detaille' in p.name:assert count==total,(count,total)
    else:total+=count
    b=s.BoundBox
    rows.append(dict(file=p.name,passed=True,solids=count,closed=True,valid=True,elapsed_seconds=time.perf_counter()-start,
        bounds_mm=[b.XMin,b.XMax,b.YMin,b.YMax,b.ZMin,b.ZMax],sha256=sha(p)))
    print(p.name,'PASS',count,'solids',flush=True)
for r in d['instances']:assert sha(ROOT/r['source'])==r['source_sha256'],r['source']
ast.parse((ROOT/'tools/build_vehicle_assembly.py').read_text(encoding='utf-8'))
result=dict(all_passed=True,FreeCAD_version=FreeCAD.Version(),models=rows,sources_unchanged=True,
    complete_matches_sum_of_zones=True,hardware_tested=False,GUI_opening_tested=False,
    assembly_interference_check_complete=False,harness_electrical_connection_validated=False)
(B/'validation-freecad.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('ALL PASS',flush=True)
