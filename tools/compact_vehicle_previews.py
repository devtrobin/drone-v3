"""Compact portable previews after exact native assembly has been saved.

No native BREP change: STEP tyre grooves are suppressed in a viewing copy.
GLB uses all exact surfaces with explicit 0.18 mm / 0.35 rad tessellation.
"""
import os,sys,json,time
from pathlib import Path
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
import FreeCAD as App,FreeCADGui as Gui,Part
if not App.GuiUp:Gui.showMainWindow()
import ImportGui
from prepare_vehicle_viewers import Glb,colour_list,sha
ROOT=Path(__file__).resolve().parents[1];BUILD=ROOT/'Assemblage/preparation'
def tire_blank():
    def p(r,z):return App.Vector(r,0,z)
    edges=[];current=p(23.5,-13)
    def line(r,z):
        nonlocal current
        nxt=p(r,z);edges.append(Part.makeLine(current,nxt));current=nxt
    def arc(r1,z1,r2,z2):
        nonlocal current
        nxt=p(r2,z2);edges.append(Part.Arc(current,p(r1,z1),nxt).toShape());current=nxt
    line(25.2,-13);arc(30,-10.8,31.5,-7.5);line(31.5,7.5);arc(30,10.8,25.2,13)
    line(23.5,13);line(23.5,11.2);line(25.4,11.2);arc(28.8,9.5,29.9,6.5)
    line(29.9,-6.5);arc(28.8,-9.5,25.4,-11.2);line(23.5,-11.2);line(23.5,-13)
    s=Part.Face(Part.Wire(edges)).revolve(App.Vector(),App.Vector(0,0,1),360)
    assert s.isValid() and len(s.Solids)==1
    return s
def main():
    report=json.loads((BUILD/'preparation.json').read_text(encoding='utf-8'))
    native=App.openDocument(str(BUILD/report['native']['file']))
    assert sha(BUILD/report['native']['file'])==report['native']['sha256']
    # Store an explicit framing. fitAll alone can be unreliable without a
    # visible OpenGL viewport during unattended document generation.
    App.setActiveDocument(native.Name)
    v=Gui.activeDocument().activeView();v.setCameraType('Orthographic');v.viewAxonometric()
    rot=v.getCameraOrientation();axis=rot.Axis;angle=rot.Angle
    extents=[r['bounds_mm'] for r in report['zones']]
    centre=App.Vector(*[(min(b[2*k] for b in extents)+max(b[2*k+1] for b in extents))/2 for k in range(3)])
    position=centre+rot.multVec(App.Vector(0,0,1000))
    v.setCamera('#Inventor V2.1 ascii\n\nOrthographicCamera { viewportMapping ADJUST_CAMERA position %.9g %.9g %.9g orientation %.9g %.9g %.9g %.9g nearDistance 1 farDistance 3000 focalDistance 1000 aspectRatio 1 height 850 }' % (position.x,position.y,position.z,axis.x,axis.y,axis.z,angle))
    corrected=BUILD/'native-camera.FCStd';native.saveAs(str(corrected))
    corrected.replace(BUILD/report['native']['file'])
    report['native']['sha256']=sha(BUILD/report['native']['file'])
    report['native']['bytes']=(BUILD/report['native']['file']).stat().st_size
    report['native']['explicit_camera_height_mm']=850
    full=Glb();rolling=App.newDocument('RoulageVisuel');blank=tire_blank();reduced=[]
    for zone in report['zones']:
        g=Glb()
        for obj in native.getObject(zone['zone']).Group:
            shape=obj.Shape
            colors=colour_list(obj,len(shape.Faces));by_color={}
            if len(set(colors))==1:g.add(shape,colors[0],obj.Label)
            else:
                for face,color in zip(shape.Faces,colors):by_color.setdefault(tuple(color),[]).append(face)
                for color,faces in by_color.items():g.add(Part.makeCompound(faces),color,obj.Label)
            if zone['zone']=='roulage':
                output=rolling.addObject('Part::Feature','Visu_'+obj.Name);output.Label=obj.Label
                if obj.Label.startswith('Roue_'):
                    assert len(shape.childShapes())==3,(obj.Label,len(shape.childShapes()))
                    sign=-1 if '_G' in obj.Label else 1;y=55 if '_AV_' in obj.Label else 445
                    tire=blank.copy();tire.Placement=App.Placement(App.Vector(sign*200,y,31.5),App.Rotation(App.Vector(0,1,0),sign*90))
                    children=shape.childShapes();rim,foam=children[1:]
                    # Keep original rim / foam; only the grooved rubber body is
                    # replaced by its original analytic section before grooves.
                    output.Shape=Part.makeCompound([tire,rim,foam])
                    counts=[len(c.Faces) for c in children]
                    tire_col=colors[0];rest=colors[counts[0]:]
                    output.ViewObject.DiffuseColor=[tire_col]*len(tire.Faces)+rest
                    output.Label+=' [pneu sans rainures pour visualisation]';reduced.append(obj.Label)
                else:output.Shape=shape.copy();output.ViewObject.DiffuseColor=colors
        path=BUILD/('drone-v3-'+zone['zone']+'.glb');zone['glb']=g.write(path);full.parts.extend(g.parts)
        sys.__stdout__.write('GLB '+zone['zone']+' '+str(path.stat().st_size)+'\n');sys.__stdout__.flush()
    rolling.recompute();path=BUILD/'drone-v3-roulage.step';ImportGui.export(rolling.RootObjects,str(path))
    zone=next(z for z in report['zones'] if z['zone']=='roulage')
    zone['step_bytes']=path.stat().st_size;zone['step_sha256']=sha(path)
    zone['view_tires_without_grooves']=reduced
    # Rebuild full viewing STEP from its four current independent exports.
    complete=App.newDocument('VueComplete')
    for zone in report['zones']:ImportGui.insert(name=str(BUILD/zone['step_file']),docName=complete.Name,merge=False,useLinkGroup=False)
    p=BUILD/report['view_step']['file'];ImportGui.export(complete.RootObjects,str(p))
    report['view_step']['bytes']=p.stat().st_size;report['view_step']['sha256']=sha(p)
    report['full_glb']=full.write(BUILD/'drone-v3-complet-ultra-detaille.glb')
    report['preview_glb_tessellation']=dict(linear_mm=.18,angular_radians=.35,exact_source_surfaces=True)
    report['step_preview_simplifications']=['Petits détails électroniques omis et intérieurs électroniques complexes remplacés par leurs enveloppes','Quatre pneus : profil exact avant rainures ; jantes et inserts conservés','Géométrie native FreeCAD inchangée et intégrale']
    assert sha(BUILD/report['native']['file'])==report['native']['sha256']
    (BUILD/'preparation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    sys.__stdout__.write('PREVIEWS DONE '+str(report['view_step']['bytes'])+' bytes STEP / '+str(report['full_glb']['bytes'])+' bytes GLB\n');sys.__stdout__.flush();os._exit(0)
if __name__=='__main__':main()
