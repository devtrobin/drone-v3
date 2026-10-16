"""Photo-informed U20CAM-4M visual reconstruction, millimetres, not fabrication CAD.

Run with tools/temp/cad-env/Scripts/python.exe. All uncertain geometry is documented.
STEP exports actual coloured B-rep geometry, not photographic textures.
"""
from pathlib import Path
import json, math, hashlib
import cadquery as cq
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'Composants/camera/3D'
OUT.mkdir(parents=True, exist_ok=True)
PARTS = []
COLORS = {
 'pcb':(.13,.14,.15),'edge':(.46,.37,.23),'trace':(.20,.21,.22),
 'gold':(.78,.60,.29),'metal':(.70,.72,.73),'solder':(.57,.60,.63),
 'plastic':(.125,.13,.135),'chip':(.18,.19,.20),'ceramic':(.60,.52,.39),
 'recess':(.028,.031,.034),
 'white':(.88,.88,.82),'glass':(.075,.18,.34),'purple':(.19,.14,.33),
}

def add(name, shape, color='plastic', basis='estimated_from_photos'):
    if not shape.isValid() or shape.Volume() <= 0:
        raise ValueError('Invalid solid: '+name)
    rgb = COLORS[color] if isinstance(color,str) else color
    PARTS.append((name,shape,rgb,basis))
    return shape

def box(l,w,h,x,y,z,rad=0):
    s=cq.Workplane('XY').box(l,w,h,centered=False)
    if rad: s=s.edges('|Z').fillet(rad)
    return s.val().translate((x,y,z))

def cylinder(r,h,x,y,z,axis=(0,0,1)):
    return cq.Solid.makeCylinder(r,h,cq.Vector(x,y,z),cq.Vector(*axis))

def annulus(ro,ri,h,x,y,z):
    return cylinder(ro,h,x,y,z).cut(cylinder(ri,h+.02,x,y,z-.01))

def rect_outline(name,x,y,l,w,z,color='white',thick=.10):
    s=box(l,w,.012,x,y,z).cut(box(l-2*thick,w-2*thick,.04,x+thick,y+thick,z-.01))
    add(name,s,color,'visible_silkscreen_estimated')

def text(name,value,x,y,z,size=.8,rotation=0,color='white',back=False):
    s=cq.Workplane('XY').text(value,size,.012,font='Arial',halign='left',valign='bottom',combine=False).val()
    if back: s=s.rotate((0,0,0),(0,1,0),180)
    s=s.rotate((0,0,0),(0,0,1),rotation).translate((x,y,z))
    add(name,s,color,'visible_marking_estimated')

# Datum: PCB bottom z=0, front surface z=1.2; front viewed from +z.
T=1.2
board=box(32,32,T,0,0,0,1.4)
holes=[(2,2),(30,2),(2,30),(30,30)]
mounts=[(7,16),(25,16)]
for x,y in holes: board=board.cut(cylinder(1.1,T+2,x,y,-1))
for x,y in mounts: board=board.cut(cylinder(.90,T+2,x,y,-1))

# Via locations traced from the front photo, normalised to the published 32 mm PCB.
vias=[(4.6,31),(6.3,30),(7.5,30.7),(9.7,30.5),(11.2,31.1),(13.8,30),(16.4,29.8),
 (20.2,29.6),(21.5,29.5),(27.6,31),(4,29),(5.8,28.1),(6.5,27.5),(8.5,27.2),
 (1,27.8),(3,27),(4.6,27),(3.2,25.8),(4,25),(3.1,24.4),(5,24.2),(3,23.2),
 (3.1,22.4),(3.8,22),(4.6,22),(5.1,22.5),(7.3,23),(1.8,19.5),(5.2,19.3),
 (5.8,18.8),(6.7,18),(7.2,17.2),(2,13),(3.3,11.4),(5,9),(5,7.6),
 (6.7,5),(1.3,3.6),(8.4,3),(9.2,4.7),(11,3.8),(12.5,4),(14.6,4.5),
 (18.2,4.1),(16.3,3),(17.4,2.5),(19.5,2),(20.7,1.8),(22.6,2.2),(23.7,3.1),
 (27.5,4),(31,5),(30.5,7.5),(28.5,9.2),(27,9.1),(25.8,9.1),(24.1,9.7),
 (25.7,12.2),(30.6,14.8),(29.6,17),(28.2,18.3),(30,22.3),(28.1,24.9),
 (25.1,25.1),(22.3,25.4),(21.6,26),(23,24.5),(23,23.6),(21.4,23.2),
 (19.9,23),(18.4,23.2),(17.8,23.9),(16.3,25.5),(14.1,26.5),(13.4,26.5),
 (12.7,26.5),(13.5,28.1),(14.6,28.1),(16.5,28.6),(9.4,28.6),(6.4,29),
 (8.1,22.9),(5.9,19.8),(8,19.8),(7.6,15.6),(3.8,12.1),(6,12),
 (8.9,3.8),(12,3.1),(17.4,1.4),(10.5,1.1),(8.2,1.1),(6.3,1.1)]
for x in [12.5,13.4,14.3,15.2]:
 for y in [23.0,23.9,24.8,25.7]: vias.append((x,y))
for x,y in vias: board=board.cut(cylinder(.09,T+.2,x,y,-.1))
add('PCB_FR4_32x32',board,'edge','published_xy_estimated_thickness_holes_positions')
masktop=box(32,32,.018,0,0,T,1.4)
maskback=box(32,32,.018,0,0,-.018,1.4)
for x,y in holes+mounts:
 for side in ['front','back']:
  if side=='front': masktop=masktop.cut(cylinder(1.9 if (x,y) in holes else 2.0,.08,x,y,T-.02))
  else: maskback=maskback.cut(cylinder(1.9 if (x,y) in holes else 2.0,.08,x,y,-.04))
for x,y in vias:
 masktop=masktop.cut(cylinder(.16,.08,x,y,T-.02))
 maskback=maskback.cut(cylinder(.16,.08,x,y,-.04))
add('Front_black_solder_mask',masktop,'pcb')
add('Rear_black_solder_mask',maskback,'pcb')
for i,(x,y) in enumerate(holes):
 for side,z in [('front',T+.002),('rear',-.018)]:
  add(f'Mounting_pad_{side}_{i}',annulus(1.9,1.1,.018,x,y,z),'gold')
 add(f'Mounting_hole_barrel_{i}',annulus(1.13,1.1,T,x,y,0),'metal')
for i,(x,y) in enumerate(vias):
 for side,z in [('front',T+.001),('rear',-.016)]:
  add(f'Via_annulus_{side}_{i:03}',annulus(.17,.09,.012,x,y,z),'trace')
 add(f'Via_barrel_{i:03}',annulus(.10,.09,T,x,y,0),'solder')

# Visible masked tracks: manually reconstructed paths, NOT a circuit/netlist.
def trace(name,points,z,width=.12):
    segs=[]
    for (x,y),(xx,yy) in zip(points,points[1:]):
        d=math.hypot(xx-x,yy-y)
        if d<.001:continue
        s=box(d,width,.012,0,-width/2,z).rotate((0,0,0),(0,0,1),math.degrees(math.atan2(yy-y,xx-x))).translate((x,y,0))
        segs.append(s)
    for x,y in points:segs.append(cylinder(width/2,.012,x,y,z))
    add(name,cq.Compound.makeCompound(segs),'trace','visible_path_approximation_no_electrical_connectivity')

frontpaths=[[(6.4,29),(7.5,29),(9,27.5),(9,5),(8.9,3.8)],
 [(9.4,28.6),(10.3,28.6),(12,30),(14.2,30),(14.6,28.1)],
 [(8.5,27.2),(7.4,27.9),(6.5,27.9)],
 [(13.4,26.5),(14.1,27.5),(15.7,27.5),(18.7,27.5),(20.2,28.4)],
 [(7.6,15.6),(8.6,15.6),(9.6,14.6),(9.6,7),(10.5,6.1),(10.5,3.1)],
 [(3.8,12.1),(5.4,12.1),(6,12)],
 [(6,12),(7.8,12),(8.7,10.8),(8.7,4.5)],
 [(12,3.1),(11.7,5.4),(12.8,6.6),(17.8,6.6),(18.8,7.5),(18.8,13)],
 [(16.3,25.5),(16.3,20.2),(17.7,19)],
 [(21.6,26),(21.6,22),(22.3,21.3)],
 [(21.4,23.2),(21.4,20.5),(20.7,19.8)]]
for i,path in enumerate(frontpaths):
 for j in range(3 if i in [0,1,3,7,8,9] else 1):
  trace(f'Front_masked_trace_{i}_{j}',[(x+.22*j,y) for x,y in path],T+.020,.10)

# Gold via array visible above the lens.
testpad=box(3.4,4.1,.022,12.1,22.1,T+.019)
for x in [12.5,13.4,14.3,15.2]:
 for y in [23.0,23.9,24.8,25.7]:testpad=testpad.cut(cylinder(.10,.1,x,y,T-.01))
add('Front_gold_test_land',testpad,'gold')
for i in range(5):
 x=20.7+i*1.16
 add(f'USB_through_pad_front_{i}',box(.74,1.3,.023,x-.37,28.2,T+.02,.25 if i else 0),'gold')
 add(f'USB_solder_front_{i}',cq.Solid.makeSphere(.36,cq.Vector(x,28.8,T+.05)).intersect(box(.9,1.2,.38,x-.45,28.2,T+.02)),'solder')

# Lens frame: square platform with rounded side ears and true screw slots.
frame=box(13.2,13.2,2.0,9.4,9.4,T+.03,.35)
for x in [7,25]:
 ear=box(3.0,3.6,1.25,min(x,9.4) if x<16 else 22.4,14.2,T+.65)
 frame=frame.fuse(ear).fuse(cylinder(1.8,1.25,x,16,T+.65))
 frame=frame.cut(cylinder(.9,3,x,16,T))
frame=frame.cut(cylinder(4.25,3,16,16,T))
add('Lens_holder_square_and_mounting_ears',frame,'plastic')
rect_outline('Lens_holder_silkscreen',8.8,8.8,14.4,14.4,T+.041)
for x in [7,25]:
 add(f'Lens_mount_boss_{x}',annulus(1.8,.9,.63,x,16,T+.03),'plastic')
 add(f'Lens_fixing_screw_shank_{x}',cylinder(.75,2.8,x,16,-.35),'metal')
 head=cylinder(.95,.55,x,16,T+1.93)
 slot=box(2.2,.20,.35,x-1.1,15.9,T+2.25).rotate((x,16,0),(x,16,1),32)
 add(f'Lens_fixing_slotted_head_{x}',head.cut(slot),'metal')
 add(f'Lens_screw_slot_dark_floor_{x}',box(1.7,.17,.008,x-.85,15.915,T+2.251).rotate((x,16,0),(x,16,1),32),'recess','visual_recess_contrast')
 back=cylinder(1.35,.8,x,16,-.8)
 back=back.cut(box(1.8,.28,.35,x-.9,15.86,-.82))
 back=back.cut(box(.28,1.8,.35,x-.14,15.1,-.82))
 add(f'Rear_mount_screw_head_{x}',back,'plastic')
 add(f'Rear_mount_washer_{x}',annulus(2.05,1.25,.075,x,16,-.07),'gold')

add('M8_5_lens_shank',annulus(4.25,2.1,2.7,16,16,T+1.65),'plastic','published_nominal_thread_diameter_estimated_height')
add('Lens_lower_collar',annulus(4.8,2.1,.65,16,16,T+3.8),'plastic')
barrel=annulus(5.0,2.1,2.1,16,16,T+4.3)
for i in range(48):
 a=2*math.pi*i/48
 barrel=barrel.cut(cylinder(.22,2.2,16+5.02*math.cos(a),16+5.02*math.sin(a),T+4.25))
add('Lens_focus_knurled_barrel_48_grooves',barrel,'plastic')
for z in [T+4.16,T+6.12]:add(f'Lens_collar_rim_{z}',annulus(5.04,4.80,.13,16,16,z),'chip')
cap=annulus(4.95,1.72,.63,16,16,T+6.4)
for i in range(8):
 a=2*math.pi*i/8
 cap=cap.cut(cylinder(1.15,.8,16+5.55*math.cos(a),16+5.55*math.sin(a),T+6.32))
add('Lens_front_scalloped_bezel',cap,'plastic')
add('Lens_glass_retaining_ring',annulus(1.87,1.62,.22,16,16,T+6.46),'chip')
# Optical appearance only; surface curvature inferred, not an optical design.
glass=cq.Solid.makeSphere(8.0,cq.Vector(16,16,T-1.1)).intersect(cylinder(1.62,.5,16,16,T+6.5))
add('Front_optical_glass_convex',glass,'glass','visual_optical_surface_not_optical_prescription')
add('Anti_reflection_coating_ring',annulus(1.63,1.53,.02,16,16,T+6.72),'purple')
text('Front_model_marking','U20-4MP',1.15,15.9,T+.05,1.30,90,'gold')
text('Front_revision_marking','A',28.0,.8,T+.05,1.3,0,'white')

# Back: source photo pixel-to-mm approximation; x mirrored into front datum.
def rearxy(px,py):return 32-(px-140)*32/810,(950-py)*32/780
def passive(n,px,py,l=1.05,w=.52,angle=0,kind='C'):
 x,y=rearxy(px,py)
 body=box(l*.64,w,.42,-l*.32,-w/2,-.46).rotate((0,0,0),(0,0,1),angle).translate((x,y,0))
 add(f'Rear_{kind}_{n}_body',body,'ceramic' if kind=='C' else 'chip')
 for k,dx in enumerate([-l*.43,l*.25]):
  terminal=box(l*.18,w,.40,dx,-w/2,-.45).rotate((0,0,0),(0,0,1),angle).translate((x,y,0))
  pad=box(l*.31,w+.23,.07,dx-l*.08,-(w+.23)/2,-.072).rotate((0,0,0),(0,0,1),angle).translate((x,y,0))
  add(f'Rear_{kind}_{n}_terminal_{k}',terminal,'metal')
  add(f'Rear_{kind}_{n}_solder_{k}',pad,'solder')
 return x,y

capcoords=[(231,320,90),(180,341,0),(181,362,0),(291,347,0),(391,344,0),
 (498,320,0),(500,350,0),(500,383,0),(500,409,0),(198,520,0),(218,555,0),
 (230,802,0),(384,636,0),(382,662,0),(440,820,90),(607,824,90),(561,825,90),
 (506,908,0),(670,901,0),(736,862,90),(781,803,0),(881,804,0),
 (722,778,90),(696,623,0),(696,569,0),(678,500,0),(705,470,90),(754,421,90),
 (777,424,90),(796,424,90),(750,462,0),(766,377,0),(765,340,0),(761,314,0),
 (757,274,0),(785,286,0),(789,309,0),(805,255,90),(784,219,90),
 (758,219,90),(732,219,90),(704,219,90),(681,219,90),(592,219,90),(561,219,90)]
for i,(x,y,a) in enumerate(capcoords):passive(i,x,y,1.0,.48,a,'C' if i%3 else 'R')
passive('large_1',348,407,2.8,1.55,0)
passive('large_2',235,723,2.15,1.50,90)
passive('pair_1',588,679,1.25,.65,90)
passive('pair_2',615,679,1.25,.65,90)
passive('resistor_14',550,447,1.0,.5,0,'R')
passive('right_edge',895,619,1.20,.6,0,'R')

def sot(name,px,py,l=2,w=1.25,leads=3,label=None):
 x,y=rearxy(px,py)
 add(name+'_moulding',box(l,w,.8,x-l/2,y-w/2,-.86,.12),'chip')
 for i in range(leads):
  dx=(i-(leads-1)/2)*.65
  for side in [-1,1]:
   add(name+f'_lead_{i}_{side}',box(.30,.63,.18,x+dx-.15,y+side*w/2-.3,-.19),'metal')
 if label:text(name+'_marking',label,x+.7,y-.2,-.873,.45,0,'white',True)
 return x,y
sot('Rear_regulator_YJ18',503,832,label='YJ18')
sot('Rear_regulator_YJ28',673,828,label='YJ28')
sot('Rear_SOT23_6_upper',243,405,l=1.75,w=1.15)
sot('Rear_SOT23_6_left',210,620,l=2.5,w=1.6)
sot('Rear_SOT23_top',646,225,l=1.2,w=1.1,leads=2)

x,y=rearxy(622,352)
add('Rear_USB_image_processor_QFN',box(6.0,6.0,.9,x-3,y-3,-.94,.18),'chip')
add('Rear_processor_top_unreadable_marking_area',box(4.1,3.1,.012,x-2.05,y-1.55,-.955),'plastic')
for side in range(4):
 for i in range(12):
  s=box(.23,.65,.12,-2.75+i*.5,2.72,-.14).rotate((0,0,0),(0,0,1),side*90).translate((x,y,0))
  add(f'QFN48_visible_contact_{side}_{i}',s,'solder')
add('QFN_pin1_dot',cylinder(.16,.014,x-2.35,y-2.35,-.958),'trace')
x,y=rearxy(842,317)
add('Rear_quartz_metal_can',box(2.4,3.0,.85,x-1.2,y-1.5,-.89,.25),'metal')
add('Rear_quartz_ceramic_base',box(2.6,3.2,.12,x-1.3,y-1.6,-.13,.2),'chip')
for dx in [-.95,.95]:
 for dy in [-1.2,1.2]:add(f'Quartz_pad_{dx}_{dy}',box(.65,.7,.08,x+dx-.325,y+dy-.35,-.075),'solder')
x,y=rearxy(844,713)
add('Rear_SOIC8_flash_memory',box(4.0,5.0,1.40,x-2,y-2.5,-1.52,.2),'chip')
for side in [-1,1]:
 for i in range(4):
  lead=box(.70,.42,.17,x+side*2-.35,y-1.91+i*1.27-.21,-.21)
  lead=lead.fuse(box(.5,.42,.9,x+side*2-.25,y-1.91+i*1.27-.21,-1.02))
  add(f'SOIC8_gullwing_{side}_{i}',lead,'metal')
add('SOIC8_pin1_dot',cylinder(.23,.015,x-1.3,y-1.8,-1.54),'trace')

# Connector viewed on rear upper left; shell and individual contacts kept separate.
cx,cy=rearxy(373,217)
housing=box(8.8,4.2,4.4,cx-4.4,cy-2.1,-4.45,.12)
housing=housing.cut(box(7.4,3.2,3.0,cx-3.7,cy-1.6,-4.50))
add('Rear_USB_5pin_shrouded_connector',housing,'white','photo_inferred_unidentified_connector')
add('USB_connector_inner_contact_carrier',box(7.1,2.8,.025,cx-3.55,cy-1.4,-1.51),'recess','visual_recess_contrast')
for i in range(5):
 xx=20.7+i*1.16
 add(f'USB_connector_contact_{i}',box(.35,.35,3.7,xx-.175,28.8-.175,-4.0),'metal')
 add(f'USB_connector_front_pin_tail_{i}',cylinder(.16,.22,xx,28.8,T),'metal')
for side in [-1,1]:add(f'USB_connector_latch_{side}',box(.30,1.2,1.0,cx+side*4.2-.15,cy-.6,-3.7),'white')

# Rear masked fanout traced from photograph; no inferred hidden copper layers.
for i in range(10):
 trace(f'Rear_processor_fanout_bottom_{i}',[(11+i*.28,21.2),(11+i*.28,19.9),(13+i*.30,17.8),(17+i*.23,17.8)],-.036,.10)
for i in range(7):
 trace(f'Rear_processor_fanout_right_{i}',[(9.5,24.2+i*.3),(8.8,24.2+i*.3),(5+i*.25,20.3),(5+i*.25,12.3)],-.036,.10)
rearpaths=[[(cx,cy-2.2),(cx,27),(18,27),(16,25)],
 [(28,22),(30,20),(30,17.5),(27,15.2),(27,8),(26,7),(26,3),(23,2)],
 [(29,12),(30,11),(30,9),(28,6.5),(28,4),(27,3),(25,3)],
 [(23,5),(25,6),(25,13),(19,18)],
 [(12,5),(12,16),(10,19)],[(8,5),(8,17),(9,18.5)],
 [(17,5),(19,6),(22,6),(23,7),(23,13),(18,17)],
 [(17,9),(20,9),(21,10),(21,14),(20,15)]]
for i,p in enumerate(rearpaths):
 for j in range(2):trace(f'Rear_masked_trace_{i}_{j}',[(x+.23*j,y) for x,y in p],-.036,.11)
for i,(x,y) in enumerate([(24,24),(28,18),(27,11),(18,20),(8,22),(11,3)]):
 rect_outline(f'Rear_SMD_outline_{i}',x-.8,y-.5,1.6,1,-.041,'white',.06)
for label,px,py in [('C4',456,416),('C10',448,385),('R14',563,467),('R0',401,642),('C15',703,594)]:
 x,y=rearxy(px,py);text('Rear_reference_'+label,label,x+.7,y,-.055,.65,0,'white',True)
text('Rear_board_revision','U20-4MP',4,31.2,-.055,.85,0,'white',True)

assembly=cq.Assembly(name='InnoMaker_U20CAM_4M_photo_reconstruction')
for name,shape,color,basis in PARTS:assembly.add(shape,name=name,color=cq.Color(*color))
step=OUT/'camera-u20cam-4m-detaillee.step'
assembly.export(str(step),exportType='STEP',mode='default',unit='MM',outputUnit='MM')
original=cq.Compound.makeCompound([s for _,s,_,_ in PARTS])
imported=cq.importers.importStep(str(step)).val()
assert imported.isValid() and all(s.isValid() for s in imported.Solids())
assert len(original.Solids())==len(imported.Solids())
v_error=abs(imported.Volume()-original.Volume())/original.Volume()
assert v_error<1e-6
b0,b1=original.BoundingBox(),imported.BoundingBox()
bb_error=max(abs(getattr(b0,k)-getattr(b1,k)) for k in ['xmin','ymin','zmin','xmax','ymax','zmax'])
assert bb_error<1e-5
steptext=step.read_text()
assert 'COLOUR_RGB' in steptext and 'STYLED_ITEM' in steptext
print('STEP exported and reimported:',len(PARTS),'parts,',len(imported.Solids()),'solids',flush=True)

MESH_CACHE=[]
for _,shape,col,_ in PARTS:
 vertices,triangles=shape.tessellate(.06,.14)
 MESH_CACHE.append((np.array([v.toTuple() for v in vertices]),triangles,np.array(col)))

# Orthographic software rasterizer, actual B-rep tessellation with a depth buffer.
def render(path,view,title):
 W,H=1600,1300
 view=np.array(view,dtype=float);view/=np.linalg.norm(view)
 right=np.cross([0,1,0] if abs(view[2])>.99 else [0,0,1],view);right/=np.linalg.norm(right)
 up=np.cross(view,right)
 basis=np.array([right,-up,view]).T
 meshes=[];ps=[]
 for world,triangles,col in MESH_CACHE:
  proj=world@basis
  meshes.append((world,proj,triangles,col));ps.append(proj)
 pts=np.vstack(ps);lo,hi=pts[:,:2].min(axis=0),pts[:,:2].max(axis=0)
 scale=min((W-140)/(hi[0]-lo[0]),(H-200)/(hi[1]-lo[1]));mid=(lo+hi)/2
 rgb=np.full((H,W,3),241,dtype=np.uint8);depth=np.full((H,W),-np.inf)
 light=view+np.array([-.35,.15,.35]);light/=np.linalg.norm(light)
 for world,proj,tris,col in meshes:
  screen=proj.copy();screen[:,:2]=(screen[:,:2]-mid)*scale+[W/2,H/2+10]
  for t in tris:
   normal=np.cross(world[t[1]]-world[t[0]],world[t[2]]-world[t[0]])
   norm=np.linalg.norm(normal)
   if norm and np.dot(normal,view)<-1e-10:continue
   a,b,c=screen[list(t)];den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
   if abs(den)<1e-8:continue
   x0=max(0,int(np.floor(min(a[0],b[0],c[0]))));x1=min(W-1,int(np.ceil(max(a[0],b[0],c[0]))))
   y0=max(70,int(np.floor(min(a[1],b[1],c[1]))));y1=min(H-60,int(np.ceil(max(a[1],b[1],c[1]))))
   if x1<x0 or y1<y0:continue
   xx,yy=np.meshgrid(np.arange(x0,x1+1)+.5,np.arange(y0,y1+1)+.5)
   u=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/den
   v=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den;w=1-u-v
   zz=u*a[2]+v*b[2]+w*c[2];old=depth[y0:y1+1,x0:x1+1]
   mask=(u>=-1e-7)&(v>=-1e-7)&(w>=-1e-7)&(zz>old)
   shade=.68+.32*abs(np.dot(normal/norm,light)) if norm else 1
   rgb[y0:y1+1,x0:x1+1][mask]=np.clip(col*shade*255,0,255).astype(np.uint8);old[mask]=zz[mask]
 im=Image.fromarray(rgb);d=ImageDraw.Draw(im)
 fontpath='C:/Windows/Fonts/arial.ttf'
 d.text((W/2,20),title,font=ImageFont.truetype(fontpath,32),anchor='mt',fill='#182128')
 d.text((W/2,H-30),'Reconstruction visuelle - mm - geometrie estimee hors cotes publiees',font=ImageFont.truetype(fontpath,21),anchor='mm',fill='#52616b')
 im.save(path)

for filename,view,title in [
 ('vue-avant.png',(0,0,1),'U20CAM-4M | Face avant'),
 ('vue-arriere.png',(0,0,-1),'U20CAM-4M | Face arriere'),
 ('vue-isometrique.png',(.65,-.9,1.2),'U20CAM-4M | STEP detaille et colore'),
 ('vue-arriere-isometrique.png',(-.6,.6,-1.1),'U20CAM-4M | Composants et connecteur USB'),
 ('vue-profil.png',(0,-1,.08),'U20CAM-4M | Profil')]:
 render(OUT/filename,view,title)
 print('RENDER',filename,flush=True)

metadata={
 'model':'InnoMaker U20CAM-4M','generated_on':'2026-10-12','unit':'mm',
 'format':'STEP coloured assembly B-rep','hardware_measured':False,'vendor_native_cad':False,
 'file':step.name,'sha256':hashlib.sha256(step.read_bytes()).hexdigest(),
 'generator':'../../../tools/build_camera_step.py','generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'parts':len(PARTS),'solids':len(imported.Solids()),'colour_records':steptext.count('COLOUR_RGB'),
 'bounds_mm':{k:getattr(b1,k) for k in ['xmin','xmax','ymin','ymax','zmin','zmax']},
 'validation':{'reimport_valid':True,'volume_relative_error':v_error,'bbox_error_mm':bb_error,'colours_present':True},
 'confirmed_dimensions':{'pcb_xy_mm':[32,32],'mounting_holes_diameter_mm':2.2,'lens_mount_nominal_spacing_mm':18,'lens_thread_nominal':'M8.5 x 0.25'},
 'estimates':{'pcb_thickness_mm':1.2,'mount_hole_centres_mm':holes,'lens_mount_centres_mm':mounts,'lens_front_z_mm':8.23,'connector_rear_z_mm':-4.45,'lens_frame_xy_mm':[13.2,13.2],'lens_cap_diameter_mm':9.9,'lens_glass_diameter_mm':3.24},
 'limitations':['No internal copper reconstructed','Visible traces approximated from photos, not an electrical netlist','No optical prescription or internal glass stack available','Small package types/counts and unreadable chip markings not identified electrically','No photorealistic textures in STEP; solid colours and geometric details only','Cable excluded from module STEP; 1m cable shape not a product dimension','PCB thickness, height, pitch of connector and hole positions require physical measurements'],
 'reference_photos':[{'file':'../photos/'+p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted((OUT.parent/'photos').glob('*.jpg'))],
 'part_manifest':[{'name':n,'rgb':c,'basis':basis,'solids':len(s.Solids())} for n,s,c,basis in PARTS]
}
(OUT/'provenance.json').write_text(json.dumps(metadata,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({k:metadata[k] for k in ['file','parts','solids','colour_records','validation']},indent=2),flush=True)
