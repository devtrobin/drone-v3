"""Photo-informed coloured STEP of one HobbyPark B0CTNVV7BJ Color A wheel.

Published nominal envelope/interfaces, estimated unreported detail. No other
component is rebuilt. Run in the project's CadQuery / OCP environment.
"""
from pathlib import Path
import argparse,hashlib,json,math,time
import cadquery as cq
import numpy as np
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.TDF import TDF_LabelSequence
from OCP.XCAFDoc import XCAFDoc_DocumentTool
from OCP.IFSelect import IFSelect_RetDone
from render_step_meshes import render_meshes

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'Composants/roues/3D'
PARAMS={'tire_diameter_mm':63,'tire_width_mm':26,'nominal_inner_diameter_mm':47,
        'axle_bore_mm':4,'hex_across_flats_mm':12,'spokes':18,'tread_repetitions':24,
        'hex_depth_mm_estimated':3.5,'hex_rear_datum_z_mm_estimated':5.0,
        'tread_cut_radius_mm_estimated':.62,'front_spoke_depth_mm_estimated':2.2}
COLORS={'tire':(.055,.060,.065),'rim':(.028,.032,.037),'foam':(.19,.20,.21)}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cyl(r,h,z=0):return cq.Solid.makeCylinder(r,h,cq.Vector(0,0,z),cq.Vector(0,0,1))
def ring(ro,ri,h,z=0):return cyl(ro,h,z).cut(cyl(ri,h+.02,z-.01))

def tire_blank():
    # Cross-section coordinates are radius and axial z, revolved about Z.
    # Straight central tread fixes maximum radius at exactly 31.5 mm.
    p=(cq.Workplane('XZ').moveTo(23.5,-13).lineTo(25.2,-13)
       .threePointArc((30.0,-10.8),(31.5,-7.5)).lineTo(31.5,7.5)
       .threePointArc((30.0,10.8),(25.2,13)).lineTo(23.5,13)
       .lineTo(23.5,11.2).lineTo(25.4,11.2)
       .threePointArc((28.8,9.5),(29.9,6.5)).lineTo(29.9,-6.5)
       .threePointArc((28.8,-9.5),(25.4,-11.2)).lineTo(23.5,-11.2).close())
    return p.revolve(360,(0,0),(0,1)).val()

def groove(angle,side):
    # Long curved herringbone grooves seen in photos 01/03/06. Pitch/depth
    # are estimates; not a tire mould specification.
    points=[]
    for i in range(7):
        t=i/6;z=side*(.8+10.0*t);theta=angle+.04+.24*t+.10*t*t
        r=31.68-.10*max(abs(z)-7.5,0)**2
        points.append(cq.Vector(r*math.cos(theta),r*math.sin(theta),z))
    edge=cq.Edge.makeSpline(points)
    profile=cq.Workplane(cq.Plane(origin=points[0],normal=edge.tangentAt(0))).circle(.62)
    return profile.sweep(cq.Workplane('XY').newObject([cq.Wire.assembleEdges([edge])]),isFrenet=True).val()

def tire():
    s=tire_blank()
    s=s.cut(cq.Solid.makeTorus(31.65,.28))
    for z in [-9.7,9.7]:
        s=s.cut(cq.Solid.makeTorus(31.05,.42,cq.Vector(0,0,z),cq.Vector(0,0,1)))
    for i in range(PARAMS['tread_repetitions']):
        angle=2*math.pi*i/PARAMS['tread_repetitions']
        for side in [-1,1]:s=s.cut(groove(angle,side))
        # Short transverse shoulder cuts, visible on the narrow edge ribs.
        for side in [-1,1]:
            a=angle+.38;r=30.5
            start=cq.Vector(r*math.cos(a),r*math.sin(a),side*10.0)
            cutter=cq.Solid.makeCylinder(.48,2.7,start,cq.Vector(0,0,side))
            s=s.cut(cutter)
        if i%6==0:print('TREAD',i,'/',PARAMS['tread_repetitions'],flush=True)
    assert s.isValid() and len(s.Solids())==1
    return s.clean()

def rim():
    s=ring(23.05,21.9,24.8,-12.4)
    pieces=[ring(23.5,21.9,.75,11.65),ring(23.5,21.9,.75,-12.4),
            ring(23.5,22.85,.32,10.90),ring(23.5,22.85,.32,-11.50),
            cyl(8.65,4.9,5.0),cyl(6.8,1.3,9.9)]
    for i in range(5):
        a=2*math.pi*i/5+.2
        pieces.append(cq.Solid.makeCylinder(1.45,1.3,cq.Vector(7.2*math.cos(a),7.2*math.sin(a),9.9),cq.Vector(0,0,1)))
    outline=[(6.5,-1.7),(10,-1.65),(22.65,-.75),(23.0,-.55),
             (23.0,.55),(22.65,.75),(10,1.65),(6.5,1.7)]
    spoke=cq.Workplane('XY').polyline(outline).close().extrude(2.2)
    spoke=spoke.edges('|Z').fillet(.32).val()
    spoke=spoke.rotate((0,0,0),(0,1,0),-10).translate((0,0,5.7))
    for i in range(PARAMS['spokes']):pieces.append(spoke.rotate((0,0,0),(0,0,1),i*360/PARAMS['spokes']))
    s=s.fuse(*pieces).clean()
    s=s.cut(cyl(2.0,28,-14))
    # Nominal AF12 rear socket, depth and axial placement unknown in sources.
    socket=cq.Workplane('XY').polygon(6,12/math.cos(math.pi/6)).extrude(3.5).val()
    socket=socket.rotate((0,0,0),(0,0,1),30).translate((0,0,5.0))
    s=s.cut(socket)
    # Front dish and five shallow moulded circles observed, not real bolts.
    s=s.cut(cyl(3.55,.50,10.7))
    for i in range(5):
        a=2*math.pi*i/5+.2;x,y=7.2*math.cos(a),7.2*math.sin(a)
        s=s.cut(cq.Solid.makeCylinder(.72,.22,cq.Vector(x,y,10.98),cq.Vector(0,0,1)))
    # Circular ejector impressions on the rear of each spoke; no fake screw.
    for i in range(PARAMS['spokes']):
        a=2*math.pi*i/PARAMS['spokes'];r=16.0
        z=5.7+r*math.sin(math.radians(10))-.04
        s=s.cut(cq.Solid.makeCylinder(.50,.12,cq.Vector(r*math.cos(a),r*math.sin(a),z),cq.Vector(0,0,1)))
    assert s.isValid() and len(s.Solids())==1
    return s.clean()

def preview(parts,path,view,title,cut=False):
    meshes=[]
    for name,s,color in parts:
        if cut:
            # An actual section of the same geometry, solely in this preview.
            mask=cq.Workplane('XY').box(70,35,32,centered=False).translate((-35,-35,-16)).val()
            s=s.intersect(mask)
        vs,ts=s.tessellate(.08,.20)
        if not ts:continue
        c=np.array(color);c=np.where(c<=.0031308,12.92*c,1.055*np.power(c,1/2.4)-.055)
        meshes.append((np.array([v.toTuple() for v in vs]),ts,c))
    render_meshes(path,meshes,view,title,'Reconstruction depuis photos - cotes nominales et details estimes - mm')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--no-render',action='store_true');args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True);started=time.perf_counter()
    rubber=tire();plastic=rim()
    # Illustrative hidden insert, trimmed to the actual modeled cavity to avoid
    # intersections. No foam density, compression law or measured section.
    foam=ring(29.75,23.65,21.4,-10.7).cut(rubber).cut(plastic).clean()
    assert foam.isValid() and len(foam.Solids())==1
    parts=[('Pneu_caoutchouc_rainures_directionnelles',rubber,COLORS['tire']),
           ('Jante_nylon_18_branches_hex12_axe4',plastic,COLORS['rim']),
           ('Insert_mousse_geometrie_interne_estimee',foam,COLORS['foam'])]
    for i,(_,a,_) in enumerate(parts):
        for _,b,_ in parts[i+1:]:assert a.intersect(b).Volume()<1e-5
    for z in [5.2,7,9,11]:assert not plastic.isInside(cq.Vector(1.95,0,z),1e-6)
    assert not plastic.isInside(cq.Vector(5.95,0,6),1e-6)
    assert plastic.isInside(cq.Vector(6.10,0,6),1e-6)
    assembly=cq.Assembly(name='HobbyPark_Color_A_63x26_reconstruction')
    for name,s,color in parts:assembly.add(s,name=name,color=cq.Color(*color))
    candidate=OUT/'roue-hobbypark-63x26-detaillee.candidate.step'
    assembly.export(str(candidate),exportType='STEP',mode='default',unit='MM',outputUnit='MM')
    imported=cq.importers.importStep(str(candidate)).val()
    original=cq.Compound.makeCompound([s for n,s,c in parts])
    assert imported.isValid() and len(imported.Solids())==3
    volume_error=abs(imported.Volume()-original.Volume())/original.Volume()
    bb=imported.BoundingBox();before=original.BoundingBox()
    bbox_error=max(abs(getattr(bb,k)-getattr(before,k)) for k in ['xmin','xmax','ymin','ymax','zmin','zmax'])
    assert volume_error<1e-6 and bbox_error<1e-5
    assert abs(bb.xlen-63)<.001 and abs(bb.ylen-63)<.001 and abs(bb.zlen-26)<.001
    doc=TDocStd_Document(TCollection_ExtendedString('Wheel validation'))
    reader=STEPCAFControl_Reader();reader.SetColorMode(True);reader.SetNameMode(True)
    assert reader.ReadFile(str(candidate))==IFSelect_RetDone and reader.Transfer(doc)
    seq=TDF_LabelSequence();XCAFDoc_DocumentTool.ColorTool_s(doc.Main()).GetColors(seq)
    assert seq.Length()>=3
    target=OUT/'roue-hobbypark-63x26-detaillee.step';candidate.replace(target)
    metadata={'name':'HobbyPark Touring Color A, one wheel','asin':'B0CTNVV7BJ','generated_on':'2026-10-13',
       'file':target.name,'unit':'mm','bytes':target.stat().st_size,'sha256':sha(target),
       'vendor_native_cad':False,'hardware_measured':False,'axis':'Z axle; tire centered on z=0; front positive Z',
       'parameters':PARAMS,'published_nominal_dimensions':['63 mm tire OD','26 mm width','47 mm nominal inner diameter interpreted as rim/bead envelope','12 mm hex across flats','4 mm axle bore'],
       'estimates':['18-spoke visual count and reconstructed profile','24 tread pattern repetitions, .62 mm cutter radius; actual depth unmeasured','Axial hub position, hex depth 3.5 mm, dish, all wall thicknesses','Shoulder shape, bead section and foam cavity inferred','Five moulded front details and rear ejector marks; dimensions estimated','No photographic rubber grain, unreadable sidewall text or exact optical finish'],
       'validation':{'valid_after_reimport':True,'solids':3,'faces':len(imported.Faces()),'colors':seq.Length(),'volume_relative_error':volume_error,'bbox_error_mm':bbox_error,'pairwise_intersection_volume_below_mm3':1e-5,'axle_bore_and_hex_void_probes_passed':True,'build_seconds':time.perf_counter()-started},
       'bounds_mm':{k:getattr(bb,k) for k in ['xmin','xmax','ymin','ymax','zmin','zmax']},
       'source_page':'https://www.amazon.com/dp/B0CTNVV7BJ','photo_manifest':'../photos/assets.json',
       'generator':'../../../tools/build_wheel_step.py','generator_sha256':sha(Path(__file__)),
       'parts':[{'name':n,'rgb_linear':c,'volume_mm3':s.Volume(),'faces':len(s.Faces())} for n,s,c in parts],
       'limitations':['Not a certified fabrication model or tolerance drawing','No simulation of tire deformation or grip','Actual hub offset, nut and spindle must be measured','FreeCAD GUI and VSCode CAD View not tested here']}
    if not args.no_render:
        for name,view,title,cut in [
            ('vue-isometrique.png',(.55,-.85,1.05),'HobbyPark 63 x 26 | Une roue detaillee',False),
            ('vue-face.png',(0,0,1),'HobbyPark | Jante avant et passage axe',False),
            ('vue-arriere.png',(.20,-.35,-1),'HobbyPark | Empreinte hexagonale arriere',False),
            ('vue-bande-roulement.png',(1,-.35,.15),'HobbyPark | Rainures directionnelles',False),
            ('vue-coupe.png',(.5,1,.60),'HobbyPark | Coupe - interieur estime',True)]:
            preview(parts,OUT/name,view,title,cut);print('RENDER',name,flush=True)
        metadata['previews']=[{'file':p.name,'sha256':sha(p)} for p in sorted(OUT.glob('vue-*.png'))]
    (OUT/'provenance.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:metadata[k] for k in ['file','bytes','validation','bounds_mm']}),flush=True)

if __name__=='__main__':main()
