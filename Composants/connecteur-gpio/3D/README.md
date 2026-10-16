<!-- vitesse-r1 -->
> **Extension capteurs de vitesse du15octobre2026 :** faisceau actuel à13 contacts montés,18 à provisionner avec5 de réserve. Ajouts : pins16/18 (GPIO23/24),17 (3,3 V) et25 (GND). La puissance5 V reste séparée. [Raccordement actuel](../../capteurs-vitesse/integration.md). Les modèles et notices GPIO antérieurs sont des instantanés.
<!-- /vitesse-r1 -->

> **Révision électrique du 15 octobre 2026 :** les assemblages complets avec MIDI, deux cosses CP0 ou alimentation par contacts Molex sont historiques. Les pièces unitaires conservées restent utilisables comme références géométriques. Consulter la sélection active avant toute implantation.

# STEP du connecteur GPIO

Le boîtier reprend la géométrie native Molex. Contacts et fils sont des reconstructions d’étude.

| Modèle | STEP | Aperçu | Taille |
| --- | --- | --- | --- |
| Molex 22-55-2401 : boitier officiel recolore | [STEP](molex-22-55-2401-boitier-noir.step) | [PNG](molex-22-55-2401-boitier-noir.png) | 2.00 Mo |
| Molex 16-02-0103 : contact reconstruit | [STEP](molex-16-02-0103-contact-detaille.step) | [PNG](molex-16-02-0103-contact-detaille.png) | 0.35 Mo |
| GPIO : boitier et 15 contacts | [STEP](connecteur-gpio-15-contacts-detaille.step) | [PNG](connecteur-gpio-15-contacts-detaille.png) | 7.28 Mo |
| GPIO : faisceau de pose avec 15 fils continus | [STEP](connecteur-gpio-faisceau-detaille.step) | [PNG](connecteur-gpio-faisceau-detaille.png) | 8.22 Mo |

[STEP original Molex, intact](sources/022552401.stp), [ZIP original](sources/Molex-22-55-2401-CAO-originale.zip), [métadonnées natives](source-native.json).

Le modèle équipé utilise quinze contacts, pas quarante contacts achetés ou montés. Les vingt-cinq cavités libres restent visibles. Les contacts colorés séparent or et étain ; leurs formes ne sont pas certifiées par un plan local.

Les quinze fils continus sont placés pour l’implantation, avec deux étages de courbure pour garder les rangées séparées. Les extrémités sont volontairement ouvertes ; aucune fiche RC aval fictive ajoutée. Ce STEP ne sert pas de liste de coupe.

[Provenance](provenance.json), [contrôles FreeCAD](validation-freecad.json), [cotes et jeux](../cotes.md), [notice](../notices/notice-connecteur-gpio-v3.pdf).
