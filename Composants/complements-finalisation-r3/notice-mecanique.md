# Notice mécanique de l’armature R3

Repère du projet enmm : X transversal, Y de l’avant vers l’arrière, Z vers le haut ; sol 0, dessus du plateau 11. Les STEP sont dans ce repère global. Les DXF de gabarits utilisent une origine locale indiquée dans le rapport DXF ; ne pas les superposer directement aux anciens plans.

## Matières et débit

- Quatre montants R301 : tube aluminium 10x 30x 1.5, L122, basZ14, hautZ136. CentresX±151 ; Y150 et 355. Tube ouvert en haut et en bas.
- Deux rails R303 : tube aluminium 30x 10x 1, L325, Y50..375, Z136..146. CentresX±151.
- Deux traverses R304 : même tube 30x 10x 1, L272, X−136..136 ; centresY60 et 335. Les deux extrémités sont en contact avec les faces intérieures des rails.
- Quatre éclisses R305 : aluminium 40x 30x 3, centresX±141/Y60 ou 335, sous-faceZ146. Quatre trousØ3.4 aux entraxes 20x 16.
- Six consoles R306 : plats aluminium 3 mm, trois 60x 20, un 65x 20 et deux 20x 115, sous-faceZ146. Les deux dernières avancent les bridesP06 de 95 mm depuis la traverseY335 ; leur table de perçage est en coordonnées globales.
- Huit brides : POM-C, bases 12x 24x 7 et capots 12x 24x 5 ; usiner l’alésageØ7.2 en réunissant les deux demi-pièces. Deux trousØ3.4, entraxe 16. Une garniture silicone 50 ShoreA nominal 0.5, largeur 10, longueur~21.5 par bride ; la CAO représente 0.35 comprimé. Les faces POM servent de butée de serrage.
- Bouchons de montants R312 : aluminium 6.9x 26.9x 12, taraudageM4x 0.7 ; retenue transversaleM3 àYlocal+8/Z130. La retenue ne traverse pas l’axe de la visM4.
- Entretoises R310 dans rails/traverses : aluminiumL8, OD5.5/ID3.4 pourM3, OD7/ID4.5 pourM4. Entretoises R313 dans montants : OD8/ID4.5 L7. Mettre les entretoises avant de fermer les tubes.

Choisir une matière aluminium dont Re≥200 MPa est attesté pour les pièces sollicitées ; sinon recalculer à partir du certificat matière. L’étude simplifiée porte sur 20 N au total sur les supports de câbles, pas sur une personne s’appuyant dessus ni un choc de véhicule.

## Montage et accès

Les montants se fixent par deuxM4 horizontales sur les ailes verticales des longerons L01 existants. Ajouter quatre trousØ4.5 par longeron : Y142,158,347,363 ; Z25 ; axeX. Une calePOM1 mm par vis couvre le jeu entre face extérieure du longeronX±145 et face du montantX±146. Ne pas ajouter de trous au plateauC01 pour cette armature.

Perçages, taraudages et positions : [table complète](plans/percages-globaux-r3.csv), [pièces](pieces.json), STEP et DXF associés. Une visM4x20 se visse dans le bouchon à travers le rail ; sa pénétration nominale est9.2mm. Les bouchons sont retenus parM3 décalées. Monter les éclisses, puis les consoles, entretoises et brides. Sur les tubes, le rectangle du DXF est un repère de gabarit de perçage, pas une instruction de découper une tôle.

Ébavurer les arêtes, casser les angles au contact des mains et des câbles. Vérifier que chaque entretoise est réellement prise entre les deux parois du tube avant serrage. Serrer les brides jusqu’au contact des faces POM ; vérifier retenue axiale, absence de pincement de gaine et température après essai. Les couples de serrage des bornes électriques restent ceux du fabricant.

L’armature se démonte indépendamment du support caméra. Les écrous des brides placées au-dessus des tubes restent accessibles avant mise en place de l’électronique. Ce montage nominal ne remplace pas la vérification de l’accès avec l’outillage réel.
