"""Black nylon kit: 14 individual nominal pieces + four-point study assembly.

Real external/internal helical geometry. Fine dimensions and thread clearance
are estimates, not Ewwtrey factory CAD or manufacturing/gauge data. No chassis
or Raspberry Pi geometry is authored or modified by this script.
"""
from pathlib import Path
import json, math, sys, itertools
import cadquery as cq
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from build_running_gear_step import cyl, box, hexagon, export_model

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'Composants/fixations-raspberry-pi-5';OUT=BASE/'3D'
BLACK=(.018,.020,.023);P=.45;D=2.5;AF=5.0
HOLES=[(3.5,3.5),(61.5,3.5),(61.5,52.5),(3.5,52.5)]
LIMITS=[
 'Longueurs et quantités : fiche et illustration Amazon de la variante noire M2.5.',
 'Surplats 5 mm, tête 4.7 x 2 mm, écrou 2 mm, rondelle 5 x 2.7 x 0.5 mm : estimations, à mesurer.',
 'Filetage M2.5 x 0.45 : pas métrique usuel d’étude ; pas et classe du lot non mesurés.',
 'Profils hélicoïdaux proches de 60 degrés, fonds et crêtes simplifiés ; jeu radial CAO 0.03 mm estimé.',
 'MF et FF hexagonales confirmées par les images haute définition ; surplats exact non publié.',
 'Taraudage MF borgne, profondeur min(6.5, L-2) mm ; FF traversant : hypothèses non publiées.',
 'Pas de matière interne, marquage ni tolérance inventés ; aucune CAO fabricant propre au kit trouvée.',
 'Châssis conçu en dernier selon décision utilisateur du 14 octobre 2026 ; hauteurs définitives ouvertes.'
]

def optimal(self,tolerance=None):
 b=Bnd_Box();BRepBndLib.AddOptimal_s(self.wrapped,b,False,False);return cq.BoundBox(b)

def thread(d,length,pitch=P):
 # Symmetric nominal 60-degree flanks with truncated crest. Root radius and
 # thread run-out are reconstructed, and intentionally not gauge-accurate.
 major=d/2;depth=.61343*pitch;root=major-depth;r=(root+major)/2
 # Fuse the continuous core and the untrimmed helix before cutting the ends.
 # Cutting the ridge first creates coincident cap faces that OCC may discard
 # during union even while reporting a valid solid.
 core=cyl(root+.012,length+4*pitch,-2*pitch)
 helix=cq.Wire.makeHelix(pitch,length+2*pitch,r)
 ridge=(cq.Workplane('XZ').polyline([(root-.025,-.416667*pitch),
  (major,-pitch/16),(major,pitch/16),(root-.025,.416667*pitch)])
  .close().sweep(cq.Workplane('XY').newObject([helix]),isFrenet=True).val().translate((0,0,-pitch)))
 s=core.fuse(ridge,tol=1e-6).intersect(cyl(major+.01,length),tol=1e-6).clean()
 assert s.isValid() and len(s.Solids())==1
 for z in [length/4,length/2,3*length/4]:assert s.isInside(cq.Vector(0,0,z),1e-6),('thread core',length,z)
 for k in range(2,int(length/pitch)-1,3):
  assert s.isInside(cq.Vector(major-.10,0,k*pitch),1e-6),('thread crest',length,k)
  assert not s.isInside(cq.Vector(major-.10,0,(k+.5)*pitch),1e-6),('thread valley',length,k)
 return s

def female_tool(length):
 # Same helix phase as the external thread, 0.03 mm radial reconstruction
 # clearance. A straight drilled bottom avoids a fictional drill tip angle.
 return thread(D+.06,length)

def normalize_ff(s,name):
 # STEP converts certain helically trimmed surfaces to spline form. Prepare
 # that representation once for long internal threads, retaining an explicit
 # record of its sub-0.1% volume change; final round-trip remains checked at
 # <0.01% in export_model. This is a reconstruction, not a gauge model.
 tmp=ROOT/'tools/temp/pi-mount-review/normalization';tmp.mkdir(parents=True,exist_ok=True)
 a=cq.Assembly(name='Spline_preparation');a.add(s,name='piece',color=cq.Color(*BLACK))
 path=tmp/(name+'.step');a.export(str(path),exportType='STEP',unit='MM',outputUnit='MM')
 new=cq.importers.importStep(str(path)).val();before=s.Volume(tol=1e-9);after=new.Volume(tol=1e-9)
 drift=abs(after-before)/before
 a0=s.BoundingBox();b0=new.BoundingBox();err=max(abs(getattr(a0,k)-getattr(b0,k)) for k in ['xmin','xmax','ymin','ymax','zmin','zmax'])
 assert new.isValid() and len(new.Solids())==1 and drift<1e-3 and err<.01,(name,drift,err)
 return new,dict(method='Initial STEP spline preparation, explicit reconstruction conversion',volume_before_mm3=before,
  volume_after_mm3=after,volume_relative_change=drift,volume_relative_change_limit=1e-3,bbox_change_mm=err,valid=True)

def chamfer_envelope_hex(length):
 s=hexagon(AF,length)
 # Small end bevels estimated from the close-up, modelled by cone envelopes.
 rc=AF/math.sqrt(3);small=rc-.18
 lo=cq.Solid.makeCone(small,rc+.05,.23,cq.Vector(0,0,0),cq.Vector(0,0,1))
 hi=cq.Solid.makeCone(rc+.05,small,.23,cq.Vector(0,0,length-.23),cq.Vector(0,0,1))
 return s.intersect(lo.fuse(cyl(rc+.05,length-.46,.23)).fuse(hi)).clean()

def spacer(length,male=True):
 s=chamfer_envelope_hex(length)
 if male:
  s=s.fuse(thread(D,6).translate((0,0,length)))
  bore_depth=min(6.5,length-2)
  s=s.cut(female_tool(bore_depth))
  s=s.cut(cq.Solid.makeCone(1.40,1.03,.28,cq.Vector(0,0,0),cq.Vector(0,0,1)))
 else:
  bore_depth=length
  s=s.cut(female_tool(length))
  s=s.cut(cq.Solid.makeCone(1.40,1.03,.28,cq.Vector(0,0,0),cq.Vector(0,0,1)))
  s=s.cut(cq.Solid.makeCone(1.03,1.40,.28,cq.Vector(0,0,length-.28),cq.Vector(0,0,1)))
 s=s.clean();assert s.isValid() and len(s.Solids())==1
 return s,bore_depth

def screw(length):
 head=cyl(2.35,1.35,length)
 # Shallow domed pan head, approximated by two smooth cones, rounded rim.
 head=head.fuse(cq.Solid.makeCone(2.35,1.95,.65,cq.Vector(0,0,length+1.35),cq.Vector(0,0,1)))
 for a in (0,90):
  recess=box(2.55,.64,1.16,(0,0,length+.92)).rotate((0,0,0),(0,0,1),a)
  head=head.cut(recess)
 s=thread(D,length).fuse(head).clean();assert s.isValid() and len(s.Solids())==1
 return s

def nut():
 s=chamfer_envelope_hex(2).cut(female_tool(2))
 s=s.cut(cq.Solid.makeCone(1.43,1.03,.30,cq.Vector(0,0,0),cq.Vector(0,0,1)))
 s=s.cut(cq.Solid.makeCone(1.03,1.43,.30,cq.Vector(0,0,1.70),cq.Vector(0,0,1)))
 s=s.clean();assert s.isValid() and len(s.Solids())==1
 return s

def washer():
 s=cyl(2.5,.5).cut(cyl(1.35,.52,-.01)).clean()
 assert s.isValid() and len(s.Solids())==1;return s

def helix_probes(d,length,z=0,internal=False):
 probes=[]
 for k in range(2,int(length/P)-1,3):
  probes.extend([dict(point=[d/2-.10,0,z+k*P],occupied=not internal,kind='helical_crest'),
   dict(point=[d/2-.10,0,z+(k+.5)*P],occupied=internal,kind='helical_valley')])
 return probes

def item(file,title,parts,params,probes=None,design=False,view=(.7,-.9,1.05)):
 return dict(folder='fixations-raspberry-pi-5',filename=file,title=title,parts=[('Piece_'+n,s,c) for n,s,c in parts],
  published=['Nylon noir, filetage commercial M2.5, longueur nominale selon variante Amazon.',
   'Raspberry Pi 5 : quatre trous Ø2.7 mm, rectangle de référence 58 x 49 mm.'],
  estimated=LIMITS,params=params,probes=probes or [],design=design,view=view,
  source_pages=['photos/Ewwtrey-longueurs-original.jpg','photos/Ewwtrey-details-original.jpg',
   'notices/RaspberryPi-5-plan-mecanique-original.pdf p.1',
   'Essentra-filetages-plastiques-reference-original.pdf : autre fabricant, pas usuel seulement'])

def main():
 sys.stdout.reconfigure(encoding='utf-8');OUT.mkdir(parents=True,exist_ok=True)
 cq.Shape.BoundingBox=optimal;models=[];pieces={}
 for male,lengths in [(True,[6,8,10,15,20]),(False,[6,10,15,20])]:
  for length in lengths:
   s,depth=spacer(length,male);kind='mf' if male else 'ff';name=f'entretoise-{kind}-m2-5-{length}'+('-plus-6' if male else '')
   normalization=None
   if not male:s,normalization=normalize_ff(s,name)
   pieces[name]=s
   probes=[dict(point=[0,0,.5],occupied=False),dict(point=[2.2,0,min(2,length/2)],occupied=True)]
   probes += helix_probes(D+.06,depth,internal=True)
   if male:probes += [dict(point=[0,0,length-.5],occupied=True),dict(point=[0,0,length+3],occupied=True)]+helix_probes(D,6,z=length)
   else:probes += [dict(point=[0,0,length/2],occupied=False)]
   models.append(item(name+'.step',f'Entretoise {kind.upper()} M2.5 | {length}'+('+6' if male else '')+' mm',[(name,s,BLACK)],
    dict(body_length_mm=length,male_length_mm=6 if male else 0,surplats_estimated_mm=AF,
     female_depth_estimated_mm=depth,female_through_assumed=not male,thread_nominal_mm=D,pitch_assumed_mm=P,
     spline_preparation=normalization),probes))
 for length in [8,12,20]:
  s=screw(length);name=f'vis-cruciforme-m2-5-{length}';pieces[name]=s
  models.append(item(name+'.step',f'Vis nylon M2.5 x {length} | empreinte cruciforme',[(name,s,BLACK)],
   dict(under_head_length_mm=length,head_diameter_estimated_mm=4.7,head_height_estimated_mm=2,pitch_assumed_mm=P),
   [dict(point=[0,0,1],occupied=True),dict(point=[0,0,length+1.5],occupied=False)]+helix_probes(D,length)))
 pieces['ecrou-m2-5']=nut();pieces['rondelle-m2-5']=washer()
 models.append(item('ecrou-m2-5.step','Ecrou hexagonal nylon M2.5 | filetage interieur',
  [('Ecrou_noir',pieces['ecrou-m2-5'],BLACK)],dict(surplats_estimated_mm=5,height_estimated_mm=2,pitch_assumed_mm=P),
  [dict(point=[0,0,1],occupied=False),dict(point=[2.2,0,1],occupied=True)]+helix_probes(D+.06,2,internal=True)))
 models.append(item('rondelle-m2-5.step','Rondelle nylon M2.5 | dimensions estimees',
  [('Rondelle_noire',pieces['rondelle-m2-5'],BLACK)],dict(od_estimated_mm=5,id_estimated_mm=2.7,thickness_estimated_mm=.5),
  [dict(point=[0,0,.25],occupied=False),dict(point=[2,0,.25],occupied=True)]))
 # Demonstration arrangement only: no chassis, PCB, cooler or GPIO solids.
 # Body sits on z=0. Stud points up through the future PCB at z=10.
 # 1.6-mm PCB and 2-mm panel are explicit temporary thickness assumptions.
 station=[];body=pieces['entretoise-mf-m2-5-10-plus-6'];nut_z=12.1
 topnut=pieces['ecrou-m2-5'].rotate((0,0,0),(0,0,1),(nut_z-10)*360/P).translate((0,0,nut_z))
 bottomscrew=pieces['vis-cruciforme-m2-5-8'].rotate((0,0,0),(0,1,0),180)
 bottomscrew=bottomscrew.rotate((0,0,0),(0,0,1),5.5*360/P-180).translate((0,0,5.5))
 station=[('Entretoise_MF_10_plus_6',body,BLACK),('Ecrou_superieur',topnut,BLACK),
  ('Rondelle_superieure',pieces['rondelle-m2-5'].translate((0,0,11.6)),BLACK),
  ('Rondelle_inferieure',pieces['rondelle-m2-5'].translate((0,0,-2.5)),BLACK),('Vis_inferieure_8',bottomscrew,BLACK)]
 overlaps=[]
 for (na,a,ca),(nb,b,cb) in itertools.combinations(station,2):
  v=a.intersect(b).Volume();overlaps.append(dict(a=na,b=nb,intersection_mm3=v));assert v<1e-6,(na,nb,v)
 parts=[]
 for i,(x,y) in enumerate(HOLES):
  parts.extend((f'Point_{i+1}_{n}',s.translate((x,y,0)),c) for n,s,c in station)
 models.append(item('quatre-fixations-pi-5-10mm-etude.step','Pi 5 | quatre fixations nylon | pose provisoire 10 mm',parts,
  dict(hole_centres_reference_mm=HOLES,rectangle_reference_mm=[58,49],body_height_study_mm=10,
   PCB_thickness_study_mm=1.6,panel_thickness_study_mm=2,washer_thickness_study_mm=.5,
   lower_screw_engagement_study_mm=5.5,female_depth_study_mm=6.5,upper_stud_free_length_study_mm=1.9,
   PCB_and_chassis_omitted_intentionally=True,chassis_final_component=True,definitive_height_selected=False,
   parts_per_station=5,station_overlaps=overlaps),design=True,view=(.6,-.8,1.8)))
 results=[]
 for m in models:
  data=export_model(m);data['generated_on']='2026-10-14'
  imported=cq.importers.importStep(str(OUT/m['filename'])).val()
  data['validation']['volume_after_default_quadrature_mm3']=imported.Volume()
  data['validation']['default_volume_purpose']='Compare with FreeCAD default Volume; adaptive values remain the strict STEP round-trip reference.'
  data['coordinate_system']='Axe Z. Pièce seule : base du corps z=0 ; vis : pointe z=0, dessous tête z=L. Pose : assise z=0, PCB étudié à z=10, châssis absent.'
  data['native_vendor_cad']=False;data['hardware_measured']=False
  (OUT/m['filename']).with_suffix('.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');results.append(data)
 catalogue=dict(generated_on='2026-10-14',native_vendor_cad=False,hardware_measured=False,
  total_models=len(results),models=results,limits=LIMITS)
 (OUT/'catalogue.json').write_text(json.dumps(catalogue,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('MODELS',len(results),'COMPLETE',flush=True)

if __name__=='__main__':main()
