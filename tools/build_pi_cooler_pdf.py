"""Create a six-page SC1148 notice and render every page for visual review."""
from pathlib import Path
import sys,json,hashlib,html
import pymupdf
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate,Image,Spacer,PageBreak
from build_heatsink_pdf import p as bp,table as bt,banner as bb,GREY
from pi_cooler_text import fmt
from collect_pi_cooler_refs import MAKER,PORTAL
from build_pi_cooler_data import HARDWARE,AMAZON
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/refroidissement-raspberry-pi-5'
OUT=BASE/'notices/notice-active-cooler-pi5-v3.pdf';TMP=ROOT/'tools/temp/pi-cooler-review/pdf'
def clean(s):return fmt(s).replace('–','-').replace('—','-')
def p(s,style='body'):return bp(clean(s),style)
def table(rows,widths):return bt([[clean(str(c)) for c in row] for row in rows],widths)
def banner(s):return bb(clean(s))
def read(pth):return json.loads(pth.read_text(encoding='utf-8'))
def pic(path,width):
    with PILImage.open(path) as im:w,h=im.size
    return Image(str(path),width=width*mm,height=width*h/w*mm)
def ref(label,url):return p(f'<link href="{html.escape(url,quote=True)}" color="#174969"><b>{label}</b></link>','small')
def footer(c,d):
    c.saveState();c.setStrokeColor(colors.HexColor('#ccdbe4'));c.line(18*mm,17*mm,192*mm,17*mm)
    c.setFont('HV3',7.4);c.setFillColor(GREY);c.drawString(18*mm,12*mm,'Drone V3 | Active Cooler SC1148 | 14 octobre 2026 | Etude non testée')
    c.drawRightString(192*mm,12*mm,str(d.page));c.restoreState()
def main():
    sys.stdout.reconfigure(encoding='utf-8');TMP.mkdir(parents=True,exist_ok=True)
    cat=read(BASE/'3D/catalogue.json');fc=read(BASE/'3D/validation-freecad.json');offer=read(BASE/'achat-amazon.json');calc=read(BASE/'calculs.json')
    assert fc['all_passed'] and len(fc['checks'])==cat['model_count']==4
    plan=pymupdf.open(BASE/'notices/RaspberryPi-ActiveCooler-plan-reference-original.pdf')
    crop=ROOT/'tools/temp/pi-cooler-review/sources/plan-cadrage.png'
    plan[0].get_pixmap(matrix=pymupdf.Matrix(2.5,2.5),clip=pymupdf.Rect(78,94,394,341)).save(crop)
    story=[p('Refroidissement du Pi5<br/>Raspberry Pi Active Cooler','title'),p('SC1148 - une unité préassemblée pour la carte de contrôle4Go'),
        banner('<b>Référence retenue, non achetée et non testée.</b> OffreAmazon.fr B0CLXZBR5P : <b>6,99€TTC</b> au14octobre2026 ; stock affiché5. Port gratuit proposé pour une première commande, à revalider dans le panier.'),Spacer(1,4*mm),
        table([['Caractéristique','Donnée fabricant janvier2026'],['Composition','Dissipateur aluminium anodisé, ventilateur radial, deux clips à ressort, pads préposés et cordon4fils'],
            ['Alimentation /commande','5V via connecteurFAN Pi5 ; PWM avec retour tachymétrique'],['Débit /vitesse max','1,09CFM /8000tr/min ±15%'],
            ['Dimensions de référence','63,5×42,5mm ;13,7mm attaches incluses ; ventilateur30×30mm']],[58,116]),Spacer(1,3*mm),
        pic(BASE/'photos/RaspberryPi-fiche-p2-1.jpeg',133),
        p('Photo constructeur extraite de la fiche, page2. LePi illustré est une présentation ; aucunPi ni boîtier n’est inclus dans cette ligne d’achat. La variante mémoire photographiée n’est pas identifiée. CréditRaspberryPiLtd.','small'),
        ref('Offre Amazon.fr et prix daté',AMAZON),PageBreak()]
    story += [p('Montage et maintien','title'),
        p('Le produit arrive préassemblé. Le dissipateur utilise deux trous dédiés duPi5 ; les quatre trous de fixation de la carte au châssis restent distincts.'),
        p('<b>1.</b> Débrancher pack, alimentationPi et équilibrage. Stabiliser la carte, contrôler ventilateur, pads et attaches. Retirer les papiers de protection des pads sous le module.'),
        p('<b>2.</b> Orienter selon le dessin de la boîte et la fiche du fabricant. Approcher sans heurter ports et composants, puis aligner les deux clips avec les trous de dissipateur.'),
        p('<b>3.</b> Appuyer régulièrement sur les deux têtes blanches jusqu’à l’encliquetage. Vérifier leur retenue par-dessous. Le métal doit rester éloigné des contacts et composants hors des interfaces thermiques prévues.'),
        p('<b>4.</b> Insérer la fiche dans <b>FAN</b>, dans le sens prévu. Arrêter en cas de résistance, retirer et inspecter les deux connecteurs. Ne pas déplacer la fiche au hasard sur le GPIO40broches.'),
        pic(BASE/'photos/Waveshare-produit-3.jpg',105),
        p('Dessous observé sur une photoWaveshare du produit officiel : trois pads. Ils sont inclus dans le module ; leur géométrie et leur épaisseur comprimée ne sont pas publiées. Filigrane conservé, créditWaveshare.','small'),
        p('<b>5.</b> Retenir le cordon en gardant admission du ventilateur et sortie vers les ailettes libres. Vérifier les dégagements au châssis et aux ports ; aucun refroidissement lié à la vitesse de roulage n’est supposé.'),
        p('<b>6.</b> Le fabricant recommande de laisser le montage en place. Les démontages répétés dégradent clips et pads ; remplacer une attache endommagée ou mal retenue selon la notice du lot.','small'),PageBreak()]
    rows=[['Courant fan*','Puissance à5V','Énergie20min','Énergie45min']]
    for r in calc['current_examples']:rows.append([f"{r['fan_current_example_A']:.2f} A".replace('.',','),f"{r['fan_power_W']:.2f} W".replace('.',','),f"{r['energy20min_Wh']:.3f} Wh".replace('.',','),f"{r['energy45min_Wh']:.3f} Wh".replace('.',',')])
    story += [p('Commande et alimentation','title'),
        table([['Broche officielleFAN','Fonction','Couleur'],['1','+5V','Rouge'],['2','PWM','Bleu'],['3','GND','Noir'],['4','Tachymètre','Jaune']],[58,61,55]),Spacer(1,3*mm),
        p('ConnecteurJST-SH quatre voies, pas1mm. Utiliser la fiche livrée ; la vue de numérotation doit être lue dans la documentationPi. Le contrôleFAN est distinct desPWM GPIO12/13/18 réservés aux deuxESC et au servo.'),
        table([['Température montante*','Commande décrite actuellement'],['Sous50°C','Ventilateur arrêté'],['50°C /60°C','30% /50%'],['67,5°C /75°C','70% /100%'],['Descente','Hystérésis5°C']],[65,109]),Spacer(1,3*mm),
        p('*Profil de la documentationPi actuelle ; noyau et firmware du système reçu à relever. Le billet2023 ne décrivait que60/67,5/75°C. Aucun réglage duPi n’a été appliqué.','small'),
        banner('FAN partage la limite de courant des périphériquesUSB. Les60mA du ventilateur du <b>boîtier officiel</b> ne sont pas une spécificationSC1148. La ficheActiveCooler ne publie pas son courant : mesurer démarrage et régime avec la caméra.'),Spacer(1,3*mm),
        table(rows,[44,43,43,44]),Spacer(1,2*mm),
        p('*Exemples arithmétiques, pas des valeurs nominales ou mesurées du produit. P=5I et E=Pt. Le budget25W d’étude de la branchePi inclut déjàPi, caméra et refroidissement ; ne pas compter le ventilateur deux fois. Aucun gain d’autonomie démontré.','small'),PageBreak()]
    story += [p('Cotes et références mécaniques','title'),
        pic(crop,149),
        p('Cadrage du plan original pour lecture, sourceRaspberryPiLtd. L’archivePDF reste intacte. Les cotes du dessin sont <b>approximatives et destinées à la référence</b>, pas à produire directement des données de fabrication.','small'),
        table([['Grandeur','Valeur /statut'],['Enveloppe du dessin','63,50×42,50mm ; hauteur13,70mm avec clips'],['Ventilateur','30×30mm documentés'],
            ['Attaches CAO','Centres(2,75;2,75) et(60,75;39,75) ;58×37mm, lecture des plans à vérifier'],
            ['Ailettes','6colonnes×9segments observés ; épaisseurs, pas, hauteur et stries estimés'],['Pads /rotor','Trois pads observés ; dimensions et épaisseurs estimées.30aubes CAO, nombre et profil non publiés']],[51,123]),Spacer(1,3*mm),
        p('Les13,7mm comprennent les attaches et ne donnent pas la hauteur à réserver au-dessus duPCB installé. La compression des pads, la position réelle des composants, les supports et le cordon déterminent les jeux finaux.'),
        p('Mesurer le lot avant fabrication du support définitif. Aucun plan de perçage certifié, aucune précharge de ressort ni empreinte de fiche de remplacement validée. LePiSTEP existant est conservé sans modification.','small'),PageBreak()]
    story += [p('Modèles STEP et contrôles','title'),
        pic(BASE/'3D/raspberry-pi-active-cooler-sc1148-detaille.png',133),
        table([['Variante','Contenu','Taille'],*[[label,desc,f"{m['bytes']/1e6:.2f}Mo"] for label,desc,m in zip(
            ['Complet','Sans cordon','Dissipateur','Implantation légère'],['Détails et4fils continus','Module complet, fils omis','Ailettes et marquage','Stries, logo et cordon omis'],cat['models'])]],[49,94,31]),Spacer(1,3*mm),
        p('Les modèles sont des reconstructions colorées enmillimètres. Détails visibles : stries, rotor, capot et têtes de vis, clips fendus, ressorts hélicoïdaux et pads. Le marquage provient des contours du plan, avec relief de lecture0,018mm non mesuré.'),
        p('Quatre fils continus sont contrôlés : âme et gaine en un solide chacune, deux courbes raccordées avec tangentes continues,192sondes de matière de gaine par fil et82sondes d’axe. Aucune intersection volumique entre fils ; le trajet est une pose illustrative, pas la longueur du cordon livré.'),
        p('Export/réimportSTEP : solides, volumes, enveloppes et couleurs conservés. <b>Quatre fichiers contrôlés indépendamment avecFreeCAD sans interface</b> : solides fermés et géométrie valide. Pas d’essai dansCADView ni de qualification sur matériel. Les JSON voisins conservent sources et estimations.','small'),PageBreak()]
    story += [p('Essais, avis et documentation','title'),
        p('À la réception, vérifierSC1148, pads, clips et fiche ; relever versionsOS/noyau/firmware. Contrôler rotation et régime, tension5V auPi, appel de courant et budgetUSB/FAN avec la caméra active.'),
        p('Dans le châssis final et robot immobile, mesurer températureCPU, fréquence, sous-tension/throttling, bruit et courant du ventilateur. Faire ces relevés pendant une charge vidéo prolongée avec commandes moteurs ; comparer cadence réelle, latence et stabilité des impulsions. Le refroidisseur seul ne valide pas le retour1080p60 ni l’autonomie.'),
        p('Avis et retours consultés','sub'),
        p('Amazon.fr affiche4,7/5 sur1242évaluations au relevé. Compteur potentiellement international ; aucun taux de panne déduit et aucun avis individuel inventé. Prix6,99€TTC observé, port et panier à revalider.'),
        p('JeffGeerling décrit en2024 un bruit proche du fond sonore de son studio à5000tr/min. Son test ne garantit pas le bruit dans notre montage. Sa vidéo2023 comprend un chapitrethermique à10:17 ; ce n’est pas un essaiUSB1080p60 versMac de notre robot.'),
        p('Les forums officiels rapportent des perceptions de bruit et une interférence avec un couvercle intérieur de boîtierPi. Vérifier le lot et les jeux. Aucun résultat de montage fermé n’est transposé automatiquement au châssisV3.','small'),
        p('Sources','sub'),
        ref('Fabricant : produit, contenu et fichejanvier2026',MAKER),
        ref('Portail : fiche et plan originaux',PORTAL),
        ref('BrochageFAN, régulation et budgetUSB partagé',HARDWARE),
        ref('Amazon.fr : SC1148 /B0CLXZBR5P',AMAZON),
        ref('Photos complémentaires du produit officielWaveshare','https://www.waveshare.com/product/accessories/power-heat-sinks/raspberry-pi-5-official-active-cooler.htm'),
        ref('JeffGeerling : article2024 avec mesures','https://www.jeffgeerling.com/blog/2024/water-cooling-overkill-pi-5/'),
        ref('Vidéo de référence2023, chapitre10:17','https://www.youtube.com/watch?v=nBtOEmUqASQ'),
        ref('Forum officiel : interférence de boîtier','https://forums.raspberrypi.com/viewtopic.php?t=367026'),
        p('Les URL etSHA256 sont conservés dansassets.json. Les aliasPIP/datasheets donnent les mêmes deux documents : le fichier local nommé«historique» contient aussi l’éditionjanvier2026. Images etPDF sources inchangés ; détails non publiés signalés danscotes.md et les JSON desSTEP.','small')]
    doc=SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=18*mm,bottomMargin=23*mm,
        title='Drone V3 - Raspberry Pi Active Cooler SC1148',author='Projet Drone V3')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    pdf=pymupdf.open(OUT);pages=[]
    for i,page in enumerate(pdf):
        png=TMP/f'page-{i+1}.png';page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(png)
        pages.append(dict(page=i+1,render=str(png.relative_to(ROOT)),chars=len(page.get_text())))
    OUT.with_suffix('.json').write_text(json.dumps(dict(file=OUT.name,pages=len(pdf),sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),
        generator='tools/build_pi_cooler_pdf.py',generated_on='2026-10-14',renders=pages,visual_review_complete=False),indent=2)+'\n',encoding='utf-8')
    print('PDF',len(pdf),'pages',OUT.stat().st_size,'bytes',flush=True)
    for i,page in enumerate(pdf):print('PAGE',i+1,len(page.get_text()),flush=True)
    assert len(pdf)==6,len(pdf)
if __name__=='__main__':main()
