"""Simple replaceable camera support P1: wood pedestal + one pivot cradle.

Custom design, not vendor CAD. Camera interface positions remain estimates.
No chassis geometry or final vehicle fastening is invented.
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
from reportlab.graphics.shapes import Drawing,Line,Rect,String,Polygon,Circle
from build_running_gear_step import box,cyl,hexagon,export_model
from build_heatsink_pdf import p as base_p,table as base_table,banner as base_banner,BLUE,GREY
from monitor_typography import clean

ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Composants/support-camera';OUT=B/'3D'
WOOD=(.55,.33,.13);EDGE=(.42,.24,.08);PLASTIC=(.06,.16,.23);STEEL=(.45,.48,.50);NYLON=(.80,.79,.68)
H=220;ANGLE=20

def p(text,*args,**kwargs):return base_p(clean(text),*args,**kwargs)
def table(rows,*args,**kwargs):return base_table([[clean(x) for x in r] for r in rows],*args,**kwargs)
def banner(text,*args,**kwargs):return base_banner(clean(text),*args,**kwargs)

def optimal(self,tolerance=None):
    b=Bnd_Box();BRepBndLib.AddOptimal_s(self.wrapped,b,False,False);return cq.BoundBox(b)
cq.Shape.BoundingBox=optimal
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t.strip()+'\n',encoding='utf-8')
def dump(p,o):write(p,json.dumps(o,ensure_ascii=False,indent=2))

def slot(wp,u,v,length,width,angle=0):return wp.center(u,v).slot2D(length,width,angle).center(-u,-v)

def profiles():
    base=cq.Workplane('XY').rect(80,70)
    for y in [-22,22]:base=slot(base,25,y,14,4.5)
    mast=cq.Workplane('XY').rect(40,240)
    mast=slot(mast,0,84,44.5,4.5,90)
    for x in [-12,12]:mast=mast.center(x,34).circle(2).center(-x,-34)
    brace=cq.Workplane('XY').polyline([(0,0),(40,0),(0,40)]).close()
    return base,mast,brace

def fixed_parts():
    base,mast,brace=profiles()
    base=base.extrude(6).val().translate((-5,0,0))
    # Flat mast u=-20..20,v=-120..120 -> Y=u,Z=v+126, X=-38..-32.
    mast=mast.extrude(6).val().rotate((0,0,0),(0,1,0),90).rotate((0,0,0),(1,0,0),90)
    # Explicit transform via plane avoids ambiguous stacked rotations.
    wp=cq.Workplane('YZ',origin=(-38,0,126)).rect(40,240)
    wp=slot(wp,0,84,44.5,4.5,90)
    for y in [-12,12]:wp=wp.center(y,34).circle(2).center(-y,-34)
    mast=wp.extrude(6).val()
    brace=cq.Workplane('XZ',origin=(-32,3,6)).polyline([(0,0),(40,0),(0,40)]).close().extrude(6).val()
    return [('C01_Base_CP6_80x70',base,WOOD),('C02_Montant_CP6_40x240',mast,WOOD),('C03_Gousset_CP6_40x40',brace,EDGE)]

def cradle():
    wp=cq.Workplane('XZ',origin=(0,15,0)).rect(48,48).rect(20,20)
    for sx in [-1,1]:
        for sz in [-1,1]:wp=slot(wp,14*sx,14*sz,7,2.5,45 if sx*sz>0 else -45)
    plate=wp.extrude(3).val()
    ear=cq.Workplane('YZ',origin=(-31,3,0)).rect(24,28).extrude(5).edges('|X').fillet(3).val()
    ear=ear.cut(cyl(2.15,7,0,-32,0,axis=(1,0,0)))
    web=box(8,3,24,(-27,13.5,-12))
    s=plate.fuse(ear).fuse(web).clean()
    assert s.isValid() and len(s.Solids())==1
    return s

def pitch(s,h=H,a=ANGLE):return s.rotate((0,0,0),(1,0,0),a).translate((0,0,h))

def camera_and_spacers():
    # Lightweight representation only; existing detailed camera STEP is preserved.
    pcb=cq.Workplane('XZ',origin=(0,0,0)).rect(32,32)
    for x in [-14,14]:
        for z in [-14,14]:pcb=pcb.center(x,z).circle(1.1).center(-x,-z)
    pcb=pcb.extrude(1.2).val()
    front=box(13.2,2,13.2,(0,-2.2,-6.6)).fuse(cyl(4.95,7.03,0,0,-1.2,axis=(0,-1,0))).clean()
    # cyl positional arguments are z,x,y: all optical elements centered Z=0.
    glass=cyl(3.4,.05,0,0,-8.23,axis=(0,-1,0))
    usb=box(8,4.45,5,(7,2.225,11.17))
    parts=[('CAM_Gabarit_PCB_32x32_estime',pcb,(.035,.04,.045)),('CAM_Objectif_gabarit_estime',front,(.015,.015,.018)),('CAM_Verre_gabarit_estime',glass,(.035,.12,.19)),('CAM_USB_gabarit_estime',usb,STEEL)]
    mounts=[]
    for x in [-14,14]:
        for z in [-14,14]:
            tag=f'{x}_{z}'
            spacer=cyl(2,12,z,x,0,axis=(0,1,0)).cut(cyl(1.1,12.2,z,x,-.1,axis=(0,1,0)))
            shaft=cyl(.98,20,z,x,-1.2,axis=(0,1,0))
            head=cyl(1.8,1.4,z,x,-2.6,axis=(0,1,0))
            nut=hexagon(4,1.6).rotate((0,0,0),(1,0,0),-90).translate((x,15.5,z))
            nut=nut.cut(cyl(1.02,1.8,z,x,15.4,axis=(0,1,0)))
            mounts.extend([('Entretoise_M2_12_'+tag,spacer,NYLON),('Vis_M2x20_nominale_'+tag,shaft.fuse(head),NYLON),('Ecrou_M2_nominal_'+tag,nut,NYLON)])
    return parts,mounts

def pivot_parts():
    parts=[]
    shaft=cyl(1.98,20,H,-39,0,axis=(1,0,0))
    head=hexagon(7,3).rotate((0,0,0),(0,1,0),90).translate((-42,0,H))
    parts.append(('Pivot_M4x20_nominal_sans_filet',shaft.fuse(head),STEEL))
    for name,x,color,ro in [('Rondelle_exterieure',-39,STEEL,4.5),('Rondelle_friction_nylon',-32,NYLON,5),('Rondelle_interieure',-26,STEEL,4.5)]:
        s=cyl(ro,1,H,x,0,axis=(1,0,0)).cut(cyl(2.2,1.2,H,x-.1,0,axis=(1,0,0)))
        parts.append((name,s,color))
    nut=hexagon(7,3.2).rotate((0,0,0),(0,1,0),90).translate((-25,0,H))
    nut=nut.cut(cyl(2.05,3.4,H,-25.1,0,axis=(1,0,0)))
    parts.append(('Ecrou_M4_nominal',nut,STEEL))
    return parts

def save(name,title,parts,params):
    m=export_model(dict(folder='support-camera',filename=name,title=title,parts=parts,design=True,
      published=['Camera board32x32mm and mounting holesdiam2.2 from existing local manufacturer dossier.'],
      estimated=['Custom prototype, no strength or vibration test. Camera28mm pitch,1.2mm thickness,lens and USB shapes estimated from existing model.',
        'Threads not modeled. Provisional hardware only. No chassis or USB cable route included.'],params=params,
      view=(.9,-1.4,.7),probes=[],source_pages=['../camera/notices/U20CAM-4M-Usermanual.pdf; ../camera/3D/provenance.json']))
    m.update(generated_on='2026-10-15',coordinate_system='X lateral, -Y forward, Z up. Base bottomZ0. Pivot axisX atY0,Z220 in nominal assembly.',hardware_tested=False)
    dump(OUT/Path(name).with_suffix('.json'),m);return m

def plans():
    pdir=B/'plans';pdir.mkdir(exist_ok=True)
    for name,wp in zip(['C01-base-CP6','C02-montant-CP6','C03-gousset-CP6'],profiles()):
        # DXF contours, no cutter compensation or machine code.
        # center() leaves pending wires but no objects: export an actual planar
        # face so inner slots and circles are present in the DXF as well.
        face=wp.extrude(1).faces('>Z')
        cq.exporters.export(face,str(pdir/(name+'.dxf')),exportType='DXF')
    # Dimensioned vector sheet, in drawing coordinates rather than toolpaths.
    d=Drawing(174*mm,145*mm)
    def line(x,y,a,b):d.add(Line(x*mm,y*mm,a*mm,b*mm,strokeColor=BLUE,strokeWidth=.7))
    def txt(x,y,s,size=8):d.add(String(x*mm,y*mm,s,fontName='HV3',fontSize=size,fillColor=BLUE))
    def dim(x,y,a,b,label):
        line(x,y,a,b)
        if y==b:line(x,y-1,x,y+1);line(a,b-1,a,b+1);txt((x+a)/2-4,y+2,label)
        else:line(x-1,y,x+1,y);line(a-1,b,a+1,b);txt(x+2,(y+b)/2,label)
    # Base 1:1, upper left.
    d.add(Rect(3*mm,64*mm,80*mm,70*mm,strokeColor=BLUE,fillColor=colors.HexColor('#f6eee4')))
    for yy in [77,121]:
        d.add(Rect(61*mm,(yy-2.25)*mm,14*mm,4.5*mm,rx=2.25*mm,ry=2.25*mm,strokeColor=BLUE,fillColor=colors.white))
    txt(3,139,'C01 - base, CP6');dim(3,59,83,59,'80');dim(87,64,87,134,'70')
    txt(3,52,'2 lumieres 14 x4,5 ; centres (65;13)/(65;57)',7.4)
    # Mast at 1:2, right side.
    d.add(Rect(121*mm,15*mm,20*mm,120*mm,strokeColor=BLUE,fillColor=colors.HexColor('#f6eee4')))
    d.add(Rect(129.875*mm,105.875*mm,2.25*mm,22.25*mm,rx=1.125*mm,ry=1.125*mm,strokeColor=BLUE,fillColor=colors.white))
    for xx in [125,137]:d.add(Circle(xx*mm,92*mm,1*mm,strokeColor=BLUE,fillColor=colors.white))
    txt(112,140,'C02 - montant, CP6 (1:2)');dim(146,15,146,135,'240');dim(121,10,141,10,'40')
    txt(101,3,'Slot 44,5 x4,5 ; centres utiles 190-230 au montage',6.9)
    # Brace 1:1, bottom left.
    d.add(Polygon([3*mm,6*mm,43*mm,6*mm,3*mm,46*mm],strokeColor=BLUE,fillColor=colors.HexColor('#f6eee4')))
    txt(48,38,'C03 - gousset CP6');txt(48,32,'Triangle rectangle');txt(48,26,'40 x40, angle45 degres');txt(48,20,'Sans trou : collage sur bois propre')
    from reportlab.graphics import renderSVG
    renderSVG.drawToFile(d,str(pdir/'decoupe-bois-cotes.svg'))
    return d

def docs(meta,collision):
    write(B/'README.md','''# Support caméra provisoire P1

Support simple et remplaçable pour la caméra arrière en hauteur. **Quatre pièces à fabriquer** : une base, un montant, un petit gousset en contreplaqué et un berceau plastique à un seul pivot. Pas de châssis définitif ni de visserie finale conçus ici.

- Base CP6 : **80 x70 mm**. Montant CP6 : **40 x240 mm** ; gousset CP6 : triangle **40 x40 mm**.
- Berceau : platine **48 x48 x3 mm**, oreille latérale de pivot ; impression PETG proposée. STEP disponible aussi pour adapter un usinage plastique avec reprise ; aucun G-code fourni.
- Centre caméra à **220 mm** au-dessus du dessous de base dans le montage nominal ; réglable **190-230 mm**. Inclinaison de départ **20° vers le bas**, réglable au pivot, zone d'essai prévue **10-35°**.
- Caméra sur quatre entretoises nylon M2 de **12 mm**. Les quatre lumières diagonales **7 x2,5** couvrent environ **25-31 mm** d'entraxe carré ; le28 mm du modèle caméra reste une estimation à contrôler.

[Notice et plan coté PDF](notices/notice-support-camera-provisoire-p1.pdf) · [Plans bois DXF/SVG](plans/README.md) · [STEP et STL](3D/README.md) · [Nomenclature provisoire](nomenclature.csv) · [Cotes](cotes.json) · [Contrôles](verification/conception.json).

Le câble USB doit garder une boucle libre au pivot puis être retenu par un collier sur le montant (deux trousØ4 prévus). Le serrage ne porte jamais sur les composants ou le connecteur USB. Vérifier le passage de la fiche réelle et le débattement avant fabrication du berceau.

À l'essai : cadrer plateau et route en faisant varier hauteur et angle. **Voir tout le plateau n'est pas garanti par le seul support** : champ annoncé58° horizontal, cadrage vertical et recadrage vidéo à vérifier. Valider d'abord à l'arrêt puis à faible vitesse ; rigidité, tenue des collages et vibrations à40 km/h non qualifiées. Un câble trop tendu peut faire bouger la caméra malgré le pivot serré.

Coût : chutes de CP6, petit berceau et quincaillerie générique ; pas de panier d'achat ni de prix TTC inventé. Sources : [dossier caméra existant](../camera/README.md), [hypothèses de son modèle](../camera/3D/README.md), [notice constructeur conservée](../camera/notices/U20CAM-4M-Usermanual.pdf). Aucun achat ou essai matériel effectué.
''')
    write(B/'plans/README.md','''# Plans de découpe P1

[Plan coté vectoriel](decoupe-bois-cotes.svg), [base DXF](C01-base-CP6.dxf), [montant DXF](C02-montant-CP6.dxf), [gousset DXF](C03-gousset-CP6.dxf). Millimètres, contours sans compensation d'outil ; CP6 est une épaisseur nominale à mesurer. Le PDF indique les cotes qui priment sur l'échelle d'impression.

Repères locaux : base centrée(0,0),80 x70 ; lumières centrées(25,±22),14 x4,5. Montant centré(0,0),40 x240 ; lumière centrée(0,84),44,5 x4,5 verticale ; deux trousØ4 en(±12,34). Gousset : triangle(0,0),(40,0),(0,40). Les cotes de position de la feuille SVG sont aussi données depuis les bords inférieurs gauches pour lecture manuelle.

Ne pas envoyer directement un DXF à la CNC : choisir fraise, compensation, bridage, profondeur et origine dans la FAO. Base et montant : fraise compatible avec les lumières4,5 ; gousset découpable à la scie. Pas d'usinage des lumières2,5 du berceau dans ces DXF bois.
''')
    write(B/'3D/README.md','''# CAO du support provisoire P1

- [Assemblage léger avec gabarit caméra](support-camera-provisoire-p1.step), [aperçu](support-camera-provisoire-p1.png). Caméra simplifiée pour garder un chargement rapide ; le STEP détaillé original n'est pas modifié.
- [Berceau seul STEP](berceau-camera-provisoire-p1.step), [STL orienté sur le dos de la platine](berceau-camera-provisoire-p1.stl). Pièce monobloc, pivot et lumières réels. Des supports d'impression sont nécessaires sous l'oreille ; nettoyer les perçages avant montage.
- [Pièces à fabriquer en STEP](pieces-support-camera-p1.step) : base, montant, gousset et berceau, sans quincaillerie ni caméra.

Assemblage nominal : X transversal, -Y avant, Z vertical ; base poséeZ0. Pivot horizontal suivantX, hauteur220, déclinaison20° vers le sol. Les vis/écrous sont des gabarits nominaux, sans filetage, pas des références fabricant détaillées. Cotes du support = conception ; entraxe28 de caméra, épaisseur1,2, objectif et USB = estimations du dossier existant. Les faisceaux et fixations au futur châssis sont absents.

[Provenance et validations](provenance.json), [import indépendant FreeCAD](validation-freecad.json). La CAO ne démontre pas la tenue à la vibration ou à40 km/h.
''')
    rows=[['C01','Base CP6 80x70',1,'Fabrication sur chute, deux lumières14x4,5'],['C02','Montant CP6 40x240',1,'Une lumière44,5x4,5 et deux trousØ4'],['C03','Gousset CP6 triangle40x40',1,'Collage bois, sans vis définitives'],['C04','Berceau plastique P1',1,'PETG imprimé proposé ; dimensions de conception, pas une pièce achetée'],['P01','Vis nylon M2x20',4,'Provisoire ; longueur à contrôler avec pièces reçues'],['P02','Entretoise nylon M2 /12 mm /Øext<=4',4,'Pas de contact sur les composants caméra'],['P03','Écrou nylon M2',4,'Provisoire'],['P04','Rondelle nylon M2',8,'Provisoire, non représentée individuellement au montage caméra'],['P05','Vis M4x20 +écrou M4',1,'Pivot, longueur de filetage à contrôler'],['P06','Rondelle M4 métallique /1 mm',2,'Øext9 et trou4,4 nominaux dans la CAO'],['P07','Rondelle nylon M4 /1 mm',1,'Friction, Øext10 nominal'],['P08','Colle bois +collier de câble',1,'Consommables ; maintien définitif au châssis reporté']]
    with (B/'nomenclature.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f,delimiter=';');w.writerow(['Repère','Désignation','Quantité','Note']);w.writerows(rows)
    dump(B/'cotes.json',dict(revision='P1',units='mm',custom_parts=4,hardware_tested=False,base=[80,70,6],mast=[40,240,6],brace_triangle_legs=[40,40],cradle_face=[48,48,3],window=[20,20],pivot_diameter=4.3,mast_slot=[44.5,4.5],camera_slot=[7,2.5],camera_spacing_nominal_estimated=28,camera_square_spacing_covered_approx=[25,31],camera_spacer_length=12,height_nominal=220,height_range=[190,230],down_pitch_nominal_deg=20,down_pitch_study_range_deg=[10,35],chassis_mounting_final=False,estimated_wood_thickness=True))
    dump(B/'verification/conception.json',collision)
    dump(OUT/'provenance.json',dict(revision='P1',hardware_tested=False,models=meta,camera_source_sha256=sha(ROOT/'Composants/camera/3D/camera-u20cam-4m-detaillee.step'),source_model_untouched=True))

def pdf(drawing):
    n=B/'notices/notice-support-camera-provisoire-p1.pdf';n.parent.mkdir(parents=True,exist_ok=True);tmp=ROOT/'tools/temp/support-camera-p1';tmp.mkdir(parents=True,exist_ok=True)
    def footer(c,d):
        c.setFont('HV3',7.5);c.setFillColor(GREY);c.drawString(18*mm,12*mm,'Drone V3 | Support caméra provisoire P1 | 15 octobre2026 | Non testé');c.drawRightString(192*mm,12*mm,str(d.page))
    from build_monitor_pdf import picture
    story=[p('Support caméra<br/>provisoire et remplaçable','title'),p('P1 - caméra arrière en hauteur, un seul pivot'),
      banner('<b>Quatre pièces à fabriquer.</b> Base, montant et gousset en contreplaqué6 mm ; petit berceau plastique. Montage simple pour les premiers essais, sans définir le châssis ni la visserie finale.'),Spacer(1,4*mm),
      picture(OUT/'support-camera-provisoire-p1.png',153,120),Spacer(1,3*mm),
      table([['Réglage / cote','Choix de départ'],['Base / montant','80 x70 x6 ; montant40 x240 x6 mm'],['Hauteur du centre caméra','220 mm au-dessus du dessous de base ; réglable190-230'],['Inclinaison','20° vers le bas ; pivot prévu pour essais10-35°'],['Fixation caméra','4 entretoises nylon M2 de12 mm ; lumières7 x2,5 ; entraxe28 estimé, plage carrée environ25-31']],[58,116]),
      p('Caméra montrée comme un gabarit léger. Les positions des trous et le connecteur restent à contrôler sur la pièce reçue ; le STEP détaillé original est conservé.','small'),PageBreak(),
      p('Trois découpes bois faciles','title'),drawing,Spacer(1,5*mm),
      table([['Pièce','Opération'],['C01 - CP6','Découper80 x70 ; deux lumières14 x4,5. Origine coin inférieur gauche : centres(65;13) et(65;57).'],['C02 - CP6','Découper40 x240 ; lumière44,5 x4,5 verticale centrée(20;204). Deux trousØ4 aux points(8;154)/(32;154).'],['C03 - CP6','Triangle rectangle40 x40, épaisseur6 ; poncer les surfaces de collage.'],['Fichiers fournis','DXF millimétriques sans compensation, SVG coté et STEP. Mesurer l’épaisseur réelle du bois ; aucune trajectoire CNC produite.']],[43,131]),
      p('Assemblage bois : coller le montant vertical sur la base, face extérieure à7 mm du bord gauche ; le placer centré en profondeur. Le gousset part de sa face intérieure et s’étend de40 mm vers la droite. Laisser durcir la colle selon sa notice avant de charger le support.','small'),PageBreak(),
      p('Montage et réglage sans complication','title'),
      table([['Étape','Geste à réaliser'],['1 - Berceau','Imprimer le petit berceau PETG, ou adapter un usinage plastique à partir du STEP. STL posé sur le dos de la platine ; supports sous l’oreille. Nettoyer les trous, sans forcer.'],['2 - Caméra','4 entretoises nylon12 mm, vis M2x20 et écrous. Présenter la caméra et sa vraie fiche USB avant serrage ; vérifier que les entretoises portent uniquement autour des trous.'],['3 - Pivot','M4x20 : rondelle extérieure, montant, rondelle nylon1 mm, oreille, rondelle intérieure, écrou. Vérifier longueur et absence de contact avec la carte.'],['4 - Cadrage','Faire coulisser le pivot pour la hauteur ; orienter la caméra, puis serrer juste assez pour que le cadre tienne à la main. Aucune valeur de couple inventée pour le plastique et le bois.'],['5 - Câble / châssis','Garder une boucle libre au pivot et retenir le câble sur le montant avec un collier aux deux trousØ4. Les deux lumières de base serviront à la fixation provisoire ; emplacement final après le châssis.']],[39,135]),Spacer(1,4*mm),
      banner('Vérifier d’abord à l’arrêt, puis à faible vitesse : collage, glissement du pivot, vibrations, image et passage du câble. <b>La tenue à40 km/h n’est pas encore qualifiée.</b> Le support pourra être remplacé sans changer la caméra.'),
      p('Voir le plateau et la route dépend du cadrage réel. Le champ horizontal annoncé est58° ; le champ vertical utile et les recadrages1080p sont à vérifier. Ce support ne garantit pas la visibilité de tous les coins du plateau.','small'),
      p('Coût : chutes de contreplaqué, petit berceau et quincaillerie générique. Pas de prix TTC ni de panier d’achat inventé. Nomenclature provisoire séparée ; la visserie finale reste après le châssis.','small'),
      p('Sources : dossier caméra local, notice constructeur U20CAM-4M et provenance de son modèle. Carte32 x32 et trousØ2,2 publiés ; entraxe28, épaisseur1,2 et géométrie USB estimés. Modèle, perçages et débattement vérifiés numériquement ; aucun essai matériel.','small')]
    for f in story:
        if isinstance(f,Table):f.spaceAfter=3*mm
    SimpleDocTemplate(str(n),pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=18*mm,bottomMargin=22*mm,title='Drone V3 - Support caméra provisoire P1').build(story,onFirstPage=footer,onLaterPages=footer)
    doc=pymupdf.open(n);assert len(doc)==3,len(doc)
    renders=[]
    for i,page in enumerate(doc):
        q=tmp/f'page-{i+1}.png';page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(q);renders.append(str(q.relative_to(ROOT)))
    dump(n.with_suffix('.json'),dict(pages=len(doc),sha256=sha(n),renders=renders,visual_review_completed=False))

def main():
    sys.stdout.reconfigure(encoding='utf-8');OUT.mkdir(parents=True,exist_ok=True);(B/'verification').mkdir(exist_ok=True)
    if '--docs-only' in sys.argv:
        pdf(plans());indices();return
    fixed=fixed_parts();cr=cradle();cams,mounts=camera_and_spacers();moving=[('C04_Berceau_pivot',cr,PLASTIC),*cams,*mounts]
    placed=[(n,pitch(s),c) for n,s,c in moving]
    # Genuine geometric check: moving support/camera against fixed wood over the study range.
    worst=0;cases=[]
    moving_solid=cq.Compound.makeCompound([s for _,s,_ in moving])
    for h in [190,220,230]:
        for a in [10,20,35]:
            posed=pitch(moving_solid,h,a)
            vol=sum(posed.intersect(s).Volume() for _,s,_ in fixed);worst=max(worst,vol)
            assert vol<1e-5,(h,a,vol)
            cases.append(dict(height_mm=h,down_pitch_deg=a,overlap_with_fixed_wood_mm3=vol))
    # Board and USB envelopes must not collide with cradle/spacers.
    inner=[]
    for n,s,_ in cams:
        v=s.intersect(cr).Volume();assert v<1e-5,(n,v);inner.append(dict(part=n,cradle_overlap_mm3=v))
    params=dict(revision='P1',height_mm=H,down_pitch_deg=ANGLE,custom_parts=4,camera_gabarit_only=True)
    a=save('support-camera-provisoire-p1.step','Support camera P1 | simple et remplacable',fixed+placed+pivot_parts(),params)
    b=save('berceau-camera-provisoire-p1.step','P1 | berceau monobloc, une vis de pivot',[('C04_Berceau',cr,PLASTIC)],dict(part='C04',camera_spacing_estimated_mm=28,slots_mm=[7,2.5]))
    # Back of the plate placed at Z0; ear extends upward, requiring support material.
    printable=cr.rotate((0,0,0),(1,0,0),-90).translate((0,0,15))
    assert abs(printable.BoundingBox().zmin)<1e-6
    cq.exporters.export(printable,str(OUT/'berceau-camera-provisoire-p1.stl'),tolerance=.05,angularTolerance=.12)
    c=save('pieces-support-camera-p1.step','P1 | quatre pieces a fabriquer',fixed+[placed[0]],dict(custom_parts=4,hardware_included=False))
    check=dict(hardware_tested=False,geometry_valid=True,clearance_grid=cases,max_fixed_overlap_mm3=worst,camera_cradle_clearance=inner,thread_geometry_included=False,USB_plug_and_cable_not_tested=True,structural_qualification=False)
    docs([a,b,c],check);drawing=plans();pdf(drawing)
    indices()
    print('Support P1 built, three STEP imports checked, nine clearance poses checked, PDF3 pages.',flush=True)

def indices():
    # Add one index entry without touching existing component records.
    index=ROOT/'Composants/README.md';t=index.read_text(encoding='utf-8')
    row='| [Support caméra provisoire](support-camera/README.md) | P1 : base et montant bois, berceau à un pivot | À fabriquer / chutes | STEP, plan coté, DXF et notice ; hauteur190-230 mm, remplaçable |'
    if row not in t:t=t.replace('| [Caméra](camera/README.md)',row+'\n| [Caméra](camera/README.md)',1)
    write(index,t)
    plan=ROOT/'PLAN-CONCEPTION.md';t=plan.read_text(encoding='utf-8');t=t.replace('2. Support caméra arrière et en hauteur, pour observer le plateau et la route.','2. [Support caméra provisoire P1](Composants/support-camera/README.md), arrière et en hauteur. Conception simple créée : STEP, DXF bois, plan coté et notice ; essais matériels à faire.')
    write(plan,t)

if __name__=='__main__':main()
