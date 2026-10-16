<!-- surveillance-m1 -->
> **Suite active du 15 octobre 2026 :** [carte de surveillance M1](carte-surveillance-electrique/README.md). Ordre : surveillance, support caméra, supports capteurs, châssis, visserie finale. Les reports de phase ci-dessous sont historiques.
<!-- /surveillance-m1 -->

> **Alimentation R2 du15 octobre2026 :** [raccordements et qualification](verification-alimentation/README.md). Les descriptions ?lectriques pr?c?dentes sont historiques ; chargeS65 compl?t?e.

# Ensembles complémentaires avant châssis

14 octobre 2026. Dix dossiers de références au sein de quatre ensembles ; notice PDF, originaux disponibles, cotes, recherche d’achat, devis, avis et STEP par ensemble. Aucun achat ni essai matériel effectué.

| Ensemble | Dossier | Notice | Modèles |
| --- | --- | --- | --- |
| Commande servo / ESC | [Dossier](connecteurs-commande/README.md) | [PDF](connecteurs-commande/notices/notice-connecteurs-commande-v3.pdf) | [STEP](connecteurs-commande/3D/README.md) |
| Alimentation et mesure 2S | [Dossier](liaisons-alimentation-surveillance/README.md) | [PDF](liaisons-alimentation-surveillance/notices/notice-liaisons-alimentation-surveillance-v3.pdf) | [STEP](liaisons-alimentation-surveillance/3D/README.md) |
| Maintien batterie | [Dossier](maintien-batterie/README.md) | [PDF](maintien-batterie/notices/notice-maintien-batterie-v3.pdf) | [STEP](maintien-batterie/3D/README.md) |
| Coupure manuelle | [Dossier](coupure-manuelle/README.md) | [PDF](coupure-manuelle/notices/notice-coupure-manuelle-v3.pdf) | [STEP](coupure-manuelle/3D/README.md) |

## Achat et chiffrage partiel

Prix relevés sur les pages publiques indiquées dans chaque dossier, pour les quantités entières. Marchandises connues : 10,50 EUR pour commande (JR et une 413), 4,10 EUR pour liaisons (deux 413, une 415 et la rallonge), 11,99 EUR pour les deux feuilles silicone, 83,88 EUR pour ED80. **Sous-total EUR partiel : 110,47 EUR TTC, hors livraison**, hors embase XH et deux cosses 95R6 dont les prix restent ouverts. Ajouter les deux lots fabricant en devis USD : BNTECHGO 9,48 USD et GEPRC 5,99 USD, soit 15,47 USD avant taxes, import et livraison France non confirmés. Aucune conversion ni total global V3 validé.

L’offre Amazon.fr du silicone est identifiée par ASIN B08KFTBDF2. Pour les autres références, une recherche Amazon n’établit pas une offre exacte ; des liens fabricant ou distributeur sont proposés avec leur état de vérification. Les prix doivent être revalidés à la commande.

## Phase finale réservée

Schéma électrique et routage de la carte de surveillance, support caméra, visserie restante et châssis seront conçus ensemble à la fin. Aucun de ces éléments n’est dessiné dans les nouveaux fichiers.

Les poses de câbles, de sangles et de cosses sont provisoires. La coupure ED80 est ajoutée après MIDI, avant D+ ; les anciens documents de faisceau restent des instantanés sans ce dispositif. Les notices d’intégration actuelles renvoient à cette mise à jour.

L’interface XT60 du pack reste à qualifier pour les courants de l’étude. Coupure électrique ne signifie pas freinage instantané ; les fils d’équilibrage restent sous tension. Les objectifs de vitesse, autonomie et vidéo n’ont pas été validés par des essais.


<!-- cordon-principal-batterie-v3 -->
15 octobre 2026 : version active IC5 après le choix utilisateur, pack G1 SPMX50002S30H5 et cordon SPMXCA510 pré-câblé en 10 AWG. CP0+ vers entrée MIDI M5 ; CP0- vers D- N2, avec deux TE 130191. Après MIDI, ED80 et D+ restent en 6 mm². Variante XT60 non retenue ; courant et coordination du MIDI 60 A à qualifier. Charge IC5/S65 distincte à sélectionner avant charge.
<!-- /cordon-principal-batterie-v3 -->
