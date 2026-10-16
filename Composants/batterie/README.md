> **R?vision active du15 octobre2026.** G1 IC5 conserv? ; charge S65 + BEEC1067 + ?quilibrage d?di?. Le raccord de charge est s?lectionn?. [?tat courant](../verification-alimentation/README.md). Les valeurs diff?rentes de l?alimentation dans les documents anciens restent historiques.

> **Révision du 15 octobre 2026 : batterie 2S G1 IC5 et cordon 10 AWG proposés après le choix utilisateur.** [État courant](../cordon-principal-batterie/README.md). Les anciens plans/PDF Zeee restent datés. Charge S65 initiale à 5 A, avec un raccord IC5 distinct à sélectionner avant charge.

# Batterie de propulsion et d’électronique

Choix d’étude du **13 octobre 2026** : **Zeee 2S1P 7,4 V 5 200 mAh 80C — boîtier rigide, XT60**. Non acheté, non testé.

Une batterie embarquée ; référence Amazon vendue en lot de deux. La seconde est une réserve, sans mise en parallèle.

La 2S conserve le dimensionnement moteur/transmission existant. Le pack de 5,2 Ah offre une réserve d’énergie supérieure aux scénarios de 2,2 et 3 Ah, avec une masse annoncée raisonnable pour l’hypothèse de véhicule de 2 kg. La coque rigide convient à une intégration sur véhicule, à protéger et fixer sans écraser les fils.

## Caractéristiques et cotes

| Donnée | Valeur / statut |
| --- | --- |
| Configuration | LiPo standard 2S1P, 7,4 V nominal, 8,4 V pleine charge ; pas LiHV |
| Capacité / énergie annoncée | 5 200 mAh / 38,48 Wh par batterie ; capacité réelle non mesurée |
| Dimensions fabricant | 138 × 47 × 25 mm, tolérance annoncée ±2 mm ; fils et connecteurs hors boîtier |
| Masse approximative | 250 g par pack annoncés |
| Prises | Puissance XT60 ; prise d’équilibrage 3 voies visible, famille JST-XH à vérifier sur le pack reçu |
| 80C | Notation commerciale annoncée ; aucun essai indépendant de courant continu pour cet ASIN n’est validé |
| Limites cellule publiées | Ne pas dépasser 4,2 V ; ne pas descendre sous 3,2 V par cellule. Une tension totale ne surveille pas chaque cellule. |
| Usage | Un seul pack alimente les deux ESC et la branche Pi ; servo sur le BEC d’un seul ESC réglé à 6 V |

## Achat Amazon et disponibilité

ASIN identifié : **B08DCYVHSF**, [fiche Amazon.com consultée](https://www.amazon.com/dp/B08DCYVHSF). [Même identifiant sur Amazon.fr](https://www.amazon.fr/dp/B08DCYVHSF) : accès indisponible dans cette session, présence commerciale française et achat livrable **non confirmés**.

**Aucun prix en euros, vendeur, stock ou frais livrés n’est inventé.** Les deux identifiants confirmés le sont sur Amazon.com ; un changement de domaine ne prouve pas une offre en France.

## Documents et modèle

[Notice d’intégration du projet](notices/notice-integration-v3.md), [recherche, avis et informations manquantes](recherche-technique.md), [sources structurées](sources.json), [photos constructeur](photos/README.md), [liste des originaux](assets.json).

[Modèles STEP, aperçus et provenance](3D/README.md).

[Référence technique fabricant](https://zeeebattery.com/products/zeee-2s-lipo-battery-5200mah-7-4v-80c-xt60-plug). [Architecture et dimensionnement de l’alimentation](../alimentation/README.md).

Le dossier des [prises des deux ESC](../connecteurs-alimentation/README.md) distingue leurs courants individuels de celui du XT60 commun du pack. Le scénario 40 A moteurs + 25 W Pi à 6,4 V / 90 % + 0,05 A auxiliaire donne **44,39 A au connecteur batterie**, non mesuré. Révision et tenue de cette interface inconnues ; ce scénario dépasse la référence prudente de 30 A prise pour les nouveaux XT60H. Qualification ou révision de la liaison commune à prévoir, sans modifier le pack pendant cette étude.
