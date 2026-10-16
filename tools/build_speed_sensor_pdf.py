"""Create the shared, illustrated PDF and render every page for visual inspection."""
from pathlib import Path
import hashlib,html,json,sys,re
import pymupdf
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate,Image,Spacer,PageBreak,Table
from reportlab.graphics.shapes import Drawing,Line,Rect,String,Circle
from build_heatsink_pdf import p as raw_p,table as raw_table,banner as raw_banner,GREY,BLUE

ROOT=Path(__file__).resolve().parents[1]
B=ROOT/'Composants/capteurs-vitesse'
OUT=B/'notices/notice-capteurs-vitesse-v3.pdf'
TMP=ROOT/'tools/temp/speed-review/pdf'


def readable(text):
    text=re.sub(r'([a-zà-ÿ]{2,})(?=\d)',r'\1 ',str(text))
    text=re.sub(r'\b(à|M)(?=\d)',r'\1 ',text)
    for a,b in {'Pi5':'Pi 5','etGND':'et GND','référenceGND':'référence GND','sousLinux':'sous Linux',
                'etWi-Fi':'et Wi-Fi','etSHA256':'et SHA256','champBOP':'champ BOP','TI4221343':'TI 4221343',
                'KEMET100':'KEMET 100','le5 V':'le 5 V','Aucun5':'Aucun 5'}.items():text=text.replace(a,b)
    text=re.sub(r'([:;])(?=\S)',r'\1 ',text)
    text=re.sub(r'(?<=\d)(?=(?:mm|cm|km|Hz|mA|kHz|µs|nF)\b)',' ',text)
    text=re.sub(r'\s*([≤≥≈])\s*',r' \1 ',text)
    return text


def p(text,style='body'):
    return raw_p(''.join(s if s.startswith('<') else readable(s) for s in re.split(r'(<[^>]*>)',str(text))),style)


def table(rows,widths):
    return raw_table([[readable(str(cell)) for cell in row] for row in rows],widths)


def banner(text):
    return raw_banner(''.join(s if s.startswith('<') else readable(s) for s in re.split(r'(<[^>]*>)',text)))


def photo(path,w,h):
    with PILImage.open(path) as im:x,y=im.size
    scale=min(w*mm/x,h*mm/y)
    return Image(str(path),width=x*scale,height=y*scale)


def footer(c,d):
    c.saveState();c.setStrokeColor(colors.HexColor('#ccdbe4'));c.line(18*mm,17*mm,192*mm,17*mm)
    c.setFont('HV3',7.3);c.setFillColor(GREY)
    c.drawString(18*mm,12*mm,'Drone V3 | Capteurs de vitesse | 15 octobre 2026 | Etude non testée')
    c.drawRightString(192*mm,12*mm,str(d.page));c.restoreState()


def ref(name,url):
    return p('<link href="'+html.escape(url,quote=True)+'" color="#174969">'+html.escape(name)+'</link>','small')


def circuit():
    d=Drawing(174*mm,70*mm)
    def line(x1,y1,x2,y2):d.add(Line(x1*mm,y1*mm,x2*mm,y2*mm,strokeColor=BLUE,strokeWidth=1.1))
    def label(x,y,s,size=8):d.add(String(x*mm,y*mm,s,fontName='HV3',fontSize=size,fillColor=BLUE))
    # One of two identical channels, functional connection diagram.
    d.add(Rect(80*mm,20*mm,40*mm,24*mm,fillColor=colors.HexColor('#edf4f7'),strokeColor=BLUE))
    label(84,33,'DRV5033 LPG',9);label(94,39,'1 VCC');label(94,22,'2 GND');label(108,28,'3 OUT',7)
    label(4,64,'Une voie - deux exemplaires identiques',9)
    label(4,56,'3,3 V / pin17');line(12,52,160,52)
    label(4,5,'GND / pin25');line(12,14,160,14)
    line(100,44,100,52);line(100,20,100,14)
    # Decoupler is between the power rails, with no crossing of the output net.
    line(40,52,40,38);line(35,38,45,38);line(35,36,45,36);line(40,36,40,14)
    label(16,29,'100 nF local')
    # Output and its pullup are on the right; distinct from VCC and GND.
    line(120,32,160,32);label(124,26,'Vers GPIO23 ou 24',7.5)
    line(145,52,145,45);d.add(Rect(143*mm,36*mm,4*mm,9*mm,strokeColor=BLUE,fillColor=colors.white))
    line(145,36,145,32);label(150,40,'10 kΩ')
    for x,y in [(40,52),(100,52),(145,52),(40,14),(100,14),(145,32)]:
        d.add(Circle(x*mm,y*mm,.65*mm,fillColor=BLUE,strokeColor=BLUE))
    label(4,0,'Rappel côté Pi ; condensateur au capteur. Aucun rappel à 5 V.',8)
    return d


def main():
    sys.stdout.reconfigure(encoding='utf-8');TMP.mkdir(parents=True,exist_ok=True)
    c=json.loads((B/'calculs.json').read_text(encoding='utf-8'))
    fc=json.loads((B/'3D/validation-freecad.json').read_text(encoding='utf-8'));assert fc['all_passed']
    story=[p('Mesure de vitesse<br/>des roues arrière','title'),p('Deux capteurs Hall, quatre aimants et leurs composants de raccordement'),
           banner('<b>Sélection et modèles d’étude, non achetés et non testés.</b> Deux aimants par roue donnent deux impulsions par tour si le montage permet un retour haut entre passages. La fixation définitive reste pour le châssis.'),Spacer(1,4*mm),
           table([['Pièce / référence','Quantité montée'],['TI DRV5033AJQLPG, boîtier LPG TO-92','2 capteurs nus'],['supermagnete S-03-02-N, N48, Ø3 × 2 mm','4 aimants : deux par roue'],['Vishay MRS25000C1002FCT00, 10 kΩ ±1 %','2 résistances de rappel'],['KEMET C315C104K5R5TA, 100 nF X7R / 50 V','2 condensateurs locaux']],[127,47]),Spacer(1,4*mm),
           p('Le Pi 5 reste la seule carte de commande. Les capteurs utilisent son 3,3 V, GPIO23 et GPIO24. Aucune carte microcontrôleur ajoutée. Les fils, contacts et consommables des lots prévus complètent ces pièces.'),
           photo(B/'3D/apercu-composants.png',156,112),
           p('Cinq STEP : capteur, aimant, résistance droite et formée, condensateur natif. Chaque vignette a sa propre échelle. Aucun support de roue ou de châssis fabriqué.','small'),PageBreak(),
           p('Capteur TI DRV5033AJQLPG','title'),
           table([['Donnée','Spécification ou choix V3'],['Alimentation / sortie','2,5-38 V ; retenu à3,3 V. Drain ouvert actif bas, rappel externe.'],['Brochage LPG','1 VCC ; 2 GND ; 3 OUT. Ne pas utiliser le brochage DBZ.'],['Seuils AJ, module du champ','BOP :3 /6,9 /12 mT ; BRP :1 /3,5 /5 mT, min /typ /max.'],['Rapidité','Bande passante20 kHz min /30 kHz typ ; délai25 µs max sous conditions TI.'],['Courant','2,7 mA typ à25 °C ;3,6 mA max à125 °C selon la fiche.'],['Corps LPG0003A','Largeur3,9-4,1 ; hauteur3,05-3,25 ; profondeur1,42-1,62 mm.'],['Pattes','Pas1,27 ±0,05 ; longueur sous corps15,1-15,5 mm.']],[57,117]),Spacer(1,3*mm),
           photo(B/'capteur-hall-drv5033/3D/drv5033ajqlpg-detaille.png',155,104),
           p('Reconstruction du plan TI4221343/C. Face marquée vers -Y, corps bas z=0 et pattes vers -Z ; VCC /GND /OUT à x=-1,27 /0 /+1,27 mm. Le marquage +QLAJ est documenté ; police, position et petits rayons estimés. Puce et connexions internes non représentées.','small'),
           banner('Identifier les broches sur la figure TI p.4 avant soudure. La sortie se réarme quand le champ diminue : ce capteur omnipolaire n’exige pas l’alternance des pôles.'),PageBreak(),
           p('Aimants et implantation','title'),
           table([['Article exact','supermagnete S-03-02-N'],['Dimensions / tolérance','Ø3 × hauteur2 mm ; ±0,1 mm.'],['Matière / direction','NdFeB fritté N48 ; aimantation axiale ; Ni-Cu-Ni argent.'],['Masse / température','0,1074 g dans le PDF,0,11 g arrondi sur la page ;80 °C max.'],['Disposition V3','Deux aimants identiques à180° par roue ; rétention captive à concevoir.'],['Entrefer initial à essayer','1-2 mm entre surfaces extérieures, avec marge aux jeux ; aucune portée garantie.']],[57,117]),Spacer(1,3*mm),
           photo(B/'aimants-s-03-02-n/3D/aimant-s-03-02-n-detaille.png',108,71),
           p('Aligner l’axe des aimants avec la face sensible. Prévoir une rétention mécanique et contrôler le voile. Ne pas utiliser la seule attraction magnétique pour retenir les aimants. La disposition symétrique réduit le balourd théorique ; l’équilibrage réel reste à vérifier.'),
           p(f"Au rayon illustratif de12 mm et avec0,11 g par aimant, effort centrifuge calculé à40 km/h : <b>{c['centrifugal']['force_per_magnet_at40_N']:.3f} N par aimant</b>. Ce n’est pas une qualification de collage. L’adhérence commerciale2,94 N sur contre-pièce ne valide pas notre fixation."),
           p('Estimation du champ, sans garantie','sub'),
           table([['Entrefer extérieur*','1 mm','2 mm','3 mm','4 mm'],['Champ axial estimé',*[f"{x['on_axis_field_mT']:.1f} mT" for x in c['field_estimate']['rows']]]],[54,30,30,30,30]),
           p('*Cylindre uniforme en air libre, Br=1,37 T et profondeur active supposée0,6 mm. Ignore métaux voisins, champ moteur, désalignement et tolérances. Valider BOP/BRP par les états réels sur un tour complet, puis moteurs actifs.','small'),PageBreak(),
           p('Rappels et découplages','title'),
           Table([[photo(B/'resistances-rappel-10k/3D/mrs25-10k-formee-pas10-16.png',83,70),photo(B/'condensateurs-decouplage-100nf/3D/kemet-c315c104k5r5ta-officiel.png',83,70)]],colWidths=[87*mm,87*mm]),Spacer(1,3*mm),
           table([['Pièce','Cotes et fonction'],['Vishay MRS25 10 kΩ ±1 %','Une par OUT vers3,3 V, côté Pi. Corps Ø2,5 max ×6,5 max ; fil Ø0,6 nominal ; pattes droites≥28 mm.'],['Variante formée','Pas10,16 mm, conforme au minimumM=10 mm du plan. Rayons et coupe des pattes sont une pose d’étude.'],['Code couleur','Brun /noir /noir /rouge /brun pour10 kΩ à1 %. Nuance bleue et placement des bandes estimés.'],['KEMET100 nF ±10 %','50 V DC, X7R, non polarisé. VCC-GND au plus près de chaque capteur.'],['Corps /pattes KEMET','3,81 ×3,14 ×2,54 mm max ; pas2,54 ±0,78 ; Ø0,51 +0,1/-0,025 ; LL≥7 mm.'],['TI demande au minimum','10 nF local :100 nF nominal retenu. Ne pas confondre avec un condensateur placé sur OUT.']],[51,123]),Spacer(1,4*mm),
           p('À3,3 V, chaque rappel consomme environ0,33 mA /1,09 mW quand OUT est bas. Budget des deux capteurs et deux rappels bas : environ7,87 mA sous l’hypothèse conservatrice de la table TI à125 °C et de résistances à9,9 kΩ. Vérifier le budget global de la ligne3,3 V.'),
           p('CAO KEMET native, obtenue par le lien du PDF spécifique : fichier et couleurs conservés à l’identique. La description générique C0G de RS ne concerne pas cette référence X7R. Les composants internes ne sont pas reconstruits.','small'),PageBreak(),
           p('Raccordement au Raspberry Pi 5','title'),
           table([['Fonction','Gauche','Droite'],['OUT LPG3','GPIO23 /pin physique16','GPIO24 /pin physique18'],['VCC LPG1','3,3 V /pin17, dérivation Y','Même alimentation3,3 V'],['GND LPG2','GND /pin25, dérivation Y','Même référenceGND'],['Rappel /découplage','10 kΩ vers3,3 V ;100 nF local','Idem, composants distincts']],[46,64,64]),Spacer(1,3*mm),
           circuit(),Spacer(1,3*mm),
           p('Ajout de quatre contacts16 /17 /18 /25 : <b>13 montés,18 à provisionner avec cinq de réserve</b>. Les positions2 /4 /6 /9 /14 /20 de la fiche de signaux restent vides. Le5 V de puissance de la Pi conserve son faisceau séparé. Les anciens PDF/STEP GPIO sont des versions datées.'),
           p('Employer le fil22 AWG prévu. Les Y de3,3 V etGND sont soudés, isolés individuellement et maintenus ; pas de double fil dans un contact Molex. Longueurs après implantation. Faire suivre les signaux de leurGND, à distance des phases moteur et de la puissance.'),
           banner('Alimentation et rappels uniquement à3,3 V du Pi. Aucun5 V, BEC6 V ou positif batterie sur ces GPIO. Pi et capteurs s’alimentent ensemble. Les capteurs ne constituent pas un arrêt de sécurité.'),PageBreak(),
           p('Mesure, essais et contrôle des fichiers','title'),
           p('<b>v [km/h] = f [Hz] × π × D [m] ×3,6 /2</b><br/>Compter les fronts descendants seulement. Deux aimants donnent deux fronts par tour si le montage se réarme correctement. D=0,063 m est le diamètre nominal, à calibrer par roulage sous charge.'),
           table([['Vitesse','Roue tr/min','Fréquence /roue','Période'],*[[f"{r['speed_kmh']} km/h",f"{r['wheel_rpm']:.0f}",f"{r['pulses_per_s']:.2f} Hz",f"{r['period_ms']:.2f} ms"] for r in c['wheel_rows']]],[38,44,48,44]),Spacer(1,3*mm),
           p('Un événement représente environ99 mm nominaux parcourus. La mesure par période est utile à basse vitesse. Un seul capteur par roue ne donne pas le sens de marche ; le patinage fausse la vitesse au sol. Ne pas égaliser constamment les deux roues en virage.'),
           p('Validation progressive du montage','sub'),
           p('Contrôler les références, isolations et polarités hors tension. Tester sous3,3 V limité en courant ; vérifier OUT haut et bas, puis deux impulsions et deux retours hauts par tour. Répéter aux jeux extrêmes et avec moteurs, freinage, caméra etWi-Fi actifs. Contrôler rétention des aimants et dégagement avant rotation rapide.'),
           p('Acquérir des événements horodatés avec une interface GPIO compatible Pi5. Initialiser après stabilisation : la fiche TI décrit une impulsion au démarrage. Comparer le comptage à un oscilloscope ou compteur de référence. Mesurer les largeurs minimales haut/bas ;112 Hz seuls ne garantissent pas la capture sousLinux.'),
           p('Avec une charge de ligne supposée1 nF,10 kΩ donne un temps de montée10-90 % d’environ22 µs. Ce n’est pas une mesure du câble. Adapter le filtrage aux impulsions mesurées, sans anti-rebond long qui supprime les passages rapides. Un fil débranché peut ressembler à une roue arrêtée.'),
           p('Contrôles géométriques effectués','sub'),
           p('Les cinq STEP sont réimportés par CadQuery et FreeCAD sans interface : solides valides et fermés, nombres de solides, enveloppes, volumes et empreintes comparés. Couleurs vérifiées sur les reconstructions ; fichier KEMET inchangé. Cela ne constitue ni un essai matériel ni une ouverture dans les interfaces FreeCAD ou CADView.'),PageBreak(),
           p('Achat, sources et traçabilité','title'),
           table([['Achat proposé','Prix de conditionnement'],['RS :10 capteurs /25 résistances /20 condensateurs','4,16 /2,75 /4,68 EUR HT ; total11,59 HT. Environ13,91 TTC à20 %, hors frais.'],['supermagnete :20 aimants','4,80 EUR TTC le lot ; panier du marchand≥20 EUR hors port.'],['Provision avec minimum marchand','Environ33,91 EUR TTC avant ports, contacts et consommables, selon les hypothèses ci-dessus.'],['Contacts /fils','4 contacts Molex supplémentaires ; lots de fil/gaine déjà prévus. Prix France final non confirmé.']],[70,104]),Spacer(1,3*mm),
           p('Le total nominal18,71 EUR des quatre lots ne permet pas un achat isolé chez supermagnete. Le TTC RS affiché de la résistance est incohérent avec sonHT ; retenir le calcul indicatif et vérifier le panier. Aucun achat effectué. Aucune offre Amazon.fr exacte vérifiée ; des pages de contrôle d’accès ont été reçues.'),
           p('Documents originaux et recherche','sub'),
           ref('TI : fiche DRV5033, brochage et caractéristiques','https://www.ti.com/lit/pdf/slis152'),
           ref('TI : plan LPG0003A /4221343C','https://www.ti.com/lit/pdf/MPBC003B'),
           ref('TI E2E : portée dépendant du champ de l’aimant','https://e2e.ti.com/support/sensors-group/sensors/f/sensors-forum/816464/drv5033-hall-sensing-distance'),
           ref('supermagnete : article exact, fiche et prix','https://www.supermagnete.fr/aimants-disques-neodyme/disque-magnetique-3mm-2mm_S-03-02-N'),
           ref('Vishay : MRS16 /MRS25, cotes p.3','https://www.vishay.com/docs/28724/mrs16m25.pdf'),
           ref('KEMET : fiche spécifique et lien STEP natif','https://search.kemet.com/component-documentation/download/specsheet/C315C104K5R5TA'),
           ref('RS France : capteur900-9807 dans la catégorie','https://fr.rs-online.com/web/c/semi-conducteurs/?pn=67'),
           ref('RS : résistance683-2939','https://fr.rs-online.com/web/p/resistances-traversantes/6832939'),
           ref('RS : condensateur146-3570, lot20','https://fr.rs-online.com/web/p/condensateurs-ceramique-multicouches/1463570'),
           p('Cinq PDF constructeur, planSVG, photo d’aimant, STEP KEMET et pages accessibles archivés sans modification. Le registre assets.json donne URL, date, erreurs etSHA256. Recherche forums/YouTube : aucun essai vérifié reproduisant cet ensemble ; aucun avis ou score produit inventé.','small')]
    # Spaces in prose are authored explicitly; avoid transformations of part references or URLs.
    doc=SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=18*mm,bottomMargin=23*mm,
                          title='Drone V3 - Capteurs de vitesse des roues',author='Projet Drone V3')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    d=pymupdf.open(OUT);assert len(d)==7,len(d)
    renders=[]
    for i,page in enumerate(d):
        path=TMP/f'page-{i+1}.png';page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(path)
        renders.append(dict(page=i+1,file=str(path.relative_to(ROOT))))
    OUT.with_suffix('.json').write_text(json.dumps(dict(file=str(OUT.relative_to(ROOT)),pages=len(d),generated_on='2026-10-15',
        generator='tools/build_speed_sensor_pdf.py',sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),renders=renders,
        visual_review_complete=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PDF',len(d),'pages',OUT.stat().st_size,'bytes',flush=True)


if __name__=='__main__':main()
