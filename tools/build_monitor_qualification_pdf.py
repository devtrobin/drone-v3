"""Six-page M1P prototype/bench annex, with explicit unclosed release gates."""
from pathlib import Path
import hashlib,json,sys
import pymupdf
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate,Spacer,PageBreak,Table
from reportlab.graphics.shapes import Drawing,Rect,Line,String
from build_heatsink_pdf import p as base_p,table as base_table,banner as base_banner,BLUE,GREY
from build_monitor_pdf import picture,source
from monitor_typography import clean

ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Composants/carte-surveillance-electrique'
OUT=B/'notices/annexe-preparation-fabrication-essais-m1p.pdf'
TMP=ROOT/'tools/temp/surveillance-review/qualification-pdf'

def p(text,*args,**kwargs):return base_p(clean(text),*args,**kwargs)
def banner(text,*args,**kwargs):return base_banner(clean(text),*args,**kwargs)
def table(rows,*args,**kwargs):return base_table([[clean(c) for c in row] for row in rows],*args,**kwargs)

def footer(c,d):
    c.saveState();c.setStrokeColor(colors.HexColor('#cad9e0'));c.line(18*mm,17*mm,192*mm,17*mm)
    c.setFont('HV3',7.2);c.setFillColor(GREY);c.drawString(18*mm,12*mm,'Drone V3 | M1P | Fabrication prototype / banc limité | Aucun essai réalisé')
    c.drawRightString(192*mm,12*mm,str(d.page));c.restoreState()

def bench_diagram():
    d=Drawing(174*mm,91*mm)
    def txt(x,y,t,size=8):d.add(String(x*mm,y*mm,t,fontName='HV3',fontSize=size,fillColor=BLUE))
    def rect(x,y,w,h,t):
        d.add(Rect(x*mm,y*mm,w*mm,h*mm,strokeColor=BLUE,fillColor=colors.HexColor('#edf4f7')));txt(x+2,y+h/2-1,t)
    def line(x,y,a,b):d.add(Line(x*mm,y*mm,a*mm,b*mm,strokeColor=BLUE,strokeWidth=1))
    rect(0,65,44,15,'AUX 7,4 V / CC250 mA');rect(56,65,39,15,'4,7 ohms / >=25 W');rect(110,65,63,15,'Porteuse J1 : AUX et D-')
    line(44,73,56,73);line(95,73,110,73)
    rect(0,36,60,15,'C1 : 0-4,2 V / CC20 mA');rect(0,13,60,15,'C2 : 0-4,2 V / CC20 mA')
    rect(84,24,38,21,'3 x100 ohms');rect(135,24,38,21,'J2 B0/B1/B2_R')
    line(60,44,73,44);line(73,44,73,39);line(73,39,84,39)
    line(60,20,73,20);line(73,20,73,29);line(73,29,84,29);line(122,34,135,34)
    txt(0,5,'C1 et C2 en serie ; B0 relie a D- AVANT RA0, jamais apres.',7.8)
    txt(0,86,'Principe de banc : les trois sources sont distinctes et limitees.',8.4)
    txt(83,12,'EVM poses sur supports isolants separes',7)
    return d

def main():
    sys.stdout.reconfigure(encoding='utf-8');TMP.mkdir(parents=True,exist_ok=True)
    c=json.loads((B/'verification/coordination-protections.json').read_text(encoding='utf-8'));a=c['adiabatic_screen'];t=c['bench']
    m=json.loads((B/'fabrication/manifest.json').read_text(encoding='utf-8'))
    story=[p('Préparer la fabrication<br/>et les essais','title'),p('Surveillance2S - révisionM1P -15 octobre2026'),
      banner('<b>Porteuse préparée pour fabrication de prototype sur banc limité.</b> Aucun matériel acheté, fabriqué ou testé. Le raccordement à la LiPo et au véhicule reste non libéré.'),
      table([['État','Résultat de cette passe'],['Porteuse KiCad','Schéma et routage contrôlés : ERC0, DRC0, connexions manquantes0, parité0.'],['Cuivre renforcé','Alimentation0,40 mm ; signaux0,20 ; cuivre70 micromètres nominal /55 minimum.'],['Dossier de fabrication','Gerbers, perçages PTH/NPTH, positions, spécification et manifest SHA256. Aucun envoi ou achat.'],['Banc fonctionnel','Câblage, limites de sources, paliersB00-B14 et fichier de résultats vierge.'],['Cotes TI exactes','Non disponibles dans le guide ; Gerbers401. Pas2,54 spécifié ; contour seulement relevé.'],['Coordination LiPo','Non prouvée : fusion nominale ≠ coupure totale maximale. Essais et preuves complémentaires nécessaires.']],[48,126]),Spacer(1,3*mm),
      p('Les modules restent2xTPS3700EVM-114,2xTMR1-0511 et1xPololu2831. Les seuils et le brochage logique restent ceux deM1 : avertissement actif haut, coupure dure indépendante de Linux.'),
      p('Cette annexe complète la notice principale. Pour fabriquer la porteuse seule, les dimensions exactes de contour TI ne sont pas nécessaires : les modules sont reliés par câbles, sans socle compatible inventé. Au banc, ils restent sur supports isolants séparés.','small'),PageBreak(),
      p('Dimensions TI : preuve disponible','title'),
      picture(B/'modules/TI-vue-routage-originale-page5.png',110,112),Spacer(1,3*mm),
      p('Extrait vectoriel original TI SLVU683A, figure4, page5. Treize entraxes de broches sont comparés au pas2,54 mm donné dans la BOM p.8. Le dessin donne environ <b>51,05 x48,26 mm</b> pour le contour. Il s’agit d’une <b>inférence sans tolérance fabricant</b>, et non d’un plan de perçage.'),
      table([['Grandeur','Statut'],['Pas des connecteurs','2,54 mm spécifié ; J1-J9 à2 broches communes, J10/J11 à3.'],['Contour / épaisseur / hauteur','Contour relevé seulement ; épaisseur et hauteur assemblée exactes inconnues.'],['Fixations','Aucun entraxe de trous de montage certifié ; ne pas utiliser des vias comme fixations.'],['Réservation','60 x60 x12 par module ; garde d’implantation à confirmer à réception. Porteuse+modules :140 x75 x30, hors pièces extérieures.']],[48,126]),
      p('Le dossier conserve le calcul reproductible, la source SHA256 et les échecs de téléchargement. Pour fermer la cote exacte : obtenir normalement SLVC413 depuis TI, relever contour/perçages et révision, ou mesurer l’exemplaire reçu et son incertitude. Aucun accès à un compte ni demande au fabricant effectué.','small'),
      source('Source TI : guide, schéma, BOM et vues','https://www.ti.com/lit/pdf/SLVU683'),PageBreak(),
      p('Protections : calcul et décision','title'),
      table([['Protection','Ce qui est établi'],['FAUX1 A / KLKD001.T','Secours de la branche auxiliaire. Ne borne pas le courant à1 A ; conditions DC et énergie de coupureR2 encore ouvertes.'],['F1/F2 /0454.500MR','Deux500 mA lents recommandés parTRACO pour les entrées5 V. Fusion nominale0,240 A²s, pas une énergie maximale de coupure.'],['RA0/RA1/RA2','100 ohms /3 W au départ de chaque fil de mesure. Scénario batterie seule : <=93,3 mA et0,784 W ; pas une protection universelle contre toutes les pannes d’isolement.']],[48,126]),Spacer(1,3*mm),
      table([['Comparaison de cuivre*','Budget de contrôle40 ->105 °C'],['Ancienne piste0,20 /25 micromètres min',f"{a['previous_trace_I2t_A2s']:.3f} A²s"],['M1P alimentation0,35 /55 minimum',f"{a['new_power_trace_I2t_A2s']:.3f} A²s"],['M1P signaux0,175 /55 minimum',f"{a['new_signal_trace_I2t_A2s']:.3f} A²s"]],[104,70]),
      p('*Modèle adiabatique de piste uniforme : densité8960 kg/m³, capacité385 J/kg/K, résistivité20 °C1,724e-8 ohm.m, coefficient0,00393/K. Hypothèses d’ingénierie explicites, pas de certification de l’ensemble. Longues durées et étranglements requièrent une étude distincte.','small'),
      p('La fiche fusible autorise jusqu’à60 s à1 A,3 s à1,5 A et0,1 s à4 A. L’énergie totale maximale aux conditions réelles du pack manque. Le «1 A» du Pololu est sa capacité de sortie, pas une borne de défaut garantie. La chaîne LiPo ne peut donc pas être déclarée coordonnée sur ces seules données.'),
      banner('Pour avancer : fabriquer le prototype, réaliser la campagne bornée et relever ses résultats. La qualification véhicule exige une enveloppe maximale de coupure ou une limitation électronique démontrée, ainsi que la fermeture des conditionsR2.'),
      source('Littelfuse452/454 : caractéristiques de la série','https://www.littelfuse.com/assetdocs/littelfuse-fuse-452-454-datasheet?assetguid=8c87aa93-80a7-4ea8-8749-a19ba03901c2'),PageBreak(),
      p('Fabrication de la porteuse seule','title'),
      picture(B/'3D/porteuse-surveillance-2s-m1-detaillee.png',150,96),Spacer(1,3*mm),
      table([['Demande de fabrication','Valeur à faire accepter'],['PCB','FR4,140 x75 x1,6 mm ; épaisseur±0,16 ; contour±0,20 ; centres de trous±0,10.'],['Cuivre fini','70 micromètres nominal /55 minimum sur les deux faces ; alimentation0,40 /0,35 min gravée ; signaux0,20 /0,175 min.'],['Vias et règles','Ø0,80 / trou finiØ0,40 ; paroi>=20 micromètres ; isolement0,15. Le fabricant doit accepter ces règles avec le cuivre demandé.'],['Exports contrôlés',f"{m['native_pth_count']} perçages métallisés dont{m['vias']} vias ;{m['native_npth_count']} fixations non métallisées. Coordonnées identiques au PCB. Contour140 x75 vérifié dans le Gerber."],['Montage','R7/R8 DNP sur porteuse, rappels installés côtéPi. EVM et Pololu2831 par faisceaux ; RA et FAUX horsPCB.']],[47,127]),
      p('Le ZIP de fabrication contient les Gerbers cuivre/masque/sérigraphie/contour, les perçages séparés et leurs cartesSVG, les positionsCSV, la spécification et les SHA256. Pas de stencil de pâte validé. Demander le contrôle électrique du PCB nu et inspecter cotes, métallisation et brochages avant montage.','small'),
      banner('La fabrication décrite nécessite deux couches et des trous métallisés. Elle ne constitue pas un programme CNC. Les modèles STEP servent à l’implantation et à la revue, pas à remplacer les fichiers de cuivre et de perçage.'),PageBreak(),
      p('Banc : câblage et énergie bornée','title'),bench_diagram(),
      table([['Source / élément','Exigence avant connexion'],['AUX de laboratoire','Sortie<=8,4 V ; CC réglée250 mA ; maximum accepté300 mA après10 ms. Capacité de sortie connue<=470 microfarads avant la résistance.'],['Résistance série','4,7 ohms />=25 W /5 % ou mieux ; minimum garanti4,4 ohms avec température. Placée au départ de la source, montage et dissipation conformes à sa fiche.'],['Cellules simulées','Deux voies flottantes isolées, capables d’absorber un petit retour,0-4,2 V /20 mA chacune ; trois100 ohms au départ versJ2.'],['InterfacePi simulée','3,3 V /5 mA pour rappels47k ; OFF chargé par10k versD- ; Pi et2813 débranchés au premier palier.'],['Mesure','Voltmètres et sonde différentielle. Pas de pince de masse oscilloscope qui relie deux références isolées.']],[47,127]),
      p(f"Contrôle du trajet d’entréeAUX : pointe bornée par la résistance à{t['maximum_initial_limited_current_A']:.3f} A, budget avantCC{t['screening_I2t_before_CC_settles_A2s']:.4f} A²s. Ce calcul est conditionnel aux caractéristiques de la source et ne se transpose pas au secondaire du convertisseurM5."),
      banner('SansLiPo, chargeur, moteurs ni alimentation de puissancePi. Ne pas débuter par un court-circuit de la carte. Vérifier les sources sur charge fictive, puis monter et alimenter par étapesB00-B03.'),PageBreak(),
      p('Essais et critères de passage','title'),
      table([['Paliers','Contrôles à consigner'],['B00-B03','Sources documentées ; inspection et adaptationsTI ;3V3_AUX et5V_MON ; ajouter unTMR à la fois. Couper si5V_MON/TMR ne s’établit pas.'],['B04-B07','Cellules à4,0 V puis descente/remontée voie par voie. Relever warning, coupure, hystérésis, niveaux et délais.'],['Fenêtres en descente','Coupure3,258-3,420 V ; avertissement3,466-3,636 V. WARN bas<0,4 V / haut>2,8 V ; OFF chargé>1,5 V en défaut.'],['B08-B12','PerteM5/TMR, DONE, câblesWARN etB0/B1/B2 ; relever les pannes non détectées, notammentB1 ouvert et perte communeAUX/D-.'],['B13','Endurance30 min, ambiante<=40 °C ; élévation pistes/connecteurs<=10 °C ; chaque boîtier garde>=20 °C sous son maximum recommandé.'],['B14','100 ohms isolée horsPCB/pack, source8,4 V limitée150 mA ; mesurer courant et température. Aucun court-circuit deLiPo.']],[43,131]),Spacer(1,3*mm),
      p('Les protocoles détaillés sont dans verification/banc-essais.md ; resultats-banc.csv comporte les15 lignesB00-B14 marquées <b>NON RÉALISÉ</b>. Ne pas confondre critères attendus et résultats mesurés. Les instruments, réglages, incertitudes et captures sont à joindre.'),
      p('Après réussite : mesurer l’entréeOFF réelle du2813 avec charge fictive légère, tester le réarmement pendant un défaut, puis lePi sans moteurs et son logiciel d’extinction. La charge10k ne prouve pas le comportement complet du2813. Les transitoires moteur et la coordination véhicule viennent ensuite.'),
      banner('<b>État restant ouvert :</b> cotes mécaniques exactesTI et supports définitifs ; coordination maximale de la chaîneLiPo ; essais électriques et thermiques ; logicielPi et comportement du2813. La réussite du banc fonctionnel ne libère pas à elle seule le véhicule.'),
      p('Le support caméra sera traité après cette préparation de prototype, selon l’ordre demandé. Aucune géométrie définitive de châssis ni visserie finale créée dans cette passe.','small')]
    for f in story:
        if isinstance(f,Table):f.spaceAfter=3*mm
    doc=SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=18*mm,bottomMargin=23*mm,title='Drone V3 - M1P fabrication prototype et essais',author='Projet Drone V3')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    d=pymupdf.open(OUT);renders=[]
    for i,page in enumerate(d):
        path=TMP/f'page-{i+1}.png';page.get_pixmap(matrix=pymupdf.Matrix(1.35,1.35),alpha=False).save(path);renders.append(str(path.relative_to(ROOT)))
    OUT.with_suffix('.json').write_text(json.dumps(dict(pages=len(d),renders=renders,visual_review_completed=False,hardware_tested=False,sha256=hashlib.sha256(OUT.read_bytes()).hexdigest()),indent=2),encoding='utf-8')
    assert len(d)==6,len(d)
    print('Qualification annex pages',len(d),flush=True)

if __name__=='__main__':main()
