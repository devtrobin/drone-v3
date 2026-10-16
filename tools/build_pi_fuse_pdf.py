"""Author one French project notice and render all pages for visual review."""
from pathlib import Path
import json,sys,hashlib
import pymupdf
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate,Spacer,Image,PageBreak
from build_heatsink_pdf import p,table,banner,source,GREY
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/protection-branche-pi'
OUT=BASE/'notices/notice-protection-branche-pi-v3.pdf';TMP=ROOT/'tools/temp/pi-fuse-review/pdf'
def footer(c,d):
    c.saveState();c.setStrokeColor(colors.HexColor('#ccdbe4'));c.line(18*mm,17*mm,192*mm,17*mm)
    c.setFont('HV3',7.4);c.setFillColor(GREY);c.drawString(18*mm,12*mm,'Drone V3 | Protection du depart Pi | 14 octobre 2026 | Etude non testée')
    c.drawRightString(192*mm,12*mm,str(d.page));c.restoreState()
def main():
    sys.stdout.reconfigure(encoding='utf-8');TMP.mkdir(parents=True,exist_ok=True)
    cal=json.loads((BASE/'calculs.json').read_text(encoding='utf-8'));cat=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'))
    fc=json.loads((BASE/'3D/validation-freecad.json').read_text(encoding='utf-8'));assert fc['all_passed']
    story=[p('Protection du départ Pi<br/>Porte-fusible et ATO 7,5 A','title'),p('Batterie LiPo 2S - alimentation du Pi, de la caméra et de la commande SSR'),
        banner('<b>Sélection d’étude : Blue Sea 5065 + Littelfuse 0ATO07.5V.</b> Fusible en série au début du départ positif, avant le Pololu 2813. Non acheté, non testé. Offre Amazon.fr et coordination de défaut encore à confirmer.'),Spacer(1,4*mm),
        table([['Pièce','Référence et fonction'],['Porte-fusible','5065 ; ATO/ATC, deux fils 12 AWG ; maximum fabricant 30 A ; capot/joint, fusible vendu séparément'],
            ['Fusible retenu pour étude','0ATO07.5V / ATO7.5 ; 7,5 A, brun, 32 V DC ; 1 000 A de pouvoir de coupure à 32 V DC'],
            ['Conditionnement possible','0ATO07.5VP / ATO7.5BP : carte de cinq, un embarqué et quatre de rechange si ce lot est acheté'],
            ['But de la protection','Protection du départ de fils ; pas une garantie de protection rapide des semi-conducteurs']],[48,126]),Spacer(1,4*mm),
        Image(str(BASE/'3D/ensemble-pi-ato-7-5a-ferme-etude.png'),width=141*mm,height=114.56*mm),
        p('Assemblage reconstruit : deux fils rouges sortent du même côté. Longueurs, brins, contacts et support estimés d’après la photo. Cosses et fixation de châssis absentes.','small'),PageBreak()]
    story += [p('Choix du calibre','title'),
        banner('<b>I entrée ≈ 25 / (6,4 × 0,90) + 0,015 = 4,355 A</b><br/>25 W au 5 V, rendement 90 %, pack 6,4 V et commande SSR 15 mA : hypothèses, pas mesures. Les chutes de fils/contacts et la consommation propre du Pololu ne sont pas incluses dans cette première somme.'),Spacer(1,4*mm),
        table([['Tension disponible / rendement supposé','Courant calculé'],['8,4 V / 90 %','3,322 A'],['6,4 V / 90 %','4,355 A'],['6,4 V / 80 %','4,898 A'],['6,2 V / 80 %','5,055 A']],[128,46]),Spacer(1,3*mm),
        p('Calculer avec la tension effectivement disponible à VIN après les pertes. Démarrage, USB/caméra active et creux provoqués par les moteurs doivent être mesurés.'),
        table([['ATO nominal','À 20 °C*','À 65 °C*','À 85 °C*'],['5 A','5 A','4 A','4 A'],['7,5 A - étude','7 A','6 A','5 A'],['10 A','10 A','8 A','7 A']],[55,39,40,40]),Spacer(1,3*mm),
        p('*Courant recommandé typique dans la fiche Littelfuse aftermarket du 15 novembre 2022, avec ses connexions et conditions d’essai. Le 5 A est trop juste au scénario chaud ; 7,5 A laisse de la marge à 65 °C. À 85 °C et rendement 80 %, la marge devient faible ou disparaît avec les pertes.','small'),
        p('Limites du Pololu 2813','sub'),p('Les <b>6 A associés à 55 °C</b> décrivent une température MOSFET mesurée sous 12 V, ambiante 22 °C, air calme. Ce n’est pas une garantie à 55 °C ambiants ni un seuil de coupure : l’interrupteur ne limite pas le courant. Sa tenue à 2S et dans le châssis reste à qualifier.'),
        p('Pertes du fusible à froid','sub'),p('Résistance typique 10,91 mΩ : à 4,355 A, environ <b>47,5 mV / 0,207 W</b>, hors contacts et fils. La fiche donne aussi 116 mV dans ses conditions d’essai. I²t typique 60 A²s : fusion avant l’arc, pas énergie totale de coupure garantie.','small'),PageBreak()]
    story += [p('Raccordement et cotes','title'),
        banner('<b>MiniBus D+ P4 → 5065 / ATO 7,5 A → VIN Pololu 2813 → VSW → régulateur → Pi.</b><br/>Les deux fils rouges sont entrée et sortie du même positif. Les négatifs restent sur D-. Le courant des moteurs ne traverse pas le Pi.'),Spacer(1,3*mm),
        table([['Interface','Valeur / portée'],['Fusible, plan de référence','19,1 × 5,1 × 18,8 mm ; lames 4,1 × 0,65 ; dépassement 6,5'],
            ['Lames du fusible','14,5 mm est leur largeur extérieure ; entraxe déduit 10,4 mm'],
            ['Support et oreille en CAO','37,5 × 38 × 15 mm estimés, hors fils ; aucun plan constructeur obtenu'],
            ['Trou de fixation CAO','Ø5,0 estimé ; témoignage revendeur ≈3/16 pouce, pas un plan de perçage'],
            ['Longueur de fils CAO','100 mm extérieurs + bouts nus de 8 mm ; pose illustrative, longueur livrée inconnue']],[60,114]),Spacer(1,3*mm),
        Image(str(BASE/'porte-fusible/photos/Amazon-5065-original.jpg'),width=93*mm,height=93*mm),
        p('Photo commerciale exacte Amazon.com B004ZIUA62, archivée inchangée. Support sans fusible : socle, capot et joint orange. Les indices IP chiffrés trouvés chez des marchands ne sont pas confirmés par le fabricant pour le 5065.','small'),
        p('Placer le support au plus près de P4, avant réduction de section. L’arrivée avant le petit fusible reste à coordonner avec le principal ; la garder très courte et protégée mécaniquement. Sertir, isoler et retenir les fils. Conserver l’écrou #10-32 du MiniBus, couple du lot à confirmer.','small'),
        p('Prolongement côté batterie proposé : cuivre 1,5 mm² court, à qualifier avec isolant, température, regroupement et défauts. Le 0,75 mm² de la fiche est une section d’essai. La liaison 5 V régulateur/Pi est un circuit distinct à dimensionner.','small'),PageBreak()]
    story += [p('Coupure, défauts et essais','title'),p('<b>7,5 A ne signifie pas coupure immédiate à 7,5 A.</b> Pour la référence retenue, la fiche publie les fenêtres suivantes :'),
        table([['Rapport au calibre','Courant','Temps d’ouverture'],['110 %','8,25 A','Au moins 360 000 s ; pas de maximum'],['135 %','10,125 A','0,75 à 600 s'],
            ['160 %','12 A','0,25 à 50 s'],['200 %','15 A','0,15 à 5 s'],['350 %','26,25 A','0,08 à 0,5 s'],['600 %','45 A','0,1 s maximum']],[44,39,91]),Spacer(1,4*mm),
        banner('<b>Pouvoir de coupure : 1 000 A à 32 V DC.</b> Courant prospectif de la LiPo à établir. Le principal MIDI 60 A ne qualifie pas automatiquement une association en série ou une sélectivité garantie avec ce petit ATO.'),Spacer(1,3*mm),
        p('Repère ohmique simplifié : <b>8,4 V / 1 000 A = 8,4 mΩ</b>. Pour estimer le courant prospectif, ne pas inclure la résistance du fusible de branche dans la boucle servant à justifier son pouvoir de coupure. Le marquage batterie « 80C » ne mesure pas le courant de défaut. Pas de court-circuit volontaire du pack.'),
        p('La limitation du régulateur peut empêcher la fusion lors d’un défaut de sortie. Ni le Pi, ni le régulateur, ni le Pololu ne sont garantis protégés rapidement par ce fusible. Une fusion peut couper VSW et la commande SSR ; l’arrêt Linux propre n’est pas garanti. Freinage et régénération restent à évaluer.'),
        p('Qualification avant utilisation','sub'),p('Batterie et équilibrage débranchés : contrôler références, sections, sertissage, retenue, polarité et isolement. Première alimentation limitée après contrôle du schéma. Mesurer courant de démarrage et sous caméra active, creux VIN/5 V, pertes et températures ; vérifier les durées d’usage prévues.'),
        p('Valider le courant prospectif et la coordination avant mise en service. Si un critère échoue, revoir la technologie de fusible, la thermique ou le faisceau. Ne pas augmenter automatiquement le calibre pour masquer un défaut ou un démarrage mal compris.','small'),PageBreak()]
    story += [p('Achat, modèles et références','title'),
        p('Support 5065 : <b>ASIN B004ZIUA62 confirmé sur Amazon.com</b>. Offre Amazon.fr, vendeur, stock et prix TTC non confirmés. Fusible exact : pas d’ASIN Amazon vérifié. Repères étrangers : 15,01 USD/support chez Hodges Marine et 1,35 USD/fusible unitaire chez DigiKey, hors livraison et fiscalité France. Aucun achat effectué.'),
        p('Retours trouvés : utilisateur Maine Sail, forum 2014, dit employer le 5065 ; cinq avis eBay apprécient installation/qualité perçue, sans protocole de mesure. Canadian Tire regroupe 151 avis de plusieurs calibres ; la note ne qualifie pas ce 7,5 A. Aucun essai vidéo exact exploitable trouvé.','small'),
        table([['STEP reconstruit','Solides / faces'],*[[m['title'],f"{m['validation']['solids']} / {m['validation']['faces']}"] for m in cat['models']]],[133,41]),Spacer(1,3*mm),
        p('Les six STEP ont passé les contrôles <b>FreeCAD sans interface</b> : validité, solides fermés, nombre de solides et enveloppes. Réimports CadQuery : volumes, couleurs et non-chevauchement. Aucun test GUI FreeCAD/CAD View revendiqué. Support non mesuré, cotes de moulage estimées et aucun STEP natif fabricant.','small'),
        p('Sources et copies archivées','sub'),
        source('Support, fabricant','https://www.bluesea.com/products/5065'),
        source('Fusible aftermarket, fiche exacte 2022','https://www.mouser.com/datasheet/2/240/media-3323444.pdf'),
        source('Pololu 2813, conditions thermiques et limites','https://www.pololu.com/product/2813'),
        source('Mesures approximatives de revendeur','https://shop.pkys.com/Blue-Sea-5065--Waterproof-In-Line-Fuse-Holder-for-ATOATC-Fuses_p_2716.html'),
        p('Copie RSP de la fiche ATO 2022 avec bannières distributeur et page Mouser conservée telle que fournie ; catalogue Littelfuse 2013 et fiche FHM de comparaison archivés. Catalogue Blue Sea 2024 référencé localement dans le dossier de distribution. SHA256, URL, statuts, cotes et limites : assets.json, sources.json, recherche-technique.md et JSON voisins des STEP.','small')]
    SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=18*mm,bottomMargin=23*mm,
        title='Drone V3 - Protection du depart Raspberry Pi',author='Projet Drone V3').build(story,onFirstPage=footer,onLaterPages=footer)
    doc=pymupdf.open(OUT);assert len(doc)==5,len(doc);pages=[]
    for i,page in enumerate(doc):
        png=TMP/f'page-{i+1}.png';page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(png)
        pages.append(dict(page=i+1,render=str(png.relative_to(ROOT)).replace('\\','/'),chars=len(page.get_text())))
    OUT.with_suffix('.json').write_text(json.dumps(dict(file=OUT.name,pages=len(doc),sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),
        generated_on='2026-10-14',generator='tools/build_pi_fuse_pdf.py',renders=pages,visual_review_complete=False),indent=2)+'\n',encoding='utf-8')
    print('PDF',len(doc),'pages',OUT.stat().st_size,'bytes',flush=True)
if __name__=='__main__':main()
