"""Four ensembles, individual component dossiers, dated provenance and quotes."""
from pathlib import Path
import json,sys,html
from urllib.parse import quote_plus
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants';DATE='2026-10-14'
BN='https://bntechgo.com/bntechgo-18-gauge-silicone-wire-kit-ultra-flexible-20-ft-black-and-red-each-color-10-ft-high-temp-200-c-600v-18-awg-silicone-wire-150-strands-of-tinned-copper-wire-stranded-wire-stranded-wire-for-model-battery/'
PARTS={
 'connecteurs-commande':[
 dict(id='jr-pololu-1925',ref='Pololu 1925 - JR mâle, lot pour trois connecteurs',qty=1,unit='lot',price=9.75,currency='EUR',tax='TTC affiché (FR)',
  buy='https://opencircuit.fr/produit/jr-connector-pack-male',maker='https://www.pololu.com/product/1925',query='connecteur servo JR Pololu 1925',
  stock='274 en entrepôt externe, délai affiché 5 à 7 jours ouvrables (HTML direct du 14/10).',
  scope='3 boîtiers intérieurs + 3 capots + 12 contacts mâles dorés ; 8 contacts utilisés, 4 réservés. Fils 22-26 AWG, pas 2,54 mm.',
  role='Mates des deux prises ESC et de celle du servo. Le connecteur ESC droit n’a aucun contact central BEC.',
  cotes=[['Boîtier intérieur','7,90 / 7,70 x 2,75 / 2,65 x 14','Plan Pololu, selon extrémité'],['Capot','10,30 x 4 x 18','Plan Pololu'],['Ouverture capot','8,05 x 2,80','Plan Pololu'],['Pas / entraxe extrêmes','2,54 ±0,10 / 5,08 ±0,20','Plan Pololu'],['Contacts, poches et crimp','Détails visibles reconstruits','Estimations, aucune tolérance fabricant attribuée']]),
 ],
 'liaisons-alimentation-surveillance':[
 dict(id='wago-221-413',ref='WAGO 221-413 - trois entrées, un potentiel',qty=2,unit='pièce',price=None,currency='EUR',tax='Non relevé',
  buy='https://www.wago.com/fr/bornes-d-installation/borne-de-raccordement-avec-levier/p/221-413',maker='https://www.wago.com/221-413',query='WAGO 221-413',stock='Offre Amazon exacte et prix livré non confirmés.',
  scope='Deux bornes : une pour 5 V (1 entrée 18 AWG + 2 sorties GPIO 22 AWG) ; une pour 6 V BEC (2 fils, une place libre).',
  role='Répartir 5 V et connecter le BEC unique au servo. Aucune connexion entre ces deux potentiels.',
  cotes=[['Enveloppe retenue','18,8 x 18,6 x 8,4','Plan WAGO FR version24.07.2025'],['Dénudage','11','Notice WAGO'],['Cuivre fin','0,14-4 mm² / AWG24-12','Fiche WAGO'],['Courant de référence','32 A IEC ; 20 A UL groupe C','Conditions différentes, non interchangeables'],['Ancienne fiche Inde2021','18,8 x18,8 x8,6','Discordance conservée, pas mélangée à la CAO']]),
 dict(id='wago-221-415',ref='WAGO 221-415 - cinq entrées, un potentiel',qty=1,unit='pièce',price=1.2,currency='EUR',tax='TTC affiché DigiKey, hors port',
  buy='https://www.digikey.fr/fr/products/detail/wago-corporation/221-415/13549457',maker='https://www.wago.com/221-415',query='WAGO 221-415',stock='152 857 pièces affichées par la page web consultée ; HTML direct403, stock à revalider.',
  scope='1 entrée GND 18 AWG du régulateur + 4 sorties GND 22 AWG vers les broches physiques6,9,14,20.',
  role='Retour d’alimentation Pi uniquement ; masses ESC signal et servo documentées séparément.',
  cotes=[['Enveloppe','30 x 18,6 x 8,4','Plan WAGO29.09.2024'],['Dénudage','11','Notice WAGO'],['Nombre de potentiels','1','Les cinq ports sont reliés entre eux'],['Masse','4 g','Fiche WAGO ; lot à mesurer']]),
 dict(id='jst-xh-3',ref='JST B3B-XH-A(LF)(SN), XHP-3 et SXH-001T-P0.6',qty=1,unit='embase à réserver',price=None,currency='EUR',tax='Non relevé',
  buy='https://www.jst.fr/fr/produit/xh_224',maker='https://www.jst-mfg.com/product/index.php?series=277',query='JST B3B-XH-A XHP-3 SXH-001T-P0.6',stock='Embase choisie pour l’étude ; prix et conditionnement français non confirmés.',
  scope='1 embase B3B-XH-A pour future surveillance. Le boîtier XHP-3 et ses3contacts sont des références de famille / CAO ; pas d’achat en plus si déjà inclus dans la rallonge.',
  role='Interface mécanique de mesure2S ; attribution B0/B1/B2 et protections de la carte reportées avec schéma/routage.',
  cotes=[['Pas','2,50','JST officiel, pas2,54'],['XHP-3','9,8 x5,7 x7,5','JST p.4 ; lèvre0,25 visible'],['B3B-XH-A','9,9 x5,75 x7 ; queues3,4','JST p.5, sans bossage'],['Pins / portée','Carré0,64 ; entraxe5,0','JST p.5'],['Contact SXH-001T-P0.6','6,1 x2,4 x1,95, développé simplifié','JST p.3 formeB ; détails de ressort estimés'],['Courant / fils','3 A à22AWG ;22-28AWG pour ce contact','JST, pas applicable à un clone sans preuve']]),
 dict(id='rallonge-equilibrage-2s',ref='INTERMODEL 3-RAL2S - rallonge JST-XH 2S',qty=1,unit='cordon',price=1.4,currency='EUR',tax='TTC affiché, hors port',
  buy='https://www.intermodel.fr/cordons-et-prises-de-charge/548-rallonge-pour-prise-equilibrage-2s-intermodel-rallonge-2s-rallonge-prise-equilibrage-2s.html',maker='https://www.intermodel.fr/cordons-et-prises-de-charge/548-rallonge-pour-prise-equilibrage-2s-intermodel-rallonge-2s-rallonge-prise-equilibrage-2s.html',query='rallonge equilibrage JST XH 2S 3 broches 20cm',stock='Disponible, dernières pièces affichées. Amazon exact non confirmé.',
  scope='1 cordon de20cm,3positions, typeXH annoncé. Calibre, diamètre gaine et origine JST des contacts non publiés.',
  role='Relier la prise batterie à l’embase de mesure, après contrôle du type et de l’ordre des cellules. Prise mâle en bout de cordon reconstruite, ce n’est pas une référence JST mâle à sertir.',
  cotes=[['Longueur','200','Annonce INTERMODEL ; convention de mesure non précisée'],['Positions','3','Annonce pour2S'],['Gaine / âme CAO','Ø1,5 / section0,326 mm²','Hypothèse visuelle22AWG, non donnée fabricant du cordon'],['Connecteurs CAO','FamilleXH + protection arrière estimée','Pas de CAO native propre au cordon disponible']]),
 dict(id='fil-18awg',ref='BNTECHGO big-SW18G15008F10C2 - 18 AWG rouge/noir',qty=1,unit='lot 3,048m par couleur',price=9.48,currency='USD',tax='Prix fabricant sans taxes/import/port France confirmés',
  buy=BN,maker=BN,query='BNTECHGO 18 AWG rouge noir 10ft 150 brins',stock='Achat proposé sur site fabricant ; offre Amazon.fr exacte non confirmée.',
  scope='Deux fils séparés18AWG ;150brins Ø0,08 ; cuivre étamé, silicone. Représentation courte pour lecture, pas une bobine vendue de30mm.',
  role='VOUT et GND régulateur vers bornes5V/GND ; provision0,20m par couleur avant implantation. Connexion grands pads à qualifier.',
  cotes=[['Brins','150 x Ø0,08','Fabricant'],['Section de brins calculée','0,754 mm²','150π0,08²/4 ; inférieur au nominalAWG18≈0,823'],['Diamètre isolant','2,3','Image technique fabricant ; à confirmer à réception'],['Longueur livrée','3 048 par couleur','10ft chacune'],['Courant','5 A étudePi','Aucune capacité continue de ce lot validée dans le robot']]),
 ],
 'maintien-batterie':[
 dict(id='sangles-geprc',ref='GEPRC New Version Battery Strap - jaune20 x250, lot5',qty=1,unit='lot5',price=5.99,currency='USD',tax='Taxes/port France non confirmés',buy='https://geprc.com/product/geprc-new-version-battery-strap5pcs/',maker='https://geprc.com/product/geprc-new-version-battery-strap5pcs/',query='GEPRC battery strap 20 250 jaune',stock='Variantes20x220 et20x250 ; choisir250. Offre Amazon exacte non confirmée.',scope='2 sangles montées,3 en réserve ; boucle métallique et surfaces noires/jaunes observées sur photo.',role='Maintien autour de la section47x25 du pack, avec patin et passages à déterminer au châssis.',
 cotes=[['Largeur x longueur','20 x250','Fabricant'],['Épaisseur sangle / fil boucle','1,2 / Ø1,6','Estimations photo'],['Boucle extérieure CAO','25 x10,6','Estimation, pas mesurée'],['Résistance à traction / vibrations','Non chiffrée','Aucune charge admissible retenue'],['Pose fermée','Section interne47x27','Hypothèse pack25 + patin2, sans épaisseur châssis définitive']]),
 dict(id='patin-silicone',ref='BENECREAT B08KFTBDF2 - deux feuilles blanches200 x200 x2',qty=1,unit='lot2',price=11.99,currency='EUR',tax='TTC Amazon.fr, frais à revalider',buy='https://www.amazon.fr/dp/B08KFTBDF2',maker='https://www.amazon.fr/dp/B08KFTBDF2',query='BENECREAT B08KFTBDF2',stock='En stock ; BENECREAT FR BOUTIQUE, expédié Amazon selon page publique HTML directe du14/10.',scope='Deux feuilles entières ; un patin d’étude142x51x2 découpé dans une feuille. Seconde feuille en réserve.',role='Augmenter l’adhérence sous le pack. Ni résistance au feu LiPo, ni adhésif, ni dissipateur thermique qualifié.',
 cotes=[['Feuille','200 x200 x2','Annonce Amazon'],['Patin CAO','142 x51 x2','Choix provisoire : pack138x47±2, marge2 par côté'],['Dureté / densité / coefficient friction','Non publiés','Aucun calcul de maintien à partir de valeurs fictives'],['Plage thermique annoncée','-40 à220°C','Déclaration vendeur, pas qualification du pack'],['Châssis / colle / perçages','Reportés','Aucun support caméra ajouté']]),
 ],
 'coupure-manuelle':[
 dict(id='albright-ed80',ref='Albright ED80-1 - coupure d’urgence unipolaire80 A',qty=1,unit='dispositif',price=83.88,currency='EUR',tax='TTC affiché Parts&Go, hors port',buy='https://www.partsandgo.fr/fr/arrets-d-urgence/52668-arret-d-urgence.html',maker='https://www.albrightinternational.com/products/ed80-2/',query='Albright ED80-1 coupe batterie',stock='Disponible/InStock sur page publique ; réf.vendeur52668, marqueAlbright annoncée. Authenticité du lot à contrôler.',
 scope='Contact mécanique à action brusque,80A thermique ; rupture de défaut500A/48V selon conditionsAlbright, pas capacité de court-circuit du véhicule entier.',
 role='Insérer sur positif commun après MIDI et avant D+ ; ouvre moteurs ET alimentationPi. Usage d’urgence ou isolation hors charge, pas commutation courante en charge.',
 cotes=[['Corps / hauteur','59 x contourØ58 ;37','PlanAlbright2024, corps à pans reconstruit'],['Bouton','Ø48, hauteur14','PlanAlbright'],['Au-dessus face de montage','56 fermé /51 ouvert','PlanAlbright'],['Sous face de montage','55 avec bornes','PlanAlbright'],['Fixation','CentreØ25 +2trousØ5,5 entraxe48','Plan de référence ; perçages châssis reportés'],['Bornes','M6 ; serrage3,6-3,9N·m','PlanAlbright ; cosses et appui à contrôler'],['Masse indicative','223g','FicheAlbright, pas820g de l’autre produit52666']]),
 dict(id='cosses-klauke-95r6',ref='Klauke95R6 - cosse cuivre étamé6mm², M6',qty=2,unit='pièce',price=None,currency='EUR',tax='Non relevé',buy='https://www.buerklin.com/en/p/klauke/cable-lugs/95r6/07F2055/',maker='https://www.klauke.com/gb/en/tubular-cable-lugs-cu-standard-type-4959',query='Klauke 95R6 6mm2 M6',stock='Référence exacte identifiée ; offre française et prix à l’unité non vérifiés, ne pas budgéter un lot100 à prix2pièces.',scope='Deux nouvelles cosses pour les bornes ED80 ; ne remplacent pas les95R5 aux extrémitésMIDI et MiniBus.',role='Terminer les deux segments6mm² MIDI→ED80 puisED80→D+ ; outil/matrice Klauke compatibles, contrôle du sertissage.',
 cotes=[['d1 / a / b','4 /9 /10','CatalogueKlauke p.14PDF /12 imprimée'],['d2 / d4','6,5 /6','TrouM6 / canon'],['c1 / c2 / l','7 /6,5 /19','Longueur l depuis centre trou'],['Longueur CAO','26 =7+19','Déduite du dessin, pas l seule'],['Paume / fenêtre inspection','2 /Ø1,4','Estimations non cotées']]),
 ]}
TITLES={'connecteurs-commande':'Connecteurs et faisceau de commande','liaisons-alimentation-surveillance':'Liaisons alimentation et mesure2S','maintien-batterie':'Maintien de la batterie','coupure-manuelle':'Coupure manuelle indépendante'}
INTEGRATION={
 'connecteurs-commande':[
 'Numéros physiques Pi :32/GPIO12→PWM ESC gauche ;33/GPIO13→PWM ESC droit ;12/GPIO18→servo. GND gauche34, GND droit39. Les trois signaux restent séparés.',
 'Prise ESC gauche : masse versPi et servo ; contact central BEC6V vers servo uniquement ; signalGPIO12. Prise droite : masseGPIO39 et signalGPIO13 ; cavité centrale vide, BEC droit isolé côté ESC.',
 'Prise servo : masse commune issue ESC gauche, BEC gauche6V, signalGPIO18. Les raccords BEC et masse sont faits par deux bornes413 distinctes : celleBEC est comptée dans le dossierliaisons ; cellemasse servo est une3e413, comptée ici en supplément (prix inconnu).',
 'Régler un seulBEC à6V. Ne pas relier les deuxBEC, ne pas envoyer6V versPi5V/3V3, ne pas utiliser unY entièrement câblé qui relierait deuxPWM.',
 'Sertir22AWG avec outil approprié, tirer doucement chaque fil, encliqueter contacts et capot selonPololu. Identifier GND/BEC/PWM par mesure/notice et détrompage avant raccordement ; ne pas présumer les couleurs.',
 'Le faisceauGPIO existant fournit les contactsMolex et fils22AWG : aucun deuxième kit de fils compté. Longueurs définitives après implantation ; queues CAO courtes illustratives.',
 'SeuilsESC3,3V et tenue de l’alimentationservo aux pointes restent à mesurer. Au démarrage et après réarmement, commande neutre puis armement explicite. Aucun test physique effectué.'
 ],
 'liaisons-alimentation-surveillance':[
 'VOUT grand pad duD24V90F5→18AWGrouge→413-5V→deux22AWG vers broches2et4 ; grandGND→18AWGnoir→415-GND→quatre22AWG vers6,9,14,20. Les masses signalESC sont déjà distinctes dans le faisceaucommande.',
 'Les trois bornes413 du projet sont trois potentiels distincts :5V,6VBEC et masse duservo. Le devisliaisons compte2, le deviscommande compte1 : aucun double comptage.',
 'Les ports d’uneWAGO sont tous reliés. Un conducteur par port, cuivre propre dénudé11mm ; lever, insérer à fond, fermer, contrôle visuel et traction. Ne pas étamer la zone serrée ni mélanger positifs etGND dans une borne.',
 'Modèle de chute de tension :ρCu20°C=0,0175Ωmm²/m ;18AWG pris conservativement0,754mm² calculé sur150brins ; boucle2x0,20m à5A→0,0464V et0,232W. Ajouter contacts, soudures, filsGPIO, échauffement et déséquilibre entre broches ; aucun5A/header garanti.',
 'Le régulateur fixe5V±4% peut tomber à4,8V avant chute de faisceau ; le simple choix18AWG ne garantit pas la tension à laPi. Mesurer en charge et aux accélérations, sans alimentationUSB-C simultanée.',
 'La rallonge2S relie la prise du pack à la future embaseB3B-XH-A de surveillance. B0=moins total, B1=point milieu, B2=plus total, à vérifier au voltmètre selon le détrompage réel. AucunB1 surmassePi. Aucun courant moteur/servo/Pi par cette prise.',
 'La prise batterie doit être confirméeXH2,50mm avant achat. Ne pas forcer un clone2,54, ne pas déplacer les contacts du pack pour obtenir un branchement supposé. La protection contre courts-circuits des fils de mesure appartient au schéma final différé ; aucune connexion sous tension à la carte avant validation.',
 'Interface principale batterie→MIDI/D− : reste conditionnelle auXT60 réel du pack. Le courant commun44,39A est unehypothèse et dépasse l’hypothèseprudenteXT60H30A continu déjàretenue. Les6mm² et l’ED80 ne qualifient pas leXT60 ; aucun adaptateur magique ni modification du pack retenu.',
 'Une fois l’interface batterie qualifiée, conserverCP0+ versMIDIentrée etCP0− versD− ; les deuxESC ont leurs branches12AWG documentées. Réutiliser les gaines/cosses déjàcomptées. Pas de second câbleUSB :1m fourni avec lacaméra.'
 ],
 'maintien-batterie':[
 'Deux sangles indépendantes autour de la section47x25 du pack, réparties sur sa longueur138, et unpatin provisoire142x51x2. La poseCAD suppose une hauteur totale27 sansplaquechâssis ; les positionsX±40 restent des hypothèses.',
 'Périmètre minimum théorique2x(47+25+2)=148mm ; sur250mm il reste102mm avantboucle, épaisseurchâssis et recouvrement. Avec pack auxdimensionshautes49x27 :156mm et94mm restants. Il faudra vérifier le recouvrement utilisable, non publié, sur lamonture finale.',
 'Le patin seul ne garantit pas la rétention lors d’un freinage ou choc. À40km/h un pack250g porte15,43J d’énergie cinétique ; aucun essai de choc ni charge admissible des sangles publié ne garantit son maintien.',
 'Découper le patin horspack, coins doux, éliminer débris ; ne pas percer le boîtier batterie. Nettoyer surfaces, mettre les sangles sur zones résistantes duhardcase sans écraser, vérifier que le pack neglisse pas.',
 'Passages de sangles, butées, accèsXT60/équilibrage et visserie seront conçus avec lechâssis. Séparer câbles des surfaces de pincement ; le boîtier du pack n’est pas un point de vissage.',
 'Aucun adhésif sélectionné ni température admissible batterie déduite des220°C annoncés pour lasilicone. Dureté etfriction inconnues : essais de roulage lent et freinage avant vitesseélevée.'
 ],
 'coupure-manuelle':[
 'Chaîne positive retenue à compter du14/10 :pack→MIDI60A→ED80→MiniBusD+→branches moteurs etPi existantes. Le moins communD− resteinchangé. Ceci remplace le segmentCP1+ directMIDI→D+ représenté dans le dossierfaisceauantérieur.',
 'CP1A+=MIDI sortie→ED80 entrée,6mm²,95R5/M5 vers95R6/M6 ;CP1B+=ED80 sortie→D+P2,6mm²,95R6/M6 vers95R5/#10-32. Réutiliser les2cosses95R5 initiales, ajouter2cosses95R6. Deux longueursprovisoires0,20m chacune dans l’enveloppe de provisionfil existante, pas unelistede coupe.',
 'Coupure indépendante duPi, duWi-Fi, duPololu etduSSR. Enurgence, pression surbouton ouvre les2branches. LePi perd sonalimentation sans arrêtLinux ; coupurelogicielle/Pololupour arrêtnormal, puisED80 àvide pourisoler.',
 'L’ED80 est unipolaire : fils de mesureéquilibrage et surveillance peuvent rester sous tension, ainsi que le côtébatterie duMIDI. Pour intervenir,débrancher aussi la priseprincipaleETl’équilibrage. Ce n’est pas uneisolationgalvanique complète duvéhicule.',
 'Aucune garantie de freinageinstantané : lesroues peuvent continuer enrouelibre, inertie et capaciteursESC persistent. Ne pas remplacer ce dispositif par un petitboutonGPIO. Les48V/500A publiés sont desconditionsd’essai de défautdufabricant, pas certification de l’installation.',
 'BornesM6 :3,6-3,9N·m selonplan. Sertir les95R6 selonoutil/matrice fabricant pour6mm²classe5, isolerles paumescontre contactsaccidentels, ajouterdécharge de traction. Montagemécanique etvisM5fournies restent àadapter à l’épaisseurchâssis enphasefinale.',
 'Comparaisonécartée :BlueSea6006/9003E ont unfortcourant deconduction mais25A de commutation publiés ; cette donnée nejustifie pas une coupure44,39A de l’étude. Aucune extrapolation à2S sanscourbeacceptée.',
 'À44,39A,40mV/80A correspond approximativementà0,5mΩ,22,2mV et0,985W pour contactsneufs ; hypothèselinéaire, pas mesure ni garantie. ED8080A dépend desconducteurs et de l’environnement, tenircomptedes223g et del’encombrement.',
 'Réarmement manuel après diagnostic seulement ; rouesimmobiles et commandesneutres. Essaid’ouverture d’abord surchargecontrôlée, puisessaisdéfauts àfaible vitesse ; emplacementaccessible décidéauchâssis.'
 ]}
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s+'\n',encoding='utf-8')
def dump(p,v):write(p,json.dumps(v,ensure_ascii=False,indent=2))
def tab(rows):return '\n'.join(['| Grandeur | Valeur | Statut |','| --- | --- | --- |',*['| '+' | '.join(r)+' |' for r in rows]])
def main():
 sys.stdout.reconfigure(encoding='utf-8')
 from final_components_text import TEXT
 INTEGRATION.update(TEXT)
 for a in PARTS['liaisons-alimentation-surveillance']:
  if a['id']=='fil-18awg':
   a['cotes'] += [['Faisceau / résistance','Ø1,13 /22,98 Ω/km','Image technique BNTECHGO, conditions de résistance non publiées'],['Section / isolation annoncées','0,75 mm² /0,58 mm','Image technique BNTECHGO ; pas une mesure du lot']]
  if a['id'] in ['wago-221-413','wago-221-415']:
   a['buy']='https://www.gotronic.fr/cat-bornes-de-connexion-wago-0-5-a-2-5-mm2.htm'
   a['price']=.75 if a['id'].endswith('413') else 1.20
   a['tax']='TTC affiché GoTronic, hors livraison'
   a['stock']='En stock affiché sur catalogue GoTronic du14/10 ; offre Amazon exacte non confirmée.'
 for folder,parts in PARTS.items():
  b=BASE/folder;b.mkdir(parents=True,exist_ok=True)
  rows=[]
  for a in parts:
   c=b/a['id'];a['amazon_search']='https://www.amazon.fr/s?k='+quote_plus(a['query']);a['amazon_FR_verified']=a['id']=='patin-silicone'
   price='Non confirmé' if a['price'] is None else f"{a['price']:.2f} {a['currency']} par {a['unit']} - {a['tax']}"
   if a['price'] is not None and a['qty']>1:price+=f" ; {a['price']*a['qty']:.2f} {a['currency']} pour {a['qty']}"
   rows.append(f"| [{a['ref']}]({a['id']}/README.md) | {a['qty']} {a['unit']} | {price} |")
   dump(c/'selection.json',dict(checked_on=DATE,purchase_made=False,hardware_tested=False,**a))
   write(c/'README.md',f"# {a['ref']}\n\nChoix d’étude du14octobre2026, non acheté et non testé.\n\n{a['role']}\n\n{a['scope']}\n\n[Achat proposé]({a['buy']}), [source technique]({a['maker']}), [recherche Amazon]({a['amazon_search']}).\n\nPrix : **{price}**. {a['stock']}\n\n[Cotes](cotes.md), [notice de préparation](notice.md), [avis et limites](avis-utilisateurs.md), [sources de l’ensemble](../sources.json), [notice PDF commune](../notices/notice-{folder}-v3.pdf), [modèles STEP](3D/README.md), [intégration](../integration.md).")
   write(c/'cotes.md',f"# Cotes - {a['ref']}\n\nToutes les cotes enmm saufmention.\n\n"+tab(a['cotes'])+'\n\nLes détails non cotés sont reconstruits et signalés dans les JSON de chaque STEP. Aucune mesure de pièces, aucune CAO fabricant revendiquée.\n\n[Source]('+a['maker']+').')
   write(c/'notice.md',f"# Notice de projet - {a['ref']}\n\n{a['scope']}\n\n{a['role']}\n\nSe référer aux procédures de l’[ensemble](../integration.md) et à sa [notice PDF](../notices/notice-{folder}-v3.pdf). Les PDF originaux constructeur sont dans le dossiernotices de l’ensemble, avec leurs versions et empreintes dans [sources.json](../sources.json).\n\nLa présente note n’est pas une notice officielle. Vérifier référence, polarité, dimensions et compatibilité du lot reçu ; essais détaillés dans l’intégration. Le montagechâssis, la visserie restante et la surveillance définitive sont reportés.")
   avis='Aucun retour d’utilisateur exact avec mesures ni vidéo YouTube validant cette référence dans notre robot trouvé. Les données nominales proviennent du constructeur ou de l’offre indiquée, pas d’une note client.'
   if a['id']=='fil-18awg':avis+=' Le fabricant conserve9avis du lot20ft ; certains apprécient la souplesse etle travail des fils. Aucun decesavis nequalifie5A en environnementdurobot. [Avis du fabricant]('+BN+'#product-reviews).'
   if a['id'].startswith('wago'):avis+=' Les discussions publiques sur lesWAGO soulignent le choix de la vraie référence et l’attention aux copies ; aucune note ne certifie un lotMarketplace. [Discussion de réception](https://www.reddit.com/r/brico/comments/1n7gnyi).'
   write(c/'avis-utilisateurs.md','# Avis et informations manquantes\n\n'+avis+'\n\nManquent encore les essais thermiques/vibratoires dans l’ensemble, les longueurs finales et les interfaces réelles. Le dossier ne transforme pas un usage rapporté sur un autre appareil en validationV3.')
   write(c/'3D/README.md','# Modèles STEP\n\nLe catalogue est généré par `tools/build_final_components_step.py` ; chaqueSTEP a unaperçuPNG et unJSON decotes/provenance. [Catalogue de l’ensemble](../../3D/README.md).')
  extra= '\n| WAGO 221-413 pour masse servo (troisième borne distincte) | 1 pièce | 0,75 EUR TTC GoTronic, comptée ici uniquement |' if folder=='connecteurs-commande' else ''
  dump(b/'nomenclature.json',dict(date=DATE,parts=parts,additional_parts=([dict(ref='WAGO221-413 GNDservo',quantity=1,price=.75,currency='EUR',tax='TTC GoTronic hors port',counted_elsewhere=False)] if folder=='connecteurs-commande' else []),excluded=['Châssis','Visserie restante','Support caméra','Schéma et routage carte surveillance']))
  write(b/'README.md',f"# {TITLES[folder]}\n\nÉtude du14octobre2026. Composants séparés, non achetés, non testés.\n\n| Composant | Quantité ajoutée | Devis marchandises |\n| --- | --- | --- |\n"+'\n'.join(rows)+extra+f"\n\n[Notice PDF](notices/notice-{folder}-v3.pdf), [intégration et préparation](integration.md), [cotes par pièce](nomenclature.json), [devis](devis.md), [sources originales et SHA256](sources.json), [STEP détaillés et assemblages](3D/README.md).\n\nLe châssis, la visserie restante, le supportcaméra, le schéma et leroutage de lacartesurveillance seront faits ensemble à lafin. Les poses et longueurs d’implantation sont provisoires ; pas de nouvelle carte électronique conçue ici.")
  write(b/'integration.md',f"# Intégration - {TITLES[folder]}\n\n14octobre2026. Aucune mise en service effectuée.\n\n"+'\n\n'.join(f'{i+1}. {s}' for i,s in enumerate(INTEGRATION[folder]))+f"\n\n[Composants et achat](README.md), [modèles](3D/README.md), [notice PDF](notices/notice-{folder}-v3.pdf).")
  write(b/'devis.md','# Devis indicatif - 14 octobre 2026\n\nQuantités de lots entiers ; aucun achat effectué. Prix affichés hors livraison sauf mention, aucune conversion USD→EUR inventée.\n\n| Référence | Besoin / lot | Marchandises |\n| --- | --- | --- |\n'+'\n'.join(rows)+extra+'\n\nLes prix non confirmés restent ouverts. Aucun total global V3 ni total livré de ces ensembles n’est validé. Les fils 22 AWG, 6 mm², gaines et deux cosses 95R5 déjà budgétés sont réutilisés dans l’étude ; pas de deuxième achat présumé.\n\nOpencircuit : prix 9,75 EUR du HTML direct actuel, pas 4,55 EUR de l’index web ancien. GoTronic : 0,75 EUR par 413 et 1,20 EUR par 415. Frais France à revalider. GEPRC et BNTECHGO : devis en USD, taxes/import/port non confirmés. Parts&Go : 83,88 EUR TTC du dispositif seul ; vérifier la révision ED80-1 conforme à la fiche 2024. Amazon : 11,99 EUR TTC pour deux feuilles entières ; stock, frais et vendeur à revalider à la commande.')
  write(b/'notices/README.md',f'# Notices et documents originaux\n\n[Notice V3](notice-{folder}-v3.pdf) : documentprojet en français, distinct des noticesfabricant. [Répertoire des originaux](../sources.json) : URLs, dates, versions etSHA256 ; échecs d’accès explicités. Pas de fausse noticefabricant pour lesproduits sansPDFpublié.')
  write(b/'photos/README.md','# Photographies de référence\n\nImages publiques originales, nonmodifiées ; attribution etempreintes dans [sources.json](../sources.json). LesPNG du dossier3D sont desrendus de reconstruction, pas desphotos du matériel.')
 # Machine-readable calculations and interface handoff; no PCB or chassis data.
 dump(BASE/'liaisons-alimentation-surveillance/calculs.json',dict(cu_rho_20C_ohm_mm2_per_m=.0175,strand_count=150,strand_diameter_mm=.08,computed_section_mm2=.7539822368615503,one_way_length_study_m=.2,current_study_A=5,loop_drop_V=.04642019173513615,loop_loss_W=.23210095867568075,contact_losses_included=False,header_current_share_guaranteed=False,main_current_study_A=44.39,main_XT60_qualified=False))
 dump(BASE/'maintien-batterie/calculs.json',dict(geprc_length_mm=250,pack_nominal_mm=[138,47,25],pad_study_mm=[142,51,2],minimum_perimeter_mm=148,remaining_before_buckle_chassis_overlap_mm=102,worst_pack_section_perimeter_mm=156,remaining_worst_mm=94,pack_mass_kg=.25,speed_kmh=40,kinetic_energy_J=15.432098765432098,retention_tested=False))
 dump(BASE/'coupure-manuelle/calculs.json',dict(current_study_A=44.39,ED80_thermal_A=80,ED80_typical_new_contact_drop_V=.04,ED80_drop_reference_A=80,estimated_contact_R_ohm=.0005,estimated_drop_V=.022195,estimated_loss_W=.98523605,contact_model='Linear approximation, new contacts only; no measurement',complete_galvanic_isolation=False))
 print('DATA',len(PARTS),'ensembles',sum(map(len,PARTS.values())),'component dossiers')
if __name__=='__main__':main()
