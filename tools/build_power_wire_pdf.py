"""Create the four-page wire notice and render every page for manual review."""
from pathlib import Path
import json,hashlib,sys
import pymupdf
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate,Spacer,Image,PageBreak
from build_heatsink_pdf import p,table,banner,GREY
from collect_power_wire_refs import MAKER
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/cable-puissance-12awg'
OUT=BASE/'notices/notice-cable-puissance-12awg-v3.pdf';TMP=ROOT/'tools/temp/power-wire-review/pdf'
def footer(c,d):
    c.saveState();c.setStrokeColor(colors.HexColor('#ccdbe4'));c.line(18*mm,17*mm,192*mm,17*mm)
    c.setFont('HV3',7.4);c.setFillColor(GREY);c.drawString(18*mm,12*mm,'Drone V3 | Câble 12 AWG des départs ESC | 14 octobre 2026 | Etude non testée')
    c.drawRightString(192*mm,12*mm,str(d.page));c.restoreState()
def ref(label,url):return p(f'<link href="{url}" color="#174969"><b>{label}</b></link>','small')
def main():
    sys.stdout.reconfigure(encoding='utf-8');TMP.mkdir(parents=True,exist_ok=True)
    cat=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'));calc=json.loads((BASE/'calculs.json').read_text(encoding='utf-8'))
    assert json.loads((BASE/'3D/validation-freecad.json').read_text(encoding='utf-8'))['all_passed']
    story=[p('Câble de puissance<br/>des deux départs moteurs','title'),p('BNTECHGO SW12G68008F10C2 - 12 AWG - deux fils séparés rouge/noir'),
        banner('<b>Choix d’étude, non acheté et non testé.</b> Lot 10 ft par couleur, soit 3,048 m rouge + 3,048 m noir. Queues après chaque ATO30 vers XT60H-F et retours indépendants vers D-. Tronc principal 6 mm² étudié séparément.'),Spacer(1,3*mm),
        table([['Caractéristique annoncée','Valeur / portée'],['Conducteur','680 brins de Ø0,08 mm en cuivre étamé ; 12 AWG nominal ≈3,31 mm²'],
            ['Image technique BNTECHGO','Faisceau Ø2,41 mm ; section arrondie 3,4 mm² ; résistance 5,06 Ω/km'],
            ['Gaine silicone','Ø4,5 ±0,1 mm sur l’offre ; épaisseur nominale 1,05 mm sur l’image'],
            ['Température / tension','-60 à +200 °C / 600 V annoncés ; courant admissible V3 non qualifié']],[59,115]),Spacer(1,4*mm),
        Image(str(BASE/'photos/BNTECHGO-original-2.jpg'),width=158*mm,height=97.73*mm),
        p('Image technique originale de la marque, archivée inchangée depuis le CDN de sa page produit. Elle complète les cotes et la résistance absentes du texte principal. Pas une photo du lot reçu ni un rapport de mesure indépendant.','small'),PageBreak()]
    story += [p('Raccordements et préparation','title'),
        table([['Queue V3','Chemin','Couleur'],['CM1+','Sortie 5065 / ATO30 ESC1 → + XT60H-F1','Rouge'],['CM2+','Sortie 5065 / ATO30 ESC2 → + XT60H-F2','Rouge'],
            ['CM1-','- XT60H-F1 → cosse MiniBus D- N1','Noir'],['CM2-','- XT60H-F2 → cosse MiniBus D- N3','Noir']],[31,111,32]),Spacer(1,3*mm),
        p('Les fils 12 AWG des porte-fusibles et les entrées 16 AWG / 75 mm des ESC restent inclus dans leurs composants. Raccords fil-à-fil et cosses de MiniBus à choisir. Goujons #10-32 UNF, pas M5 ; passage réel et outil de sertissage à vérifier.'),
        banner('<b>Contrôler le passage de la gaine dans les capots XT60H.</b> Le fil choisi annonce Ø4,5 ±0,1 mm ; l’ancien fil CAO était Ø4,2 estimé et les trous du capot étaient aussi estimés. Aucune compatibilité d’ajustement prouvée par ces modèles.'),Spacer(1,2*mm),
        p('Procédure du projet','sub'),
        p('<b>1.</b> Batterie et équilibrage débranchés : mesurer le chemin, prévoir terminaisons et maintien, puis établir la liste de coupe. L’exemple 0,20 m par queue n’est pas une instruction de coupe.'),
        p('<b>2.</b> Vérifier variante 12 AWG, rouge/noir, cuivre étamé déclaré, diamètre et état. Le cuivre étamé industriel est différent d’aluminium cuivré ou d’un bout rigidifié par soudure.'),
        p('<b>3.</b> Régler le dénudage selon godet, cosse ou raccord réel. Inspecter les brins fins sous grossissement : aucun brin coupé ou retiré. Les 5 mm dénudés des modèles sont illustratifs.'),
        p('<b>4.</b> Pour XT60H, passer le capot avant soudure, garder tous les brins et éviter chauffe prolongée. Pour un sertissage, suivre notice du raccord et matrice prescrite, sans soudure ajoutée non prévue.'),
        p('<b>5.</b> Isoler, identifier et retenir les raccords ; garder les fils hors engrenages, roues, arêtes et zones chaudes. Pas de traction sur les godets ou soudures ; protéger la gaine du frottement.'),
        p('<b>6.</b> Contrôler continuité, polarités, isolement et serrages, puis première alimentation limitée et supervisée. Mesurer les courants, chutes et températures du faisceau complet.'),
        p('Si un fil entre dans une borne vissée, confirmer l’acceptation du très fin multibrins et l’embout applicable ; ne pas pré-étamer cette extrémité à la soudure. Aucun raccord, cosse ou outillage inclus dans le lot de fil.','small'),PageBreak()]
    story += [p('Dimensions, pertes et limites','title'),
        table([['Grandeur','Valeur / interprétation'],['Section 12 AWG nominale','≈3,31 mm² ; désignation, pas section mesurée du lot'],
            ['Image BNTECHGO','3,4 mm² ; Ø2,41 de faisceau ; Ø4,5 extérieur ; épaisseur1,05'],
            ['Somme des 680 disques Ø0,08','3,41805 mm² calculés ; tolérances, étamage et torsade non pris en compte'],
            ['Épaisseur déduite des Ø','(4,50-2,41)/2 = 1,045 mm, cohérent avec arrondi1,05'],
            ['Longueur du lot','10 ft ×304,8 = 3 048 mm par couleur ; total6,096 m']],[60,114]),Spacer(1,3*mm),
        p('Ø2,41 est l’enveloppe du faisceau, pas le diamètre d’un cuivre massif de 3,31 mm² (≈2,053 mm). Les espaces entre brins ne conduisent pas comme le cuivre. Pas de torsade, épaisseur d’étamage et rayon minimal du lot non publiés.','small'),
        p('Exemples à 20 A par boucle','sub'),
        table([['Longueur par conducteur','Boucle à 5,06 mΩ/m','Chute / pertes'],
            *[[f"{r['one_way_length_m']:.2f} m".replace('.',','),f"{1000*r['loop_resistance_ohm']:.3f} mΩ".replace('.',','),
                f"{1000*r['drop_V']:.2f} mV / {r['loss_per_branch_W']:.4f} W".replace('.',',')] for r in calc['loop_examples'] if r['current_A']==20]],[63,49,62]),Spacer(1,3*mm),
        p('R = 2 × longueur aller × 0,00506 Ω/m ; ΔV = IR ; P = I²R. À 0,20 m aller et retour : <b>0,8096 W par branche, 1,6192 W pour deux branches identiques</b>. Ajouter fils des supports, ESC, prises, raccords et chauffage. À 30 A sur cette boucle : 60,72 mV / 1,8216 W.','small'),
        banner('<b>5,06 Ω/km est une résistance annoncée.</b> Température, méthode et valeur maximale non précisées ; calcul de pertes, pas certificat d’ampacité. Les inscriptions 200 °C / 600 V ne qualifient pas le courant de nos câbles, soudures ou capots.'),Spacer(1,2*mm),
        p('Le scénario 20 A par ESC reste une hypothèse sans limitation active. ATO30 peut laisser durer une surcharge ; qualifier les fils neufs, raccords et fils ESC16 AWG avec sa courbe et le courant prospectif LiPo. Le nouveau fil ne qualifie pas le XT60 commun du pack.'),
        p('Mesurer courant RMS et pointes, chute sur longueur connue et températures sur les durées prévues. La mesure de résistance doit distinguer les cordons et contacts ; mesure quatre fils utile. Aucun essai volontaire de court-circuit de batterie.','small'),PageBreak()]
    story += [p('Achat, modèles et sources','title'),
        p('<b>ASIN exact B01ABOPMEI</b> : titre Amazon.com 12 AWG, rouge/noir 10ft par couleur vérifié. Prix, stock et livraison Amazon.fr non confirmés. Site BNTECHGO : <b>14,98 USD</b> au relevé du 14 octobre 2026, taxes et frais français non confirmés ; aucun prix TTC livré en euros attribué.'),
        p('Un lot proposé ; exemple quatre queues0,20 m = 0,40 m rouge + 0,40 m noir, réserve2,648 m par couleur. Longueurs finales après implantation. Le lien de forum B01AO7586O ouvre du <b>14 AWG</b> et est écarté ; ne pas copier un ASIN sans vérifier sa variante.','small'),
        table([['Modèle STEP','Solides'],*[[m['title'],str(m['validation']['solids'])] for m in cat['models']]],[145,29]),Spacer(1,3*mm),
        p('Trois modèles d’implantation légers, trois modèles détaillés avec <b>680 brins individuels chacun</b>. Brins droits en réseau idéal ; torsade et disposition réelle non mesurées. Étamage représenté par couleur, sans épaisseur inventée. Longueurs25/100 mm et dénudages5 mm illustratifs. La fenêtre de gaine est volontaire.','small'),
        p('Imports CadQuery et <b>FreeCAD sans interface</b> : validité, solides fermés, enveloppes et nombre de brins contrôlés. Version courbée : continuité de matière échantillonnée. Aucun essai GUI/CAD View ou matériel revendiqué. Les volumes pleins des versions légères ne servent pas à calculer masse ou section de cuivre.','small'),
        p('Avis BNTECHGO : souplesse/soudure appréciées ; Jeff Y. (2018) signale des brins coupés par une pince mal réglée. R/C Tech2025 corrobore l’usage de cordons de charge mais contient le lien14 AWG. Aucun essai vidéo exact avec mesures résistance/température trouvé.','small'),
        ref('BNTECHGO : référence, images techniques et avis',MAKER),
        ref('Amazon.com : variante exacte B01ABOPMEI','https://www.amazon.com/dp/B01ABOPMEI'),
        ref('Junhao : catalogue comparatif, page12','https://en.junhaodx.com/Catalogue.pdf'),
        ref('ModalAI : exemple fabricant de câble BNTECHGO/XT60','https://storage.googleapis.com/modalai_public/modal_drawings/MCBL-00110%20Drawing%20v4.pdf'),
        p('Aucun PDF officiel BNTECHGO exact obtenu. Original Junhao = produit voisin, sans certification transférée ; plan ModalAI = exemple d’usage, sans courant V3 validé. Sources, statuts, images et SHA256 sont conservés dans le dossier.','small')]
    SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=18*mm,bottomMargin=23*mm,
        title='Drone V3 - Cable BNTECHGO 12 AWG',author='Projet Drone V3').build(story,onFirstPage=footer,onLaterPages=footer)
    doc=pymupdf.open(OUT);pages=[]
    for i,page in enumerate(doc):
        png=TMP/f'page-{i+1}.png';page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(png)
        pages.append(dict(page=i+1,render=str(png.relative_to(ROOT)).replace('\\','/'),chars=len(page.get_text())))
    OUT.with_suffix('.json').write_text(json.dumps(dict(file=OUT.name,pages=len(doc),sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),
        generator='tools/build_power_wire_pdf.py',generated_on='2026-10-14',renders=pages,visual_review_complete=False),indent=2)+'\n',encoding='utf-8')
    print('PDF',len(doc),'pages',OUT.stat().st_size,'bytes',flush=True);assert len(doc)==4,len(doc)
if __name__=='__main__':main()
