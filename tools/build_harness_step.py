"""Fourteen coloured STEP study models. No invented vendor measurements."""
from pathlib import Path
import sys,json,math,os
import cadquery as cq
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from PIL import Image,ImageDraw,ImageFont
from build_running_gear_step import box,cyl,ring,add,MODELS,export_model,sha,BLACK,BRIGHT,RED
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants';COMMON=BASE/'faisceau-puissance'
YELLOW=(.85,.59,.015);ADHESIVE=(.65,.39,.13);COPPER=(.60,.23,.075);NATURAL=(.86,.82,.68)

def optimal_bounds(self,tolerance=None):
    # OCC ordinary boxes overestimate trimmed spline lofts. Use the same precise
    # algorithm before/after STEP, also checked with FreeCAD optimalBoundingBox.
    bb=Bnd_Box();BRepBndLib.AddOptimal_s(self.wrapped,bb,False,False)
    return cq.BoundBox(bb)

def annulus_x(ro,ri,length,x=0,z=0):
    return cyl(ro,length,z,x,axis=(1,0,0)).cut(cyl(ri,length+.02,z,x-.01,axis=(1,0,0)))

def ancor_ring():
    f='cosses-puissance/ancor-312303'
    # Shape estimates only: no dimensional drawing was published for this SKU.
    palm=box(10,9.6,1.0,(5,0,0),1.4).cut(cyl(2.6,1.2,-.1,4.2))
    neck=(cq.Workplane(cq.Plane(origin=(9,0,.5),xDir=(0,1,0),normal=(1,0,0)))
        .rect(4.7,1).workplane(offset=3).center(0,1.85).circle(2.35).loft(combine=False).val())
    barrel=annulus_x(2.35,1.60,8.5,12,z=2.35)
    metal=palm.fuse(neck).fuse(barrel).clean()
    liner=annulus_x(2.53,2.35,12,12,z=2.35)
    sleeve=annulus_x(2.95,2.53,12,12,z=2.35)
    add(f,'cosse-ancor-312303-12awg-num10.step','Ancor 312303 | oeillet #10, 12-10 AWG',
        [('Cuivre_etame_forme_estimee',metal,BRIGHT),('Adhesif_geometrie_estimee',liner,ADHESIVE),('Gaine_jaune_estimee',sleeve,YELLOW)],
        ['12-10 AWG / 3-5 mm2; oeillet pour goujon #10; cuivre etame, joint brase, gaine adhesive'],
        ['Toutes cotes mecaniques estimees: encombrement24x9.6x5.9; trou5.2 et canon3.2 non publies',
         '4.8 mm catalogue = taille nominale de vis #10, pas un alesage mesure',
         'Etat non serti; epaisseurs, raccord de paume et couleur optique reconstruits'],
        params={'hole_assumed_mm':5.2,'terminal_stud_designation':'#10','wire_AWG':[12,10]},
        view=(.8,-1,1.6),probes=[dict(point=(4.2,0,.5),occupied=False)],source_pages=['Ancor catalogue2020 p.26 / catalogue2024 p.24'])

def klauke():
    for ref,c1,c2,l,hole in [('95r4',5,5.5,18,4.3),('95r5',6,6,19,5.3)]:
        # Family drawing: l starts at hole centre, not at front of palm.
        barrel_start=l-9;thick=2.0
        palm=box(c1+c2,9.5,thick,((c2-c1)/2,0,0),.55)
        wp=cq.Workplane(cq.Plane(origin=(c2,0,thick/2),xDir=(0,1,0),normal=(1,0,0))).rect(9.5,thick)
        transition=wp.workplane(offset=barrel_start-c2).center(0,3-thick/2).circle(3).loft(combine=False).val()
        s=palm.fuse(transition).fuse(cyl(3,9,3,barrel_start,axis=(1,0,0))).clean()
        s=s.cut(cyl(hole/2,thick+.2,-.1))
        # The inspection aperture is documented, its diameter/position are estimates.
        s=s.cut(cyl(2,l-barrel_start+1.31,3,barrel_start-1.3,axis=(1,0,0)))
        s=s.cut(cyl(.7,3,3,barrel_start-.3)).clean()
        params=dict(section_mm2=6,d1=4,a=9,b=9.5,d2=hole,d4=6,c1=c1,c2=c2,l=l,
                    reconstructed_overall_length_mm=l+c1,palm_thickness_assumed_mm=2,inspection_hole_assumed_mm=1.4,
                    l_datum='centre du trou -> extremite du canon, dessin famille archive')
        add('cosses-puissance/klauke-'+ref,'cosse-klauke-'+ref+'-6mm2.step',
            'Klauke '+ref.upper()+' | 6 mm2, trou '+str(hole)+' mm',[('Cosse_Cu_etame_non_sertie',s,BRIGHT)],
            [f'd1=4; a=9; b=9.5; d2={hole}; d4=6; c1={c1}; c2={c2}; l={l} mm',
             'Dessin famille archive: l est depuis centre trou; l+c1 donne23/25 mm dans reconstruction'],
            ['Epaisseur de paume2mm, rayons, loft et trou inspection reconstruits; chanfrein interne non cote omis',
             'Pas de marque gravee ni deformation de sertissage inventee; mesurer le lot avant usinage',
             'Vis SSR #8-32 ou ecrous #10-32 conserves; trou M4/M5 ne change pas le filetage'],params=params,
            view=(.8,-1,1.1),probes=[dict(point=(0,0,1),occupied=False),dict(point=(l-.5,0,3),occupied=False)],
            source_pages=['Klauke catalogue archive via PowerCables, PDF p.14 / imprimee12','Klauke tableau actuel 95R4/95R5'])
        if ref=='95r4':
            cut=s.cut(box(40,10,10,(5,5,0)))
            add('cosses-puissance/klauke-'+ref,'cosse-klauke-'+ref+'-coupe-etude.step','Klauke 95R4 | coupe technique',
                [('Demi_cossee_coupe_volontaire',cut,BRIGHT)],['Meme cotes nominales que variante entiere'],
                ['Coupe volontaire y>=0, pour lecture du canon et du trou inspection; piece non utilisable'],params=params,view=(.7,1,1))

def butt():
    f='raccords-12awg';metal=annulus_x(2.4,1.65,15,0)
    # Physical stop is an estimated internal ring, not a solid wall cutting the current path.
    stop=annulus_x(1.65,1.2,.6,7.2);metal=metal.fuse(stop).clean()
    liner=annulus_x(2.58,2.4,30,-7.5);sleeve=annulus_x(3.05,2.58,30,-7.5)
    params={'metal_length_assumed_mm':15,'total_length_assumed_mm':30,'outer_diameter_assumed_mm':6.1,'wire_AWG':[12,10]}
    for cut in (False,True):
        parts=[('Canon_Cu_etame',metal,BRIGHT),('Adhesif_interieur_estime',liner,ADHESIVE),('Gaine_jaune_estimee',sleeve,YELLOW)]
        if cut:parts=[(n,s.cut(box(40,10,10,(7.5,5,-5))),c) for n,s,c in parts]
        add(f,'raccord-ancor-309203'+('-coupe' if cut else '')+'.step','Ancor 309203 | '+('coupe technique' if cut else 'raccord 12-10 AWG'),parts,
            ['12-10 AWG / 3-5 mm2; cuivre etame, joint brase, gaine adhesive, lot3'],
            ['Toutes longueurs, diametres, epaisseurs et butee interne estimes',
             'Etat non serti; pas de qualification du cuivre silicone tres fin BNTECHGO',
             'Coupe y>=0 volontaire' if cut else 'Aucun fil represente: canon libre'],params=params,
            view=(.7,1,1.2) if cut else (.7,-1,1.1),source_pages=['Ancor2020 p.27 /2024 p.25'])

def shrink():
    f='gaine-thermoretractable'
    # Published dimensions apply after free recovery, not to a sleeve on a wire.
    states=[('expansee',4,4.17,4.35,40),('retreinte-libre',1,1.5,2,36),('retreinte-libre-coupe',1,1.5,2,36)]
    for state,ri,mid,ro,length in states:
        parts=[('Adhesif_ambre_estime_optique',annulus_x(mid,ri,length),ADHESIVE),('Polyolefine_noire',annulus_x(ro,mid,length),BLACK)]
        if state.endswith('coupe'):parts=[(n,s.cut(box(length+2,10,10,(length/2,5,-5))),c) for n,s,c in parts]
        add(f,'gaine-te-atum-8-2-'+state+'.step','TE ATUM 8/2 | '+state,parts,
            ['Diametre fourni min8; libre retreint max2; paroi libre totale1.0+/-0.3, adhesif0.5nom mm',
             'Retrait longitudinal0 a -15%: plan TE A2, 2023; couleur noire'],
            ['Longueurs40/36mm exemples de coupe, pas une longueur livree; 1.2m STK',
             'Etat expanse: OD8.7 et partage0.17/0.18mm estimes; paroi fournie non publiee',
             'Adhesif ambre est une couleur de lecture, teinte reelle non documentee',
             'Retreinte libre n est pas la geometrie installee sur fil4.7 ou canon6mm',
             'Demi-coupe volontaire' if state.endswith('coupe') else 'Modele d etude sans marquages inventes'],
            params=dict(state=state,inside_mm=2*ri,outside_mm=2*ro,length_example_mm=length,
                free_recovered_wall_mm=1,free_recovered_adhesive_mm=.5),
            view=(.5,1 if state.endswith('coupe') else -1,1.2),
            source_pages=['TE drawing ATUM_4_to_RATIO_STANDARD_SIZES revA2','TE datasheet ATUM05/24','Raytronics fiche secondaire archivee'])

def tie_mount():
    f='maintien-faisceau/colliers'
    head=box(4.8,4.45,3.7,(2.4,0,0),.22)
    head=head.cut(box(5.1,2.75,1.55,(2.4,0,1.15)))
    strap=box(87.2,2.5,1,(48.4,0,0))
    tip=cq.Workplane('XY').polyline([(92,-1.25),(100,-.45),(100,.45),(92,1.25)]).close().extrude(1).val()
    s=head.fuse(strap).fuse(tip)
    # Teeth are cut into the inside face: preserve nominal strap thickness1mm.
    for x in [8+i*.65 for i in range(122)]:s=s.cut(box(.24,2.1,.23,(x,0,-.01)))
    # Reconstructed pawl joined to head roof, estimated mechanical mechanism.
    pawl=box(.6,2.4,.85,(3.3,0,1.95));s=s.fuse(pawl).clean()
    add(f,'collier-ht-t18r-11101919.step','HellermannTyton T18R | 100 x 2.5, naturel',[('PA66_naturel_serrure_denture',s,NATURAL)],
        ['TDS actuelle: L100 W2.5 T1 H3.7mm; tete4.8x4.45 annoncee page; couleur naturelle',
         'Plan famille2025 different: T1.1+/-0.2; tete4.8 et H3.5+/-0.2'],
        ['Pas/dentures, forme pointe, logement et cliquet estimes; pose droite, pas pre-serree',
         '80N est une resistance minimale de boucle, jamais une consigne de serrage',
         'Les variantes noire et UV ne sont pas la reference111-01919'],
        params=dict(length=100,width=2.5,thickness=1,head_height=3.7,head_width=4.45,head_length=4.8,teeth_pitch_assumed=.65),view=(.7,-1,1.9),
        source_pages=['HT TDS111-01919,9Oct2026','Plan famille10-0585-001-CSC rev10.1,5Dec2025'])
    f='maintien-faisceau/embases'
    # Historic maker plan141622: one round-end tongue + tie crossbar, not square adhesive mount.
    tongue=box(12.5,6.75,3.3,(6.25,10.875,0))
    tongue=tongue.fuse(cyl(6.25,3.3,0,6.25,14.25)).clean()
    # Trim length to20.5 and flat transverse ends; rounded top reaches20.5.
    cross=box(12.5,2.5,3.3,(6.25,1.25,0))
    neck=box(10,5,1.7,(6.25,5,0))
    mount=tongue.fuse(neck).fuse(cross).cut(cyl(2.5,3.5,-.1,6.25,14.25)).clean()
    add(f,'embase-ht-mb2-15128210.step','HellermannTyton MB2 | 20.5 x 12.5 x 3.3',[('PA66_noir_embase_vis',mount,BLACK)],
        ['Plan141622: A12.5+/-0.5 B20.5+/-0.5 C3.3+/-0.2 D2.5+/-0.2 E5+/-0.2 F5+/-0.2 G10+/-0.2 H1.7+/-0.2',
         'TDS actuelle: passage collier max5mm, visM4, trou5mm, noir PA66'],
        ['Position du trou et longueur de languette extrapolees du dessin non cotees',
         'Rayons de moulage, faible depouille et details de surface non mesures',
         'Vis, rondelle, ecrou et chassis absents; longueur vis a determiner'],
        params=dict(length=20.5,width=12.5,height=3.3,hole=5,tie_passage_length=5,bridge_width=10,bridge_height=1.7),
        view=(.8,-1,1.3),probes=[dict(point=(6.25,14.25,1),occupied=False)],source_pages=['HT plan141622,15Oct2002','HT MB2 page actuelle151-28210'])

def mainwire():
    f='cable-principal-6mm2';ri=math.sqrt(6/math.pi)
    for color,name in [(RED,'rouge'),(BLACK,'noir')]:
        core=cyl(ri,100,0,axis=(1,0,0));sheath=annulus_x(2.35,ri,80,10)
        add(f,'cable-auprotec-flryb-6mm2-'+name+'-100mm.step','AUPROTEC FLRY-B 6 mm2 | '+name+' 100 mm',
            [('Cuivre_cylindre_equivalent_section_6mm2',core,COPPER),('PVC_'+name,sheath,color)],
            ['Section6mm2, cuivre nu recuitECu; gainePVC; ODenv4.7mm; filamentsmax0.300mm'],
            ['Ame pleine equivalente aire6mm2: pas le diametre du faisceau ni une reconstruction des brins',
             'Nombre, toronnage et OD reel du cuivre non publies; couleurs reconstituees',
             'Longueur100 et denudage10par bout illustratifs, pas liste de coupe'],
            params=dict(section_mm2=6,outside_diameter_nominal_approx_mm=4.7,equivalent_core_diameter=2*ri,length_example=100,strip_example=10,
                        actual_strand_count=None,actual_strand_lay_known=False),view=(.7,-1,.8),source_pages=['AUPROTEC page FLRYB6 rouge6m044906'])
    core=cyl(ri,40,0,axis=(1,0,0));sheath=annulus_x(2.35,ri,40).cut(box(42,10,10,(20,5,-5)))
    add(f,'cable-auprotec-flryb-6mm2-coupe-equivalente.step','FLRY-B 6 mm2 | coupe de lecture',
        [('Cuivre_equivalent6mm2_sans_brins_inventes',core,COPPER),('Demi_gaine_PVC_coupe_volontaire',sheath,RED)],
        ['Section6mm2, ODenv4.7mm'],['Coupe gaine volontaire; ame equivalente pleine; aucun nombre de brins deduit'],
        params=dict(section_mm2=6,length_example=40,actual_strand_count=None),view=(.7,1,1))

def main():
    sys.stdout.reconfigure(encoding='utf-8');cq.Shape.BoundingBox=optimal_bounds;MODELS.clear()
    for f in [ancor_ring,klauke,butt,shrink,tie_mount,mainwire]:f()
    assert len(MODELS)==14,len(MODELS);out=COMMON/'3D';out.mkdir(parents=True,exist_ok=True);results=[];groups={}
    for item in MODELS:
        m=export_model(item);m.update(generated_on='2026-10-14',generator='tools/build_harness_step.py',generator_sha256=sha(Path(__file__)),
            coordinate_system='Cosses/cables/gaines: axe X, holecentreX0 Klauke; MB2 baseZ0; collier droitX0..100. Voir parametres.')
        target=BASE/item['folder']/'3D'/Path(m['file']).with_suffix('.json');target.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        m=dict(folder=item['folder'],**m);results.append(m);groups.setdefault(item['folder'],[]).append(m)
    for folder,models in groups.items():
        loc=BASE/folder/'3D';lines=['# Modèles STEP - '+folder,'','Solides nommés, couleurs et unités mm. Reconstructions d’étude ; aucun matériel mesuré.','',
            '| Modèle | STEP | Aperçu |','| --- | --- | --- |']
        for m in models:lines.append(f'| {m["title"]} | [STEP]({m["file"]}) | [PNG]({m["preview"]["file"]}) |')
        rel=Path(os.path.relpath(out/'validation-freecad.json',loc)).as_posix()
        lines+=['','Chaque JSON voisin distingue cotes publiées, estimations et contrôles. Les coupes techniques sont volontaires. Les fils sont des exemples de pose et ne prescrivent pas une longueur de coupe.',
            '',f'[Contrôle FreeCAD]({rel}), [fiche composant](../README.md), [provenance](provenance.json).','']
        (loc/'README.md').write_text('\n'.join(lines),encoding='utf-8')
        (loc/'provenance.json').write_text(json.dumps(dict(generator='tools/build_harness_step.py',generator_sha256=sha(Path(__file__)),models=models),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (out/'catalogue.json').write_text(json.dumps(dict(model_count=len(results),folder_count=len(groups),models=results),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Modèles du faisceau de puissance','',f'**{len(results)} STEP colorés dans {len(groups)} dossiers.** Les variantes en coupe sont faites pour lire la construction.','',
        '| Composant | Modèles | Dossier |','| --- | --- | --- |']
    for folder,models in groups.items():
        rel=Path(os.path.relpath(BASE/folder/'3D/README.md',out)).as_posix();lines.append(f'| {folder} | {len(models)} | [STEP et aperçus]({rel}) |')
    lines+=['','[Vue d’ensemble](apercu-composants.png), [catalogue](catalogue.json), [contrôles FreeCAD](validation-freecad.json), [documentation](../README.md).',
        '', 'Les enveloppes Ancor sont estimées ; aucun plan coté exact trouvé. Sur le dessin Klauke, l est mesuré depuis le centre du trou : ne pas le confondre avec la longueur totale. La gaine rétreinte libre n’est pas une gaine installée. Le cuivre du câble 6 mm² est représenté par un cylindre de section équivalente, sans brins inventés.','']
    (out/'README.md').write_text('\n'.join(lines),encoding='utf-8')
    tw,th,cols=470,395,4;canvas=Image.new('RGB',(cols*tw,math.ceil(len(results)/cols)*th+50),'white');d=ImageDraw.Draw(canvas)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18);d.text((18,12),'Drone V3 | Faisceau de puissance - 14 modèles, échelles indépendantes',font=font,fill='#24313e')
    for i,m in enumerate(results):
        im=Image.open(BASE/m['folder']/'3D'/m['preview']['file']);im.thumbnail((tw-8,th-25));x=i%cols*tw;y=i//cols*th+50
        canvas.paste(im,(x+(tw-im.width)//2,y));d.text((x+8,y+th-24),Path(m['file']).stem[:44],font=font,fill='#24313e')
    canvas.save(out/'apercu-composants.png');print('DONE',len(results),'STEP models',flush=True)
if __name__=='__main__':main()
