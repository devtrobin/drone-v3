"""Four French notices with explicit quote status, CAD and receipt procedures."""
from pathlib import Path
import sys,json,html,hashlib,re
import pymupdf
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate,Spacer,Image,PageBreak,KeepTogether
from build_heatsink_pdf import p as hp,table as ht,banner as hb,GREY
from build_final_components_data import TITLES
from final_components_text import TEXT
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants';TMP=ROOT/'tools/temp/final-components/pdf'
def clean(s):
 s=str(s).replace('−','-').replace('–','-').replace('—','-').replace('‑','-')
 if re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)+',s):return s
 fixes={'mesure2S':'mesure 2S','jaune20':'jaune 20','lot5':'lot de 5','lot2':'lot de 2','blanches200':'blanches 200',
 'section47':'section 47','interne47':'interne 47','pack25':'pack 25','patin2':'patin 2','pack138':'pack 138','marge2':'marge 2',
 'à220':'à 220','choisir250':'choisir 250','Variantes20':'Variantes 20',' et20':' et 20','3contacts':'3 contacts',
 'pour2S':'pour 2S','typeXH':'type XH','FamilleXH':'Famille XH','vers5V/GND':'vers 5V/GND','provision0':'provision 0',
 'Grands pads':'Grands pads','5AétudePi':'5 A, étude Pi','TableAlbright':'Table Albright','PlanAlbright':'Plan Albright',
 'FicheAlbright':'Fiche Albright','CatalogueKlauke':'Catalogue Klauke','20cm,3positions':'20 cm, 3 positions',
 'unpatin':'un patin','d’étude142':'d’étude 142','Carte2S':'Carte 2S','future surveillance':'future surveillance',
 'voir22AWG':'voir 22 AWG','visuelle22AWG':'visuelle 22 AWG','nominalAWG':'nominal AWG','Catalogue2025':'Catalogue 2025',
 'du14/10':'du 14/10','des3contacts':'des 3 contacts','150brins':'150 brins','Deux fils séparés18AWG':'Deux fils séparés 18 AWG',
 'borneED80':'borne ED80','95R6 -':'95R6 -','fil6mm²':'fil 6 mm²','2mm':'2 mm','20mm':'20 mm',
 'familleXH':'famille XH','MIDIentrée':'MIDI entrée','MIDI→ED80':'MIDI → ED80','ED80→D+':'ED80 → D+',
 'fiche2024':'fiche 2024','calibrePi':'calibre Pi','côtéMIDI':'côté MIDI','1m':'1 m'}
 # Tags, URLs and identifiers inside attributes remain intact.
 segments=re.split(r'(<[^>]*>)',s)
 for i,part in enumerate(segments):
  if part.startswith('<'):continue
  for a,b in fixes.items():part=part.replace(a,b)
  part=re.sub(r'(\d)x(?=\d)',r'\1 x ',part)
  part=re.sub(r'(\d)(mm²|mm|cm|ft|AWG|brins|positions|contacts)(?=\b|[,;/])',r'\1 \2',part)
  segments[i]=part
 return ''.join(segments)
def p(s,style='body'):return hp(clean(s),style)
def table(rows,w):return ht([[html.escape(clean(c)) for c in row] for row in rows],w)
def banner(s):return hb(clean(s))
def ref(label,url):return p(f'<link href="{html.escape(url,quote=True)}" color="#174969">{html.escape(label)}</link>','small')
def pic(path,width=125):
 with PILImage.open(path) as im:w,h=im.size
 return Image(str(path),width=width*mm,height=width*h/w*mm)
def footer(c,d):
 c.saveState();c.setStrokeColor(colors.HexColor('#ccdbe4'));c.line(18*mm,17*mm,192*mm,17*mm)
 c.setFont('HV3',7.3);c.setFillColor(GREY);c.drawString(18*mm,12*mm,'Drone V3 | Compléments avant châssis | 14 octobre 2026 | Étude non testée')
 c.drawRightString(192*mm,12*mm,str(d.page));c.restoreState()
def main():
 sys.stdout.reconfigure(encoding='utf-8');TMP.mkdir(parents=True,exist_ok=True)
 for folder,title in TITLES.items():
  b=BASE/folder;nom=json.loads((b/'nomenclature.json').read_text(encoding='utf-8'));parts=nom['parts']
  cat=json.loads((b/'3D/catalogue.json').read_text(encoding='utf-8'));fc=json.loads((b/'3D/validation-freecad.json').read_text(encoding='utf-8'));assert fc['all_passed']
  story=[p(title,'title'),p('Choix de composants séparés et ensembles provisoires'),
   banner('<b>Documentation de projet, non achetée et non testée.</b> Châssis, visserie restante, support caméra, schéma et routage de la carte de surveillance réservés pour la phase finale.'),Spacer(1,4*mm)]
  rows=[['Référence / lot','Besoin ajouté','Prix unitaire ou lot']]
  for a in parts:
   price='À confirmer' if a['price'] is None else f"{a['price']:.2f} {a['currency']} ({a['tax']})"
   if a['price'] is not None and a['qty']>1:price+=f" ; {a['price']*a['qty']:.2f} {a['currency']} pour {a['qty']} pièces"
   rows.append([a['ref'],f"{a['qty']} {a['unit']}",price])
  if folder=='connecteurs-commande':rows.append(['WAGO 221-413 - masse du servo','1 pièce','0,75 EUR TTC GoTronic, hors port'])
  story+=[table(rows,[74,34,66]),Spacer(1,3*mm),p('Lots entiers, sans conversion monétaire ni total livré inventé. Les prix manquants restent ouverts ; pas de nouveau budget global V3 validé. Les fils 22 AWG, 6 mm², gaines et deux cosses 95R5 déjà prévus sont réutilisés.','small')]
  for a in parts:story.append(ref('Achat proposé : '+a['ref'],a['buy']))
  story.append(PageBreak())
  # Cotes bypiece are fully attributed, with source version alternatives kept.
  story.append(p('Interfaces et cotes','title'))
  story.append(p('Cotes en millimètres, sauf unité explicitement indiquée. Les détails non cotés sont reconstruits.','small'))
  for a in parts:
   group=[p(a['ref'],'sub'),p(a['role']),table([['Grandeur','Valeur','Statut'],*a['cotes']],[42,67,65]),Spacer(1,3*mm)]
   story.append(KeepTogether(group))
  story += [p('Les rayons, ressorts, coutures, filets, couleurs et détails non cotés sont des reconstructions signalées dans le JSON de chaque STEP. Ils ne sont pas des données de fabrication.','small'),PageBreak(),p('Préparation et intégration','title')]
  for i,t in enumerate(TEXT[folder]):story.append(p(f'<b>{i+1}.</b> '+html.escape(t)))
  story += [PageBreak(),p('Modèles détaillés','title')]
  images={
   'connecteurs-commande':[('jr-pololu-1925/3D/jr-complet-3contacts.png','Boîtier, capot et contacts mâles'),('jr-pololu-1925/3D/trois-commandes-terminaisons-etude.png','Trois prises avec huit contacts au total')],
   'liaisons-alimentation-surveillance':[('wago-221-413/3D/wago-221-413-detaille.png','Borne trois ports : un potentiel seulement'),('fil-18awg/3D/bntechgo-18awg-150brins.png','150 brins individuels droits ; échantillon de lecture')],
   'maintien-batterie':[('sangles-geprc/3D/sangle-geprc-20x250-detaillee.png','Sangle à plat, boucle et coutures estimées'),('3D/deux-sangles-et-patin-etude.png','Pose provisoire sans batterie ni châssis')],
   'coupure-manuelle':[('albright-ed80/3D/albright-ed80-ferme-detaille.png','État fermé : commande tirée'),('3D/ed80-et-deux-cosses-etude.png','Deux cosses M6 en pose de lecture')]
  }
  for rel,caption in images[folder]:
   story.append(pic(b/rel,105));story.append(p(caption,'small'))
  story += [p('Chaque fichier a son aperçu PNG et sa provenance JSON ; les poses de câbles ou sangles sont des études. Les structures cachées non documentées ne sont pas inventées.','small'),PageBreak(),p('Catalogue et contrôles','title')]
  rows=[['STEP (extension .step)','Solides','Taille']]
  for m in cat['models']:rows.append([m['file'].removesuffix('.step'),str(m['validation']['solids']),f"{m['bytes']/1024:.0f} Ko"])
  story += [table(rows,[132,20,22]),Spacer(1,4*mm),
   p(f"<b>{len(cat['models'])} STEP contrôlés.</b> Réimport CadQuery : géométrie, solides, enveloppe, volumes et couleurs. FreeCAD indépendant sans interface : solides fermés, validité, nombre de solides, enveloppe et volume comparables contrôlés."),
   p('Volumes hélicoïdaux : la comparaison FreeCAD utilise la même quadrature par défaut que le STEP importé CadQuery ; le contrôle adaptatif strict avant/après export reste conservé séparément. Aucun essai FreeCAD GUI ou extension CAD View effectué.','small'),
   p('Les assemblages de lecture ne constituent pas une validation des tolérances, des collisions en mouvement, du sertissage, du courant admissible ou du montage réel. Les fichiers servent à l’implantation et doivent être confrontés aux pièces reçues.','small'),PageBreak(),p('Achat, avis et sources','title')]
  for a in parts:
   story.append(p(a['ref'],'sub'));story.append(p(a['stock']));story.append(p(a['scope'],'small'));story.append(ref('Source technique',a['maker']));story.append(ref('Recherche Amazon - présence exacte à confirmer sauf feuille silicone',a['amazon_search']))
  story += [p('Les archives originales et leurs empreintes SHA256 sont répertoriées dans sources.json. Les erreurs d’accès et les différences de versions sont conservées. Un lien de recherche Amazon ne prouve ni stock, ni prix, ni livraison en France.','small'),
   p('Aucun avis précis ni vidéo YouTube avec mesures validant ces ensembles dans notre robot trouvé. Les retours fabricant BNTECHGO parlent de souplesse et de facilité de travail ; les discussions WAGO rappellent le contrôle des références. Ils ne remplacent pas les essais V3. Aucun nombre d’étoiles inter-variantes utilisé comme preuve.','small')]
  out=b/'notices'/f'notice-{folder}-v3.pdf';out.parent.mkdir(parents=True,exist_ok=True)
  SimpleDocTemplate(str(out),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=18*mm,bottomMargin=24*mm,title=title,author='Drone V3').build(story,onFirstPage=footer,onLaterPages=footer)
  d=pymupdf.open(out);pages=[];t=TMP/folder;t.mkdir(parents=True,exist_ok=True)
  for i,page in enumerate(d):
   dst=t/f'page-{i+1:02}.png';page.get_pixmap(matrix=pymupdf.Matrix(1.55,1.55)).save(dst)
   pages.append(dict(page=i+1,png=str(dst.relative_to(ROOT)),characters=len(page.get_text())))
   assert page.get_text().strip()
  data=dict(file=out.name,pages=len(d),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),rendered_pages=pages,visual_review_complete=False)
  out.with_suffix('.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  print('PDF',folder,len(d),out.stat().st_size,flush=True)
if __name__=='__main__':main()
