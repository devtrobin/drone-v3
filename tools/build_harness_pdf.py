"""Eight-page power-harness notice, with all pages rendered for visual review."""
from pathlib import Path
import json,hashlib,sys,html
import pymupdf
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate,Spacer,Image,PageBreak,Table
from build_heatsink_pdf import p as base_p,table as base_table,banner as base_banner,GREY
from harness_text import format_text
from build_harness_data import PARTS,TE,HTT,HTM,KLAUKE,AUPROTEC,ANCOR
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants';COMMON=BASE/'faisceau-puissance'
OUT=COMMON/'notices/notice-faisceau-puissance-v3.pdf';TMP=ROOT/'tools/temp/harness-review/pdf'
def p(s,style='body'):return base_p(format_text(s),style)
def table(rows,widths):return base_table([[format_text(c) for c in row] for row in rows],widths)
def banner(s):return base_banner(format_text(s))
def read(pth):return json.loads(pth.read_text(encoding='utf-8'))
def footer(c,d):
    c.saveState();c.setStrokeColor(colors.HexColor('#ccdbe4'));c.line(18*mm,17*mm,192*mm,17*mm)
    c.setFont('HV3',7.4);c.setFillColor(GREY);c.drawString(18*mm,12*mm,'Drone V3 | Faisceau de puissance | 14 octobre 2026 | Etude non testée')
    c.drawRightString(192*mm,12*mm,str(d.page));c.restoreState()
def pic(folder,name,width=82):
    path=BASE/folder/'3D'/name
    with PILImage.open(path) as im:w,h=im.size
    return Image(str(path),width=width*mm,height=width*h/w*mm)
def duo(a,b):
    t=Table([[a,b]],colWidths=[87*mm,87*mm]);t.setStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0)])
    return t
def ref(label,url):return p(f'<link href="{html.escape(url,quote=True)}" color="#174969"><b>{label}</b></link>','small')
def main():
    sys.stdout.reconfigure(encoding='utf-8');TMP.mkdir(parents=True,exist_ok=True)
    cat=read(COMMON/'3D/catalogue.json');fc=read(COMMON/'3D/validation-freecad.json');calc=read(COMMON/'calculs.json')
    assert fc['all_passed'] and len(fc['checks'])==cat['model_count']==14
    story=[p('Faisceau de puissance<br/>Cosses, raccords et maintien','title'),
        p('Deux moteurs arrière - deux branches protégées - tronc principal 6 mm²'),
        banner('<b>Sélection d’étude : huit références, aucun achat ni essai matériel.</b> Les recherches Amazon.fr sont conservées ; aucune offre exacte, aucun prix TTC ni délai français confirmé.'),Spacer(1,4*mm),
        table([['Référence','Emploi','Besoin d’étude'],
            ['Ancor 312303','Œillet #10, fils 12 AWG sur MiniBus','2 retours + 1 conditionnelle Pi ; pack3'],
            ['Klauke 95R4','6 mm², œillet Ø4,3 ; relais','2'],
            ['Klauke 95R5','6 mm², œillet Ø5,3 ; MIDI / MiniBus','4 + 1 conditionnelle entrée MIDI'],
            ['Ancor 309203','12-10 AWG ; rallonge positive après ATO30','2 ; pack3'],
            ['TE ATUM-8/2-0-STK','Gaine adhésive noire 4:1','1 barre1,2m ; coupes à définir'],
            ['HT T18R 111-01919','Collier PA66 naturel100 ×2,5','12 d’implantation ; pack fabricant100'],
            ['HT MB2 151-28210','Embase noire à visM4','8 d’implantation ; pack fabricant100'],
            ['AUPROTEC FLRY-B6','Fil principal6mm², rouge/noir','Provision2m/couleur ; lot exact ouvert']],[45,76,53]),Spacer(1,4*mm),
        p('Les 12 AWG BNTECHGO, prises XT60H-F, trois 5065, fusibles, bus et relais sont déjà documentés. Ils ne sont pas rachetés par cette sélection. Vis de châssis, embout UD et outillage sont à arrêter selon le lot et l’atelier.'),
        p('La liste de coupe et la quantité des colliers suivent l’implantation. Cette notice précise les raccordements et les contrôles ; elle ne prouve pas la tenue à40 km/h ni l’autonomie.','small'),PageBreak()]
    story += [p('Raccordements et quantités','title'),
        p('Le courant positif principal traverse MIDI puis D+. Le relais interrompt les deux moteurs, puis le UD-80A répartit vers deux ATO30. Les retours moteurs sont indépendants sur D−.'),
        table([['Repère','Chemin','Extrémités prévues'],
            ['CP1+ /6mm²','MIDI sortie → D+P2','95R5 /95R5'],
            ['CP2+ /6mm²','D+P3 → relais +2','95R5 /95R4'],
            ['CP3+ /6mm²','relais1 → UD IN','95R4 /borne UD à qualifier'],
            ['CP0+ /6mm²','interface pack → MIDI entrée','Interface ouverte /95R5 conditionnelle'],
            ['CP0− /6mm²','interface pack → D−N2','Interface ouverte /95R5'],
            ['CM1− /12AWG','XT60F1 → D−N1','Godet XT60 /312303'],
            ['CM2− /12AWG','XT60F2 → D−N3','Godet XT60 /312303'],
            ['CM1+ /12AWG','5065 ATO30 n°1 → XT60F1','309203 /godet XT60'],
            ['CM2+ /12AWG','5065 ATO30 n°2 → XT60F2','309203 /godet XT60']],[34,70,70]),Spacer(1,3*mm),
        p('UD S1/S4 : fils12AWG inclus des5065, un fil par port. Troisième312303 possible sur l’arrivée du5065 Pi en D+P4. D+P1 libre ; section et terminaisons du retour électronique D−N4 à définir.'),
        banner('<b>Œillet et filetage sont deux informations différentes.</b> Vis #8-32 UNC du relais, écrous #10-32 UNF des MiniBus et écrous M5×0,8 MIDI conservés. Les œillets M4/M5 des cosses ne permettent pas de remplacer ces vis ou écrous par métriques.'),Spacer(1,2*mm),
        p('Sept cosses6mm² et gaines si la cinquième95R5 est retenue côté pack. Huit morceaux20mm constituent une réserve indicative, pas des longueurs de pose. Le point d’interface batterie reste à concevoir et qualifier.','small'),PageBreak()]
    story += [p('Cosses : cotes et fidélité','title'),
        table([['Grandeur','95R4 /6mm²','95R5 /6mm²'],['d1 /a /b','4 /9 /9,5 mm','4 /9 /9,5 mm'],
            ['d2 /d4','4,3 /6 mm','5,3 /6 mm'],['c1 /c2 /l','5 /5,5 /18 mm','6 /6 /19 mm'],
            ['Encombrement reconstruit','23 mm = c1+l','25 mm = c1+l']],[66,54,54]),Spacer(1,2*mm),
        p('<b>La cote l part du centre du trou</b> sur le dessin Klauke archivé. Ne pas la reprendre comme longueur totale. Les valeurs6mm² concordent avec le tableau actuel ; paume2mm, transition, rayons et trou d’inspectionØ1,4 sont reconstruits.'),
        duo(pic('cosses-puissance/klauke-95r5','cosse-klauke-95r5-6mm2.png'),pic('cosses-puissance/ancor-312303','cosse-ancor-312303-12awg-num10.png')),Spacer(1,2*mm),
        p('À gauche : 95R5 non sertie. À droite : Ancor312303, forme extérieure entièrement estimée. L’œillet #10, la plage12–10AWG et la construction cuivre étamé /gaine adhésive sont documentés ; trouØ5,2 et encombrement24 ×9,6 ×5,9 ne sont pas des cotes fabricant.','small'),
        p('La 95R4 passe nominalement une tige#8 deØ4,166 ; la95R5 passe nominalement M5 et#10. Vérifier les bornes réelles : largeur9,5, appui, cloisons et longueur utile de vis. La seule comparaison des diamètres ne qualifie pas l’assemblage.'),
        p('La gamme Klauke est donnée pour fins brins classe5 ; vérifier la classe acceptée du câble acheté. Pour Ancor, la compatibilité avec le très fin filBNTECHGO680 ×0,08mm doit être vérifiée avec outil, fil et gaine réels. Aucun certificat d’essai de cet ensemble trouvé.','small'),PageBreak()]
    story += [p('Raccords et gaine adhésive','title'),
        p('<b>Ancor309203 :</b> un fil12AWG par côté, un raccord sur chaque rallonge positive après ATO30. Plage catalogue3–5mm² : elle ne couvre pas le6mm² principal.'),
        duo(pic('raccords-12awg','raccord-ancor-309203-coupe.png'),pic('gaine-thermoretractable','gaine-te-atum-8-2-retreinte-libre-coupe.png')),Spacer(1,2*mm),
        p('Coupes volontaires pour lire les couches. Le raccord Ancor est estiméØ6,1 ×30mm, canon15mm ; aucune cote complète publiée. L’adhésif ambre est une couleur pédagogique, sa teinte réelle n’est pas documentée.','small'),
        table([['TE ATUM8/2 noire','Valeur publiée'],['Øint fourni /libre rétreint','≥8 /≤2mm'],['Paroi après rétraction libre','1,0 ±0,3mm total ; adhésif0,5mm nominal'],
            ['Retrait longitudinal','0 à−15% (planA2,2023)'],['Températures gaine','Début80°C ; rétraction complète110°C ; service−55..+110°C'],['Longueur STK','1,2m, conditionnement vendeur à vérifier']],[65,109]),Spacer(1,3*mm),
        p('Le canon KlaukeØ6 et le filØ4,7 sont nominalement dans la plage8/2. Passer la gaine avant sertissage ; recouvrir le canon et la gaine du fil en laissant la paume de contact dégagée. Mesurer les transitions et le recouvrement nécessaire.'),
        banner('Les modèles montrent des états <b>libres</b>. Une gaine installée sur le filØ4,7 ne descend pas àØ2 et sa paroi ne reprend pas automatiquement1mm. Les40/36mm dessinés sont des exemples ; épaisseur fournie et retrait réel de la coupe non mesurés.'),PageBreak()]
    rows=[['Aller simple*','Courant commun','Chute idéale','Pertes cuivre']]
    for r in calc['loops']:rows.append([f"{r['one_way_length_m']:.2f}m",f"{r['current_A']:.2f}A",f"{r['drop_V']:.3f}V",f"{r['loss_W']:.2f}W"])
    story += [p('Câble principal6mm²','title'),
        p('AUPROTEC FLRY-B : cuivreECu nu recuit, PVC, diamètre extérieur environ4,7mm ; brinsØmax0,300mm. Le nombre et le toronnage ne sont pas publiés. La page primaire annonce−40 à+70°C et50VAC/60VDC ; les annonces+85/+105°C d’autres variantes ne sont pas reprises.'),
        table([['Donnée d’achat','Statut'],['Provision d’étude','2m rouge +2m noir ; longueurs à arrêter'],['Référence primaire consultée','044906 : rouge6m, pas le lot2m ni une paire'],['ASIN candidatB00HDGB6GG','Reprises marchandes : rouge5m ; Amazon bloqué, exactitude non confirmée'],['Entrée UD-80A','Minimum6mm² ; 10AWG≈5,26mm² insuffisant pour cette plage']],[59,115]),Spacer(1,3*mm),
        pic('cable-principal-6mm2','cable-auprotec-flryb-6mm2-coupe-equivalente.png',92),
        p('Âme CAO pleine d’aire équivalente6mm², diamètre2,764mm. Ce n’est pas le diamètre réel du faisceau ni un nombre de brins mesuré. Coupe de gaine volontaire ; longueur100mm et dénudage10mm illustratifs.','small'),
        table(rows,[39,42,46,47]),Spacer(1,2*mm),
        p('*Boucle rouge/noir de même longueur ; cuivre idéal à20°C, ρ supposée0,01724Ω·mm²/m. R=2Lρ/6. Contacts, température et pose exclus. Courant d’étude44,39A =40 +25/(6,4 ×0,9) +0,05, non imposé et non mesuré. Ce calcul ne donne pas le courant admissible du câble.','small'),
        p('<b>Interface communeXT60 de batterie toujours à qualifier.</b> Le câble6mm² ne règle pas à lui seul la tenue de cette prise ; pas d’insertion forcée dans ses godets, pas de modification du pack.'),PageBreak()]
    story += [p('Maintien du faisceau','title'),
        duo(pic('maintien-faisceau/colliers','collier-ht-t18r-11101919.png'),pic('maintien-faisceau/embases','embase-ht-mb2-15128210.png')),Spacer(1,3*mm),
        table([['Composant','Données documentées'],['T18R111-01919','PA66 naturel ; 100 ×2,5 ×1mm ; tête actuelle4,8 ×4,45 ×3,7'],
            ['T18R usage','Intérieur ; Øboucle1,5–22mm ;−40..+85°C ; non réutilisable ; non stabiliséUV'],['T18R effort','Résistance minimale de boucle80N, pas une force de pose'],
            ['MB2151-28210','PA66 noir ; 20,5 ×12,5 ×3,3mm ; trouØ5 pour visM4'],['MB2 passages','Colliers≤5mm, familleT18–T50 ; une fixation, deux directions d’entrée'],
            ['Provision d’étude','12colliers /8embases ; vis et implantation à déterminer']],[49,125]),Spacer(1,3*mm),
        p('MB2 est une embase à vis ; aucun adhésif n’est inclus dans le modèle. Choisir longueurM4, rondelle et éventuel écrou selon le châssis. Le trou5mm ne signifie pas fixationM5.'),
        p('La denture, le cliquet et la pointe du collier sont reconstruits. Son plan de famille2025 indique T1,1±0,2 et tête légèrement différente ; la référence actuelle naturelle est modélisée avec les cotes de sa fiche. Sur MB2, rayons et position du trou sont estimés autour de l’enveloppe et des passages du plan.'),
        p('Retenir les fils avant les raccords en laissant une boucle de service. Éviter écrasement, arêtes, roues, courroies et engrenages ; dégager les zones chaudes. Couper les queues proprement. Des colliers serrés ne prouvent pas la qualité d’une connexion électrique.','small'),PageBreak()]
    story += [p('Préparation et sertissage','title'),
        banner('Les modèles ne sont pas des calibres de sertissage. Choisir le système <b>cosse +fil +outil</b> validé par ses fabricants ; réaliser des éprouvettes avec le fil effectivement reçu.'),Spacer(1,3*mm),
        p('<b>1.</b> Pack et équilibrage débranchés : implanter les composants, relever chemins et longueurs. Prévoir maintien sans tension sur les godets ou bornes. Contrôler variante et matière, diamètre du fil, trou de cosse et dégagement.'),
        p('<b>2.</b> Passer capots et gaines avant terminaison. Régler le dénudage selon le canon réel et sa procédure ; ne pas retirer de brins pour faire entrer le fil. Les10mm dessinés et les20mm de réserve de gaine ne sont pas des instructions de coupe.'),
        table([['Famille','Outillage et contrôle'],['Ancor12–10AWG','Outil pour heat-shrink, matrice adaptée. Catalogue2020 p.54 :703010, single crimp22–8AWG. La703030 y est décrite pour nylon/vinyle. Vérifier la procédure actuelle du lot.'],
            ['Klauke6mm²','Outil pour cosses tubulairesCu standard6mm². Tableau imprimép.38 : K2 parmi les outils0,75–16mm² ; confirmer l’appairage95R4/95R5 avec le câble reçu. Ce n’est pas la matrice isolée jaune Ancor.']],[43,131]),Spacer(1,3*mm),
        p('<b>3.</b> Vérifier insertion complète et tous les brins engagés ; utiliser le trou de contrôle Klauke. Sertir sans ajout de soudure non prévu. Pour309203, traiter chaque côté selon l’outil ; un sertissage au centre ne remplace pas les deux jonctions.'),
        p('<b>4.</b> Contrôler sur éprouvettes tenue mécanique, aspect et section du sertissage, résistance et échauffement. La force d’essai suit la procédure du système ; aucune force universelle n’est inventée. La gaine rétreinte n’est pas le contact de puissance.'),
        p('<b>5.</b> Rétracter localement selon le produit reçu : Ancor135°C annoncés ; ATUM80°C début et110°C pleine récupération. Ces températures ne sont pas la consigne du pistolet. Préserver le PVC et les éléments proches, inspecter adhésif, isolation et absence de brins libres.'),
        p('<b>6.</b> Monter les cosses avec la visserie d’origine, appui propre et couple du lot. Une seule cosse prévue par borne du relais, sans empilement arbitraire. Ne pas masquer la paume par la gaine.'),
        p('<b>7.</b> UD-80A : confirmer conducteur fin/embout. DonnéesIEC17mm/3,5Nm etUL9,14mm/2,2Nm sont des alternatives documentées à trancher pour le lot, pas une moyenne. Ces longueurs et couples ne sont pas ceux des cosses.','small'),PageBreak()]
    story += [p('Contrôles et sources','title'),
        p('<b>Avant alimentation :</b> continuité, polarités, isolement, surfaces de puissance couvertes, sertissages, appui et couples, maintien et aucun fil dans une pièce mobile. Première mise sous tension supervisée avec une alimentation limitée adaptée, puis mesures sur l’usage réel.'),
        p('Relever pointes et courants, chutes et températures des prises, cosses, fils et protections. L’étude20A par ESC /44,39A commun n’est pas une limite imposée ; ATO30 et MIDI60 ne limitent pas ces courants. Tenue des fils16AWG d’usine, ampacité du6mm², interface du pack et coordination des défauts restent ouvertes.'),
        p('<b>14STEP validés</b> après export/réimport, volumes, enveloppes et couleurs, puis contrôlés indépendamment avec FreeCAD sans interface : géométrie valide et solides fermés. Aucun essai GUI CAD View, aucun matériel mesuré. Les coupes sont volontaires et les détails non documentés sont signalés.'),
        p('Achat et retours','sub'),
        p('Amazon.fr a renvoyé pages vides/challenges ; recherches par référence conservées, aucun prix ou stock attesté. Témoignages génériques sur forums favorables à la familleAncor et discutant le choix de pince ; aucune qualification de nos SKU, fil680brins ou montage44,39A. Aucun essai YouTube pertinent de cet ensemble retenu.'),
        p('Documents de référence','sub'),
        ref('Ancor2024 : cosses p.24 et raccords p.25',ANCOR+'24/'),
        ref('Ancor2020 original, via ProjectK : p.26,27 et54','https://www.projectk.co.jp/marine/pdf/2020_ancor_catalog.pdf'),
        ref('Klauke95R4/95R5 : tableau actuel',KLAUKE),
        ref('Klauke catalogue fabricant archivé via PowerCables : PDFp.14 et40','https://www.powerandcables.com/wp-content/uploads/2018/09/Klauke-Cable-Lug-Connectors-Tools-Crimping-Cutting-Section-1.pdf'),
        ref('TE ATUM : planA2 et fiche05/24 accessibles depuis la page produit',TE),
        ref('HellermannTytonT18R : fiche actuelle et plan de famille',HTT),
        ref('HellermannTytonMB2 : page actuelle et dessin141622',HTM),
        ref('AUPROTECFLRY-B6 : page primaire rouge6m044906',AUPROTEC),
        p('Dossier local : chaque composant a sa fiche, ses cotes, sources et index3D ; dossier commun avec nomenclature, raccordements, avis, calculs et contrôles. PDF originaux conservés inchangés avecSHA256 et statuts. DocumentsTE actuels consultés via le web, téléchargements directs403 : la copieRaytronics conservée est secondaire, pas un originalTE.','small')]
    doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=18*mm,bottomMargin=23*mm,
        title='Drone V3 - Faisceau de puissance',author='Projet Drone V3')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    pdf=pymupdf.open(OUT);pages=[]
    for i,page in enumerate(pdf):
        png=TMP/f'page-{i+1}.png';page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(png)
        pages.append(dict(page=i+1,render=str(png.relative_to(ROOT)),chars=len(page.get_text())))
    OUT.with_suffix('.json').write_text(json.dumps(dict(file=OUT.name,pages=len(pdf),sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),
        generator='tools/build_harness_pdf.py',generated_on='2026-10-14',renders=pages,visual_review_complete=False),indent=2)+'\n',encoding='utf-8')
    print('PDF',len(pdf),'pages',OUT.stat().st_size,'bytes',flush=True)
    for i,page in enumerate(pdf):print('PAGE',i+1,len(page.get_text()),page.get_text().split('\n')[0],flush=True)
    assert len(pdf)==8,len(pdf)
if __name__=='__main__':main()
