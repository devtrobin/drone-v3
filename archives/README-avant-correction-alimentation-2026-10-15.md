> **Révision du 15 octobre 2026 : batterie 2S G1 IC5 et cordon 10 AWG proposés après le choix utilisateur.** [État courant](Composants/cordon-principal-batterie/README.md). Les anciens plans/PDF Zeee restent datés. Charge S65 initiale à 5 A, avec un raccord IC5 distinct à sélectionner avant charge.

# Drone terrestre V3

Étude commencée le **12 octobre 2026**. Objectif budgétaire initial : **200 € pour tout le matériel neuf** ; dimensionner d'abord pour les performances demandées, puis rechercher les économies et compromis. Châssis à fabriquer avec composants séparés, sol plat intérieur, pilotage par Wi-Fi depuis le Mac. Retour vidéo réel en 1920 × 1080 à 60 images/s ; autonomie de 10 à 20 minutes à 40 km/h et d'au moins 45 minutes à 20 km/h.

Cette version est au stade du cadrage. Aucun panier, montage ou résultat physique n'est validé. Voir les [spécifications](SPECIFICATIONS.md) et l'[étude de faisabilité](faisabilite.md).

Les références retenues progressivement sont regroupées dans [Composants](Composants/README.md). Première sélection : [caméra InnoMaker U20CAM-4M](Composants/camera/README.md), Amazon.fr, 23,00 € TTC au relevé du 12 octobre 2026, 1080p60 MJPEG annoncé ; contrôle matériel à faire.

Carte de contrôle retenue le **13 octobre 2026** : [Raspberry Pi 5 de 4 Go](Composants/raspberry-pi-5/README.md), seul pour la vidéo, le Wi-Fi et la commande des deux variateurs moteurs. Documentation et intégration prévisionnelle conservées dans son dossier ; montage non encore testé.

Train roulant retenu : deux moteurs arrière et deux roues avant non motrices pour la direction. [Roues HobbyPark Touring Color A, 63 × 26 mm](Composants/roues/README.md), lot de quatre pré-collées choisi le 13 octobre ; documentation, photos et STEP d'une roue conservés dans son dossier. Moyeux, transmission et direction restent à dimensionner.

La [direction et les transmissions](Composants/direction-et-transmission/README.md) disposent désormais de dossiers par composant : servo FT90M, fusées/axes Tamiya, moyeux, roulements, biellettes, engrenages et pièces d'adaptation à fabriquer. Les [modèles STEP colorés et leurs aperçus](Composants/direction-et-transmission/3D/README.md) reprennent les cotes documentées et indiquent les estimations ; arbres et supports restent des études à valider. Réduction d'étude 7,59375 ; montage, interfaces, prix et essais restent à valider.

La [batterie, l’alimentation du Pi et le chargeur](Composants/alimentation/README.md) sont documentés : Zeee 2S 5 200 mAh XT60, Pololu D24V90F5 et SkyRC S65. Chaque référence dispose de sources, notices ou notes d’intégration, photos, avis et modèles STEP détaillés. Le [catalogue 3D](Composants/alimentation/3D/README.md) inclut le cordon secteur séparé. Les offres Amazon françaises et l’autonomie réelle restent à vérifier ; distribution, protections et faisceau sont les prochains éléments à définir.

La [surveillance et la coupure de batterie](Composants/protection-batterie/README.md) disposent d’une étude modulaire : carte analogique 2S V3 à fabriquer, Pololu 2813 HP pour la branche Pi et Crydom D1D100 pour les moteurs. Sources, calculs, notice PDF et trois STEP sont conservés. Le [refroidissement par HS251 et HSP-1](Composants/dissipateur-relais/README.md) dispose de sa documentation et de cinq STEP, dont la CAO officielle et l'assemblage d'étude. Il reste à qualifier les circuits et la thermique, produire le schéma/routage et sélectionner faisceau et protections ; aucun montage ni panier Amazon n’est validé.

Les dossiers V1 et V2 restent les références historiques. La V3 ne reprend pas automatiquement leurs composants ni leurs contraintes d'achat.

Le [fusible principal et son porte-fusible](Composants/protection-surintensite/README.md), sélectionnés pour l'étude le **14 octobre 2026**, disposent de deux dossiers composants, des notices et cotes, des calculs et de quatre STEP détaillés. Calibre principal proposé : MIDI 60 A, sous réserve de coordination avec le faisceau et les défauts du pack. Les protections individuelles des ESC sont désormais proposées dans leur dossier ; aucun montage n'est testé.

La [distribution électrique](Composants/distribution-alimentation/README.md) retient deux Blue Sea MiniBus 2315 avec capots inclus : positif après le principal et retours négatifs séparés. Documentation, plans, cotes, avis, notice PDF et [cinq STEP](Composants/distribution-alimentation/3D/README.md) sont conservés. Offre Amazon.fr, couple du lot, cosses, faisceau et fusibles de branches restent à valider.

La [protection du départ Pi](Composants/protection-branche-pi/README.md) propose un porte-fusible Blue Sea 5065 et un Littelfuse ATO 7,5 A, au début du départ positif avant le Pololu 2813. Deux dossiers composants regroupent documentation, avis, cotes, calculs, notice PDF et [six STEP détaillés](Composants/protection-branche-pi/3D/README.md). Le calibre reste une étude : offre Amazon.fr, courant prospectif de la LiPo, sections, démarrage et coordination doivent être validés avant montage.

Les [protections des deux départs moteurs](Composants/protection-branches-moteurs/README.md) proposent deux 5065 et deux Littelfuse ATO 30 A, un ensemble par variateur après le relais. Documentation, avis, cotes, calculs, notice PDF et [cinq STEP détaillés](Composants/protection-branches-moteurs/3D/README.md) sont conservés. Hypothèse supplémentaire : 20 A par départ ; elle n'est pas imposée par les fusibles. Offre Amazon.fr, tenue des fils 16 AWG des ESC et coordination restent à qualifier. Le faisceau reste à sélectionner.

La [répartition en sortie du relais](Composants/repartition-moteurs/README.md) retient pour l'étude un nVent ERIFLEX UD-80A / 569010 avec capot, 80 A IEC. Une arrivée 6 mm² et deux petites sorties alimentent les porte-fusibles moteurs. Sources, notices et cotes, avis, calculs, notice V3 et [cinq STEP avec CAO fabricant intacte](Composants/repartition-moteurs/3D/README.md) sont disponibles. Offre RS France : 21,13 € TTC hors frais au relevé du 14 octobre 2026 ; pas d'offre Amazon exacte confirmée. Les différences IEC/UL de préparation des grosses bornes sont signalées ; câblage et qualification restent à terminer.

Les [connecteurs des deux départs ESC](Composants/connecteurs-alimentation/README.md) proposent deux AMASS XT60H-F avec capots pour les XT60 mâles existants. Notices et cotes fabricant, différences de révision, recherche Amazon et avis, procédure de montage et [huit STEP détaillés](Composants/connecteurs-alimentation/3D/README.md) sont disponibles. Le [câble BNTECHGO 12 AWG rouge/noir](Composants/cable-puissance-12awg/README.md) est désormais proposé pour les queues ; documentation, avis, cotes, notice V3 et [six STEP](Composants/cable-puissance-12awg/3D/README.md) sont disponibles, dont des modèles courts à 680 brins. Longueurs, raccords et cosses restent à définir ; courant individuel, capots et interface commune de batterie à qualifier. Prix et livraison Amazon.fr non confirmés.

## Travail à mener

1. Chiffrer tous les composants neufs sans déduire de réutilisation ; Mac existant supposé hors budget, comme dans V1/V2. Préciser les coûts de fabrication et le réseau disponible.
2. Dimensionner pour les durées confirmées avec vidéo active ; mesurer ensuite consommation selon vitesse, charge et terrain.
3. Comparer des propulsions et transmissions séparées pour un châssis fabriqué ; la base RC complète est écartée selon le choix utilisateur.
4. Sélectionner une chaîne caméra–encodeur–liaison–Mac capable de 1080p60, puis vérifier débit et latence.
5. Dimensionner batterie, alimentation, transmission, direction et freinage à partir des composants retenus.
6. Établir nomenclature, câblage, implantation, logiciel et protocole d'essais avant de finaliser la fabrication.

Le budget doit inclure batterie, chargeur, commande embarquée, vidéo, châssis, fixations, câblage et livraison. Aucune pièce de V1/V2 n'est considérée gratuite. Voir le [dimensionnement initial](dimensionnement.md) et les [pistes techniques](pistes-techniques.md).

<!-- faisceau-puissance-v3 -->

Le [faisceau de puissance](Composants/faisceau-puissance/README.md) complète la sélection : cosses Ancor12AWG, cosses Klauke6mm², manchons, ATUM8/2, colliers, embases et fil FLRY-B6mm². Huit dossiers, notice, sources, cotes et [quatorze STEP](Composants/faisceau-puissance/3D/README.md). Les mentions antérieures « à choisir » sont complétées par cette étude datée du14octobre2026 ; offresAmazon.fr, implantation, interface batterie et qualification matérielle restent ouvertes.

<!-- active-cooler-sc1148-v3 -->

Le [refroidissement du Pi 5](Composants/refroidissement-raspberry-pi-5/README.md) retient un Active Cooler officiel SC1148, préassemblé avec pads et clips. Amazon.fr B0CLXZBR5P :6,99 € TTC au 14 octobre 2026, port conditionnel. Sources, avis, cotes, notice PDF et [quatre STEP](Composants/refroidissement-raspberry-pi-5/3D/README.md), dont une version légère. Aucun montage testé ; courant USB / FAN, thermique et dégagements à qualifier.

La [carte microSD officielle Raspberry Pi de 64 Go](Composants/carte-microsd/achat-microsd-raspberry-pi-64go.pdf) est retenue pour le système et le logiciel du Pi 5. La fiche PDF contient le lien d’achat identifié et la recherche Amazon, dont l’offre exacte reste non confirmée.

<!-- connecteur-gpio-v3 -->

Le [connecteur GPIO et son faisceau](Composants/connecteur-gpio/README.md) retiennent un boîtier Molex à 40 positions et 15 contacts câblés pour l’étude. Documentation, devis, cotes, notice PDF et quatre STEP sont disponibles ; le boîtier possède une CAO fabricant archivée intacte. Prix français, insertion, thermique, seuils ESC et dégagements au cooler restent à vérifier.

<!-- fixations-pi-v3 -->

Les [fixations du Pi 5](Composants/fixations-raspberry-pi-5/README.md) disposent du dossier complet et de quinze STEP détaillés : kit Ewwtrey M2.5 nylon noir, 335 pièces, 9,98 € TTC au relevé Amazon.fr du 14 octobre 2026. Exemple de quatre supports à 10 mm, hauteur provisoire. **Le châssis sera le dernier composant conçu**, selon le choix utilisateur ; implantation et dimensions de fabrication restent ouvertes.

<!-- /fixations-pi-v3 -->

<!-- complements-avant-chassis-v3 -->

Les compléments avant châssis sont regroupés dans quatre ensembles, avec un dossier par référence, notices PDF, originaux constructeur, cotes, devis, sources et STEP colorés :

- [Connecteurs et faisceau de commande](Composants/connecteurs-commande/README.md) : trois prises JR, huit contacts utilisés et séparation des PWM ; un seul BEC pour le servo.
- [Liaisons d’alimentation et de mesure](Composants/liaisons-alimentation-surveillance/README.md) : bornes WAGO, fil 18 AWG, interface XH trois positions et rallonge d’équilibrage 2S.
- [Maintien de batterie](Composants/maintien-batterie/README.md) : deux sangles GEPRC et un patin silicone provisoire, hors conception de châssis.
- [Coupure manuelle](Composants/coupure-manuelle/README.md) : Albright ED80-1 après MIDI et avant D+, avec deux cosses M6 ; coupe moteurs et Pi indépendamment du logiciel.

Décision utilisateur : **schéma et routage de surveillance, support caméra, visserie restante et châssis seront conçus ensemble à la fin**. Les anciens PDF de faisceau sont des instantanés ; la coupure ED80 remplace désormais la liaison directe MIDI vers D+. L’interface XT60 de la batterie et les performances restent à qualifier, aucune commande effectuée.

<!-- /complements-avant-chassis-v3 -->


<!-- cordon-principal-batterie-v3 -->
15 octobre 2026 : version active IC5 après le choix utilisateur, pack G1 SPMX50002S30H5 et cordon SPMXCA510 pré-câblé en 10 AWG. CP0+ vers entrée MIDI M5 ; CP0- vers D- N2, avec deux TE 130191. Après MIDI, ED80 et D+ restent en 6 mm². Variante XT60 non retenue ; courant et coordination du MIDI 60 A à qualifier. Charge IC5/S65 distincte à sélectionner avant charge.
<!-- /cordon-principal-batterie-v3 -->
