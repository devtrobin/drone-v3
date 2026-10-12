# Caméra — InnoMaker U20CAM-4M

**Référence retenue pour l'étude V3, non achetée.** Module USB compact avec capteur couleur OV4688. Le mode demandé **1920 × 1080 à 60 images/s** est annoncé en **MJPEG** sur Amazon et dans le tableau des résolutions de la notice constructeur, page 4.

## Achat Amazon.fr

- [Annonce exacte — ASIN B0H36XDQY8](https://www.amazon.fr/dp/B0H36XDQY8).
- Variante : module caméra USB HDR 4MP OV4688 / U20CAM-4M.
- Quantité prévue : **1**.
- Prix relevé le **12 octobre 2026** : **23,00 € TTC**.
- Vendeur : **InnoMaker** ; expédition : **Amazon**.
- Disponibilité affichée : **en stock**.
- Livraison gratuite affichée dans la session consultée ; tarif à revalider pour la commande.
- Module avec câble USB de 1 m annoncé. Fixations et support restent à ajouter au châssis.

Ce choix représente 11,5 % du plafond de 200 € ; il reste 177 € pour les autres postes si le prix et la livraison sont maintenus. L'ordinateur embarqué, les supports et l'alimentation ne sont pas inclus dans ces 23 €.

## Caractéristiques utiles

| Caractéristique | Donnée publiée |
| --- | --- |
| Capteur | OmniVision OV4688, couleur, obturateur roulant |
| Interface | USB 2.0 High-Speed, UVC 1.0 |
| Mode retenu | **MJPEG : 1920 × 1080 à 60 images/s** |
| Mode brut YUY2 à la même résolution | 3 images/s dans la notice ; ne satisfait pas l'objectif |
| Carte | 32 × 32 mm |
| Fixations | 4 trous de diamètre 2,2 mm ; entraxes à relever avant fabrication |
| Champ de vision | 71° diagonal, 58° horizontal |
| Câble | 1 m |
| Mise au point | À vérifier sur le module ; ne pas compter sur un autofocus, documentation ambiguë |

La masse, la hauteur totale, la consommation et les entraxes de fixation ne sont pas considérés mesurés.

## Compatibilité Raspberry Pi

La fiche Amazon cite Raspberry Pi, et la notice indique une interface UVC utilisable sous Linux. La caméra se branche sur un **port USB hôte**, pas sur le connecteur CSI : aucune nappe caméra Raspberry Pi n'est nécessaire.

- Pi 4 / Pi 5 : connexion au port USB avec le câble fourni, sous réserve de reconnaissance et validation du mode.
- Pi Zero / Zero 2 W : prévoir un adaptateur USB OTG vers USB-A pour le port USB de données ; le port d'alimentation ne sert pas de port caméra. Adaptateur à chiffrer si cette carte est choisie.

La compatibilité de connexion ne garantit pas le **retour Wi-Fi 1080p60**. Le flux MJPEG peut être relayé tel quel avec un débit à mesurer, ou décodé puis réencodé en H.264 avec un calculateur adapté. Le Pi Zero 2 W des versions précédentes est [spécifié pour encoder en H.264 1080p30](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) ; on ne validera donc pas une chaîne H.264 1080p60 sur ce Pi sur la seule base de cette caméra.

## Réserves documentaires et réception

La notice V1.0 présente une incohérence : page 3, la ligne générale de cadence indique 30 fps ; page 4, le tableau détaillé indique explicitement 1080p60 en MJPEG. Un avis Amazon rapporte également des modes par défaut à 30 fps. Ces éléments n'établissent pas l'impossibilité du 60 fps, mais justifient de conserver ce choix **sous réserve de contrôle matériel**, sans annoncer une performance déjà démontrée.

À réception :

1. Vérifier modèle, capteur, câble et reconnaissance UVC ; consulter les modes réellement exposés avec `v4l2-ctl --list-formats-ext` après identification du périphérique.
2. Demander MJPEG, 1920 × 1080 et 60 images/s. Ne pas utiliser un filtre qui duplique les images pour atteindre 60 fps.
3. Mesurer cadence effective et images uniques sur une scène en mouvement ; régler l'exposition en intérieur pour éviter une baisse de cadence en faible lumière.
4. Mesurer latence caméra–écran et débit avec la vidéo et les commandes Wi-Fi actives sur le calculateur retenu.
5. Relever consommation, masse et dimensions de montage.

## Sources conservées

- [Registre des sources et de l'achat](sources.json).
- [Notice constructeur locale](notices/U20CAM-4M-Usermanual.pdf), V1.0 du 21 mai 2026.
- [Dépôt documentaire officiel InnoMaker](https://github.com/INNO-MAKER/U20CAM-4M).
- [Index des composants](../README.md).
