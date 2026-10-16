> **R?vision active du15 octobre2026.** Alimentation active :D42V55F5 et faisceau 18 AWG d?di? soud? aux pads ; Molex r?serv? ?neuf signaux. [?tat courant](../verification-alimentation/README.md). Les valeurs diff?rentes de l?alimentation dans les documents anciens restent historiques.

# Carte de contrôle - Raspberry Pi 5, 4 Go

**Choix utilisateur confirmé le 13 octobre 2026 : une seule carte Raspberry Pi 5 de 4 Go pour le Wi-Fi, la vidéo et la commande des deux variateurs moteurs.** Aucun microcontrôleur séparé n'est retenu à ce stade. Carte non achetée ; aucun montage ou essai matériel validé.

## Documents du dossier

- [Notices et repères de lecture](notices/README.md) : fiche constructeur, plan mécanique, documentation RP1 et étude H.264, en PDF originaux.
- [Intégration électrique et commande des moteurs](integration.md).
- [Recherche technique, limites et essais à réception](recherche-technique.md).
- [Photo constructeur et crédit](photos/README.md).
- [Sources, caractéristiques structurées et empreintes SHA-256](sources.json).
- [Modèle 3D STEP détaillé officiel, aperçus et provenance](3D/README.md).

## Achat de référence

- [Annonce Amazon.fr - ASIN B0CK3L9WD3](https://www.amazon.fr/dp/B0CK3L9WD3).
- Variante recherchée : **Raspberry Pi 5, 4 GB / 4 Go**, carte seule.
- Quantité prévue : **1**.
- Le titre de la fiche Amazon consultée identifie bien le Pi 5 de 4 Go. **Prix TTC, stock, vendeur, expéditeur, livraison et contenu exact de l'offre non vérifiés** au 13 octobre 2026 : la consultation disponible ne permet pas de confirmer une offre achetable.
- Le choix du modèle ne constitue pas une commande ni une validation de vendeur. Vérifier la variante et le panier livré avant achat.

Le coût de cette carte et de ses accessoires reste à intégrer au budget : on dimensionne d'abord pour les objectifs techniques, puis on recherche les économies pour revenir vers l'objectif initial de 200 EUR pour tout le matériel neuf.

## Caractéristiques utiles à la V3

| Caractéristique | Donnée publiée / conséquence |
| --- | --- |
| Processeur | Broadcom BCM2712, quatre coeurs Arm Cortex-A76 à 2,4 GHz |
| Mémoire retenue | 4 Go LPDDR4X |
| Réseau | Wi-Fi 802.11ac double bande, Bluetooth 5.0/BLE, Ethernet Gigabit |
| USB hôte | 2 ports USB 3.0 et 2 ports USB 2.0 |
| Stockage système | Emplacement microSD ; carte à ajouter |
| Alimentation constructeur | 5 V / 5 A via USB-C, prise en charge USB Power Delivery |
| Commande externe | Connecteur GPIO 40 broches ; logique 3,3 V |
| Génération des impulsions | PWM matériel fourni par RP1 ; deux canaux à réserver pour les deux ESC |
| Carte / fixation | Environ 85 x 56 mm ; plan de référence avec trous de 2,7 mm et entraxes 58 x 49 mm |

Sources : [fiche constructeur locale](notices/Raspberry-Pi-5-fiche-constructeur.pdf), [plan local](notices/Raspberry-Pi-5-plan-mecanique.pdf), [documentation matérielle officielle](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html), [RP1 local](notices/RP1-peripheriques-GPIO-PWM.pdf).

Le plan constructeur indique que ses cotes sont approximatives et ne doivent pas servir directement de données de production. Prévoir également les connecteurs, le câble USB, le refroidissement, les dégagements de montage et l'accès à la microSD ; vérifier sur la carte reçue avant de fabriquer un support définitif.

## Rôle dans le drone

Le Pi reçoit les commandes du Mac par Wi-Fi, acquiert la vidéo de la [caméra InnoMaker U20CAM-4M](../camera/README.md), transmet le retour vidéo et produit deux commandes indépendantes vers les [variateurs Hobbywing WP16BL30 G2](../moteur/README.md).

Les variateurs restent indispensables : ils fournissent la puissance aux moteurs brushless. Les GPIO du Pi ne sont que des signaux de commande. L'architecture retenue conserve deux moteurs et deux variateurs pour les roues arrière ; les deux roues avant non motrices assurent la direction. La commande du [servo FT90M-C001](../servo-direction/README.md) s'ajoute aux deux commandes de variateur ; sa charge et l'alimentation depuis un seul BEC réglé à 6 V restent à valider.

La séparation du service vidéo et du service moteur est une proposition logicielle pour limiter les interférences entre tâches. Elle ne crée pas de supervision matérielle indépendante. Les fonctions de démarrage au neutre, freinage, arrêt sur perte Wi-Fi et comportement en cas de blocage doivent être réalisées et testées : voir [integration.md](integration.md).

## Vidéo 1920 x 1080 à 60 images/s

La caméra choisie est **USB UVC**, pas CSI : utiliser son câble USB fourni. Son mode 1080p60 est annoncé en **MJPEG**, sous réserve du contrôle décrit dans son dossier.

Deux chemins restent à tester : transmission du MJPEG reçu sans réencodage, ou décodage MJPEG puis encodage H.264 logiciel pour réduire le débit réseau. Le Pi 5 n'a pas d'encodeur H.264 matériel. L'[étude officielle](notices/Raspberry-Pi-5-etude-encodage-H264.pdf) mesure notamment le 1080p30 et extrapole une capacité 1080p60 ; elle ne mesure pas notre caméra USB, notre traitement complet ni notre liaison Wi-Fi.

La sortie HDMI 4K60 et le décodeur HEVC ne prouvent pas un retour vidéo 1080p60. La cadence d'images uniques, la latence Mac, le débit, les températures et la puissance prélevée à la batterie restent à mesurer simultanément avec les commandes moteur.

## Alimentation et accessoires à ajouter

- Convertisseur embarqué depuis la batterie vers une alimentation adaptée au Pi 5. L'indication 5 A est une capacité d'alimentation à prévoir, pas un courant permanent mesuré.
- Refroidissement retenu : [Active Cooler officiel SC1148](../refroidissement-raspberry-pi-5/README.md), 6,99 € TTC au 14 octobre 2026. Montage, courant FAN et thermique dans le châssis à qualifier.
- MicroSD et lecteur compatible avec le Mac ; proposition initiale : 32 Go avec Raspberry Pi OS Lite 64 bits, à préciser avant installation.
- Supports isolants, visserie, câble USB caméra et faisceau de commande des deux variateurs.
- Adaptation de niveau des signaux si nécessaire après vérification des entrées ESC, protections et coupure générale à concevoir.

Avec une alimentation standard, le Pi 5 peut limiter le courant USB total à **600 mA** ; une alimentation 5 V / 5 A reconnue permet **1,6 A**, budget partagé avec le ventilateur. Une sortie de convertisseur marquée « 5 A » ne garantit pas, à elle seule, la reconnaissance USB-PD. La déclaration USB de 500 mA rapportée pour notre caméra ne laisse qu'une faible marge à 600 mA. Vérifier toute la branche, les câbles et la configuration avant d'augmenter une limite. [Documentation constructeur sur l'alimentation](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html).

Le BEC des variateurs délivre 6 / 7,4 V : ne pas le raccorder directement au Pi. Le schéma de distribution définitif n'est pas encore validé.

## État de validation

Documents téléchargés et pages utiles contrôlées ; photo constructeur extraite sans retouche. **Aucun essai électrique, vidéo, moteur ou d'autonomie réalisé.** Les informations manquantes et les critères de réception sont conservés dans la [recherche technique](recherche-technique.md).

[Retour à l'index des composants](../README.md).
