# Modèles détaillés — moteur 2435SL G3 et variateur WP16BL30 G2

Deux assemblages **STEP colorés**, reconstruits le **12 octobre 2026** à partir des notices et des photos conservées dans ce dossier. Unités : **millimètres**. Les accessoires câblés sont inclus dans une position illustrative.

| Modèle | Fichier STEP | Aperçus |
| --- | --- | --- |
| Moteur QuicRun 2435SL G3, 4 500 KV | [Moteur détaillé](moteur-quicrun-2435-g3-4500kv-detaille.step) | [Corps en perspective](moteur-vue-isometrique.png), [axe et fixations](moteur-vue-fixations.png), [ensemble avec câbles](moteur-vue-complete.png) |
| Variateur QuicRun WP16BL30 G2 | [Variateur détaillé](variateur-quicrun-wp16bl30-g2-detaille.step) | [Boîtier en perspective](variateur-vue-isometrique.png), [dessus](variateur-vue-dessus.png), [ensemble câblé](variateur-vue-complete.png), [interrupteur](variateur-vue-interrupteur.png) |

## Détails du moteur

Corps cylindrique noir avec rainures périphériques, joints de flasques, capot arrière rouge, marquages blancs sur la face et autour du cylindre, indications de phases, bague métallique et joint visibles autour de l'axe. Axe avec méplat et chanfrein, six trous de fixation avec entrées et fonds, sortie de câbles avec joint, trois câbles noirs, gaines orange/jaune/bleue et contacts dorés de 3,5 mm avec fentes.

Les marquages sont des reliefs géométriques très fins, conservés dans le STEP ; la police est une approximation du graphisme commercial. Le modèle affiche **4 500 KV**, même lorsque la galerie photographique commune montre l'autre variante.

Origine moteur : centre de la face de fixation, z = 0 ; corps vers +z jusqu'à 36 mm ; axe vers -z jusqu'à -12 mm. Le plan coté donne Ø24 mm, longueur du corps 36 ±0,20 mm, axe Ø2 mm sorti de 12 ±0,5 mm, cote sur méplat 1,7 mm et longueur de méplat 9 mm.

Les groupes de trous M2,5/M3 et cercles de Ø14/16/17 mm sont interprétés depuis le plan. Les angles de placement devront être contrôlés avant fabrication d'un support. Le filetage intérieur hélicoïdal n'est pas reproduit ; les alésages représentent des diamètres nominaux, pas des trous à percer avant taraudage.

## Détails du variateur

Boîtier noir arrondi, couvercle inférieur, zone supérieure sombre de scellement, dissipateur rouge avec ailettes et plate-forme de logo, condensateur visible avec bague métallique et étiquette blanche/rose, repères de phases et étiquettes latérales. Les valeurs illisibles du condensateur ne sont pas inventées.

Trois câbles de phases avec gaines et prises femelles, câbles rouge/noir de batterie, connecteur jaune XT60 avec cavités et contacts dorés, reliefs de préhension, câble de commande à trois fils, fil jaune de programmation et leurs boîtiers de connecteur. L'interrupteur déporté comprend une base noire, un cadre métallique, quatre vis fendues en croix et un capuchon de protection brun/gris avec les reliefs des commandes.

Origine variateur : coin inférieur du boîtier, z = 0. L'enveloppe du boîtier et du dissipateur est **33,4 × 26,8 × 15,1 mm** selon le constructeur. Elle exclut câbles, connecteurs, interrupteur et les très faibles reliefs des inscriptions. Les bornes de l'assemblage complet sont consignées dans le registre.

## Cotes publiées et estimations

| Élément | Statut |
| --- | --- |
| Corps, axe, méplat et fixations du moteur | Cotes de la notice ; lecture du plan pour les positions |
| Enveloppe du variateur | Cote constructeur publiée |
| Contacts de phases Ø3,5 mm, entrée XT60 | Interfaces constructeur ; détails des boîtiers estimés |
| Câbles du variateur | 16 AWG, longueurs nominales 75 mm à l'entrée et 60 mm en sortie publiées ; position, gaine et extrémités représentées d'après photos |
| Rainures, épaisseurs, joints et détails d'impression | Reconstruction photographique |
| Dissipateur, condensateur et interrupteur | Dimensions et formes estimées à l'intérieur de l'enveloppe publiée |
| Câbles moteur et petits connecteurs de commande | Longueurs et détails non cotés ; estimations photographiques |

Les chemins de câbles ne sont pas une installation mécanique validée. Les fils souples sont représentés dans une position fixe permettant de distinguer les composants. Le calibre AWG désigne le conducteur, pas le diamètre extérieur de la gaine. Confirmer connecteurs, positions et dégagements sur le matériel reçu avant de fabriquer les supports ou le faisceau.

## Fidélité et limites

Ces fichiers sont des reconstructions de l'**aspect extérieur**, pas des CAO natives Hobbywing. Les bobinages, aimants, rotor interne, carte électronique et pistes cachées du variateur ne sont pas reconstruits sans source les décrivant. Une coupe du modèle n'est donc pas une vue fidèle de l'intérieur réel.

Les couleurs sont approximées depuis les photos, sans calibration ; STEP conserve les couleurs des solides, mais pas les textures, la transparence optique du capuchon ni le grain des matériaux. Aucun calcul électrique, électromagnétique ou thermique ne découle de ces géométries.

## Validation et reproduction

### Correction des câbles — 13 octobre 2026

L'aspect coupé de certains câbles du variateur n'était pas volontaire. Les anciennes courbes étaient continues dans la géométrie, mais leur tessellation produisait des ruptures visibles dans l'aperçu. Les onze câbles du variateur utilisent désormais des courbes de Bézier à un seul segment. Les trois sorties de phases comprennent également une transition de gaine qui chevauche les protections des connecteurs.

Chaque câble est un solide valide et continu ; 51 points de sa ligne centrale sont contrôlés. L'export STEP est réimporté et validé avant de remplacer le fichier livré. L'[aperçu complet](variateur-vue-complete.png) est régénéré depuis la géométrie corrigée.

- [Registre moteur](moteur-quicrun-2435-g3-4500kv-detaille-provenance.json).
- [Registre variateur](variateur-quicrun-wp16bl30-g2-detaille-provenance.json).
- [Générateur reproductible](../../../tools/build_motor_esc_step.py).
- [Notices originales](../notices/README.md) et [photos utilisées](../photos/README.md).

Chaque STEP est réimporté avec OpenCascade : validité, nombre de solides, volume, enveloppe et couleurs XCAF sont contrôlés. Les registres conservent les résultats, les empreintes des fichiers et le détail des éléments nommés. Les aperçus proviennent de la tessellation des mêmes solides, via le rendu déjà utilisé pour la caméra.

Résultats : moteur **67 éléments nommés, 90 solides, 11 couleurs récupérées** ; variateur **106 éléments nommés, 143 solides, 13 couleurs récupérées**. Les écarts de volume et d'enveloppe après réimportation sont inférieurs aux seuils du générateur.

```powershell
tools/temp/cad-env/Scripts/python.exe tools/build_motor_esc_step.py
```

Options : `--model motor`, `--model esc`, ou `--no-render` pour exporter sans images. L'environnement temporaire de dépendances est exclu de Git. L'architecture actuelle utilise deux moteurs et deux variateurs à l'arrière, avec deux roues avant non motrices dédiées à la direction.
