"""Two project PDFs. Render all pages; independent visual QA is recorded later."""
from pathlib import Path
import sys, json, html, hashlib
import pymupdf
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Spacer, PageBreak, Image
from build_heatsink_pdf import p as raw_p, table, banner as raw_banner, GREY
from supply_audit_pdf_text import charge_story, PARAGRAPH_CORRECTIONS
import re
ROOT=Path(__file__).resolve().parents[1]; C=ROOT/'Composants'; BASE=C/'verification-alimentation'; TMP=ROOT/'tools/temp/supply-audit/pdf'
def readable(text):
 for prefix,replacement in PARAGRAPH_CORRECTIONS.items():
  if text.startswith(prefix):text=replacement;break
 for word in ['Pololu','LAPP','LFT','KLKD','MIDI','ATO','AWG','WAGO','SSR','ESC','Pi','CP','TE','RC','S65','G1','XH','IC5','EC5','BEC','GPIO','JSON','F0','F1','F2','FP','VSW','ED80','D1D100','UD80','HS251','UL','STEP','PDF','CSA','Midget']:
  text=re.sub(r'(?<=[a-z?-?])'+re.escape(word), ' '+word,text)
 text=re.sub(r'(?<=\d)(?=(?:AWG|mm|cm|km|min|A\b|V\b|W\b|Wh\b|EUR|USD|\bbrins))',' ',text)
 fixes={'auxpads':'aux pads','airlocal':'air local','?puissance':'? puissance','?travers':'? travers','?dimensionner':'? dimensionner','lescharges':'les charges','pourstockage':'pour stockage','isolant105':'isolant 105','parcellule':'par cellule','sixfils':'six fils','cinquede':'cinq de','neufsignaux':'neuf signaux','deuxfois':'deux fois','deuxpositifs':'deux positifs','quatreGND':'quatre GND','LesPDF':'Les PDF','TableBlueSea':'Table Blue Sea','avantF0':'avant F0','apr?sF0':'apr?s F0','supportLFT':'support LFT','moteursKLKD':'moteurs KLKD','deBEC':'de BEC','duLFT':'du LFT','unmaximum':'un maximum','unoriginal':'un original','de2 s':'de 2 s','vid?oactive':'vid?o active','SCCRg?n?rique':'SCCR g?n?rique','?600':'? 600','?20':'? 20','?5':'? 5','?40':'? 40','?6':'? 6','?8':'? 8','?135':'? 135','?200':'? 200','cadreUL':'cadre UL','sourcePi':'source Pi','supportPi':'support Pi','principal50':'principal 50','de50':'de 50','de20':'de 20','de10':'de 10'}
 for a,b in fixes.items():text=text.replace(a,b)
 # Separate ordinary prose from numbers, while preserving uppercase part codes.
 text=re.sub(r'([a-zà-ÿ]{3,})(?=\d)',r'\1 ',text)
 text=re.sub(r'\b(au|de|du|à|le|la|des|les)(?=\d)',r'\1 ',text)
 for a,b in {'tenueDC':'tenue DC','deL600':'de L600','retourD':'retour D','lepack':'le pack','descharges':'des charges','côtéPi':'côté Pi','auxpadsPi':'aux pads Pi','etS':'et S','k100':'k 100','moteur/Pi':'moteur / Pi','JLLN050.T50':'JLLN050.T / 50','KLKD020.T20':'KLKD020.T / 20','KLKD010.T10':'KLKD010.T / 10'}.items():text=text.replace(a,b)
 for a,b in {'Beez 2B':'Beez2B','positifSPMX':'positif SPMX','négatifSPMX':'négatif SPMX','SOLISTRAND32151':'SOLISTRAND 32151','TE32151':'TE 32151','TE130191':'TE 130191','ATUM8':'ATUM 8','LAPP6':'LAPP 6','HEAT180':'HEAT 180','SiF6':'SiF 6','Pi18':'Pi 18','Pi5':'Pi 5','GND18':'GND 18','Molex40':'Molex 40','MIDI60':'MIDI 60','de5':'de 5'}.items():text=text.replace(a,b)
 text=re.sub(r'\s*([≤≥≈])\s*',r' \1 ',text)
 return text

def p(text,style='body'):
 # Protect markup and link targets; only visible text is formatted.
 parts=re.split(r'(<[^>]*>)',str(text))
 return raw_p(''.join(x if x.startswith('<') else readable(x) for x in parts),style)
def banner(text):return raw_banner(readable(text))

def t(rows,widths=(57,117)):
 return table([[html.escape(readable(str(c))) for c in row] for row in rows],widths)
def ref(label,url): return p(f'<link href="{html.escape(url,quote=True)}" color="#174969">{html.escape(label)}</link>','small')
def pic(path,width):
 with PILImage.open(path) as image:w,h=image.size
 return Image(str(path),width=width*mm,height=(width*h/w)*mm)
def footer(canvas,doc):
 canvas.saveState();canvas.setStrokeColor(colors.HexColor('#ccdbe4'));canvas.line(18*mm,17*mm,192*mm,17*mm)
 canvas.setFont('HV3',7.2);canvas.setFillColor(GREY);canvas.drawString(18*mm,12*mm,'Drone V3 | Alimentation R2 | 15 octobre 2026 | Étude, aucun essai matériel')
 canvas.drawRightString(192*mm,12*mm,str(doc.page));canvas.restoreState()
def build(out,story,name):
 out.parent.mkdir(parents=True,exist_ok=True)
 doc=SimpleDocTemplate(str(out),pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=18*mm,bottomMargin=23*mm,title=name,author='Projet Drone V3')
 doc.build(story,onFirstPage=footer,onLaterPages=footer)
 pdf=pymupdf.open(out);folder=TMP/out.stem;folder.mkdir(parents=True,exist_ok=True);renders=[]
 for i,page in enumerate(pdf):
  path=folder/f'page-{i+1}.png';page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(path)
  renders.append(dict(page=i+1,file=str(path.relative_to(ROOT)),text_chars=len(page.get_text())))
 meta=dict(file=str(out.relative_to(ROOT)),pages=len(pdf),generated_on='2026-10-15',sha256=hashlib.sha256(out.read_bytes()).hexdigest(),renders=renders,visual_review_complete=False,generator='tools/build_supply_audit_pdf.py')
 out.with_suffix('.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 sheet=PILImage.new('RGB',(1200,((len(pdf)+1)//2)*850),'#d8dfe3')
 for i,r in enumerate(renders):
  im=PILImage.open(ROOT/r['file']).convert('RGB');im.thumbnail((588,838));sheet.paste(im,((i%2)*600+6,(i//2)*850+6))
 sheet.save(folder/'contact-sheet.png'); print(out.name,len(pdf),'pages',out.stat().st_size,'bytes',flush=True)

def audit():
 calc=json.loads((BASE/'calculs.json').read_text(encoding='utf-8'))
 story=[p('Alimentation V3<br/>Vérification et corrections','title'),p('Pack G1 IC5, protection, alimentation Pi et charge S65'),
  banner('<b>Conception révisée, pas une qualification matérielle.</b> Charge complétée ; références et raccordements corrigés. Confirmer les terminaisons des supports et leur association en défaut DC, puis vérifier le montage reçu avant mise sous tension.'),Spacer(1,4*mm),
  t([['Ancien choix / problème','Révision proposée'],['S65 XT60 / pack IC5 sans cordon','Beez2B BEEC1067 XT60–EC5 ; rallonge XH 2S dédiée'],['MIDI 60 A / défaut inconnu','JLLN050.T rapide 50 A / 20 kA DC ; LFT300601C et capot'],['ATO 30 A des deux ESC','Deux KLKD020.T rapides 20 A ; étude 15 A continus par ESC'],['ATO 7,5 A entrée Pi','KLKD010.T 10 A ; entrée régulateur ≠ courant de sortie Pi'],['Fil FLRY-B limité à70 °C','LAPP HEAT180 SiF6 mm² ; pose fixe espacée et ventilée'],['D24V90F5 / faible marge','Pololu D42V55F5 /5571, 5 V ±3 %, dropout typique ≈0,25 V à5 A'],['Puissance via contacts Molex','Neuf signaux ; alimentation Pi18 AWG soudée aux pads, deux positifs / quatre GND'],['Retour de logique via B0','Logique sur positif aprèsF0 / avantED80, retourD− ; voies de cellules isolées']]),Spacer(1,4*mm),
  p('Moteurs, Pi5, caméra, batterie G1, rails2315, ED80, D1D100 / HS251 et UD80 conservés. Objectifs40 km/h, 10–20 min à40 et45 min à20 inchangés. Aucun achat, montage ou essai physique.'),PageBreak(),
  p('Cordon principal et protection','title'),
  p('<b>Chemin positif :</b> packIC5 → positifSPMXCA510 ≥85 mm → TE32151 → extensionLAPP6 mm² ≥120 mm → JLLN50 /supportLFT → ED80 → D+.'),
  p('<b>Retour :</b> négatifSPMXCA510 → une TE130191 → D− N2. La cosseM5 positive disparaît. Extension et raccord non représentés dans les anciens STEP du cordon : ils deviennent historiques.'),
  t([['Élément','Préparation / limite'],['SPMXCA510','Deux fils10 AWG inclus. Ne pas raccourcir le positif sous85 mm de conducteur après préparation.'],['TE SOLISTRAND32151','Bout à bout12–10 AWG /2,62–6,64 mm² par côté ; cuivre ; L14,35 mm /ID3,28 mm. Sertissage constructeur.'],['Extension LAPP6 mm²','Au moins120 mm de conducteur avantF0 ; section admise≤6,64 mm² pour le calcul ; protection contre abrasion.'],['ATUM8/2 au raccord','Provision35–40 mm, à ajuster au recouvrement et retrait longitudinal ; même lot de gaine prévu.'],['LFT300601C + LFT30060FBC','Support60 A recevant le fusible50 A ; capot distinct ; fil6–14 AWG :2,8 N·m. Admission des brins fins à confirmer.']]),Spacer(1,3*mm),
  p('Le segment avantF0 reste hors protection parF0. Il doit rester court, isolé et protégé mécaniquement. La longueur minimale vient du calcul de défaut ; aucun fil négatif n’est crédité. Le principal ne protège pas les fils d’équilibrage.'),
  p(f"<b>Borne conditionnelle de courant :</b> à8,4 V, cuivre à0 °C, Rmin du seul positif ≈{calc['fault_bound']['positive_wire_R_min_ohm']*1000:.3f} mΩ ; Iprospectif ≤{calc['fault_bound']['source_fault_upper_A']/1000:.2f} kA. Sections maximales retenues :6,0 mm² pour le510 et6,64 mm² pour l’extension. Résistance de batterie, retour, raccord et fusible tous exclus."),
  banner('Cette borne est un calcul de conception sous conditions de longueur, section et topologie. Ce n’est pas le courant mesuré du pack. Une alimentation parallèle ou un défaut en amont deF0 n’est pas couvert.'),PageBreak(),
  p('Départs, fusibles et thermique','title'),
  t([['Départ','Calibre / hypothèse'],['Principal','JLLN050.T50 A ; budget commun continu36 A'],['ESC1 etESC2','KLKD020.T20 A chacun ; régime continu étudié15 A chacun'],['Pi, avant2813','KLKD010.T10 A ; calcul du courant d’entrée par puissance / rendement / tension'],['Supports de départ','L60030M1PQ×3, pression sous vis10–14 AWG ;2,3 N·m. Languettes rapides20 A inutilisées.'],['Pi au support de fusible','12 AWG dans le support ; deux WAGO221-413 supplémentaires, positif et GND, pour passer au18 AWG côtéPi.']]),Spacer(1,3*mm),
  p('KLKD :50 kA DC dans le cadreUL248-14, distinct des10 kA de l’usage photovoltaïqueUL248-19. Le fabricant recommande le supportMidget, mais la tenueDC de l’association et la terminaison duLFT restent à confirmer.'),
  p('KLKD à135 % du calibre : coupure≤60 min ; à200 % :≤2 min selon la table des exigences. Ce ne sont pas des limiteurs instantanés. Un PWM ne mesure pas le courant.'),
  t([['Conducteur / comparaison','Valeur'],['10 AWG /6 mm² /16 AWG','TableBlueSea, air30 °C, isolant105 °C, fils libres :60 /65 /25 A'],['Comparaison à40 °C','Facteur prudent supposé0,90 :54 /58,5 /22,5 A ; pas une ampacité certifiée du lot'],['Fil16 AWG, examen court','Avec k100 etS1,31 mm² :I²t de comparaison17 161 A²s'],['KLKD20, coupure publiée','1 151 A²s à20 kA /600 V DC ; pas un maximum garanti à8,4 V'],['KLKD10, coupure publiée','455 A²s, mêmes conditions ; fil 18 AWG retenu, 150 brins de diamètre 0,08 mm : S ≈ 0,754 mm², comparaison ≈ 5 685 A²s']]),Spacer(1,3*mm),
  p('Le calcul court suppose cuivre initialement≤85 °C et borne finale160 °C. Il ne remplace pas la thermique d’une surcharge lente. Les fils16 AWG d’usine doivent avoir un isolant et une pose appropriés. La pose groupée / sous mousse est exclue de ce repère. Ne pas utiliser la valeur incohérente15,930 W de pertesKLKD20 à80 % dans la fiche2025.'),
  p('À ce stade : pas de sélectivité complète ni de survie du relais garanties ; le courant normal, les pointes, les températures et l’énergie maximale de coupure restent à qualifier.'),PageBreak(),
  p('Alimentation Pi et marge de tension','title'),
  p('Nouveau Pololu5571 :5 V ±3 %, courant typique5–8 A selon conditions ; dropout à5 A≈0,25 V lu sur la courbe. Version5 V, pas5,3 V. Le plan et le STEP officiels sont archivés.'),
  pic(BASE/'references/Pololu-0J13533.jpg',145),p('Courbe officielle Pololu D42V55Fx ; sortie5 V en vert. Lecture typique, pas une garantie de dropout maximal. Source : pagePololu5571.','small'),
  t([['Budget choisi','Valeur / qualification'],['Sortie maximale étudiée','5,15 V ×5 A =25,75 W ; rendement bas supposé80 %'],['Boucle commune avantD+/D−','Résistance acceptée≤5 mΩ, à mesurer'],['Chemin d’entréePi','Résistance acceptée≤50 mΩ, à mesurer'],['VIN et sortiePi','VIN≥5,8 V ;4,75–5,25 V auxpadsPi, sans sous-tension ni redémarrage'],['Faisceau5 V','Deux+5 V /quatreGND18 AWG,≤50 mm ; grands pads et maintien']]),
  p('Le Molex n’achemine plus la puissance. Ses positions2/4/6/9/14/20 restent vides ; neuf contacts logiques conservés. Pas deBEC6 V sur les railsPi. Aucun réglage de capacité5 A appliqué avant essais.'),PageBreak(),
  p('Calcul global et autonomie','title'),
  p('Résolution du courant d’entrée àpuissance constante, avec pertes des budgets de résistance. Les résistances et le rendement sont des hypothèses d’acceptation, pas des mesures. La commandeSSR est comptée à15 mA dans la branchePi.'),
  t([['Pack /moteurs','VIN Pi','I branchePi','I commun'],*[[f"{r['Vpack_V']:.1f} V /{r['motors_A']} A",f"{r['Pi_VIN_V']:.3f} V",f"{r['Pi_branch_A']:.2f} A",f"{r['main_A']:.2f} A"] for r in calc['supply_rows']]],(58,38,39,39)),Spacer(1,3*mm),
  p('Cas continu proposé :15 A parESC, soit30 A moteurs ; total calculé≈35,4 A à6,4 V avecPi5 A. Budget36 A, air local≤40 °C. Deux fois20 A constituent le scénario court de2 s, pas le régime permanent accepté. Le logiciel n’impose pas encore ces intensités.'),
  t([['Objectif','Puissance totale moyenne maximale'],['45 min à20 km/h','39,47 W'],['20 min à40 km/h','88,8 W'],['10 min à40 km/h','177,6 W']]),Spacer(1,3*mm),
  p('Pack5 Ah /7,4 V :37 Wh nominaux ;29,6 Wh avec80 % utilisables supposés. Tous les consommateurs et pertes sont inclus. À44 A constants, l’estimation idéale ne donne que6,82 min, sans réserve : ce n’est pas notre consommation moyenne annoncée.'),
  p('La vitesse seule ne fixe pas le courant moteur. Les objectifs utilisateur restent identiques ; relever vitesse,Wh et températures en roulage vidéoactive à20 et40 km/h.'),PageBreak(),
  p('Surveillance et qualification restante','title'),
  p('<b>Correction de masse :</b> alimenter la logique indépendante depuis le positif aprèsF0 /avantED80, àtravers une protection auxiliaire àdimensionner ; retourD−. B0/B1/B2 ne rejoignent que les circuits de cellule locaux et leurs optocoupleurs. Pas de retour moteur/Pi par le fil d’équilibrage.'),
  p('Prévoir les protections proches du pack sur les voies fines. Leur schéma/routage est réservé àla phase finale : le principal50 A ne les protège pas. La surveillance reste alimentée après coupure descharges ; débrancher lepack pourstockage.'),
  banner('<b>Confirmations fabricant avant achat des supports :</b> admission des brins fins /terminaisonLFT ; tenueDC deL60030M1PQ +KLKD ; enveloppe maximale de coupure aux défauts pertinents à8,4 V. Aucune de ces confirmations n’est simulée par un nouveau choix de référence.'),Spacer(1,3*mm),
  p('Essais matériels àexécuter ensuite','sub'),
  p('Réception et polarités ; préparation/traction des sertissages ; alimentation limitée au laboratoire ; sourcePi0–5 A etéchelons ; mesureKelvin desbudgets ; thermique stable15 A parESC avecPi active ; pointes etfreinage ; perteWi-Fi etcommandes ; seuils decellules simulées ; chargeBalance2S ; parcours d’autonomieavecvidéo.'),
  p('Ne pas court-circuiter laLiPo pourmesurer son courant de défaut. La température du radiateur ne mesure pas directement celle de lajonctionSSR. Les tolérancesfabricant et les limites lesplus basses prévalent sur les critèresprojet.'),
  p('Archives et implantation','sub'),
  p('AnciensPDF/STEPavecMIDI, deuxcossesCP0 etpuissanceMolex : historiques, signalésdanslesindex. Lesancienscontrôles303PASSnevalidentpasR2. NouveauSTEPduPololuofficiel conservé ; lesautresnouveauxcomposantsne sontpasmodélisésdanscettevérification. Châssis, supportcaméra, visseriefinale etroutage de surveillance restentàlafin.'),PageBreak(),
  p('Achat et sources traçables','title'),
  p('Charge :BEEC1067 à6,90 EUR TTC, SKUexactdisponible dansleJSONpublic ; rallonge dédiée2S à1,40 EUR au relevéantérieur, àrevalider. Complément8,30 EUR horsport. DeuxWAGO supplémentaires auprixantérieur0,75 EUR/pièce, àrevalider. Pasdetotalglobal avec les prixinconnus.'),
  p('Pololu5571 :47,95 USD fabricant. Nouvellesprotections, capots,LAPP,raccord : prixFrance nonconfirmés. Lesprix du supportMidgetC ne sontpastransférés auPQ. AucuneoffreAmazon.fr exactevalidée ; lesrecherches parréférence neprouventpasunstock.'),
  ref('JLLN 2025 : tensions, pouvoir de coupure et courbes','https://www.littelfuse.com/assetdocs/jlln-datasheet?assetguid=3a7bc9bf-d932-4401-bdc7-b39f302195cf'),
  ref('KLKD 2025 : exigences, énergies et dérating','https://www.littelfuse.com/assetdocs/klkd-fuse-datasheet?assetguid=7b52eebb-c7cc-43df-a8da-9682a338e0f6'),
  ref('Support LFT, fiche2025 et capots','https://www.littelfuse.com/assetdocs/lft-datasheet?assetguid=56b8955c-9cf7-4814-a923-97a4406bfa77'),
  ref('CertificatCSA : LFT30060 /20 kA DC, pagePDF7','https://www.littelfuse.com/assetdocs/csa-6225-01-007316?assetguid=203ad805-7e22-463f-997a-2431bbdfbbd1'),
  ref('SupportsMidget : types, plages, couples et recommandationKLKD','https://www.littelfuse.com/de/assetdocs/powr-gard-catalog?assetguid=85d36235-a32b-4608-bfed-f9878aa43af0'),
  ref('TE32151, raccord2,62–6,64 mm²','https://www.te.com/en/product-32151.html'),
  ref('LAPP SiF : catalogue de famille et références rouge/noir','https://e.lapp.com/jp/p/temperature-resistant-cables/oelflex-heat-180-sif-1x6-ye-0054005'),
  ref('Pololu 5571 — source, courbes et documents','https://www.pololu.com/product/5571'),
  ref('RC Team : cordon compatibleS65','https://www.rcteam.com/products/beez2b-cable-de-charge-xt60-vers-ec5-beec1067'),
  p('Archiveslocales :planPololu,ficheLAPP,tableBlueSea2011 (PDF5),ficheTE32151,docsMidgetetKLKD2021, photosetJSONstock. JLLN/KLKD/LFT2025consultésenligne ; copie directerefusée403. Fichiers etSHA256dansassets.json. NoticesS65/Horizon/ESC conservéesdansleursdossiers. Aucunoriginalmodifié.','small')]
 build(BASE/'notices/verification-alimentation-v3.pdf',story,'Drone V3 — correction alimentation R2')

def charge():
 folder=C/'cordon-charge-s65-ic5'
 story=charge_story(folder,p,t,banner,pic,ref,Spacer,PageBreak,mm)
 build(folder/'notices/notice-cordon-charge-s65-ic5-v3.pdf',story,'Drone V3 ? cordon de charge S65 IC5')

if __name__=='__main__':
 sys.stdout.reconfigure(encoding='utf-8');audit();charge()
