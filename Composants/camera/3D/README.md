# Modèle détaillé — InnoMaker U20CAM-4M

Reconstruction du **12 octobre 2026**, à partir de la notice, des photos de l'annonce Amazon B0H36XDQY8 et d'une photo utilisateur du verso du même produit.

- [Caméra détaillée en STEP, avec couleurs](camera-u20cam-4m-detaillee.step).
- [Vue isométrique](vue-isometrique.png), [avant](vue-avant.png), [arrière](vue-arriere.png), [arrière en perspective](vue-arriere-isometrique.png), [profil](vue-profil.png).
- [Dimensions, hypothèses et rapport de validation](provenance.json).
- [Contrôle d'importation des couleurs](validation-couleurs.json) : 13 couleurs récupérées par le lecteur STEP XCAF.
- [Photos de référence et crédits](../photos/README.md).
- Générateur reproductible : [build_camera_step.py](../../../tools/build_camera_step.py).

## Détails représentés

Carte FR4 à coins arrondis, vernis noir sur les deux faces, chants de carte, trous et métallisation, pastilles de fixation dorées, vias traversants, zone de test dorée perforée, pistes visibles sous le vernis et sérigraphies lisibles sur les photos.

Support d'objectif carré avec oreilles de fixation, bossages, vis et rondelles, fentes des têtes, fût nominal M8,5, collerettes, bague de réglage avec 48 rainures périphériques, capuchon avant festonné, anneau de maintien et surface de verre convexe colorée.

Au verso : boîtiers et terminaisons des composants CMS, dépôts de soudure, grand circuit QFN avec contacts périphériques, circuit à huit pattes, petits régulateurs, capot métallique du quartz, connecteur USB cinq broches avec cavité, contacts et languettes, fanout de pistes et repères visibles. Les noms fonctionnels des puces sont descriptifs et ne constituent pas une identification électrique de références illisibles.

Les détails sont des **solides et reliefs géométriques**, conservés dans le STEP. Les couleurs correspondent à l'aspect des photographies, sans calibration colorimétrique. STEP ne conserve pas les textures photographiques, le grain du plastique ni un matériau optique réaliste comme un moteur de rendu.

## Cotes et fidélité

| Élément | Valeur utilisée | Provenance / statut |
| --- | --- | --- |
| Carte | 32 × 32 mm | Notice et annonce |
| Trous de fixation de la carte | Ø2,2 mm | Notice |
| Entraxe de fixation de l'objectif | 18 mm | Notice et annonce ; interprétation mécanique à vérifier |
| Filetage nominal de l'objectif | M8,5 × 0,25 | Notice ; le pas de filetage caché n'est pas reconstruit |
| Centres des quatre trous de carte | (2 ; 2), (30 ; 2), (2 ; 30), (30 ; 30) mm | Estimation photographique, entraxe 28 mm non mesuré |
| Épaisseur de carte | 1,2 mm | Estimation photographique |
| Plateforme de l'objectif | 13,2 × 13,2 mm | Estimation photographique |
| Diamètre extérieur de la bague avant | Environ 9,9 mm | Estimation photographique |
| Centres, dimensions et hauteurs des CMS | Voir générateur et registre | Estimations depuis la photo arrière |
| Hauteur totale, connecteur et vis | Voir bornes calculées du modèle | Estimation ; pas un encombrement fabricant garanti |

Origine : coin inférieur gauche de la carte vue de face, plan arrière du PCB à z = 0 ; face de l'objectif vers +z. Unités : **millimètres**. Les cinq vues montrent le même assemblage.

Ce modèle sert à visualiser et à préparer une implantation. Les inconnues ne sont pas devenues des mesures par le seul fait d'être dessinées. Confirmer les entraxes, l'épaisseur, les hauteurs et le dégagement du connecteur avant de fabriquer un support.

## Limites des sources

Aucun fichier CAO natif, schéma ou Gerber exact n'a été trouvé dans le dépôt officiel du modèle. Les photos ne montrent pas toutes les pistes : seules des portions visibles sont reproduites approximativement. Le PCB est annoncé à quatre couches ; **les couches internes ne sont pas inventées**.

L'intérieur optique, les puces cachées sous le support d'objectif et les inscriptions illisibles ne sont pas reconstruits. La géométrie du verre représente son apparence extérieure, pas une prescription optique. Le câble USB de 1 m est exclu de ce STEP du module : sa position dépendra de l'assemblage du drone.

## Reproduction et validation

Le générateur utilise CadQuery/OpenCascade et Pillow. Environnement local de construction : `tools/temp/cad-env`, exclu de Git par `.gitignore`.

```powershell
tools/temp/cad-env/Scripts/python.exe tools/build_camera_step.py
```

Après export, le fichier est réimporté : validité des solides, nombre de solides, conservation du volume, enveloppe et présence des entités de couleur sont contrôlés. Les aperçus sont obtenus par tessellation de la géométrie CAO avec un tampon de profondeur ; ils ne sont pas des images générées indépendamment du STEP.
