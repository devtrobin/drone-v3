# Plans A2-R1

[Plans cotés PDF](plans-chassis-a2-r1.pdf), [tous les centres et découpes CSV](percages-et-decoupes.csv), [débit et quantités](../liste-debit.csv).

Un fichier DXF par pièceC01 àC19, avec G/D distincts lorsque nécessaire. C09x2,C16x2,C17x4 etC18x2 sont identiques : découper la quantité indiquée. C11G/D ont le même contour mais sont indexés pour leur emplacement. Les contours exportés contiennent réellement les trous/lumières ; toutes les unités sont des millimètres. Les sectionsL01/L02/L03 sont les profils de cornières brutes, pas des développés de tôles pliées.

Pour les cornières, cinq DXF supplémentaires de gabarits de perçage par aile :L01-semelle,L02-semelle,L02-verticale,L03-arriere,L03-pivot. Usiner seulement le calquePERCAGE sur la cornière déjà débitée. Le rectangle grisREFERENCE_AILE_NE_PAS_DECOUPER est un repère ; ne pas le traiter comme un contour à découper. Origines de ces faces expliquées dans le CSV et le débit.

Pas de G-code, de compensation outil ni de nidification matière imposée. Positionner les bruts selon les courses et le bridage de la CNC. Les trous fournisseur inconnus ne sont pas dans le plateau ; report sur les cassettes après présentation. Les fenêtresR1 réclamentØ2 ou une adaptation de rayon contrôlée.

Les identifiants et numéros de détail du PDF correspondent exactement au CSV. Celui-ci donne longueur totale de lumière (extrémité à extrémité), largeur et angle positif antihoraire depuisX. Le0 du dessin est le coin bas gauche du brut, y compris pour les contours non rectangulaires. Aucun PDF à imprimer en«ajuster» pour en déduire des dimensions ; prendre les cotes ou le DXF1:1.
