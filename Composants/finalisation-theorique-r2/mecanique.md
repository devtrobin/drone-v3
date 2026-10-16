# Mécanique R2

Repère : X transversal, Y vers l’arrière, Z vertical ; sol Z0. Dessus du plateau Z11 ; axes Z31.5 ; essieu avant Y55, arrière Y445. Les cotes X suivantes décrivent le côté droit ; le gauche est symétrique.

## Dimensionnement et matière

Masse de calcul 9 kg, part avant 45%, charge verticale 3 g. Arbres C45E avec **Re minimal 355 MPa exigé au certificat** ; cette valeur n’est pas déduite du seul nom C45. Paliers 6082-T6, arêtes cassées 0.2 ; aucune capacité de tournage ou d’alésage de la CNC circuits n’est supposée.

Pour la sortie arrière : charge verticale de travail **72.84 N par roue**, porte-à-faux 7 mm, couple d’étude 0.5 N.m, facteurs d’entaille 2 en flexion/1.5 en torsion. Équivalent calculé **98.5 MPa**, comparé à 177.5 MPa (Re/2). C’est un contrôle statique simplifié : pas de fatigue, impact local de denture, défaut de serrage ou calcul d’éléments finis. Le couple 0.5 N.m n’est pas une limite active imposée aux moteurs.

## Arbres, retenues et entretoises

Les stations complètes figurent dans[empilages-arbres.csv](plans/empilages-arbres.csv). Les longueurs de l’arbre comprennent l’extrémité filetée.

| Pièce | Longueur | Points définis |
| --- | ---: | --- |
| R201 intermédiaire |91.5 mm|X95..186.5 ; roulements 99..103 et 179..183 ; pignon 24 inversé 106..122 ; couronne 54 128..140|
| R202 sortie |145.5 mm|X73..218.5 ; épaulementØ7 105..108 ; roulements 108..112 et 191..195 ; rotor 80..88 ; couronne 117..129|
| R210 avant |42.5 mm|X176..218.5 ; roulements 178..182 et 190..194 ; entretoise 8 mm entre bagues intérieures|
| Extrémités de roues |M4 x 0.7 sur 10 mm|Épaulement à 208.5 ; goupilleØ2 à 202.5 ; position du fond hexagonal encore à relever D04|

Sorties : l’épaulement monoblocØ7 reprend l’effort axial, et l’empilage de bagues intérieures/entretoises/moyeu se referme par l’écrou de roue. Le rotor est captif entre un circlip DIN471-5 etun épaulementØ7 à X88..91 ; ses deux vis ne servent qu’au blocage de rotation. Intermédiaires : épaulement monoblocØ6 à X95..99 etun circlip en sortie, avecentretoise L1.8 ; les vis des engrenages ne sont pas les retenues axiales.

Quatre circlips DIN471-5 en acier àressort : gorgeØ4.80 +0/-0.05, largeur choisie 0.70..0.73, anneau nominal 0.60, d’après la fiche Beneri. Gorge intermédiaire X184.8..185.5, lèvre restante 1 mm au bout 186.5 ; gorge du rotor X79.3..80.0. La distance au bout excède le minimumcatalogue 0.3 mm. Le profil d’oreilles du STEP est reconstruit dans l’enveloppe de montageØ10.3 ; acheter les anneaux, ne pas les usiner depuis le STEP. Leur tenue catalogue ne remplace pas la vérification de la gorge usinée etdu jeu après montage. Les colliers miniatures hypothétiques sont supprimés.

L’appui intérieur est localisant ; l’extérieur dispose d’une poche 4.4 mm pour un roulement 4 mm. Régler le jeu axial de fonctionnement 0.05..0.15 mm avec des cales, sans précharger les deux bagues extérieures. Toutes les entretoises portent sur les **bagues intérieures uniquement**, Øextérieur 6 mm, Øintérieur 5.1 mm. Les cotes L62 et L7.5 sont des dimensions de fabrication, pas des tubes à couper à vue.

Les entretoises E6 arrière et 8.5 mm avant ont une encoche de passage de goupille sur leur face extérieure : largeur 2.1 mm, profondeur axiale 1 mm, suivant le STEP. La goupille est centrée sur la face arrière du moyeu X202.5. Le filetage M4 de 10 mm laisse environ 2.3 mm au-delà d’un écrou de 5 mm situé après la face de jante estimée X211.2 ; contrôler ces deux valeurs D04.

## Ajustements de prototype

Roulements de marque à jeu MC5 demandé et vérifié, pas simple sachet anonyme 5 x 11 x 4. Portées d’arbre appairées à l’alésage reçu, cible d’interférence 1..3 micromètres ; contrôle de rotation après montage. Les portées d’engrenage peuvent être dégagées 4.990..4.995 mm, sans entailler les portées de roulement ; méplats 0.3 mm. LogementsØ11H7 sous charge extérieure principalement fixe ; la sélection finale du jeu se confirme avec le fabricant du roulement. Ne pas attribuer automatiquement ces ajustements à n’importe quel MR115.

Exiger coaxialité des deux logements≤0.03 mm sur l’entraxe, battement des portées≤0.02 mm, parallélisme des faces d’entretoises≤0.02 mm. Ces exigences doivent être acceptées par l’atelier. Ne jamais faire passer un effort d’emmanchement par les billes.

Aux épaulements de roulement, rayon de raccordement≤0.1 mm ; ne pas appliquer le cassage d’arête général 0.2 mm àces portées. Les butées de direction sont des limites de débattement du prototype, sans qualification d’effort de blocage du gros servo : ne pas les utiliser pour calibrer en forçant. Les premiers essais restent bornés en courant etcommandés dans la plage±55°.

## Direction

Les pivots sont à X±170,Y55 ; centres de pneus à±200. La voie des **pivots 340 mm** sert à la géométrie d’Ackermann, les 400 mm décrivent les roues. Bras :23.83 mm vers l’intérieur et 40 mm vers l’arrière. Deux rotules sur le bras gauche, la seconde décalée de 4 mm vers l’intérieur et 8 mm vers l’arrière. Traverse à Z82 ; commande à Z90 pour éviter leur croisement. Palonnier R20, axe servo nominal(0,80).

Les longueurs sont **entre centres de rotules** :292.34 et 142.20 mm. Débit de tige M3 = entraxe - deux distances réelles centre-de-rotule/entrée de chape + deux engagements ; ces cotes de chape restent à mesurer. Engagement métallique minimal 4.5 mm ; montage dans le plastique selon la notice et la chape reçue. Il n’est pas possible de transformer honnêtement un entraxe connu en longueur de tige exacte avec une chape non cotée.

La table résout les fermetures de deux biellettes, pas une égalité forcée des angles de roues. L’erreur maximale de l’approximation Ackermann est 0.672° dans la plage testée par le solveur. Soft-limit servo±55° ; deux pionsØ3 par côté fixent les butées mécaniques à±25°, sur les supports R219 et R209. Contrôler leur contact avec les pièces réelles.

Couple servo requis **1.178 N.m**, coefficient de frottement 0.8, rayon effectif 45 mm, facteur 2 inclus et rapport cinématique réel. FT90M nominal 0.0686 N.m insuffisant. La page actuelle FT5335M indique 1.324 N.m nominal à 6 V ; marge théorique 1.12, sous réserve de recevoir cette révision. Le couple de blocage n’est pas utilisé comme couple continu.

À40 km/h : roue 3368 tr/min, intermédiaire 7579, moteur 25578. Les données KHK à bas régime ne qualifient pas ce service ; confirmation D01 indispensable.

## Carters

R215 : écran démontable en polycarbonate 2 mm, deux coquilles symétriques, et tubes de protection R216 sur les portions d’arbres accessibles. Ouverture moteurØ26 et passages d’arbre dégagés. Les fixations, la découpe des passages et le confinement du rotor Hall nécessitent une passe de finition ; les rapports identifient les éventuelles collisions restantes. Aucun confinement d’éclatement n’est revendiqué.
