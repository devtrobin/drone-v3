"""Native Molex housing, estimated contact details and continuous GPIO leads."""
from pathlib import Path
import sys,json,math,itertools
import cadquery as cq
import numpy as np
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from build_running_gear_step import box,cyl,export_model,sha
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/connecteur-gpio';OUT=BASE/'3D'
BLACK=(.012,.014,.018);GOLD=(.7,.43,.1);TIN=(.56,.59,.62);CU=(.61,.28,.10)
COLORS={'red':(.7,.01,.008),'black':(.014,.017,.02),'white':(.87,.87,.82),'green':(.01,.36,.07),'yellow':(.9,.69,.015),'blue':(.015,.08,.65)}
CONTACT_FIT_RELIEF_MM3=0
PINS=[(1,'3V3_MON','green'),(2,'5V_A','red'),(4,'5V_B','red'),(6,'GND_PWR_A','black'),(9,'GND_PWR_B','black'),
 (11,'WARN1','white'),(12,'PWM_SERVO','yellow'),(13,'WARN2','white'),(14,'GND_PWR_C','black'),(15,'DONE','blue'),
 (20,'GND_PWR_D','black'),(32,'PWM_ESC_G','yellow'),(33,'PWM_ESC_D','yellow'),(34,'GND_ESC_G','black'),(39,'GND_ESC_D','black')]
def pos(pin):return (((pin-1)//2-9.5)*2.54,(-1 if pin%2 else 1)*1.27)
def optimal(self,tolerance=None):
 b=Bnd_Box();BRepBndLib.AddOptimal_s(self.wrapped,b,False,False);return cq.BoundBox(b)
def housing():
 s=cq.importers.importStep(str(OUT/'sources/022552401.stp')).val()
 solids=s.Solids();assert len(solids)==1
 # Drawing Y is mating direction; reframe it as Z, geometry unchanged.
 return solids[0].rotate((0,0,0),(1,0,0),-90).translate((0,0,7.62))
def terminal(native_housing=None):
 global CONTACT_FIT_RELIEF_MM3
 # Local details reconstructed from the supplier photo, NOT native contact CAD.
 # Gold sleeve has two stamped spring beams around the square mating pin.
 outer=box(1.28,1.28,5.7,(0,0,1.45));inner=box(.99,.99,5.9,(0,0,1.35))
 front=outer.cut(inner)
 front=front.cut(box(.18,1.35,4.7,(.54,0,2.25)))
 front=front.cut(box(.7,.3,2.5,(0,.62,3.0)))
 # Formed beams converge but leave the nominal mating cavity open.
 for sign in [-1,1]:
  beam=cq.Workplane('YZ').polyline([(sign*.60,2.2),(sign*.40,4.1),(sign*.36,5.6),(sign*.48,6.5),
    (sign*.59,6.5),(sign*.50,5.6),(sign*.54,4.1),(sign*.64,2.2)]).close().extrude(.65).val().translate((-.325,0,0))
  front=front.fuse(beam)
 front=front.fuse(box(.98,.15,1.2,(0,-.565,7.0)))
 rear=box(.98,.15,4.10,(0,-.565,7.95))
 # Retaining tongue and separate conductor / insulation crimp wings.
 rear=rear.fuse(box(.60,.17,1.4,(0,-.57,7.9)).rotate((0,-.57,7.9),(1,-.57,7.9),-12))
 for z,h,r in [(9.75,1.7,.47),(12.0,1.8,.88)]:
  shell=cyl(r,h,z).cut(cyl(max(r-(.13 if r>.6 else .14),.2),h+.2,z-.1))
  shell=shell.cut(box(.25,2*r+.1,h+.3,(0,0,z-.15)))
  shell=shell.fuse(box(.94,.16,h,(0,-.83 if r>.6 else -.48,z)))
  rear=rear.fuse(shell)
 bridge=cq.Workplane('YZ').polyline([(-.64,11.45),(-.49,11.45),(-.75,12.15),(-.91,12.15)]).close().extrude(.94).val().translate((-.47,0,0))
 rear=rear.fuse(bridge).intersect(box(5,5,12,(0,0,8.2)))
 # The estimated neck needs a tiny clearance relief at a native housing rib.
 # This changes only our reconstruction, never the supplier's housing geometry.
 if native_housing is None:native_housing=housing()
 x,y=pos(1);pocket=native_housing.intersect(rear.translate((x,y,0))).translate((-x,-y,0))
 CONTACT_FIT_RELIEF_MM3=pocket.Volume()
 if CONTACT_FIT_RELIEF_MM3>1e-9:rear=rear.cut(pocket)
 front=front.clean();rear=rear.clean();assert front.isValid() and rear.isValid()
 assert len(front.Solids())==len(rear.Solids())==1,(len(front.Solids()),len(rear.Solids()))
 return front,rear
def cable(pin,color):
 x,y=pos(pin);# Both rows bend outward (+Y), away from cooling air intake.
 top=27.1+(3 if pin%2 else 0)
 points=[cq.Vector(x,y,18.1),cq.Vector(x,y,25.1),cq.Vector(x,y+7,top+5),cq.Vector(x,y+21,top+5)]
 e=cq.Edge.makeBezier(points)
 def sweep_from(z,r):
  start=cq.Vector(x,y,z);line=cq.Edge.makeLine(start,points[0]);path=cq.Wire.assembleEdges([line,e])
  return cq.Workplane(cq.Plane(origin=start,normal=(0,0,1))).circle(r).sweep(cq.Workplane('XY').newObject([path]),isFrenet=False).val()
 outer=sweep_from(12.2,.75);core=sweep_from(9.6,math.sqrt(.326/math.pi))
 sheath=outer.cut(core).clean();assert len(core.Solids())==len(sheath.Solids())==1 and core.isValid() and sheath.isValid()
 for u in np.linspace(0,1,61):
  q=e.positionAt(float(u));assert core.isInside(q,1e-6)
  assert sheath.isInside(q+cq.Vector(.55,0,0),1e-6)
 for z in [9.7,12.3,15.24,18.0]:assert core.isInside(cq.Vector(x,y,z),1e-6)
 return [(f'Pin{pin:02}_ame_equivalente_22AWG',core,CU),(f'Pin{pin:02}_gaine_{color}',sheath,COLORS[color])],dict(pin=pin,core_solids=1,sheath_solids=1,centreline_probes=65,sheath_probes=61,
  endpoint=e.endPoint().toTuple(),length_axis_mm=e.Length()+8.5,stripped_length_study_mm=2.6,pose_illustrative=True)
def item(file,title,parts,params):return dict(folder='connecteur-gpio',filename=file,title=title,parts=parts,
 params=params,estimated=['Boîtier : géométrie CAO Molex conservée, seulement rotation et translation.',
 'Contacts : reconstruction de lecture à partir de la photo ; longueur, tôlerie, ressorts et forme du sertissage estimés.',
 'Couleurs : noir de résine publié, or/étain publiés ; nuances optiques reconstruites.',
 'Fil : diamètre gaine 1,5 mm annoncé pour Adafruit3175 ; âme équivalente AWG22, nombre de brins non publié non inventé.',
 'Fils courbes courts pour implantation : ni longueurs de coupe ni terminaisons aval à fabriquer selon ce STEP.',
 'Modèle d’étude : aucun essai sur GPIO Pi ni tenue thermique, vibration ou sertissage qualifié.'],
 published=['Molex22-55-2401 : 40 positions, pas2,54mm et géométrie du STEP natif.',
 'Contact16-02-0103 : 22/24AWG, diamètre isolant max1,63mm, bronze phosphoreux, contact or et terminaison étain.'],
 view=(.45,-1,.65),design=False,probes=[],source_pages=['Molex CAO native via Farnell1991069.zip',
 'Plan SD-70450-0001-0026 via IHS','Fiche contact2013 via Farnell1711811.pdf','Adafruit3175 produit'])
def main():
 sys.stdout.reconfigure(encoding='utf-8');cq.Shape.BoundingBox=optimal;OUT.mkdir(parents=True,exist_ok=True)
 body=housing();gold,tin=terminal(body);b=body.BoundingBox()
 print('HOUSING',b.xlen,b.ylen,b.zlen,flush=True)
 parts=[('Boitier_Molex_geometrie_native',body,BLACK)];fitted=[];wires=[];continuity=[];overlaps=[];wire_pairs=[]
 for pin,signal,col in PINS:
  x,y=pos(pin);g=gold.translate((x,y,0));t=tin.translate((x,y,0))
  # Contact fit is estimated; report reconstruction interference, never hide it.
  overlap=body.intersect(g.fuse(t)).Volume()
  overlaps.append(dict(pin=pin,contact_housing_overlap_mm3=overlap))
  fitted.extend([(f'Pin{pin:02}_{signal}_contact_or',g,GOLD),(f'Pin{pin:02}_{signal}_sertissage_etain',t,TIN)])
  wire,check=cable(pin,col);wires+=wire;continuity.append(check)
  volume_wire_plastic=body.intersect(wire[0][1].fuse(wire[1][1])).Volume()
  assert volume_wire_plastic<1e-6,('wire/plastic',pin,volume_wire_plastic)
  assert g.intersect(t).Volume()<1e-6,('gold/tin',pin)
  crimp_insulation_overlap=t.intersect(wire[1][1]).Volume()
  assert crimp_insulation_overlap<1e-6,('crimp/insulation',pin,crimp_insulation_overlap)
 print('CONTACT_INTERFERENCE',max(r['contact_housing_overlap_mm3'] for r in overlaps),flush=True)
 assert max(r['contact_housing_overlap_mm3'] for r in overlaps)<1e-6
 # Only equal-column wires can approach within their summed radii. The others
 # have a constant X gap >=2.54mm, above the 1.5mm combined wire diameter.
 for i,j in itertools.combinations(range(len(PINS)),2):
  if abs(pos(PINS[i][0])[0]-pos(PINS[j][0])[0])>1.5:continue
  a=wires[2*i][1].fuse(wires[2*i+1][1]);bwire=wires[2*j][1].fuse(wires[2*j+1][1]);v=a.intersect(bwire).Volume()
  wire_pairs.append(dict(pins=[PINS[i][0],PINS[j][0]],overlap_mm3=v));assert v<1e-6,wire_pairs[-1]
 par=dict(pitch_mm=2.54,positions=40,populated_pins=[p for p,n,c in PINS],body_mm=[b.xlen,b.ylen,b.zlen],
  native_source_sha256=sha(OUT/'sources/022552401.stp'),contact_dimensions_estimated=True,contact_fit_relief_estimated_mm3=CONTACT_FIT_RELIEF_MM3,
  contact_housing_reconstruction_overlap=overlaps,wire_continuity=continuity,wire_close_pair_checks=wire_pairs,
  wire_OD_announced_mm=1.5,wire_core_equivalent_area_mm2=.326)
 models=[item('molex-22-55-2401-boitier-noir.step','Molex 22-55-2401 : boitier officiel recolore',parts,par),
  item('molex-16-02-0103-contact-detaille.step','Molex 16-02-0103 : contact reconstruit', [('Zone_contact_or',gold,GOLD),('Zone_sertissage_etain',tin,TIN)],par),
  item('connecteur-gpio-15-contacts-detaille.step','GPIO : boitier et 15 contacts',parts+fitted,par),
  item('connecteur-gpio-faisceau-detaille.step','GPIO : faisceau de pose avec 15 fils continus',parts+fitted+wires,par)]
 results=[]
 for m in models:
  meta=export_model(m);meta.update(generated_on='2026-10-14',generator='tools/build_gpio_step.py',generator_sha256=sha(Path(__file__)),
   coordinate_system='X:20 colonnes, Y:2 rangées; face accouplement Z0, sortie fils +Z; pin1=(-24.13,-1.27). Vue conforme au plan de raccordement.',
   source_manifest_sha256=sha(BASE/'assets.json'),body_geometry_native=not m['filename'].startswith('molex-16'),native_non_solid_annotations_omitted=True)
  if m['filename'].startswith('molex-22'):
   meta['native_vendor_cad']=True;meta['geometry_modified']=False;meta['coordinate_transformed']=True
  (OUT/Path(meta['file']).with_suffix('.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');results.append(meta)
 cat=dict(generated_on='2026-10-14',model_count=4,models=results)
 (OUT/'catalogue.json').write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (OUT/'provenance.json').write_text(json.dumps(dict(**cat,source_manifest_sha256=sha(BASE/'assets.json'),original_STEP='sources/022552401.stp'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('DONE',[(m['file'],m['bytes']) for m in results],flush=True)
if __name__=='__main__':main()
