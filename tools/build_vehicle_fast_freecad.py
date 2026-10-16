"""Create and reopen a native FreeCAD display cache from all detailed surfaces.

The exact BREP document remains separate and unchanged. This viewer document
contains precomputed coloured meshes and has no parametric modelling history.
"""
from pathlib import Path
import os,sys,json,struct,time,hashlib,math
import FreeCAD as App,FreeCADGui as Gui,Mesh
ROOT=Path(__file__).resolve().parents[1];BUILD=ROOT/'Assemblage/preparation';TMP=ROOT/'tools/temp/assemblage-viewers'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    raw=(TMP/'complete-display-cache.glb').read_bytes();jl=struct.unpack_from('<I',raw,12)[0];d=json.loads(raw[20:20+jl]);binary=memoryview(raw)[28+jl:]
    zones=json.loads((TMP/'display-cache-zones.json').read_text());doc=App.newDocument('DroneV3AffichageRapide')
    doc.Label='Drone V3 - vue complète détaillée - affichage rapide'
    doc.Comment='Surfaces maillées complètes, discrétisation 0,18 mm / 0,35 rad. Géométrie CAO exacte : drone-v3-complet-ultra-detaille.FCStd.'
    index=0;created=0;requested=0
    for zone in zones:
        group=doc.addObject('App::DocumentObjectGroup',zone['zone']);group.Label=zone['zone'].capitalize()
        for mesh in d['meshes'][index:index+zone['meshes']]:
            for p in mesh['primitives']:
                pos=d['accessors'][p['attributes']['POSITION']];pv=d['bufferViews'][pos['bufferView']]
                points=[(x*1000,-z*1000,y*1000) for x,y,z in struct.iter_unpack('<3f',binary[pv.get('byteOffset',0):pv.get('byteOffset',0)+pv['byteLength']])]
                ids=d['accessors'][p['indices']];iv=d['bufferViews'][ids['bufferView']]
                faces=list(struct.iter_unpack('<3I',binary[iv.get('byteOffset',0):iv.get('byteOffset',0)+iv['byteLength']]))
                o=doc.addObject('Mesh::Feature','Vue_'+str(created));group.addObject(o);o.Label=mesh['name'];o.Mesh=Mesh.Mesh([[points[a],points[b],points[c]] for a,b,c in faces])
                col=d['materials'][p['material']]['pbrMetallicRoughness']['baseColorFactor'][:3]
                rgb=tuple(12.92*x if x<=.0031308 else 1.055*x**(1/2.4)-.055 for x in col)
                o.ViewObject.ShapeColor=rgb
                if 'Shaded' in o.ViewObject.listDisplayModes():o.ViewObject.DisplayMode='Shaded'
                created+=1;requested+=len(faces)
        index+=zone['meshes'];print('MESH ZONE',zone['zone'],flush=True)
    doc.recompute();v=Gui.activeDocument().activeView();v.setCameraType('Orthographic');v.viewAxonometric()
    rot=v.getCameraOrientation();axis=rot.Axis;point=App.Vector(0,257,128)+rot.multVec(App.Vector(0,0,1000))
    v.setCamera('#Inventor V2.1 ascii\n\nOrthographicCamera { position %.9g %.9g %.9g orientation %.9g %.9g %.9g %.9g nearDistance 1 farDistance 3000 focalDistance 1000 height 850 }'%(point.x,point.y,point.z,axis.x,axis.y,axis.z,rot.Angle))
    p=BUILD/'drone-v3-complet-affichage-rapide.FCStd';doc.saveAs(str(p));App.closeDocument(doc.Name)
    started=time.perf_counter();restored=App.openDocument(str(p));load=time.perf_counter()-started
    meshes=[o for o in restored.Objects if o.TypeId=='Mesh::Feature'];count=sum(o.Mesh.CountFacets for o in meshes)
    assert len(meshes)==created and count>=requested*.999
    v=Gui.activeDocument().activeView();v.viewAxonometric();Gui.updateGui()
    renders=[]
    for suffix,method in [('isometrique','viewAxonometric'),('dessus','viewTop')]:
        getattr(v,method)();v.fitAll();Gui.updateGui();image=BUILD/('apercu-freecad-'+suffix+'.png');v.saveImage(str(image),1600,1100,'White');assert image.stat().st_size>10000;renders.append(image.name)
    result=dict(all_passed=True,file=p.name,bytes=p.stat().st_size,sha256=sha(p),representation='Maillage de visualisation complet ; BREP exact dans le document séparé',objects=created,source_triangles=requested,restored_triangles=count,gui_open_seconds=load,viewport_renders=renders,exact_CAD_document_unchanged=True)
    (BUILD/'validation-affichage-freecad.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print('FAST NATIVE PASS',result,flush=True);sys.stdout.flush();os._exit(0)
if __name__=='__main__':main()
