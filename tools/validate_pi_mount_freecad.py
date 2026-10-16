"""Independent FreeCAD check of every STEP from this component catalogue."""
from pathlib import Path
import FreeCAD,Part,json,hashlib,time,sys
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/fixations-raspberry-pi-5/3D'
sys.stdout.reconfigure(encoding='utf-8');cat=json.loads((BASE/'catalogue.json').read_text(encoding='utf-8'));checks=[]
for m in cat['models']:
 p=BASE/m['file'];t=time.perf_counter();s=Part.read(str(p));b=s.optimalBoundingBox()
 bounds=dict(xmin=b.XMin,xmax=b.XMax,ymin=b.YMin,ymax=b.YMax,zmin=b.ZMin,zmax=b.ZMax)
 error=max(abs(v-m['bounds_mm'][k]) for k,v in bounds.items());closed=all(a.isClosed() for a in s.Solids)
 target=m['validation']['volume_after_default_quadrature_mm3']
 ve=abs(s.Volume-target)/s.Volume
 probes=[]
 for probe in m['validation']['void_and_material_probes']:
  occupied=any(a.isInside(FreeCAD.Vector(*probe['point']),1e-6,True) for a in s.Solids)
  probes.append(dict(point=probe['point'],expected=probe['occupied'],occupied=occupied,passed=occupied==probe['occupied']))
 passed=s.isValid() and closed and len(s.Solids)==m['validation']['solids'] and error<.01 and ve<1e-4 and all(p['passed'] for p in probes)
 checks.append(dict(file=m['file'],sha256=hashlib.sha256(p.read_bytes()).hexdigest(),passed=passed,valid=s.isValid(),solids_closed=closed,
  solids=len(s.Solids),faces=len(s.Faces),bbox_error_mm=error,volume_relative_error=ve,
  volume_mm3=s.Volume,compared_default_quadrature_mm3=target,
  source_adaptive_volume_mm3=m['validation']['volume_after_mm3'],
  material_and_helical_probes=probes,seconds=time.perf_counter()-t))
 print('FREECAD',p.name,'PASS' if passed else 'FAIL',len(s.Solids),'solids',flush=True)
report=dict(checked_on='2026-10-14',all_passed=all(c['passed'] for c in checks),mode='headless',FreeCAD_version=FreeCAD.Version(),
 volume_method='FreeCAD Volume compared to CadQuery default quadrature of identical STEP; strict adaptive round-trip conserved separately in catalogue.',
 GUI_tested=False,CADView_tested=False,hardware_tested=False,checks=checks)
(BASE/'validation-freecad.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');assert report['all_passed']
