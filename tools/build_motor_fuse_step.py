"""Named, colored solid STEP reconstructions for two independent ESC supply fuses."""
from pathlib import Path
import cadquery as cq
from OCP.BRepTools import BRepTools
import json,sys,hashlib,itertools
from build_running_gear_step import box,export_model as shared_export
import build_pi_fuse_step as pi
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/protection-branches-moteurs'
GREEN=(.022,.26,.060);METAL=pi.METAL;WHITE=pi.WHITE
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def fuse30():
    outline=[(-7.25,6.5),(-9.55,8.25),(-9.55,18.8),(9.55,18.8),(9.55,8.25),(7.25,6.5)]
    prism=cq.Workplane('XZ').polyline(outline).close().extrude(5.1).val().translate((0,2.55,0))
    side=[(-1.30,6.5),(-2.05,15.6),(-2.55,16),(-2.55,18.8),(2.55,18.8),(2.55,16),(2.05,15.6),(1.30,6.5)]
    draft=cq.Workplane('YZ').polyline(side).close().extrude(19.1).val().translate((-9.55,0,0));body=prism.intersect(draft)
    for sign in [-1,1]:
        body=body.cut(box(15.3,.12,7.0,(0,sign*1.80,8.8),.04))
        for x in [-5.2,5.2]:body=body.cut(box(1.5,.35,3.3,(x,sign*1.60,9.0)))
    parts=[]
    for i,x in enumerate([-5.2,5.2],1):
        shape=[(-2.05,.55),(-1.5,0),(1.5,0),(2.05,.55),(2.05,6.5),(-2.05,6.5)]
        blade=cq.Workplane('XZ').polyline(shape).close().extrude(.65).val().translate((x,.325,0))
        parts.append((f'Lame_{i}_etamee_4_1x0_65',blade,METAL))
        pad=box(1.25,1.0,.03,(x,0,18.77),.10);body=body.cut(box(1.4,1.14,.12,(x,0,18.71),.1))
        parts.append((f'Point_test_{i}_position_estimee',pad,METAL))
    ink=cq.Workplane('XY').text('30',2.25,.015,font='Arial',halign='center',valign='center',combine=False).val().translate((0,0,18.782))
    body=body.cut(ink).cut(ink.translate((0,0,.01)))
    return [('Corps_PA66_vert_moulage_approche',body.clean(),GREEN)]+parts+[('Marquage_30_blanc_approche',ink,WHITE)]
HLIMITS=['Support 5065 reconstruit: aucun plan ni STEP natif fabricant obtenu; non mesure.',
    'Corps et oreille37.5x38x15mm estimes; trou5.0mm est une estimation, pas un plan de percage.',
    'Contacts femelles, joint orange et languettes estimes; compression illustree, aucune qualification IP.',
    'Deux fils rouges12AWG sortent du meme cote; 100mm exterieurs et denudage8mm illustratifs.',
    '19brins de rayon0.235mm par fil: representation de3.30mm2; nombre de brins reel inconnu.',
    'Sans cosses, XT60, vis de chassis, jonction commune ou faisceau final.']
FLIMITS=['Enveloppe et lames selon ficheATOaftermarket2022, sans tolerances de production.',
    'Depouilles, rayons, poches, points de test et police du30 estimes; vert translucide rendu opaque.',
    'Element interne de fusion non represente: pas un modele de fabrication ou de simulation electrique.']
FPARAMS=dict(reference='0ATO030.V',nominal_A=30,fuse_envelope_mm=[19.1,5.1,18.8],blade_width_mm=4.1,
    blade_thickness_mm=.65,blade_exposed_mm=6.5,blade_outside_span_mm=14.5,blade_pitch_inferred_mm=10.4)
HPARAMS=dict(reference='BlueSea5065',manufacturer_max_fuse_A=30,wire_gauge='12AWG',holder_body_and_tab_estimated_mm=[37.5,38,15],
    wire_outer_diameter_estimated_mm=4.3,wire_external_length_illustrative_mm=100,stripped_end_illustrative_mm=8,
    strands_illustrative_count=19,mount_hole_estimated_mm=5.0,native_vendor_dimensions_obtained=False)
def item(folder,file,title,parts,params,limits,view=(.6,-1,1.05)):
    return dict(folder='protection-branches-moteurs/'+folder if folder else 'protection-branches-moteurs',filename=file,
        title=title,parts=parts,params=params,estimated=limits,published=['5065:ATO/ATC,12AWG,max30A,fusible separe.',
        'ATO30:19.1x5.1x18.8mm,lames4.1x0.65mm,enveloppe14.5mm; fiche2022.'],probes=[],view=view,design=False,
        source_pages=['Fiche Littelfuse ATOaftermarket2022,p1-3','BlueSea5065 fabricant et photo AmazonB004ZIUA62',
        'Provenance support et mesures approximatives: dossier protection-branche-pi/cotes.md'])
def export(m):
    for n,s,c in m['parts']:BRepTools.Clean_s(s.wrapped)
    boxes=[s.BoundingBox() for n,s,c in m['parts']];overlaps=[]
    for i,j in itertools.combinations(range(len(m['parts'])),2):
        a,b=boxes[i],boxes[j]
        if any(min(getattr(a,k+'max'),getattr(b,k+'max'))<max(getattr(a,k+'min'),getattr(b,k+'min'))-1e-7 for k in ['x','y','z']):continue
        v=m['parts'][i][1].intersect(m['parts'][j][1]).Volume()
        if v>1e-5:overlaps.append(dict(a=m['parts'][i][0],b=m['parts'][j][0],volume_mm3=v))
    assert not overlaps,(m['filename'],overlaps)
    meta=shared_export(m);meta.update(generated_on='2026-10-14',generator='tools/build_motor_fuse_step.py',generator_sha256=sha(Path(__file__)),
        reused_geometry_generator='tools/build_pi_fuse_step.py',reused_geometry_generator_sha256=sha(Path(pi.__file__)),
        coordinate_system='Support:X largeur,Y insertion,Z epaisseur; fils vers-Y. Fusible isole:Z hauteur. Montage rotationX-90,Y+4,Z+7.5.')
    meta['validation']['pairwise_material_overlaps']=overlaps
    save(ROOT/'Composants'/m['folder']/'3D'/Path(meta['file']).with_suffix('.json'),meta);return dict(folder=m['folder'],**meta)
def main():
    sys.stdout.reconfigure(encoding='utf-8');f=fuse30();h=pi.holder();c=[('Capot_5065_estime',pi.cap(),pi.BLACK)]
    mounted=pi.mounted_fuse(f);closed=h+c+mounted;models=[]
    models.append(export(item('fusible-30a','littelfuse-0ato030-v-detaille.step','Littelfuse ATO30 : fusible vert 30 A',f,FPARAMS,FLIMITS,view=(.6,-1,.65))))
    models.append(export(item('porte-fusible','bluesea-5065-porte-fusible-detaille.step','Blue Sea 5065 : support sans fusible',h+c,HPARAMS,HLIMITS)))
    models.append(export(item('','ensemble-moteur-ato30-ferme-etude.step','Depart moteur : 5065 et ATO30 ferme',closed,dict(HPARAMS,fuse=FPARAMS),HLIMITS+FLIMITS)))
    opened=h+[(n,s.translate((0,36,0)),co) for n,s,co in c]+mounted
    models.append(export(item('','ensemble-moteur-ato30-ouvert-etude.step','Depart moteur : capot eclate',opened,dict(HPARAMS,fuse=FPARAMS,cover_shift_y_mm=36),HLIMITS+FLIMITS,view=(.65,1,1.0))))
    pair=[]
    for i,x in enumerate([-26,26],1):pair += [(f'Branche_ESC{i}_'+n,s.translate((x,0,0)),co) for n,s,co in closed]
    models.append(export(item('','deux-protections-moteurs-ato30-etude.step','Deux departs ESC independants : pose etude',pair,dict(HPARAMS,fuse=FPARAMS,holder_centres_x_mm=[-26,26]),HLIMITS+FLIMITS+['Pose deux supports sans jonction commune; les4fils rouges ne sont pas connectes dans ce modele.'])))
    save(BASE/'3D/catalogue.json',dict(generated_on='2026-10-14',unit='mm',model_count=len(models),models=models));print('DONE',len(models),'STEP',flush=True)
if __name__=='__main__':main()
