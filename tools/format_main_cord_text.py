"""Polish human prose only; preserve URL, code, filenames and source evidence."""
from pathlib import Path
import re,sys
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/cordon-principal-batterie'
def human(s):
 fixes={'faisceau3':'faisceau 3','Environ24':'Environ 24','TE2025':'TE 2025','GuideTE':'Guide TE','notamment0':'notamment 0','CAOnative':'CAO native',
 'cuivreρ':'cuivre ρ','sectionnominale':'section nominale','deuxfilsde0,10m':'deux fils de 0,10 m','Rboucle':'R boucle','du510':'du 510','le510':'le 510','à20°C':'à 20 °C','TVAFrance':'TVA France','indicatif61':'indicatif : 61',
 'branchesESC':'branches ESC','packIC5':'pack IC5','21octobre2020':'21 octobre 2020','ForumutilisateursARRMA2020':'Forum utilisateurs ARRMA 2020','CitationHorizon':'Citation Horizon','activeIC5':'active IC5',
 'troisIC5actifs':'trois IC5 actifs','huitfichiersinitiauxXT60':'huit fichiers initiaux XT60','RéimportCadQuery':'Réimport CadQuery','ImportFreeCAD':'Import FreeCAD','sansinterface':'sans interface',
 'solidesfermés':'solides fermés','Pasd’essai':'Pas d’essai','interfaceFreeCAD':'interface FreeCAD','ouCADView':'ou CAD View','àsection':'à section','milliersde':'milliers de','sondesradiales':'sondes radiales',
 'JeuxCAO':'Jeux CAO','auxraccordscontact':'aux raccords contact','Aucunfilcoupé':'Aucun fil coupé','danslesmodèlesinstallés':'dans les modèles installés','sertissageW':'sertissage W',
 'échantillons12':'échantillons 12','à680':'à 680','desréférencesdel’étudeinitiale':'des références de l’étude initiale','fils10':'fils 10','Cossesnues':'Cosses nues','etATUMfourni':'et ATUM fourni','AncienpackZeee':'Ancien pack Zeee',
 'sesSTEP':'ses STEP','conservéscomme':'conservés comme','référencesdatées':'références datées','renommésSpektrum':'renommés Spektrum','batterieG1':'batterie G1','CordonIC5':'Cordon IC5',
 'anciennepage':'ancienne page','générationG1etstatutarrêté':'génération G1 et statut arrêté','cordon510':'cordon 510','4pouces':'4 pouces','photoofficielle':'photo officielle','FAQG1/G2':'FAQ G1/G2',
 'originalPDFarchivé':'original PDF archivé','applicationFirma100A/IC5':'application Firma 100 A /IC5','SKUexact':'SKU exact','stocketprix':'stock et prix','produit130191etoutilsassociés':'produit 130191 et outils associés',
 'TEviaLCSC':'TE via LCSC','fichefabricant4':'fiche fabricant 4','originalarchivé':'original archivé','guideSOLISTRAND':'guide SOLISTRAND','consultéenligne':'consulté en ligne','TEviaFarnell':'TE via Farnell',
 'notice408':'notice 408','1542RevP':'1542 Rev P','gaineATUM':'gaine ATUM','documentationpartagée':'documentation partagée','retoursutilisateurs510du':'retours utilisateurs 510 du',
 'PDFsources':'PDF sources','FAQHorizon':'FAQ Horizon','guideFirma':'guide Firma','ficheTE':'fiche TE','deuxrévisionsTE':'deux révisions TE','catalogueAMASS':'catalogue AMASS','ficheXT60HV1.2':'fiche XT60H V1.2',
 'desURL':'des URL','voisinsdesSTEP':'voisins des STEP','référencesXT60ne':'références XT60 ne','justifientpaslecordonIC5':'justifient pas le cordon IC5','desprotections':'des protections','carte desurveillance':'carte de surveillance',
 'objectifs40km/h':'objectifs 40 km/h','à40km/h':'à 40 km/h','à20km/h':'à 20 km/h','et45':'et 45','ModèlesSTEP':'Modèles STEP','contrôléssur':'contrôlés sur'}
 fixes.update({'BatterieG1':'Batterie G1','CossesTE':'Cosses TE','sectionnominale':'section nominale','page et139':'page et 139','TE408':'TE 408'})
 for a,b in fixes.items():s=s.replace(a,b)
 replacements={'du15octobre2026':'du 15 octobre 2026','15octobre2026':'15 octobre 2026','TE130191':'TE 130191','BNTECHGO12AWG':'BNTECHGO 12 AWG','SOLISTRAND130191':'SOLISTRAND 130191','AMASS2026':'AMASS 2026','ATUM8/2':'ATUM 8/2','MIDI60A':'MIDI 60 A','Pack2S':'Pack 2S','pack2S':'pack 2S','Zeee2S':'Zeee 2S','AmazonUS':'Amazon US','de0,':'de 0,','à0,':'à 0,','du7mars2025':'du 7 mars 2025','7mars2025':'7 mars 2025','juin2020':'juin 2020','guideSOLISTRAND':'guide SOLISTRAND','guideTE':'guide TE','planA3':'plan A3','PlanTEA3':'Plan TE A3','STEPnatifs':'STEP natifs','Prix HT':'Prix HT','TypeW':'Type W','guideSOLISTRAND':'guide SOLISTRAND','d’outil':'d’outil','pièce.':'pièce.','V1.2historique':'V1.2 historique','MIDIentrée':'MIDI entrée','D-N2':'D- N2','aprèsMIDI':'après MIDI','versD-':'vers D-','surXT60':'sur XT60','étudeXT60':'étude XT60','scénario44':'scénario 44','MiniBusD-':'MiniBus D-','MiniBus2315':'MiniBus 2315','cordonCP0':'cordon CP0','principalCP0':'principal CP0','ensembleV3':'ensemble V3','versionXT60':'version XT60','priseMIDI':'prise MIDI','Lot10':'Lot 10','lot10':'lot 10','du10mars2011':'du 10 mars 2011','RevN':'Rev N','viaTME':'via TME','viaLCSC':'via LCSC','viaFarnell':'via Farnell','catalogue2026':'catalogue 2026','fiche2025':'fiche 2025','solidescolorés':'solides colorés','modèlesSTEP':'modèles STEP','ModèlesSTEP':'Modèles STEP','CatalogueSTEP':'Catalogue STEP','ValidationFreeCAD':'Validation FreeCAD','jeuCAO':'jeu CAO','longueursCAO':'longueurs CAO','CP0_moins':'CP0_moins'}
 for a,b in replacements.items():s=s.replace(a,b)
 s=re.sub(r'(\d)(mm²|mm|cm|ft|AWG|brins|solides|pages|pièces|paires|coupes|pouces|g\b|EUR|USD|mV|mΩ|W\b|A\b|N·m|in-lb|contacts|min\b|minutes)',r'\1 \2',s)
 s=re.sub(r'\b(à|du|et|de|par|pour|sur|en|le|la|nominale|largeur|MIDI|Cordon|Batterie|TE|coupe|coupes|environ|L|W|ID)(?=\d)',r'\1 ',s,flags=re.I)
 s=re.sub(r',(?=[A-Za-zÀ-ÿ])',', ',s)
 s=re.sub(r'(?<=[A-Za-zÀ-ÿ]),(?=\d)',', ',s)
 s=re.sub(r'\b(fil|fils|gaine|cosses|cosse|lot|barre|paume|canon|longueur|épaisseur|œil|outil|matrice|page|paroi|diamètre|retrait|courant|version|rubrique|surface)(?=\d)',r'\1 ',s,flags=re.I)
 s=re.sub(r'(\d)(?=continus?\b)',r'\1 ',s)
 s=re.sub(r'(?<=\d)\s*×\s*(?=\d)',' × ',s)
 return s
def markdown(s):
 # Protect link targets, literal code, URLs and file basenames.
 parts=re.split(r'(```[\s\S]*?```|`[^`]+`|https?://[^\s<>\)]+|\]\([^\)]+\))',s)
 return ''.join(p if p.startswith(('```','`','http','](')) else human(p) for p in parts)
def main():
 sys.stdout.reconfigure(encoding='utf-8')
 for path in BASE.rglob('*.md'):path.write_text(markdown(path.read_text(encoding='utf-8')),encoding='utf-8')
 for rel in ['README.md','SPECIFICATIONS.md','Composants/README.md','Composants/ENSEMBLES-AVANT-CHASSIS.md','Composants/faisceau-puissance/integration.md','Composants/batterie/integration.md','Composants/protection-surintensite/integration.md','Composants/distribution-alimentation/integration.md','Composants/cable-puissance-12awg/README.md','Composants/connecteurs-alimentation/README.md']:
  path=ROOT/rel
  if path.exists():
   s=path.read_text(encoding='utf-8');a=s.find('<!-- cordon-principal-batterie-v3 -->');b=s.find('<!-- /cordon-principal-batterie-v3 -->',a)
   if a>=0 and b>=a:path.write_text(s[:a]+markdown(s[a:b])+s[b:],encoding='utf-8')
 print('French prose formatted; URLs and earlier dossier contents preserved')
if __name__=='__main__':main()
