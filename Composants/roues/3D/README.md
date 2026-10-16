# Modèle STEP d'une roue HobbyPark 63 × 26 mm

Reconstruction du **13 octobre 2026**, variante **Color A**, ASIN **B0CTNVV7BJ**. Modèle d'aspect paramétrique issu des [photos originales](../photos/README.md) et des cotes commerciales ; **aucune CAO native du fabricant ni mesure physique**.

- [Roue détaillée en STEP](roue-hobbypark-63x26-detaillee.step).
- [Perspective](vue-isometrique.png), [face avant](vue-face.png), [arrière et hexagone](vue-arriere.png), [bande de roulement](vue-bande-roulement.png), [coupe](vue-coupe.png).
- [Provenance et validation](provenance.json).

Le STEP contient une roue, avec **pneu, jante et insert mousse séparés**, et leurs couleurs approximatives de caoutchouc et plastique noirs, avec une mousse grise. Il reproduit les épaules arrondies, les rainures directionnelles, la jante noire à branches, les lèvres périphériques, le passage d'axe et l'empreinte hexagonale arrière. Les petits détails de moulage sont reconstruits ; les cercles sur la jante ne sont pas modélisés comme de fausses vis métalliques. Aucun écrou ni axe de véhicule n'est inclus.

## Repère et cotes

Unités **millimètres**, axe de roue **Z**, pneu centré en **z = 0**, face extérieure vers **+Z**. L'enveloppe nominale attendue est **63 × 63 × 26 mm**. Les quatre roues du véhicule utiliseront ce modèle placé dans le repère du châssis ; le STEP ne représente pas le train roulant complet.

Les données publiées reprises sont diamètre 63 mm, largeur 26 mm, diamètre intérieur nominal 47 mm, hexagone 12 mm entre plats et trou de passage 4 mm. L'interprétation géométrique du diamètre de 47 mm suit la photo cotée, sans constituer un plan du talon du pneu.

**Estimations** : comptage/reconstruction de 18 branches, répétition de 24 motifs du pneu, rainures, rayons d'épaule, épaisseurs, creux de la jante, position du moyeu, profondeur d'hexagone de 3,5 mm, mousse et détails de moulage. Le déport réel n'est pas certifié. La rugosité microscopique du caoutchouc, les inscriptions illisibles et la déformation sous charge ne sont pas inventées.

## Contrôles

Le générateur vérifie la validité des trois solides, l'absence d'intersection volumique entre eux, le passage d'axe et l'empreinte hexagonale par sondes géométriques. Il exporte puis réimporte le STEP : **3 solides valides, 681 faces, 3 couleurs**, enveloppe 63 × 63 × 26 mm ; erreur relative de volume d'environ 8,6 × 10⁻⁸. Le fichier fait **11,8 Mo** et n'est pas ignoré par Git. Les résultats et l'empreinte sont dans le registre. Les aperçus proviennent des mêmes géométries ; la coupe est une section de ces solides, pas une photographie de l'intérieur réel.

Le modèle est destiné à l'étude de placement. Mesurer déport et interfaces avant fabrication définitive. L'ouverture dans l'interface FreeCAD et CAD View n'est pas testée ici ; les contrôles utilisent OpenCascade. Le fichier est conservé directement dans Git s'il reste sous la limite de taille du dépôt ; aucun commit ni envoi n'est réalisé.

Reproduction depuis la racine `drone-v3` :

```powershell
tools/temp/cad-env/Scripts/python.exe tools/build_wheel_step.py
```

[Générateur](../../../tools/build_wheel_step.py), option `--no-render`. Les dépendances CadQuery/OpenCascade, NumPy, Pillow et Numba résident dans l'environnement temporaire du projet, ignoré par Git.

[Retour à la fiche](../README.md).
