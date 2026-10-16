"""Detailed coloured reconstructions; four ensembles, no chassis or PCB design."""
from pathlib import Path
import sys,json,math,hashlib
import cadquery as cq
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from build_running_gear_step import box,cyl,hexagon,export_model,ring
from build_pi_mount_step import thread
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants'
BLACK=(.018,.021,.025);TIN=(.54,.59,.62);GOLD=(.72,.46,.12);COPPER=(.58,.25,.10)
WHITE=(.87,.87,.83);GLASS=(.56,.65,.68);ORANGE=(.93,.22,.008);RED=(.7,.008,.009);YELLOW=(.66,.85,.016)
ALL=[]
def optimal(self,tolerance=None):
 b=Bnd_Box();BRepBndLib.AddOptimal_s(self.wrapped,b,False,False);return cq.BoundBox(b)
def add(folder,name,title,parts,published,estimated,params=None,probes=None,view=(.75,-1,1.2),design=False):
 a=dict(folder=folder,filename=name+'.step',title=title,parts=[('Piece_'+n,s,c) for n,s,c in parts],published=published,
 estimated=estimated+['Nuances optiques estimées ; géométrie non mesurée. Pas de plan de fabrication ni de qualification mécanique/électrique.'],
 params=params or {},probes=probes or [],view=view,design=design,source_pages=['Voir sources.json et cotes.md du composant / ensemble'])
 m=export_model(a);m['generated_on']='2026-10-14'
 s=cq.importers.importStep(str(BASE/folder/'3D'/m['file'])).val();m['validation']['volume_after_default_quadrature_mm3']=s.Volume()
 m['component_folder']=folder;m['relative_step_path']=(Path(folder)/'3D'/m['file']).as_posix()
 p=BASE/folder/'3D'/m['file'];p.with_suffix('.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 ALL.append(m);print('STEP',folder,name,m['validation']['solids'],m['bytes'],flush=True);return m
def wire(start,end,od,section,col,name,strip=0):
 # A single smooth Bezier span, straight tangent at both connector ends.
 a=cq.Vector(*start);b=cq.Vector(*end);delta=b-a
 e=cq.Edge.makeBezier([a,a+cq.Vector(0,0,delta.z*.40),b-cq.Vector(0,0,delta.z*.40),b])
 w=cq.Wire.assembleEdges([e]);pl=cq.Plane(origin=a,normal=e.tangentAt(0));r=math.sqrt(section/math.pi)
 core=cq.Workplane(pl).circle(r).sweep(cq.Workplane('XY').newObject([w]),isFrenet=False).val()
 sheath=cq.Workplane(pl).circle(od/2).sweep(cq.Workplane('XY').newObject([w]),isFrenet=False).val().cut(core).clean()
 assert len(core.Solids())==len(sheath.Solids())==1 and core.isValid() and sheath.isValid()
 for k in range(31):assert core.isInside(e.positionAt(k/30),1e-6)
 return [(name+'_ame_equivalente',core,COPPER),(name+'_gaine',sheath,col)]
def jr():
 f='connecteurs-commande/jr-pololu-1925';pub=['PlansPololu : boîtier14x7.90/7.70x2.75/2.65 ; capot18x10.30x4 ; pas2.54 mm.']
 est=['Contact, crimp, languettes et chanfreins fins reconstruits ; longueurs courtes du câblage illustratives.']
 # Inner housing: body width change near rear, three contact channels.
 body=box(7.9,2.75,8).fuse(box(7.7,2.65,6,(0,0,8)))
 for x in [-2.54,0,2.54]:
  body=body.cut(box(1.35,1.35,14.4,(x,0,-.2)))
  body=body.cut(box(1.25,.8,2.3,(x,-1.1,7)))
  body=body.fuse(box(.6,.22,2.0,(x,-1.27,6.8)))
 body=body.clean()
 assert len(body.Solids())==1 and body.isValid()
 cap=box(10.3,4,18,fillet=.12).cut(box(8.05,2.8,18.4,(0,0,-.2))).clean()
 # Integral retaining bump is small and offset from contact channels.
 cap=cap.fuse(box(.6,.10,1,(3.8,1.35,6))).clean()
 pin=box(.64,.64,5.5,(0,0,1.0)).fuse(box(.96,.16,8.5,(0,-.34,6.4)))
 pin=pin.fuse(box(.5,.13,1.8,(0,-.33,9.0)).rotate((0,-.33,9),(1,-.33,9),-14))
 for z,ro,ri,h in [(13.8,.46,.31,1.5),(15.6,.85,.74,1.9)]:
  shell=ring(ro,ri,h,z).cut(box(.20,2*ro+.1,h+.1,(0,0,z-.05)))
  # Narrow bridge joins both crimp regions without closing the wire channel.
  shell=shell.fuse(box(.7,.17,h+.2,(0,-ro+.08,z-.1)))
  pin=pin.fuse(shell).fuse(box(.6,.14,2,(0,-.33,z-.8)))
 pin=pin.clean()
 # A small horizontal bridge closes a numerical gap to the large crimp wing.
 if len(pin.Solids())!=1:pin=pin.fuse(box(.6,.45,2,(0,-.48,15.0))).clean()
 assert len(pin.Solids())==1 and pin.isValid()
 for name,title,s,col in [('jr-boitier','JR | boîtier intérieur',body,BLACK),('jr-capot','JR | capot extérieur',cap,BLACK),('jr-contact-male','JR | contact mâle à sertir',pin,GOLD)]:
  add(f,name,title,[(name,s,col)],pub,est,params=dict(pitch_mm=2.54))
 def connector(two=False):
  # Housing translated into shroud; pins leave rear for wire crimp.
  out=[('capot',cap,BLACK),('boitier',body.translate((0,0,6)),BLACK)]
  for i,x in enumerate([-2.54,0,2.54]):
   if two and i==1:continue
   out.append((f'contact_{i+1}',pin.translate((x,0,3.8)),GOLD))
  return out
 add(f,'jr-complet-3contacts','JR | connecteur complet3contacts',connector(),pub,est)
 add(f,'jr-esc-droit-2contacts','JR | ESC droit, BEC absent',connector(True),pub,est+['Cavité centrale réellement sans métal côté faisceauPi.'])
 allparts=[]
 for n,x0,two in [('ESC_gauche',-18,False),('Servo',0,False),('ESC_droit',18,True)]:
  for na,s,c in connector(two):allparts.append((n+'_'+na,s.translate((x0,0,0)),c))
  for i,x in enumerate([-2.54,0,2.54]):
   if two and i==1:continue
   color=[BLACK,RED,YELLOW][i]
   for na,s,c in wire((x0+x,0,21.0),(x0+x,9,54),1.5,.326,color,n+f'_fil{i+1}'):
    allparts.append((na,s,c))
 add(f,'trois-commandes-terminaisons-etude','Commandes | trois prises séparées',allparts,pub,est+['Pose éclatée des prises, queuescourtes ; raccordements aux bornes etGPIO décritsdans integration.md, pas reliésvisuellement ici.'],params=dict(installed_contacts=8,unused_in_12_contact_pack=4),design=True,view=(.6,-1,.8))
def wago(n):
 width=18.8 if n==3 else 30.;pitch=5.6;xs=[(i-(n-1)/2)*pitch for i in range(n)]
 shell=box(width,18.6,7.7,fillet=.55)
 # Front ports are rounded quadrangular openings with continuing passages.
 for x in xs:
  shell=shell.cut(box(4.2,14.5,4.25,(x,-2.3,1.3),.25))
  shell=shell.cut(box(4.7,13.8,1.5,(x,-.6,6.2),.20))
  shell=shell.cut(cyl(.65,1.9,6.0,x,7.7))
 parts=[('boitier_PC_transparence_non_encodee',shell.clean(),GLASS)]
 for i,x in enumerate(xs):
  lever=box(4.6,12.8,1.2,(x,-.45,7.2),.4)
  lever=lever.cut(box(2.8,3,.16,(x,3.9,8.28)))
  lever=lever.fuse(cyl(.75,4.0,6.9,x-2,5.5,axis=(1,0,0))).clean()
  parts.append((f'levier_orange_{i+1}',lever,ORANGE))
 # Shared metal part explicitly shows one potential. Spring shape illustrative.
 metal=box(width-1.8,2.6,.4,(0,5.6,2.0))
 for x in xs:
  metal=metal.fuse(box(3.2,11.5,.4,(x,.1,2.0)))
  spring=(cq.Workplane('YZ').polyline([(-4,2.4),(-4,2.7),(1.7,5.3),(5.0,4.2),(5.0,3.9),(1.8,4.9)]).close().extrude(2.8).val().translate((x-1.4,0,0)))
  metal=metal.fuse(spring)
  metal=metal.fuse(box(2.8,1.0,.45,(x,-3.9,2.15)))
 metal=metal.clean();assert len(metal.Solids())==1 and metal.isValid()
 parts.append(('barre_et_ressorts_estimes_un_potentiel',metal.clean(),TIN))
 return parts
def xh():
 # B3B-XH-A top-entry; published main geometry, no auxiliary footprint/PCB.
 h=box(9.9,5.75,7).cut(box(8.65,4.4,6.0,(0,0,1.3)))
 for x in [-3.8,3.8]:h=h.cut(box(.65,1.1,2.8,(x,-2.65,4.2)))
 for x in [-2.5,0,2.5]:h=h.cut(box(.64,.64,1.5,(x,-.525,-.1)))
 h=h.clean();pins=[(f'pin_{i+1}',box(.64,.64,9.2,(x,-.525,-3.4)),TIN) for i,x in enumerate([-2.5,0,2.5])]
 # XHP front portion has narrowed exterior which enters header; rear collar9.8.
 b=box(8.2,4.35,5.7).fuse(box(9.8,5.7,1.8,(0,0,5.7)))
 for x in [-2.5,0,2.5]:
  b=b.cut(box(1.95,1.8,7.9,(x,-.525,-.2)))
  b=b.cut(box(1.45,1.25,1.6,(x,-2.45,3.9)))
 for sign in [-1,1]:b=b.fuse(box(.35,1.3,1.0,(sign*4.25,0,1.0)))
 b=b.clean()
 contact=box(1.1,.15,4.8,(0,-.70,.2))
 for sign in [-1,1]:
  side=box(.12,1.05,2.8,(sign*.53,-.21,.2));contact=contact.fuse(side)
  beam=(cq.Workplane('XZ').polyline([(sign*.52,.4),(sign*.31,1.8),(sign*.38,3.0),(sign*.49,3.0),(sign*.42,1.8),(sign*.64,.4)]).close().extrude(.6).val().translate((0,.05,0)))
  contact=contact.fuse(beam)
 # Conductor/insulation crimps; open slit permits conductor entry.
 for z,ro,ri,hei in [(3.6,.53,.39,1.2),(4.7,.85,.70,1.4)]:
  shell=ring(ro,ri,hei,z).cut(box(.2,2,hei+.1,(0,0,z-.05)))
  contact=contact.fuse(shell).fuse(box(.65,.25,hei+.2,(0,-.60,z-.1)))
 contact=contact.clean()
 if len(contact.Solids())!=1:contact=contact.fuse(box(.6,.4,2.4,(0,-.61,3.4))).clean()
 assert len(contact.Solids())==1 and contact.isValid()
 return h,pins,b,contact
def connections():
 common='liaisons-alimentation-surveillance';pub=['WAGO2025/2024 :18.8ou30 x18.6x8.4,3ou5ports et unpotentiel.']
 est=['Poches, leviers, ressorts etbarreconductrice reconstruits ; transparence réelle représentée pargrisopaque dansSTEP.']
 for n in [3,5]:add(common+f'/wago-221-41{n}',f'wago-221-41{n}-detaille',f'WAGO221-41{n} | {n} ports',wago(n),pub,est,params=dict(width_mm=18.8 if n==3 else 30,depth_mm=18.6,height_mm=8.4,strip_mm=11,common_potentials=1))
 f=common+'/jst-xh-3';h,pins,b,contact=xh();p=['JST2025 : pas2.50,3positions ; embasesansboss9.9x5.75x7 ;XHP3collerette9.8x5.7x7.5 ;pin0.64.']
 e=['Réconstruction des évidements etressorts à partirdu catalogue, ajustement visuel seulement ; aucune donnéeCAO native téléchargée (distributionfabricantparformulaire/email).']
 add(f,'jst-b3b-xh-a','JSTB3B-XH-A | embase3positions',[('boitier',h,WHITE),*pins],p,e)
 add(f,'jst-xhp-3','JSTXHP-3 | boîtier3positions',[('boitier',b,WHITE)],p,e)
 add(f,'jst-sxh-001t-p06','JSTSXH | contact femelle',[('contact',contact,TIN)],p,e+['Dimensionsdel’enroulementdecrimp estimées ; aucunegéométrie d’outil oucotationsertissage inventée.'])
 # Mated projection: frontal narrowed body lies within header, collar above.
 con=[('embase',h,WHITE),*pins,('boitier_femelle',b.translate((0,0,2.30)),WHITE)]
 for i,x in enumerate([-2.5,0,2.5]):con.append((f'contact_femelle{i+1}',contact.translate((x,-.525,2.7)),TIN))
 add(f,'jst-xh-3-accouple-etude','JSTXH3 | accouplement de lecture',con,p,e+['Hauteurmâtée9.8nominale, positiondescontacts reconstruite ; assemblagenon validéen tolérances.'],design=True)
 balance_only()
 bn_only()
 f=common+'/fil-18awg'
 parts=[]
 for x,col in [(-2,RED),(2,BLACK)]:parts+=wire((x,0,0),(x,12,58),2.3,.7539822369,col,'fil18_'+('rouge' if x<0 else'noir'))
 add(f,'paire-18awg-courbe-etude','AlimentationPi | paire18AWG',parts,['18AWGBNTECHGO, siliconeØ2.3.'],['Âmeéquivalente0.754mm² pourreprésentationcourbe ; pas150brinscourbesdanscemodèle, longueurcourteillustrative.'],design=True)
 # Isolated multi-borne study, no Pi/PCB geometry and no unresolved5V sharing
 # represented as certified. All wires keep separate insulated paths.
 parts=[]
 for n,y,name in [(3,0,'5V'),(5,26,'GND'),(3,52,'BEC6V')]:
  parts +=[(name+'_'+na,s.translate((0,y,0)),c) for na,s,c in wago(n)]
 add(common,'trois-bornes-potentiels-separes-etude','Liaisons |5V,GND,6V distincts',parts,pub,est+['Implantationisolée pourlecture, aucuneconnexionentrelesbarres, longueursfinalesauchâssis. La3e413masseServo estdanslenomenclaturecommande.'],design=True,view=(.7,-1,1.7))
def strap_flat():
 # Flat250mm tape, metalloop, rounded end, three stitched panels.
 fabric=box(250,20,.9,fillet=2.3)
 parts=[('ruban_noir',fabric,BLACK)]
 for x,length in [(-91,66),(108,29)]:
  panel=box(length,20,.30,(x,0,.9),2.0);parts.append(('renfort_jaune_'+str(x),panel,YELLOW))
  stitches=[]
  for sign in [-1,1]:
   for xx in range(int(x-length/2+3),int(x+length/2-2),3):stitches.append(box(1.4,.18,.1,(xx,sign*8.7,1.20)))
  parts.append(('coutures_estimees_'+str(x),cq.Compound.makeCompound(stitches),TIN))
 # Steelwireloop inplaneXY, roundedrectangular centreline. Capsule corners
 # represented byfour torusquarters plusstraightsegments fusedbeforecut.
 outer=box(9.8,24.8,1.6,(127,0,-.20),3.0)
 loop=outer.cut(box(6.6,21.6,2,(127,0,-.40),1.4)).clean();parts.append(('boucle_metal_reconstruite',loop,TIN))
 # Geometric text, no texture needed in STEP.
 logo=cq.Workplane('XY').text('GEPRC',5,.06,font='Arial',kind='bold',halign='center',valign='center').val().translate((-92,0,1.2))
 parts.append(('marquage_GEPRC_estime',logo,WHITE));return parts
def strap_closed(x=0):
 # Rounded rectangle inYZ, swept widthX; tape perimeter outer-inner gives
 # one closed solid. This is a deformed installed-study state, no tensileclaim.
 outer=cq.Workplane('XY').box(20,49.4,29.4,centered=(True,True,False)).edges('|X').fillet(2.7).val().translate((x,0,0))
 inner=cq.Workplane('XY').box(20.4,47,27,centered=(True,True,False)).edges('|X').fillet(1.5).val().translate((x,0,1.2))
 tape=outer.cut(inner).clean()
 parts=[('ruban_ferme_pose_etude',tape,BLACK)]
 # Yellowreinforcements lie on top; overlap50mm stored alongtopandedge.
 parts.append(('renfort_superieur_jaune',box(20,36,.3,(x,0,29.4),2),YELLOW))
 loop=box(24.8,9.8,1.6,(x,18,29.1),3).cut(box(21.6,6.6,2,(x,18,28.9),1.4)).clean()
 parts.append(('boucle_metal',loop,TIN));return parts
def retention():
 f='maintien-batterie/sangles-geprc';p=['GEPRC :20x250, jaune/bleu,lot5 ; métalboucleobservé.']
 e=['Épaisseurs, boucle, texture etcoutures reconstruites ; fibres etcrochetsmicroscopiques noninventés. Formesdepose provisoires.']
 add(f,'sangle-geprc-20x250-detaillee','GEPRC | sangle20x250',strap_flat(),p,e,params=dict(tape_width_mm=20,tape_nominal_length_mm=250,study_thickness_mm=1.2),view=(.3,-1,2.2))
 add(f,'sangle-geprc-fermee-etude','GEPRC | posefermée provisoire',strap_closed(),p,e+['Modèlefermé simplifié, recouvrementreprésentéparrenfort, paslongueurdéveloppéefabrication.'],design=True)
 f='maintien-batterie/patin-silicone'
 for name,w,d,title in [('feuille-silicone-200x200x2',200,200,'Silicone | feuille200x200x2'),('patin-silicone-142x51-etude',142,51,'Silicone | patin142x51 provisoire')]:
  s=box(w,d,2,fillet=1 if w<200 else .25)
  add(f,name,title,[('silicone_blanc',s,WHITE)],['BENECREAT : deuxfeuilles200x200x2 blanches.'],['Coinsetaspect surfaceestimés ; patin142x51choixprovisoire, duretéetfriction inconnues.'],params=dict(length_mm=w,width_mm=d,thickness_mm=2),design=w<200,view=(.45,-1,1.5))
 parts=[('patin_provisoire',box(142,51,2,(0,0,1.2),1),WHITE)]
 for i,x in enumerate([-40,40]):parts.extend((f'sangle{i+1}_'+n,s,c) for n,s,c in strap_closed(x))
 add('maintien-batterie','deux-sangles-et-patin-etude','Maintien | deuxsangles etpatin',parts,p,e+['Batterieetchâssisabsents ; sections etespacements provisoires ; niveauintérieurbas1.2,padjusquà3.2,pack25hypothétique.'],design=True,view=(.6,-1,1.1))
def ed80(opened=False):
 # Datum z=0 is uppercase mountingplane; lowerbodyheight37 and terminals55.
 pts=[(-21,-25),(-29.5,-12),(-29.5,12),(-21,25),(0,29),(21,25),(29.5,12),(29.5,-12),(21,-25),(0,-29)]
 body=cq.Workplane('XY').polyline(pts).close().extrude(37).val().translate((0,0,-37))
 # Exteriorseam andshaftpassage; hidden switchinginternalsnot fabricated.
 body=body.cut(cyl(11.5,12,-11.9)).cut(box(1.1,2,21,(0,-28.8,-36)))
 body=body.cut(box(51,41,1.4,(0,0,-1.4),2.5))
 for x in [-24,24]:body=body.cut(cyl(2.75,37.4,-37.2,x,0))
 body=body.clean();parts=[('corps_noir_details_estimes',body,BLACK)]
 plate=box(51,41,1.4,(0,0,-1.4),2.5).cut(cyl(11.5,1.7,-1.5))
 for x in [-24,24]:plate=plate.cut(cyl(2.75,1.7,-1.5,x,0))
 parts.append(('capot_superieur',plate.clean(),BLACK))
 dz=-5 if opened else 0
 shaft=cyl(5,39,-8+dz).fuse(cyl(12.5,6,0+dz)).clean();parts.append(('axe_et_collet_noir_selon_photo',shaft,BLACK))
 # Knob14high,Ø48 withroundededges; lowerneckshape estimated.
 knob=cq.Workplane('XY').circle(24).extrude(14).edges().fillet(3.5).val().translate((0,0,42+dz))
 neck=cyl(16,32,10+dz).cut(cyl(1.7,32,13+dz,-16,0,axis=(1,0,0)))
 parts.append(('bouton_rouge',knob.fuse(neck).clean(),RED))
 for i,y in enumerate([-10.5,10.5]):
  terminal=thread(6,18,1).translate((0,y,-55)).fuse(cyl(4.7,4,-41,0,y)).clean()
  parts.append((f'borne_M6_{i+1}',terminal,TIN))
  nut=hexagon(10,5).cut(cyl(3.1,5.2,-.1)).translate((0,y,-52))
  washer=ring(6,3.2,1,-46).translate((0,y,0))
  parts.extend([(f'ecrou_borne_fourni_{i+1}',nut,TIN),(f'rondelle_borne_fournie_{i+1}',washer,TIN)])
 # IncludedM5mountingscrews visible, no separate purchase or chassis holes.
 for i,x in enumerate([-24,24]):
  head=cyl(4.8,3.1,0,x,0)
  for angle in [0,90]:head=head.cut(box(5.4,1.2,1.8,(x,0,1.4)).rotate((x,0,0),(x,0,1),angle))
  parts.append((f'tete_M5_posidriv_fournie_estimee_{i+1}',head.clean(),TIN))
 return parts
def lug():
 # Klauke95R6table: centre ofeye datum, actual lengthc1+l=26.
 palm=box(13.5,10,2,(-.25,0,0),.55);start=10
 transition=(cq.Workplane(cq.Plane(origin=(6.5,0,1),xDir=(0,1,0),normal=(1,0,0))).rect(10,2).workplane(offset=3.5).center(0,2).circle(3).loft(combine=False).val())
 s=palm.fuse(transition).fuse(cyl(3,9,3,start,axis=(1,0,0)))
 s=s.cut(cyl(3.25,2.2,-.1)).cut(cyl(2,10.3,3,8.7,axis=(1,0,0))).cut(cyl(.7,3,3,9.7)).clean()
 return s
def disconnect():
 f='coupure-manuelle/albright-ed80';p=['Albright2024 :59xcontourØ58, corps37 ;bornesM6 ;dessous55 ;hauteurhaut56/51 ;boutonØ48,h14.']
 e=['Corps àpans, axe,collet etformesfinestêtesécrous reconstruits ; bornesM6x1 supposéespasusuel, filetshélicoïdaux ;contactsressortsinternes nonreproduits.']
 for opened in [False,True]:
  add(f,'albright-ed80-'+('ouvert' if opened else'ferme')+'-detaille','AlbrightED80 | '+('ouvert' if opened else'fermé'),ed80(opened),p,e,params=dict(contact_state='open' if opened else'closed',stud_size='M6',stud_torque_Nm=[3.6,3.9],mount_reference_holes_mm=[25,5.5],mount_pitch_mm=48),view=(.7,-1,.9))
 f='coupure-manuelle/cosses-klauke-95r6';s=lug()
 add(f,'cosse-klauke-95r6-6mm2','Klauke95R6 | 6mm2,M6',[('Cuivre_etame',s,TIN)],['CatalogueKlauke :d1=4,a9,b10,d2=6.5,d4=6,c1=7,c2=6.5,l19.'],['Paume2,rayons,loft etfenêtreØ1.4estimés ;sanssertissage, sansgravureinventée.'],params=dict(section_mm2=6,hole_mm=6.5,overall_reconstructed_mm=26),probes=[dict(point=[0,0,1],occupied=False),dict(point=[18.5,0,3],occupied=False)])
 # Harness ends touchstudsenseparately. Uncrimpedterminal geometry explicitly
 # remains an externalintegration reference, not fabricatedconnection.
 parts=ed80(False)
 for i,y in enumerate([-10.5,10.5]):
  cos=s.rotate((0,0,0),(0,0,1),180 if i==0 else 0).translate((0,y,-44.5));parts.append((f'cosse95R6_{i+1}_pose_nonsertie',cos,TIN))
 add('coupure-manuelle','ed80-et-deux-cosses-etude','Coupure | ED80 etdeuxcosses',parts,p,e+['Positiondescossesprovisoire,sanscâblesdepuissance ;5mmdeborneetpaume peuventdemander autreempilement,lectureseulement. Visserieauchâssisreportée.'],design=True,view=(.7,-1,.8))
def index():
 groups={}
 for m in ALL:groups.setdefault(m['component_folder'].split('/')[0],[]).append(m)
 for folder,models in groups.items():
  b=BASE/folder/'3D';b.mkdir(parents=True,exist_ok=True)
  (b/'catalogue.json').write_text(json.dumps(dict(generated_on='2026-10-14',models=models),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  lines=['# STEP détaillés et ensembles','', 'Reconstructions colorées enmillimètres ; détails estimés signalés par fichier. Pasdematérielmésuré, pasdeCAOnativefabricant revendiquée.','', '| Modèle | Solides | STEP | Aperçu |','| --- | --- | --- | --- |']
  for m in models:
   p=Path(m['relative_step_path']);rel=Path('..')/Path(*p.parts[1:]);safe_title=m['title'].replace('|',' / ');lines.append(f"| {safe_title} | {m['validation']['solids']} | [{m['file']}]({rel.as_posix()}) | [PNG]({rel.with_suffix('.png').as_posix()}) |")
  lines+=['','[ContrôleFreeCADindépendant](validation-freecad.json), [cataloguestructuré](catalogue.json), [noticeetachat](../README.md).']
  (b/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
  for component in set(m['component_folder'] for m in models if '/' in m['component_folder']):
   ms=[m for m in models if m['component_folder']==component]
   (BASE/component/'3D/README.md').write_text('# Modèles STEP\n\n'+'\n'.join(f"- [{m['file']}]({m['file']}) - [aperçu]({Path(m['file']).with_suffix('.png').name}), [provenance]({Path(m['file']).with_suffix('.json').name})." for m in ms)+'\n\n[Catalogueetvalidation del’ensemble](../../3D/README.md).\n',encoding='utf-8')
 (ROOT/'tools/temp/final-components/models.json').write_text(json.dumps(ALL,ensure_ascii=False,indent=2),encoding='utf-8')
def balance_only():
 f='liaisons-alimentation-surveillance/rallonge-equilibrage-2s';h,pins,b,contact=xh()
 parts=[('prise_male_corps',h,WHITE),*pins,('prise_femelle_corps',b.translate((0,0,-200)),WHITE)]
 sleeve=box(10.8,6.8,5,(0,0,-7.5)).cut(box(8,4.3,5.3,(0,0,-7.65)))
 parts.append(('protection_arriere_male_estimee',sleeve,WHITE))
 for i,x in enumerate([-2.5,0,2.5]):
  parts.append((f'contact_femelle{i+1}',contact.translate((x,-.525,-199.8)),TIN))
  core=cyl(math.sqrt(.326/math.pi),191.65,-194.8,x,-.525)
  sheath=ring(.75,math.sqrt(.326/math.pi),188,-192.5).translate((x,-.525,0))
  assert len(core.Solids())==len(sheath.Solids())==1
  for z in [-194.5,-100,-3.3]:assert core.isInside(cq.Vector(x,-.525,z),1e-6)
  parts.extend([(f'fil{i+1}_ame_estimee22AWG',core,COPPER),(f'fil{i+1}_gaine_estimee',sheath,RED if i==2 else BLACK)])
 add(f,'rallonge-equilibrage-2s-20cm','Équilibrage 2S | cordon 20 cm',parts,['INTERMODEL : 20 cm, trois positions, type XH annoncé.'],
 ['Famille XH reconstruite ; pas de CAO native du cordon. Calibre et OD non publiés : âme équivalente22AWG et gaine1.5 estimées.',
  'Trois âmes et trois gaines continues, entrées orientées vers le câble. Plansde référence séparésde200mm, conventionfournisseuràconfirmer.',
  'Contacts à sertir non déformés, extrémités conductrices insérées dans les terminaisons ; sertissage et isolation réels à contrôler.'],
 params=dict(length_advertised_mm=200,gauge_CAD_assumed_only=22,leads_continuous=True),
 probes=[dict(point=[x,-.525,z],occupied=True) for x in [-2.5,0,2.5] for z in [-194.5,-100,-3.3]],view=(.6,-1,.8))
def bn_only():
 f='liaisons-alimentation-surveillance/fil-18awg';spacing=.0802
 points=[(spacing*(i+j/2),spacing*math.sqrt(3)/2*j) for i in range(-12,13) for j in range(-12,13)]
 points=sorted(points,key=lambda p:p[0]**2+p[1]**2)[:150]
 actual_d=2*(max(math.hypot(x,y) for x,y in points)+.04)
 assert actual_d<=1.13,(actual_d,len(points))
 strands=[(f'brin_{i+1:03}',cyl(.04,30,0,x,y),TIN) for i,(x,y) in enumerate(points)]
 cores=cq.Compound.makeCompound([s for n,s,c in strands]);sheath=cyl(1.15,24,3).cut(cyl(.565,24.2,2.9)).clean()
 # Theinterstitial airsiliconeinterface is notknown. A smoothinner bore uses
 # publishedbundle OD without inventing silicone penetrationintoeverystrand.
 add(f,'bntechgo-18awg-150brins','BNTECHGO 18 AWG | 150 brins',strands+[('silicone_rouge',sheath,RED)],
 ['150 brins Ø0.08 ; faisceauØ1.13 ; gaineØ2.3 ; épaisseurannoncée0.58 ; résistance22.98Ω/km, imageBNTECHGO.'],
 ['Répartition hexagonale de150brinsdroits, pasdetorsadeinconnu. Faisceau CAO tient dansleØ1.13publié.',
  'Échantillon30mm,gaine24mm, pas longueurvendue ; nuanceset arrangement reconstruit, pas de gravureinventée.'],
 params=dict(strands=150,strand_diameter_mm=.08,published_conductor_OD_mm=1.13,reconstructed_strand_envelope_mm=actual_d,outer_diameter_mm=2.3,specimen_mm=30),view=(.75,-1,1.6))
def main():
 sys.stdout.reconfigure(encoding='utf-8');cq.Shape.BoundingBox=optimal
 mode=sys.argv[1] if len(sys.argv)>1 else'all'
 for name,fun in [('jr',jr),('connections',connections),('retention',retention),('disconnect',disconnect),('cordon',balance_only),('brins',bn_only)]:
  if mode==name or (mode=='all' and name not in ['cordon','brins']):fun()
 if mode!='all':
  # Incrementalruns retain othergroups without reexportingthem.
  files=list(BASE.glob('connecteurs-commande/**/3D/*.json'))+list(BASE.glob('liaisons-alimentation-surveillance/**/3D/*.json'))+list(BASE.glob('maintien-batterie/**/3D/*.json'))+list(BASE.glob('coupure-manuelle/**/3D/*.json'))
  found={m['relative_step_path']:m for m in ALL}
  for p in files:
   try:m=json.loads(p.read_text(encoding='utf-8'))
   except Exception:continue
   if 'relative_step_path' in m:found[m['relative_step_path']]=m
  ALL[:]=list(found.values())
 index();print('TOTAL',len(ALL),flush=True)
if __name__=='__main__':main()
