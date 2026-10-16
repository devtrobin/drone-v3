# Mesure de vitesse des roues arrière

Sélection du **15 octobre 2026**. Deux capteurs numériques TI et quatre aimants, complétés par leurs rappels et découplages. Ajout de mesure pour la mise au point ; aucune pièce ni performance testée.

| Composant | Référence | Monté | Dossier |
| --- | --- | ---: | --- |
| Capteur Hall 3,3 V | DRV5033AJQLPG, TO-92 LPG | 2 | [Documentation et STEP](capteur-hall-drv5033/README.md) |
| Aimant axial Ø3 × 2 | supermagnete S-03-02-N, N48 | 4 | [Documentation et STEP](aimants-s-03-02-n/README.md) |
| Rappel OUT | Vishay MRS25 10 kΩ ±1 % | 2 | [Documentation et STEP](resistances-rappel-10k/README.md) |
| Découplage local | KEMET C315C104K5R5TA, 100 nF X7R | 2 | [Documentation et STEP officiel](condensateurs-decouplage-100nf/README.md) |

[Notice PDF](notices/notice-capteurs-vitesse-v3.pdf) · [Raccordement et acquisition](integration.md) · [Cotes d’ensemble](cotes.md) · [Calculs](calculs.json) · [Devis](devis.md) · [Recherche et avis](recherche-technique.md) · [Documents constructeur](notices/README.md) · [Tous les modèles](3D/README.md) · [Brochage](brochage.json).

Deux aimants identiques à 180° donnent deux impulsions par tour. À 40 km/h avec une roue nominale de 63 mm : environ **3 368 tr/min et 112,28 Hz**. Le capteur ne donne pas le sens de marche ; le patinage et le diamètre sous charge limitent la vitesse au sol estimée. En virage, les deux vitesses de roue sont différentes.

GPIO23/pin16 et GPIO24/pin18 sont réservées aux sorties, avec 3,3 V pin17 et GND pin25. Le Molex passe à **13 contacts montés et 18 à provisionner** avec cinq de réserve. Le faisceau 5 V séparé de la Pi reste celui de la révision alimentation R2. Les anciens modèles de faisceau GPIO ne représentent pas cette extension.

Aucune offre Amazon.fr exacte vérifiée ; les pistes RS et supermagnete sont documentées. Devis partiel avec conditionnements et minimum de commande, sans achat. Fixation captive des aimants, supports, longueurs des fils et implantation mécanique réservés au châssis final. Aucun schéma/routage de la carte de surveillance modifié par cet ajout.

[Contr?les des fichiers et de l?int?gration](verification.json) : coh?rence documentaire et CAO ; aucun essai mat?riel.
