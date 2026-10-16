"""Six-page dossier with dated purchase links and visually reviewable CAD."""
from pathlib import Path
import json,sys,hashlib,html
import pymupdf
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate,Image,Spacer,PageBreak,Flowable
from build_heatsink_pdf import p as hp,table as ht,banner as hb,GREY
from build_pi_mount_data import AMAZON,PI,ESSENTRA

ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/fixations-raspberry-pi-5'
OUT=BASE/'notices/notice-fixations-pi-5-v3.pdf';TMP=ROOT/'tools/temp/pi-mount-review/pdf'

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
 c.setFont('HV3',7.4);c.setFillColor(GREY);c.drawString(18*mm,12*mm,'Drone V3 | Fixations du Pi 5 | 14 octobre 2026 | Etude provisoire')
 c.drawRightString(192*mm,12*mm,str(d.page));c.restoreState()

class Pattern(Flowable):
 def __init__(self):super().__init__();self.width=174*mm;self.height=48*mm
 def draw(self):
  c=self.canv;scale=.7*mm;x0=43*mm;y0=6*mm
  c.setStrokeColor(colors.HexColor('#174969'));c.setLineWidth(.8)
  c.rect(x0,y0,85*scale,56*scale)
  for x,y in [(3.5,3.5),(61.5,3.5),(61.5,52.5),(3.5,52.5)]:
   c.circle(x0+x*scale,y0+y*scale,1.35*scale,fill=0,stroke=1)
  c.setDash(2,2);c.line(x0+3.5*scale,y0+3.5*scale,x0+61.5*scale,y0+3.5*scale)
  c.line(x0+61.5*scale,y0+3.5*scale,x0+61.5*scale,y0+52.5*scale);c.setDash()
  c.setFillColor(colors.HexColor('#24313e'));c.setFont('HV3B',9)
  c.drawCentredString(x0+32.5*scale,y0-3*mm,'58 mm')
  c.drawString(x0+65*scale,y0+27*scale,'49 mm')
  c.setFont('HV3',8);c.drawString(108*mm,34*mm,'4 trous de carte : Ø2,7')
  c.drawString(108*mm,27*mm,'Contour PCB indicatif : 85 x 56')
  c.drawString(108*mm,20*mm,'Repère : bord gauche / inférieur')
  c.drawString(108*mm,13*mm,'Aucun châssis conçu ici')

def main():
 sys.stdout.reconfigure(encoding='utf-8');TMP.mkdir(parents=True,exist_ok=True)
 cat=read(BASE/'3D/catalogue.json');fc=read(BASE/'3D/validation-freecad.json');nom=read(BASE/'nomenclature.json');obs=read(BASE/'observation-amazon.json')
 assert fc['all_passed'] and len(cat['models'])==15
 story=[p('Fixations isolantes<br/>du Raspberry Pi 5','title'),p('Ewwtrey | nylon noir M2.5 | kit de 335 pièces'),
  banner('<b>Sélection documentée, non achetée et non testée.</b> Le châssis sera conçu en dernier. Hauteur de travail 10 mm et épaisseurs de montage provisoires : elles ne figent pas la fabrication.'),Spacer(1,4*mm),
  table([['Achat du lot exact','Relevé du 14 octobre 2026'],['ASIN / référence','B0DCS5C7SN / DJJRX 260018'],
   ['Prix des marchandises','1 kit : 9,98 € TTC, entier'],['Vendeur / expédition','QianHaiDian / Amazon, affiché en stock'],
   ['Livraison','Gratuite dans la session Prime consultée ; à revalider']],[52,122]),Spacer(1,3*mm),
  ref('Lien direct Amazon.fr - variante noire M2.5',AMAZON),pic(BASE/'photos/Ewwtrey-kit-original.jpg',82),
  p('Photo commerciale originale. Les 90 g et 170 x 97 x 18 mm affichés concernent le lot/article, pas chaque pièce ni la masse embarquée. Seule une mesure des pièces choisies donnera cette masse.','small'),PageBreak()]
 rows=[['Type','Taille annoncée','Kit','Étude','Réserve']]
 for e in nom['parts']:
  name=e['component'].replace('Entretoise mâle-femelle','Entretoise MF').replace('Entretoise femelle-femelle','Entretoise FF')
  rows.append([name,e['specification'],str(e['bought_in_one_kit']),str(e['used_in_study']),str(e['reserve'])])
 rows.append(['TOTAL','Un kit acheté en entier','335','20','315'])
 story += [p('Contenu du kit et allocation','title'),p('MF : mâle-femelle ; FF : femelle-femelle. « 10+6 » = corps de 10 mm et goujon mâle de 6 mm. Une vis se mesure sous la tête.'),
  table(rows,[43,67,21,21,22]),Spacer(1,4*mm),
  p('La pose étudiée utilise quatre MF 10+6, quatre écrous, huit rondelles et quatre vis de 8 mm. Les autres tailles servent aux choix ultérieurs. Inventaire selon fiche et illustration commerciale ; contenu réel à compter à réception.'),
  p('Boîte incluse, Pi et outils exclus. Le devis ajoute 9,98 € pour le kit entier ; aucun prix au prorata des seules pièces montées. Total livré égal à 9,98 € si la gratuité affichée s’applique, sinon frais réels à ajouter. Aucun nouveau budget global V3 établi.','small'),PageBreak()]
 story += [p('Interfaces et cotes de référence','title'),Pattern(),Spacer(1,3*mm),
  table([['Cote','Statut'],['Pi 5 : 4 trous Ø2,7, rectangle 58 x 49','Plan officiel, approximatif, pour référence'],
   ['Centres : 3,5 / 61,5 en X ; 3,5 / 52,5 en Y','Déduits du plan, dans le repère indiqué'],
   ['Filetage commercial M2.5','Annonce du lot ; pas 0,45 supposé en CAO'],
   ['Surplats entretoises / écrou : 5 mm','Estimation, pas un plan du fournisseur'],
   ['Tête : Ø4,7, hauteur 2 ; écrou : hauteur 2','Dimensions estimées ; formes photographiques'],
   ['Rondelle : Ø5 / Ø2,7 / épaisseur 0,5','Trois cotes estimées, à mesurer'],
   ['MF : taraudage borgne min(6,5 ; L-2)','Hypothèse CAO ; profondeur réelle inconnue'],
   ['FF : taraudage traversant','Hypothèse CAO ; lot à contrôler']],[86,88]),Spacer(1,4*mm),
  p('Le plan du Pi est explicitement non destiné à produire des données de fabrication. Les deux trous du cooler ont une autre fonction. Les repères Ø6 aux fixations ne certifient pas tous les dégagements des composants en 3D.'),
  p('Les images haute définition confirment les corps MF et FF hexagonaux ; leur surplats reste estimé. Le catalogue Essentra illustre le pas usuel, sans définir ce kit.','small'),
  ref('Plan mécanique officiel Raspberry Pi 5',PI),PageBreak()]
 story += [p('Montage provisoire à quatre points','title'),
  p('Corps MF de 10 mm sous le Pi, goujon vers le haut. Un écrou et une rondelle retiennent la carte ; une vis de 8 mm et une rondelle fixent chaque corps au panneau futur.'),
  pic(BASE/'3D/quatre-fixations-pi-5-10mm-etude.png',145),
  p('<b>PCB et châssis intentionnellement absents du STEP.</b> Les vingt pièces sont seules, sur le rectangle de fixation du Pi. Aucun trou de châssis ni épaisseur de fabrication définitive n’est décidé.','small'),
  table([['Hypothèse de pose','Calcul d’étude'],['Carte 1,6 ; panneau 2 ; rondelles 0,5','Épaisseurs temporaires, pas mesurées'],
   ['Engagement de la vis inférieure','8 - 2 - 0,5 = 5,5 mm'],['Fond MF supposé à 6,5 mm','Marge avant butée : 1 mm'],
   ['Goujon / carte / rondelle / écrou','6 - 1,6 - 0,5 - 2 = 1,9 mm dépassant']],[80,94]),Spacer(1,3*mm),
  p('La longueur des vis dépendra de l’épaisseur réelle et du taraudage reçu. Réserver les accès microSD, USB, bouton, GPIO et circulation d’air. Vérifier que les quatre appuis sont coplanaires et ne déforment pas le PCB.','small'),PageBreak()]
 groups=[]
 for i,m in enumerate(cat['models']):
  short=m['file'].replace('.step','')
  groups.append([short,str(m['validation']['solids']),f"{m['bytes']/1024:.0f} Ko"])
 story += [p('Modèles détaillés et contrôles','title'),
  p('Quinze STEP noirs en millimètres : neuf entretoises, trois vis, un écrou, une rondelle et une pose à quatre points. Chaque fichier possède son aperçu et un JSON de provenance.'),
  table([['Fichier (extension .step)','Solides','Taille'],*groups],[134,19,21]),Spacer(1,4*mm),
  p('Filetages intérieurs et extérieurs hélicoïdaux, entrées chanfreinées, crêtes/fonds simplifiés, tête et empreinte cruciforme reconstruits. Jeu radial de représentation 0,03 mm estimé, aucune classe de tolérance attribuée.'),
  p('Réimport CadQuery : validité, solides, enveloppes, volumes et couleurs contrôlés. FreeCAD sans interface : quinze fichiers contrôlés indépendamment, solides fermés et géométries valides. Les cinq pièces d’un point de pose ne présentent pas de chevauchement volumique détecté.'),
  p('Aucun essai dans FreeCAD GUI ou CAD View, ni montage physique. Les CAO existantes du Pi, du cooler et du GPIO sont inchangées. Ces reconstructions servent à l’implantation ; elles ne sont ni des jauges, ni des plans de production, ni une preuve de résistance.','small'),PageBreak()]
 story += [p('Réception, avis et sources','title'),
  p('À réception et pendant l’étude finale','sub'),
  p('Contrôler référence, quantité, formes, pas et profondeurs. Choisir hauteur et vis après implantation. Engager les filets à la main, serrer progressivement avec un petit outil adapté, sans fléchir la carte ni atteindre le fond. Aucun couple constructeur chiffré du lot trouvé.'),
  p('Vérifier maintien et dégagements avant alimentation, puis après essais progressifs. Les rondelles ne rendent pas les écrous autofreinés. Température admissible, qualité de nylon et tenue aux vibrations/chocs du robot ne sont pas établies.'),
  p('Avis consultés : 4,6/5 sur 871 évaluations','sub'),
  p('La note regroupe plusieurs tailles et couleurs. Deux avis de la variante noire M2.5, Gallimard (27/09/2026) et RL (24/05/2026), décrivent des montages électroniques utiles et un vissage satisfaisant ; sans mesures ni essais sur notre Pi 5.'),
  p('Un avis allemand de la variante noire apprécie la surélévation des cartes. Un avis italien du 22/12/2024 décrit un DAC sur Raspberry Pi avec le kit blanc : autre couleur, modèle du Pi inconnu. Aucun essai de ce kit exact trouvé sur forum ou YouTube.','small'),
  ref('Fiche exacte, images et avis Amazon.fr',AMAZON),
  ref('Avis noir M2.5 de Gallimard','https://www.amazon.fr/portal/customer-reviews/srp/-/RVVUFD9D8AD8U/'),
  ref('Avis noir M2.5 de RL','https://www.amazon.fr/portal/customer-reviews/srp/-/R2ETNH017T6C07/'),
  p('Documents conservés et fidélité','sub'),
  ref('Raspberry Pi Ltd : plan mécanique original',PI),
  ref('Essentra : catalogue original de fixations plastiques',ESSENTRA),
  p('Deux PDF originaux archivés inchangés, quatre images commerciales, observation datée, calculs, devis et sources dans le dossier. Essentra est un autre fabricant : seule l’hypothèse de pas M2.5 x 0,45 est retenue, pas ses dimensions ou caractéristiques de matière.'),
  p('<b>Aucune notice constructeur propre au kit identifiée.</b> Ce PDF est la notice d’étude de Drone V3. Les cotes non publiées restent des hypothèses, et la hauteur finale sera décidée au moment du châssis, dernier composant.','small')]
 SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=18*mm,bottomMargin=23*mm,
  title='Drone V3 - Fixations nylon du Raspberry Pi 5',author='Projet Drone V3').build(story,onFirstPage=footer,onLaterPages=footer)
 doc=pymupdf.open(OUT);renders=[]
 for i,page in enumerate(doc):
  png=TMP/f'page-{i+1}.png';page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(png)
  body=[]
  for b in page.get_text('dict')['blocks']:
   if b.get('type')==0:
    for line in b['lines']:
     for span in line['spans']:
      if span['bbox'][1]<780:body.append(span['bbox'][3])
  renders.append(dict(page=i+1,render=str(png.relative_to(ROOT)),chars=len(page.get_text()),body_bottom_pt=max(body) if body else 0,links=len(page.get_links())))
 meta=dict(file=OUT.name,pages=len(doc),sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),bytes=OUT.stat().st_size,
  generated_on='2026-10-14',generator='tools/build_pi_mount_pdf.py',renders=renders,visual_review_complete=False)
 OUT.with_suffix('.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
 print('PDF',len(doc),'pages',OUT.stat().st_size,'bytes',flush=True);assert len(doc)==6,len(doc)

if __name__=='__main__':main()
