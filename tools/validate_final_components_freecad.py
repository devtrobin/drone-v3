"""Independent STEP imports, closed solids, envelopes and like-volume comparison."""
from pathlib import Path
import FreeCAD,Part,json,hashlib,time,sys
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants'
sys.stdout.reconfigure(encoding='utf-8')
folders=['connecteurs-commande','liaisons-alimentation-surveillance','maintien-batterie','coupure-manuelle']
for folder in folders:
 cat=json.loads((BASE/folder/'3D/catalogue.json').read_text(encoding='utf-8'));checks=[]
 for m in cat['models']:
  p=BASE/m['relative_step_path'];t=time.perf_counter();s=Part.read(str(p));b=s.optimalBoundingBox()
  bounds=dict(xmin=b.XMin,xmax=b.XMax,ymin=b.YMin,ymax=b.YMax,zmin=b.ZMin,zmax=b.ZMax)
  err=max(abs(v-m['bounds_mm'][k]) for k,v in bounds.items());closed=all(a.isClosed() for a in s.Solids)
  target=m['validation']['volume_after_default_quadrature_mm3'];ve=abs(s.Volume-target)/s.Volume;probes=[]
  for q in m['validation']['void_and_material_probes']:
   actual=any(a.isInside(FreeCAD.Vector(*q['point']),1e-6,True) for a in s.Solids)
   probes.append(dict(point=q['point'],expected=q['occupied'],occupied=actual,passed=actual==q['occupied']))
  passed=s.isValid() and closed and len(s.Solids)==m['validation']['solids'] and err<.01 and ve<1e-4 and all(q['passed'] for q in probes)
  checks.append(dict(file=m['file'],relative_step_path=m['relative_step_path'],sha256=hashlib.sha256(p.read_bytes()).hexdigest(),passed=passed,
   valid=s.isValid(),solids_closed=closed,solids=len(s.Solids),faces=len(s.Faces),bbox_error_mm=err,volume_relative_error=ve,
   volume_mm3=s.Volume,compared_CadQuery_default_quadrature_mm3=target,material_probes=probes,seconds=time.perf_counter()-t))
  print('FREECAD',m['file'],'PASS' if passed else'FAIL',len(s.Solids),flush=True)
 report=dict(checked_on='2026-10-14',all_passed=all(c['passed'] for c in checks),checks=checks,mode='headless',
  FreeCAD_version=FreeCAD.Version(),GUI_tested=False,CADView_tested=False,hardware_tested=False,
  comparison='FreeCAD default quadrature versus same CadQuery imported STEP default quadrature. Strict adaptive roundtrip independently in catalogue.')
 (BASE/folder/'3D/validation-freecad.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');assert report['all_passed']
