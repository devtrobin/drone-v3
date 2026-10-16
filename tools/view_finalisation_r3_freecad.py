"""Run in installed FreeCAD: import, native save/reopen and real viewport images."""
from pathlib import Path
import FreeCAD as App,FreeCADGui as Gui,ImportGui
import hashlib,json,time,os
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'Assemblage/R3';V=ROOT/'Composants/complements-finalisation-r3/verification'
start=time.perf_counter();doc=App.newDocument('DroneV3_R3');src=A/'drone-v3-r3-faisceau.step'
ImportGui.insert(str(src),doc.Name);doc.recompute()
for o in doc.Objects:
    if o.isDerivedFrom('Part::Feature') and not o.Shape.isNull():o.ViewObject.DisplayMode='Flat Lines'
Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll()
native=A/'drone-v3-r3-faisceau.FCStd';doc.saveAs(str(native))
features=[o for o in doc.Objects if o.isDerivedFrom('Part::Feature') and not o.Shape.isNull()]
assert features and all(o.Shape.isValid() for o in features)
count=len(features);solids=sum(len(o.Shape.Solids) for o in features)
App.closeDocument(doc.Name);t=time.perf_counter();doc=App.openDocument(str(native));elapsed=time.perf_counter()-t
Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll()
Gui.activeDocument().activeView().saveImage(str(A/'apercu-r3-isometrique.png'),1400,1000,'White')
Gui.activeDocument().activeView().viewTop();Gui.activeDocument().activeView().fitAll()
Gui.activeDocument().activeView().saveImage(str(A/'apercu-r3-dessus.png'),1400,1000,'White')
Gui.activeDocument().activeView().viewAxonometric();doc.save()
d=dict(source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),features=count,solids=solids,all_shapes_valid=True,native_reopened=True,native_reopen_seconds=elapsed,total_seconds=time.perf_counter()-start)
(V/'freecad.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d,flush=True);os._exit(0)
