"""Detailed outside reconstructions and untouched native CAD for V3 power.

Existing component CAD is not rebuilt. Battery/charger dimensions are sourced;
local details are explicit estimates. Never treat the CAD as an electrical
netlist or a fabrication model for mains equipment or a battery.
"""
from pathlib import Path
import argparse,json,math,hashlib,sys
import cadquery as cq
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.BRepTools import BRepTools
from OCP.TDF import TDF_LabelSequence
from OCP.XCAFDoc import XCAFDoc_ColorSurf,XCAFDoc_ColorGen
from OCP.Quantity import Quantity_Color
from build_running_gear_step import box,cyl,ring,hexagon,export_model
from prepare_pi5_step import read_xcaf,collect_leaves
from render_step_meshes import render_meshes

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'Composants'
BLACK=(.016,.020,.024)
SOFT_BLACK=(.030,.032,.037)
STEEL=(.48,.50,.53)
GOLD=(.63,.40,.07)
WHITE=(.90,.92,.94)
BLUE=(.015,.060,.42)
CYAN=(.010,.45,.70)
RED=(.68,.009,.006)
YELLOW=(.92,.61,.008)
PARTS=[]


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def lettering(text,size,h=.025,font='Arial'):
    return cq.Workplane('XY').text(text,size,h,font=font,combine=False).val()


def sphere(radius,pos):
    return cq.Solid.makeSphere(radius,cq.Vector(*pos),angleDegrees1=-90)


def cable(points,radius):
    """A single cubic/quintic Bezier sweep with Frenet frames.

    Endpoint/control points define an illustrative cable pose, not delivered
    cable length. Material continuity is probed along the entire centreline.
    """
    vectors=[cq.Vector(*p) for p in points]
    edge=cq.Edge.makeBezier(vectors)
    plane=cq.Plane(origin=vectors[0],normal=edge.tangentAt(0))
    # Two circular arcs avoid a periodic single-edge seam at export. These
    # Beziers used here have no inflection; the Frenet frame is well defined.
    profile=(cq.Workplane(plane).moveTo(radius,0)
        .threePointArc((0,radius),(-radius,0)).threePointArc((0,-radius),(radius,0)).close())
    s=profile.sweep(cq.Workplane('XY').newObject([cq.Wire.assembleEdges([edge])]),isFrenet=True).val()
    assert s.isValid() and len(s.Solids())==1
    theoretical_volume=math.pi*radius**2*edge.Length()
    assert abs(s.Volume(tol=1e-9)/theoretical_volume-1)<1e-4
    for u in np.linspace(0,1,51):assert s.isInside(edge.positionAt(float(u)),1e-6)
    return s,edge.Length()


def model(folder,filename,title,parts,published,estimated,params,view=(.6,-.8,1)):
    return dict(folder=folder,filename=filename,title=title,parts=parts,published=published,
        estimated=estimated,params=params,view=view,design=False,probes=[],source_pages=[])


def xt60_female():
    # Local Z is plug insertion axis, cable end at z=0, open socket at +Z.
    # Dimensions are photo-informed estimates, not an AMASS manufacturing CAD.
    outline=[(-8,-4), (5.8,-4), (8,-1.8), (8,1.8), (5.8,4), (-8,4)]
    s=cq.Workplane('XY').polyline(outline).close().extrude(15.8).val()
    for x in (-3.65,3.65):
        s=s.cut(cyl(2.15,10.1,5.8,x))
    for x in (-7.8,7.8):
        s=s.cut(box(.35,5.7,5,(x,0,2.4)))
    s=s.cut(box(15.4,1.0,.5,(0,3.8,6.0)))
    sockets=[ring(2.08,1.74,9.9,5.85).translate((x,0,0)) for x in (-3.65,3.65)]
    for x,sign in [(-3.65,'-'),(3.65,'+')]:
        t=lettering(sign,2.0,.05).rotate((0,0,0),(1,0,0),90).translate((x,-4.03,4))
        s=s.fuse(t)
    return [('Prise_XT60_corps_estime',s.clean(),YELLOW)]+[(f'Contact_XT60_femelle_{i+1}',q,GOLD) for i,q in enumerate(sockets)]


def battery():
    parts=[];L,W,H=138,47,25
    # Full case envelope exactly nominal. Joint and walls are reconstructions.
    lower=box(L,W,12.3,fillet=2.0)
    upper=box(L,W,12.6,(0,0,12.4),2.0)
    # Cable exits cut from the actual case edge; sleeves enter the openings.
    for y in (-14,-8):
        hole=cq.Solid.makeCylinder(1.85,6,cq.Vector(-72,y,8),cq.Vector(1,0,0))
        lower=lower.cut(hole)
    for z in (14,16.5,19):
        upper=upper.cut(cq.Solid.makeCylinder(.65,6,cq.Vector(-72,7,z),cq.Vector(1,0,0)))
    parts += [('Coque_inferieure_noire_cavite_non_documentee',lower,BLACK),
              ('Coque_superieure_noire',upper,BLACK),
              ('Ligne_joint_estimee',box(137.2,46.2,.09,(0,0,12.305),1.8),SOFT_BLACK)]
    # Narrow ribs and end-cap seam impressions visible in product photographs.
    for x in (-67.5,67.5):
        ridge=box(.7,42.8,24.5,(x,0,.25),.2)
        parts.append((f'Moulure_extremite_{str(x).replace(".","_")}',ridge,SOFT_BLACK))
    # Labels in native 3D: simple bands approximate the blue graphic treatment.
    # No photographic texture is embedded in STEP, and unreadable print omitted.
    label=box(132,42,.045,(0,0,25.01),.7)
    parts.append(('Etiquette_superieure_fond_noir',label,BLACK))
    blue=cq.Workplane('XY').polyline([(-64,-20),(-64,20),(22,20),(30,-10),(48,-20)]).close().extrude(.035).val().translate((0,0,25.06))
    parts.append(('Etiquette_motif_bleu_reconstruit',blue,BLUE))
    for i in range(24):
        x=-64+i*3.7
        # Graphic strokes clipped to the blue area: an estimate of the visible
        # motif, not a calibrated copy of the label's streak texture.
        stripe=cq.Workplane('XY').polyline([(x,-19.3),(x+.45,-19.3),(x+17,19.3),(x+16.45,19.3)]).close().extrude(.008).val().translate((0,0,25.098)).intersect(blue.translate((0,0,.04)))
        if stripe.Solids():parts.append((f'Graphisme_bleu_{i+1:02d}',stripe,CYAN if i%3==0 else (.018,.14,.57)))
    for title,size,x,y,col in [('5200mAh',10,-20,6,WHITE),('80C  7.4V  38.48Wh',3.5,-20,-9,WHITE),('Zeee',8.5,46,3,CYAN),('High Performance Lithium Polymer Battery',2.6,-9,-17,WHITE)]:
        parts.append(('Marquage_'+title.replace(' ','_'),lettering(title,size).translate((x,y,25.13)),col))
    # Front side label repeats the observed nominal values, text fit estimated.
    side=box(131,.035,9.8,(0,-23.52,13.9))
    parts.append(('Etiquette_laterale_fond_bleu',side,BLUE))
    for txt,size,x in [('5200mAh',6.0,-28),('80C 7.4V',3.0,25),('Zeee',5.5,51)]:
        q=lettering(txt,size).rotate((0,0,0),(1,0,0),90).translate((x,-23.56,19.1))
        parts.append(('Marquage_lateral_'+txt.replace(' ','_'),q,WHITE))
    cable_lengths=[];cable_shapes=[]
    # Two silicone leads, retained in a compact U pose akin to the product photo.
    for i,(y,color) in enumerate([(-14,BLACK),(-8,RED)]):
        end_z=11.65 if i==0 else 4.35
        # The XT60's two contacts are stacked in Z in this compact pose. This
        # allows the leads to arrive along the insertion axis without crossing.
        points=[(-67,y,8),(-100,y,end_z),(-95,-48,end_z),(-48,-48,end_z)]
        lead,length=cable(points,1.68);cable_lengths.append(length);cable_shapes.append(lead)
        parts.append((f'Cordon_puissance_{i+1}_continu_pose_estimee',lead,color))
        sleeve=cq.Solid.makeCylinder(1.84,7,cq.Vector(-48,-48,end_z),cq.Vector(1,0,0))
        parts.append((f'Gaine_thermoretractable_{i+1}',sleeve,color))
    # Connector +Z maps to +X; black reaches the marked minus, red the plus.
    pose=lambda q:q.rotate((0,0,0),(0,1,0),90).translate((-43,-48,8))
    parts += [(n,pose(q),c) for n,q,c in xt60_female()]
    # Balance connector is 3 ways for 2S, approximate XH housing and stamped
    # contacts. No circuitry or logical pin order is inferred from the colours.
    for i,color in enumerate([BLACK,YELLOW,RED]):
        z=14+i*2.5
        # Parallel planes separate the compact cable loops; plug row is in Z.
        points=[(-67,7,z),(-84,7,z),(-96,-33,z),(-62,-32,z)]
        lead,length=cable(points,.55);cable_lengths.append(length);cable_shapes.append(lead)
        parts.append((f'Cordon_equilibrage_{i+1}_continu',lead,color))
    connector=box(8.2,5.7,8.2,(-59.5,-32,12.4),.3)
    for i in range(3):
        z=14+i*2.5
        connector=connector.cut(box(5.4,1.1,1.1,(-59.5,-32,z-.55)))
        contact=box(3.8,.70,.70,(-59.5,-32,z-.35)).cut(box(3.9,.38,.40,(-59.5,-32,z-.20)))
        parts.append((f'Contact_equilibrage_{i+1}_estime',contact,STEEL))
    for y in (-35.0,-29.0):
        connector=connector.fuse(box(5.1,.55,5.1,(-59.5,y,14),.1))
    parts.append(('Connecteur_equilibrage_3_voies_XH_estime',connector.clean(),WHITE))
    for i,a in enumerate(cable_shapes):
        for j,b in enumerate(cable_shapes[i+1:],i+1):
            overlap=a.intersect(b).Volume()
            assert overlap<1e-5,(i,j,overlap)
    return model('batterie','batterie-zeee-2s-5200mah-detaillee.step','Zeee 2S 5200mAh | un pack, fils et prises',parts,
        ['Boitier138 x47 x25 mm ±2; 250g annonçés; configuration2S1P, XT60',
         'Photographies fabricant: coque rigide noire, etiquette bleue, deux fils de puissance et trois d equilibrage'],
        ['Fils: diamètre, longueur et pose estimés; pas une longueur livrée garantie',
         'Genres et géométrie des prises, section des fils, empreintes et parois a verifier',
         'Motifs vectoriels/textes/fontes approchés; pas de texture photographique',
         'Coques pleines pour l extérieur; cellules, chimie interne et BMS non représentés; ne pas calculer la masse depuis le volume CAD'],
        dict(body_nominal_mm=[138,47,25],nominal_Wh=38.48,
             cable_pose_lengths_mm_estimated=cable_lengths,all_five_cables_one_closed_solid=True,
             cable_centerline_probes=51,pairwise_cable_intersections_below_mm3=1e-5,
             red_lead_at_marked_plus=True,black_lead_at_marked_minus=True,
             nominal_dimensions_exclude_labels_and_cables=True),view=(.38,-.66,1.2))


def polygon_wire(width,depth,corner,z=0):
    x=width/2;y=depth/2;c=corner
    points=[(-x,-y+c),(-x+c,-y),(x-c,-y),(x,-y+c),(x,y-c),(x-c,y),(-x+c,y),(-x,y-c)]
    return cq.Workplane('XY').polyline(points).close().wire().val().translate((0,0,z))


def charger():
    parts=[];theta=math.radians(4)
    # Upper display plane slopes gently: projected case still ends at z45.
    plane_z=45-49.5*math.sin(theta)
    place=lambda s:s.rotate((0,0,0),(1,0,0),4).translate((0,0,plane_z))
    foot_positions=[(-42,-40),(42,-40),(-42,40),(42,40)]
    base=cq.Solid.extrudeLinear(polygon_wire(118,115,12,2),[],cq.Vector(0,0,2))
    for i,(x,y) in enumerate(foot_positions):
        foot=box(10,9,2.1,(x,y,0),2)
        base=base.cut(foot)
        parts.append((f'Pied_antiderapant_{i+1}_estime',foot,SOFT_BLACK))
    parts.append(('Fond_coque_noire',base,BLACK))
    bottom=polygon_wire(118,115,12,4.12)
    shoulder=polygon_wire(118,115,12,27)
    top=polygon_wire(114,99,11)
    top=place(top)
    body=cq.Solid.makeLoft([bottom,shoulder,top],ruled=True)
    # Hidden cavity only enables the visible ventilation and connectors; wall
    # section is an estimate, not a teardown or a claimed mains PCB layout.
    cavity=box(110,107,20,(0,0,4),7).fuse(box(100,96,13,(0,0,24),7))
    body=body.cut(cavity)
    # Display aperture in the same sloped panel.
    body=body.cut(place(box(79,25,5,(0,16,-2.7),1.7)))
    # Front connector apertures in Y-facing wall.
    for x,w,h,z in [(-31,16,7,12.0),(2,18,11,9.5),(28,8,4.2,12.0)]:
        body=body.cut(box(w,9,h,(x,-55,z),.4))
    # IEC C8 inlet on rear face, no invented switch.
    body=body.cut(box(24.5,9,14.0,(-21,55,9.0),.8))
    # Right side fan opening and the lower vents visible in product photos.
    fan_y=21;fan_z=21
    body=body.cut(cq.Solid.makeCylinder(16.8,10,cq.Vector(51,fan_y,fan_z),cq.Vector(1,0,0)))
    for i in range(5):
        body=body.cut(box(10,31,1.5,(56,-28,9+i*3.3),.35))
    parts.append(('Coque_principale_profilee_cavite_estimee',body.clean(),BLACK))
    joint=cq.Solid.extrudeLinear(polygon_wire(117.4,114.4,11.8,4.025),[],cq.Vector(0,0,.08))
    joint=joint.cut(box(111,108,.2,(0,0,3.98),7))
    parts.append(('Joint_coque',joint,SOFT_BLACK))
    # LCD, printed face surround and four controls.
    panel=place(box(97,76,.06,(0,10,.015),3.0))
    panel=panel.cut(place(box(79.1,25.1,.3,(0,16,-.1),1.7)))
    parts.append(('Facade_imprimee_noire',panel,SOFT_BLACK))
    bezel=box(80.5,26.5,.2,(0,16,-.15),2.1).cut(box(77,23,1,(0,16,-.5),1.7))
    parts.append(('Contour_afficheur_clair',place(bezel),WHITE))
    glass=place(box(76.8,22.8,.35,(0,16,-.44),1.3))
    parts.append(('Fenetre_LCD_bleu',glass,(.010,.18,.31)))
    # A plausible LiPo example; labels do not claim the depicted unit is on.
    for txt,y in [('LiPo BALANCE',20.3),('2.6A 7.4V(2S)',12.5)]:
        q=lettering(txt,3.35,.025,font='Consolas').translate((0,y,-.06))
        parts.append(('LCD_exemple_'+txt.replace(' ','_'),place(q),CYAN))
    for x,name,below in [(-36,'BATT/PROG','Stop'),(-12,'DEC','v STATUS'),(12,'INC','STATUS ^'),(36,'ENTER','Start')]:
        border=box(12,10,.20,(x,-9,.09),1.1).cut(box(10.8,8.8,.4,(x,-9,.02),.8))
        key=box(10.5,8.5,1.25,(x,-9,.10),.8)
        symbol='-' if name=='DEC' else '+' if name=='INC' else '[]'
        parts.append(('Bord_bouton_'+name.replace('/','_'),place(border),WHITE))
        parts.append(('Bouton_'+name.replace('/','_'),place(key),BLACK))
        parts.append(('Symbole_'+name.replace('/','_'),place(lettering(symbol,4).translate((x,-9,1.365))),SOFT_BLACK))
        parts.append(('Texte_'+name.replace('/','_'),place(lettering(name,2.8).translate((x,-.1,.095))),WHITE))
        parts.append(('Texte_bas_'+name.replace('/','_'),place(lettering(below,2.2).translate((x,-17,.095))),WHITE))
    for txt,size,x,y in [('S65',7.5,-33,39),('AC Balance',3.0,-5,40),('Charger/Discharger',2.8,-3,35),('SKYRC',3.6,33,39)]:
        parts.append(('Impression_'+txt.replace('/','_').replace(' ','_'),place(lettering(txt,size).translate((x,y,.10))),WHITE))
    grip=place(box(37,12,1.8,(0,-34,.02),1.8))
    parts.append(('Renfort_avant_superieur_estime',grip,BLACK))
    # Front XH connector 5 positions (2 to 4S), outside/inside details estimated.
    xh=box(15.4,5.0,6.0,(-31,-56.7,12.5),.35)
    xh=xh.cut(box(12.5,4.5,3.8,(-31,-58.5,13.55),.15))
    parts.append(('Port_equilibrage_XH_5voies_estime',xh,WHITE))
    for i in range(5):
        parts.append((f'Contact_XH_{i+1}',box(.60,3.8,.60,(-36+i*2.5,-56.4,15.05)),GOLD))
    # XT60 frontal well. The manufacturer calls it "female"; physical contact
    # gender is reconstructed from photos and must be checked for the cable.
    power=box(17.2,5.8,10.0,(2,-56.6,10),.7)
    power=power.cut(box(14.4,5.8,7.7,(2,-58.7,11.15),.5))
    parts.append(('Port_XT60_noir_geometrie_estimee',power,BLACK))
    for i,x in enumerate((-1.65,5.65)):
        pin=cq.Solid.makeCylinder(1.65,4.7,cq.Vector(x,-58.25,15),cq.Vector(0,1,0))
        for angle in (0,90):
            notch=box(.18,4.3,3.0,(x,-57.7,13.5)).rotate((x,0,15),(x,1,15),angle)
            pin=pin.cut(notch)
        parts.append((f'Contact_XT60_{i+1}_genre_a_verifier',pin.clean(),GOLD))
    temp=box(7.3,5.7,3.5,(28,-56.6,12.35),.35).cut(box(6,4.7,2,(28,-58,13.1)))
    parts.append(('Prise_sonde_temperature',temp,BLACK))
    for i,x in enumerate((26.7,29.3)):
        parts.append((f'Contact_sonde_{i+1}',box(.5,3,.5,(x,-57.2,13.9)),GOLD))
    for txt,x,z in [('4321',-31,22),('+   -',2,24),('T',28,21)]:
        q=lettering(txt,2.8).rotate((0,0,0),(1,0,0),90).translate((x,-57.56,z))
        parts.append(('Marquage_frontal_'+txt.replace(' ','_'),q,SOFT_BLACK))
    # C8 figure-eight cavity and recessed metal pins at the rear.
    inlet=box(24,5.8,13.5,(-21,56.6,9.25),.9)
    for x in (-25.3,-16.7):
        inlet=inlet.cut(cq.Solid.makeCylinder(4.9,4.3,cq.Vector(x,55.0,16),cq.Vector(0,1,0)))
    inlet=inlet.cut(box(8.6,4.3,7.3,(-21,57.0,12.3)))
    parts.append(('Embase_secteur_C8_estimee',inlet,SOFT_BLACK))
    for i,x in enumerate((-25.3,-16.7)):
        pin=cq.Solid.makeCylinder(1.2,3.8,cq.Vector(x,55.2,16),cq.Vector(0,1,0))
        parts.append((f'Contact_secteur_C8_{i+1}',pin,STEEL))
    # Fan guard on right wall; rings, spokes and visible rotor are study detail.
    fan_pose=lambda q:q.rotate((0,0,0),(0,1,0),90).translate((57.0,fan_y,fan_z))
    guard=ring(17.0,15.9,1.0)
    for r in (6.0,10.0,13.1):guard=guard.fuse(ring(r+.35,r-.35,.7,.15))
    for i in range(6):
        spoke=box(31.8,.6,.7,(0,0,.15)).rotate((0,0,0),(0,0,1),i*30)
        guard=guard.fuse(spoke)
    guard=guard.fuse(cyl(4.2,.7,.15)).clean()
    parts.append(('Grille_ventilateur_anneaux_et_rayons_estimes',fan_pose(guard),SOFT_BLACK))
    rotor=cyl(4.1,2,-3)
    blade=cq.Workplane('XY').polyline([(3,-1),(5,-2.4),(13,-4),(15,-2),(12,1.5),(5,1.4)]).close().extrude(.8).val().translate((0,0,-2.8))
    for i in range(5):rotor=rotor.fuse(blade.rotate((0,0,0),(0,0,1),i*72))
    parts.append(('Rotor_ventilateur_visible_pales_estimees',fan_pose(rotor.clean()),BLACK))
    for i in range(2):
        head=cyl(1.25,.5)
        head=head.cut(box(1.8,.45,.3,(0,0,.25)))
        parts.append((f'Tete_vis_grille_{i+1}',fan_pose(head.translate((0,(-1 if i else 1)*14,1.05))),STEEL))
    return model('chargeur-batterie','chargeur-skyrc-s65-detaille.step','SkyRC S65 | boitier, ecran, ports et ventilation',parts,
        ['118 x115 x45 mm, PDF constructeur V2.10 p24; quatre boutons LCD2x16 bleu',
         'Ports, embase secteur, ventilation et renfort visibles dans photos constructeur',
         'Masse annoncée315g; modèle hors véhicule'],
        ['Contours et pente4 deg reconstruits; positions et dimensions locales estimées',
         'Chapes/grilles/rotor, parois et cavité ne résultent pas d un démontage',
         'LCD représente un exemple LiPo2S, non un écran allumé réel ou une programmation du chargeur',
         'Prise XT60 dite femelle dans notice; genre contacts à vérifier avant adapter la batterie',
         'Aucune électronique secteur interne inventée; aucun modèle destiné à fabriquer ou modifier le chargeur',
         '117 x105 x55 relevé chez des distributeurs: variante/erreur inconnue, ne pas en déduire une mesure'],
        dict(case_nominal_mm=[118,115,45],roof_slope_deg_estimated=4,
             fan_diameter_mm_estimated=34,rotor_blades_estimated=5,internal_walls_estimated=True),view=(.68,-.9,1.05))


def mains_cord():
    parts=[]
    lead,length=cable([(0,0,0),(0,90,0),(130,90,0),(130,20,0)],2.3)
    parts.append(('Cordon_double_isolation_trace_estime',lead,BLACK))
    # Generic illustrative C7 connector; not a dimensional IEC certified part.
    c7=box(18,25,11,(0,-11,-5.5),2.2)
    for x in (-4.3,4.3):
        c7=c7.cut(cq.Solid.makeCylinder(2.6,10,cq.Vector(x,-23.6,0),cq.Vector(0,1,0)))
        socket=ring(2.25,1.3,7)
        socket=socket.rotate((0,0,0),(1,0,0),-90).translate((x,-22,0))
        parts.append(('Contact_C7_'+str(x),socket,STEEL))
    for y in (-13,-10,-7):c7=c7.cut(box(14,.65,.45,(0,y,5.10),.1))
    parts.append(('Fiche_C7_reconstruction',c7,BLACK))
    euro=box(31,23,12,(130,9,-6),4)
    for i,x in enumerate((120.5,139.5)):
        pin=cq.Solid.makeCylinder(2,19,cq.Vector(x,-2.5,0),cq.Vector(0,-1,0))
        parts.append((f'Broche_EU_{i+1}_geometrie_estimee',pin,STEEL))
        sleeve=cq.Solid.makeCylinder(2.1,8,cq.Vector(x,-2.5,0),cq.Vector(0,-1,0))
        sleeve=sleeve.cut(cq.Solid.makeCylinder(2,8.02,cq.Vector(x,-2.49,0),cq.Vector(0,-1,0)))
        parts.append((f'Isolation_broche_EU_{i+1}',sleeve,BLACK))
    for i in range(5):
        euro=euro.cut(box(23,.60,.45,(130,2+i*2.4,5.10),.15))
    parts.append(('Fiche_EU_deux_broches_estimee',euro,BLACK))
    return model('chargeur-batterie','cordon-secteur-c7-eu-etude.step','S65 | cordon secteur EU, pose illustrative',parts,
        ['Cordon secteur seul accessoire annoncé, PDF23; deux broches et fiche type8 visibles'],
        ['Toutes dimensions de prise et longueur de câble estimées; pas un plan IEC ni modèle de fabrication',
         'Longueur de la pose compacte ne représente pas la longueur livrée; pays et fiche de l offre à contrôler',
         'Sections, isolation et performances électriques non déduites de la CAO'],
        dict(cable_pose_length_mm_estimated=length,not_actual_delivered_length=True),view=(.1,-.3,1.5))


def native_regulator():
    folder='regulateur-alimentation';out=BASE/folder/'3D';path=out/'pololu-d24v90f5-officiel.step'
    assets=json.loads((BASE/folder/'assets.json').read_text(encoding='utf-8'))['assets']
    record=next(x for x in assets if x['file']=='3D/'+path.name)
    assert sha(path)==record['sha256']
    doc=read_xcaf(path);leaves,whole,ct,roots,ncolors=collect_leaves(doc)
    assert whole.isValid() and len(whole.Solids())==1
    bb=whole.BoundingBox()
    assert abs(bb.xlen-40.64)<.01 and abs(bb.ylen-20.32)<.01
    meshes=[];face_colors=set()
    for name,placed,color,raw in leaves:
        BRepTools.Clean_s(placed.wrapped);BRepMesh_IncrementalMesh(placed.wrapped,.015,False,.12,True)
        for original,f in zip(cq.Shape.cast(raw).Faces(),placed.Faces()):
            fc=color
            for kind in (XCAFDoc_ColorSurf,XCAFDoc_ColorGen):
                col=Quantity_Color()
                if ct.GetColor(original.wrapped,kind,col):
                    fc=(col.Red(),col.Green(),col.Blue());break
            vs,tri=f.tessellate(.015,.12)
            assert tri
            face_colors.add(tuple(round(c,6) for c in fc))
            c=np.array(fc);c=np.where(c<=.0031308,12.92*c,1.055*np.power(c,1/2.4)-.055)
            meshes.append((np.array([v.toTuple() for v in vs]),tri,c))
    previews=[]
    for file,view,title in [('pololu-d24v90f5-dessus.png',(0,0,1),'Pololu D24V90F5 | CAO constructeur - dessus'),
                            ('pololu-d24v90f5-dessous.png',(0,0,-1),'Pololu D24V90F5 | CAO constructeur - dessous'),
                            ('pololu-d24v90f5-isometrique.png',(.6,-.8,1.05),'Pololu D24V90F5 | CAO constructeur detaillee')]:
        p=out/file;render_meshes(p,meshes,view,title,'Pololu - STEP officiel commun D24V60F5 / D24V90F5 - geometrie et couleurs conservees')
        previews.append(dict(file=file,sha256=sha(p)))
    meta=dict(file=path.name,title='Pololu D24V90F5, native shared manufacturer model',generated_on='2026-10-13',
        unit='mm',native_vendor_cad=True,geometry_modified=False,hardware_measured=False,
        family_model='D24V60F5 and D24V90F5, supplied by manufacturer for both items',
        manufacturer_copyright='Pololu Corporation; no separate CAD redistribution licence identified',
        bytes=path.stat().st_size,sha256=sha(path),source_url=record['url'],
        bounds_mm={k:getattr(bb,k) for k in ['xmin','xmax','ymin','ymax','zmin','zmax']},
        validation=dict(valid_after_reimport=True,solids=1,faces=len(whole.Faces()),xcaf_colors=ncolors,
            rendered_face_colors=len(face_colors),identical_to_download_sha256=True),
        previews=previews,published_nominal=['PCB40.64 x20.32 mm; 4 trousØ2.18, centres35.56x15.24'],
        estimates_and_limitations=['Native model is guidance; actual item revision and component markings may differ',
            'No inference of internal copper layers, electrical netlist, performance or measured connector clearances',
            'Factory STEP fuses different materials into one BRep solid; do not calculate physical mass from this one volume'])
    path.with_suffix('.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return dict(folder=folder),meta


def write_outputs(results):
    groups={}
    for item,meta in results:groups.setdefault(item['folder'],[]).append(meta)
    for folder,models in groups.items():
        out=BASE/folder/'3D';out.mkdir(parents=True,exist_ok=True)
        native=folder=='regulateur-alimentation'
        text=['# Modèles 3D — '+folder,'',
            'STEP **officiel Pololu**, inchangé, géométrie et couleurs conservées.' if native else 'STEP colorés, solides nommés, millimètres. Reconstructions extérieures : cotes nominales documentées et détails locaux estimés.',
            '', '| Modèle | STEP | Aperçu |', '| --- | --- | --- |']
        for m in models:
            p=(m['previews'][-1] if 'previews' in m else m['preview'])['file']
            text += [f'| {m["title"]} | [{m["file"]}]({m["file"]}) | [PNG]({p}) |']
        text += ['', '## Fidélité et usage','',
            'Chaque `.json` voisin indique la source, les dimensions, les limites et les contrôles. La CAO ne remplace pas la mesure des exemplaires reçus ni un test électrique. Les traces de câble servent à la présentation ; elles ne donnent pas une longueur de câble livrée.',
            '', 'Le modèle Pololu est fourni par le constructeur pour deux références partageant leur géométrie. La batterie et le chargeur sont reconstruits depuis les photos et plans, sans cellules ni électronique secteur internes fictives. Des inscriptions et motifs sont approchés par des solides vectoriels, sans texture photographique.',
            '', '[Provenance](provenance.json), [contrôles FreeCAD](../../alimentation/3D/validation-freecad.json), [fiche composant](../README.md).','']
        (out/'README.md').write_text('\n'.join(text),encoding='utf-8')
        manifest=dict(generated_on='2026-10-13',generator='tools/build_power_step.py',
            generator_sha256=sha(Path(__file__)),source_assets='../assets.json',
            source_assets_sha256=sha(BASE/folder/'assets.json'),models=models)
        (out/'provenance.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    common=BASE/'alimentation/3D';common.mkdir(parents=True,exist_ok=True)
    catalog=dict(generated_on='2026-10-13',model_count=len(results),component_folders=list(groups),
        models=[dict(folder=i['folder'],**m) for i,m in results])
    (common/'catalogue.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    text=['# Modèles 3D de l’alimentation','',
          '**Trois composants et un cordon secteur accessoire : quatre STEP.** Caméra, moteurs, ESC, Pi, roues et train roulant existants ne sont pas régénérés.',
          '', '[Batterie](../../batterie/3D/README.md), [régulateur Pololu officiel](../../regulateur-alimentation/3D/README.md), [chargeur et cordon](../../chargeur-batterie/3D/README.md).',
          '', '[Vue d’ensemble](apercu-alimentation.png). Chaque modèle a sa propre échelle.',
          '', '[Catalogue](catalogue.json), [validation FreeCAD](validation-freecad.json), [architecture et énergie](../README.md).',
          '', 'Génération : `tools/temp/cad-env/Scripts/python.exe tools/build_power_step.py`. Contrôles : `D:/FreeCAD/bin/python.exe tools/validate_power_freecad.py`. Les STEP sont versionnables et ne sont pas ignorés par Git.', '']
    (common/'README.md').write_text('\n'.join(text),encoding='utf-8')
    gallery=Image.new('RGB',(1600,1400),'white');draw=ImageDraw.Draw(gallery)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',28)
    draw.text((25,16),'V3 | Batterie, alimentation Pi, chargeur et cordon',font=font,fill='#26333f')
    for index,(item,m) in enumerate(results):
        name=(m['previews'][-1] if 'previews' in m else m['preview'])['file']
        im=Image.open(BASE/item['folder']/'3D'/name).convert('RGB');im.thumbnail((780,640))
        x=(index%2)*800;y=60+(index//2)*665
        gallery.paste(im,(x+(800-im.width)//2,y))
    gallery.save(common/'apercu-alimentation.png')


def main():
    sys.stdout.reconfigure(encoding='utf-8');results=[]
    for build in [battery,charger,mains_cord]:
        item=build()
        if build==battery:
            item['source_pages']=['Zeee manufacturer product page and photographs: ../assets.json']
            coordinates='Boitier centre en X/Y; longueur X, largeur Y; fond z=0; fils dans une pose estimee'
        elif build==charger:
            item['source_pages']=['SkyRC S65 manual V2.10, PDF pages 4, 23 and 24; manufacturer photographs: ../assets.json']
            coordinates='Boitier centre en X/Y; largeur X, profondeur Y; bas des pieds z=0'
        else:
            item['source_pages']=['SkyRC S65 manual V2.10, PDF page 23; manufacturer cord photograph: ../assets.json']
            coordinates='Pose illustrative dans le plan XY; centreline du cable z=0'
        meta=export_model(item)
        meta['coordinate_system']=coordinates
        meta['generator']='tools/build_power_step.py';meta['generator_sha256']=sha(Path(__file__))
        p=BASE/item['folder']/'3D'/Path(meta['file']).with_suffix('.json')
        p.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        results.append((item,meta))
    results.insert(1,native_regulator())
    write_outputs(results)
    print('DONE',len(results),'power STEP models',flush=True)


if __name__=='__main__':main()
