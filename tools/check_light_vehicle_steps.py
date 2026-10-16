"""Refresh the STEP section while retaining the completed exact native checks."""
from pathlib import Path
import json,hashlib
import FreeCAD,Part
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Assemblage/preparation'
prep=json.loads((B/'preparation.json').read_text(encoding='utf-8'));fc=json.loads((B/'validation-freecad.json').read_text(encoding='utf-8'))
assert fc['all_passed'] and fc['native_solids']==5441
assert hashlib.sha256((B/prep['native']['file']).read_bytes()).hexdigest()==prep['native']['sha256']
rows=[];n=0
for row in prep['zones']+[prep['view_step']]:
 name=row.get('step_file',row.get('file'));p=B/name;s=Part.read(str(p));expected=row.get('view_solids',row.get('solids'))
 assert s.isValid() and len(s.Solids)==expected and all(q.isClosed() for q in s.Solids)
 if 'complet-detaille' in name:assert len(s.Solids)==n
 else:n+=len(s.Solids)
 rows.append(dict(file=name,passed=True,solids=len(s.Solids),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 print('LIGHT STEP PASS',name,len(s.Solids),flush=True)
assert n==225
fc['view_steps']=rows;fc['view_step_representation']='Implantation légère A2-R1 ; géométrie CAO complète inchangée'
(B/'validation-freecad.json').write_text(json.dumps(fc,ensure_ascii=False,indent=2),encoding='utf-8')
