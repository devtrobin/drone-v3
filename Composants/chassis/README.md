<!-- finalisation-r2 -->
> **ÉtudeR2 du16octobre2026 :** [définition mécanique etimplantation révisées](../finalisation-theorique-r2/README.md). Les anciens arbres50mm etFT90M ne sont plus la définition nominaleR2 ; les réservations/interfaces non mesurées restent conditionnelles. Conserver les modèles/documents ci-dessous comme référencesA2-R1.
<!-- /finalisation-r2 -->

# Châssis A2-R1 - plateau ouvert

Conception du15 octobre2026 à partir de la [photo retenue](../../../image.png), des dossiers locaux et des spécificationsV3. Aucune recherche de pièce ni achat en ligne. Les matériaux, dimensions et interfaces propres au châssis sont choisis ici. Prototype non fabriqué, non testé.

- **Plateau520 x300 x3mm**, aluminium5754 H22 ;4 anglesR12,2 longerons en cornière25 x25 x3, longueur275.
- **Empattement390mm**, rouesØ63 x26, axes avantY55 et arrièreY445. Centres de rouesX±200 : voie400mm supposant un déport avant de30mm. Encombrement droit426mm en largeur ; réserver450mm au braquage±30°. Ce déport reste à contrôler sur roues/moyeux réels.
- **Garde au sol nominale8mm** sous plateau, avant têtes de vis, sangles, déformation et tolérances. Têtes sous plateau≤4mm. SolZ0, dessus du plateauZ11, axesZ31.5.
- BatterieG1 IC5 au centre et en bas ;2 sangles20 x250, patin140 x46 x2 et butées. Pont électronique160 x250 x2, démontable, sous-faceZ81.
- Deux moteurs arrière et deux roues avant directrices non motrices. Transmissions sur cassettes séparées, supports HallP1 repris avec H20.5mm.
- **Portique caméra métallique à2 montants**, comme la photoA2, réutilisant le berceauP1. Le montant/base bois du supportP1 restent une variante. Pivot arrière(0;482;231), déclinaison20°, réglage190-230 au-dessus du plateau.

## Fichiers

[Dossier de plans PDF](plans/plans-chassis-a2-r1.pdf) · [STEP et aperçus](3D/README.md) · [Découpe DXF](plans/README.md) · [Liste de débit](liste-debit.csv) · [Tous les perçages/contours](plans/percages-et-decoupes.csv) · [Pièces paramétrées](pieces.json) · [Implantation](implantation.json) · [Contrôles de conception](verification/conception.json).

Le PDF cote les bruts et décrit les perçages. Le CSV donne **chaque centre, diamètre et lumière** ; origine locale au coin bas gauche du rectangle brut de chaque pièce. Le DXF1:1 est généré depuis les mêmes solides que les STEP : aucune conversion d’image ou mise à l’échelle arbitraire. PourC01 : X_local=X_global+150, Y_local=Y_global. Pour toutes les autres pièces, voir origine/pose dans pieces.json.

## Matériaux et fabrication

5754H22 pour plateau/pont,6061T6 ou6082T6 pour traverse avant, montants et cornières. Pas de pliage à faire : cornières brutes coupées, percées et assemblées. PP compact pour les cassettes électriques ; nylon pour les petites cales et entretoises, silicone sous batterie. Le plastique doit être compatible avec température, serrage et isolation de l’équipement : aucun classement thermique/feu inventé.

Découpe CNC et perçage proposés ; aucune trajectoire d’outil ni machine supposée compatible. Brider sans déformer, laisser les attaches nécessaires, finir les chants. Fenêtres àR1 : fraiseØ2 ou reprise adaptée après contrôle. Contours±0.3, centres±0.15, trous de passage+0.2/0 sont des exigences de conception à vérifier avec l’atelier. Les rayons internes des cornières brutes ne sont pas représentés dans les L idéaux.

Masse des seules pièces plates estimée **2.264kg**, avecρaluminium2700kg/m³ etρPP910kg/m³, avant vis, profilés, équipements et câbles. Ce n’est pas la masse du véhicule. Aucun devis ou gain d’autonomie déduit de la CAO.

## Interfaces et essais restants

Le plateau principal porte les trous des **cassettes**, pas les trous supposés des nouveaux supports de fusibles. Les interfaces fournisseur encore incertaines sont à relever puis percer sur ces seules pièces démontables. Les gabaritsF0 et4 supportsKLKD sont des **réservations choisies**, pas des modèles constructeur ; confirmer leurs dimensions avant usiner leurs cassettes. FAUX de surveillance est inclus, sans oublier les3 résistances de mesure et les raccordements locaux.

La porteuseM1P140 x75 et ses quatre fixations sont reprises ; les2EVM sont réservés **séparément** sur deux cassettes isolantes. Le modulePololu2831, le2813, leD42V55F5, les WAGO et les dégagements d’accès aux pads Pi sont prévus. Ne pas utiliser les gabarits EVM superposés de l’ancien assemblage comme des modules réels fixés au PCB.

Le modèle implanté garde les composants simplifiés et nommés pour s’ouvrir rapidement : les filetages des rails, le relais/dissipateur et la coupure utilisent des gabarits allégés, avec les cotes extérieures des dossiers. ED80 : corps sous la face inférieure du panneauZ70, dessus du panneauZ73, extrémité des bornesZ15, soit4mm au-dessus du plateau. Le châssis nu et ses pièces plates sont les références de fabrication. Les engrenages sont des contours d’encombrement sans denture ; **empilage des arbres, retenues, fixations des paliers, platine moteur, carters et cinématique de direction restent à qualifier** à partir du montage réel. Les anciens arbres50mm sont des études, pas des axes à fabriquer. La sélection Losi/KHK conserve sa vérification d’appairage restante ; aucune vitesse réelle garantie.

Les contrôles de rotation portent sur les pneus et le châssis aux positions de conception. Ils n’incluent pas les fils ni toutes les pièces d’articulation non mesurées. Vérifier aussi la flexion du portique, les têtes sous plateau, le glissement du pack, l’accès aux protections et la convection du HS251. Le plateau métallique ne sert jamais de retour électrique. S65 et cordons de charge restent hors véhicule.

Conserver le rayon fixe≥30mm du SiF6mm² et les deux longueurs minimales≥85mm/≥120mm avantF0. Les fils de sortie5V du régulateur vers le Pi restent≤50mm, à contrôler sur le faisceau déployé. Câbles espacés, maintenus sur isolant, éloignés des roues/engrenages. Les parties tournantes doivent recevoir leurs carters avant entraînement ; ces derniers dépendent de l’empilage réel.

Le dossier permet de découper la **structure de prototype**, puis de faire les reports d’interface au montage à blanc. Il ne constitue pas une libération du véhicule complet à40km/h. Les objectifs d’autonomie, vidéo et liaison Wi-Fi restent inchangés et à mesurer. [Ordre du projet](../../PLAN-CONCEPTION.md) : prochaine étape, visserie finale.
