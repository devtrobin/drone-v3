"""French dossier for a conditional main cord matching the currently selected pack."""
from pathlib import Path
import json,sys,hashlib
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/cordon-principal-batterie'
AMASS='https://www.china-amass.com/biao/283.html'
TE='https://www.te.com/en/product-130191.html'
BN='https://bntechgo.com/bntechgo-12-gauge-silicone-wire-kit-ultra-flexible-20-ft-black-and-red-each-color-10-ft-high-temp-200-c-600v-12-awg-silicone-wire-680-strands-of-tinned-copper-wire-stranded-wire-stranded-wire-for-model-battery/'
LUGBUY='https://www.digikey.fr/fr/products/detail/te-connectivity-amp-connectors/130191/1864623'
PLUGBUY='https://www.tme.eu/fr/details/xt60h-m/connecteurs-dc/amass/'
SOURCES=[
 dict(id='amass-current',url=AMASS,type='manufacturer',supports='35 A MAX, 12 AWG, élévation <85 K ; PA et contacts laiton doré ; pas une garantie à 44 A'),
 dict(id='amass-catalog',url='https://www.china-amass.com/public/upload/20260207/7fa24f5a6f35ec66c7a115c07a34ab06.pdf',type='manufacturer_pdf',local='notices/AMASS-catalogue-XT-2026-original.pdf',pages='page imprimée 15 / index 14',supports='XT60H-M 23,85 ×16,4 ×9,2 mm ; 35 A sous conditions ; XT90H 45 A sous conditions'),
 dict(id='amass-legacy',url='https://www.shoptronica.com/ficheros/XT60H.pdf',type='manufacturer_pdf_mirror',local='notices/AMASS-XT60H-V1.2-original.pdf',supports='30 A RC /60 A MC, entraxe 7,2 mm ; révision distincte'),
 dict(id='te-product',url=TE,type='manufacturer',supports='130191, 12-10 AWG /2,62-6,64 mm², oeillet 5,26 ; L19,3 ; paume0,79 ; canon ID3,28'),
 dict(id='te-datasheet-lcsc',url='https://datasheet.lcsc.com/datasheet/pdf/7c59fb4e89ed2939992bd29da7889710.pdf?productCode=C592185',type='manufacturer_pdf_mirror',local='notices/TE-130191-fiche-via-LCSC-original.pdf',supports='fiche TE de 4 pages, datée 01/07/2025 dans le document, pas le plan coté A3'),
 dict(id='te-guide',url='https://www.te.com/content/dam/te-com/documents/appliances/global/solistrand-terminals-and-splices-qrg.pdf',type='manufacturer_pdf_online',supports='p5 : variante130191 L19,10/W9,50/ID3,30 ; outils49935,58546-1,58545-1 ; écarts conservés'),
 dict(id='te-tool',url='https://www.farnell.com/datasheets/1922603.pdf',type='manufacturer_pdf_mirror',local='notices/TE-49935-notice-408-1542-via-Farnell-original.pdf',supports='sertissage des SOLISTRAND ; 12-10 AWG, dénudage6,35-7,14 mm standard ; contrôles de qualité'),
 dict(id='bntechgo',url=BN,type='manufacturer',local='references/BNTECHGO-12awg-page.html',supports='SKU big-SW12G68008F10C2 ; 680 brins étamés ; prix14,98USD ; image technique dans dossier fil existant'),
 dict(id='amazon-wire',url='https://www.amazon.fr/dp/B01ABOPMEI',type='marketplace_public_html',local='references/Amazon-FR-B01ABOPMEI.html',supports='titre12AWG/680/10ft par couleur ; 31,93EUR affichés, En stock, vendu et expédié Amazon US ; destination finale non vérifiée'),
 dict(id='amazon-plug-rejected',url='https://www.amazon.fr/dp/B074PN6N4K',type='marketplace_rejected',local='references/Amazon-FR-B074PN6N4K.html',supports='titre FR mélange disque dur/Sonos/XT60H ; indisponible ; fiche écartée comme preuve d’achat'),
 dict(id='digikey',url=LUGBUY,type='distributor_indexed_offer',supports='0,56EUR HT /0,672EUR TTC par pièce dans résultat indexé, prix indicatif ancien ; accès direct403 ; frais ouverts'),
 dict(id='tme',url=PLUGBUY,type='distributor_reference',supports='référence AMASS XT60H-M ; prix, stock actuel et livraison non vérifiés'),
 dict(id='lemon',url='https://www.lacameraembarquee.fr/cables-adaptateurs-connecteurs-fpv/14943-connecteur-amass-xt60h-male-avec-jupe-lemonfpv.html',type='seller_and_reviews',supports='H023-6-A, une prise mâle avec jupe ; 1,10EUR affiché sous Prix HT ; deux avis5/5 du7mars2025 ; sa revendication60Acontinu non reprise'),
 dict(id='hobbyking-guide',url='https://hobbyking.com/blog/xt60-soldering-guide-for-rc-builds',type='manufacturer_retailer_own_guide',supports='étamage séparé, pas de brins retranchés, logement de maintien, contrôle avant gaine ; pas procédure AMASS de durée/température'),
 dict(id='forum',url='https://www.rccrawler.com/forums/threads/battery-connectors.618927/',type='firsthand_users',supports='juin2020, préférence pour prises authentiques et maintien par prise complémentaire pendant soudure ; témoignage, pas certification'),
 dict(id='atum',url='https://www.te.com/en/product-NB11802001.html',type='manufacturer_shared_reference',supports='ATUM8/2 déjà documenté : ID8 fourni/2 libre, paroi1±0,3, adhésif0,5, rétraction110°C, longueur -15% max')]
PARTS=[
 dict(folder='prise-xt60h-m',ref='AMASS XT60H-M avec capot',qty=1,unit='prise',buy=PLUGBUY,role='Interface côté véhicule : contacts mâles, à brancher sur les contacts femelles du pack 2S actuellement choisi.',reuse='Une prise du lot déjà prévu, si lot confirmé authentique et en quantité suffisante ; sinon une pièce à acheter.',price=None,currency='EUR',cotes=[['Enveloppe actuelle M','23,85 ×16,4 ×9,2 mm','Catalogue AMASS2026 p15'],['Entraxe contacts','7,2 mm','Fiche V1.2 historique ; lot actuel à contrôler'],['Courant annoncé','35 A MAX /12 AWG /élévation <85 K','Document actuel ; 44,39 A non justifiés'],['Révision ancienne','30 A RC /60 A MC','V1.2 ; pas 60 A continu garantis']]),
 dict(folder='fils-12awg',ref='BNTECHGO SW12G68008F10C2',qty=.20,unit='m par couleur, provision',buy='https://www.amazon.fr/dp/B01ABOPMEI',role='Deux fils séparés, rouge CP0+ vers entrée MIDI, noir CP0- vers D- N2 ; 12 AWG compatible avec la section d’essai AMASS.',reuse='Prélever dans le lot déjà prévu : besoin total connu passe de0,40 à0,60 m par couleur ; pas un deuxième lot.',price=31.93,currency='EUR',cotes=[['Lot','3,048 m rouge +3,048 m noir','10 ft par couleur ; Amazon/BNTECHGO'],['Construction','680 brins Ø0,08 mm, cuivre étamé','Fabricant ; non mesuré'],['Diamètre','gaine4,5 ±0,1 ; faisceau2,41 mm','Offre /image technique archivée'],['Section','3,4 mm² annoncés ; AWG nominal3,31','Valeurs distinctes ; pas calcul de masse CAO'],['Résistance','5,06 mΩ/m','Image fabricant ; température non précisée']]),
 dict(folder='cosses-te-130191',ref='TE SOLISTRAND 130191',qty=2,unit='cosses',buy=LUGBUY,role='Une cosse sur goujon M5 de l’entrée MIDI ; une sur goujon #10-32 du MiniBus négatif N2.',reuse='Remplace uniquement les deux terminaisons Klauke95R5 conditionnelles de CP0 ; les autres95R5 restent prévues.',price=.672,currency='EUR',cotes=[['Section admise','12-10 AWG /2,62-6,64 mm²','Page TE ; sertissage avec fil680brins à qualifier'],['Oeillet','Ø5,26 mm, désignation M5','TE ; passage nominal sur #10-32 Ø4,826'],['Longueur','19,3 mm','Page et fiche TE2025'],['Paume','épaisseur0,79 mm','Page et fiche TE ; distributeurs0,99 divergents'],['Canon','Ø intérieur3,28 mm','TE ; profil extérieur non coté ici'],['Variante catalogue','L19,10 ; largeur9,50 ; ID3,30 mm','Guide TE ; non fusionnée avec fiche2025']]),
 dict(folder='isolation-atum',ref='TE/Raychem ATUM-8/2-0-STK',qty=2,unit='coupes provisionnelles de20mm',buy='https://www.te.com/en/product-NB11802001.html',role='Deux manchons noirs sur les canons nus des cosses ; jupe XT60H utilisée côté prise, fermeture et isolement à contrôler.',reuse='Même barre1,2m déjà prévue ; besoin CP0 ≈40mm, dont20mm peuvent remplacer la coupe positive conditionnelle ancienne. Pas de seconde barre.',price=None,currency='EUR',cotes=[['Avant rétraction','Ø intérieur ≥8 mm','Fiche TE ATUM du dossier partagé'],['Libre après rétraction','Ø intérieur ≤2 mm ; paroi1 ±0,3 mm','Valeurs libres, pas diamètre installé'],['Adhésif','0,5 mm nominal libre','Fiche TE ; installation représentée estimée'],['Chauffe','début80°C ; complète110°C','Température de rétraction, pas réglage pistolet'],['Longueur','retrait jusqu’à15%','Prévoir le recouvrement selon lot']])]
INTEGRATION=[
'Version d’étude conservant le pack Zeee 2S XT60 actuel. La prise réelle du pack, son sexe par contacts, la polarité, les fils d’usine et la révision doivent être contrôlés. Aucun changement de batterie n’a été décidé et aucun pack n’est modifié.',
'CP0+ : contact positif de la XT60H-M → fil rouge12AWG → TE130191 → entrée du porte-fusible MIDI M5. Le MIDI reste au plus près du pack : la longueur0,20m est une provision d’approvisionnement, pas une prescription de tronçon positif non protégé.',
'CP0- : contact négatif de la XT60H-M → fil noir12AWG → TE130191 → MiniBus négatif D- N2, goujon #10-32. L’œilØ5,26 offre un passage nominal ; vérifier paume, rondelle, appui et fermeture du capot. Conserver l’écrou #10-32 d’origine ; ne pas monter un écrou M5.',
'Le positif aval reste MIDI sortie → CP1A+6mm² → ED80 → CP1B+6mm² → D+ P2. CP2+/CP3+ et l’admission minimale6mm² de l’UD80A ne changent pas. Pas d’adaptateur XT60→XT90 et pas de fil6mm² forcé dans un godet12AWG.',
'Soudure côté XT60 : travailler sur le cordon détaché, sans batterie ni équilibrage. Passer le capot avant terminaison, contrôler ± sur la pièce réelle, dénuder selon le godet mesuré, étamer fil et godet sans grossir excessivement le faisceau, puis souder et immobiliser jusqu’au refroidissement. Aucun brin retiré. La géométrie CAO n’est pas une longueur de dénudage constructeur. Utiliser une prise complémentaire non alimentée comme maintien ; ne pas utiliser le pack comme gabarit.',
'Sertissage côté cosse : manchons déjà enfilés ; conducteur cuivre non pré-étamé à la soudure, avec tous ses brins. Le guide TE associe130191 aux49935 ou58546-1/matrice58545-1. La notice408-1542 décrit49935 et la chambre12-10AWG : dénudage standard6,35-7,14mm, paume orientée selon la figure et canon centré. Faire confirmer l’outil et son applicabilité au fil très fin680brins ; ne pas substituer automatiquement la pince Ancor pour cosses isolées. Réaliser et contrôler des éprouvettes avant les deux raccords finaux.',
'Gaine ATUM : recouvrir le canon et suffisamment la gaine silicone sans couvrir la paume électrique. Les coupes20mm sont provisionnelles : vérifier dimensions réelles et retrait. Chauffer localement selon TE, préserver prise et câble ; contrôler l’adhésif et l’absence de métal arrière accessible. Le capot XT60H doit fermer sans forcer sur une soudure ni pincer le fil ; vérifier son isolation réelle.',
'Sur batterie débranchée, conserver écrous et rondelles du porte-fusible et du MiniBus. MIDI : plage commune déjà documentée,4,5N·m proposé à vérifier sur le lot. MiniBus2315 : écart15in-lb/1,69N·m contre18in-lb/2,03N·m des pages consultées à résoudre avec la notice du lot, sans appliquer4,5N·m. Retenir les fils hors bornes ; support et visserie de châssis restent pour la fin.',
'Avant mise en service : continuité de chaque pôle, absence de liaison +/-, polarité à la prise et aux cosses, isolement, clips et tenue mécanique. Première vérification avec source adaptée limitée ; puis qualification instrumentée du courant moyen/RMS et pointes, chute de tension et échauffement sous usage réel. Aucun essai de court-circuit volontaire du pack.',
'44,39A est un scénario de dimensionnement, pas une consommation mesurée. Le XT60H actuel35A sous conditions et l’ancienne référence30A RC ne valident pas44A continus. Une proposition ≤30A reste à qualifier avec le lot, les températures et les protections ; ce n’est pas une limitation active. Le MIDI60A ne fixe ni30 ni44A et sa coordination avec ce12AWG, le XT60 et les fils du pack doit être revue. Ne pas fabriquer/mettre en service cette version pour44A continus.',
'Si le courant requis impose un autre connecteur, rechercher un pack2S équipé d’usine et recalculer câble, protection, charge, maintien et implantation. Un adaptateur plus gros conserve le point faible XT60. Le XT90H du catalogue actuel annonce45A MAX sous élévation élevée, pas90A continu ; il n’est pas un remplacement automatiquement validé à44A.',
'Longueurs et chemin CAO provisoires jusqu’au châssis. Les objectifs40km/h et45min ne sont pas démontrés par ce cordon. Schéma/routage de la surveillance, support caméra et visserie finale restent réservés à la phase finale.'
]
RESEARCH="""# Recherche, devis, citations et retours utilisateurs

Consultation du **15 octobre 2026**, sans achat. Le dossier représente une interface compatible mécaniquement avec le pack choisi, **pas un cordon homologué pour44A continus**.

## Achat et devis partiel

| Référence | Offre et quantité d'achat | Prix observé ou indicatif | État |
| --- | --- | --- | --- |
| BNTECHGO12AWG B01ABOPMEI | Amazon.fr, lot10ft rouge+10ft noir | **31,93EUR affichés** | titre exact, En stock ; Amazon US vendeur/expéditeur ; livraison finale et total panier non vérifiés |
| AMASS XT60H-M | une prise du lot prévu, sinon TME exact | prix actuel à confirmer | aucune offre Amazon.fr exacte retenue |
| TE130191 | DigiKey, deux pièces à l'unité | **0,672EUR TTC indicatifs/pièce,1,344EUR pour2** | résultat indexé daté de plusieurs semaines ; accès direct403 ; revalider prix, TVA et stock avant commande |
| ATUM8/2 | deux coupes ≈20mm dans la barre prévue | achat supplémentaire0 si barre suffisante | coût de la barre déjà ouvert, pas un matériau gratuit |

Le prix du fil est celui du **lot entier**, pas de40cm. Il remplace l'ancienne estimation USD pour ce lot lorsque l'offre France convient ; ne pas additionner les deux devis. Le fabricant affiche14,98USD sans total livré France. Avec les deux cosses indicatives, les lignes fil+cosse représentent33,274EUR, sans prise, gaine, frais ou outillage ; ce **n'est pas un total V3 ni un devis livré**. La dépense supplémentaire du présent ensemble concerne surtout les2cosses si les lots déjà prévus suffisent ; leur coût final reste ouvert.

[Amazon fil](https://www.amazon.fr/dp/B01ABOPMEI) · [TME XT60H-M](https://www.tme.eu/fr/details/xt60h-m/connecteurs-dc/amass/) · [DigiKey130191](https://www.digikey.fr/fr/products/detail/te-connectivity-amp-connectors/130191/1864623) · [ATUM fabricant](https://www.te.com/en/product-NB11802001.html).

**Fiche XT60H B074PN6N4K écartée sur Amazon.fr** : titre mélangeant disque dur, Sonos et XT60H, indisponibilité affichée. Son ASIN américain ancien ne suffit pas à établir la bonne variante française. Recherche Amazon.fr par références réalisée, aucun ASIN TE130191 exact vérifié. Ne pas acheter un kit générique sur la seule ressemblance des photos.

La Camera Embarquée identifie un XT60H-M avec jupe H023-6-A et affiche1,10EUR sous une mention Prix HT ; traitement TVA à confirmer. La date de livraison affichée précède la date de consultation, donc aucun délai fiable repris. Cette offre de détail est une alternative, pas le prix ferme du lot déjà prévu. Sa revendication60Acontinus est contredite par les conditions des documents AMASS actuels ; elle n'est pas utilisée pour dimensionner.

## Citations courtes et avis

Deux avis5/5, tous deux du7mars2025, sont visibles pour cette prise chez La Camera Embarquée. L'un dit **« Conforme a mes attentes »**. Ils décrivent une satisfaction, sans données d'échauffement, de résistance ou de courant. Aucun avis exact pertinent sur le couple TE130191+fil680brins trouvé. La quantité d'avis Amazon n'est pas utilisée comme preuve technique.

[Avis et offre XT60H-M](https://www.lacameraembarquee.fr/cables-adaptateurs-connecteurs-fpv/14943-connecteur-amass-xt60h-male-avec-jupe-lemonfpv.html).

## Forums et guide pratique

Le fil RCCrawler de juin2020 contient des retours favorables aux prises AMASS authentiques et propose de maintenir l'alignement avec la moitié complémentaire pendant soudure. Témoignages utiles au montage, aucune validation à44A. Nous utilisons une moitié **non alimentée**, jamais la batterie comme support de soudure.

Le guide publié par HobbyKing rappelle l'étamage séparé, l'insertion complète, le contrôle avant de masquer le joint et l'absence de brins retranchés. Il ne remplace pas une procédure AMASS de soudure (alliage, durée, température et profondeur) qui n'a pas été retrouvée pour le lot. Aucune température universelle de fer n'est inventée. Recherche vidéo/YouTube et forums réalisée par les mots-clés XT60H/sertissage SOLISTRAND ; aucun essai instrumenté exact de l'ensemble V3 retrouvé, aucune vidéo présentée comme visionnée en entier.

[RCCrawler2020](https://www.rccrawler.com/forums/threads/battery-connectors.618927/) · [Guide HobbyKing](https://hobbyking.com/blog/xt60-soldering-guide-for-rc-builds).

## Ambiguïtés documentées

- AMASS : ancien30ARC/60AMC, actuel35AMAX sur12AWG avec élévation<85K. Révisions non interchangeables ;60Ane signifie pas60Acontinu. La page chinoise imprime une unité de résistance ambiguë ; elle n'est pas employée dans les calculs du présent cordon.
- TE130191 : fiche actuelle L19,3/épaisseur0,79/ID3,28, guide L19,10/W9,50/ID3,30 ; distributeurs épaisseur0,99. Mesurer le lot avant ajustements. La largeur9,53 du modèle reste une hypothèse issue de distributeurs, pas une cote du plan A3 consulté.
- Plan TE A3 et liens CAO natifs visibles sur la page fabricant, mais téléchargement direct403 ; **aucun STEP natif récupéré**. Le PDF LCSC est une fiche TE de4pages, pas le plan A3. Deux notices408-1542 de révisions différentes sont conservées, sans mélange de paramètres d'outil.
- BNTECHGO annonce680×Ø0,08, soit3,418mm² arithmétiques, mais3,4arrondis/Ø2,41de faisceau ; packing et étamage non mesurés. Pas d'ampacité garantie calculée à partir de la seule section ou200°Cdu silicone.
- Œillet5,26 compatible nominalement avec M5 et#10-32 ; paume, capot, couple et fil très fin à contrôler. La plage AWG ne démontre pas automatiquement la qualification du sertissage680brins.
- Fusible60A actuellement étudié : ne protège pas automatiquement chaque élément du cordon ni ne limite activement le courant. Son calibre et les courbes doivent être revus avec le courant requis et le câble réellement monté.

[Manifestes des sources](sources.json) · [Archives et SHA256](assets.json) · [Intégration](integration.md).
"""
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s.strip()+'\n',encoding='utf-8')
def jwrite(p,a):write(p,json.dumps(a,ensure_ascii=False,indent=2))
def main():
 sys.stdout.reconfigure(encoding='utf-8');BASE.mkdir(parents=True,exist_ok=True)
 # The retrieved LCSC PDF is a datasheet, not the inaccessible drawing.
 old=BASE/'notices/TE-130191-plan-via-LCSC-original.pdf';new=BASE/'notices/TE-130191-fiche-via-LCSC-original.pdf'
 if old.exists():old.rename(new)
 asset=BASE/'assets.json';data=json.loads(asset.read_text(encoding='utf-8'))
 for a in data['assets']:
  if a.get('local')=='notices/TE-130191-plan-via-LCSC-original.pdf':a['local']=new.relative_to(BASE).as_posix();a['id']='te-datasheet-lcsc';a['document_kind']='TE product datasheet 4 pages, NOT customer drawing'
 jwrite(asset,data);jwrite(BASE/'sources.json',dict(checked_on='2026-10-15',sources=SOURCES))
 jwrite(BASE/'nomenclature.json',dict(checked_on='2026-10-15',status='conditional_study_not_44A_qualified',parts=PARTS,pack_unchanged=True,main_fuse_coordination_validated=False,hardware_purchased=False))
 calc=dict(checked_on='2026-10-15',R_per_m_ohm=.00506,provisional_length_per_pole_m=.20,loop_length_m=.40,R_loop_ohm=.002024,source='BNTECHGO image; temperature unspecified',excludes=['plug','solder','lugs','pack leads','fuse','ED80','bus'],rows=[])
 for current in [10,20,30,35,44.39]:calc['rows'].append(dict(current_A=current,drop_V=current*.002024,loss_W=current**2*.002024))
 calc['does_not_establish_ampacity']=True;calc['does_not_establish_autonomy']=True;calc['not_an_active_current_limit']=True;jwrite(BASE/'calculs.json',calc)
 write(BASE/'integration.md','# Intégration et montage\n\n'+'\n\n'.join(f'{i+1}. {t}' for i,t in enumerate(INTEGRATION))+'''\n\n```mermaid
flowchart LR
 B[Pack2S XT60 femelle] --> X[XT60H-M côté véhicule]
 X --> R[CP0+ rouge12AWG + TE130191]
 R --> F[MIDI entrée M5 - protection à revoir]
 F --> E[CP1A+6mm² puis ED80]
 E --> D[CP1B+6mm² vers D+P2]
 X --> N[CP0- noir12AWG + TE130191]
 N --> M[MiniBus D- N2 #10-32]
```

Le graphe décrit les raccordements de ces pièces ; ce n'est pas le schéma de la carte de surveillance, réservé pour la fin. [Notice PDF](notices/notice-cordon-principal-batterie-v3.pdf).''')
 write(BASE/'recherche-technique.md',RESEARCH)
 write(BASE/'cotes.md','# Cotes et provenance\n\nMillimètres sauf indication. Fils et formes installées provisoires ; pas une liste de coupe.\n\n'+'\n\n'.join('## '+p['ref']+'\n\n| Grandeur | Valeur | Source / statut |\n| --- | --- | --- |\n'+'\n'.join('| '+' | '.join(row)+' |' for row in p['cotes']) for p in PARTS)+'\n\nLe STEP global emploie le faisceau métalliqueØ2,41 comme enveloppe d’implantation. Les deux échantillons détaillés conservent680brins individuels, mais leur arrangement n’est pas mesuré. Canon extérieur, lèvres, sertissage, transitions, couleurs et chemin du cordon sont estimés. Voir le JSON de chaque STEP.')
 write(BASE/'README.md','''# Cordon principal batterie vers distribution

**Étude du15octobre2026 : interface XT60 du pack Zeee2S actuel conservée, sans validation à44A continus.** Aucun achat ni essai matériel. L'écart de courant est ouvert ; aucun changement de batterie ou baisse de performance n'est acté.

Le cordon comprend une prise **AMASS XT60H-M avec capot**, **deux fils BNTECHGO12AWG** rouge/noir, **deux cosses TE SOLISTRAND130191** et **deux manchons ATUM8/2**. Le positif aboutit à l'entrée MIDI, le négatif au MiniBusD-N2. Après MIDI, l'ED80 et les fils6mm² restent en place.

| Composant | Dossier | Achat |
| --- | --- | --- |
| Prise côté véhicule | [XT60H-M](prise-xt60h-m/README.md) | [TME exact](https://www.tme.eu/fr/details/xt60h-m/connecteurs-dc/amass/) |
| Fil rouge/noir | [BNTECHGO12AWG](fils-12awg/README.md) | [Amazon.fr B01ABOPMEI](https://www.amazon.fr/dp/B01ABOPMEI) |
| Deux cosses M5 | [TE130191](cosses-te-130191/README.md) | [DigiKey](https://www.digikey.fr/fr/products/detail/te-connectivity-amp-connectors/130191/1864623) |
| Isolation des cosses | [ATUM8/2](isolation-atum/README.md) | [TE](https://www.te.com/en/product-NB11802001.html) |

[Notice PDF et originaux](notices/README.md) · [Cotes](cotes.md) · [Intégration](integration.md) · [Devis, citations et avis](recherche-technique.md) · [Modèles STEP détaillés](3D/README.md) · [Nomenclature](nomenclature.json) · [Sources](sources.json) · [Calculs](calculs.json) · [Vérification du dossier](verification.json).

Amazon.fr affiche31,93EUR et En stock pour le lot exact de fil, vendeur/expéditeur AmazonUS ; destination et prix final à revalider. Les deux cosses sont estimées à1,344EUR TTC d'après une offre indexée, pas un prix actuel confirmé. Prise et gaine peuvent provenir des lots déjà prévus ; aucun lot n'est compté deux fois. L'ancienne fiche Amazon.fr du XT60H est écartée pour titre incohérent. Le devis demeure partiel.

**Point de dimensionnement ouvert :** les35A du XT60H actuel sont annoncés sous conditions de température, et la fiche historique cite30ARC. Cela ne valide pas le scénario44,39A. Le MIDI60A ne limite pas activement ce courant et sa protection du12AWG/XT60 doit être revue. Cette version n'est pas prête à être construite pour44A continus. Un plus gros adaptateur n'annulerait pas la limite de la prise du pack.

Longueurs et poses provisoires. Châssis, visserie finale, support caméra, schéma et routage de surveillance réservés pour la fin. Les fichiers précédents restent des instantanés datés ; l'intégrationCP0 décrite ici remplace uniquement leurs deux terminaisons ouvertes.''')
 for part in PARTS:
  b=BASE/part['folder'];write(b/'README.md',f"# {part['ref']}\n\n{part['role']}\n\n**Choix conditionnel du15octobre2026, non testé.** {part['reuse']}\n\nBesoin : {part['qty']} {part['unit']}. [Achat proposé]({part['buy']}) ; statut et prix dans le [devis commun](../recherche-technique.md). Aucun total livré confirmé.\n\n[Cotes](cotes.md) · [Montage](integration.md) · [Notice PDF](../notices/notice-cordon-principal-batterie-v3.pdf) · [Originaux](../notices/README.md) · [Sources](sources.json) · [ModèlesSTEP](3D/README.md) · [Ensemble](../README.md).\n\nLa versionXT60 du présent cordon ne valide pas44A continus ; coordination de protection et qualification du lot restent à effectuer.")
  write(b/'cotes.md',f"# Cotes - {part['ref']}\n\n| Grandeur | Valeur | Source / statut |\n| --- | --- | --- |\n"+'\n'.join('| '+' | '.join(row)+' |' for row in part['cotes'])+'\n\nReconstruction CAO, cotes du lot non mesurées. Consulter les variantes dans le [dossier commun](../cotes.md) et le JSON voisin du STEP.')
  write(b/'integration.md',f"# Montage - {part['ref']}\n\n{part['role']}\n\n{part['reuse']}\n\nLa procédure complète et les contrôles associés se trouvent dans [l’intégration de l’ensemble](../integration.md). Les longueursCAO ne sont pas une liste de coupe ; suivre la notice du lot et l’outil documenté.")
  jwrite(b/'nomenclature.json',part);jwrite(b/'sources.json',dict(checked_on='2026-10-15',source_manifest='../sources.json',originals='../notices/README.md',exact_model_native=False))
 write(BASE/'notices/README.md','''# Notice et documents originaux

- [Notice française du cordon V3](notice-cordon-principal-batterie-v3.pdf) : choix, devis partiel, cotes, procédure, calculs, contrôles et limites.
- [Fiche TE130191 viaLCSC](TE-130191-fiche-via-LCSC-original.pdf),4pages : original fabricant, pas le planA3.
- [Notice TE408-1542 viaFarnell](TE-49935-notice-408-1542-via-Farnell-original.pdf), révision à lire dans le document.
- [Notice historique TE408-1542 viaTME](TE-49935-notice-408-1542-via-TME-original.pdf),RevN du10mars2011,6pages.
- [Catalogue AMASS2026](AMASS-catalogue-XT-2026-original.pdf) : copie originale inchangée, page15pourXT60H.
- [Fiche historique AMASSV1.2](AMASS-XT60H-V1.2-original.pdf), versiondistincte.

Les originaux sont conservés sans modification. PlanTEA3 et ZIPSTEPnatifs non récupérés (403), guideSOLISTRAND consulté en ligne mais non téléchargé. Les notices du [fil](../../cable-puissance-12awg/notices/README.md) et de la [gaine](../../gaine-thermoretractable/README.md) restent dans leurs dossiers partagés. [SHA256 et états de récupération](../assets.json).''')
 # Scoped handoffs: preserve all previous dossier text and dated PDFs.
 handoff='''\n\n<!-- cordon-principal-batterie-v3 -->
Mise à jour du15octobre2026 : [cordon principalCP0](LINK) en étudeXT60H-M + fils12AWG + deuxTE130191. Positif vers entréeMIDI, négatif versD-N2 ; remplace les terminaisons95R5 ouvertes/conditionnelles de ces seuls segments. Le6mm² aval, MIDI→ED80→D+, reste distinct. **44A continus non validés surXT60 ; coordination duMIDI60A avec ce cordon à revoir avant construction.** Pas de changement de batterie ni de performance décidé. Lots fil/gaine réutilisés sans double achat ; prix et ASINFR mis à jour dans le dossier commun.
<!-- /cordon-principal-batterie-v3 -->\n'''
 for rel,link in [('README.md','Composants/cordon-principal-batterie/README.md'),('Composants/README.md','cordon-principal-batterie/README.md'),('SPECIFICATIONS.md','Composants/cordon-principal-batterie/README.md'),('Composants/ENSEMBLES-AVANT-CHASSIS.md','cordon-principal-batterie/README.md'),('Composants/faisceau-puissance/integration.md','../cordon-principal-batterie/integration.md'),('Composants/batterie/integration.md','../cordon-principal-batterie/README.md'),('Composants/protection-surintensite/integration.md','../cordon-principal-batterie/integration.md'),('Composants/distribution-alimentation/integration.md','../cordon-principal-batterie/integration.md'),('Composants/cable-puissance-12awg/README.md','../cordon-principal-batterie/recherche-technique.md'),('Composants/connecteurs-alimentation/README.md','../cordon-principal-batterie/recherche-technique.md')]:
  path=ROOT/rel
  if path.exists():
   text=path.read_text(encoding='utf-8')
   if '<!-- cordon-principal-batterie-v3 -->' not in text:write(path,text+handoff.replace('LINK',link))
 print('Dossier et4composants écrits',flush=True)
if __name__=='__main__':main()
