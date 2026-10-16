# Refroidissement du Raspberry Pi 5 - Active Cooler SC1148

**Référence retenue : Raspberry Pi Active Cooler officiel SC1148, une unité.** Dissipateur en aluminium anodisé avec ventilateur radial régulé, pads thermiques préposés, deux attaches à ressort et cordon quatre fils. Non acheté, non testé.

## Achat Amazon et devis

[Fiche Amazon.fr identifiée](https://www.amazon.fr/dp/B0CLXZBR5P), ASIN **B0CLXZBR5P**. Relevé du **14 octobre 2026 : 6,99 € TTC**, stock affiché 5 exemplaires. Le titre français est générique, mais les détails du produit indiquent **SC1148**, Raspberry Pi et le GTIN 05056561803357. La fiche américaine correspond au même identifiant.

La page propose une livraison gratuite pour une première commande, au 21 octobre dans le contexte consulté ; **ce n’est pas un port garanti pour notre panier**. Vérifier au paiement vendeur, contenu, compte et frais. Aucune commande effectuée. [Relevé structuré et source archivée](achat-amazon.json).

## Documents et modèle

- [Notice PDF V3](notices/notice-active-cooler-pi5-v3.pdf) et [PDF fabricant originaux](notices/README.md).
- [Cotes publiées et estimations](cotes.md).
- [Intégration, brochage et contrôles](integration.md).
- [Recherche technique et avis](recherche-technique.md).
- [Photos originales et crédits](photos/README.md).
- [Quatre variantes STEP, aperçus et provenance](3D/README.md), dont une version d’implantation légère.
- [Nomenclature](nomenclature.json), [sources](sources.json), [calculs](calculs.json) et [validation du dossier](validation-dossier.json).

Le refroidisseur se branche sur **FAN**, pas sur les sorties PWM 12/13/18 réservées aux deux ESC et au servo. Le ventilateur partage le budget des périphériques USB ; son courant doit être mesuré avec la caméra.

L’enveloppe du plan est **63,5 × 42,5 mm**, hauteur **13,7 mm attaches incluses**, ventilateur 30 × 30 mm. Ce sont des cotes de référence approximatives, explicitement impropres à produire directement des données de fabrication. La hauteur à réserver au-dessus du PCB et le chemin du cordon dépendent de la pose.

Le modèle reprend les ailettes et leur striation, le rotor visible, le capot, vis et clips, les ressorts hélicoïdaux, trois pads observés, le logo issu du plan et les quatre fils continus avec leur fiche. Les dimensions locales inconnues restent des estimations documentées.

[Fabricant](https://www.raspberrypi.com/products/active-cooler/), [portail documentaire](https://pip.raspberrypi.com/categories/993-raspberry-pi-active-cooler), [Pi 5 retenu](../raspberry-pi-5/README.md).
