"""Preserve vendor STEP; create placed derivatives, two pad variants and an assembly."""
from pathlib import Path
import json, sys, hashlib
import cadquery as cq
import numpy as np
from prepare_pi5_step import read_xcaf,collect_leaves
from build_running_gear_step import export_model,box,cyl
from build_battery_protection_step import ssr
from render_step_meshes import render_meshes

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'Composants/dissipateur-relais'
OUT=BASE/'3D'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,data):p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def model(name,title,parts,params,limits,published):
    return dict(folder='dissipateur-relais',filename=name,title=title,parts=parts,
        params=params,estimated=limits,published=published,view=(.5,-1,.8),design=False,
        probes=[],source_pages=['Sensata HS251 STEP et fiche PDF 2024 p.2',
            'Sensata HSP fiche 2018 p.1 / PCN-SSR-231214 / annexe TTI',
            'D1D100 modele exterieur existant et fiche PDF p.3'])
def pad(thickness):
    p=box(57.1,44.2,thickness)
    for sign in (-1,1):
        p=p.cut(cyl(2.415,thickness+.2,-.1,sign*23.75,0))
        p=p.cut(box(6,4.83,thickness+.2,(sign*26.75,0,-.1)))
    return p.clean()
def finish(meta):
    meta['generator']='tools/build_heatsink_step.py'
    meta['generator_sha256']=sha(Path(__file__))
    meta['coordinate_system']='X largeur et entraxe SSR; Y longueur; Z normal au contact. Face SSR du dissipateur Z=40.640 mm; centre des trous Y=0.'
    save(OUT/Path(meta['file']).with_suffix('.json'),meta)
    return meta

def main():
    sys.stdout.reconfigure(encoding='utf-8');OUT.mkdir(parents=True,exist_ok=True)
    source=OUT/'sensata-hs251-officiel.step';digest=sha(source)
    doc=read_xcaf(source);leaves,whole,ct,roots,colors=collect_leaves(doc)
    assert whole.isValid() and len(whole.Solids())==1
    bb=whole.BoundingBox()
    native=dict(file=source.name,title='HS251 | STEP officiel inchange',unit='mm',sha256=digest,bytes=source.stat().st_size,
        native_vendor_cad=True,geometry_modified=False,hardware_measured=False,
        coordinate_system='Repere fabricant; contact SSR normal +Y. Voir modele implantation pour repere V3.',
        source_url='https://www.sensata.com.cn/sites/default/files/a/sensata-hs251-heatsink-accessories-drawing.step',
        bounds_mm={k:getattr(bb,k) for k in ['xmin','xmax','ymin','ymax','zmin','zmax']},
        validation=dict(valid_after_reimport=True,solids=len(whole.Solids()),faces=len(whole.Faces()),xcaf_colors=colors),
        estimates_and_limitations=['Modele officiel: filetages representes par alesages, pas helices physiques.',
            'Corps et pattes regroupes dans un solide officiel; ni vis de montage ni pad.',
            'Ne reproduit pas rugosite, rayures ou tolerance de la piece recue.'],
        manufacturer_copyright='Sensata Technologies / Crydom; aucune licence de redistribution distincte identifiee')
    meshes=[]
    placed=[]
    for n,s,c,raw in leaves:
        normalized=s.rotate((0,0,0),(1,0,0),90).translate((0,26.162,21.082))
        placed.append(('HS251_geometrie_officielle',normalized,c))
        vs,ts=normalized.tessellate(.025,.1);col=np.array(c)
        col=np.where(col<=.0031308,12.92*col,1.055*col**(1/2.4)-.055)
        meshes.append((np.array([v.toTuple() for v in vs]),ts,col))
    render_meshes(OUT/'sensata-hs251-officiel.png',meshes,(.5,-1,.8),'Sensata HS251 | geometrie officielle','Apercu tourne pour lisibilite; fichier STEP original inchange')
    native['preview']=dict(file='sensata-hs251-officiel.png',sha256=sha(OUT/'sensata-hs251-officiel.png'))
    save(source.with_suffix('.json'),native)
    results=[native]
    sink=cq.Compound.makeCompound([s for n,s,c in placed])
    for x in (-23.8125,23.8125):assert not sink.isInside(cq.Vector(x,0,39.5),1e-5)
    m=model('sensata-hs251-implantation-v3.step','HS251 | implantation V3',placed,
        dict(envelope_with_tabs_mm=[85.344,52.324,40.640],ssr_hole_centres_mm=47.625,ssr_mount_face_z_mm=40.640,
            transformation='rotate X +90 deg; translate [0,26.162,21.082] mm'),
        native['estimates_and_limitations'],['Geometrie et couleur issues du STEP constructeur sans modification de forme.'])
    meta=finish(export_model(m));meta['derived_from']=dict(file=source.name,sha256=digest,geometry_changes='rotation et translation seulement')
    save(OUT/Path(meta['file']).with_suffix('.json'),meta);results.append(meta)
    linear=lambda col:tuple((v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4) for v in col)
    for variant,t,col in [('gris-2018',.076,linear((.67,.69,.70))),('rose-pcn-2023',.127,linear((.91,.53,.65)))]:
        shape=pad(t)
        m=model('sensata-hsp1-'+variant+'.step','HSP-1 | '+variant,[(variant,shape,col)],
            dict(outline_mm=[57.1,44.2],thickness_mm=t,notches_centre_mm=47.5,notch_width_mm=4.83),
            ['Reconstruction du contour 2018: dimensions arrondies, rayons de coins non cotes non ajoutes.',
             'Le contour de la version rose est suppose identique au plan 2018; lot reel a verifier.',
             'Aucun film protecteur, compression ni texture microscopique represente.',
             'Le plan 2011 donne 57.2x44.5 et 47.8; revisions conservees dans notices, pas melangees.'],
            ['Contour et epaisseur gris selon fiche 2018; rose 0.127 mm selon annexe preliminaire du PCN 2023.'])
        meta=finish(export_model(m));meta['coordinate_system']='Centre X/Y; bas du pad Z=0; encoche selon X.'
        save(OUT/Path(meta['file']).with_suffix('.json'),meta);results.append(meta)
    relay=ssr()['parts']
    relay_placed=[('D1D100_'+n,s.rotate((0,0,0),(0,0,1),90).translate((0,0,40.767)),c) for n,s,c in relay]
    pink=pad(.127).translate((0,0,40.640))
    relay_compound=cq.Compound.makeCompound([s for n,s,c in relay_placed])
    overlap=sink.intersect(relay_compound).Volume()
    assert overlap<1e-6,overlap
    assert sink.intersect(pink).Volume()<1e-6
    assert relay_compound.intersect(pink).Volume()<1e-6
    parts=placed+[('HSP1_rose_sans_films',pink,linear((.91,.53,.65)))]+relay_placed
    m=model('assemblage-d1d100-hs251-hsp1-etude.step','D1D100 + HS251 + HSP-1 | assemblage etude',parts,
        dict(sink_face_z_mm=40.640,pad_uncompressed_mm=.127,relay_bottom_z_mm=40.767,
            sink_holes_x_mm=[-23.8125,23.8125],relay_holes_x_mm=[-23.8,23.8],centre_offset_each_mm=.0125),
        ['Implantation CAO seulement; aucune qualification thermique ou sur piece physique.',
         'Relais: reconstruction exterieure existante; aucune electronique interne inventee.',
         'Pad rose: contour 2018 suppose; vis HK1 et fixation chassis absentes de cet assemblage.',
         'Orientation 3D choisie pour integration; convection a verifier, ailettes verticales recommandees.'],
        ['HS251: STEP officiel; D1D100: enveloppe nominale et entraxe 47.6 mm.'])
    meta=finish(export_model(m));meta['assembly_checks']=dict(no_volume_overlap=True,relay_heatsink_overlap_mm3=overlap,
        thermal_layer_gap_mm=0,matching_nominal_holes_offset_each_mm=.0125,physical_fit_tested=False)
    save(OUT/Path(meta['file']).with_suffix('.json'),meta);results.append(meta)
    assert sha(source)==digest
    save(OUT/'catalogue.json',dict(model_count=len(results),models=results,source_assets='../assets.json'))
    save(OUT/'provenance.json',dict(generator='tools/build_heatsink_step.py',generator_sha256=sha(Path(__file__)),
        original_preserved=True,original_sha256=digest,models=results))
    print('DONE',len(results),'models',flush=True)
if __name__=='__main__':main()
