<!-- surveillance-m1 -->
> **Surveillance M1 : WARN1/2 sont actifs hauts**, rappels 47 kohms au 3,3 V côté Pi. [Contrat courant](../carte-surveillance-electrique/integration.md). Les 13 contacts restent inchangés ; anciens PDF datés.
<!-- /surveillance-m1 -->

<!-- vitesse-r1 -->
> **Extension capteurs de vitesse du15octobre2026 :** faisceau actuel à13 contacts montés,18 à provisionner avec5 de réserve. Ajouts : pins16/18 (GPIO23/24),17 (3,3 V) et25 (GND). La puissance5 V reste séparée. [Raccordement actuel](../capteurs-vitesse/integration.md). Les modèles et notices GPIO antérieurs sont des instantanés.
<!-- /vitesse-r1 -->

<!-- alimentation-r2 -->
> **Sélection active révisée le 15 octobre 2026.** Molex conservé pour neuf signaux. Six positions de puissance non câblées dans cette prise. Alimentation Pi séparée : deux positifs et quatre retours courts en 18 AWG soudés aux pads du connecteur Pi ; les anciens quinze fils et leur STEP sont historiques.
> [État électrique courant](../verification-alimentation/README.md) · [Raccordements](../verification-alimentation/integration.md). Les références différentes dans les documents ci-dessous sont historiques. Qualification matérielle non réalisée ; confirmations restantes explicites.
<!-- /alimentation-r2 -->

# Connecteur GPIO et faisceau du Raspberry Pi 5

**Sélection d’étude du 14 octobre 2026 : Molex 22-55-2401, avec 15 contacts 16-02-0103, cinq contacts de réserve et fil multibrin Adafruit 3175 de 22 AWG.** Boîtier femelle à 40 positions, 2 × 20 au pas de 2,54 mm. Les contacts sont vendus séparément. Aucun achat, câblage ni essai physique réalisé.

Cette liaison reprend les deux commandes ESC, la direction, WARN1/WARN2 et DONE. Elle prévoit aussi les arrivées 5 V régulées et les retours de la branche Pi selon l’architecture existante. Les broches physiques ne sont pas les numéros GPIO BCM.

## Dossier

- [Notice PDF de montage](notices/notice-connecteur-gpio-v3.pdf) et [documents fabricant originaux](notices/README.md).
- [Cotes et statut des dimensions](cotes.md), [intégration et brochage](integration.md), [brochage structuré](brochage.json).
- [Recherche et informations manquantes](recherche-technique.md), [devis et liens d’achat](devis.md), [nomenclature](nomenclature.json).
- [STEP, aperçus et provenance](3D/README.md), [photos et crédits](photos/README.md).
- [Sources](sources.json), [archives et empreintes](assets.json), [calculs](calculs.json), [contrôles](validation-dossier.json).

## Achat

Les liens Amazon sont des recherches par référence : aucun ASIN, prix TTC français ou stock exact confirmé. Les fiches distributeur identifiées sont conservées dans le devis ; les prix consultés aux États-Unis ne constituent pas un panier livré en France. Le coût de l’outillage de sertissage reste distinct et non chiffré.

## Géométrie et raccordement

Le boîtier utilise une **CAO originale Molex**, archivée intacte. Les variantes de lecture tournent cette géométrie et lui donnent le noir de résine indiqué dans la fiche. Les contacts et la pose des fils sont reconstruits et signalés comme estimés. Les fils se terminent volontairement sans connecteurs aval dans le modèle d’implantation ; ce sont des extrémités de pose, pas des câbles prêts à brancher.

Les GPIO sont en 3,3 V. Le BEC 6 V du premier ESC alimente le servo selon le dossier direction ; il ne rejoint ni GPIO, ni les rails 5 V du Pi. Le positif BEC du second ESC reste isolé. Le seuil logique des ESC et l’alimentation Pi à 5 A restent à qualifier.

[Raspberry Pi retenu](../raspberry-pi-5/README.md), [refroidisseur](../refroidissement-raspberry-pi-5/README.md), [surveillance 2S](../protection-batterie/integration.md).
