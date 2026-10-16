# Intégration R2

## Révisions de pièces et montage

Remplacer C04G/D par C04-R2 rectangulaires 93 x 90 x 3 : l’ancien évidement est devenu inutile avec le déplacement Hall. Reprendre C01/C03 avec les perçages additionnels fournis. Les fichiers STEP C01-R2 et C03-R2 sont dans le repère global ; la surcouche DXF porte le rectangle du plateau sur un calque de référence à ne pas découper.

Le CSV de perçage indique la pièce concernée. Les trous X±158 des fourches sont sur C03, ceux X±170/180 des paliers sont sur C04, jamais dans le plateau de largeur 300 mm. Les arbres à fabriquer ne sont pas les fichiers d’étude 50 mm des anciens dossiers.

Servo : berceau de base R212, cales latérales isolantes et deux brides à définir avec le lot D02 ; ne pas fraiser une cannelure 17T ou 25T supposée. Réutiliser un palonnier compatible du fabricant, rayon utile 20 mm. FT90M et son ancien support C08 retirés. Le boîtier de servo représenté est une réservation ; sa position d’axe et les brides devront être figées après réception de la fiche du lot.

UBEC sur R213, dessus Z45 ; interface de commande réservée derrière lui, hors de son enveloppe 45 x 20 x 16.2. FS sur une cassette indépendante à X95,Y60. Ni l’UBEC ni les petits modules ne sont supposés posséder des trous non publiés.

## Câblage et dégagements

Le fichier[routage/parcours.json](routage/parcours.json) donne les points de passage, le diamètre d’enveloppe et le rayon de courbure. Les longueursCSV sont des **débits candidats**, incluant une provision explicitée. Les coordonnées de bornes non connues restent des points d’approche ; les parcours ne constituent pas un faisceau raccordé.

P01 conserve plus de 205 mm de conducteur avant F0, avec rayon 30 mm. Après présentation, placer le raccord pour conserver au moins 85 mm de conducteur 10AWG d’origine et 120 mm de Si F ; ne pas les réduire au motif qu’un chemin court existe. Le calcul de défaut antérieur dépend de ces deux minimums.

P03-P06 requièrent des corridors hauts et des descentes qui ne sont pas encore définies aux bornes : ils restent **hors du STEP assemblé**. Leur fabrication n’est pas libérée. Cette difficulté d’encombrement est le résultat de la revue, elle n’est pas masquée par une spline qui traverserait les composants.

Liaisons 5 V Pi : garder chaque dérivation 18AWG vers les pads≤50 mm et de longueur égale entre positifs. Les tronçons communs régulateur/WAGO doivent aussi être inclus dans le calcul de chute de tension ; une limite par fil ne limite pas la longueur électrique totale. Cible de recette :5 V mesuré sur Pi, courant 5 A et caméra/ventilateur actifs, budget d’impédance de boucle de sortie≤20 milliohms hors régulateur, soit≤0.10 V à 5 A. Ce budget est à vérifier, pas une résistance déjà mesurée.

Réserver au moins 2 mm aux pièces fixes, davantage aux pièces mobiles ; le disque Hall ne doit pas toucher sa retenue. Garde sous plateau 8 mm avant têtes de vis ; utiliser des têtes≤4 mm sous plateau et contrôler la garde restante. Un rayon 30 mm ne s’applique pas automatiquement à l’USB : vérifier le câble reçu et sa notice.

## Contrôles

Les rapports séparent validité des solides, interférences nominales, montage estimé des roues et balayage échantillonné. Un balayage à pas 1° ne prouve pas tout le mouvement continu ; les réservations n’attestent pas les cotes réelles. Toute collision non résolue dans les rapports interdit de qualifier l’assemblage comme prêt à fabriquer.
