"""P1 speed-sensor mounts and captive-magnet encoder rotor, no final chassis.

Local X is output-shaft axis; rotor frontX0 faces sensor on negativeX.
Station Z0 is a mounting plane, NOT ground level. Nominal shaft height24.
"""
from pathlib import Path
import csv,hashlib,json,math,sys
import cadquery as cq
import pymupdf
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate,Spacer,PageBreak,Table
from reportlab.graphics.shapes import Drawing,Line,Rect,String,Circle
from build_running_gear_step import box,cyl,export_model
from build_heatsink_pdf import p as base_p,table as base_table,banner as base_banner,BLUE,GREY
from monitor_typography import clean

ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Composants/supports-capteurs-vitesse';OUT=B/'3D'
H=24;R=12;GAP=2.5;CZ=H+R
BLUEPL=(.035,.15,.23);ORANGE=(.75,.19,.025);GREYMET=(.48,.51,.54);BLACK=(.015,.018,.022)

def p(t,*a,**kw):return base_p(clean(t),*a,**kw)
def table(rows,*a,**kw):return base_table([[clean(c) for c in r] for r in rows],*a,**kw)
def banner(t,*a,**kw):return base_banner(clean(t),*a,**kw)
def write(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t.strip()+'\n',encoding='utf-8')
def dump(p,o):write(p,json.dumps(o,ensure_ascii=False,indent=2))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def optimal(self,tolerance=None):
    b=Bnd_Box();BRepBndLib.AddOptimal_s(self.wrapped,b,False,False);return cq.BoundBox(b)
cq.Shape.BoundingBox=optimal

def base_profile():
    w=cq.Workplane('XY').rect(40,30)
    for y in [-10,10]:w=w.center(-4,y).slot2D(20,3.5).center(4,-y)
    return w

def bracket():
    foot=base_profile().extrude(3).val().translate((-25,0,0))
    w=cq.Workplane('YZ',origin=(-13,0,27.5)).rect(28,49)
    for y in [-10,10]:w=w.center(y,3.5).slot2D(16,3.5,90).center(-y,-3.5)
    upright=w.extrude(3).val()
    # Fork opening clears the rotating shaft throughout H18..30, incl. play.
    upright=upright.cut(box(5,10,32,(-11.5,0,2)))
    s=foot.fuse(upright)
    for y in [-13,10]:
        rib=cq.Workplane('XZ',origin=(0,y+3,0)).polyline([(-25,3),(-10,3),(-10,20)]).close().extrude(3).val()
        s=s.fuse(rib)
    return s.clean()

def head_parts():
    back=-10;front=-GAP
    head=box(7.5,26,14,(-6.25,0,CZ-7))
    # Body clearance covers TI maximum envelope4.1 x1.62 x3.25.
    head=head.cut(box(2.0,4.4,3.6,(-3.4,0,CZ-1.8)))
    # Narrow individual terminal passages preserve a supporting ledge.
    for y in [-1.27,0,1.27]:head=head.cut(box(1.5,.8,1.0,(-2.9,y,CZ-2.7)))
    # Local decoupling and insulated solder joints: open-bottom recess.
    head=head.cut(box(3.4,5,5.0,(-4.15,0,CZ-7.2)))
    for y in [-10,10]:head=head.cut(cyl(1.25,5.6,CZ-5,back-.1,y,axis=(1,0,0)))
    for y in [-9,9]:head=head.cut(cyl(.8,5.8,CZ+4,front+.1,y,axis=(-1,0,0)))
    cap=box(1.5,26,14,(-1.75,0,CZ-7))
    cap=cap.cut(box(2,3,2,(-1.7,0,CZ-1)))
    cap=cap.cut(box(2,5,4.9,(-1.7,0,CZ-7.1)))
    for y in [-9,9]:
        cap=cap.cut(cyl(1.15,1.7,CZ+4,-2.6,y,axis=(1,0,0)))
        # Countersink for provisional M2 flat-head screw, below outer face.
        cone=cq.Solid.makeCone(1.15,2.05,.9,cq.Vector(-1.9,y,CZ+4),cq.Vector(1,0,0))
        cap=cap.cut(cone)
    return head.clean(),cap.clean()

def rotor():
    s=cyl(16,8,H,0,0,axis=(1,0,0)).cut(cyl(2.55,8.2,H,-.1,0,axis=(1,0,0)))
    # Load both magnets from the shaft bore via a fully internal channel.
    # Shaft blocks the only large entrance after installation; no glued lid.
    s=s.cut(box(2.3,3.3,24,(1.75,0,H-12)))
    for sign in [-1,1]:
        s=s.cut(cyl(1.65,2.3,H+sign*R,.6,0,axis=(1,0,0)))
        s=s.cut(cyl(1.25,14,H,5,sign*2.3,axis=(0,sign,0)))
        s=s.cut(cyl(2.85,6,H,5,sign*10.5,axis=(0,sign,0)))
    return s.clean()

def hall():
    s=cq.Workplane('XY').polyline([(-2,-.76),(2,-.76),(2,0),(1.24,.76),(-1.24,.76),(-2,0)]).close().extrude(3.15).val()
    t=(-GAP-.76,0,CZ-1.575)
    body=s.rotate((0,0,0),(0,0,1),90).translate(t)
    parts=[('DRV5033_corps_nominal_face_plusX',body,BLACK)]
    for x,name in [(-1.27,'VCC'),(0,'GND'),(1.27,'OUT')]:
        lead=box(.415,.435,6,(x,-.2175,-6)).rotate((0,0,0),(0,0,1),90).translate(t)
        parts.append(('DRV5033_'+name+'_patte_raccourcie6',lead,GREYMET))
    return parts

def moving_parts():
    parts=[('P04_Rotor_capteur_faceX0',rotor(),ORANGE)]
    for sign in [-1,1]:
        parts.append(('Aimant_3x2_'+str(sign),cyl(1.5,2,H+sign*R,.6,0,axis=(1,0,0)),GREYMET))
        shank=cyl(1.48,8,H,5,sign*2.5,axis=(0,sign,0))
        head=cyl(2.75,3,H,5,sign*10.5,axis=(0,sign,0))
        parts.append(('Vis_blocage_M3x8_nominale_'+str(sign),shank.fuse(head),GREYMET))
    return parts

def station():
    hd,cap=head_parts()
    return [('P01_Equerre_fourche',bracket(),BLUEPL),('P02_Porte_capteur',hd,BLUEPL),('P03_Retenue_capteur',cap,BLUEPL),*hall(),*moving_parts(),
      ('Axe5_gabarit_non_fourni',cyl(2.5,38,H,-18,0,axis=(1,0,0)),GREYMET)]

def validate_geometry(parts):
    fixed=parts[:3]+hall();rows=[]
    for h in [18,24,30]:
        for gap in [2.5,3.5]:
            # Full cylinder is a conservative swept volume of the entire rotor.
            swept=cyl(16,8,h,0,0,axis=(1,0,0));shaft=cyl(2.5,38,h,-18,0,axis=(1,0,0))
            posed=[fixed[0]]+[(n,s.translate((-(gap-GAP),0,h-H)),c) for n,s,c in fixed[1:]]
            rv=sum(s.intersect(swept).Volume() for _,s,_ in posed)
            av=sum(s.intersect(shaft).Volume() for _,s,_ in posed)
            assert rv<1e-6 and av<1e-6,(h,gap,rv,av)
            rows.append(dict(axle_height=h,sensor_flat_face_gap=gap,rotor_swept_overlap_mm3=rv,shaft_overlap_mm3=av))
    hd,cap=head_parts()
    for n,s,_ in hall():assert s.intersect(hd).Volume()<1e-6 and s.intersect(cap).Volume()<1e-6,n
    # Three supplier magnet sizes fit and can be loaded through the radial path.
    rr=rotor();magrows=[]
    for dia,depth in [(2.9,1.9),(3,2),(3.1,2.1)]:
        for radius in [0,3,6,9,12]:
            m=cyl(dia/2,depth,H+radius,.65,0,axis=(1,0,0));v=m.intersect(rr).Volume()
            assert v<1e-6,(dia,depth,radius,v)
        magrows.append(dict(diameter=dia,thickness=depth,radial_loading_positions=[0,3,6,9,12],all_fit=True))
    # Internal pocket joins bore but not clamp drill: separation .85 mm nominal.
    omega=40/3.6/(.063/2)
    return dict(hardware_tested=False,continuous_rotation_swept_envelope_checked=True,clearance_cases=rows,magnet_loading=magrows,
      magnet_front_wall_mm=.6,magnet_radial_outer_wall_min_mm=16-13.65,magnet_channel_to_clamp_drill_min_mm=5-1.25-2.9,
      bore_diameter_mm=5.1,assumed_shaft_diameter_mm=5,diametral_bore_clearance_mm=.1,
      retention='Magnets load from bore; full-length shaft blocks entry after mounting. Adhesive locates magnets, not sole ejection barrier. Rotor axial restraint and clamp endurance remain to qualify.',
      nominal_wheel_rpm=omega*60/(2*math.pi),pulses_per_revolution=2,frequency_at40_hz=2*omega/(2*math.pi),magnet_force_at40_N=.00011*omega**2*.012,
      magnetic_detection_validated=False,structural_strength_validated=False,shaft_height_is_relative_to_mounting_plane_not_ground=True)

def save(name,title,parts,params):
    m=export_model(dict(folder='supports-capteurs-vitesse',filename=name,title=title,parts=parts,design=True,
      published=['TI LPG body maximum4.1x1.62x3.25mm; magnet3x2mm +/-0.1 from existing primary-source dossier.'],
      estimated=['Project prototype dimensions, not manufactured or tested.', 'Hall active point height, axle and magnet alignment require physical adjustment. Pins shown shortened to6mm; solder and cable routes absent.',
       'Provisional screw envelopes without thread geometry. No final chassis, gear, bearing or wheel assembly is claimed.'],
      params=params,view=(-1.2,-1,.9),probes=[],source_pages=['../capteurs-vitesse/README.md; ../capteurs-vitesse/notices/TI-DRV5033-original.pdf; ../capteurs-vitesse/aimants-s-03-02-n/cotes.md']))
    m.update(generated_on='2026-10-15',coordinate_system='X shaft axis; rotor frontX0, backX8; sensor marked face on negativeX looking+X. Mounting planeZ0, nominal shaftZ24, magnet orbitR12.',hardware_tested=False)
    dump(OUT/Path(name).with_suffix('.json'),m);return m

def stl(s,name,axis=(0,1,0),angle=0):
    s=s.rotate((0,0,0),axis,angle);bb=s.BoundingBox();s=s.translate((-(bb.xmin+bb.xmax)/2,-(bb.ymin+bb.ymax)/2,-bb.zmin))
    assert abs(s.BoundingBox().zmin)<1e-6
    cq.exporters.export(s,str(OUT/(name+'.stl')),tolerance=.035,angularTolerance=.10)

def diagram():
    d=Drawing(174*mm,111*mm)
    def txt(x,y,t,size=8):d.add(String(x*mm,y*mm,t,fontName='HV3',fontSize=size,fillColor=BLUE))
    def line(x,y,a,b):d.add(Line(x*mm,y*mm,a*mm,b*mm,strokeColor=BLUE,strokeWidth=.7))
    # Front view of rotor, two magnets180deg apart.
    d.add(Circle(27*mm,74*mm,16*mm,strokeColor=BLUE,fillColor=colors.HexColor('#f8e2d3')))
    d.add(Circle(27*mm,74*mm,2.55*mm,strokeColor=BLUE,fillColor=colors.white))
    for zz in [62,86]:d.add(Circle(27*mm,zz*mm,1.5*mm,strokeColor=BLUE,fillColor=colors.HexColor('#bac5ce')))
    line(27,74,27,86);txt(30,79,'R12');txt(7,96,'Rotor : diametre32 x8');txt(5,51,'Alesage5,1 ; deux aimants3 x2',7.4)
    # True schematic axial section, enlarged, not machining scale.
    d.add(Rect(87*mm,63*mm,60*mm,25*mm,strokeColor=BLUE,fillColor=colors.HexColor('#f8e2d3')))
    d.add(Rect(91.5*mm,70*mm,15*mm,11*mm,strokeColor=BLUE,fillColor=colors.HexColor('#bac5ce')))
    d.add(Rect(68*mm,67*mm,5*mm,14*mm,strokeColor=BLUE,fillColor=colors.HexColor('#26343c')))
    line(73,60,87,60);txt(72,55,'Face Hall -> rotor :2,5 initial',7)
    txt(84,93,'Coupe axiale de principe (sans echelle)');txt(89,43,'Paroi avant0,6 ; canal interne2,3');txt(89,37,'Chargement par alesage AVANT axe',7.5)
    # Foot mounting template.
    d.add(Rect(5*mm,6*mm,40*mm,30*mm,strokeColor=BLUE,fillColor=colors.HexColor('#e9f1f6')))
    for y in [11,31]:d.add(Rect(11*mm,(y-1.75)*mm,20*mm,3.5*mm,rx=1.75*mm,ry=1.75*mm,strokeColor=BLUE,fillColor=colors.white))
    txt(50,27,'Pied40 x30 x3 ; fixation provisoire');txt(50,21,'2 lumieres20 x3,5, entraxe20');txt(50,15,'Centres depuis coin : (16;5)/(16;25)');txt(50,9,'Axe reglable18-30 au-dessus du plan de pose',7.5)
    from reportlab.graphics import renderSVG
    renderSVG.drawToFile(d,str(B/'plans/cotes-supports-vitesse-p1.svg'))
    return d

def docs(meta,check):
    write(B/'README.md','''# Supports réglables des capteurs de vitesse - P1

Deux stations identiques, une par roue arrière : **équerre à fourche, porte-capteur coulissant, petite retenue frontale, rotor porte-aimants**. Quatre pièces à fabriquer par côté, huit pour le véhicule. Modèles de test démontables ; aucun châssis définitif ni visserie finale.

[Notice et plan coté PDF](notices/notice-supports-capteurs-vitesse-p1.pdf) · [STEP, STL et aperçus](3D/README.md) · [Cotes](cotes.json) · [Nomenclature](nomenclature.csv) · [Plans](plans/README.md) · [Contrôles géométriques](verification/conception.json).

Le rotor se monte sur **l'axe de sortie roueØ5**, à1 tour de rotor par tour de roue, pas sur un arbre intermédiaire. Réserver **11 mm de longueur d'axe** autour du rotor8 mm, ainsi qu'un dégagement radialØ32. L'empilage réel avec roulements, couronnes et moyeu sera défini avec le châssis ; aucun arbre existant n'est déclaré compatible sans ce contrôle.

Deux aimantsØ3 x2 à180° sont chargés dans les canaux internes par l'alésage, avant montage sur l'axe. Une fois l'axe inséré sur toute la largeur, il bloque l'entrée des aimants. Les parois du rotor les entourent, dont0,6 mm côté capteur. Une petite quantité de colle compatible peut les immobiliser au rayon12, mais elle n'est pas la seule barrière contre l'éjection. Deux vis M3x8 opposées bloquent le rotor sur l'axe ; taraudages et endurance à vérifier, puis retenue axiale définitive avec le train roulant.

Face plane du Hall tournée vers le rotor. Réglage initial **2,5 mm entre face plane Hall et face extérieure rotor**, soit environ3,1 mm jusqu'à la face de l'aimant enfouie. La retenue de1,5 mm avance devant les bords du capteur : son jeu mécanique initial est1 mm. Ce réglage est un point de départ, **pas une portée de détection garantie**. La fourche dégage l'axe ; deux lumières verticales adaptent sa hauteur de18 à30 mm **par rapport au plan de fixation**, pas au sol. La hauteur nominale24 mm ne fixe donc pas la hauteur du futur châssis.

Le boîtier Hall est logé sans serrer ses pattes. Une poche au-dessous réserve le découplage100 nF et les soudures isolées. Les pattes sont représentées raccourcies à6 mm pour dégager l'axe ; décider leur longueur et leur formage après présentation réelle. Rappels et GPIO restent ceux du [dossier capteurs](../capteurs-vitesse/integration.md), aucun changement électrique.

Essayer d'abord à la main : absence de contact sur360°, rotor bloqué, capteur retenu, fils éloignés des pièces tournantes. Obtenir **deux fronts descendants et un retour haut entre aimants** par tour, puis contrôler progressivement sous écran à vitesse croissante. L'acier de l'axe, les vis et les moteurs peuvent modifier le champ. La rétention, l'équilibrage, le glissement et la détection à40 km/h ne sont pas qualifiés par la CAO.

PETG proposé pour prototypage ; rotor dense, contrôler canaux et parois avant usage. Pas de support d'impression enfermé dans les canaux. Les STEP permettent une adaptation de fabrication, mais le rotor monobloc à canaux internes n'est pas directement une pièce à fraiser en une seule prise. Prix de matière et quincaillerie à chiffrer, aucun panier d'achat ni achat effectué.

Sources : [TI DRV5033](https://www.ti.com/lit/ds/symlink/drv5033.pdf), [supermagnete S-03-02-N](https://www.supermagnete.fr/aimants-disques-neodyme/disque-magnetique-3mm-2mm_S-03-02-N), notices originales conservées dans [capteurs-vitesse](../capteurs-vitesse/notices/README.md). Les pièces électroniques, les aimants, la transmission et leurs modèles d'origine sont conservés.
''')
    write(B/'3D/README.md','''# Modèles P1 - supports de vitesse

- [Une station assemblée](station-capteur-vitesse-p1.step), [aperçu](station-capteur-vitesse-p1.png).
- [Paire gauche/droite](paire-supports-vitesse-p1.step), [aperçu](paire-supports-vitesse-p1.png). Les stations sont espacées de100 mm pour présentation, **pas pour définir la voie du véhicule**. La gauche est tournée, pas un miroir des broches.
- [Pièces à fabriquer](pieces-supports-vitesse-p1.step), quatre solides séparés en position d'étude : équerre, porte-capteur, retenue, rotor.
- STL individuels : [équerre](P01-equerre.stl), [porte-capteur](P02-porte-capteur.stl), [retenue](P03-retenue.stl), [rotor](P04-rotor.stl). Chaque STL est posé sur son plan d'impression ; prévoir le traitement des ponts de la fourche, sans enfermer de supports dans le rotor.

Repère local : X axe roue ; rotorX0..8, face capteurX0. Capteur côtéX négatif ; sa face marquée regarde+X. Z0 plan de pose, axeZ24 nominal, capteur centréZ36. Le boîtier est reconstruit à partir du plan TI ; pattes raccourcies6 mm, petits rayons et couleurs indicatifs. AimantsØ3 x2 nominaux. Axe et vis de blocage sont des gabarits, sans filetage. Soudures, capteur actif interne, câblage et condensateur réel ne sont pas représentés ; poche réservée au découplage.

[Provenance](provenance.json), [contrôle FreeCAD](validation-freecad.json) et [contrôles de conception](../verification/conception.json). Les volumes de rotation continus et les passages d'aimants sont vérifiés ; champ magnétique et résistance matérielle non testés.
''')
    write(B/'plans/README.md','''# Plans P1

[Plan coté SVG](cotes-supports-vitesse-p1.svg), [gabarit de fixation DXF](gabarit-fixation-40x30.dxf). Le DXF est le pied40 x30 et ses deux lumières20 x3,5, en millimètres, sans compensation d'outil. Origine du DXF au centre du pied ; centres des lumières(-4;±10). Depuis le coin inférieur gauche : (16;5)/(16;25).

Le DXF sert à préparer une fixation provisoire, pas à découper une équerre complète ou un châssis déjà défini. Pour les volumes utiliser les STEP/STL. Pattes électroniques, longueur d'axe, jeu au palier, dégagement axial et fixation au véhicule restent à vérifier dans l'assemblage de châssis.
''')
    rows=[['P01','Équerre fourche',2,'Pied40x30x3 ; hauteur52 ; passages axe et réglages M3'],['P02','Porte-capteur coulissant',2,'Cavité4,4x1,9x3,6 ; poche découplage'],['P03','Retenue frontale',2,'Épaisseur1,5 ; fenêtre sensible3x2 ; vis fraisées'],['P04','Rotor porte-aimants',2,'Ø32x8, alésage5,1 ; canaux internes, deux aimants par rotor'],['E01','DRV5033AJQLPG',2,'Déjà sélectionné, pas un nouvel achat en double'],['E02','S-03-02-N Ø3x2',4,'Déjà sélectionné'],['F01','M3x8 pour blocage rotor',4,'Deux par rotor ; têtesØ5,5/h3 nominales ; tarauder pilotes2,5'],['F02','M3x8 +rondelles pour tête coulissante',4,'Montage par arrière ; engagement à contrôler, pas de vis traversante face rotor'],['F03','M2x6 tête fraisée',4,'Deux par retenue ; tarauder pilotes1,6 ; têtes affleurantes'],['F04','Fixations pied M3',4,'Longueur et écrous après châssis, non modélisés'],['C01','Colle compatible +isolants et maintien câble',1,'À définir au montage ; colle ne remplace pas les parois captives']]
    with (B/'nomenclature.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f,delimiter=';');w.writerow(['Repère','Désignation','Quantité véhicule','Note']);w.writerows(rows)
    dump(B/'cotes.json',dict(revision='P1',units='mm',custom_parts_per_station=4,stations=2,shaft_height_nominal=H,shaft_height_range=[18,30],height_datum='Local mounting plane, not ground',foot=[40,30,3],tower_height=52,vertical_slots=[16,3.5],rotor=[32,8],shaft_bore=5.1,shaft_nominal=5,shaft_axial_reservation=11,magnet_orbit=12,magnet_pockets_diameter=3.3,internal_channel=[3.3,2.3],magnet_front_wall=.6,sensor_gap_initial=GAP,cover_thickness=1.5,cover_mechanical_clearance_initial=1.0,sensor_body_pocket=[4.4,1.9,3.6],sensor_leads_trimmed_nominal=6,final_chassis_defined=False))
    dump(B/'verification/conception.json',check)
    dump(OUT/'provenance.json',dict(revision='P1',models=meta,hardware_tested=False,source_sha256={str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in [ROOT/'Composants/capteurs-vitesse/capteur-hall-drv5033/3D/drv5033ajqlpg-detaille.step',ROOT/'Composants/capteurs-vitesse/aimants-s-03-02-n/3D/aimant-s-03-02-n-detaille.step']}))

def pdf():
    from build_monitor_pdf import picture
    out=B/'notices/notice-supports-capteurs-vitesse-p1.pdf';out.parent.mkdir(parents=True,exist_ok=True)
    tmp=ROOT/'tools/temp/speed-mount/pdf';tmp.mkdir(parents=True,exist_ok=True)
    check=json.loads((B/'verification/conception.json').read_text(encoding='utf-8'))
    def footer(c,d):
        c.setFont('HV3',7.4);c.setFillColor(GREY);c.drawString(18*mm,12*mm,'Drone V3 | Supports de vitesse P1 | 15 octobre2026 | Prototype non teste');c.drawRightString(192*mm,12*mm,str(d.page))
    story=[p('Supports des capteurs<br/>de vitesse arrière','title'),p('P1 - deux stations réglables, deux rotors à aimants captifs'),
      banner('<b>Quatre pièces à fabriquer par côté.</b> Équerre, tête coulissante, retenue et rotor. Capteurs et quatre aimants déjà sélectionnés ; pas de nouvelle carte électronique.'),Spacer(1,3*mm),
      picture(OUT/'paire-supports-vitesse-p1.png',165,105),Spacer(1,3*mm),
      table([['Interface','Choix de conception'],['Axe','Sortie de roueØ5 ; réserver11 mm axial autour du rotor8 mm. Ne pas placer sur un arbre intermédiaire.'],['Rotor','Ø32 x8 ; alésage5,1 ; deux aimantsØ3 x2 à180°, rayon nominal12'],['Réglage','Hauteur d’axe18-30 au-dessus du plan de pose,24 nominal. Pied40 x30, deux lumières20 x3,5 pour l’approche axiale.'],['Face capteur / rotor','2,5 mm de départ,1 mm de jeu à la retenue. Aimant sous paroi0,6 : distance face Hall/aimant environ3,1 mm. Détection à tester.']],[46,128]),
      p('La juxtaposition des deux stations dans la CAO ne définit pas la voie du robot. Le châssis intégrera ensuite ces réservations avec couronnes, roulements, moyeux et roues.','small'),PageBreak(),
      p('Cotes, logement et aimants captifs','title'),diagram(),Spacer(1,4*mm),
      table([['Élément','Cote / contrôle'],['Capteur','Cavité4,4 x1,9 x3,6 pour boîtier TI max4,1 x1,62 x3,25 ; face plane vers le rotor, fenêtre3 x2. Pas d’effort de serrage sur les pattes.'],['Magnets / canal','Ø3±0,1, épaisseur2±0,1 ; pochesØ3,3, canal axial2,3 xlargeur3,3. Chargement par l’alésage avant l’axe.'],['Retenue rotor','Front fermé0,6 et bord radial minimal2,35 ; axeØ5 ferme l’entrée d’assemblage. La colle localise les aimants mais n’est pas seule à les retenir.'],['Blocage sur axe','Deux M3x8 opposées ; pilotes2,5 à tarauder. Serrer et contrôler sans écraser ou fissurer le plastique ; retenue axiale finale avec le train roulant.'],['Fabrication','STL PETG proposés, rotor dense et canaux propres ; pas de supports enfermés. STEP éditables, DXF de fixation millimétrique sans G-code.']],[45,129]),
      p('Les modèles ne qualifient pas les tolérances d’impression ou la résistance du PETG. Contrôler le boîtier, les canaux, l’épaisseur des parois et le serrage sur les pièces réelles. Ne pas percer, usiner ou chauffer les aimants.','small'),PageBreak(),
      p('Montage et essais progressifs','title'),
      table([['Étape','Contrôle'],['1 - Rotor','Charger les aimants par l’alésage, même face polaire orientée vers le capteur, les placer au rayon12. Contrôler leur position et la colle compatible, puis insérer l’axe sur toute la largeur8 mm.'],['2 - Serrage','Bloquer les deux vis opposées du rotor. Vérifier qu’il ne glisse ni en rotation ni axialement ; le châssis devra prévoir sa retenue axiale et l’espace entre paliers/engrenages.'],['3 - Capteur','Repérer LPG1=VCC,2=GND,3=OUT avec le plan TI. Présenter le corps ; retailler et former les pattes sans effort au ras du boîtier. Poche pour100 nF et jonctions isolées au-dessous.'],['4 - Réglage','Monter la retenue avec têtes fraisées affleurantes. Approcher par les lumières de pied et régler la hauteur par les deux lumières verticales ; face Hall à2,5 mm du rotor pour commencer. Vérifier360° à la main.'],['5 - Mesure','3,3 V du Pi, rappel10k côté Pi et100 nF local, câblage existant inchangé. Deux fronts descendants et retour haut entre aimants par tour. Ajuster selon signaux réels et jeux mécaniques.']],[38,136]),Spacer(1,3*mm),
      p(f"À40 km/h etØ63 nominal : <b>{check['nominal_wheel_rpm']:.0f} tr/min</b>, <b>{check['frequency_at40_hz']:.2f} Hz</b> par voie. Effort centrifuge illustratif par aimant0,11 g au rayon12 : <b>{check['magnet_force_at40_N']:.3f} N</b>. Ce calcul n’est pas un essai de rétention."),
      banner('Le volume balayé sur360° et le passage d’axe sont sans collision dans les six configurations contrôlées. <b>Champ magnétique, équilibre, tenue des vis et fonctionnement à40 km/h restent à tester</b>, progressivement et sous protection. L’axe acier et les moteurs peuvent modifier le champ.'),
      p('Un capteur par roue ne donne pas le sens de marche et ne constitue pas un arrêt de sécurité. Aucun câblage déployé, achat ni essai matériel effectué. Fixations au châssis et visserie finale restent dans les étapes suivantes.','small'),
      p('Sources : TI DRV5033, schéma LPG et plan mécanique ; supermagnete S-03-02-N. Notices originales et choix électriques conservés dans le dossier capteurs-vitesse. Recherche des sources primaires revue le15 octobre2026. Prix de matière et quincaillerie à chiffrer.','small')]
    for f in story:
        if isinstance(f,Table):f.spaceAfter=3*mm
    SimpleDocTemplate(str(out),pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=18*mm,bottomMargin=23*mm,title='Drone V3 - Supports des capteurs de vitesse P1').build(story,onFirstPage=footer,onLaterPages=footer)
    d=pymupdf.open(out);assert len(d)==3,len(d)
    renders=[]
    for i,page in enumerate(d):
        q=tmp/f'page-{i+1}.png';page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(q);renders.append(str(q.relative_to(ROOT)))
    dump(out.with_suffix('.json'),dict(pages=3,renders=renders,sha256=sha(out),visual_review_completed=False))

def indices():
    p=ROOT/'Composants/README.md';t=p.read_text(encoding='utf-8')
    row='| [Supports des capteurs de vitesse](supports-capteurs-vitesse/README.md) | P1 : deux stations et deux rotors à aimants captifs | À fabriquer | STEP/STL, plan coté et notice ; fixation finale au châssis à venir |'
    if row not in t:t=t.replace('| [Support caméra provisoire]',row+'\n| [Support caméra provisoire]',1)
    write(p,t)
    p=ROOT/'PLAN-CONCEPTION.md';t=p.read_text(encoding='utf-8').replace('3. Supports des capteurs de vitesse.','3. [Supports des capteurs de vitesse P1](Composants/supports-capteurs-vitesse/README.md). Deux stations réglables et rotors captifs conçus ; STEP/STL, plan et notice, essais matériels restants.')
    write(p,t)
    p=ROOT/'Composants/capteurs-vitesse/integration.md';t=p.read_text(encoding='utf-8')
    notice='> **Support mécanique P1 désormais conçu :** [stations réglables et rotors captifs](../supports-capteurs-vitesse/README.md). La proposition ci-dessous reste l’historique électrique ; pour les distances et la rétention mécanique, suivre le dossier P1. Le réglage initial tient compte de la paroi et de la retenue du capteur ; détection et tenue toujours à tester.\n\n'
    if notice not in t:write(p,notice+t)

def main():
    sys.stdout.reconfigure(encoding='utf-8');OUT.mkdir(parents=True,exist_ok=True);(B/'plans').mkdir(exist_ok=True)
    if '--docs-only' in sys.argv:pdf();indices();return
    parts=station();check=validate_geometry(parts)
    a=save('station-capteur-vitesse-p1.step','P1 | capteur reglable et rotor captif',parts,dict(axle_height=H,gap=GAP,shaft_reservation_mm=11))
    pair=[]
    for side in ['G','D']:
        for n,s,c in parts:
            ss=s.rotate((0,0,0),(0,0,1),180).translate((-50,0,0)) if side=='G' else s.translate((50,0,0))
            pair.append((side+'_'+n,ss,c))
    b=save('paire-supports-vitesse-p1.step','Deux stations P1 | presentation, pas voie du chassis',pair,dict(presentation_center_spacing_mm=100,defines_vehicle_track=False))
    hd,cap=head_parts();custom=[parts[0],('P02_Porte_capteur',hd,BLUEPL),('P03_Retenue',cap,BLUEPL),('P04_Rotor',rotor(),ORANGE)]
    c=save('pieces-supports-vitesse-p1.step','P1 | quatre pieces a fabriquer par roue',custom,dict(custom_parts_per_side=4,quantity_each_for_vehicle=2))
    for n,s,angle in [('P01-equerre',bracket(),0),('P02-porte-capteur',hd,-90),('P03-retenue',cap,90),('P04-rotor',rotor(),-90)]:stl(s,n,angle=angle)
    cq.exporters.export(base_profile().extrude(1).faces('>Z'),str(B/'plans/gabarit-fixation-40x30.dxf'),exportType='DXF')
    docs([a,b,c],check);pdf();indices()
    print('P1 speed mounts built:3STEP,4STL,DXF,3-page PDF; six swept-envelope cases and three magnet tolerance cases passed.',flush=True)

if __name__=='__main__':main()
