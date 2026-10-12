# Pistes techniques et contrainte de coût

Relevé du **12 octobre 2026**. Aucun panier validé. Les capacités constructeur ne prouvent pas le fonctionnement de la chaîne complète.

## Architecture à comparer

- Quatre roues, batterie basse, direction avant par servo.
- Propulsion arrière : comparer un moteur avec réduction et différentiel du commerce à deux entraînements indépendants. Un arbre arrière rigide entraîne du ripage en virage et ne sera pas retenu sans étude.
- Contrôleur automobile avec freinage et marche arrière documentés. Ne pas substituer un ESC d'avion dépourvu des fonctions nécessaires.
- Ordinateur embarqué pour vidéo et Wi-Fi ; commande servo/ESC via contrôleur dont le comportement sur perte de liaison ou gel logiciel est testé. Un microcontrôleur indépendant est une piste pour cet arrêt.
- Alimentation propulsion séparée de la branche 5 V régulée vidéo/commande, issue de la même batterie si compatible. Vérifier bruit électrique et tension pendant accélération et freinage.

## Références candidates, sans sélection d'achat

Mise à jour caméra : [InnoMaker U20CAM-4M](Composants/camera/README.md) retenue pour l'étude à 23,00 € sur Amazon.fr, 1080p60 MJPEG annoncé, sous réserve d'essai. La Waveshare ci-dessous reste une alternative de recherche. Le calculateur embarqué reste à choisir ; la compatibilité Raspberry Pi de la caméra ne valide pas à elle seule la chaîne de transmission.

| Élément | Preuve disponible | Incertitude restante |
| --- | --- | --- |
| Radxa ZERO 3W | [Constructeur](https://radxa.com/products/zeros/zero3w/) : encodeur H.264/H.265 jusqu'à 1080p60, Wi-Fi, USB hôte | Prix livré en France et stock non validés ; accès logiciel à l'encodeur et traitement MJPEG à vérifier |
| Waveshare IMX415 8MP USB Camera (A), SKU 33562 | [Fabricant](https://www.waveshare.com/product/ai/imx415-8mp-usb-camera-a.htm) : MJPEG, 1920 × 1080 à 60 fps ; prix affiché 37,99 USD | TVA/port/change non établis ; sortie MJPEG à décoder puis réencoder en H.264 ; latence et 60 images uniques à mesurer |
| Hobbywing QuicRun 16BL30 G2 + moteur 2435 | [Fabricant ESC](https://www.hobbywing.com/en/rc-systems/rc-cars-power-system) et [combo officiel](https://www.hobbywingdirect.com/products/quicrun-wp-16bl30-2435sl-combo-g2?variant=51925223178607) | Famille de propulsion à étudier, pas un choix final ; coût, régime chargé, courant, intégration transmission et freinage à vérifier |
| Racerstar 2435 + ESC 25 A | [Constructeur](https://www.racerstar.com/Racerstar-2435-Waterproof-Brushless-Sensorless-Motor-4500-or-4800KV-25A-ESC-For-1-or-16-1-or-18-RC-Car-p-13.html) | Prix livré, génération exacte, documentation de freinage et marche arrière à vérifier |

L'Arducam UB0241 encodait du 1080p60 en H.264/H.265, mais est [déclarée arrêtée par le fabricant](https://www.arducam.com/blog/product/1080p-60fps-hd-usb-camera-h-265-h-264-high-definition-uvc-camera-ub0241/) : exclue du panier neuf. Une caméra avec encodeur intégré et disponible pourrait éviter le traitement MJPEG sur la carte ; chercher une référence réellement documentée et vendue.

## Enveloppes de travail, pas des prix fournisseurs

Pour arbitrer les recherches, la répartition suivante totalise exactement 200 €. Chaque montant est un **plafond de recherche**, sans preuve qu'un lot compatible existe à ce prix.

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
