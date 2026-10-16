"""IC5 reconstruction based on the actual SPMXCA510 photograph; dimensions estimated."""
from pathlib import Path
import sys,json,math,hashlib,os
import cadquery as cq
import build_main_cord_step as m
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/cordon-principal-batterie'
ORANGE=(.95,.24,.005);GOLD=(.72,.46,.10);BLACK=m.BLACK;RED=m.RED;TIN=m.TIN
def plug():
 # All envelope dimensions here are estimates, not a Spektrum drawing.
 body=m.box(20.5,10.8,17.,fillet=.45)
 for x in [-4.8,4.8]:body=body.cut(m.cyl(3.35,10.8,-.1,x)).cut(m.cyl(2.67,17.3,-.1,x))
 body=body.cut(m.box(1.5,2.3,7.,(0,0,-.1),.2)).clean()
 for x,t in [(-7.7,'-'),(7.7,'+')]:
  pl=cq.Plane(origin=(x,-5.4,12.8),xDir=(1,0,0),normal=(0,-1,0))
  body=body.cut(cq.Workplane(pl).text(t,1.6,-.12,font='Arial',kind='bold',combine=True).val())
 cap=m.box(21.,11.2,9.,(0,0,15.),.6).cut(m.box(19.4,9.6,7.6,(0,0,14.9),.3))
 for x in [-4.8,4.8]:cap=cap.cut(m.cyl(2.85,9.4,14.8,x))
 for z in [16.5,18.2,19.9,21.6]:
  for y in [-5.55,5.55]:cap=cap.cut(m.box(18.5,.26,.40,(0,y,z),.07))
 parts=[('boitier_IC5_estime',body.clean(),ORANGE)]
 for i,x in enumerate([-4.8,4.8]):
  c=m.cyl(2.5,9.2,3.5,x).fuse(m.cyl(2.6,6.9,11.7,x))
  for angle in [0,90]:c=c.cut(m.box(.24,5.2,6.3,(x,0,3.45)).rotate((x,0,0),(x,0,1),angle))
  c=c.cut(m.cyl(.75,6.,3.4,x)).cut(m.cyl(1.9,5.3,13.4,x))
  parts.append((f'contact_puissance_{i+1}_estime',c.clean(),GOLD))
 # Small central data cavity shown, not an invented data wire or telemetry circuit.
 parts.append(('capot_noir_estime',cap.clean(),BLACK));return parts
def path(x,endx,endz):
 sign=1 if endx>x else -1;R=40.;a=math.acos(1-abs(endx-x)/(2*R));z=35.;z2=z+2*R*math.sin(a)
 def p(t):return cq.Vector(x+sign*R*(1-math.cos(t)),0,z+R*math.sin(t))
 def q(t):return cq.Vector(endx-sign*R*(1-math.cos(t)),0,z2-R*math.sin(t))
 return [cq.Edge.makeLine(cq.Vector(x,0,13.5),p(0)),cq.Edge.makeThreePointArc(p(0),p(a/2),p(a)),cq.Edge.makeThreePointArc(q(a),q(a/2),q(0)),cq.Edge.makeLine(q(0),cq.Vector(endx,0,endz))]
def sheath():
 # Installed contour on the estimated wire/cossette, independent of free ATUM dimensions.
 inside=[(2.75,-10),(2.75,-1),(2.80,1),(2.80,5.5),(3.60,7),(3.60,8)]
 return [('adhesif_installe_estime',m.revolved(inside+[(r+.18,z) for r,z in reversed(inside)]),m.ADHESIVE),('gaine_installee_estimee',m.revolved([(r+.18,z) for r,z in inside]+[(r+.83,z) for r,z in reversed(inside)]),BLACK)]
def lug():
 # Reconstructed contact bore in installed state, not the unknown actual W-crimp.
 ri=1.5;ro=math.sqrt(2.43**2-1.64**2+ri**2)
 shell=m.cyl(ro,7.3).cut(m.cyl(ri,7.6,-.1))
 tab=m.box(5.8,.79,6.9,(0,-2.035,5.8))
 ring=cq.Solid.makeCylinder(4.765,.79,cq.Vector(0,-2.43,14.535),cq.Vector(0,1,0))
 hole=cq.Solid.makeCylinder(2.63,1.1,cq.Vector(0,-2.55,14.535),cq.Vector(0,1,0))
 s=shell.fuse(tab).fuse(ring).cut(hole).clean();assert s.isValid() and len(s.Solids())==1;return s
def cable(parts,terminated):
 out=list(parts);probes=[];checks=[];cores=[]
 for i,(x,endx,color,name) in enumerate([(-4.8,-14.8,BLACK,'CP0_moins'),(4.8,14.8,RED,'CP0_plus')]):
  endz=104.5 if terminated else 114.0
  edges=path(x,endx,endz);core,n=m.swept(edges,1.5);je=m.trim_edges(edges,20.5,97.9 if terminated else 109.0);jacket,k=m.swept(je,2.75,1.5)
  solder=m.cyl(1.9,4.0,13.5,x).cut(m.cyl(1.5,4.2,13.4,x));bond=dict(contact_solder_mm=parts[i+1][1].distance(solder),solder_core_mm=solder.distance(core))
  out += [(name+'_metal_enveloppe_estimee',core,TIN),(name+'_gaine10AWG_estimee',jacket,color),(name+'_joint_usine_estime',solder,TIN)];cores.append(core)
  if terminated:
   c=lug().translate((endx,0,97.9));out.append((name+'_TE130191_sertie_estimee',c,TIN));bond['core_lug_mm']=core.distance(c)
   assert jacket.intersect(c).Volume()<1e-5
   probes.append(dict(point=(endx,-2.0,109.95),occupied=False,material='oeillet_integralement_circulaire'))
   out += [(name+'_'+n,s.translate((endx,0,97.9)),col) for n,s,col in sheath()]
  assert max(bond.values())<1e-6,bond
  for e in edges:
   for u in [.1,.5,.9]:probes.append(dict(point=e.positionAt(u).toTuple(),occupied=True))
  for e in je:probes.append(dict(point=(e.positionAt(.5)+cq.Vector(0,2.125,0)).toTuple(),occupied=True,material='gaine_silicone_annulaire'))
  checks.append(dict(pole=name,core_path_length_mm=sum(e.Length() for e in edges),core_radial_samples=n,jacket_radial_samples=k,bonds=bond))
 assert cores[0].distance(cores[1])>6.;return out,probes,checks
def main():
 sys.stdout.reconfigure(encoding='utf-8');cq.Shape.BoundingBox=m.optimal
 old=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'));m.ALL=[a for a in old['models'] if a.get('version')!='IC5_active' and a.get('component_folder')!='cordon-principal-batterie/cordon-ic5-spektrum'];initial=len(m.ALL)
 for a in m.ALL:a['version']='XT60_legacy_or_shared_component'
 pp=plug();pub=['Spektrum SPMXCA510 : IC5 Device, deux fils10AWG4in ; photo officielle montrant pré-câblage et capot.']
 est=['Reconstruction visuelle sans CAO native ni plan coté ; corps24×21×11 environ, contacts/entraxe, capot, lèvres et rayons estimés.', 'SiliconeØ5,5 et faisceau métalliqueØ3,0 estimés ; enveloppe pleine, pas nombre de brins ni masse de cuivre.', 'Polarité graphique illustrative : contrôler les marques et continuités du lot reçu. Pas de filSmart ajouté, cavitécentrale simplifiée.', 'Référencearrêtéechezfabricant ; aucun essai de courant ou de compatibilité d’accouplement du modèle.']
 m.add('cordon-ic5-spektrum','ic5-device-reconstruction-detaillee','IC5 Device | prise estimée du510',pp,pub,est,params=dict(body_all_dimensions_estimated=True),view=(.7,-1,-.6))
 for terminated,name,title in [(False,'spektrum-spmxca510-queue-etude','SPMXCA510 | pré-câblage de référence'),(True,'cordon-principal-ic5-10awg-etude','Cordon actif | IC5, 10 AWG et cosses')]:
  parts,probes,checks=cable(pp,terminated)
  a=m.add('cordon-ic5-spektrum',name,title,parts,pub+['TE130191 : L19,3 ; trou5,26 ; épaisseur0,79 ; plage12-10AWG.'],est+['Pose provisoire à2arcs tangents ; fils entiers du godet au raccord. Les queuesouvertes du modèle référence reproduisent un cordon avant ajout decosses, pas la terminaison installée.','Étatserti et profilATUM estimés, pas empreinteW validée. Étatinstallé : environ92mm de métal, sous longueur initiale4in ; aucune liste de coupe.'],params=dict(nominal_AWG=10,wire_OD_estimated_mm=5.5,bundle_OD_estimated_mm=3.,terminated=terminated),probes=probes,view=(.6,-1,.35),design=True)
  a['wire_continuity_checks']=checks
 for a in m.ALL[initial:]:
  a['version']='IC5_active';a['generator']='tools/build_main_cord_ic5_step.py';a['generator_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();p=ROOT/'Composants'/a['relative_step_path'];p.with_suffix('.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 out=BASE/'cordon-ic5-spektrum/3D';models=m.ALL[initial:];(out/'catalogue.json').write_text(json.dumps(dict(models=models,model_count=len(models)),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (out/'README.md').write_text('# STEP du cordon IC5 actif\n\nReconstruction détaillée, géométrie non mesurée. Les cotes de corps, contacts, capot et diamètres de fil sont estimées ; calibre10AWG/4in publiés.\n\n'+'\n'.join(f"- [{a['title']}]({a['file']}) ; [aperçu]({a['preview']['file']}) ; [provenance]({Path(a['file']).with_suffix('.json')})." for a in models)+'\n\nLes queues du modèle510de référence sont dénudées intentionnellement comme avant terminaison. Ouvrir cordon-principal-ic5-10awg-etude.step pour les deux cosses et gaines. Fils continus :1solide métallique et1gaine par pôle, quatre segments tangents ; volumes analytiques et sondes radiales contrôlés.\n\n[Montageactif](../../integration.md).\n',encoding='utf-8')
 (BASE/'3D/catalogue.json').write_text(json.dumps(dict(generated_on='2026-10-15',model_count=len(m.ALL),active_IC5_count=len(models),models=m.ALL),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 rows=['# Catalogue STEP : cordon actif IC5 et variante initiale','','## Version active IC5','']
 for a in models:rows.append(f"- [{a['title']}]({os.path.relpath(ROOT/'Composants'/a['relative_step_path'],BASE/'3D').replace(chr(92),'/')}) - {a['validation']['solids']} solides ; aperçu et JSON voisins.")
 rows+=['','## Composants communs et variante XT60 non retenue','']
 for a in m.ALL[:initial]:rows.append(f"- [{a['title']}]({os.path.relpath(ROOT/'Composants'/a['relative_step_path'],BASE/'3D').replace(chr(92),'/')}) - {a['validation']['solids']} solides.")
 rows+=['','Les cosses nues et la gaine fournie sont communes ; l’état serti12AWG et les modèlesXT60 ne sont pas le montageIC5. Deuxéchantillons de fil680brins réutilisés depuis le dossier12AWG, pas fils10AWGdu510. Référencesnonmesurées, détailsestimés ; pas unequalificationélectrique.','', '[Catalogue](catalogue.json) · [ImportsFreeCAD](validation-freecad.json) · [Sélectionactive](../README.md).','']
 (BASE/'3D/README.md').write_text('\n'.join(rows),encoding='utf-8');print('IC5',len(models),'models; total',len(m.ALL),flush=True)
if __name__=='__main__':main()
