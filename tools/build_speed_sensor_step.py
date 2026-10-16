"""Coloured exterior STEP models, exact KEMET original, provenance and previews."""
from pathlib import Path
import hashlib
import json
import math
import shutil
import sys

import cadquery as cq
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from build_running_gear_step import box,cyl,export_model
from prepare_pi5_step import read_xcaf,collect_leaves,mesh_shapes
from render_step_meshes import render_meshes

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'Composants/capteurs-vitesse'
MODELS=[]
TIN=(.58,.61,.64);BLACK=(.014,.016,.019);GREY=(.35,.37,.38)


def optimal(self,tolerance=None):
    b=Bnd_Box();BRepBndLib.AddOptimal_s(self.wrapped,b,False,False)
    return cq.BoundBox(b)


def save(folder,filename,title,parts,published,estimates,params,view=(.7,-1,.6)):
    item=dict(folder='capteurs-vitesse/'+folder,filename=filename,title=title,parts=parts,
              published=published,estimated=estimates+['Colours and minor optical details estimated; no measured hardware or internal reconstruction'],
              params=params,view=view,design=False,probes=[],source_pages=['See component cotes.md and original PDFs in ../notices'])
    m=export_model(item)
    p=BASE/folder/'3D'/filename
    shape=cq.importers.importStep(str(p)).val()
    m.update(generated_on='2026-10-15',component_folder=folder,relative_step_path=str(p.relative_to(ROOT)).replace('\\','/'),
             coordinate_system=params.get('coordinate_system','See parameters'))
    m['validation']['volume_after_default_quadrature_mm3']=shape.Volume()
    p.with_suffix('.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    MODELS.append(m)


def sensor():
    # LPG0003A bottom outline, mid-range dimensions; three straight rectangular leads.
    body=cq.Workplane('XY').polyline([(-2,-.76),(2,-.76),(2,0),(1.24,.76),(-1.24,.76),(-2,0)]).close().extrude(3.15)
    body=body.edges('|Z').fillet(.035).val()
    parts=[('Corps_LPG_resine_noire',body,BLACK)]
    for x,n in [(-1.27,'1_VCC'),(0,'2_GND'),(1.27,'3_OUT')]:
        # Shoulder narrows smoothly over 0.8 mm. Metal terminates at the body datum.
        lead=(cq.Workplane('XY',origin=(x,-.2175,-15.3)).rect(.415,.435).extrude(13.4)
              .faces('>Z').workplane().rect(.415,.435).workplane(offset=.8).rect(.475,.435).loft(combine=True)
              .faces('>Z').workplane().rect(.475,.435).extrude(1.1)).val()
        parts.append(('Patte_'+n+'_etamee',lead,TIN))
    # Marking is documented by the June 2026 ordering addendum. Its font/location is indicative.
    letters=cq.Workplane('XY').text('+QLAJ',.64,.002,font='Arial',combine=False).val()
    letters=letters.rotate((0,0,0),(1,0,0),90).translate((0,-.7601,1.7))
    parts.append(('Marquage_plus_QLAJ_position_estimee',letters,GREY))
    save('capteur-hall-drv5033','drv5033ajqlpg-detaille.step','TI DRV5033AJQLPG | boitier LPG et pattes',parts,
         ['TI LPG0003A drawing 4221343/C: width3.9-4.1; body height3.05-3.25; thickness1.42-1.62mm',
          'Lead length15.1-15.5; pitch1.27+/-0.05mm; body back flats and 45degree corners',
          'TI addendum24Jun2026: marking +QLAJ; pin1VCC pin2GND pin3OUT'],
         ['Mould radii0.035mm, shoulder location, marking font/position/thickness estimated',
          'No undocumented die, bonding wires, leadframe or mould seam'],
         dict(body_width_mm=4,body_depth_mm=1.52,body_height_mm=3.15,lead_length_mm=15.3,lead_pitch_mm=1.27,
              coordinate_system='X across pins; body bottom Z=0, top Z=3.15; leads to -Z; marked flat face -Y; pins1/2/3 at X=-1.27/0/+1.27'),view=(.5,-1,.38))


def magnet():
    shape=cq.Workplane('XY').circle(1.5).extrude(2).edges().fillet(.025).val()
    save('aimants-s-03-02-n','aimant-s-03-02-n-detaille.step','supermagnete S-03-02-N | diametre3 x2mm',
         [('Aimant_NdFeB_N48_surface_NiCuNi',shape,(.62,.65,.68))],
         ['Article PDF: diameter3, height2mm, tolerances+/-0.1mm; axial magnetisation; NiCuNi silver'],
         ['Edge radius0.025mm estimated; plating layer thicknesses unpublished and not modelled',
          'No coloured pole paint: actual product is silver; N/S cannot be determined from STEP'],
         dict(diameter_mm=3,height_mm=2,estimated_edge_radius_mm=.025,magnetisation_axis='Z',coordinate_system='Disc axisZ; bottom faceZ=0; no absolute pole assignment'))


def resistor_parts(formed=False):
    body=cq.Workplane('YZ').circle(1.25).extrude(6.5).edges('%Circle').chamfer(.16).val().translate((-3.25,0,0))
    parts=[]
    bands=[(-2.3,(.13,.045,.015)),(-1.38,(.008,.008,.008)),(-.46,(.008,.008,.008)),(.46,(.65,.008,.006)),(2.2,(.13,.045,.015))]
    for i,(x,color) in enumerate(bands):
        shell=cyl(1.27,.4,0,x-.2,0,axis=(1,0,0)).cut(cyl(1.23,.42,0,x-.21,0,axis=(1,0,0)))
        paint=body.intersect(shell)
        body=body.cut(paint)
        parts.append((f'Anneau_{i+1}_code10k_1pct',paint,color))
    parts.insert(0,('Corps_laque_bleue_estimee',body.clean(),(.025,.20,.38)))
    if not formed:
        parts.extend([('Fil_gauche_28mm',cyl(.3,28,0,-31.25,0,axis=(1,0,0)),TIN),
                      ('Fil_droit_28mm',cyl(.3,28,0,3.25,0,axis=(1,0,0)),TIN)])
        return parts
    # Horizontal body centre Z=2.45; bend radius1.2, terminal pitch10.16mm.
    parts=[(n,s.translate((0,0,2.45)),c) for n,s,c in parts]
    for side in [-1,1]:
        p0=cq.Vector(side*3.25,0,2.45);p1=cq.Vector(side*3.88,0,2.45)
        pm=cq.Vector(side*(3.88+1.2/math.sqrt(2)),0,1.25+1.2/math.sqrt(2))
        p2=cq.Vector(side*5.08,0,1.25);p3=cq.Vector(side*5.08,0,-3)
        path=cq.Wire.assembleEdges([cq.Edge.makeLine(p0,p1),cq.Edge.makeThreePointArc(p1,pm,p2),cq.Edge.makeLine(p2,p3)])
        lead=cq.Workplane(cq.Plane(origin=p0,normal=(side,0,0))).circle(.3).sweep(cq.Workplane('XY').newObject([path]),isFrenet=False).val()
        parts.append(('Fil_forme_'+str(side),lead,TIN))
    return parts


def resistor():
    published=['Vishay28724 p3: body diameter2.5max, length6.5max, wire diameter0.6nom, lead length28min each, formed pitch10min']
    est=['Body envelope drawn at maximum, end chamfers and lacquer thickness estimated',
         'Five band code brown black black red brown; exact lot paint colour and band geometry unmeasured']
    for formed in [False,True]:
        name='mrs25-10k-formee-pas10-16.step' if formed else 'mrs25-10k-pattes-droites.step'
        save('resistances-rappel-10k',name,'Vishay MRS25 10k | '+('pattes formees pas10.16mm' if formed else 'pattes droites non recoupees'),resistor_parts(formed),published,
             est+(['Formed geometry is project pose: radius1.2mm, pitch10.16mm, trimmed endsZ=-3; not supplier-preformed part'] if formed else []),
             dict(body_length_max_mm=6.5,body_diameter_max_mm=2.5,lead_diameter_mm=.6,
                  formed=formed,terminal_pitch_mm=10.16 if formed else None,
                  coordinate_system='Body axisX; centreZ=2.45 for formed version, Z=0 for straight; formed leads downward'),view=(.8,-1,1.0) if formed else (.25,-1,.7))


def capacitor():
    source=BASE/'references/KEMET-C315C104K5R5TA-original.step'
    out=BASE/'condensateurs-decouplage-100nf/3D';out.mkdir(parents=True,exist_ok=True)
    target=out/'kemet-c315c104k5r5ta-officiel.step';shutil.copyfile(source,target)
    doc=read_xcaf(target);leaves,whole,ct,roots,colors=collect_leaves(doc)
    assert whole.isValid() and all(shell.Closed() for shell in whole.Shells())
    meshes=mesh_shapes(leaves,ct)
    preview=target.with_suffix('.png')
    render_meshes(preview,meshes,(.6,-1,.6),'KEMET C315C104K5R5TA | CAO officielle','STEP original constructeur - geometrie et couleurs du fichier conservees')
    # Use the same import path for numerical comparisons with FreeCAD.
    shape=cq.importers.importStep(str(target)).val();b=shape.BoundingBox()
    m=dict(file=target.name,title='KEMET C315C104K5R5TA | CAO officielle',generated_on='2026-10-15',unit='mm',
           component_folder='condensateurs-decouplage-100nf',relative_step_path=str(target.relative_to(ROOT)).replace('\\','/'),
           source='https://search.kemet.com/component-documentation/download/step/C315C104K5R5TA.STEP',
           sha256=hashlib.sha256(target.read_bytes()).hexdigest(),bytes=target.stat().st_size,native_vendor_cad=True,
           original_unchanged=True,hardware_measured=False,published_nominal=['See specific KEMET PDF; official STEP is nominal, not lot tolerance'],
           estimates_and_limitations=['No geometry or original colours modified; installed lead forming not designed'],
           bounds_mm={k:getattr(b,k) for k in ['xmin','xmax','ymin','ymax','zmin','zmax']},
           validation=dict(valid_after_reimport=shape.isValid(),solids=len(shape.Solids()),faces=len(shape.Faces()),
                           colors=colors,volume_after_default_quadrature_mm3=shape.Volume()),
           preview=dict(file=preview.name,sha256=hashlib.sha256(preview.read_bytes()).hexdigest()))
    target.with_suffix('.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');MODELS.append(m)


def index():
    common=BASE/'3D';common.mkdir(parents=True,exist_ok=True)
    for folder in sorted({m['component_folder'] for m in MODELS}):
        models=[m for m in MODELS if m['component_folder']==folder]
        lines=['# Modèles STEP - '+folder,'','Fichiers en millimètres ; [cotes et limites](../cotes.md).','',
               '| Modèle | STEP | Aperçu |','| --- | --- | --- |']
        for m in models:lines.append(f'| {m["title"]} | [{m["file"]}]({m["file"]}) | [PNG]({m["preview"]["file"]}) |')
        lines+=['','Le JSON voisin de chaque STEP donne les paramètres, les sources et les contrôles. La CAO KEMET est native et intacte ; les autres modèles sont des reconstructions extérieures avec détails estimés. Aucune structure interne non documentée. Pas de support de châssis dans ces fichiers.',
                '', '[Contrôle FreeCAD commun](../../3D/validation-freecad.json) et [catalogue](../../3D/catalogue.json).']
        (BASE/folder/'3D/README.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    catalog=dict(generated_on='2026-10-15',generator='tools/build_speed_sensor_step.py',model_count=len(MODELS),models=MODELS)
    (common/'catalogue.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Modèles des capteurs de vitesse','',f'{len(MODELS)} STEP : capteur, aimant, résistance droite et formée, condensateur officiel.','',
           '| Pièce | Documentation 3D |','| --- | --- |']
    for folder in sorted({m['component_folder'] for m in MODELS}):lines.append(f'| {folder} | [STEP, aperçus et provenance](../{folder}/3D/README.md) |')
    lines+=['','[Vue d’ensemble](apercu-composants.png) ; échelles indépendantes. [Catalogue et provenance](catalogue.json), [contrôles FreeCAD](validation-freecad.json).',
            '', 'Les modèles individuels ne définissent ni la fixation des aimants ni le support de capteur. Ces interfaces restent pour le châssis. Les inscriptions et petits rayons reconstruits sont identifiés comme estimés. Les originaux fournisseur ne sont pas modifiés.']
    (common/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    gallery=Image.new('RGB',(1500,3*640),'white')
    for i,m in enumerate(MODELS):
        p=ROOT/m['relative_step_path'];im=Image.open(p.with_suffix('.png')).convert('RGB');im.thumbnail((744,620))
        gallery.paste(im,((i%2)*750+(750-im.width)//2,(i//2)*640))
    gallery.save(common/'apercu-composants.png')


def main():
    sys.stdout.reconfigure(encoding='utf-8');cq.Shape.BoundingBox=optimal
    sensor();magnet();resistor();capacitor();index()
    print('Five STEP models built',flush=True)


if __name__=='__main__':main()
