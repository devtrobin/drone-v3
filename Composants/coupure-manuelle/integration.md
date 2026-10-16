<!-- alimentation-r2 -->
> **Sélection active révisée le 15 octobre 2026.** ED80 conservé, après le nouveau F0 classe T et avant D+. La logique de surveillance alimentée avant ED80 et les voies de cellule restent à débrancher pour stockage. ED80 coupe les charges, pas une protection universelle du pack.
> [État électrique courant](../verification-alimentation/README.md) · [Raccordements](../verification-alimentation/integration.md). Les références différentes dans les documents ci-dessous sont historiques. Qualification matérielle non réalisée ; confirmations restantes explicites.
<!-- /alimentation-r2 -->

# Intégration - Coupure manuelle indépendante

14 octobre 2026. Aucune mise en service effectuée.

1. La chaîne positive proposée devient : batterie → MIDI 60 A → ED80 → MiniBus D+ → branches moteurs et Pi existantes. Le retour négatif D− est conservé. Cette mise à jour remplace le segment direct CP1+ MIDI vers D+ représenté dans le dossier de faisceau antérieur ; ses anciens PDF restent des instantanés datés.

2. CP1A+ rejoint MIDI sortie à ED80 entrée : fil 6 mm², cosse 95R5 côté M5 et nouvelle 95R6 côté M6. CP1B+ rejoint ED80 sortie à D+ P2 : 6 mm², 95R6 côté M6 et 95R5 côté goujon #10-32. Les deux 95R5 initiales sont réutilisées ; seules deux 95R6 sont ajoutées. Deux provisions de 0,20 m restent à adapter aux trajets définitifs.

3. L’ED80 ouvre mécaniquement l’alimentation commune des moteurs et du Pi, indépendamment du logiciel, du Wi-Fi et du relais électronique. Le fabricant réserve son usage à une rupture d’urgence ou à une isolation hors charge, pas à des commutations régulières sous charge. Pour l’arrêt normal, arrêter la commande et Linux par les fonctions prévues, puis isoler à vide.

4. Une ouverture d’urgence coupe brutalement le Pi et peut interrompre une écriture microSD. Le dispositif est unipolaire : le côté batterie du MIDI et les fils de mesure des cellules restent sous tension. La surveillance peut encore être alimentée par l’équilibrage. Pour intervenir, débrancher la prise principale et celle d’équilibrage. La coupure ne constitue pas une isolation galvanique complète du véhicule.

5. Les roues peuvent continuer à rouler après la coupure ; les condensateurs des ESC gardent une énergie résiduelle. Aucun freinage instantané ni arrêt télécommandé de sécurité n’est garanti. Le pouvoir de rupture de défaut publié, 500 A à 48 V dans les conditions Albright, ne qualifie pas le courant de court-circuit de notre pack ou le système complet.

6. Les bornes principales M6 sont données pour 3,6 à 3,9 N·m. Utiliser les cosses et l’outil/matrice compatibles avec le 6 mm² classe 5 selon Klauke ; vérifier appui, sertissage, isolation et décharge de traction. Les vis de fixation M5 fournies avec l’ED80 figurent seulement comme partie du dispositif ; l’adaptation au panneau et la visserie restante seront décidées avec le châssis.

7. Les Blue Sea 6006 et 9003E ont été écartés pour cette fonction : leur courant de conduction élevé ne remplace pas leur limite de commutation publiée de 25 A. Aucune extrapolation à une batterie 2S n’a été admise pour justifier la coupure des 44,39 A de l’hypothèse de calcul.

8. Les 40 mV typiques à 80 A donnent une résistance de contact neuf approximative de 0,5 mΩ. À 44,39 A, un modèle linéaire donnerait 22,2 mV et 0,985 W ; ce n’est pas une mesure ni une garantie. Le calibre thermique de 80 A dépend du montage et des conducteurs. Réserver la masse indicative de 223 g et l’enveloppe du plan 2024.

9. Positionner le bouton pour qu’il soit accessible une fois le châssis défini. Vérifier l’ouverture sur une charge contrôlée puis les défauts à faible vitesse. Réarmer manuellement après diagnostic seulement, roues immobiles et PWM au neutre ; aucun essai matériel effectué.

[Composants et achat](README.md), [modèles](3D/README.md), [notice PDF](notices/notice-coupure-manuelle-v3.pdf).
