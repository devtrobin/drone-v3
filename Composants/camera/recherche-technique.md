# Recherche complémentaire — InnoMaker U20CAM-4M

Recherche du **12 octobre 2026**, sur le modèle U20CAM-4M, le capteur OV4688 et l'ASIN B0H36XDQY8. Objectif : compléter la notice sans transférer les caractéristiques d'une autre caméra.

## Conclusion pour la V3

La caméra reste une candidate, **sans validation du 1080p60 réel**. La recherche précise la mise au point et apporte des retours d'intégration, mais ne résout pas toutes les lacunes. Aucun essai public identifié ne mesure simultanément résolution native, images uniques à 60 fps et latence du modèle exact.

## Ce qui est précisé

| Point | Résultat | Nature de la preuve |
| --- | --- | --- |
| Mise au point | Manuelle, réglable en tournant l'avant de l'objectif ; ne pas prévoir d'autofocus | Deux témoignages directs concordants [A1][a1], [A2][a2] ; notice ambiguë |
| Utilisation Raspberry Pi | Un utilisateur rapporte reconnaissance sous Linux et enregistrement Full HD avec FFmpeg | Témoignage [A3][a3] ; modèle de Pi et cadence non précisés |
| Câble | USB-A côté hôte, petit connecteur 5 broches côté carte, longueur annoncée 1 m | Témoignage [A2][a2] ; pas de référence ni brochage du connecteur |
| Identification USB | VID 0x364D, PID 0x6203, UVC 1.00, USB High-Speed 480 Mbit/s | Relevé utilisateur [A1][a1], cohérent avec la notice |
| Alimentation | Par le bus USB ; le relevé utilisateur rapporte 500 mA demandés dans les informations USB | [A1][a1] ; déclaration USB, **pas une mesure** |
| Compression | MJPEG et YUY2 documentés ; pas de sortie H.264/H.265 documentée | Notice officielle et identification utilisateur |

Les trois avis consultés sont marqués **Vine / produit gratuit**. Ils sont utiles comme observations directes, mais ne remplacent pas un banc d'essai avec fichiers d'origine, configuration et mesures.

### Mise au point : conséquence pratique

Le témoignage [A2][a2] décrit explicitement la rotation de l'objectif pour régler la netteté. [A1][a1] indique également un réglage manuel. La mention de contrôle « Auto Focus » dans la notice ne suffit donc pas à établir la présence d'un mécanisme motorisé. Pour la V3, prévoir un réglage avant conduite et son maintien ; plage de netteté et distance minimale restent inconnues. La mise au point manuelle n'impose pas un sujet immobile : un sujet peut rester net tant qu'il demeure dans la profondeur de champ.

### Consommation : ce que signifient les 500 mA

Le relevé USB [A1][a1] indique 500 mA demandés, pas le courant réel durant une capture. À 5 V, **5 × 0,5 = 2,5 W** peut servir de réserve de dimensionnement pour cette branche USB. Ce n'est ni une consommation typique, ni une mesure en 1080p60, ni une limite certifiée du module.

Le [fabricant du capteur OV4688][capteur] publie 261 mW en activité pour le **capteur seul**. Cette valeur exclut l'électronique USB, le traitement d'image et les pertes de la carte ; elle ne doit pas remplacer la consommation de la caméra complète dans le calcul d'autonomie.

## Contradiction de cadence : analyse

| Source | Ce qu'elle indique | Ce qu'elle ne démontre pas |
| --- | --- | --- |
| Notice V1.0, page 3 | Ligne générale de cadence : 30 fps | Cette ligne ne détaille pas les intervalles de chaque mode |
| Notice V1.0, page 4 | MJPEG 1920 × 1080 à 60 fps ; YUY2 1920 × 1080 à 3 fps | Pas de capture mesurée ou de conditions d'éclairage |
| Utilisateur [A1][a1], 22 juillet 2026 | Modes **par défaut** incluant 1080p30 MJPEG ; rapporte aussi 2560 × 1440 à 60 fps dans l'application Windows | Pas d'énumération complète des intervalles, ni de comptage d'images uniques |
| Utilisateur [A2][a2], 24 juillet 2026 | Décrit une vidéo fluide à 60 fps | Résolution et mesure de cadence non fournies |
| Utilisateur [A3][a3], 30 juillet 2026 | Enregistrement Full HD sur Raspberry Pi | Pas de cadence indiquée |

**Interprétation :** un mode par défaut à 30 fps peut coexister avec d'autres intervalles à la même résolution. La [documentation Linux][intervalles] décrit précisément l'énumération des intervalles par format et taille. Le relevé utilisateur ne permet donc pas de conclure que 30 fps est le maximum. Inversement, une application affichant « 60 fps » ne prouve pas une acquisition de 60 images uniques. Aucune preuve trouvée ne permet d'attribuer l'écart à une version de firmware, ni de proposer une mise à jour corrective.

Le [capteur OV4688][capteur] est capable de cadences supérieures à 60 fps selon ses modes. Cela rend le 60 fps plausible côté capteur, **sans valider le pont USB, le firmware ou ce module précis**.

## Recherche forums, YouTube et autres retours

- Recherches exactes : `U20CAM-4M review fps`, `U20CAM-4M youtube`, `B0H36XDQY8`, ainsi que `innomaker OV4688`.
- Recherches ciblées : YouTube, Reddit et forums Raspberry Pi, avec le modèle exact puis le couple marque/capteur.
- Recherche directe dans YouTube : `Innomaker U20CAM-4M`. Les résultats visibles portent sur d'autres caméras et projets ; aucun test attribuable au modèle exact n'a été identifié. Aucune vidéo YouTube n'est utilisée comme preuve.
- Le [dépôt officiel du modèle][depot] fournit la notice ; la [liste d'issues ouverte][issues] consultée ne contient aucun résultat. Cela ne prouve pas l'absence de problème ou de discussion ailleurs.
- Le [guide logiciel UVC du fabricant][logiciel] confirme l'utilisation de `uvcvideo`, FFmpeg et qv4l2 sous Linux ; c'est un guide générique, pas une mesure de ce modèle.
- Les fiches de revendeurs trouvées reprennent les annonces commerciales. Elles ne constituent pas des confirmations indépendantes des 60 fps.
- Les retours sur U20CAM-1080P-S1, U20CAM-9281M, IMX415 et les modules IMT d'InnoMaker Technologies sont exclus des caractéristiques de ce module : références et électronique différentes ou correspondance non établie.

## Informations toujours manquantes

| Donnée | État après recherche | Comment la résoudre |
| --- | --- | --- |
| 1080p60 avec images uniques | Annoncé ; non démontré | Énumération des intervalles, négociation puis capture d'une scène en mouvement |
| HDR actif en 1080p60 | Non établi | Contrôle exposé et essai HDR/cadence ; confirmation constructeur si nécessaire |
| Consommation réelle | Non trouvée | Mesure USB à l'arrêt, en 1080p30 et en 1080p60 |
| Masse du module et du câble | Non trouvée | Pesées séparées |
| Hauteur totale et entraxes des trous | Non trouvés | Mesure ou plan coté constructeur ; carte seule documentée à 32 × 32 mm |
| Brochage et référence du connecteur 5 broches | Non trouvés | Conserver le câble fourni ; obtenir plan avant câble personnalisé |
| Distance minimale et profondeur de champ | Non trouvées | Réglage et essais à différentes distances |
| Filtre IR et transmission optique | Non établis pour cette variante | Confirmation ou caractérisation du module exact |
| Température admissible de la carte complète | Non trouvée | Ne pas substituer la plage du capteur à celle du module |
| Débit MJPEG et réglage de qualité | Non mesurés | Taille des paquets/fichiers sur plusieurs scènes et contrôles disponibles |
| Latence et portée Wi-Fi | Non mesurées | Essai de la chaîne complète avec commandes simultanées |
| Version firmware expliquant les écarts | Aucun lien établi | Relever identifiants/révision et interroger les sources constructeur |

## Procédure permettant de trancher à réception

Ces commandes sont proposées pour le Raspberry Pi sous Linux ; **elles n'ont pas été exécutées sur une caméra**. Installer `v4l-utils`, FFmpeg et ffprobe depuis les paquets du système si nécessaire. Identifier d'abord le bon périphérique ; `/dev/video0` ci-dessous est un exemple.

```bash
v4l2-ctl --list-devices
v4l2-ctl -d /dev/video0 --list-formats-ext
v4l2-ctl -d /dev/video0 --list-ctrls-menus
v4l2-ctl -d /dev/video0 --set-fmt-video=width=1920,height=1080,pixelformat=MJPG --set-parm=60
v4l2-ctl -d /dev/video0 --get-fmt-video --get-parm
ffmpeg -f v4l2 -input_format mjpeg -video_size 1920x1080 -framerate 60 -i /dev/video0 -t 30 -an -c:v copy capture-1080p60.mkv
ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=codec_name,width,height,r_frame_rate,avg_frame_rate,nb_read_packets:format=duration,size -of json capture-1080p60.mkv
```

Conserver les sorties et avertissements, notamment toute cadence substituée par le pilote. Les paquets/timestamps établissent la livraison d'images, pas leur unicité : compléter par un objet en mouvement et l'inspection des images successives. Le choix `-c:v copy` conserve le MJPEG reçu ; ne pas ajouter `-r 60` en sortie ni un filtre `fps=60`, qui pourraient masquer une acquisition à 30 fps par duplication.

Les options d'entrée viennent de la [documentation FFmpeg V4L2][ffmpeg]. L'[exposition automatique Linux][exposition] peut, selon le contrôle disponible, modifier la cadence en faible lumière. Inspecter les contrôles réellement exposés avant de régler l'exposition ; à 60 fps, la période d'image est de 16,67 ms. La présence de bandes sous éclairage intérieur et la netteté à vitesse élevée doivent être testées dans le bâtiment prévu.

[a1]: https://www.amazon.fr/gp/customer-reviews/R3TLNFYAXTGZ5K
[a2]: https://www.amazon.fr/gp/customer-reviews/R18XXIYKPVDNYE
[a3]: https://www.amazon.fr/gp/customer-reviews/RVYF7X6V5XRLS
[depot]: https://github.com/INNO-MAKER/U20CAM-4M
[issues]: https://github.com/INNO-MAKER/U20CAM-4M/issues
[logiciel]: https://github.com/INNO-MAKER/UVC-Camera-Software
[capteur]: https://www.ovt.com/products/ov4688/
[intervalles]: https://docs.kernel.org/userspace-api/media/v4l/vidioc-enum-frameintervals.html
[exposition]: https://docs.kernel.org/userspace-api/media/v4l/ext-ctrls-camera.html
[ffmpeg]: https://ffmpeg.org/ffmpeg-devices.html#video4linux2_002c-v4l2
