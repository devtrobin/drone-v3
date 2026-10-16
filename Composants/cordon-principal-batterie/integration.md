<!-- alimentation-r2 -->
> **Sélection active révisée le 15 octobre 2026.** Positif CP0+ préparé sans cosse M5 vers le support classe T ; négatif CP0− avec une TE 130191 vers D−. Une seule cosse 130191 active, pas deux. Les STEP et l’ancien PDF avec deux cosses sont historiques.
> [État électrique courant](../verification-alimentation/README.md) · [Raccordements](../verification-alimentation/integration.md). Les références différentes dans les documents ci-dessous sont historiques. Qualification matérielle non réalisée ; confirmations restantes explicites.
<!-- /alimentation-r2 -->

# Montage du cordon IC5 actif

1. Utiliser un seul pack Spektrum G1 SPMX50002S30H5, équipé IC5 d’usine. Ne pas modifier ses fils. Pour cette version, la Zeee XT60 n’est plus retenue. Côté véhicule : SPMXCA510 « Device », distinct du SPMXCA505 « Battery » et des cordons série/parallèle.

2. CP0+ : fil rouge 10 AWG du 510 → TE 130191 → entrée MIDI M5. CP0- : fil noir 10 AWG du 510 → TE 130191 → MiniBus D- N2 #10-32. Après MIDI, le positif traverse ED80 puis D+ P2 par les deux segments 6 mm² existants ; l’UD80 A conserve son arrivée 6 mm².

3. Les deux fils 10 AWG sont inclus dans le 510 : aucun nouveau lot de fil pour CP0. Longueur publiée : 4 pouces, soit 101,6 mm, arrondie à 100 mm chez les vendeurs ; origine de mesure et dénudage d’usine non cotés. Mesurer le lot. Placer le MIDI près du pack et adapter l’implantation à la longueur utile, en gardant court le segment positif non protégé.

4. La photo officielle du 510 montre deux fils de puissance et aucun fil Smart libre. Ne pas ajouter de liaison de télémétrie au Pi. Le pack G1 conserve sa prise d’équilibrage B0/B1/B2 ; schéma et protection des petites liaisons de surveillance restent pour la phase finale. B1 n’est jamais le retour de puissance.

5. Avant sertissage, vérifier conducteur et extrémités d’usine. Si elles sont pré-étamées à la soudure, retirer cette portion et redénuder un conducteur intact. L’étamage individuel de surface des brins, s’il existe, est distinct d’un paquet rigidifié à la soudure. La longueur utile dépend de cette préparation ; les fils du STEP installé mesurent environ 93 mm, à titre d’étude.

6. TE 130191 admet 12-10 AWG /2,62-6,64 mm². Le guide SOLISTRAND cite l’outil 49935 ; la notice 408-1542 Rev P décrit la chambre 12-10 AWG, un dénudage standard de 6,35-7,14 mm, le positionnement de la paume et le cycle complet du cliquet. Faire confirmer outil/matrice et fil réel ; réaliser des éprouvettes et contrôler insertion, brins, tenue et résistance. Ne pas ajouter de soudure au sertissage.

7. Enfiler deux morceaux ATUM 8/2 d’environ 20 mm avant sertissage. Couvrir le canon et recouvrir la gaine du fil ; laisser la paume électrique libre. Diamètre installé et retrait jusqu’à 15 % à vérifier sur le lot. Chauffer localement selon TE : début de rétraction 80 °C, complète 110 °C ; ces températures ne sont pas le réglage du pistolet. La prise IC5 arrive pré-câblée : aucune soudure au connecteur n’est nécessaire ici.

8. Batterie et équilibrage débranchés, monter les cosses avec écrous et rondelles d’origine. MIDI M5 : 4,5 N·m proposé dans la plage commune des documents existants, lot à confirmer. MiniBus #10-32 : écart 1,69/2,03 N·m à résoudre avec la notice du lot ; aucun écrou M5 ou couple de 4,5 N·m par défaut. Retenir les fils hors des bornes et vérifier les capots. Fixations du châssis réservées pour la fin.

9. Contrôler polarité réelle, continuité de chaque pôle, absence de liaison +/-, isolement, clips et tenue mécanique. Première vérification avec source adaptée et limitée ; puis qualification du courant RMS et des pointes, chutes de tension et températures sur la durée et à l’ambiante prévues. Aucun court-circuit volontaire du pack.

10. Spektrum emploie un IC5 unique sur le Firma 100 A SPMXSE1100. Cette application motive le choix pour le scénario 44,39 A, par inférence ; elle ne donne pas une ampacité indépendante garantie du 510. Aucun chiffre de 120 A continus n’est attribué au connecteur. Fils du pack, 10 AWG du cordon et coordination du MIDI 60 A restent à qualifier. Un fusible ne limite pas activement le courant.

11. Charge : la FAQ Horizon permet l’emploi d’une G1 avec équilibrage sur un chargeur classique. Le S65 couvre la LiPo standard 2S, 8,4 V max ; réglage initial 1C = 5 A, soit 42 W en fin de charge. Un cordon/adaptateur de charge vers IC5 et la liaison JST-XH 2S sont nécessaires avant utilisation. Ils sont distincts du cordon embarqué à cosses. La G2 sans équilibrage ne peut pas remplacer la G1 avec ce chargeur.

12. Le pack est annoncé à 139 × 46 × 25 mm /294 g sur l’ancienne page fabricant. La référence G1 est arrêtée chez le fabricant ; RC Team affiche encore le SKU exact disponible à 49,99 EUR. Vérifier date, état et notice du lot avant achat. Énergie nominale 37 Wh contre 38,48 Wh pour la Zeee (-3,85 %), masse annoncée +44 g. Vitesse et autonomie restent des objectifs à mesurer ; aucune baisse de performance n’est actée.
