<!-- finalisation-r2 -->
> **ÉtudeR2 du16octobre2026 :** [définition mécanique etimplantation révisées](../finalisation-theorique-r2/README.md). Les anciens arbres50mm etFT90M ne sont plus la définition nominaleR2 ; les réservations/interfaces non mesurées restent conditionnelles. Conserver les modèles/documents ci-dessous comme référencesA2-R1.
<!-- /finalisation-r2 -->

# Direction avant et transmissions arrière — sélection V3

**13 octobre 2026.** Choix effectués sous l'autorisation de sélectionner les composants. Deux roues arrière motrices, deux roues avant non motrices pour la direction ; châssis fabriqué. Les [modèles STEP et aperçus](3D/README.md) disposent d’une provenance et de contrôles par fichier. Aucun achat, montage ou essai physique.

## Dossiers créés

| Fonction | Choix de conception | Dossier |
| --- | --- | --- |
| Servo | FEETECH FT90M-C001, micro-servo de position à engrenages métalliques | [Servo](../servo-direction/README.md) |
| Fusées et renvois avant | Pièces Tamiya 51002, A7/A6 et A1/A8 | [Fusées](../fusees-avant/README.md) |
| Axes avant | Deux axes métalliques Tamiya 50823 | [Axes](../axes-avant/README.md) |
| Moyeux | Quatre Tamiya 53569, serrage sur axe, épaisseur 6 mm | [Moyeux](../moyeux/README.md) |
| Roulements | Douze MR115ZZ, format 5×11×4 ; fiche SMB de référence | [Roulements](../roulements/README.md) |
| Biellettes | Chapes 50596, rotules 50592 et tiges filetées acier M3 | [Biellettes et sous-composants](../biellettes-direction/README.md) |
| Réductions arrière | Deux transmissions à deux étages, 16→54 puis 24→54 | [Transmissions et engrenages](../transmission-arriere/README.md) |
| Arbres arrière | Deux intermédiaires Ø5 et deux sorties Ø5/M4 à fabriquer | [Arbres](../arbres-transmission/README.md) |
| Adaptation au châssis | Paliers à deux roulements et fourches avant à fabriquer | [Supports](../paliers-transmission/README.md) |
| Fixations | Goupilles, écrous M4, vis de pivot et vis de renvoi documentés | [Fixations](../fixations-train-roulant/README.md) |

Chaque référence a une fiche, une notice d'intégration et un registre de sources. Les chapes, rotules, tiges et trois références d'engrenages ont leurs sous-dossiers séparés. Les PDF originaux sont centralisés dans [notices](notices/README.md), sans modifications ni multiplication de copies. [Sélection et calculs structurés](selection.json).

## Ce que les choix établissent

Le train avant reprend une famille dont la notice montre l'assemblage fusée–axe métallique–roulements–moyeu–écrou. Les roues HobbyPark gardent leur empreinte de 12 mm et leur passage de 4 mm : l'axe porteur est Ø5 au roulement, avec une extrémité filetée M4 pour traverser la jante. Les interfaces de fabrication du châssis et le déport réel restent à relever.

La réduction arrière retenue pour l'étude vaut **7,59375:1**. Elle emploie un pignon moteur nominalement adapté à l'axe Ø2 et des roues/pignons Ø5 aux étages suivants. Le pignon Losi publie son module, mais pas son angle de pression : son appairage avec les engrenages KHK 20° reste une **condition à vérifier**, pas une compatibilité déjà certifiée.

## Ce qui n'est pas encore un panier prêt à acheter

Les offres Amazon France, prix, vendeurs et livraisons n'ont pas été confirmés pour ces références. Les liens Amazon sont des **recherches par référence**, clairement indiquées comme telles. Des sources constructeur et fournisseurs sont proposées pour identifier le matériel exact. Aucun ASIN ni stock n'est inventé.

Les arbres arrière, paliers, fourches, platine de servo et carters sont des **pièces à fabriquer**, dont le coût et les plans définitifs restent à établir. Posséder une CNC pour circuits ne certifie pas le tournage d'un axe, un ajustement de roulement ou l'usinage d'aluminium épais. La recherche ne remplace pas cette vérification de fabrication.

Les limites de charge des roulements et couples des engrenages concernent les conditions de leurs documents, pas une homologation du véhicule à 40 km/h. Les engrenages KHK sélectionnés représentent déjà **214 g** pour les deux transmissions, hors pignons moteur et arbres ; l'allègement et la baisse de prix restent des étapes possibles. Les objectifs d'autonomie et le retour vers 200 € ne sont pas validés par cette sélection.

[Intégration et dimensionnement](integration.md), [index général](../README.md).
