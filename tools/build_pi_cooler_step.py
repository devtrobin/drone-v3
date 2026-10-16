"""Detailed Active Cooler reconstruction: documented envelope, estimated local details.

Never rewrites the Pi STEP. Includes physical fins, rotor, pins, helical springs,
three pads and four continuous wires. Vendor drawing is reference-only.
"""
from pathlib import Path
import math,json,sys,hashlib,itertools
import cadquery as cq
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from build_running_gear_step import box,cyl,ring,hexagon,export_model,sha
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/refroidissement-raspberry-pi-5';OUT=BASE/'3D'
SILVER=(.61,.63,.66);STEEL=(.42,.45,.49);BLACK=(.015,.018,.023);WHITE=(.89,.88,.83);PAD=(.49,.64,.94);MARK=(.16,.17,.18)
RED=(.66,.012,.008);BLUE=(.01,.10,.66);YELLOW=(.87,.62,.013);TIN=(.46,.50,.54)
PINS=[(2.75,2.75),(60.75,39.75)];FAN=(42,27.5);SCREWS=[(31,40),(54.5,40),(54.5,15)]

def optimal_bounds(self,tolerance=None):
    bb=Bnd_Box();BRepBndLib.AddOptimal_s(self.wrapped,bb,False,False);return cq.BoundBox(bb)

def sink(detailed=True):
    outline=[(2.75,0),(33.5,0),(36.5,.7),(44,9.5),(47,12.5),(60.5,12.5),(63.5,15.5),(63.5,42.5),
        (6.3,42.5),(6.3,10),(5.8,8.5),(.3,3.7),(0,2.75),(.7,1)]
    base=cq.Workplane('XY').polyline(outline).close().extrude(1.4).val()
    # Six columns x nine cut segments, visible in maker plan and underside photos.
    fin=box(2.05,2.95,7.8,(0,0,1.4))
    if detailed:
        for z in np.arange(2.15,8.95,.85):
            for sign in [-1,1]:fin=fin.cut(box(.28,3.1,.18,(sign*1.0,0,float(z))))
    fins=[fin.translate((8.1+col*3.45,1.6+row*4.85,0)) for col in range(6) for row in range(9)]
    s=base
    for i,f in enumerate(fins):s=s.fuse(f)
    for x,y in PINS:s=s.cut(cyl(1.5,1.6,-.1,x,y))
    for x,y in SCREWS:s=s.cut(cyl(.85,1.6,-.1,x,y))
    s=s.clean();assert s.isValid() and len(s.Solids())==1
    return s

def logo():
    d=json.loads((BASE/'cotes-logo-vecteur.json').read_text(encoding='utf-8'));groups=[];current=[]
    for item in d['segments']:
        if item[0]!='l':continue
        a,b=item[1:];a=tuple(a);b=tuple(b)
        if current and math.dist(a,current[-1])>.003:current=[]
        if not current:current=[a]
        current.append(b)
        if len(current)>3 and math.dist(b,current[0])<.003:
            groups.append(current[:-1]);current=[]
    solids=[];scale=180/63.5
    for pts in groups:
        p=[((x-115.7942)/scale,42.5-(y-136.073)/scale) for x,y in pts]
        try:
            shape=cq.Workplane('XY').polyline(p).close().extrude(.018).val().translate((0,0,1.4))
            if shape.isValid() and shape.Volume()>1e-5:solids.append(shape)
        except Exception:continue
    assert solids,('logo vector conversion produced no closed contours',len(groups))
    # Even-odd filling: nested contours leave their centre open, disjoint leaves stay separate.
    solids.sort(key=lambda s:s.Volume(),reverse=True);result=solids[0]
    for s in solids[1:]:result=result.cut(s).fuse(s.cut(result))
    result=result.clean();assert result.isValid() and result.Solids()
    return result,dict(closed_loops_used=len(solids),source_line_segments=len(d['segments']),nominal_relief_mm=.018,
        depth_estimated=True,source_pdf='notices/RaspberryPi-ActiveCooler-plan-reference-original.pdf',drawing_scale_points_per_mm=scale,
        optical_mark_only=True)

def plastic_pin(x,y):
    shank=cyl(.9,9.95,-1.05)
    tail=cq.Solid.makeCone(.5,1.60,2.4,cq.Vector(0,0,-3.2),cq.Vector(0,0,1))
    tip=tail.fuse(cyl(1.25,.35,-1.0)).fuse(shank)
    tip=tip.cut(box(.55,4,3.0,(0,0,-3.21)))
    head=hexagon(4.7631397208,1.6,8.9)
    pin=tip.fuse(head).clean();assert pin.isValid() and len(pin.Solids())==1
    return pin.translate((x,y,0))

def spring(x,y):
    helix=cq.Wire.makeHelix(.85,6.8,2.05)
    plane=cq.Plane(origin=helix.Edges()[0].startPoint(),normal=helix.Edges()[0].tangentAt(0))
    coil=cq.Workplane(plane).circle(.22).sweep(cq.Workplane('XY').newObject([helix]),isFrenet=False).val().translate((x,y,1.65))
    coil=coil.intersect(cyl(4,7.25,1.65,x,y)).clean()
    assert coil.isValid() and len(coil.Solids())==1
    return coil

def blower():
    x,y=FAN;parts=[]
    housing=box(30,30,7.5,(x,y,1.4),.45)
    housing=housing.cut(cyl(11.4,7.0,2.08,x,y))
    # Outlet faces the fins; bottom and side walls remain connected.
    housing=housing.cut(box(6.4,18,5.9,(29.9,y,2.08)))
    for xx,yy in SCREWS:housing=housing.cut(cyl(.85,8,1.3,xx,yy))
    # Small lead exit opening in the rear wall (assumed geometry).
    housing=housing.cut(box(2.0,4.3,1.35,(56.9,39,4.2))).clean()
    parts.append(('Ventilateur_coque_noire_reconstruite',housing,BLACK))
    cover=box(30,30,.38,(x,y,8.9),.22).cut(cyl(11.1,.58,8.8,x,y))
    for xx,yy in SCREWS:cover=cover.cut(cyl(.85,.6,8.8,xx,yy))
    for xx in (31,54.5):
        tab=box(3.2,.40,4.4,(xx,12.68,4.7)).cut(box(1.7,.8,2.4,(xx,12.68,5.5)))
        # Thin metal folds meet the lid through a continuous side strip.
        bridge=box(3.2,.40,.6,(xx,12.68,8.65))
        cover=cover.fuse(tab).fuse(bridge)
    cover=cover.clean();assert cover.isValid() and len(cover.Solids())==1
    housing=housing.cut(cover).clean()
    parts[0]=('Ventilateur_coque_noire_reconstruite',housing,BLACK)
    parts.append(('Capot_argente_et_deux_agrafes_estimes',cover,SILVER))
    rotor=cyl(10.6,.8,2.2,x,y).fuse(cyl(6.4,4.7,2.8,x,y))
    blade=(cq.Workplane('XY').moveTo(6.3,0).threePointArc((8.5,-.45),(10.2,-1.8))
        .lineTo(10.5,-1.2).threePointArc((8.7,.18),(6.3,.52)).close().extrude(3.75).val().translate((0,0,2.85)))
    for i in range(30):rotor=rotor.fuse(blade.rotate((0,0,0),(0,0,1),i*12).translate((x,y,0)))
    rotor=rotor.cut(cyl(.35,.12,7.42,x,y)).clean()
    assert rotor.isValid() and len(rotor.Solids())==1
    parts.append(('Rotor_visible_30_aubes_nombre_estime',rotor,BLACK))
    for i,(xx,yy) in enumerate(SCREWS):
        head=cyl(1.36,1.15,9.28,xx,yy)
        recess=cyl(.44,.60,9.93,xx,yy)
        for a in range(6):recess=recess.fuse(cyl(.25,.60,9.93,xx+.54*math.cos(a*math.pi/3),yy+.54*math.sin(a*math.pi/3)))
        head=head.cut(recess).clean();parts.append((f'Tete_vis_{i+1}_empreinte_6lobes_estimee',head,STEEL))
    return parts

def pads():
    # Three pads observed in the underside supplier photograph; dimensions unknown.
    return [
        ('Pad_CPU_17x17_ep0_5_estime',box(17,17,.5,(32.4,16,-.5)),PAD),
        ('Pad_RAM_14x10_ep1_estime',box(14,10,1,(32.4,32.45,-1)),PAD),
        ('Pad_PMIC_8x8_ep1_5_estime',box(8,8,1.5,(10.45,8.45,-1.5)),PAD)]

def wire(i,radius):
    off=i-1.5;px=66.75;py=39+off
    # Four identical XZ curves, separated along Y by the documented1mm pitch.
    # This is illustrative free pose, not a Pi-board installed-cable simulation.
    start=(56.85,py,4.8)
    joint=(65.5,py,9.0)
    penultimate=(64,py,10)
    control=(67,py,8)
    spans=[ [start,(61,py,4.8),penultimate,joint],
            [joint,control,(px,py,7.0),(px,py,2.5)] ]
    edges=[cq.Edge.makeBezier([cq.Vector(*p) for p in seg]) for seg in spans]
    path=cq.Wire.assembleEdges(edges);plane=cq.Plane(origin=start,normal=edges[0].tangentAt(0))
    shape=cq.Workplane(plane).circle(radius).sweep(cq.Workplane('XY').newObject([path]),isFrenet=False).val()
    assert shape.isValid() and len(shape.Solids())==1
    for edge in edges:
        for u in np.linspace(0,1,41):assert shape.isInside(edge.positionAt(float(u)),1e-6)
    return shape,edges

def harness():
    parts=[];checks=[];gaine=[]
    # Current official pinout; contact numbering belongs to the mate's documented view.
    for i,(label,color) in enumerate([('1_5V_rouge',RED),('2_PWM_bleu',BLUE),('3_GND_noir',BLACK),('4_TACH_jaune',YELLOW)]):
        outer,edges=wire(i,.30);core,_=wire(i,.105);sleeve=outer.cut(core).clean()
        assert sleeve.isValid() and len(sleeve.Solids())==1
        # Check material on 24 positions and four quadrants along each span,
        # rather than only proving the sweep is a formally closed solid.
        samples=0
        for edge in edges:
            for u in np.linspace(.02,.98,24):
                pos=edge.positionAt(float(u));t=edge.tangentAt(float(u)).normalized();n=t.cross(cq.Vector(0,0,1))
                if n.Length<.01:n=t.cross(cq.Vector(1,0,0))
                n=n.normalized();b=t.cross(n).normalized()
                for a in [0,math.pi/2,math.pi,3*math.pi/2]:
                    point=pos+n*(.23*math.cos(a))+b*(.23*math.sin(a))
                    assert sleeve.isInside(point,1e-5);samples+=1
        gaine.append(outer);parts.extend([(f'Fil_{label}_ame_equivalente_continue',core,TIN),(f'Fil_{label}_gaine_continue',sleeve,color)])
        checks.append(dict(pin=i+1,core_solids=1,sheath_solids=1,curve_spans=2,material_samples=samples,
            centreline_samples=82,endpoint=[66.75,39+(i-1.5),2.5],tangent_continuity=True))
    overlaps=[]
    for i,j in itertools.combinations(range(4),2):
        v=gaine[i].intersect(gaine[j]).Volume();assert v<1e-6,(i,j,v);overlaps.append(dict(pair=[i+1,j+1],overlap_mm3=v))
    plug=box(2.8,5.9,3.6,(66.75,39,0),.15)
    for i in range(4):
        yy=39+(i-1.5)
        plug=plug.cut(box(1.15,.72,2.55,(66.75,yy,-.01)))
        plug=plug.cut(cyl(.33,1.25,2.45,66.75,yy))
        contact=box(.84,.52,2.4,(66.75,yy,.10)).cut(box(.48,.30,2.6,(66.75,yy,0)))
        # Cap bridges to the wire core; wire enters at2.5, buried in housing.
        contact=contact.fuse(box(.84,.52,.18,(66.75,yy,2.4))).clean()
        parts.append((f'Contact_JST_pin_{i+1}_estime',contact,TIN))
    plug=plug.fuse(box(.45,4.9,1.1,(68.2,39,.4))).clean()
    parts.append(('Fiche_4voies_pas1mm_forme_estimee',plug,WHITE))
    return parts,checks,overlaps

def item(name,title,parts,params,view=(.6,-1,1.3),limits=None):
    return dict(folder='refroidissement-raspberry-pi-5',filename=name,title=title,parts=parts,
        params=params,published=['Plan fabricant:63.5x42.5mm; hauteur13.7mm avec attaches; ventilateur30x30mm; cotes approximatives',
            'Fiche janvier2026:5V, PWM/tach, dissipateur anodise,3vis,2attaches avec ressorts,pads preposes',
            'Documentation Pi:connecteur JST-SH4voies pas1mm; ordre5V/PWM/GND/TACH et rouge/bleu/noir/jaune'],
        estimated=limits or LIMITS,view=view,design=False,probes=[],
        source_pages=['RaspberryPi-ActiveCooler-fiche-actuelle-originale.pdf p.2-6','RaspberryPi-ActiveCooler-plan-reference-original.pdf p.1',
            'Photos fournisseur Waveshare original1/3/5/7','Documentation RaspberryPi computer hardware,FAN pinout'])

LIMITS=[
 'Reconstruction, pas un STEP natif fabricant ni du materiel mesure. Le plan ne donne pas de tolerances de production.',
 'Contour local, position/diametre des trous, epaisseur1.4mm et repartition de hauteur reconstruits.',
 '54segments6x9 observes; epaisseur2.05, entraxes3.45/4.85mm et stries0.18mm estimes.',
 'Rotor visible30aubes: nombre/profil estimes; moteur, bobinages et electronique internes non documentes non inventes.',
 'Trois pads observes dessous; dimensions17x17/14x10/8x8, epaisseurs0.5/1/1.5 et placement estimes, non qualifies sur composants.',
 'Attaches entraxes58x37 issus de lecture du plan Pi, et geometrie des clips/ressorts estimes, sans classe de tolerance.',
 'Marquage vectoriel issu du plan, relief0.018mm de lecture non physique; couleur reconstituee.',
 'Fils0.60mmOD et ame0.21mm equivalente, longueur et courbes de pose estimes; pas un cordon de remplacement specifie.',
 'Connecteur:pas1mm documente, boitier et contacts reconstruits; vue de numerotation a confirmer avant fabrication.',
 'L encombrement cable compris depend de la pose;13.7mm du dessin n est pas la hauteur reservee au-dessus du PCB installe.',
 'Les quatre fichiers sont des variantes de lecture, pas quatre refroidisseurs a acheter.']

def main():
    sys.stdout.reconfigure(encoding='utf-8');cq.Shape.BoundingBox=optimal_bounds;OUT.mkdir(parents=True,exist_ok=True)
    print('BUILD sink',flush=True);base=sink();print('BUILD logo',flush=True);mark,logo_info=logo();parts=[('Dissipateur_aluminium_54segments_stries',base,SILVER),('Marquage_RaspberryPi_contours_plan',mark,MARK)]
    for i,(x,y) in enumerate(PINS):
        parts += [(f'Attache_blanche_{i+1}_clip_fendu',plastic_pin(x,y),WHITE),
            (f'Ressort_helicoidal_{i+1}_pas0_85_estime',spring(x,y),STEEL),
            (f'Rondelle_appui_{i+1}_estimee',ring(2.55,1.05,.25,1.4).translate((x,y,0)),WHITE)]
    print('BUILD blower and harness',flush=True);module=parts+blower()+pads();wires,continuity,overlaps=harness()
    par=dict(body_plan_mm=[63.5,42.5],module_height_with_pushpins_reference_mm=13.7,fan_body_mm=[30,30],
        pin_centres_study_mm=PINS,pins2d_delta=[58,37],fin_segments=54,fin_columns=6,fin_rows=9,rotor_blades_estimated=30,
        connector_pitch_mm=1,thermal_pads=3,logo=logo_info)
    # Validate separation of main physical groups (optical mark excluded).
    physical=[s for n,s,c in module if 'Marquage' not in n]
    collisions=[]
    for (i,a),(j,b) in itertools.combinations(enumerate(physical),2):
        v=a.intersect(b).Volume()
        if v>1e-5:collisions.append(dict(parts=[i,j],volume_mm3=v))
    par['physical_pair_overlaps']=collisions;assert not collisions,collisions;print('PHYSICAL_OVERLAPS',collisions,flush=True)
    # The estimated lid folds intentionally wrap the outer plastic wall. No
    # global mechanical fit is claimed; record any reconstruction overlaps.
    models=[item('raspberry-pi-active-cooler-sc1148-detaille.step','Raspberry Pi Active Cooler SC1148 | detaille',module+wires,
            dict(**par,cable_continuity_checks=continuity,cable_pair_overlap_checks=overlaps)),
        item('raspberry-pi-active-cooler-sc1148-sans-cable.step','Active Cooler SC1148 | module sans cable',module,par),
        item('raspberry-pi-active-cooler-dissipateur-detaille.step','Active Cooler | dissipateur 54 segments',parts[:2],par,view=(.7,-1,1.15)),
        item('raspberry-pi-active-cooler-implantation-legere.step','Active Cooler | implantation sans stries ni logo',
            [('Dissipateur_sans_stries_simplifie',sink(False),SILVER)]+[t for t in module[2:]],
            dict(**par,omitted_details=['stries des ailettes','marquage vectoriel','cordon complet']),
            limits=LIMITS+['Variante legere: stries et marquage omis; pas un remplacement du detail ni un plan de fabrication'])]
    results=[]
    for model in models:
        m=export_model(model);m.update(generated_on='2026-10-14',generator='tools/build_pi_cooler_step.py',generator_sha256=sha(Path(__file__)),
            coordinate_system='Module:base z0..1.4; fins vers+Z; attaches aux(2.75,2.75)/(60.75,39.75); fan centre(42,27.5). Axe pins Z.',
            wire_continuity_checks=[],
            source_manifest_sha256=sha(BASE/'assets.json'))
        # Explicit filename criterion (no interpretation of light variant).
        m['wire_continuity_checks']=continuity if model['filename']=='raspberry-pi-active-cooler-sc1148-detaille.step' else []
        (OUT/Path(m['file']).with_suffix('.json')).write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');results.append(m)
    catalog=dict(generated_on='2026-10-14',model_count=4,models=results,generator='tools/build_pi_cooler_step.py',generator_sha256=sha(Path(__file__)))
    (OUT/'catalogue.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUT/'provenance.json').write_text(json.dumps(dict(**catalog,source_manifest_sha256=sha(BASE/'assets.json'),native_vendor_cad=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# STEP de l’Active Cooler SC1148','','**Quatre variantes colorées en millimètres.** Une seule unité à acheter ; les autres fichiers facilitent la lecture ou l’implantation.','',
        '| Variante | STEP | Aperçu | Taille |','| --- | --- | --- | --- |']
    for m in results:lines.append(f'| {m["title"]} | [STEP]({m["file"]}) | [PNG]({m["preview"]["file"]}) | {m["bytes"]/1e6:.2f}Mo |')
    lines+=['','Le fichier complet représente les ailettes striées, le rotor visible, le capot, les têtes de vis, les deux clips fendus avec ressorts hélicoïdaux, trois pads, le marquage du plan, quatre fils continus et leur fiche.',
        '', 'Les dimensions de référence sont approximatives. Toutes les cotes locales inconnues sont signalées dans les JSON. Les fils sont placés pour l’illustration, pas à une longueur garantie. Les variantes sans cordon l’omettent volontairement. La version d’implantation omet aussi les stries et le logo pour une ouverture plus rapide.',
        '', 'Le marquage est extrait des contours vectoriels du plan ; son relief de lecture n’est pas une gravure mesurée. Aucun moteur ni circuit interne de ventilateur n’est inventé.',
        '', '[Provenance](provenance.json), [contrôles FreeCAD](validation-freecad.json), [cotes](../cotes.md), [fiche composant](../README.md).','']
    (OUT/'README.md').write_text('\n'.join(lines),encoding='utf-8')
    canvas=Image.new('RGB',(2000,425),'white')
    for i,m in enumerate(results):
        im=Image.open(OUT/m['preview']['file']);im.thumbnail((495,420));canvas.paste(im,(i*500+(500-im.width)//2,0))
    canvas.save(OUT/'apercu-composants.png');print('DONE4STEP',[(m['file'],m['bytes'],m['validation']['solids']) for m in results],flush=True)
if __name__=='__main__':main()
