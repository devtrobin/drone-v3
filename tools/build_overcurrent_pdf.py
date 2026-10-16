"""Create and render one project notice; manufacturer's PDFs remain untouched."""
from pathlib import Path
import sys,json,hashlib
import pymupdf
from build_heatsink_pdf import p,table,banner,footer as unused,source,GREY
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate,Spacer,Image,PageBreak
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/protection-surintensite'
OUT=BASE/'notices/notice-fusible-principal-v3.pdf';TMP=ROOT/'tools/temp/overcurrent-review/pdf'
def footer(c,d):
    c.saveState();c.setStrokeColor(colors.HexColor('#ccdbe4'));c.line(18*mm,17*mm,192*mm,17*mm)
    c.setFont('HV3',7.4);c.setFillColor(GREY);c.drawString(18*mm,12*mm,'Drone V3 | Fusible principal MIDI | 14 octobre 2026 | Etude non testée')
    c.drawRightString(192*mm,12*mm,str(d.page));c.restoreState()
def main():
    sys.stdout.reconfigure(encoding='utf-8');TMP.mkdir(parents=True,exist_ok=True)
    cal=json.loads((BASE/'calculs.json').read_text(encoding='utf-8'))
    cad=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'))
    fc=json.loads((BASE/'3D/validation-freecad.json').read_text(encoding='utf-8'));assert fc['all_passed']
    story=[p('Fusible principal<br/>et porte-fusible MIDI','title'),p('Protection du faisceau - batterie LiPo 2S - sélection et CAO V3'),
        banner('<b>Choix d’étude, non acheté et non testé.</b> Support Littelfuse 04980900ZXT + fusible 0498060.M de 60 A. Calibre, fils et coordination à valider avant mise en service. Offre Amazon française non confirmée.'),Spacer(1,5*mm),
        table([['Composant','Référence et caractéristique'],['Porte-fusible','04980900ZXT ; socle et capot, goujons M5, écrous et rondelles ; fusible/câbles non compris'],
            ['Fusible principal','0498060.M ; MIDI temporisé, 60 A / 32 V DC ; deux trous pour M5'],
            ['Compatibilité de tension','Pack 2S, 8,4 V maximum ; ensemble limité par le fusible 32 V DC'],
            ['Fonction recherchée','Protection des conducteurs de puissance près de la batterie']],[45,129]),Spacer(1,5*mm),
        Image(str(BASE/'porte-fusible/3D/ensemble-midi-60a-ferme-etude.png'),width=149*mm,height=121.06*mm),
        p('Ensemble fermé reconstruit. Le fusible est dans le capot ; pas de cosses ou fils ajoutés. Cotes publiées complétées par des détails estimés. Ce fichier n’est pas une CAO constructeur.','small'),PageBreak()]
    story += [p('Choix du calibre : 60 A d’étude','title'),
        table([['Hypothèse','Valeur retenue pour le calcul'],['Moteurs, courant continu total','40 A : enveloppe thermique proposée, pas une mesure ni une limite imposée'],
            ['Pi + caméra au 5 V','25 W supposés ; régulateur à 90 % de rendement supposé'],['Batterie / auxiliaires','6,4 V pour le calcul ; réserve auxiliaire de 0,05 A supposée']],[56,118]),Spacer(1,4*mm),
        banner('<b>I principal = 40 + 25 / (6,4 × 0,90) + 0,05 = 44,39 A</b><br/>Les capacités de 30 A des ESC ne déterminent pas seules ce courant.'),
        p('Comparaison du déclassement typique constructeur','sub'),
        table([['Calibre','À 20 °C','À 65 °C','Lecture pour le scénario'],['40 A','38 A','32 A','Inférieur aux 44,39 A calculés'],
            ['50 A','50 A','45 A','Très peu de marge à 65 °C'],['60 A','58 A','48 A','Retenu pour l’étude ; essais et courant de défaut encore nécessaires']],[28,26,26,94]),Spacer(1,4*mm),
        p('Ces valeurs viennent de la révision REV07272021, avec les connexions et sections d’essai fabricant. Elles peuvent changer avec le montage. À 85 °C, le 60 A tombe à 43 A dans ce tableau : notre scénario ne rentre plus.'),
        p('Fils et petites branches','sub'),p('Tronc principal proposé : <b>cuivre 6 mm²</b>, sous réserve du type de fil, de la pose et des températures. Cette section est aussi celle de l’essai fabricant du fusible ; elle n’est pas une garantie universelle d’intensité admissible.'),
        p('Les fils du pack, les connecteurs XT60 et les câbles des ESC restent à vérifier. Le fusible principal de 60 A ne protège pas à lui seul les départs plus fins, notamment la branche Pi : protections de départ à sélectionner.'),
        p('Pertes à froid, hors contacts et fils','sub'),
        table([['Courant','Pertes à 0,87 mΩ','Chute calculée'],['40 A','1,39 W','34,8 mV'],['44,39 A','1,71 W','38,6 mV']],[44,66,64]),Spacer(1,3*mm),
        p('La résistance 0,87 mΩ est typique à froid. La chute fabricant de 68 mV correspond à ses conditions d’essai ; l’échauffement et les contacts changent les pertes.','small'),PageBreak()]
    story += [p('Cotes et montage mécanique','title'),
        table([['Pièce / interface','Cote publiée utilisée'],['Support, longueur × largeur × hauteur','51,4 × 27,3 × 24,9 mm ; hors lanière et câbles'],
            ['Fixation du socle','Deux Ø3,81 ; positions diagonales sur rectangle 41 × 15,2 mm'],
            ['Goujons électriques','M5 × 0,8 ; entraxe fonctionnel 30 mm'],['Fusible 60 A','41 × 12 × 8,0 mm ; centre 16 mm ; lames 0,41 mm'],
            ['Trous du fusible M5','Deux Ø5,5 ; entraxe 30 mm']],[69,105]),Spacer(1,3*mm),
        p('Le plan distingue largeur et hauteur du support. La hauteur 8,3 mm du fusible indiquée par certains vendeurs concerne les calibres supérieurs du plan : pour 60 A, le modèle suit 8,0 mm.'),
        Image(str(BASE/'porte-fusible/3D/ensemble-midi-60a-vue-eclatee.png'),width=128*mm,height=104*mm),
        p('Vue éclatée : capot décalé de 25 mm, lanière omise ; ce n’est pas une simulation de son articulation. Les visseries, poches, clips, lanière et rayons non cotés sont estimés.','small'),
        p('Fixer le socle près du positif batterie. Batterie débranchée, monter des cosses à oeillet M5 adaptées aux fils et au sertissage. L’ordre d’empilage doit suivre les pièces reçues : la CAO sans cosses n’est pas une instruction de câblage.'),
        p('Couple d’étude : <b>4,5 N·m</b>, dans la plage commune du support 4-5 N·m et du fusible M5 4,5 ±1 N·m. Les fixations au châssis sont distinctes. Replacer le capot et retenir les câbles sans traction sur les goujons.','small'),PageBreak()]
    story += [p('Courbes, défauts et limites','title'),p('<b>60 A ne signifie pas une coupure immédiate à 60 A.</b> La temporisation supporte des pointes ; le tableau fabricant indique les fenêtres suivantes, pour cette famille 30-125 A :'),
        table([['Courant / calibre','Courant pour 60 A','Temps d’ouverture publié'],['110 %','66 A','Au moins 14 400 s, sans maximum indiqué'],
            ['150 %','90 A','90 à 3 600 s'],['200 %','120 A','3 à 100 s'],['300 %','180 A','0,3 à 3 s'],['500 %','300 A','0,1 à 1 s']],[43,54,77]),Spacer(1,4*mm),
        banner('<b>Le fusible n’impose pas la limite thermique moteurs de 40 A.</b> Il ne garantit pas la protection rapide du relais ou des ESC. Courant, transitoires et protections de branches restent à coordonner.'),
        p('Pouvoir de coupure et révisions','sub'),p('Révision 2021 et fiche 2024 : <b>2 000 A à 32 V DC</b>. Ancienne fiche TME : <b>1 000 A</b>. Le lot et la fiche applicable doivent être vérifiés. Le « 80C » commercial du pack ne mesure pas son courant de court-circuit.'),
        p('Repère ohmique : 8,4 V / 2 000 A = <b>4,2 mΩ</b> pour la boucle totale. Ce calcul ne valide pas le courant prospectif réel. Utiliser les données d’impédance de batterie et de boucle, sans court-circuit volontaire, puis vérifier le pouvoir de coupure adapté.'),
        p('L’I²t typique de 21 700 A²s décrit la fusion dans les essais, avant l’arc. Ce n’est pas une garantie d’énergie de coupure totale ni de protection du SSR. La coordination doit considérer fils, semi-conducteurs, contacts et défauts possibles.'),
        p('Essais avant mise en service','sub'),p('Mesurer courant principal et pointes d’accélération, chutes de tension, température des contacts et du fusible dans l’implantation réelle. Reproduire l’usage long prévu. Revoir la sélection si les marges sont insuffisantes ; ne pas augmenter le calibre pour masquer un défaut.'),PageBreak()]
    story += [p('Documentation et contrôles','title'),p('Quatre STEP colorés ont passé les contrôles FreeCAD sans interface : validité, fermeture des solides, nombre de solides et enveloppe. Aucun test dans l’interface FreeCAD ou l’extension CAD View de VSCode n’est revendiqué.'),
        table([['Modèle','Solides / faces'],*[[m['file'],f"{m['validation']['solids']} / {m['validation']['faces']}"] for m in cad['models']]],[139,35]),Spacer(1,4*mm),
        p('Origine et précision des modèles','sub'),p('Reconstruction suivant les plans et photos. Aucun élément de fusion interne inventé ; cette CAO ne permet pas de fabriquer un fusible calibré. Les détails estimés figurent dans cotes.md et les JSON. L’accès CAO officiel proposé par Littelfuse exige un formulaire ; aucun formulaire ni message n’a été envoyé.'),
        p('Achat et retours d’expérience','sub'),p('Amazon a renvoyé des pages de vérification sans catalogue exploitable : aucune offre exacte, ASIN ni prix français confirmé. Les avis eBay exacts consultés étaient absents ; aucun essai indépendant exploitable de ce montage V3 trouvé sur les forums/YouTube. Les retours généraux sur MIDI ne prouvent pas ses performances.'),
        p('Sources et originaux conservés','sub'),
        source('Support, fiche fabricant via TME','https://www.tme.eu/Document/751067cde59f8870ba92d17db0ce52da/04980900ZXT.pdf'),
        source('Fusible, révision actuelle consultée en ligne','https://www.littelfuse.com/products/fuses-overcurrent-protection/fuses/automotive-fuses/bolt-down-fuses/midi'),
        source('Fusible exact et révision 2021 liée par le fournisseur','https://uk.farnell.com/littelfuse/0498060-m/automotive-fuse-time-delay-60a/dp/3516004'),
        source('CAO constructeur proposée après formulaire','https://info.littelfuse.com/midi-498-series-3dmodel-landingpage'),
        p('Quatre PDF fabricant d’origine sont archivés : support 2008, catalogue 2012 (PDF p.164 / imprimée159), fusible ancien et REV07272021. La fiche 2024 consultée en ligne n’a pas été téléchargée. SHA256, URL exactes, photos, réponses refusées et limites : assets.json, sources.json, recherche-technique.md.','small')]
    SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=18*mm,bottomMargin=23*mm,
        title='Drone V3 - Fusible principal MIDI 60 A',author='Projet Drone V3').build(story,onFirstPage=footer,onLaterPages=footer)
    pdf=pymupdf.open(OUT);assert len(pdf)==5,len(pdf);pages=[]
    for i,page in enumerate(pdf):
        png=TMP/f'page-{i+1}.png';page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(png)
        pages.append(dict(page=i+1,render=str(png.relative_to(ROOT)).replace('\\','/'),chars=len(page.get_text())))
    OUT.with_suffix('.json').write_text(json.dumps(dict(file=OUT.name,pages=len(pdf),sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),
        generated_on='2026-10-14',generator='tools/build_overcurrent_pdf.py',renders=pages,visual_review_complete=False),indent=2)+'\n',encoding='utf-8')
    print('PDF',len(pdf),'pages',OUT.stat().st_size,'bytes',flush=True)
if __name__=='__main__':main()
