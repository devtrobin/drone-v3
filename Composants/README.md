<!-- complements-r3 -->
> **RévisionR3 :** [armature, cordons, visserie et revue électrique](complements-finalisation-r3/README.md). La brancheFT5335M+UBEC6V n’est pas validée sur toute la plage2S ; les réservations3D ne constituent pas un panier validé.
<!-- /complements-r3 -->

<!-- finalisation-r2 -->
> **Finalisation du16octobre2026 :** [mécanique/intégration/électricitéR2](finalisation-theorique-r2/README.md), [visserie](visserie-finale/README.md), [servo proposéFT5335M](servo-direction/ft5335m-r2/README.md), [alimentation de direction](alimentation-direction/README.md), [interfacePWM isolée](interface-pwm-isolee/README.md). Révision d’étude sous conditions, pas de panier intégral validé.
<!-- /finalisation-r2 -->

> **Surveillance M1P :** [porteuse pour fabrication de prototype et banc limit?](carte-surveillance-electrique/fabrication/README.md). Gerbers et proc?dure pr?par?s ; aucun essai r?alis?, cotes TI exactes et raccordement LiPo non lib?r?s.

<!-- surveillance-m1 -->
> **Surveillance active M1 :** [dossier, schéma, routage et CAO](carte-surveillance-electrique/README.md). Remplace le concept TLV6700 pour cette étude ; WARN maintenant actif haut. [Ordre de conception](../PLAN-CONCEPTION.md).
<!-- /surveillance-m1 -->

> **État actif de l’alimentation : révision du 15 octobre 2026.** [Audit et corrections](verification-alimentation/README.md), [cordon de charge S65–IC5](cordon-charge-s65-ic5/README.md). Les anciens calibres MIDI/ATO, le FLRY-B et le D24V90F5 restent des choix historiques ; suivre la nomenclature révisée.

> **Révision du 15 octobre 2026 : batterie 2S G1 IC5 et cordon 10 AWG proposés après le choix utilisateur.** [État courant](cordon-principal-batterie/README.md). Les anciens plans/PDF Zeee restent datés. Charge S65 initiale à 5 A, avec un raccord IC5 distinct à sélectionner avant charge.

# Composants — Drone V3

Un dossier par composant du drone. Chaque fiche conserve la référence exacte, le lien d'achat, le prix daté, les sources techniques et les vérifications encore nécessaires.

| Composant | Référence retenue pour l'étude | Prix relevé | État |
| --- | --- | ---: | --- |
| [Châssis plateau ouvert](chassis/README.md) | A2-R1, aluminium 520 x 300 x 3, pont et portique arrière | Matière à chiffrer | STEP, plans PDF/DXF et débit ; interfaces à présenter, essais physiques restants |
| [Supports des capteurs de vitesse](supports-capteurs-vitesse/README.md) | P1 : deux stations et deux rotors à aimants captifs | À fabriquer | Fixations prévues sur A2-R1 ; hauteur relative 20,5 mm, essais restants |
| [Support caméra provisoire](support-camera/README.md) | P1 : base et montant bois, berceau à un pivot | À fabriquer / chutes | STEP, plan coté, DXF et notice ; hauteur190-230 mm, remplaçable |
| [Caméra](camera/README.md) | InnoMaker U20CAM-4M, capteur OV4688, USB 2.0 UVC | 23,00 € TTC | Non achetée ; 1080p60 annoncé, essai matériel à faire |
| [Moteur](moteur/README.md) | Hobbywing QuicRun 2435SL G3, 4 500 KV ; offre avec WP16BL30 G2 | 66,34 € TTC par kit | Non acheté ; deux moteurs et deux variateurs retenus pour les roues arrière ; direction avant non motrice |
| [Carte de contrôle](raspberry-pi-5/README.md) | Raspberry Pi 5, 4 Go | À vérifier | Retenu le 13 octobre 2026, non acheté ; Wi-Fi, vidéo et commande des deux variateurs sur une seule carte |
| [Roues](roues/README.md) | HobbyPark Touring Color A, 63 × 26 mm, pré-collées, ASIN B0CTNVV7BJ | À vérifier | Lot de quatre retenu le 13 octobre 2026 ; deux roues arrière motrices, deux avant pour la direction ; non acheté |
| [Servo de direction](servo-direction/README.md) | FEETECH FT90M-C001, micro-servo à engrenages métalliques | À vérifier | Choix de conception ; couple selon masse et géométrie à valider |
| [Fusées avant](fusees-avant/README.md) | Tamiya 51002, pièces A7/A6 et renvois A1/A8 | À vérifier | Famille documentée ; adaptation au châssis à fabriquer |
| [Axes avant](axes-avant/README.md) | Tamiya 50823, deux axes métalliques | À vérifier | Roues avant libres ; pas de cardans de propulsion à l'avant |
| [Moyeux](moyeux/README.md) | Tamiya 53569, quatre moyeux serrés de 6 mm | À vérifier | Interface avec roues à vérifier sur pièces reçues |
| [Roulements](roulements/README.md) | MR115ZZ 5×11×4, douze prévus | À vérifier | Fiche SMB ; fournisseur et jeux à arrêter |
| [Biellettes](biellettes-direction/README.md) | Chapes 50596, rotules 50592, tiges M3 | À vérifier | Sous-dossiers par composant ; longueurs après implantation |
| [Transmissions arrière](transmission-arriere/README.md) | Losi 16T/Ø2 + KHK 54T et 24T/Ø5 ; deux étages | À vérifier | Rapport 7,59375 ; angle de pression du couple Losi/KHK et endurance à vérifier |
| [Arbres de transmission](arbres-transmission/README.md) | Deux intermédiaires Ø5 et deux sorties Ø5/M4 | Fabrication à chiffrer | Références de fabrication ; plans après implantation |
| [Paliers et fourches](paliers-transmission/README.md) | Supports V3 adaptés aux interfaces retenues | Fabrication à chiffrer | Modèles 3D d’étude ; dimensions et fabrication à valider |
| [Fixations du train roulant](fixations-train-roulant/README.md) | Goupilles 2×10, écrous M4 et vis de pivot Tamiya | À vérifier | Contenus des sachets et doublons à contrôler |
| [Batterie](batterie/README.md) | Zeee LiPo 2S 7,4 V, 5 200 mAh, XT60, coque rigide ; ASIN B08DCYVHSF | À vérifier | Un pack embarqué ; référence Amazon.com identifiée, offre française non confirmée |
| [Alimentation Pi](regulateur-alimentation/README.md) | Pololu D24V90F5, 5 V ; ASIN B01M9C9Q1E | À vérifier | Courant disponible selon tension et température ; qualification avec les moteurs nécessaire |
| [Chargeur](chargeur-batterie/README.md) | SkyRC S65 SK-100152, secteur, 65 W / 6 A | À vérifier | Référence documentée ; ASIN et offre française non confirmés ; appareil hors véhicule |
| [Surveillance électrique M1](carte-surveillance-electrique/README.md) | 2 TPS3700EVM-114, 2 TMR 1-0511, Pololu 2831 et porteuse | Devis partiel | Schéma/routage KiCad contrôlés, notice et STEP ; cotes TI et qualification matérielle restantes |
| [Interrupteur de branche Pi](protection-batterie/interrupteur-pi/README.md) | Pololu 2813 HP | À vérifier | Choix d’étude ; courant moteurs hors de cette carte ; CAO officielle |
| [Coupure de puissance moteurs](protection-batterie/coupure-moteurs/README.md) | Sensata/Crydom D1D100, version à vis | À vérifier | Choix d’étude ; HS251 proposé pour le refroidissement ; comportement sous charge à valider |
| [Dissipateur du relais](dissipateur-relais/README.md) | Sensata/Crydom HS251 + une interface HSP-1 | À vérifier | STEP officiel et assemblage disponibles ; enveloppe thermique d'étude 40 A / 40 °C, non testée ; offre Amazon non confirmée |
| [Porte-fusible principal](protection-surintensite/porte-fusible/README.md) | Littelfuse 04980900ZXT, MIDI/BF1, goujons M5 | À vérifier | Support avec capot, sans fusible ni fils ; reconstructions STEP documentées |
| [Fusible principal](protection-surintensite/fusible-60a/README.md) | Littelfuse 0498060.M, MIDI temporisé 60 A / 32 V DC | À vérifier | Calibre d'étude à qualifier avec le faisceau ; pouvoir de coupure du lot à vérifier ; Amazon non confirmé |
| [Distribution électrique](distribution-alimentation/README.md) | Deux Blue Sea MiniBus 2315, 100 A, quatre goujons #10-32, capots 2713 inclus | Amazon.fr à vérifier | Un rail positif et un rail négatif ; ASIN B000OTJ8A0 identifié sur Amazon.com ; notice, cotes et cinq STEP |
| [Porte-fusible de branche Pi](protection-branche-pi/porte-fusible/README.md) | Blue Sea 5065, ATO/ATC, fils 12 AWG, fusible séparé | À vérifier | ASIN B004ZIUA62 identifié sur Amazon.com ; offre Amazon.fr non confirmée ; dimensions du support estimées |
| [Fusible de branche Pi](protection-branche-pi/fusible-7-5a/README.md) | Littelfuse 0ATO07.5V, ATO 7,5 A / 32 V DC | À vérifier | Calibre d'étude ; pouvoir de coupure 1 000 A à qualifier avec la LiPo ; offre Amazon exacte non confirmée |
| [Porte-fusibles moteurs](protection-branches-moteurs/porte-fusible/README.md) | Deux Blue Sea 5065, ATO/ATC, fils 12 AWG | À vérifier | Un par départ ESC après le relais ; même référence que pour le Pi ; offre Amazon.fr non confirmée |
| [Fusibles moteurs](protection-branches-moteurs/fusible-30a/README.md) | Deux Littelfuse 0ATO030.V, ATO 30 A verts / 32 V DC | À vérifier | Calibre d'étude à 20 A par départ ; fils ESC 16 AWG et pouvoir de coupure 1 000 A à qualifier ; aucun ASIN exact confirmé |
| [Répartiteur après relais](repartition-moteurs/README.md) | nVent ERIFLEX UD-80A, article 569010, capot inclus | RS : 21,13 € TTC hors frais | Une arrivée, deux sorties utilisées ; 80 A IEC ; Amazon exact non confirmé ; CAO fabricant conservée intacte |
| [Connecteurs des départs ESC](connecteurs-alimentation/README.md) | Deux AMASS XT60H-F avec capots ; M déjà sur les ESC | À vérifier | Lot SoloGood 10 paires B074PN6N4K identifié sur Amazon.com ; livraison France non confirmée ; notice et huit STEP |
| [Câble des départs ESC](cable-puissance-12awg/README.md) | BNTECHGO SW12G68008F10C2, 12 AWG, deux fils rouge/noir 3,048 m chacun | Amazon.fr à vérifier | ASIN exact B01ABOPMEI, 680 brins annoncés, Ø4,5 mm ; notice, cotes et six STEP ; courant et passage de capot à qualifier |
| [Refroidissement du Pi 5](refroidissement-raspberry-pi-5/README.md) | Raspberry Pi Active Cooler SC1148, préassemblé |6,99 € TTC | Amazon.fr B0CLXZBR5P, stock affiché au 14 octobre 2026 ; non acheté ; quatre STEP |
| [Carte microSD](carte-microsd/achat-microsd-raspberry-pi-64go.pdf) | Raspberry Pi officielle SC1629, 64 Go, A2 / U3 / V30 | Reichelt : 47,22 € TTC hors port | Une carte ; fiche d’achat PDF ; Amazon exact non confirmé ; non achetée |
| [Connecteur GPIO et faisceau](connecteur-gpio/README.md) | Molex 22-55-2401 + contacts 16-02-0103 ; fil Adafruit 3175 | France à vérifier | CAO boîtier officielle, quatre STEP et notice ; 15 contacts montés en étude, non acheté |
| [Fixations du Pi 5](fixations-raspberry-pi-5/README.md) | Ewwtrey 335 pièces nylon noir M2.5, B0DCS5C7SN | 9,98 € TTC | En stock au relevé du 14 octobre ; non acheté ; quinze STEP ; hauteur provisoire, châssis en dernier |

Prix caméra et moteur relevés le **12 octobre 2026**, Amazon.fr. Livraison gratuite affichée dans la session consultée ; à revalider avant commande. Pour le Pi 5, référence Amazon identifiée le 13 octobre, mais offre, prix et disponibilité non vérifiés. Ce tableau ne constitue pas encore la nomenclature complète ni le budget final du drone.

La [sélection direction et transmission](direction-et-transmission/README.md) du 13 octobre 2026 comporte les sources, PDF originaux et calculs. Les [modèles 3D STEP, aperçus et contrôles](direction-et-transmission/3D/README.md) ont leur index commun et un dossier `3D` par composant. Les nouveaux liens Amazon sont des recherches par référence : offres, vendeurs et stock non confirmés. Les arbres et supports sont des modèles paramétriques d’étude dont les dimensions doivent être arrêtées avant fabrication.

La [sélection alimentation et charge](alimentation/README.md) conserve les recherches, notices, cotes et avis pour les trois nouvelles références. Ses [quatre STEP et contrôles FreeCAD](alimentation/3D/README.md) comprennent la batterie, le régulateur, le chargeur et son cordon. Les pages Amazon.fr étant inaccessibles lors de cette recherche, le panier français et son prix ne sont pas validés. Le dimensionnement énergétique reste conditionnel à la consommation mesurée.

La [protection de batterie](protection-batterie/README.md) est une proposition modulaire, avec fiches constructeur, notice PDF du projet et [trois STEP](protection-batterie/3D/README.md). La surveillance est une conception V3 non fabriquée ; aucune offre Amazon regroupant toutes les fonctions n’a été vérifiée. La qualification électrique et le routage restent à réaliser.

Le [refroidissement du relais](dissipateur-relais/README.md) est documenté avec six PDF fabricant, une notice V3 et [cinq STEP](dissipateur-relais/3D/README.md), dont l'original Sensata et l'assemblage d'étude. Les deux pads sont des variantes de lot alternatives. La sélection reste conditionnelle aux mesures de courant, de température et à une offre d'achat vérifiée.

La [protection principale contre les surintensités](protection-surintensite/README.md), étudiée le 14 octobre 2026, regroupe deux dossiers de composants, les documents et cotes, une notice PDF et quatre STEP. Le couple MIDI/M5 et le calibre de 60 A sont une sélection d'étude ; sections, courant prospectif et protections des départs restent à définir et qualifier.

La [distribution par deux MiniBus 2315](distribution-alimentation/README.md) est documentée avec plans et PDF constructeur, avis, cotes, notice V3 et [cinq STEP](distribution-alimentation/3D/README.md). Les deux capots sont inclus ; offre Amazon.fr, serrage du lot, cosses et protections de branches restent à vérifier.

La [protection du départ Pi](protection-branche-pi/README.md) associe un Blue Sea 5065 et un Littelfuse ATO 7,5 A pour l'étude. Documentation, avis, [cotes](protection-branche-pi/cotes.md), [notice PDF](protection-branche-pi/notices/README.md) et [six STEP contrôlés avec FreeCAD](protection-branche-pi/3D/README.md) sont conservés. Les cotes du support non publiées sont signalées comme estimées ; offre Amazon.fr, démarrage, faisceau et coordination des fusibles restent à qualifier.

Les [deux départs moteurs](protection-branches-moteurs/README.md) disposent chacun d'un Blue Sea 5065 et d'un ATO 30 A pour l'étude. Sources, avis, cotes, calculs, notice PDF et [cinq STEP contrôlés FreeCAD](protection-branches-moteurs/3D/README.md) sont conservés. Les protections sont placées après le relais commun ; raccord de répartition, faisceau, fils ESC 16 AWG, pointes et courant prospectif restent à qualifier. Trois supports 5065 prévus au total avec le Pi, aucun commandé.

Le [répartiteur après relais UD-80A](repartition-moteurs/README.md) est retenu pour l'étude : une unité avec capot, entrée 6–16 mm², deux petites sorties utilisées vers les 5065. Notices constructeur, recherche, cotes, notice V3 et [cinq STEP](repartition-moteurs/3D/README.md) sont conservés, dont l'original nVent intact. Prix RS France relevé le 14 octobre 2026, hors livraison ; Amazon exact non confirmé. Sertissage, serrage du lot et qualification du faisceau restent à réaliser.

Les [prises complémentaires des deux ESC](connecteurs-alimentation/README.md) retiennent deux AMASS XT60H-F avec capots. Documentation fabricant actuelle et historique, cotes, recherche et avis, notice V3 et [huit STEP colorés](connecteurs-alimentation/3D/README.md) sont conservés. Les détails non cotés sont estimés. Le catalogue 2026 donne 35 A sous conditions ; référence de travail prudente 30 A, scénario 20 A par ESC à qualifier. La prise commune de la batterie reste à vérifier séparément.

Le [câble 12 AWG rouge/noir](cable-puissance-12awg/README.md) est proposé pour les queues après ATO30 et les retours indépendants : BNTECHGO, deux longueurs de 3,048 m. Sources, image technique, avis, notice V3, calculs et [six STEP](cable-puissance-12awg/3D/README.md) sont conservés, dont trois coupes à 680 brins chacune et trois versions d'implantation. La gaine Ø4,5 ±0,1 mm remplace l'hypothèse Ø4,2 des anciens fils illustratifs ; capots, raccords, cosses et thermique à qualifier. Offre française et liste de coupe non validées.

<!-- faisceau-puissance-v3 -->

Le [faisceau de puissance](faisceau-puissance/README.md) complète la sélection : cosses Ancor12AWG, cosses Klauke6mm², manchons, ATUM8/2, colliers, embases et fil FLRY-B6mm². Huit dossiers, notice, sources, cotes et [quatorze STEP](faisceau-puissance/3D/README.md). Les mentions antérieures « à choisir » sont complétées par cette étude datée du14octobre2026 ; offresAmazon.fr, implantation, interface batterie et qualification matérielle restent ouvertes.

<!-- fixations-pi-v3 -->

Les [fixations isolantes du Pi 5](fixations-raspberry-pi-5/README.md) retiennent le kit Ewwtrey noir M2.5, 335 pièces, 9,98 € TTC sur Amazon.fr au 14 octobre 2026. Notice, devis, cotes, avis, documents originaux et [quinze STEP](fixations-raspberry-pi-5/3D/README.md). Montage à 10 mm provisoire ; hauteur, appuis et vis à confirmer lorsque le châssis sera conçu, en dernier.

<!-- /fixations-pi-v3 -->

<!-- complements-avant-chassis-v3 -->

Les compléments avant châssis sont regroupés dans quatre ensembles, avec un dossier par référence, notices PDF, originaux constructeur, cotes, devis, sources et STEP colorés :

- [Connecteurs et faisceau de commande](connecteurs-commande/README.md) : trois prises JR, huit contacts utilisés et séparation des PWM ; un seul BEC pour le servo.
- [Liaisons d’alimentation et de mesure](liaisons-alimentation-surveillance/README.md) : bornes WAGO, fil 18 AWG, interface XH trois positions et rallonge d’équilibrage 2S.
- [Maintien de batterie](maintien-batterie/README.md) : deux sangles GEPRC et un patin silicone provisoire, hors conception de châssis.
- [Coupure manuelle](coupure-manuelle/README.md) : Albright ED80-1 après MIDI et avant D+, avec deux cosses M6 ; coupe moteurs et Pi indépendamment du logiciel.

Décision utilisateur : **schéma et routage de surveillance, support caméra, visserie restante et châssis seront conçus ensemble à la fin**. Les anciens PDF de faisceau sont des instantanés ; la coupure ED80 remplace désormais la liaison directe MIDI vers D+. L’interface XT60 de la batterie et les performances restent à qualifier, aucune commande effectuée.

<!-- /complements-avant-chassis-v3 -->


<!-- cordon-principal-batterie-v3 -->
15 octobre 2026 : version active IC5 après le choix utilisateur, pack G1 SPMX50002S30H5 et cordon SPMXCA510 pré-câblé en 10 AWG. CP0+ vers entrée MIDI M5 ; CP0- vers D- N2, avec deux TE 130191. Après MIDI, ED80 et D+ restent en 6 mm². Variante XT60 non retenue ; courant et coordination du MIDI 60 A à qualifier. Charge IC5/S65 distincte à sélectionner avant charge.
<!-- /cordon-principal-batterie-v3 -->


<!-- capteurs-vitesse-v3 -->
## Capteurs de vitesse ajoutés le15octobre2026

[Ensemble documenté](capteurs-vitesse/README.md) : deux DRV5033AJQLPG, quatre aimants S-03-02-N, deux rappels10 kΩ et deux100 nF. Notice, cotes, devis, originaux constructeur et STEP par composant. Brochage GPIO actif à13 contacts ; anciens ensembles électriques datés conservés. Supports et rétention des aimants réservés au châssis final.
<!-- /capteurs-vitesse-v3 -->
