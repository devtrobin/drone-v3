# Première étude de faisabilité — V3

Consultation initiale : **12 octobre 2026** ; choix du calculateur mis à jour le **13 octobre 2026**. Les modèles caméra, moteur et carte de contrôle sont retenus pour l'étude ; le montage et le panier complet restent à valider.

## Vidéo : revoir la chaîne complète

Calculateur désormais retenu : [Raspberry Pi 5, 4 Go](Composants/raspberry-pi-5/README.md), seul pour vidéo, Wi-Fi et commande des deux variateurs. Caméra choisie : [InnoMaker U20CAM-4M USB UVC](Composants/camera/README.md), 1080p60 MJPEG annoncé. Tester la transmission MJPEG ou la conversion H.264 logiciel sur Pi 5 ; aucun résultat de chaîne complète n'est encore mesuré. Les paragraphes ci-dessous expliquent les limites des alternatives initiales.

Le [Pi Zero 2 W officiel](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) est spécifié pour l'encodage H.264 en 1080p30. Il ne constitue donc pas une base documentée permettant de garantir le 1080p60 demandé.

La [fiche officielle Camera Module 3](https://pip.raspberrypi.com/categories/786-raspberry-pi-camera-module-3) annonce notamment 1080p50. La [documentation des caméras](https://www.raspberrypi.com/documentation/accessories/camera.html) indique un mode 2304 × 1296 à 56 images/s pour ce module. Ces spécifications ne valident pas une acquisition native 1920 × 1080 à 60 images/s.

Il faut sélectionner ensemble le capteur, l'encodeur, le transport radio et le récepteur sur Mac. La mention commerciale « 1080p60 » devra concerner la sortie diffusée en direct, avec mesure des images uniques reçues et de la latence, plutôt que le seul enregistrement.

Le débit radio utile dépendra du codec et de la qualité retenus. À titre de comparaison, le brut RGB 24 bits représente 1920 × 1080 × 60 × 24 = **2,99 Gbit/s**, hors protocole : compression indispensable pour la piste Wi-Fi envisagée.

## Vitesse : nouvelle base mécanique à étudier

40 km/h = **11,11 m/s**, soit environ 18 fois l'estimation de vitesse V2. L'architecture retenue est un **châssis fabriqué à quatre roues : deux moteurs arrière et deux roues avant non motrices dédiées à la direction**. Prévoir deux variateurs, une réduction par roue arrière et un train avant orientable. Le [2435SL G3 à 4 500 KV](Composants/moteur/README.md) est retenu comme modèle moteur. Une voiture RC complète est exclue.

Avec des roues de diamètre 65 mm, atteindre 40 km/h demande environ **3 265 tr/min aux roues en charge**, d'après n = 60 × v / (π × D). Ce calcul cinématique ne détermine ni puissance moteur, ni rapport de transmission, ni vitesse réelle.

À 40 km/h, un retard vidéo de 100 ms correspond à **1,11 m parcouru** avant l'apparition de l'image ; 200 ms correspondent à **2,22 m**. Il faut encore ajouter réaction du pilote et distance de freinage. Les essais progresseront à partir d'une vitesse limitée, après validation de la commande et du freinage.

## Autonomie : distinguer énergie et durée de conduite

La V2 estime 4 h 53 avec 28,305 Wh disponibles en sortie USB et 5,8 W supposés. Cette estimation concerne une base lente ; elle ne s'applique pas à une propulsion V3.

À titre de scénario énergétique, avec **30 Wh utilisables** pour l'ensemble du véhicule :

| Puissance moyenne totale supposée | Durée calculée |
| --- | --- |
| 6 W | 5 h |
| 20 W | 1 h 30 |
| 40 W | 45 min |
| 80 W | 22 min 30 s |

Ces puissances illustrent la relation durée = énergie / puissance ; elles ne prédisent pas la consommation V3. Une autonomie de cinq heures avec 30 Wh impose une moyenne de seulement 6 W, vidéo et propulsion comprises. La faisabilité dépend donc fortement de la part de conduite lente, des arrêts et des pointes rapides.

## Budget : conclusion provisoire

Le dossier ne permet pas encore d'affirmer que les trois objectifs peuvent être réunis à 200 €. Il faut comparer des paniers complets, avec chargeur, alimentation vidéo, commande, fixations et livraison, et déclarer les éventuelles pièces réutilisées. Le panier V2 à 257,03 € n'est pas une base de coût compatible par simple ajout.

Le dimensionnement vise 10 à 20 minutes à 40 km/h et au moins 45 minutes à 20 km/h. À la demande de l'utilisateur, on chiffre d'abord les performances demandées, puis on recherche les économies et compromis pour revenir vers l'objectif initial de 200 € pour tout le matériel neuf. L'estimation V2 de plusieurs heures n'est plus la cible de dimensionnement. Voir le [dimensionnement](dimensionnement.md) et les [pistes techniques](pistes-techniques.md).
