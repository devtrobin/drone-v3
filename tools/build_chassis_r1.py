"""Chassis A2-R1, local dossiers only; one common geometry source for STEP/DXF/plans.

Machining drawings describe custom chassis parts, not unmeasured vendor parts.
Component envelopes are identified separately from the manufactured chassis.
"""
from pathlib import Path
import argparse,csv,hashlib,json,math,re,sys
import cadquery as cq
import numpy as np
import ezdxf,pymupdf
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from reportlab.lib import colors
from reportlab.lib.pagesizes import A3,landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.graphics import renderSVG,renderPDF
from reportlab.graphics.shapes import Drawing,Line,Rect,String,Circle,Polygon
from build_running_gear_step import box,cyl,export_model
from build_heatsink_pdf import p as unused_font_registration
import build_camera_support as cam
import build_speed_mounts as speed

ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Composants/chassis';O=B/'3D';P=B/'plans';V=B/'verification'
ALU=(.56,.59,.63);PP=(.075,.09,.11);BLACK=(.018,.022,.027);BLUE=(.025,.19,.31);RED=(.65,.018,.01);GREEN=(.018,.18,.065);ORANGE=(.85,.23,.005);STEEL=(.42,.45,.49)
PLATES=[];HOLES=[];FITTINGS=[];PLACEMENTS=[];SOURCES={};CUSTOM=[]
GROUND=0;DECK_BOTTOM=8;DECK_TOP=11;AXLE=31.5;REAR=445;FRONT=55

def optimal(self,tolerance=None):
    b=Bnd_Box();BRepBndLib.AddOptimal_s(self.wrapped,b,False,False);return cq.BoundBox(b)
cq.Shape.BoundingBox=optimal
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,text):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text.strip()+'\n',encoding='utf-8')
def dump(path,data):write(path,json.dumps(data,ensure_ascii=False,indent=2))
def source(rel):
    path=ROOT/rel;assert path.exists(),path;SOURCES[rel]=sha(path)
def slot(x,y,length,width,angle=0,role=''):
    return dict(type='slot',x=x,y=y,length=length,width=width,angle=angle,role=role)
def hole(x,y,d,role=''):return dict(type='hole',x=x,y=y,d=d,role=role)
def window(x,y,w,h,role=''):return dict(type='window',x=x,y=y,w=w,h=h,role=role)

def angle_templates():
    return [('L01-semelle',275,25,[hole(x,15,4.5,'Station depuis coupe avant, distance depuis talon extérieur') for x in [20,115,255]]),
        ('L02-semelle',40,40,[hole(x,15,4.5,'Depuis coin avant gauche de la semelle') for x in [10,30]]),
        ('L02-verticale',40,40,[hole(20,y,4.5,'Depuis côté gauche et dessous semelle') for y in [15,31]]),
        ('L03-arriere',40,50,[hole(x,35,4.5,'Depuis côté gauche et coupe inférieure') for x in [15,35]]),
        ('L03-pivot',40,50,[slot(13,25,44.5,4.5,90,'Depuis chant avant et coupe inférieure')])]

def angle_dxf():
    for name,w,h,features in angle_templates():
        doc=ezdxf.new('R2010');doc.units=4
        doc.layers.new('REFERENCE_AILE_NE_PAS_DECOUPER',dxfattribs={'color':8})
        doc.layers.new('PERCAGE',dxfattribs={'color':1});ms=doc.modelspace()
        ms.add_lwpolyline([(0,0),(w,0),(w,h),(0,h)],close=True,dxfattribs={'layer':'REFERENCE_AILE_NE_PAS_DECOUPER'})
        for f in features:
            if f['type']=='hole':ms.add_circle((f['x'],f['y']),f['d']/2,dxfattribs={'layer':'PERCAGE'})
            else:
                x,y=f['x'],f['y'];r=f['width']/2;a=(f['length']-f['width'])/2
                ms.add_line((x-r,y-a),(x-r,y+a),dxfattribs={'layer':'PERCAGE'})
                ms.add_line((x+r,y-a),(x+r,y+a),dxfattribs={'layer':'PERCAGE'})
                ms.add_arc((x,y+a),r,0,180,dxfattribs={'layer':'PERCAGE'})
                ms.add_arc((x,y-a),r,180,360,dxfattribs={'layer':'PERCAGE'})
        doc.saveas(P/(name+'.dxf'))

def plate(code,label,w,h,t,material='Al 5754 H22',qty=1,features=None,outline=None,r=0,origin=(0,0),z=11,pose=None):
    # 2D drawing origin is the lower left corner of the stock bounding rectangle.
    d=dict(code=code,label=label,w=w,h=h,t=t,material=material,qty=qty,features=features or [],outline=outline,r=r,origin=origin,z=z,pose=pose)
    PLATES.append(d);return d

def profile(d):
    if d['outline']:
        wp=cq.Workplane('XY').polyline(d['outline']).close()
        s=wp.extrude(d['t']).val()
    else:s=box(d['w'],d['h'],d['t'],(d['w']/2,d['h']/2,0),d['r'])
    for f in d['features']:
        if f['type']=='hole':cut=cyl(f['d']/2,d['t']+2,-1,f['x'],f['y'])
        elif f['type']=='slot':cut=cq.Workplane('XY').center(f['x'],f['y']).slot2D(f['length'],f['width'],f['angle']).extrude(d['t']+2).val().translate((0,0,-1))
        else:cut=box(f['w'],f['h'],d['t']+2,(f['x'],f['y'],-1),1)
        s=s.cut(cut)
    assert s.isValid() and len(s.Solids())==1,d['code']
    return s.clean()

def posed(d,s):
    if d['pose']=='post':
        # local u -> X, v -> Z, thickness -> -Y; rear face atY496.
        return s.rotate((0,0,0),(1,0,0),90).translate((d['origin'][0],518,14))
    if d['pose']=='crossbar':return s.rotate((0,0,0),(1,0,0),90).translate((-142,512,219))
    return s.translate((*d['origin'],d['z']))

def make_design():
    # Locations of chassis-to-cassette holes are project-controlled. Do not infer
    # manufacturer mounting patterns from an envelope.
    floor=[]
    def F(x,y,d,role):floor.append(hole(x+150,y,d,role))
    for x in [-135,-100,100,135]:
        for y in [40,70]:F(x,y,4.5,'C03 traverse avant')
    for x in [-130,130]:
        for y in [120,215,355]:F(x,y,4.5,'L01 longeron')
    for x in [-72,72]:
        for y in [194,408]:F(x,y,4.5,'Pont C02 / tube L70')
    for x in [-23,23]:
        for y in [68,92]:F(x,y,2.7,'C08 servo / entretoise20')
    for x in [-133,-57]:
        for y in [102,178]:F(x,y,4.5,'C07 pod ED80 / tube L56')
    # Encoder feet, two holes per side; M3 through the original longitudinal slots.
    for sign in [-1,1]:
        for y in [435,455]:F(sign*74,y,3.5,'P1 capteur vitesse, pied réglable')
    for y in [230,310]:
        for x in [-34,34]:floor.append(slot(x+150,y,23,3.5,90,'Sangle20 batterie'))
    for y in [193,347]:
        for x in [-20,20]:F(x,y,3.5,'C16 butée batterie')
    for x in [-28,28]:
        for y in [212,328]:F(x,y,3.5,'C17 guide latéral batterie')
    for sign in [-1,1]:
        for x in [118,138]:F(sign*x,487,4.5,'L02 pieds portique caméra')
    floorplate=plate('C01','Plateau principal',300,520,3,r=12,origin=(-150,0),z=8,features=floor)
    # Modules with unknown supplier holes get a removable blank, never guessed holes.
    def cassette(code,label,w,h,t,x,y,offsetx,offsety,material='PP compact',z=14,extra=None):
        fs=[hole(w/2+sx*offsetx,h/2+sy*offsety,3.5,'Fixation cassette M3') for sx in [-1,1] for sy in [-1,1]]
        fs+=extra or []
        d=plate(code,label,w,h,t,material,features=fs,origin=(x-w/2,y-h/2),z=z)
        for f in fs[:4]:F(x-w/2+f['x'],y-h/2+f['y'],3.5,code+' cassette')
        return d
    cassette('C05','Cassette F0 classe T',125,90,5,75,140,55,38)
    cassette('C06','Cassette 4 supports de branches',104,120,5,88,262,45,52)
    cassette('C12','Cassette UD80A',50,85,5,112,368,15,35)
    cassette('C13','Platine dissipateur HS251',62,82,3,-110,225,24,33,'Al 5754 H22')
    cassette('C14','Cassette D+ et D-',106,65,3,-88,303,46,25)
    cassette('C15','Maintien raccord IC5 et voies fines',40,40,3,-10,145,13,13,extra=[slot(20,20,20,3.5,90,'Collier isolé')])
    for code,x in [('C11G',-47),('C11D',47)]:
        cassette(code,'Platine ESC '+code[-1],50,40,3,x,376,19,14,
            extra=[slot(14,20,25,3.5,90,'Maintien ESC'),slot(36,20,25,3.5,90,'Maintien ESC')])
    # Rear reinforcement/removable transmission adapters, mirrored mechanical parts.
    for sign,code in [(1,'C04D'),(-1,'C04G')]:
        poly=[(0,0),(90,0),(90,90),(0,90),(0,82),(10,82),(10,48),(0,48)]
        fs=[slot(x,y,15,4.5,0,'Fixation transmission au plateau') for x in [28,48] for y in [12,80]]
        if sign<0:
            poly=[(90-x,y) for x,y in poly][::-1]
            fs=[slot(90-f['x'],f['y'],15,4.5,0,f['role']) for f in fs]
        origin=(92,380) if sign>0 else (-182,380)
        d=plate(code,'Platine transmission '+code[-1],90,90,3,'Al 6061 T6',outline=poly,features=fs,origin=origin,z=11)
        for f in fs:F(origin[0]+f['x'],origin[1]+f['y'],4.5,code+' lumières')
    # Front crossmember maintains the existing F-AV nominal mounting height.
    outline=[(0,18.5),(30,18.5),(30,0),(318,0),(318,18.5),(348,18.5),(348,48.5),(318,48.5),(318,55),(30,55),(30,48.5),(0,48.5)]
    fs=[hole(x+174,y-30,4.5,'Fixation au plateau') for x in [-135,-100,100,135] for y in [40,70]]
    fs += [hole(x+174,y-30,3.5,'Fourche F-AV, montage nominal') for x in [-170,170] for y in [56,70]]
    fs += [hole(x+174,38,2.7,'Entretoise avant servo17.5') for x in [-23,23]]
    plate('C03','Traverse et oreilles avant',348,55,2.5,'Al 6061 T6',outline=outline,features=fs,origin=(-174,30),z=11)
    # Two longitudinal raw angles; no bending operation is required.
    # The slots/chassis planes of the camera cradle are preserved; the wood mast
    # is replaced in the A2 installation by a removable metal two-post gantry.
    plate('C07','Dessus du pod ED80',90,90,3,origin=(-140,95),z=70,features=
        [hole(45,45,25,'ED80 centre'),hole(21,45,5.5,'ED80 fixation'),hole(69,45,5.5,'ED80 fixation')]+
        [hole(x,y,4.5,'Tube L56') for x in [7,83] for y in [7,83]])
    plate('C08','Support haut du servo',55,35,3,origin=(-27.5,62.5),z=31,features=
        [window(27.5,17.5,24,13,'Passage corps FT90M')]+
        [hole(27.5+x,17.5,2.2,'FT90M oreilles à vérifier') for x in [-14.25,14.25]]+
        [hole(27.5+x,17.5+y,2.7,'Entretoises20') for x in [-23,23] for y in [-12,12]])
    # Deck of the bridge, four pillar holes and exact project PCB pattern.
    fs=[hole(x+80,y-180,4.5,'Tube L70') for x in [-72,72] for y in [194,408]]
    fs += [hole(x+80,y-180,3.5,'Porteuse M1P') for x in [-66,66] for y in [274,341]]
    fs += [hole(x+80,y-180,2.7,'Pi5 rectangle58 x49') for x in [-31.5,26.5] for y in [353.5,402.5]]
    fs += [window(63,227,18,4,'Passage des fils sous GPIO ; souder Pi hors châssis')]
    for cx in [-38,38]:
        for x in [-31,31]:
            for y in [-31,31]:fs.append(hole(cx+x+80,230+y-180,3.5,'Cassette EVM'))
    # Regulator and small-signal connector plates fixed on the upper bridge.
    fs += [hole(x+80,y-180,3.5,'Cassette régulateur') for x in [-70,-46] for y in [368,396]]
    for y in [183,267,346]:
        for x in [-70,70]:fs.append(slot(x+80,y-180,10,3.5,0,'Signal / retenue câble'))
    plate('C02','Pont électronique démontable',160,250,2,r=4,origin=(-80,180),z=81,features=fs)
    fs=[hole(x,y,3.5,'Fixation cassette EVM') for x in [5,67] for y in [5,67]]
    fs += [slot(x,36,20,3,90,'Lien silicone sur isolant') for x in [3,69]]
    # Second identical plate exported only once; assembly creates two copies.
    plate('C09','Cassette EVM TI sans trous EVM',72,72,3,'PP compact',qty=2,origin=(-74,194),z=93,features=fs)
    plate('C10','Cassette régulateur',35,44,3,'PP compact',origin=(-75,358),z=83,features=
        [hole(x,y,3.5,'Fixation au pont, tête affleurante') for x in [5,29] for y in [10,38]])
    plate('C16','Butée longitudinale batterie',56,12,8,'PP compact',qty=2,origin=(-28,187),z=11,features=[hole(x,6,3.5,'Butée M3') for x in [8,48]])
    plate('C17','Guide latéral batterie',8,16,8,'PP compact',qty=4,origin=(-32,204),z=11,features=[hole(4,8,3.5,'Guide M3')])
    plate('C18','Montant portique caméra',25,230,6,'Al 6061 T6',qty=2,origin=(-140.5,0),pose='post',features=[hole(12.5,v,4.5,'Portique M4') for v in [12,28,212,224]])
    plate('C19','Traverse haute caméra',284,25,3,origin=(-142,0),pose='crossbar',features=
        [hole(x+142,z-219,4.5,'Montants caméra M4') for x in [-128,128] for z in [226,238]]+
        [hole(x+142,12,4.5,'L03 angle pivot') for x in [-20,0]])
    # Appenditions to floor are complete; copied list remains the shared list.
    assert floorplate['features'] is floor

def angle_section(a,b,t,length):
    return cq.Workplane('XY').polyline([(0,0),(a,0),(a,t),(t,t),(t,b),(0,b)]).close().extrude(length).val()

def custom_parts():
    parts=[]
    for d in PLATES:
        s=profile(d);color=PP if d['material'].startswith('PP') else ALU
        for i in range(d['qty']):
            q=posed(d,s)
            if d['code']=='C09' and i==1:q=q.translate((76,0,0))
            if d['code']=='C16' and i==1:q=q.translate((0,154,0))
            if d['code']=='C17':q=q.translate((56*(i%2),116*(i//2),0))
            if d['code']=='C18' and i==1:q=q.translate((256,0,0))
            parts.append((d['code']+'_'+str(i+1),q,color))
    # Longitudinal25x25x3 angle, local X horizontal inboard, Z vertical.
    for sign in [-1,1]:
        s=box(25,275,3,(132.5,237.5,11)).fuse(box(3,275,22,(143.5,237.5,14)))
        for y in [120,215,355]:s=s.cut(cyl(2.25,5,10,130,y))
        if sign<0:s=s.mirror('YZ')
        parts.append(('L01_longeron_'+str(sign),s.clean(),ALU))
    # Camera feet from40x40x3 raw angles, length40 along X.
    for x in [-128,128]:
        s=box(40,40,3,(x,492,11)).fuse(box(40,3,37,(x,510.5,14)))
        for xx in [x-10,x+10]:s=s.cut(cyl(2.25,5,10,xx,487))
        for z in [26,42]:s=s.cut(cyl(2.25,5,z,x,508.5,axis=(0,1,0)))
        parts.append(('L02_pied_camera_'+str(x),s.clean(),ALU))
    # Vertical angle40x40x3 cut50, links existing cradle to the gantry.
    s=box(40,3,50,(-15,507.5,196)).fuse(box(3,37,50,(-33.5,487.5,196)))
    cut=cq.Workplane('YZ',origin=(-36,482,221)).slot2D(44.5,4.5,90).extrude(5).val();s=s.cut(cut)
    for x in [-20,0]:s=s.cut(cyl(2.25,5,231,x,505,axis=(0,1,0)))
    parts.append(('L03_angle_pivot_camera',s.clean(),ALU))
    # Hollow raw tubes, not purchased product references.
    for x in [-72,72]:
        for y in [194,408]:parts.append(('T01_L70_'+str(x)+'_'+str(y),cyl(5,70,11,x,y).cut(cyl(2.25,70.2,10.9,x,y)),ALU))
    for x in [-133,-57]:
        for y in [102,178]:parts.append(('T02_L56_'+str(x)+'_'+str(y),cyl(5,56,14,x,y).cut(cyl(2.25,56.2,13.9,x,y)),ALU))
    for x in [-23,23]:
        for y in [68,92]:
            z=13.5 if y==68 else 11;h=31-z
            parts.append(('N01_entretoise_servo_'+str(x)+'_'+str(y),cyl(2.5,h,z,x,y).cut(cyl(1.35,h+.2,z-.1,x,y)),BLACK))
    #3mm spacers raise cassettes to the top plane of the longitudinal angles.
    # Do not place a second spacer on top of an existing angle.
    for f in PLATES[0]['features']:
        if f['type']!='hole' or not ('cassette' in f['role'] or 'pod ED80' in f['role']):continue
        x=f['x']-150;y=f['y']
        on_angle=120<=abs(x)<=145 and 100<=y<=375
        on_rear=95<=abs(x)<=179 and 383<=y<=467 and not(abs(x)<105 and 425<y<465)
        if not on_angle and not on_rear:parts.append(('N02_cale3_'+str(len(parts)),cyl(3,3,11,x,y).cut(cyl(f['d']/2,3.2,10.9,x,y)),BLACK))
    # Nonconductive pads and soft bumper are in the cut list, not electrical returns.
    parts.append(('S01_patin_silicone140x46x2',box(46,140,2,(0,270,11)),BLACK))
    parts.append(('S02_bumper_EVA260x15x6',box(260,6,15,(0,-3,8)),BLACK))
    return parts

def envelope(name,w,h,t,x,y,z,color,folder,status='Réservation, fixation composant à relever'):
    s=box(w,h,t,(x,y,z),min(1,w/10,h/10))
    PLACEMENTS.append(dict(name=name,x=x,y=y,z_bottom=z,envelope_mm=[w,h,t],folder=folder,status=status))
    return (name,s,color)

def equipment():
    p=[]
    p.append(envelope('B01_G1_IC5_139x46x25',46,139,25,0,270,13,BLACK,'cordon-principal-batterie','139 x46 x25 selon archive RCTeam G1, pas ancienne Zeee'))
    # Two visible straps; shape gives a reserved envelope, not a fabric strength model.
    for y in [230,310]:
        belt=box(68,20,1.2,(0,y,38)).fuse(box(1.2,20,31.2,(-34,y,8))).fuse(box(1.2,20,31.2,(34,y,8))).fuse(box(68,20,1.2,(0,y,6.8)))
        p.append(('Sangle20_gabarit_'+str(y),belt,BLACK))
    # Raised ED80: gabarit with body under the panel, no reconstruction screws
    # embedded in the panel. Native detailed model remains separately archived.
    path=ROOT/'Composants/coupure-manuelle/albright-ed80/3D/albright-ed80-ferme-detaille.step';source(str(path.relative_to(ROOT)).replace('\\','/'))
    ed=box(59,58,37,(-95,140,33),4)
    for x in [-119,-71]:ed=ed.cut(cyl(2.75,37.2,32.9,x,140))
    p.append(('ED80_corps_sous_panneau_gabarit',ed,BLACK))
    p.append(('ED80_collet_gabarit',cyl(12.4,6,70,-95,140),BLACK))
    p.append(('ED80_tige_gabarit',cyl(5,39,62,-95,140),BLACK))
    p.append(('ED80_col_bouton_gabarit',cyl(16,32,80,-95,140),RED))
    p.append(('ED80_bouton_gabarit',cyl(24,14,112,-95,140),RED))
    for y in [129.5,150.5]:p.append(('ED80_borne_gabarit_'+str(y),cyl(3,18,15,-95,y),STEEL))
    PLACEMENTS.append(dict(name='ED80',x=-95,y=140,mounting_plane_underside_z=70,panel_top_z=73,bottom_z=15,folder='coupure-manuelle',status='Plan ED80 : perçages25 et5.5 /48 ; gabarit sous panneau, ancien STEP conservé'))
    p.append(envelope('F0_LFT_JLLN50_reserve_NON_CAO',120,60,65,75,140,19,BLUE,'support-fusible-classe-t'))
    for x,n,folder in [(50,'F1_KLKD20','supports-branches-rapides'),(75,'F2_KLKD20','supports-branches-rapides'),(100,'FP_KLKD10','supports-branches-rapides'),(125,'FAUX_KLKD1','carte-surveillance-electrique')]:
        p.append(envelope(n+'_reserve_NON_CAO',22,85,55,x,262,19,BLUE,folder))
    for y,n in [(285,'D_plus'),(320,'D_moins')]:
        path=ROOT/'Composants/distribution-alimentation/bornier-2315/3D/bluesea-2315-complet-detaille.step';source(str(path.relative_to(ROOT)).replace('\\','/'))
        s=box(106.68,22.86,6,(-87,y,17),1)
        for x in [-87-45.245,-87+45.245]:s=s.cut(cyl(2.75,6.2,16.9,x,y))
        p.append((n+'_2315_base_gabarit',s,BLACK))
        p.append((n+'_2315_barre_gabarit',box(78,12.7,1.98,(-87,y,30)),STEEL))
        for k in range(4):p.append((n+'_goujon_sans_filetage_'+str(k),cyl(2.413,12,31.98,-87+(k-1.5)*21.59,y),STEEL))
        cap=box(86.36,22,13.75,(-87,y,35)).cut(box(83.36,19,12.35,(-87,y,34.9)))
        p.append((n+'_capot_gabarit',cap,BLUE))
        PLACEMENTS.append(dict(name=n,x=-87,y=y,z_bottom=17,envelope_mm=[106.68,22.86,31.75],folder='distribution-alimentation',status='Enveloppe modèle existant, trous propres dans cassette après présentation'))
    path=ROOT/'Composants/dissipateur-relais/3D/assemblage-d1d100-hs251-hsp1-etude.step';source(str(path.relative_to(ROOT)).replace('\\','/'))
    p.append(('HS251_semelle_gabarit',box(52.324,85.344,3,(-112,227,17)),ALU))
    for i in range(9):p.append(('HS251_ailette_estimee_'+str(i),box(2,58.7,33.64,(-134+i*5.5,227,20)),ALU))
    p.append(('HS251_face_contact_gabarit',box(50.3,58.7,4,(-112,227,53.64)),ALU))
    p.append(('D1D100_gabarit',box(44.2,57.1,22.6,(-112,227,57.767)),BLACK))
    PLACEMENTS.append(dict(name='HS251_D1D100',x=-112,y=227,z_bottom=17,rotation_z_deg=90,envelope_mm=[52.324,85.344,63.367],folder='dissipateur-relais',status='Gabarit allégé aux cotes extérieures archivées ; convection réelle à tester'))
    p.append(envelope('UD80A_reserve',30.1,69.1,46.3,108,368,19,BLUE,'repartition-moteurs'))
    for x,n in [(-47,'G'),(47,'D')]:p.append(envelope('ESC_'+n,33.4,26.8,15.1,x,376,17,BLACK,'moteur','Corps nominal, câbles75mm et connecteurs réservés autour'))
    # PCB outline and sockets are lightweight placement bodies, not the heavy
    #142MB native model or a new representation of its internal circuitry.
    p.append(envelope('Pi5_PCB_gabarit',85,56,1.6,7.5,378,98,GREEN,'raspberry-pi-5','Origine PCB(-35,350), fixations58 x49, entretoises15, pièces allégées'))
    p.append(('Pi_ports_USB_Ethernet_gabarit',box(26,54,16,(37,378,99.6)),STEEL))
    p.append(('Pi_GPIO_signal9contacts_gabarit',box(50.8,5.08,22.5,(-2.5,402.5,99.6)),BLACK))
    p.append(('Pi_ActiveCooler_gabarit',box(40,40,15,(-10,374,99.6)),ALU))
    p.append(('Pi_ventilateur_gabarit',cyl(14,4,114.6,-10,374),BLACK))
    # Carrier alone. Two separate EVM cassettes avoid using the old overlapping
    #visual reserves as if they were physical parts mounted on the carrier.
    p.append(envelope('M1P_porteuse_et_corps',140,75,15,0,307.5,98,GREEN,'carte-surveillance-electrique','PCB140x75 et entraxes132x67 exacts du projet, sous-face libre15'))
    for x in [-38,38]:p.append(envelope('EVM60_reserve_'+str(x),60,60,12,x,230,96,BLUE,'carte-surveillance-electrique','TI : réservation60x60x12 ; maintien isolant souple, aucun trou TI inventé'))
    p.append(envelope('Pololu2831_reserve',18,13,5.5,0,187,83,BLUE,'carte-surveillance-electrique'))
    p.append(envelope('D42V55F5_reserve',25.4,25.4,10.825,-57.5,388,96,GREEN,'regulateur-alimentation/d42v55f5','Sous-face96 :10 de dégagement au-dessus C10 ; trous constructeur à reporter'))
    p.append(envelope('Pololu2813_HP_reserve',21,18,5,30,190,83,GREEN,'protection-batterie/interrupteur-pi'))
    for x,y,n in [(-60,325,'INplus'),(-35,325,'INmoins')]:
        p.append(envelope('WAGO413_'+n,18.8,18.6,8.4,x,y,83,ORANGE,'liaisons-alimentation-surveillance/wago-221-413'))
    p.append(envelope('WAGO413_5V',18.8,18.6,8.4,-30,420,83,ORANGE,'liaisons-alimentation-surveillance/wago-221-413','Sur pont derrière Pi ; sorties vers pads courts, à mesurer'))
    p.append(envelope('WAGO415_retours',30,18.6,8.4,-24,388,83,ORANGE,'liaisons-alimentation-surveillance/wago-221-415','Sous Pi sur pont ; accès après dépose Pi, maintien isolant'))
    # Actual support columns for boards with project-known mounting patterns.
    for x in [-31.5,26.5]:
        for y in [353.5,402.5]:p.append(('Entretoise_Pi15_'+str(x)+'_'+str(y),cyl(2.5,15,83,x,y).cut(cyl(1.35,15.2,82.9,x,y)),BLACK))
    for x in [-66,66]:
        for y in [274,341]:p.append(('Entretoise_M1_15_'+str(x)+'_'+str(y),cyl(3,15,83,x,y).cut(cyl(1.75,15.2,82.9,x,y)),BLACK))
    for cx in [-38,38]:
        for dx in [-31,31]:
            for dy in [-31,31]:
                x=cx+dx;y=230+dy;p.append(('Entretoise_EVM_10_'+str(x)+'_'+str(y),cyl(3,10,83,x,y).cut(cyl(1.75,10.2,82.9,x,y)),BLACK))
    # Auxiliary sense resistor holder and local XH/IC5 area, not bare live conductors.
    p.append(envelope('AC03_XH_zone_locale',40,30,10,-10,145,17,PP,'carte-surveillance-electrique','3 AC03 protégées, prise XH et retenue isolante ; fils vers pack non coupés'))
    p.append(envelope('IC5_zone_connecteur',25,20,14,0,190,13,ORANGE,'cordon-principal-batterie'))
    # Existing Hall mount: lower the movable head3.5mm, keeping base on the deck.
    for sign,n in [(1,'D'),(-1,'G')]:
        for name,s,col in speed.station():
            if name.startswith('Axe5'):continue
            if not name.startswith('P01'):s=s.translate((0,0,-3.5))
            if sign<0:s=s.rotate((0,0,0),(0,0,1),180)
            s=s.translate((sign*103,REAR,11));p.append(('HALL_'+n+'_'+name,s,col))
        source('Composants/supports-capteurs-vitesse/3D/station-capteur-vitesse-p1.step')
        # Gearbox reserved extent, drawn as edge rails rather than a false box.
        for xx in [118,176]:p.append(('Transmission_'+n+'_limite_'+str(xx),box(2,71,2,(sign*xx,423.5,56)),BLUE))
        for yy in [388,459]:p.append(('Transmission_'+n+'_limite_'+str(yy),box(60,2,2,(sign*147,yy,56)),BLUE))
        # Nominal motor, shaft and gear outlines for orientation only.
        motor=cyl(12,36,31.5,sign*140,408,axis=(sign,0,0));p.append(('Moteur2435_'+n+'_corps_nominal',motor,RED))
        p.append(('Moteur_'+n+'_axe2',cyl(1,12,31.5,sign*128,408,axis=(sign,0,0)),STEEL))
        for x,y,r in [(130.5,425.5,14),(119.5,REAR,14),(119.5,425.5,6.5)]:
            p.append(('Engrenage_'+n+'_'+str(x)+'_'+str(y)+'_enveloppe_sans_denture',cyl(r,5,31.5,sign*(x-2.5),y,axis=(sign,0,0)),STEEL))
        p.append(('Arbre_sortie_'+n+'_enveloppe_a_definir',cyl(2.5,115,31.5,sign*92,REAR,axis=(sign,0,0)),STEEL))
        PLACEMENTS.append(dict(name='Train_arriere_'+n,axle_y=REAR,axis_z=31.5,base='C04'+n,folder='transmission-arriere',status='2 étages, entraxes17.5/19.5 en Y, empilage axial/paliers/carter non libérés ; contours schématiques'))
    # Front forks from existing study, not certified Tamiya geometry.
    path=ROOT/'Composants/paliers-transmission/3D/fourche-f-av-v3-etude.step';source(str(path.relative_to(ROOT)).replace('\\','/'))
    fork=cq.importers.importStep(str(path)).val()
    for sign,n in [(-1,'G'),(1,'D')]:
        p.append(('F_AV_'+n+'_etude_existante',fork.translate((sign*170,55,31.5)),ALU))
        p.append(('A7_'+n+'_gabarit',cyl(7,14,31.5,sign*163,55,axis=(sign,0,0)),BLACK))
        p.append(('Axe_avant_'+n+'_gabarit',cyl(2.5,30,31.5,sign*170,55,axis=(sign,0,0)),STEEL))
    p.append(envelope('FT90M_corps',23.3,12.1,21.45,0,80,14.2,BLACK,'servo-direction','Oreilles à Z31, supportC08 ; interface reconstruite à contrôler'))
    p.append(('Servo_palonnier_gabarit',box(24,6,2,(-5.7,80,38)),BLACK))
    # A front tie-rod corridor, not a kinematic certification or final M3 cut length.
    p.append(('Direction_biellette_gabarit',cyl(1.5,310,40,-155,70,axis=(1,0,0)),STEEL))
    for x in [-200,200]:
        for y in [55,445]:
            tire=cyl(31.5,26,31.5,x-13,y,axis=(1,0,0)).cut(cyl(22.5,26.2,31.5,x-13.1,y,axis=(1,0,0)))
            rim=cyl(22.5,25,31.5,x-12.5,y,axis=(1,0,0)).cut(cyl(2.6,25.2,31.5,x-12.6,y,axis=(1,0,0)))
            p.extend([('Pneu63x26_'+str(x)+'_'+str(y),tire,BLACK),('Jante_gabarit_'+str(x)+'_'+str(y),rim,STEEL)])
    # Reuse P1 camera cradle and light camera; single wood mast becomes an A2 gantry.
    for name,s,col in [('Berceau_P1_reutilise',cam.cradle(),BLUE),*cam.camera_and_spacers()[0],*cam.camera_and_spacers()[1]]:
        p.append(('Camera_'+name,cam.pitch(s,h=231,a=20).translate((0,482,0)),col))
    pivot=cyl(1.98,16,231,-36,482,axis=(1,0,0)).fuse(cyl(3.5,3,231,-39,482,axis=(1,0,0)))
    p.append(('Pivot_camera_M4_nominal',pivot,STEEL))
    source('Composants/support-camera/3D/berceau-camera-provisoire-p1.step')
    PLACEMENTS.append(dict(name='Camera_USB',x=0,y=482,pivot_z=231,pitch_down_deg=20,adjustment_height_above_deck=[190,230],folder='support-camera',status='BerceauP1, portique A2 métal ; USB sur montant, cadrage réel à tester'))
    return p

def validate(custom,equip):
    results={};over=[];feature_checks=[]
    # Check material exists around a drilling operation; STEP validity alone
    #cannot tell whether a "mounting hole" has been placed outside its plate.
    for d in PLATES:
        stock=profile(dict(d,features=[]));tools=[]
        for i,f in enumerate(d['features']):
            if f['type']=='hole':shape=cyl(f['d']/2,1,0,f['x'],f['y']);centers=[(f['x'],f['y'])];radius=f['d']/2
            elif f['type']=='slot':
                shape=cq.Workplane('XY').center(f['x'],f['y']).slot2D(f['length'],f['width'],f['angle']).extrude(1).val()
                a=math.radians(f['angle']);q=(f['length']-f['width'])/2
                centers=[(f['x']+u*math.cos(a),f['y']+u*math.sin(a)) for u in [-q,0,q]];radius=f['width']/2
            else:
                shape=box(f['w'],f['h'],1,(f['x'],f['y'],0),1);centers=[];radius=0
                for xx in [-f['w']/2-.6,f['w']/2+.6]:
                    for yy in [-f['h']/2-.6,f['h']/2+.6]:assert stock.isInside(cq.Vector(f['x']+xx,f['y']+yy,d['t']/2),1e-7),(d['code'],i,'window margin')
            for x,y in centers:
                for angle in range(0,360,15):
                    a=math.radians(angle)
                    assert stock.isInside(cq.Vector(x+(radius+.6)*math.cos(a),y+(radius+.6)*math.sin(a),d['t']/2),1e-7),(d['code'],i,'drill outside plate or edge web<.6')
            tools.append(shape)
        mindist=None
        for i,a in enumerate(tools):
            aa=a.BoundingBox()
            for j,b in enumerate(tools[i+1:],i+1):
                bb=b.BoundingBox()
                dx=max(0,aa.xmin-bb.xmax,bb.xmin-aa.xmax);dy=max(0,aa.ymin-bb.ymax,bb.ymin-aa.ymax)
                if math.hypot(dx,dy)>5:continue
                distance=a.distance(b)
                assert distance>=.8-1e-5,(d['code'],i+1,j+1,'insufficient web',distance)
                mindist=distance if mindist is None else min(mindist,distance)
        feature_checks.append(dict(piece=d['code'],features=len(tools),edge_web_sample_margin_mm=.6,minimum_checked_nearby_feature_web_mm=mindist))
    results['machining_feature_checks']=feature_checks
    for i,(n,a,_) in enumerate(custom):
        aa=a.BoundingBox()
        for m,b,_ in custom[i+1:]:
            bb=b.BoundingBox()
            if min(aa.xmax,bb.xmax)-max(aa.xmin,bb.xmin)<1e-6 or min(aa.ymax,bb.ymax)-max(aa.ymin,bb.ymin)<1e-6 or min(aa.zmax,bb.zmax)-max(aa.zmin,bb.zmin)<1e-6:continue
            vol=a.intersect(b).Volume()
            if vol>1e-5:over.append(dict(a=n,b=m,volume_mm3=vol))
    results['custom_part_overlaps']=over
    assert not over,over
    checked=[];component_over=[]
    prefixes=('B01_','ED80_','F0_','F1_','F2_','FP_','FAUX_','HS251_','D1D100_','D_plus_','D_moins_','UD80A_','ESC_','Pi5_PCB','M1P_','EVM60_','D42V','Pololu','WAGO')
    for n,a,_ in equip:
        if not n.startswith(prefixes):continue
        aa=a.BoundingBox()
        for m,b,_ in custom:
            bb=b.BoundingBox()
            if min(aa.xmax,bb.xmax)-max(aa.xmin,bb.xmin)<1e-6 or min(aa.ymax,bb.ymax)-max(aa.ymin,bb.ymin)<1e-6 or min(aa.zmax,bb.zmax)-max(aa.zmin,bb.zmin)<1e-6:continue
            vol=a.intersect(b).Volume()
            if vol>1e-5:component_over.append(dict(equipment=n,chassis=m,volume_mm3=vol))
        checked.append(n)
    assert not component_over,component_over
    results['selected_equipment_to_chassis']=dict(checked=checked,overlaps=component_over,does_not_validate_supplier_dimensions_or_cables=True)
    # Front cylindrical tire is tested throughout +/-30deg, at both steering
    # pivots. This proves chassis clearance for the chosen provisional offset30.
    fixed=[(n,s,c) for n,s,c in custom if not n.startswith(('S02','S01'))]
    rows=[]
    for sign in [-1,1]:
        tire=cyl(31.5,26,31.5,sign*200-13,55,axis=(1,0,0))
        for a in range(-30,31,2):
            swept=tire.rotate((sign*170,55,0),(sign*170,55,1),a)
            bb=swept.BoundingBox();vol=0
            for n,s,_ in fixed:
                sb=s.BoundingBox()
                if bb.xmax<=sb.xmin or bb.xmin>=sb.xmax or bb.ymax<=sb.ymin or bb.ymin>=sb.ymax or bb.zmax<=sb.zmin or bb.zmin>=sb.zmax:continue
                vol+=swept.intersect(s).Volume()
            assert vol<1e-5,(sign,a,vol)
            rows.append(dict(side=sign,angle_deg=a,overlap_mm3=vol))
    results.update(front_tire_clearance=rows,steering_limit_deg=30,steering_offset_provisional_mm=30,
        rear_tire_to_base_axial_gap_mm=187-182,rotor_to_deck_gap_mm=31.5-16-11,main_ground_clearance_mm=8,
        screw_head_ground_clearance_design_mm=4,ED80_bottom_to_deck_clearance_mm=15-11,
        support_Hall_relative_axle_height_mm=20.5,tray_under_clearance_over_battery_mm=81-38,
        carrier_and_EVM_separate=True,magnetic_or_structural_or_thermal_qualification=False,
        component_to_component_complete_fit_validated=False,transmission_and_front_hardware_are_unmeasured=True)
    # Conservative loading calculation, an engineering estimate, not a FEM result.
    # Two raw L25 angles, disregarding the plate's contribution to bending.
    A=25*3+22*3;zc=(75*1.5+66*14)/A
    I=25*3**3/12+75*(zc-1.5)**2+3*22**3/12+66*(14-zc)**2
    F=4*9.81*2/2;span=390;E=69000;M=F*span/4;stress=M*max(zc,25-zc)/I;deflection=F*span**3/(48*E*I)
    # Long rails end atY375, so a390-span beam is NOT the real support case.
    # Calculation retained as a material section comparison only; no validation.
    results['section_comparison_only']=dict(payload_assumption_kg=4,dynamic_factor=2,span_assumed_mm=span,L25_I_mm4=I,stress_MPa=stress,deflection_mm=deflection,not_actual_boundary_conditions=True)
    results['strap_square_envelope']=dict(length=250,loop_mm=2*(68+30),remaining_before_buckle_and_overlap_mm=250-2*(68+30))
    results['hardware_tested']=False
    dump(V/'conception.json',results);return results

def export_parts(custom,equip):
    metas=[]
    for filename,title,parts in [('chassis-a2-r1-nu.step','A2-R1 | chassis nu et portique',custom),('chassis-a2-r1-implante.step','A2-R1 | implantation, gabarits identifies',custom+equip)]:
        m=export_model(dict(folder='chassis',filename=filename,title=title,parts=parts,design=True,published=[],estimated=[
            'Custom chassis prototype; no machining, measurement or structural/thermal qualification.',
            'Equipment named reserve/gabarit is only an allocation envelope; not production CAD or a certified complete fit.',
            'Final purchased part holes, transmission internal mounting and actual front wheel offset remain to check on removable adapters.'],
            params=dict(plate=[300,520,3],wheelbase=390,wheel_center_track=400,ground_clearance=8,steering_limit_deg=30),
            probes=[],view=(.9,-1.4,1.05),source_pages=['../SPECIFICATIONS.md; ../PLAN-CONCEPTION.md; implantation.json; ../../image.png']))
        m.update(generated_on='2026-10-15',coordinate_system='X transversal, -Y marche avant, Z haut ; solZ0, plateauY0..520, rouesAV55/AR445. mm.',hardware_tested=False)
        dump(O/Path(filename).with_suffix('.json'),m);metas.append(m)
    # Individual flat stock STEP files are uncomplicated to edit or check at1:1.
    for d in PLATES:
        s=profile(d);cq.exporters.export(s,str(O/(d['code']+'.step')))
        # DXF must be genuinely2D atZ0, not at the top face's plate thickness.
        face=cq.Workplane('XY').newObject([s]).faces('>Z').translate((0,0,-d['t']))
        cq.exporters.export(face,str(P/(d['code']+'.dxf')),exportType='DXF')
        d['volume_mm3']=s.Volume()
        if d['material'].startswith('Al'):density=.00270
        else:density=.00091
        d['mass_kg_estimate']=s.Volume()*density/1000*d['qty']
    # Angle cross sections are true-size contours; drilling is a separate table.
    for name,a,b,t,L in [('L01-section',25,25,3,275),('L02-section',40,40,3,40),('L03-section',40,40,3,50)]:
        s=angle_section(a,b,t,1);cq.exporters.export(cq.Workplane('XY').newObject([s]).faces('>Z').translate((0,0,-1)),str(P/(name+'.dxf')),exportType='DXF')
    angle_dxf()
    dump(O/'provenance.json',dict(revision='A2-R1',models=metas,sources_sha256=SOURCES,generator='tools/build_chassis_r1.py',generator_sha256=sha(Path(__file__)),hardware_tested=False))
    return metas

def write_tables(custom):
    dump(B/'pieces.json',PLATES)
    dump(B/'implantation.json',dict(revision='A2-R1',unit='mm',axis='X transversal;-Y avant;Z haut; origine centre avant du plateau au sol',placements=PLACEMENTS,
        non_cut_supplier_holes='Report sur cassettes après contrôle du lot ; aucune empreinte fournisseur inconnue dans C01',
        drive_train_internal_stack='Réservation châssis. Les arbres50mm et supports historiques restent des études ; ne pas les fabriquer depuis ces anciens STEP.'))
    with (P/'percages-et-decoupes.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f,delimiter=';');w.writerow(['piece','feature','type','x_mm','y_mm','diametre_mm','longueur_mm','largeur_mm','angle_deg','usage'])
        for d in PLATES:
            for i,h in enumerate(d['features']):w.writerow([d['code'],i+1,h['type'],h['x'],h['y'],h.get('d',''),h.get('length',h.get('w','')),h.get('width',h.get('h','')),h.get('angle',''),h['role']])
        for code,ww,hh,features in angle_templates():
            for i,h in enumerate(features):w.writerow([code,i+1,h['type'],h['x'],h['y'],h.get('d',''),h.get('length',''),h.get('width',''),h.get('angle',''),h['role']])
    stock=[['L01','Cornière25 x25 x3, longueur275','Al6061T6 ou6082T6',2,'Pied:3 trousØ4.5, centre à15 du talon extérieur, stations20/115/255 depuis coupe avant'],
           ['L02','Cornière40 x40 x3, longueur40','Al6061T6 ou6082T6',2,'Semelle:Ø4.5, X10/30, à15 du bord avant; vertical: X20, Z15/31 depuis dessous semelle'],
           ['L03','Cornière40 x40 x3, longueur50','Al6061T6 ou6082T6',1,'Aile pivot: slot44.5x4.5, centre Y13,Z25 depuis bord avant/bas; aile arrière:Ø4.5 àX15/35,Z35'],
           ['T01','TubeØ10, alésageØ4.5, L70','Al6061T6',4,'Coupe droite, faces parallèles ;70±0.10'],
           ['T02','TubeØ10, alésageØ4.5, L56','Al6061T6',4,'Coupe droite, faces parallèles ;56±0.10'],
           ['N01','Entretoises servo:2x17.5 et2x20, passageM2.5','Nylon du kit existant à recouper',4,'Avant sur traverse2.5 ; arrière sur plateau ; toutes les faces hautesZ31'],
           ['N02','Cales3, diamètre6, passageM3/M4','PP/nylon',sum(n.startswith('N02') for n,_,_ in custom),'Sous cassettes, seulement hors longeron'],
           ['S01','Patin140 x46 x2','Silicone existant',1,'Recoupe à la règle, pas laser'],
           ['S02','Bande260 x15 x6','Mousse EVA',1,'Bord avant, collage ; pas de capacité d’absorption chiffrée']]
    with (B/'liste-debit.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f,delimiter=';');w.writerow(['piece','description','matiere','quantite','notes'])
        for d in PLATES:w.writerow([d['code'],f"{d['label']} / brut {d['w']}x{d['h']}x{d['t']}",d['material'],d['qty'],'Contours et trous DXF ; voir PDF'])
        w.writerows(stock)
    return stock

def line(c,x,y,a,b,col='#244f68',width=.6):c.setStrokeColor(colors.HexColor(col));c.setLineWidth(width);c.line(x*mm,y*mm,a*mm,b*mm)
def typography(s):
    s=re.sub(r'(?<=[a-zéèêàù])(?=\d)', ' ',str(s))
    s=re.sub(r'(?<=\d)(?=(?:mm|kg|min|km|octobre|au|de|sur|à|et|par)\b)', ' ',s)
    return s
def text(c,x,y,s,size=8,bold=False,col='#243441'):
    c.setFillColor(colors.HexColor(col));c.setFont('HV3B' if bold else 'HV3',size);c.drawString(x*mm,y*mm,typography(s))
def wrap(c,x,y,s,width=115,size=8,leading=4):
    from reportlab.pdfbase.pdfmetrics import stringWidth
    words=typography(s).split();row=''
    for word in words:
        trial=(row+' '+word).strip()
        if stringWidth(trial,'HV3',size)>width*mm and row:text(c,x,y,row,size);y-=leading;row=word
        else:row=trial
    if row:text(c,x,y,row,size);y-=leading
    return y
def header(c,title,sub):
    c.setPageSize(landscape(A3));text(c,16,277,title,21,True);text(c,16,267,sub,9)
    line(c,16,261,404,261,col='#b9cbd4')
def foot(c,page):
    line(c,16,15,404,15,col='#b9cbd4');text(c,16,9,'DRONE V3 | A2-R1 | 15 octobre 2026 | mm | conception prototype non testée',7)
    text(c,390,9,str(page),8)

def draw_plate(c,d,x0,y0,scale,labels=True):
    # All graphical positions are drawn from exactly the CAD parameters.
    def pt(x,y):return (x0+x*scale)*mm,(y0+y*scale)*mm
    c.setLineWidth(.55);c.setStrokeColor(colors.HexColor('#174969'));c.setFillColor(colors.HexColor('#edf3f6'))
    if d['outline']:
        path=c.beginPath();path.moveTo(*pt(*d['outline'][0]))
        for q in d['outline'][1:]:path.lineTo(*pt(*q))
        path.close();c.drawPath(path,stroke=1,fill=1)
    else:c.roundRect(x0*mm,y0*mm,d['w']*scale*mm,d['h']*scale*mm,d['r']*scale*mm,stroke=1,fill=1)
    for i,f in enumerate(d['features']):
        xx,yy=pt(f['x'],f['y']);c.setFillColor(colors.white)
        if f['type']=='hole':c.circle(xx,yy,f['d']/2*scale*mm,stroke=1,fill=1)
        elif f['type']=='slot':
            c.saveState();c.translate(xx,yy);c.rotate(f['angle']);c.roundRect(-f['length']/2*scale*mm,-f['width']/2*scale*mm,f['length']*scale*mm,f['width']*scale*mm,f['width']/2*scale*mm,stroke=1,fill=1);c.restoreState()
        else:c.roundRect(xx-f['w']/2*scale*mm,yy-f['h']/2*scale*mm,f['w']*scale*mm,f['h']*scale*mm,scale*mm,stroke=1,fill=1)
        if labels:
            text(c,xx/mm+1,yy/mm+1,str(i+1),5,col='#58636b')
    # Main stock dimensions and datums. Local feature coordinates are in CSV.
    w=d['w']*scale;h=d['h']*scale
    line(c,x0,y0-5,x0+w,y0-5);line(c,x0,y0-7,x0,y0-3);line(c,x0+w,y0-7,x0+w,y0-3)
    text(c,x0+w/2-4,y0-4,d['w'],7)
    line(c,x0+w+5,y0,x0+w+5,y0+h);line(c,x0+w+3,y0,x0+w+7,y0);line(c,x0+w+3,y0+h,x0+w+7,y0+h)
    text(c,x0+w+7,y0+h/2,d['h'],7);text(c,x0,y0-12,'O(0;0) - bas gauche du brut',7)

def pdf(stock,metas):
    path=P/'plans-chassis-a2-r1.pdf';c=canvas.Canvas(str(path),pagesize=landscape(A3));c.setTitle('Drone V3 - Châssis A2-R1 - plans de découpe et implantation')
    page=0
    def finish():
        nonlocal page
        page+=1;foot(c,page);c.showPage()
    header(c,'Châssis A2-R1 - plateau ouvert','Plan de conception et découpe | Photo A2 comme référence de forme | aucune recherche ni nouvelle sélection de pièce en ligne')
    c.drawImage(str(O/'chassis-a2-r1-implante.png'),15*mm,31*mm,width=235*mm,height=191*mm,preserveAspectRatio=True,anchor='c',mask='auto')
    y=244
    for a,b in [('Plateau','520 x300 x3, aluminium5754 H22'),('Roues / empattement','Ø63 x26 ;390 entre axes ; voie400 au neutre, hypothèse de déport'),('Pont central','160 x250 x2 ; sous-faceZ81, démontable'),('Caméra','Portique métallique2 montants ; pivotZ231, regard vers-Y, déclinaison20°'),('Architecture','2 moteurs arrière ;2 roues avant directrices libres ; pas de suspension'),('Cassettes','Isolantes et remplaçables, cotes fournisseur inconnues reportées après présentation')]:
        text(c,262,y,a,10,True);y=wrap(c,262,y-6,b,138,9,4.5)-8
    wrap(c,262,y,'Le modèle implanté mélange les pièces de châssis exactes et des gabarits nommés. Les plans fabriquent le châssis ; ils ne libèrent pas l’usinage des anciens arbres ou le montage interne du train roulant.',137,9,4.8)
    finish()
    header(c,'Implantation - deux niveaux distincts','Dessus du plateau et dessus du pont | coordonnées globales dans implantation.json | rectangles = réservations, pas des interfaces fournisseur')
    def mapbox(x0,y0,sc,x,y,w,h,label,color='#e1ebf0'):
        c.setStrokeColor(colors.HexColor('#174969'));c.setFillColor(colors.HexColor(color))
        c.rect((x0+(x-w/2)*sc)*mm,(y0+(y-h/2)*sc)*mm,w*sc*mm,h*sc*mm,stroke=1,fill=1)
        text(c,x0+x*sc-w*sc/2+1,y0+y*sc-1,label,6.5,True)
    # Whole floor diagram; map origin is globalX0,Y0, not stock lower left.
    x0=97;y0=35;sc=.36
    mapbox(x0,y0,sc,0,260,300,520,'','#f7f9fa')
    floor=[(-95,140,59,58,'ED80'),(75,140,120,60,'F0'),(-10,145,40,30,'AC03/XH'),(0,190,25,20,'IC5'),(0,270,46,139,'G1'),
        (-112,227,52.324,85.344,'HS/SSR'),(-87,285,106.68,22.86,'D+'),(-87,320,106.68,22.86,'D-'),(108,368,30.1,69.1,'UD80'),
        (-47,376,33.4,26.8,'ESC G'),(47,376,33.4,26.8,'ESC D'),(0,80,23.3,12.1,'SERVO')]
    floor += [(x,262,22,85,t) for x,t in [(50,'F1'),(75,'F2'),(100,'FP'),(125,'FA')]]
    for q in floor:mapbox(x0,y0,sc,*q)
    for x in [-200,200]:
        for y in [55,445]:mapbox(x0,y0,sc,x,y,26,63,'R','#d2d7db')
    text(c,20,250,'NIVEAU BAS - plateauZ8..11',11,True)
    text(c,20,25,'Avant vers le bas du dessin. G1 = batterieIC5. FA = fusible auxiliaire de surveillance.',8)
    # Upper deck occupies its actual Y180..430 position, independently enlarged.
    x0=295;y0=-80;sc=.75
    mapbox(x0,y0,sc,0,305,160,250,'','#f7f9fa')
    upper=[(0,307.5,140,75,'M1P'),(-38,230,60,60,'EVM1'),(38,230,60,60,'EVM2'),(7.5,378,85,56,'Pi5'),
        (-57.5,388,25.4,25.4,'REG'),(0,187,18,13,'2831'),(30,190,21,18,'2813'),(-30,420,18.8,18.6,'5V'),
        (-24,388,30,18.6,'GND*'),(-60,325,18.8,18.6,'IN+*'),(-35,325,18.8,18.6,'IN-*')]
    for q in upper:mapbox(x0,y0,sc,*q)
    text(c,235,250,'PONT CENTRAL - sous-faceZ81',11,True)
    wrap(c,235,40,'* WAGO au niveau du pont, sous les PCB sur entretoises : la superposition en plan ne signifie pas une collision. Déposer le PCB pour accéder aux leviers. Vérifier les soudures et leurs dégagements réels.',160,8.5,4.5)
    wrap(c,180,225,'Batterie accessible par l’avant après ouverture des sangles. BoutonED80 en accès direct sur le pod. Les modulesTI restent séparés du PCB de surveillance.',43,8.5,4.5)
    finish()
    header(c,'01 - plateau principal C01','Al5754 H22, épaisseur3 | vue de dessus à1:2.5 | découpe C01.dxf, coordonnées exhaustives dans percages-et-decoupes.csv')
    draw_plate(c,PLATES[0],25,35,.4)
    y=245
    lines=[('Repères absolus','X=0 axe médian, Y=0 bord avant ; le CSV local C01 utiliseX_local=X+150. SolZ0, plateauZ8..11.'),
        ('Contour','300 x520,4 rayonsR12. Chanfrein de finition0.3 sur arêtes, ébavurer chaque trou et lumière.'),
        ('Train avant','PivotX=±170,Y55 ; traverseC03 sur le plateau. Roues au neutreX=±200. Limite de conception±30°, à régler mécaniquement/logiciellement.'),
        ('Train arrière','SortiesY445,Z31.5 ;4 trous de fixation par cassetteC04 ; entraxes réglables, pas de trou fabricant inventé.'),
        ('Pont','4 piliersX=±72,Y194/408 ;70mm entre dessus du plateau et dessous du pont.'),
        ('Batterie','Centre(0;270), pack139 x46 x25, patin2 ; butées réglées pour environ1.5mm de jeu longitudinal par côté.'),
        ('Sangles','4 lumières23 x3.5, centresX=±34,Y230/310. Colliers et sangles ne doivent jamais frotter sur métal brut.'),
        ('Capteurs','Pieds P1 surX=±74,Y435/455 ; faces rotorX=±103. Tête abaissée3.5 depuis l’étudeH24 : H20.5 sur ce châssis.'),
        ('Garde au sol','8mm nominal sous plateau ; réserver4mm maximum sous le plateau pour têtes/rondelles. La bande de sangle descend àZ6.8, avant flèche et tolérances.')]
    for a,b in lines:text(c,184,y,a,9,True);y=wrap(c,184,y-5,b,213,8.5,4.4)-5
    finish()
    header(c,'02 - pont C02 et traverse avant C03','Pièces usinées à plat ;1:1 sur DXF | aucune correction de rayon d’outil incluse')
    d=next(d for d in PLATES if d['code']=='C02');draw_plate(c,d,20,48,.77)
    text(c,20,245,'C02 - Al5754 H22,2mm',11,True)
    d=next(d for d in PLATES if d['code']=='C03');draw_plate(c,d,181,180,.59);text(c,181,245,'C03 - Al6061 T6,2.5mm',11,True)
    y=152
    for s in ['C02 : fixations Pi5 au rectangle58 x49 ;4 trousØ2.7. PCB origine globale(-35;350), dessous àZ98 sur entretoises15.',
              'Passage18 x4 sous le GPIO pour les fils ; souder le Pi hors châssis avant montage. Régulateur voisin surC10 ;2 positifs et4 retours de sortie ≤50mm restent à fabriquer et contrôler.',
              'M1P : origine globale(-70;270),4 trous aux(4;4),(136;4),(4;71),(136;71) du PCB. Ne pas confondre ces trous avec ceux des modules TI.',
              'Deux EVM sur des cassettesC09 séparées. Leur réservation60 x60 x12 n’est pas une cote de montage garantie.',
              'C03 : oreilles pour fourches F-AV existantes ; épaisseur2.5 choisie pour axe roueZ31.5 avec leur hauteur nominale18. Contrôler l’interface réelle avant percer les fourches.']:
        y=wrap(c,181,y,s,218,9,4.8)-6
    finish()
    # Each adapter page groups four pieces, with a readable geometry and concise
    # hole table. CSV+DXF remain exact even when the print is reduced.
    groups=[['C04G','C04D','C05','C06'],['C07','C08','C09','C10'],['C11G','C11D','C12','C13'],['C14','C15','C16','C17']]
    for group in groups:
        header(c,'03 - pièces à plat : '+', '.join(group),'Contours1:1 dans DXF et STEP individuels | numéros de détails = lignes du CSV par pièce | quantités dans liste-debit.csv')
        for j,code in enumerate(group):
            d=next(d for d in PLATES if d['code']==code);x=20+(j%2)*198;y=145-(j//2)*112
            sc=min(.7,85/d['w'],74/d['h']);draw_plate(c,d,x,y,sc)
            xx=x+100;yy=y+65;text(c,xx,yy,code+' - '+str(d['qty'])+' pièce(s)',10,True)
            yy=wrap(c,xx,yy-6,d['label'],88,9,4.5)-2
            yy=wrap(c,xx,yy,f"{d['material']} ; brut {d['w']} x {d['h']} x {d['t']}",88,8.5,4.5)-3
            if code in ['C04G','C04D']:note='4 lumières15 x4.5 ; encoche pour support Hall. Perçages propres aux paliers, carter et platine moteur : à reporter après empilage réel.'
            elif code in ['C05','C06','C12','C13','C14']:note='4 trousØ3.5 de cassette. Fixations du composant à relever sur le lot, puis percer cette pièce seule. Aucune fixation par colle seule en puissance.'
            elif code=='C09':note='2 cassettes TI identiques72 x72 ;4 trousØ3.5 et2 lumières20 x3. Maintien isolant souple sur entretoises, sans effort sur composants.'
            elif code=='C07':note='ED80 : centreØ25,2 trousØ5.5 entraxe48 ;4 trousØ4.5 pour tubes. Sous-face de montageZ70, dessus73 ; borne inférieureZ15.'
            elif code=='C08':note='Fenêtre24 x13 ;2 trousØ2.2 entraxe28.5 et4 trousØ2.7 rectangle46 x24. Tabulation FT90M reconstruite à vérifier.'
            else:note='Positions et diamètres exhaustifs dans CSV. Ébavurer, garder les pièces isolantes démontables et vérifier les chants contre les câbles.'
            wrap(c,xx,yy,note,88,8,4.3)
        finish()
    header(c,'04 - portique arrière conforme au principe A2','Deux montants métal, traverse, goussets de pied | berceauP1 réutilisé ; ancien support bois conservé comme variante')
    for code,x,y,sc in [('C18',22,41,.78),('C19',98,210,.95)]:
        d=next(d for d in PLATES if d['code']==code);draw_plate(c,d,x,y,sc);text(c,x,245,f"{code} - {d['qty']}x - {d['material']} - ép.{d['t']}",10,True)
    y=180
    for s in ['C18 :2 montants25 x230 x6, trousØ4.5 à12/28/212/224 depuis le pied ; axe médian à12.5 du chant. Pied du montantZ14, sommetZ244.',
              'C19 :284 x25 x3 ;4 trous auxX14/270 etY7/19 ;2 trousX122/142,Y12 pourL03. TraverseY509..512, face avant.',
              'L02 :2 pieds en cornière40 x40 x3, débit40. Semelle surZ11, deY472 à512 ; montants contre aile verticale. Positions absoluesX±128.',
              'L03 :cornière40 x40 x3, débit50. Aile côté berceau avec lumière44.5 x4.5, centres utilesZ201..241. Pivot choisiZ231, soit220 au-dessus du plateau.',
              'PivotM4 horizontal, rondelle de friction isolante, berceau existant à20° vers le bas. Verrouiller l’inclinaison après essai. USB fixé le long d’un montant, boucle de service près du pivot.',
              'La géométrie réserve une caméra à l’arrière qui regarde vers l’avant. La couverture de toute la plateforme et de la route reste à vérifier à l’image réelle.']:
        y=wrap(c,98,y,s,290,9,4.8)-7
    finish()
    header(c,'05 - débit et perçage des profilés','Profilés bruts choisis pour fabrication ; pas de lien d’achat ou prix inventé | aucune opération de pliage nécessaire')
    y=247
    for code,desc,mat,qty,note in stock:
        text(c,20,y,code,10,True);text(c,40,y,f'{qty}x  {desc} | {mat}',10)
        y=wrap(c,40,y-6,note,350,8.5,4.4)-8
    wrap(c,20,40,'Les sections DXF L01/L02/L03 décrivent des L idéaux sans rayon de filage. Relever les rayons intérieurs réels, garder les vis hors du congé et reprendre les chants si nécessaire. Ne pas usiner une cornière pleine à partir du contour de section comme une pièce plate.',370,9,4.7)
    finish()
    header(c,'06 - montage, contrôle et limites','Fichiers de fabrication du châssis ; mise en service et performances à qualifier séparément')
    y=246
    steps=[('1. Préparer','Contrôler épaisseurs et planéité des bruts. Fraiser/contourner les pièces ; percer, ébavurer et casser les arêtes0.3. Contrôle dimensionnel des deux diagonales du plateau et des4 appuis du pont.'),
        ('2. Monter la structure','Longerons puis traverse avant, cassettes arrière, pieds et portique. Assembler sans contrainte ; toutes les surfaces d’appui doivent porter. Vis et écrous freinés selon nomenclature finale ; pas de têtes dépassant de plus de4 sous le plateau.'),
        ('3. Présenter les organes','Poser4 roues,2 transmissions et direction ; contrôler déport réel, paliers et jeux. Les anciens arbres de50mm ne sont pas libérés par ce plan. Percer uniquement les cassettes pour les interfaces non cotées, puis compléter carters des engrenages avant entraînement.'),
        ('4. Électricité et batterie','Monter supports isolants, cassettes et ED80 sur son pod. Aucun retour par aluminium. Batterie sur silicone,2 sangles et butées ; pas de vis saillante vers le pack. Les chargeurS65, cordon de charge et outillage restent hors véhicule.'),
        ('5. Câbles','LAPP6mm² : rayon fixe≥30, conducteurs espacés et ventilés. Conserver positif d’origine≥85 et extension≥120 avantF0. Passages protégés, petites embases vissées sur cassettes, aucun fil près des pneus ou dents ; câble USB séparé des phases moteurs.'),
        ('6. Vérifier','À la main : braquage±30, rotation complète, déplacement des supports Hall, accès au bouton et retrait du pack. Contrôler les jeux avec fils et connecteurs réels, puis sous faible énergie au banc. Mesurer échauffement, flèche, vibration et rétention avant roulage progressif.')]
    for a,b in steps:text(c,20,y,a,10,True);y=wrap(c,20,y-6,b,378,9,4.8)-8
    y-=3
    y=wrap(c,20,y,'Tolérances proposées : contours±0.3mm, centres de fixation±0.15mm, diamètres de passage +0.2/0mm ; épaisseurs réelles à relever. Les DXF sont en mm à100%, sans compensation de fraise ni G-code. Pour les fenêtresR1, fraiseØ2 ou adaptation du rayon après contrôle des jeux.',378,9,4.8)-6
    wrap(c,20,y,'Les objectifs40km/h,10-20min à40 et45min à20, ainsi que1080p60/Wi-Fi, restent ceux du projet. Ni une CAO, ni le choix d’aluminium ne valident ces performances. Masse à peser, comportement et freinage à mesurer. La prochaine étape est la visserie finale, puis fabrication et essais.',378,9,4.8)
    finish();c.save()
    doc=pymupdf.open(path);tmp=ROOT/'tools/temp/chassis-r1/pdf';tmp.mkdir(parents=True,exist_ok=True)
    for i,pg in enumerate(doc):pg.get_pixmap(matrix=pymupdf.Matrix(1,1)).save(tmp/f'page-{i+1}.png')
    dump(path.with_suffix('.json'),dict(pages=len(doc),sha256=sha(path),visual_review_completed=False,renders=[str((tmp/f'page-{i+1}.png').relative_to(ROOT)).replace('\\','/') for i in range(len(doc))]))
    return len(doc)

def docs(stock,metas):
    totalplate=sum(d['mass_kg_estimate'] for d in PLATES)
    write(B/'README.md',f'''# Châssis A2-R1 - plateau ouvert

Conception du15 octobre2026 à partir de la [photo retenue](../../../image.png), des dossiers locaux et des spécificationsV3. Aucune recherche de pièce ni achat en ligne. Les matériaux, dimensions et interfaces propres au châssis sont choisis ici. Prototype non fabriqué, non testé.

- **Plateau520 x300 x3mm**, aluminium5754 H22 ;4 anglesR12,2 longerons en cornière25 x25 x3, longueur275.
- **Empattement390mm**, rouesØ63 x26, axes avantY55 et arrièreY445. Centres de rouesX±200 : voie400mm supposant un déport avant de30mm. Encombrement droit426mm en largeur ; réserver450mm au braquage±30°. Ce déport reste à contrôler sur roues/moyeux réels.
- **Garde au sol nominale8mm** sous plateau, avant têtes de vis, sangles, déformation et tolérances. Têtes sous plateau≤4mm. SolZ0, dessus du plateauZ11, axesZ31.5.
- BatterieG1 IC5 au centre et en bas ;2 sangles20 x250, patin140 x46 x2 et butées. Pont électronique160 x250 x2, démontable, sous-faceZ81.
- Deux moteurs arrière et deux roues avant directrices non motrices. Transmissions sur cassettes séparées, supports HallP1 repris avec H20.5mm.
- **Portique caméra métallique à2 montants**, comme la photoA2, réutilisant le berceauP1. Le montant/base bois du supportP1 restent une variante. Pivot arrière(0;482;231), déclinaison20°, réglage190-230 au-dessus du plateau.

## Fichiers

[Dossier de plans PDF](plans/plans-chassis-a2-r1.pdf) · [STEP et aperçus](3D/README.md) · [Découpe DXF](plans/README.md) · [Liste de débit](liste-debit.csv) · [Tous les perçages/contours](plans/percages-et-decoupes.csv) · [Pièces paramétrées](pieces.json) · [Implantation](implantation.json) · [Contrôles de conception](verification/conception.json).

Le PDF cote les bruts et décrit les perçages. Le CSV donne **chaque centre, diamètre et lumière** ; origine locale au coin bas gauche du rectangle brut de chaque pièce. Le DXF1:1 est généré depuis les mêmes solides que les STEP : aucune conversion d’image ou mise à l’échelle arbitraire. PourC01 : X_local=X_global+150, Y_local=Y_global. Pour toutes les autres pièces, voir origine/pose dans pieces.json.

## Matériaux et fabrication

5754H22 pour plateau/pont,6061T6 ou6082T6 pour traverse avant, montants et cornières. Pas de pliage à faire : cornières brutes coupées, percées et assemblées. PP compact pour les cassettes électriques ; nylon pour les petites cales et entretoises, silicone sous batterie. Le plastique doit être compatible avec température, serrage et isolation de l’équipement : aucun classement thermique/feu inventé.

Découpe CNC et perçage proposés ; aucune trajectoire d’outil ni machine supposée compatible. Brider sans déformer, laisser les attaches nécessaires, finir les chants. Fenêtres àR1 : fraiseØ2 ou reprise adaptée après contrôle. Contours±0.3, centres±0.15, trous de passage+0.2/0 sont des exigences de conception à vérifier avec l’atelier. Les rayons internes des cornières brutes ne sont pas représentés dans les L idéaux.

Masse des seules pièces plates estimée **{totalplate:.3f}kg**, avecρaluminium2700kg/m³ etρPP910kg/m³, avant vis, profilés, équipements et câbles. Ce n’est pas la masse du véhicule. Aucun devis ou gain d’autonomie déduit de la CAO.

## Interfaces et essais restants

Le plateau principal porte les trous des **cassettes**, pas les trous supposés des nouveaux supports de fusibles. Les interfaces fournisseur encore incertaines sont à relever puis percer sur ces seules pièces démontables. Les gabaritsF0 et4 supportsKLKD sont des **réservations choisies**, pas des modèles constructeur ; confirmer leurs dimensions avant usiner leurs cassettes. FAUX de surveillance est inclus, sans oublier les3 résistances de mesure et les raccordements locaux.

La porteuseM1P140 x75 et ses quatre fixations sont reprises ; les2EVM sont réservés **séparément** sur deux cassettes isolantes. Le modulePololu2831, le2813, leD42V55F5, les WAGO et les dégagements d’accès aux pads Pi sont prévus. Ne pas utiliser les gabarits EVM superposés de l’ancien assemblage comme des modules réels fixés au PCB.

Le modèle implanté garde les composants simplifiés et nommés pour s’ouvrir rapidement : les filetages des rails, le relais/dissipateur et la coupure utilisent des gabarits allégés, avec les cotes extérieures des dossiers. ED80 : corps sous la face inférieure du panneauZ70, dessus du panneauZ73, extrémité des bornesZ15, soit4mm au-dessus du plateau. Le châssis nu et ses pièces plates sont les références de fabrication. Les engrenages sont des contours d’encombrement sans denture ; **empilage des arbres, retenues, fixations des paliers, platine moteur, carters et cinématique de direction restent à qualifier** à partir du montage réel. Les anciens arbres50mm sont des études, pas des axes à fabriquer. La sélection Losi/KHK conserve sa vérification d’appairage restante ; aucune vitesse réelle garantie.

Les contrôles de rotation portent sur les pneus et le châssis aux positions de conception. Ils n’incluent pas les fils ni toutes les pièces d’articulation non mesurées. Vérifier aussi la flexion du portique, les têtes sous plateau, le glissement du pack, l’accès aux protections et la convection du HS251. Le plateau métallique ne sert jamais de retour électrique. S65 et cordons de charge restent hors véhicule.

Conserver le rayon fixe≥30mm du SiF6mm² et les deux longueurs minimales≥85mm/≥120mm avantF0. Les fils de sortie5V du régulateur vers le Pi restent≤50mm, à contrôler sur le faisceau déployé. Câbles espacés, maintenus sur isolant, éloignés des roues/engrenages. Les parties tournantes doivent recevoir leurs carters avant entraînement ; ces derniers dépendent de l’empilage réel.

Le dossier permet de découper la **structure de prototype**, puis de faire les reports d’interface au montage à blanc. Il ne constitue pas une libération du véhicule complet à40km/h. Les objectifs d’autonomie, vidéo et liaison Wi-Fi restent inchangés et à mesurer. [Ordre du projet](../../PLAN-CONCEPTION.md) : prochaine étape, visserie finale.
''')
    write(P/'README.md','''# Plans A2-R1

[Plans cotés PDF](plans-chassis-a2-r1.pdf), [tous les centres et découpes CSV](percages-et-decoupes.csv), [débit et quantités](../liste-debit.csv).

Un fichier DXF par pièceC01 àC19, avec G/D distincts lorsque nécessaire. C09x2,C16x2,C17x4 etC18x2 sont identiques : découper la quantité indiquée. C11G/D ont le même contour mais sont indexés pour leur emplacement. Les contours exportés contiennent réellement les trous/lumières ; toutes les unités sont des millimètres. Les sectionsL01/L02/L03 sont les profils de cornières brutes, pas des développés de tôles pliées.

Pour les cornières, cinq DXF supplémentaires de gabarits de perçage par aile :L01-semelle,L02-semelle,L02-verticale,L03-arriere,L03-pivot. Usiner seulement le calquePERCAGE sur la cornière déjà débitée. Le rectangle grisREFERENCE_AILE_NE_PAS_DECOUPER est un repère ; ne pas le traiter comme un contour à découper. Origines de ces faces expliquées dans le CSV et le débit.

Pas de G-code, de compensation outil ni de nidification matière imposée. Positionner les bruts selon les courses et le bridage de la CNC. Les trous fournisseur inconnus ne sont pas dans le plateau ; report sur les cassettes après présentation. Les fenêtresR1 réclamentØ2 ou une adaptation de rayon contrôlée.

Les identifiants et numéros de détail du PDF correspondent exactement au CSV. Celui-ci donne longueur totale de lumière (extrémité à extrémité), largeur et angle positif antihoraire depuisX. Le0 du dessin est le coin bas gauche du brut, y compris pour les contours non rectangulaires. Aucun PDF à imprimer en«ajuster» pour en déduire des dimensions ; prendre les cotes ou le DXF1:1.
''')
    write(O/'README.md','''# CAO A2-R1

- [Châssis nu](chassis-a2-r1-nu.step) : structure, cassettes, portique, cales et patin ; [aperçu](chassis-a2-r1-nu.png).
- [Implantation avec composants allégés](chassis-a2-r1-implante.step) : roues, électronique, Hall, caméra et réservations ; [aperçu](chassis-a2-r1-implante.png).
- C01.step àC19.step : pièces plates seules, repère local du DXF et de pieces.json. G/D gardent leurs identifiants distincts.

Les noms «reserve»,«gabarit» et«enveloppe» identifient les équipements non représentés au détail ou non cotés. Ne pas les envoyer à usiner. Pi/cooler sont volontairement simplifiés ; les gros fichiers détaillés d’origine ne sont pas copiés dans l’assemblage. Les gabarits d’engrenages n’ont pas de dents et ne libèrent aucun empilage interne.

Les anciennes pièces ne sont pas écrasées : provenance etSHA256 dans [manifest](provenance.json). [Contrôles indépendants FreeCAD](validation-freecad.json) et [cohérence des fichiers](../verification/fichiers.json). Les contrôles CAO ne sont pas des essais matériels.
''')

def main():
    sys.stdout.reconfigure(encoding='utf-8');ap=argparse.ArgumentParser();ap.add_argument('--docs-only',action='store_true');args=ap.parse_args()
    for d in [B,O,P,V]:d.mkdir(parents=True,exist_ok=True)
    source('SPECIFICATIONS.md');source('PLAN-CONCEPTION.md');source('Composants/verification-alimentation/selection-active.json');source('Composants/carte-surveillance-electrique/cotes.md');source('Composants/cordon-principal-batterie/references/SPMX50002S30H5-rcteam.json')
    make_design();custom=custom_parts();equip=equipment()
    if args.docs_only:
        metas=json.loads((O/'provenance.json').read_text(encoding='utf-8'))['models']
        for d in PLATES:d['volume_mm3']=profile(d).Volume();d['mass_kg_estimate']=d['volume_mm3']*(.0027 if d['material'].startswith('Al') else .00091)/1000*d['qty']
    else:
        validate(custom,equip);metas=export_parts(custom,equip)
    stock=write_tables(custom);docs(stock,metas);pages=pdf(stock,metas)
    print('DONE A2-R1:',len(PLATES),'flat designs;',len(custom),'custom solids entries;',pages,'PDF pages',flush=True)

if __name__=='__main__':main()
