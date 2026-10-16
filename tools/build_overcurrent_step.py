"""Detailed exterior reconstructions from Littelfuse plans; no hidden fuse element."""
from pathlib import Path
import json,sys,hashlib,math
import cadquery as cq
from build_running_gear_step import box,cyl,ring,hexagon,thread,tube,export_model as shared_export
from OCP.BRepTools import BRepTools
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/protection-surintensite'
BLACK=(.015,.017,.020);DARK=(.026,.029,.032);METAL=(.57,.59,.60);YELLOW=(.65,.55,.035);HARDWARE=(.53,.39,.13)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def export_model(m):
    # Shared pieces have already been meshed by a previous preview. Remove that
    # cache so both source and STEP bounds use the same exact surface method.
    for n,s,c in m['parts']:BRepTools.Clean_s(s.wrapped)
    return shared_export(m)
def text_shape(txt,size,pos,parts,name,color,rotation=0):
    s=cq.Workplane('XY').text(txt,size,.015,font='Arial',halign='center',valign='center',combine=False).val()
    s=s.rotate((0,0,0),(0,0,1),rotation).translate(pos)
    parts.append((name,s,color));return s
def fuse():
    parts=[]
    profile=[(-8,2.0),(-8,6),(-6.4,6),(-4.7,8),(4.7,8),(6.4,6),(8,6),(8,2),(6.4,2),(4.7,0),(-4.7,0),(-6.4,2)]
    body=cq.Workplane('XZ').polyline(profile).close().extrude(12).val().translate((0,6,0))
    # A shallow exterior mould seam; this is not the fuse's internal geometry.
    outer=box(16.1,12.1,.08,(0,0,1.94));inner=box(15.5,11.5,.12,(0,0,1.92))
    body=body.cut(outer.cut(inner))
    for x in (-6.6,6.6):
        for y in (-3.7,3.7):body=body.cut(cyl(.54,.1,5.94,x,y))
    mark=[]
    yellow=text_shape('60',3.7,(0,0,7.982),mark,'Marquage_60_jaune_approche',YELLOW,90)
    # Open the pocket through the outer surface: a black skin above the ink
    # would otherwise hide the calibre in the STEP preview.
    body=body.cut(yellow).cut(yellow.translate((0,0,.01)))
    for sign in (-1,1):
        # Tin plated terminal: rounded corners, two M5 clearance holes.
        terminal=box(13.0,10,.41,(sign*14.0,0,3.795),.7)
        terminal=terminal.cut(cyl(2.75,.7,3.65,sign*15,0))
        parts.append((f'Patte_cuivre_etame_{sign}',terminal,METAL))
        body=body.cut(terminal)
    parts.append(('Boitier_noir_PA66_GF25_exterieur',body,BLACK));parts+=mark
    return parts
def cover():
    outer=cq.Workplane('XY').workplane(offset=8).rect(51.4,25.7).workplane(offset=16.9).rect(48.2,23.5).loft().val()
    inside=cq.Workplane('XY').workplane(offset=7.9).rect(48.6,22.9).workplane(offset=15.5).rect(45.6,20.9).loft().val()
    shell=outer.cut(inside)
    for x in (-25,25):shell=shell.cut(box(5,9,9,(x,0,7.9)))
    for sign in (-1,1):
        for x in (-6.5,6.5):
            # Long shallow finger ribs on the sloping cover.
            rib=box(.85,.6,8,(x,sign*12.18,12))
            shell=shell.fuse(rib)
    # Recessed top graphic, rather than a false raised label exceeding the envelope.
    graphic=cq.Workplane('XY').text('Littelfuse',3.1,.06,font='Arial',halign='center',valign='center',combine=False).val().translate((0,0,24.85))
    shell=shell.cut(graphic)
    lines=box(21.6,.2,.15,(0,-3.6,24.78)).fuse(box(21.6,.2,.15,(0,3.6,24.78)))
    shell=shell.cut(lines)
    return shell.clean()
def holder():
    parts=[]
    floor=box(51.4,25.3,2,(0,0,0),.65)
    walls=box(51.4,25.3,5.8,(0,0,2),.65).cut(box(48.5,22.4,6.0,(0,0,1.9),.5))
    base=floor.fuse(walls)
    for x in (-15,15):base=base.fuse(cyl(5.4,4,2,x,0))
    for x,y in [(-20.5,7.6),(20.5,-7.6)]:
        base=base.fuse(cyl(3.2,4.0,2,x,y));base=base.cut(cyl(1.905,6.3,-.1,x,y))
    for x in (-25,25):base=base.cut(box(4,9,4.5,(x,0,3.5)))
    for x in (-6.5,6.5):
        for sign in (-1,1):
            base=base.fuse(box(3.0,1.0,3.1,(x,sign*13.15,1.7),.2))
    for x in (-15,15):base=base.cut(cyl(2.55,6.3,-.1,x,0))
    parts.append(('Socle_noir_poches_et_fixation',base.clean(),BLACK))
    for sign,x in enumerate((-15,15),1):
        stud=cyl(2.5,5.0,1,x,0).fuse(thread(5,12,.8,6).translate((x,0,0))).clean()
        parts.append((f'Goujon_M5x08_{sign}_longueur_estimee',stud,HARDWARE))
        parts.append((f'Rondelle_plate_{sign}',ring(5.0,2.65,.7,6.41).translate((x,0,0)),HARDWARE))
        lock=ring(4.35,2.65,.85,7.11).translate((x,0,0))
        lock=lock.cut(box(.65,5.0,1.1,(x,4,7.0)))
        parts.append((f'Rondelle_frein_fendue_{sign}',lock,HARDWARE))
        nut=hexagon(8,4,7.96).cut(cyl(2.5,4.2,7.86)).translate((x,0,0))
        parts.append((f'Ecrou_M5_AF8_{sign}_taraudage_simplifie',nut,HARDWARE))
    cap=cover();parts.append(('Capot_AD_estime_exterieur',cap,DARK))
    # Exterior retaining tether estimated from photos; the body plan excludes it.
    tether=tube([(-25.25,0,4),(-33.5,0,4),(-36,0,9),(-33,0,15),(-24.9,0,14)],.55)
    parts.append(('Laniere_souple_estimee_sans_cables_electriques',tether,BLACK))
    assert base.isInside(cq.Vector(-25.25,0,4),1e-5)==False # cable breakout; anchor at the edge below
    # Anchor bosses meet the tether at the breakouts without representing a lead.
    parts.append(('Ancrage_laniere_socle_estime',box(1.5,2,1.6,(-25.1,0,3.2)),BLACK))
    parts.append(('Ancrage_laniere_capot_estime',box(1.0,2,1.6,(-24.9,0,13.2)),DARK))
    return parts
def item(folder,filename,title,parts,params,published,limits):
    return dict(folder='protection-surintensite/'+folder,filename=filename,title=title,parts=parts,
        params=params,published=published,estimated=limits,view=(.6,-1,1.0),design=False,probes=[],
        source_pages=['Porte-fusible: catalogue Littelfuse 2012, PDF p.164 (imprime159); fiche2008 p.1',
            'Fusible: Littelfuse REV07272021 p.2; photo Farnell0498060.M'])
def main():
    sys.stdout.reconfigure(encoding='utf-8');results=[]
    fp=fuse();hp=holder()
    holder_limits=['Reconstruction exterieure: pas le STEP constructeur, dont acces propose par formulaire.',
        'Diametre3.81 des trous de fixation; deux goujons M5 entraxe30 selon interface MIDI.',
        'Poches, nervures, clips, visserie, cotes de laniere et marquages estimes d apres plan/photos.',
        'Plan du corps51.4x27.3x24.9; laniere deborde, reserve d espace supplementaire.',
        'Dimensions d empilage hors cosses estimees; taraudage des ecrous simplifie.']
    m=item('porte-fusible','littelfuse-04980900zxt-detaille.step','04980900ZXT | porte-fusible ferme',hp,
        dict(body_envelope_nominal_mm=[51.4,27.3,24.9],studs_pitch_mm=30,stud_thread='M5x0.8',
            mount_holes_mm=3.81,mount_holes_centres_mm=[[-20.5,7.6],[20.5,-7.6]],tether_is_estimate=True),
        ['Socle et capot noirs, goujonsM5, ecrous/rondelles; fusible vendu separement.',
         'Cotes de corps et montage suivant plan catalogue2012.'],holder_limits)
    results.append((m['folder'],export_model(m)))
    m=item('fusible-60a','littelfuse-0498060m-midi-60a-detaille.step','0498060.M | MIDI 60 A',fp,
        dict(overall_mm=[41,12,8],terminal_thickness_mm=.41,hole_diameter_mm=5.5,hole_centres_mm=30,nominal_A=60),
        ['Corps noir; reperage60 jaune; deux trous5.5 pour M5, entraxe30.',
         'Hauteur8.0 pour60A selon plan;8.3 dans certaines fiches marchandes est une cote de famille.'],
        ['Interieur et element fusible non representes; modele ne valide aucune fonction electrique.',
         'Profil exterieur, rayons, seam et petits details de moulage reconstruits/estimes.',
         'Police et position du marquage approximatives, non photographie projetee.'])
    results.append((m['folder'],export_model(m)))
    mounted=[('Fusible_'+n,s.translate((0,0,2.205)),c) for n,s,c in fp]
    compound=cq.Compound.makeCompound([s for n,s,c in mounted])
    for name,s,c in hp:
        overlap=s.intersect(compound).Volume()
        assert overlap<1e-5,(name,overlap)
    m=item('porte-fusible','ensemble-midi-60a-ferme-etude.step','MIDI 60 A | ensemble ferme',hp+mounted,
        dict(fuse_terminal_bottom_z_mm=6.0,fuse_translation_z_mm=2.205,terminal_mount_pitch_mm=30),
        ['InterfaceM5/30 mm du fusible et porte-fusible.'],holder_limits+['Sans cosses, sans fils; positions des rondelles et serrage a verifier sur kit reel.'])
    meta=export_model(m);meta['assembly_checks']=dict(fuse_holder_no_overlap=True,matching_studs_pitch_mm=30,physical_fit_tested=False)
    results.append((m['folder'],meta))
    exploded=[]
    for name,s,c in hp:
        if 'Laniere' in name or 'Ancrage_laniere' in name:continue
        if name.startswith('Capot'):s=s.translate((0,0,25))
        exploded.append((name,s,c))
    m=item('porte-fusible','ensemble-midi-60a-vue-eclatee.step','MIDI 60 A | vue eclatee',exploded+mounted,
        dict(cover_exploded_offset_z_mm=25),['Memes pieces reconstruites que montage ferme.'],
        holder_limits+['Vue eclatee illustrative; laniere omise, ce n est pas une simulation de son articulation.'])
    results.append((m['folder'],export_model(m)))
    for folder,meta in results:
        meta.update(generated_on='2026-10-14',generator='tools/build_overcurrent_step.py',generator_sha256=sha(Path(__file__)),
            coordinate_system='X longueur et entraxeM5; Y largeur; Z vertical. Fond socle/fusibleZ=0. Vue eclatee capot+25mm.',native_vendor_cad=False)
        save(ROOT/'Composants'/folder/'3D'/Path(meta['file']).with_suffix('.json'),meta)
    out=BASE/'3D';out.mkdir(parents=True,exist_ok=True)
    save(out/'catalogue.json',dict(generated_on='2026-10-14',model_count=len(results),models=[dict(folder=f,**m) for f,m in results]))
    for folder in sorted(set(f for f,m in results)):
        save(ROOT/'Composants'/folder/'3D/provenance.json',dict(generator='tools/build_overcurrent_step.py',generator_sha256=sha(Path(__file__)),
            generated_on='2026-10-14',native_vendor_cad=False,hardware_measured=False,models=[m for f,m in results if f==folder]))
    print('DONE',len(results),'STEP models',flush=True)
if __name__=='__main__':main()
