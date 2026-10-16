"""One French project notice, manufacturer originals unchanged, full-page QA renders."""
from pathlib import Path
import sys,json,html,re,hashlib
import pymupdf
from PIL import Image as PILImage,ImageDraw,ImageFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate,Spacer,Image,PageBreak,Table,TableStyle
from build_heatsink_pdf import p as hp,table as ht,banner as hb,GREY
from build_main_cord_data import PARTS,INTEGRATION,SOURCES
from format_main_cord_text import human
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/cordon-principal-batterie';TMP=ROOT/'tools/temp/main-cord/pdf'
def clean(s):
 s=human(str(s)).replace('−','-').replace('–','-').replace('—','-').replace('‑','-')
 for a,b in [('du15octobre2026','du 15 octobre 2026'),('SOLISTRAND130191','SOLISTRAND 130191'),('TE130191','TE 130191'),('BNTECHGO12AWG','BNTECHGO 12 AWG'),('ATUM8/2','ATUM 8/2'),('AMASS2026','AMASS 2026'),('V1.2historique','V1.2 historique'),('MIDI60A','MIDI 60 A'),('guideTE','guide TE'),('MiniBusD-','MiniBus D-'),('MiniBus2315','MiniBus 2315'),('Pack2S','Pack 2S'),('lot10ft','lot 10 ft'),('AmazonUS','Amazon US'),('MIDIentrée','MIDI entrée'),('D-N2','D- N2'),('fiche2025','fiche 2025'),('canon7,3','canon 7,3'),('FIL12','FIL 12'),('planA3','plan A3'),('catalogue2026','catalogue 2026')]:s=s.replace(a,b)
 s=re.sub(r'(\d)(mm²|mm|cm|ft|AWG|brins|solides|pages|EUR|USD|N·m|in-lb|contacts|minutes|min|A\b)',r'\1 \2',s)
 s=re.sub(r'(?i)\b(fil|fils|silicone|section|oeil|paume|canon|épaisseur|longueur|outil|matrice|guide|barre|rétraction|pièce|cosse|cosses|lot)(?=\d)',r'\1 ',s)
 s=re.sub(r'(\d)(?=[A-Za-zÀ-ÿ])',lambda m:m.group(0),s)
 s=re.sub(r'(\d)\s*×\s*(?=\d)',r'\1 × ',s)
 return s
def p(s,style='body'):return hp(clean(s),style)
def table(rows,widths):return ht([[html.escape(clean(c)) for c in row] for row in rows],widths)
def banner(s):return hb(clean(s))
def ref(label,url):return p(f'<link href="{html.escape(url,quote=True)}" color="#174969">{html.escape(label)}</link>','small')
def pic(path,width):
 with PILImage.open(path) as im:w,h=im.size
 return Image(str(path),width=width*mm,height=width*h/w*mm)
def footer(c,d):
 c.saveState();c.setStrokeColor(colors.HexColor('#ccdbe4'));c.line(18*mm,17*mm,192*mm,17*mm)
 c.setFont('HV3',7.2);c.setFillColor(GREY);c.drawString(18*mm,12*mm,'Drone V3 | Cordon principal | 15 octobre 2026 | Étude non testée')
 c.drawRightString(192*mm,12*mm,str(d.page));c.restoreState()
def main():
 sys.stdout.reconfigure(encoding='utf-8');TMP.mkdir(parents=True,exist_ok=True)
 cat=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'));fc=json.loads((BASE/'3D/validation-freecad.json').read_text(encoding='utf-8'));assert fc['all_passed']
 story=[p('Cordon principal<br/>batterie vers distribution','title'),p('XT60H-M, deux fils 12 AWG, deux cosses TE 130191'),banner('<b>Version d’étude conservant le pack Zeee 2S actuel.</b> Le montage mécanique est documenté ; <b>44 A continus ne sont pas validés</b>. Pas de changement de batterie, de budget ou de performances décidé. Aucun matériel acheté ou testé.'),Spacer(1,3*mm),
  table([['Pièce / besoin','Approvisionnement proposé'],['XT60H-M + capot, une prise','Lot déjà prévu, sinon AMASS exact chez TME'],['BNTECHGO 12 AWG, rouge et noir','≈0,20 m par couleur, lot existant ; Amazon.fr 31,93 EUR affichés'],['TE SOLISTRAND 130191, deux cosses','Deux pièces ajoutées ; prix indicatif 1,344 EUR TTC hors port'],['ATUM-8/2, deux coupes ≈20 mm','Même barre déjà prévue ; pas de deuxième lot']],[78,96]),Spacer(1,2*mm),
  pic(BASE/'3D/cordon-principal-xt60-12awg-etude.png',105),p('Ensemble léger : prise, conducteurs continus, cosses et isolation. Longueurs et pose provisoires ; paumes métalliques volontairement accessibles pour les bornes.','small'),PageBreak(),p('Interfaces : prise et cosses','title')]
 for index in [0,2]:
  a=PARTS[index];story += [p(a['ref'],'sub'),p(a['role']),table([['Grandeur','Valeur','Provenance'],*a['cotes']],[40,63,71]),Spacer(1,3*mm)]
 story += [p('Le MiniBus utilise un goujon #10-32 : l’œil M5 Ø5,26 passe nominalement, mais l’écrou demeure #10-32. Appui, rondelles et capots à vérifier. Révisions et cotes divergentes conservées sans mélange.','small'),PageBreak(),p('Fils, isolation et pertes','title')]
 for index in [1,3]:
  a=PARTS[index];story += [p(a['ref'],'sub'),table([['Grandeur','Valeur','Provenance'],*a['cotes']],[40,72,62]),Spacer(1,2*mm)]
 story += [p('Provision : 0,20 m de chaque couleur. Le besoin connu du même lot passe de 0,40 à 0,60 m par couleur, sur 3,048 m disponibles si le lot est effectivement acheté. Les fils d’usine du pack/ESC restent distincts.','small'),
  p('Pas d’ampacité déduite de 200 °C ou de la seule section. Le volume rempli du STEP global suit l’enveloppe Ø2,41 ; il ne donne pas la masse du cuivre. Manchon installé et retrait réel sont différents des cotes libres.','small'),PageBreak(),p('Préparation et raccordements','title')]
 for i,t in enumerate(INTEGRATION[:7]):story.append(p(f'<b>{i+1}.</b> '+html.escape(t)))
 story += [PageBreak(),p('Contrôles et dimensionnement','title')]
 for i,t in enumerate(INTEGRATION[7:],start=8):story.append(p(f'<b>{i}.</b> '+html.escape(t)))
 calc=json.loads((BASE/'calculs.json').read_text(encoding='utf-8'))
 rows=[['Courant de calcul','Chute des fils','Pertes des fils']]
 for a in calc['rows']:rows.append([f"{a['current_A']} A",f"{a['drop_V']*1000:.1f} mV",f"{a['loss_W']:.2f} W"])
 story += [table(rows,[58,58,58]),Spacer(1,2*mm),p('R = 5,06 mΩ/m ×0,40 m = 2,024 mΩ pour les deux fils. Conditions de résistance non précisées par BNTECHGO ; contacts, soudures, cosses, pack, MIDI, ED80 et rails exclus. Ce calcul ne valide ni l’échauffement ni l’autonomie.','small'),PageBreak(),p('Devis et retours utilisateurs','title'),
  p('<b>Fil : 31,93 EUR affichés sur Amazon.fr</b> pour B01ABOPMEI, titre 12 AWG/680 brins/10 ft par couleur, « En stock », vendeur et expéditeur Amazon US. Le total livré à la destination finale n’est pas vérifié. Réutiliser le même lot prévu ; ne pas acheter un lot pour chaque branche.'),
  p('<b>Cosses : 0,672 EUR TTC indicatifs par pièce</b> dans un résultat DigiKey indexé, soit 1,344 EUR pour deux. Page directe inaccessible ; stock, TVA et prix actuels à revalider. Fil + cosses = 33,274 EUR partiels, hors prise, gaine, frais et outils. Ce n’est ni le coût supplémentaire du seul cordon ni un total V3.'),
  p('TME propose la référence AMASS XT60H-M ; prix et stock actuels non confirmés. Prise et gaine proviennent si possible des lots déjà prévus. L’ancienne fiche Amazon.fr B074PN6N4K a un titre incohérent et affiche indisponible : écartée comme preuve d’achat. Aucun ASIN français TE 130191 exact retrouvé.'),
  ref('Achat fil : Amazon.fr B01ABOPMEI','https://www.amazon.fr/dp/B01ABOPMEI'),ref('Prise exacte : AMASS XT60H-M chez TME',PARTS[0]['buy']),ref('Cosses à l’unité : TE 130191 chez DigiKey',PARTS[2]['buy']),ref('Gaine partagée : TE/Raychem ATUM-8/2',PARTS[3]['buy']),
  p('Deux avis 5/5 du 7 mars 2025 sont visibles chez La Camera Embarquée pour un XT60H-M avec jupe. L’un indique « Conforme a mes attentes ». Aucun courant, température ni résistance mesuré : ce retour ne qualifie pas le cordon. Le prix de 1,10 EUR y figure sous « Prix HT » ; TVA et délai à confirmer. Sa revendication 60 A continus n’est pas reprise.'),
  ref('Offre alternative et deux avis XT60H-M','https://www.lacameraembarquee.fr/cables-adaptateurs-connecteurs-fpv/14943-connecteur-amass-xt60h-male-avec-jupe-lemonfpv.html'),
  p('RCCrawler (juin 2020) évoque prises authentiques et maintien des contacts par moitié complémentaire. Guide HobbyKing : préparer fil et godet, conserver tous les brins, contrôler avant gaine. Témoignages et guide pratique, pas essai du montage V3. Pas de vidéo instrumentée exacte retrouvée ou présentée comme visionnée intégralement.'),
  ref('Forum utilisateurs RCCrawler2020','https://www.rccrawler.com/forums/threads/battery-connectors.618927/'),ref('Guide pratique propre à HobbyKing','https://hobbyking.com/blog/xt60-soldering-guide-for-rc-builds'),PageBreak(),p('Modèles et traçabilité','title')]
 rows=[['STEP','Solides','Taille']]
 for m in cat['models']:rows.append([m['file'].removesuffix('.step'),str(m['validation']['solids']),f"{m['bytes']/1024:.0f} Ko"])
 story += [table(rows,[130,20,24]),Spacer(1,3*mm),p(f'<b>{len(cat["models"])} STEP contrôlés</b> par réimport CadQuery et import FreeCAD indépendant sans interface : solides fermés, validité, nombre de solides, enveloppes, volumes et sondes d’occupation. Couleurs conservées. Cela ne constitue pas un essai dans l’interface FreeCAD ou CAD View.'),
  p('Les deux échantillons de fil contiennent chacun 680 brins +une gaine ; ouvrir l’ensemble léger pour l’implantation. Le cuivre et la gaine du cordon sont chacun un solide continu par pôle, sondé radialement sur quatre segments ; raccords godet/soudure/conducteur/cosse sans jeu CAO. L’empreinte W réelle n’est pas connue : le canon serti cylindrique est illustratif.'),
  Table([[pic(BASE/'cosses-te-130191/3D/te-130191-nue-detaillee.png',77),pic(BASE/'3D/terminaison-cosse-isolee-detail.png',77)]],colWidths=[87*mm,87*mm]),
  p('Cosse nue et terminaison isolée, vues à échelles distinctes. Échantillon court à extrémité ouverte intentionnelle ; dans l’ensemble complet, chaque conducteur aboutit à un godet et une cosse.','small'),
  p('Documents originaux conservés : catalogue AMASS2026, ficheV1.2, ficheTE130191 viaLCSC (4pages), deux révisionsTE408-1542 viaFarnell/TME. PlanTEA3 et STEPnatifs non téléchargés (403), guideSOLISTRAND lu en ligne. Notices fil/ATUM partagées dans leurs dossiers existants. SHA256 et limites consignés dans assets.json et les JSON voisins des modèles.','small'),PageBreak(),p('Sources de référence','title')]
 for source in SOURCES:
  if source['type']=='marketplace_rejected':continue
  story.append(ref(source['id']+' : '+source['supports'],source['url']))
 story += [p('Les PDF fabricants archivés sont inchangés. La présente notice est une documentation du projet, pas une notice constructeur ni une validation de courant. Les sources actuellement inaccessibles sont identifiées comme telles dans assets.json. Châssis, fixations finales, support caméra et carte de surveillance restent à concevoir lors de la phase finale.','small')]
 out=BASE/'notices/notice-cordon-principal-batterie-v3.pdf'
 doc=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=18*mm,bottomMargin=23*mm,title='Drone V3 - Cordon principal batterie vers distribution',author='Projet Drone V3')
 doc.build(story,onFirstPage=footer,onLaterPages=footer)
 pdf=pymupdf.open(out);pages=[]
 for i,page in enumerate(pdf):
  render=TMP/f'page-{i+1}.png';page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(render);pages.append(dict(page=i+1,render=str(render.relative_to(ROOT)),chars=len(page.get_text())))
 out.with_suffix('.json').write_text(json.dumps(dict(file=out.name,pages=len(pdf),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),generated_on='2026-10-15',renders=pages,visual_review_complete=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 cols=2;thumbw=570;thumbh=810;rows=(len(pages)+1)//2;sheet=PILImage.new('RGB',(cols*thumbw,rows*thumbh),'#d8dfe3')
 for i,a in enumerate(pages):
  im=PILImage.open(ROOT/a['render']).convert('RGB');im.thumbnail((thumbw-12,thumbh-12));sheet.paste(im,((i%2)*thumbw+6,(i//2)*thumbh+6))
 sheet.save(TMP/'contact-sheet.png');print('PDF',len(pdf),'pages',out.stat().st_size,'bytes',flush=True)
if __name__=='__main__':main()
