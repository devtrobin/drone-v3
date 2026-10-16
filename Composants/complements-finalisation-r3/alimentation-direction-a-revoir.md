# Alimentation de direction : anomalie à résoudre

Le calcul nominal à 6.4 V pack,30 A moteurs et 1 A de sortie servo donne environ 5.975 V à l’entrée de l’UBEC, sous les hypothèses de câblage/contact/température affichées. Le point d’étude de pointe descend plus bas. **Un abaisseur ne peut fournir 6 V à partir de moins de 6 V. Le couple FT5335M+Hobbywing 6 V ne peut donc pas être déclaré compatible avec toute l’enveloppe retenue.** Ce n’est pas un détail à remplacer par une simple mention «à tester».

Les composants visibles dans l’assemblage restent les réservations de l’étudeR2 ; la R3 livre l’armature et les parcours, sans annoncer la branche de direction prête à acheter. Les corrections possibles demandent une nouvelle sélection d’alimentation/servo ou une limitation de fonctionnement explicitement calculée ; relever le fusible ne corrige pas ce problème.

Une alternative a été documentée : **Hitec D950TW36950S**, avec [fiche originaleV2.2](references/Hitec-D950TW-datasheet.pdf) et [STEP constructeur original](references/Hitec-D950TW-original.stp). Le fabricant publie40x20x38mm,68g,25TØ6,21kg.cm de blocage à4.8V. Ce couple de blocage n’est pas un couple permanent ; le couple au rendement optimal est seulement4.2kg.cm à4.8V. Le corps et les fixations diffèrent du FT5335M ; ce n’est pas une substitution mécanique directe.

La page fabricantUS annonce 4.8..8.4 V ; la ficheV2.2 indique 3.5..8.4 V mais recommande l’utilisation au maximum de tension seulement sur une courte durée. **L’alimentation directe sur 2S pleine n’est donc pas retenue automatiquement.** Un palonnier 25T de rayon 20 et une alimentation adaptée doivent être fixés avant intégration. Aucun changement silencieux de cette pièce n’a été introduit dans la CAO.

Les petits régulateurs examinés ne sont pas validés sur leur seul courant typique annoncé : vérifier aussi tension minimale, tolérance de sortie, pertes du câble d’usine, transitoires et thermique. Le PDF permet de reprendre cette sélection avec des exigences explicites plutôt que de mélanger des variantes.

Sources : [HitecUS](https://hitecrcd.com/d950tw-wide-voltage-titanium-gear-25t-digital-coreless-servo/), [HitecEU et CAD](https://shop.hitec-europe.eu/collections/standard-servos/products/servo-d950tw). Aucun achat ni essai effectué.
