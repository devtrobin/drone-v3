# Cotes et provenance

**Aucun matériel mesuré.** Référence UD-80A / 569010 ; original STEP obtenu via le service CAD lié à la page fabricant, format AP214, entrée ZIP E10106602.step.

| Donnée | Valeur | Provenance / portée |
| --- | --- | --- |
| Enveloppe nominale H/W/D | 69 / 30 / 46 mm | Fiche nVent 2023, p2 ; pattes comprises |
| Repère de fixation | 54 mm | Instruction IP7802_M, p1 |
| Cote de fixation indiquée | 4,5 mm, annotation M5 | Instruction ; passage de la vis et géométrie sur pièce à confirmer |
| Masse nominale | 0,07 kg | Fiche ; accessoires et câbles exclus |
| Entrée / sorties | 1 / 6 communes | Fiche et plans : deux grandes sorties, quatre petites |
| Matériaux | Cuivre étamé, thermoplastique | Référence produit ; détails de grade de chaque pièce non tous publiés |
| Capot | Bleu transparent, articulé/amovible | Photographies et fiche fabricant ; inclus |
| Fils, embouts, vis de panneau | Absents de la CAO | Choix du faisceau ultérieur |

Les enveloppes précises issues du STEP et des exports sont consignées dans [catalogue.json](3D/catalogue.json). Elles diffèrent légèrement des valeurs commerciales arrondies ; réserver aussi l'accès à l'outil, les fils et l'ouverture du capot. Le STEP officiel contient **trois solides** : il ne présente pas toutes les vis et petites formes comme des pièces séparées. Il n'est pas un dossier de fabrication ou une simulation électrique.

Repère natif : X hauteur fabricant, Y profondeur, Z largeur, centre non nul. Repère d'implantation V3 : X largeur, Y longueur de fixation, Z profondeur depuis le plan arrière. Rotation autour de (1,1,1) de +120°, puis translation définie dans les JSON. Les dérivés gardent les formes officielles ; couleurs de lecture attribuées et capot bleu rendu opaque. L'original reste intact, avec les styles exportés par le fabricant.

Vue sans capot : retrait du solide officiel correspondant. Vue éclatée : capot décalé de Z+22 mm ; présentation séparée, pas trajectoire garantie de charnière. Aucune géométrie interne supplémentaire inventée. Une intersection de volume d'environ 5,10 mm³ entre socle et capot est héritée de l'assemblage fabricant et conservée, sans correction de forme ; ce n'est pas une preuve d'ajustement sur pièce. Les calculs d'enveloppe utilisent le calcul précis OpenCascade sans triangulation pour les surfaces courbes ; imports indépendants FreeCAD contrôlés.

La photo RS montre un marquage historique ERICO / 690 V ; la photo nVent et la fiche actuelle indiquent ERIFLEX / 1 000 V AC/DC IEC. Cette variation est conservée comme provenance de révision ; ne pas recopier un ancien marquage sur un modèle prétendument mesuré. Les dimensions de colis Graybar et les bornes Amazon UKK80 génériques ne servent pas de cotes de cette référence.
