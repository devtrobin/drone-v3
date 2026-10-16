# Recherche et avis - Active Cooler SC1148

## Sources primaires et variantes

[Fabricant](https://www.raspberrypi.com/products/active-cooler/), [portail](https://pip.raspberrypi.com/categories/993-raspberry-pi-active-cooler), fiche publiée janvier 2026 et plan de référence archivé. Le portail indique mises à jour 9janvier 2026 /6 octobre 2025. **Débitmax 1,09 CFM**, vitessemax 8000 tr/min± 15 %, MTTF 379000h à 25 °C (estimation de fiabilité, pas durée de vie garantie). Plusieurs vendeurs affichent 1,4 CFM : la valeur actuelle du fabricant prévaut.

Les URL historiquesdatasheets et les liens PIP téléchargent ici les **mêmes fichiers actuels**, SHA256 identiques. Le fichier local nommé « fiche-historique-originale » provient de l’ancienneURL, mais son contenu est janvier 2026, pas une édition 2023. Les alias sont conservés pour documenter cette résolution ; cinq PDF téléchargés correspondent à deux contenus distincts, sans retouche.

Le plan présente un dessin simplifié d’entrée d’air, tandis que les photos montrent un rotor dans une ouverture circulaire. Le modèle suit les photos pour les détails et le plan pour les cotes disponibles. Les trois pads sont visibles sur une photo de dessous Waveshare, fournisseur du produit officiel ; toutes leurs dimensions restent estimées. Aucun STEP constructeur de ce refroidisseur trouvé dans le portail, ni CAO native adoptée sans provenance. Pi STEP existants conservés.

## Achat et retours Amazon

[Amazon.fr](https://www.amazon.fr/dp/B0CLXZBR5P) a pu être archivé après un premier accès refusé ; identité SC1148 /GTIN et prix 6,99 € TTC affichés, stock 5 au relevé 14 octobre 2026. Le prix d’un bundle Pi, celui d’un autre vendeur ou un total importDesertcart ne sont pas utilisés. L’ASIN trouvé viaDesertcart est ensuite confirmé par les détails Amazon.com et Amazon.fr. Les champs « processeur / RAM / Ethernet » de ces reprises marchandes ne sont pas des fonctionnalités du refroidisseur.

La fiche française affiche 4,7/5 et 1242 évaluations au relevé. Ce compteur peut agréger les pays et les versions de fiche ; il ne donne pas une statistique de panne de notre lot. Le widget ne fournit pas ici des témoignages individuels complets exploitables ; aucun avis Amazon inventé. Port et vendeur du panier final à vérifier ; les premières occurrences de « vendu par » dans la page peuvent concerner des produits associés, et ne sont pas utilisées pour identifier le vendeur du refroidisseur.

Olimex affiche 5,00 EUR mais «outofstock» au relevé, baseTVA / port français non établie : pas une offre de remplacement achetable à ce montant. Le prix choisi pour la ligne SC1148 est celui de la page Amazon.fr, sans frais garantis.

## Essais indépendants et forums

- [Jeff Geerling,2024, article avec mesures](https://www.jeffgeerling.com/blog/2024/water-cooling-overkill-pi-5/) : il rapporte un Active Cooler proche du bruit ambiant de son studio à 5000 tr/min. Mesure d’un testeur dans son montage, sans garantie de bruit ou de température dans notre châssis.
- [Jeff Geerling, vidéo 2023](https://www.youtube.com/watch?v=nBtOEmUqASQ) : chapitre 10:17 consacré à la thermique et à l’Active Cooler ; vidéo de référence identifiée, pas d’essai 1080p60USB-vers Mac de notre robot. La page YouTube est archivée ; aucun résultat non consulté n’en est déduit.
- [Forum officiel, bruit](https://forums.raspberrypi.com/viewtopic.php?p=2179285) : discussion sur niveaux de bruit mesurés et perceptions. Points d’attention pour vérifier le lot, sans garantie acoustique. Accès direct 403, contenu consulté via rechercheWeb.
- [Forum officiel, boîtier](https://forums.raspberrypi.com/viewtopic.php?t=367026) : un utilisateur décrit une interférence avec le couvercle intérieur d’un boîtier Pi. Ce n’est pas notre châssis, mais cela justifie de vérifier les dégagements au lieu de supposer un assemblage universel.
- [Billet constructeur thermique 2023](https://www.raspberrypi.com/news/heating-and-cooling-raspberry-pi-5/) : essais de charge dans leurs conditions. La régulation décrite est ancienne ; le profil actuel est lu dans la [documentation matérielle](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html). Les 60 mA cités pour le ventilateur de boîtier ne sont pas transposés au SC1148.

## Informations non établies

Courant SC1148 réel, résistance thermique du module dans le châssis, niveau sonore normalisé, vibrations, épaisseurs comprimées des pads, classe de tolérance, profil exact du rotor, longueurs et sections du cordon, empreinte de fiche et hauteur installée au-dessus du PCB. Les vues détaillées sont des reconstructions, pas des mesures. Aucun essai embarqué, aucune validation 1080p60 ni gain d’autonomie annoncé.

[Sources et archives](assets.json), [cotes](cotes.md), [intégration](integration.md), [modèles 3D](3D/README.md).
