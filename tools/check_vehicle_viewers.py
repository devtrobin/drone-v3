"""Reopen the actual FCStd and five viewing STEP files in a fresh FreeCAD.

Native colours, geometry and placements are checked after restoring the file.
Use --render with Qt's windows platform for a FreeCAD viewport export if a
desktop/OpenGL context is available. This is a CAD API render, not UI automation.
"""
from pathlib import Path
import os,sys,time,json,hashlib,zipfile,struct,math,re
if '--render' not in sys.argv:os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
import FreeCAD as App,FreeCADGui as Gui,Part
if not App.GuiUp:Gui.showMainWindow()
ROOT=Path(__file__).resolve().parents[1];BUILD=ROOT/'Assemblage/preparation'
if not (BUILD/'preparation.json').exists():BUILD=ROOT/'Assemblage'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bnd(s):
    b=s.BoundBox
    return [b.XMin,b.XMax,b.YMin,b.YMax,b.ZMin,b.ZMax]
def close(a,b,tol=1e-4):return max(abs(x-y) for x,y in zip(a,b))<tol
def centre(s):
    props=[(q.Volume,tuple(q.CenterOfMass)) for q in s.Solids]
    volume=sum(v for v,c in props)
    return [sum(v*c[k] for v,c in props)/volume for k in range(3)]
def main():
    report=json.loads((BUILD/'preparation.json').read_text(encoding='utf-8'))
    path=BUILD/report['native']['file'];assert sha(path)==report['native']['sha256']
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        assert 'Document.xml' in z.namelist() and 'GuiDocument.xml' in z.namelist()
    start=time.perf_counter();doc=App.openDocument(str(path));load=time.perf_counter()-start
    sys.__stdout__.write('NATIVE OPENED '+str(load)+' seconds\n');sys.__stdout__.flush()
    camera=Gui.activeDocument().activeView().getCamera()
    assert float(re.search(r'height\s+([0-9.eE+-]+)',camera).group(1))>600
    native=[];total=0
    for row in report['zones']:
        group=doc.getObject(row['zone']);assert group is not None
        features=list(group.Group);shapes=[];n_colors=0
        assert len(features)==row['native_components']
        for obj,entry in zip(features,row['components']):
            assert obj.Label==entry['component']
            shape=obj.Shape;assert not shape.isNull()
            assert len(shape.Solids)==entry['exact_solids']
            assert len(shape.Faces)==entry['faces']
            assert shape.isValid() and all(s.isClosed() for s in shape.Solids),obj.Label
            colors=list(obj.ViewObject.DiffuseColor)
            assert len(colors) in (1,len(shape.Faces)),(obj.Label,len(colors),len(shape.Faces))
            assert colors and obj.ViewObject.Visibility
            assert obj.ViewObject.DisplayMode=='Shaded'
            n_colors+=len(colors);shapes.append(shape)
        whole=Part.makeCompound(shapes);assert close(bnd(whole),row['bounds_mm'],5)
        if row['volume_mm3'] is not None:
            assert abs(whole.Volume-row['volume_mm3'])<max(1e-5,whole.Volume*1e-8)
            assert close(centre(whole),row['centre_mm'],1e-5)
        total+=len(whole.Solids)
        native.append(dict(zone=row['zone'],passed=True,solids=len(whole.Solids),faces=len(whole.Faces),features=len(features),face_color_entries=n_colors,bounds_mm=bnd(whole)))
    assert total==5441
    renders=[]
    if '--render' in sys.argv:
        Gui.activeDocument().activeView().setCameraType('Orthographic')
        for name,view in [('isometrique','viewAxonometric'),('dessus','viewTop')]:
            getattr(Gui.activeDocument().activeView(),view)()
            Gui.activeDocument().activeView().fitAll();Gui.updateGui()
            p=BUILD/('apercu-freecad-cao-'+name+'.png')
            Gui.activeDocument().activeView().saveImage(str(p),1600,1100,'White')
            assert p.exists() and p.stat().st_size>10000
            renders.append(dict(file=p.name,bytes=p.stat().st_size,sha256=sha(p)))
    App.closeDocument(doc.Name)
    steps=[];view_solids=0
    for row in report['zones']+[report['view_step']]:
        name=row.get('step_file',row.get('file'));expected=row.get('view_solids',row.get('solids'))
        p=BUILD/name;digest=row.get('step_sha256',row.get('sha256'))
        assert sha(p)==digest
        started=time.perf_counter();s=Part.read(str(p))
        assert s.isValid() and len(s.Solids)==expected
        assert all(q.isClosed() for q in s.Solids)
        if 'complet-detaille' in name:assert len(s.Solids)==view_solids
        else:view_solids+=len(s.Solids)
        steps.append(dict(file=name,passed=True,sha256=digest,bytes=p.stat().st_size,solids=len(s.Solids),seconds=time.perf_counter()-started))
    for row in json.loads(zipfile.ZipFile(ROOT/'Assemblage/sources-step-detaillees-originales.zip').read('provenance.json'))['instances']:
        assert sha(ROOT/row['source'])==row['source_sha256'],row['source']
    from PySide6.QtGui import QGuiApplication
    result=dict(all_passed=True,FreeCAD_version=App.Version(),native_file=path.name,native_load_seconds=load,native_solids=total,native_zones=native,native_GUI_document_restored=True,native_camera=camera,qt_platform=QGuiApplication.platformName(),viewport_renders=renders,view_steps=steps,component_sources_unchanged=True,physical_fit_validated=False,complete_wiring_validated=False)
    (BUILD/'validation-freecad.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    sys.__stdout__.write('ALL PASS '+json.dumps(dict(native_load_seconds=load,native_solids=total,steps=len(steps),renders=len(renders)))+'\n');sys.__stdout__.flush()
    os._exit(0)
if __name__=='__main__':main()
