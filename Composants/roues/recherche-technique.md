# Recherche technique — HobbyPark B0CTNVV7BJ, Color A

Recherche du **13 octobre 2026**. Aucun exemplaire physique reçu, aucun essai.

## Sources consultées

La [fiche Amazon.com](https://www.amazon.com/dp/B0CTNVV7BJ) donne les dimensions nominales, matériaux et état pré-collé. Ses images originales sont conservées avec URL et SHA-256 dans [photos/assets.json](photos/assets.json). Le contenu consultable est indexé ; son offre commerciale ne permet pas de vérifier le stock du jour en France.

La fiche Amazon.fr reste inaccessible à nos outils ; aucun prix en euros, vendeur ou stock n'est inventé. Les reprises Tiendamia identifient le même ASIN, mais leurs prix et masses avec emballage ne sont pas utilisés pour dimensionner les roues. Aucun plan coté complet, STEP constructeur ou PDF de notice spécifique à cet ASIN n'a été trouvé dans les recherches effectuées. Aucun essai YouTube identifié pour cette variante exacte ne fournit de mesure exploitable de vitesse admissible, résistance au roulement ou adhérence sur notre sol. Cela ne prouve pas l'absence de toute autre documentation.

## Lecture des photos

| Image | Information exploitable |
| --- | --- |
| 01 | Lot de quatre roues noires et quatre écrous représentés ; rainures en chevrons |
| 02 | Cotes 63 mm, 26 mm, 47 mm, 12 mm et 4 mm ; les faces avant et arrière sont visibles |
| 03 | État pré-collé, nylon, caoutchouc et motif du pneu annoncés dans l'image commerciale |
| 04 | Insert mousse annulaire d'une pièce présenté ; argumentaire commercial, sans mesure de résistance |
| 05 et 07 | Illustrations sur voiture RC ; pas une preuve de nos performances |
| 06 | Détails des branches, de l'empreinte hexagonale, des marques de moulage et des rainures |
| 08 | Usage routier illustré sur asphalte et béton ; adhérence sur carrelage ou parquet non mesurée |

Le modèle reconstruit **18 branches** à partir des vues et un motif de pneu répété. Ce comptage, la courbure des branches, les détails de moulage et le pas exact des rainures restent des interprétations visuelles. Le diamètre intérieur de 47 mm est interprété comme l'enveloppe jante/talon dans le modèle ; il ne constitue pas un plan de la section interne du pneu.

## Incidences pour V3

Les quatre roues peuvent partager la même référence commerciale. Chaque roue arrière recevra son propre entraînement par réduction. À l'avant, les roues tournent librement sur des fusées orientables ; le servomoteur agit sur les biellettes, pas sur les pneus.

La mécanique doit reprendre les charges dans les axes et roulements. La rétention de roue demande un écrou et un filetage adaptés à la fusée retenue ; un trou de passage annoncé de 4 mm ne certifie pas un filetage M4 fourni. Prévoir une surface d'appui correcte du moyeu hexagonal, sans serrer la jante contre une partie fixe qui bloquerait la rotation.

Le déport et la position axiale de l'appui hexagonal influencent la voie, le rayon de pivot et l'effort du servo. Les estimations CAO ne suffisent pas pour arrêter ces interfaces de fabrication. En virage, les vitesses des deux roues arrière devront tenir compte des trajectoires différentes.

Pour D = 0,063 m, circonférence nominale πD ≈ 197,92 mm. La vitesse cinématique n = 60v/(πD) vaut environ 1 684 tr/min à 20 km/h et 3 368 tr/min à 40 km/h. Avec le scénario moteur 4 500 KV et 7,4 V, le rapport de 9,9 environ est seulement un résultat à vide à tension nominale ; il ne sélectionne pas notre transmission.

La déformation sous charge réduit le rayon effectif et change la vitesse réelle. Ni la résistance au roulement ni la masse d'une roue ne sont établies : pas de gain d'autonomie chiffré à déduire de cette sélection.

## Informations à relever à réception

| Point | Vérification |
| --- | --- |
| Variante et lot | Marquages, quatre roues, accessoires et pré-collage effectifs |
| Masse | Peser une roue puis le lot sans emballage |
| Géométrie | Diamètre, largeur, voile et faux-rond ; dimensions du pneu chargé |
| Interface | Hexagone entre plats, profondeur, fond, trou et tolérances ; déport par rapport au milieu du pneu |
| Fixation | Filetage des écrous, portée, longueur de fusée et dégagement d'outil |
| Direction | Dégagement au braquage, jeu des pivots, effort réel du servo |
| Roulement | Frottements, collage, vibration et température lors d'essais progressifs |
| Performances | Vitesse réelle, Wh et freinage avec vidéo active ; aucune vitesse garantie par la mention 2S/3S |

[Fiche composant](README.md).
