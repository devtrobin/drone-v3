# Recherche, achat et avis - 13 octobre 2026

## Sélection

| Candidat documenté | Résistance thermique | Masse / matière | Décision pour la V3 |
| --- | ---: | --- | --- |
| **Sensata HS251** | **2,5 °C/W** | 100 g, aluminium naturel | Retenu pour l'étude ; taraudages #8-32, refroidissement passif documenté |
| Sensata HS301 | 3 °C/W | 178 g, aluminium anodisé noir ; catalogue historique | Compatible et accepte un ventilateur de 40 mm ; plus lourd, sans gain thermique passif |
| Sensata HS501DR | 5 °C/W | 52 g dans le catalogue historique, **acier zingué**, montage DIN | Plus plat, mais courbe D1D100 à 5 °C/W environ 35 A à 40 °C ; insuffisant pour l'enveloppe de 40 A |
| Petits dissipateurs SSR génériques | Non vérifiée | Variable | Pas retenus : dimensions, taraudages et résistance thermique non établis pour une offre précise |

Ces données ne démontrent pas que le HS251 est le plus compact de tous les dissipateurs existants. Elles permettent de choisir parmi les références comparées. La fiche Sensata 2024 prime pour le HS251 ; le catalogue historique conservé sert à comprendre les dimensions et les alternatives. Les courbes des ensembles HS251-D2450 concernent un **relais AC**, et ne dimensionnent pas notre D1D100 DC.

## Amazon et coût

Les recherches Amazon.fr, Amazon.com et moteurs de recherche n'ont pas identifié d'offre exacte vérifiable pour HS251 ou HSP-1. L'ouverture directe d'Amazon.fr a échoué. **Aucun ASIN, vendeur, prix TTC, stock français ni livraison n'est validé.** Les liens ci-dessous sont des recherches :

- [Amazon.fr - Crydom HS251](https://www.amazon.fr/s?k=Crydom+HS251)
- [Amazon.fr - Crydom HSP-1](https://www.amazon.fr/s?k=Crydom+HSP-1)

Une page DigiKey consultée affichait 25,54 USD pour une unité et 417 unités disponibles ; Newark affichait 43,38 USD et 103 unités. Ce sont des observations de pages internationales, susceptibles de changer, **pas des devis français livrés**. Livraison, taxes, quantité minimale du pad et contenu du kit HK1 restent à établir. Aucune commande n'a été passée. Sources : [DigiKey HS251](https://www.digikey.com/en/products/detail/sensata-crydom/HS251/2122804), [Newark HS251](https://www.newark.com/sensata-crydom/hs251/heat-sink-50-3-mm-2-5-c-w-panel/dp/41X7868).

## Retours d'utilisateurs

Un avis produit public eBay, daté du **9 mai 2025**, indique un ajustement satisfaisant sur un **D06D100**, avec vis reçues. Extrait : « Fits the D06D100 SSR ». Source : [avis HS251](https://www.ebay.com/p/1210661465). Il s'agit d'un autre relais et d'un seul témoignage : cela ne prouve ni la tenue thermique avec D1D100 ni le contenu d'une future offre Amazon.

Les recherches de forums et YouTube n'ont pas apporté d'essai exploitable de l'ensemble **HS251 + D1D100 + deux ESC sous 2S**. Les nombreux retours sur des radiateurs de moteurs RC, processeurs ou relais AC sont hors de cette qualification. Aucun résultat d'essai ou avis Amazon n'est inventé.

## Ambiguïtés résolues ou conservées

- **Encombrement :** le catalogue annonce 58,7 × 50,3 × 38,4 mm pour le corps ; le plan 2024 et le STEP montrent les pattes. Réserver environ **85,3 × 52,3 × 40,6 mm** pour le dissipateur complet, avant le relais et les dégagements.
- **Surface :** la fiche 2024 écrit `521./336` pour in²/cm² ; le catalogue indique 52,1 in² / 336 cm². La première écriture semble contenir une virgule décimale manquante. Cette surface n'est pas utilisée pour recalculer une capacité thermique.
- **Filetage :** deux #8-32 UNC selon Sensata ; le STEP montre les perçages, pas les hélices du taraudage.
- **Pad :** la fiche 2018, le plan 2011 et le PCN 2023 donnent des révisions différentes. La géométrie principale retenue suit **57,1 × 44,2 mm, entraxe d'encoches 47,5 mm, ouverture 4,83 mm** de la fiche 2018. Les autres cotes restent explicitement dans les sources.
- **Version rose :** matériau et couleur confirmés dans le PCN archivé ; épaisseur **0,127 mm** dans son annexe préliminaire consultée sur TTI. Le contour exact du lot rose n'a pas été mesuré : le modèle réutilise le contour 2018 et l'annonce.
- **Interface thermique :** ne pas traiter une impédance surfacique en °C·in²/W comme une résistance globale en °C/W. Les performances dépendent des surfaces et du serrage. Le calcul utilise une hypothèse déclarée de 0,2 °C/W.

## Sources principales

1. [Sensata HS251 - fiche, plan et STEP](https://www.sensata.com/products/relays/hs-series-heat-sinks-hs251).
2. [Fiche HS251 Sensata 2024, miroir Farnell](https://www.farnell.com/datasheets/4619827.pdf).
3. [Guide HS 2024, miroir RS](https://docs.rs-online.com/766e/A700000009477596.pdf).
4. [Catalogue Crydom HS, miroir RS](https://docs.rs-online.com/cf62/A700000010035084.pdf).
5. [HSP fiche 2018, miroir Farnell](https://www.farnell.com/datasheets/4600889.pdf), [plan historique](https://www.farnell.com/cad/4775092.pdf).
6. [PCN-SSR-231214 archivé, miroir Farnell](https://www.farnell.com/datasheets/4129384.pdf), [version TTI avec annexe préliminaire consultée](https://www.ttiasia.com/content/dam/ttiinc/products/PCN/sensata/Sensata-PCN-SSR-231214.pdf).
7. [D1D100 Sensata, fiche originale déjà archivée](../protection-batterie/coupure-moteurs/notices/Sensata-Crydom-1-DC-D1D100-datasheet.pdf).

Les réponses refusées et documents effectivement téléchargés sont distingués dans [assets.json](assets.json). Le STEP original est conservé byte pour byte ; les nouveaux modèles et la notice du projet sont identifiés comme tels.
