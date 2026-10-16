"""Author and render the French project notice; originals remain unchanged."""
from pathlib import Path
import json,hashlib,sys
import pymupdf
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate,Spacer,Image,PageBreak
from build_heatsink_pdf import p,table,banner,source,GREY
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/distribution-alimentation'
OUT=BASE/'notices/notice-distribution-alimentation-v3.pdf';TMP=ROOT/'tools/temp/distribution-review/pdf'
def footer(c,d):
    c.saveState();c.setStrokeColor(colors.HexColor('#ccdbe4'));c.line(18*mm,17*mm,192*mm,17*mm)
    c.setFont('HV3',7.4);c.setFillColor(GREY);c.drawString(18*mm,12*mm,'Drone V3 | Distribution MiniBus | 14 octobre 2026 | Etude non testée')
    c.drawRightString(192*mm,12*mm,str(d.page));c.restoreState()
def main():
    sys.stdout.reconfigure(encoding='utf-8');TMP.mkdir(parents=True,exist_ok=True)
    cat=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'))
    fc=json.loads((BASE/'3D/validation-freecad.json').read_text(encoding='utf-8'));assert fc['all_passed']
    story=[p('Distribution électrique<br/>Deux MiniBus 2315','title'),p('Deux rails indépendants pour la batterie LiPo 2S'),
        banner('<b>Sélection d’étude : deux Blue Sea Systems 2315 avec capots 2713 inclus.</b> Un rail positif après le MIDI principal, un rail négatif pour les retours. Non acheté, non testé ; offre Amazon.fr et prix non confirmés.'),Spacer(1,4*mm),
        table([['Caractéristique publiée','Valeur'],['Calibre continu / tension DC','100 A par bornier / 48 V DC ; pack V3 limité à 8,4 V'],
            ['Connexions','Quatre goujons #10-32 UNF par bornier ; tous sont communs'],
            ['Matériaux','Cuivre C110 étamé ; socle renforcé ; capot polycarbonate transparent'],
            ['Masse arrondie','0,08 kg par unité ; environ 160 g pour deux, hors faisceau']],[57,117]),Spacer(1,3*mm),
        Image(str(BASE/'3D/bluesea-2315-vue-eclatee.png'),width=145*mm,height=117.8*mm),
        p('Reconstruction extérieure suivant plans et photos. Le capot réel est transparent ; affichage clair opaque dans cet export. Détails non cotés estimés, aucun faisceau représenté.','small'),PageBreak()]
    story += [p('Cotes et interfaces','title'),
        table([['Cote publiée','Valeur et portée'],['Socle, longueur × largeur','106,68 × 22,86 mm'],
            ['Fixation au châssis','Entraxe 90,49 mm ; trous acceptant vis #10 ou M5'],
            ['Goujons extrêmes','Entraxe 64,77 mm ; quatre positions uniformes déduites du plan'],
            ['Filetage électrique','#10-32 UNF ; diamètre nominal 4,826 ; pas 0,79375 mm'],
            ['Hauteur avec capot','31,75 mm MINIMUM ; maximum avec cosses non établi'],
            ['Cote verticale sans capot','15,88 mm dans le plan ; détail interne non coté']],[60,114]),Spacer(1,3*mm),
        Image(str(BASE/'notices/BlueSea-2315-plan-original.jpg'),width=101*mm,height=87.13*mm),
        p('Plan constructeur original. La CAO utilise ce socle et les entraxes comme références ; ce plan ne fournit pas de tolérances de fabrication.','small'),
        p('Visserie à distinguer','sub'),p('Les <b>M5 des trous de fixation</b> ne sont pas les goujons électriques. Conserver les écrous #10-32 fournis. Un oeillet commercial M5 peut convenir si son passage et son encombrement sont adaptés ; un écrou M5 × 0,8 ne convient pas.'),
        p('Diamètre des passages CAO 5,5 mm, lamages, épaisseurs, rayons, longueur des goujons et attaches du capot : estimations. La hauteur minimale n’est pas une garantie de passage du faisceau. Relever les pièces et cosses avant de figer le châssis.','small'),PageBreak()]
    story += [p('Chemins de puissance','title'),
        banner('<b>D+ : pack positif → MIDI 60 A → MiniBus → départs protégés.</b><br/>Moteurs : protection → D1D100 → deux ESC.<br/>Pi : fusible de départ → Pololu 2813 → D24V90F5 → Pi/caméra.<br/><b>D- : retours de puissance séparés vers le négatif pack.</b>'),Spacer(1,4*mm),
        table([['Rail / borne V3','Affectation proposée'],['D+ / P1','Réserve, sans conducteur'],['D+ / P2','Arrivée depuis le MIDI principal'],
            ['D+ / P3','Départ moteurs protégé vers borne +2 du D1D100'],['D+ / P4','Départ Pi protégé vers VIN du Pololu 2813'],
            ['D- / N1','Retour ESC 1'],['D- / N2','Retour négatif du pack B0'],['D- / N3','Retour ESC 2'],['D- / N4','Retour électronique et auxiliaires']],[51,123]),Spacer(1,3*mm),
        p('Numéros de projet, de gauche à droite sur X dans la CAO. Les quatre bornes de chaque rail sont électriquement communes ; <b>aucun pont entre D+ et D-</b>. Une cosse principale par borne dans cette proposition.'),
        p('Hypothèse de courant','sub'),p('<b>40 + 25 / (6,4 × 0,90) + 0,05 = 44,39 A.</b> Moteurs 40 A au total, Pi/caméra 25 W, rendement 90 % et auxiliaires 0,05 A sont des hypothèses. Les capacités 30 A des ESC ne donnent pas leur consommation réelle.'),
        p('100 A est une capacité du bus, pas une limite de courant ou un fusible. Le principal 60 A ne protège pas seul les départs plus fins. Fusible Pi au début du départ ; protections moteurs et fils de chaque ESC à coordonner. Calibres de branches, sections et courant prospectif restent à établir.'),
        p('Retours moteurs directement au rail, sans passer par le Pi ou l’USB. Un seul BEC 6 V alimente le servo ; second positif BEC isolé. B1 du pack est une référence de mesure de cellule, jamais le retour de puissance. SSR : +3 à VSW, 4 à B0, selon le dossier de protection.','small'),PageBreak()]
    story += [p('Montage et qualification','title'),
        p('Batterie et prise d’équilibrage débranchées. Fixer les socles, isoler des pièces conductrices, repérer positif et négatif. Sertir les cosses avec un outil adapté, isoler les fûts et poser l’oeillet sur la barre conductrice, sous l’écrou à flasque. Retenir les câbles pour ne pas tirer sur les goujons.'),
        table([['Couple publié','Document / interprétation'],['1,69 N·m / 15 in-lb','Page exacte 2315, rubrique « screw terminal torque »'],
            ['2,03 N·m / 18 in-lb','Page 2305 sans capot, rubrique « stud torque »']],[57,117]),Spacer(1,4*mm),
        banner('<b>Écart à résoudre avec la documentation du lot avant mise en service.</b> Valeur de préparation conservatrice 1,69 N·m, sans qualification de tenue mécanique. Ne pas appliquer les 4,5 N·m du porte-fusible MIDI M5.'),Spacer(1,4*mm),
        p('Poser les capots après contrôle des contacts, de la polarité et de la garde aux cosses. Les borniers n’ont pas une étanchéité IP démontrée. La FAQ évoque au plus quatre cosses par goujon ; cela ne valide pas leur empilage ni leur passage sous le capot avec nos fils.'),
        p('Mesures nécessaires','sub'),p('Vérifier continuité de chaque rail, absence de court-circuit D+/D-, sections, protections et tenue mécanique. Première mise sous tension sur alimentation limitée, après schéma et contrôle du faisceau. Enregistrer les pointes, chutes de tension et températures aux contacts dans l’usage prévu ; vérifier vibrations et fixation des capots.'),
        p('Tronc cuivre 6 mm² : proposition reprise de l’étude du MIDI, pas une intensité admissible universelle. Sections du pack, XT60, cosses et fils ESC à confirmer. Résistance de contact 2315 non publiée : aucune perte ou chute de tension garantie calculée. Pas de court-circuit volontaire du pack.'),
        p('Implantation d’étude','sub'),
        p('Centres des rails Y ±23 mm. Deux socles occupent 106,68 × 68,86 mm, hors fils. Étiquettes rouge/noire ajoutées par la V3 ; aucune pièce double commercialisée supposée. L’aperçu et le STEP à deux rails sont fournis dans le dossier 3D.','small'),PageBreak()]
    story += [p('Achat, CAO et sources','title'),
        p('<b>ASIN B000OTJ8A0 confirmé sur Amazon.com</b> par le titre et la description. Offre, prix TTC, stock et livraison sur Amazon.fr non confirmés. Les requêtes directes ont renvoyé une vérification automatique. Aucun achat effectué. Repère hors Amazon : Hodges Marine affichait 26,40 USD/unité, soit 52,80 USD pour deux, hors livraison et traitement fiscal en France.'),
        p('Avis exact Walmart du 20 octobre 2020 : compacité et capot appréciés, sans mesure sous charge. Forum R3Owners : proposition de la variante 2305 pour organiser des raccords de moto, pas un essai V3. Aucun essai vidéo exact exploitable trouvé. Ces retours ne démontrent ni le calibre en usage ni l’autonomie.'),
        table([['Modèle reconstruit','Solides / faces'],*[[m['title'],f"{m['validation']['solids']} / {m['validation']['faces']}"] for m in cat['models']]],[134,40]),Spacer(1,4*mm),
        p('Les cinq STEP ont passé les imports et contrôles <b>FreeCAD sans interface</b> : validité, solides fermés, nombre de solides et enveloppes. Contrôles CadQuery : volumes, couleurs, interfaces sondées et absence de chevauchement matériel. Aucun essai dans l’interface FreeCAD ou CAD View de VSCode revendiqué. Cotes non mesurées et fichiers non natifs fabricant.'),
        p('Sources conservées et consultées','sub'),
        source('2315, caractéristiques et capot inclus','https://www.bluesea.com/products/2315'),
        source('2305, référence de goujons et couple distinct','https://www.bluesea.com/products/2305/Common_100A_Mini_BusBar_-_4_Gang'),
        source('Catalogue 2024, PDF original via PrimeMarine, page 100','https://primemarine.com.pl/pli/141_Katalog%20BlueSea.pdf'),
        source('Fiche Amazon.com identifiée','https://www.amazon.com/dp/B000OTJ8A0'),
        p('Plans JPG et photos originaux, catalogue complet, certificat IMCI 2014 et déclaration 2009 archivés inchangés. Ces deux documents historiques ne certifient pas le robot ou le lot actuel. Aucun manuel autonome exact trouvé ; articles fabricant complètent les plans. URL, statuts, empreintes et limites dans assets.json, sources.json, recherche-technique.md et JSON voisins des STEP.','small')]
    SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=18*mm,bottomMargin=23*mm,
        title='Drone V3 - Distribution electrique MiniBus 2315',author='Projet Drone V3').build(story,onFirstPage=footer,onLaterPages=footer)
    doc=pymupdf.open(OUT);assert len(doc)==5,len(doc);pages=[]
    for i,page in enumerate(doc):
        png=TMP/f'page-{i+1}.png';page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(png)
        pages.append(dict(page=i+1,render=str(png.relative_to(ROOT)).replace('\\','/'),chars=len(page.get_text())))
    OUT.with_suffix('.json').write_text(json.dumps(dict(file=OUT.name,pages=len(doc),sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),
        generated_on='2026-10-14',generator='tools/build_distribution_pdf.py',renders=pages,visual_review_complete=False),indent=2)+'\n',encoding='utf-8')
    print('PDF',len(doc),'pages',OUT.stat().st_size,'bytes',flush=True)
if __name__=='__main__':main()
