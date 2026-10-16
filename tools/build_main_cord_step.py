"""Compact coloured cord assembly, detailed components, continuous swept wires."""
from pathlib import Path
import sys,json,math,hashlib,shutil,os
import cadquery as cq
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from build_running_gear_step import box,cyl,export_model
from build_connector_step import connector
ROOT=Path(__file__).resolve().parents[1];ALLBASE=ROOT/'Composants';BASE=ALLBASE/'cordon-principal-batterie'
TIN=(.57,.62,.65);BLACK=(.015,.019,.024);RED=(.70,.01,.01);ADHESIVE=(.13,.10,.075)
ALL=[];CORDCHECKS=[]
def optimal(self,tolerance=None):
 b=Bnd_Box();BRepBndLib.AddOptimal_s(self.wrapped,b,False,False);return cq.BoundBox(b)
def save(m,folder):
 m.update(generated_on='2026-10-15',component_folder=folder,relative_step_path=(Path(folder)/'3D'/m['file']).as_posix())
 p=ALLBASE/m['relative_step_path'];s=cq.importers.importStep(str(p)).val();m['validation']['volume_after_default_quadrature_mm3']=s.Volume()
 m['generator']='tools/build_main_cord_step.py';m['generator_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
 p.with_suffix('.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');ALL.append(m)
 return m
def add(sub,name,title,parts,published,estimated,params=None,probes=None,view=(.6,-1,.55),design=False):
 folder='cordon-principal-batterie'+('/'+sub if sub else '')
 item=dict(folder=folder,filename=name+'.step',title=title,parts=[('Piece_'+n,s,c) for n,s,c in parts],published=published,
  estimated=estimated+['Couleurs et détails non cotés estimés, aucune pièce mesurée ; aucune qualification à44A.'],params=params or {},probes=probes or [],view=view,design=design,source_pages=['Voir sources.json et assets.json du cordon'])
 m=export_model(item);return save(m,folder)
def lug(crimp=False):
 # Principal TE product-page dimensions. Outer barrel/profile are estimated.
 ri=1.205 if crimp else 1.64
 ro=math.sqrt(2.43**2-1.64**2+ri**2) if crimp else 2.43
 shell=cyl(ro,7.3).cut(cyl(ri,7.6,-.1))
 if not crimp:
  shell=shell.cut(cq.Solid.makeCone(ri+.20,ri,.55,cq.Vector(0,0,0),cq.Vector(0,0,1)))
  for z in [1.6,2.4,3.2,4.,4.8]:shell=shell.cut(cyl(ri+.055,.12,z))
 # Flattened tongue tangent to bottom of barrel, not an idealised separate washer.
 tab=box(5.8,.79,6.9,(0,-2.035,5.8))
 plate=cq.Solid.makeCylinder(4.765,.79,cq.Vector(0,-2.43,14.535),cq.Vector(0,1,0))
 hole=cq.Solid.makeCylinder(2.63,1.1,cq.Vector(0,-2.55,14.535),cq.Vector(0,1,0))
 s=shell.fuse(tab).fuse(plate).cut(hole).clean()
 # Fine seam relief and embossed/engraved wire gauge; optical estimates.
 if not crimp:s=s.cut(box(.05,.10,5.3,(0,ro-.02,.65)))
 plane=cq.Plane(origin=(0,-2.43,9.1),xDir=(1,0,0),normal=(0,-1,0))
 marks=cq.Workplane(plane).text('12-10',1.05,-.07,font='Arial',kind='bold',combine=True).val()
 s=s.cut(marks).clean();assert s.isValid() and len(s.Solids())==1
 return s
def revolved(pts):
 return cq.Workplane('XZ').polyline(pts).close().revolve(360,(0,0),(0,1)).val()
def sleeve(installed=False):
 if not installed:
  return [('paroi_polyolefine',cyl(4.4,20).cut(cyl(4.15,20.2,-.1)),BLACK),('adhesif',cyl(4.15,20).cut(cyl(4.,20.2,-.1)),ADHESIVE)]
 # Fitted contour is estimated, not the free recovered ATUM dimensions.
 inside=[(2.25,-10),(2.25,-1),(2.60,1),(2.60,5.5),(3.60,7),(3.60,8)]
 glue=.18;wall=.65
 gluepts=inside+[(r+glue,z) for r,z in reversed(inside)]
 wallpts=[(r+glue,z) for r,z in inside]+[(r+glue+wall,z) for r,z in reversed(inside)]
 return [('adhesif_installe_estime',revolved(gluepts),ADHESIVE),('paroi_installee_estimee',revolved(wallpts),BLACK)]
def edges_for(x,endx,endz):
 # Two exact circular arcs avoid unstable long annular Bezier sweep surfaces.
 # Straight ends and both arc tangents match; no conductor is cut at the joins.
 sign=1 if endx>x else -1;R=60.;angle=math.acos(1-abs(endx-x)/(2*R));z0=50.;z2=z0+2*R*math.sin(angle)
 def first(v):return cq.Vector(x+sign*R*(1-math.cos(v)),0,z0+R*math.sin(v))
 def second(v):return cq.Vector(endx-sign*R*(1-math.cos(v)),0,z2-R*math.sin(v))
 return [cq.Edge.makeLine(cq.Vector(x,0,14.2),first(0)),cq.Edge.makeThreePointArc(first(0),first(angle/2),first(angle)),
  cq.Edge.makeThreePointArc(second(angle),second(angle/2),second(0)),cq.Edge.makeLine(second(0),cq.Vector(endx,0,endz))]
def trim_edges(edges,zstart,zend):
 # Only straight end segments are trimmed; curved middle is preserved exactly.
 return [cq.Edge.makeLine(cq.Vector(edges[0].startPoint().x,0,zstart),edges[0].endPoint()),*edges[1:-1],cq.Edge.makeLine(edges[-1].startPoint(),cq.Vector(edges[-1].endPoint().x,0,zend))]
def swept(edges,ro,ri=None):
 wire=cq.Wire.assembleEdges(edges);pl=cq.Plane(origin=edges[0].startPoint(),normal=edges[0].tangentAt(0))
 wp=cq.Workplane(pl).circle(ro)
 if ri:wp=wp.circle(ri)
 s=wp.sweep(cq.Workplane('XY').newObject([wire]),isFrenet=False).val()
 assert s.isValid() and len(s.Solids())==1
 target=math.pi*(ro**2-(ri or 0)**2)*sum(e.Length() for e in edges)
 assert abs(s.Volume()-target)/target<1e-4,('sweep volume',s.Volume(),target)
 count=0
 for edge in edges:
  for k in range(1,40):
   p=edge.positionAt(k/40);t=edge.tangentAt(k/40).normalized();a=t.cross(cq.Vector(0,1,0)).normalized()
   b=t.cross(a).normalized();rad=(ro+ri)/2 if ri else ro*.65
   for j in range(12):
    q=p+a.multiply(rad*math.cos(j*math.pi/6))+b.multiply(rad*math.sin(j*math.pi/6))
    assert s.isInside(q,1e-6),('continuity',k,j,p.toTuple());count+=1
 return s,count
def copy_wire(col):
 old=ALLBASE/'cable-puissance-12awg/3D'/f'bntechgo-12awg-{col}-680brins-detaille.step'
 folder='cordon-principal-batterie/fils-12awg';dest=ALLBASE/folder/'3D';dest.mkdir(parents=True,exist_ok=True)
 for suffix in ['.step','.png']:shutil.copyfile(old.with_suffix(suffix),dest/old.with_suffix(suffix).name)
 m=json.loads(old.with_suffix('.json').read_text(encoding='utf-8'));m['copied_unchanged_from']=str(old.relative_to(ALLBASE));m['reuse_reason']='Même référence et même lot déjà prévu ; échantillon25mm, pas longueur du cordon'
 save(m,folder)
def main():
 sys.stdout.reconfigure(encoding='utf-8');cq.Shape.BoundingBox=optimal
 plug=connector('M');pub=['AMASS2026 : M23,85 ×16,4 ×9,2 ; entraxe7,2historique']
 est=['Même reconstruction que le dossier XT60H ; godets, capot, marquages et rayons estimés. Sexe par contacts mâles côté véhicule ; polarité graphique illustrative, signes réels à contrôler.']
 add('prise-xt60h-m','amass-xt60h-m-cordon-detaille','AMASS XT60H-M | prise du cordon',plug,pub,est,params=dict(historical_pitch_mm=7.2,wire_exit_diameter_estimated_mm=4.5))
 copy_wire('rouge');copy_wire('noir')
 base=lug();compressed=lug(True)
 lp=['TE130191 : L19,3 ; œil5,26 ; paume0,79 ; IDcanon3,28 ; 12-10AWG.']
 le=['Largeur9,53 issue de distributeurs ; extérieurØ4,86, canon7,3, transition et marquage reconstruits sans planA3 récupéré.', 'Différences guideTE19,10/9,50/3,30 et distributeurs0,99 d’épaisseur conservées dans cotes.md.']
 add('cosses-te-130191','te-130191-nue-detaillee','TE SOLISTRAND 130191 | cosse nue', [('cosse_cuivre_etame',base,TIN)],lp,le,params=dict(length_mm=19.3,hole_diameter_mm=5.26,tongue_thickness_mm=.79,barrel_ID_mm=3.28,width_estimated_mm=9.53),probes=[dict(point=(0,-2.0,14.535),occupied=False),dict(point=(0,-2.0,12.05),occupied=False),dict(point=(4.,-2.0,14.535),occupied=True)],view=(.4,-1,.85))
 add('cosses-te-130191','te-130191-sertissage-illustratif','TE130191 | état serti illustratif',[('cosse_deformee_estimee',compressed,TIN)],lp,le+['Canon cylindrique ramené au faisceauØ2,41, section métallique conservée ; empreinteW et redistribution réelle non connues. Pas un résultat de sertissage qualifié.'],params=dict(crimp_bore_estimated_mm=2.41),view=(.4,-1,.85),design=True)
 add('isolation-atum','atum-8-2-coupe-20mm','ATUM8/2 | coupe avant rétraction',sleeve(),['TE : Øintfourni≥8 ; coupe20mm proposée, retraitlongitudinal jusqu’à15%.'],['Paroi fournie0,25 et adhésif0,15 estimés ; valeurs libres rétreintes ne décrivent pas cet état.'],params=dict(provisional_cut_length_mm=20),view=(.45,-1,.65),design=True)
 parts=list(plug);probes=[];cores=[]
 for i,(x,endx,name,color) in enumerate([(-3.6,-20.,'CP0_moins',BLACK),(3.6,20.,'CP0_plus',RED)]):
  edges=edges_for(x,endx,216.6);core,ncore=swept(edges,1.205);jacket,njacket=swept(trim_edges(edges,19.,210.),2.25,1.205)
  solder=cyl(1.65,4.0,14.2,x).cut(cyl(1.205,4.2,14.1,x))
  end=compressed.translate((endx,0,210.));installed=[(name+'_'+n,s.translate((endx,0,210.)),c) for n,s,c in sleeve(True)]
  contact=plug[i+1][1];gaps=dict(contact_solder_mm=contact.distance(solder),solder_core_mm=solder.distance(core),core_lug_mm=core.distance(end))
  assert max(gaps.values())<1e-6,gaps
  assert jacket.intersect(end).Volume()<1e-5
  CORDCHECKS.append(dict(pole=name,core_solids=1,jacket_solids=1,core_radial_samples=ncore,jacket_radial_samples=njacket,core_path_length_mm=sum(e.Length() for e in edges),bonds=gaps))
  cores.append(core);parts+=[(name+'_faisceau_etame_enveloppe',core,TIN),(name+'_silicone',jacket,color),(name+'_soudure',solder,TIN),(name+'_cosse_sertie_estimee',end,TIN)]+installed
  # Imported occupancy samples through straight/curved junctions and barrel end.
  for edge in edges:
   for u in [.1,.5,.9]:probes.append(dict(point=edge.positionAt(u).toTuple(),occupied=True))
  for edge in trim_edges(edges,19.,210.):
   p=edge.positionAt(.5)+cq.Vector(0,1.7275,0)
   probes.append(dict(point=p.toTuple(),occupied=True,material='gaine_silicone_annulaire'))
 assert cores[0].distance(cores[1])>4.;CORDCHECKS.append(dict(opposite_cores_min_gap_mm=cores[0].distance(cores[1])))
 ce=['Pose provisoire, environ0,20m par pôle ; aucune longueur finale ni emplacement de borne imposé.',
  'Faisceau métalliqueØ2,41 rempli pour implantation : pas680brins dans l’ensemble et pas un volume de cuivre réel ; voir les échantillons détaillés.',
  'Soudure et sertissage illustratifs ; manchon installé18mm avec profil/adhésif estimés, pas modèle du retrait réel.',
  'Contacts avant mâles et paumes sont volontairement nus pour raccordement ; arrière isolé par capot et manchons. Aucun fil interrompu ou extrémité flottante.',
  'La polarité dessinée ne dispense pas du contrôle sur le pack et les marques réels ; version44A non validée.']
 m=add('','cordon-principal-xt60-12awg-etude','Cordon principal | XT60H et deux cosses',parts,pub+lp+['BNTECHGO : siliconeØ4,5 ; faisceauØ2,41 annoncé.'],ce,params=dict(provision_m_per_color=.20,wire_OD_mm=4.5,wire_bundle_envelope_mm=2.41,lug_install_z_mm=210),probes=probes,view=(.60,-1,.32),design=True)
 m['wire_continuity_checks']=CORDCHECKS;savepath=ALLBASE/m['relative_step_path'];savepath.with_suffix('.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 # Close-up shows terminal transition and exposed electrical palm, not a cut in the cord.
 sample_core=cyl(1.205,29.2,-22.6);sample_jacket=cyl(2.25,22.6,-22.6).cut(cyl(1.205,22.8,-22.7))
 detail=[('cosse_sertie_estimee',compressed,TIN),('conducteur_enveloppe',sample_core,TIN),('gaine_silicone_rouge',sample_jacket,RED)]+sleeve(True)
 add('','terminaison-cosse-isolee-detail','CP0+ | détail de cosse et isolation',detail,lp+['Gaine siliconeØ4,5 ; faisceauØ2,41'],ce+['Échantillon court séparé du cordon, extrémité distale ouverte intentionnellement ; ne représente pas un fil laissé nu dans le véhicule.'],params=dict(sample_only=True),view=(.5,-1,.8),design=True)
 groups={}
 for m in ALL:groups.setdefault(m['component_folder'],[]).append(m)
 for folder,models in groups.items():
  out=ALLBASE/folder/'3D';out.mkdir(parents=True,exist_ok=True)
  (out/'catalogue.json').write_text(json.dumps(dict(generated_on='2026-10-15',model_count=len(models),models=models),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  rows=['# ModèlesSTEP - cordon principal','', 'Solides colorés en millimètres. Enveloppes et paramètres publiés séparés des détails estimés dans chaque JSON. Pas de CAO native fabricant récupérée.','', '| Modèle | Solides | STEP | Aperçu | Provenance |','| --- | ---: | --- | --- | --- |']
  for m in models:rows.append(f"| {m['title']} | {m['validation']['solids']} | [{m['file']}]({m['file']}) | [PNG]({m['preview']['file']}) | [JSON]({Path(m['file']).with_suffix('.json')}) |")
  rows+=['','Fils de l’ensemble continus du godet à la cosse, sondés radialement et raccords métalliques sans jeuCAO. Manchons et sertissage illustratifs ; capots/jeu réel à contrôler. Échantillons680brins à ouvrir séparément, ensemble léger pour implantation.','', 'L’ensemble ne représente ni batterie, ni fusible, ni rails, ni châssis : uniquement le cordon, avec paumes disponibles pour les bornes. La versionXT60 ne valide pas44A continus.', '', '[Dossier](../README.md)', '']
  (out/'README.md').write_text('\n'.join(rows),encoding='utf-8')
 # Global catalogue references every component file without duplicating geometry.
 (BASE/'3D/catalogue.json').write_text(json.dumps(dict(generated_on='2026-10-15',model_count=len(ALL),models=ALL,wire_continuity_checks=CORDCHECKS),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 rows=['# Catalogue STEP du cordon principal','','Solides colorés en millimètres, aperçu et JSON voisins de chaque fichier.','']
 for m in ALL:
  rel=os.path.relpath(ALLBASE/m['relative_step_path'],BASE/'3D').replace('\\','/')
  rows.append(f"- [{m['title']}]({rel}) - {m['validation']['solids']} solides.")
 rows+=['','Huit fichiers : ensemble léger, détail de terminaison, prise, deux fils à 680 brins, cosse nue/sertie et gaine avant rétraction. Fil plein de l’ensemble = enveloppe, pas volume de cuivre ; poses, sertissage, couleurs et profils non cotés estimés.','', '[Continuité et catalogue](catalogue.json) · [Validation FreeCAD](validation-freecad.json) · [Dossier](../README.md).', '']
 (BASE/'3D/README.md').write_text('\n'.join(rows),encoding='utf-8')
 print('DONE',len(ALL),'STEP',flush=True)
if __name__=='__main__':main()
