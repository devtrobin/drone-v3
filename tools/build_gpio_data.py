"""Document the GPIO connector selection, wiring, drawings and purchase limits."""
from pathlib import Path
import json,sys,math,re
from build_gpio_step import PINS
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/connecteur-gpio';OUT=BASE/'3D'
MOLEX='https://www.molex.com/en-us/products/part-detail/0022552401'
CONTACT='https://www.molex.com/en-us/products/part-detail/0016020103'
WIRE='https://www.adafruit.com/product/3175'
GPIO='https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#gpio-and-the-40-pin-header'
FAMILY='https://www.molex.com/en-us/products/connectors/wire-to-wire-connectors/sl-connectors'
def dump(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s.strip()+'\n',encoding='utf-8')
def main():
 sys.stdout.reconfigure(encoding='utf-8');cat=json.loads((OUT/'catalogue.json').read_text(encoding='utf-8'))
 functions={1:('3,3 V Pi','Alimentation des remontées WARN du circuit de surveillance'),2:('5 V régulés A','Entrée depuis VOUT du D24V90F5'),
 4:('5 V régulés B','Deuxième entrée depuis le même VOUT ; pas une seconde source'),6:('GND alimentation A','Retour régulateur, chemin de puissance électronique'),
 9:('GND alimentation B','Retour régulateur'),11:('GPIO17 / WARN1','Collecteur optocoupleur cellule 1, remontée 47 kΩ à 3,3 V Pi'),
 12:('GPIO18 / PWM servo','Signal de position FT90M ; puissance fournie par BEC1 à 6 V'),13:('GPIO27 / WARN2','Collecteur optocoupleur cellule 2, remontée 47 kΩ à 3,3 V Pi'),
 14:('GND alimentation C','Retour régulateur'),15:('GPIO22 / DONE','Vers la diode de la logique OFF du circuit de surveillance'),20:('GND alimentation D','Retour régulateur'),
 32:('GPIO12 / PWM ESC gauche','Entrée accélérateur du variateur gauche ; seuil 3,3 V à vérifier'),33:('GPIO13 / PWM ESC droit','Entrée accélérateur du variateur droit ; seuil 3,3 V à vérifier'),
 34:('GND signal ESC gauche','Référence de commande ; aucun courant de propulsion prévu'),39:('GND signal ESC droit','Référence de commande ; aucun courant de propulsion prévu')}
 colors={'red':'rouge','black':'noir','white':'blanc, repéré','green':'vert','yellow':'jaune, repéré','blue':'bleu'}
 pins=[dict(physical_pin=p,signal=n,color=colors[c],AWG=22,function=functions[p][0],destination=functions[p][1]) for p,n,c in PINS]
 dump(BASE/'brochage.json',dict(view='Numéros physiques du Pi, vue de dessus. Vue face d’accouplement du câble : miroir à contrôler.',pins=pins,
  unused_pins=[p for p in range(1,41) if p not in [r['physical_pin'] for r in pins]],hardware_wired=False,
  ESC_3V3_input_validated=False,servo_BEC6V_not_connected_to_GPIO=True,OFF_raw_not_directly_connected_to_GPIO=True))
 parts=[dict(reference='Molex 22-55-2401 / 0022552401',quantity=1,type='boîtier nu, 40 positions femelles, 2 rangées',manufacturer=MOLEX,
  purchase='https://www.digikey.fr/fr/products/detail/molex/0022552401/171975',amazon='https://www.amazon.fr/s?k=Molex+22-55-2401',price_EUR_TTC=None,
  observed_USD_unit_price=2.95,price_source='https://www.newark.com/molex/22-55-2401/connector-rcpt-40pos-2row-2-54mm/dp/77C6142'),
 dict(reference='Molex 16-02-0103 / 0016020103',quantity=20,installed=15,spares=5,type='contacts femelles dorés en vrac, pas de bobine à acheter',manufacturer=CONTACT,
  purchase='https://www.digikey.fr/fr/products/detail/molex/0016020103/115063',amazon='https://www.amazon.fr/s?k=Molex+16-02-0103',price_EUR_TTC=None,
  observed_USD_unit_price=0.25,price_source='https://www.digikey.com/en/products/detail/molex/0638118700/1832243'),
 dict(reference='Adafruit 3175',quantity=1,type='lot de fil multibrin 22 AWG, diamètre isolant annoncé 1,5 mm',manufacturer=WIRE,purchase=WIRE,
  amazon='https://www.amazon.fr/s?k=Adafruit+3175',price_EUR_TTC=None,observed_USD_unit_price=29.95,
  package_content_discrepancy='Titre 10 bobines de 25 ft, prose 6 bobines : contenu à confirmer avant achat.',price_source=WIRE)]
 dump(BASE/'nomenclature.json',dict(selected_on='2026-10-14',parts=parts,connector_populated_contacts=15,connector_total_positions=40,
  french_total_EUR_TTC=None,provisional_sum_USD_at_unit1_prices=37.90,tooling_shipping_taxes_excluded=True,
  purchased=False,wire_cut_list_final=False,RC_end_connectors_not_included=True))
 rho=.01724;A=.326;L=.15;I=5;Rwire=rho/A*L*(1/2+1/4)
 rows=[]
 for Rc in [.010,.020]:
  R=Rwire+Rc*(1/2+1/4);rows.append(dict(contact_resistance_assumed_ohm=Rc,loop_resistance_ohm=R,drop_V=I*R,loss_W=I*I*R))
 dump(BASE/'calculs.json',dict(example_only=True,copper_rho_ohm_mm2_m=rho,area_AWG22_mm2=A,one_way_length_assumed_m=L,
  Pi_current_study_A=I,positive_parallel_paths=2,negative_parallel_paths=4,wire_loop_R_ohm=Rwire,
  positive_current_equal_share_A=I/2,negative_current_equal_share_A=I/4,rows=rows,
  equal_share_guaranteed=False,current_and_temperature_measured=False,wire_supplier_ampacity_published=False,
  insulation_OD_announced_mm=1.5,contact_insulation_OD_max_mm=1.63,nominal_OD_margin_mm=.13,
  GPIO_body_ymin_in_Pi_study_mm=52.5-5.0546/2,cooler_body_ymax_study_mm=6.75+42.5,
  planar_gap_study_mm=52.5-5.0546/2-49.25,cooler_mount_delta_y_read_from_Pi_plan_mm=37.5,
  existing_cooler_model_delta_y_mm=37,installed_fit_verified=False))
 dump(BASE/'sources.json',dict(checked_on='2026-10-14',manufacturer_housing=MOLEX,manufacturer_contact=CONTACT,wire_reference=WIRE,
  product_family_current_up_to_A=3,family_source=FAMILY,Pi_header_current_certified=False,Pi5_current5A_validated=False,
  housing_drawing_mm=dict(pitch=2.54,rows=2,positions=40,A_centres=48.26,B_length_reference=50.77,width_reference=5.05,height_reference=15.24),
  contact=dict(AWG=[22,24],insulation_OD_max_mm=1.63,mating_plating='or sélectif',termination_plating='étain',material='bronze phosphoreux'),
  crimp_reference=dict(document='ATS-638118700',revision='E, 2017-11-09, actuellement publiée',strip_length_mm=[2.54,3.17],insulation_profile_range_mm=[1.30,1.65],
   conductor_height_AWG22_mm=[.75,.85],conductor_width_reference_mm=1.43,insulation_height_reference_mm=1.70,
   insulation_width_reference_mm=1.76,pull_min_AWG22_N=39.2,pull_min_AWG24_N=29.4,
   manufacturer_tool_reference='63811-8700',tool_in_budget=False),
  amazon_exact_offer_verified=False,ASIN=None,price_EUR_TTC=None,assets='assets.json',models='3D/catalogue.json',hardware_tested=False))
 write(BASE/'README.md',f'''# Connecteur GPIO et faisceau du Raspberry Pi 5

**Sélection d’étude du 14 octobre 2026 : Molex 22-55-2401, avec 15 contacts 16-02-0103, cinq contacts de réserve et fil multibrin Adafruit 3175 de 22 AWG.** Boîtier femelle à 40 positions, 2 × 20 au pas de 2,54 mm. Les contacts sont vendus séparément. Aucun achat, câblage ni essai physique réalisé.

Cette liaison reprend les deux commandes ESC, la direction, WARN1/WARN2 et DONE. Elle prévoit aussi les arrivées 5 V régulées et les retours de la branche Pi selon l’architecture existante. Les broches physiques ne sont pas les numéros GPIO BCM.

## Dossier

- [Notice PDF de montage](notices/notice-connecteur-gpio-v3.pdf) et [documents fabricant originaux](notices/README.md).
- [Cotes et statut des dimensions](cotes.md), [intégration et brochage](integration.md), [brochage structuré](brochage.json).
- [Recherche et informations manquantes](recherche-technique.md), [devis et liens d’achat](devis.md), [nomenclature](nomenclature.json).
- [STEP, aperçus et provenance](3D/README.md), [photos et crédits](photos/README.md).
- [Sources](sources.json), [archives et empreintes](assets.json), [calculs](calculs.json), [contrôles](validation-dossier.json).

## Achat

Les liens Amazon sont des recherches par référence : aucun ASIN, prix TTC français ou stock exact confirmé. Les fiches distributeur identifiées sont conservées dans le devis ; les prix consultés aux États-Unis ne constituent pas un panier livré en France. Le coût de l’outillage de sertissage reste distinct et non chiffré.

## Géométrie et raccordement

Le boîtier utilise une **CAO originale Molex**, archivée intacte. Les variantes de lecture tournent cette géométrie et lui donnent le noir de résine indiqué dans la fiche. Les contacts et la pose des fils sont reconstruits et signalés comme estimés. Les fils se terminent volontairement sans connecteurs aval dans le modèle d’implantation ; ce sont des extrémités de pose, pas des câbles prêts à brancher.

Les GPIO sont en 3,3 V. Le BEC 6 V du premier ESC alimente le servo selon le dossier direction ; il ne rejoint ni GPIO, ni les rails 5 V du Pi. Le positif BEC du second ESC reste isolé. Le seuil logique des ESC et l’alimentation Pi à 5 A restent à qualifier.

[Raspberry Pi retenu](../raspberry-pi-5/README.md), [refroidisseur](../refroidissement-raspberry-pi-5/README.md), [surveillance 2S](../protection-batterie/integration.md).
''')
 write(BASE/'devis.md',f'''# Devis indicatif et liens d’achat - GPIO

Relevé documentaire du **14 octobre 2026**, aucune commande.

| Référence | Quantité projet | Lien direct identifié | Relevé étranger |
| --- | ---: | --- | ---: |
| Molex 22-55-2401 | 1 boîtier | [DigiKey France](https://www.digikey.fr/fr/products/detail/molex/0022552401/171975) | [Newark US](https://www.newark.com/molex/22-55-2401/connector-rcpt-40pos-2row-2-54mm/dp/77C6142) : 2,95 USD à l’unité |
| Molex 16-02-0103, vrac | 20, dont 15 installés | [DigiKey France](https://www.digikey.fr/fr/products/detail/molex/0016020103/115063) | [DigiKey US, produit associé](https://www.digikey.com/en/products/detail/molex/0638118700/1832243) : 0,25 USD à l’unité |
| Adafruit 3175, fil multibrin 22 AWG | 1 lot | [Fabricant et vente]({WIRE}) | 29,95 USD le lot |

**Somme indicative : 37,90 USD**, en multipliant les prix unitaires consultés, hors taxes éventuelles, transport, remises de quantité et outillage. Ce n’est pas un devis TTC français ni un panier unique. Aucun total en euros inventé. Le métrage installé sera bien inférieur au contenu du lot ; il reste à arrêter après implantation.

Le titre Adafruit indique **10 bobines de 25 ft**, alors qu’un paragraphe indique six : confirmer le contenu du lot. Le diamètre isolant publié est 1,5 mm ; contrôler le lot réel avant sertissage. Ne pas substituer le kit de fil monobrin ni un silicone Ø1,7 mm en conservant la même qualification.

Recherches Amazon : [boîtier](https://www.amazon.fr/s?k=Molex+22-55-2401), [contacts](https://www.amazon.fr/s?k=Molex+16-02-0103), [fil](https://www.amazon.fr/s?k=Adafruit+3175). Les téléchargements de recherche ont rendu une réponse vide ; aucune offre exacte vérifiée. Les fiches France ont été identifiées mais leur prix et leur stock n’ont pas pu être confirmés. Les liens restent utiles pour retrouver la référence avant achat.

La pince 63811-8700 est la référence de procédure du constructeur. Aucun achat de cette pince coûteuse n’est décidé : utiliser un sertissage conforme à la notice ou faire préparer le faisceau, puis contrôler les résultats. Le devis final doit inclure cette opération et les terminaisons aval RC/logiques, encore à arrêter.
''')
 write(BASE/'cotes.md','''# Cotes du connecteur GPIO

| Élément | Valeur | Statut |
| --- | --- | --- |
| Boîtier | 40 positions, 2 rangées de 20 | Référence 22-55-2401 |
| Pas de colonnes et rangées | 2,54 mm | Plan et CAO fabricant |
| A, entraxe extrêmes | 48,26 mm | Tableau pour 40 circuits |
| B, longueur | 50,77 mm de référence | Plan SD-70450-0001-0026, ancienne révision archivée |
| Largeur / hauteur | 5,05 / 15,24 mm de référence | Plan ; pas des tolérances du lot reçu |
| Enveloppe du solide natif | 50,7746 × 5,0546 × 15,24 mm | Mesure de la CAO, pas du matériel |
| Broche mâle admise | 0,64 mm carrée ou ronde | Plan du boîtier |
| Contact | 22 ou 24 AWG ; isolant Ø1,63 mm max | Fiche 16-02-0103 et page fabricant actuelle |
| Fil retenu | 22 AWG multibrin ; isolant Ø1,5 mm annoncé | Adafruit 3175 ; tolérance non publiée |
| Réserve nominale d’isolant | 0,13 mm | Différence arithmétique, pas une marge garantie |
| Dénudage | 2,54 à 3,17 mm | Notice ATS-638118700 révision E |
| Isolant pour le profil 22–24 AWG | 1,30 à 1,65 mm ; contact choisi limité à 1,63 | Révision E consultée sur Molex |
| Sertissage conducteur 22 AWG | Hauteur 0,75–0,85 ; largeur réf. 1,43 mm | Valeurs de procédure, avec l’outillage prescrit |
| Sertissage isolant | Hauteur réf. 1,70 ; largeur réf. 1,76 mm | Référence de procédure, pas dimensions détaillées du STEP reconstruit |

La CAO native décrit le boîtier et quelques annotations sans volume. Les variantes colorées conservent le solide exact, mais omettent les annotations non solides ; l’original reste archivé. Les tôleries et ressorts du contact ne proviennent pas d’une CAO native. Le modèle suit la photo d’un contact serti ; dimensions locales, détails du ressort et crimp sont estimés. Le dessin générique de la notice d’outillage n’est pas un plan de fabrication du contact.

Une petite réservation estimée de 0,014 mm³ est ajoutée au col du contact reconstruit pour dégager une nervure du boîtier natif. Le boîtier fournisseur n’est pas retouché. Ce détail de reconstruction permet un assemblage CAO sans chevauchement, mais ne certifie pas la forme du contact réel.

Les fils de pose ont une gaine de 1,5 mm et une âme équivalente de 0,326 mm². Le nombre de brins n’est pas publié, donc aucune subdivision arbitraire n’est présentée comme réelle. Les extrémités ouvertes sont volontaires. Les courbes ne constituent pas la liste de coupe finale.

La pose sur le Pi utilise le repère de sa CAO : centre du header (32,5 ; 52,5), emprise 50,8 × 5,08, face haute plastique Z=3,876. Le boîtier posé à cette cote donne un sommet Z=19,116. La profondeur réelle d’insertion reste à mesurer.

La pose indicative du refroidisseur reprend son premier clip à (3,5 ; 9,5). Le jeu en plan au boîtier GPIO serait environ **0,72 mm** dans ce repère. La lecture du plan Pi donne 37,5 mm entre les clips en Y, tandis que la reconstruction existante utilise 37 mm : cet écart de 0,5 mm et les cotes approximatives empêchent de déclarer l’ajustement acquis. Contrôler le lot et les deux orientations avant fabrication du support. Aucun STEP du Pi ou du refroidisseur modifié.

[Archives originales](notices/README.md), [provenance](3D/provenance.json), [calculs](calculs.json).
''')
 rows=['| Broche physique Pi | Fonction | Couleur | Destination |','| ---: | --- | --- | --- |']
 rows += [f"| {r['physical_pin']} | {r['function']} | {r['color']} | {r['destination']} |" for r in pins]
 write(BASE/'integration.md','''# Montage et raccordement du GPIO V3

Le plan utilise les **numéros physiques du Pi**, vu de dessus. Le logement femelle vu depuis sa face d’accouplement se lit en miroir. Aligner le repère de broche 1 du fabricant sur la broche 1 du Pi, puis vérifier au multimètre ; ne pas se fier uniquement à la couleur ni à une photographie. Ce boîtier est non polarisé et peut être décalé ou retourné sur une embase nue.

## Affectation proposée

'''+ '\n'.join(rows)+'''

Les 25 autres cavités restent sans contact. Les fils WARN blancs et PWM jaunes portent des repères distincts aux deux extrémités. Le point milieu B1 du pack et l’entrée OFF brute du Pololu ne rejoignent aucune cavité GPIO. DONE arrive à la logique avec la diode prévue dans le dossier surveillance ; ce n’est pas un branchement GPIO vers le relais de puissance.

## Servo et deux ESC

Conserver une masse de référence cohérente avec les retours de puissance séparés. Aucun courant de propulsion ne doit utiliser les fils de commande ou les pistes du Pi. Le signal du FT90M peut utiliser le 3,3 V publié pour cette révision ; confirmer le lot. La compatibilité du seuil logique des WP16BL30 G2 doit être mesurée avant leur raccordement ; ce faisceau passif ne convertit pas les niveaux.

Le premier BEC, réglé à 6 V, alimente uniquement la puissance du servo selon le montage à finaliser. Le second positif BEC est isolé. Le +6 V ne rejoint ni pin 1, ni pins 2/4, ni PWM. Les cordons RC d’origine restent utilisés côté actionneurs ; sens, détrompage et connecteurs aval ne sont pas spécifiés par les fils ouverts du STEP. La voie jaune de programmation Hobbywing reste distincte de l’accélérateur.

## Branche 5 V du Pi

Deux fils rouges alimentent pins 2 et 4 depuis le **même** VOUT du D24V90F5. Quatre fils noirs reviennent au régulateur par pins 6/9/14/20. Les courants d’étude seraient 2,5 A par rouge et 1,25 A par noir à partage égal ; ce partage n’est pas garanti. La famille SL est donnée jusqu’à 3 A sous conditions, ce qui ne certifie pas l’embase du Pi, les sertissages, le faisceau groupé ni une branche complète de 5 A.

Couper l’alimentation si un conducteur parallèle est absent ou défectueux ; ne pas supposer qu’un seul rouge peut porter 5 A. Mesurer courant de chaque chemin, chute de tension à la carte et températures en charge vidéo. Garder les protections externes existantes et qualifier la source avant toute déclaration EEPROM de 5 A. Aucun courant du moteur ou du servo dans ces six fils d’alimentation.

## Préparation du connecteur

1. Débrancher batterie, port d’équilibrage et alimentation du Pi. Établir une liste de coupe après implantation ; garder du mou sans boucle vers les roues, engrenages ou ventilateur.
2. Vérifier référence des contacts en vrac, fil multibrin 22 AWG et diamètre de gaine réel. Réaliser un échantillon de sertissage selon la notice de l’outillage retenu. La procédure Molex indique 2,54–3,17 mm de dénudage ; ne pas étamer les brins avant sertissage.
3. Contrôler la retenue du cuivre, de l’isolant et l’absence de brins libres. Pour l’outillage prescrit, la notice donne 39,2 N minimum à 22 AWG lors de l’essai de traction sans contribution du sertissage isolant. Ces valeurs ne certifient pas une pince générique.
4. Insérer chaque contact depuis l’arrière du boîtier jusqu’à sa retenue, contrôler par traction légère et comparer la table fil par fil. Les cinq contacts de réserve ne sont pas montés sans fonction.
5. Tester la continuité de chaque chemin et l’absence de court-circuit entre rails et signaux. Vérifier spécialement pins 1/2/4, les 25 cavités libres, les BEC et B1. Le débranchement du faisceau se fait par le boîtier, pas en tirant les fils.
6. Poser verticalement sur le header hors tension. Retenir mécaniquement le faisceau sur le châssis ; un collier sur les fils ne verrouille pas automatiquement l’accouplement. Aucune tenue aux vibrations garantie sur l’embase nue.

## Dégagements et réception

Les fils sont dirigés vers l’extérieur du bord GPIO, avec une montée avant courbure pour préserver le refroidisseur. Le jeu de 0,72 mm est une lecture d’étude, pas une tolérance garantie ; voir les cotes. La géométrie des contacts est estimée. Essayer d’abord sans moteurs armés : source, signal neutre, trois PWM puis caméra active. Le connecteur n’ajoute ni watchdog ni arrêt matériel : vérifier toujours perte de commande, gel logiciel et freinage.

[Pi et PWM](../raspberry-pi-5/integration.md), [surveillance et coupure](../protection-batterie/integration.md), [refroidissement](../refroidissement-raspberry-pi-5/integration.md), [régulateur](../regulateur-alimentation/README.md).
''')
 write(BASE/'recherche-technique.md',f'''# Recherche et limites de la sélection GPIO

Les fiches Molex identifient le boîtier 22-55-2401, famille 70450, et le contact 16-02-0103, famille 70058. La référence 16-02-0087 est le conditionnement en bande du contact ; le vrac évite d’acheter une bobine. Plans et CAO fabricant sont disponibles via des miroirs distributeur, alors que plusieurs URL Molex ont expiré ou répondu trop lentement. Chaque résultat de téléchargement figure dans [assets.json](assets.json).

Le plan SD-70450-0001-0026 conservé est ancien : il donne A=48,26 et B=50,77 pour 40 circuits, pas de 2,54, largeur 5,05 et hauteur 15,24. La CAO native corroborant cette enveloppe est conservée dans son ZIP et en STEP intact. Les valeurs récentes de matière et plage de fil du contact ont été consultées sur [Molex]({CONTACT}) ; sa fiche archivée de 2013 indique les mêmes fonctions et Ø1,63 max. Aucun plan coté détaillé du contact téléchargé avec succès.

La [famille SL actuelle]({FAMILY}) annonce jusqu’à 3 A. Cette indication de famille ne permet pas de sommer librement les 40 contacts ni de certifier le header du Pi. La [documentation Pi]({GPIO}) confirme 40 broches, pas de 2,54 et signaux de 3,3 V. Le brochage du projet garde les affectations PWM et surveillance déjà choisies. Un boîtier non polarisé impose un repérage vérifié.

Le [fil Adafruit 3175]({WIRE}) est annoncé multibrin 22 AWG et Ø1,5 mm, contrairement aux silicones plus gros. Son titre parle de dix bobines, sa prose de six : confirmer avant achat. Nombre exact de brins, tolérance de diamètre, résistance linéique et intensité admissible dans notre faisceau non publiés ; les calculs emploient une section AWG équivalente, pas une mesure. Une page ou une vidéo de présentation du fil ne qualifie pas le montage Pi/ESC/servo.

La notice Molex ATS-638118700 actuellement publiée est révision E du 9 novembre 2017. Elle recommande un isolant de 1,30–1,65 mm pour le profil 22–24 AWG, là où l’ancienne révision C archivée indiquait 1,09–1,65. Le contact choisi reste limité à 1,63 mm par sa fiche. Les paramètres de dénudage, profils de référence et traction cités sont identiques dans les deux éditions. Les vues de terminal sont génériques ; elles ne sont pas utilisées comme un plan dimensionnel du 16-02-0103. Les critères d’outillage restent liés au système prescrit. Aucun achat de pince ni fabrication de carte supplémentaire décidé.

Les recherches Amazon ont rendu des réponses vides, les pages DigiKey France ont refusé l’archivage. Le produit exact est identifié chez des distributeurs ; prix TTC et disponibilité France restent non confirmés. Les prix USD du [devis](devis.md) sont des repères étrangers et non un panier français. Aucun avis individuel ni résultat d’essai de cette combinaison dans notre robot trouvé ou inventé. Les images sont identifiées comme illustration constructeur.

Restent à vérifier : révision reçue, sens et insertion sur Pi, maintien aux vibrations, tolérance des fils, sertissage, partage de courant, chute de tension, bruit moteur, seuil logique des ESC et jeux au refroidisseur. Le plan Pi donne une lecture de 37,5 mm en Y entre clips du cooler, contre 37 mm dans la reconstruction antérieure : cet écart est documenté, sans correction arbitraire des anciens STEP.
''')
 assets=json.loads((BASE/'assets.json').read_text(encoding='utf-8'))['assets']
 lines=['# Documents fabricant originaux','','[Notice PDF V3](notice-connecteur-gpio-v3.pdf).','','| Archive | Source |','| --- | --- |']
 for a in assets:
  if a.get('status')=='downloaded' and a['file'].endswith('.pdf'):
   lines.append(f'| [{Path(a["file"]).name}]({Path(a["file"]).name}) | [Source]({a["url"]}) |')
 lines+=['','Le fichier nommé « plan-Farnell » contient une fiche d’identification de 2014 ; le plan réellement coté est l’archive miroir IHS. La notice archivée chez Official Electronic est révision C de 2012. La révision E du 9 novembre 2017, actuellement publiée sur Molex, a été consultée et prévaut pour les paramètres cités ; les statuts de téléchargement indiquent si sa copie locale a pu être conservée. Les originaux sont inchangés.',
  '', '[Notice E actuelle](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/applicationtoolingspecificationpdf/638/63811/ATS-638118700-001.pdf), [intégrité et refus d’accès](../assets.json), [fiche composant](../README.md).']
 write(BASE/'notices/README.md','\n'.join(lines))
 write(BASE/'photos/README.md','''# Photos et crédits

`Molex-contact-original-3.jpeg` est l’illustration d’un contact avec fil de la fiche Molex archivée de 2013, extraite sans retouche. Crédit Molex. Elle reste une image représentative, pas une pièce mesurée. Les autres images extraites sont des logos, pas des photos du composant reçu.

La vue PDF du boîtier est une illustration de CAO constructeur et conserve son cartouche. Les aperçus de reconstruction se trouvent dans le dossier 3D. Aucune photographie d’un montage réel réalisée.
''')
 lines=['# STEP du connecteur GPIO','','Le boîtier reprend la géométrie native Molex. Contacts et fils sont des reconstructions d’étude.','',
 '| Modèle | STEP | Aperçu | Taille |','| --- | --- | --- | --- |']
 for m in cat['models']:lines.append(f'| {m["title"]} | [STEP]({m["file"]}) | [PNG]({m["preview"]["file"]}) | {m["bytes"]/1e6:.2f} Mo |')
 lines += ['', '[STEP original Molex, intact](sources/022552401.stp), [ZIP original](sources/Molex-22-55-2401-CAO-originale.zip), [métadonnées natives](source-native.json).',
 '', 'Le modèle équipé utilise quinze contacts, pas quarante contacts achetés ou montés. Les vingt-cinq cavités libres restent visibles. Les contacts colorés séparent or et étain ; leurs formes ne sont pas certifiées par un plan local.',
 '', 'Les quinze fils continus sont placés pour l’implantation, avec deux étages de courbure pour garder les rangées séparées. Les extrémités sont volontairement ouvertes ; aucune fiche RC aval fictive ajoutée. Ce STEP ne sert pas de liste de coupe.',
 '', '[Provenance](provenance.json), [contrôles FreeCAD](validation-freecad.json), [cotes et jeux](../cotes.md), [notice](../notices/notice-connecteur-gpio-v3.pdf).']
 write(OUT/'README.md','\n'.join(lines))
 p=ROOT/'Composants/README.md';t=p.read_text(encoding='utf-8');row='| [Connecteur GPIO et faisceau](connecteur-gpio/README.md) | Molex 22-55-2401 + contacts 16-02-0103 ; fil Adafruit 3175 | France à vérifier | CAO boîtier officielle, quatre STEP et notice ; 15 contacts montés en étude, non acheté |'
 if 'connecteur-gpio/README.md' not in t:t=t.replace('\nPrix caméra et moteur','\n'+row+'\n\nPrix caméra et moteur',1)
 start,end=t.split('\nPrix caméra et moteur',1)
 start=re.sub(r'(\|[^\n]+\|)\n(?:\n)+(?=\|)',r'\1\n',start)
 t=start+'\nPrix caméra et moteur'+end
 p.write_text(t,encoding='utf-8')
 p=ROOT/'ReadMe.md';t=p.read_text(encoding='utf-8');marker='<!-- connecteur-gpio-v3 -->'
 if marker not in t:t+='\n'+marker+'\n\nLe [connecteur GPIO et son faisceau](Composants/connecteur-gpio/README.md) retiennent un boîtier Molex à 40 positions et 15 contacts câblés pour l’étude. Documentation, devis, cotes, notice PDF et quatre STEP sont disponibles ; le boîtier possède une CAO fabricant archivée intacte. Prix français, insertion, thermique, seuils ESC et dégagements au cooler restent à vérifier.\n'
 p.write_text(t,encoding='utf-8')
 p=ROOT/'Composants/raspberry-pi-5/integration.md';t=p.read_text(encoding='utf-8')
 if marker not in t:t+='\n'+marker+'\n\nLe [connecteur Molex 40 positions et faisceau de 15 fils](../connecteur-gpio/integration.md) documente le brochage proposé, les sertissages et les limites des deux arrivées 5 V. Sa notice ne valide pas les 5 A de la branche, les entrées ESC ou la tenue aux vibrations.\n'
 p.write_text(t,encoding='utf-8');print('DATA complete',flush=True)
if __name__=='__main__':main()
