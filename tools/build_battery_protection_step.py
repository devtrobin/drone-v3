"""Three study models. Native Pololu CAD stays intact; PCB is an unbuilt concept."""
from pathlib import Path
import json,hashlib,sys
import cadquery as cq
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.BRepTools import BRepTools
from OCP.Quantity import Quantity_Color
from OCP.XCAFDoc import XCAFDoc_ColorSurf,XCAFDoc_ColorGen
from build_running_gear_step import box,cyl,ring,export_model
from prepare_pi5_step import read_xcaf,collect_leaves
from render_step_meshes import render_meshes

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'Composants/protection-batterie'
BLACK=(.015,.020,.025);GREEN=(.008,.14,.035);GOLD=(.62,.40,.09)
STEEL=(.50,.52,.55);WHITE=(.87,.90,.93);COPPER=(.64,.30,.08)

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def text_shape(text,size,pos,color,parts,name):
    q=cq.Workplane('XY').text(text,size,.018,font='Arial',combine=False).val().translate(pos)
    parts.append((name,q,color))

def item(folder,file,title,parts,published,estimated,params,design=False):
    return dict(folder='protection-batterie/'+folder,filename=file,title=title,parts=parts,
        published=published,estimated=estimated,params=params,view=(.5,-.7,1.2),
        design=design,probes=[],source_pages=[])

def package(parts,name,x,y,width,depth,height,pins,pitch):
    parts.append((name+'_boitier',box(width,depth,height,(x,y,1.82),.12),BLACK))
    for side in (-1,1):
        count=pins//2+(1 if pins%2 and side==-1 else 0)
        for n in range(count):
            px=x+(n-(count-1)/2)*pitch;py=y+side*(depth/2+.30)
            lead=box(.30,.76,.14,(px,py,1.63))
            lead=lead.fuse(box(.30,.20,.42,(px,y+side*(depth/2+.06),1.70)))
            parts.append((f'{name}_patte_{side}_{n}',lead,STEEL))
            parts.append((f'{name}_pad_{side}_{n}',box(.60,1.0,.035,(px,py,1.605)),GOLD))

def resistor(parts,name,value,x,y):
    parts.append((name+'_ceramique',box(2.0,1.25,.50,(x,y,1.72),.09),BLACK))
    for side in (-1,1):
        parts.append((name+'_terminaison_'+str(side),box(.35,1.25,.50,(x+side*.82,y,1.72)),STEEL))
        parts.append((name+'_pad_'+str(side),box(.65,1.5,.035,(x+side*.98,y,1.605)),GOLD))
    text_shape(value,.55,(x,y,2.24),WHITE,parts,name+'_valeur_illustrative')

def supervisor():
    parts=[]
    board=box(54,32,1.6,fillet=1)
    for x in (-24,24):
        for y in (-13,13):board=board.cut(cyl(1.1,1.8,-.1,x,y))
    # Slots visually separate the two local-cell domains from logic. Routing is
    # illustrative and NOT a manufacturable validated PCB/netlist.
    for y in (-11,-5,5,11):board=board.cut(box(.8,2.8,1.8,(7,y,-.1),.3))
    parts.append(('PCB_V3_etude_non_routee_pour_fabrication',board,GREEN))
    for row,y in enumerate((-8,8),1):
        package(parts,f'U{row}_TLV6700_DDC',-12,y,2.9,1.6,.8,6,.95)
        for i,(value,dx,dy) in enumerate([('4022',-21,-3),('4022',-18,-3),('1002',-14,-3),('7502',-21,3),('1002',-17,3),('1501',-5,-3),('1501',-5,3)]):
            resistor(parts,f'R_C{row}_{i+1}',value,dx,y+dy)
        parts.append((f'C_C{row}_100nF',box(2,1.25,.8,(-8,y,1.70),.1),(.51,.30,.12)))
        for n,dy in enumerate((-3,3),1):
            parts.append((f'C_FIL_C{row}_{n}_100nF',box(2,1.25,.8,(-10,y+dy,1.70),.1),(.51,.30,.12)))
        for j,dy in enumerate((-3,3),1):
            # VOS618A approximate package and lead shape; pinout is in PDF.
            name=f'OP_C{row}_{j}_VOS618A8T'
            body=box(4.4,2.6,2.0,(7,y+dy,1.75),.15)
            parts.append((name+'_boitier',body,BLACK))
            for sx in (-1,1):
                for sy in (-1,1):
                    profile=[(sx*a,z) for a,z in [(3.5,1.65),(2.85,1.65),(2.6,2.15),(2.2,2.15),(2.2,2.27),(2.75,2.27),(2.95,1.77),(3.5,1.77)]]
                    lead=cq.Workplane('XZ').polyline(profile).close().extrude(.4).val().translate((7,y+dy+sy*.635+.2,0))
                    parts.append((name+f'_patte_{sx}_{sy}',lead,STEEL))
                    parts.append((name+f'_pad_{sx}_{sy}',box(1.25,.90,.035,(7+sx*3.125,y+dy+sy*.635,1.605)),GOLD))
            text_shape('618',.70,(7,y+dy,3.77),WHITE,parts,name+'_texte_indicatif')
        # Exposed illustrative track segments remain inside local cell domain.
        for n,dy in enumerate((-3,3)):
            parts.append((f'Piste_C{row}_{n}_illustrative',box(13,.28,.035,(-15,y+dy,1.605)),COPPER))
        text_shape(f'CELL {row}',1.3,(-12,y+5,1.66),WHITE,parts,f'Serig_C{row}')
    package(parts,'U3_SN74LVC2G17_DCK',17,-4,2,1.25,.85,6,.65)
    parts.append(('U4_MCP1703A_SOT89_corps_estime',box(4.5,2.5,1.6,(17,5,1.82),.12),BLACK))
    for i,x in enumerate((15.5,17,18.5),1):
        parts.append((f'U4_broche_{i}',box(.50,1.5,.20,(x,3.65,1.66)),STEEL))
    parts.append(('U4_SOT89_tab_metal_non_quatrieme_broche',box(1.8,1.2,.20,(17,6.4,1.66)),STEEL))
    for i,y in enumerate((-9,-6,-3),1):package(parts,f'D{i}_BAT54_SOT23',20,y,2.9,1.3,1.0,3,1.9)
    for i,(value,x,y) in enumerate([('4702',12,-4),('4702',12,-1),('1002',21,11),('1002',18,11),('1003',17,-12)],1):resistor(parts,'R_LOG_'+str(i),value,x,y)
    for x,y in ((12,6),(22,8)):parts.append(('C_LDO_'+str(x),box(2,1.25,1.0,(x,y,1.70),.1),(.53,.33,.15)))
    parts.append(('C_LOG_100nF',box(2,1.25,.8,(14.5,-1,1.70),.1),(.53,.33,.15)))
    # Study XH-style three-way upright sensor input. It carries milliamps only.
    housing=box(6,10,6.5,(-24,-5,1.65),.3)
    housing=housing.cut(box(4.4,8.4,5.2,(-24,-5,3.0),.2))
    parts.append(('J1_equilibrage_XH_estime',housing,WHITE))
    for i in range(3):
        y=-7.5+i*2.5
        parts.append((f'J1_broche_{i+1}',box(.64,.64,6.2,(-24,y,1.6)),STEEL))
        parts.append((f'J1_pad_{i+1}',ring(.85,.38,.035,1.605).translate((-24,y,0)),GOLD))
    # Six-way logic connector: proposed interface, not a purchased reference.
    header=box(2.5,15.24,2.54,(24.1,-2,1.65))
    parts.append(('J2_logique_6_voies_etude',header,BLACK))
    for i in range(6):parts.append((f'J2_broche_{i+1}',box(.64,.64,7,(24.1,-8.35+i*2.54,1.62)),GOLD))
    text_shape('V3 2S SUPERVISION',1.4,(0,13.0,1.66),WHITE,parts,'Titre_carte_V3')
    text_shape('ETUDE - NON TESTEE',.95,(2,-13,1.66),WHITE,parts,'Statut_carte')
    m=item('surveillance-2s','surveillance-2s-v3-concept-detaille.step','V3 | supervision 2S analogique - CONCEPT',parts,
        ['TLV6700 DDC: corps nominal 2.9x1.6 mm, reference/hysteresis dans PDF TI',
         'Composants reels proposes; pas de microcontroleur de commande ajoute'],
        ['Carte propre au projet, non fabriquee: aucune photographie de carte commerciale',
         'Implantation, connecteurs et hauteurs de certains boitiers approximatifs',
         'Pistes visibles illustratives: pas un routage valide, pas de Gerber ni plan CNC',
         'Les valences/marquages sont des annotations CAO, pas une copie de codes fabricant'],
        dict(project_board_mm=[54,32,1.6],holes_diameter_mm=2.2,holes_centres_mm=[48,26],
             domains='Cell1 B0/B1; Cell2 B1/B2; logic B0/3.3V',manufacturing_ready=False),True)
    m['source_pages']=['TI TLV6700 PDF3,5; Vishay VOS618A PDF7; project integration.md']
    return m

def ssr():
    parts=[];W,L,H=44.5,57.3,22.6
    base=box(W,L,1.8,fillet=1.0)
    for y in (-23.8,23.8):base=base.cut(cyl(2.45,2,-.1,0,y))
    base=base.cut(box(4.9,5.1,2,(0,-27,-.1)))
    parts.append(('Semelle_aluminium_cotes_nominales',base,STEEL))
    body=box(W,L,17.0,(0,0,1.8),1.1)
    for y in (-27.2,27.2):body=body.cut(cyl(5.9,18,1.7,0,y))
    for x in (-13.95,13.95):
        for y in (-21.6,21.6):body=body.cut(box(11,11,6,(x,y,14.2),.5))
    parts.append(('Coque_noire_exterieure_estimee',body,BLACK))
    for i,(x,y,big) in enumerate([(-13.95,21.6,True),(13.95,21.6,True),(-12.7,-21.6,False),(12.7,-21.6,False)],1):
        radius=2.083 if big else 1.753
        plate=box(10,9.5,1.2,(x,y,17.9),.2).cut(cyl(radius,1.4,17.8,x,y))
        parts.append((f'Borne_{i}_plaque_metal',plate,STEEL))
        parts.append((f'Borne_{i}_rondelle',ring(4.6 if big else 4.1,radius, .60,19.1).translate((x,y,0)),STEEL))
        screw=cyl(radius,5.5,15.0,x,y).fuse(cyl(4.25 if big else 3.8,2.5,20.1,x,y))
        for angle in (0,90):
            cut=box(6,.85,.9,(x,y,21.8)).rotate((x,y,0),(x,y,1),angle)
            screw=screw.cut(cut)
        parts.append((f'Borne_{i}_vis_UNC_empreinte_estimee',screw,STEEL))
        for dx in (-5.3,5.3):parts.append((f'Borne_{i}_barriere_{dx}',box(.5,10,4.2,(x+dx,y,15)),BLACK))
    parts.append(('Etiquette_fond_blanc',box(36.5,29.2,.05,(0,0,18.82),.4),WHITE))
    for name,txt,size,y in [('Logo','crydom',4.3,7.4),('Type','D1D100',3.2,1.6),('Fonction','SOLID STATE RELAY',1.65,-2.8),('Output','1-72 VDC / 100 A*',1.55,-6.0),('Input','INPUT 3.5-32 VDC',1.55,-9.2)]:text_shape(txt,size,(0,y,18.90),BLACK,parts,name+'_texte_approche')
    for txt,x,y in [('1 OUTPUT',-10,14),('+2',14,14),('4 INPUT',-10,-14),('+3',14,-14)]:text_shape(txt,1.3,(x,y,18.85),WHITE,parts,'Repere_'+txt.replace(' ','_'))
    m=item('coupure-moteurs','crydom-d1d100-exterieur-detaille.step','Crydom D1D100 | exterieur reconstruit',parts,
        ['Sensata PDF3: largeur44.5, longueur57.3, hauteur22.6, trous/slot4.9, entraxe47.6; tolerance0.5mm',
         'Sensata PDF2: vis entree #6-32 UNC et sortie #8-32 UNC; semelle aluminium'],
        ['Moulage, barriers, rondelles, tete de vis et etiquette reconstruits: cotes locales estimees',
         'Pas de circuit interne, dissipateur ou capot KS101 supposes inclus',
         'Pas de garantie de courant depuis la CAO; qualification thermique et dissipateur a definir'],
        dict(nominal_envelope_mm=[W,L,H],mounting_hole_diameter_mm=4.9,mounting_centres_mm=47.6,
             screws='UNC #6-32 input / #8-32 output; threads not modeled',heatsink_included=False))
    m['source_pages']=['Sensata-Crydom-1-DC-D1D100-datasheet.pdf PDF1-4']
    return m

def native():
    folder='interrupteur-pi';path=BASE/folder/'3D/pololu-2813-officiel.step'
    assets=json.loads((BASE/folder/'assets.json').read_text(encoding='utf-8'))['assets']
    a=next(a for a in assets if a['file']=='3D/'+path.name);assert sha(path)==a['sha256']
    doc=read_xcaf(path);leaves,whole,ct,roots,ncolors=collect_leaves(doc);assert whole.isValid()
    meshes=[]
    for name,placed,color,raw in leaves:
        BRepTools.Clean_s(placed.wrapped);BRepMesh_IncrementalMesh(placed.wrapped,.012,False,.1,True)
        for original,face in zip(cq.Shape.cast(raw).Faces(),placed.Faces()):
            col=Quantity_Color();fc=color
            for kind in (XCAFDoc_ColorSurf,XCAFDoc_ColorGen):
                if ct.GetColor(original.wrapped,kind,col):fc=(col.Red(),col.Green(),col.Blue());break
            vs,tri=face.tessellate(.012,.1);assert tri
            c=np.array(fc);c=np.where(c<=.0031308,12.92*c,1.055*np.power(c,1/2.4)-.055)
            meshes.append((np.array([v.toTuple() for v in vs]),tri,c))
    p=path.with_suffix('.png');render_meshes(p,meshes,(.5,-.7,1.1),'Pololu 2813 HP | CAO constructeur commune MP/HP','STEP constructeur inchange - revision et composants reels a verifier')
    bb=whole.BoundingBox()
    meta=dict(file=path.name,title='Pololu 2813 HP - CAO officielle commune',unit='mm',bytes=path.stat().st_size,
        sha256=sha(path),source_url=a['url'],native_vendor_cad=True,geometry_modified=False,
        hardware_measured=False,family_model='2812 MP / 2813 HP',generated_on='2026-10-13',
        preview=dict(file=p.name,sha256=sha(p)),bounds_mm={k:getattr(bb,k) for k in ['xmin','xmax','ymin','ymax','zmin','zmax']},
        validation=dict(valid_after_reimport=True,solids=len(whole.Solids()),faces=len(whole.Faces()),xcaf_colors=ncolors),
        estimates_and_limitations=['Modele commun constructeur; revision recue et accessoires a verifier',
          'Modele fusionnant plusieurs materiaux: masse physique non deduite du volume'],manufacturer_copyright='Pololu Corporation; no separate redistribution licence identified')
    path.with_suffix('.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return folder,meta

def main():
    sys.stdout.reconfigure(encoding='utf-8');results=[]
    for build in (supervisor,ssr):
        m=build();meta=export_model(m);folder=m['folder'].split('/')[-1]
        meta['coordinate_system']='Centre X/Y; bas du PCB ou de la semelle z=0'
        meta['generator']='tools/build_battery_protection_step.py';meta['generator_sha256']=sha(Path(__file__))
        (BASE/folder/'3D'/Path(meta['file']).with_suffix('.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        results.append((folder,meta))
    results.insert(1,native())
    for folder,meta in results:
        out=BASE/folder/'3D'
        manifest=dict(generator='tools/build_battery_protection_step.py',generator_sha256=sha(Path(__file__)),
            generated_on='2026-10-13',models=[meta],source_assets='../assets.json')
        (out/'provenance.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (out/'README.md').write_text('# Modele 3D\n\n'+f'[{meta["file"]}]({meta["file"]}) | [Apercu]({meta["preview"]["file"]})\n\n'+
            'Modele officiel inchange pour le Pololu. La surveillance est une conception V3 non fabriquee; le relais est une reconstruction exterieure. Les estimations sont dans le JSON voisin.\n\n'+
            '[Provenance](provenance.json), [validation FreeCAD](../../3D/validation-freecad.json), [fiche](../README.md).\n',encoding='utf-8')
    out=BASE/'3D';out.mkdir(exist_ok=True)
    (out/'catalogue.json').write_text(json.dumps(dict(model_count=3,models=[dict(folder='protection-batterie/'+f,**m) for f,m in results]),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    gallery=Image.new('RGB',(1600,960),'white');draw=ImageDraw.Draw(gallery)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',25)
    draw.text((30,14),'V3 | Surveillance 2S, interrupteur Pi, coupure moteurs - etude non testee',fill='#26333f',font=font)
    for n,(folder,m) in enumerate(results):
        im=Image.open(BASE/folder/'3D'/m['preview']['file']).convert('RGB');im.thumbnail((525,820))
        gallery.paste(im,(n*533+(533-im.width)//2,65))
    gallery.save(out/'apercu-protection.png')
    (out/'README.md').write_text('# CAO de la protection batterie\n\nTrois STEP, trois echelles distinctes. [Vue d ensemble](apercu-protection.png).\n\n'+
      '\n'.join(f'- [{m["title"]}](../{f}/3D/{m["file"]})' for f,m in results)+
      '\n\n[Catalogue](catalogue.json), [validation FreeCAD](validation-freecad.json), [architecture](../integration.md).\n\n'+
      'La carte de surveillance est une etude mecanique, pas une carte du commerce ni un PCB pret a fabriquer. Aucun circuit secteur interne invente.\n',encoding='utf-8')
    print('DONE',len(results),'STEP models',flush=True)

if __name__=='__main__':main()
