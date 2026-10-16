# Recherche complémentaire — QuicRun 2435SL G3 4 500 KV

Recherche du **12 octobre 2026**. Référence retenue : moteur G3 4 500 KV avec variateur WP16BL30 **G2**, annonce Amazon B0FM6D1F1W. Documents anglais lus et contrôlés visuellement ; aucun essai matériel exécuté.

## Ce qui est établi et ce qui reste ouvert

| Point | Résultat | Preuve / limite |
| --- | --- | --- |
| Contenu de l'offre | Un moteur et un variateur | Variante et rubrique « Contenu du carton » de l'[annonce Amazon](https://www.amazon.fr/dp/B0FM6D1F1W), pas inventaire du colis reçu |
| Compacité | Corps Ø24 × 36 mm, masse publiée 61,2 g, axe Ø2 mm sorti de 12 mm | [Notice moteur locale](notices/QuicRun-2435SL-G3-notice-constructeur.pdf), section 03 ; corps 36 ±0,20 mm, sortie 12 ±0,5 mm sur le plan |
| Fixation | Groupes d'entraxes 14 / 16 / 17 mm, M2,5 et M3, trous profonds de 4 mm | Même notice, sections 03–04 ; profondeur du trou ne signifie pas longueur de vis à choisir sans tenir compte du support |
| Courant moteur | 2,1 A à vide publié ; 15 A Amazon sans conditions | Pas de courbe courant/couple/régime trouvée ; aucun de ces nombres ne donne la consommation à 20 ou 40 km/h |
| Variateur | 30 A continus annoncés ; masse 38,5 g, corps 33,4 × 26,8 × 15,1 mm | [Fiche constructeur actuelle](https://www.hobbywing.com/en/products/quicrun-wp-16bl30-g2) ; limite annoncée, pas consommation ni essai thermique V3 |
| Batterie | Moteur 4 500 KV et ESC compatibles 2–3S | Notices ; scénario 2S pour commencer, batterie non choisie |
| Alimentation auxiliaire BEC | 6 / 7,4 V ; courant contradictoire selon source | 1,5 A dans la notice G2 / 2 A dans la fiche actuelle ; pas de 5 V USB direct |
| Connecteurs | Phases moteur mâles 3,5 mm, ESC femelles 3,5 mm et entrée XT60 selon fiche actuelle | Photos et fiche ; vérifier la variante livrée avant fabrication du faisceau |
| Commande depuis le Raspberry Pi | ESC commandé via son câble de commande, pas par USB | Brochage, niveaux logiques, fréquence et plage d'impulsion de notre contrôleur à confirmer ; aucune compatibilité GPIO 3,3 V garantie trouvée |

La fiche moteur officielle donne le numéro **30404002** pour le G3 4 500 KV. Certains vendeurs utilisent d'autres références commerciales (notamment 30404004) : conserver le modèle, la génération et les KV comme critères de réception, sans présumer une équivalence de révision.

## Divergences documentaires

### BEC : 1,5 A ou 2 A

Le tableau section 03 de la [notice variateur du 11 mars 2025](notices/QuicRun-WP16BL30-G2-notice-constructeur.pdf) indique 1,5 A pour le WP16BL30 G2. La [fiche web actuelle](https://www.hobbywing.com/en/products/quicrun-wp-16bl30-g2) indique 2 A continus, avec une pointe de 4 A dans la présentation. Aucune explication de révision n'est établie. Ne pas dimensionner une alimentation indispensable sur le seul chiffre supérieur.

La notice explique que le fil rouge du câble de commande fournit le BEC. Avec une alimentation séparée du contrôleur, ce fil doit être isolé selon le câblage retenu ; ne pas mettre deux sorties BEC en parallèle. Les masses de signal et les protections doivent être conçues avec la branche d'alimentation 5 V.

### Générations et variantes

Le 2435 **G2** est une autre génération : ses valeurs 73 g, axe 2,3 mm et deux pôles ne décrivent pas notre G3. Le G3 **6 500 KV** est limité au 2S dans sa notice ; ne pas recopier cette ligne dans la fiche du 4 500 KV. Le variateur WP16BL30 **G1** a également sa propre documentation. La page G2 conserve une mention de moteur G2 dans un champ alors que sa présentation cite le G3 : les notices et le contenu réel du kit doivent être contrôlés ensemble.

Les champs génériques Amazon affichent notamment « 4 500 tr/min », 250 g et 15 A. Ils ne remplacent pas le régime par volt du moteur, sa masse seule ou une mesure de courant. À 7,4 V, 4 500 KV donne **33 300 tr/min théoriques à vide** ; ce calcul n'est ni un régime chargé ni une vitesse du véhicule.

## Fonctions utiles à notre architecture

La notice G2 décrit un mode avec freinage puis marche arrière : après une commande de frein, retour au neutre et nouvelle commande de recul lorsque le moteur est arrêté. Le logiciel devra respecter cette séquence pour chaque roue. Le mode de renversement immédiat existe aussi, mais n'est pas notre réglage initial retenu.

L'étalonnage enregistre neutre, pleine marche avant et plein frein avec le bouton SET. Chaque variateur devra être étalonné avec le contrôleur réellement utilisé. Le réglage de l'accélération (« punch »), du freinage et du neutre est documenté ; leurs valeurs finales sont à déterminer par essais. Les signaux proposés pour un autre ESC ne deviennent pas des caractéristiques garanties de celui-ci.

La notice prévoit une protection de basse tension avec réduction de puissance avant coupure ; ce n'est pas un arrêt immédiat de tous les circuits. Elle demande aussi de configurer le comportement sur perte de commande. Si notre logiciel se fige en continuant à émettre une commande valide, la perte Wi-Fi n'est pas nécessairement visible du variateur : prévoir et tester un arrêt supervisé. Le délai d'arrêt effectif n'est pas mesuré.

## Retours d'utilisation

Les observations ci-dessous sont des témoignages directs, pas des essais reproductibles du drone V3. Les identifiants permettent de retrouver les avis dans l'[annonce du kit](https://www.amazon.fr/dp/B0FM6D1F1W).

| Retour consulté | Observation résumée | Limite |
| --- | --- | --- |
| Anthony, 29 décembre 2025, avis R2U5MQOFM9W8JZ, achat vérifié, variante 4 500 KV | Installation sur Granite Grom ; signale un premier variateur défectueux remplacé et insiste sur le rapport de transmission | Pas de courant, durée, température ou vitesse enregistrés |
| Jerry V, 8 mai 2026, avis RJ8J5MXV5FWLF, achat vérifié, variante 4 500 KV | Installation sur Mojave Grom, programmation par bouton ou carte séparée | Observation d'intégration, pas preuve de notre autonomie |
| Mariano Hamilton, 11 juin 2026, avis RA0TKKMSXX0YB, achat vérifié, variante 4 500 KV | Rapporte une rupture d'axe en usage agressif | Cause exacte, charge et fréquence des défaillances inconnues |
| [Discussion Reddit sur des ruptures d'axes](https://www.reddit.com/r/rccars/comments/1c36nur/) | L'auteur cite explicitement le 2435SL 4 500 KV G3 et rapporte deux ruptures | Extrait indexé consulté ; discussion complète inaccessible via l'outil web, génération de l'ESC non prouvée |

Un avis de rupture concernant le **6 500 KV** est exclu des observations spécifiques à notre variante. Les témoignages ne permettent pas de calculer un taux de panne. Ils motivent la vérification du montage du pignon et des charges sur l'axe, déjà nécessaire pour notre transmission.

Requêtes complémentaires : `2435 4500 G3 test site:youtube.com`, `16BL30 G2 2435 site:youtube.com`, recherches de courbes de rendement et de plage de commande. Aucun essai YouTube attribuable à notre ensemble exact apportant des mesures de courant, de rendement et d'autonomie n'a été identifié dans les résultats consultés. Aucune vidéo non visionnée n'est utilisée comme preuve. Cela ne signifie pas qu'aucune vidéo ou courbe n'existe ailleurs.

## Conséquences pour deux moteurs arrière et une direction avant

L'architecture retenue est **deux roues arrière motrices et deux roues avant non motrices dédiées à la direction**. Chaque roue arrière nécessite son moteur, son ESC et sa réduction : deux kits sont retenus, sans achat effectué. La coordination des vitesses arrière en virage reste à concevoir.

Il faut adapter l'inversion de phases d'un côté au sens d'avance mécanique, coordonner freinage et recul des deux roues, et mesurer la symétrie des vitesses. Aucune courbe de démarrage ni précision de conduite lente n'est établie pour notre charge avec ces moteurs sans capteur. Les axes de roue sur roulements reprendront le poids du véhicule : l'axe moteur Ø2 mm ne remplace pas un axe porteur.

Le train avant orientable, l'adhérence, le comportement en virage et la stabilité à 40 km/h restent à valider sur notre châssis. Le [dimensionnement V3](../../dimensionnement.md) conserve les objectifs énergétiques et les calculs conditionnels.

## Informations manquantes et validation à réception

| Donnée | Moyen de vérification |
| --- | --- |
| Révision et contenu exacts | Relever les marquages, KV, générations, notices livrées et connecteurs |
| Masse et encombrement installés | Peser séparément ; mesurer supports, pignons, câble et interrupteur |
| Régime, couple et consommation chargés | Mesurer vitesse et courant avec la réduction réelle ; ne pas déduire une courbe complète des KV |
| Signal de commande compatible | Confirmer niveaux, impulsions et fréquence avant connexion ; étalonner chaque ESC |
| Symétrie des entraînements | Essais limités, roues dégagées puis roulage lent ; vérifier neutre et sens d'avance |
| Freinage et perte de liaison | Tester séquences frein/recul, perte Wi-Fi et gel du contrôleur, puis relever délais et distances |
| Autonomies et échauffement | Mesurer Wh, courant, température et vitesse, vidéo active, à 20 puis 40 km/h dans un espace adapté |
| Direction avant et stabilité | Dimensionner servomoteur, biellettes et pivots ; vérifier la géométrie et le comportement sur le sol retenu |

La notice moteur demande un rapport initial conservateur et le contrôle de température ; son seuil de 100 °C est une limite constructeur, pas une température visée. La notice déconseille la pleine commande sans pignon installé. Aucun essai à vide à plein régime n'est proposé ici.

## Sources

- [Notice et repères de lecture](notices/README.md).
- [Fiche constructeur moteur G3](https://www.hobbywing.com/en/products/quicrun2435slg3.html).
- [Fiche constructeur variateur G2](https://www.hobbywing.com/en/products/quicrun-wp-16bl30-g2).
- [Annonce Amazon et avis consultés](https://www.amazon.fr/dp/B0FM6D1F1W).
- [Registre structuré et empreintes des fichiers](sources.json).
