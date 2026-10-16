"""Author and render a four-page French notice for the motor distribution block."""
from pathlib import Path
import json,sys,hashlib
import pymupdf
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate,Spacer,Image,PageBreak
from build_heatsink_pdf import p,table,banner,GREY
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/repartition-moteurs'
OUT=BASE/'notices/notice-repartition-moteurs-v3.pdf';TMP=ROOT/'tools/temp/motor-splitter-review/pdf'
def ref(label,url):return p(f'<link href="{url}" color="#174969"><b>{label}</b></link>','small')
def footer(c,d):
    c.saveState();c.setStrokeColor(colors.HexColor('#ccdbe4'));c.line(18*mm,17*mm,192*mm,17*mm)
    c.setFont('HV3',7.4);c.setFillColor(GREY);c.drawString(18*mm,12*mm,'Drone V3 | Répartition après relais | 14 octobre 2026 | Etude non testée')
    c.drawRightString(192*mm,12*mm,str(d.page));c.restoreState()
def main():
    sys.stdout.reconfigure(encoding='utf-8');TMP.mkdir(parents=True,exist_ok=True)
    cat=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'));cal=json.loads((BASE/'calculs.json').read_text(encoding='utf-8'))
    assert json.loads((BASE/'3D/validation-freecad.json').read_text(encoding='utf-8'))['all_passed']
    story=[p('Répartiteur des deux<br/>départs moteurs','title'),p('nVent ERIFLEX UD-80A - article 569010 - une unité avec capot'),
        banner('<b>Sélection d’étude, non achetée et non testée.</b> Jonction positive passive après le D1D100, avant les deux porte-fusibles. Une arrivée, deux sorties utilisées sur six. Aucun négatif dans ce bloc.'),Spacer(1,4*mm),
        table([['Donnée fabricant','Valeur / portée'],['Courant nominal','80 A IEC / 85 A UL/CSA ; pas une limitation active'],['Connexions','1 entrée 6-16 mm² ; 2 grandes sorties 2,5-16 et 4 petites 2,5-6 mm², toutes communes'],
            ['Enveloppe nominale / masse','H69 × W30 × D46 mm, pattes comprises ; 0,07 kg, hors fils et fixations'],['Boîtier et capot','Thermoplastique, cuivre étamé, capot articulé inclus ; IP20, sans étanchéité']],[56,118]),Spacer(1,3*mm),
        Image(str(BASE/'3D/eriflex-ud80a-implantation-v3.png'),width=124*mm,height=100.75*mm),
        p('Géométrie officielle obtenue via le service CAD nVent. Original STEP conservé intact. Vue V3 tournée/repositionnée ; capot affiché bleu opaque pour lisibilité. Fils, embouts et vis de panneau absents.','small'),PageBreak()]
    story += [p('Raccordement et serrage','title'),
        banner('<b>MiniBus D+ P3 → relais (+2 puis 1) → entrée IN du UD80A.</b><br/>Petites sorties S1 et S4 → fils 12 AWG des deux 5065 → ATO30 → ESC. Repères S1/S4 propres au projet ; les autres sorties restent sans conducteur.'),Spacer(1,3*mm),
        p('Un fil par orifice utilisé. Arrivée cuivre 6 mm² proposée ; fils des supports 12 AWG, environ 3,31 mm², dans la plage des petites sorties. Les fils ESC 16 AWG, environ 1,31 mm², sont sous le minimum métrique 2,5 mm² : <b>pas de connexion directe de ces fils dans le bloc</b>.'),
        p('Tableau IEC de la notice IP7802_M, page 1','sub'),
        table([['Groupe de borne','Sections','Couple','Dénudage'],['Entrée IN','6-16 mm²','3,5 N·m','17,0 mm'],['Grandes sorties L1/L2','2,5-16 mm²','3,5 N·m','17,0 mm'],['Petites sorties S1-S4','2,5-6 mm²','1,2 N·m','10,2 mm']],[59,43,36,36]),Spacer(1,3*mm),
        p('La page UL/CSA 2 donne pour entrée/grandes sorties <b>19,5 in-lb ≈ 2,20 N·m et 0,36 pouce ≈ 9,14 mm</b> ; pour petites sorties 10,6 in-lb ≈ 1,20 N·m et 0,40 pouce ≈ 10,16 mm. Les grosses bornes présentent une différence réelle entre tableaux : vérifier le régime applicable et la notice reçue avant câblage. Ne pas mélanger couple IEC et longueur UL.','small'),
        p('Préparation et fixation','sub'),p('Batterie et équilibrage débranchés : choisir fil/embout selon section réelle et classe des brins, sans embout 4 mm² automatiquement attribué au 12 AWG. Confirmer l’entrée souple exacte, la fiche citant le multibrins compact. Dénuder sans blesser les brins, insérer entièrement, serrer avec un outil contrôlé et refermer le capot.'),
        p('La notice demande de serrer aussi les vis des orifices inutilisés selon leur groupe, et de maintenir l’entrée à environ <b>15 cm du bloc</b>. Prévoir retenue mécanique et accès à l’outil. Fixation panneau proposée, sans rail DIN ajouté.'),
        p('Repère de fixation 54 mm, cote 4,5 mm avec annotation M5 : mesurer passage et géométrie sur le lot avant de choisir la visserie ou percer. Réserver le débattement du capot. IP20 ne permet pas eau ou copeau conducteur.','small'),PageBreak()]
    story += [p('Courant et coordination','title'),
        banner('<b>Scénario moteur : 40 A au total, hypothèse non mesurée.</b> Charge nominale 40/80 = 50 %. La courbe de déclassement ne garantit pas 80 A avec notre arrivée 6 mm² ou n’importe quel montage.'),Spacer(1,3*mm),
        table([['Air local*','Coefficient fabricant','80 A × coefficient','Scénario 40 A'],
            *[[f"{r['ambient_C']} °C",str(r['coefficient']).replace('.',','),f"{r['computed_IEC_allowance_A']:.1f} A".replace('.',','),'Dans la valeur' if r['scenario40A_within_nominal'] else 'Hors valeur'] for r in cal['derating']]],[40,46,46,42]),Spacer(1,3*mm),
        p('*Environnement du bornier dans l’armoire, température de fonctionnement visée 85 °C dans le guide fabricant. L’air local de l’étude V3 est 40 °C ; à 75 °C, la valeur calculée 37,6 A ne couvre plus le scénario. Résistance de contact non publiée ici : aucune perte ou autonomie garantie inventée.','small'),
        p('Tronc et arrivées avant les ATO','sub'),p('Le tronc commun et les fils avant les petits fusibles restent coordonnés avec le principal MIDI 60 A. Rapprocher les deux supports de la dérivation ; arrivées très courtes, isolées et retenues. Le 12 AWG en amont de l’ATO30 n’est pas automatiquement qualifié par le principal.'),
        p('Grandeurs de défaut distinctes','sub'),p('Le fabricant publie <b>Icw 3 kA pendant 1 s, Ipk 22 kA et SCCR jusqu’à 100 kA</b>. Ce bloc ne coupe pas le courant. La notice UL lie le SCCR 100 kA à un fusible <b>200 A Class J ou T, 600 V maximum</b> ; cette association n’est pas notre MIDI 60 A. Ne pas transférer sa qualification aux ATO à 1 000 A ou au SSR.','small'),
        p('Contrôler continuité, polarités et isolement hors tension, puis essai limité. Mesurer courants, chutes des trois connexions utilisées, températures et tenue sous vibration. Qualifier défauts, freinage/régénération et perte d’un départ ; aucun court-circuit volontaire du pack.','small'),PageBreak()]
    story += [p('Achat, CAO et références','title'),
        p('Alternative française identifiée : <b>RS 277-6180, article 569010, 17,61 € HT / 21,13 € TTC</b>, stock annoncé sur la page consultée le 14 octobre 2026. Frais de traitement et livraison à vérifier ; aucune commande. Recherche Amazon.fr : <b>pas d’offre exacte ni ASIN confirmé</b>. Ne pas assimiler les UKK80 génériques à cette référence.'),
        p('Conditionnement : une unité avec capot ; ni fil, embout, rail DIN ou fixation de châssis supposé fourni. Retour PLCtalk 2020 : un utilisateur dit employer le UD80A et discute son SCCR ; référence à la notice corroborée. L’avis marchand « test3 » signé administrateur est exclu ; aucun essai vidéo exact avec mesures V3 trouvé.','small'),
        table([['STEP livré','Solides / faces'],*[[m['title'],f"{m['validation']['solids']} / {m['validation']['faces']}"] for m in cat['models']]],[133,41]),Spacer(1,3*mm),
        p('Imports <b>FreeCAD sans interface</b> : validité, solides fermés et enveloppes contrôlés. Original AP214 extrait du ZIP et conservé intact ; dérivés par rotation/translation, retrait ou décalage du capot. Réimports : volumes et enveloppes précises contrôlés. Aucun test GUI FreeCAD/CAD View ou matériel revendiqué.','small'),
        p('Le natif regroupe seulement trois solides ; toutes les vis, textures et inscriptions ne sont pas représentées comme détails indépendants. Géométrie de référence fabricant pour implantation, pas un dossier de fabrication ou une simulation électrique.','small'),
        p('Sources et notices originales','sub'),
        ref('nVent : fiche produit UD-80A / 569010','https://www.nvent.com/en-us/ERIFLEX/products/EFSUD-80A'),
        ref('nVent : instruction IP7802_M, tableaux IEC/UL','https://nvent.widen.net/content/vhxyvvgeqg/original/ip7802.pdf'),
        ref('Fiche nVent française 2023 via RS','https://docs.rs-online.com/e8ac/A700000010539200.pdf'),
        ref('RS France : référence et offre exacte','https://fr.rs-online.com/web/p/blocs-de-distribution/2776180'),
        p('Documents fabricant archivés inchangés : instructions, fiches FR/EN, copies historiques, spécification UD 2022 et catalogue P1215C. Photos et plans sont conservés. URL, statuts, SHA256, original CAD et réserves : sources.json, assets.json, cotes.md et JSON voisins des STEP.','small')]
    SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=18*mm,bottomMargin=23*mm,
        title='Drone V3 - Repartition moteurs UD80A',author='Projet Drone V3').build(story,onFirstPage=footer,onLaterPages=footer)
    doc=pymupdf.open(OUT);pages=[]
    for i,page in enumerate(doc):
        png=TMP/f'page-{i+1}.png';page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(png)
        pages.append(dict(page=i+1,render=str(png.relative_to(ROOT)).replace('\\','/'),chars=len(page.get_text())))
    OUT.with_suffix('.json').write_text(json.dumps(dict(file=OUT.name,pages=len(doc),sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),generated_on='2026-10-14',
        generator='tools/build_motor_splitter_pdf.py',renders=pages,visual_review_complete=False),indent=2)+'\n',encoding='utf-8');print('PDF',len(doc),'pages',OUT.stat().st_size,'bytes',flush=True);assert len(doc)==4,len(doc)
if __name__=='__main__':main()
