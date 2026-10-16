# Quatre concepts visuels de châssis V3

Génération du 15 octobre 2026 avec l’outil intégré **image_gen**. Les quatre images et les [prompts complets](prompts.json) sont conservés dans ce dossier. Aucune CAO de châssis, liste de perçages ou qualification mécanique n’est produite à cette étape.

| Concept | Image | Intention |
| --- | --- | --- |
| A - Plateau ouvert | [PNG](a-plateau-ouvert.png) | Plaque principale et petit pont démontable ; accès direct pour montage et mise au point. |
| B - Poutre centrale | [PNG](b-poutre-centrale.png) | Batterie au centre et modules latéraux ; organisation distincte des équipements de puissance. |
| C - Bac à deux niveaux | [PNG](c-bac-deux-niveaux.png) | Rebords protecteurs et étage électronique démontable ; implantation plus enveloppée. |
| D - Cadre modulaire | [PNG](d-cadre-modulaire.png) | Deux longerons, traverses et platines remplaçables ; assemblage boulonné évolutif. |

## Configuration prise en compte

Quatre roues de 63 ×26 mm ; direction avant non motrice avec servo et biellettes ; deux moteurs arrière indépendants et deux réductions à deux étages ; deux ESC ; caméra USB à l’avant ; Pi5 et refroidissement actif ; batterie G1 IC5 de139 ×46 ×25 mm avec sangles ; régulateur D42V55F5 ; relais D1D100 et dissipateur HS251 ; distribution par deux MiniBus2315 et UD80 ; coupure manuelle ED80 ; fusible principal classeT et trois fusibles de branche de la révision alimentationR2 ; bornes, câblage, capteurs de vitesse et réserve pour la future carte de surveillance. Le chargeur S65 reste hors du véhicule.

L’enveloppe d’environ430 ×300 mm donnée au générateur sert uniquement de repère visuel initial pour éviter de miniaturiser les grosses protections. Elle n’est ni calculée par assemblage des STEP, ni une dimension finale. Aucune masse, rigidité, facilité d’usinage de l’aluminium ou performance à40 km/h n’est validée par les images.

## Fidélité des images

Les images illustrent les architectures et l’accès aux pièces. Les boîtiers, câbles, engrenages, supports et fixations y sont interprétés par le générateur ; ils ne remplacent pas les modèles et documents des composants. Les antennes externes dessinées ne sont pas un nouveau composant retenu : le Pi utilise son Wi-Fi intégré. La caméra retenue reste USB, même si un rendu suggère une nappe. Les deux réductions arrière conservent les engrenages sélectionnés, même si un rendu stylise leur carter.

La sélection active reste celle des [composants](../../README.md), de l’[alimentationR2](../../verification-alimentation/README.md) et des [capteurs de vitesse](../../capteurs-vitesse/README.md). Fixations captives des aimants, supports caméra/capteurs, longueurs des fils, carte de surveillance, visserie, dégagements de direction et protections des engrenages seront déterminés avec l’assemblage CAO final. Les confirmations électriques déjà ouvertes restent applicables.

Ces concepts sont proposés pour choisir une forme de départ. Aucun nouveau composant commercial n’est sélectionné par les détails des illustrations.


## Variante A2 - cam?ra arri?re en hauteur

[Image A2](a2-plateau-ouvert-camera-arriere.png), modification du concept A r?alis?e avec image_gen int?gr? le15octobre2026 ; [prompt exact](a2-camera-arriere-prompt.json). L?original A est conserv?.

Une seule cam?ra, d?plac?e au centre arri?re sur un portique d?montable ? deux montants et traverse ; objectif orient? vers l?avant, inclinaison r?glable et c?ble USB maintenu sur un montant. L?ancienne cam?ra et son support avant sont retir?s, ainsi que l?antenne externe illustr?e dans A. Les deux moteurs arri?re, la direction avant et l?architecture du plateau ouvert sont conserv?s.

Hauteur, rigidit?, vibrations et cadrage restent ? d?finir en CAO puis sur montage r?el. L?image ne garantit pas la visibilit? int?grale du plateau et de la route avec le champ de vision de l?objectif retenu. Elle ne valide ni fixations ni d?tails du c?blage.
