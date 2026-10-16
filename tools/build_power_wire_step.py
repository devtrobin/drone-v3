"""Light installation STEP and short 680-strand, coloured wire reconstructions."""
from pathlib import Path
import math,json,sys,hashlib
import cadquery as cq
from build_running_gear_step import box,cyl,export_model
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/cable-puissance-12awg'
RED=(.64,.014,.009);BLACK=(.015,.020,.026);TIN=(.51,.54,.58)
MAKER='https://bntechgo.com/bntechgo-12-gauge-silicone-wire-kit-ultra-flexible-20-ft-black-and-red-each-color-10-ft-high-temp-200-c-600v-12-awg-silicone-wire-680-strands-of-tinned-copper-wire-stranded-wire-stranded-wire-for-model-battery/'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def lattice():
    pitch=.082;pts=[]
    for i in range(-22,23):
        for j in range(-22,23):
            x=(i+j*.5)*pitch;y=j*math.sqrt(3)*pitch/2
            pts.append((x*x+y*y,x,y))
    pts=sorted(pts)[:680];xy=[(x,y) for r,x,y in pts]
    edge=max(math.hypot(x,y)+.04 for x,y in xy)
    assert edge<1.205 and len(xy)==680
    minimum=min(math.hypot(x-xx,y-yy) for i,(x,y) in enumerate(xy) for xx,yy in xy[i+1:])
    assert minimum>.08
    return xy,dict(strands=680,diameter_mm=.08,area_sum_mm2=680*math.pi*.04**2,
        lattice_pitch_estimated_mm=pitch,bundle_envelope_estimated_mm=2*edge,minimum_surface_gap_mm=minimum-.08,
        actual_lay_measured=False,representation='straight strands, ideal packing; plating colour only')
def straight(color,length=100):
    sheath=cyl(2.25,length-10,5).cut(cyl(1.205,length-9.8,4.9))
    core=cyl(1.205,length)
    return [('Gaine_silicone',sheath,color),('Enveloppe_des_brins_simplifiee',core,TIN)]
def detailed(color,xy,cutaway=False):
    sheath=cyl(2.25,15,5).cut(cyl(1.205,15.2,4.9))
    if cutaway:sheath=sheath.cut(box(5,5,15.2,(2.5,0,4.9)))
    return [('Gaine_silicone_fenetre' if cutaway else 'Gaine_silicone',sheath,color)]+[
        (f'Brin_cuivre_etame_{i+1:03d}',cyl(.04,25,0,x,y),TIN) for i,(x,y) in enumerate(xy)]
def curved(x,color):
    curve=cq.Edge.makeBezier([cq.Vector(*p) for p in [(x,0,20),(x,0,50),(x+30,0,50),(x+30,0,80)]])
    def make(outer,start,inner=None):
        wire=cq.Wire.assembleEdges([cq.Edge.makeLine(cq.Vector(x,0,start),cq.Vector(x,0,20)),curve,
            cq.Edge.makeLine(cq.Vector(x+30,0,80),cq.Vector(x+30,0,100))])
        profile=cq.Workplane(cq.Plane(origin=(x,0,start),normal=(0,0,1))).circle(outer)
        if inner:profile=profile.circle(inner)
        s=profile.sweep(cq.Workplane('XY').newObject([wire]),isFrenet=False).val()
        if inner:s=s.cut(box(100,100,6,(20,0,95)))
        assert s.isValid() and len(s.Solids())==1
        checks=0
        for u in [0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1]:
            p=curve.positionAt(u);t=curve.tangentAt(u).normalized();a=t.cross(cq.Vector(0,1,0)).normalized();b=t.cross(a).normalized()
            radius=1.75 if inner else .8
            for i in range(12):
                angle=i*math.pi/6;q=p+a.multiply(radius*math.cos(angle))+b.multiply(radius*math.sin(angle))
                assert s.isInside(q,1e-6),'curve material discontinuity';checks+=1
        return s,checks
    core,n=make(1.205,0);sheath,m=make(2.25,5,1.205)
    return [('Gaine_silicone',sheath,color),('Enveloppe_brins_simplifiee',core,TIN)],dict(core_solids=1,sheath_solids=1,material_samples=n+m,strip_each_end_mm=5,shape_is_installation_example=True)
def main():
    sys.stdout.reconfigure(encoding='utf-8');out=BASE/'3D';out.mkdir(parents=True,exist_ok=True)
    xy,packing=lattice();checks=[];pair=[]
    for i,(x,c) in enumerate([(-4.5,RED),(4.5,BLACK)]):
        p,v=curved(x,c);pair += [(('Rouge_' if i==0 else 'Noir_')+n,s,c) for n,s,c in p];checks.append(v)
    defs=[('bntechgo-12awg-rouge-100mm-implantation.step','12 AWG rouge | exemple droit 100 mm',straight(RED)),
        ('bntechgo-12awg-noir-100mm-implantation.step','12 AWG noir | exemple droit 100 mm',straight(BLACK)),
        ('bntechgo-12awg-paire-courbee-implantation.step','12 AWG rouge et noir | chemin illustratif',pair),
        ('bntechgo-12awg-rouge-680brins-detaille.step','12 AWG rouge | 680 brins visibles, 25 mm',detailed(RED,xy)),
        ('bntechgo-12awg-noir-680brins-detaille.step','12 AWG noir | 680 brins visibles, 25 mm',detailed(BLACK,xy)),
        ('bntechgo-12awg-coupe-680brins-detaillee.step','12 AWG | coupe de gaine et 680 brins, 25 mm',detailed(RED,xy,True))]
    results=[]
    for filename,title,parts in defs:
        detail='680brins' in filename
        item=dict(folder='cable-puissance-12awg',filename=filename,title=title,parts=parts,
            published=['BNTECHGO 680 brins de0.08, conducteur2.41, gaine4.5mm, epaisseur1.05 nominale',
                '680 et0.08, gaine4.5+/-0.1 : offre exacteB01ABOPMEI ; pas de cote mesuree'],
            estimated=['Reconstruction, pas CAO fabricant ; aucune piece mesuree',
                'Longueurs100/25mm, denudages5mm, trace courbe et fenetre de coupe : illustration',
                '680 brins droits en reseau ideal, torsade et pas reels non publies ; etamage couleur sans epaisseur inventee',
                'Versions implantation : enveloppe de brins pleineØ2.41 pour implantation ; ne pas en deduire masse/section conductrice',
                'Les longueurs de modele ne sont pas des longueurs livrees ni une liste de coupe'],
            params=dict(outer_diameter_mm=4.5,conductor_bundle_diameter_mm=2.41,strands=680 if detail else 'bulk envelope',strand_diameter_mm=.08,
                strip_length_each_end_mm=5,wire_length_straight_mm=25 if detail else 100),
            view=(1,-1,.65) if detail else (1,-1,.3),design=False,probes=[],source_pages=[MAKER,'https://www.amazon.com/dp/B01ABOPMEI'])
        m=export_model(item);m.update(generated_on='2026-10-14',generator='tools/build_power_wire_step.py',generator_sha256=sha(Path(__file__)),
            coordinate_system='Axe Z du fil droit ; face initiale z0 ; fils courbes dans plan XZ ; dimensions en mm',
            strand_packing=packing if detail else None,curve_continuity_checks=checks if 'courbee' in filename else [],
            is_installation_length_illustration=True)
        (out/Path(filename).with_suffix('.json')).write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');results.append(m)
    (out/'catalogue.json').write_text(json.dumps(dict(generated_on='2026-10-14',model_count=len(results),models=results),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    rows=['# STEP - câble BNTECHGO 12 AWG','',
        'Six modèles colorés : trois vues d’implantation à enveloppe simplifiée et trois coupes courtes détaillant chacune **680 brins individuels**. Le noir et le rouge sont deux fils séparés ; la paire courbée ne représente pas un câble collé à deux conducteurs.','',
        '| Modèle | Solides | STEP | Aperçu | Provenance |','| --- | ---: | --- | --- | --- |']
    for m in results:rows.append(f"| {m['title']} | {m['validation']['solids']} | [STEP]({m['file']}) | [PNG]({m['preview']['file']}) | [JSON]({Path(m['file']).with_suffix('.json')}) |")
    rows += ['','**Ouvrir une version implantation pour l’assemblage général.** Les versions détaillées contiennent 681 solides et servent à observer les brins/coupes. Longueurs25/100mm et dénudages5mm illustratifs, pas une commande de coupe.', '',
        'Ø4,5 ±0,1 mm extérieur et Ø2,41 mm de faisceau annoncés. Disposition idéale et rectiligne des brins, pas de torsade inventée ; chaque brin Ø0,08 est un solide continu. Couleur argentée de l’étamage, sans épaisseur de placage supposée. Gaine coupée volontairement dans la vue de coupe ; extrémités dénudées volontaires.', '',
        'Les versions légères remplissent l’enveloppe du faisceau : elles ne servent pas au calcul de masse ou de section de cuivre. Les modèles courts conservent le nombre annoncé, pas un nombre de brins mesuré. Aucun modèle CAD natif exact trouvé.', '',
        '[Imports FreeCAD](validation-freecad.json), [catalogue](catalogue.json), [cotes](../cotes.md), [notice et achat](../README.md).','']
    (out/'README.md').write_text('\n'.join(rows),encoding='utf-8');print('DONE',len(results),'models',flush=True)
if __name__=='__main__':main()
