"""Detailed exterior reconstructions of the Pi branch holder and ATO fuse."""
from pathlib import Path
import cadquery as cq
from OCP.BRepTools import BRepTools
import json,sys,hashlib,math,itertools
from build_running_gear_step import box,cyl,export_model as shared_export
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/protection-branche-pi'
BLACK=(.015,.017,.02);METAL=(.65,.67,.68);BROWN=(.25,.092,.048);WHITE=(.89,.89,.86)
RED=(.64,.035,.025);ORANGE=(.87,.28,.025);CONTACT=(.50,.34,.12)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rod(r,length,x,y,z):return cyl(r,length,z,x,y,axis=(0,1,0))
def stadium(w,h,length,y,zc=7.5):
    """Oval cross-section X/Z, extruded along Y; end radii h/2."""
    radius=h/2;cx=(w-h)/2
    return box(w-h,length,h,(0,y+length/2,zc-radius)).fuse(rod(radius,length,-cx,y,zc)).fuse(rod(radius,length,cx,y,zc)).clean()
def fuse():
    # Drawing p2: width19.1, depth5.1, height18.8; blades4.1/0.65,
    # outside span14.5, thus centre pitch14.5-4.1=10.4 (not14.5).
    front=[(-7.25,6.5),(-9.55,8.25),(-9.55,18.8),(9.55,18.8),(9.55,8.25),(7.25,6.5)]
    prism=cq.Workplane('XZ').polyline(front).close().extrude(5.1).val().translate((0,2.55,0))
    side=[(-1.30,6.5),(-2.05,15.6),(-2.55,16),(-2.55,18.8),(2.55,18.8),(2.55,16),(2.05,15.6),(1.30,6.5)]
    draft=cq.Workplane('YZ').polyline(side).close().extrude(19.1).val().translate((-9.55,0,0))
    body=prism.intersect(draft)
    for sign in [-1,1]:
        # Small exterior mould recesses; no calibrated internal fuse link invented.
        body=body.cut(box(15.3,.12,7.0,(0,sign*1.80,8.8),.04))
        for x in [-5.2,5.2]:body=body.cut(box(1.5,.35,3.3,(x,sign*1.60,9.0)))
    metal=[]
    for i,x in enumerate([-5.2,5.2],1):
        outline=[(-2.05,.55),(-1.5,0),(1.5,0),(2.05,.55),(2.05,6.5),(-2.05,6.5)]
        blade=cq.Workplane('XZ').polyline(outline).close().extrude(.65).val().translate((x,.325,0))
        metal.append((f'Lame_{i}_etamee_4_1x0_65',blade,METAL))
        pad=box(1.25,1.0,.03,(x,0,18.77),.10)
        body=body.cut(box(1.4,1.14,.12,(x,0,18.71),.1))
        metal.append((f'Point_test_superieur_{i}_position_estimee',pad,METAL))
    ink=cq.Workplane('XY').text('7.5',2.25,.015,font='Arial',halign='center',valign='center',combine=False).val().translate((0,0,18.782))
    body=body.cut(ink).cut(ink.translate((0,0,.01)))
    return [('Corps_PA66_brun_moulage_approche',body.clean(),BROWN)]+metal+[('Marquage_7_5_blanc_approche',ink,WHITE)]
def cap():
    outer=stadium(25,15,30,-3.5)
    inner=stadium(22.8,12.8,28.7,-3.6)
    result=outer.cut(inner)
    # Tab joins the curved cover; hole diameter and locations are estimates.
    tab=box(18,7.94,1.7,(-16,22.53,13.3),.6).cut(cyl(2.5,1.9,13.2,-21.03,22.53))
    result=result.fuse(tab)
    for x in [-5.3,5.3]:
        result=result.fuse(box(.8,17.5,.38,(x,9.0,14.62),.15))
        result=result.fuse(box(1.5,4.4,.38,(x,1.0,14.62),.18))
    result=result.fuse(box(1.5,4,.35,(0,8.8,14.65),.18))
    return result.clean()
def holder():
    base=stadium(22,11,22,-11.5)
    for x in [-5,5]:base=base.fuse(box(2.2,14,.42,(x,2,12.97),.1))
    # The orange seals are shown in a lightly compressed study pose.
    seals=[]
    for i,y in enumerate([-1.5,.1,1.7],1):
        seal=stadium(22.6,12.6,1.0,y).cut(stadium(22,11,1.2,y-.1)).cut(base)
        seals.append((f'Joint_orange_nervure_{i}_compression_estimee',seal.clean(),ORANGE))
    parts=[];contacts=[];wires=[]
    for i,x in enumerate([-5.2,5.2],1):
        # Female terminals are exterior approximations from the photo, not vendor CAD.
        socket=box(4.8,14.5,2.6,(x,3.25,6.2)).cut(box(4.2,14.1,.70,(x,3.55,7.15)))
        for side in [-1,1]:socket=socket.cut(box(.35,2.6,.85,(x+side*2.30,9.2,8.0)))
        contacts.append((f'Contact_femelle_{i}_forme_et_matiere_estimees',socket.clean(),CONTACT))
        # Both positive wires leave the same rear face, as in the reference photo.
        jacket=rod(2.15,106.5,x,-112.5,7.5).cut(rod(1.20,106.7,x,-112.6,7.5))
        wires.append((f'Gaine_rouge_{i}_pose100mm_hors_corps_estimee',jacket,RED))
        centres=[(0,0)]
        for ring,radius,count in [(1,.47,6),(2,.94,12)]:
            for j in range(count):centres.append((radius*math.cos(2*math.pi*j/count),radius*math.sin(2*math.pi*j/count)))
        for j,(dx,dz) in enumerate(centres,1):
            strand=rod(.235,116.5,x+dx,-120.5,7.5+dz)
            wires.append((f'Fil_{i}_brin_etame_{j:02d}_nombre_brins_estime',strand,METAL))
        base=base.cut(rod(2.15,7.6,x,-11.6,7.5))
        base=base.cut(socket)
        # Keep the insertion opening free up to the front face.
        base=base.cut(box(4.2,6.8,.80,(x,7.2,7.1)))
    parts.append(('Socle_noir_et_guides_reconstruits',base.clean(),BLACK));parts+=contacts+seals+wires
    return parts
def mounted_fuse(parts):return [('Fusible_'+n,s.rotate((0,0,0),(1,0,0),-90).translate((0,4,7.5)),c) for n,s,c in parts]
def item(folder,file,title,parts,params,limits,probes=None,view=None):
    return dict(folder='protection-branche-pi/'+folder if folder else 'protection-branche-pi',filename=file,title=title,
        parts=parts,params=params,published=['FusibleATO:19.1x5.1x18.8; lames4.1x0.65; depassement6.5; span14.5 selonfiche2022.',
        '5065: unATO/ATC, fils12AWG, maximum30A; fusible vendu separement.'],estimated=limits,
        view=view or (.6,-1,1.05),design=False,probes=probes or [],
        source_pages=['Littelfuse ATOaftermarket2022 p2; catalogue2013 PDFp8','BlueSea5065 photoAmazonB004ZIUA62','PKYSmesures2017; marchandSkysat38x25x15 non fabricant'])
def export(m):
    for n,s,c in m['parts']:BRepTools.Clean_s(s.wrapped)
    boxes=[s.BoundingBox() for n,s,c in m['parts']];overlaps=[]
    for i,j in itertools.combinations(range(len(m['parts'])),2):
        a,b=boxes[i],boxes[j]
        if any(min(getattr(a,ax+'max'),getattr(b,ax+'max'))<max(getattr(a,ax+'min'),getattr(b,ax+'min'))-1e-7 for ax in ['x','y','z']):continue
        v=m['parts'][i][1].intersect(m['parts'][j][1]).Volume()
        if v>1e-5:overlaps.append(dict(a=m['parts'][i][0],b=m['parts'][j][0],volume_mm3=v))
    assert not overlaps,(m['filename'],overlaps)
    meta=shared_export(m);meta.update(generated_on='2026-10-14',generator='tools/build_pi_fuse_step.py',generator_sha256=sha(Path(__file__)))
    meta['validation']['pairwise_material_overlaps']=overlaps
    meta['coordinate_system']='Holder:X largeur,Y insertion, Z epaisseur; cables vers-Y. Fusibleisole:Zhauteur, centreXY; montage rotationX-90,Y+4,Z+7.5.'
    meta['appearance_note']='Fusible reel translucide brun; export brun opaque. Aucune simulation optique ou electrique.'
    save(ROOT/'Composants'/m['folder']/'3D'/Path(meta['file']).with_suffix('.json'),meta)
    return dict(folder=m['folder'],**meta)
def main():
    sys.stdout.reconfigure(encoding='utf-8');models=[];fp=fuse();hp=holder();cp=[('Capot_noir_5065_avec_oreille_estime',cap(),BLACK)]
    flimits=['Cotes d enveloppe et lames selon dessin de reference2022, sans tolerances de production.',
        'Taper, rayons, poches, points de test et marquage estimes; interieur/calibratedfusionlink non modelise.',
        'Representation opaque du PA66 brun translucide; pas un modele pour fabriquer un fusible.']
    hlimits=['Reconstruction estimee: pas de plan constructeur ni STEP natif du5065 obtenus.',
        'Enveloppe corps/oreille37.5x38x15 proposee; taille38x25x15 d un marchand ambiguë, nongarantie.',
        'Capot creux, languettes, joint et contacts inspiresde photo, formes/epaisseurs/matieres aconfirmer.',
        'Les deux fils12AWG sortentdu memecote; longueur representee100mm horscorps et denudage8mm illustratifs.',
        '19brins de rayon0.235 parfil: aire3.30mm2 approximant12AWG, nombre debrins reel nonpublie.',
        'Compressiondes joints estune poseCAO estimee, nequalifiepas etancheite.',
        'Troude fixationmodele5.0: estimation, mesureapproxPKYS3/16in, aucunplan deperçage garanti.',
        'Sans cosses/vis au chassis; fils libres sont leurs terminaisons illustrees, pas uncable interrompu.']
    params=dict(fuse_envelope_mm=[19.1,5.1,18.8],blade_width_mm=4.1,blade_thickness_mm=.65,
        blade_free_length_mm=6.5,blade_outside_span_mm=14.5,blade_pitch_inferred_mm=10.4)
    models.append(export(item('fusible-7-5a','littelfuse-0ato07-5v-detaille.step','ATO 7,5 A | fusible de la branche Pi',fp,params,flimits,view=(.6,-1,.65))))
    hp_params=dict(holder_body_and_tab_estimated_mm=[37.5,38,15],wire_gauge_published='12AWG',
        representative_outer_wire_diameter_mm=4.3,model_external_lead_length_mm=100,model_stripped_end_mm=8,
        representative_strands=19,representative_strand_radius_mm=.235,mount_hole_estimated_mm=5.0,
        mount_hole_centre_estimated_mm=[-21.03,22.53],native_vendor_dimensions_obtained=False)
    models.append(export(item('porte-fusible','bluesea-5065-porte-fusible-detaille.step','5065 | porte-fusible avec fils et capot',hp+cp,hp_params,hlimits)))
    models.append(export(item('porte-fusible','bluesea-5065-corps-ouvert-detaille.step','5065 | socle et contacts sans capot',hp,hp_params,hlimits,view=(.65,1,1.0))))
    models.append(export(item('porte-fusible','bluesea-5065-capot-detaille.step','5065 | capot avec oreille',cp,hp_params,hlimits)))
    mounted=mounted_fuse(fp)
    models.append(export(item('','ensemble-pi-ato-7-5a-ferme-etude.step','Branche Pi | ensemble ATO ferme',hp+cp+mounted,
        dict(hp_params,**params),hlimits+flimits+['InterfaceenCAO verifiee; pas unmontagephysique ni faisceauqualifie.'])))
    exploded=hp+[(n,s.translate((0,36,0)),c) for n,s,c in cp]+mounted
    models.append(export(item('','ensemble-pi-ato-7-5a-ouvert-etude.step','Branche Pi | vue eclatee',exploded,
        dict(hp_params,cover_exploded_y_mm=36,**params),hlimits+flimits+['CapottranslateY+36: vue eclatee, paspose defonctionnement.'])))
    save(BASE/'3D/catalogue.json',dict(generated_on='2026-10-14',model_count=len(models),unit='mm',models=models))
    print('DONE',len(models),'STEP files',flush=True)
if __name__=='__main__':main()
