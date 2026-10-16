"""Six-page integration notice, with clickable purchase and manufacturer links."""
from pathlib import Path
import sys,json,hashlib,html
import pymupdf
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate,Image,Spacer,PageBreak,Flowable
from build_heatsink_pdf import p as hp,table as ht,banner as hb,GREY
from build_gpio_data import MOLEX,CONTACT,WIRE,GPIO,FAMILY
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/connecteur-gpio';OUT=BASE/'notices/notice-connecteur-gpio-v3.pdf'
TMP=ROOT/'tools/temp/gpio-review/pdf'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def clean(s):return str(s).replace('–','-').replace('—','-').replace('‑','-')
def p(s,style='body'):return hp(clean(s),style)
def table(rows,widths):return ht([[clean(c) for c in row] for row in rows],widths)
def banner(s):return hb(clean(s))
def pic(path,width):
 with PILImage.open(path) as im:w,h=im.size
 return Image(str(path),width=width*mm,height=width*h/w*mm)
def ref(label,url):return p(f'<link href="{html.escape(url,quote=True)}" color="#174969"><b>{label}</b></link>','small')
def footer(c,d):
 c.saveState();c.setStrokeColor(colors.HexColor('#ccdbe4'));c.line(18*mm,17*mm,192*mm,17*mm)
 c.setFont('HV3',7.4);c.setFillColor(GREY);c.drawString(18*mm,12*mm,'Drone V3 | Connecteur GPIO | 14 octobre 2026 | Montage non testé')
 c.drawRightString(192*mm,12*mm,str(d.page));c.restoreState()
class Pinout(Flowable):
 def __init__(self,pins):super().__init__();self.width=174*mm;self.height=24*mm;self.used={p['physical_pin'] for p in pins}
 def draw(self):
  c=self.canv;cell=self.width/20
  c.setFont('HV3',6.7)
  for col in range(20):
   for row in range(2):
    pin=2*col+1+row;x=(col+.5)*cell;y=(8+row*8)*mm
    c.setFillColor(colors.HexColor('#174969') if pin in self.used else colors.HexColor('#dce5eb'))
    c.circle(x,y,1.5*mm,fill=1,stroke=0)
    c.setFillColor(colors.HexColor('#24313e'));c.drawCentredString(x,y-3.6*mm,str(pin))
  c.setFont('HV3B',7.2);c.drawString(0,22*mm,'Vue de dessus du Pi : broches physiques ; bleu = cavité câblée')
def main():
 sys.stdout.reconfigure(encoding='utf-8');TMP.mkdir(parents=True,exist_ok=True)
 cat=read(BASE/'3D/catalogue.json');fc=read(BASE/'3D/validation-freecad.json');pin=read(BASE/'brochage.json')['pins'];calc=read(BASE/'calculs.json')
 assert fc['all_passed'] and len(fc['checks'])==4
 story=[p('Connecteur GPIO<br/>et faisceau du Raspberry Pi 5','title'),p('Molex 22-55-2401 + contacts 16-02-0103 + fil multibrin 22 AWG'),
  banner('<b>Sélection d’étude, non achetée et non testée.</b> Quarante cavités, quinze contacts prévus ; pas de carte de commande supplémentaire.'),Spacer(1,4*mm),
  table([['Pièce','Quantité','Relevé étranger*'],['Boîtier Molex 22-55-2401','1','Newark : 2,95 USD / unité'],
   ['Contacts 16-02-0103, vrac','20 : 15 montés + 5 réserve','DigiKey US : 0,25 USD / unité'],['Fil Adafruit 3175','1 lot','29,95 USD / lot']],[72,50,52]),Spacer(1,2*mm),
  p('*Somme indicative 37,90 USD aux prix unitaires consultés, hors taxes, transport et outillage. Aucun devis TTC français ni panier unique validé.','small'),
  pic(BASE/'3D/molex-22-55-2401-boitier-noir.png',126),
  p('Boîtier : solide exact de la CAO constructeur, transformé en repère de pose et coloré en noir. Le STEP original reste archivé intact ; les annotations non solides sont omises dans cette variante.','small'),
  ref('Achat identifié : boîtier, DigiKey France','https://www.digikey.fr/fr/products/detail/molex/0022552401/171975'),
  ref('Achat identifié : contacts en vrac, DigiKey France','https://www.digikey.fr/fr/products/detail/molex/0016020103/115063'),
  ref('Achat : fil, Adafruit 3175',WIRE),p('Offres Amazon exactes non confirmées ; les liens de recherche figurent dans devis.md. Le titre du lot de fil indique dix bobines, un paragraphe six : contenu à confirmer avant achat.','small'),PageBreak()]
 story += [p('Brochage proposé','title'),Pinout(pin),Spacer(1,3*mm),
  table([['Pin Pi','Fonction','Destination'],*[[r['physical_pin'],r['function'],r['destination']] for r in pin]],[20,56,98]),Spacer(1,3*mm),
  p('Vue de dessus du Pi. La face d’accouplement du boîtier femelle se lit <b>en miroir</b>. Le connecteur est non polarisé : confirmer broche 1, continuité et absence de décalage hors tension.'),
  p('Repérer les WARN blancs et les PWM jaunes aux deux extrémités. Les vingt-cinq autres cavités restent sans contact. B1 du pack et OFF brut du Pololu n’ont aucune liaison directe vers le GPIO.','small'),PageBreak()]
 story += [p('Préparation et sertissage','title'),
  p('Débrancher batterie, port d’équilibrage et alimentation du Pi. Vérifier références et diamètre réel du fil avant préparation. Couper après implantation ; garder une retenue sur le châssis et du mou aux sorties.'),
  table([['Paramètre de procédure','Valeur de référence'],['Document actuel','ATS-638118700, révision E du 9 novembre 2017'],
   ['Contact / fil','16-02-0103 ; multibrin 22 AWG'],['Isolant, profil 22–24','1,30–1,65 mm ; contact choisi limité à 1,63 mm'],
   ['Dénudage','2,54–3,17 mm'],['Crimp conducteur 22 AWG','Hauteur 0,75–0,85 ; largeur réf. 1,43 mm'],
   ['Crimp isolant','Hauteur réf. 1,70 ; largeur réf. 1,76 mm'],['Traction minimum 22 AWG','39,2 N, sans contribution du sertissage isolant']],[69,105]),Spacer(1,4*mm),
  p('<b>1.</b> Réaliser un échantillon avec l’outillage qualifié pour le contact et le fil. Ne pas étamer les brins avant sertissage. Contrôler les profils et la retenue selon la procédure reçue.'),
  p('<b>2.</b> Vérifier cuivre et isolant retenus, absence de brins libres et contact non déformé. Les dimensions de procédure ne sont pas un plan de fabrication du contact reconstruit.'),
  p('<b>3.</b> Introduire les contacts sertis depuis l’arrière du boîtier, vérifier leur retenue et reporter chaque fil dans la table. Garder les cinq pièces de réserve séparées.'),
  p('<b>4.</b> Contrôler continuité et absence de courts-circuits, puis poser verticalement hors tension. Retirer en tenant le boîtier, pas les fils.'),
  banner('La notice de l’outil Molex 63811-8700 est la référence de procédure. Une pince générique n’est pas certifiée par ces valeurs. Aucun achat de cette pince ni sertissage réel réalisé.'),Spacer(1,3*mm),
  ref('Notice actuelle constructeur, révision E','https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/applicationtoolingspecificationpdf/638/63811/ATS-638118700-001.pdf'),
  p('La copie historique C archivée recommande 1,09–1,65 mm ; la révision E relève le minimum à 1,30 mm. Dépouiller la révision du lot avant montage.','small'),PageBreak()]
 rows=[['Rcontact supposée*','Chute totale à 5 A*','Pertes totales*']]
 for r in calc['rows']:rows.append([f"{r['contact_resistance_assumed_ohm']*1000:.0f} mΩ",f"{r['drop_V']:.3f} V".replace('.',','),f"{r['loss_W']:.3f} W".replace('.',',')])
 story += [p('Alimentation et actionneurs','title'),
  p('Pins 2 et 4 : deux arrivées depuis le <b>même VOUT 5 V du D24V90F5</b>. Pins 6/9/14/20 : quatre retours au régulateur. À partage égal, 2,5 A par rouge et 1,25 A par retour pour la branche d’étude de 5 A.'),
  banner('<b>Le partage du courant n’est pas garanti.</b> La famille SL annonce jusqu’à 3 A sous conditions ; cela ne qualifie ni le header du Pi, ni les sertissages ou un faisceau groupé de 5 A. Un rouge seul ne doit pas porter les 5 A.'),Spacer(1,4*mm),
  table(rows,[58,58,58]),Spacer(1,2*mm),
  p('*Exemples : fil cuivre équivalent 0,326 mm², 15 cm par trajet, deux positifs et quatre négatifs en parallèle. Résistance de contact supposée, pas spécification mesurée. Terminaisons aval et tolérance du régulateur non incluses.','small'),
  p('Mesurer courants par chemin, tension au Pi, températures et creux sous caméra active. Conserver les protections externes déjà étudiées. Déclarer une source 5 A dans l’EEPROM seulement après qualification de l’alimentation.'),
  p('Deux variateurs et servo','sub'),p('Les GPIO produisent des signaux 3,3 V. Vérifier le seuil des entrées des WP16BL30 G2 avant raccordement ; le faisceau n’adapte pas les niveaux. La fiche FT90M documentée accepte ce niveau, à confirmer sur le lot.'),
  p('Le BEC du premier ESC, réglé à 6 V, alimente uniquement la puissance du servo selon le montage à finaliser. Le positif BEC du second reste isolé. Aucun +6 V sur GPIO ou rail 5 V Pi. La voie jaune de programmation Hobbywing est distincte de l’accélérateur.'),
  p('WARN1/WARN2 viennent des collecteurs optocouplés avec remontée à 3,3 V Pi. DONE rejoint la diode de logique OFF, pas l’entrée brute du relais. Les retours de puissance moteurs restent distincts des références de commande.'),
  ref('GPIO : niveaux, pas et numérotation',GPIO),ref('Famille Molex SL : limites publiées',FAMILY),PageBreak()]
 story += [p('Cotes et dégagements','title'),
  pic(ROOT/'tools/temp/gpio-review/sources/Molex-boitier-plan-miroir-original-1.png',157),
  p('Plan SD-70450-0001-0026 : archive originale inchangée via miroir IHS, ancienne révision. Crédit Molex. Les valeurs de référence du tableau sont utilisées pour l’étude.','small'),
  table([['Grandeur','Valeur / portée'],['Boîtier 40 positions','A=48,26 ; B=50,77 ; largeur 5,05 ; hauteur 15,24 mm'],
   ['Pas / broche mâle','2,54 mm ; 0,64 mm carrée ou ronde'],['CAO exacte du solide','50,7746 × 5,0546 × 15,24 mm, sans tolérances du lot'],
   ['Fil / contact','Gaine annoncée 1,5 ; contact limité à 1,63 mm'],['Pose indicative sur Pi','Centre (32,5 ; 52,5), base Z=3,876 ; sommet Z=19,116 mm']],[58,116]),Spacer(1,3*mm),
  p('Les fils montent avant de tourner vers l’extérieur du bord GPIO. Le jeu en plan au cooler serait environ <b>0,72 mm</b> dans le repère étudié. Le plan Pi donne 37,5 mm en Y entre clips du refroidisseur, contre 37 mm dans sa reconstruction existante : jeu et insertion restent à mesurer.'),
  p('Aucun montage sur Pi reçu, aucune tenue aux vibrations ni réserve de refroidissement acquise. Garder admission, ailettes, ports et transmissions dégagés. Les STEP Pi et cooler restent conservés.','small'),PageBreak()]
 story += [p('Modèles et réception','title'),pic(BASE/'3D/connecteur-gpio-faisceau-detaille.png',126),
  table([['Variante','Taille','Nature'],*[[label,f"{m['bytes']/1e6:.2f} Mo",nature] for m,label,nature in zip(cat['models'],
   ['Boîtier noir','Contact détaillé','15 contacts','Faisceau de pose'],['Solide natif transformé','Reconstruction estimée','Boîtier natif + contacts','15 fils continus, bouts ouverts'])]],[51,33,90]),Spacer(1,3*mm),
  p('Réimport STEP et contrôle indépendant FreeCAD sans interface : géométrie valide, solides fermés et enveloppes contrôlées. Contacts or/étain séparés ; quinze âmes et quinze gaines continues. Les fils proches ne se chevauchent pas et ne traversent pas le plastique.'),
  p('Les extrémités sont volontairement ouvertes : aucun connecteur RC aval ni longueur de coupe fictive. Le nombre de brins du fil n’est pas publié ; l’âme CAO est une section équivalente, pas une reconstitution d’un toron mesuré.','small'),
  p('À réception, vérifier références, orientation, contacts, diamètre de fil et contenu du lot. Contrôler sertissages, continuité, partages de courant et températures, puis les trois impulsions PWM pendant une charge vidéo. Tester les défauts de commande et le freinage avant roulage rapide.'),
  p('Ni le connecteur ni sa CAO n’ajoutent un arrêt matériel ou ne qualifient le 1080p60. Aucun avis ou essai de cette combinaison dans notre véhicule disponible. La documentation conserve les limites et refus d’accès.','small'),
  ref('Fabricant : boîtier Molex',MOLEX),ref('Fabricant : contact 16-02-0103',CONTACT),
  p('Archives originales, détails des calculs et contrôles disponibles dans les fichiers voisins. Aucun achat ni essai dans CAD View effectué.','small')]
 SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=18*mm,bottomMargin=23*mm,
  title='Drone V3 - Connecteur GPIO Molex et faisceau',author='Projet Drone V3').build(story,onFirstPage=footer,onLaterPages=footer)
 pdf=pymupdf.open(OUT);pages=[]
 for i,page in enumerate(pdf):
  png=TMP/f'page-{i+1}.png';page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(png)
  pages.append(dict(page=i+1,render=str(png.relative_to(ROOT)),chars=len(page.get_text())))
 meta=dict(file=OUT.name,pages=len(pdf),sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),generator='tools/build_gpio_pdf.py',
  generated_on='2026-10-14',renders=pages,visual_review_complete=False)
 OUT.with_suffix('.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
 print('PDF',len(pdf),'pages',OUT.stat().st_size,'bytes',flush=True);assert len(pdf)==6
if __name__=='__main__':main()
