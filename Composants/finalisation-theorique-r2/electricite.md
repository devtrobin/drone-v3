# Électricité R2 - étude et raccordements

La protection M1P conserve son schéma et son routage contrôlés. **Aucun Gerber M1P ni seuil de surveillance n’est changé par cette révision.** Les documents R2 complètent l’intégration, sans supprimer les conditions de raccordement Li Po du dossier de surveillance.

## Nouvelle branche de direction

Après le relais de propulsion, depuis une sortie UD80 disponible : **FS candidat KLKD005.T /support L60030M1PQ → UBEC Hobbywing 30603003 → servo FT5335M**. Régler 6 V avant connexion. Positif et négatif 18AWG, ou 12AWG dans le support si sa plage 10..14AWG est conservée, puis transition vers 18AWG par WAGO. La borne du support ne reçoit pas de 18AWG hors plage. Cette position coupe aussi le servo en arrêt analogique dur : il ne doit pas continuer àdécharger le pack après la coupure des moteurs etdu Pi.

UBEC30603003 :2..6S, sortie 6/7.4/8.4 V,10 A continus/15 A de pointe,45 x 20 x 16.2 mm selon sa notice. Ne pas substituer l’ancien 30603000 au boîtier différent. Les BEC des ESC ne sont plus chargés par le servo ; leurs positifs ne sont jamais joints à l’UBEC ni au 5 V Pi.

Étude servo : prévoir jusqu’à 6 A à 6 V pour couvrir la fiche historique, même si la page récente cite 2.4 A. À6.4 V et rendement de calcul 80%, cela représente **7.03 A d’entrée en pointe**. FS5 A est un candidat à tester au démarrage ; ne pas le présenter comme un limiteur 5 A. Vérifier courant de repos, pointe et protection du fil d’usine du servo. La révision et le courant réel doivent être confirmés D02.

Avec 30 A moteurs,5.4 A Pi et environ 1 A de sortie servo en régime de travail, le besoin estimé dépasse l’ancienne enveloppe 36 A : **40 A devient l’enveloppe commune de calcul**. Avec 40 A moteurs etla pointe servo conservatrice, la pointe peut approcher 53 A. Le principal 50 A nécessite une vérification sur courbe/conditions réelles ; ce calcul ne démontre pas la sélectivité. L’inhibition douce par PWM conserve la direction, maisla coupure SSR ou ED80 coupe aussi son alimentation. Le courant etla dissipation du SSR doivent être réévalués avec cette nouvelle charge.

La tenue 6 V en fin de pack est une condition de recette non prouvée par la mention«2S» : vérifier la sortie UBEC sous les pointes du servo, jusqu’au seuil réel de surveillance, en incluant les chutes de câbles etdu SSR. Si la sortie sort de la plage du servo reçu, changer leconvertisseur oula révision servo/seuils avant de libérer ce couple. Les petits Pololu 6V2/2.5 A examinés ne couvrent pas automatiquement l’ancien scénario 6 A : aucun remplacement non qualifié n’est déclaré compatible.

Le parcours P02 dépasse la longueur utile du cordon seul. Ajouter au négatif un raccord TE32151 avec ATUM8/2 etune extension Si F6 mm² vers une 95R5 au D− ; la TE130191 directe de l’ancienne étude n’est alors plus montée. Provisionner 160 mm de Si F négatif en plus du conducteur d’origine àprésenter. Cette résistance supplémentaire n’est pas créditée dans la borne de défaut 16.4 k A, qui reste conservatrice. Les débits restent conditionnels aux approches de bornes.

## Masses et commandes PWM

Le faisceau précédent réunissait les masses de commande au Pi alors que les ESC et le Pi revenaient déjà au D− par leurs fils d’alimentation. En cas de mauvais retour de puissance, les petits fils GND peuvent devenir un chemin de retour. La solution R2 étudiée est **trois canaux ISO7710F indépendants**, un par ESC et un pour le servo, pas une isolation complète de toutes les alimentations du véhicule.

Côté entrée de chaque ISO7710FDR, boîtier SOIC8-D : broches 1 et 3 au 3.3 V Pi ;4 au GND Pi ;2 reçoit PWM à travers 220 ohms, avec rappel 10 kohms au GND Pi. Broche 7 non connectée. Côté sortie :8 au 3.3 V local,5 au GND local,6 vers le signal de l’actionneur à travers 220 ohms et rappel 10 kohms au GND local. Deux 100 n F au plus près des alimentations. Chaque 3.3 V local est obtenu par un MCP1703 A-3302 depuis le BEC/UBEC correspondant, avec condensateurs d’entrée/sortie 1µF effectifs minimum conformément à sa fiche.

Les trois domaines de sortie restent séparés sur le montage :BEC gauche/GND gauche, BEC droit/GND droit et UBEC servo/GND servo. Aucun pont GND1-GND2 sur les adaptateurs. Utiliser des adaptateurs SOIC8 à pistes séparées et vérifier leur continuité ; pas un module dont le plan de masse court-circuite les deux côtés. Schéma fonctionnel et brochage sont fournis, **aucune nouvelle carte routée n’est annoncée prête à fabriquer**.

Le suffixe F impose une sortie basse en perte d’alimentation d’entrée lorsque le côté sortie est alimenté ; cela ne neutralise pas une commande PWM qui resterait valide après gel logiciel. Le seuil ESC3.3 V et la réaction à l’absence d’impulsions restent à tester. Le Pi garde seul la commande ; aucune carte microcontrôleur n’est ajoutée.

Le[brochageR2](routage/brochage-gpio-r2.json) remplace les destinations directes desGPIO12/13/18 et desGND34/39. Les13contactsMolex restent13 ; les arrivées5V de puissance restent séparées. WARN1/WARN2 restent actifsHAUT, DONE resteGPIO22 ; ne pas réintroduire l’ancienne polarité.

## Protection et énergie

La borne conditionnelle de défaut 16.4 k A ne change pas : mêmes minimums de cuivre avant F0 et aucun chemin de retour alternatif crédité. Elle ne couvre pas les courts-circuits avant F0. Les trois confirmations D03 sur les supports, brins fins et énergie totale de coupure restent ouvertes. Aucun essai de court-circuit sur Li Po n’est proposé : le banc M1P utilise ses sources bornées et ses résistances de limitation.

Pack 2S5Ah nominal 37 Wh ; hypothèse 80% utilisables : **29.6 Wh**. Pour 45 min, puissance moyenne totale≤39.5 W ; pour 20 min≤88.8 W ; pour 10 min≤177.6 W. Ces budgets comprennent Pi, caméra, direction et pertes. Les 40 A sont une enveloppe de pointe/charge élevée, pas une consommation compatible 45 min. À très faible vitesse, le temps de fonctionnement ne croît pas indéfiniment : la consommation fixe Pi/vidéo subsiste.

Sources : [FEETECH actuel](https://www.feetechrc.com/84v-40kg-digital-steering-gear-ft5335m.html), [notice historiqueFEETECH](references/FEETECH-FT5335M-historique.pdf), [Hobbywing30603003](references/Hobbywing-UBEC10ACar.pdf), [TIISO7710](references/TI-ISO7710.pdf), [MCP1703A conservé](../carte-surveillance-electrique/notices/Microchip-MCP1703A-datasheet.pdf). Les différences entre versions sont conservées dans les conditions, pas moyennées.
