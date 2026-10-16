"""Promote validated CAD viewing artifacts; keep original exports archived."""
from pathlib import Path
import json,hashlib,zipfile
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'Assemblage';BUILD=OUT/'preparation';TEMP=ROOT/'tools/temp/assemblage-viewers'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    prep=read(BUILD/'preparation.json');fc=read(BUILD/'validation-freecad.json');glb=read(BUILD/'validation-glb.json')
    fast=read(BUILD/'validation-affichage-freecad.json')
    assert fast['all_passed'] and sha(BUILD/fast['file'])==fast['sha256']
    assert fc['all_passed'] and glb['all_passed'] and fc['native_solids']==5441
    engines=[]
    for name in ['structure','roulage','electronique','puissance','complet-detaille']:
        row=read(BUILD/('cad-viewer-'+name+'.json'))
        path=BUILD/('drone-v3-'+name+'.step')
        assert row['success'] and row['meshes'] and row['sha256']==sha(path)
        engines.append({**row,'file':path.name})
    assert sha(BUILD/prep['native']['file'])==prep['native']['sha256']
    archive_rows=read(BUILD/'archives.json')
    for row in archive_rows:
        p=BUILD/row['file'];assert sha(p)==row['sha256']
        with zipfile.ZipFile(p) as z:assert z.testzip() is None
    old=read(OUT/'provenance.json')
    model_rows=[]
    for name in ['structure','roulage','electronique','puissance','complet-detaille']:
        p=BUILD/('drone-v3-'+name+'.step')
        model_rows.append(dict(file=p.name,bytes=p.stat().st_size,sha256=sha(p),representation='Visualisation optimisée ; détails complets dans le FCStd'))
    # Keep the single large history ZIP locally, and publish the same original
    # bytes as two standard ZIPs below the per-file GitHub size limit.
    (OUT/'sources-step-detaillees-originales.zip').replace(TEMP/'source-archive-all-five.zip')
    for row in archive_rows:(BUILD/row['file']).replace(OUT/row['file'])
    prep['archive']=archive_rows[0];prep['original_full_step_archive']=archive_rows[1]
    prep['fast_freecad_display']=fast
    (BUILD/'preparation.json').write_text(json.dumps(prep,ensure_ascii=False,indent=2),encoding='utf-8')
    viewer_report=dict(all_passed=True,engine=engines[0]['engine'],models=engines,scope='Actual bundled STEP parser exercised. GUI display checked separately where recorded; not inferred from parser success.')
    viewer_report['actual_app_test']=read(BUILD/'validation-cad-viewer-gui.json')
    assert viewer_report['actual_app_test']['all_passed']
    (BUILD/'validation-cad-viewer.json').write_text(json.dumps(viewer_report,ensure_ascii=False,indent=2),encoding='utf-8')
    names=[r['file'] for r in model_rows]+[prep['native']['file']]+[r['file'] for r in glb['models']]
    names+=[fast['file'],'validation-affichage-freecad.json','preparation.json','validation-freecad.json','validation-glb.json','validation-cad-viewer.json','validation-cad-viewer-gui.json']
    names += [p.name for p in BUILD.glob('apercu-assemblage-*.png')]
    names += [p.name for p in BUILD.glob('apercu-freecad-*.png')]
    for name in names:(BUILD/name).replace(OUT/name)
    old['revision']='A2-R2 - compatibilité CAD Viewer et FreeCAD natif'
    if 'generator_sha256' in old:old['original_generator_sha256']=old.pop('generator_sha256')
    old['models']=model_rows;old['native_model']=prep['native'];old['original_step_archives']=archive_rows
    old['fast_freecad_display']=fast
    old['complete_native_geometry_retained']=True;old['view_step_simplifications']=prep['step_preview_simplifications']
    old['generation_scripts_sha256']={name:sha(ROOT/'tools'/name) for name in ['prepare_vehicle_viewers.py','transfer_vehicle_components.py','finish_vehicle_native.py','compact_vehicle_previews.py','build_vehicle_fast_freecad.py','merge_vehicle_glb.py','build_vehicle_light_steps.py','check_light_vehicle_steps.py','check_vehicle_viewers.py','check_vehicle_glb.py','check_cad_viewer.cjs','run_freecad_job.py']}
    (OUT/'provenance.json').write_text(json.dumps(old,ensure_ascii=False,indent=2),encoding='utf-8')
    native_mb=prep['native']['bytes']/1e6;glb_mb=prep['full_glb']['bytes']/1e6
    rows='\n'.join('| '+r['file']+' | '+f"{r['bytes']/1e6:.1f}"+' Mo |' for r in model_rows)
    text=f'''# Drone V3 — assemblage A2-R2

Pour ouvrir et examiner tout le robot dans FreeCAD, utiliser **[la version d'affichage rapide](drone-v3-complet-affichage-rapide.FCStd)** ({fast['bytes']/1e6:.1f} Mo). Réouverture mesurée dans l'application : **{fast['gui_open_seconds']:.1f} secondes**. Elle conserve toutes les surfaces détaillées et leurs couleurs sous forme de **2 342 728 triangles**, calculés depuis la géométrie complète à 0,18 mm / 0,35 rad. Cette version est une visualisation maillée.

Pour la géométrie CAO exacte, ouvrir **[le document natif FreeCAD ultra détaillé](drone-v3-complet-ultra-detaille.FCStd)** ({native_mb:.1f} Mo) directement avec **Fichier → Ouvrir**. Il conserve les **5 441 solides** et toutes les faces des modèles détaillés, regroupés en **{prep['native']['features']} objets** dans quatre sous-ensembles. Couleurs conservées, affichage ombré, cadrage isométrique enregistré. Réouverture mesurée : **{fc['native_load_seconds']/60:.1f} minutes**. Il s'agit de géométrie importée, sans historique de conception paramétrique.

Pour VS Code / CAD Viewer, privilégier **[l'aperçu complet détaillé GLB](drone-v3-complet-ultra-detaille.glb)** ({glb_mb:.1f} Mo). Ses surfaces proviennent de la géométrie complète ; discrétisation à 0,18 mm / 0,35 rad, unités glTF en mètres et axe vertical Y. Il sert à visualiser, sans remplacer le BREP pour la fabrication.

**Fermer puis rouvrir les anciens onglets CAD Viewer** après remplacement des fichiers : un onglet déjà chargé peut garder l'ancienne version. Ouvrir un seul assemblage complet à la fois. Dans FreeCAD, les groupes Structure, Roulage, Electronique et Puissance peuvent être masqués séparément.

## Les cinq STEP pour visualisation

Ces cinq fichiers sont des **vues d'implantation légères A2-R1**, avec formes simples et volumes réservés : **225 solides** au total. Ils conservent les noms de fichiers et le repère du véhicule. Les dimensions générales et le placement d'étude viennent du modèle léger du châssis. Les interfaces fines, dentures, pneus sculptés, circuits et faisceaux détaillés se trouvent dans les versions FreeCAD et GLB complètes. Les STEP d'implantation servent à ouvrir rapidement l'ensemble dans CAD Viewer ; leurs formes simplifiées ne qualifient pas les interfaces mécaniques ni les jeux locaux.

| Fichier | Taille |
| --- | --- |
{rows}

Sous-ensembles : [structure](drone-v3-structure.step), [roulage](drone-v3-roulage.step), [électronique](drone-v3-electronique.step), [puissance](drone-v3-puissance.step). [Assemblage STEP complet optimisé](drone-v3-complet-detaille.step). Ne pas superposer les quatre sous-ensembles au complet : cela doublerait les pièces.

Les [GLB de structure](drone-v3-structure.glb), [roulage](drone-v3-roulage.glb), [électronique](drone-v3-electronique.glb) et [puissance](drone-v3-puissance.glb) sont également disponibles, avec les détails de surface.

## Vérifications et origine du blocage

Les journaux locaux de CAD Viewer 1.5.7 indiquaient `RangeError: Invalid array length` pendant la transmission des anciens STEP de 359 et 293 Mo à la webview, avant même leur lecture par le moteur CAO. Le test précédent de validité géométrique ne vérifiait pas cette étape d'ouverture.

Le [rapport FreeCAD](validation-freecad.json) contrôle la réouverture du FCStd, les couleurs, les formes fermées/valides, le cadrage enregistré et les cinq STEP. Le [rapport CAD Viewer](validation-cad-viewer.json) teste les cinq STEP avec le moteur WebAssembly livré dans l'extension installée. L'[essai dans VS Code](validation-cad-viewer-gui.json) confirme le signal `modelLoaded` pour une copie identique du STEP complet léger. Le [contrôle GLB](validation-glb.json) vérifie les buffers, indices, nombres de triangles et encombrements. Les deux versions natives ont été ouvertes dans l'application FreeCAD installée et leurs vues exportées ; le contrôle de l'affichage rapide conserve les temps et nombres de triangles mesurés.

[Vue FreeCAD isométrique](apercu-freecad-isometrique.png) · [Vue FreeCAD de dessus](apercu-freecad-dessus.png) · [Contrôle de l'affichage rapide](validation-affichage-freecad.json) · [Provenance](provenance.json) · [Préparation](preparation.json).

Les quatre STEP détaillés d'origine et leurs rapports sont conservés dans [cette archive](sources-step-detaillees-originales.zip) ; le grand STEP complet d'origine est dans [cette seconde archive](sources-step-complet-original.zip). Les sources individuelles des composants et les plans du châssis ne sont pas modifiés.

## Limites de l'assemblage

La batterie G1, les supports de fusibles révisés, les EVM TI et le Pololu 2831 sans modèle exact gardent leurs volumes réservés. Les anciens modèles Zeee/MIDI/ATO ne sont pas réintroduits. Les axes définitifs, paliers adaptés, carters, cinématique et visserie restent à finaliser. Les câbles des composants gardent une pose illustrative : le faisceau n'est pas entièrement raccordé. Les interférences de l'assemblage détaillé et l'ajustement physique ne sont pas qualifiés.
'''
    (OUT/'README.md').write_text(text,encoding='utf-8')
    print('PUBLISHED',len(model_rows),'STEP;',native_mb,'Mo FCStd;',glb_mb,'Mo GLB')
if __name__=='__main__':main()
