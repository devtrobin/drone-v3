# Intégration des fixations - étude provisoire

Le châssis est le dernier composant à concevoir. Réserver quatre fixations aux coins du Pi, sans choisir maintenant l'implantation sur le véhicule, la hauteur finale ni l'épaisseur du châssis. Plusieurs hauteurs du kit servent à explorer ce choix ultérieur.

## Configuration étudiée

Quatre MF 10+6 mm, goujon mâle vers le haut. Une vis M2.5 x 8 et une rondelle par point attachent le corps au panneau futur. Le Pi repose sur les quatre corps ; une rondelle et un écrou par point retiennent la carte sur le goujon. Ce sont cinq pièces par point et vingt au total.

La CAO dessine les filetages en position d'engrènement ; elle ne dessine ni châssis ni PCB. Hauteur 10 mm, carte 1,6 mm, panneau 2 mm et rondelles 0,5 mm sont des hypothèses révisables. Engagement inférieur 5,5 mm et dépassement supérieur 1,9 mm ne valent que pour ces hypothèses. Voir cotes.md et calculs.json.

## Montage proposé après réception et étude du châssis

1. Hors alimentation, contrôler la variante M2.5 et le contenu du lot. Mesurer hauteurs, surplats, diamètre et épaisseur des rondelles, longueur des vis, pas, profondeur réelle des taraudages et épaisseur locale de carte. Les formes commerciales ne sont pas un plan de fabrication.
2. Vérifier l'accès à la microSD, au bouton du Pi, à l'USB caméra, au refroidisseur, au GPIO et à tous les câbles. Contrôler dessous de carte, appui des quatre corps et face d'appui des rondelles. Utiliser les quatre trous de carte ; les deux trous du cooler ont une autre fonction.
3. Choisir la hauteur finale et les vis avec un engagement suffisant sans fond de taraudage atteint, ni extrémité en contact avec un composant. Le châssis doit fournir quatre appuis coplanaires ; ne pas contraindre le PCB pour corriger un décalage de perçage.
4. Engager chaque filetage à la main. Immobiliser doucement le corps sur ses méplats, poser les rondelles et serrer progressivement les quatre points avec un petit outil adapté. Aucun couple fabricant chiffré du lot trouvé : ne pas lui appliquer un couple de vis acier.
5. Vérifier que la carte ne fléchit pas, que les pièces ne tournent pas librement et qu'aucune rondelle/vis ne gêne les connecteurs. Reprendre les mesures si un taraudage force ; ne pas agrandir les trous du Pi pour adapter un lot M3.
6. Après premiers essais progressifs, contrôler maintien, fissures, desserrage et frottements des câbles. La tenue dynamique doit être vérifiée sur le véhicule final ; une géométrie STEP valide n'est pas un essai de choc à 40 km/h.

Les rondelles répartissent localement l'appui ; elles ne transforment pas les écrous simples en écrous autofreinés. Ne pas attribuer de propriété de blocage, de classe thermique ou de qualité nylon 6/6 au lot sans données. Les fixations servent au Pi, pas aux moteurs, à la batterie ou aux organes de direction.

L'Active Cooler utilise ses propres clips fournis. Les dégagements Pi/cooler/GPIO restent ceux des études existantes ; ce dossier ne corrige ni ne valide automatiquement leurs modèles. Les fils doivent être maintenus par le maintien de faisceau afin de limiter les efforts sur la carte.
