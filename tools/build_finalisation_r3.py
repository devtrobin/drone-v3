"""Demountable cable frame, four main routes and exact nominal fastener stacks.

R2 files are inputs only. R3 terminal approach points are design ports, not
invented terminal coordinates. Final tails are fitted to measured components.
"""
from pathlib import Path
import json,csv,math,hashlib,time,sys
import cadquery as cq
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from build_running_gear_step import box,cyl
from build_finalisation_r2 import rounded
ROOT=Path(__file__).resolve().parents[1]
B=ROOT/'Composants/complements-finalisation-r3';O=B/'3D';P=B/'plans';V=B/'verification';A=ROOT/'Assemblage/R3';T=ROOT/'tools/temp/finalisation-r3'
for d in [O,P,V,A,T]:d.mkdir(parents=True,exist_ok=True)
ITEMS=[];SPECS=[];HOLES=[];BOLTS=[];ROUTES=[]
AL=(.58,.62,.66);POM=(.12,.14,.16);RED=(.7,.025,.025)
def optimal(self,tolerance=None):
    b=Bnd_Box();BRepBndLib.AddOptimal_s(self.wrapped,b,False,False);return cq.BoundBox(b)
cq.Shape.BoundingBox=optimal
def dump(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def csvout(p,rows):
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');w.writeheader();w.writerows(rows)
def add(name,s,material='Al6082-T6',group='frame',note='',color=None):
    assert s.isValid() and all(x.Closed() for x in s.Shells()),name
    ITEMS.append((name,s,color or (POM if material=='POM-C' else AL),group))
    cq.exporters.export(s,str(O/(name+'.step')));cq.exporters.export(s,str(T/(name+'.brep')))
    bb=s.BoundingBox();density=1.41 if material=='POM-C' else 1.1 if material=='SiF6' else 2.7
    SPECS.append(dict(code=name,material=material,group=group,volume_mm3=s.Volume(),estimated_mass_g=s.Volume()/1000*density,envelope_mm=[bb.xlen,bb.ylen,bb.zlen],note=note))
    return s
def hole(x,y,z,d,axis=(0,0,1),target='',kind='traversant'):
    HOLES.append(dict(piece=target,x=x,y=y,z=z,diametre_mm=d,axe=str(axis),type=kind))
def bolt(code,ref,q,grip,washers,nut,engagement,chosen,note):
    if ref.startswith('M3') and nut:nut=4 # DIN985 M3 maximum nominal height.
    minimum=grip+washers+(nut+1 if nut else engagement)
    assert chosen+1e-8>=minimum,(code,minimum,chosen)
    BOLTS.append(dict(code=code,reference=ref,quantite=q,empilage_mm=grip,rondelles_mm=washers,ecrou_mm=nut,engagement_mm=engagement,longueur_min_mm=round(minimum,2),longueur_retenue_mm=chosen,note=note))

def frame():
    # Four outboard posts attach horizontally to the existing L01 vertical webs.
    # A 1 mm shim spans the gap from web outer face X145 to post inner X146.
    for sign,side in [(-1,'G'),(1,'D')]:
        for yy in [150,355]:
            name=f'R301_montant_{side}_{yy}';s=box(10,30,122,(151,yy,14)).cut(box(7,27,122.2,(151,yy,13.9)))
            for y in [yy-8,yy+8]:
                s=s.cut(cyl(2.25,12,25,145,y,axis=(1,0,0)))
                hole(sign*146,y,25,4.5,axis=(sign,0,0),target=name)
                hole(sign*142,y,25,4.5,axis=(sign,0,0),target='L01_R3_'+side)
            s=s.cut(cyl(1.7,10.2,130,145.9,yy+8,axis=(1,0,0)))
            add(name,s if sign>0 else s.mirror('YZ'),note='Tube10x30x1.5 L122; 2 passagesM4 horizontaux; retenue du bouchonM3 àZ130,Y+8')
            plug=box(6.9,26.9,12,(151,yy,124)).cut(cyl(1.65,12.2,123.9,151,yy)).cut(cyl(1.7,7.1,130,147.45,yy+8,axis=(1,0,0)))
            add(f'R312_bouchon_{side}_{yy}',plug if sign>0 else plug.mirror('YZ'),note='6.9x26.9x12; taraudageM4 axial; retenueM3 décaléeY+8 àZ130')
            hole(sign*151,yy,136,3.3,target=f'R312_bouchon_{side}_{yy}',kind='tarauderM4x0.7 traversant12')
            for y in [yy-8,yy+8]:
                sleeve=cyl(4,7,25,147.5,y,axis=(1,0,0)).cut(cyl(2.25,7.2,25,147.4,y,axis=(1,0,0)))
                add(f'R313_anti_ecrasement_montant_{side}_{y}',sleeve if sign>0 else sleeve.mirror('YZ'),note='OD8/ID4.5 L7; dans montant, autour desM4 de pied')
            for y in [yy-8,yy+8]:
                shim=box(1,8,12,(145.5,y,19)).cut(cyl(2.25,1.2,25,144.9,y,axis=(1,0,0)))
                add(f'R302_cale1_{side}_{y}',shim if sign>0 else shim.mirror('YZ'),material='POM-C',note='1 mm; cale de présentation, pas isolateur de sécurité')
    # Longitudinal and transverse rectangular tubes; all cuts are square.
    for sign,side in [(-1,'G'),(1,'D')]:
        s=box(30,325,10,(sign*151,212.5,136)).cut(box(28,325.2,8,(sign*151,212.5,137)))
        for yy in [150,355]:s=s.cut(cyl(2.25,10.2,135.9,sign*151,yy))
        for yy in [60,335]:
            for y in [yy-8,yy+8]:s=s.cut(cyl(1.7,10.2,135.9,sign*151,y))
        add('R303_rail_'+side,s,note='Tube30x10x1 L325, Y50..375; Z136..146; anti-écrasement8mm')
    for yy in [60,335]:
        s=box(272,30,10,(0,yy,136)).cut(box(272.2,28,8,(0,yy,137)))
        for sign in [-1,1]:
            for y in [yy-8,yy+8]:s=s.cut(cyl(1.7,10.2,135.9,sign*131,y))
        add(f'R304_traverse_{yy}',s,note='Tube30x10x1 L272, entre les rails; Z136..146; anti-écrasement8mm')
        for sign,side in [(-1,'G'),(1,'D')]:
            s=box(40,30,3,(sign*141,yy,146))
            for x in [sign*131,sign*151]:
                for y in [yy-8,yy+8]:s=s.cut(cyl(1.7,3.2,145.9,x,y));hole(x,y,146,3.4,target=f'R305_eclisse_{side}_{yy}')
            add(f'R305_eclisse_{side}_{yy}',s,note='40x30x3, quatre trous Ø3.4, entraxes20x16')
    bolt('R3V01','M4 tête basse classe8.8',8,14,1.6,5,0,25,'L01:3 + cale1 + montant10; deux rondelles0.8; écrouM4')
    bolt('R3V02','M4 tête cylindrique classe8.8',4,10,.8,0,8,20,'Rail10, entretoise anti-écrasement8, engagement9.2 dans bouchon')
    bolt('R3V03','M3 tête cylindrique classe8.8',16,13,1,3.4,0,20,'Éclisse3 + tube10; deux rondelles0.5; écrouM3')
    bolt('R3V05','M3 tête cylindrique classe8.8',4,10,1,3.4,0,16,'Retenue des quatre bouchons; décalée du taraudageM4')

def routes():
    specs=[
      ('P03',[(120,140,95),(120,140,160),(120,60,160),(-55,60,160),(-55,140,160),(-55,140,95)],'F0 sortie → ED80 entrée'),
      ('P04',[(-100,185,95),(-100,185,160),(-180,185,160),(-180,285,160),(-87,285,160),(-87,285,60)],'ED80 sortie → D+'),
      ('P05',[(-87,300,60),(-87,300,175),(-166,300,175),(-166,220,175),(-110,220,175),(-110,220,95)],'D+ → SSR+2'),
      ('P06',[(-80,240,95),(-80,240,160),(108,240,160),(108,368,160),(108,368,78)],'SSR1 → UD80')]
    # P05 lateral last leg56mm is followed by a single corner only after an80mm
    # middle span; choose a wider return point to keep two30mm setbacks clear.
    specs[2]=('P05',[(-87,300,60),(-87,300,175),(-180,300,175),(-180,220,175),(-110,220,175),(-110,220,95)],'D+ → SSR+2')
    for code,points,net in specs:
        wire,length=rounded(points,30)
        plane=cq.Plane(origin=cq.Vector(*points[0]),normal=wire.Edges()[0].tangentAt(0))
        s=cq.Workplane(plane).circle(3.25).sweep(cq.Workplane('XY').newObject([wire]),isFrenet=False).val()
        add(code+'_R3',s,material='SiF6',group='cable',note='Enveloppe isolée Ø6.5; points extrêmes = approches, pas bornes exactes',color=RED)
        ROUTES.append(dict(code=code,net=net,section_mm2=6,diametre_etude_mm=6.5,rayon_axe_mm=30,longueur_axe_mm=round(length,2),reserve_raccordement_mm=300,brut_approvisionnement_mm=math.ceil((length+300)/10)*10,points_mm=points,extremites_sont_bornes_exactes=False,pret_a_couper_definitivement=False))

def clamps():
    # axis X clamp: local X follows the wire; local Y carries the screws.
    # P04 and P05 share X-180 at different elevations, never the same space.
    entries=[('P03',60,60,160,'X','cross'),('P03',0,60,160,'X','cross'),
       ('P04',-180,220,160,'Y','side'),('P04',-180,240,160,'Y','side'),
       ('P05',-180,260,175,'Y','side'),
       ('P06',0,240,160,'X','offset'),('P06',60,240,160,'X','offset'),
       ('P06',108,300,160,'Y','right')]
    for i,(net,x,y,z,axis,mount) in enumerate(entries,1):
        # Cross clamps stand on tube146. Side clamps stand on new bracket149.
        surface=146 if mount=='cross' else 149
        base=box(12,24,7,(0,0,-7)).cut(cyl(3.6,12.2,0,-6.1,0,axis=(1,0,0)))
        cap=box(12,24,5,(0,0,0)).cut(cyl(3.6,12.2,0,-6.1,0,axis=(1,0,0)))
        for yy in [-8,8]:
            base=base.cut(cyl(1.7,7.2,-7.1,0,yy));cap=cap.cut(cyl(1.7,5.2,-.1,0,yy))
        def place(s):
            if axis=='Y':s=s.rotate((0,0,0),(0,0,1),90)
            return s.translate((x,y,z))
        add(f'R307_base_{i:02d}_{net}',place(base),'POM-C','clamp',note='Demi-bride12x24x7; alésage7.2; M3 entraxe16')
        add(f'R308_capot_{i:02d}_{net}',place(cap),'POM-C','clamp',note='Demi-bride12x24x5; serrer sur faces, pas écraser le câble')
        liner=cyl(3.6,10,0,-5,0,axis=(1,0,0)).cut(cyl(3.25,10.2,0,-5.1,0,axis=(1,0,0)))
        add(f'R311_garniture_{i:02d}',place(liner),'Silicone50A','liner',note='Bande silicone nominale0.5, largeur10, longueur~21.5; épaisseur représentée comprimée0.35')
        h=z-7-surface
        for side in [-1,1]:
            xx,yy=(x,y+side*8) if axis=='X' else (x-side*8,y)
            s=cyl(3,h,surface,xx,yy).cut(cyl(1.7,h+.2,surface-.1,xx,yy))
            add(f'R309_entretoise_{i:02d}_{side}',s,'POM-C','clamp',note=f'Ø6/3.4 L{h:g}')
        if mount=='offset':
            s=box(20,115,3,(x,287.5,146))
            for xx in [x-5,x+5]:
                s=s.cut(cyl(1.7,3.2,145.9,xx,335));hole(xx,335,136,3.4,target='R304_traverse_335')
            for yy in [y-8,y+8]:s=s.cut(cyl(1.7,3.2,145.9,x,yy));hole(x,yy,146,3.4,target=f'R306_console_{i:02d}')
            add(f'R306_console_{i:02d}',s,note='Plat20x115x3, porte-à-faux95mm depuis la traverseY335')
        elif mount!='cross':
            cx=-165 if mount=='side' else 129.5;width=60 if mount=='side' else 65
            s=box(width,20,3,(cx,y,146))
            railx=-151 if mount=='side' else 151
            for yy in [y-5,y+5]:s=s.cut(cyl(1.7,3.2,145.9,railx,yy))
            for xx in [x-8,x+8]:s=s.cut(cyl(1.7,3.2,145.9,xx,y))
            add(f'R306_console_{i:02d}',s,note=f'Plat{width}x20x3; centres globaux table perçages')
            for yy in [y-5,y+5]:hole(railx,yy,146,3.4,target=f'R306_console_{i:02d} et R303')
            for xx in [x-8,x+8]:hole(xx,y,146,3.4,target=f'R306_console_{i:02d}')
            if net=='P06' and mount=='side':
                for xx in [x-8,x+8]:hole(xx,y,136,3.4,target=f'R303_rail_G bride{i:02d}')
        else:
            for yy in [y-8,y+8]:hole(x,yy,136,3.4,target=f'R304_traverse_{y}')
        grip=12+h+(10 if mount=='cross' else 13 if net=='P06' and mount=='side' else 3)
        length=next(n for n in [20,25,30,35,40,45,50,55,60,65] if n>=grip+1+3.4+1)
        bolt(f'R3V-C{i:02d}','M3 tête cylindrique classe8.8',2,grip,1,3.4,0,length,f'Bride{net} n°{i}; entretoisesL{h:g}; écrouM3 sous support')
    bolt('R3V04','M3 tête cylindrique classe8.8',12,13,1,3.4,0,20,'Six consoles3 sur tubes10, 2 vis par console')
    # Machine rail/traverse holes from the same recorded bolt coordinates.
    replace=[]
    for name,s,c,g in ITEMS:
        if name.startswith(('R303_','R304_')):
            for h in HOLES:
                if 'R303' in h['piece'] and name.startswith('R303_') and (('G' in name)==(h['x']<0)):
                    s=s.cut(cyl(h['diametre_mm']/2,10.2,135.9,h['x'],h['y']))
                if h['piece']==name:s=s.cut(cyl(h['diametre_mm']/2,10.2,135.9,h['x'],h['y']))
            cq.exporters.export(s,str(O/(name+'.step')));cq.exporters.export(s,str(T/(name+'.brep')))
        replace.append((name,s,c,g))
    ITEMS[:]=replace
    # Anti-crush sleeves wherever a through bolt traverses a hollow tube.
    sleeve=[]
    for sign in [-1,1]:
        for yy in [150,355]:sleeve.append((sign*151,yy,4.5,7))
        for yy in [60,335]:
            for xx in [sign*131,sign*151]:
                for y in [yy-8,yy+8]:sleeve.append((xx,y,3.4,5.5))
    for h in HOLES:
        if 'R303' in h['piece'] or h['piece'].startswith('R304_'):sleeve.append((h['x'],h['y'],3.4,5.5))
    for i,(x,y,bore,od) in enumerate(sleeve,1):
        s=cyl(od/2,8,137,x,y).cut(cyl(bore/2,8.2,136.9,x,y))
        add(f'R310_anti_ecrasement_{i:02d}',s,note=f'Tube usiné OD{od:g}/ID{bore:g} L8, insérer par extrémité avant assemblage')
    # Custom sleeves occupy only the hollow volume, not tube walls.

def build():
    start=time.time();frame();routes();clamps()
    base=cq.Assembly.load(str(ROOT/'Assemblage/R2/drone-v3-r2-etude.step'))
    assembly=cq.Assembly(name='DroneV3_R3_faisceau_etude')
    base_objects=[]
    for child in base.children:
        s=child.obj
        if child.name.startswith('L01_longeron_'):
            sign=-1 if child.name.endswith('-1') else 1
            for yy in [150,355]:
                for y in [yy-8,yy+8]:s=s.cut(cyl(2.25,5,25,sign*141,y,axis=(sign,0,0)))
            add('L01_R3_'+('G' if sign<0 else 'D'),s,note='L01 R2 conservé, quatre trousØ4.5 supplémentaires dans aile verticale')
            # Added separately, avoid duplicate L01.
            continue
        assembly.add(child,name=child.name)
        base_objects.append((child.name,s,child.loc))
    for name,s,c,g in ITEMS:assembly.add(s,name=name,color=cq.Color(*c))
    dest=A/'drone-v3-r3-faisceau.step';assembly.export(str(dest),exportType='STEP',unit='MM',outputUnit='MM')
    sub=cq.Assembly(name='Complement_R3')
    for name,s,c,g in ITEMS:sub.add(s,name=name,color=cq.Color(*c))
    sub.export(str(O/'complement-r3.step'),exportType='STEP',unit='MM',outputUnit='MM')
    # Save exact flattened scene for independent checks; retain source placement.
    scene=[]
    for name,s,loc in base_objects:
        s=s.moved(loc);p=T/('base-'+name+'.brep');cq.exporters.export(s,str(p));scene.append(dict(name=name,file=p.name,group='base'))
    for name,s,c,g in ITEMS:scene.append(dict(name=name,file=name+'.brep',group=g))
    # Refresh final cut volumes after rail drilling, not pre-drill estimates.
    smap={n:s for n,s,c,g in ITEMS}
    for row in SPECS:
        row['volume_mm3']=smap[row['code']].Volume()
        density=1.41 if row['material']=='POM-C' else 1.1 if row['material']=='SiF6' else 1.2 if row['material']=='Silicone50A' else 2.7
        row['estimated_mass_g']=row['volume_mm3']/1000*density
    dump(T/'scene.json',scene);dump(B/'pieces.json',SPECS);dump(B/'parcours.json',ROUTES)
    csvout(P/'percages-globaux-r3.csv',HOLES);csvout(B/'visserie-r3.csv',BOLTS)
    csvout(B/'longueurs-cables.csv',[{k:v for k,v in r.items() if k!='points_mm'} for r in ROUTES])
    dump(V/'generation.json',dict(seconds=time.time()-start,parts=len(SPECS),assembly_objects=len(assembly.children),step=str(dest.relative_to(ROOT)),sha256=sha(dest),R2_source_sha256=sha(ROOT/'Assemblage/R2/drone-v3-r2-etude.step'),terminal_coordinates_measured=False,hardware_tested=False))
    # Preserve, outside the delivery folder, obsolete files from our iterations.
    expected={r['code']+'.step' for r in SPECS}|{'complement-r3.step'}
    stale=T/'iterations';stale.mkdir(exist_ok=True)
    for p in O.glob('*.step'):
        if p.name not in expected:
            assert p.resolve().is_relative_to(ROOT) and stale.resolve().is_relative_to(ROOT)
            p.rename(stale/(str(time.time_ns())+'-'+p.name))
    print('BUILD',len(SPECS),'parts',len(assembly.children),'objects',flush=True)
if __name__=='__main__':sys.stdout.reconfigure(encoding='utf-8');build()
