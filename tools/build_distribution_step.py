"""MiniBus exterior reconstructions, with published interfaces and named estimates."""
from pathlib import Path
import cadquery as cq
from OCP.BRepTools import BRepTools
import json,sys,hashlib,itertools,math
from build_running_gear_step import box,cyl,ring,hexagon,export_model as shared_export
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/distribution-alimentation'
BLACK=(.012,.014,.017);METAL=(.65,.67,.69);CLEAR=(.78,.81,.82)
RED=(.65,.015,.012);INK=(.012,.012,.012)
STUDS=[-32.385,-10.795,10.795,32.385];MOUNTS=[-45.245,45.245]
THREAD_CHECK={}
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def text_solid(text,size,pos,depth=.06):
    return cq.Workplane('XY').text(text,size,depth,font='Arial',halign='center',valign='center',combine=False).val().translate(pos)
def flange_nut():
    flange=cyl(5.45,1.2,15.88)
    # Small radial serrations under the flange, reconstructed from photos.
    for a in range(0,360,20):
        cutter=box(3.0,.26,.14,(4.15,0,15.879)).rotate((0,0,0),(0,0,1),a)
        flange=flange.cut(cutter)
    top=hexagon(9.525,3.9,16.8)
    top=cq.Workplane('XY').newObject([top]).edges('#Z').chamfer(.26).val()
    result=flange.fuse(top).cut(cyl(2.48,5.1,15.78)).clean()
    return result
def helical_thread(d,length,pitch):
    # PipeShell smooth helical surfaces were silently lost in OCC booleans.
    # Ruled radial sections give a stable physical helix, with <=0.047mm
    # radial chord error at16 sections/turn. This is not a gauge geometry.
    depth=.54*pitch;ro=d/2;ri=ro-depth;start=-pitch;end=length+pitch
    steps=math.ceil((end-start)/pitch*16);wires=[]
    for j in range(steps+1):
        z=start+(end-start)*j/steps;a=2*math.pi*z/pitch
        pts=[cq.Vector(r*math.cos(a),r*math.sin(a),z+v) for r,v in
             [(ri-.04,-.38*pitch),(ro,-.065*pitch),(ro,.065*pitch),(ri-.04,.38*pitch)]]
        wires.append(cq.Wire.makePolygon(pts+[pts[0]]))
    ridge=cq.Solid.makeLoft(wires,True).intersect(box(6,6,length))
    core=cyl(ri+.015,length);overlap=core.intersect(ridge).Volume();assert overlap>1
    shape=core.fuse(ridge).clean();assert shape.isValid() and len(shape.Solids())==1
    assert shape.Volume()>core.Volume()+10 and len(shape.Faces())>100
    return shape
def bare():
    base=box(106.68,22.86,7.2,fillet=3.6)
    pedestal=box(81.6,16.8,6.70,(0,0,7.2),4.4)
    base=base.fuse(pedestal)
    # Recesses accept fixing screws. Bore diameter and counterbore are estimates.
    for x in MOUNTS:
        base=base.cut(cyl(2.75,7.4,-.1,x)).cut(cyl(5.5,2.8,4.6,x))
    # Shallow mould seam and underside relief, neither is a manufacturing datum.
    seam=box(106.8,23.0,.06,(0,0,6.8),3.6).cut(box(106.25,22.35,.1,(0,0,6.78),3.3))
    base=base.cut(seam)
    for x in [-26,-13,0,13,26]:
        base=base.cut(box(10.5,8.3,1.1,(x,0,-.05),.8))
    bus=box(78.74,12.7,1.98,(0,0,13.9),6.0)
    for x in STUDS:
        base=base.cut(cyl(2.413,7.1,7.0,x))
        bus=bus.cut(cyl(2.413,2.2,13.8,x))
    parts=[('Socle_noir_moule_reconstruction',base.clean(),BLACK),('Barre_cuivre_C110_etame_estimee',bus.clean(),METAL)]
    # #10-32 nominal diameter 4.826, pitch 25.4/32. Visible helix, simplified roots.
    stud=cyl(2.413,8.68,7.2).fuse(helical_thread(4.826,13.1,25.4/32).translate((0,0,15.88))).clean()
    samples=[stud.isInside(cq.Vector(2.2,0,22+j*(25.4/32)/16),1e-6) for j in range(16)]
    assert 0<sum(samples)<16 and len(stud.Faces())>100
    THREAD_CHECK.update(radius_mm=2.2,z_start_mm=22,z_step_mm=(25.4/32)/16,samples_occupied=samples,
                        sections_per_turn_minimum=16,maximum_radial_chord_error_mm=.047)
    nut=flange_nut()
    for i,x in enumerate(STUDS,1):
        parts.append((f'Goujon_10_32_UNF_{i}_longueur_estimee',stud.translate((x,0,0)),METAL))
        parts.append((f'Ecrou_flange_dentee_{i}_alesage_simplifie',nut.translate((x,0,0)),METAL))
    return parts
def cover():
    # Height is modelled at the manufacturer's MINIMUM; wiring can raise it.
    def rounded_wire(w,h,r,z):
        return cq.Workplane('XY').newObject([box(w,h,.1,fillet=r)]).faces('>Z').wires().val().translate((0,0,z-.1))
    outer=cq.Solid.makeLoft([rounded_wire(86.36,22,3,23.5),rounded_wire(83.6,19.7,2.7,31.75)],True)
    inner=cq.Solid.makeLoft([rounded_wire(83.9,19.5,2.5,23.3),rounded_wire(81.5,17.4,2.2,30.45)],True)
    cap=outer.cut(inner)
    for x in [-32.385,32.385]:
        sleeve=ring(7.1,6.15,12.6,18.0).translate((x,0,0))
        top_seat=ring(6.2,2.48,1.25,29.3).translate((x,0,0))
        cap=cap.fuse(sleeve).fuse(top_seat)
        # Decorative circular recess on the cover, not a fixing screw hole.
        cap=cap.cut(cyl(5.8,.17,31.60,x))
    logo=text_solid('BLUE SEA',3.1,(0,2.0,31.65),.13).fuse(text_solid('SYSTEMS',2.6,(0,-2.1,31.65),.13))
    cap=cap.cut(logo)
    # Rim and mould lines estimated; no claim of IP sealing.
    return cap.clean()
def item(folder,name,title,parts,params,limits,probes=None,design=False):
    return dict(folder='distribution-alimentation/'+folder if folder else 'distribution-alimentation',
        filename=name,title=title,parts=parts,params=params,published=[
            '2315: quatre goujons #10-32, bus commun, capot 2713 inclus.',
            'Plan constructeur: L106.68 W22.86; fixation90.49; goujons extremes64.77.',
            'Hauteur minimum avec capot31.75; cote verticale sans capot15.88 du plan.'],
        estimated=limits,view=(.5,-1,1.1),design=design,probes=probes or [],
        source_pages=['Plan JPG2315 officiel','Catalogue BlueSea2024: PDF p100','Photos Amazon.com ASINB000OTJ8A0'])
def export(m):
    for n,s,c in m['parts']:BRepTools.Clean_s(s.wrapped)
    # Check that mechanically assembled parts have no material overlap.
    intersections=[]
    for (na,a,ca),(nb,b,cb) in itertools.combinations(m['parts'],2):
        v=a.intersect(b).Volume()
        if v>1e-5:intersections.append(dict(a=na,b=nb,volume_mm3=v))
    assert not intersections,(m['filename'],intersections)
    meta=shared_export(m);meta['generated_on']='2026-10-14'
    meta['coordinate_system']='X longueur; Y largeur; Z vertical; centre XY du socle; dessous z=0. Assemblages: decalages explicites.'
    meta['validation']['pairwise_overlap_limit_mm3']=1e-5;meta['validation']['pairwise_material_overlaps']=intersections
    meta['validation']['visible_thread_verified']=any('Goujon' in n for n,s,c in m['parts'])
    meta['validation']['external_thread_validation']=THREAD_CHECK if meta['validation']['visible_thread_verified'] else None
    meta['appearance_note']='Polycarbonate transparent reel; teinte claire opaque dans cet export pour compatibilite. Aucun indice optique valide.'
    save(ROOT/'Composants'/m['folder']/'3D'/Path(meta['file']).with_suffix('.json'),meta)
    return dict(folder=m['folder'],**meta)
def main():
    sys.stdout.reconfigure(encoding='utf-8');models=[]
    bp=bare();cap=cover();cp=[('Capot_2713_PC_clair_affichage_opaque',cap,CLEAR)]
    params=dict(base_envelope_mm=[106.68,22.86],mount_pitch_mm=90.49,mount_bore_estimated_mm=5.5,
        stud_thread='#10-32 UNF',stud_diameter_mm=4.826,stud_pitch_mm=25.4/32,
        extreme_stud_pitch_mm=64.77,stud_centres_mm=STUDS,adjacent_stud_pitch_inferred_mm=21.59,
        closed_minimum_height_mm=31.75,bus_cross_section_estimated_mm=[12.7,1.98])
    limits=['Reconstruction, pas un STEP natif fabricant; dimensions non mesurees sur pieces.',
        'Hauteur31.75 est MINIMUM constructeur: ne garantit pas enveloppe maximum avec cosses.',
        'Diametres de fixation5.5 et lamages11, epaisseurs, contour du bus et visserie estimes.',
        'Filetages externes #10-32 UNF par sections reglees, erreur radiale de corde<=0.047mm; taraudages simplifies.',
        'Manchons, clips, parois, reliefs, rayons et logos du capot non cotes estimes.',
        'Cosses, cables, vis de chassis et fusibles de branches absents; implantation a terminer.',
        'Cote15.88 du plan utilisee comme dessus de barre pour reconstruction; interpretation interne non cotee.']
    models.append(export(item('bornier-2315','bluesea-2305-borniers-sans-capot-detaille.step','MiniBus 2315 | socle, bus et quatre goujons',bp,params,limits,
        probes=[dict(point=(MOUNTS[0],0,2),occupied=False),dict(point=(0,0,14.7),occupied=True)])))
    models.append(export(item('capot-2713','bluesea-2713-capot-detaille.step','2713 | capot de protection MiniBus',cp,params,limits)))
    models.append(export(item('bornier-2315','bluesea-2315-complet-detaille.step','MiniBus 2315 | ensemble ferme',bp+cp,params,limits)))
    exploded=bp+[(n,s.translate((0,0,19)),c) for n,s,c in cp]
    models.append(export(item('','bluesea-2315-vue-eclatee.step','MiniBus 2315 | vue eclatee',exploded,dict(params,cover_exploded_offset_mm=19),limits)))
    twin=[]
    # Independent rails, no bridge and no electrical jumpers represented.
    for prefix,y in [('POSITIF',-23),('NEGATIF',23)]:
        for n,s,c in bp+cp:twin.append((prefix+'_'+n,s.translate((0,y,0)),c))
        label=box(16,2.5,.03,(0,y-9.98,7.2))
        # Labels are a V3 proposal; factory parts are identical black units.
        twin.append((prefix+'_Etiquette_V3_ajoutee',label,RED if prefix=='POSITIF' else INK))
    models.append(export(item('','distribution-deux-minibus-2315-etude.step','V3 | deux MiniBus isoles, positif et negatif',twin,
        dict(params,rail_centres_y_mm=[-23,23],base_edge_gap_mm=23.14),limits+[
            'Decalage des rails46 et etiquettes rouge/noire: implantation de projet, pas un produit double vendu.',
            'Le socle est represente sans chassis. Encombrement de fils/cosses non valide.'],design=True)))
    save(BASE/'3D/catalogue.json',dict(generated_on='2026-10-14',unit='mm',models=models))
    print('DONE',len(models),'models',flush=True)
if __name__=='__main__':main()
