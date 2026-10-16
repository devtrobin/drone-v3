"""Integrate current wiring handoff and deferred work without editing old PDFs."""
from pathlib import Path
import json,sys,re
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants'
from build_final_components_data import TITLES
def block(path,key,txt):
 s=path.read_text(encoding='utf-8');opening=f'<!-- {key} -->';closing=f'<!-- /{key} -->';new=opening+'\n\n'+txt.strip()+'\n\n'+closing
 if opening in s:s=re.sub(re.escape(opening)+r'.*?'+re.escape(closing),lambda _:new,s,flags=re.S)
 else:s=s.rstrip()+'\n\n'+new+'\n'
 path.write_text(s,encoding='utf-8')
def main():
 sys.stdout.reconfigure(encoding='utf-8')
 text='''Les compléments avant châssis sont regroupés dans quatre ensembles, avec un dossier par référence, notices PDF, originaux constructeur, cotes, devis, sources et STEP colorés :

- [Connecteurs et faisceau de commande](Composants/connecteurs-commande/README.md) : trois prises JR, huit contacts utilisés et séparation des PWM ; un seul BEC pour le servo.
- [Liaisons d’alimentation et de mesure](Composants/liaisons-alimentation-surveillance/README.md) : bornes WAGO, fil 18 AWG, interface XH trois positions et rallonge d’équilibrage 2S.
- [Maintien de batterie](Composants/maintien-batterie/README.md) : deux sangles GEPRC et un patin silicone provisoire, hors conception de châssis.
- [Coupure manuelle](Composants/coupure-manuelle/README.md) : Albright ED80-1 après MIDI et avant D+, avec deux cosses M6 ; coupe moteurs et Pi indépendamment du logiciel.

Décision utilisateur : **schéma et routage de surveillance, support caméra, visserie restante et châssis seront conçus ensemble à la fin**. Les anciens PDF de faisceau sont des instantanés ; la coupure ED80 remplace désormais la liaison directe MIDI vers D+. L’interface XT60 de la batterie et les performances restent à qualifier, aucune commande effectuée.'''
 block(ROOT/'ReadMe.md','complements-avant-chassis-v3',text)
 block(BASE/'README.md','complements-avant-chassis-v3',text.replace('](Composants/',']('))
 block(ROOT/'SPECIFICATIONS.md','phase-finale-v3','''Le schéma électrique et le routage de la carte de surveillance, le support caméra, la visserie restante et le châssis sont reportés ensemble à la dernière phase, conformément à la demande utilisateur.

Les [quatre ensembles de compléments](Composants/README.md) sont documentés. Coupure manuelle proposée : **batterie → MIDI → ED80 → D+**. C’est une ouverture du positif commun, indépendante du Pi ; elle n’assure ni freinage instantané, ni isolation des fils d’équilibrage, ni arrêt télécommandé de sécurité. Qualification de l’interface batterie XT60 et des courants toujours ouverte.''')
 for folder in ['faisceau-puissance','distribution-alimentation','protection-surintensite','protection-batterie']:
  target=BASE/folder/'integration.md'
  if not target.exists():target=BASE/folder/'README.md'
  block(target,'complements-avant-chassis-v3','''Mise à jour du 14 octobre 2026 : [coupure ED80 et deux cosses M6](../coupure-manuelle/integration.md) sur le positif commun **après MIDI, avant D+**. Le segment direct CP1+ est remplacé par CP1A+ MIDI→ED80 et CP1B+ ED80→D+. Les deux cosses 95R5 sont réutilisées ; deux 95R6 sont ajoutées. Les anciens PDF/STEP de faisceau ne comprennent pas ce changement et restent des références datées.

[Liaisons alimentation/mesure](../liaisons-alimentation-surveillance/integration.md) et [commandes servo/ESC](../connecteurs-commande/integration.md) détaillent les extrémités aval. L’interface batterie XT60 reste à qualifier ; schéma/routage de surveillance, support caméra, visserie restante et châssis réservés pour la phase finale.''')
 block(BASE/'connecteur-gpio/integration.md','terminaisons-commande-v3','''Les [trois prises JR et bornes de commande](../connecteurs-commande/integration.md) complètent les extrémités ouvertes du faisceau : broches 32/33/12 pour les trois PWM distincts ; GND 34/39 pour les ESC. Une seule sortie BEC 6 V rejoint le servo, aucune sortie BEC vers le Pi. La prise droite est à deux contacts, cavité centrale vide.

Les broches 2/4 et GND 6/9/14/20 rejoignent les [bornes 5 V et GND](../liaisons-alimentation-surveillance/integration.md) depuis le régulateur. Les fichiers 3D précédents restent des vues datées à fils ouverts ; leur numérotation ne change pas. WARN/DONE et leur protection finale seront arrêtés avec le schéma de surveillance différé.''')
 # Light editorial correction of generated French labels; never touches URLs,
 # standard references or original downloaded documents.
 fixes={'du14octobre2026':'du 14 octobre 2026','du14/10':'du 14/10','du14octobre':'du 14 octobre','du14/10':'du 14/10',
 '14octobre2026':'14 octobre 2026','enmm':'en mm','saufmention':'sauf mention','lot5':'lot de 5','lot2':'lot de 2',
 'supportcaméra':'support caméra','visserie restante et la surveillance définitive':'visserie restante et la surveillance définitive',
 'montagechâssis':'montage du châssis','cartesurveillance':'carte de surveillance','lacartesurveillance':'la carte de surveillance',
 'supportcaméra':'support caméra','le schéma et leroutage de lacartesurveillance':'le schéma et le routage de la carte de surveillance',
 'du composant / ensemble':'du composant ou de l’ensemble','dossiernotices':'dossier notices','noticefabricant':'notice fabricant',
 'noticesfabricant':'notices fabricant','pas de fausse noticefabricant':'pas de fausse notice fabricant','PDFpublié':'PDF publié',
 'nonmodifiées':'non modifiées','desrendus':'des rendus','decesensembles':'de ces ensembles','prixnonconfirmés':'prix non confirmés',
 'prix2pièces':'prix de deux pièces','àrevalideràcommande':'à revalider à la commande','duHTMLdirect':'du HTML direct',
 'de l’indexweb ancien':'de l’index web ancien','devis enUSD':'devis en USD','taxes/import/port nonconfirmés':'taxes/import/port non confirmés',
 'àl’unité':'à l’unité','fil déjàbudgétés':'fil déjà budgétés','déjàbudgétés':'déjà budgétés','deuxcosses':'deux cosses',
 'déjàprésentes':'déjà présentes','d’undevis':'d’un devis','surveillance seront faits ensemble à lafin':'surveillance seront faits ensemble à la fin',
 'fibres etcrochetsmicroscopiques':'fibres et crochets microscopiques','contactsfemelles':'contacts femelles',
 'Catalogueetvalidation del’ensemble':'Catalogue et validation de l’ensemble','unaperçuPNG':'un aperçu PNG','unJSON decotes/provenance':'un JSON de cotes/provenance',
 'documentprojet':'document de projet','version etempreintes':'version et empreintes','avec leurs versions et empreintes':'avec leurs versions et empreintes',
 'réutilisés dansl’étude':'réutilisés dans l’étude','secondachat':'second achat','deuxfeuilles':'deux feuilles',
 '4,55€':'4,55 €','9,75€':'9,75 €','83,88€TTC':'83,88 € TTC','11,99€TTC':'11,99 € TTC',
 'hauteurhaut':'hauteur supérieure','lot àmesurer':'lot à mesurer'}
 for folder in TITLES:
  for p in (BASE/folder).rglob('*.md'):
   s=p.read_text(encoding='utf-8')
   for a,b in fixes.items():s=s.replace(a,b)
   p.write_text(s,encoding='utf-8')
 # Current human index and a partial quote, expressly not the entire vehicle.
 (BASE/'ENSEMBLES-AVANT-CHASSIS.md').write_text('''# Ensembles complémentaires avant châssis

14 octobre 2026. Dix dossiers de références au sein de quatre ensembles ; notice PDF, originaux disponibles, cotes, recherche d’achat, devis, avis et STEP par ensemble. Aucun achat ni essai matériel effectué.

| Ensemble | Dossier | Notice | Modèles |
| --- | --- | --- | --- |
| Commande servo / ESC | [Dossier](connecteurs-commande/README.md) | [PDF](connecteurs-commande/notices/notice-connecteurs-commande-v3.pdf) | [STEP](connecteurs-commande/3D/README.md) |
| Alimentation et mesure 2S | [Dossier](liaisons-alimentation-surveillance/README.md) | [PDF](liaisons-alimentation-surveillance/notices/notice-liaisons-alimentation-surveillance-v3.pdf) | [STEP](liaisons-alimentation-surveillance/3D/README.md) |
| Maintien batterie | [Dossier](maintien-batterie/README.md) | [PDF](maintien-batterie/notices/notice-maintien-batterie-v3.pdf) | [STEP](maintien-batterie/3D/README.md) |
| Coupure manuelle | [Dossier](coupure-manuelle/README.md) | [PDF](coupure-manuelle/notices/notice-coupure-manuelle-v3.pdf) | [STEP](coupure-manuelle/3D/README.md) |

## Achat et chiffrage partiel

Prix relevés sur les pages publiques indiquées dans chaque dossier, pour les quantités entières. Marchandises connues : 10,50 EUR pour commande (JR et une 413), 4,10 EUR pour liaisons (deux 413, une 415 et la rallonge), 11,99 EUR pour les deux feuilles silicone, 83,88 EUR pour ED80. **Sous-total EUR partiel : 110,47 EUR TTC, hors livraison**, hors embase XH et deux cosses 95R6 dont les prix restent ouverts. Ajouter les deux lots fabricant en devis USD : BNTECHGO 9,48 USD et GEPRC 5,99 USD, soit 15,47 USD avant taxes, import et livraison France non confirmés. Aucune conversion ni total global V3 validé.

L’offre Amazon.fr du silicone est identifiée par ASIN B08KFTBDF2. Pour les autres références, une recherche Amazon n’établit pas une offre exacte ; des liens fabricant ou distributeur sont proposés avec leur état de vérification. Les prix doivent être revalidés à la commande.

## Phase finale réservée

Schéma électrique et routage de la carte de surveillance, support caméra, visserie restante et châssis seront conçus ensemble à la fin. Aucun de ces éléments n’est dessiné dans les nouveaux fichiers.

Les poses de câbles, de sangles et de cosses sont provisoires. La coupure ED80 est ajoutée après MIDI, avant D+ ; les anciens documents de faisceau restent des instantanés sans ce dispositif. Les notices d’intégration actuelles renvoient à cette mise à jour.

L’interface XT60 du pack reste à qualifier pour les courants de l’étude. Coupure électrique ne signifie pas freinage instantané ; les fils d’équilibrage restent sous tension. Les objectifs de vitesse, autonomie et vidéo n’ont pas été validés par des essais.
''',encoding='utf-8')
 for folder in TITLES:
  p=BASE/folder/'README.md';s=p.read_text(encoding='utf-8')
  s=s.replace('le schéma et leroutage de lacarte de surveillance','le schéma et le routage de la carte de surveillance')
  s=s.replace('mesure2S','mesure 2S').replace('2 pièce |','2 pièces |')
  p.write_text(s,encoding='utf-8')
 print('INTEGRATION updated, original PDFs unchanged')
if __name__=='__main__':main()
