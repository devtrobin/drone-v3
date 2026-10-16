# Pistes techniques et contrainte de coût

Relevé du **12 octobre 2026**. Aucun panier validé. Les capacités constructeur ne prouvent pas le fonctionnement de la chaîne complète.

## Architecture à comparer

- Architecture retenue : **deux roues arrière motrices et deux roues avant non motrices pour la direction**, batterie basse. La bille avant est abandonnée. [Servo, biellettes, fusées et moyeux](Composants/direction-et-transmission/README.md) sont documentés ; géométrie et interfaces de fabrication restent à établir.
- Moteur retenu : [Hobbywing 2435SL G3, 4 500 KV](Composants/moteur/README.md), **deux moteurs et deux variateurs**, un ensemble par roue arrière. La direction est assurée par les roues avant. La coordination des vitesses arrière en virage reste à définir pour limiter le ripage.
- Roues retenues le 13 octobre : [HobbyPark Touring Color A, 63 × 26 mm](Composants/roues/README.md), un lot de quatre pré-collées. Moyeux, axes et roulements documentés dans les [dossiers du train roulant](Composants/direction-et-transmission/README.md) ; déport, pivots et montage restent à valider. Offre française et prix non vérifiés.
- Réduction retenue pour l'étude : [16→54 puis 24→54](Composants/transmission-arriere/README.md), i=7,59375 par roue. Pignon d'entrée Ø2, arbres suivants Ø5 ; angle de pression du couple Losi/KHK, endurance et prix à valider. Les arbres, fourches et paliers restent des pièces à fabriquer.
- Contrôleur automobile avec freinage et marche arrière documentés. Ne pas substituer un ESC d'avion dépourvu des fonctions nécessaires.
- Choix du 13 octobre 2026 : [Raspberry Pi 5 de 4 Go](Composants/raspberry-pi-5/README.md) seul pour vidéo, Wi-Fi et commande des deux variateurs par PWM matériel. Aucun microcontrôleur séparé retenu. Le comportement sur perte de liaison ou gel logiciel reste à concevoir et tester.
- Alimentation propulsion séparée de la branche 5 V régulée vidéo/commande, issue de la même batterie si compatible. Vérifier bruit électrique et tension pendant accélération et freinage.

## Références candidates, sans sélection d'achat

Mise à jour caméra : [InnoMaker U20CAM-4M](Composants/camera/README.md) retenue pour l'étude à 23,00 € sur Amazon.fr, 1080p60 MJPEG annoncé, sous réserve d'essai. La Waveshare ci-dessous reste une alternative de recherche. Le calculateur retenu est le Pi 5 de 4 Go ; sa compatibilité USB avec la caméra ne valide pas à elle seule la chaîne de transmission.

| Élément | Preuve disponible | Incertitude restante |
| --- | --- | --- |
| Radxa ZERO 3W | [Constructeur](https://radxa.com/products/zeros/zero3w/) : encodeur H.264/H.265 jusqu'à 1080p60, Wi-Fi, USB hôte | Prix livré en France et stock non validés ; accès logiciel à l'encodeur et traitement MJPEG à vérifier |
| Waveshare IMX415 8MP USB Camera (A), SKU 33562 | [Fabricant](https://www.waveshare.com/product/ai/imx415-8mp-usb-camera-a.htm) : MJPEG, 1920 × 1080 à 60 fps ; prix affiché 37,99 USD | TVA/port/change non établis ; sortie MJPEG à décoder puis réencoder en H.264 ; latence et 60 images uniques à mesurer |
| Hobbywing QuicRun 16BL30 G2 + moteur 2435SL G3 4 500 KV | [Choix et offre Amazon](Composants/moteur/README.md) : 66,34 € par kit lors du relevé | Modèle retenu ; quantité, régime chargé, consommation, transmission et freinage à vérifier |
| Racerstar 2435 + ESC 25 A | [Constructeur](https://www.racerstar.com/Racerstar-2435-Waterproof-Brushless-Sensorless-Motor-4500-or-4800KV-25A-ESC-For-1-or-16-1-or-18-RC-Car-p-13.html) | Prix livré, génération exacte, documentation de freinage et marche arrière à vérifier |

L'Arducam UB0241 encodait du 1080p60 en H.264/H.265, mais est [déclarée arrêtée par le fabricant](https://www.arducam.com/blog/product/1080p-60fps-hd-usb-camera-h-265-h-264-high-definition-uvc-camera-ub0241/) : exclue du panier neuf. Une caméra avec encodeur intégré et disponible pourrait éviter le traitement MJPEG sur la carte ; chercher une référence réellement documentée et vendue.

## Enveloppes de travail, pas des prix fournisseurs

La répartition initiale ci-dessous totalisait 200 €. Elle reste un repère historique, pas une limite pour le dimensionnement actuel : l'utilisateur demande de chiffrer d'abord les spécifications complètes, puis de chercher les économies et les compromis pour revenir vers 200 €.

| Poste | Plafond de recherche |
| --- | ---: |
| Caméra, ordinateur Wi-Fi, stockage et câbles vidéo | 65 € |
| Moteur(s) et ESC/pilote(s) | 35 € |
| Batterie et chargeur compatibles | 35 € |
| Roues, axes, roulements, réduction, différentiel et direction mécanique | 30 € |
| Servo, commande embarquée, convertisseur et protections électriques | 15 € |
| Matière châssis, fabrication, fixations et livraison | 20 € |
| **Total maximal** | **200 €** |

Cette enveloppe est très tendue, notamment pour la transmission et la vidéo. Un dépassement d'un poste oblige à revoir les autres références ; il ne justifie pas d'omettre chargeur, frais, direction ou fixations. Les outils du fablab ne sont pas achetés, mais tout coût de fabrication nécessaire est à compter. Aucune réutilisation n'est déduite.

## Portée Wi-Fi

La portée utile signifie : vidéo à cadence et latence acceptables **et** commande fiable. La distance où le réseau reste visible ne suffit pas. Tester ensemble Mac, point d'accès ou liaison directe, antennes et équipement embarqué dans le bâtiment visé. Tout routeur ou adaptateur supplémentaire nécessaire sera ajouté au budget.

## Prochaines preuves nécessaires

1. Panier livré en France pour vidéo et stockage, avec disponibilité et modes compatibles vérifiés.
2. Coût et géométrie d'une transmission fabricable, incluant direction et fixation des roues.
3. Dimensionnement mécanique et énergétique avec masse et puissance totale crédibles.
4. Essais vidéo/commande sur table avant plans définitifs et essais rapides.
