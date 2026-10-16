"""Coloured V3 assembly from existing components; preserve uncertain reservations.

No regeneration of component details and no rewriting of chassis fabrication data.
"""
from pathlib import Path
import hashlib,json,sys,time
import cadquery as cq

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'Assemblage';OUT.mkdir(exist_ok=True)
CACHE={};ROWS=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def T(v):return cq.Location(cq.Vector(*v))
def R(axis,angle):return cq.Location(cq.Vector(),cq.Vector(*axis),angle)
def load(rel):
    if rel not in CACHE:
        print('LOAD',rel,flush=True)
        try:CACHE[rel]=cq.Assembly.load(str(ROOT/rel))
        except ValueError as e:
            if 'does not contain an assembly' not in str(e):raise
            CACHE[rel]=cq.Assembly(cq.importers.importStep(str(ROOT/rel)).val(),name=Path(rel).stem,color=cq.Color(.035,.19,.065))
    return CACHE[rel]
groups={k:cq.Assembly(name=k) for k in ['structure','roulage','electronique','puissance']}
def add(group,name,rel,loc):
    source=load(rel);groups[group].add(source,name=name,loc=loc)
    ROWS.append(dict(name=name,group=group,source=rel,source_sha256=sha(ROOT/rel),location=loc.toTuple(),status='Modèle existant placé ; pose des câbles et interfaces non qualifiées'))
def centered(group,name,rel,x,y,z):
    a=load(rel);b=a.toCompound().BoundingBox()
    add(group,name,rel,T((x-(b.xmin+b.xmax)/2,y-(b.ymin+b.ymax)/2,z-b.zmin)))

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    base=load('Composants/chassis/3D/chassis-a2-r1-implante.step')
    remove=('Pneu','Jante','Pi5_','Pi_ports','Pi_GPIO','Pi_ActiveCooler','Pi_ventilateur','M1P_porteuse','HS251_','D1D100_',
        'D_plus_','D_moins_','ESC_','FT90M_','Servo_palonnier','Moteur2435_','Moteur_','Engrenage_','UD80A_',
        'D42V55F5_','Pololu2813_','WAGO413_','WAGO415_','A7_','Camera_CAM_','ED80_')
    reserves=[]
    for child in base.children:
        if child.name.startswith(remove):continue
        groups['structure'].add(child,name=child.name)
        if 'reserve' in child.name.lower() or child.name.startswith(('B01_','Pololu2831','AC03_','IC5_','Arbre_sortie','Direction_')):reserves.append(child.name)
    # Rigid component placement using documented body datums, not cable bounds.
    for sign,suffix in [(-1,'G'),(1,'D')]:
        normal=R((0,1,0),90*sign)
        for y,axle in [(55,'AV'),(445,'AR')]:
            add('roulage','Roue_'+axle+'_'+suffix,'Composants/roues/3D/roue-hobbypark-63x26-detaillee.step',T((sign*200,y,31.5))*normal)
        add('roulage','Moteur_'+suffix,'Composants/moteur/3D/moteur-quicrun-2435-g3-4500kv-detaille.step',T((sign*140,408,31.5))*normal)
        add('roulage','Pignon16_'+suffix,'Composants/transmission-arriere/pignon-moteur/3D/pignon-losi-los212054-16t.step',T((sign*128,408,31.5))*normal)
        add('roulage','Couronne54_etage1_'+suffix,'Composants/transmission-arriere/engrenages-54dents/3D/couronne-khk-ss0-5-54a.step',T((sign*128,425.5,31.5))*normal)
        # Flip the long24B hub towards the inside, clear of the other gear.
        add('roulage','Pignon24_'+suffix,'Composants/transmission-arriere/pignon-intermediaire/3D/pignon-khk-ss0-5-24b.step',T((sign*122,425.5,31.5))*R((0,1,0),-90*sign))
        add('roulage','Couronne54_etage2_'+suffix,'Composants/transmission-arriere/engrenages-54dents/3D/couronne-khk-ss0-5-54a.step',T((sign*117,445,31.5))*normal)
        for x,y in [(101,425.5),(145,425.5),(113.5,445),(171.5,445)]:
            add('roulage','MR115_'+suffix+'_'+str(x),'Composants/roulements/3D/roulement-mr115zz-5x11x4.step',T((sign*(x-2),y,31.5))*normal)
        # Fourche already retained; A7 is a study reconstruction, no guessed
        #final kingpin or shaft length is presented as manufactured hardware.
        add('roulage','Fusee_A7_'+suffix,'Composants/fusees-avant/3D/fusee-a7-'+('gauche' if sign<0 else 'droite')+'-tamiya-51002.step',T((sign*170,55,31.5)))
        add('electronique','ESC_'+suffix,'Composants/moteur/3D/variateur-quicrun-wp16bl30-g2-detaille.step',T((sign*47-16.7,376-13.4,17)))
    add('roulage','Servo_FT90M','Composants/servo-direction/3D/servo-feetech-ft90m-detaille.step',T((0,80,14.2)))
    add('roulage','Palonnier','Composants/servo-direction/3D/palonnier-double-ft90m.step',T((-5.7,80,38)))
    add('electronique','Pi5_4Go_detail','Composants/raspberry-pi-5/3D/raspberry-pi-5-4go-ultra-detaille.step',T((-35,350,98)))
    add('electronique','ActiveCooler','Composants/refroidissement-raspberry-pi-5/3D/raspberry-pi-active-cooler-sc1148-detaille.step',T((-34.25,356.75,102)))
    add('electronique','Camera_U20CAM4M','Composants/camera/3D/camera-u20cam-4m-detaillee.step',T((0,482,231))*R((1,0,0),20)*T((-16,0,-16))*R((1,0,0),90))
    add('electronique','Surveillance_M1P','Composants/carte-surveillance-electrique/3D/porteuse-surveillance-2s-m1-detaillee.step',T((-70,270,98)))
    centered('electronique','D42V55F5','Composants/regulateur-alimentation/d42v55f5/3D/pololu-d42v55fx-officiel.step',-57.5,388,96)
    centered('electronique','Pololu2813','Composants/protection-batterie/interrupteur-pi/3D/pololu-2813-officiel.step',30,190,83)
    for x,y,name,kind in [(-60,325,'INplus','413'),(-35,325,'INmoins','413'),(-30,420,'5V','413'),(-24,388,'GND','415')]:
        centered('electronique','WAGO_'+name,f'Composants/liaisons-alimentation-surveillance/wago-221-{kind}/3D/wago-221-{kind}-detaille.step',x,y,83)
    for y,name in [(285,'D_plus'),(320,'D_moins')]:add('puissance',name,'Composants/distribution-alimentation/bornier-2315/3D/bluesea-2315-complet-detaille.step',T((-87,y,17)))
    add('puissance','HS251_D1D100','Composants/dissipateur-relais/3D/assemblage-d1d100-hs251-hsp1-etude.step',T((-112,227,17))*R((0,0,1),90))
    add('puissance','UD80','Composants/repartition-moteurs/3D/eriflex-ud80a-implantation-v3.step',T((108,368,19)))
    # Original ED80 datum is underneath the panel. Move its two supplied heads
    #above the3mm panel, retaining each original body and colour.
    rel='Composants/coupure-manuelle/albright-ed80/3D/albright-ed80-ferme-detaille.step'
    ed=cq.Assembly(name='ED80_monte_sur_panneau3')
    for child in load(rel).children:
        if 'tete_M5' in child.name:ed.add(child,name=child.name,loc=T((0,0,3)))
        else:ed.add(child,name=child.name)
    groups['puissance'].add(ed,name='ED80',loc=T((-95,140,70)))
    ROWS.append(dict(name='ED80',group='puissance',source=rel,source_sha256=sha(ROOT/rel),location=T((-95,140,70)).toTuple(),status='Têtes M5 relevées3mm au-dessus du panneau ; corps inchangés'))
    complete=cq.Assembly(name='DroneV3_assemblage_detaille_A2R1')
    for name,a in groups.items():complete.add(a,name=name)
    results=[]
    # A full file for the requested assembly, plus manageable independent zones.
    for name,a in [*groups.items(),('complet-detaille',complete)]:
        path=OUT/('drone-v3-'+name+'.step');print('EXPORT',path.name,flush=True)
        a.export(str(path),exportType='STEP',unit='MM',outputUnit='MM')
        results.append(dict(file=path.name,bytes=path.stat().st_size,sha256=sha(path)))
    manifest=dict(revision='A2-R1 assemblage détaillé',models=results,instances=ROWS,reservations_retained=reserves,
        native_sources_unchanged=True,physical_fit_validated=False,complete_harness_routed=False,
        explicit_missing=['BatterieG1 IC5 : pas de STEP exact, ne pas réutiliser Zeee',
            'LFT classeT et4 supportsKLKD : volumes réservés conservés',
            'EVM TI et Pololu2831 : gabarits conservés',
            'Arbres définitifs, paliers adaptés, carters et visserie finale non libérés',
            'Câbles détaillés des composants gardent leur pose de référence, pas des liaisons électriques achevées'],
        generator_sha256=sha(Path(__file__)))
    (OUT/'provenance.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'README.md').write_text('''# Drone V3 - assemblage détaillé A2-R1

[Modèle complet](drone-v3-complet-detaille.step) : structure et modèles détaillés déjà disponibles, avec noms et couleurs STEP. Le fichier peut être lourd. Pour une ouverture rapide, garder le [modèle léger](../Composants/chassis/3D/chassis-a2-r1-implante.step).

Sous-ensembles dans le même repère global, superposables sans déplacement : [structure et réservations](drone-v3-structure.step), [roulage](drone-v3-roulage.step), [électronique](drone-v3-electronique.step), [puissance](drone-v3-puissance.step). Ne pas importer les sous-ensembles en plus du complet dans le même document : cela doublerait les pièces.

Les sources détaillées sont réutilisées sans modification. Quatre roues, deux moteurs/ESC, Pi5, refroidisseur, caméra, porteuse, rails et organes disponibles sont remplacés par leurs STEP existants. Le moyeu long du24B est tourné vers l'intérieur pour éviter la superposition avec la couronne du premier étage.

Ce fichier est une étude d'assemblage, pas une qualification mécanique. La batterieG1, les supports de fusibles révisés et les EVM sans modèle exact gardent leurs réservations identifiées. Les anciens modèlesZeee/MIDI/ATO ne sont pas remis dans le véhicule. Les arbres50mm historiques ne remplacent pas les axes définitifs ; paliers adaptés, retenues, carters, cinématique et visserie restent à finaliser. Les câbles propres aux STEP conservent une pose illustrative et ne sont pas un faisceau entièrement raccordé.

Les broches et couleurs détaillées ne prouvent pas le raccordement électrique. Les collisions de l'ensemble détaillé, la phase des dentures, le déport réel des roues et le refroidisseur restent à contrôler ; l'import de STEP valide ne suffit pas. Les plans de découpe A2-R1 ne sont pas réécrits par cette génération. [Sources, poses, limites et empreintes](provenance.json).
''',encoding='utf-8')
    print('DONE',len(ROWS),'detailed component instances;',len(results),'STEP files',flush=True)

if __name__=='__main__':main()
