"""French engineering review and fabrication/measurement handover, R2."""
from pathlib import Path
import json,csv,math,sys,hashlib,re
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pymupdf

ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Composants/finalisation-theorique-r2';V=B/'verification';PL=B/'plans'
def display(t):
    t=str(t)
    if 'http' in t:return t
    t=re.sub(r'(?<=[a-zà-ÿ])(?=[A-Z])',' ',t)
    t=re.sub(r'(?<=[a-zà-ÿ])(?=\d)',' ',t)
    t=re.sub(r'(?<=\d)(?=[a-zà-ÿ])',' ',t)
    t=re.sub(r'(?<=\d)(?=(?:MPa|kPa|Pa|A|V|W|N|Wh)\b)',' ',t)
    return t
def write(p,t):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.suffix=='.md':t='\n'.join(line if any(x in line for x in ['[',']','`','http']) else display(line) for line in t.splitlines())
    p.write_text(t.strip()+'\n',encoding='utf-8')
def dump(p,o):write(p,json.dumps(o,indent=2,ensure_ascii=False))
def csvout(p,rows):
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');w.writeheader();w.writerows(rows)
def load(p):return json.loads(p.read_text(encoding='utf-8'))

GATES=[
 dict(id='D01',type='documentaire',objet='Losi LOS212054 /KHK',condition='Confirmer angle de pression20°, largeur utile, régime admissible et charge radiale du moteur ; sinon changer le pignon et recalculer.',impact='Pas de libération de transmission motorisée. La CAO utilise un profil20° supposé.'),
 dict(id='D02',type='documentaire',objet='FEETECH FT5335M',condition='Obtenir la fiche correspondant au lot : la page actuelle25T/13.5kg.cm nominal à6V diffère de l’ancienne fiche17T/4A. Commander le palonnier assorti, rayon20mm.',impact='Servo retenu pour étude, pas panier validé. La fixation par berceau évite de recopier une empreinte incertaine.'),
 dict(id='D03',type='documentaire',objet='LFT /L60030M +JLLN /KLKD',condition='Confirmation des terminaisons à brins fins, de l’association DC et de l’énergie maximale de coupure à8.4V et aux défauts étudiés.',impact='La coordination électrique reste non démontrée ; un pouvoir de coupure catalogue ne suffit pas.'),
 dict(id='D04',type='mesure de réception',objet='Jante et moyeu HobbyPark /53569',condition='Relever la position du fond hexagonal et de la face d’écrou. Les stations202.5/208.5/211.2 proviennent du modèle estimé.',impact='Ajuster uniquement les entretoises de roue et les extrémités des arbres avant tournage final.'),
 dict(id='D05',type='mesure de réception',objet='ModulesTI, supports de fusibles, UBEC et palonnier',condition='Vérifier enveloppes, accès et fixations. Conserver les cassettes démontables, ne pas percer des empreintes supposées.',impact='Les réservations sont des limites d’étude, pas des dimensions fournisseur certifiées.'),
 dict(id='D06',type='conception à terminer après D03/D05',objet='Faisceau principal et ancrages',condition='Fixer les coordonnées des bornes et concevoir les supports des corridors hautsP03-P06 ; reprendre les descentes avecR≥30mm.',impact='P03-P06 restent des parcours candidats séparés ; ils sont exclus du STEP assemblé. Aucun débit définitif pour ces4liaisons.'),
 dict(id='D07',type='prototype électrique',objet='InterfacePWM isolée',condition='Assembler les trois canaux sur adaptateursSOIC indépendants, contrôler le schéma et les états au démarrage. Aucun nouveau Gerber n’est fourni.',impact='Évite les retours moteurs par les filsGND de commande ; circuit de banc défini, intégration à qualifier.'),
 dict(id='P01',type='essai',objet='Masse, charges et direction',condition='Peser le véhicule : ≤9kg et charge avant≤45% pour appliquer les calculs ; mesurer le couple et la température du servo.',impact='Recalcul obligatoire si ces hypothèses sont dépassées ; le couple de frottement au sol reste estimé.'),
 dict(id='P02',type='essai',objet='Transmission et interfaces',condition='Contrôler montage à blanc, portée des roulements, jeu d’engrènement, échauffement, vibrations et retenues sous écran.',impact='Les contrôles3D ne démontrent ni fatigue ni endurance ni confinement d’une rupture.'),
 dict(id='P03',type='essai',objet='Électricité /surveillanceM1P',condition='Suivre le banc limitéM1P avant touteLiPo ; vérifier courant, chute de tension, température, faux défauts et arrêt sur perte de commande.',impact='Conserver les interdictions de raccordement véhicule du dossierM1P.'),
 dict(id='P04',type='essai',objet='Vitesse, autonomie et vidéo',condition='Mesurer progressivement après qualification du prototype ; pas de40km/h en intérieur de bureau.',impact='40km/h,45min à20km/h et1080p60 restent des objectifs. Aucun essai ni achat effectué.')]

def docs(calc,k):
    write(B/'README.md',f'''# Finalisation théorique R2 - 16 octobre 2026

Cette révision traite les quatre volets demandés : mécanique, intégration, électricité et visserie. Elle ajoute des pièces et des calculs contrôlables. **Elle n’est pas une autorisation de fabriquer puis alimenter le véhicule complet : les points D01 à D07 restent ouverts.** Les essais et mesures de réception sont séparés dans le registre.

[Dossier PDF](plans/dossier-finalisation-r2.pdf) · [Mécanique](mecanique.md) · [Intégration](integration.md) · [Électricité](electricite.md) · [Visserie](../visserie-finale/README.md) · [Conditions restantes](conditions-restantes.md).

## Décisions de conception

- Enveloppe de calcul : **9 kg maximum, au plus45% sur l’avant**, cas vertical3g. Il s’agit de limites de calcul, pas d’une masse pesée.
- Deux transmissions7.59375:1 conservées ; arbres intermédiaires **91.5mm**, sorties **145.5mm**, axes avant **42.5mm**. Les arbres50mm historiques ne sont pas à fabriquer.
- Palier extérieur arrière porté àX±193, contre±171.5 précédemment ; porte-à-faux roue ramené de28.5 à **7mm**. Les deux C04 deviennent des platines93x90x3 sans ancien évidement.
- Rotors Hall àX±80, pieds àX±51 : leur nouvelle position évite les paliers et les dentures.
- [Retenues normaliséesDIN471-5](../retenues-axiales/README.md) : quatre circlips etdesépaulements monoblocs remplacent les petits colliers non définis.
- Deux fusées/fourches usinées remplacent les interfacesTamiyaA7/A6/50823 reconstruites et non mesurées. Moyeux53569, roues et famille de roulements conservés.
- FT90M retiré de la sélectionR2. **FT5335M à6V +UBEC Hobbywing30603003**, brancheFS candidate5A ; BEC desESC réservés aux interfaces de commande, jamais en parallèle.
- Direction à deux biellettes, résolue numériquement ; traverse **{k['tierod_ball_centers_mm']:.2f}mm**, commande **{k['draglink_ball_centers_mm']:.2f}mm entre centres de rotules**. Commande servo limitée à±55° ; roues sous25° dans l’étude.
- Interface de trois PWM isolés proposée pour supprimer les retours de puissance par les masses de commande. Schéma de banc détaillé ; aucune fabrication électronique supplémentaire déclarée prête.

## Livrables

- [Pièces STEP](3D/) et [liste des pièces](pieces.json) : repère global conservé ; filetages simplifiés géométriquement mais spécifiés dans les plans.
- [AssemblageR2 léger](../../Assemblage/R2/drone-v3-r2-etude.step), distinct des versions détailléesR1 existantes. Réservations et parcours non raccordés restent identifiés.
- [Empilages cotés](plans/empilages-arbres.csv), [perçagesR2](plans/percages-r2-global.csv), [surcoucheDXF](plans/surcouche-percages-r2.dxf).
- [Table de direction](table-direction.csv), [calculs](calculs.json), [parcours et débits candidats](routage/longueurs-cables.csv), [brochage actifR2](routage/brochage-gpio-r2.json).
- [Nomenclature de visserie](../visserie-finale/nomenclature.csv) et accessoires distincts des fixations fournisseur encore inconnues.
- [Rapports de contrôle](verification/), [sources consultées et archives](sources.json).

Les STEP de pièces sont des définitions nominales de l’étude. Les ajustements, les filetages et les exigences de matière se lisent dans les documents associés ; la CAO seule ne sert pas de calibre. Les plans et archivesR1 sont conservés et ne doivent pas être mélangés avec les piècesR2.
''')
    write(B/'mecanique.md',f'''# Mécanique R2

Repère : X transversal, Y vers l’arrière, Z vertical ; solZ0. Dessus du plateauZ11 ; axesZ31.5 ; essieu avantY55, arrièreY445. Les cotesX suivantes décrivent le côté droit ; le gauche est symétrique.

## Dimensionnement et matière

Masse de calcul9kg, part avant45%, charge verticale3g. ArbresC45E avec **Re minimal355MPa exigé au certificat** ; cette valeur n’est pas déduite du seul nomC45. Paliers6082-T6, arêtes cassées0.2 ; aucune capacité de tournage ou d’alésage de la CNC circuits n’est supposée.

Pour la sortie arrière : charge verticale de travail **{calc['rear_shaft']['radial_study_load_N']:.2f}N par roue**, porte-à-faux7mm, couple d’étude0.5N.m, facteurs d’entaille2 en flexion/1.5 en torsion. Équivalent calculé **{calc['rear_shaft']['von_mises_MPa']:.1f}MPa**, comparé à177.5MPa (Re/2). C’est un contrôle statique simplifié : pas de fatigue, impact local de denture, défaut de serrage ou calcul d’éléments finis. Le couple0.5N.m n’est pas une limite active imposée aux moteurs.

## Arbres, retenues et entretoises

Les stations complètes figurent dans[empilages-arbres.csv](plans/empilages-arbres.csv). Les longueurs de l’arbre comprennent l’extrémité filetée.

| Pièce | Longueur | Points définis |
| --- | ---: | --- |
| R201 intermédiaire |91.5mm|X95..186.5 ; roulements99..103 et179..183 ; pignon24 inversé106..122 ; couronne54 128..140|
| R202 sortie |145.5mm|X73..218.5 ; épaulementØ7 105..108 ; roulements108..112 et191..195 ; rotor80..88 ; couronne117..129|
| R210 avant |42.5mm|X176..218.5 ; roulements178..182 et190..194 ; entretoise8mm entre bagues intérieures|
| Extrémités de roues |M4x0.7 sur10mm|Épaulement à208.5 ; goupilleØ2 à202.5 ; position du fond hexagonal encore à releverD04|

Sorties : l’épaulement monoblocØ7 reprend l’effort axial, et l’empilage de bagues intérieures/entretoises/moyeu se referme par l’écrou de roue. Le rotor est captif entre un circlipDIN471-5 etun épaulementØ7 àX88..91 ; ses deux vis ne servent qu’au blocage de rotation. Intermédiaires : épaulement monoblocØ6 àX95..99 etun circlip en sortie, avecentretoiseL1.8 ; les vis des engrenages ne sont pas les retenues axiales.

Quatre circlipsDIN471-5 en acier àressort : gorgeØ4.80 +0/-0.05, largeur choisie0.70..0.73, anneau nominal0.60, d’après la ficheBeneri. Gorge intermédiaireX184.8..185.5, lèvre restante1mm au bout186.5 ; gorge du rotorX79.3..80.0. La distance au bout excède le minimumcatalogue0.3mm. Le profil d’oreilles duSTEP est reconstruit dans l’enveloppe de montageØ10.3 ; acheter les anneaux, ne pas les usiner depuis leSTEP. Leur tenue catalogue ne remplace pas la vérification de la gorge usinée etdu jeu après montage. Les colliers miniatures hypothétiques sont supprimés.

L’appui intérieur est localisant ; l’extérieur dispose d’une poche4.4mm pour un roulement4mm. Régler le jeu axial de fonctionnement0.05..0.15mm avec des cales, sans précharger les deux bagues extérieures. Toutes les entretoises portent sur les **bagues intérieures uniquement**, Øextérieur6mm, Øintérieur5.1mm. Les cotesL62 etL7.5 sont des dimensions de fabrication, pas des tubes à couper à vue.

Les entretoises E6 arrière et8.5mm avant ont une encoche de passage de goupille sur leur face extérieure : largeur2.1mm, profondeur axiale1mm, suivant leSTEP. La goupille est centrée sur la face arrière du moyeuX202.5. Le filetageM4 de10mm laisse environ2.3mm au-delà d’un écrou de5mm situé après la face de jante estiméeX211.2 ; contrôler ces deux valeursD04.

## Ajustements de prototype

Roulements de marque à jeuMC5 demandé et vérifié, pas simple sachet anonyme5x11x4. Portées d’arbre appairées à l’alésage reçu, cible d’interférence1..3micromètres ; contrôle de rotation après montage. Les portées d’engrenage peuvent être dégagées4.990..4.995mm, sans entailler les portées de roulement ; méplats0.3mm. LogementsØ11H7 sous charge extérieure principalement fixe ; la sélection finale du jeu se confirme avec le fabricant du roulement. Ne pas attribuer automatiquement ces ajustements à n’importe quelMR115.

Exiger coaxialité des deux logements≤0.03mm sur l’entraxe, battement des portées≤0.02mm, parallélisme des faces d’entretoises≤0.02mm. Ces exigences doivent être acceptées par l’atelier. Ne jamais faire passer un effort d’emmanchement par les billes.

Aux épaulements de roulement, rayon de raccordement≤0.1mm ; ne pas appliquer le cassage d’arête général0.2mm àces portées. Les butées de direction sont des limites de débattement du prototype, sans qualification d’effort de blocage du gros servo : ne pas les utiliser pour calibrer en forçant. Les premiers essais restent bornés en courant etcommandés dans la plage±55°.

## Direction

Les pivots sont àX±170,Y55 ; centres de pneus à±200. La voie des **pivots340mm** sert à la géométrie d’Ackermann, les400mm décrivent les roues. Bras :{k['arm_inward_mm']:.2f}mm vers l’intérieur et40mm vers l’arrière. Deux rotules sur le bras gauche, la seconde décalée de4mm vers l’intérieur et8mm vers l’arrière. Traverse àZ82 ; commande àZ90 pour éviter leur croisement. PalonnierR20, axe servo nominal(0,80).

Les longueurs sont **entre centres de rotules** :{k['tierod_ball_centers_mm']:.2f} et{k['draglink_ball_centers_mm']:.2f}mm. Débit de tigeM3 = entraxe - deux distances réelles centre-de-rotule/entrée de chape + deux engagements ; ces cotes de chape restent à mesurer. Engagement métallique minimal4.5mm ; montage dans le plastique selon la notice et la chape reçue. Il n’est pas possible de transformer honnêtement un entraxe connu en longueur de tige exacte avec une chape non cotée.

La table résout les fermetures de deux biellettes, pas une égalité forcée des angles de roues. L’erreur maximale de l’approximationAckermann est{k['max_ackermann_error_deg']:.3f}° dans la plage testée par le solveur. Soft-limit servo±55° ; deux pionsØ3 par côté fixent les butées mécaniques à±25°, sur les supportsR219 etR209. Contrôler leur contact avec les pièces réelles.

Couple servo requis **{calc['direction']['required_servo_torque_Nm']:.3f}N.m**, coefficient de frottement0.8, rayon effectif45mm, facteur2 inclus et rapport cinématique réel. FT90M nominal0.0686N.m insuffisant. La page actuelleFT5335M indique1.324N.m nominal à6V ; marge théorique{calc['direction']['margin']:.2f}, sous réserve de recevoir cette révision. Le couple de blocage n’est pas utilisé comme couple continu.

À40km/h : roue{calc['speeds']['wheel_rpm_40']:.0f}tr/min, intermédiaire{calc['speeds']['intermediate_rpm_40']:.0f}, moteur{calc['speeds']['motor_rpm_40']:.0f}. Les donnéesKHK à bas régime ne qualifient pas ce service ; confirmationD01 indispensable.

## Carters

R215 : écran démontable en polycarbonate2mm, deux coquilles symétriques, et tubes de protectionR216 sur les portions d’arbres accessibles. Ouverture moteurØ26 et passages d’arbre dégagés. Les fixations, la découpe des passages et le confinement du rotorHall nécessitent une passe de finition ; les rapports identifient les éventuelles collisions restantes. Aucun confinement d’éclatement n’est revendiqué.
''')
    write(B/'integration.md','''# Intégration R2

## Révisions de pièces et montage

Remplacer C04G/D par C04-R2 rectangulaires93x90x3 : l’ancien évidement est devenu inutile avec le déplacementHall. Reprendre C01/C03 avec les perçages additionnels fournis. Les fichiersSTEP C01-R2 etC03-R2 sont dans le repère global ; la surcoucheDXF porte le rectangle du plateau sur un calque de référence à ne pas découper.

Le CSV de perçage indique la pièce concernée. Les trousX±158 des fourches sont surC03, ceuxX±170/180 des paliers sont surC04, jamais dans le plateau de largeur300mm. Les arbres à fabriquer ne sont pas les fichiers d’étude50mm des anciens dossiers.

Servo : berceau de baseR212, cales latérales isolantes et deux brides à définir avec le lotD02 ; ne pas fraiser une cannelure17T ou25T supposée. Réutiliser un palonnier compatible du fabricant, rayon utile20mm. FT90M et son ancien supportC08 retirés. Le boîtier de servo représenté est une réservation ; sa position d’axe et les brides devront être figées après réception de la fiche du lot.

UBEC surR213, dessusZ45 ; interface de commande réservée derrière lui, hors de son enveloppe45x20x16.2. FS sur une cassette indépendante àX95,Y60. Ni l’UBEC ni les petits modules ne sont supposés posséder des trous non publiés.

## Câblage et dégagements

Le fichier[routage/parcours.json](routage/parcours.json) donne les points de passage, le diamètre d’enveloppe et le rayon de courbure. Les longueursCSV sont des **débits candidats**, incluant une provision explicitée. Les coordonnées de bornes non connues restent des points d’approche ; les parcours ne constituent pas un faisceau raccordé.

P01 conserve plus de205mm de conducteur avantF0, avec rayon30mm. Après présentation, placer le raccord pour conserver au moins85mm de conducteur10AWG d’origine et120mm deSiF ; ne pas les réduire au motif qu’un chemin court existe. Le calcul de défaut antérieur dépend de ces deux minimums.

P03-P06 requièrent des corridors hauts et des descentes qui ne sont pas encore définies aux bornes : ils restent **hors du STEP assemblé**. Leur fabrication n’est pas libérée. Cette difficulté d’encombrement est le résultat de la revue, elle n’est pas masquée par une spline qui traverserait les composants.

Liaisons5V Pi : garder chaque dérivation18AWG vers les pads≤50mm et de longueur égale entre positifs. Les tronçons communs régulateur/WAGO doivent aussi être inclus dans le calcul de chute de tension ; une limite par fil ne limite pas la longueur électrique totale. Cible de recette :5V mesuré surPi, courant5A et caméra/ventilateur actifs, budget d’impédance de boucle de sortie≤20milliohms hors régulateur, soit≤0.10V à5A. Ce budget est à vérifier, pas une résistance déjà mesurée.

Réserver au moins2mm aux pièces fixes, davantage aux pièces mobiles ; le disqueHall ne doit pas toucher sa retenue. Garde sous plateau8mm avant têtes de vis ; utiliser des têtes≤4mm sous plateau et contrôler la garde restante. Un rayon30mm ne s’applique pas automatiquement à l’USB : vérifier le câble reçu et sa notice.

## Contrôles

Les rapports séparent validité des solides, interférences nominales, montage estimé des roues et balayage échantillonné. Un balayage à pas1° ne prouve pas tout le mouvement continu ; les réservations n’attestent pas les cotes réelles. Toute collision non résolue dans les rapports interdit de qualifier l’assemblage comme prêt à fabriquer.
''')
    write(B/'electricite.md',f'''# Électricité R2 - étude et raccordements

La protectionM1P conserve son schéma et son routage contrôlés. **Aucun GerberM1P ni seuil de surveillance n’est changé par cette révision.** Les documentsR2 complètent l’intégration, sans supprimer les conditions de raccordementLiPo du dossier de surveillance.

## Nouvelle branche de direction

Après le relais de propulsion, depuis une sortieUD80 disponible : **FS candidat KLKD005.T /supportL60030M1PQ → UBEC Hobbywing30603003 → servoFT5335M**. Régler6V avant connexion. Positif et négatif18AWG, ou12AWG dans le support si sa plage10..14AWG est conservée, puis transition vers18AWG parWAGO. La borne du support ne reçoit pas de18AWG hors plage. Cette position coupe aussi le servo en arrêt analogique dur : il ne doit pas continuer àdécharger le pack après la coupure des moteurs etduPi.

UBEC30603003 :2..6S, sortie6/7.4/8.4V,10A continus/15A de pointe,45x20x16.2mm selon sa notice. Ne pas substituer l’ancien30603000 au boîtier différent. Les BEC desESC ne sont plus chargés par le servo ; leurs positifs ne sont jamais joints à l’UBEC ni au5V Pi.

Étude servo : prévoir jusqu’à6A à6V pour couvrir la fiche historique, même si la page récente cite2.4A. À6.4V et rendement de calcul80%, cela représente **7.03A d’entrée en pointe**. FS5A est un candidat à tester au démarrage ; ne pas le présenter comme un limiteur5A. Vérifier courant de repos, pointe et protection du fil d’usine du servo. La révision et le courant réel doivent être confirmésD02.

Avec30A moteurs,5.4A Pi et environ1A de sortie servo en régime de travail, le besoin estimé dépasse l’ancienne enveloppe36A : **40A devient l’enveloppe commune de calcul**. Avec40A moteurs etla pointe servo conservatrice, la pointe peut approcher53A. Le principal50A nécessite une vérification sur courbe/conditions réelles ; ce calcul ne démontre pas la sélectivité. L’inhibition douce parPWM conserve la direction, maisla coupureSSR ouED80 coupe aussi son alimentation. Le courant etla dissipation duSSR doivent être réévalués avec cette nouvelle charge.

La tenue6V en fin de pack est une condition de recette non prouvée par la mention«2S» : vérifier la sortieUBEC sous les pointes du servo, jusqu’au seuil réel de surveillance, en incluant les chutes de câbles etduSSR. Si la sortie sort de la plage du servo reçu, changer leconvertisseur oula révision servo/seuils avant de libérer ce couple. Les petitsPololu6V2/2.5A examinés ne couvrent pas automatiquement l’ancien scénario6A : aucun remplacement non qualifié n’est déclaré compatible.

Le parcoursP02 dépasse la longueur utile du cordon seul. Ajouter au négatif un raccordTE32151 avecATUM8/2 etune extensionSiF6mm² vers une95R5 auD− ; laTE130191 directe de l’ancienne étude n’est alors plus montée. Provisionner160mm deSiF négatif en plus du conducteur d’origine àprésenter. Cette résistance supplémentaire n’est pas créditée dans la borne de défaut16.4kA, qui reste conservatrice. Les débits restent conditionnels aux approches de bornes.

## Masses et commandesPWM

Le faisceau précédent réunissait les masses de commande auPi alors que lesESC et lePi revenaient déjà auD− par leurs fils d’alimentation. En cas de mauvais retour de puissance, les petits filsGND peuvent devenir un chemin de retour. La solutionR2 étudiée est **trois canauxISO7710F indépendants**, un parESC et un pour le servo, pas une isolation complète de toutes les alimentations du véhicule.

Côté entrée de chaqueISO7710FDR, boîtierSOIC8-D : broches1 et3 au3.3V Pi ;4 auGND Pi ;2 reçoitPWM à travers220ohms, avec rappel10kohms auGND Pi. Broche7 non connectée. Côté sortie :8 au3.3V local,5 auGND local,6 vers le signal de l’actionneur à travers220ohms et rappel10kohms auGND local. Deux100nF au plus près des alimentations. Chaque3.3V local est obtenu par unMCP1703A-3302 depuis leBEC/UBEC correspondant, avec condensateurs d’entrée/sortie1µF effectifs minimum conformément à sa fiche.

Les trois domaines de sortie restent séparés sur le montage :BEC gauche/GND gauche, BEC droit/GND droit etUBEC servo/GND servo. Aucun pontGND1-GND2 sur les adaptateurs. Utiliser des adaptateursSOIC8 à pistes séparées et vérifier leur continuité ; pas un module dont le plan de masse court-circuite les deux côtés. Schéma fonctionnel et brochage sont fournis, **aucune nouvelle carte routée n’est annoncée prête à fabriquer**.

Le suffixeF impose une sortie basse en perte d’alimentation d’entrée lorsque le côté sortie est alimenté ; cela ne neutralise pas une commandePWM qui resterait valide après gel logiciel. Le seuilESC3.3V et la réaction à l’absence d’impulsions restent à tester. LePi garde seul la commande ; aucune carte microcontrôleur n’est ajoutée.

Le[brochageR2](routage/brochage-gpio-r2.json) remplace les destinations directes desGPIO12/13/18 et desGND34/39. Les13contactsMolex restent13 ; les arrivées5V de puissance restent séparées. WARN1/WARN2 restent actifsHAUT, DONE resteGPIO22 ; ne pas réintroduire l’ancienne polarité.

## Protection et énergie

La borne conditionnelle de défaut16.4kA ne change pas : mêmes minimums de cuivre avantF0 et aucun chemin de retour alternatif crédité. Elle ne couvre pas les courts-circuits avantF0. Les trois confirmationsD03 sur les supports, brins fins et énergie totale de coupure restent ouvertes. Aucun essai de court-circuit surLiPo n’est proposé : le bancM1P utilise ses sources bornées et ses résistances de limitation.

Pack2S5Ah nominal37Wh ; hypothèse80% utilisables : **{calc['electricity']['energy_usable_study_Wh']:.1f}Wh**. Pour45min, puissance moyenne totale≤{calc['electricity']['power_budget_45min_W']:.1f}W ; pour20min≤{calc['electricity']['power_budget_20min_W']:.1f}W ; pour10min≤{calc['electricity']['power_budget_10min_W']:.1f}W. Ces budgets comprennentPi, caméra, direction et pertes. Les40A sont une enveloppe de pointe/charge élevée, pas une consommation compatible45min. À très faible vitesse, le temps de fonctionnement ne croît pas indéfiniment : la consommation fixePi/vidéo subsiste.

Sources : [FEETECH actuel](https://www.feetechrc.com/84v-40kg-digital-steering-gear-ft5335m.html), [notice historiqueFEETECH](references/FEETECH-FT5335M-historique.pdf), [Hobbywing30603003](references/Hobbywing-UBEC10ACar.pdf), [TIISO7710](references/TI-ISO7710.pdf), [MCP1703A conservé](../carte-surveillance-electrique/notices/Microchip-MCP1703A-datasheet.pdf). Les différences entre versions sont conservées dans les conditions, pas moyennées.
''')
    write(B/'conditions-restantes.md','# Conditions restantes - sans validation inventée\n\n'+ '\n\n'.join('## '+g['id']+' - '+g['objet']+'\n\n**'+g['type']+'**. '+g['condition']+'\n\n'+g['impact'] for g in GATES))
    dump(B/'conditions-restantes.json',GATES)
    write(B/'questions-fabricants-non-envoyees.md','''# Questions préparées - aucun message envoyé

## FEETECH /vendeur du lot FT5335M

Merci de fournir la fiche du lot proposé : couple nominal à6V, courant maximal et protection, cannelure, palonnier fourni et son rayon utile20mm, dessin coté du corps et axe de sortie. La page actuelle et la ficheV1.0 indiquent des cannelures/courants différents.

## Losi /KHK /Hobbywing

Confirmer l’angle de pression duLOS212054, son appairage avecSS0.5-54A20° àenviron25580tr/min moteur et le service des deux étages ; préciser la charge radiale admissible du2435G3 et les conditions de lubrification/durée de vie des engrenages àces régimes.

## Littelfuse

Confirmer LFT300601C +JLLN050.T et L60030M1PQ +KLKD aux courantsDC disponibles à8.4V, l’admission des conducteurs très souples/embouts, et les enveloppes maximales d’énergie totale de coupure aux courants pertinents. Distinguer leSCCR AC des conditionsDC. Fournir plans de montage des supports et capots.
''')
    write(ROOT/'Composants/visserie-finale/README.md','''# Visserie finale - définition nominale R2

[Nomenclature calculéeCSV](nomenclature.csv) · [Accessoires et interfaces](accessoires-et-interfaces.json) · [DossierR2](../finalisation-theorique-r2/README.md).

Les longueurs sont calculées sous tête, hors tête, **sauf les vis fraisées dont la longueur inclut la tête**. Pour les montages traversants : épaisseurs solides +rondelles +hauteur d’écrou +dépassement. Pour les taraudages : épaisseurs traversées +engagement, sans talonner dans le trou borgne. Les profondeurs et formes réelles des écrous restent à contrôler àréception. Les pieds de paliers sont taraudés àtravers8mm ; le léger dépassement desM3x16 intérieures reste hors des pièces mobiles.

Vis métal classe8.8 ou acier inoxydable dont les caractéristiques sont explicitement acceptées au calcul ; ne pas substituer automatiquement l’inox àl’acier. M3 dans aluminium : engagement6mm minimum ; M2 :4mm de travail ; têtes sous le plateau≤4mm. Écrous autofreinés pour les assemblages métalliques vibrants, rondelles larges sur les lumières ; ne pas écraser les plastiques.

Pas de couple universel appliqué aux bornes électriques, aux roues, au servo ou aux vis de pression. Les couples fabricant priment ; les assemblages propres au projet doivent être serrés avec contrôle de l’engagement et de la déformation. Les entretoises de laPi passent à15mm ; l’ancien exemple10mm ne définit plus leur hauteur.

Les fixations propres aux supports de fusibles et aux modules non cotés restent identifiées dans les accessoires. Le tableau ne constitue donc pas encore un panier exhaustif sans condition : aucune quantité de vis fournisseur n’a été inventée. Les éléments des kits déjà sélectionnés sont àdéduire du besoin après contrôle du contenu.
''')
    write(ROOT/'Assemblage/R2/README.md','''# AssemblageR2 - étude en cours de qualification

[FreeCAD léger](drone-v3-r2-etude.FCStd) · [STEP léger](drone-v3-r2-etude.step) · [Dossier de conceptionR2](../../Composants/finalisation-theorique-r2/README.md) · [Conditions restantes](../../Composants/finalisation-theorique-r2/conditions-restantes.md).

[Vue isométrique](apercu-r2-isometrique.png) · [Vue de dessus](apercu-r2-dessus.png). La réouverture du fichier natif est testée dans FreeCAD ; le parseur OCCT installé avec CAD Viewer accepte le STEP. Ces contrôles de lecture ne qualifient pas les interfaces mécaniques.

Cet assemblage remplace les anciennes études d’arbres/fourches et leFT90M par les propositionsR2, ajoute les paliers, supports, branche de direction et une partie des corridors de câbles. Il utilise les enveloppes légères des équipements. Les corridors hautsP03-P06 sont exclus parce que leurs supports et leurs descentes ne sont pas finalisés.

Les versions FreeCAD ultra détaillées dans le dossier parent restent des vues **A2-R1**. Ne pas les considérer comme contenant ces correctionsR2 ; leurs fichiers sont conservés sans écrasement. Les rapportsR2 distinguent les contrôles réussis et les interférences encore ouvertes.
''')
    # Update destination table without overwriting prior snapshot.
    pins=load(ROOT/'Composants/connecteur-gpio/brochage.json')
    for row in pins['pins']:
        n=row['physical_pin']
        if n==1:row['destination']='3.3V Pi, WARN et côtés entrée des3ISO7710F ; aucun BEC'
        if n in [12,32,33]:row['destination']='EntréeISO7710F canal '+{12:'servo',32:'ESC gauche',33:'ESC droit'}[n]+' ; GPIO ne rejoint plus directement l’actionneur'
        if n in [34,39]:row['destination']='GND Pi côté entréeISO ; pas de liaison directe auGND ESC'
    pins.update(revision='R2, proposition avec interfacePWM isolée',power_contacts_not_used=[2,4,6,9,14,20],contacts_installed=13,hardware_validated=False)
    dump(B/'routage/brochage-gpio-r2.json',pins)
    # Auditable cutlist for the interface; all three output domains are distinct.
    iso=[]
    for n,src,gpio in [('G','BEC_ESC_G',12),('D','BEC_ESC_D',13),('S','UBEC_SERVO',18)]:
        for pin,net in [(1,'3V3_PI'),(3,'3V3_PI'),(2,'PWM_'+n+'_220R'),(4,'GND_PI'),(5,'GND_'+src),(6,'OUT_'+n),(7,'NC'),(8,'3V3_'+src)]:iso.append(dict(device='ISO7710FDR_'+n,pin=pin,net=net,BCM=gpio if pin==2 else ''))
    csvout(B/'routage/interface-pwm-netlist.csv',iso)
    dump(B/'routage/interface-pwm-bom.json',dict(ISO7710FDR=3,MCP1703A_3302=3,C100nF=6,C1uF_effective_min=6,R220ohm=6,R10kohm=6,SOIC8_adapter_separate_rows=3,prototype_hand_wired=True,new_PCB_ready=False))


class PDF:
    def __init__(self,path):
        font=Path('C:/Windows/Fonts/arial.ttf');bold=Path('C:/Windows/Fonts/arialbd.ttf')
        pdfmetrics.registerFont(TTFont('F',str(font)));pdfmetrics.registerFont(TTFont('FB',str(bold)))
        self.c=canvas.Canvas(str(path),pagesize=(842,595));self.n=0;self.y=0
        self.c.setTitle('Drone V3 - Revue de conception R2 - 16 octobre 2026')
    def page(self,title,subtitle='Étude théorique sous conditions - prototype non fabriqué'):
        if self.n:self.footer();self.c.showPage()
        self.n+=1;self.y=517
        self.c.setFillColor(HexColor('#12304a'));self.c.rect(0,553,842,42,fill=1,stroke=0)
        self.c.setFillColor(HexColor('#ffffff'));self.c.setFont('FB',17);self.c.drawString(30,568,title)
        self.c.setFillColor(HexColor('#475569'));self.c.setFont('F',9);self.c.drawString(30,537,subtitle)
    def footer(self):
        self.c.setFillColor(HexColor('#64748b'));self.c.setFont('F',8);self.c.drawString(30,19,'Drone V3 | R2 | 16 octobre 2026 | cotes en mm | ne pas mélanger avec A2-R1')
        self.c.drawRightString(812,19,str(self.n))
    def text(self,t,size=10,gap=7,bold=False):
        t=display(t)
        lines=simpleSplit(t,'FB' if bold else 'F',size,782)
        self.c.setFillColor(HexColor('#182536'));self.c.setFont('FB' if bold else 'F',size)
        for l in lines:self.c.drawString(30,self.y,l);self.y-=size+4
        self.y-=gap
    def table(self,headers,rows,widths,size=8.5):
        c=self.c;lineh=size+3
        for ri,row in enumerate([headers]+rows):
            blocks=[simpleSplit(display(v),'FB' if ri==0 else 'F',size,w-10) for v,w in zip(row,widths)]
            h=max(len(x) for x in blocks)*lineh+9
            if self.y-h<45:self.page('Suite - tableau de définition')
            c.setFillColor(HexColor('#dce8f0' if ri==0 else '#f1f5f9' if ri%2 else '#ffffff'));c.rect(30,self.y-h,sum(widths),h,fill=1,stroke=0)
            x=30
            for lines,w in zip(blocks,widths):
                c.setFillColor(HexColor('#152c40'));c.setFont('FB' if ri==0 else 'F',size)
                for j,line in enumerate(lines):c.drawString(x+5,self.y-13-j*lineh,line)
                x+=w
            self.y-=h
        self.y-=10
    def save(self):self.footer();self.c.save()

def pdf(calc,k):
    p=PDF(PL/'dossier-finalisation-r2.pdf')
    p.page('Drone V3 - Finalisation théorique R2')
    p.text('Les quatre volets sont étudiés. Plusieurs conditions documentaires et de conception restent ouvertes ; le véhicule complet n’est pas libéré pour fabrication et mise sous tension.',11,12,True)
    p.table(['Volet','Résultat de la passe','Limite restante'],[
      ['Mécanique','Arbres cotés, paliers, nouvelle direction, carters et supportsR2','Appairage/régime des engrenages ; révision servo ; finition des fixations de carters'],
      ['Intégration','Assemblage distinctR2, perçages et chemins de câbles tracés','Interfaces fournisseur estimées ; corridors hauts et descentes non finalisés'],
      ['Électricité','Branche servo dédiée, budget courant/énergie révisé, isolationPWM étudiée','Coordination fusibles/supports et interface de banc à qualifier'],
      ['Visserie','Longueurs nominales calculées par empilage, accessoires séparés','Vis propres aux composants dont les plans sont absents']], [100,360,322],10)
    p.text('Référence de charge : masse maximale9kg, charge avant maximale45%, cas vertical3g. La masse réelle n’est pas connue. Les seules pièces platesA2-R1 étaient estimées à2.264kg.',10)
    p.text('Changements : FT90M remplacé dans l’étude ; nouvelles fusées/fourches ; palier extérieur arrière àX193 ; rotorsHall àX80 ; platinesC04 élargies et complétées.',10)
    p.text('Conserver le kitA2-R1 intact. Les nouvelles pièces sont dans finalisation-theorique-r2/3D et l’assemblage léger dans Assemblage/R2.',10)
    p.page('Arbres et empilages axiaux')
    p.text('Côté droit, X croissant vers la roue ; côté gauche symétrique. FiletagesM4 représentés au diamètre nominal dans lesSTEP. Les stations des roues restent conditionnées au déport réelD04.',10)
    stations=list(csv.DictReader((PL/'empilages-arbres.csv').open(encoding='utf-8-sig'),delimiter=';'))
    for code,label in [('R201','Intermédiaire - L91.5'),('R202','Sortie arrière - L145.5'),('R210','Avant - L42.5')]:
        rows=[r for r in stations if r['code']==code];xmin=min(float(r['x_debut']) for r in rows);xmax=max(float(r['x_fin']) for r in rows)
        c=p.c;y=p.y-38;scale=4.8 if xmax-xmin<100 else 4.6
        p.text(label,11,6,True)
        y=p.y-25
        labels=[]
        for i,r in enumerate(rows):
            a=float(r['x_debut']);b=float(r['x_fin']);x=45+(a-xmin)*scale;w=(b-a)*scale
            c.setFillColor(HexColor('#52738d' if 'roulement' in r['fonction'] else '#b67334' if 'couronne' in r['fonction'] or 'pignon' in r['fonction'] else '#c3d1dc'))
            c.rect(x,y,w,18,fill=1,stroke=0);c.setStrokeColor(HexColor('#ffffff'));c.line(x,y,x,y+18)
            labels.append((x,f'{a:g}'))
            if b-a>10:
                lab=str(r['fonction']).replace('couronne54 étage1','54d E1').replace('couronne54 étage2','54d E2').replace('pignon24 inversé','24d inv.').replace('entretoise','E ').replace('épaulement','Ép.')
                while pdfmetrics.stringWidth(lab,'F',7)>w-4:lab=lab[:-1]
                c.setFillColor(HexColor('#24364b'));c.setFont('F',7);c.drawCentredString(x+w/2,y+4,lab)
        labels.append((45+(xmax-xmin)*scale,f'{xmax:g}'))
        last_pos=-999;last_w=0
        for anchor,lab in labels:
            width=pdfmetrics.stringWidth(lab,'F',7);pos=max(anchor,last_pos+last_w/2+width/2+7)
            c.setStrokeColor(HexColor('#778b9c'));c.setLineWidth(.35);c.line(anchor,y,pos,y-10)
            c.setFillColor(HexColor('#24364b'));c.setFont('F',7);c.drawCentredString(pos,y-19,lab)
            last_pos=pos;last_w=width
        p.y=y-46
    p.text('Sortie : épaulement monoblocØ7 àX105..108 ; entretoises sur bagues intérieures seulement ; appui extérieur flottant0.4mm. Régler jeu axial0.05..0.15mm sans précharge des deux bagues extérieures.',10)
    p.page('Paliers, pièces et exigences de fabrication')
    specs=load(B/'pieces.json')
    selected=[s for s in specs if s['code'] in ['R203_palier_interieur_intermediaire','R204_palier_exterieur_intermediaire','R205_palier_interieur_sortie','R206_palier_sortie_porte_a_faux','R208_fusee_droite','R209_fourche_droite','R218_platine_moteur','R215_carter_transmission_droit']]
    p.table(['Pièce','Qté','Définition'],[[s['code'].replace('_',' '),s['quantity'],s['dimensions'] or s['description']] for s in selected],[235,35,512],8.5)
    p.text('Ajustements : portéesØ5 appairées au roulement reçu, interférence cible1..3µm et jeuMC5 ; logementØ11H7 ; poche extérieure4.4mm. Coaxialité des appuis≤0.03mm ; battement≤0.02mm ; entretoisesL±0.02mm.',10)
    p.text(f"Sortie arrière, contrôle statique : {calc['rear_shaft']['radial_study_load_N']:.1f}N à7mm, couple0.5N.m ; contrainte équivalente{calc['rear_shaft']['von_mises_MPa']:.1f}MPa <177.5MPa. Re355MPa minimal exigé ; contrôle simplifié, sans fatigue ni qualification du montage.",10)
    p.page('Direction - géométrie et commande')
    p.text(f"PivotsX±170,Y55 ; roueX±200 ; empattement390. Bras : {k['arm_inward_mm']:.2f} vers l’intérieur,40 vers l’arrière. TraverseZ82, commandeZ90, palonnierR20. Longueurs entre rotules : {k['tierod_ball_centers_mm']:.2f} /{k['draglink_ball_centers_mm']:.2f}.",11)
    rows=[]
    for phi in [-55,-40,-20,0,20,40,55]:
        r=min(k['rows'],key=lambda r:abs(r['servo_deg']-phi));rows.append([f"{r['servo_deg']:.2f}",f"{r['left_deg']:.2f}",f"{r['right_deg']:.2f}"])
    p.table(['Servo (°)','Roue gauche (°)','Roue droite (°)'],rows,[180,240,240],10)
    p.text(f"Couple requis{calc['direction']['required_servo_torque_Nm']:.3f}N.m, facteur2 inclus et rapport différentiel de la cinématique. FT90M insuffisant. FT5335M actuel :1.324N.m nominal à6V sous réserveD02 ; marge{calc['direction']['margin']:.2f}.",10)
    p.text('La table doit être calibrée avec le vrai palonnier et les jeux. Soft-limit±55° ; butées mécaniques±25° représentées par les pions etsupportsR219/R209. La longueur à couper des tiges dépend des chapes reçues ; entraxe connu ne signifie pas débit connu.',10)
    p.page('Routage et interfaces')
    routes=load(B/'routage/parcours.json')
    p.table(['Liaison','Rayon','Axe tracé','Brut candidat','Statut'],[[r['code']+' '+r['net'],str(r['bend_radius_mm']),str(r['centreline_mm']),str(r['blank_length_mm']),r['status']] for r in routes],[260,45,70,85,322],8)
    p.text('P03-P06 sont exclus de l’assemblageR2 : supports et descentes à finaliserD06. Les extrémités vers bornes non cotées sont des points d’approche. Les longueurs ne sont pas des cotes de coupe libérées.',9)
    p.page('Alimentation et commandes')
    p.text('Nouvelle branche : UD80 aprèsSSR ->FS candidat5A ->UBEC30603003 réglé6V ->FT5335M. Entrée support12AWG si plage10..14AWG ; transition18AWG parWAGO. Le servo est coupé en arrêt analogique dur. Vérifier la tenue6V àfin de pack sous pointe ; elle n’est pas prouvée. Ni les deuxBEC ni le5V Pi ne sont mis en parallèle.',11)
    p.text('CommandeR2 : troisISO7710F indépendants. EntréePi3.3V/GND ; sortie alimentée localement parBEC gauche, BEC droit ouUBEC servo, viaMCP1703A3.3V. Aucun pont de masse entre côtés des adaptateurs. Le suffixeF impose un défaut bas, sans neutraliser unPWM valide figé.',10)
    p.table(['ISO7710FDR - SOIC8','Connexion'],[['1 et3','VCC1 =3.3V Pi'],['2','IN :GPIO12,13 ou18,220ohms série et rappel10kohms'],['4','GND1 =GND Pi'],['5','GND2 =GND local de l’actionneur'],['6','OUT ->220ohms ->signal actionneur ; rappel10kohms local'],['7','NC'],['8','VCC2 =3.3V local, jamais6V direct']],[245,537],9)
    p.text('Découplage :100nF de chaque côté de chaqueISO ; LDO avec entrée/sortie1µF effectifs minimum. Adaptateurs et montage de banc à contrôler ; aucun nouveauPCB routé n’est livré.',10)
    p.text(f"Énergie de travail :{calc['electricity']['energy_usable_study_Wh']:.1f}Wh à80% de37Wh. Pour45min :≤{calc['electricity']['power_budget_45min_W']:.1f}W moyens tout compris. Enveloppe commune40A et pointe~53A : coordinationF0/FS àqualifier, aucun limiteur actif.",10)
    p.page('Énergie et limites de direction - scénario illustratif')
    scenarios=list(csv.DictReader((B/'scenarios-performance.csv').open(encoding='utf-8-sig'),delimiter=';'))
    p.text('Hypothèses :9kg, coefficient de roulement0.02, CdA0.08m², air1.2kg/m³, rendement de propulsion70%, consommation auxiliaire12W, énergie utilisable29.6Wh. Ces valeurs ne sont pas des mesures du véhicule.',11)
    p.table(['Vitesse km/h','Puissance totale W','Autonomie calculée min','Angle moyen proposé max°'],[[r['vitesse_kmh'],f"{float(r['puissance_totale_W']):.1f}",f"{float(r['autonomie_min']):.1f}",f"{float(r['angle_moyen_max_deg']):.2f}"] for r in scenarios],[160,200,220,202],11)
    p.text('Dans ce scénario, les objectifs45min à20km/h et10-20min à40km/h sont compatibles avec le budget d’énergie. Un autre roulement des pneus, la traînée, le rendement ou la puissance vidéo peuvent inverser cette conclusion. Mesurer avant de conclure.',10)
    p.text('La limite de direction suit un plafond de calcul de0.3g latéral etun plafond lent de22°. À40km/h, le rayon correspondant est d’environ42m : les grands braquages servent aux manœuvres lentes. Cette loi de commande est proposée, pas déployée ni une garantie de stabilité.',10)
    p.page('Visserie nominale et quantités')
    fast=list(csv.DictReader((ROOT/'Composants/visserie-finale/nomenclature.csv').open(encoding='utf-8-sig'),delimiter=';'))
    p.table(['Repère','Désignation','Qté','Affectation','Lmin /Lchoisie'],[[r['code'],r['designation'],r['quantite'],r['affectation'],r['longueur_min_mm']+' /'+r['longueur_retenue_mm']] for r in fast],[48,200,35,380,119],8)
    p.text('Sous plateau : tête≤4mm. Ne pas appliquer ces longueurs aux bornes d’appareils. Les interfaces fournisseur non cotées restent hors quantité définitive ; accessoires séparés dans leJSON de visserie.',9)
    p.page('Conditions restantes et libération')
    p.table(['ID','Type','Action avant libération'],[[g['id'],g['type'],g['objet']+' : '+g['condition']] for g in GATES],[42,160,580],8.2)
    p.text('Aucun achat, assemblage ou essai réel n’a été réalisé. Les points documentaires ouverts ne sont pas remplacés par une hypothèse favorable. Réponses fabricant non demandées automatiquement : questions préparées dans le dossier, aucun message envoyé.',9)
    p.page('Sources et lecture des fichiers')
    for r in load(B/'sources.json'):
        p.text(r['url'],9,3);p.text(r['note']+' | Archive locale : '+('oui' if r['archived'] else 'non, consulter la source'),9,10)
    p.text('Les rapportsJSON donnent la portée exacte des contrôles. LeSTEP assemblé est une vue d’étude ; les modèles détaillésFreeCADA2-R1 ne contiennent pas les modificationsR2. Les pièces isolées et plansR2 doivent être utilisés ensemble.',10)
    p.save()
    # Render every page for mandatory visual inspection; no delivery screenshots.
    render=ROOT/'tools/temp/finalisation-r2/pdf';render.mkdir(parents=True,exist_ok=True)
    doc=pymupdf.open(PL/'dossier-finalisation-r2.pdf')
    pages=[]
    for i,page in enumerate(doc):
        image=render/f'page-{i+1:02d}.png';page.get_pixmap(matrix=pymupdf.Matrix(1.35,1.35)).save(image)
        rects=[span['bbox'] for b in page.get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for span in l['spans']]
        assert all(x0>=18 and y0>=8 and x1<=830 and y1<=589 for x0,y0,x1,y1 in rects),(i,'text overflow')
        pages.append(dict(page=i+1,render=str(image.relative_to(ROOT)),text_characters=len(page.get_text()),text_within_page=True))
    dump(V/'pdf.json',dict(pages=pages,page_count=len(pages),all_pages_rendered=True,visual_review_pending=True))
    print('PDF',len(pages),'pages',flush=True)

def main():
    sys.stdout.reconfigure(encoding='utf-8');calc=load(B/'calculs.json');k=load(B/'cinematique.json')
    k['rows']=list(csv.DictReader((B/'table-direction.csv').open(encoding='utf-8-sig'),delimiter=';'))
    for r in k['rows']:
        for key in r:r[key]=float(r[key])
    docs(calc,k);pdf(calc,k)
if __name__=='__main__':main()
