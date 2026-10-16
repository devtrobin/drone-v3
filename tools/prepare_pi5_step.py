"""Prepare the official Pi 5 STEP with graphics, preserving its exact geometry.

Run with tools/temp/cad-env/Scripts/python.exe. No other component is rebuilt.
The compressed vendor source in Composants/raspberry-pi-5/3D is authoritative.
"""
from pathlib import Path
import argparse, ast, hashlib, json, pickle, shutil, zipfile, time
import cadquery as cq
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.TDF import TDF_LabelSequence, TDF_Label
from OCP.TDataStd import TDataStd_Name
from OCP.XCAFDoc import XCAFDoc_DocumentTool, XCAFDoc_ColorSurf, XCAFDoc_ColorGen
from OCP.Quantity import Quantity_Color
from OCP.TopLoc import TopLoc_Location
from OCP.IFSelect import IFSelect_RetDone

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'Composants/raspberry-pi-5/3D'
TMP=ROOT/'tools/temp/raspberry-pi-5-native'
STEP_NAME='raspberry-pi-5-officiel-avec-graphismes.step'
ZIP_NAME='raspberry-pi-5-officiel-avec-graphismes.zip'
SOURCE_URL='https://pip-assets.raspberrypi.com/categories/892-raspberry-pi-5/documents/RP-010082-CA-1-rpi-5%203D%20STEP%20-%20With%20Graphics%20large%20file.zip'
EXPECTED_ZIP_HASH='1b38b554a317411bc60604f066ae004273e6c857778ecf997925ea0b56b44e0b'
EXPECTED_STEP_HASH='625683b44669593fbeba2fecb9b3555b7e5a16c846c7fde0eab505c66478b3e0'
MEMBER='rpi-5b_with_graphics.step'

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def prepare_source():
    OUT.mkdir(parents=True,exist_ok=True);TMP.mkdir(parents=True,exist_ok=True)
    archive=OUT/ZIP_NAME
    if not archive.exists():shutil.copyfile(TMP/'pi5-with-graphics-official.zip',archive)
    assert sha(archive)==EXPECTED_ZIP_HASH
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        target=OUT/STEP_NAME
        if not target.exists() or sha(target)!=EXPECTED_STEP_HASH:
            # Explicit member names only: no arbitrary archive paths are extracted.
            temporary=TMP/'delivered-step-candidate.step'
            with z.open(MEMBER) as src,temporary.open('wb') as dst:shutil.copyfileobj(src,dst)
            assert sha(temporary)==EXPECTED_STEP_HASH
            temporary.replace(target)
        (OUT/'LICENSE-constructeur.txt').write_bytes(z.read('LICENSE.txt'))
    return target

def read_xcaf(path):
    print('Reading STEP / XCAF',flush=True)
    doc=TDocStd_Document(TCollection_ExtendedString('Raspberry Pi 5 official'))
    reader=STEPCAFControl_Reader();reader.SetNameMode(True);reader.SetColorMode(True)
    assert reader.ReadFile(str(path))==IFSelect_RetDone
    print('Transferring STEP assembly',flush=True)
    assert reader.Transfer(doc)
    return doc

def label_name(label):
    a=TDataStd_Name()
    return a.Get().ToExtString() if label.FindAttribute(TDataStd_Name.GetID_s(),a) else ''

def label_colour(label,ct,default):
    for kind in [XCAFDoc_ColorSurf,XCAFDoc_ColorGen]:
        c=Quantity_Color()
        if ct.GetColor_s(label,kind,c):return (c.Red(),c.Green(),c.Blue())
    return default

def collect_leaves(doc):
    st=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main());ct=XCAFDoc_DocumentTool.ColorTool_s(doc.Main())
    roots=TDF_LabelSequence();st.GetFreeShapes(roots)
    leaves=[]
    def walk(label,loc=TopLoc_Location(),color=(.65,.65,.65)):
        color=label_colour(label,ct,color)
        if st.IsReference_s(label):
            ref=TDF_Label();assert st.GetReferredShape_s(label,ref)
            walk(ref,loc.Multiplied(st.GetLocation_s(label)),color)
            return
        children=TDF_LabelSequence()
        if st.GetComponents_s(label,children):
            for i in range(1,children.Length()+1):walk(children.Value(i),loc,color)
        else:
            raw=st.GetShape_s(label)
            if raw.IsNull():return
            placed=raw.Moved(loc)
            leaves.append((label_name(label),cq.Shape.cast(placed),color,raw))
    for i in range(1,roots.Length()+1):walk(roots.Value(i))
    colours=TDF_LabelSequence();ct.GetColors(colours)
    whole=cq.Compound.makeCompound([cq.Shape.cast(st.GetShape_s(roots.Value(i))) for i in range(1,roots.Length()+1)])
    return leaves,whole,ct,roots.Length(),colours.Length()

def mesh_shapes(leaves,ct):
    meshes=[];missing=0
    for i,(name,shape,col,raw) in enumerate(leaves):
        # Vendor styles can apply to individual faces; preserve them in previews.
        colored_faces=[]
        raw_faces=cq.Shape.cast(raw).Faces();placed_faces=shape.Faces()
        assert len(raw_faces)==len(placed_faces)
        has_face_styles=False
        for f,placed in zip(raw_faces,placed_faces):
            fc=col
            for kind in [XCAFDoc_ColorSurf,XCAFDoc_ColorGen]:
                c=Quantity_Color()
                if ct.GetColor(f.wrapped,kind,c):
                    fc=(c.Red(),c.Green(),c.Blue());has_face_styles=True;break
            colored_faces.append((placed,fc))
        elements=colored_faces if has_face_styles else [(shape,col)]
        for element,colour in elements:
            try:
                vs,ts=element.tessellate(.12,.24)
            except Exception:
                # A second OCCT tessellation attempt, not a substituted geometry.
                vs,ts=element.tessellate(.2,.3)
            if not ts:
                if element.Faces():missing+=1
                continue
            meshes.append((np.asarray([v.toTuple() for v in vs],dtype=float),ts,np.asarray(colour,dtype=float)))
        if i%250==0:print('MESH',i,'/',len(leaves),flush=True)
    assert not missing,missing
    print('MESH complete',len(meshes),'groups',sum(len(x[1]) for x in meshes),'triangles',flush=True)
    return meshes

camera_tree=ast.parse((ROOT/'tools/build_camera_step.py').read_text(encoding='utf-8'))
render_node=next(n for n in camera_tree.body if isinstance(n,ast.FunctionDef) and n.name=='render')
for node in ast.walk(render_node):
    if isinstance(node,ast.If) and ast.unparse(node.test)=='norm and np.dot(normal, view) < -1e-10':node.test=ast.Constant(False)
    if isinstance(node,ast.Constant) and isinstance(node.value,str) and node.value.startswith('Reconstruction visuelle - mm'):
        node.value='CAO officielle Raspberry Pi Ltd - geometrie et couleurs conservees'
ast.fix_missing_locations(render_node)
exec(compile(ast.Module(body=[render_node],type_ignores=[]),str(ROOT/'tools/build_camera_step.py'),'exec'))

def previews(meshes):
    global MESH_CACHE
    from render_step_meshes import render_meshes
    # XCAF Quantity_Color returns linear RGB; PNG pixels must use sRGB.
    MESH_CACHE=[(v,t,np.where(c<=.0031308,12.92*c,1.055*np.power(c,1/2.4)-.055)) for v,t,c in meshes]
    for filename,view,title in [
        ('vue-dessus.png',(0,0,1),'Raspberry Pi 5 | Vue de dessus'),
        ('vue-dessous.png',(0,0,-1),'Raspberry Pi 5 | Vue de dessous'),
        ('vue-isometrique.png',(.6,-.8,1.1),'Raspberry Pi 5 | STEP constructeur detaille'),
        ('vue-connecteurs.png',(1,-.45,.55),'Raspberry Pi 5 | Connecteurs et composants')]:
        render_meshes(OUT/filename,MESH_CACHE,view,title)
        print('RENDER',filename,flush=True)
    register=OUT/'provenance.json'
    if register.exists():
        metadata=json.loads(register.read_text(encoding='utf-8'))
        metadata.setdefault('initial_record_script_sha256',metadata['preparation_script_sha256'])
        metadata['preparation_script_sha256']=sha(Path(__file__))
        metadata['part_manifest_colour_space']='Linear RGB returned by OpenCascade Quantity_Color'
        metadata['preview_colour_space']='sRGB converted from XCAF linear RGB before shading'
        metadata['preview_renderer']='../../../tools/render_step_meshes.py'
        metadata['preview_renderer_sha256']=sha(ROOT/'tools/render_step_meshes.py')
        metadata['previews']=[{'file':p.name,'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(OUT.glob('vue-*.png'))]
        register.write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--render-only',action='store_true');parser.add_argument('--no-render',action='store_true');args=parser.parse_args()
    path=prepare_source()
    cache=TMP/'preview-meshes.pkl'
    if args.render_only:
        data=pickle.loads(cache.read_bytes())
        assert data['step_sha256']==sha(path)
        previews(data['meshes']);return
    doc=read_xcaf(path)
    leaves,whole,ct,nroots,ncolors=collect_leaves(doc)
    print('VALIDATION',len(leaves),'leaf instances',ncolors,'colors',flush=True)
    bb=whole.BoundingBox()
    leaf_bb=cq.Compound.makeCompound([s for n,s,c,r in leaves]).BoundingBox()
    placement_error=max(abs(getattr(bb,k)-getattr(leaf_bb,k)) for k in ['xmin','xmax','ymin','ymax','zmin','zmax'])
    assert placement_error<1e-4
    prior=TMP/'inspection.json'
    prior_source=TMP/'native-source.json'
    prior_valid=False
    if prior.exists() and prior_source.exists():
        source=json.loads(prior_source.read_text(encoding='utf-8'))
        report=json.loads(prior.read_text(encoding='utf-8'))
        prior_valid=source['step_sha256']==sha(path) and report['shape_valid'] is True
    invalid=[]
    if not prior_valid:
        assert whole.isValid()
        for i,(name,s,c,r) in enumerate(leaves):
            if not s.isValid():invalid.append({'index':i,'name':name})
    print('VALIDITY complete, invalid leaves:',len(invalid),flush=True)
    solids=whole.Solids()
    metadata={
        'name':'Raspberry Pi 5 - detailed official model for V3 4GB selection','file':path.name,'prepared_on':'2026-10-13','unit':'mm',
        'vendor_distributed_cad':True,'geometry_modified':False,'hardware_measured':False,'ram_variant_identified_in_cad':False,
        'source_url':SOURCE_URL,'source_archive':ZIP_NAME,'source_member':MEMBER,'source_license':'MIT - Raspberry Pi Ltd 2026',
        'source_archive_sha256':sha(OUT/ZIP_NAME),'sha256':sha(path),'bytes':path.stat().st_size,
        'native_step_timestamp':'2026-05-27T13:28:21','native_step_exporter':'FreeCAD / Open CASCADE STEP processor 7.8',
        'free_roots':nroots,'leaf_instances':len(leaves),'solids':len(solids),'faces':len(whole.Faces()),'xcaf_colours':ncolors,
        'bounds_mm':{k:getattr(bb,k) for k in ['xmin','xmax','ymin','ymax','zmin','zmax']},
        'validation':{'xcaf_import_success':True,'delivered_step_identical_to_archive_member':True,'whole_model_valid':True,'whole_validity_reused_for_identical_sha256':prior_valid,'leaf_placement_bbox_error_mm':placement_error,'invalid_leaf_shapes':invalid},
        'limitations':['Manufacturer model is for guidance only; inspect actual board before fabrication','Official model may represent another Pi 5 revision or memory variant; 4GB markings not fabricated','No inference of hidden PCB copper or validated electrical netlist from visual geometry','Flat graphic faces and any native open shapes are preserved; not all entities are closed solids','Colours are those of the vendor STEP; no photographic textures or material optical simulation'],
        'preparation_script':'../../../tools/prepare_pi5_step.py','preparation_script_sha256':sha(Path(__file__)),
        'part_manifest_colour_space':'Linear RGB returned by OpenCascade Quantity_Color',
        'renderer_source':'../../../tools/build_camera_step.py','renderer_source_sha256':sha(ROOT/'tools/build_camera_step.py'),
        'part_manifest':[{'index':i,'native_name':n,'solids':len(s.Solids()),'faces':len(s.Faces()),'rgb':c} for i,(n,s,c,r) in enumerate(leaves)]
    }
    (OUT/'provenance.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:metadata[k] for k in ['leaf_instances','solids','faces','xcaf_colours','bounds_mm','validation']}),flush=True)
    meshes=mesh_shapes(leaves,ct)
    cache.write_bytes(pickle.dumps({'step_sha256':sha(path),'meshes':meshes},protocol=5))
    if not args.no_render:previews(meshes)

if __name__=='__main__':main()
