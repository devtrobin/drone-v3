<!-- complements-r3 -->
> [AssemblageR3 avec partie fixe du faisceau](R3/README.md). Les vues détailléesR1 et l’étudeR2 sont conservées ; R3 est une vue légère avec les ajouts. Les points extrêmes des câbles sont des approches, pas des raccordements fournisseur certifiés.
<!-- /complements-r3 -->

<!-- finalisation-r2 -->
> **Une étudeR2 distincte existe :** [assemblageR2](R2/README.md), [dossier de conception](../Composants/finalisation-theorique-r2/README.md). Les fichiers de cette page restentA2-R1 ; ils ne contiennent pas les corrections de direction/paliers/visserieR2.
<!-- /finalisation-r2 -->

# Drone V3 — assemblage A2-R2

Pour ouvrir et examiner tout le robot dans FreeCAD, utiliser **[la version d'affichage rapide](drone-v3-complet-affichage-rapide.FCStd)** (27.8 Mo). Réouverture mesurée dans l'application : **18.3 secondes**. Elle conserve toutes les surfaces détaillées et leurs couleurs sous forme de **2 342 728 triangles**, calculés depuis la géométrie complète à 0,18 mm / 0,35 rad. Cette version est une visualisation maillée.

Pour la géométrie CAO exacte, ouvrir **[le document natif FreeCAD ultra détaillé](drone-v3-complet-ultra-detaille.FCStd)** (27.2 Mo) directement avec **Fichier → Ouvrir**. Il conserve les **5 441 solides** et toutes les faces des modèles détaillés, regroupés en **194 objets** dans quatre sous-ensembles. Couleurs conservées, affichage ombré, cadrage isométrique enregistré. Réouverture mesurée : **3.7 minutes**. Il s'agit de géométrie importée, sans historique de conception paramétrique.

Pour VS Code / CAD Viewer, privilégier **[l'aperçu complet détaillé GLB](drone-v3-complet-ultra-detaille.glb)** (57.0 Mo). Ses surfaces proviennent de la géométrie complète ; discrétisation à 0,18 mm / 0,35 rad, unités glTF en mètres et axe vertical Y. Il sert à visualiser, sans remplacer le BREP pour la fabrication.

**Fermer puis rouvrir les anciens onglets CAD Viewer** après remplacement des fichiers : un onglet déjà chargé peut garder l'ancienne version. Ouvrir un seul assemblage complet à la fois. Dans FreeCAD, les groupes Structure, Roulage, Electronique et Puissance peuvent être masqués séparément.

## Les cinq STEP pour visualisation

Ces cinq fichiers sont des **vues d'implantation légères A2-R1**, avec formes simples et volumes réservés : **225 solides** au total. Ils conservent les noms de fichiers et le repère du véhicule. Les dimensions générales et le placement d'étude viennent du modèle léger du châssis. Les interfaces fines, dentures, pneus sculptés, circuits et faisceaux détaillés se trouvent dans les versions FreeCAD et GLB complètes. Les STEP d'implantation servent à ouvrir rapidement l'ensemble dans CAD Viewer ; leurs formes simplifiées ne qualifient pas les interfaces mécaniques ni les jeux locaux.

| Fichier | Taille |
| --- | --- |
| drone-v3-structure.step | 2.3 Mo |
| drone-v3-roulage.step | 0.1 Mo |
| drone-v3-electronique.step | 0.2 Mo |
| drone-v3-puissance.step | 0.3 Mo |
| drone-v3-complet-detaille.step | 6.6 Mo |

Sous-ensembles : [structure](drone-v3-structure.step), [roulage](drone-v3-roulage.step), [électronique](drone-v3-electronique.step), [puissance](drone-v3-puissance.step). [Assemblage STEP complet optimisé](drone-v3-complet-detaille.step). Ne pas superposer les quatre sous-ensembles au complet : cela doublerait les pièces.

Les [GLB de structure](drone-v3-structure.glb), [roulage](drone-v3-roulage.glb), [électronique](drone-v3-electronique.glb) et [puissance](drone-v3-puissance.glb) sont également disponibles, avec les détails de surface.

## Vérifications et origine du blocage

Les journaux locaux de CAD Viewer 1.5.7 indiquaient `RangeError: Invalid array length` pendant la transmission des anciens STEP de 359 et 293 Mo à la webview, avant même leur lecture par le moteur CAO. Le test précédent de validité géométrique ne vérifiait pas cette étape d'ouverture.

Le [rapport FreeCAD](validation-freecad.json) contrôle la réouverture du FCStd, les couleurs, les formes fermées/valides, le cadrage enregistré et les cinq STEP. Le [rapport CAD Viewer](validation-cad-viewer.json) teste les cinq STEP avec le moteur WebAssembly livré dans l'extension installée. L'[essai dans VS Code](validation-cad-viewer-gui.json) confirme le signal `modelLoaded` pour une copie identique du STEP complet léger. Le [contrôle GLB](validation-glb.json) vérifie les buffers, indices, nombres de triangles et encombrements. Les deux versions natives ont été ouvertes dans l'application FreeCAD installée et leurs vues exportées ; le contrôle de l'affichage rapide conserve les temps et nombres de triangles mesurés.

[Vue FreeCAD isométrique](apercu-freecad-isometrique.png) · [Vue FreeCAD de dessus](apercu-freecad-dessus.png) · [Contrôle de l'affichage rapide](validation-affichage-freecad.json) · [Provenance](provenance.json) · [Préparation](preparation.json).

Les quatre STEP détaillés d'origine et leurs rapports sont conservés dans [cette archive](sources-step-detaillees-originales.zip) ; le grand STEP complet d'origine est dans [cette seconde archive](sources-step-complet-original.zip). Les sources individuelles des composants et les plans du châssis ne sont pas modifiés.

## Limites de l'assemblage

La batterie G1, les supports de fusibles révisés, les EVM TI et le Pololu 2831 sans modèle exact gardent leurs volumes réservés. Les anciens modèles Zeee/MIDI/ATO ne sont pas réintroduits. Les axes définitifs, paliers adaptés, carters, cinématique et visserie restent à finaliser. Les câbles des composants gardent une pose illustrative : le faisceau n'est pas entièrement raccordé. Les interférences de l'assemblage détaillé et l'ajustement physique ne sont pas qualifiés.
