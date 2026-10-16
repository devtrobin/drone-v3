# Cotes, repères et fidélité des modèles

Toutes les dimensions ci-dessous sont en millimètres. Aucun élément n'a été mesuré sur une pièce réelle.

| Élément | Valeur | Statut et origine |
| --- | --- | --- |
| Pi 5, quatre trous de fixation | Ø2,7 ; rectangle 58 x 49 | Plan officiel p.1, référence approximative |
| Pi, centres dans notre repère | (3,5;3,5), (61,5;3,5), (61,5;52,5), (3,5;52,5) | Déduits du plan ; origine bord gauche/bord inférieur du PCB |
| Zones circulaires aux fixations | Ø6 | Repère du plan ; ne garantit pas le dégagement en 3D |
| MF : corps + goujon | 6+6, 8+6, 10+6, 15+6, 20+6 | Illustration et description du kit exact |
| FF : corps | 6, 10, 15, 20 | Illustration et description du kit exact |
| Vis : longueur sous tête | 8, 12, 20 | Illustration et description du kit exact |
| Désignation du filetage | M2.5 | Publiée pour le kit |
| Pas CAO | 0,45 | Pas usuel d'étude, cohérent avec exemples Essentra ; non spécifié/mesuré sur ce lot |
| Entretoises : forme et surplats | Hexagonal ; 5,0 sur plats | Forme d'après photo de détails, surplats estimé |
| Tête de vis | Ø4,7 ; hauteur 2,0 ; empreinte cruciforme | Forme visible, dimensions et raccords estimés |
| Écrou | Surplats 5,0 ; hauteur 2,0 | Forme visible, dimensions estimées |
| Rondelle | Øextérieur 5,0 ; Øintérieur 2,7 ; épaisseur 0,5 | Dimensions estimées, aucune cotation fabricant trouvée |
| MF : taraudage borgne | Profondeur min(6,5 ; longueur corps - 2) | Hypothèse de CAO, avec fond plat non spécifié |
| FF : taraudage traversant | Sur toute la longueur | Hypothèse de CAO ; ne certifie pas le lot |
| Filetage intérieur | Jeu radial de reconstruction 0,03 | Hypothèse graphique de montage, pas une classe de tolérance |

Le profil des filetages comporte une vraie hélice droite, des flancs proches du profil métrique de 60 degrés, des crêtes tronquées et des fonds simplifiés. Les entrées sont chanfreinées ; détails de moulage, rayons exacts, amorces et bavures ne sont pas certifiés. **Ne pas employer ces STEP comme jauges, plans de production ou preuves de résistance.**

Les images haute définition de tailles et de détails confirment les corps MF et FF hexagonaux. Leur dimension surplats reste estimée à 5 mm. Vérifier la forme et les dimensions du lot à réception.

Les FF passent par une préparation en représentation spline STEP avant le contrôle final. L'écart de volume de cette conversion est tracé dans leur JSON (limite 0,1 %) ; le réimport final garde une limite de 0,01 %. Cela ne change pas le statut d'estimation des détails internes.

## Montage de travail à 10 mm

Le plancher futur est à z=0 dans l'assemblage, sans être dessiné. Entretoise MF : corps z=0 à 10, goujon z=10 à 16. Dessous de carte étudié z=10 ; épaisseur temporaire **1,6 mm**, pas une cote vérifiée du Pi retenu. Rondelle supérieure z=11,6 à 12,1 ; écrou z=12,1 à 14,1. Le goujon dépasse de **1,9 mm** dans cette hypothèse.

Au-dessous, épaisseur temporaire de panneau **2 mm**, non décidée pour le châssis. Rondelle inférieure z=-2,5 à -2 ; vis sous tête 8 mm, engagement d'étude **5,5 mm** : 8 - 2 - 0,5. Taraudage modélisé 6,5 mm : marge de fond **1 mm**. Mesurer la profondeur réelle avant de choisir une vis ; une vis en butée ne serre pas le panneau.

Le jeu radial nominal M2.5/Ø2.7 serait **0,10 mm**, sans tolérances. Avec un hexagone estimé à 5 mm surplats, rayon de sommet **2,887 mm** et marge nominale au cercle Ø6 **0,113 mm**. Cette petite marge est un calcul de référence, pas un contrôle des composants proches ni une qualification physique.

L'assemblage ne contient que les **20 pièces du kit**, disposées sur le rectangle de fixation du Pi. **Le PCB et le châssis sont intentionnellement absents.** Les épaisseurs servent à étudier l'engagement et à documenter les espaces vides ; elles ne figent aucune fabrication.

[Plan officiel](https://datasheets.raspberrypi.com/rpi5/raspberry-pi-5-mechanical-drawing.pdf) et [hypothèses calculables](calculs.json). La hauteur finale et les trous du châssis seront définis lors de son étude, en dernier.
