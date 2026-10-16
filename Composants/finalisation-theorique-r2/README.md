# Finalisation théorique R2 - 16 octobre 2026

Cette révision traite les quatre volets demandés : mécanique, intégration, électricité et visserie. Elle ajoute des pièces et des calculs contrôlables. **Elle n’est pas une autorisation de fabriquer puis alimenter le véhicule complet : les points D01 à D07 restent ouverts.** Les essais et mesures de réception sont séparés dans le registre.

[Dossier PDF](plans/dossier-finalisation-r2.pdf) · [Mécanique](mecanique.md) · [Intégration](integration.md) · [Électricité](electricite.md) · [Visserie](../visserie-finale/README.md) · [Conditions restantes](conditions-restantes.md).

[Archive de la révision R2](dossier-finalisation-r2.zip) : dossier de revue, pièces et assemblage R2, composants complémentaires et visserie. Elle complète le projet existant ; les anciens dossiers de composants et les modèles détaillés R1 restent dans le dépôt.

## Décisions de conception

- Enveloppe de calcul : **9 kg maximum, au plus 45% sur l’avant**, cas vertical 3 g. Il s’agit de limites de calcul, pas d’une masse pesée.
- Deux transmissions 7.59375:1 conservées ; arbres intermédiaires **91.5 mm**, sorties **145.5 mm**, axes avant **42.5 mm**. Les arbres 50 mm historiques ne sont pas à fabriquer.
- Palier extérieur arrière porté à X±193, contre±171.5 précédemment ; porte-à-faux roue ramené de 28.5 à **7 mm**. Les deux C04 deviennent des platines 93 x 90 x 3 sans ancien évidement.
- Rotors Hall à X±80, pieds à X±51 : leur nouvelle position évite les paliers et les dentures.
- [Retenues normaliséesDIN471-5](../retenues-axiales/README.md) : quatre circlips etdesépaulements monoblocs remplacent les petits colliers non définis.
- Deux fusées/fourches usinées remplacent les interfaces Tamiya A7/A6/50823 reconstruites et non mesurées. Moyeux 53569, roues et famille de roulements conservés.
- FT90M retiré de la sélection R2. **FT5335M à 6 V +UBEC Hobbywing 30603003**, branche FS candidate 5 A ; BEC des ESC réservés aux interfaces de commande, jamais en parallèle.
- Direction à deux biellettes, résolue numériquement ; traverse **292.34 mm**, commande **142.20 mm entre centres de rotules**. Commande servo limitée à±55° ; roues sous 25° dans l’étude.
- Interface de trois PWM isolés proposée pour supprimer les retours de puissance par les masses de commande. Schéma de banc détaillé ; aucune fabrication électronique supplémentaire déclarée prête.

## Livrables

- [Pièces STEP](3D/) et [liste des pièces](pieces.json) : repère global conservé ; filetages simplifiés géométriquement mais spécifiés dans les plans.
- [AssemblageR2 léger](../../Assemblage/R2/drone-v3-r2-etude.step), distinct des versions détailléesR1 existantes. Réservations et parcours non raccordés restent identifiés.
- [Empilages cotés](plans/empilages-arbres.csv), [perçagesR2](plans/percages-r2-global.csv), [surcoucheDXF](plans/surcouche-percages-r2.dxf).
- [Table de direction](table-direction.csv), [calculs](calculs.json), [parcours et débits candidats](routage/longueurs-cables.csv), [brochage actifR2](routage/brochage-gpio-r2.json).
- [Nomenclature de visserie](../visserie-finale/nomenclature.csv) et accessoires distincts des fixations fournisseur encore inconnues.
- [Rapports de contrôle](verification/), [sources consultées et archives](sources.json).

Les STEP de pièces sont des définitions nominales de l’étude. Les ajustements, les filetages et les exigences de matière se lisent dans les documents associés ; la CAO seule ne sert pas de calibre. Les plans et archives R1 sont conservés et ne doivent pas être mélangés avec les pièces R2.
