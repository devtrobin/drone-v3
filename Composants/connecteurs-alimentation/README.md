# Connecteurs des deux départs moteurs - AMASS XT60H

Choix d'étude du **14 octobre 2026** : **deux XT60H-F, contacts femelles, avec capots arrière**, côté faisceau, complémentaires aux XT60 à contacts mâles des deux Hobbywing WP16BL30 G2. La [photo constructeur conservée](photos/Hobbywing-WP16BL30-G2-contacts-originaux.jpg) montre les broches mâles ; contrôler cette interface et ses polarités à réception. Aucun achat ni essai matériel réalisé.

| Élément | Quantité à ajouter | Fonction |
| --- | ---: | --- |
| [XT60H-F et son capot](xt60h-f/README.md) | **2** | Positif après chaque ATO30 et négatif séparé vers D- ; départs ESC1 et ESC2 |
| [XT60H-M de référence](xt60h-m/README.md) | **0 obligatoire** | Interface déjà montée sur les ESC ; CAO de l'accouplement, pièces de rechange si lot par paires |
| Capots | 2 pour les F utilisés | Vérifier leur présence dans l'offre ; le catalogue fabricant les décrit comme optionnels |

Ces deux prises ne sont ni un connecteur de phases moteur ni un remplacement du XT60 de la batterie. Leurs deux pôles portent **le courant d'un seul ESC**. Les calibres des ESC et fusibles n'imposent pas le courant réellement traversé.

## Documentation et fichiers

- [Notice PDF et documents AMASS originaux](notices/README.md).
- [Cotes et différences de révision](cotes.md), [intégration et procédure de montage](integration.md).
- [Recherche Amazon, citation et avis utilisateurs](recherche-technique.md), [sources](sources.json), [archives et empreintes](assets.json).
- [Calculs et limites de courant](calculs.json), [nomenclature](nomenclature.json).
- [Huit STEP colorés avec aperçus et contrôles FreeCAD](3D/README.md) : F, M, sans capot, capot séparé, accouplement, éclaté et F câblé illustratif.

## Achat proposé

Lot **SoloGood / AMASS, 10 paires XT60H**, ASIN **B074PN6N4K**, [fiche Amazon.com](https://www.amazon.com/dp/B074PN6N4K). Titre et boutique SoloGood retrouvés dans la page consultée ; variante 10 paires à revérifier avant commande. [Lien Amazon.fr par ASIN](https://www.amazon.fr/dp/B074PN6N4K) et [recherche française](https://www.amazon.fr/s?k=AMASS+XT60H+capot) : **prix, vendeur, stock et livraison en France non confirmés**, pages directes bloquées. Aucune disponibilité française inventée.

Le besoin réel est de deux femelles, pas dix paires. Si ce lot est retenu et conforme, il annonce dix F et dix M ; deux F et leurs capots utilisés, huit F et dix M en réserve. Vérifier les **vingt capots** attendus, la couleur et l'authenticité sur l'offre exacte. Une petite quantité de F seuls avec capots peut coûter moins cher : [AMASS XT60H-F chez TME](https://www.tme.eu/fr/details/xt60h-f/connecteurs-dc/amass/), prix total rendu à comparer. Aucun prix exploitable relevé, aucun total budgétaire attribué.

## Courant retenu pour l'étude

La fiche historique V1.2 indique **30 A RC / 60 A MC**, sans durée d'impulsion publiée. Le catalogue fabricant **2026**, page 15, indique **35 A MAX, 12 AWG, Δ < 85 °C**, et 100 cycles ; la page produit exprime Δ < 85 K. Ces différences sont documentées, sans additionner les meilleures valeurs des révisions. Le « 60 A continu » des annonces commerciales n'est pas adopté.

Nous conservons une référence prudente de **30 A par prise**, avec un scénario **20 A par ESC non mesuré et non limité activement**. Ni cette référence ni le fusible ATO30 ne qualifient les pointes, les fils 16 AWG d'origine, ou le défaut LiPo. La paire XT60 du pack voit environ **44,39 A dans le scénario commun**, au-delà de cette référence de 30 A : cette interface reste à qualifier ou revoir séparément.


<!-- cordon-principal-batterie-v3 -->
Mise à jour du 15 octobre 2026 : [cordon principal CP0](../cordon-principal-batterie/recherche-technique.md) en étude XT60H-M + fils 12 AWG + deuxTE 130191. Positif vers entréeMIDI, négatif vers D- N2 ; remplace les terminaisons95R5 ouvertes/conditionnelles de ces seuls segments. Le6 mm² aval, MIDI→ED80→D+, reste distinct. **44 A continus non validés sur XT60 ; coordination duMIDI 60 A avec ce cordon à revoir avant construction.** Pas de changement de batterie ni de performance décidé. Lots fil/gaine réutilisés sans double achat ; prix et ASINFR mis à jour dans le dossier commun.
<!-- /cordon-principal-batterie-v3 -->
