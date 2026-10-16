<!-- alimentation-r2 -->
> **Sélection active révisée le 15 octobre 2026.** S65 conservé pour le pack G1 5 Ah : charge LiPo Balance 2S, 5 A, 42 W maximum. Cordon BEEC1067 et rallonge 2S dédiée sélectionnés ; les anciennes valeurs Zeee 5,2 Ah / 5,2 A sont historiques.
> [État électrique courant](../verification-alimentation/README.md) · [Raccordements](../verification-alimentation/integration.md). Les références différentes dans les documents ci-dessous sont historiques. Qualification matérielle non réalisée ; confirmations restantes explicites.
<!-- /alimentation-r2 -->

# Chargeur équilibré de la batterie

Choix d’étude du **13 octobre 2026** : **SkyRC S65 — SK-100152, 65 W / 6 A, secteur intégré**. Non acheté, non testé.

Un chargeur à l’atelier, hors du véhicule ; il n’entre pas dans la masse embarquée.

Il couvre la batterie 2S de 5,2 Ah avec charge équilibrée, stockage et lecture des cellules. Sa puissance et son courant permettent le réglage de 5,2 A sans être limités par le plafond de 65 W à 8,4 V. Sa notice originale et plusieurs photos permettent de modéliser l’extérieur sans ouvrir un appareil secteur.

## Caractéristiques et cotes

| Donnée | Valeur / statut |
| --- | --- |
| Alimentation | 100–240 V AC ; chargeur secteur avec cordon, distinct du S65neo et des B6 sans alimentation |
| Charge | 0,1–6 A, puissance maximale 65 W ; notre 2S à 5,2 A et 8,4 V demande au plus 43,68 W côté batterie |
| Batteries lithium | LiPo/LiIon/LiFe/LiHV de 2 à4 cellules ; choisir LiPo pour le pack Zeee standard |
| Équilibrage | 300 mA/cellule max selon notice originale V2.10 et page fabricant ; ne pas recopier 1 A de fiches tierces |
| Décharge | 0,1–2 A, limitée à 10 W ; cela limite fortement une décharge d’un gros pack |
| Dimensions retenues | 118 ×115 ×45 mm dans la notice fabricant V2.10, page PDF24, et page fabricant actuelle |
| Cote alternative rencontrée | 117 ×105 ×55 mm dans des fiches distributeurs : divergence conservée, aucune mesure physique |
| Masse / affichage | 315 g annoncés, LCD 2×16 rétroéclairé bleu, quatre boutons |
| Connectique | XT60 en face avant, port d’équilibrage XH 2–4S et prise de sonde thermique ; genre physique des contacts à vérifier |
| Contenu manuel | Chargeur + cordon secteur, PDF23 ; rallonges de charge/équilibrage non annoncées dans ce contenu |

## Achat Amazon et disponibilité

[Recherche Amazon.fr SkyRC S65 SK-100152](https://www.amazon.fr/s?k=SkyRC+S65+SK-100152). Une offre Amazon.de Marketplace est référencée par [Geizhals](https://geizhals.de/skyrc-s65-ac-2-4s-6a-65w-ladegeraet-sk-100152-02-a3309283.html), mais la redirection est bloquée. **ASIN et offre française non confirmés** ; ce lien de recherche n’est pas une offre vérifiée.

**Aucun prix en euros, vendeur, stock ou frais livrés n’est inventé.** Les deux identifiants confirmés le sont sur Amazon.com ; un changement de domaine ne prouve pas une offre en France.

## Documents et modèle

[Notice d’intégration du projet](notices/notice-integration-v3.md), [recherche, avis et informations manquantes](recherche-technique.md), [sources structurées](sources.json), [photos constructeur](photos/README.md), [liste des originaux](assets.json).

[Modèles STEP, aperçus et provenance](3D/README.md).

[Référence technique fabricant](https://www1.skyrc.com/s65?from=nav). [Architecture et dimensionnement de l’alimentation](../alimentation/README.md).
