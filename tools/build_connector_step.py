"""Detailed, coloured XT60H reconstructions: manufacturer envelopes, estimated internals."""
from pathlib import Path
import json,hashlib,sys,math
import cadquery as cq
from build_running_gear_step import box,cyl,tube,export_model
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/connecteurs-alimentation'
YELLOW=(.95,.54,.008);GOLD=(.72,.46,.10);BLACK=(.055,.065,.080)
RED=(.65,.012,.008);WIREBLACK=(.012,.016,.020);COPPER=(.57,.23,.06);TIN=(.50,.53,.56)
SOURCE='https://www.china-amass.com/public/upload/20260207/7fa24f5a6f35ec66c7a115c07a34ab06.pdf'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def keyed(w,h,length,z=0):
    a=w/2;b=h/2;c=1.8
    return cq.Workplane('XY').polyline([(-a,-b),(a-c,-b),(a,-b+c),(a,b-c),(a-c,b),(-a,b)]).close().extrude(length).edges('|Z').fillet(.22).val().translate((0,0,z))
def lettering(shape,label,origin,size=1.8):
    plane=cq.Plane(origin=origin,xDir=(1,0,0),normal=(0,-1,0))
    letters=cq.Workplane(plane).text(label,size,.3,font='Arial',kind='bold',combine=True).val()
    return shape.cut(letters)
def cap_at(z):
    length=11.8
    s=box(16.4,9.2,length,(0,0,z),1.25)
    # Open front cavity, then two real wire exits in the rear wall.
    s=s.cut(box(14.65,7.45,length-1.55,(0,0,z-.05),.7))
    for x in (-3.6,3.6):s=s.cut(cyl(2.25,length+.2,z-.1,x))
    # Three shallow grip scallops on each broad face, closed geometry.
    for dz in (3.1,5.5,7.9):
        for y in (-4.73,4.73):
            groove=box(11.2,.66,1.15,(0,y,z+dz),.28)
            s=s.cut(groove)
    # Snap windows at the front and split-line relief, dimensions estimated.
    for x in (-8.15,8.15):s=s.cut(box(.7,3.1,1.65,(x,0,z+.6),.12))
    return s.clean()
def connector(gender):
    # Current 2026 catalogue, page 15: overall F24.95, M23.85; 16.4 x 9.2.
    shoulder=9.1 if gender=='F' else 8.0
    front=keyed(14.8,7.6,shoulder) if gender=='F' else keyed(16.0,8.75,shoulder)
    if gender=='M':front=front.cut(keyed(15.02,7.84,7.82,-.03))
    collar=box(16.4,9.2,4,(0,0,shoulder),1.0)
    neck=box(14.2,7.05,3.0,(0,0,shoulder+4),.75)
    body=front.fuse(collar).fuse(neck)
    for x in (-3.6,3.6):body=body.cut(cyl(2.14,shoulder+7.2,-.1,x))
    if gender=='F':
        # A moulded key protrusion visible on the manufacturer photograph.
        body=body.fuse(box(1.0,1.45,shoulder,(0,0,0),.16))
    body=lettering(body,'XT60H-'+gender,(0,-4.44,shoulder+2.0),1.72)
    # Polarity symbols on a broad side; use actual part markings when wiring.
    for x,label in [(-5.8,'-'),(5.8,'+')]:body=lettering(body,label,(x,-4.44,shoulder+.8),1.4)
    body=body.clean();parts=[(f'Boitier_PA_XT60H_{gender}',body,YELLOW)]
    for i,x in enumerate((-3.6,3.6)):
        if gender=='F':
            c=cyl(2.10,shoulder+10.75,.12,x)
            c=c.cut(cyl(1.77,shoulder-.72,-.01,x))
            c=c.cut(cq.Solid.makeCone(1.92,1.77,.35,cq.Vector(x,0,.12),cq.Vector(0,0,1)))
        else:
            c=cyl(2.10,11.37,shoulder-.5,x).fuse(cyl(1.75,shoulder-.55,.45,x))
            c=c.cut(cyl(.68,shoulder-1.5,.4,x))
            for angle in (0,90):
                slot=box(.23,3.8,shoulder-2,(x,0,.35)).rotate((x,0,0),(x,0,1),angle)
                c=c.cut(slot)
            # A rounded entrance chamfer is estimated, not a gauge dimension.
            c=c.cut(cq.Solid.makeCone(.91,.68,.3,cq.Vector(x,0,.45),cq.Vector(0,0,1)))
        cup_z=shoulder+5.3
        c=c.cut(cyl(1.65,5.7,cup_z,x))
        # Open half-cup at the soldering end, matching the current product photo.
        c=c.cut(box(4.5,2.3,4.0,(x,1.18,shoulder+7.0)))
        # Small retention recess around the embedded barrel (estimated).
        recess=cyl(2.14,.32,shoulder+1.1,x).cut(cyl(1.98,.35,shoulder+1.09,x))
        c=c.cut(recess).clean()
        parts.append((f'Contact_{gender}_{i+1}_laiton_dore',c,GOLD))
    parts.append(('Capot_PA_gris_sombre',cap_at(shoulder+4.05),BLACK))
    return parts
def transform(parts,offset=(0,0,0),rotate=False,prefix=''):
    return [(prefix+n,(s.rotate((0,0,0),(1,0,0),180) if rotate else s).translate(offset),c) for n,s,c in parts]
def wire_shape(x,outer,start,inner=None):
    d=-1 if x<0 else 1
    edges=[cq.Edge.makeLine(cq.Vector(x,0,start),cq.Vector(x,0,27)),
        cq.Edge.makeBezier([cq.Vector(*p) for p in [(x,0,27),(x,0,40),(x+5*d,2.5,54),(x+5*d,2.5,67)]])]
    wire=cq.Wire.assembleEdges(edges);profile=cq.Workplane(cq.Plane(origin=(x,0,start),normal=(0,0,1))).circle(outer)
    if inner:profile=profile.circle(inner)
    s=profile.sweep(cq.Workplane('XY').newObject([wire]),isFrenet=False).val()
    assert s.isValid() and len(s.Solids())==1
    if inner:s=s.cut(box(50,50,6,(0,0,63.5)))
    # Material samples through the line/Bezier junction and every curved section.
    radius=(outer+inner)/2 if inner else outer*.7
    samples=0
    for edge in edges:
        for u in [0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1]:
            p=edge.positionAt(u);t=edge.tangentAt(u).normalized()
            if p.z<=start+.2 or p.z>=63.2:continue
            a=t.cross(cq.Vector(0,1,0)).normalized();b=t.cross(a).normalized()
            for j in range(12):
                ang=j*math.pi/6;q=p+a.multiply(radius*math.cos(ang))+b.multiply(radius*math.sin(ang))
                assert s.isInside(q,1e-6),(x,start,inner,u,j,'wire continuity')
                samples+=1
    return s,samples
def main():
    sys.stdout.reconfigure(encoding='utf-8');out=BASE/'3D';out.mkdir(parents=True,exist_ok=True)
    f=connector('F');m=connector('M');cap=cap_at(0)
    pair=transform(f,(0,0,7.5),True,'F_')+transform(m,prefix='M_')
    # Illustrative 7.5 mm engagement, neither measured nor specified by supplier.
    interference=[]
    for n,a,c in pair[:4]:
        for nn,b,cc in pair[4:]:
            volume=a.intersect(b).Volume()
            if volume>1e-5:interference.append(dict(a=n,b=nn,mm3=volume))
    assert not interference,interference
    exploded=[]
    for gender,parts,dx in [('F',f,-13),('M',m,13)]:
        for n,s,c in parts:
            if 'Capot' in n:s=s.translate((0,0,16))
            elif 'Contact' in n:s=s.translate((0,0,6))
            exploded.append((gender+'_'+n,s.translate((dx,0,0)),c))
    wired=list(f);wire_checks=[]
    for i,x in enumerate((-3.6,3.6)):
        core,core_samples=wire_shape(x,math.sqrt(3.31/math.pi),15.4)
        jacket,jacket_samples=wire_shape(x,2.1,22.0,math.sqrt(3.31/math.pi))
        # Insulation starts behind the solder cups; exposed remote end intentional.
        solder=cyl(1.65,4.55,15.4,x).cut(cyl(math.sqrt(3.31/math.pi),4.7,15.35,x))
        assert f[i+1][1].distance(solder)<1e-6 and solder.distance(core)<1e-6,'bond discontinuity'
        wire_checks.append(dict(contact=i+1,core_solids=len(core.Solids()),jacket_solids=len(jacket.Solids()),
            core_material_samples=core_samples,jacket_material_samples=jacket_samples,bond_gap_mm=0,
            core_start_in_cup_z_mm=15.4,insulation_start_z_mm=22.0,remote_strip_start_z_mm=63.5))
        wired += [(f'Conducteur_cuivre_{i+1}_12AWG_equivalent',core,COPPER),
            (f'Gaine_silicone_{i+1}_illustration',jacket,RED if x>0 else WIREBLACK),
            (f'Soudure_{i+1}_illustration',solder,TIN)]
    published=['F24.95 ou M23.85 mm ; largeur16.4, hauteur9.2 : catalogue AMASS2026 p15',
        'Deux contacts : femelle F cote source, male M cote ESC ; PA, laiton dore',
        'Entraxe7.20 : fiche historique V1.2, conserve comme hypothese de compatibilite courante']
    estimated=['Reconstruction parametrique, pas CAO native fabricant ni piece mesuree',
        'Profils, profondeurs, epaisseurs, rainures, clips, contacts3.5, godets3.3 et rayons estimes',
        'Front F9.1, M8.0 et capot11.8 : repartition estimee des longueurs officielles',
        'Marquages simplifiés graves et teintes visuelles ; pas de microtexture ni placage physique',
        'Accouplement7.5 et jeux non qualifies ; plan fabricant en ligne arronditF25/M23.9',
        'Catalogue2026 differe deV1.2 F23.5/M23.8 ; lot Amazon a mesurer avant usinage']
    defs=[('amass-xt60h-f-detaille.step','XT60H-F | prise faisceau avec capot',f),
        ('amass-xt60h-m-detaille.step','XT60H-M | reference cote variateur',m),
        ('amass-xt60h-f-sans-capot.step','XT60H-F | contacts et godets visibles',f[:-1]),
        ('amass-xt60h-m-sans-capot.step','XT60H-M | broches fendues et godets',m[:-1]),
        ('amass-xt60h-capot-detaille.step','XT60H | capot commun estime', [('Capot_PA_gris_sombre',cap,BLACK)]),
        ('amass-xt60h-paire-accouplee.step','XT60H F et M | assemblage illustratif',pair),
        ('amass-xt60h-paire-eclatee.step','XT60H F et M | vue eclatee',exploded),
        ('amass-xt60h-f-cable-12awg-illustration.step','XT60H-F | deux fils illustratifs',wired)]
    models=[]
    for filename,title,parts in defs:
        item=dict(folder='connecteurs-alimentation',filename=filename,title=title,parts=parts,published=published,
            estimated=estimated,params=dict(F_length_mm=24.95,M_length_mm=23.85,width_mm=16.4,height_mm=9.2,
            historical_pitch_mm=7.2,cap_length_estimated_mm=11.8,mating_depth_estimated_mm=7.5),
            view=(.9,-1.15,-.8) if 'eclatee' not in filename and 'cable' not in filename else (.9,-1.3,.8),
            design=False,probes=[],source_pages=[SOURCE,'https://www.shoptronica.com/ficheros/XT60H.pdf'])
        result=export_model(item)
        result.update(generated_on='2026-10-14',coordinate_system='X entraxe contacts, Y epaisseur, Z axe de connexion ; face avant z0 ; fils vers +Z',
            generator='tools/build_connector_step.py',generator_sha256=sha(Path(__file__)),mating_overlap_check=interference if 'accouplee' in filename else None,
            wires_hardware_specified=False,polarity_orientation_illustrative=True,
            wire_continuity_checks=wire_checks if 'cable' in filename else [])
        (out/Path(filename).with_suffix('.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');models.append(result)
    (out/'catalogue.json').write_text(json.dumps(dict(generated_on='2026-10-14',model_count=len(models),models=models),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    rows=['# Modèles STEP détaillés - AMASS XT60H','',
        'Huit reconstructions colorées AP214. Les enveloppes suivent le catalogue AMASS 2026 ; les détails non cotés sont estimés et consignés dans chaque JSON. Aucun modèle natif exact retrouvé dans les téléchargements fabricant consultés. Le lot à acheter n’a pas été mesuré.','',
        '| Modèle | Solides / faces | STEP | Aperçu | Provenance |','| --- | ---: | --- | --- | --- |']
    for r in models:
        rows.append(f"| {r['title']} | {r['validation']['solids']} / {r['validation']['faces']} | [{r['file']}]({r['file']}) | [PNG]({r['preview']['file']}) | [JSON]({Path(r['file']).with_suffix('.json')}) |")
    rows += ['', 'Le F seul est le complément à ajouter au faisceau. Le M représente l’interface existante du variateur et n’est pas un achat supplémentaire obligatoire.', '',
        'Le capot commun est une reconstruction : compatibilité réelle et clips à vérifier. Accouplement de 7,5 mm illustratif, contrôlé sans chevauchement volumique mais sans qualification d’ajustement. La vue éclatée déplace contacts et capots pour lecture.', '',
        'Les deux fils du modèle câblé sont des illustrations : 3,31 mm² de cuivre équivalent et gaine Ø4,2 mm estimée, longueur/chemin non arrêtés. Les extrémités distantes dénudées sont intentionnelles ; aucun câble réel n’est ainsi laissé libre sous tension. Le cuivre est continu du godet à l’extrémité. Les polarités CAO sont indicatives : se référer aux signes du lot.', '',
        'Attention aux révisions : V1.2 F23,50/M23,80 ; catalogue 2026 F24,95/M23,85 ; page produit arrondie F25,00/M23,90 mm. Réserver 25 mm pour une prise F hors fils, puis mesurer avant support ou fabrication.', '',
        '[Contrôles FreeCAD](validation-freecad.json), [catalogue](catalogue.json), [cotes](../cotes.md), [notice et sélection](../README.md).', '']
    (out/'README.md').write_text('\n'.join(rows),encoding='utf-8')
    print('DONE',len(models),'STEP',flush=True)
if __name__=='__main__':main()
