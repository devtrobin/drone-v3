# Cotes des protections moteurs

Repères du **14 octobre 2026** ; aucune pièce physique mesurée. Les fichiers STEP sont des reconstructions d'extérieur, pas des plans pour fabriquer des fusibles ou garantir le contact.

| Élément | Cote utilisée | Provenance / limite |
| --- | --- | --- |
| ATO, enveloppe totale | 19,1 × 5,1 × 18,8 mm | Plan fabricant aftermarket 2022, cotes de référence |
| Lame, largeur / épaisseur | 4,1 / 0,65 mm | Plan fabricant |
| Lame, dépassement | 6,5 mm | Plan fabricant |
| Deux lames, largeur extérieure | 14,5 mm | Ce n'est pas leur entraxe |
| Entraxe des lames | 10,4 mm | Déduit : 14,5 - 4,1 ; centres X ±5,2 |
| Masse fusible seul | 1,4 g ±5 % | Fabricant ; 2,8 g pour deux, hors supports |
| Support avec oreille, hors fils | 37,5 × 38 × 15 mm | **Estimation CAO**, photo 5065, pas une cote publiée |
| Trou de support | Ø5,0 mm | **Estimation CAO** ; mesure revendeur ≈3/16 pouce, soit 4,7625 mm |
| Centre du trou CAO | X -21,03 / Y 22,53 mm | **Position estimée**, mesurer avant perçage |
| Fils de support | 12 AWG | Fabricant, environ 3,31 mm² nominal |
| Fils en CAO | Ø4,3 ; longueur extérieure 100 ; bouts nus 8 mm | **Illustration**, diamètre et longueur livrés non confirmés |
| Brins en CAO | 19 × Ø0,47 mm par fil | **Illustration**, aire 3,296 mm², nombre réel inconnu |
| Entrée ESC | 16 AWG ; 75 mm rouge et noir | Fiche Hobbywing G2 actuelle ; environ 1,31 mm² nominal |
| Pose de deux supports | Centres X -26 et +26 mm | **Implantation d'étude**, aucune entraxe de montage imposé |

Le support reprend la géométrie documentée dans [le dossier Pi](../protection-branche-pi/cotes.md) : socle, capot creux, oreille, guides, joint orange à nervures et contacts femelles approchés. Les deux fils rouges continus sortent du même côté. Leurs bouts nus sont les terminaisons représentées, pas des interruptions accidentelles.

Le fusible vert comporte deux lames avec chanfreins, dépouilles de corps, poches, deux points de test et marquage « 30 ». Les petites formes, rayons, police et teinte sont estimés. Le PA66 réel translucide est rendu opaque ; l'élément interne calibré n'est pas inventé. Aucune étanchéité ou pression de contact n'est validée par la CAO.

Les dimensions DigiKey 19,05 × 5,08 × 12,19 mm concernent une description de corps ; elles ne remplacent pas les 18,8 mm totaux du plan. Les cotes marchandes de la carte de cinq fusibles et les tailles de colis ne servent pas de cotes de pièce.

Repères : support X largeur, Y insertion, Z épaisseur, fils vers -Y. Fusible isolé Z hauteur ; montage par rotation X -90°, translation (0,4,7,5). Vue éclatée : capot Y+36 mm. Assemblage double : quatre fils libres, sans raccord électrique commun, cosses ou XT60.
