# Recherche technique - Raspberry Pi 5 de 4 Go

Recherche du **13 octobre 2026**, sur documentation officielle Raspberry Pi et documents déjà conservés pour la caméra et les variateurs. Aucun essai matériel. Le choix utilisateur porte sur le Pi 5 seul comme carte de contrôle.

## Ce qui est établi et ce qui reste à confirmer

| Point | Preuve disponible | Limite / contrôle restant |
| --- | --- | --- |
| Modèle et RAM | Pi 5 de 4 Go retenu ; titre Amazon B0CK3L9WD3 correspondant | Offre livrable, prix, vendeur et contenu du colis non vérifiés |
| Caméra | USB hôte sur Pi 5 ; caméra UVC sous Linux dans sa notice | Reconnaissance du modèle exact et acquisition 60 images uniques à vérifier |
| Vidéo H.264 | Encodage logiciel sur Pi 5 ; étude constructeur avec mesures 1080p30 et extrapolation 1080p60 | Pas une mesure de notre chaîne MJPEG USB, encodage, Wi-Fi et affichage Mac |
| Deux commandes moteur | RP1 : canaux PWM indépendants ; routage GPIO12/13 publié | Pilote, multiplexage, signal électrique, impulsions et calibration ESC à tester |
| Alimentation | 5 V / 5 A USB-C dans la fiche Pi 5 | Convertisseur batterie, reconnaissance du courant disponible et consommation réelle inconnus |
| Alimentation caméra | Limite USB 600 mA ou 1,6 A selon alimentation/configuration ; budget partagé avec ventilateur | Caméra déclarant 500 mA selon un utilisateur : consommation et marge réelle à mesurer |
| Mécanique | Plan de référence constructeur disponible | Cotes approximatives, hauteur installée avec refroidissement et câbles à mesurer |
| Arrêt | Protections ESC et watchdog Pi sont des éléments possibles | Aucune distance ni durée d'arrêt validée ; PWM maintenu en cas de gel à traiter |

## Pi 5 et H.264 : ne pas confondre mesure et extrapolation

L'étude officielle est datée du 28 avril 2026 (construction du document le 5 mai 2026). Elle compare l'encodeur logiciel du Pi 5 à l'encodeur matériel du Pi 4 à partir de séquences vidéo. Elle n'est pas un essai de notre caméra U20CAM-4M.

Le passage au 1080p60 est présenté comme une extrapolation dans le résumé et la conclusion. Nous conservons donc le Pi 5 comme calculateur candidat à ce traitement, sans promettre 60 fps, une latence donnée ou une autonomie avant mesure. La réception d'un flux MJPEG déjà comprimé peut aussi permettre une transmission sans réencodage, avec un débit réseau plus élevé à mesurer.

La caméra USB doit être testée via V4L2 / FFmpeg ou un logiciel UVC approprié. Les exemples `rpicam-vid` pour caméras CSI ne sont pas une procédure validée pour ce module USB. La [procédure caméra existante](../camera/recherche-technique.md) conserve l'énumération des modes et une capture MJPEG sans duplication d'images.

## Documents et révisions

La fiche Pi 5 téléchargée est l'édition d'octobre 2026, PDF de sept pages. Le PDF RP1 proposé par le portail au moment de la recherche porte une date de construction du 7 novembre 2023 et un filigrane « DRAFT » ; la date de mise à jour du portail ne doit pas être assimilée à une nouvelle révision de son contenu. Le plan mécanique est explicitement un document de référence, pas une définition de fabrication.

La photo d'illustration constructeur représente la famille Pi 5 ; elle ne prouve pas la capacité RAM du produit livré. Aucun retour utilisateur ou essai vidéo public n'est utilisé ici comme preuve du fonctionnement de notre assemblage complet.

## Essais et relevés à réception

| Essai | Information à conserver |
| --- | --- |
| Identification | Modèle Pi 5, RAM de 4 Go, révision carte, système, noyau et firmware |
| Alimentation | Tension/courant à la batterie et à l'entrée Pi, chute lors des accélérations, état des limites USB |
| Refroidissement | Températures CPU et régulation de fréquence sous capture et encodage prolongés |
| Caméra | Modes exposés, négociation MJPEG 1080p60, débit et nombre d'images uniques |
| Réseau | Débit utile, pertes et latence écran avec les commandes simultanées, à plusieurs positions dans le bâtiment |
| Signaux ESC | Deux formes d'onde mesurées, niveaux, neutre, pleine commande et frein, stabilité pendant la vidéo |
| Commande | Calibration, sens gauche/droite, limitation d'accélération et comportement frein/recul |
| Défauts | Wi-Fi perdu, commandes expirées, logiciel interrompu ou figé, redémarrage et défaut d'alimentation ; absence de départ intempestif |
| Autonomie | Wh consommés par l'ensemble et températures ; durées à 20 et 40 km/h avec vidéo active |

Les numéros de broches proposés sont dans [integration.md](integration.md). Les seuils d'acceptation de latence, temps d'arrêt et température seront définis pour le véhicule et son espace de roulage avant essais rapides.

Sources : [index des PDF](notices/README.md), [documentation matérielle](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html), [portail Pi 5](https://pip.raspberrypi.com/categories/892-raspberry-pi-5), [recherche moteur](../moteur/recherche-technique.md), [recherche caméra](../camera/recherche-technique.md). Les empreintes sont dans [sources.json](sources.json).
