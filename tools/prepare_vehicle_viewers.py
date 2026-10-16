"""Prepare exact native FreeCAD assembly and bounded-size STEP viewing copies.

Run with D:/FreeCAD/bin/python.exe. Original exports are archived first.
The native document retains every BREP face; only viewing STEP electronics are
simplified. Component source files and manufacturing data are never rewritten.
"""
from pathlib import Path
import os,sys,json,hashlib,time,zipfile,math,struct,gc
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
import FreeCAD as App, FreeCADGui as Gui, Part, MeshPart
if not App.GuiUp:Gui.showMainWindow()
import ImportGui
sys.stdout=sys.__stdout__

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'Assemblage';BUILD=OUT/'preparation';BUILD.mkdir(exist_ok=True)
TEMP=ROOT/'tools/temp/assemblage-viewers';TEMP.mkdir(exist_ok=True)
ZONES=['structure','roulage','electronique','puissance']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bounds(s):
    # Conservative BREP bounds. Avoid expensive B-spline extrema searches;
    # triangulation caches can tighten them by a few millimetres on tyres.
    b=s.BoundBox
    return [b.XMin,b.XMax,b.YMin,b.YMax,b.ZMin,b.ZMax]
def error(a,b):return max(abs(x-y) for x,y in zip(a,b))
def centre(s):
    props=[(q.Volume,tuple(q.CenterOfMass)) for q in s.Solids]
    volume=sum(v for v,c in props)
    return [sum(v*c[k] for v,c in props)/volume for k in range(3)]
def leaves(o):
    if o.TypeId in ('App::Part','App::DocumentObjectGroup','App::LinkGroup'):
        for c in o.Group:yield from leaves(c)
    elif o.isDerivedFrom('Part::Feature') and not o.Shape.isNull():yield o
    else:raise RuntimeError(('Unrecognised STEP object',o.Name,o.TypeId))
def rgba(c):return tuple(float(x) for x in c[:3])
def colour_list(o,n):
    colors=list(o.ViewObject.DiffuseColor)
    if len(colors)==n:return [tuple(c) for c in colors]
    c=colors[0] if colors else tuple(o.ViewObject.ShapeColor)
    return [tuple(c)]*n

class Glb:
    """Exact source surfaces tessellated for viewing, with source colours."""
    def __init__(self):self.parts=[]
    def add(self,shape,color,name):
        # Explicit angular tolerance prevents FreeCAD's very fine default
        # tessellation from making portable previews unnecessarily large.
        mesh=MeshPart.meshFromShape(Shape=shape,LinearDeflection=.18,AngularDeflection=.35,Relative=False)
        v,t=mesh.Topology
        if t:self.parts.append(([(p.x*.001,p.z*.001,-p.y*.001) for p in v],t,rgba(color),name))
    def write(self,path):
        data=bytearray();views=[];access=[];meshes=[];nodes=[];materials=[];mc={}
        def buf(raw,target):
            while len(data)%4:data.append(0)
            idx=len(views);views.append(dict(buffer=0,byteOffset=len(data),byteLength=len(raw),target=target));data.extend(raw);return idx
        for verts,tris,col,name in self.parts:
            normals=[[0.,0.,0.] for _ in verts]
            for a,b,c in tris:
                p,q,r=verts[a],verts[b],verts[c]
                u=[q[k]-p[k] for k in range(3)];v=[r[k]-p[k] for k in range(3)]
                n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
                for i in (a,b,c):
                    for k in range(3):normals[i][k]+=n[k]
            for n in normals:
                l=math.sqrt(sum(x*x for x in n))
                if l:
                    for k in range(3):n[k]/=l
            pos=len(access);vi=buf(b''.join(struct.pack('<3f',*p) for p in verts),34962)
            access.append(dict(bufferView=vi,componentType=5126,count=len(verts),type='VEC3',min=[min(v[k] for v in verts) for k in range(3)],max=[max(v[k] for v in verts) for k in range(3)]))
            normal=len(access);ni=buf(b''.join(struct.pack('<3f',*n) for n in normals),34962)
            access.append(dict(bufferView=ni,componentType=5126,count=len(verts),type='VEC3'))
            indices=len(access);ii=buf(b''.join(struct.pack('<3I',*t) for t in tris),34963)
            access.append(dict(bufferView=ii,componentType=5125,count=len(tris)*3,type='SCALAR'))
            # FreeCAD display colours are sRGB; glTF baseColorFactor is linear.
            if col not in mc:
                mc[col]=len(materials)
                linear=[c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4 for c in col]
                materials.append(dict(name='Source_'+str(len(materials)),pbrMetallicRoughness=dict(baseColorFactor=linear+[1],metallicFactor=0,roughnessFactor=.65),doubleSided=True))
            meshes.append(dict(name=name,primitives=[dict(attributes=dict(POSITION=pos,NORMAL=normal),indices=indices,material=mc[col])]))
            nodes.append(dict(name=name,mesh=len(meshes)-1))
        doc=dict(asset=dict(version='2.0',generator='Drone V3 - exact BREP tessellation 0.18 mm'),scene=0,scenes=[dict(nodes=list(range(len(nodes))))],nodes=nodes,meshes=meshes,materials=materials,buffers=[dict(byteLength=len(data))],bufferViews=views,accessors=access)
        j=json.dumps(doc,separators=(',',':'),ensure_ascii=True).encode()
        j+=b' '*((-len(j))%4);data+=b'\0'*((-len(data))%4)
        path.write_bytes(struct.pack('<4sII',b'glTF',2,12+8+len(j)+8+len(data))+struct.pack('<I4s',len(j),b'JSON')+j+struct.pack('<I4s',len(data),b'BIN\0')+data)
        return dict(meshes=len(meshes),triangles=sum(len(t) for _,t,_,_ in self.parts),bytes=path.stat().st_size,sha256=sha(path))

def main():
    if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
    baseline=OUT/'sources-step-detaillees-originales.zip'
    if not baseline.exists():
        manifest=json.loads((OUT/'provenance.json').read_text(encoding='utf-8'))
        with zipfile.ZipFile(baseline,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            for row in manifest['models']:
                p=OUT/row['file'];assert sha(p)==row['sha256'];z.write(p,p.name)
            for name in ['provenance.json','validation-freecad.json']:z.write(OUT/name,name)
        with zipfile.ZipFile(baseline) as z:assert z.testzip() is None
    with zipfile.ZipFile(baseline) as z:
        old=json.loads(z.read('provenance.json'))
        source_validation=json.loads(z.read('validation-freecad.json'))
        for zone in ZONES:
            name='drone-v3-'+zone+'.step';p=TEMP/name
            expected=next(r['sha256'] for r in old['models'] if r['file']==name)
            if not p.exists() or sha(p)!=expected:p.write_bytes(z.read(name))
            assert sha(p)==expected
    native=App.newDocument('DroneV3UltraDetaille')
    native.Label='Drone V3 - assemblage complet ultra détaillé A2-R1'
    native.Comment='BREP exact conservé. Volumes réservés et limites : voir Assemblage/README.md. Les STEP voisins sont des copies simplifiées pour visualisation.'
    native.CreatedBy='Projet Drone V3'
    view=App.newDocument('DroneV3Visualisation')
    report=dict(revision='A2-R2 compatibilité visualiseurs',archive=dict(file=baseline.name,sha256=sha(baseline)),zones=[],limitations=old['explicit_missing'],GUI_screenshot_tested=False,all_original_BREP_retained_in_native=True)
    full_glb=Glb();native_total=0;view_total=0
    App.ParamGet('User parameter:BaseApp/Preferences/Mod/Part/STEP').SetString('Scheme','AP214IS')
    for zone in ZONES:
        print('IMPORT',zone,flush=True);started=time.perf_counter()
        source=App.newDocument('Source_'+zone)
        ImportGui.insert(name=str(TEMP/('drone-v3-'+zone+'.step')),docName=source.Name,merge=False,useLinkGroup=False)
        assert len(source.RootObjects)==1,(zone,[o.Name for o in source.RootObjects])
        root=source.RootObjects[0]
        ng=native.addObject('App::DocumentObjectGroup',zone);ng.Label=zone.capitalize()
        vg=view.addObject('App::DocumentObjectGroup',zone);vg.Label=zone.capitalize()+' - visualisation'
        n_shapes=[];v_shapes=[];entries=[];zone_glb=Glb()
        for index,component in enumerate(root.Group):
            if zone!='structure':print('COMPONENT',zone,component.Label,flush=True)
            exact=[];exact_colors=[];simple=[];simple_colors=[];omitted=0;proxies=0
            for obj in leaves(component):
                shape=obj.Shape.copy();shape.Placement=obj.getGlobalPlacement()
                nf=len(shape.Faces);colors=colour_list(obj,nf)
                exact.append(shape);exact_colors.extend(colors)
                # Retain all exact surface detail in GLB and native FreeCAD.
                by_color={}
                if '--mesh-first' in sys.argv:
                    if len(set(colors))==1:
                        zone_glb.add(shape,colors[0],component.Label)
                    else:
                        for face,col in zip(shape.Faces,colors):by_color.setdefault(tuple(col),[]).append(face)
                        for col,faces in by_color.items():zone_glb.add(Part.makeCompound(faces),col,component.Label)
                b=shape.BoundBox
                # STEP viewing copies omit fine electronic artwork/SMD bodies;
                # complex electronic internals become explicit envelope solids.
                # Structure, running gear and power shapes remain exact.
                small=zone=='electronique' and (max(b.XLength,b.YLength,b.ZLength)<2 or b.XLength*b.YLength*b.ZLength<.2)
                if small:omitted+=1;continue
                if zone=='electronique' and nf>150:
                    shape=Part.makeBox(b.XLength,b.YLength,b.ZLength,App.Vector(b.XMin,b.YMin,b.ZMin))
                    cols=[colors[0]]*len(shape.Faces);proxies+=1
                else:cols=colors
                simple.append(shape);simple_colors.extend(cols)
            assert exact,component.Label
            whole=Part.makeCompound(exact);n_shapes.append(whole)
            no=native.addObject('Part::Feature','Detail_'+zone+'_'+str(index));ng.addObject(no)
            no.Label=component.Label;no.Shape=whole
            no.addProperty('App::PropertyString','Representation','Provenance');no.Representation='Géométrie BREP intégrale du STEP original'
            no.ViewObject.DiffuseColor=exact_colors
            no.ViewObject.DisplayMode='Shaded'
            no.ViewObject.Deviation=.25;no.ViewObject.AngularDeflection=20
            if simple:
                vs=Part.makeCompound(simple);v_shapes.append(vs)
                vo=view.addObject('Part::Feature','Visu_'+zone+'_'+str(index));vg.addObject(vo)
                vo.Label=component.Label+(' [électronique simplifiée]' if omitted or proxies else '')
                vo.Shape=vs;vo.ViewObject.DiffuseColor=simple_colors;vo.ViewObject.DisplayMode='Shaded'
            entries.append(dict(component=component.Label,exact_solids=len(whole.Solids),faces=len(whole.Faces),view_solids=sum(len(s.Solids) for s in simple),electronic_leaves_omitted=omitted,envelope_proxies=proxies))
        exact_zone=Part.makeCompound(n_shapes);simple_zone=Part.makeCompound(v_shapes)
        expected=next(r for r in source_validation['models'] if r['file']=='drone-v3-'+zone+'.step')
        assert len(exact_zone.Solids)==expected['solids'],(zone,len(exact_zone.Solids),expected['solids'])
        reference=root.Shape
        assert error(bounds(exact_zone),bounds(reference))<5,(zone,bounds(exact_zone),bounds(reference))
        # All individual BREP shapes are copied, with their global placement.
        # Exact face/solid counts and independent geometric bounds are checked.
        # Full mass-property integration is deliberately left to design checks.
        native_total+=len(exact_zone.Solids);view_total+=len(simple_zone.Solids)
        native.recompute();view.recompute()
        native.saveAs(str(TEMP/'native-checkpoint.FCStd'))
        path=BUILD/('drone-v3-'+zone+'.step')
        ImportGui.export(vg.Group,str(path))
        glb_path=BUILD/('drone-v3-'+zone+'.glb');glb=zone_glb.write(glb_path) if '--mesh-first' in sys.argv else None
        full_glb.parts.extend(zone_glb.parts)
        item=dict(zone=zone,exact_solids=len(exact_zone.Solids),exact_faces=len(exact_zone.Faces),native_components=len(ng.Group),view_solids=len(simple_zone.Solids),bounds_mm=bounds(exact_zone),volume_mm3=None,centre_mm=None,original_source_bounds_match=True,original_volume_and_centre_match=None,step_file=path.name,step_bytes=path.stat().st_size,step_sha256=sha(path),glb=glb,components=entries,seconds=time.perf_counter()-started)
        report['zones'].append(item)
        print('ZONE DONE',zone,'exact',item['exact_solids'],'view',item['view_solids'],'STEP',item['step_bytes'],flush=True)
        App.closeDocument(source.Name);del source;gc.collect()
        (BUILD/'progress.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('SAVE NATIVE',flush=True)
    App.setActiveDocument(native.Name)
    Gui.activeDocument().activeView().setCameraType('Orthographic')
    Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll()
    native.recompute();native_path=BUILD/'drone-v3-complet-ultra-detaille.FCStd';native.saveAs(str(native_path))
    print('NATIVE SAVED',native_path.stat().st_size,flush=True)
    full_step=BUILD/'drone-v3-complet-detaille.step';ImportGui.export(view.RootObjects,str(full_step))
    report['full_glb']=full_glb.write(BUILD/'drone-v3-complet-ultra-detaille.glb') if '--mesh-first' in sys.argv else None
    report['native']=dict(file=native_path.name,bytes=native_path.stat().st_size,sha256=sha(native_path),solids=native_total,features=sum(r['native_components'] for r in report['zones']))
    report['view_step']=dict(file=full_step.name,bytes=full_step.stat().st_size,sha256=sha(full_step),solids=view_total)
    report['all_original_BREP_solids_preserved']=native_total==5441
    assert report['all_original_BREP_solids_preserved']
    (BUILD/'preparation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('DONE',json.dumps(report['native']),json.dumps(report['view_step']),flush=True)
    # Qt's offscreen GUI teardown can return an error despite successful saves.
    sys.stdout.flush();os._exit(0)
if __name__=='__main__':main()
