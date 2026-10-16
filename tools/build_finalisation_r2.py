"""R2 theoretical closure. New deliverables only; R1 fabrication kit is preserved.

Run in tools/temp/cad-env. Sources, hypotheses and unverified interfaces are
kept separate. No hardware qualification or manufacturer response is invented.
"""
from pathlib import Path
import csv, json, math, hashlib, sys, time, html, urllib.request
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import cadquery as cq
import ezdxf
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pymupdf
from study_finalisation_r2 import calculate, end, drag_end
from build_running_gear_step import box,cyl

ROOT=Path(__file__).resolve().parents[1]
B=ROOT/'Composants/finalisation-theorique-r2'
OUT=B/'3D'; PL=B/'plans'; V=B/'verification'
for d in [B,OUT,PL,V,B/'references',B/'routage',ROOT/'Composants/visserie-finale',ROOT/'Assemblage/R2']:
    d.mkdir(parents=True,exist_ok=True)
PARTS=[]; SPECS=[]; FAST=[]; ROUTES=[]
AL=(.56,.60,.65); STEEL=(.4,.44,.48); BLACK=(.035,.045,.06); BLUE=(.02,.16,.31); ORANGE=(.85,.24,.02)

def write(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t.strip()+'\n',encoding='utf-8')
def dump(p,t):write(p,json.dumps(t,indent=2,ensure_ascii=False))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def csvout(p,rows,fields=None):
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]),delimiter=';');w.writeheader();w.writerows(rows)

def part(code,s,color=AL,qty=1,description='',material='6082-T6',dimensions=''):
    if not s.isValid() or not all(a.Closed() for a in s.Shells()):
        print('INVALID',code,'valid',s.isValid(),'solids',len(s.Solids()),'shells',[a.Closed() for a in s.Shells()],flush=True)
        cq.exporters.export(s,str(ROOT/'tools/temp'/('debug-'+code+'.brep')))
        raise ValueError(code)
    cq.exporters.export(s,str(OUT/(code+'.step')))
    SPECS.append(dict(code=code,description=description,quantity=qty,material=material,dimensions=dimensions,solid_count=len(s.Solids()),volume_mm3=s.Volume()))
    return s

def put(name,s,col=AL,group='mecanique'):
    PARTS.append((name,s,col,group));return s

def xring(ro,ri,length,x,y=0,z=31.5):
    return cyl(ro,length,z,x,y,axis=(1,0,0)).cut(cyl(ri,length+.2,z,x-.1,y,axis=(1,0,0)))

def circlip5(x,y):
    # DIN471-5 nominal0.6mm; ear outline is reconstructed inside the10.3mm
    # published mounting-clearance envelope, not a profile to manufacture.
    s=xring(3.5,2.4,.6,x,y)
    for yy in [y-2.1,y+2.1]:s=s.fuse(cyl(1.2,.6,28.2,x,yy,axis=(1,0,0)))
    s=s.cut(box(.8,1.3,5,(x+.3,y,26)))
    for yy in [y-2.1,y+2.1]:s=s.cut(cyl(.5,.8,28.2,x-.1,yy,axis=(1,0,0)))
    return s.clean()

def rod(p,q,r=1.5):
    v=cq.Vector(*q)-cq.Vector(*p)
    return cq.Solid.makeCylinder(r,v.Length,cq.Vector(*p),v.normalized())

def flatbeam(p,q,w,z,t):
    p=np.array(p,float);q=np.array(q,float);v=q-p;v=v/np.linalg.norm(v);n=np.array([-v[1],v[0]])*w/2
    return cq.Workplane('XY').polyline([tuple(p+n),tuple(q+n),tuple(q-n),tuple(p-n)]).close().extrude(t).val().translate((0,0,z))

def bearing(x,y,z=31.5):
    # Nominal external rings and shields, no invented internal ball arrangement.
    return xring(5.5,2.5,4,x,y,z)

def block(x,y,outer=False):
    # Bearing pocket opens in +X; support face on the outer race only.
    foot_x=x+3
    base=box(6,30,8,(x+3,y,14))
    stem=box(6,12,14,(x+3,y,18))
    body=base.fuse(stem).fuse(cyl(8.5,6,31.5,x,y,axis=(1,0,0)))
    body=body.cut(cyl(4.5,6.2,31.5,x-.1,y,axis=(1,0,0)))
    depth=4.4 if outer else 4.
    body=body.cut(cyl(5.5,depth+.1,31.5,x+6-depth,y,axis=(1,0,0)))
    for yy in [y-7,y+7]:body=body.fuse(cyl(3,6,31.5,x,yy,axis=(1,0,0)))
    body=body.cut(cyl(4.5,6.2,31.5,x-.1,y,axis=(1,0,0))).cut(cyl(5.5,depth+.1,31.5,x+6-depth,y,axis=(1,0,0)))
    for yy in [y-11,y+11]:body=body.cut(cyl(1.25,12,14,foot_x,yy))
    # Two M2 blind tapped cap holes; nominal tap-drill geometry in the model.
    for yy in [y-7,y+7]:body=body.cut(cyl(.8,5,31.5,x+1,yy,axis=(1,0,0)))
    cap=xring(8.5,4.5,1.5,x+6,y)
    for yy in [y-7,y+7]:cap=cap.fuse(cyl(3,1.5,31.5,x+6,yy,axis=(1,0,0)))
    for yy in [y-7,y+7]:cap=cap.cut(cyl(1.1,1.7,31.5,x+5.9,yy,axis=(1,0,0)))
    return body.clean(),cap.clean()

def output_block():
    # Cantilever into the empty rear rim, bringing the bearing centre to X193.
    foot=box(8,30,8,(170,445,14)).fuse(box(8,12,2,(170,445,22)))
    bridge=box(29,12,4,(180.5,445,22.5))
    body=cyl(8.5,6,31.5,189,445,axis=(1,0,0)).fuse(box(6,12,10,(192,445,20)))
    s=foot.fuse(bridge).fuse(body)
    for yy in [438,452]:s=s.fuse(cyl(3,6,31.5,189,yy,axis=(1,0,0)))
    s=s.cut(cyl(4.5,6.2,31.5,188.9,445,axis=(1,0,0)))
    s=s.cut(cyl(5.5,4.4+.1,31.5,190.6,445,axis=(1,0,0)))
    for yy in [434,456]:s=s.cut(cyl(1.25,12,14,170,yy))
    for yy in [438,452]:s=s.cut(cyl(.8,5,31.5,190,yy,axis=(1,0,0)))
    cap=xring(8.5,4.5,1.5,195,445)
    for yy in [438,452]:cap=cap.fuse(cyl(3,1.5,31.5,195,yy,axis=(1,0,0)))
    for yy in [438,452]:cap=cap.cut(cyl(1.1,1.7,31.5,194.9,yy,axis=(1,0,0)))
    return s.clean(),cap.clean()

def mechanical(k):
    # C04-R2 extends3mm outboard for edge distance of palier screws.
    plate=box(93,90,3,(138.5,425,11))
    for x in [120,140]:
        for y in [392,460]:plate=plate.cut(cq.Workplane('XY').center(x,y).slot2D(15,4.5).extrude(3.2).val().translate((0,0,10.9)))
    for x,y in [(100,414.5),(100,436.5),(180,414.5),(180,436.5),(109,434),(109,456),(170,434),(170,456),(155,398),(155,418)]:plate=plate.cut(cyl(1.75,3.2,10.9,x,y))
    for x in [110,141.6]:
        for y in [386.5,466.5]:plate=plate.cut(cyl(1.75,3.2,10.9,x,y))
    part('C04_R2_droite',plate,qty=1,description='Remplace C04D-R1, largeur93mm, ancien évidement supprimé après déplacementHall',dimensions='X92..185 Y380..470 Z11..14 ;4lumières conservées ;8nouveauxtrous')
    part('C04_R2_gauche',plate.mirror('YZ'),qty=1,description='Remplace C04G-R1')
    put('C04_R2_D',plate);put('C04_R2_G',plate.mirror('YZ'))
    mid=cyl(2.5,91.5,31.5,95,425.5,axis=(1,0,0)).fuse(cyl(3,4,31.5,95,425.5,axis=(1,0,0)))
    mid=mid.cut(xring(2.6,2.4,.7,184.8,425.5))
    for x,l in [(106,16),(128,12)]:mid=mid.cut(box(l,2,3,(x+l/2,428.8,30)))
    part('R201_arbre_intermediaire',mid,STEEL,2,'Arbre intermédiaire droit ; gauche symétrique','C45E, Re minimal 355 MPa','L91.5 ; X95..186.5 ; épaulementØ6 X95..99 ; portées99..103 /179..183 ; gorgeØ4.8 largeur0.7 X184.8..185.5')
    out=cyl(2.5,135.5,31.5,73,445,axis=(1,0,0)).fuse(cyl(3.5,3,31.5,105,445,axis=(1,0,0)))
    out=out.fuse(cyl(2,10,31.5,208.5,445,axis=(1,0,0)))
    out=out.fuse(cyl(3.5,3,31.5,88,445,axis=(1,0,0))).cut(xring(2.6,2.4,.7,79.3,445))
    out=out.cut(cyl(1,7,28,202.5,445))
    out=out.cut(box(12,2,3,(123,448.8,30)))
    part('R202_arbre_sortie',out,STEEL,2,'Arbre de roue arrière, filetage M4 représenté au diamètre nominal','C45E, Re minimal 355 MPa','L145.5 ; X73..218.5 ; épaulementsØ7 X88..91 et105..108 ; gorgeØ4.8 L0.7 X79.3..80 ; M4final10 ; goupilleØ2 X202.5')
    for code,x,y,outer in [('R203_palier_interieur_intermediaire',97,425.5,False),('R204_palier_exterieur_intermediaire',177,425.5,True),('R205_palier_interieur_sortie',106,445,False)]:
        s,c=block(x,y,outer)
        part(code,s,qty=2,description='Palier à poche Ø11, passageØ9 et taraudages M3 de semelle',dimensions=f'Plan X{x}..{x+6} ; Y{y} ; Zaxe31.5 ; poche'+('4.4 flottante' if outer else '4 fixe'))
        part(code+'_capot',c,qty=2,description='Retenue de bague extérieure',dimensions='Épaisseur1.5 ; Ø17 /Ø9 ; deux passagesØ2.2 àY±7')
        for sign,n in [(1,'D'),(-1,'G')]:
            put(code+'_'+n,s if sign>0 else s.mirror('YZ'));put(code+'_cap_'+n,c if sign>0 else c.mirror('YZ'))
    s,c=output_block()
    part('R206_palier_sortie_porte_a_faux',s,qty=2,description='Palier extérieur à pied déporté ; roulement dans le creux de jante',dimensions='Pied X166..174 ; axeX193 Y445 Z31.5 ; appui flottant ; pocheØ11 L4.4')
    part('R206_capot',c,qty=2,description='Retenue extérieure de palier',dimensions='Ø17 /Ø9 ; e1.5 ; M2 entraxe14')
    for sign,n in [(1,'D'),(-1,'G')]:
        mirror=lambda s:s if sign>0 else s.mirror('YZ')
        put('R201_'+n,mirror(mid),STEEL);put('R202_'+n,mirror(out),STEEL)
        put('R206_'+n,mirror(s));put('R206_cap_'+n,mirror(c))
        for x,y in [(99,425.5),(179,425.5),(108,445),(191,445)]:put('MR115_AR_'+n+'_'+str(x),mirror(bearing(x,y)),STEEL)
        for x,length,y,label in [(103,3,425.5,'E1'),(122,6,425.5,'E2'),(140,39,425.5,'E3'),(112,5,445,'E4'),(129,62,445,'E5'),(195,7.5,445,'E6')]:
            sh=xring(3,2.55,length,x,y)
            if label=='E6':sh=sh.cut(box(1.2,2.1,10.2,(202.1,y,26.4)))
            put('Entretoise_'+label+'_'+n,mirror(sh),STEEL)
            if sign>0:part('R207_'+label,sh,STEEL,2,'Entretoise de bague intérieure','Acier rectifié',f'Ø6 /Ø5.1 ; L{length} ; tolérance longueur±0.02')
        for x,y,label in [(184.9,425.5,'I_ext'),(79.4,445,'Hall')]:put('Circlip5_'+n+'_'+label,mirror(circlip5(x,y)),STEEL)
        sh=xring(3,2.55,1.8,183,425.5);put('Entretoise_clip_'+n,mirror(sh),STEEL)
        if sign>0:
            part('R225_circlip_DIN471_5',circlip5(184.9,425.5),STEEL,4,'Circlip acheté DIN471-5, profil desoreilles reconstruit','Acier àressort, fabricantBeneri ouéquivalentdocumenté','Épaisseur0.6 ; gorgeØ4.8 largeur0.70..0.73 ; enveloppe de montageØ10.3')
            part('R226_entretoise_clip',sh,STEEL,2,'Entretoise debague intérieure avantcirclip','Acier rectifié','Ø6 /Ø5.1 L1.8±0.02 ; jeu axial àcaler')
        put('R206_palier_'+n,mirror(s)) if False else None
    # Front custom upright replaces reconstructed Tamiya moulded interfaces.
    a=k['arm_inward_mm']
    barrel=cyl(8.5,18,31.5,178,55,axis=(1,0,0))
    for yy in [48,62]:barrel=barrel.fuse(cyl(3,18,31.5,178,yy,axis=(1,0,0)))
    barrel=barrel.cut(cyl(3.1,18.2,31.5,177.9,55,axis=(1,0,0)))
    for x in [178,190]:barrel=barrel.cut(cyl(5.5,4.01,31.5,x,55,axis=(1,0,0)))
    for yy in [48,62]:barrel=barrel.cut(cyl(.8,5,31.5,178,yy,axis=(1,0,0)))
    pivot=cyl(5.5,55.1,20.7,170,55).cut(cyl(4,55.3,20.6,170,55))
    webs=box(14,8,2.3,(174,55,23)).fuse(box(14,8,2.3,(174,55,37.7)))
    p=(170-a,95)
    arm=flatbeam((170,55),p,8,70,3).fuse(cyl(4,3,70,170,55)).fuse(cyl(4,3,70,*p))
    pd=(p[0]-4,103)
    arm=arm.fuse(flatbeam(p,pd,8,70,3)).fuse(cyl(4,3,70,*pd))
    for x,y in [p,pd]:arm=arm.cut(cyl(1.25,3.2,69.9,x,y))
    print('UPRIGHT_STAGE',[(n,s.isValid(),len(s.Solids()),s.Volume()) for n,s in [('barrel',barrel),('pivot',pivot),('webs',webs),('arm',arm)]],flush=True)
    upright=barrel.fuse(pivot).fuse(webs).fuse(arm).clean()
    print('UPRIGHT_FUSED',upright.isValid(),len(upright.Solids()),upright.Volume(),flush=True)
    # Restore the kingpin through-bore after webs intersect it.
    upright=upright.cut(cyl(4,55.3,20.6,170,55)).clean()
    part('R208_fusee_droite',upright,qty=1,description='Fusée usinée à axe de pivotØ6 et deux MR115',dimensions='Pivot(170,55) ; axe roueZ31.5 ; roulements178..182 /190..194 ; bras calculé')
    part('R208_fusee_gauche',upright.mirror('YZ'),qty=1,description='Symétrique de la fusée droite')
    base=box(26,30,4,(166,64,13.5)).fuse(box(16,42.5,4,(170,28.25,13.5)))
    back=box(16,6,62.5,(170,10,17.5))
    low=box(16,45,4,(170,32.5,16.5)).fuse(cyl(5.5,4,16.5,170,55))
    high=box(16,45,4,(170,32.5,76)).fuse(cyl(5.5,4,76,170,55))
    fork=base.fuse(back).fuse(low).fuse(high)
    fork=fork.cut(cyl(3.05,66.6,13.4,170,55))
    for yy in [54,74]:fork=fork.cut(cyl(1.75,4.2,13.4,158,yy))
    # Mechanical stops: pins contact a straight arm flank at +/-25deg.
    stop_points=[]
    vec=np.array([-a,40.]);vec/=np.linalg.norm(vec)
    for direction in [1,-1]:
        angle=math.radians(25*direction);c,ss=math.cos(angle),math.sin(angle)
        v=np.array([[c,-ss],[ss,c]])@vec;n=np.array([-v[1],v[0]])
        point=np.array([170.,55.])+25*v+direction*5.5*n
        stop_points.append(point)
    post=stop_points[1]
    # Bring the negative stop from above the tyre instead of putting a tall
    # pillar into its swept corner. Horizontal stop loads act in the stiff
    # plane of this12x4.5mm bridge; the vertical tyre clearance is1mm minimum.
    stopbridge=flatbeam((170,10),(190,10),12,65,4.5).fuse(flatbeam((190,10),(190,float(post[1])),12,65,4.5)).fuse(flatbeam((190,float(post[1])),post,12,65,4.5))
    fork=fork.fuse(stopbridge).fuse(cyl(4,5.8,64,*post)).cut(cyl(1.5,5.5,64.5,*post))
    # Reliefs are derived from the tyre motion: preserve at least2mm to the
    # calculated shoulder at +/-25deg rather than accepting a corner clash.
    fork=fork.cut(box(30,29,10,(188,28.5,12))).cut(box(30,10,7,(190.5,77,12)))
    fork=fork.clean();part('R209_fourche_droite',fork,qty=1,description='Fourche fixe, deux appuis de pivot, colonne avantY10 et butée haute',dimensions='Base26x30x4 +extension16x42.5 ; perçages(158,54)/(158,74) ; passagepivotØ6.1 ; appuisZ20.5/76 ; pont de butée12x4.5 àZ65')
    part('R209_fourche_gauche',fork.mirror('YZ'),qty=1,description='Symétrique de R209 droite')
    frontshaft=cyl(2.5,32.5,31.5,176,55,axis=(1,0,0)).fuse(cyl(3.5,2,31.5,176,55,axis=(1,0,0))).fuse(cyl(2,10,31.5,208.5,55,axis=(1,0,0)))
    frontshaft=frontshaft.cut(cyl(1,7,28,202.5,55))
    part('R210_axe_roue_avant',frontshaft,STEEL,2,'Axe avant tournant, filetage nominal','C45E Re355MPa min','L42.5 ; X176..218.5 ; épaulementØ7 X176..178 ; M4x0.7 final10 ; trouØ2 àX202.5')
    frontcap=xring(6,4.5,1.5,176.5,55)
    for yy in [48,62]:frontcap=frontcap.fuse(cyl(3,1.5,31.5,176.5,yy,axis=(1,0,0)))
    for yy in [48,62]:frontcap=frontcap.cut(cyl(1.1,1.7,31.5,176.4,yy,axis=(1,0,0)))
    part('R220_capot_roulements_avant',frontcap,qty=2,description='Retenue des bagues extérieures du porte-fusée',dimensions='Épaisseur1.5 ; ouvertureØ9 ; deuxM2 entraxe14')
    for sign,n in [(1,'D'),(-1,'G')]:
        mirror=lambda s:s if sign>0 else s.mirror('YZ')
        put('R208_'+n,mirror(upright));put('R209_'+n,mirror(fork));put('R210_'+n,mirror(frontshaft),STEEL)
        put('R220_'+n,mirror(frontcap))
        for x in [178,190]:put('MR115_AV_'+n+'_'+str(x),mirror(bearing(x,55)),STEEL)
        # Stationary Ø6 pin and two replaceable polymer plain bushings.
        pin=cyl(5,2,9,170,55).fuse(cyl(3,69,11,170,55)).fuse(cyl(2.5,8,80,170,55))
        put('R211_pivot6_'+n,mirror(pin),STEEL)
        if sign>0:part('R211_pivot6',pin,STEEL,2,'Pivot fixe defusée, M5nominal','C45E Re355MPa minimal','L79 ; têteØ10 e2 ; corpsØ6 L69 ; M5x0.8 L8 ; repèreZ9..88')
        for xy in stop_points:put('Butee_pin3_'+n+'_'+str(round(float(xy[0]),2)),mirror(cyl(1.5,10,64.5,*xy)),STEEL)
        for z in [20.7,67.8]:put('Bague6_8_L8_'+n+'_'+str(z),mirror(cyl(4,8,z,170,55).cut(cyl(3,8.2,z-.1,170,55))),BLACK)
        put('Entretoise_AV_8_'+n,mirror(xring(3,2.55,8,182,55)),STEEL)
        put('Entretoise_AV_8_5_'+n,mirror(xring(3,2.55,8.5,194,55).cut(box(1.2,2.1,10.2,(202.1,55,26.4)))),STEEL)
    # Existing bought interfaces as nominal envelopes, not additional parts to
    # manufacture. They expose the wheel stack and nut engagement for review.
    for sign,n in [(1,'D'),(-1,'G')]:
        for y,axle in [(55,'AV'),(445,'AR')]:
            hub=cq.Workplane('YZ',origin=(202.5,y,31.5)).polygon(6,12/math.cos(math.pi/6)).extrude(6).val()
            hub=hub.cut(cyl(2.5,6.2,31.5,202.4,y,axis=(1,0,0))).cut(box(1.2,2.1,10.2,(203.1,y,26.4)))
            pin=cyl(1,10,26.5,202.5,y)
            nut=cq.Workplane('YZ',origin=(211.2,y,31.5)).polygon(6,7/math.cos(math.pi/6)).extrude(5).val().cut(cyl(2,5.2,31.5,211.1,y,axis=(1,0,0)))
            for label,sh in [('Moyeu53569_nominal',hub),('Goupille2x10',pin),('EcrouRoueM4_nominal',nut)]:
                put(label+'_'+axle+'_'+n,sh if sign>0 else sh.mirror('YZ'),STEEL)
    post=stop_points[0]
    stopbase=box(16,14,3,(143,float(post[1]),13.5)).fuse(cyl(4,53.3,16.5,*post))
    stopbase=stopbase.cut(cyl(1.5,10.1,59.8,*post))
    for yy in [post[1]-4,post[1]+4]:stopbase=stopbase.cut(cyl(1.75,3.2,13.4,139,float(yy)))
    part('R219_butee_avant',stopbase,qty=2,description='Butée mécanique25deg, support positif ; deuxième montant intégré àR209',dimensions=f'PionØ3 au point{post.tolist()} ; sommetsupportZ69.8 ; pionZ64.5..74.5')
    put('R219_D',stopbase);put('R219_G',stopbase.mirror('YZ'))
    # Two separate link planes; avoid crossing and touching ball sockets.
    el=end(-1,0,a);er=end(1,0,a);dl=drag_end(0,a);sp=np.array([0.,100.])
    for name,p,q,z in [('Traverse',el,er,82),('Commande',dl,sp,90)]:
        put('Biellette_'+name,rod((*p,z),(*q,z)),STEEL)
        for i,xy in enumerate([p,q]):put('Rotule_'+name+'_'+str(i),cq.Solid.makeSphere(3,cq.Vector(*xy,z)),STEEL)
    # R2 servo is a published-envelope model, not a falsely detailed supplier CAD.
    put('FT5335M_RESERVE',box(62.8,32.5,55.9,(21,80,17)),BLACK,'electricite')
    put('Palonnier_R20_RESERVE',rod((0,80,77),(0,100,77),3),BLACK)
    put('Adaptateur_rotule_servo_H13',cyl(2,13,77,0,100),STEEL)
    put('UBEC_30603003_RESERVE',box(45,20,16.2,(-25,130,45)),BLUE,'electricite')
    put('FS_KLKD5_RESERVE',box(22,85,55,(95,60,19)),BLUE,'electricite')
    put('Interface_3PWM_isoles_RESERVE',box(48,20,12,(-25,155,45)),BLUE,'electricite')
    for code,w,h,x,y,z,holes in [
      ('R212_support_servo',105,60,12.5,80,14,[(-30,55),(-30,105),(60,55),(60,105)]),
      ('R213_support_UBEC',50,70,-25,135,42,[(-47,104),(-3,104),(-47,166),(-3,166)]),
      ('R214_cassette_FS',34,97,95,60,14,[(84,17.5),(106,17.5),(84,102.5),(106,102.5)])]:
        ss=box(w,h,3,(x,y,z))
        for xx,yy in holes:ss=ss.cut(cyl(1.75,3.2,z-.1,xx,yy))
        if code=='R212_support_servo':ss=ss.cut(cyl(1.75,3.2,z-.1,-3,104))
        if code=='R212_support_servo':
            for xx in [10,40]:
                for yy in [57,103]:ss=ss.cut(cq.Workplane('XY').center(xx,yy).slot2D(12,3.5).extrude(3.2).val().translate((0,0,z-.1)))
        if code=='R213_support_UBEC':
            for xx in [-35,-15]:
                for yy in [117,143]:ss=ss.cut(cq.Workplane('XY').center(xx,yy).slot2D(12,3.5).extrude(3.2).val().translate((0,0,z-.1)))
        if code=='R214_cassette_FS':
            for yy in [15,105]:ss=ss.cut(cq.Workplane('XY').center(95,yy).slot2D(12,3.5).extrude(3.2).val().translate((0,0,z-.1)))
        part(code,ss,qty=1,description='Support démontable R2',dimensions=f'{w}x{h}x3 ; Z{z} ; trousØ3.5 {holes}')
        put(code,ss)
        if z>14:
            for xx,yy in holes:
                bottom=17 if (xx,yy)==(-3,104) else 11
                put('Entretoise_'+code+'_'+str(xx)+'_'+str(yy),cyl(3,z-bottom,bottom,xx,yy).cut(cyl(1.75,z-bottom+.2,bottom-.1,xx,yy)),BLACK)
    for xx,yy,z,h in [(-30,55,13.5,.5),(60,55,13.5,.5),(-30,105,11,3),(60,105,11,3),(-3,104,11,3),*( (xx,yy,11,3) for xx in [84,106] for yy in [17.5,102.5])]:
        put('Cale_R2_'+str(xx)+'_'+str(yy),cyl(3,h,z,xx,yy).cut(cyl(1.75,h+.2,z-.1,xx,yy)),BLACK)
    # Two adjustable motor brackets; rotate each motor so its Ø16 mounting
    # hole pair is vertical. Gear-hub relief is explicit rather than colliding.
    foot=box(23,28,3,(148.5,408,14))
    upright=box(3,28,32.5,(138.5,408,17))
    upright=upright.cut(cyl(13,3.2,31.5,136.9,425.5,axis=(1,0,0)))
    upright=upright.cut(cyl(3.2,3.2,31.5,136.9,408,axis=(1,0,0)))
    for zz in [23.5,39.5]:upright=upright.cut(cyl(1.35,3.2,zz,136.9,408,axis=(1,0,0)))
    for yy in [398,418]:foot=foot.cut(cq.Workplane('XY').center(155,yy).slot2D(7,3.5,90).extrude(3.2).val().translate((0,0,13.9)))
    motorplate=upright.fuse(foot).clean()
    part('R218_platine_moteur',motorplate,qty=2,description='Support moteur ajustable enY, empreinteM2.5 entraxe16',dimensions='FaceX140 ; épaisseur3 ; 2xØ2.7 àZ23.5/39.5 ; portéeY408 ;2lumières7x3.5 ensemelle')
    for sign,n in [(1,'D'),(-1,'G')]:put('R218_'+n,motorplate if sign>0 else motorplate.mirror('YZ'))
    # Open-bottom removable polycarbonate guard; aperture permits output shaft.
    guard=box(44,71.5,39,(124.8,426.75,14)).cut(box(40,67.5,37.1,(124.8,426.75,13.9)))
    # Motor body extends outside the gear case; deliberately open service aperture.
    guard=guard.cut(cyl(13,10,31.5,140,408,axis=(1,0,0)))
    guard=guard.cut(cyl(4,45,31.5,102.7,445,axis=(1,0,0)))
    guard=guard.cut(cyl(7.5,2.3,31.5,104.7,425.5,axis=(1,0,0)))
    guard=guard.cut(cyl(11,2.3,31.5,102.7,425.5,axis=(1,0,0)))
    guard=guard.cut(box(3,32,10,(104,425.5,13.9)))
    guard=guard.cut(cyl(3.5,45,31.5,103,425.5,axis=(1,0,0)))
    guard=guard.cut(box(26,30,4.2,(149,408,13.9)))
    for xx in [110,141.6]:
        for yy in [386.5,466.5]:
            tab=box(10,12,2,(xx,yy,14)).cut(cyl(1.75,2.2,13.9,xx,yy));guard=guard.fuse(tab)
    part('R215_carter_transmission_droit',guard.clean(),BLUE,1,'Écran anti-contact démontable ; non qualifié contre éclatement','Polycarbonate compact 2mm','Enveloppe44x71.5x39 ; ouvert en dessous ; ouverture moteurØ26 ; passagesØ8 ; encoche autoursemelleR203')
    part('R215_carter_transmission_gauche',guard.mirror('YZ'),BLUE,1,'Symétrique du carter droit','Polycarbonate compact 2mm')
    for n,ss in [('D',guard),('G',guard.mirror('YZ'))]:put('R215_'+n,ss,BLUE,'carter')
    for sign,n in [(1,'D'),(-1,'G')]:
        for x,y,l,label in [(146.8,425.5,30.2,'intermediaire'),(146.8,445,42.2,'sortie')]:
            sh=xring(4.5,3.5,l,x,y)
            if sign>0:part('R216_tube_'+label,sh,BLUE,2,'Tube de protection desmontable, maintien àqualifier','Polycarbonate compact',f'Ø9 /Ø7 L{l}')
            if sign<0:sh=sh.mirror('YZ')
            put('R216_tube_'+label+'_'+n,sh,BLUE,'carter')
    return upright,fork

def cut_plans():
    # Additive drill overlay, tied to the immutable C01 R1 coordinate system.
    holes=[]
    def add(x,y,d,role):
        target='C01+C04-R2' if ('palier' in role or 'carter' in role) and abs(x)<150 else 'C04-R2' if ('palier' in role or 'carter' in role) else 'C03' if ('Fourche' in role or 'Pivot' in role) else 'C01+C03' if 30<=y<=85 else 'C01'
        holes.append(dict(piece=target,x_global=x,y_global=y,x_C01=x+150 if abs(x)<150 else None,y_C01=y if abs(x)<150 else None,diameter=d,role=role))
    for sign in [-1,1]:
        for x,y in [(100,414.5),(100,436.5),(180,414.5),(180,436.5),(109,434),(109,456),(170,434),(170,456),(155,398),(155,418)]:
            add(sign*x,y,3.5,'R2 palier, vis sous plateau ; C04 à repercer également')
        for y in [435,455]:add(sign*51,y,3.5,'Pied Hall déplacé : rotorX±80')
        for y in [54,74]:add(sign*158,y,3.5,'FourcheR209 : traverse C03 à reprendre, hors plateauC01')
        add(sign*170,55,6.2,'PivotR211 : passage à traversC03')
        a=calculate()['arm_inward_mm'];v=np.array([-a,40.]);v/=np.linalg.norm(v);an=math.radians(25);rot=np.array([[math.cos(an),-math.sin(an)],[math.sin(an),math.cos(an)]])@v
        st=np.array([170.,55.])+25*rot+5.5*np.array([-rot[1],rot[0]])
        for yy in [st[1]-4,st[1]+4]:add(sign*139,float(yy),3.5,'ButéeR219 surC01+C03')
        for x in [110,141.6]:
            for y in [386.5,466.5]:add(sign*x,y,3.5,'Fixation carterR215')
    for x,y in [(-30,55),(-30,105),(60,55),(60,105),(-47,104),(-3,104),(-47,166),(-3,166),(84,17.5),(106,17.5),(84,102.5),(106,102.5)]:add(x,y,3.5,'Support R212/R213/R214')
    csvout(PL/'percages-r2-global.csv',holes)
    doc=ezdxf.new('R2010');doc.units=4;ms=doc.modelspace()
    doc.layers.new('REFERENCE_NE_PAS_DECOUPER',dxfattribs={'color':8});doc.layers.new('PERCAGE_R2',dxfattribs={'color':1})
    ms.add_lwpolyline([(-150,0),(150,0),(150,520),(-150,520)],close=True,dxfattribs={'layer':'REFERENCE_NE_PAS_DECOUPER'})
    for h in holes:ms.add_circle((h['x_global'],h['y_global']),h['diameter']/2,dxfattribs={'layer':'PERCAGE_R2'})
    doc.saveas(PL/'surcouche-percages-r2.dxf')
    # Publish modified chassis plates as separate R2 files and preserve R1 kit.
    for code,z,t,dx,dy in [('C01',8,3,-150,0),('C03',11,2.5,-174,30)]:
        s=cq.importers.importStep(str(ROOT/'Composants/chassis/3D'/(code+'.step'))).val().translate((dx,dy,z))
        for h in holes:
            x,y=h['x_global'],h['y_global']
            if code=='C01' and h['piece'] in ['C04-R2','C03']:continue
            if code=='C03' and not(-174<=x<=174 and 30<=y<=85):continue
            s=s.cut(cyl(h['diameter']/2,t+.2,z-.1,x,y))
        s=s.clean();part(code+'_R2',s,qty=1,description='R1 avec perçages additionnels R2, même repère global')
        put(code+'_R2',s)
    # Definitive shaft stations, not inferred from a screenshot.
    stations=[
      ('R201','arbre intermédiaire',95,99,'épaulementØ6'),('R201','arbre intermédiaire',99,103,'roulement fixe'),('R201','arbre intermédiaire',103,106,'entretoiseL3'),('R201','arbre intermédiaire',106,122,'pignon24 inversé'),('R201','arbre intermédiaire',122,128,'entretoiseL6'),('R201','arbre intermédiaire',128,140,'couronne54 étage1'),('R201','arbre intermédiaire',140,179,'entretoiseL39'),('R201','arbre intermédiaire',179,183,'roulement flottant'),('R201','arbre intermédiaire',183,184.8,'entretoiseL1.8'),('R201','arbre intermédiaire',184.8,185.5,'gorgeDIN471'),('R201','arbre intermédiaire',185.5,186.5,'lèvre1mm'),
      ('R202','sortie',73,79.3,'bout libre'),('R202','sortie',79.3,80,'gorgeDIN471'),('R202','sortie',80,88,'rotor Hall'),('R202','sortie',88,91,'épaulementØ7'),('R202','sortie',91,105,'dégagement'),('R202','sortie',105,108,'épaulementØ7'),('R202','sortie',108,112,'roulement fixe'),('R202','sortie',112,117,'entretoiseL5'),('R202','sortie',117,129,'couronne54 étage2'),('R202','sortie',129,191,'entretoiseL62'),('R202','sortie',191,195,'roulement flottant'),('R202','sortie',195,202.5,'entretoiseL7.5'),('R202','sortie',202.5,208.5,'moyeu12mm'),('R202','sortie',208.5,218.5,'filetage M4 roue'),
      ('R210','avant',176,178,'épaulementØ7'),('R210','avant',178,182,'roulement'),('R210','avant',182,190,'entretoiseL8'),('R210','avant',190,194,'roulement'),('R210','avant',194,202.5,'entretoiseL8.5'),('R210','avant',202.5,208.5,'moyeu'),('R210','avant',208.5,218.5,'M4')]
    rows=[dict(code=c,arbre=n,x_debut=x,x_fin=y,longueur=y-x,fonction=f) for c,n,x,y,f in stations]
    csvout(PL/'empilages-arbres.csv',rows);return rows,holes

def rounded(points,radius):
    """Polyline with exact circular corner fillets, used for cable bend checks."""
    p=[np.array(x,float) for x in points];edges=[];last=p[0];length=0
    for i in range(1,len(p)-1):
        a,b,c=p[i-1:i+2];u=(b-a)/np.linalg.norm(b-a);v=(c-b)/np.linalg.norm(c-b)
        angle=math.acos(float(np.clip(u@v,-1,1)));setback=radius*math.tan(angle/2)
        assert setback<np.linalg.norm(b-a) and setback<np.linalg.norm(c-b)
        s=b-u*setback;e=b+v*setback
        # Tangency setbacks of neighbouring corners must not overlap.
        assert np.dot(s-last,u)>=-1e-7,(points,i)
        if np.linalg.norm(s-last)>1e-6:edges.append(cq.Edge.makeLine(cq.Vector(*last),cq.Vector(*s)));length+=np.linalg.norm(s-last)
        centre=s+v*radius if abs(float(u@v))<1e-6 else b+(-u+v)/np.linalg.norm(-u+v)*radius/math.cos(angle/2)
        vs=(s-centre);ve=e-centre;mid=centre+(vs+ve)/np.linalg.norm(vs+ve)*radius
        edges.append(cq.Edge.makeThreePointArc(cq.Vector(*s),cq.Vector(*mid),cq.Vector(*e)));length+=radius*angle;last=e
    if np.linalg.norm(p[-1]-last)>1e-6:edges.append(cq.Edge.makeLine(cq.Vector(*last),cq.Vector(*p[-1])));length+=np.linalg.norm(p[-1]-last)
    return cq.Wire.assembleEdges(edges),float(length)

def route(code,net,points,awg,diam=3.3,radius=8,service=30,status='Approches des bornes à relever',color=(.5,.02,.01)):
    wire,length=rounded(points,radius)
    plane=cq.Plane(origin=cq.Vector(*points[0]),normal=wire.Edges()[0].tangentAt(0))
    shape=cq.Workplane(plane).circle(diam/2).sweep(cq.Workplane('XY').newObject([wire]),isFrenet=False).val()
    assert shape.isValid(),code
    put(code,shape,color,'cables')
    ROUTES.append(dict(code=code,net=net,wire=awg,diameter_design_mm=diam,bend_radius_mm=radius,centreline_mm=round(length,2),service_and_termination_allowance_mm=service,blank_length_mm=math.ceil((length+service)/10)*10,status=status,points_mm=points))

def routes():
    route('P01','IC5+ vers F0, chemin fixe protégé',[(0,190,55),(-40,190,55),(-40,350,55),(33,350,55),(33,170,55)],'10 AWG puis6mm²',6.5,30,40)
    route('P02','IC5- vers D-',[(0,190,64),(-46,190,64),(-46,320,64),(-87,320,64)],'10 AWG puis6mm²',6.5,30,30,color=(.03,.03,.04))
    route('P03','F0 sortie vers ED80',[(120,110,110),(120,70,110),(-65,70,110),(-65,140,110)],'6mm²',6.5,30,60,status='Corridor haut, supports et descentes aux bornes à confirmer')
    route('P04','ED80 vers D+', [(-65,140,110),(-155,140,110),(-155,285,110),(-87,285,110)],'6mm²',6.5,30,60,status='Corridor latéral haut ; descentes aux bornes à confirmer')
    route('P05','D+ vers SSR', [(-87,290,125),(-155,290,125),(-155,220,125),(-90,220,125)],'6mm²',6.5,30,80,status='Corridor latéral haut ; descentes aux bornes à confirmer')
    route('P06','SSR vers UD80',[(-90,227,135),(-155,227,135),(-155,450,135),(108,450,135),(108,368,135)],'6mm²',6.5,30,60,status='Corridor supérieur avec pont de maintien à concevoir ; non libéré')
    for sign,n in [(-1,'G'),(1,'D')]:
        route('M_'+n,'F'+('1' if sign<0 else '2')+' vers XT60 ESC'+n,[(sign*47,376,44),(sign*47,340,44),(60 if sign<0 else 85,340,44),(60 if sign<0 else 85,310,44)],'12 AWG',4,8,40)
        route('N_'+n,'ESC'+n+' retour D-',[(sign*47,376,47),(sign*47,330,47),(-87,330,47),(-87,320,47)],'12 AWG',4,4,35,color=(.03,.03,.04))
    route('S01','FS5A vers UBEC6V',[(95,20,24),(70,20,24),(70,105,54),(-25,105,54),(-25,120,54)],'18 AWG',2.8,5,40)
    # Signals follow a separate upper corridor and camera cable the rear post.
    route('L01','GPIO vers interface avant', [(-10,407,123),(65,407,123),(65,185,123),(65,175,95),(0,175,95),(0,110,90)],'22 AWG signaux, enveloppe8mm',8,8,60,color=(.7,.5,.01))
    for sign,n in [(-1,'G'),(1,'D')]:route('H_'+n,'Hall'+n+' VCC/GND/OUT',[(0,407,123),(sign*60,407,123),(sign*60,445,70),(sign*76,445,48)],'3x22 AWG',3.5,5,50,color=(.2,.4,.1))
    route('USB','Caméra vers USB Pi',[(0,482,231),(118,482,231),(118,490,150),(118,490,128),(70,490,128),(70,395,128),(48,395,112)],'USB blindé, câble caméra à confirmer',5,20,100,color=(.04,.04,.05))
    csvout(B/'routage/longueurs-cables.csv',[{k:v for k,v in r.items() if k!='points_mm'} for r in ROUTES])
    dump(B/'routage/parcours.json',ROUTES)

def fasteners(holes):
    def f(code,designation,q,where,grip,washer,nut,eng,minimum,chosen,statut='Calcul nominal ; présentation réelle à contrôler'):
        FAST.append(dict(code=code,designation=designation,quantite=q,affectation=where,empilage_mm=grip,rondelles_mm=washer,ecrou_mm=nut,engagement_ou_depassement_mm=eng,longueur_min_mm=minimum,longueur_retenue_mm=chosen,statut=statut))
    f('V01','M4x12 tête basse classe8.8',8,'C03 surC01',5.5,.8,5,0.7,12,12)
    f('V02','M4x14 tête basse classe8.8',6,'Longerons L01',6,.8,5,.7,12.5,14)
    f('V03','M4x85 tête basse classe8.8',4,'Pont : plateau3 +tube70 +pont2',75,1.6,5,.7,82.3,85)
    f('V04','M4x70 tête basse classe8.8',4,'Pod ED80 : plateau3 +cale3 +tube56 +toit3',65,.8,5,.7,71.5,75,'Corriger : M4x75 nécessaire ; M4x70 rejetée')
    FAST[-1].update(designation='M4x75 tête basse classe8.8',longueur_retenue_mm=75)
    f('V05','M4x14 tête basse classe8.8',8,'C04 sur plateau',6,1.6,5,.7,13.3,14)
    f('V06a','M3x16 tête basse classe8.8',8,'Semelles4paliers intérieurs, C01+C04, taraudagetraversant8mm',6,.5,0,8,14.5,16)
    f('V06b','M3x10 tête basse classe8.8',8,'Semelles4paliers extérieurs, C04 seulement',3,.5,0,6.5,9.5,10)
    f('V07','M2x6 tête cylindrique',16,'Capots des8paliers, taraudageM2',1.5,0,0,4.5,5.5,6)
    f('V08','M3x14 tête basse classe8.8',4,'FourchesR209 /C03',6.5,.5,4,1,12,14)
    f('V09a','M3x12 tête basse',4,'PiedsHall surplateau',6,.5,4,1,11.5,12)
    f('V09b','M3x16 tête basse',4,'R214 /cale3 /plateau3',9,.5,4,1,14.5,16)
    f('V10','M3x40 tête basse',4,'Pod UBEC : plateau3 +entretoise31 +support3',37,.5,4,1,42.5,45)
    FAST[-1]['designation']='M3x45 tête basse'
    f('V11','M3x16 tête basse',4,'R212 /cales0.5ou3 /C03 ouC01',9,.5,4,1,14.5,16)
    f('V12a','M4x14 tête basse',4,'Pieds caméra surplateau',6,.8,5,.7,12.5,14)
    f('V12b','M4x16 tête cylindrique',8,'Pieds/montants etmontants/traverse',9,.8,5,.7,15.5,16)
    f('V13','M4x14 tête cylindrique',2,'Angle pivot caméra /traverse',6,.8,5,.7,12.5,14)
    f('V14','M2.5x25 tête basse +écrou nylon',4,'Pi : PCB1.6 +entretoise15 +pont2',18.6,1,2.5,1,23.1,25)
    f('V15','M3x25 +écrou nylon',4,'Porteuse : PCB1.6 +entretoise15 +pont2',18.6,1,4,1,24.6,25)
    f('V16','M3x20 +écrou nylon',8,'Cassettes EVM : pont2 +entretoise10 +cassette3',15,1,4,1,21,25)
    FAST[-1]['designation']='M3x25 +écrou nylon'
    f('V17a','M3x20 tête basse',12,'C05/C06/C12 : plateau3 +caleoucornière3 +cassette5',11,.5,4,1,16.5,20)
    f('V17b','M3x16 tête basse',8,'C13/C14 : plateau3 +caleoucornière3 +cassette3',9,.5,4,1,14.5,16)
    f('V17c','M3x12 tête fraisée',4,'C10 surpont : pont2 +cassette3 ; longueur têtecomprise',5,.5,4,1,10.5,12)
    f('V18','M3x16 tête basse',8,'Deux platinesESC : plateau3 +cale3 +platine3',9,.5,4,1,14.5,16)
    f('V19','M3x20 tête basse',4,'Butées batterieC16 : plateau3 +butée8',11,.5,4,1,16.5,20)
    f('V20','M3x20 tête basse',4,'Guides batterieC17 : plateau3 +guide8',11,.5,4,1,16.5,20)
    f('V21','M3x16 tête basse +écrou nylstop',8,'CarterR215 /C04 /C01',8,.5,4,1,13.5,16)
    f('V22','M4 écrou de roue àflasque',4,'Roues, sur arbreM4x0.7',0,0,5,0,5,0,'Pièce Tamiya9805557 ; engagement à contrôler selon jante réelle')
    f('V23','M3x16 tête basse +écrou nylstop',4,'ButéesR219 /C03 /C01',8.5,.5,4,1,14,16)
    f('V24','M2.5x6 tête cylindrique',4,'Moteur, platine3 +rondelle0.5',3,.5,0,2.5,6,6,'Profondeur moteur4mm ; engagement2.5mm ; ne pas talonner')
    f('V25','M3x10 tête basse +écrou nylstop',4,'Supportmoteur /C04 seulement',6,.5,4,1,11.5,12)
    FAST[-1]['designation']='M3x12 tête basse +écrou nylstop'
    f('V26','M3x16 tête basse',4,'CassetteIC5 /cale3 /C01',9,.5,4,1,14.5,16)
    f('V27','M3x8 tête cylindrique',8,'4blocagesrotors +4réglagesHall',3,.5,0,4.5,8,8,'Vérifier paroi /absence de contact ; vis de réglage issuesdu dossierP1')
    f('V28','M2x6 tête fraisée',4,'RetenuescapteursHall',1.5,0,0,4.5,6,6)
    f('V29','M2x20 nylon +écrou',4,'Caméra : PCB1.6 +entretoise12 +berceau3',16.6,1,1.6,.4,19.6,20)
    f('V30','M4x20 avec rondelles',1,'PivotberceaucaméraP1 surcornière3',9,3,5,.7,17.7,20)
    f('V31','M2x6 tête cylindrique',4,'Deux capots desroulementsavant',1.5,0,0,4.5,5.5,6)
    for r in FAST:
        if r['longueur_retenue_mm'] and r['longueur_retenue_mm']+1e-8<r['longueur_min_mm']:raise ValueError(r)
    csvout(ROOT/'Composants/visserie-finale/nomenclature.csv',FAST)
    # Hardware outside ISO through-bolt model is counted separately.
    specials=[dict(item='GoupilleØ2x10',quantite=4,statut='Déjà sélectionnée ; position nominaleX±202.5'),dict(item='Collier fendu Ø5, OD≤8',quantite=8,statut='2pararbreintermédiaire +2parrotor ; effort axial à confirmer'),dict(item='Pivot usiné Ø6 /M5',quantite=2,statut='R211 ; têteØ10x2 ; corps6 de69mm ; M5final8 ; longueur totale79mm ; deux écrousM5 etrondelles'),dict(item='Pion de butéeØ3x10',quantite=4,statut='AcierRe355min ;5.3mm insérés ;4.7mm exposés ; ajustementserré etretenueàqualifier'),dict(item='Bague lisse6x8x8',quantite=4,statut='POM-C usiné ; ajusterjeu6.02..6.06'),dict(item='Rotules/chapesM3',quantite=4,statut='Deux biellettes ; quatreutilisées sur6prévues ; hauteur des rotules àrelever'),dict(item='VispressionengrènementM4',quantite=6,statut='Normalement inclusesKHK ; contrôlerlot'),dict(item='Vispressionpignonmoteur',quantite=2,statut='FourniesLosi ; nepasinventerpas'),dict(item='Fixations propres supportsfusibles/rails/SSR/modules',quantite=None,statut='Point documentaire ouvert ; cassettes restent démontables, aucun nombre inventé')]
    specials=[r for r in specials if not r['item'].startswith('Collier fendu')]
    specials.append(dict(item='CirclipDIN471-5 acierressort',quantite=4,statut='Beneri5 ouéquivalentdocumenté ; gorge4.8 /0.70..0.73 ; acheterlescirclips etcontrôlerlesgorges'))
    dump(ROOT/'Composants/visserie-finale/accessoires-et-interfaces.json',specials)
    return specials

def calculations(k):
    m=9.;front=.45;mu=.8;r=.045;g=9.81
    torque=mu*m*front*g*r*k['max_jacobian_sum'] # factor2 /two equal front loads
    fy=m*(1-front)/2*g*3
    bend=32*(fy*7)/(math.pi*5**3)*2
    tors=16*500/(math.pi*5**3)*1.5
    vm=math.sqrt(bend*bend+3*tors*tors)
    speed=40/3.6;wheelrpm=speed/(math.pi*.063)*60
    energy=7.4*5*.8
    calc=dict(date='2026-10-16',revision='R2 étude théorique, sous conditions',hardware_tested=False,
      mass=dict(design_ceiling_kg=m,front_fraction_max=.45,rear_fraction=.55,vertical_load_factor=3,coefficient_friction=.8,effective_steering_friction_radius_mm=45,not_a_weighed_vehicle=True),
      direction=dict(required_servo_torque_Nm=torque,margin_factor_included=2,selected='FEETECH FT5335M current manufacturer revision,6V',published_rated_Nm=13.5*.0980665,margin=13.5*.0980665/torque,old_FT90M_rated_Nm=.7*.0980665,old_servo_rejected=True,servo_pwm_soft_limit_deg=55,mechanical_wheel_stop_deg=25,nominal_kinematics_only=True),
      rear_shaft=dict(outside_support_x_mm=193,wheel_centre_x_mm=200,overhang_mm=7,old_overhang_mm=28.5,radial_study_load_N=fy,wheel_torque_design_Nm=.5,bending_notch_factor=2,torsion_notch_factor=1.5,bending_MPa=bend,torsion_MPa=tors,von_mises_MPa=vm,material_yield_required_MPa=355,allowable_MPa=177.5,pass_screening=vm<177.5,fatigue_and_holes_not_fea=True),
      speeds=dict(wheel_rpm_40=wheelrpm,intermediate_rpm_40=wheelrpm*2.25,motor_rpm_40=wheelrpm*7.59375,ratio=7.59375,mesh1_centre_mm=17.5,mesh2_centre_mm=19.5,mesh1_pitch_speed_m_s=math.pi*.008*(wheelrpm*7.59375)/60,gear_ratings_at_this_speed_unconfirmed=True),
      electricity=dict(energy_usable_study_Wh=energy,capacity_use_fraction=.8,power_budget_45min_W=energy/.75,power_budget_20min_W=energy/(1/3),power_budget_10min_W=energy/(1/6),main_budget_previous_A=36,main_budget_with_servo_A=40,servo_peak_6V_A=6,servo_BEC1_supply_rejected=True,FS_candidate='KLKD005.T +L60030M1PQ',main_fault_current_bound_A=16402.605867658778,full_coordination_proven=False,hardware_current_limit=False),
      fit=dict(shafts_nominal_mm=5,bearing_housing_nominal_mm=11,bearing_clearance_selection='MC5 to order and verify',shaft_interference_target_um=[1,3],housing='H7 light stationary load; floating pocket0.4mm ; confirm exact bearing maker',kinematic_joint_radial_clearance_mm=[.02,.06],axial_running_clearance_mm=[.05,.15],gear_flat_depth_mm=.3,gear_pressure_angle_Losi_unconfirmed=True))
    dump(B/'calculs.json',calc)
    scenarios=[]
    for speed_kmh in [5,10,20,40]:
        speed_ms=speed_kmh/3.6;force=.02*m*g+.5*1.2*.08*speed_ms**2
        power=force*speed_ms/.7+12
        scenarios.append(dict(vitesse_kmh=speed_kmh,puissance_totale_W=power,autonomie_min=energy/power*60,hypothese='9kg,Crr0.02,CdA0.08m²,eta0.7,aux12W ; aucune mesure',angle_moyen_max_deg=min(22,math.degrees(math.atan(.39/(speed_ms**2/(.3*g)))))))
    csvout(B/'scenarios-performance.csv',scenarios)
    csvout(B/'table-direction.csv',k['rows'])
    dump(B/'cinematique.json',{key:value for key,value in k.items() if key!='rows'})
    return calc

def assembly():
    base=cq.Assembly.load(str(ROOT/'Composants/chassis/3D/chassis-a2-r1-implante.step'))
    out=cq.Assembly(name='DroneV3_R2_etude_theorique')
    removed=[]
    reject=('F_AV_','A7_','Axe_avant_','FT90M_','Servo_palonnier','Direction_','Arbre_sortie_','Transmission_','C04D_','C04G_','C01_','C03_')
    for child in base.children:
        if child.name.startswith(reject) or child.name.startswith(('C08_','N01_')):removed.append(child.name);continue
        if child.name.startswith('HALL_'):
            # Local mounting datum moves103 ->80. Preserve the station adjustment.
            delta=-23 if child.name.startswith('HALL_D') else 23
            out.add(child,name=child.name,loc=cq.Location(cq.Vector(delta,0,0)));continue
        out.add(child,name=child.name)
    for name,s,col,group in PARTS:
        # A failed cable proposal is never inserted into the released layout.
        if name in ['P03','P04','P05','P06']:continue
        out.add(s,name=name,color=cq.Color(*col))
    target=ROOT/'Assemblage/R2/drone-v3-r2-etude.step'
    out.export(str(target),exportType='STEP',unit='MM',outputUnit='MM')
    only=cq.Assembly(name='Mecanique_et_integration_R2')
    for name,s,col,group in PARTS:
        if name in ['P03','P04','P05','P06']:continue
        only.add(s,name=name,color=cq.Color(*col))
    only.export(str(OUT/'complement-mecanique-integration-r2.step'),exportType='STEP',unit='MM',outputUnit='MM')
    dump(V/'assemblage.json',dict(file=str(target.relative_to(ROOT)),bytes=target.stat().st_size,sha256=sha(target),removed_R1_items=removed,new_named_objects=len(PARTS),all_geometry_checked_locally=True,full_vehicle_collision_validation=False))
    dump(B/'pieces.json',SPECS)
    cache=ROOT/'tools/temp/finalisation-r2';cache.mkdir(exist_ok=True)
    for name,s,col,group in PARTS:cq.exporters.export(s,str(cache/(name+'.brep')))
    dump(cache/'instances.json',[dict(name=n,group=g,color=c) for n,s,c,g in PARTS])
    return out

def get_refs():
    refs=[
      ('FEETECH-FT5335M-actuel.html','https://www.feetechrc.com/84v-40kg-digital-steering-gear-ft5335m.html','Current manufacturer table: nominal torque13.5kg.cm@6V. Differs from historical17T PDF; require matched revision.'),
      ('FEETECH-FT5335M-historique.pdf','https://www.pololu.com/file/0J1434/FT5335M-specs.pdf','Historical manufacturer sheet, mirrored unchanged by Pololu: conflicting17T and4A, not current25T table.'),
      ('Hobbywing-UBEC10ACar.pdf','https://hobbywing.oss-cn-shenzhen.aliyuncs.com/pdf/pdfen/UBEC10ACar.pdf','30603003,2-6S,6V output selected,45x20x16.2mm. Not old30603000.'),
      ('TI-ISO7710.pdf','https://www.ti.com/lit/ds/symlink/iso7710.pdf','ISO7710F, default low,2.25..5.5V; avoid direct6V supply.'),
      ('NSK-ajustements.html','https://www.nsk.com/tools-resources/abc-bearings/fits-and-internal-clearance/','Interference reduces internal clearance; avoid nominal fits claimed without incoming metrology.'),
      ('SMB-MR115ZZ.pdf','https://www.smbbearings.com/firebrick/ckeditor/plugins/upload/Uploads/Documents/bearingpdfs/MR115ZZ-miniature-bearing-5x11x4mm.pdf','External dimensions and load ratings; a generic unbranded bearing cannot inherit this specification.')]
    def fetch(row):
        name,url,note=row;p=B/'references'/name
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
            data=urllib.request.urlopen(req,timeout=18).read()
            if name.endswith('.pdf'):assert data.startswith(b'%PDF')
            p.write_bytes(data);return dict(file='references/'+name,url=url,note=note,archived=True,sha256=sha(p))
        except Exception as e:return dict(file=None,url=url,note=note,archived=False,error=str(e))
    with ThreadPoolExecutor(max_workers=5) as pool:result=list(pool.map(fetch,refs))
    dump(B/'sources.json',result)
    return result

def main():
    sys.stdout.reconfigure(encoding='utf-8');start=time.time()
    k=calculate();calc=calculations(k);print('CALCULS',calc['direction'],flush=True)
    mechanical(k);print('GEOMETRIE',len(PARTS),flush=True)
    stations,holes=cut_plans();routes();specials=fasteners(holes)
    out=assembly();print('ASSEMBLAGE',len(out.children),flush=True)
    refs=get_refs() if '--refs' in sys.argv else [];print('REFERENCES',sum(x['archived'] for x in refs),flush=True)
    dump(V/'generation.json',dict(seconds=time.time()-start,geometry_objects=len(PARTS),part_specs=len(SPECS),routes=len(ROUTES),screw_lines=len(FAST),authoring_script_sha256=sha(Path(__file__))))

if __name__=='__main__':main()
