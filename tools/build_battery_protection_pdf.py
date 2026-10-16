"""Create one clearly identified preliminary project notice and render all pages."""
from pathlib import Path
import json,hashlib,sys,math
import pymupdf
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image
from reportlab.graphics.shapes import Drawing,Rect,String,PolyLine,Polygon

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'Composants/protection-batterie'
OUT=BASE/'notices/notice-protection-batterie-v3.pdf'
TEMP=ROOT/'tools/temp/protection-review/pdf';TEMP.mkdir(parents=True,exist_ok=True)
pdfmetrics.registerFont(TTFont('ArialV3','C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialV3Bold','C:/Windows/Fonts/arialbd.ttf'))
BLUE=colors.HexColor('#174969');GREY=colors.HexColor('#506273');LIGHT=colors.HexColor('#eef4f7')
styles={
 'body':ParagraphStyle('body',fontName='ArialV3',fontSize=9.4,leading=13.2,spaceAfter=7,textColor=colors.HexColor('#24313e')),
 'small':ParagraphStyle('small',fontName='ArialV3',fontSize=8,leading=11,spaceAfter=5,textColor=GREY),
 'h1':ParagraphStyle('h1',fontName='ArialV3Bold',fontSize=20,leading=25,spaceAfter=14,textColor=BLUE),
 'h2':ParagraphStyle('h2',fontName='ArialV3Bold',fontSize=12,leading=16,spaceBefore=9,spaceAfter=7,textColor=BLUE),
 'table':ParagraphStyle('table',fontName='ArialV3',fontSize=8.3,leading=11,textColor=colors.HexColor('#263643')),
}

def p(text,style='body'):return Paragraph(text,styles[style])
def table(rows,widths):
    data=[[p(str(cell),'table') for cell in row] for row in rows]
    t=Table(data,colWidths=[w*mm for w in widths],hAlign='LEFT',repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),LIGHT),('VALIGN',(0,0),(-1,-1),'TOP'),
      ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
      ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
      ('LINEBELOW',(0,0),(-1,0),.6,BLUE),('LINEBELOW',(0,1),(-1,-1),.25,colors.HexColor('#d5e0e6'))]))
    return t

def banner(text):
    t=Table([[p(text)]],colWidths=[174*mm]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),LIGHT),('BOX',(0,0),(-1,-1),.7,BLUE),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),3)]));return t

def diagram():
    d=Drawing(490,228)
    def node(x,y,w,h,lines):
        d.add(Rect(x,y,w,h,rx=5,ry=5,fillColor=LIGHT,strokeColor=BLUE,strokeWidth=.8))
        for n,line in enumerate(lines):d.add(String(x+w/2,y+h/2+(len(lines)-1)*6-n*12,line,fontName='ArialV3',fontSize=8.5,textAnchor='middle',fillColor=BLUE))
    def arrow(points,col=BLUE):
        d.add(PolyLine([z for pt in points for z in pt],strokeColor=col,strokeWidth=1.5))
        (x0,y0),(x,y)=points[-2:];a=math.atan2(y-y0,x-x0)
        left=(x-5*math.cos(a)+2.6*math.sin(a),y-5*math.sin(a)-2.6*math.cos(a))
        right=(x-5*math.cos(a)-2.6*math.sin(a),y-5*math.sin(a)+2.6*math.cos(a))
        d.add(Polygon([x,y,*left,*right],fillColor=col,strokeColor=col))
    node(2,96,74,52,['Batterie 2S','distribution','protégée à définir'])
    node(110,96,116,52,['Pololu 2813 HP','VOUT = VSW'])
    node(261,96,108,52,['D24V90F5','5 V vers le Pi'])
    node(402,96,86,52,['Pi 5','caméra / Wi-Fi'])
    node(111,11,125,50,['D1D100','coupure moteurs'])
    node(355,11,132,50,['Deux ESC','moteurs / BEC servo'])
    node(111,178,162,46,['Surveillance cellule 1 et 2','avertissement + seuil bas'])
    arrow([(76,122),(110,122)])
    arrow([(226,122),(261,122)])
    arrow([(369,122),(402,122)])
    arrow([(40,96),(40,36),(111,36)])
    arrow([(236,36),(355,36)])
    arrow([(40,148),(40,201),(111,201)],colors.HexColor('#287946'))
    arrow([(167,178),(167,148)],colors.HexColor('#915879'))
    d.add(String(173,163,'OFF',fontName='ArialV3',fontSize=8,fillColor=GREY))
    arrow([(273,201),(445,201),(445,148)],colors.HexColor('#915879'))
    d.add(String(305,207,'WARN1 / WARN2',fontName='ArialV3',fontSize=8,fillColor=GREY))
    arrow([(225,106),(247,106),(247,79),(174,79),(174,61)],colors.HexColor('#915879'))
    d.add(String(257,76,'VSW vers +3 ; 4 à B0',fontName='ArialV3',fontSize=8,fillColor=GREY))
    d.add(String(269,42,'+2 batterie / 1 ESC',fontName='ArialV3',fontSize=7.6,fillColor=GREY))
    return d

def footer(canvas,doc):
    canvas.saveState();canvas.setStrokeColor(colors.HexColor('#cfdae2'));canvas.line(18*mm,17*mm,192*mm,17*mm)
    canvas.setFont('ArialV3',7.5);canvas.setFillColor(GREY)
    canvas.drawString(18*mm,12*mm,'Drone V3 | Etude de protection 2S | 13 octobre 2026 | Non testée')
    canvas.drawRightString(192*mm,12*mm,str(doc.page));canvas.restoreState()

def main():
    sys.stdout.reconfigure(encoding='utf-8');OUT.parent.mkdir(parents=True,exist_ok=True)
    cal=json.loads((BASE/'calculs.json').read_text(encoding='utf-8'));warn=cal['warning'];hard=cal['hard_cut']
    story=[]
    story += [p('Surveillance et coupure<br/>de la batterie 2S','h1'),p('Notice de projet - proposition matérielle et modèles 3D','h2'),
      banner('<b>Etude préliminaire, non fabriquée et non testée.</b> La solution combine une carte analogique V3 à fabriquer, un interrupteur Pololu et un relais statique DC. Aucun module Amazon unique satisfaisant toutes les fonctions n’a été vérifié.'),Spacer(1,10*mm),
      table([['Partie','Référence / statut'],['Surveillance par cellule','Carte V3 : 2 TLV6700, 4 VOS618A-8T, logique et alimentation auxiliaire'],['Branche Pi','Pololu 2813 HP - CAO officielle commune MP / HP'],['Puissance moteurs','Sensata/Crydom D1D100, version à vis - reconstruction extérieure']],[49,125]),Spacer(1,6*mm),
      p('La surveillance doit avertir le Pi avant une décharge excessive, puis demander une coupure indépendante si une cellule continue de baisser. Le Pi reste le seul ordinateur de commande ; la carte analogique n’ajoute pas de microcontrôleur.'),
      Image(str(BASE/'3D/apercu-protection.png'),width=174*mm,height=104.4*mm),
      p('Trois échelles distinctes. Les pistes de la carte V3 sont illustratives : cette CAO ne constitue pas un PCB prêt à fabriquer. Les modèles détaillés se trouvent dans les sous-dossiers 3D.','small'),PageBreak()]
    story += [p('1. Architecture proposée','h1'),diagram(),Spacer(1,5*mm),
      p('Le relais D1D100 porte le courant des deux ESC. Le Pololu 2813 porte seulement l’entrée du régulateur Pi et le faible courant de commande du relais. Il ne faut pas envoyer le courant des moteurs dans la petite carte Pololu.'),
      p('Deux voies de puissance commandées ensemble','h2'),
      p('Quand le Pololu coupe VSW, le régulateur du Pi perd son alimentation et l’entrée du relais moteur devient inactive. La surveillance reste alimentée côté batterie pour maintenir sa demande d’arrêt. La distribution, les protections contre les transitoires et les chemins de régénération restent à qualifier.'),
      table([['Repère','Raccordement de principe'],['D1D100 +2','Positif batterie après protection de branche'],['D1D100 1','Positif commun aux deux ESC'],['D1D100 +3 / 4','Commande : VSW / B0 ; aucune GPIO 3,3 V directement'],['Pololu VIN / VOUT','Batterie protégée / VSW vers D24V90F5 et commande SSR'],['B0 / B1 / B2','Négatif / point milieu / positif : mesure à faible courant']],[47,127]),
      p('La polarité du SSR est celle du schéma constructeur, page PDF 3. Son entrée demande au moins 3,5 V : la sortie batterie commutée est employée ici. Le relais n’est pas un contact mécanique réversible. Ne pas remplacer cette référence DC par un SSR à sortie AC.'),PageBreak()]
    story += [p('2. Mesure par cellule et seuils','h1'),
      p('Le circuit de cellule 1 utilise B1 comme alimentation positive et B0 comme référence. Le circuit de cellule 2 utilise B2 et B1. Leurs signaux rejoignent la logique par optocoupleurs ; le retour local B1 de la cellule 2 ne doit pas être relié au GND du Pi.'),
      table([['Voie','Pont 0,1 %','Descente typique','Bornes calculées'],['Avertissement INA+ / OUTA','80,4 kΩ / 10 kΩ',f'{warn["falling_typical_V"]:.3f} V',f'{warn["falling_corner_min_V"]:.3f} à {warn["falling_corner_max_V"]:.3f} V'],['Coupure INB- / OUTB','75,0 kΩ / 10 kΩ',f'{hard["falling_typical_V"]:.3f} V',f'{hard["falling_corner_min_V"]:.3f} à {hard["falling_corner_max_V"]:.3f} V']],[46,46,37,45]),Spacer(1,4*mm),
      p('Seuil = VIT- × (1 + Rhaut / Rbas) + Ibiais × Rhaut. La valeur typique VIT- est 394,5 mV ; elle inclut l’hystérésis. Les bornes utilisent 387 à 400 mV sur la plage de température constructeur, les résistances à ±0,1 % et un biais conservateur de ±25 nA. Ce sont des calculs de composants, pas des mesures de la carte.'),
      p('Séparation des deux fonctions','h2'),
      p('Sous le premier seuil, OUTA devient bas et active l’opto WARN. Au-dessus du seuil bas, OUTB reste bas et maintient l’opto HEALTHY actif. Si la cellule descend sous ce seuil, HEALTHY se désactive : son collecteur remonte, le tampon logique commande OFF. Chaque cellule a sa propre voie de défaut.'),
      p('La borne basse calculée du seuil de coupure reste supérieure au minimum de 3,2 V publié pour le pack Zeee. Les creux rapides, l’erreur de montage et les délais physiques ne sont pas couverts par cette comparaison : ils doivent être mesurés.'),
      p('Filtrage et consommation','h2'),
      p('Prévoir 100 nF près de chaque TLV et sur chaque entrée de mesure. La constante de temps des ponts filtrés est voisine de 0,9 ms. Les optocoupleurs proposés utilisent des résistances LED de 1,5 kΩ ; vérifier le courant, le CTR du bin -8T et la saturation à la température d’usage. La carte et ses optos continuent de consommer après la coupure : débrancher le pack et son équilibrage au stockage.'),PageBreak()]
    story += [p('3. Interface Pi et arrêt','h1'),
      table([['Fonction','GPIO BCM','Broche physique','Etat proposé'],['Cellule 1 faible','17','11','WARN1 bas'],['Cellule 2 faible','27','13','WARN2 bas'],['Fin d’arrêt système','22','15','Haut vers OFF, via diode'],['Référence','GND','6 ou 9','Masse système']],[59,30,35,50]),Spacer(1,4*mm),
      p('Les sorties d’opto WARN sont ramenées au 3,3 V du Pi par 47 kΩ. La logique de coupure possède son propre 3,3 V permanent, fourni par le MCP1703A depuis la batterie. Cette alimentation auxiliaire ne fournit pas le Pi.'),
      p('Commande OFF, sans relier les sorties ensemble','h2'),
      p('Chaque HEALTHY remonte à la source auxiliaire par 47 kΩ. Un SN74LVC2G17 fournit deux sorties à faible impédance, nécessaires pour attaquer le réseau d’entrée du Pololu. Deux BAT54 réunissent ces défauts vers OFF ; une troisième apporte la commande finale du Pi. Les cathodes sont côté OFF. Une remontée de 47 kΩ seule ne garantit pas le courant exigé par l’entrée OFF.'),
      p('Déroulement prévu','h2'),
      p('1. Au démarrage, garder les moteurs non armés jusqu’aux contrôles et à la commande neutre.<br/>2. Sur WARN, interdire l’accélération, arrêter les moteurs selon le freinage vérifié, fermer les enregistrements puis demander l’arrêt du Pi.<br/>3. Au terme de l’arrêt système, une GPIO de poweroff déclenche OFF.<br/>4. Si la cellule atteint le seuil bas avant la fin, le circuit analogique demande la coupure immédiatement, même si Linux ne répond plus.'),
      banner('La fenêtre de tension ne garantit pas un délai fixe d’extinction. En cas de décharge rapide ou de défaut, la coupure peut précéder la fin de l’arrêt Linux.'),Spacer(1,4*mm),
      p('Piste logicielle : dtoverlay=gpio-poweroff,gpiopin=22, sortie active haute. Ce n’est pas une configuration appliquée. Vérifier son fonctionnement sur Pi 5 et l’OS reçu, y compris reboot, watchdog et bouton. Le README officiel indique que cet overlay modifie la séquence normale de mise hors tension. Le service de surveillance WARN reste à développer.','small'),PageBreak()]
    story += [p('4. Pièces, chaleur et CAO','h1'),
      table([['Pièce','Informations utiles'],['TLV6700DDCR ×2','SOT-23-6 ; boîtier nominal 2,9 × 1,6 mm ; sorties à drain ouvert'],['VOS618A-8T ×4','Optocoupleurs faibles courants ; deux fonctions par cellule'],['SN74LVC2G17DCKR ×1','Tampon logique double ; alimentation auxiliaire 3,3 V'],['MCP1703AT-3302E/MB ×1','SOT-89 ; LDO auxiliaire ; capacités et disposition selon fiche Microchip'],['Pololu 2813 HP ×1','PCB nominal 20,3 × 25,4 mm ; modèle constructeur inchangé'],['Crydom D1D100 ×1','57,3 × 44,5 × 22,6 mm ; masse typique 75,5 g ; dissipateur à définir']],[64,110]),Spacer(1,4*mm),
      p('Le nombre 100 A ne signifie pas un fonctionnement sans refroidissement. Le constructeur donne les courbes de déclassement et demande 0,5 °C/W pour le courant nominal à 40 °C. Pour Rds = 5 mΩ, les pertes de conduction estimées sont :'),
      table([['Courant moteurs total','Chute estimée','Chaleur estimée'],*[ [str(x['current_A'])+' A',f'{x["drop_V"]:.2f} V',f'{x["power_W"]:.1f} W'] for x in cal['ssr_losses_W']]],[68,53,53]),Spacer(1,4*mm),
      p('Ces calculs n’incluent ni les bornes, ni les fils, ni l’évolution thermique de la résistance. Un dissipateur adapté au courant réel et à l’air disponible doit être choisi. Les courants nominaux des ESC ne sont pas une mesure de consommation.'),
      p('Les trois STEP sont en millimètres, avec des couleurs et des solides nommés. La surveillance est un concept de PCB 54 × 32 × 1,6 mm ; le Pololu est une CAO native partagée MP/HP ; le Crydom est reconstruit depuis son plan extérieur. Marquages, moulage, connecteurs et certains boîtiers sont approchés. Aucun volume CAO mixte ne sert à calculer la masse physique.','small'),PageBreak()]
    story += [p('5. Qualification et achats','h1'),
      p('Avant un PCB ou un câblage','h2'),
      p('Produire un schéma électrique détaillé, vérifier les broches exactes, les domaines locaux de cellule, les niveaux logiques et le réseau OFF. Réaliser ERC/DRC et routage. Le STEP et ses pistes illustratives ne remplacent pas un Gerber ou un plan CNC. La compatibilité théorique des fiches ne vaut pas qualification du montage.'),
      p('Essais nécessaires','h2'),
      p('Avec deux cellules simulées et une alimentation limitée : mesurer les seuils en montée/descente ; provoquer un déséquilibre ; vérifier déconnexion des fils de mesure, maintien du défaut, réarmement manuel, bruit, retour d’alimentation et consommation de chaque cellule. Mesurer l’arrêt Pi avec caméra active et service bloqué. Tester le relais à des courants représentatifs en mesurant chute de tension et température, puis vérifier les transitoires lors du freinage et de la coupure.'),
      p('Retours d’expérience disponibles','h2'),
      p('Un utilisateur Pololu rapporte en 2021 une extinction réussie après correction de la polarité gpio-poweroff, sur un interrupteur Mini et un ancien Pi. Un autre signale en 2017 un allumage inattendu du 2813 lors de fluctuations en automobile. Ces témoignages orientent les essais ; aucun ne valide notre montage Pi 5 / 2S. Il n’existe pas d’avis d’utilisateur pour notre carte non fabriquée.'),
      banner('Achat Amazon non confirmé : aucun ASIN fiable, prix euro, vendeur ou stock n’est annoncé pour cet ensemble. Les recherches par référence et les sources alternatives sont dans recherche-technique.md. La référence Crydom industrielle et son refroidissement peuvent être coûteux ; le budget complet reste à chiffrer.'),Spacer(1,5*mm),
      p('Ce circuit vise la gestion de décharge et l’arrêt de fonctionnement. Il ne constitue pas un arrêt d’urgence certifié. Le fabricant Pololu déconseille cet usage pour sa carte. La coupure n’isole pas tous les chemins possibles ; le stockage demande de débrancher la batterie et la prise de mesure.','small'),PageBreak()]
    story += [p('6. Sources et fichiers','h1'),
      p('Les fiches constructeur originales sont conservées sans modification. Les manifests assets.json indiquent URL, taille et SHA256. Le PDF Sensata a été récupéré chez Farnell après le refus 403 du téléchargement direct ; il conserve le contenu constructeur.'),
      table([['Document / référence','Pages ou rôle'],['TI TLV6700, révision B','PDF 3 : broches ; PDF 5 : seuils, biais, hystérésis ; implantation et boîtiers'],['Vishay VOS618A, document 83465','PDF 1 : variantes CTR ; PDF 3 : saturation ; PDF 7 : package'],['Microchip MCP1703A, DS20005122','Alimentation auxiliaire, capacités, brochage et boîtiers'],['TI SN74LVC2G17','Niveaux d’entrée et de sortie du tampon logique ; package DCK'],['Diodes BAT54, DS11005','Diode simple BAT54-7-F ; polarité, chute et package'],['Pololu 2813','Page produit, schéma blocs, plan coté et STEP constructeur commun 2812/2813'],['Sensata/Crydom 1-DC, document 2020','PDF 1-2 : électrique ; PDF 3 : polarité, cotes ; PDF 4 : courbes thermiques'],['Raspberry Pi firmware / overlays','README original : gpio-poweroff et effets sur arrêt/redémarrage']],[82,92]),Spacer(1,5*mm),
      p('Liens primaires','h2'),
      p('<link href="https://www.ti.com/product/TLV6700" color="#174969">TI - TLV6700</link> | <link href="https://www.vishay.com/en/product/83465/" color="#174969">Vishay - VOS618A</link> | <link href="https://www.microchip.com/en-us/product/MCP1703A" color="#174969">Microchip - MCP1703A</link><br/><link href="https://www.pololu.com/product/2813" color="#174969">Pololu - 2813 HP</link> | <link href="https://www.sensata.com/sites/default/files/a/sensata-1-dc-series-d1d-dc-output-panel-mount-datasheet.pdf" color="#174969">Sensata - fiche 1-DC</link><br/><link href="https://raw.githubusercontent.com/raspberrypi/firmware/master/boot/overlays/README" color="#174969">Raspberry Pi - documentation des overlays</link>'),
      p('Fichiers voisins utiles','h2'),
      p('README.md : index et statut.<br/>integration.md : architecture détaillée et séquence.<br/>recherche-technique.md : alternatives, avis et recherches Amazon.<br/>calculs.json : seuils, coins de tolérance et pertes.<br/>nomenclature.json : liste provisoire, éléments restant à sélectionner.<br/>3D/catalogue.json : modèles et empreintes SHA256.<br/>3D/validation-freecad.json : résultat d’import géométrique, distinct de tout essai électrique.'),
      p('Cette notice est un document du projet Drone V3. Elle ne modifie aucune fiche constructeur et n’affirme ni fabrication prête, ni disponibilité Amazon, ni autonomie mesurée.','small')]
    doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=18*mm,bottomMargin=23*mm,
        title='Drone V3 - Surveillance et coupure batterie 2S - Etude preliminaire',author='Projet Drone V3')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    d=pymupdf.open(OUT);assert len(d)==7,('Unexpected page flow',len(d))
    for i,page in enumerate(d):
        assert len(page.get_text().strip())>100
        page.get_pixmap(matrix=pymupdf.Matrix(1.3,1.3)).save(str(TEMP/f'notice-p{i+1:02d}.png'))
    (OUT.with_suffix('.json')).write_text(json.dumps(dict(file=OUT.name,sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),pages=len(d),
        created_on='2026-10-13',is_project_notice=True,hardware_tested=False,rendered_pages=len(d),visual_review_complete=False,
        source_index='../README.md',generator='tools/build_battery_protection_pdf.py'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PDF',len(d),'pages, rendered:',OUT,flush=True)

if __name__=='__main__':main()
