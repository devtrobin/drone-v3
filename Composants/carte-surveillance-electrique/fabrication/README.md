# Fabrication M1P - porteuse pour prototype de banc

**Lot prototype seulement.** [Coordination](../verification/coordination-protections.md), [banc B00-B14](../verification/banc-essais.md) et [registre](../verification/liberation-prototype.json) définissent le périmètre. Aucune qualification LiPo, aucun matériel testé. Les Gerbers sont ceux de la porteuse, pas ceux des modules TI.

## Demande de fabrication à joindre au ZIP

- FR4,140 x75 mm, épaisseur1,6 mm ±0,16 ; deux couches ; vernis épargne deux faces, sérigraphie face composants. Contour rectangulaire,4 trous mécaniques non métallisésØ3,2. Finition soudable sans plomb (ENIG ou équivalent validé par l'assembleur).
- Cuivre fini **70 micromètres nominal,55 minimum** sur chacune des deux faces. Le nom «2oz» seul ne dispense pas de confirmer le cuivre fini minimal. Pistes alimentation0,40 (gravées>=0,35), signaux0,20 (>=0,175). Isolement cuivre minimal du projet0,15 ; le fabricant doit confirmer sa capacité avec cette épaisseur.
- ViasØ0,80, perçage **fini**Ø0,40, tolérance admise±0,05 ; métallisation paroi>=20 micromètres. Autres trous métallisés selon Excellon. Ne pas appliquer un diamètre de foret brut comme diamètre fini. Vérifier les jeux de broches sur les fiches reçues (TMR /XH) ; diamètres source dans le PCB et les fichiers de perçage.
- Dimensions hors tout ±0,20 mm ; centres de trous ±0,10. Pas de cuivre de puissance moteur/Pi. Ne pas diminuer les largeurs ou métallisations sans refaire l'étude. Demander au fabricant un contrôle électrique de continuité/isolement du PCB nu à partir de sa netlist de fabrication.
- **Ce routage n'est pas directement usinable sur la CNC** : trous métallisés, deux faces et pas CMS fin. Aucune trajectoire d'outil ou qualification de la CNC n'est fournie. La fabrication décrite est industrielle ou équivalente avec contrôle de métallisation.

## Montage et contrôle

Utiliser la [BOM complète](../nomenclature-assemblage.csv), la [BOM porteuse](../KiCad/nomenclature.csv), les positions et les vues de montage. R7/R8 sont DNP sur la porteuse et installées côté Pi ; ne pas les remplacer par des straps. Les EVM et le Pololu2831 restent hors porteuse, reliés par faisceaux. Les modifications de résistances TI sont réalisées sur les modules selon [configuration](../modules/configuration.md). Au banc, les EVM sont posés séparément sur supports isolants, sans attendre leurs supports définitifs.

Avant de souder : PCB nu propre, contrôle des largeurs/cotes, pas de court-circuit visible, contrôle électrique, comparaison des empreintes et brochages aux fiches/échantillons. Puis montage par sous-ensembles selon B01-B03, avec sources limitées. Les cotes exactes de contour TI ne conditionnent aucune empreinte de ce PCB : [preuve et limites](../modules/cotes-ti.md).

Les fichiers incluent cuivre, masque, sérigraphie, contour, perçages séparés PTH/NPTH et netlist de test **IPC-D-356** ; **pas de stencil de pâte validé** ou d'assemblage automatisé promis. Les positions CSV facilitent la revue et le montage ; les boîtiers traversants ne se montent pas par pick-and-place CMS.

## Intégrité

[Manifest SHA256](manifest.json) : PCB/schéma contrôlés, exports, comptage et coordonnées des perçages, dimensions contour. Les vues SVG de cuivre et montage servent à la revue visuelle. Le ZIP contient ces fichiers et cette spécification ; ne pas commander une variante du PCB sans régénérer et revérifier ce lot.
