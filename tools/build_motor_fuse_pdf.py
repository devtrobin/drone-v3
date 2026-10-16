"""Author the motor protection project notice and render every page for review."""
from pathlib import Path
import json,sys,hashlib
import pymupdf
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate,Spacer,Image,PageBreak
from build_heatsink_pdf import p,table,banner,GREY
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/protection-branches-moteurs'
OUT=BASE/'notices/notice-protection-branches-moteurs-v3.pdf';TMP=ROOT/'tools/temp/motor-fuse-review/pdf'
def ref(label,url):return p(f'<link href="{url}" color="#174969"><b>{label}</b></link>','small')
def footer(c,d):
    c.saveState();c.setStrokeColor(colors.HexColor('#ccdbe4'));c.line(18*mm,17*mm,192*mm,17*mm)
    c.setFont('HV3',7.4);c.setFillColor(GREY);c.drawString(18*mm,12*mm,'Drone V3 | Protections des deux ESC | 14 octobre 2026 | Etude non testée')
    c.drawRightString(192*mm,12*mm,str(d.page));c.restoreState()
def main():
    sys.stdout.reconfigure(encoding='utf-8');TMP.mkdir(parents=True,exist_ok=True)
    cat=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'))
    assert json.loads((BASE/'3D/validation-freecad.json').read_text(encoding='utf-8'))['all_passed']
    story=[p('Protection des deux<br/>départs moteurs','title'),p('Blue Sea 5065 + Littelfuse ATO 30 A - un ensemble par variateur'),
        banner('<b>Sélection d’étude, non achetée et non testée.</b> Deux protections séparées sur les positifs batterie des ESC, après le relais commun. Offre Amazon.fr, tenue des fils 16 AWG et coordination de défaut à confirmer.'),Spacer(1,4*mm),
        table([['Pièce','Quantité embarquée / portée'],['Porte-fusible Blue Sea 5065','Deux ; un circuit ATO/ATC chacun, fils 12 AWG ; fusible séparé ; calibre maximal fabricant 30 A'],
            ['Littelfuse 0ATO030.V / ATO30','Deux ; 30 A / 32 V DC, PA66 vert ; pouvoir de coupure 1 000 A à 32 V DC'],
            ['Conditionnement possible','Une carte 0ATO030.VP / ATO30BP de cinq : deux installés, trois de rechange si ce lot est acheté']],[54,120]),Spacer(1,3*mm),
        Image(str(BASE/'3D/deux-protections-moteurs-ato30-etude.png'),width=130*mm,height=105.625*mm),
        p('Pose CAO illustrative : deux supports identiques avec quatre fils rouges libres. Raccord de répartition, XT60, cosses et fixation au châssis absents. Les dimensions non publiées du support sont estimées.','small'),PageBreak()]
    story += [p('Courants et choix du calibre','title'),
        banner('<b>Scénario : 40 A moteurs au total, 20 A par départ.</b><br/>Hypothèses supplémentaires de répartition, sans mesure ni limitation imposée. Un total de 40 A ne garantit pas 20 A maximum sur chaque roue. Inclure le BEC du servo dans le courant de son ESC.'),Spacer(1,4*mm),
        table([['Calibre ATO','À 20 °C*','À 65 °C*','À 85 °C*'],['20 A','18 A','15 A','14 A'],['25 A','23 A','19 A','18 A'],['30 A - étude','27 A','23 A','21 A']],[54,40,40,40]),Spacer(1,3*mm),
        p('*Courants recommandés typiques dans la fiche aftermarket Littelfuse du 15 novembre 2022, selon ses connexions et sections d’essai. 65 et 85 °C servent à comparer les marges, pas à fixer la température du robot. Le 25 A manque de marge au scénario 20 A chaud ; le 30 A est retenu pour l’étude.','small'),
        p('Le support 5065 est limité au calibre 30 A : aucune hausse automatique pour passer le démarrage. Le chiffre « 30 A continu / 100 A de pointe » de l’ESC indique une capacité annoncée ; durée de la pointe, consommation et limitations réelles non établies.'),
        p('Pertes du fusible à froid','sub'),
        table([['Courant sur un départ','Chute, Rc = 1,97 mΩ','Perte du fusible'],['20 A','39,4 mV','0,788 W'],['25 A','49,25 mV','1,231 W'],['30 A','59,1 mV','1,773 W']],[58,65,51]),Spacer(1,3*mm),
        p('Deux fusibles à 20 A : <b>1,576 W</b>, hors contacts, fils et chauffage. Les 84 mV de la fiche concernent ses propres conditions d’essai. I²t typique 1 500 A²s : fusion avant l’arc, pas énergie totale de coupure garantie.'),
        p('Exemple de prolongements','sub'),p('Par branche : cuivre 4 mm², 0,20 m positif + 0,20 m retour ; résistivité supposée à 20 °C 0,0175 Ω·mm²/m. À 20 A : <b>1,75 mΩ / 35 mV / 0,700 W</b>. Ajouter les fils du support, ceux de l’ESC, les connecteurs, les raccords et la température réelle. Longueurs et sections finales à qualifier.','small'),PageBreak()]
    story += [p('Raccordement et interfaces','title'),
        banner('<b>MiniBus D+ P3 → relais D1D100 (+2 puis 1) → répartition positive → deux départs séparés.</b><br/>Chaque départ : 5065 / ATO30 → entrée XT60 de son ESC. Retours négatifs séparés vers N1 et N3 de D-. Aucun fusible dans les trois phases moteur.'),Spacer(1,3*mm),
        table([['Interface','Donnée / validation restante'],['Tronc commun avant petits fusibles','6 mm² cuivre proposé, protégé par le MIDI principal 60 A ; coordination à qualifier'],
            ['Répartition après borne 1 du SSR','Raccord à sélectionner ; pas d’empilage de deux cosses supposé validé'],
            ['Deux fils de chaque 5065','12 AWG, ≈3,31 mm² nominaux ; deux positifs entrée/sortie, sans retour négatif'],
            ['Fils d’entrée de chaque ESC','16 AWG, 75 mm rouge et noir, XT60 ; ≈1,31 mm² nominal selon fiche Hobbywing'],
            ['Prolongements proposés','4 mm² par départ et retour ; cela ne qualifie pas les fils 16 AWG de l’ESC']],[61,113]),Spacer(1,3*mm),
        p('<b>Tenue des fils d’origine à démontrer.</b> Identifier l’isolant, vérifier échauffement, pointes et énergie de défaut du 16 AWG avec la courbe ATO30. La section de 4 mm² utilisée pour l’essai fabricant du fusible n’est pas une certification du faisceau V3.'),
        p('Cotes de référence et estimations','sub'),
        table([['Fusible, référence fabricant','19,1 × 5,1 × 18,8 mm ; lames 4,1 × 0,65 ; dépassement 6,5'],['Lames, entraxe déduit','14,5 mm est leur largeur extérieure ; entraxe 10,4 mm'],
            ['Support en CAO, hors fils','37,5 × 38 × 15 mm, trou Ø5,0 : estimations, à mesurer avant perçage'],['Fils de la CAO','100 mm extérieurs + 8 mm nus ; 19 brins illustratifs, longueur livrée inconnue']],[61,113]),Spacer(1,3*mm),
        p('Placer chaque fusible au début de sa dérivation. Les arrivées avant eux restent à coordonner avec le principal : courtes, isolées et retenues. Le servo reste sur un seul BEC à 6 V ; positif du second BEC isolé, aucun BEC vers le 5 V Pi.','small'),PageBreak()]
    story += [p('Pointes, défauts et arrêt','title'),p('<b>30 A ne signifie pas coupure immédiate à 30 A.</b> Fenêtres tabulées applicables à notre référence :'),
        table([['Rapport au calibre','Courant ATO30','Temps d’ouverture'],['110 %','33 A','Au moins 360 000 s ; pas de maximum'],['135 %','40,5 A','0,75 à 600 s'],
            ['160 %','48 A','0,25 à 50 s'],['200 %','60 A','0,15 à 5 s'],['350 %','105 A','0,08 à 0,5 s'],['600 %','180 A','0,1 s maximum']],[44,40,90]),Spacer(1,3*mm),
        p('À 100 A, aucune fenêtre tabulée exacte n’est fournie : ne pas lui attribuer la fenêtre de 105 A. Mesurer les impulsions d’entrée et vérifier passage des pointes et vieillissement avec les critères fabricant.','small'),
        banner('<b>Pouvoir de coupure : 1 000 A à 32 V DC.</b> Courant prospectif LiPo à établir. Le principal MIDI 60 A ne qualifie pas automatiquement la capacité de coupure en série ou la sélectivité avec les ATO30.'),Spacer(1,3*mm),
        p('Repère ohmique simplifié : <b>8,4 V / 1 000 A = 8,4 mΩ</b>. Exclure la résistance du fusible de branche pour justifier le courant prospectif. Le « 80C » ne donne pas cette mesure ; pas de court-circuit volontaire du pack.'),
        p('Ces fusibles ne garantissent pas de sauver les semi-conducteurs. Le rapport 60/30 ne prouve pas la sélectivité ; l’I²t de fusion seul ne prouve pas la tenue du SSR. Deux ATO30 ne font pas respecter l’enveloppe thermique de 40 A continu total proposée pour le relais.'),
        p('Perte d’un seul départ','sub'),p('Une fusion peut supprimer propulsion et freinage commandé d’une roue pendant que l’autre fonctionne encore. Prévoir détection et arrêt global supervisé ; aucun retour de fusion fourni ici. Vérifier freinage/régénération et transitoires à la coupure. Remplacer un fusible uniquement pack et équilibrage débranchés, après recherche de la cause.'),
        p('Qualification : polarités et isolement hors tension ; premier essai limité ; mesures des deux courants et de leur somme, chutes, températures, pointes, défauts et comportement de perte d’une propulsion. Voir le protocole détaillé dans integration.md.','small'),PageBreak()]
    story += [p('Achat, modèles et sources','title'),
        p('Deux 5065 supplémentaires, soit <b>trois prévus au total avec le Pi</b>. ASIN B004ZIUA62 déjà identifié sur Amazon.com ; offre Amazon.fr non confirmée. Fusibles exacts : aucun ASIN Amazon validé. Pack ATO30BP de cinq : deux utilisés et trois de rechange, si acheté.'),
        p('Repères étrangers : fusible exact 1,43 USD/unité chez DigiKey ; support 15,01 USD au relevé antérieur du même jour chez Hodges. Deux de chaque : 32,88 USD, hors livraison et fiscalité France. Canadian Tire affiche 6,29 CAD pour cinq fusibles ; option alternative, pas à additionner aux deux unités. Aucun devis TTC livré validé.','small'),
        p('Avis : Maine Sail, forum 2014, dit utiliser le 5065 ; aucune mesure RC. Canadian Tire : 4,6/5, 172 avis regroupant plusieurs calibres ; pas une validation du 30 A. Aucun essai vidéo exact donnant les mesures recherchées identifié.','small'),
        table([['Modèle STEP','Solides / faces'],*[[m['title'],f"{m['validation']['solids']} / {m['validation']['faces']}"] for m in cat['models']]],[134,40]),Spacer(1,3*mm),
        p('Les cinq fichiers passent les contrôles <b>FreeCAD sans interface</b> : validité, solides fermés, nombres et enveloppes. Réimports CadQuery : volumes, couleurs et absence de chevauchement. Fils continus ; géométrie du support estimée, fusible aux cotes de référence. Aucun test GUI FreeCAD/CAD View revendiqué.','small'),
        p('Références consultables','sub'),
        ref('Blue Sea : fiche exacte 5065','https://www.bluesea.com/products/5065'),
        ref('Littelfuse : ATO aftermarket, révision 15 novembre 2022','https://www.littelfuse.com/assetdocs/littelfuse-datasheet-ato?assetguid=bba6ed2a-96e5-4b07-ab5d-0e8d267c0bd1'),
        ref('Hobbywing : WP16BL30 G2, fils d’entrée et connecteurs','https://www.hobbywing.com/en/products/quicrun-wp-16bl30-g2'),
        ref('DigiKey : référence exacte 0ATO030.V','https://www.digikey.com/en/products/detail/littelfuse-inc/0ATO030-V/2519124'),
        p('Fiche ATO copie RSP inchangée, catalogue 2013 et photo 5065 archivés. Catalogue Blue Sea et notice ESC référencés dans les dossiers existants. URL, statuts de téléchargement, empreintes, cotes et limites : sources.json, assets.json et JSON voisins des STEP.','small')]
    SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=18*mm,bottomMargin=23*mm,
        title='Drone V3 - Protection des deux departs moteurs',author='Projet Drone V3').build(story,onFirstPage=footer,onLaterPages=footer)
    doc=pymupdf.open(OUT);pages=[]
    for i,page in enumerate(doc):
        png=TMP/f'page-{i+1}.png';page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(png)
        pages.append(dict(page=i+1,render=str(png.relative_to(ROOT)).replace('\\','/'),chars=len(page.get_text())))
    OUT.with_suffix('.json').write_text(json.dumps(dict(file=OUT.name,pages=len(doc),sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),
        generated_on='2026-10-14',generator='tools/build_motor_fuse_pdf.py',renders=pages,visual_review_complete=False),indent=2)+'\n',encoding='utf-8')
    print('PDF',len(doc),'pages',OUT.stat().st_size,'bytes',flush=True);assert len(doc)==5,len(doc)
if __name__=='__main__':main()
