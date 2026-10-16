# Câble de puissance 12 AWG - BNTECHGO rouge et noir

Choix d'étude du **14 octobre 2026** : **BNTECHGO SW12G68008F10C2**, deux fils séparés en cuivre étamé multibrins avec isolation silicone. Lot **10 ft rouge + 10 ft noir**, soit **3,048 m par couleur / 6,096 m total**. ASIN **B01ABOPMEI**, titre et variante 12 AWG contrôlés sur [Amazon.com](https://www.amazon.com/dp/B01ABOPMEI). Non acheté, non testé.

Ces fils servent aux raccordements courts **après chaque ATO30 vers son XT60H-F** et aux deux retours négatifs indépendants vers le MiniBus. Le tronc commun 6 mm² proposé reste une référence distincte à sélectionner et qualifier.

| Donnée annoncée | Valeur / source |
| --- | --- |
| Calibre | 12 AWG ; section nominale AWG ≈3,31 mm² |
| Construction BNTECHGO | **680 brins de Ø0,08 mm**, cuivre étamé ; pas aluminium cuivré |
| Faisceau métallique | **Ø2,41 mm**, section arrondie **3,4 mm²**, image technique BNTECHGO |
| Gaine | Silicone rouge ou noir, **Ø4,5 mm ±0,1** sur l'offre ; épaisseur nominale 1,05 mm sur l'image technique |
| Résistance annoncée | **5,06 Ω/km = 5,06 mΩ/m**, image BNTECHGO ; température et méthode d'essai non précisées |
| Température / tension annoncées | -60 à +200 °C / 600 V ; pas une capacité de courant certifiée pour notre montage |
| Courant de l'étude | 20 A par boucle ESC, hypothèse ; aucun courant continu admissible exact du lot sous nos conditions publié |

## Dossier

- [Intégration et procédure de préparation](integration.md), [cotes et provenance](cotes.md).
- [Recherche Amazon, prix, citation et avis](recherche-technique.md), [sources](sources.json), [archives et SHA256](assets.json).
- [Calculs](calculs.json), [nomenclature et besoin provisoire](nomenclature.json).
- [Notice PDF V3 et documents de comparaison](notices/README.md), [images originales](photos/README.md).
- [Six STEP colorés avec aperçus](3D/README.md) : implantation rouge/noir/paire courbée et trois modèles courts à **680 brins individuels chacun**.

## Achat et quantité

[Amazon.fr B01ABOPMEI](https://www.amazon.fr/dp/B01ABOPMEI) : **prix, vendeur, stock et livraison en France non confirmés**, accès direct bloqué. La fiche Amazon.com identifie le produit ; elle ne prouve pas une offre française livrable. Prix sur [le site BNTECHGO](https://bntechgo.com/bntechgo-12-gauge-silicone-wire-kit-ultra-flexible-20-ft-black-and-red-each-color-10-ft-high-temp-200-c-600v-12-awg-silicone-wire-680-strands-of-tinned-copper-wire-stranded-wire-stranded-wire-for-model-battery/) : **14,98 USD**, relevé le 14 octobre 2026, taxes et frais vers la France non confirmés ; aucune conversion présentée comme prix TTC livré.

Le lot suffit au besoin provisoire de quatre queues de 0,20 m (deux rouges et deux noires), soit **0,40 m par couleur**, avec réserve. Ces longueurs ne constituent pas une liste de coupe : déterminer les trajets et les raccords avant de couper. Les fils des porte-fusibles et ceux des ESC sont déjà inclus dans leurs composants et ne sont pas rachetés comme ces queues.

Le lot rouge/noir est choisi pour sa référence vérifiée ; des variantes plus courtes existent chez le fabricant mais leurs offres Amazon exactes ne sont pas validées ici. **B01AO7586O est du 14 AWG à la consultation : écarté**, même s'il est cité dans un forum parlant de 12 AWG.


<!-- cordon-principal-batterie-v3 -->
Mise à jour du 15 octobre 2026 : [cordon principal CP0](../cordon-principal-batterie/recherche-technique.md) en étude XT60H-M + fils 12 AWG + deuxTE 130191. Positif vers entréeMIDI, négatif vers D- N2 ; remplace les terminaisons95R5 ouvertes/conditionnelles de ces seuls segments. Le6 mm² aval, MIDI→ED80→D+, reste distinct. **44 A continus non validés sur XT60 ; coordination duMIDI 60 A avec ce cordon à revoir avant construction.** Pas de changement de batterie ni de performance décidé. Lots fil/gaine réutilisés sans double achat ; prix et ASINFR mis à jour dans le dossier commun.
<!-- /cordon-principal-batterie-v3 -->
