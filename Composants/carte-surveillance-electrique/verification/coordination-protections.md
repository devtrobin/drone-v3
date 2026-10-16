# Coordination des protections - conclusion M1P

**Fabrication de prototype et essais fonctionnels sur banc borné : préparés. Raccordement direct à la LiPo : non libéré.** Aucun essai réel ni certification de tenue n'est produit. [Calculs et hypothèses](coordination-protections.json).

## Correction de la porteuse

Les pistes d'alimentation passent de **0,20 à 0,40 mm**, les pistes de signaux restent **0,20 mm** pour les circuits à pas fin. Le cuivre spécifié passe de35 supposés à **70 micromètres nominaux, au moins55 micromètres finis**, et les vias de0,60/0,30 à **0,80/0,40 mm**, métallisation des parois **20 micromètres minimum**. Largeurs gravées minimales de calcul : **0,35 mm alimentation /0,175 mm signaux**. Les petites plages gardent leurs empreintes fabricant. Il faut une fabrication avec trous métallisés ; les Gerbers ne sont pas un parcours CNC.

Un calcul adiabatique du cuivre, de40 à105 °C, donne environ **0.271 A²s pour l'ancienne section minimale** contre **4.010 A²s pour l'alimentation**, soit **14.8 fois** plus. Les signaux fins ont un critère de **1.003 A²s**. Il s'agit d'une comparaison de pistes uniformes, pas d'une qualification du PCB complet : tolérances, étranglements, broches, pastilles, composants et régime permanent restent distincts. Pour une durée longue, ignorer les pertes de chaleur surestime l'échauffement ; un dépassement du budget n'est donc pas une preuve de destruction.

## Ce que permettent réellement les fusibles

| Élément | Fonction | Conclusion vérifiée sur documents |
| --- | --- | --- |
| FAUX KLKD001.T / 1 A | Secours de la branche AUX, près de la dérivation | Ne limite pas le courant à 1 A. Support DC / énergie de coupure toujours sous conditions R2. |
| F1/F2 0454.500MR / 500 mA lents | Recommandation TRACO pour chaque entrée 5 V | Choix cohérent avec la recommandation ; coordination complète non prouvée. |
| RA0/RA1/RA2 100 ohms / 3 W | Limitation des trois fils de mesure au départ du pack | Calcul batterie seule : 8,4 / 90 = 93,3 mA ; 0,784 W. Ne couvre pas toutes les pannes d'isolement des sources 5 V. |

La fiche Littelfuse indique **0,240 A²s de fusion nominale**, calculée à 8 ms : ce n'est ni une borne maximale ni l'énergie totale de coupure. Le pouvoir de coupure annoncé est **50 A à 125 V DC et 300 A à 32 V DC**, pas une garantie de sélectivité entre fusibles. À deux fois le calibre (1 A), l'ouverture peut demander jusqu'à 60 s ; à 1,5 A jusqu'à 3 s ; à 4 A jusqu'à 0,1 s. Les deux derniers points donnent respectivement 6,75 et 1,60 A²s à courant constant : l'amélioration du cuivre ne ferme pas à elle seule toutes ces conditions.

M5 annonce une protection contre les courts-circuits, mais son courant « 1 A » est une capacité de sortie, **pas une borne garantie de courant de défaut**. Un court-circuit VIN/VOUT interne contournerait aussi son fonctionnement normal. Ne pas utiliser une limitation supposée du régulateur pour déclarer F1/F2 protégés contre tous les défauts.

## Mode banc retenu pour pouvoir fabriquer puis vérifier

- Source AUX isolée de la LiPo, **8,4 V maximum**, réglage CC **250 mA** ; valeur maximale acceptée 300 mA après10 ms. Ajouter **4,7 ohms / au moins25 W /5 % ou mieux** en série juste à sa sortie. Minimum de calcul **4,4 ohms**, tolérance et température comprises ; respecter la pose et la dissipation du modèle utilisé.
- La réserve capacitive de la source **avant** cette résistance doit être connue et au plus **470 microfarads**. Vérifier ces caractéristiques dans sa documentation ou sur charge fictive, avant de brancher la porteuse ; un bloc secteur ordinaire ne convient pas. Ne pas ajouter de gros condensateur au point J1.
- Avec ces hypothèses, pointe bornée à **1.909 A** par la résistance ; budget de contrôle entrée AUX **0.0402 A²s** avant CC, avec double comptage conservateur de la réserve capacitive. Marge au critère de piste uniforme environ **100**. Ce calcul ne se transfère pas automatiquement au secondaire du convertisseur M5.
- Deux simulateurs de cellules flottants et limités chacun à **20 mA / 4,2 V**. La source de rappel Pi simulée est limitée à **5 mA / 3,3 V**. Pas de batterie, chargeur, moteurs ou puissance Pi pendant la première campagne. [Câblage et séquence](banc-essais.md).
- Sous courant limité les fusibles peuvent ne jamais fondre : c'est attendu. Ils restent montés ; aucun pont ne les remplace. Les essais de coupure à fort courant de la LiPo sont hors de cette campagne.

## Fermeture pour la version véhicule

Il reste à obtenir une enveloppe maximale d'énergie totale de coupure aux conditions de défaut réelles, à comparer à chaque tronçon/connexion, **ou à ajouter une limitation électronique qualifiée** qui protège même en défaut interne de M5. Une eFuse n'est pas ajoutée au hasard : son état au démarrage, sa programmation, sa limite maximale, sa réponse rapide et son défaut en court-circuit doivent aussi être traités. Le module eFuse 2 Click / TPS259631 a été examiné ; il nécessite une configuration I2C et son stock constructeur est absent à la consultation. Il n'est donc pas déclaré substitut monté/validé.

Les confirmations R2 sur supports et fusibles de puissance restent ouvertes ; leur portée dépasse cette porteuse. Le [registre de libération](liberation-prototype.json) garde les deux états séparés. Le prochain travail mécanique peut employer la réservation 140 x 75 x 30, mais pas une implantation TI définitivement percée.

Sources primaires : [Littelfuse 452/454](https://www.littelfuse.com/assetdocs/littelfuse-fuse-452-454-datasheet?assetguid=8c87aa93-80a7-4ea8-8749-a19ba03901c2), [TRACO TMR1](https://www.tracopower.com/tmr1-datasheet), [Pololu 2831](https://www.pololu.com/product/2831), [Mikroe eFuse 2](https://www.mikroe.com/efuse-2-click). Les valeurs de matériaux dans le calcul sont des hypothèses d'ingénierie explicites ; aucune conformité normative n'en est déduite.
