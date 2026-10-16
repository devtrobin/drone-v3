"""User-selected 2S factory IC5 route; preserve the initial XT60 study as a variant."""
from pathlib import Path
import sys,json,math,hashlib,re,urllib.request
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/cordon-principal-batterie'
BATT='https://www.rcteam.com/products/spektrum-accu-lipo-smart-74v-5000mah-30c-ic5'
OEM='https://www.spektrumrc.com/product/connector-ic5-device-w-4-10awg-wires/SPMXCA510.html'
BUY='https://www.freakware.de/en/p/ic5-geraeteanschluss-kabel-4-100mm-10awg-spektrum-spmxca510-a167682.htm'
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s.strip()+'\n',encoding='utf-8')
def jw(p,a):write(p,json.dumps(a,ensure_ascii=False,indent=2))
INTRO='Choix utilisateur du 15 octobre 2026 : revoir la batterie 2S pour une prise plus forte montée d’usine. Proposition retenue pour l’étude : Spektrum Smart G1 SPMX50002S30H5, 7,4 V /5 000 mAh /IC5, et cordon véhicule SPMXCA510 pré-câblé en 10 AWG. Aucun achat ni essai matériel.'
MOUNT=[
'Utiliser un seul pack Spektrum G1 SPMX50002S30H5, équipé IC5 d’usine. Ne pas modifier ses fils et ne pas réutiliser la Zeee avec un adaptateur pour cette version. Le cordon côté véhicule est le SPMXCA510 « Device », pas le SPMXCA505 « Battery », ni un cordon série ou parallèle.',
'CP0+ : fil rouge10AWG du510 → TE130191 → entréeMIDI M5. CP0- : fil noir10AWG du510 → TE130191 → D-N2 #10-32. Le positif aprèsMIDI traverse ED80 puisD+ par les deuxsegments6mm² existants. L’UD80A conserve son arrivée6mm².',
'Les deux fils10AWG sont inclus dans le510. Aucun lot BNTECHGO12AWG supplémentaire pour le cordon actif ; ce lot reste affecté aux branchesESC. La longueur fabricant est4in, environ101,6mm/100mm selon la fiche. L’origine de cette longueur et le dénudage d’usine ne sont pas cotés ; mesurer le lot. Placer leMIDI près du pack, éviter de rallonger le segment non protégé pour suivre une poseCAO.',
'Le cordon510 a seulement deux fils de puissance visibles sur la photo officielle ; pas de troisième filSmart à brancher auPi. La fonctionSmart n’est pas utilisée dans la commande du véhicule. L’équilibrageG1 fournit toujoursB0/B1/B2 à la surveillance, avec la protection et le schéma encore réservés pour la fin.',
'Avant sertissage, vérifier le type de conducteur et les extrémités d’usine. Si elles sont pré-étamées à la soudure, enlever cette portion puis redénuder du conducteur intact ; conserver l’étamage de surface des brins lorsqu’il est d’origine. Ne pas sertir un paquet rigidifié à la soudure. La longueur utile est donc inférieure au101,6mm initial selon le lot ; leSTEP montre≈92mm d’enveloppe métallique par fil pour l’étude, pas un débit à fabriquer.',
'TE130191 admet12-10AWG, soit2,62-6,64mm². L’outil49935, chambre12-10, figure dans leguideSOLISTRAND ; procédure408-1542RevP : dénudage standard6,35-7,14mm, paume orientée selon la figure, canon centré, cycle complet du cliquet. Confirmer la combinaison fil réel/outil/matrice et contrôler les éprouvettes (insertion, brins, tenue, résistance). Ne pas appliquer automatiquement une pince pour cosses isolées ou ajouter de soudure au sertissage.',
'Deux coupes ATUM8/2 d’environ20mm dans la barre prévue. Les enfiler avant sertissage ; couvrir lecanon et la gaine dufil, laisser la paume de contact libre. Diamètres installés duSTEP estimés, à vérifier avec le10AWG reçu et le retrait jusqu’à15%. Chauffe locale selon TE : début80°C, complète110°C ; ces valeurs ne sont pas le réglage d’un pistolet. La priseIC5 arrive pré-câblée : aucune soudure au connecteur n’est nécessaire pour ce montage.',
'Batterie et équilibrage débranchés, monter lescosses avec écrous/rondelles d’origine. M5MIDI :4,5N·m dans la plage commune des documents existants, lot à confirmer. MiniBus#10-32 : écart1,69/2,03N·m à résoudre par la notice du lot ; jamais écrouM5 ni4,5N·m par défaut. Retenir lesfils hors bornes et assurer la fermeture des capots. Fixations de châssis réservées pour la fin.',
'Contrôlerpolarité sur lesmarquages réels, continuité de chaque pôle et absence de court-circuit, isolement, tenue et capots. Vérifier ensuite avec unesource adaptée limitée, puis qualifier courantRMS et pointes, résistances/chutes descontacts et température de tous lesraccords sur la durée et l’ambiante prévues. Aucun court-circuit volontaire du pack.',
'L’IC5 est employé par Spektrum sur leFirma100A SPMXSE1100 : cette applicationdocumentée motive lechoix à44,39A, mais ne constitue pas uneampacité indépendante du510 dans notreimplantation. Aucune valeur «120Acontinus garantis» n’est attribuée auconnecteur. Tenue du12AWG d’usine du pack, du10AWG ducordon et coordination duMIDI60A encore à qualifier ; unfusible n’est pas une limitation active de courant.',
'ChargeG1 : laFAQHorizon confirme qu’uneG1 avec prise d’équilibrage n’exige pas dechargeurSmart. LeS65 couvre laLiPo2S standard,8,4V max ; régler initialement1C=5A (42W à8,4V), pas5,2A repris de laZeee. Il faut aussi uncordon/adaptateur decharge versIC5 et leJST-XH2S ; ce raccord decharge est distinct ducordon embarqué et doit être sélectionné/contrôlé avantcharge. Ne pas substituer uneG2 sans équilibrage, incompatible avec leS65 classique.',
'Pack proposé139×46×25mm/294g selonanciennepage fabricant. RéférenceG1 arrêtée sur lesite actuel, mais offreRC Team vérifiée disponible à49,99EUR ; date/état du lot et notice à contrôler à l’achat. Capacité5,0Ah/37Wh contre5,2Ah/38,48Wh : -3,85% d’énergie nominale et +44g annoncés. Lesobjectifs40km/h,10-20min et45min restent soumis auxmesures ; aucune réduction de performance demandée n’est décidée par ce seulchoix.',
]
def main():
 sys.stdout.reconfigure(encoding='utf-8')
 stock=json.loads((BASE/'references/SPMX50002S30H5-offer.json').read_text(encoding='utf-8'));assert stock['available'] and stock['variants'][0]['sku']=='SPMX50002S30H5'
 # Exact EU cord offer, public read; no checkout or purchase.
 a=json.loads((BASE/'assets.json').read_text(encoding='utf-8'))
 try:
  data=urllib.request.urlopen(urllib.request.Request(BUY,headers={'User-Agent':'Mozilla/5.0'}),timeout=25).read();assert data
  p=BASE/'references/SPMXCA510-freakware.html';p.write_bytes(data);a['assets'].append(dict(id='ic5-eu-offer',url=BUY,local='references/SPMXCA510-freakware.html',bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),status='downloaded_original',checked_on='2026-10-15'))
 except Exception as e:a['assets'].append(dict(id='ic5-eu-offer',url=BUY,status='not_downloaded',error=str(e),checked_on='2026-10-15'))
 jw(BASE/'assets.json',a)
 data=dict(checked_on='2026-10-15',user_choice='factory_stronger_connector_2S',active_battery=dict(ref='SPMX50002S30H5',generation='G1',voltage_nominal_V=7.4,voltage_full_V=8.4,capacity_Ah=5,energy_Wh=37,dimensions_nominal_mm=[139,46,25],mass_announced_g=294,connector='IC5 factory',balance='3way JST-XH photo; lot to check',manufacturer_discontinued=True,offer_price_EUR=49.99,offer_available=True,buy=BATT),active_cord=dict(ref='SPMXCA510',included_wire_gauge='10 AWG',wires=2,manufacturer_wire_length_in=4,manufacturer_wire_length_mm=101.6,body_dimensions_measured=False,buy=BUY,offer_price_EUR=9.89,price_FR_delivered_confirmed=False),hardware_tested=False,standalone_connector_current_rating_not_found=True,current_44A_basis='Engineering inference from Spektrum Firma100A with single IC5, not a connector rating',fuse_coordination_validated=False,charger='SkyRC S65 retained; separate charge lead IC5 adaptation still required',charge_initial_A=5,legacy_XT60_not_selected=True)
 jw(BASE/'selection-active.json',data)
 src=json.loads((BASE/'sources.json').read_text(encoding='utf-8'))
 src['sources'] += [dict(id='spektrum-g1',url='https://my.spektrumrc.com/Products/Default.aspx?ProdID=SPMX50002S30H5',local='references/battery-g1.html',type='manufacturer',supports='139×46×25/294g/2S5AhIC5 ; anciennepage'),dict(id='spektrum-g1-current',url='https://www.spektrumrc.com/product/7.4v-5000mah-2s-30c-smart-hardcase-lipo-battery-ic5/SPMX50002S30H5.html',local='references/battery-g1-current.html',type='manufacturer',supports='G1 et référence arrêtée'),dict(id='spektrum-oem-cord',url=OEM,local='references/ic5-spektrum.html',type='manufacturer',supports='Device,10AWG,4in ; deuxfils enphoto ; référence arrêtée'),dict(id='spektrum-faq',url='https://www.horizonhobby.com/on/demandware.static/-/Sites-horizon-master/default/dwdb93431e/Manuals/Smart_G2_Battery_and_Charger_FAQ.pdf',local='notices/Spektrum-G1-G2-FAQ-original.pdf',type='manufacturer_pdf',supports='G1avecéquilibrage utilisable avec chargeurclassique ; G2requiertSmart'),dict(id='spektrum-use',url='https://www.spektrumrc.com/ProdInfo/Files/SPMXSE1100-Programming_Guide.pdf',local='notices/Spektrum-Firma100A-IC5-reference-original.pdf',type='manufacturer_pdf',supports='ESC100A avecunIC5 ; application,pas ampacitéindépendante du510'),dict(id='battery-verified-offer',url=BATT+'.js',local='references/SPMX50002S30H5-offer.json',type='distributor_public_product_data',supports='SKUexact,availabletrue,price4999centimes'),dict(id='ic5-eu-offer',url=BUY,local='references/SPMXCA510-freakware.html',type='distributor',supports='9,89EURincltaxlocale,stockannoncé ; France/paniernonvérifiés')]
 jw(BASE/'sources.json',src)
 old=json.loads((BASE/'nomenclature.json').read_text(encoding='utf-8'));old['legacy_parts']=old.pop('parts');old['parts']=[dict(ref='SPMXCA510',qty=1,unit='cordon pré-câblé',includes='IC5 Device +2fils10AWG4in',price_EUR=9.89,price_FR_delivered_confirmed=False,buy=BUY),dict(ref='TE130191',qty=2,unit='cosses',price_each_indicative_EUR=.672,buy='https://www.digikey.fr/fr/products/detail/te-connectivity-amp-connectors/130191/1864623'),dict(ref='ATUM-8/2-0-STK',qty=2,unit='coupes≈20mm',reuse='barreexistante,aucunsecondlot')];old['status']='IC5_user_selected_engineering_study';old['pack_unchanged']=False;old['active_battery_reference']='SPMX50002S30H5';old['legacy_parts_not_to_add_to_active_purchase']=True;jw(BASE/'nomenclature.json',old)
 write(BASE/'variante-xt60-non-retenue.md','# Variante XT60 non retenue\n\nLes huit premiers STEP et les dossiers prise-xt60h-m/fils-12awg constituent l’étude préparée avant la réponse utilisateur. Ils ne sont pas à ajouter au cordonIC5 actif. Les44A continus n’y sont pas justifiés et leMIDI60A doit être recoordonné. Lescosses et la référenceATUM restent communes. Le lotBNTECHGO12AWG est conservé pour lesbranchesESC, pas racheté pourCP0.\n\n'+(BASE/'integration.md').read_text(encoding='utf-8'))
 write(BASE/'integration.md','# Intégration active IC5\n\n'+INTRO+'\n\n'+'\n\n'.join(f'{i+1}. {t}' for i,t in enumerate(MOUNT)))
 write(BASE/'README.md',f'''# Cordon principal batterie vers distribution - IC5

{INTRO}

| Élément actif | Dossier / référence | Quantité | Achat |
| --- | --- | ---: | --- |
| IC5 véhicule et deux fils10AWG inclus | [SpektrumSPMXCA510](cordon-ic5-spektrum/README.md) |1cordon | [FreakwareEU]({BUY}) |
| Cosses de puissanceM5 | [TE130191](cosses-te-130191/README.md) |2 | [DigiKey](https://www.digikey.fr/fr/products/detail/te-connectivity-amp-connectors/130191/1864623) |
| Gaine adhésive | [ATUM8/2](isolation-atum/README.md) |2coupes≈20mm | mêmebarreprévue |
| Batterie2S révisée | [SPMX50002S30H5G1](../batterie/spektrum-g1-ic5/README.md) |1pack | [RCTeam]({BATT}) |

[NoticePDF et originaux](notices/README.md) · [Intégrationactive](integration.md) · [CotesIC5](cordon-ic5-spektrum/cotes.md) · [Devis, sources et avis](revision-batterie-ic5.md) · [CatalogueSTEP](3D/README.md) · [Sélectionstructurée](selection-active.json) · [Nomenclature](nomenclature.json) · [Contrôles](verification.json).

Le510 arrive pré-câblé : pas d’assemblage deprise, pas d’adaptateurXT60 en propulsion, pas de lotfil racheté. Deuxcossesàsertir et deuxmanchons leterminent versMIDIentrée etD-N2. Lesfils6mm² avalMIDI/ED80 etversUD80 restentinchangés.

LechoixIC5 est motivépar son emploi documenté sur unSpektrumFirma100A ; ceconstat est uneinférence d’ingénierie, pas uneampacité certifiée de notrecordon. Courant44,39A, fils du pack, températures etcoordinationduMIDI60A encore àqualifier. Aucunevaleur120Acontinu garante inventée.

Prixpartiels : pack49,99EUR, cordon9,89EURincltaxlocale, deuxcosses1,344EURTTCindicatifs, soit61,224EURavantgaine/frais/outils et sansTVAFrance finaleconfirmée. LesréférencesG1/510 sont arrêtéeschezfabricant ; offresdistributeursexistantes vérifiées ouindexées, étatdulotàcontrôler. Pasd’offreAmazonexactevalidée pourcesréférences.

LeS65 peutêtre conservé avec laG1àéquilibrage, chargeinitiale5A ; **cordon/adaptateur dechargeIC5distinct àsélectionneravantcharge**. Ne pascommander uneG2comme substitution. Énergie37Whcontre38,48WhdeZeee(-3,85%), sanspreuve d’autonomie. Châssis, supportcaméra, surveillance etvisserie finale restentpourlafin.

[VarianteXT60 nonretenue](variante-xt60-non-retenue.md) : modèlesinitiaux gardéscommeargumentdecomparaison ; pas un achat supplémentaire.''')
 write(BASE/'revision-batterie-ic5.md',f'''# Révision batterie et cordon IC5

{INTRO}

## Batterie et charge

LaSpektrumG1SPMX50002S30H5resteuneLiPostandard2S7,4V,8,4Vmax,5000mAh/37Wh. Dimensions139×46×25mm/294g annoncées suranciennepagefabricant ; laficheactuelle confirmegénérationG1mais signale«Discontinued». LeSKUexactchezRCTeam afficheavailable:trueet49,99EUR lorsdela consultation publique15octobre2026. La photodeceréférence montrel’équilibrage3voies ; autresphotosdegamme ne sont pas despreuvesdecotes. Vérifierdate/étatdulot etnotice. Unseulpackembarqué,pasdesérie/parallèle.

[AchatRCTeam]({BATT}) · [Référencefabricant](https://my.spektrumrc.com/Products/Default.aspx?ProdID=SPMX50002S30H5) · [FAQG1/G2](notices/Spektrum-G1-G2-FAQ-original.pdf).

LaFAQHorizon permet lachargeG1avecéquilibrage surunchargeurclassique. LeS65est conservé :LiPoBalance2S,1C=5A initialement,8,4V,42W, équilibrageJST-XH. Adaptationducordondecharge versIC5àprévoirséparément : nepasbrancherlecordonauxcossesduvéhiculeauchargeur. LaG2sanséquilibrage neconvientpasauS65 ; ses fonctionsSmart nécessitentchargeurG2. LacarteSmartG1stocke etdéchargeautomatiquement maisne remplacepas lacoupurebasse tension duvéhicule.

## Pourquoi IC5

LeguideSpektrumduFirmaSPMXSE1100donne100Acontinus pourcetESCetunepriseIC5unique. Nouseninférons que cettefamilleauthentique estunemeilleurepistepour44,39A qu’unXT60documenté35AMAX. **Cen’estpas uneampacitéindépendante du510 niunequalificationdenotremontage.** AucuneprisegénériqueEC5substituée surlaseuleressemblancedulogement : laficheAMASSE C5 historique40ARC nevalidepas44A. Pasderating120Ainventé, pasdecalibredufusibleconfonduavecunlimiteur.

[Guideapplication100A/IC5](notices/Spektrum-Firma100A-IC5-reference-original.pdf) · [Cordonconstructeur]({OEM}).

## Pièces, achat et devis

SPMXCA510est lecordon«Device»pré-câblé deuxfils10AWGde4in,environ100/101,6mm. Photooriginale : deuxfilsrouge/noir, aucunfilSmartlibre. Diamètredegaine, brins, godets, précisionlongueuretréférenceinsulation noncotés. Lesemboutsvisiblementétamés peuventnécessiterune recoupeavantsertissage ; longueurutileàmesurer. Ne pasallongerautomatiquementlepositifavantfusible. Pré-câblage permetdeconserverlesraccordsfabricant ; seulsertissagedescossesparl’utilisateur.

Freakware affiche9,89EURtaxelocaleincluse etstockpourSPMXCA510 ; livraisonetTVAFrancefinalesnonconfirmées. PackRCTeam49,99EURdisponible. DeuxTE1301910,672EURTTCindicativeschacune d’aprèsDigiKeyindexé, soit1,344EUR. **Sous-total61,224EURindicatif**, horsgaineexistante, port,outils etajustementTVA ; pasdetotalV3. LelotBNTECHGO12AWG(31,93EURAmazon) resteallouéauxESC etne se rajoutepasaucordonIC5. Lesdeuxcosses remplacentles95R5deCP0,paslesautres95R5.

[Freakwarecordon]({BUY}) · [TE130191](https://www.te.com/en/product-130191.html). RechercheAmazonfrparSPMX50002S30H5/SPMXCA510 :aucuneoffreexactevérifiée ; fournisseursalternatifsidentifiés, pasde lien derecherche présentécommeoffreinstock.

## Avis et limites

Le forumARRMAdu21octobre2020décrit le510pouradapterunecommandeclassiqueauxbatteriesIC5. Retoursutilisateursconfus surlesexedeslogements :choisir«Device»parréférenceetvérifiercontacts/polarité, pasleterme«mâle»seul. Nous terminonslesfilsauxcosses, sansjonctionfilàfildufaisceauembarqué. AucunessaiinstrumentédelaassociationG1+510+130191exacttrouvé, niavisquantitatifde43/44A. Avisdedistributeuretnotesd’autresréférencesn’ontpasététransposés.

[ForumARRMA](https://www.arrmaforum.com/threads/castle-esc-to-spektrum-smart-battery-connection.29211/).

Capacité-3,85%etmasse+44gannoncéesparrapportZeee ; maintienprovisoiregéométriquementprochemais àrequalifierpourlanouvellemasse. Longueur/quantitédesmanchonsàconfirmer.DimensionscorpsIC5estiméesdansCAO : réserved’espaceetmesuresavantchâssis. Objectifsvitesse/autonomie inchangés, nonmesurés.''')
 sub=BASE/'cordon-ic5-spektrum';write(sub/'README.md',f'# Spektrum SPMXCA510 - IC5 Device pré-câblé\n\n{INTRO}\n\nUneprise et deuxfils10AWG4in inclus :1cordonàacheter, pasunconnecteur+unlotfilenplus. [AchatEU]({BUY}),9,89EURtaxelocaleaffichés, totalFranceàconfirmer. Référencearrêtéechezfabricant mais stockedchezdistributeurs.\n\n[Cotes](cotes.md) · [Notice](../notices/notice-cordon-principal-batterie-v3.pdf) · [Montage](../integration.md) · [Devisetsources](../revision-batterie-ic5.md) · [STEP](3D/README.md) · [Photooriginale](../references/Spektrum-SPMXCA510-original.jpg).')
 write(sub/'cotes.md','''# Cotes du SPMXCA510

| Grandeur | Donnée | Statut |
| --- | --- | --- |
| Référence | IC5 Device,SPMXCA510 | Spektrum ; complément du packIC5 |
| Conducteurs | Deuxfils10AWG,4in≈101,6mm | Spektrum/photoconstructeur ; cuivre10AWGnominal≈5,26mm² |
| Diamètre gaine | Ø5,5mm dansCAO | estimé,aucunODconstructeurretrouvé |
| Enveloppe métal | Ø3,0mm dansCAO | estimée ; pasnombredebrins/massedecuivre |
| Corps | ≈24×21×11mm | reconstructionvisuelleestimée,pasplancoté |
| Entraxe / contacts | 9,6mm/Ø5mm dansCAO | estimés,mesureravantconceptiond’unconnecteuraccouplé |
| Extrémités | Pré-étamage apparent surphoto | lotàcontrôler,recoupeavantsertissagesinécessaire |
| Fils installés CAO | ≈92mm développés,poseprovisoire | en dessouslongueurinitiale, pasdébitdefabrication |

Seulelongueur/calibre/identitésont desdonnéescommercialespubliées. Lesrayons, clips, godets, profondeurs, couleurs, capot etcontactSmart nonconnecté sontestimés. Aucunecompatibilitédejeuouampacitévalidéepar leSTEP.''')
 jw(sub/'sources.json',dict(checked_on='2026-10-15',manifest='../sources.json',manufacturer=OEM,photo='../references/Spektrum-SPMXCA510-original.jpg',buy=BUY));jw(sub/'nomenclature.json',dict(ref='SPMXCA510',quantity=1,included=['IC5 Device','2x10AWG 4in'],connector_separate_purchase=False,wire_separate_purchase=False))
 # Mark initial component dossiers as legacy without deleting existing files.
 for folder in ['prise-xt60h-m','fils-12awg']:
  p=BASE/folder/'README.md';text=p.read_text(encoding='utf-8');write(p,'> **Variante initiale non retenue pourCP0 aprèslechoixIC5.** Voirla [sélectionactive](../README.md).\n\n'+text)
 # Shared termination references are still active on 10AWG, not only the old12AWG.
 for folder in ['cosses-te-130191','isolation-atum']:
  p=BASE/folder/'README.md';write(p,p.read_text(encoding='utf-8')+'\n\nMiseàjourIC5 : deuxterminaisonssurlesfils10AWGduSPMXCA510 ; lesmentionsXT60 ducorpsdecedossier concernentlavarianteinitiale. [Montageactif](../integration.md).')
 batt=ROOT/'Composants/batterie/spektrum-g1-ic5';write(batt/'README.md',f'''# Batterie2S révisée - Spektrum G1 IC5

{INTRO}

SPMX50002S30H5 :LiPostandard2S,7,4V/8,4Vmax,5000mAh/37Wh,139×46×25mm/294g annoncés,priseIC5d’usine. G1avecéquilibrage3voiesvisible,àcontrôlersurlot. [AchatRCTeam]({BATT}),49,99EURetdisponibleàla consultation. Fabricantcurrentannonce arrêté ; surveillerétat/date dulot, disponibiliténonpérenne. AucunAmazonexactvalidé.

LeS65 resteappropriéàlaG1aveclaconnexiondechargeadaptée,5Ainitialement ; pasuneG2sanspriseéquilibrage. Laconfigurationmoteur2Sresteinchangée. Énergie-3,85%parrapportZeee, masse+44gannoncés, doncmaintien/autonomieàréévalueret objectifsnonvalidés.

[Noticecommune](../../cordon-principal-batterie/notices/notice-cordon-principal-batterie-v3.pdf) · [Révisionetsources](../../cordon-principal-batterie/revision-batterie-ic5.md) · [Photoexacte](../../cordon-principal-batterie/references/SPMX50002S30H5-photo-1.jpg). LesSTEPZeeeexistants représentent l’ancienpack et ne deviennentpasdesmodèlesSpektrum.''')
 jw(batt/'selection.json',data['active_battery'])
 for rel,link in [('README.md','Composants/cordon-principal-batterie/README.md'),('SPECIFICATIONS.md','Composants/cordon-principal-batterie/README.md'),('Composants/README.md','cordon-principal-batterie/README.md'),('Composants/batterie/README.md','spektrum-g1-ic5/README.md'),('Composants/chargeur-batterie/README.md','../cordon-principal-batterie/revision-batterie-ic5.md'),('Composants/maintien-batterie/integration.md','../cordon-principal-batterie/revision-batterie-ic5.md')]:
  p=ROOT/rel
  if p.exists():write(p,'> **Révisiondu15octobre2026 : batterie2S G1IC5etcordon10AWGproposésaprèschoixutilisateur.** [Étatcourant]('+link+'). Anciensplans/PDFdeZeee restentdatés ; chargeS65à5AavecadaptationIC5distincteàprévoir.\n\n'+p.read_text(encoding='utf-8'))
 # Replace the scoped current handoff, keeping prior unscoped content intact.
 for p in [ROOT/'README.md',ROOT/'SPECIFICATIONS.md',ROOT/'Composants/README.md',ROOT/'Composants/ENSEMBLES-AVANT-CHASSIS.md',ROOT/'Composants/faisceau-puissance/integration.md',ROOT/'Composants/protection-surintensite/integration.md',ROOT/'Composants/distribution-alimentation/integration.md']:
  if p.exists():
   s=p.read_text(encoding='utf-8');s=re.sub(r'(?s)(<!-- cordon-principal-batterie-v3 -->).*?(<!-- /cordon-principal-batterie-v3 -->)',r'\1\n15 octobre 2026 : version activeIC5aprèschoixutilisateur, packSpektrumG1SPMX50002S30H5 etcordonpré-câbléSPMXCA51010AWG. CP0+→MIDIentréeM5,CP0-→D-N2avecTE130191 ; avalMIDI→ED80→D+reste6mm². VarianteXT60 nonretenue. CourantetcoordinationduMIDI60Aàqualifier ; adapterlachargeIC5/S65séparémentavantcharge.\n\2',s);write(p,s)
 write(BASE/'notices/README.md',(BASE/'notices/README.md').read_text(encoding='utf-8')+'\n\n## RévisionIC5active\n\n[FAQHorizonG1/G2originale](Spektrum-G1-G2-FAQ-original.pdf) · [ApplicationFirma100AIC5originale](Spektrum-Firma100A-IC5-reference-original.pdf). La noticefrançaise présente lecordonIC5actif ; lesdocumentsXT60 sont desréférencesdelavarianteinitiale.')
 # Theoretical wire losses, explicitly not a manufacturer resistance.
 calc=dict(checked_on='2026-10-15',active='IC5 10AWG',wire_section_nominal_mm2=5.26,length_per_pole_study_m=.10,resistivity_assumed_Cu_20C_ohm_m=1.724e-8,R_loop_theoretical_ohm=1.724e-8* .20/(5.26e-6),actual_wire_resistance_not_published=True,excludes=['packleads','IC5contacts','terminations','fuse','ED80','bus'],does_not_establish_ampacity=True,rows=[])
 for I in [10,20,30,44.39]:calc['rows'].append(dict(current_A=I,drop_V=I*calc['R_loop_theoretical_ohm'],loss_W=I**2*calc['R_loop_theoretical_ohm']))
 jw(BASE/'calculs-ic5.json',calc)
 from main_cord_ic5_text import write_human_documents
 write_human_documents(ROOT)
 print('IC5 revision written',flush=True)
if __name__=='__main__':main()
