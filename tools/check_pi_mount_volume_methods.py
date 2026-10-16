"""Record default quadrature for fair comparison with FreeCAD default Volume.

STEP files are read-only. Source round-trip adaptive checks remain unchanged.
This reconciles the numerical methods, rather than changing their threshold.
"""
from pathlib import Path
import cadquery as cq,json,sys,hashlib
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/fixations-raspberry-pi-5/3D'
sys.stdout.reconfigure(encoding='utf-8');cat=json.loads((BASE/'catalogue.json').read_text(encoding='utf-8'))
for i,m in enumerate(cat['models']):
 p=BASE/m['file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==m['sha256']
 s=cq.importers.importStep(str(p)).val();v=s.Volume();ad=s.Volume(tol=1e-9)
 assert abs(ad-m['validation']['volume_after_mm3'])/ad<1e-7
 m['validation']['volume_after_default_quadrature_mm3']=v
 m['validation']['default_volume_purpose']='Compare with FreeCAD default Volume; adaptive values remain the strict STEP round-trip reference.'
 p.with_suffix('.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('QUADRATURE',p.name,round(v,6),round(ad,6),flush=True)
(BASE/'catalogue.json').write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
