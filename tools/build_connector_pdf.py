"""Create and render the four-page French connector notice."""
from pathlib import Path
import json,sys,hashlib
import pymupdf
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate,Spacer,Image,PageBreak
from build_heatsink_pdf import p,table,banner,GREY
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/connecteurs-alimentation'
OUT=BASE/'notices/notice-connecteurs-xt60h-v3.pdf';TMP=ROOT/'tools/temp/connectors-review/pdf'
def ref(label,url):return p(f'<link href="{url}" color="#174969"><b>{label}</b></link>','small')
def footer(c,d):
    c.saveState();c.setStrokeColor(colors.HexColor('#ccdbe4'));c.line(18*mm,17*mm,192*mm,17*mm)
    c.setFont('HV3',7.4);c.setFillColor(GREY);c.drawString(18*mm,12*mm,'Drone V3 | Connecteurs des départs ESC | 14 octobre 2026 | Etude non testée')
    c.drawRightString(192*mm,12*mm,str(d.page));c.restoreState()
def main():
    sys.stdout.reconfigure(encoding='utf-8');TMP.mkdir(parents=True,exist_ok=True)
    cat=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'))
    assert json.loads((BASE/'3D/validation-freecad.json').read_text(encoding='utf-8'))['all_passed']
    story=[p('Prises des deux<br/>départs moteurs','title'),p('Deux AMASS XT60H-F avec capots - contacts femelles côté faisceau'),
        banner('<b>Choix d’étude, non acheté et non testé.</b> Chaque prise alimente un seul ESC arrière. Le XT60 mâle est déjà monté sur chaque Hobbywing WP16BL30 G2 selon la photo constructeur. Contrôler contacts et polarités à réception.'),Spacer(1,3*mm),
        table([['Besoin réel','Fonction / statut'],['2 × XT60H-F + 2 capots','Compléments côté faisceau ; positif après chaque ATO30, retour négatif séparé'],
            ['0 × M supplémentaire obligatoire','Interface déjà incluse dans les kits ESC ; modèle M de référence pour l’accouplement'],
            ['Référence de travail : 30 A / prise','Scénario 20 A par ESC, non mesuré et sans limitation active'],
            ['F : 24,95 × 16,40 × 9,20 mm','Catalogue AMASS 2026, capot compris, hors fils et dégagement']],[60,114]),Spacer(1,3*mm),
        Image(str(BASE/'3D/amass-xt60h-f-detaille.png'),width=117*mm,height=95.06*mm),
        p('Reconstruction colorée : corps détrompé jaune, logements femelles dorés, capot gris sombre, rainures et marquages. Enveloppe fabricant ; détails internes estimés. Ce modèle ne constitue pas une pièce mesurée ni une CAO native AMASS.','small'),PageBreak()]
    story += [p('Raccordement et montage','title'),
        banner('<b>D1D100 sortie 1 → UD80A → deux supports 5065 / ATO30.</b><br/>Après chaque fusible : + de son XT60H-F → XT60 de son ESC.<br/>Chaque - du F → retour indépendant D- N1 ou N3.'),Spacer(1,3*mm),
        p('N2 reste le retour pack, N4 l’électronique. Pas de négatif dans le UD80A et pas de fusible dans les trois phases moteur. Les deux pôles d’une prise portent le courant d’un même ESC. Une seule prise commune aux deux ESC ne convient pas à cette proposition.'),
        p('Section et retenue','sub'),p('AMASS recommande du <b>12 AWG, environ 3,31 mm² de cuivre</b> : queues courtes proposées, longueurs après implantation. Les ESC gardent leurs fils 16 AWG / 75 mm. Les exemples précédents de 4 mm² ne prouvent pas qu’ils entrent dans ces godets ; ni 4 ni 6 mm² forcés, aucun brin retiré. Raccords et cosses restent à sélectionner.'),
        p('Le capot isole les godets, mais sa tenue à la traction n’est pas publiée. Retenir le faisceau sur le châssis sans effort sur les soudures et garder accès aux prises et fusibles.','small'),
        p('Procédure du projet, hors tension','sub'),
        p('<b>1.</b> Débrancher batterie et équilibrage. Préparer les prises neuves détachées ; ne pas modifier les fils du pack pendant cette étude.'),
        p('<b>2.</b> F = logements métalliques femelles, M = broches mâles. Lire + et - sur la pièce ; les vues avant et arrière s’inversent. Ne pas décider à partir du seul mot « mâle » d’une annonce.'),
        p('<b>3.</b> Passer les fils dans le capot avant soudure, présenter le dénudage dans les godets, conserver tous les brins. Aucun temps, dénudage ou réglage de fer officiel du lot confirmé.'),
        p('<b>4.</b> Souder séparément, éviter pont d’étain et chauffe prolongée du PA. Un complément neuf hors tension peut maintenir les contacts ; jamais une batterie comme gabarit.'),
        p('<b>5.</b> Laisser refroidir, vérifier godets, brins, isolation et absence de contact mobile/plastique déformé. Clipser le capot sans forcer ; débrancher ensuite en tenant les corps.'),
        p('<b>6.</b> Contrôler continuité, isolement et polarités, puis première alimentation limitée et supervisée. Qualifier chute de tension, températures, pointes et vibrations sur le faisceau fini.'),PageBreak()]
    story += [p('Cotes et valeurs de courant','title'),
        table([['Source','Longueur F / M','Largeur / épaisseur'],['Catalogue AMASS 2026 p.15','24,95 / 23,85 mm','16,40 / 9,20 mm'],
            ['Plan page produit, arrondis','25,00 / 23,90 mm','16,40 / 9,20 mm'],['Ancienne fiche V1.2','23,50 / 23,80 mm','16,40 / 9,20 mm']],[70,52,52]),Spacer(1,3*mm),
        p('Les STEP suivent l’enveloppe du catalogue 2026. Entraxe 7,20 mm repris de V1.2 comme hypothèse actuelle ; profils, diamètres, profondeur de logements, clips et répartition des longueurs sont estimés. Réserver 25 mm pour F hors fils et dégagement, puis mesurer le lot avant support ou usinage.','small'),
        table([['Document','Donnée publiée / interprétation'],['V1.2 AMASS','30 A RC / 60 A MC ; durée MC non publiée ; 0,50 mΩ CR ; 1 000 usages'],
            ['AMASS 2026, page 15','35 A MAX (12 AWG / Δ &lt; 85 °C) ; 100 cycles ; IP40 ; tenue 500 V DC'],
            ['Page produit actuelle','35 A MAX / Δ &lt; 85 K ; PA, laiton doré. Unité CR « MΩ » incohérente : valeur non adoptée']],[49,125]),Spacer(1,3*mm),
        banner('<b>Le « 60 A » marchand n’est pas retenu comme courant continu garanti.</b> Ni le catalogue ni la référence prudente 30 A ne qualifient les fils, les soudures ou notre confinement. L’écart Δ85 n’est pas une température visée pour le robot.'),Spacer(1,2*mm),
        p('Pertes : analyse conditionnelle à 20 A','sub'),
        table([['R supposée par pôle accouplé*','Chute sur deux pôles','Pertes par prise'],['0,50 mΩ','20 mV','0,40 W'],['1,20 mΩ','48 mV','0,96 W']],[74,50,50]),Spacer(1,2*mm),
        p('*Deux valeurs d’analyse, pas une résistance garantie du lot actuel ; portée exacte de la CR historique non précisée. Formules ΔV = 2IR et P = 2I²R. Doubler les pertes pour deux branches identiques ; exclut fils, soudures et variations thermiques.','small'),
        p('40 A au total ne garantit pas 20 A sur chaque ESC. Les ATO30 peuvent laisser durer une surcharge ; les 100 A de pointe ESC ne qualifient pas la prise. Mesurer courant RMS, impulsions, freinage/régénération et échauffement.'),
        p('La paire XT60 commune du pack voit environ <b>44,39 A</b> dans le scénario 40 A moteurs + 25 W à 6,4 V / 90 % + 0,05 A auxiliaire. Révision inconnue, dépasse la référence 30 A : <b>interface à qualifier ou revoir séparément</b>.','small'),PageBreak()]
    story += [p('Achat, CAO et références','title'),
        p('Lot proposé : <b>SoloGood / AMASS, 10 paires XT60H, ASIN B074PN6N4K</b>. Titre et boutique retrouvés sur Amazon.com. Prix, stock, vendeur et livraison Amazon.fr non confirmés. Besoin : deux F avec capots ; un petit lot peut être plus économique.'),
        p('Si le lot annoncé est conforme : dix F et dix M, capots à vérifier ; deux F utilisés, huit F et dix M en réserve. Les capots sont optionnels au catalogue fabricant : confirmer leur présence dans l’offre. Aucune commande.','small'),
        table([['STEP disponible','Solides / faces'],*[[m['title'],f"{m['validation']['solids']} / {m['validation']['faces']}"] for m in cat['models']]],[137,37]),Spacer(1,3*mm),
        p('Réimports CadQuery et <b>FreeCAD sans interface</b> : validité, solides fermés et enveloppes contrôlés. Couleurs, volumes et empreintes SHA256 vérifiés. Engagement illustratif 7,5 mm sans collision volumique ; pas un ajustement ou un test GUI CAD View. Le câblé utilise deux conducteurs continus, gaines et soudure illustratives ; ses bouts dénudés sont intentionnels.','small'),
        p('RCCrawler 2020 : utilisateurs apprécient le capot et discutent maintien/marquages. DashCamTalk 2023 : fabrication de câbles avec cet ASIN. Retours qualitatifs, sans qualification des courants V3. Vidéo SoloGood du 8 octobre 2019 identifiée sur la soudure XT60H ; vidéo du vendeur, non visionnée intégralement ici.','small'),
        ref('AMASS : page produit et plan courant','https://www.china-amass.com/biao/283.html'),
        ref('AMASS : catalogue 2026, XT60H page 15','https://www.china-amass.com/public/upload/20260207/7fa24f5a6f35ec66c7a115c07a34ab06.pdf'),
        ref('AMASS : ancienne fiche V1.2 via Shoptronica','https://www.shoptronica.com/ficheros/XT60H.pdf'),
        ref('Amazon.com : lot identifié B074PN6N4K','https://www.amazon.com/dp/B074PN6N4K'),
        p('PDF originaux inchangés, photos, URL et statuts d’accès conservés. Cotes, notice détaillée de montage, avis, calculs et réserves : fichiers Markdown/JSON du dossier. Aucun essai matériel ni performance de vitesse/autonomie validée.','small')]
    SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=18*mm,bottomMargin=23*mm,
        title='Drone V3 - Connecteurs AMASS XT60H',author='Projet Drone V3').build(story,onFirstPage=footer,onLaterPages=footer)
    doc=pymupdf.open(OUT);pages=[]
    for i,page in enumerate(doc):
        png=TMP/f'page-{i+1}.png';page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(png)
        pages.append(dict(page=i+1,render=str(png.relative_to(ROOT)).replace('\\','/'),chars=len(page.get_text())))
    OUT.with_suffix('.json').write_text(json.dumps(dict(file=OUT.name,pages=len(doc),sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),generated_on='2026-10-14',
        generator='tools/build_connector_pdf.py',renders=pages,visual_review_complete=False),indent=2)+'\n',encoding='utf-8')
    print('PDF',len(doc),'pages',OUT.stat().st_size,'bytes',flush=True);assert len(doc)==4,len(doc)
if __name__=='__main__':main()
