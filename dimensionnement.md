# Dimensionnement initial — énergie et vitesse

**12 octobre 2026**. Calculs conditionnels ; aucune consommation ni performance V3 mesurée.

## Énergie disponible et puissance admissible

Scénario : batterie LiPo 2S, tension nominale 7,4 V, fraction d'énergie utilisable 80 %. Cette fraction réserve une marge globale ; elle n'est pas une mesure de la batterie et ne définit pas le seuil électrique de coupure.

E_utilisable = 7,4 × capacité_Ah × 0,80.

P_moyenne_max = E_utilisable / durée_heures. La puissance est celle prélevée à la batterie par **tous** les circuits : propulsion, vidéo, commande, direction et pertes.

| Capacité 2S | Énergie nominale | Énergie utilisable supposée | Maximum pour 45 min à 20 km/h | Maximum pour 20 min à 40 km/h | Maximum pour 10 min à 40 km/h |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2 200 mAh | 16,28 Wh | 13,02 Wh | 17,37 W | 39,07 W | 78,14 W |
| 3 000 mAh | 22,20 Wh | 17,76 Wh | 23,68 W | 53,28 W | 106,56 W |
| 5 000 mAh | 37,00 Wh | 29,60 Wh | 39,47 W | 88,80 W | 177,60 W |
| 5 200 mAh, choix V3 | 38,48 Wh | 30,78 Wh | 41,05 W | 92,35 W | 184,70 W |

Le scénario 3 000 mAh est un point de comparaison, pas une batterie retenue. Exemple : si vidéo, commande et conversion consomment ensemble 6 W **à la batterie**, il reste 17,68 W en moyenne pour propulsion et direction afin de tenir 45 minutes. Cette consommation de 6 W est illustrative.

Une batterie plus grosse ajoute masse, coût et encombrement. Les courants de pointe, connecteurs, résistance interne, température, fixation et chargeur doivent être vérifiés indépendamment de la durée énergétique.

**Choix d’étude du 13 octobre 2026 : [Zeee 2S 5 200 mAh XT60](Composants/batterie/README.md), un seul pack embarqué.** Sa capacité et ses 250 g sont annoncés, sans mesure sur notre exemplaire. La [branche Pi Pololu et le chargeur SkyRC S65](Composants/alimentation/README.md) ont leur dimensionnement détaillé : rendement supposé, limites de courant selon tension, alimentation du Pi sans USB PD et charge équilibrée. Pour l’objectif 45 minutes, les 41,05 W du tableau couvrent tous les circuits. Un second pack de réserve ne double pas cette autonomie sur une charge.

## Pourquoi l'autonomie ne suit pas simplement l'inverse de la vitesse

Modèle de travail, sur plat et à vitesse constante :

P_batterie(v) ≈ P_auxiliaires + [Crr × m × g × v + 0,5 × rho × CdA × v³] / rendement.

Il manque encore les masses, le roulement des pneus sur le sol choisi, la traînée et le rendement réel. Accélérations, virages et freinages ajoutent des pertes. À très basse vitesse, rendement et consommation du moteur peuvent aussi changer ; à l'arrêt, la vidéo continue de consommer.

L'autonomie peut donc augmenter en ralentissant sans tendre vers l'infini. La courbe finale devra venir de mesures à 0, 5, 10, 20, 30 et 40 km/h, dans les espaces permettant chaque essai.

## Transmission et espace de roulage

**Roues retenues le 13 octobre 2026 : [HobbyPark 63 × 26 mm](Composants/roues/README.md).** À leur diamètre nominal de 63 mm, compter environ **1 684 tr/min à 20 km/h** et **3 368 tr/min à 40 km/h**. Le rayon roulant sous charge reste à mesurer. Le rapport de 9,9 environ avec 4 500 KV × 7,4 V est seulement une comparaison à vide, pas un choix de réduction validé.

**Réduction retenue pour l'étude le 13 octobre : [deux étages, 16→54 puis 24→54](Composants/transmission-arriere/README.md), i=7,59375.** Atteindre 40 km/h nominalement demande environ **25 578 tr/min moteur** et **7 579 tr/min sur l'arbre intermédiaire**. Le calcul à vide à 7,4 V donne environ 52,1 km/h, sans garantir 40 km/h en charge. Appairage Losi/KHK, charge, rendement et endurance restent à valider. Les [calculs de servo](Composants/direction-et-transmission/integration.md) sont eux aussi fondés sur une hypothèse de masse et de géométrie, pas sur un véhicule pesé.

Avec des roues de 65 mm : 1 632 tr/min à 20 km/h et 3 265 tr/min à 40 km/h, en charge.

Exemple de moteur 4 500 KV sous 7,4 V : régime théorique à vide de 33 300 tr/min. Un rapport moteur/roue de 10,2 correspond seulement à 40 km/h **à vide et à tension nominale** ; charge et tension de batterie changent le résultat. Cette valeur ne doit pas devenir un choix de pignons sans courbe de couple, bilan d'efforts et essais.

À 40 km/h, avec une décélération supposée constante de 3 m/s², la distance de freinage théorique v²/(2a) vaut 20,6 m. Un délai total de 200 ms ajoute 2,22 m. À 20 km/h, ces valeurs deviennent 5,14 m et 1,11 m. Ce sont des scénarios pour dimensionner l'espace, pas des performances de freinage promises.

Pour une accélération latérale limitée par hypothèse à 3 m/s², le rayon v²/a vaut 41,2 m à 40 km/h et 10,3 m à 20 km/h. La vitesse maximale ne sera donc pas la vitesse de chaque virage intérieur. Définir une limitation de direction selon la vitesse et mesurer adhérence, stabilité et freinage.

## Validation de l'autonomie

Mesurer vitesse réelle, Wh prélevés, tension, courant et température avec vidéo active. Faire des essais distincts pour 20 et 40 km/h, puis pour les vitesses inférieures. Distinguer vitesse stabilisée, parcours avec virages et moyenne de trajet. Des essais avec échange de batteries ne valident pas les durées sur une seule charge.
