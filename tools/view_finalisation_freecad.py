"""Run in installed FreeCAD GUI as a task-local macro; exports R2 native view."""
from pathlib import Path
import FreeCAD as App, FreeCADGui as Gui, ImportGui
import hashlib,json,time,os
ROOT=Path(__file__).resolve().parents[1];O=ROOT/'Assemblage/R2';V=ROOT/'Composants/finalisation-theorique-r2/verification'
t=time.perf_counter();doc=App.newDocument('DroneV3_R2')
src=O/'drone-v3-r2-etude.step'
ImportGui.insert(str(src),doc.Name)
doc.recompute()
Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll()
for obj in doc.Objects:
    if obj.isDerivedFrom('Part::Feature') and not obj.Shape.isNull():obj.ViewObject.DisplayMode='Flat Lines'
path=O/'drone-v3-r2-etude.FCStd';doc.saveAs(str(path));name=doc.Name
features=[obj for obj in doc.Objects if obj.isDerivedFrom('Part::Feature') and not obj.Shape.isNull()]
assert features and all(o.Shape.isValid() for o in features)
count=len(features);solids=sum(len(o.Shape.Solids) for o in features)
App.closeDocument(name);start=time.perf_counter();doc=App.openDocument(str(path));opened=time.perf_counter()-start
Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll()
Gui.activeDocument().activeView().saveImage(str(O/'apercu-r2-isometrique.png'),1400,1000,'White')
Gui.activeDocument().activeView().viewTop();Gui.activeDocument().activeView().fitAll()
Gui.activeDocument().activeView().saveImage(str(O/'apercu-r2-dessus.png'),1400,1000,'White')
Gui.activeDocument().activeView().viewAxonometric();doc.save()
data=dict(source=src.name,source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),native_file=path.name,bytes=path.stat().st_size,features=count,solids=solids,all_imported_shapes_valid=True,gui_reopen_seconds=opened,total_seconds=time.perf_counter()-t,native_reopen_tested=True,full_collision_validation=False)
(V/'freecad.json').write_text(json.dumps(data,indent=2),encoding='utf-8');print(data,flush=True)
os._exit(0)
