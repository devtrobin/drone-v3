"""Preserve official nVent geometry; export colored, placed and exploded derivatives."""
from pathlib import Path
import json,sys,hashlib,itertools
import cadquery as cq
import numpy as np
from prepare_pi5_step import read_xcaf,collect_leaves
from OCP.BRepBndLib import BRepBndLib
from OCP.Bnd import Bnd_Box
from render_step_meshes import render_meshes
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/repartition-moteurs';OUT=BASE/'3D'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def optimal(s):
    b=Bnd_Box();BRepBndLib.AddOptimal_s(s.wrapped,b,False,False)
    return dict(zip(['xmin','ymin','zmin','xmax','ymax','zmax'],b.Get()))
def norm(s):return s.rotate((0,0,0),(1,1,1),120).translate((-2.503300298258181,3.2138897826143875,24.30238986322877))
def preview(p,parts,title,view=(.7,-1,.85)):
    meshes=[]
    for n,s,c in parts:
        vs,ts=s.tessellate(.03,.12);col=np.array(c);col=np.where(col<=.0031308,12.92*col,1.055*col**(1/2.4)-.055)
        meshes.append((np.array([v.toTuple() for v in vs]),ts,col))
    render_meshes(p,meshes,view,title,'Geometrie officielle nVent - implantation V3 - mm - voir provenance')
def export(file,title,parts,limits,params):
    overlaps=[]
    for (an,a,ac),(bn,b,bc) in itertools.combinations(parts,2):
        v=a.intersect(b).Volume()
        if v>1e-5:overlaps.append(dict(a=an,b=bn,volume_mm3=v))
    # Record vendor assembly intersections without altering official surfaces.
    m=dict(folder='repartition-moteurs',filename=file,title=title,parts=parts,params=params,estimated=limits,
        published=['UD80A569010: nominal69x30x46mm; montage54mm/slot4.5mm selonIP7802.'],
        probes=[],view=(.7,-1,.85),design=False,source_pages=['STEPAP214 fabricant viaTraceParts, E10106602.step','nVent IP7802_M, p1-2; fiche2023 p2-3'])
    print('EXPORT',file,flush=True)
    assembly=cq.Assembly(name=Path(file).stem)
    for n,s,c in parts:assert s.isValid();assembly.add(s,name=n,color=cq.Color(*c))
    candidate=OUT/(file+'.candidate');assembly.export(str(candidate),exportType='STEP',mode='default',unit='MM',outputUnit='MM')
    before=cq.Compound.makeCompound([s for n,s,c in parts]);after=cq.importers.importStep(str(candidate)).val()
    vb=before.Volume(tol=1e-9);va=after.Volume(tol=1e-9);drift=abs(va-vb)/vb
    ob=optimal(before);oa=optimal(after);bboxerr=max(abs(ob[k]-oa[k]) for k in ob)
    assert after.isValid() and len(after.Solids())==len(before.Solids()) and drift<1e-4 and bboxerr<.01,(file,drift,bboxerr)
    candidate.replace(OUT/file);preview(OUT/Path(file).with_suffix('.png'),parts,title)
    meta=dict(file=file,title=title,unit='mm',bytes=(OUT/file).stat().st_size,sha256=sha(OUT/file),hardware_measured=False,
        parameters=params,estimates_and_limitations=limits,bounds_mm=oa,preview=dict(file=Path(file).with_suffix('.png').name,sha256=sha(OUT/Path(file).with_suffix('.png'))),
        validation=dict(valid_after_reimport=True,solids=len(after.Solids()),faces=len(after.Faces()),volume_relative_error=drift,
            volume_before_mm3=vb,volume_after_mm3=va,bbox_error_mm=bboxerr,bbox_method='BRepBndLib.AddOptimal, no triangulation, no shape tolerance',bbox_error_limit_mm=.01),
        parts=[dict(name=n,color_linear_rgb=c) for n,s,c in parts])
    meta.update(generated_on='2026-10-14',native_vendor_cad=True,geometry_source='eriflex-ud80a-officiel.step',
        original_sha256=sha(OUT/'eriflex-ud80a-officiel.step'),generator='tools/build_motor_splitter_step.py',generator_sha256=sha(Path(__file__)),
        shape_modifications='rotation and translation only; appearance and part labels for derivatives',
        coordinate_system='V3:X largeur,Y longueur de fixation,Z profondeur depuis plan arriere; transformation rotation(1,1,1)+120deg et translation indiquee.',
        appearance_note='Capot reel bleu transparent; derive exporte bleu opaque pour lisibilite. Original conserve ses styles fabricant.')
    meta['validation']['pairwise_material_overlaps']=overlaps
    save(OUT/Path(file).with_suffix('.json'),meta);return meta
def main():
    sys.stdout.reconfigure(encoding='utf-8');source=OUT/'eriflex-ud80a-officiel.step';digest=sha(source)
    doc=read_xcaf(source);leaves,whole,ct,roots,colors=collect_leaves(doc);assert whole.isValid() and len(whole.Solids())==3
    solids=whole.Solids();bb=optimal(whole);print('VENDOR',len(solids),'solids',len(whole.Faces()),'faces',colors,'colors',flush=True)
    # Bounds identify the hinged front cover independently from file entity order.
    rawcap=next(s for s in solids if s.BoundingBox().ymin>15);rawbus=next(s for s in solids if s.BoundingBox().xlen<20)
    rawbody=next(s for s in solids if s.BoundingBox().xlen>60)
    cap=norm(rawcap);bus=norm(rawbus);body=norm(rawbody)
    parts=[('Socle_clip_et_formes_officielles',body,(.83,.84,.80)),('Capot_bleu_geometrie_officielle',cap,(.018,.16,.31)),('Bloc_conducteur_geometrie_officielle',bus,(.62,.65,.67))]
    native=dict(file=source.name,title='UD80A : STEP officiel intact',unit='mm',sha256=digest,bytes=source.stat().st_size,
        native_vendor_cad=True,geometry_modified=False,hardware_measured=False,
        source_url='https://noproxy-download.nvent.com/api/traceparts/download?part_number=UD-80A&format=19&brand=ERIFLEX',
        archive_entry='E10106602.step',coordinate_system='Repere natif:X hauteur fabricant,Y profondeur,Z largeur; centre non nul.',
        bounds_mm=bb,
        validation=dict(valid_after_reimport=True,solids=len(solids),faces=len(whole.Faces()),xcaf_colors=colors),
        estimates_and_limitations=['Modele fabricant pour implantation; ne remplace pas plans de fabrication ni mesure du lot.',
            'Enveloppe CAO69.0372x46.23749x30.0482 differe legerement du nominal69x46x30mm.',
            'Trois solides seulement; vis et details internes non tous disponibles comme pieces separees.',
            'Pas de fils, embouts ou vis de fixation au chassis fournis dans cette CAO.'])
    preview(source.with_suffix('.png'),parts,native['title']);native['preview']=dict(file=source.with_suffix('.png').name,sha256=sha(source.with_suffix('.png')))
    save(source.with_suffix('.json'),native);results=[native]
    params=dict(nominal_H_W_D_mm=[69,30,46],CAD_placed_X_Y_Z_mm=[30.0482002,69.0372,46.23749018],mount_pitch_mm=54,
        slot_width_published_mm=4.5,transformation='rotateaxis[1,1,1]+120deg; translate[-2.5033002983,3.2138897826,24.3023898632]mm')
    limits=native['estimates_and_limitations']+['Couleurs derivatives choisies pour lecture; teinte exacte et transparence non garanties.',
        'Fils et embouts absents; affectationV3 ne represente pas un faisceau teste.']
    results.append(export('eriflex-ud80a-implantation-v3.step','UD80A : implantation V3',parts,limits,params))
    results.append(export('eriflex-ud80a-sans-capot.step','UD80A : capot retire', [parts[0],parts[2]],limits,params))
    exploded=[parts[0],(parts[1][0],cap.translate((0,0,22)),parts[1][2]),parts[2]]
    results.append(export('eriflex-ud80a-vue-eclatee.step','UD80A : vue eclatee',exploded,limits+['CapottranslateZ+22mm: presentation, pas trajectoire mecanique de charniere.'],dict(params,cover_shift_z_mm=22)))
    results.append(export('eriflex-ud80a-capot-officiel.step','UD80A : capot seul',[parts[1]],limits,params))
    assert sha(source)==digest;save(OUT/'catalogue.json',dict(generated_on='2026-10-14',model_count=len(results),models=results,original_preserved=True))
    print('DONE',len(results),'STEP, original unchanged',flush=True)
if __name__=='__main__':main()
