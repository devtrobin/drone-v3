<!-- alimentation-r2 -->
> **Sélection active révisée le 15 octobre 2026.** D24V90F5 retiré de la sélection active : D42V55F5 / Pololu 5571, 5 V ±3 %, dropout plus faible. CAO officielle dans le sous-dossier d42v55f5 ; vérifier le brochage, différent de l’ancien modèle.
> [État électrique courant](../verification-alimentation/README.md) · [Raccordements](../verification-alimentation/integration.md). Les références différentes dans les documents ci-dessous sont historiques. Qualification matérielle non réalisée ; confirmations restantes explicites.
<!-- /alimentation-r2 -->

# Régulateur de la branche Raspberry Pi

Choix d’étude du **13 octobre 2026** : **Pololu D24V90F5 — article 2866, sortie fixe 5 V**. Non acheté, non testé.

Un régulateur embarqué pour Pi 5, caméra et refroidissement ; pas pour les moteurs.

Sa courbe de courant procure de la marge par rapport à une branche Pi de 5 A, y compris aux tensions d’une 2S. Le dropout lu à 5 A est compatible avec une entrée de 6,4 V en régime nominal, mais les creux dus aux moteurs doivent être mesurés. Sa CAO officielle fournit une référence mécanique bien plus précise qu’une reconstruction du circuit.

## Caractéristiques et cotes

| Donnée | Valeur / statut |
| --- | --- |
| Type | Abaisseur synchrone DC-DC ; sortie nominale fixe 5 V, précision publiée ±4 % |
| Entrée | 5–38 V annoncés ; limite basse effective = sortie + dropout dépendant du courant |
| Courant | Nom de produit « 9 A » ; débit continu réel selon tension, température et refroidissement. Pas 9 A garantis partout. |
| Lecture des courbes fabricant | Vers 5 A de sortie, dropout ≈1 V ; courbe continue ≈6,7 A à 6,5 V d’entrée. Lectures approximatives, pas des garanties. |
| Cotes | PCB nominal 40,64 × 20,32 mm ; épaisseur 1,57 mm ; enveloppe CAO officielle relevée dans sa provenance |
| Fixation | Quatre trous Ø2,18, entraxes 35,56 ×15,24 mm ; tolérances fabricant de perçage ±0,1 et bord ±0,3 mm |
| Connexions | VIN, GND, VOUT, EN, PG, FB ; prendre la puissance aux grands pads, pas au petit VOUT près de FB |
| Rendement | 80–95 % typiques suivant charge/tension ; utiliser 90 % comme hypothèse de calcul, pas comme valeur mesurée |
| USB-C / PD | Aucun port USB-C ni source USB Power Delivery dans ce régulateur |
| Protections intégrées | Inversion d’entrée, courts-circuits/surintensité, température, démarrage progressif et verrouillage basse tension selon fabricant |

## Achat Amazon et disponibilité

ASIN identifié : **B01M9C9Q1E**, [fiche Amazon.com consultée](https://www.amazon.com/dp/B01M9C9Q1E). [Même identifiant sur Amazon.fr](https://www.amazon.fr/dp/B01M9C9Q1E) : accès indisponible dans cette session, présence commerciale française et achat livrable **non confirmés**.

**Aucun prix en euros, vendeur, stock ou frais livrés n’est inventé.** Les deux identifiants confirmés le sont sur Amazon.com ; un changement de domaine ne prouve pas une offre en France.

## Documents et modèle

[Notice d’intégration du projet](notices/notice-integration-v3.md), [recherche, avis et informations manquantes](recherche-technique.md), [sources structurées](sources.json), [photos constructeur](photos/README.md), [liste des originaux](assets.json).

[Modèles STEP, aperçus et provenance](3D/README.md).

[Référence technique fabricant](https://www.pololu.com/product/2866). [Architecture et dimensionnement de l’alimentation](../alimentation/README.md).
