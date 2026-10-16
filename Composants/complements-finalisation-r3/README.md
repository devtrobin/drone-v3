# Compléments de finalisation R3

La R3 ajoute une réalisation nominale de la partie fixe du faisceau : armature démontable, huit brides garnies, entretoises anti-écrasement, quatre cordons courbes et visserie calculée. Elle approfondit les recherches fabricant et définit le câblage du prototype PWM. **Elle ne ferme pas les confirmations fournisseur ni les mesures physiques encore absentes. Le véhicule complet n’est pas déclaré prêt à alimenter.**

[PDF de revue](plans/dossier-complements-r3.pdf) · [Notice mécanique et cotes](notice-mecanique.md) · [Électricité](electricite.md) · [Points restants](conditions-restantes.md) · [Pièces STEP](3D/) · [Plans DXF](plans/) · [Assemblage FreeCAD](../../Assemblage/R3/drone-v3-r3-faisceau.FCStd).

[Archive des compléments R3](complements-finalisation-r3.zip), à extraire à la racine du projet existant. Elle contient les nouveaux fichiers R3 ; les dossiers R2 référencés restent dans le projet.

- Les huit brides immobilisent les parcours fixes. Les points extrêmes des câbles sont des **points d’approche**, distincts des bornes exactes à relever. Les conducteurs s’arrêtent donc volontairement avant certains appareils dans la CAO.
- [Longueurs](longueurs-cables.csv) : rayons sur axe30mm, cuivre6mm², enveloppeØ6.5. Débits bruts avec réserve de raccordement ; couper définitivement après présentation, sans stocker la réserve en boucle contre les pièces chaudes.
- [Visserie R3](visserie-r3.csv) à ajouter à la [visserie R2](../visserie-finale/README.md). Aucune fixation fournisseur inconnue n’est comptée comme certaine.
- [Sources](sources.json), [netlist PWM](interface-pwm-netlist-r3.csv), [scénarios de tension](scenarios-tension.csv), [rapports](verification/).

L’association mécanique de direction identifiée est **Pololu3429 + palonnier3431**, sans achat. **L’alimentationFT5335M+UBEC6V n’est pas validée en fin de pack** : voir [l’anomalie et l’alternative documentée](alimentation-direction-a-revoir.md). FS5A reste suspendu à la qualification de cette branche. Le support de fusible principal a une tenue DC documentée ; les autres points de coordination restent explicitement ouverts.

La [révision R2](../finalisation-theorique-r2/README.md) et ses modèles détaillés antérieurs sont conservés. L’assemblage R3 est une **vue légère d’étude**, pas une nouvelle version ultra détaillée de tous les composants.
