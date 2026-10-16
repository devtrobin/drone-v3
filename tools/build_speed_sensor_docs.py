"""Reviewed wheel-speed selection, component records and integration notes."""
from pathlib import Path
import hashlib
import json
import math
import shutil
import sys

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'Composants/capteurs-vitesse'
DATE='2026-10-15'


def write(path,text):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text.strip()+'\n',encoding='utf-8')


def js(path,obj):
    write(path,json.dumps(obj,ensure_ascii=False,indent=2))


PARTS=[
 dict(folder='capteur-hall-drv5033',ref='Texas Instruments DRV5033AJQLPG',qty=2,
      name='Capteur Hall numérique omnipolaire',
      buy='https://fr.rs-online.com/web/p/capteurs-a-effet-hall/9009807',
      source='https://www.ti.com/product/DRV5033/part-details/DRV5033AJQLPG',
      pdf='TI-DRV5033-original.pdf',step='drv5033ajqlpg-detaille.step',
      price='RS France, catégorie semi-conducteurs : 4,16 EUR HT le lot de 10. TTC indicatif calculé à 20 % : 4,99 EUR. Stock affiché ; commande et livraison non vérifiées.',
      facts=[('Alimentation','2,5 à 38 V ; alimentation V3 à 3,3 V du Pi'),
             ('Sortie','Drain ouvert actif bas, rappel externe nécessaire ; pas une sortie analogique'),
             ('Broches LPG','1 = VCC ; 2 = GND ; 3 = OUT. Suivre la vue TI, pas le brochage DBZ'),
             ('Seuil AJ, module du champ','BOP : 3 / 6,9 / 12 mT min / typ / max ; BRP : 1 / 3,5 / 5 mT'),
             ('Fréquence et délai','Bande passante 20 kHz min / 30 kHz typ ; délai de sortie 25 µs max sous conditions TI'),
             ('Courant','2,7 mA typ à 25 °C ; 3,6 mA max à 125 °C selon table TI'),
             ('Boîtier','LPG0003A : largeur 3,9-4,1 ; corps haut 3,05-3,25 ; épaisseur 1,42-1,62 mm'),
             ('Pattes','Pas 1,27 ±0,05 mm ; longueur sous corps 15,1-15,5 mm ; métal étamé'),
             ('Compléments','Un rappel 10 kΩ et un 100 nF par capteur ; aucun module adaptateur acheté')],
      limits='Le capteur est nu, sans PCB, câble ni aimant. Le TO-92 LPG est une forme plate chanfreinée, pas le demi-cylindre TO-92 générique. Les rayons, l’épaisseur du marquage +QLAJ et les nuances sont estimés ; la puce et ses connexions internes ne sont pas documentées.'),
 dict(folder='aimants-s-03-02-n',ref='supermagnete S-03-02-N',qty=4,
      name='Aimant néodyme axial Ø3 × 2 mm',
      buy='https://www.supermagnete.fr/aimants-disques-neodyme/disque-magnetique-3mm-2mm_S-03-02-N',
      source='https://www.supermagnete.fr/data_sheet_S-03-02-N.pdf',
      pdf='supermagnete-S-03-02-N-original.pdf',step='aimant-s-03-02-n-detaille.step',
      price='0,24 EUR TTC par pièce, lot minimum de 20 : 4,80 EUR TTC. Attention : panier minimum du site de 20 EUR, hors port ; cet achat seul ne coûte donc pas seulement 4,80 EUR.',
      facts=[('Quantité montée','4 : deux aimants identiques à 180° par roue arrière'),
             ('Dimensions','Ø3 mm × hauteur 2 mm ; tolérance ±0,1 mm'),
             ('Matière et magnétisation','NdFeB fritté, grade N48, magnétisation axiale'),
             ('Surface','Ni-Cu-Ni, coloris argent ; épaisseurs de couches non publiées'),
             ('Masse','Page produit : 0,11 g arrondi ; fiche PDF : 0,1074 g'),
             ('Rémanence','1,37-1,42 T selon fiche de cet article'),
             ('Température','80 °C maximum d’utilisation ; intérieur sec'),
             ('Adhérence annoncée','2,94 N sur contre-pièce selon conditions fournisseur ; ne dimensionne pas notre fixation tournante')],
      limits='Modèle nominal Ø3 × 2 mm. Petit arrondi d’arête de 0,025 mm estimé pour l’aspect. Aucun repère N/S coloré permanent sur le STEP : le produit réel est argenté. La fixation sera captive dans un support à concevoir avec le châssis ; ne pas compter sur l’attraction magnétique seule.'),
 dict(folder='resistances-rappel-10k',ref='Vishay MRS25000C1002FCT00',qty=2,
      name='Résistance de rappel 10 kΩ',
      buy='https://fr.rs-online.com/web/p/resistances-traversantes/6832939',
      source='https://www.vishay.com/docs/28724/mrs16m25.pdf',
      pdf='Vishay-MRS16-MRS25-original.pdf',step='mrs25-10k-formee-pas10-16.step',
      price='RS 683-2939 : lot de 25 à 2,75 EUR HT. TTC calculé à 20 % : 3,30 EUR. Le TTC affiché de 3,25 EUR est incohérent avec ce HT ; à vérifier au panier.',
      facts=[('Valeur','10 kΩ ±1 %, film métallique ; 0,6 W nominal à 70 °C sous conditions constructeur'),
             ('Rôle','Une résistance par OUT vers 3,3 V, placée côté Pi'),
             ('Courant / pertes','Environ 0,33 mA et 1,09 mW quand OUT est bas'),
             ('Dimensions','Corps Ø2,5 max × longueur 6,5 mm max ; fils Ø0,6 mm nominal'),
             ('Pattes droites','Au moins 28 mm par côté dans le plan de la série'),
             ('Formage','Pas minimum M = 10 mm ; variante V3 à 10,16 mm, géométrie de pliage d’étude'),
             ('Anneaux','10 kΩ à cinq bandes : brun, noir, noir, rouge, brun ; disposition et bleu du corps estimés')],
      limits='Les deux modèles représentent une résistance droite non recoupée et une variante formée. Les anneaux sont des volumes colorés sans chevauchement ; leur position n’est pas une cote fabricant. Les couches résistives internes restent absentes.'),
 dict(folder='condensateurs-decouplage-100nf',ref='KEMET C315C104K5R5TA',qty=2,
      name='Condensateur de découplage 100 nF',
      buy='https://fr.rs-online.com/web/p/condensateurs-ceramique-multicouches/1463570',
      source='https://search.kemet.com/component-documentation/download/specsheet/C315C104K5R5TA',
      pdf='KEMET-C315C104K5R5TA-original.pdf',step='kemet-c315c104k5r5ta-officiel.step',
      price='RS 146-3570 : lot de 20 à 4,68 EUR HT / 5,62 EUR TTC affichés. Ne pas prendre la boîte industrielle de 500 du code 146-3482.',
      facts=[('Valeur','100 nF ±10 %, 50 V DC, diélectrique X7R, non polarisé'),
             ('Rôle','Un par capteur entre VCC et GND, au plus près des broches'),
             ('Exigence TI','10 nF minimum ; 100 nF nominal retenu, capacité utile à vérifier si référence remplacée'),
             ('Enveloppe corps','L 3,81 max ; H 3,14 max ; T 2,54 mm max selon fiche spécifique'),
             ('Pattes','Pas 2,54 ±0,78 mm ; Ø0,51 +0,1/-0,025 mm ; longueur LL ≥7 mm'),
             ('CAO','STEP officiel obtenu par le lien de la fiche KEMET, conservé à l’identique')],
      limits='La CAO constructeur est conservée avec sa géométrie et ses couleurs. Ses arrondis et longueurs ne remplacent pas les tolérances du lot. La prose générique C0G de RS ne concerne pas cette référence X7R : la fiche spécifique KEMET prime.'),
]

INTEGRATION='''# Raccordement des deux voies de vitesse

Deux voies identiques, alimentées par le **3,3 V du Pi**. Aucun 5 V, BEC 6 V ou positif batterie sur ces entrées. Chaque capteur garde un GND de référence. Pi et capteurs s’allument ensemble : pas d’alimentation indépendante susceptible de renvoyer du courant dans un Pi arrêté.

| Liaison | Gauche | Droite |
| --- | --- | --- |
| 3,3 V commun | Broche physique 17 → VCC LPG 1 | Même départ, dérivation en Y → VCC LPG 1 |
| GND commun | Broche physique 25 → GND LPG 2 | Même départ, dérivation en Y → GND LPG 2 |
| OUT | LPG 3 → GPIO23, broche physique 16 | LPG 3 → GPIO24, broche physique 18 |
| Rappel | R1 10 kΩ : OUT → 3,3 V côté Pi | R2 identique |
| Découplage | C1 100 nF : VCC → GND au capteur | C2 identique |

```mermaid
flowchart LR
 P17[Pi 17 : 3,3 V] --> V[DRV5033 LPG 1 : VCC]
 P25[Pi 25 : GND] --> G[DRV5033 LPG 2 : GND]
 V --- C[100 nF local]
 C --- G
 P17 --> R[10 kΩ côté Pi]
 R --> O[OUT LPG 3]
 O --> I[GPIO23 / pin16 ou GPIO24 / pin18]
```

Le plan TI est en **vue de dessus** ; ne pas lire les pattes en retournant le composant sans inverser la vue. Le STEP nomme VCC/GND/OUT et son repère est défini dans la provenance. Confirmer le repère de la pièce et la figure TI p.4 avant soudure. Ne pas reprendre le brochage du SOT-23 DBZ.

Les quatre contacts ajoutés au Molex sont 16, 17, 18, 25. Le faisceau actif passe de 9 à **13 contacts montés**, avec cinq de réserve, donc **18 contacts à provisionner**. Les broches 2/4/6/9/14/20 du connecteur amovible restent vides : la puissance 5 V de la Pi reste séparée. Les anciens STEP et PDF GPIO décrivent leurs anciennes versions, pas ce faisceau.

Réutiliser le fil multibrin 22 AWG du lot prévu. Les dérivations 3,3 V et GND sont des jonctions en Y soudées, isolées individuellement et maintenues ; ne pas doubler deux fils dans un contact Molex prévu pour un seul. Longueurs après implantation. Faire suivre chaque signal de sa référence GND ; garder ces petits faisceaux à distance des phases moteur et de la puissance. Aucun blindage ni filtre RC supplémentaire n’est déclaré nécessaire sans mesure.

Un OUT flottant côté capteur, ou un câble débranché, peut ressembler à une roue arrêtée : ces capteurs ne constituent pas un dispositif d’arrêt de sécurité. La commande devra appliquer ses propres contrôles de plausibilité et son délai de perte Wi-Fi.

## Implantation mécanique réservée

Deux aimants identiques par roue à 180°, axes magnétiques parallèles à l’axe de roue, avec la même face polaire exposée pour une répétabilité initiale. Le DRV5033 est omnipolaire ; aucun passage par une polarité opposée n’est nécessaire pour le réarmer. Il faut en revanche que le champ redescende sous le seuil de relâchement entre aimants.

Placer la face sensible du capteur face aux disques. Commencer les essais avec **1 à 2 mm d’entrefer extérieur**, sans contact possible malgré le voile et les jeux. Cette plage est une position de départ, pas une portée garantie. La profondeur du point sensible, les métaux voisins, les moteurs, les aimants et les tolérances modifient le champ. Exiger deux impulsions propres et un retour haut entre elles sur chaque tour complet.

Réserver une rétention mécanique captive des aimants et un maintien du capteur ; ne pas retenir l’aimant par attraction seule ni laisser la colle seule sans qualification. Pas d’usinage de l’aimant. Un rayon de 12 mm sert uniquement au calcul illustratif des efforts ; aucun disque porteur, poche ou support de châssis n’est conçu ici. La disposition symétrique réduit le balourd théorique, sans garantir l’équilibrage de l’ensemble réel.

## Acquisition

Compter **les fronts descendants uniquement** : deux fronts par tour si la pose est correcte. Utiliser des événements horodatés du système GPIO compatible Pi 5 ; vérifier les pertes avec caméra et Wi-Fi actifs. Ignorer la phase d’établissement à la mise sous tension et initialiser le comptage après stabilisation ; la fiche TI décrit une impulsion au démarrage. Pas d’anti-rebond long qui supprimerait les événements à haute vitesse.

Avec le diamètre de roulement D en mètres : `v_km_h = f_Hz × π × D × 3,6 / 2`. Pour D nominal de 63 mm, 40 km/h correspond à 3 368 tr/min et 112,28 Hz par roue. Calibrer D par une distance roulée sous charge. Un capteur par roue mesure une rotation sans sens de marche ; il ne distingue pas arrêt, rupture de fil et champ permanent. Le patinage fausse la vitesse au sol. En virage les deux roues doivent pouvoir tourner à des vitesses différentes : aucune égalisation permanente gauche/droite.
'''

RESEARCH='''# Recherche, choix et limites

Consultation du 15 octobre 2026. Les données électriques proviennent de TI, les cotes des plans constructeur, les données de l’aimant de la fiche de l’article exact. Les pages RS servent au chiffrage et aux conditionnements, pas à remplacer une spécification fabricant.

- DRV5033AJQLPG actif dans l’addendum TI daté du 24 juin 2026 ; circuit principal SLIS152G de septembre 2016. Choix AJ TO-92 en vrac ; ne pas commander un FA ou un SOT-23 par confusion. Le capteur est plus sensible à la proximité magnétique qu’à la vitesse de rotation elle-même.
- Le support TI E2E « Hall sensing distance » explique que la portée dépend de l’aimant et renvoie au calcul du champ. Aucun entrefer universel de plusieurs centimètres n’est transféré à nos disques de 3 mm. Archive HTML conservée. Ce retour constructeur concerne la physique de détection, pas un essai de notre robot.
- Recherche forum et YouTube sur DRV5033 et vitesse de roue : aucun essai identifié et vérifié reproduisant nos capteurs, aimants, roues et implantation. Aucun avis utilisateur, score ou citation n’est inventé. Les notes Trusted Shops du marchand ne sont pas des avis sur S-03-02-N.
- Recherche Amazon.fr des références exactes : pages de contrôle d’accès reçues, sans offre produit vérifiée. Elles sont distinguées des documents techniques dans assets.json. Les liens de recherche ne garantissent ni référence ni stock. Fournisseurs spécialisés proposés en remplacement de la piste Amazon.
- RS : catégorie France pour le capteur 900-9807, fiche pour la résistance 683-2939 et le condensateur 146-3570. Leurs pages ont été consultées via recherche web ; les téléchargements directs refusent 403. Prix de panier, frais et stock final à revalider. L’affichage TTC de la résistance ne correspond pas au HT : calcul à TVA 20 % conservé séparément.
- Aimant : page et PDF donnent 0,11 g arrondi et 0,1074 g respectivement. Le calcul centrifuge utilise 0,11 g. Le minimum de commande de 20 EUR chez supermagnete est pris en compte ; on ne présente pas le lot à 4,80 EUR comme une commande isolée réalisable.
- La fiche KEMET spécifique remplace la description RS générique qui évoque C0G. Ce composant est X7R. Le lien de la fiche a fourni un STEP natif, archivé sans modification.

## Vérifications physiques nécessaires

Contrôler référence, polarités, brochage et résistances hors tension. Alimenter d’abord les deux voies seules sous 3,3 V limité en courant ; mesurer OUT haut et bas. Vérifier au moins deux états hauts et deux états bas par tour, aux jeux minimum et maximum, moteurs à l’arrêt puis en fonctionnement. Refaire le contrôle en freinage et sous charge électrique, Wi-Fi et vidéo actifs. Vérifier la tenue mécanique des aimants et le dégagement avant rotation rapide.

Comparer les fronts horodatés à un générateur/oscilloscope ou compteur de référence. Le budget RC à 1 nF de charge de ligne et 10 kΩ est une hypothèse (temps de montée 10-90 % ≈22 µs), pas une mesure de câble ni une garantie Linux. Mesurer la largeur minimale des impulsions et le retour haut ; les 112 Hz seuls ne suffisent pas à établir la marge de capture. Déterminer les délais d’alerte et la calibration au roulage.

Les modèles sont extérieurs : aucune structure de puce, piste, épaisseur de revêtement magnétique ou cellule céramique non publiée n’est inventée. L’ensemble reste non acheté, non fabriqué et non testé.
'''


def calculations():
    d=.063;ppr=2
    rows=[]
    for speed in [1,5,20,40]:
        rps=(speed/3.6)/(math.pi*d)
        rows.append(dict(speed_kmh=speed,wheel_rpm=60*rps,pulses_per_s=ppr*rps,period_ms=1000/(ppr*rps)))
    field=[]
    for gap in [1,2,3,4]:
        z=gap+.6;r=1.5;h=2
        b=1.37/2*((z+h)/math.sqrt((z+h)**2+r*r)-z/math.sqrt(z*z+r*r))
        field.append(dict(exterior_gap_mm=gap,assumed_active_depth_mm=.6,on_axis_field_mT=b*1000))
    return dict(date=DATE,hardware_measured=False,nominal_wheel_diameter_m=d,pulses_per_revolution=ppr,
        wheel_rows=rows,distance_per_pulse_m=math.pi*d/ppr,
        speed_quantization_1pulse_1s_kmh=math.pi*d*3.6/ppr,
        pullup=dict(ohm=10000,tolerance=.01,supply_V=3.3,current_low_A=3.3/10000,
                    loss_low_W=3.3**2/10000,assumed_line_capacitance_F=1e-9,rise_10_90_s=2.2*10000*1e-9),
        sensor_supply=dict(typical_each_A=.0027,maximum_each_at125C_A=.0036,
                           total_with_two_pullups_max_study_A=2*(.0036+3.3/9900),
                           scope='Published supply current and low-output pullup budget; validate complete Pi 3V3 rail'),
        centrifugal=dict(assumed_radius_m=.012,mass_conservative_kg=.00011,
                         force_per_magnet_at40_N=.00011*.012*(40/3.6/(math.pi*d)*2*math.pi)**2,
                         scope='Illustrative radius and rounded mass, not retention qualification'),
        field_estimate=dict(model='Uniformly axially magnetised cylinder, on axis, free space',
                            magnet_Br_min_T=1.37,radius_mm=1.5,height_mm=2,rows=field,
                            guaranteed=False,scope='Ignores steel, motor stray field, offset, lot and geometry tolerances; depth 0.6mm assumed'),
        mounting=dict(magnets_per_wheel=2,angular_spacing_deg=180,starting_gap_mm=[1,2],mount_designed=False),
        validation=dict(direction_measured=False,ground_speed_directly_measured=False,hardware_tested=False))


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    for part in PARTS:
        folder=BASE/part['folder']
        rows='\n'.join('| '+a+' | '+b+' |' for a,b in part['facts'])
        write(folder/'README.md',f'''# {part['name']}

**{part['ref']}**, sélection du 15 octobre 2026, non acheté et non testé. Quantité montée : **{part['qty']}**.

[Achat]({part['buy']}) · [Source constructeur]({part['source']}). {part['price']} Aucune offre Amazon.fr exacte validée.

| Caractéristique | Donnée / statut |
| --- | --- |
{rows}

[Cotes](cotes.md), [notice de montage](notice-montage.md), [notice PDF de l’ensemble](../notices/notice-capteurs-vitesse-v3.pdf), [documents originaux](../notices/README.md), [devis](../devis.md), [recherche et avis](../recherche-technique.md), [STEP et aperçus](3D/README.md).

{part['limits']}

[Vue d’ensemble et raccordement](../README.md).
''')
        write(folder/'cotes.md',f'# Cotes - {part["ref"]}\n\nSource : [fiche originale](../notices/{part["pdf"]}).\n\n| Paramètre | Valeur / statut |\n| --- | --- |\n'+rows+'\n\n'+part['limits']+'\n\nChaque STEP possède un JSON de provenance avec les cotes retenues et les estimations. Les cotes maximales d’enveloppe ne deviennent pas des valeurs nominales mesurées.\n')
        write(folder/'notice-montage.md',f'# Montage - {part["ref"]}\n\n'+INTEGRATION+'\n\n'+part['limits'])
        js(folder/'selection.json',dict(date=DATE,**part,hardware_tested=False,purchased=False,Amazon_exact_offer_verified=False))
        js(folder/'sources.json',dict(checked_on=DATE,manufacturer=part['source'],purchase=part['buy'],original_pdf='../notices/'+part['pdf'],shared_assets='../assets.json',research='../recherche-technique.md'))

    js(BASE/'calculs.json',calculations())
    js(BASE/'nomenclature.json',dict(date=DATE,items=PARTS,additional_GPIO_contacts=4,
        installed_GPIO_contacts_total=13,GPIO_contacts_to_provision_total=18,
        reused_stock_planned_not_owned=['Fil 22 AWG Adafruit 3175','Gaine et consommables selon lots prévus'],
        soldered_Y_branches=['3V3 speed sensors','GND speed sensors'],chassis_mount_deferred=True,purchased=False))
    write(BASE/'README.md','''# Mesure de vitesse des roues arrière

Sélection du **15 octobre 2026**. Deux capteurs numériques TI et quatre aimants, complétés par leurs rappels et découplages. Ajout de mesure pour la mise au point ; aucune pièce ni performance testée.

| Composant | Référence | Monté | Dossier |
| --- | --- | ---: | --- |
| Capteur Hall 3,3 V | DRV5033AJQLPG, TO-92 LPG | 2 | [Documentation et STEP](capteur-hall-drv5033/README.md) |
| Aimant axial Ø3 × 2 | supermagnete S-03-02-N, N48 | 4 | [Documentation et STEP](aimants-s-03-02-n/README.md) |
| Rappel OUT | Vishay MRS25 10 kΩ ±1 % | 2 | [Documentation et STEP](resistances-rappel-10k/README.md) |
| Découplage local | KEMET C315C104K5R5TA, 100 nF X7R | 2 | [Documentation et STEP officiel](condensateurs-decouplage-100nf/README.md) |

[Notice PDF](notices/notice-capteurs-vitesse-v3.pdf) · [Raccordement et acquisition](integration.md) · [Cotes d’ensemble](cotes.md) · [Calculs](calculs.json) · [Devis](devis.md) · [Recherche et avis](recherche-technique.md) · [Documents constructeur](notices/README.md) · [Tous les modèles](3D/README.md) · [Brochage](brochage.json).

Deux aimants identiques à 180° donnent deux impulsions par tour. À 40 km/h avec une roue nominale de 63 mm : environ **3 368 tr/min et 112,28 Hz**. Le capteur ne donne pas le sens de marche ; le patinage et le diamètre sous charge limitent la vitesse au sol estimée. En virage, les deux vitesses de roue sont différentes.

GPIO23/pin16 et GPIO24/pin18 sont réservées aux sorties, avec 3,3 V pin17 et GND pin25. Le Molex passe à **13 contacts montés et 18 à provisionner** avec cinq de réserve. Le faisceau 5 V séparé de la Pi reste celui de la révision alimentation R2. Les anciens modèles de faisceau GPIO ne représentent pas cette extension.

Aucune offre Amazon.fr exacte vérifiée ; les pistes RS et supermagnete sont documentées. Devis partiel avec conditionnements et minimum de commande, sans achat. Fixation captive des aimants, supports, longueurs des fils et implantation mécanique réservés au châssis final. Aucun schéma/routage de la carte de surveillance modifié par cet ajout.
''')
    write(BASE/'integration.md',INTEGRATION)
    write(BASE/'recherche-technique.md',RESEARCH)
    write(BASE/'cotes.md','''# Cotes de l’ensemble et interfaces

Les [quatre dossiers de composants](README.md) détaillent les dimensions sources et reconstruites. STEP en millimètres. Le capteur est reconstruit au milieu des tolérances du plan TI ; le corps de résistance reprend l’enveloppe maximale, les pattes droites la longueur minimale documentée. Le condensateur dispose d’un STEP constructeur natif. L’aimant est modélisé à Ø3 × 2 mm nominaux.

Implantation proposée : deux aimants à 180° par roue, champ axial et capteur face aux disques ; entrefer initial 1-2 mm à tester. Le rayon de 12 mm du calcul n’est pas une interface mécanique arrêtée. Les poches, rétentions, supports, débattements et câbles restent à concevoir avec le châssis. Aucune roue existante modifiée, aucun perçage imposé.

Le demi-profil LPG respecte les chanfreins du dessin constructeur. Son repère CAO : X sur l’alignement des broches, Z le long des pattes, corps bas z=0 ; face plane marquée vers -Y ; broches VCC/GND/OUT repérées x=-1,27/0/+1,27. Ce repère est propre à la reconstruction : utiliser la figure TI pour identifier les broches réelles.
''')
    write(BASE/'devis.md','''# Devis indicatif et liens d’achat

Consultation du 15 octobre 2026, aucune commande. Les références exactes sont celles de la nomenclature ; liens Amazon de recherche sans offre vérifiée.

| Pièce | Montée | Achat proposé | Prix du conditionnement |
| --- | ---: | --- | --- |
| [DRV5033AJQLPG](https://fr.rs-online.com/web/p/capteurs-a-effet-hall/9009807) | 2 | Lot de 10, RS 900-9807 | 4,16 EUR HT ; 4,99 EUR TTC calculé à 20 % |
| [MRS25000C1002FCT00](https://fr.rs-online.com/web/p/resistances-traversantes/6832939) | 2 | Lot de 25, RS 683-2939 | 2,75 EUR HT ; 3,30 EUR TTC calculé, affichage TTC incohérent à revalider |
| [C315C104K5R5TA](https://fr.rs-online.com/web/p/condensateurs-ceramique-multicouches/1463570) | 2 | Lot de 20, RS 146-3570 | 4,68 EUR HT ; 5,62 EUR TTC affiché |
| [S-03-02-N](https://www.supermagnete.fr/aimants-disques-neodyme/disque-magnetique-3mm-2mm_S-03-02-N) | 4 | Lot de 20 chez supermagnete | 4,80 EUR TTC, mais panier du marchand ≥20 EUR |
| Contacts Molex 16-02-0103 | 4 supplémentaires | Porter la provision totale de 14 à18 | Ancien prix 0,25 USD/unité à revalider ; pas un prix France |
| Fil 22 AWG, gaine et consommables | Selon implantation | Lots déjà prévus, pas supposés possédés | Pas de doublon de lot ; coupe et coût consommé après implantation |

RS : sous-total des trois conditionnements **11,59 EUR HT**, soit environ **13,91 EUR TTC à 20 %**, hors frais et revalidation. Avec le lot d’aimants seul, les marchandises nominales font 18,71 EUR TTC ; ce n’est **pas une commande isolée réalisable** chez supermagnete, dont le panier doit atteindre 20 EUR. Avec cette contrainte, provision de **33,91 EUR TTC au minimum avant ports**, hors contacts et consommables, sous les hypothèses de TVA et prix ci-dessus. Aucun ajout au panier ou achat effectué. Regrouper un achat existant ou trouver un revendeur exact pourra réduire cette contrainte ; aucun remplacement générique n’est validé ici.

Prix/stock RS trouvés sur les pages publiques consultées ; téléchargements directs 403 consignés dans assets.json. La catégorie France [semi-conducteurs](https://fr.rs-online.com/web/c/semi-conducteurs/?pn=67) affichait le capteur en stock à4,16 EUR HT le lot. Les fiches exactes résistance et condensateur affichent également un stock, sans garantie au jour de commande. Livraison, éventuels frais de traitement et TTC final à vérifier.

[Recherche Amazon capteur](https://www.amazon.fr/s?k=DRV5033AJQLPG) · [Recherche Amazon aimants](https://www.amazon.fr/s?k=supermagnete+S-03-02-N). Contrôles d’accès reçus : aucun ASIN, vendeur, prix ou stock Amazon déclaré confirmé.
''')
    write(BASE/'notices/README.md','''# Notices et documents d’origine

- [Notice V3 de montage et d’intégration](notice-capteurs-vitesse-v3.pdf), rédigée pour les deux voies de vitesse.
- [TI DRV5033 SLIS152G](TI-DRV5033-original.pdf), 32 pages : brochage p.4, caractéristiques p.5-6, champ p.10, découplage et exemple p.16-19 ; addendum de commande du24 juin2026.
- [Plan TI LPG0003A](TI-LPG0003A-plan-original.pdf), 4 pages, dessin4221343/C janvier2018.
- [Article exact supermagnete](supermagnete-S-03-02-N-original.pdf), 4 pages, propriétés, cotes et sécurité d’utilisation.
- [Vishay MRS16/MRS25](Vishay-MRS16-MRS25-original.pdf), 4 pages, fiche du7mars2016 ; cotes p.3.
- [Fiche spécifique KEMET](KEMET-C315C104K5R5TA-original.pdf), 4 pages, générée le15octobre2026 ; cotes p.1 et lien vers STEP natif.

Les cinq originaux PDF restent inchangés. Les URL, dates, erreurs d’accès et empreintes SHA256 figurent dans [assets.json](../assets.json). Les documents, plans SVG, photo d’aimant et STEP KEMET d’origine sont archivés. Les captures de contrôle d’accès Amazon ne constituent pas des offres commerciales.
''')
    js(BASE/'brochage.json',dict(date=DATE,numbering='Pi physical pins and BCM GPIO explicitly distinguished',
        Pi=dict(left_OUT=dict(physical_pin=16,BCM=23),right_OUT=dict(physical_pin=18,BCM=24),VCC_physical_pin=17,GND_physical_pin=25),
        TI_LPG=dict(pin1='VCC',pin2='GND',pin3='OUT'),supply_V=3.3,pullups_to_V=3.3,
        decoupling_each_F=1e-7,pullup_each_ohm=10000,power_5V_separate=True,hardware_wired=False))
    js(BASE/'sources.json',dict(checked_on=DATE,manufacturer_sources=[p['source'] for p in PARTS],
        supplier_pages=[p['buy'] for p in PARTS],
        sensor_FR_price_source='https://fr.rs-online.com/web/c/semi-conducteurs/?pn=67',
        forum='https://e2e.ti.com/support/sensors-group/sensors/f/sensors-forum/816464/drv5033-hall-sensing-distance',
        forum_use='Manufacturer support: sensing distance depends on magnet field, no transferred gap guarantee',
        YouTube_relevant_verified_test_found=False,Amazon_exact_offer_verified=False,hardware_tested=False))

    # Add a dated extension to the existing, reviewed R2 harness. Do not rewrite PDFs/STEP.
    gpio=ROOT/'Composants/connecteur-gpio'
    current=json.loads((gpio/'brochage.json').read_text(encoding='utf-8'))
    archive=gpio/'brochage-alimentation-r2-9-contacts.json'
    if not archive.exists():shutil.copyfile(gpio/'brochage.json',archive)
    speed_pins={16,17,18,25}
    existing={p['physical_pin'] for p in current['pins']}
    for pin,signal,color,func,dest in [
        (16,'SPEED_G','blanc, repéré','GPIO23 / vitesse gauche','OUT du DRV5033 gauche ; rappel10 kΩ à3,3 V côtéPi'),
        (17,'3V3_SPEED','vert, repéré','3,3 V capteurs','Dérivation enY vers les deux VCC, broche1 LPG'),
        (18,'SPEED_D','jaune, repéré','GPIO24 / vitesse droite','OUT du DRV5033 droit ; rappel10 kΩ à3,3 V côtéPi'),
        (25,'GND_SPEED','noir, repéré','GND capteurs','Dérivation enY vers les deux GND, broche2 LPG')]:
        if pin not in existing:current['pins'].append(dict(physical_pin=pin,signal=signal,color=color,AWG=22,function=func,destination=dest))
    current['pins'].sort(key=lambda x:x['physical_pin'])
    current['unused_pins']=sorted(set(current['unused_pins'])-speed_pins)
    current.update(revised_on=DATE,signal_contacts_used=13,harness_revision='vitesse-r1-after-alimentation-r2',speed_sensors_source='../capteurs-vitesse/integration.md')
    js(gpio/'brochage.json',current)
    nom=json.loads((gpio/'nomenclature.json').read_text(encoding='utf-8'))
    for part in nom['parts']:
        if '16-02-0103' in part['reference']:part.update(quantity=18,installed=13,spares=5)
    nom.update(connector_populated_contacts=13,provisional_sum_USD_at_unit1_prices=2.95+18*.25+29.95,
               revised_on=DATE,harness_revision='vitesse-r1-after-alimentation-r2')
    js(gpio/'nomenclature.json',nom)
    for name in ['calculs.json','validation-dossier.json']:
        path=gpio/name
        if path.exists():
            record=json.loads(path.read_text(encoding='utf-8'))
            record.update(removable_contacts_at_alimentation_r2=9,current_removable_harness_contacts=13,
                          current_harness_revision='vitesse-r1-after-alimentation-r2',
                          current_harness_check='../capteurs-vitesse/verification.json')
            js(path,record)
    prefix='''<!-- vitesse-r1 -->
> **Extension capteurs de vitesse du15octobre2026 :** faisceau actuel à13 contacts montés,18 à provisionner avec5 de réserve. Ajouts : pins16/18 (GPIO23/24),17 (3,3 V) et25 (GND). La puissance5 V reste séparée. [Raccordement actuel](../capteurs-vitesse/integration.md). Les modèles et notices GPIO antérieurs sont des instantanés.
<!-- /vitesse-r1 -->

'''
    for name in ['README.md','integration.md','devis.md','3D/README.md']:
        path=gpio/name
        if not path.exists():continue
        content=path.read_text(encoding='utf-8')
        if '<!-- vitesse-r1 -->' not in content:
            # Different relative link from the 3D subdirectory.
            write(path,(prefix.replace('../capteurs-vitesse/','../../capteurs-vitesse/') if name.startswith('3D/') else prefix)+content)
    index=ROOT/'Composants/README.md';text=index.read_text(encoding='utf-8')
    if '<!-- capteurs-vitesse-v3 -->' not in text:
        write(index,text+'''\n\n<!-- capteurs-vitesse-v3 -->
## Capteurs de vitesse ajoutés le15octobre2026

[Ensemble documenté](capteurs-vitesse/README.md) : deux DRV5033AJQLPG, quatre aimants S-03-02-N, deux rappels10 kΩ et deux100 nF. Notice, cotes, devis, originaux constructeur et STEP par composant. Brochage GPIO actif à13 contacts ; anciens ensembles électriques datés conservés. Supports et rétention des aimants réservés au châssis final.
<!-- /capteurs-vitesse-v3 -->''')
    root=ROOT/'ReadMe.md';text=root.read_text(encoding='utf-8')
    if 'capteurs-vitesse/README.md' not in text:
        write(root,text+'\n\n[Mesure de vitesse des deux roues arrière](Composants/capteurs-vitesse/README.md) : deux capteurs Hall, deux aimants par roue, rappels et découplages ; extension GPIO à13 contacts. Implantation finale avec le châssis.\n')
    print('Four component dossiers and current GPIO extension written',flush=True)


if __name__=='__main__':main()
