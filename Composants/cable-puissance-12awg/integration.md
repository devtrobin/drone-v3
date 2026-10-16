# Intégration des fils 12 AWG

| Repère de projet | Fil | Départ / arrivée | Longueur |
| --- | --- | --- | --- |
| CM1+ | Rouge | Sortie 5065 / ATO30 ESC1 → + XT60H-F1 | Après implantation ; exemple 0,20 m |
| CM2+ | Rouge | Sortie 5065 / ATO30 ESC2 → + XT60H-F2 | Après implantation ; exemple 0,20 m |
| CM1- | Noir | - XT60H-F1 → cosse D- N1 | Après implantation ; exemple 0,20 m |
| CM2- | Noir | - XT60H-F2 → cosse D- N3 | Après implantation ; exemple 0,20 m |

Un positif protégé par ESC et un retour négatif séparé. Les deux fils d'entrée 16 AWG / 75 mm des ESC et les fils 12 AWG des 5065 restent ceux de leurs kits. Ce câble ne remplace pas le tronc commun proposé 6 mm² et ne se branche pas sur les trois phases moteur, les GPIO ou l'USB.

## Interfaces

- **XT60H-F** : cuivre étamé à souder dans les godets selon référence AMASS et procédure applicable. Le 12 AWG correspond à la recommandation de câble ; gaine **Ø4,5 ±0,1 mm** et passage de capot à vérifier. Aucun brin supprimé pour gagner du diamètre.
- **Fil de sortie 5065 → queue rouge** : raccord à sélectionner pour les deux conducteurs souples réels. Ne pas considérer une soudure volante non retenue comme raccord final qualifié.
- **Retours vers MiniBus** : cosses à sertir adaptées au 12 AWG/section réelle et au goujon **#10-32**, passage et largeur à confirmer ; filetage UNF, pas M5. Références de cosses et outillage à sélectionner ensuite.
- **Si un fil entre dans le UD80A** : vérifier son acceptation en très fin multibrins et l'embout applicable. Ne pas pré-étamer à la soudure une extrémité sous une borne vissée ; l'étamage industriel de chaque brin est différent d'un faisceau rigidifié par soudure.

Les raccords, gaine de protection locale, embouts et retenue mécanique ne sont pas inclus dans le lot de fil. Les longueurs doivent conserver une marge de manipulation sans traction, rester hors engrenages/roues, arêtes et zones chaudes, et garder l'accès aux fusibles. Le silicone reste à protéger du frottement ; aucune résistance à l'abrasion ou traction admissible du lot mesurée.

## Préparation du projet

1. Batterie et équilibrage débranchés. Mesurer le chemin, prévoir les terminaisons et le maintien, puis seulement établir la liste de coupe.
2. Contrôler variante **12 AWG**, rouge/noir, diamètre, état et souplesse. Vérifier cuivre étamé déclaré ; aluminium cuivré différent et hors sélection. Contrôler la résistance sur une longueur connue si possible, en retirant la contribution des cordons de mesure.
3. Couper proprement ; régler le dénudage pour la borne/godet/raccord réel. Le 5 mm de la CAO est illustratif. Utiliser un outil adapté aux brins fins, inspecter sous grossissement : pas de brins coupés, entaillés ou perdus.
4. Pour godet soudé : passer le capot avant soudure, conserver tous les brins, éviter chauffe prolongée et remontée de soudure trop longue. Pour raccord serti : suivre notice cosse/raccord et matrice prescrite, sans ajouter une soudure non prévue.
5. Isoler et retenir le raccord, identifier chaque branche, puis contrôler continuité, isolement +/-, polarités et serrages selon les composants.
6. Première alimentation limitée et supervisée ; mesurer courant individuel, chute et températures en usage prévu. Observer moteurs, connecteurs, fusibles et fils d'origine, pas seulement le fil neuf.

## Courant et défauts

Le lot ne fournit pas un courant continu admissible garanti sous notre confinement. Les inscriptions 200 °C / 600 V ne prouvent pas 20 A ni la tenue des soudures/capots. Scénario individuel **20 A**, référence XT60H prudente **30 A** : hypothèses sans limitation active actuelle. La résistance de 5,06 Ω/km permet un exemple de pertes, pas une certification thermique ; résistance à chaud et courants RMS/pointes à mesurer.

Un ATO30 n'est pas un limiteur à 30 A. Coordination du câble, raccords et fils ESC 16 AWG avec le fusible et le courant prospectif LiPo à qualifier. Le 12 AWG neuf n'améliore pas automatiquement la tenue des fils d'origine ou celle du XT60 commun du pack. Pas d'essai volontaire de court-circuit de batterie.

[Prises XT60H](../connecteurs-alimentation/integration.md), [fusibles de branches](../protection-branches-moteurs/integration.md), [MiniBus et retours](../distribution-alimentation/integration.md), [répartiteur](../repartition-moteurs/integration.md).

<!-- faisceau-puissance-v3 -->

Complément du14octobre2026 : [cosses, raccords, gaine, maintien et câble principal](../faisceau-puissance/README.md), avec [raccordements et notice de préparation](../faisceau-puissance/integration.md). Sélection d’étude, sans achat ni qualification matérielle.
