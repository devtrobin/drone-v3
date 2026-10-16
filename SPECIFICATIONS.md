<!-- complements-r3 -->
> **RevueR3 du17octobre2026 :** objectifs40km/h,45min à20km/h et1080p60 inchangés. [DossierR3](Composants/complements-finalisation-r3/README.md) ; [conditions restantes](Composants/complements-finalisation-r3/conditions-restantes.md). L’alimentation de direction doit être revue pour couvrir les chutes en fin de pack ; aucune réduction implicite de performance ou d’autonomie n’est actée.
<!-- /complements-r3 -->

<!-- finalisation-r2 -->
> **ÉtudeR2 du16octobre2026 :** objectifs de vitesse/autonomie/vidéo conservés. Masse limite de calcul9kg etcharge avant45% ; valeurs non mesurées. FT90M insuffisant dans cette enveloppe ; propositionFT5335M avecalimentation dédiée etcommandes isolées. [Choix etconditions](Composants/finalisation-theorique-r2/README.md).
<!-- /finalisation-r2 -->

> **Alimentation r?vis?e le 15 octobre 2026.** Pack G1IC5, charge S65 +BEEC1067 et?quilibrage d?di? ; nouvellesprotections etalimentation Pi document?es dans [l?audit](Composants/verification-alimentation/README.md). Objectifs utilisateur inchang?s ; qualification restante explicite.

> **Révision du 15 octobre 2026 : batterie 2S G1 IC5 et cordon 10 AWG proposés après le choix utilisateur.** [État courant](Composants/cordon-principal-batterie/README.md). Les anciens plans/PDF Zeee restent datés. Charge S65 initiale à 5 A, avec un raccord IC5 distinct à sélectionner avant charge.

# Spécifications de cadrage — V3

Date initiale : **12 octobre 2026** ; choix de la carte de contrôle mis à jour le **13 octobre 2026**. Les valeurs ci-dessous sont des objectifs, pas des performances acquises.

| Fonction | Exigence ou point à préciser |
| --- | --- |
| Véhicule | Drone terrestre, dans la continuité de V1 et V2 |
| Budget | Objectif initial de 200 € pour tout le matériel neuf ; dimensionner et chiffrer d'abord les performances demandées, puis rechercher les économies et compromis ; inclure fabrication et livraison |
| Vitesse | Objectif de 40 km/h, avec autonomie à cette vitesse à valider |
| Autonomie à 40 km/h | Minimum visé 10 minutes ; objectif haut 20 minutes, vidéo active |
| Autonomie à 20 km/h | Au moins 45 minutes, vidéo active |
| Autonomie à vitesse inférieure | Rechercher une durée supérieure ; quantifier par essais, sans extrapolation inverse simple |
| Retour vidéo | 1920 × 1080, 60 images/s réellement acquises, transmises et affichées |
| Pilotage | Depuis le Mac existant, continuité de V1/V2 |
| Carte de contrôle | [Raspberry Pi 5, 4 Go](Composants/raspberry-pi-5/README.md), seul pour Wi-Fi, vidéo et commande des deux variateurs ; pas de microcontrôleur séparé retenu |
| Liaison | Wi-Fi ; exploiter sa portée utile avec vidéo active, sans portée chiffrée garantie |
| Terrain | Sol plat intérieur ; revêtement et espace disponible à relever |
| Fabrication | Châssis fabriqué, composants séparés ; pas de voiture RC complète ; conception du châssis en dernier, comme dernier composant (décision du 14 octobre 2026) |
| Architecture retenue | Quatre roues : deux roues arrière motrices, chacune avec son moteur et son variateur ; deux roues avant non motrices dédiées à la direction ; la bille avant est abandonnée |
| Roues retenues | [HobbyPark Touring Color A](Composants/roues/README.md), lot de quatre roues pré-collées 63 × 26 mm, empreinte hexagonale 12 mm ; non achetées, interfaces du train roulant à valider |
| Direction avant | [FT90M-C001](Composants/servo-direction/README.md), fusées Tamiya 51002, axes 50823, moyeux 53569 et biellettes documentés ; adaptation et couple à valider |
| Réduction arrière | [Deux étages par roue](Composants/transmission-arriere/README.md), 16→54 puis 24→54, i=7,59375 ; choix d'étude, appairage et performance en charge non validés |
| Latence | Mesurer le retard caméra–écran ; seuil d'acceptation à définir selon vitesse et distance de freinage |
| Arrêt | Freinage maîtrisé, arrêt sur perte de commande et absence de départ au démarrage ; à concevoir et tester |

Un flux enregistré localement en 1080p60 ne satisfait pas à lui seul l'exigence de retour vidéo. Un affichage à 60 Hz avec duplication d'images ne la satisfait pas non plus.

Les autonomies sont à obtenir sur une seule charge embarquée, sans échange de batterie pendant l'essai. Convention de dimensionnement à confirmer avant validation : vitesses réellement mesurées, vidéo active et énergie de tous les circuits incluse. Le réseau et le Mac déjà présents sont des infrastructures supposées ; tout équipement réseau supplémentaire requis doit être chiffré.

## Références antérieures

- V1 : cible d'autonomie minimale de 15 minutes et vidéo 720p30, sans résultat physique enregistré dans l'état du projet.
- V2 : cible minimale de 15 minutes ; estimation centrale de 4 h 53 à 5,8 W et environ 2,2 km/h. Ni autonomie ni vitesse mesurées.
- V2 : budget historique de 257,03 € hors livraison, déjà supérieur au plafond demandé pour V3.

Sources locales : [V1](../drone-v1/SPECIFICATIONS.md), [état V1](../drone-v1/project_state.md), [prévisions V2](../drone-v2/Mecanique/performance.md), [état V2](../drone-v2/project_state.md).

<!-- phase-finale-v3 -->

Ordre retenu le 15 octobre 2026 : [carte de surveillance électrique avec schéma et routage](Composants/carte-surveillance-electrique/README.md), support caméra, supports des capteurs, châssis, puis visserie finale. La porteuse M1 utilise cinq modules existants ; ses contrôles KiCad réussissent. Les dimensions exactes des EVM, le devis et les essais matériels restent à confirmer avant fabrication définitive. Voir le [plan de conception](PLAN-CONCEPTION.md).

Les [quatre ensembles de compléments](Composants/README.md) sont documentés. Coupure manuelle proposée : **batterie → MIDI → ED80 → D+**. C’est une ouverture du positif commun, indépendante du Pi ; elle n’assure ni freinage instantané, ni isolation des fils d’équilibrage, ni arrêt télécommandé de sécurité. Qualification de l’interface batterie XT60 et des courants toujours ouverte.

<!-- /phase-finale-v3 -->


<!-- cordon-principal-batterie-v3 -->
15 octobre 2026 : version active IC5 après le choix utilisateur, pack G1 SPMX50002S30H5 et cordon SPMXCA510 pré-câblé en 10 AWG. CP0+ vers entrée MIDI M5 ; CP0- vers D- N2, avec deux TE 130191. Après MIDI, ED80 et D+ restent en 6 mm². Variante XT60 non retenue ; courant et coordination du MIDI 60 A à qualifier. Charge IC5/S65 distincte à sélectionner avant charge.
<!-- /cordon-principal-batterie-v3 -->
