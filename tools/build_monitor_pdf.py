"""Illustrated M1 notice; run after KiCad and STEP checks. Render all pages."""
from pathlib import Path
import html,json,sys
import pymupdf
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate,Spacer,PageBreak,Image
from reportlab.graphics.shapes import Drawing,Rect,Line,String,Circle,Polygon
from build_heatsink_pdf import p as base_p,table as base_table,banner as base_banner,BLUE,GREY
from monitor_typography import clean

ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Composants/carte-surveillance-electrique'
TMP=ROOT/'tools/temp/surveillance-review/pdf';OUT=B/'notices/notice-carte-surveillance-v3.pdf'

def p(text,*args,**kwargs):return base_p(clean(text),*args,**kwargs)
def table(rows,*args,**kwargs):return base_table([[clean(c) for c in row] for row in rows],*args,**kwargs)
def banner(text,*args,**kwargs):return base_banner(clean(text),*args,**kwargs)
def picture(path,w,h):
    from PIL import Image as PI
    with PI.open(path) as im:a,b=im.size
    s=min(w*mm/a,h*mm/b);return Image(str(path),width=a*s,height=b*s)
def source(title,url):return p('<link color="#174969" href="'+html.escape(url,quote=True)+'">'+html.escape(title)+'</link>','small')
def footer(c,d):
    c.saveState();c.setStrokeColor(colors.HexColor('#cad9e0'));c.line(18*mm,17*mm,192*mm,17*mm)
    c.setFont('HV3',7.3);c.setFillColor(GREY);c.drawString(18*mm,12*mm,'Drone V3 | Surveillance M1P | 15 octobre 2026 | Banc limite, non teste')
    c.drawRightString(192*mm,12*mm,str(d.page));c.restoreState()
def architecture():
    d=Drawing(174*mm,92*mm)
    def txt(x,y,t,size=8):d.add(String(x*mm,y*mm,t,fontName='HV3',fontSize=size,fillColor=BLUE))
    def line(a,b):d.add(Line(a[0]*mm,a[1]*mm,b[0]*mm,b[1]*mm,strokeColor=BLUE,strokeWidth=1.1))
    def rect(x,y,w,h,t):
        d.add(Rect(x*mm,y*mm,w*mm,h*mm,fillColor=colors.HexColor('#edf4f7'),strokeColor=BLUE));txt(x+2,y+h/2-1,t)
    rect(0,65,45,16,'AUX apres F0 / avant ED80');rect(56,65,34,16,'Pololu 2831 / 5 V');line((45,73),(56,73))
    rect(106,73,28,13,'TMR isole C1');rect(106,51,28,13,'TMR isole C2');line((90,73),(99,73));line((99,57),(99,80));line((99,80),(106,80));line((99,57),(106,57))
    rect(144,73,29,13,'EVM cellule 1');rect(144,51,29,13,'EVM cellule 2');line((134,80),(144,80));line((134,57),(144,57))
    rect(0,30,45,16,'MCP1703A / 3,3 V AUX');line((45,70),(50,70));line((50,70),(50,38));line((50,38),(45,38))
    rect(61,30,43,16,'Optos + Schmitt + OU');line((45,38),(61,38));line((158,51),(158,38));line((158,38),(104,38))
    line((145,73),(139,73));line((139,73),(139,42));line((139,42),(104,42))
    rect(119,6,54,16,'OFF -> Pololu 2813 -> SSR');line((104,34),(111,34));line((111,34),(111,14));line((111,14),(119,14))
    rect(0,6,85,16,'Pi GPIO17/27 : WARN haut ; GPIO22 : DONE');line((61,30),(61,22));txt(1,54,'FAUX 1 A a la derivation, retour D-');txt(1,0,'B0/B1/B2 proteges par 100 ohms au pack -> SENSE et REF locaux uniquement.',8)
    return d
def optical():
    d=Drawing(174*mm,66*mm)
    def text(x,y,s,size=8):d.add(String(x*mm,y*mm,s,fontName='HV3',fontSize=size,fillColor=BLUE))
    def line(x,y,a,b):d.add(Line(x*mm,y*mm,a*mm,b*mm,strokeColor=BLUE,strokeWidth=1))
    text(2,61,'Une cellule : deux sorties isolees, alimentation ISO5 independante',9)
    for x,title in [(6,'HEALTHY'),(93,'WARN_OK')]:
        text(x,51,title,9);text(x,43,'ISO5 local');line(x+17,40,x+17,36)
        d.add(Rect((x+15)*mm,28*mm,4*mm,8*mm,fillColor=colors.white,strokeColor=BLUE));text(x+24,31,'2,2 kohms')
        line(x+17,28,x+17,23);d.add(Circle((x+17)*mm,23*mm,.7*mm,fillColor=BLUE))
        d.add(Rect((x+10)*mm,11*mm,14*mm,8*mm,fillColor=colors.HexColor('#edf4f7'),strokeColor=BLUE));text(x+12,14,'LED opto',7);line(x+17,23,x+17,19)
    line(23,11,23,5);text(5,1,'REF cellule');line(23,23,66,23);text(47,26,'OUTA / J5',7.5);text(44,15,'Bas : LED eteinte',7.2)
    line(110,11,110,5);line(110,5,158,5);text(132,9,'OUTB / J7',7.5)
    return d

def main():
    sys.stdout.reconfigure(encoding='utf-8');TMP.mkdir(parents=True,exist_ok=True)
    calc=json.loads((B/'calculs.json').read_text(encoding='utf-8'));q=json.loads((B/'verification/controle-kicad.json').read_text(encoding='utf-8'))
    # Native vector views are also delivered untouched; raster conversion only for the notice.
    for name in ['routage','montage']:
        doc=pymupdf.open(B/'KiCad/vues'/f'{name}.svg');page=doc[0];page.get_pixmap(matrix=pymupdf.Matrix(2.5,2.5),alpha=False).save(TMP/f'{name}.png')
    story=[p('Carte de surveillance<br/>électrique 2S','title'),p('Révision M1P - modules existants, porteuse et coupure indépendante'),
      banner('<b>M1P : fabrication de prototype pour banc limité, non acheté et non testé.</b> Appliquer l’annexe de préparation et le protocole B00-B14. Le raccordement LiPo / véhicule n’est pas libéré.'),
      table([['Sous-ensemble','Quantité / fonction'],['TI TPS3700EVM-114','2 : une fenêtre de tension par cellule, résistances à adapter'],['TRACO TMR 1-0511','2 : alimentation 5 V isolée des deux voies'],['Pololu D24V10F5 / 2831','1 : 5 V auxiliaire des TMR, distinct du 5 V du Pi'],['Carte porteuse M1','Alimentation 3,3 V, quatre optocoupleurs, Schmitt, diodes et connecteurs']],[65,109]),Spacer(1,3*mm),
      picture(B/'3D/porteuse-surveillance-2s-m1-detaillee.png',142,102),
      p('<b>Porteuse : 140 x 75 x 1,6 mm.</b> Réservation porteuse + modules : 140 x 75 x 30 mm, hors câbles, FAUX/support et résistances au pack. Les dimensions exactes des EVM ne sont pas certifiées ; leurs gabarits 3D sont explicitement distingués des pièces réelles.','small'),PageBreak(),
      p('Architecture et protection','title'),architecture(),Spacer(1,4*mm),
      p('L’alimentation AUX part du positif <b>après F0, avant ED80</b>, à travers un fusible auxiliaire 1 A placé près de la dérivation. Son retour rejoint D-. Le MCP1703A alimente la logique OFF ; le Pololu alimente les deux TMR. Chaque TMR crée un 5 V local isolé pour un EVM et deux LED d’optocoupleurs.'),
      table([['Point','Disposition'],['FAUX / support','KLKD001.T, L60030M1PQ + SPL001. Transition 12/14 AWG vers 22 AWG par WAGO 221-413 ; pas de 22 AWG directement dans ce support.'],['B0 / B1 / B2','100 ohms / 3 W dans CHAQUE fil, au départ du pack. Dérivation réservée à la surveillance, jamais au chargeur.'],['Courant de mesure','Environ 47 microampères max par pont au nominal 4,2 V. Les LED sont alimentées par les TMR, pas par l’équilibrage.'],['Défaut après résistance','Scénario 8,4 V / 90 ohms : moins de 94 mA et de 0,79 W par résistance ; tenue thermique de la pose à vérifier.']],[42,132]),
      p('Ces résistances limitent le courant ; elles ne sont pas des fusibles. Les petits tronçons restant avant elles doivent être séparés et enfermés. Ne pas grouper les corps sous une gaine qui empêche leur refroidissement. La charge S65 utilise sa rallonge d’équilibrage directe et distincte.','small'),
      p('Coordination analysée dans l’annexe M1P : le banc utilise une source AUX limitée à250 mA, résistance série4,7 ohms et simulateurs de cellules limités. La valeur de fusion nominale du fusible ne prouve pas la coupure totale en défaut LiPo ; conditions R2 toujours ouvertes.','small'),PageBreak(),
      p('Adaptation des cartes TI','title'),
      p('Utiliser l’EVM-114 SOT-23. Les modules d’usine surveillent une alimentation d’environ 12 V : ils nécessitent six remplacements de résistances CMS 0603 au total.'),
      table([['Chaque EVM','Réglage M1'],['R1 / R2 / R3','79,6 kohms / 634 ohms / 10 kohms, tolérance 0,1 %'],['Références Vishay','TNPW060379K6BEEA / TNPW0603634RBEEA / TNPW060310K0BEEA'],['J10 / J11','J10 1-2 : MONITOR SENSE ; J11 1-2 : VPU = VDD local isolé'],['R4 / R5 / R6','R4/R5 : 100 kohms selon schéma/BOM, à contrôler ; R6 non montée'],['VDD / GND / SENSE','VDD = ISO5 ; GND = REF local ; SENSE = positif cellule protégé'],['Sorties','J5 = OUTA HARD ; J7 = OUTB WARN_OK ; J9 VEXT libre']],[45,129]),Spacer(1,4*mm),
      table([['Fonction / cellule','Descente typique','Retour typique','Coins calculés*'],*[[('Coupure dure' if r['function']=='hard' else 'Avertissement'),f"{r['falling_nominal_V']:.3f} V",f"{r['rising_nominal_V']:.3f} V",f"{r['with_sense_network_conservative_min_V']:.3f} à {r['with_sense_network_conservative_max_V']:.3f} V"] for r in calc['thresholds']]],[44,39,39,52]),
      p('*VIT- 387 à 400 mV, résistances 0,1 %, biais des DEUX entrées et marge de 17 mV pour le réseau de mesure. La précision de 1 % du seuil positif ne suffit pas à décrire le seuil en descente. Courbes et calculs dans calculs.json.','small'),
      p('Les broches des connecteurs J1 à J9 d’un EVM sont des doublons du même signal. Une rangée deux broches n’est donc pas une paire signal/masse. J3/J4 de la porteuse utilisent un faisceau de cinq fils repérés vers cinq connecteurs TI distincts.'),
      banner('La séparation des seuils laisse une marge de tension, <b>pas un temps garanti d’arrêt Linux</b>. La coupure dure reste prioritaire. Contrôler chaque seuil avec une cellule simulée avant usage.'),PageBreak(),
      p('Logique et Raspberry Pi 5','title'),optical(),Spacer(1,3*mm),
      p('OUTA bas sous le seuil dur shunte la LED HEALTHY : sa disparition fait remonter FAULT, puis le tampon Schmitt demande OFF. OUTB bas au-dessus du seuil d’avertissement allume WARN_OK : l’opto maintient WARN bas. Sous le seuil, WARN remonte. Une perte d’alimentation locale produit aussi un avertissement et une demande de coupure, si la logique AUX reste alimentée.'),
      table([['Porteuse J6','Pi / connexion','État'],['1 - 3V3_PI','Pin physique 1','Rappels WARN au 3,3 V Pi seulement'],['2 - WARN1','GPIO17 / pin 11','HAUT = avertissement cellule 1'],['3 - WARN2','GPIO27 / pin 13','HAUT = avertissement cellule 2'],['4 - DONE','GPIO22 / pin 15','Haut en fin d’extinction, via BAT54'],['5 - GND','Référence système D-','Jamais B0_R ou B1_R']],[44,62,68]),
      p('Deux rappels 47 kohms sont montés <b>côté Pi</b>, pour qu’un câble WARN débranché reste lisible haut. R7/R8 de la porteuse sont DNP. Le faisceau GPIO conserve ses 13 contacts, avec les PWM et les capteurs de vitesse existants.'),
      p('J7 : 1 = OFF, 2 = GND vers le Pololu 2813. Les deux sorties Schmitt et DONE sont réunies par trois BAT54, cathodes côté OFF. Une remontée 47 kohms seule ne pilote pas correctement l’entrée OFF et son réseau interne 10 kohms.'),
      p('Le service d’arrêt et l’overlay gpio-poweroff restent à vérifier et tester sur Pi 5/OS choisi. Aucun logiciel n’est déployé. Ces GPIO donnent des états de seuil, pas des valeurs en volts, ampères, degrés ou pourcentage.','small'),PageBreak(),
      p('Schéma et routage de la porteuse','title'),
      picture(TMP/'routage.png',174,100),Spacer(1,4*mm),
      table([['Paramètre de conception','Valeur'],['PCB / fixation','140 x75 x1,6 mm ; quatre trous Ø3,2 : (4,4), (136,4), (4,71), (136,71)'],['Cuivre / règles','Deux couches ; alimentation0,40 / signaux0,20 mm ; isolement0,15 ; viasØ0,80 / trouØ0,40 ; cuivre70 micromètres nominal,55 minimum ; paroi20 minimum'],['Convertisseurs isolés','Zones sans pistes sous l’arrière des TMR ; seules les courtes sorties des broches occupent leur bord avant'],['Interface des modules','J3/J4 et J5 : connecteurs de faisceaux ; aucun contour TI nécessaire pour fabriquer la porteuse seule']],[52,122]),Spacer(1,3*mm),
      banner(f'<b>KiCad {q["kicad_version"]} : ERC 0 ; DRC 0 ; connexions manquantes 0 ; écarts schéma/PCB 0.</b> La netlist exportée est aussi comparée au tableau de connexions attendu. Aucun problème n’est masqué par des exclusions de conception.'),
      p('Livrés : projet .kicad_pro, schéma .kicad_sch, PCB .kicad_pcb, symboles et empreintes locales, CSV, netlist XML et vues SVG. Les schémas internes des modules restent dans leurs PDF constructeur. Ce routage fin à deux couches demande une fabrication adaptée ; aucune trajectoire CNC ou qualification de la machine n’est produite.'),
      p('Les contrôles ne vérifient pas le câblage extérieur, les reprises 0603 des EVM, l’échauffement, les marges électriques réelles ni le comportement du véhicule.','small'),PageBreak(),
      p('Modèles 3D et encombrement','title'),
      picture(B/'3D/ensemble-surveillance-2s-m1-gabarits.png',166,139),Spacer(1,3*mm),
      table([['Modèle','Nature et limites'],['Porteuse détaillée','Contour, trous, plages, fûts métallisés et pistes issus de la CAO KiCad contrôlée ; corps de composants reconstruits au nominal.'],['Ensemble avec réservations','Cadres bleus de 60 x 60 x 12 mm pour chaque EVM ; petit cadre pour Pololu 2831. Ils ne représentent PAS une géométrie fournisseur certifiée.'],['Trois AC03','Corps nominaux 13 x Ø4,8 mm, fils droits Ø0,8 / 25 mm, non coupés ; aucune longueur finale de faisceau imposée.']],[48,126]),
      p('Les STEP couleur sont réimportés et contrôlés. Les détails non cotés, inscriptions et couleurs sont signalés comme estimations. Les pistes de la porteuse suivent le routage réel ; aucune piste interne d’EVM n’est inventée.'),
      banner('Réserver <b>140 x75 x30 mm</b>, hors faisceaux, FAUX/support et résistances au pack. TI : pas2,54 mm spécifié ; contour environ51,05 x48,26 relevé dans le dessin, sans tolérance certifiée. Gerbers401 : cotes exactes encore ouvertes. EVM séparés sur supports isolants au banc.'),PageBreak(),
      p('Montage et qualification','title'),
      p('Commencer sur alimentations limitées, sans LiPo ni moteurs. Contrôler les résistances adaptées, les cavaliers, les polarités et les références locales. Tester une cellule à la fois en montée/descente, puis un pack déséquilibré. Mesurer les niveaux WARN, FAULT, OFF, les délais et les courants.'),
      table([['Essai','Résultat à établir au banc'],['Coupure autonome','Pi figé, Pi éteint, sous-tension d’une seule cellule ; contrôle du relais et du bouton de réarmement pendant un défaut maintenu.'],['Pannes des modules','Couper M5 puis chaque TMR et débrancher les optos ; vérifier que les voies HEALTHY s’éteignent et que OFF est réellement haut.'],['Pannes de câblage','Débrancher séparément B0/B1/B2, WARN, DONE et les alimentations ; documenter les cas non détectés.'],['Isolation et température','Absence de retour de puissance par équilibrage/GPIO ; échauffement des trois 100 ohms, FAUX et alimentations.'],['Essais Pi puis moteurs','Extinction avec vidéo/Wi-Fi actifs, reboot, parasites, accélération et freinage ; transitoires sur AUX et sur le 5 V MON.']],[43,131]),Spacer(1,4*mm),
      p('<b>Limites connues :</b> perte commune d’AUX, du LDO ou de D- sans garantie de demande OFF ; point milieu B1 ouvert pouvant produire une lecture trompeuse ; pas de mesure de courant ou de température, d’équilibrage ni de protection contre toutes les pannes. Cette carte n’est pas un arrêt d’urgence certifié.'),
      banner('<b>Stockage : débrancher la puissance ET l’équilibrage.</b> Chaque TMR consomme typiquement 40 mA à vide sous 5 V. Budget pack d’étude 0,7 W pour l’ensemble : environ 0,525 Wh en 45 min, soit 1,42 % des 37 Wh nominaux. Ce budget n’est pas une mesure.'),
      p('Ordre de conception conservé : carte de surveillance, support caméra arrière en hauteur, supports des capteurs, châssis, puis visserie finale. Les réservations actuelles servent à préparer cette implantation.','small'),PageBreak(),
      p('Achat, documents et traçabilité','title'),
      table([['Éléments','Prix / disponibilité au 15 octobre 2026'],['2 x TPS3700EVM-114','Prix France et stock à confirmer ; page TI à états de stock ambigus sans connexion.'],['2 x TMR 1-0511','RS : 9,28 EUR HT par pièce dans le catalogue consulté ; 18,56 HT / 22,27 TTC calculés à 20 %, hors port.'],['Pololu 2831','12,95 USD fabricant ; livraison France et stock immédiat non établis.'],['Autres pièces / PCB','Voir nomenclatures ; chiffrage incomplet, aucune somme globale TTC vérifiée.']],[55,119]),
      p('Aucune offre Amazon.fr exacte vérifiée pour les modules spécialisés ; aucun ASIN ou avis inventé. Aucun achat effectué. Les références fabricant et distributeur servent à constituer le panier, à revalider avant commande.'),
      source('TI : module, achat et documents','https://www.ti.com/tool/TPS3700EVM-114'),
      source('TI : guide EVM SLVU683A, schéma et routage d’origine','https://www.ti.com/lit/pdf/SLVU683'),
      source('TI : TPS3700 Rev G, seuils, biais et sorties','https://www.ti.com/lit/ds/symlink/tps3700.pdf'),
      source('TI E2E : calcul des résistances R1/R2/R3','https://e2e.ti.com/support/power-management-group/power-management/f/power-management-forum/1540899/tps3700evm-114-r1-r2-r3-value'),
      source('TRACO : TMR 1, fiche du 2 juillet 2026 et cotes','https://www.tracopower.com/tmr1-datasheet'),
      source('RS France : TMR 1-0511 / 781-3178','https://fr.rs-online.com/web/p/convertisseurs-dc-dc/7813178'),
      source('Pololu : régulateur auxiliaire D24V10F5 / 2831','https://www.pololu.com/product/2831'),
      source('Vishay : résistances AC03','https://www.vishay.com/docs/28730/ac_ac-at_ac-ni.pdf'),
      source('Vishay : optocoupleurs VOS618A','https://www.vishay.com/docs/83465/vos618a.pdf'),
      source('Littelfuse : fusibles lents 452/454, 500 mA','https://www.littelfuse.com/assetdocs/fuse-452-and-454-datasheet?assetguid=8c87aa93-80a7-4ea8-8749-a19ba03901c2'),
      p('Les notices originales téléchargées sont conservées sans modification et référencées par SHA256. Les échecs 401/403 sont conservés dans les registres assets. Aucun essai utilisateur ou YouTube de cet ensemble précis ne fonde la sélection ; les échanges TI sont des indications de conception, pas une validation du robot.','small')]
    doc=SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=18*mm,bottomMargin=23*mm,
       title='Drone V3 - Carte de surveillance électrique M1',author='Projet Drone V3')
    from reportlab.platypus import Table
    for flowable in story:
        if isinstance(flowable,Table):flowable.spaceAfter=3*mm
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    d=pymupdf.open(OUT);renders=[]
    for i,page in enumerate(d):
        path=TMP/f'page-{i+1}.png';page.get_pixmap(matrix=pymupdf.Matrix(1.35,1.35),alpha=False).save(path);renders.append(str(path.relative_to(ROOT)))
    (OUT.with_suffix('.json')).write_text(json.dumps(dict(pages=len(d),renders=renders,visual_review_completed=False,hardware_tested=False),indent=2),encoding='utf-8')
    assert len(d)==8,('Unexpected pagination',len(d))
    print('PDF pages',len(d),flush=True)
if __name__=='__main__':main()
