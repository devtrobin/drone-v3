"""Write the V3 cooling notice, then render every page for visual review."""
from pathlib import Path
import json,sys,hashlib
import pymupdf
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate,Paragraph,Table,TableStyle,Spacer,Image,PageBreak

ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/dissipateur-relais'
OUT=BASE/'notices/notice-dissipateur-relais-v3.pdf'
TMP=ROOT/'tools/temp/heatsink-review/pdf'
pdfmetrics.registerFont(TTFont('HV3','C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('HV3B','C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFontFamily('HV3',normal='HV3',bold='HV3B',italic='HV3',boldItalic='HV3B')
BLUE=colors.HexColor('#174969');GREY=colors.HexColor('#506273');LIGHT=colors.HexColor('#edf4f7')
ST={
 'body':ParagraphStyle('body',fontName='HV3',fontSize=9.3,leading=13,spaceAfter=7,textColor=colors.HexColor('#24313e')),
 'small':ParagraphStyle('small',fontName='HV3',fontSize=8,leading=11,spaceAfter=6,textColor=GREY),
 'title':ParagraphStyle('title',fontName='HV3B',fontSize=20,leading=25,spaceAfter=13,textColor=BLUE),
 'sub':ParagraphStyle('sub',fontName='HV3B',fontSize=12,leading=16,spaceAfter=8,spaceBefore=10,textColor=BLUE),
 'cell':ParagraphStyle('cell',fontName='HV3',fontSize=8.4,leading=11.5,textColor=colors.HexColor('#263643'))}
def p(s,style='body'):return Paragraph(s,ST[style])
def table(rows,widths):
    t=Table([[p(str(c),'cell') for c in row] for row in rows],colWidths=[x*mm for x in widths],hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),LIGHT),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LINEBELOW',(0,0),(-1,0),.7,colors.HexColor('#b7c9d3')),('LINEBELOW',(0,1),(-1,-1),.35,colors.HexColor('#dae4ea')),
        ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    return t
def banner(s):
    t=Table([[p(s)]],colWidths=[174*mm]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),LIGHT),
        ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),3)]));return t
def footer(c,d):
    c.saveState();c.setStrokeColor(colors.HexColor('#ccdbe4'));c.line(18*mm,17*mm,192*mm,17*mm)
    c.setFont('HV3',7.4);c.setFillColor(GREY);c.drawString(18*mm,12*mm,'Drone V3 | Refroidissement du relais | 13 octobre 2026 | Etude non testée')
    c.drawRightString(192*mm,12*mm,str(d.page));c.restoreState()
def source(label,url):return p(f'<b>{label}</b><br/><link href="{url}" color="#174969">{url}</link>','small')

def main():
    sys.stdout.reconfigure(encoding='utf-8');TMP.mkdir(parents=True,exist_ok=True)
    calc=json.loads((BASE/'calculs.json').read_text(encoding='utf-8'))
    cad=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'))
    fc=json.loads((BASE/'3D/validation-freecad.json').read_text(encoding='utf-8'));assert fc['all_passed']
    story=[p('Refroidissement du relais<br/>moteurs D1D100','title'),p('Sensata/Crydom HS251 + une interface HSP-1'),
        banner('<b>Choix d’étude, non acheté et non testé.</b> Enveloppe proposée : 40 A au total, air local à 40 °C au maximum, convection à qualifier. Offre Amazon.fr et prix français non confirmés.'),Spacer(1,5*mm),
        table([['Référence retenue','Donnée constructeur'],['HS251, dissipateur seul','Aluminium naturel ; 100 g ; 2,5 °C/W'],
            ['Fixation du relais','Deux #8-32 UNC ; entraxe nominal 47,6 mm ; kit HK1 associé'],
            ['Enveloppe complète CAO','85,3 × 52,3 × 40,6 mm, pattes incluses'],
            ['Corps dans le catalogue','58,7 × 50,3 × 38,4 mm : ne suffit pas pour réserver l’espace']],[52,122]),Spacer(1,4*mm),
        Image(str(BASE/'3D/sensata-hs251-officiel.png'),width=149*mm,height=121.06*mm),
        p('CAO officielle avec ailettes et pattes. STEP original conservé sans modification ; une copie positionnée sert à l’intégration V3. Les filetages sont représentés par les perçages du modèle constructeur.','small'),PageBreak()]
    rows=[['Courant total*','Pertes à 5 mΩ','Chute de tension','Tj estimée**']]
    for r in calc['rows']:rows.append([f"{r['current_A']} A",f"{r['loss_W']:.2f} W".replace('.',','),f"{r['voltage_drop_V']:.3f} V".replace('.',','),f"{r['estimated_junction_C']:.1f} °C".replace('.',',')])
    story += [p('Dimensionnement thermique','title'),p('Le relais porte le courant des deux ESC. Les 30 A annoncés par ESC sont leur capacité : ils ne donnent pas la consommation réelle du véhicule.'),
        table(rows,[39,45,45,45]),Spacer(1,4*mm),p('*Courant efficace traversant le relais. Pour des impulsions, utiliser le courant RMS de la somme instantanée des deux branches, et non le seul courant moyen.','small'),
        banner('<b>P ≈ 0,005 × (courant efficace)²</b><br/><b>Tj ≈ 40 + P × (2,5 + 0,2 + 0,27)</b><br/>**Modèle stationnaire simplifié. Les 0,2 °C/W d’interface sont une hypothèse, pas une garantie du pad. Les 0,27 °C/W jonction-semelle viennent du D1D100.'),
        p('Contrôle avec la courbe du fabricant','sub'),p('La fiche D1D100, page 4, donne environ 50 A à 40 °C avec un dissipateur de 3 °C/W. Cette lecture graphique aide à cadrer le choix de 2,5 °C/W ; elle ne remplace pas une qualification avec le pad et le montage réels.'),
        p('<b>60 A cumulés continus sont hors de l’enveloppe proposée.</b> Pour 100 A à 40 °C, la courbe constructeur indique 0,5 °C/W. Le HS251 ne permet pas de reprendre automatiquement le calibre 100 A inscrit sur le relais.'),
        table([['Alternative documentée','Comparaison'],['HS301, catalogue historique','3 °C/W ; 178 g ; aluminium noir ; ventilateur 40 mm possible'],
            ['HS501DR, catalogue historique','5 °C/W ; 52 g ; acier zingué, DIN ; trop limité pour l’objectif de 40 A'],
            ['Petit radiateur SSR générique','Pas d’offre précise avec taraudages et résistance thermique vérifiés']],[56,118]),Spacer(1,4*mm),
        p('Rds, confinement, température ambiante, orientation et contact thermique font varier le résultat. À 30 A constants pendant 45 minutes, les pertes seraient 3,375 Wh ; ce scénario n’établit pas l’autonomie du robot. Mesures sous charge nécessaires.','small'),PageBreak()]
    story += [p('Interface et montage','title'),p('Monter <b>une seule interface HSP-1</b>. Les deux modèles de pad sont des variantes de lot, jamais deux couches à empiler.'),
        table([['Variante','Documentation et limites'],['Gris, fiche 2018','0,076 mm ; contour 57,1 × 44,2 mm ; encoches 47,5 mm / ouverture 4,83 mm'],
            ['Rose, PCN 2023','JRFT-FC200 ; deux films à retirer ; 0,127 mm dans l’annexe préliminaire consultée sur TTI. Contour 2018 supposé dans la CAO, lot à contrôler'],
            ['Plan historique 2011','Cotes différentes : 57,2 × 44,5 mm ; entraxe d’encoches 47,8 mm. Pas mélangées au modèle 2018']],[43,131]),Spacer(1,4*mm),
        p('Préparer des surfaces propres et planes. Retirer les films du pad rose selon la notice du lot, chasser doucement les bulles et ne pas ajouter de pâte au pad. Le PCN décrit 5 minutes d’attente ; l’annexe préliminaire évoque une heure selon la pose. Cet écart doit être tranché avec la procédure du lot reçu.'),
        p('Mettre les deux vis #8-32 UNC en contact, puis serrer progressivement et alternativement à <b>2,2 N·m</b>. Vérifier le kit livré et la longueur des vis ; ne pas remplacer automatiquement par des M4. Le serrage des bornes électriques suit la notice distincte du D1D100.'),
        Image(str(BASE/'3D/assemblage-d1d100-hs251-hsp1-etude.png'),width=139*mm,height=112.94*mm),
        p('Assemblage CAO : dissipateur officiel + pad rose d’étude + reconstruction extérieure du relais. Vis de montage, faisceau et fixations au châssis absents. Aucun chevauchement volumique détecté entre ces trois pièces.','small'),
        p('<b>Ailettes et canaux verticaux recommandés</b> pour la convection naturelle. La pose montrée sert de repère CAO et ne valide pas une implantation enfermée. Aucun refroidissement lié à la vitesse du robot n’est supposé.','small'),PageBreak()]
    story += [p('Contrôles et traçabilité','title'),p('Les cinq STEP ont été réimportés et vérifiés par FreeCAD en mode sans interface : géométrie valide, solides fermés, nombre de solides et enveloppe contrôlés. Cela ne constitue pas un essai dans l’interface FreeCAD ou l’extension CAD View de VSCode.'),
        table([['Fichier / nature','Solides / faces'],*[[m['file'],f"{m['validation']['solids']} / {m['validation']['faces']}"] for m in cad['models']]],[136,38]),Spacer(1,4*mm),
        p('Avant de finaliser le montage','sub'),p('Mesurer courant efficace et pointes, chute de tension du relais, températures de semelle et d’air local sur l’usage prévu. Vérifier la stabilité sur longue durée et la marge à l’ambiante maximale. La température du radiateur ne mesure pas directement la jonction. Aucun essai matériel n’a encore été réalisé.'),
        p('Recherche d’achat et avis','sub'),p('Amazon.fr inaccessible pendant la recherche ; aucune offre exacte, ASIN ou prix TTC français validé. Un seul avis eBay du 9 mai 2025 rapporte un bon ajustement sur un D06D100, autre référence : aucune preuve thermique pour notre montage. Aucun essai pertinent de cet ensemble trouvé sur forums ou YouTube.'),
        p('Sources et documents conservés','sub'),
        source('Sensata HS251 : fiche, plan et STEP','https://www.sensata.com/products/relays/hs-series-heat-sinks-hs251'),
        source('Fiche HS251 2024, original via Farnell','https://www.farnell.com/datasheets/4619827.pdf'),
        source('Guide HS 2024, original via RS','https://docs.rs-online.com/766e/A700000009477596.pdf'),
        source('HSP 2018, original via Farnell','https://www.farnell.com/datasheets/4600889.pdf'),
        source('PCN 2023, original via Farnell','https://www.farnell.com/datasheets/4129384.pdf'),
        source('Avis utilisateur consulté, autre relais','https://www.ebay.com/p/1210661465'),
        p('Le dossier notices conserve six PDF fabricant inchangés, dont la fiche HSP 2018 et son plan 2011. La copie PCN locale contient quatre pages ; l’annexe préliminaire TTI a été consultée en ligne mais non téléchargée. Les URL, SHA256, limites et refus de téléchargement sont consignés dans assets.json, sources.json, recherche-technique.md et les JSON voisins des STEP.','small')]
    doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=18*mm,bottomMargin=23*mm,
        title='Drone V3 - Refroidissement D1D100 par HS251',author='Projet Drone V3')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    pdf=pymupdf.open(OUT);assert len(pdf)==4,len(pdf)
    pages=[]
    for i,page in enumerate(pdf):
        png=TMP/f'page-{i+1}.png';page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(png)
        pages.append(dict(page=i+1,render=str(png.relative_to(ROOT)),chars=len(page.get_text())))
    (OUT.with_suffix('.json')).write_text(json.dumps(dict(file=OUT.name,pages=len(pdf),sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),
        generator='tools/build_heatsink_pdf.py',generated_on='2026-10-13',renders=pages,visual_review_complete=False),indent=2)+'\n',encoding='utf-8')
    print('PDF',len(pdf),'pages',OUT.stat().st_size,'bytes',flush=True)
if __name__=='__main__':main()
