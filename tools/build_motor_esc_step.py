"""Coloured, photo-informed CAD of QuicRun 2435 G3 and WP16BL30 G2.

External appearance only. Run in tools/temp/cad-env. Geometry estimates recorded.
"""
from pathlib import Path
import argparse, ast, hashlib, json, math
import cadquery as cq
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.XCAFDoc import XCAFDoc_DocumentTool
from OCP.TDF import TDF_LabelSequence
from OCP.IFSelect import IFSelect_RetDone

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'Composants/moteur/3D'; OUT.mkdir(parents=True,exist_ok=True)
COLORS={'black':(.105,.115,.123),'groove':(.035,.041,.046),'plastic':(.16,.17,.18),
 'red':(.68,.018,.065),'red_edge':(.86,.05,.09),'white':(.91,.92,.91),
 'silver':(.66,.69,.71),'steel':(.42,.46,.49),'gold':(.81,.62,.24),
 'yellow':(.95,.68,.08),'blue':(.10,.30,.62),'orange':(.90,.35,.06),
 'pink':(.86,.17,.43),'boot':(.30,.28,.22),'led':(.35,.08,.06)}

def box(l,w,h,x,y,z,r=0):
 s=cq.Workplane('XY').box(l,w,h,centered=False)
 if r:s=s.edges('|Z').fillet(r)
 return s.val().translate((x,y,z))

def cyl(r,h,x=0,y=0,z=0,axis=(0,0,1)):
 return cq.Solid.makeCylinder(r,h,cq.Vector(x,y,z),cq.Vector(*axis))

def ring(ro,ri,h,x=0,y=0,z=0):
 return cyl(ro,h,x,y,z).cut(cyl(ri,h+.02,x,y,z-.01))

def chars(value,size,height=.014):
 return cq.Workplane('XY').text(value,size,height,font='Arial',halign='center',valign='center',combine=False).val()

def rod(a,b,r):
 a,b=cq.Vector(*a),cq.Vector(*b);v=b-a
 return cq.Solid.makeCylinder(r,v.Length,a,v.normalized())

class Model:
 def __init__(self,name,curve_kind='spline'):
  self.name=name;self.parts=[];self.curve_kind=curve_kind;self.wire_paths=[]
 def add(self,name,s,color='black',basis='photo_estimate',group='body'):
  if not s.isValid() or s.Volume()<=0:raise ValueError('Invalid: '+name)
  rgb=COLORS[color] if isinstance(color,str) else color
  self.parts.append((name,s,rgb,basis,group));return s
 def label(self,name,value,x,y,z,size,rotation=None,color='white',group='body'):
  s=chars(value,size)
  if rotation:s=s.rotate(*rotation)
  return self.add(name,s.translate((x,y,z)),color,'visible_marking_font_approximation',group)
 def wrap(self,name,value,z,size,center_angle=-math.pi/2,r=12.006):
  # Each glyph tangent to the cylinder; shallow geometric print, not a bitmap.
  width=size*.66
  for i,c in enumerate(value):
   if c==' ':continue
   theta=center_angle+(i-(len(value)-1)/2)*width/r
   s=chars(c,size).rotate((0,0,0),(1,0,0),90).rotate((0,0,0),(0,0,1),math.degrees(theta)+90)
   self.add(name+f'_{i:02}',s.translate((r*math.cos(theta),r*math.sin(theta),z)),'white','visible_marking_wrap_font_approximation')
 def wire(self,name,points,r,color='black',group='cables'):
  vs=[cq.Vector(*p) for p in points]
  edge=cq.Edge.makeBezier(vs) if self.curve_kind=='bezier' else cq.Edge.makeSpline(vs)
  tangent=edge.tangentAt(0)
  profile=cq.Workplane(cq.Plane(origin=vs[0],normal=tangent)).circle(r)
  s=profile.sweep(cq.Workplane('XY').newObject([cq.Wire.assembleEdges([edge])]),isFrenet=True).val()
  self.add(name,s,color,'cable_diameter_and_pose_estimated',group)
  self.wire_paths.append({'part':name,'edge':edge,'radius':r})
  return edge

def motor():
 m=Model('Hobbywing_QuicRun_2435SL_G3_4500KV')
 # Front datum z=0, rear z=36. Shaft projects towards -z.
 hole_specs=[(8.5,75,1.5,'M3'),(8.5,255,1.5,'M3'),
             (8,15,1.25,'M2_5'),(8,195,1.25,'M2_5'),
             (7,135,1.25,'M2_5'),(7,315,1.25,'M2_5')]
 front=ring(12,2.45,4.3)
 for i,(r,a,rr,thread) in enumerate(hole_specs):
  x,y=r*math.cos(math.radians(a)),r*math.sin(math.radians(a))
  front=front.cut(cyl(rr,4.01,x,y,-.01))
  front=front.cut(cq.Solid.makeCone(rr+.22,rr,.28,cq.Vector(x,y,0),cq.Vector(0,0,1)))
  # Dark floor at documented 4 mm depth; no invented helical threads.
  m.add(f'Fixation_{i}_{thread}_dark_floor',cyl(rr-.02,.025,x,y,3.975),'groove','published_hole_depth_interpreted_pattern')
 m.add('Front_black_anodised_endbell',front,'black','published_diameter_estimated_cap_thickness')
 can=ring(12,11.0,29.7,z=4.3)
 # Smooth roots and crests of cooling grooves from product photos.
 # 17 circumferential grooves; positions and depths visually reconstructed.
 for i in range(17):
  z=8.0+i*1.05
  can=can.cut(cq.Solid.makeTorus(12.08,.32,cq.Vector(0,0,z),cq.Vector(0,0,1)))
 m.add('Ribbed_black_anodised_motor_can',can,'black','published_outer_envelope_photo_grooves_wall_estimate')
 m.add('Front_endbell_joint_dark_line',ring(12.005,11.80,.065,z=4.235),'groove')
 m.add('Rear_endbell_joint_dark_line',ring(12.005,11.80,.075,z=33.93),'groove')
 m.add('Rear_red_anodised_endbell',cyl(12,2,z=34),'red','published_body_length_estimated_cap_thickness')
 m.add('Front_bearing_visible_metal_ring',ring(2.45,1.04,.22,z=.03),'silver','bearing_bore_visible_estimate')
 m.add('Front_bearing_black_seal',ring(2.15,1.18,.03,z=.017),'groove')
 shaft=cyl(1,12,z=-12)
 # Drawing: shaft 2 mm, flat-to-opposite dimension 1.7, flat length 9.
 shaft=shaft.cut(box(2,4,9,0.70,-2,-12))
 shaft=shaft.intersect(cq.Solid.makeCone(.85,1,.20,cq.Vector(0,0,-12),cq.Vector(0,0,1)).fuse(cyl(1,11.8,z=-11.8)))
 m.add('Steel_D_shaft_2mm_flat_1_7mm_length_9mm',shaft,'silver','published_diameter_projection_flat_and_flat_length')
 m.add('Shaft_shoulder',cyl(1.55,.23,z=-.23),'steel','photo_estimated_shoulder')
 m.wrap('Can_QUICRUN','QUICRUN',30.8,2.05)
 m.wrap('Can_model','2435 G3',27.9,1.30)
 m.wrap('Can_KV','4500KV',26.15,.92)
 m.wrap('Opposite_brand','HOBBYWING',5.7,1.0,math.pi/2)
 m.label('Rear_cap_brand','QUICRUN',0,0,36.008,2.4)
 m.label('Rear_cap_model','2435 G3',0,-2.2,36.008,1.2)
 for letter,x in zip('CBA',[-3.9,0,3.9]):m.label('Rear_phase_'+letter,letter,x,-8.0,36.008,1.25)
 # Cable exit moulding at rear circumference, three separately routable leads.
 m.add('Rear_cable_exit_seal',box(9.0,3.5,3.0,-4.5,-13.0,32.6,1.2),'plastic')
 for i,(x,col) in enumerate(zip([-3.1,0,3.1],['orange','yellow','blue'])):
  endx=x*2.2
  m.add(f'Motor_phase_{i}_exit_grommet',cyl(1.7,2,x,-12,34,axis=(0,-1,0)),'groove',group='cables')
  wire=m.wire(f'Motor_phase_{i}_silicone_cable',[(x,-12,34),(x,-19,35),(endx,-37,37),(endx,-64,37)],1.5)
  # Connector aligned along -y, adapt local z tube to world cable endpoint.
  pose=lambda s:s.rotate((0,0,0),(1,0,0),90).translate((endx,-64,37))
  sleeve=cq.Solid.makeCone(1.6,2.2,2).fuse(cyl(2.2,8,z=2))
  m.add(f'Motor_phase_{i}_colour_heatshrink',pose(sleeve),col,group='cables')
  bullet=cyl(1.75,8,z=10)
  for k in range(4):
   slot=box(.16,4,5,-.08,-2,12.8).rotate((0,0,0),(0,0,1),k*45)
   bullet=bullet.cut(slot)
  bullet=bullet.fuse(cyl(1.98,.8,z=9.6))
  m.add(f'Motor_phase_{i}_3_5mm_gold_split_bullet',pose(bullet),'gold','published_connector_diameter_estimated_split_detail','cables')
  m.add(f'Motor_phase_{i}_gold_tip',pose(cq.Solid.makeCone(1.75,1.4,.4,cq.Vector(0,0,18),cq.Vector(0,0,1))),'gold',group='cables')
  tangent=wire.tangentAt(.60);normal=tangent.cross(cq.Vector(1,0,0)).normalized()
  if normal.z<0:normal=-normal
  pt=wire.positionAt(.60)+normal*1.51
  marking=cq.Workplane(cq.Plane(origin=pt,xDir=tangent,normal=normal)).text('14AWG',.70,.008,font='Arial',halign='center',valign='center',combine=False).val()
  m.add(f'Motor_phase_{i}_cable_print',marking,'white','photographic_cable_marking_estimate','cables')
 return m

def esc():
 m=Model('Hobbywing_QuicRun_WP16BL30_G2',curve_kind='bezier')
 L,W,H=33.4,26.8,15.1
 case=box(L,W,12.4,0,0,0,1.5)
 case=case.cut(box(L-3,W-3,10.6,1.5,1.5,1.85,1.0))
 m.add('Black_polymer_case_33_4x26_8',case,'black','published_xy_estimated_wall_and_split')
 m.add('Sealed_top_dark_potting',box(L-3.2,W-3.2,1.0,1.6,1.6,10.6,.9),'groove','visible_potting_no_internals_reconstructed')
 m.add('Bottom_base_cover',box(L-.45,W-.45,.35,.225,.225,0,1.3),'plastic')
 # Visible red extrusion, transverse ribs interrupted by capacitor.
 sink=box(21.2,23.4,.8,6.1,1.7,11.6,.45)
 capx,capy=25.3,21.7
 capcut=cyl(4.05,5,capx,capy,11.5)
 m.add('Red_anodised_heatsink_base',sink.cut(capcut),'red')
 for i,y in enumerate([2.1,4.8,7.5,10.2,16.6,19.3,22.0,24.7]):
  fin=box(21.2,.75,2.66,6.1,y,12.4,.18).cut(capcut)
  m.add(f'Red_heatsink_fin_{i}',fin,'red','photo_fin_layout_published_total_height')
  crest=box(21.0,.16,.04,6.2,y+.10,15.06).cut(capcut)
  if crest.Volume()>0:m.add(f'Heatsink_crest_highlight_{i}',crest,'red_edge')
 m.add('Heatsink_logo_platform',box(21.2,4.0,.65,6.1,11.75,12.4,.2),'red')
 m.label('Heatsink_brand','HOBBYWING',16.7,13.65,13.057,1.5,((0,0,0),(0,0,1),180))
 # Exposed aluminium electrolytic can and photographed white/pink cap label.
 m.add('Visible_capacitor_black_sleeve',cyl(3.65,3.35,capx,capy,11.45),'black','visible_capacitor_dimensions_estimated')
 m.add('Capacitor_metal_top_rim',ring(3.55,3.32,.07,capx,capy,14.77),'silver')
 m.add('Capacitor_white_top_label',cyl(3.32,.025,capx,capy,14.805),'white')
 crescent=cyl(3.31,.015,capx,capy,14.831).intersect(box(2.2,7,.05,capx+1.1,capy-3.5,14.82))
 m.add('Capacitor_pink_label_edge',crescent,'pink')
 # Unreadable capacitor value not invented.
 for i,(x,y) in enumerate([(3.0,23.2),(30.6,8.1)]):
  m.add(f'Top_recess_{i}',cyl(.72,.15,x,y,11.63),'groove')
 # Two long side decals with simple geometric lettering and colour accents.
 for side,y,angle in [('front',-.040,90),('rear',W+.012,-90)]:
  decal=box(29.2,.028,8.2,2.1,y,2.15,.01)
  m.add('Side_label_'+side,decal,'groove')
  ty=-.070 if side=='front' else W+.070
  m.label('Side_brand_'+side,'QUICRUN',16.7,ty,7.65,2.65,((0,0,0),(1,0,0),angle))
  for value,x,col in [('WP',5.3,'white'),('16',11.0,'white'),('BL',15.5,'white'),('30',20.0,'white'),('G2',25.0,'white')]:
   if value=='BL':m.add('BL_red_background_'+side,box(4.3,.012,2.7,13.35,-.055 if side=='front' else W+.045,3.0),'red')
   m.label('Side_model_'+side+'_'+value,value,x,ty,4.3,1.9 if value!='G2' else .75,((0,0,0),(1,0,0),angle),col)
  m.add('Water_mark_'+side,cyl(.34,.03,2.8,y,4.6,axis=(0,-1 if side=='front' else 1,0)),'blue')
 for i,(letter,y) in enumerate(zip('ABC',[5.2,13.4,21.6])):
  # Small printed phase identification on left face.
  s=chars(letter,1.1).rotate((0,0,0),(0,1,0),-90).translate((-.015,y,8.7))
  m.add('Phase_mark_'+letter,s,'white','visible_print')
 m.label('Right_cell_count','2-3S',L+.02,13.4,5.5,1.7,((0,0,0),(0,1,0),90))
 # Output cable pose is an assembly example, not a measured installed path.
 for i,y in enumerate([4.6,13.4,22.2]):
  m.add(f'Phase_{i}_exit_seal',cyl(1.65,1.8,2.8,y,11.4,axis=(-1,0,0)),'groove',group='cables')
  m.wire(f'ESC_phase_{i}_16AWG',[(2.8,y,11.4),(-8,y,17),(-25,y,19),(-53,y,19)],1.5)
  m.add(f'Phase_{i}_connector_insulation_neck',rod((-51.5,y,19),(-55.5,y,19),1.5),'black','photo_estimated_overlapping_insulation_transition','cables')
  local=lambda s:s.rotate((0,0,0),(0,1,0),-90).translate((-53,y,19))
  housing=cyl(2.30,11).cut(cyl(1.85,7.5,z=4.0))
  # Keep material pieces separate for robust STEP exchange; overlap the neck.
  m.add(f'Phase_{i}_black_socket_boot',local(housing),'black',group='cables')
  m.add(f'Phase_{i}_female_gold_socket',local(ring(1.84,1.75,6.8,z=4.2)),'gold','published_3_5mm_contact_estimated_boot','cables')
  m.add(f'Phase_{i}_socket_dark_floor',local(cyl(1.74,.015,z=4.16)),'groove',group='cables')
  m.add(f'Phase_{i}_socket_boot_collar',local(ring(2.4,2.3,.50,z=1.5)),'plastic',group='cables')
 # Two power cables to XT60, nominal published cable length 75 mm.
 for i,(y,colour) in enumerate([(4.2,'red'),(22.6,'black')]):
  endy=13.4+(-3.6 if i==0 else 3.6)
  m.wire('Battery_'+colour+'_16AWG',[(30.8,y,11.6),(43,y,19),(69,endy,17),(100,endy,12)],1.6,colour)
  m.add('Power_exit_seal_'+colour,cyl(1.8,1.1,30.8,y,11.4),'groove',group='cables')
 # XT60 connector is drawn in a fixed pose with recessed male gold contacts.
 plug=box(12.4,16.2,8.4,103,5.3,7.8,1.0)
 for y in [9.8,17.0]:plug=plug.cut(cyl(2.45,8,108,y,12,axis=(1,0,0)))
 m.add('XT60_yellow_moulded_shell',plug,'yellow','connector_shape_and_pose_photo_estimate','cables')
 for i,y in enumerate([9.8,17.0]):
  m.add(f'XT60_gold_contact_{i}',cyl(1.75,5.6,108,y,12,axis=(1,0,0)),'gold',group='cables')
  m.add(f'XT60_contact_base_{i}',cyl(2.12,.5,108,y,12,axis=(1,0,0)),'gold',group='cables')
 m.add('XT60_black_rear_strain_relief',box(8.0,16.0,8.2,95,5.4,7.9,.7),'plastic',group='cables')
 for i in range(3):m.add(f'XT60_boot_grip_rib_{i}',box(.25,13,.16,97+i*1.6,6.9,16.1),'black',group='cables')
 m.label('XT60_embossing','XT60',109,13.4,16.215,1.55,color='yellow',group='cables')
 m.label('XT60_polarity_plus','+',113,8.2,16.215,1.7,color='yellow',group='cables')
 # Low-current lead colours and separated programmer signal.
 for i,col in enumerate(['white','red','black']):
  m.wire('Receiver_signal_'+col,[(32,12+i*.9,8.5),(44,15+i*.9,6),(60,29+i*.9,3),(88,41+i*.9,3)],.43,col)
 m.wire('Yellow_program_signal',[(32,15.2,8.5),(46,19,7),(58,36,3),(75,45.5,3)],.43,'yellow')
 # Generic JR-type 3-pin shell; exact manufacturer connector not dimensioned.
 receiver=box(10.2,5.3,4.6,88,40.4,.7,.3)
 for i in range(3):receiver=receiver.cut(box(5.8,1.1,2.8,92.5,41.15+i*1.45,1.5))
 m.add('Receiver_3pin_black_housing',receiver,'black','unpublished_connector_pitch_and_shell_estimates','cables')
 for i in range(3):m.add(f'Receiver_gold_contact_{i}',box(2.8,.7,.25,92.6,41.35+i*1.45,2.15),'gold',group='cables')
 m.add('Programmer_1pin_housing',box(8.8,2.5,3.4,75,44.7,1.3,.25),'black',group='cables')
 # Switch unit: metal rim, four screw heads, flexible brown-grey weather boot.
 sx,sy=47,-23
 sw=box(17,11.2,4.0,sx,sy,0,.7)
 m.add('Switch_black_base',sw,'black','photo_estimated_switch_dimensions','switch')
 rim=box(16.4,10.6,.55,sx+.3,sy+.3,4,.5).cut(box(12.5,6.8,1,sx+2.25,sy+2.2,3.8,.4))
 m.add('Switch_metal_top_frame',rim,'silver',group='switch')
 m.add('Switch_weather_boot',box(12.4,6.7,1.2,sx+2.3,sy+2.25,3.9,.7),'boot',group='switch')
 m.add('Switch_slider_boot_bulge',box(6.1,5.3,2.2,sx+7.1,sy+2.8,5.0,.8),'boot',group='switch')
 m.add('Switch_SET_boot_button',box(2.2,3.1,1.6,sx+3.5,sy+3.9,5.0,.45),'boot',group='switch')
 for i,(dx,dy) in enumerate([(1.3,1.3),(15.7,1.3),(1.3,9.9),(15.7,9.9)]):
  screw=cyl(.74,.45,sx+dx,sy+dy,4.48)
  for a in [0,90]:screw=screw.cut(box(1.3,.17,.25,sx+dx-.65,sy+dy-.085,4.72).rotate((sx+dx,sy+dy,0),(sx+dx,sy+dy,1),a))
  m.add('Switch_cross_screw_'+str(i),screw,'steel',group='switch')
 for i in range(2):m.wire('Switch_wire_'+str(i),[(32,11+i*.8,8),(42,9+i*.8,5),(61,-6+i*.8,2),(64,-18+i*.8,2)],.55,'red',group='switch')
 return m

def export(m,slug,confirmed,estimates):
 ass=cq.Assembly(name=m.name)
 for n,s,c,b,g in m.parts:ass.add(s,name=n,color=cq.Color(*c))
 path=OUT/(slug+'.step');candidate=ROOT/'tools/temp'/(slug+'-candidate.step')
 ass.export(str(candidate),exportType='STEP',mode='default',unit='MM',outputUnit='MM')
 original=cq.Compound.makeCompound([p[1] for p in m.parts]);back=cq.importers.importStep(str(candidate)).val()
 assert back.isValid() and all(s.isValid() for s in back.Solids())
 assert len(original.Solids())==len(back.Solids())
 error=abs(back.Volume()-original.Volume())/original.Volume();assert error<1e-6
 bb=back.BoundingBox();b0=original.BoundingBox()
 bb_error=max(abs(getattr(bb,k)-getattr(b0,k)) for k in ['xmin','xmax','ymin','ymax','zmin','zmax']);assert bb_error<1e-5
 doc=TDocStd_Document(TCollection_ExtendedString('Cad colour verification'))
 reader=STEPCAFControl_Reader();reader.SetColorMode(True);reader.SetNameMode(True)
 assert reader.ReadFile(str(candidate))==IFSelect_RetDone and reader.Transfer(doc)
 seq=TDF_LabelSequence();XCAFDoc_DocumentTool.ColorTool_s(doc.Main()).GetColors(seq)
 assert seq.Length()>0
 continuity=[]
 named={n:s for n,s,c,b,g in m.parts}
 for wire in m.wire_paths:
  shape=named[wire['part']]
  samples=[wire['edge'].positionAt(i/50) for i in range(51)]
  contained=all(shape.isInside(pt,1e-5) for pt in samples)
  assert contained and len(shape.Solids())==1,wire['part']
  continuity.append({'part':wire['part'],'curve':m.curve_kind,'valid_single_solid':True,'centerline_samples_checked':51,'all_centerline_samples_inside_solid':True})
 candidate.replace(path)
 metadata={'name':m.name,'file':path.name,'generated_on':'2026-10-13','unit':'mm',
  'vendor_native_cad':False,'hardware_measured':False,'parts':len(m.parts),'solids':len(back.Solids()),
  'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size,
  'generator':'../../../tools/build_motor_esc_step.py','generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
  'renderer_source':'../../../tools/build_camera_step.py','renderer_source_sha256':hashlib.sha256((ROOT/'tools/build_camera_step.py').read_bytes()).hexdigest(),
  'confirmed_dimensions':confirmed,'estimates':estimates,
  'bounds_including_cables_mm':{k:getattr(bb,k) for k in ['xmin','xmax','ymin','ymax','zmin','zmax']},
  'validation':{'reimport_valid':True,'solid_count_preserved':True,'volume_relative_error':error,'bbox_error_mm':bb_error,'xcaf_colours_reimported':seq.Length()},
  'cable_continuity_validation':continuity,
  'limitations':['External appearance only; hidden motor electromagnetic and ESC electronics internals not reconstructed',
   'No native manufacturer CAD and no physical measurement; unpublished dimensions estimated',
   'Cable diameter, length where undocumented, pose, connector and switch geometry estimated',
   'STEP solid colours and shallow geometric print only; approximate fonts and no textures',
   'Mounting holes nominal cylinders, no hidden screw thread helices'],
  'reference_assets':[{'file':'../'+p.relative_to(OUT.parent).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for folder in ['photos','notices'] for p in sorted((OUT.parent/folder).glob('*')) if p.suffix in ['.jpg','.pdf']],
  'part_manifest':[{'name':n,'rgb':c,'basis':b,'group':g,'solids':len(s.Solids())} for n,s,c,b,g in m.parts]}
 (OUT/(slug+'-provenance.json')).write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({k:metadata[k] for k in ['file','parts','solids','validation']}),flush=True)
 return metadata

# Reuse the already validated camera rasterizer, without running its generator.
# AST extraction restricts reuse to this one function; no camera files are rebuilt.
camera_tree=ast.parse((ROOT/'tools/build_camera_step.py').read_text(encoding='utf-8'))
render_node=next(n for n in camera_tree.body if isinstance(n,ast.FunctionDef) and n.name=='render')
# Some periodic swept faces have inconsistent triangle winding in OCCT meshes.
# Render both sides and let the depth buffer decide visibility.
for node in ast.walk(render_node):
 if isinstance(node,ast.If) and ast.unparse(node.test)=='norm and np.dot(normal, view) < -1e-10':node.test=ast.Constant(False)
ast.fix_missing_locations(render_node)
exec(compile(ast.Module(body=[render_node],type_ignores=[]),str(ROOT/'tools/build_camera_step.py'),'exec'))

def preview(m,filename,view,title,groups=None,exclude_prefixes=()):
 global MESH_CACHE
 MESH_CACHE=[]
 for n,s,c,b,g in m.parts:
  if groups and g not in groups:continue
  if n.startswith(exclude_prefixes):continue
  vertices,triangles=s.tessellate(.07,.17)
  MESH_CACHE.append((np.array([v.toTuple() for v in vertices]),triangles,np.array(c)))
 render(OUT/filename,view,title)
 print('RENDER '+filename,flush=True)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--model',choices=['motor','esc','both'],default='both');parser.add_argument('--no-render',action='store_true');args=parser.parse_args()
 if args.model in ['motor','both']:
  m=motor();export(m,'moteur-quicrun-2435-g3-4500kv-detaille',
    {'body_diameter_mm':24,'body_length_mm':36,'shaft_diameter_mm':2,'shaft_projection_mm':12,'shaft_flat_dimension_mm':1.7,'shaft_flat_length_mm':9,'mounting_threads':['M2.5','M3'],'mounting_hole_depth_mm':4,'pitch_circle_diameters_mm':[14,16,17],'bullet_diameter_mm':3.5},
    {'body_wall_mm':1,'front_cap_thickness_mm':4.3,'rear_cap_thickness_mm':2,'cooling_grooves_count':17,'cooling_groove_radius_mm':.32,'motor_wire_insulation_diameter_mm':3,'motor_wire_pose_and_length':'Illustrative, not published','mounting_pattern_angles':'Interpreted from manufacturer drawing; check before machining'})
  if not args.no_render:
   preview(m,'moteur-vue-isometrique.png',(.7,-1.1,.75),'QuicRun 2435 G3 4500KV | Corps detaille',{'body'})
   preview(m,'moteur-vue-fixations.png',(.10,-.25,-1.0),'QuicRun 2435 G3 | Axe et fixations',{'body'})
   preview(m,'moteur-vue-complete.png',(.6,-.8,.8),'QuicRun 2435 G3 | Moteur et connecteurs')
 if args.model in ['esc','both']:
  m=esc();export(m,'variateur-quicrun-wp16bl30-g2-detaille',
    {'case_xyz_mm':[33.4,26.8,15.1],'nominal_input_wire_length_mm':75,'nominal_output_wire_length_mm':60,'wire_gauge':'16AWG','phase_contact_diameter_mm':3.5,'input_connector':'XT60'},
    {'case_height_without_heatsink_mm':12.4,'case_wall_mm':1.5,'heatsink_base_xy_mm':[21.2,23.4],'capacitor_diameter_mm':7.3,'capacitor_height_mm':3.35,'switch_base_xyz_mm':[17,11.2,4],'power_insulation_diameter_mm':3.2,'receiver_connector_dimensions':'Generic JR photo estimate','cable_pose':'Illustrative; nominal published lengths not installed geometry'})
  if not args.no_render:
   preview(m,'variateur-vue-isometrique.png',(.8,-1,1.1),'WP16BL30 G2 | Boitier et dissipateur',{'body'})
   preview(m,'variateur-vue-dessus.png',(0,0,1),'WP16BL30 G2 | Vue de dessus',{'body'})
   preview(m,'variateur-vue-complete.png',(.3,-.6,1.3),'WP16BL30 G2 | Cables, XT60 et interrupteur')
   preview(m,'variateur-vue-interrupteur.png',(.4,-.8,1.0),'WP16BL30 G2 | Interrupteur',{'switch'},('Switch_wire',))
