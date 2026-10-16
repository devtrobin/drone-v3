# Cotes documentées et détails estimés

Toutes les cotes sont en **millimètres**. Aucun composant physique n'a été mesuré.

| Pièce / cote | Valeur utilisée | Source / statut |
| --- | --- | --- |
| Support : longueur X | 51,4 | Plan Littelfuse, catalogue 2012 PDF p.164, page imprimée 159 ; fiche 2008 identique |
| Support : largeur Y | 27,3 | Vue de bout du même plan |
| Support : hauteur Z | 24,9 | Vue latérale du même plan |
| Support : perçages de fixation | 2 × Ø3,81 | Plan ; deux positions diagonales |
| Support : rectangle des centres | 41 × 15,2 | Plan ; centres CAO (-20,5 ; +7,6) et (+20,5 ; -7,6) |
| Goujons électriques | 2 × M5 × 0,8, entraxe 30 | M5 publié ; pas standard M5 et interface MIDI 30 mm |
| Fusible : longueur X | 41 | Plan REV07272021 p.2 |
| Fusible : largeur maximale Y | 12 | Même plan ; lames largeur 10 |
| Fusible : hauteur Z, 60 A | 8,0 | Même plan pour les calibres 30-80 A |
| Fusible : boîtier central | 16 de long | Plan |
| Fusible : trous | 2 × Ø5,5, entraxe 30 | Version M5 du plan, pas la variante M6 Ø6,5 |
| Fusible : épaisseur des pattes | 0,41 | Plan pour 30-80 A |

Les pages marchandes permutent parfois **largeur et hauteur du support**, et donnent parfois **8,3 mm pour toute la famille de fusibles**. Les modèles suivent les vues cotées du fabricant, pas cette permutation. Les trous et ajustements CAO sont nominaux ; les tolérances exactes du lot doivent être vérifiées sur le dessin applicable.

**Détails estimés :** épaisseurs de paroi, poches du socle, chanfreins, rayons, nervures, clips, lanière, longueur des goujons, dimensions des rondelles/écrous et position exacte des marquages. Les filets des goujons sont représentés par des hélices approchées ; les taraudages des écrous sont simplifiés. Les lames sont étamées en apparence, sans couche microscopique ni élément de fusion interne inventé.

Le corps du support reprend le gabarit 51,4 × 27,3 × 24,9 ; **la lanière reconstruite déborde**. L'enveloppe totale de chaque STEP figure dans son JSON voisin. Réserver aussi l'espace pour les cosses, le rayon des câbles et l'ouverture du capot. La vue éclatée translate le capot de 25 mm et omet la lanière : cette pose ne simule pas son articulation.

[Catalogue 3D](3D/README.md), [sources et originaux](assets.json).
