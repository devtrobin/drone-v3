<!-- finalisation-r2 -->
> **ÉtudeR2 du16octobre2026 :** [définition mécanique etimplantation révisées](../finalisation-theorique-r2/README.md). Les anciens arbres50mm etFT90M ne sont plus la définition nominaleR2 ; les réservations/interfaces non mesurées restent conditionnelles. Conserver les modèles/documents ci-dessous comme référencesA2-R1.
<!-- /finalisation-r2 -->

# Servomoteur de direction

**Choix de conception du 13 octobre 2026**, effectué sous l’autorisation de sélectionner les pièces. Non acheté, non testé ; aucune garantie de performance du véhicule.

Référence : **FEETECH FT90M-C001 / FT-90M0-C001**. Quantité prévue : **1 servo avec ses palonniers 20T et sa vis de sortie**.

Ce micro-servo reste compact et sa fiche publie un couple nominal, le courant et les niveaux logiques. Le signal 3,3 V du Pi est dans la plage haute publiée pour cette révision ; alimentation moteur du servo séparée des GPIO.

## Caractéristiques et rôle

| Donnée | Valeur / statut |
| --- | --- |
| type | Servo numérique de position, engrenages métalliques ; pas FT90MR continu |
| alimentation retenue | 6 V régulés |
| plage publiée | 3–8,4 V ; caractéristiques citées à 6 V |
| couple nominal conservateur | 0,7 kgf·cm (fiche 2020) ; page actuelle 0,76 |
| couple de blocage | 2,3 kgf·cm ; ne pas utiliser comme couple continu |
| courant à 6 V | 6 mA arrêté, 150 mA à vide, 350 mA nominal et 1 A bloqué (fiche 2020) |
| commande | Période 20 ms (50 Hz), 1000–2000 µs, neutre 1500 µs |
| niveaux logiques | Haut 2–5 V ; bas 0–0,45 V dans la fiche 2020 |
| sortie | 20 dents, Ø3,95 mm ; vis M2×4 |
| encombrement | 23,2×12,1×25,25 mm dans le plan historique ; hauteur 25,5 sur page actuelle |
| masse | 13,5 ± 1 g |

## Documents

[Notice d’intégration V3](notices/notice-integration-v3.md), [recherche et incertitudes](recherche-technique.md), [sources structurées](sources.json).

- [FEETECH-FT90M-fiche-historique-miroir.pdf](../direction-et-transmission/notices/FEETECH-FT90M-fiche-historique-miroir.pdf) : document original inchangé, conservé dans le dossier commun.

## Achat et validation

[Recherche Amazon France par référence](https://www.amazon.fr/s?k=FEETECH+FT90M+C001) — lien de recherche, **pas une offre vérifiée**. Aucun ASIN, prix en euros, stock ou livraison n’est inventé. Les pièces à fabriquer doivent également être chiffrées.

Sources techniques : [source 1](https://www.feetechrc.com/6v-2kg-digital-steering-gear.html), [source 2](https://www.gotronic.fr/art-servomoteur-ft90m-36023.htm).

[Vue d’ensemble direction et transmission](../direction-et-transmission/README.md). [Modèles STEP, aperçus et provenance](3D/README.md).
