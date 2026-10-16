"""Document what is actually known, including the missing commercial basket."""
from pathlib import Path
from itertools import product
import json,sys,hashlib

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'Composants/protection-batterie'

def write(name,body):
    p=BASE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(body.strip()+'\n',encoding='utf-8')

def bounds(top,bottom=10000):
    vals=[v*(1+rt/rb)+ib*rt for v,rt,rb,ib in product((.387,.400),(top*.999,top*1.001),(bottom*.999,bottom*1.001),(-25e-9,25e-9))]
    return dict(falling_typical_V=.3945*(1+top/bottom),falling_corner_min_V=min(vals),falling_corner_max_V=max(vals),
        rising_typical_V=.400*(1+top/bottom),top_ohm=top,bottom_ohm=bottom,
        resistor_tolerance=.001,falling_reference_range_V=[.387,.400],input_bias_bound_A=25e-9)

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    calc=dict(warning=bounds(80400),hard_cut=bounds(75000),hardware_tested=False,
      manufacturer_cell_minimum_V=3.2,TLV_source='TI-TLV6700-datasheet.pdf PDF5',
      current_is_not_ESC_rating=True,SSR_rds_max_ohm=.005,
      ssr_losses_W=[dict(current_A=i,power_W=i*i*.005,drop_V=i*.005) for i in (10,20,30,40,60)],
      pi_branch_input_A_at_25W_output_6_4V_and_90pct=25/.9/6.4,
      guaranteed_shutdown_time_s=None,autonomy_guarantee=False)
    assert calc['hard_cut']['falling_corner_min_V']>3.2
    assert calc['warning']['falling_corner_min_V']>calc['hard_cut']['falling_corner_max_V']
    write('calculs.json',json.dumps(calc,ensure_ascii=False,indent=2))
    write('README.md','''# Surveillance et coupure de batterie - V3

**Etude préliminaire du 13 octobre 2026. Non achetée, non fabriquée, non testée.** Aucun module Amazon vérifiable réunissant mesure par cellule, alerte Pi, coupure indépendante et courant des deux moteurs n’a été identifié. Le panier français et le coût total restent ouverts.

La proposition comporte trois parties, chacune dans son dossier :

| Partie | Choix d’étude | Rôle |
| --- | --- | --- |
| [Surveillance 2S](surveillance-2s/README.md) | Carte analogique V3, 2 TLV6700, 4 optocoupleurs et logique | Surveiller chaque cellule ; avertir le Pi puis demander la coupure sans logiciel |
| [Interrupteur Pi](interrupteur-pi/README.md) | Pololu 2813 HP | Couper la branche du régulateur Pi et la commande du relais moteurs |
| [Coupure moteurs](coupure-moteurs/README.md) | Sensata/Crydom D1D100, version à vis | Porter le courant des deux ESC ; refroidissement à dimensionner |

La carte de surveillance est **une conception à fabriquer**, pas une carte du commerce. Son STEP représente une implantation d’étude ; les pistes ne constituent pas un routage validé. Le choix du relais industriel est une référence techniquement documentée, avec un coût et un encombrement à comparer avant achat. Ce choix ne garantit pas le budget initial de 200 euros.

Seuils typiques calculés en descente : **avertissement 3,566 V/cellule**, **coupure 3,353 V/cellule**. Ils incluent l’hystérésis du TLV6700. Les seuils exacts, les délais et le comportement sous charge restent à mesurer. Deux fenêtres de seuil distinctes permettent une extinction normale ; elles ne garantissent pas un temps fixe disponible pour l’arrêt Linux.

[Architecture et branchements proposés](integration.md), [recherche et alternatives](recherche-technique.md), [nomenclature](nomenclature.json), [calculs](calculs.json), [notice PDF du projet](notices/notice-protection-batterie-v3.pdf), [trois modèles STEP et aperçus](3D/README.md).

Les sources constructeur sont conservées sans modification, avec SHA256 dans les `assets.json` de chaque partie. La notice de projet est distincte de leurs fiches techniques. Aucune configuration ou commande n’est appliquée à une Raspberry Pi.
''')
    write('integration.md','''# Intégration proposée - surveillance et coupure 2S

**Architecture d’étude, pas un faisceau validé ou un PCB prêt à fabriquer.** La carte observe la décharge ; elle n’est ni un chargeur, ni un équilibrage actif, ni une protection contre toutes les défaillances possibles. La charge reste réalisée avec le SkyRC S65, batterie retirée du véhicule.

## Chemins de puissance

```mermaid
flowchart LR
 B[Batterie 2S] --> F[MIDI 60 A principal : choix d'étude]
 F --> D[MiniBus 2315 D+]
 D --> FP[ATO 7,5 A Pi : étude]
 FP --> P[Pololu 2813 HP]
 P -->|VSW| R[Pololu D24V90F5]
 R --> PI[Pi 5 et caméra]
 D -->|Borne +2| S[SSR Crydom D1D100]
 S -->|Borne 1| J[UD80A 569010 : répartition positive]
 J --> F1[ATO30 départ ESC1 : étude]
 J --> F2[ATO30 départ ESC2 : étude]
 F1 --> E1[ESC arrière 1 et BEC direction]
 F2 --> E2[ESC arrière 2, positif BEC isolé]
 P -.->|VSW vers entrée +3; retour 4 vers B0| S
 B -->|B0, B1, B2: mesure seulement| M[Surveillance 2S V3]
 M -->|WARN1 et WARN2| PI
 M -->|Défaut cellule: logique vers OFF| P
 PI -->|GPIO au terme de poweroff, via diode| P
```

**Le Pololu 2813 ne porte pas le courant moteur.** Il porte seulement le régulateur Pi et la commande du SSR. Pour 5 A / 5 V de sortie, 90 % de rendement supposé, 6,4 V d'entrée et 15 mA de commande SSR supposés, le courant d'étude atteint 4,36 A. Le fabricant a mesuré 6 A pour une température MOSFET de 55 °C, à 12 V et dans un air ambiant calme de 22 °C : 55 °C n'est pas la température ambiante, et 6 A n'est pas un seuil de coupure. La résistance et le chauffage à 6,4–8,4 V doivent être mesurés. Utiliser les grands pads et un faisceau de puissance dimensionné ; pas les seuls petits contacts de signal.

La [protection du départ Pi](../protection-branche-pi/integration.md) propose le Blue Sea 5065 avec un ATO 7,5 A, avant VIN du Pololu 2813. Les [deux départs moteurs](../protection-branches-moteurs/integration.md) reçoivent chacun un 5065 et un ATO30 après le relais et le [répartiteur UD80A569010](../repartition-moteurs/integration.md). Calibres, fils ESC 16 AWG, connexions, pointes et pouvoir de coupure de 1 000 A restent à qualifier avec le pack ; arrêt global sur perte d'un seul départ à concevoir.

Pour une coupure côté positif avec le D1D100 : **borne +2 au positif batterie protégé**, **borne 1 au positif des ESC**. Entrée **+3 àVSW**, **4 àB0**. La polarité est publiée dans le schéma Sensata PDF3 ; ce relais n’est pas un contact mécanique réversible. Une GPIO3,3 V seule est sous le minimum de commande3,5 V : elle ne pilote pas directement ce relais. Le contrôle suit ici la sortie batterie commutée du Pololu.

Prévoir les protections contre les transitoires conformément au fabricant et mesurer la tension des ESC au freinage et à la coupure. Le courant de régénération inverse, les condensateurs des ESC et les chemins de retour doivent être étudiés. Ne pas ajouter une diode ou une TVS sans vérifier sa tension, son énergie et son effet sur le freinage. Le choix des fusibles et des sections reste à terminer avant câblage. Le [HS251 + HSP-1](../dissipateur-relais/integration.md) constitue désormais la sélection de refroidissement d'étude ; qualification thermique à réaliser.

## Deux références locales de mesure

B0 est le négatif du pack ; B1 son point milieu ; B2 son positif. **Vcell1=B1-B0**, **Vcell2=B2-B1**. Le TLV6700 de la cellule1 est alimenté entre B1 etB0, celui de la cellule2 entre B2 etB1. Leurs sorties passent par des optocoupleurs. Le retour local B1 du second circuit ne doit pas être relié au GND du Pi. Le courant de puissance ne passe jamais dans les fils d’équilibrage.

Par cellule :

| Fonction | Circuit proposé |
| --- | --- |
| Avertissement | INA+ reçoit le pont80,4 kΩ /10 kΩ ; OUTA bas sous le seuil allume l’opto WARN |
| Réserve de coupure | INB- reçoit75,0 kΩ /10 kΩ ; OUTB bas au-dessus du seuil maintient l’opto HEALTHY allumé |
| Défaut indépendant | Sous le seuil, OUTB devient haute impédance ; l’opto HEALTHY s’éteint et son collecteur remonte |
| Filtrage |100 nF près de VDD ;100 nF à chaque entrée de mesure, constante de temps d’environ0,9 ms |

Résistances de mesure **0,1 %**. La valeur80,4 kΩ peut être réalisée avec deux40,2 kΩ en série. Résistances LED proposées1,5 kΩ ; Vishay **VOS618A-8T**, bin CTR130-260 % à1 mA. Ne pas remplacer ce bin par une référence sans bin à faible CTR en supposant les mêmes niveaux. Les limites de saturation, le CTR à la température d’usage et le courant LED doivent être contrôlés sur les pièces reçues.

## Interface logique et maintien après arrêt

La logique indépendante est alimentée en 3,3 V par un **MCP1703AT-3302E/MB (SOT-89)**, alimenté en amont de la coupure depuis B2/B0. Son rôle se limite au circuit de surveillance ; il ne fournit pas l’alimentation du Pi. Capacités entrée/sortie 1 µF à sélectionner selon la fiche Microchip, plus découplages 100 nF. Le suffixe DB correspond au SOT-223, pas au boîtier représenté ici.

Chaque collecteur HEALTHY possède une remontée47 kΩ àcette alimentation. **Deux entrées d’un SN74LVC2G17DCKR** reçoivent ces niveaux ; les deux sorties sont réunies vers OFF par **deux diodes BAT54**, cathodes côté OFF. Une troisième BAT54 reçoit la commande finale du Pi. Il s’agit d’un OU de commandes hautes, pas de sorties GPIO reliées directement ensemble. La résistance de rappel externe OFF proposée100 kΩ est à qualifier avec le réseau d’entrée Pololu.

Les tampons sont nécessaires : l’entrée OFF du Pololu possède un réseau interne10 kΩ/transistor ; une simple remontée47 kΩ depuis les optocoupleurs ne suffit pas à garantir sa commande. Le seuil publié OFF est supérieur à1 V. Les pertes des diodes et les niveaux réels doivent être mesurés. ON et CTRL restent non commandés ; le maintien d’un défaut doit empêcher le réarmement au bouton, point à vérifier au banc et non garanti ici.

Les collecteurs WARN sont séparés : remontée externe47 kΩ au **3,3 V du Pi**, émetteurs au GND Pi. Propositions de broches, non câblées :

| Signal | GPIO BCM | Broche physique | Etat |
| --- | ---: | ---: | --- |
| WARN1 |17 |11 | Bas si cellule1 faible |
| WARN2 |27 |13 | Bas si cellule2 faible |
| Arrêt final |22 |15 | Haut au terme de l’arrêt système, via diode vers OFF |
| Référence |GND |6 ou9 | Masse du système |

Ces GPIO ne chevauchent pas les PWM12/13/18 réservés aux moteurs et au servo. **Les rails de cellule et VSW ne sont pas des signaux GPIO.** Le connecteur logique d’étude porte GND,3V3 Pi,WARN1,WARN2,DONE etOFF ; le repérage doit être confirmé sur un schéma électrique définitif et sur la carte fabriquée.

## Séquence prévue

1. Mise en marche manuelle, contrôle des cellules et initialisation ; moteurs non armés avant commande neutre et autorisation logicielle.
2. En cas de WARN1 ouWARN2, interdire une nouvelle accélération, arrêter les moteurs selon le comportement de freinage vérifié, interrompre l’enregistrement puis demander l’arrêt du système.
3. Au terme de l’arrêt, la GPIO de poweroff commande OFF. Le Pololu coupe le régulateur Pi et le signal du SSR, qui coupe les ESC.
4. Si une cellule atteint auparavant le seuil bas, la voie analogique demande immédiatement OFF. La protection de batterie prend alors la priorité sur l’extinction propre ; celle-ci n’est pas garantie dans ce cas.

Le `gpio-poweroff` officiel démarre inactif et produit un signal actif àl’arrêt. Une piste pour le système reçu est `dtoverlay=gpio-poweroff,gpiopin=22`, polarité haute, **à tester sur Pi5 /OS choisi**. La documentation officielle indique des effets sur la séquence normale d’arrêt et de redémarrage : vérifier reboot, bouton, watchdog et remise sous tension. Aucun réglage n’a été appliqué. La supervision WARN exige un service logiciel qui reste à développer.

La carte reste alimentée par le port d’équilibrage après la coupure et consomme encore du courant. **Débrancher batterie et prise d’équilibrage pour le stockage.** Le montage ne garantit pas une isolation galvanique de toutes les branches et ne remplace pas un arrêt d’urgence. Pololu déconseille explicitement son interrupteur pour une fonction d’arrêt d’urgence ; il est retenu ici comme commande de fonctionnement à qualifier.

## Validation avant fabrication et roulage

Alimentation de laboratoire limitée en courant, deux cellules simulées indépendamment. Mesurer chaque seuil en montée/descente, courant de repos par cellule, fonctionnement avec cellule déséquilibrée, erreur de polarité évitée par repérage, perte de B0/B1/B2 et défaut de source logique. Vérifier OFF pendant défaut maintenu, rebonds et bruit moteur, retour d’alimentation, service bloqué et Pi éteint. Tester ensuite l’arrêt Linux avec caméra active, et le relais àcourants représentatifs avec surveillance thermique. Une alimentation virtuelle àdeux tensions ne remplace pas tous les essais sur batterie.

Il faut encore un schéma électrique détaillé, ERC/DRC, routage, empreintes et choix des protections avant tout Gerber ou usinage CNC. La CAO jointe est destinée àl’implantation mécanique. [Calculs](calculs.json), [index](README.md).
''')
    write('recherche-technique.md','''# Recherche, alternatives et retours utilisateurs

Recherche du13 octobre2026. La proposition reste une étude ; les recherches Amazon.fr ciblées n’ont pas permis d’identifier une offre vérifiable réunissant toutes les fonctions. Les liens ci-dessous sont des recherches, pas des ASIN confirmés ni un panier validé.

| Solution examinée | Constat technique | Décision |
| --- | --- | --- |
| ServoCity Low Voltage Cutoff Switch |2S: coupure fixe6 V pour le pack,15 A continus à6 V ; pas de mesure individuelle ni alerte Pi documentée | Ecarté pour cette fonction |
| BMS génériques2S | Références/courants et seuils hétérogènes ; communication et extinction Linux rarement documentées | Ne pas assimiler un marquage commercial à une validation |
| Junsi CellLog8S | Notice complète, mesure2-8S et sortie collecteur ouvert ; offre Amazon actuelle non établie et disponibilité ancienne incertaine | Référence de comparaison, pas achat retenu |
| Enepaq TinyBMS s516 actuel | Constructeur:4-16S,9-75 V ; incompatible avec notre2S | Ecarté malgré des fiches anciennes ambiguës |
| Chargery BMS8T | Pour2-3S, la notice V4.2 exige une alimentation externe15-30 V ; contacteur séparé | Ecarté pour l’intégration compacte |
| Pololu2813 sur tous les moteurs |16 A correspond à150°C et non àune limite froide ;6 A à55°C selon essai fabricant12 V | Ecarté de la puissance moteur ; retenu sur la branche Pi |
| Crydom D1D100 | Sortie DC1-72 V recommandés,100 A avec conditions thermiques ; commande3,5-32 V ; datasheet et plan | Référence d’étude pour la branche moteur, prix et dissipateur àfinaliser |

Sources des exclusions : [ServoCity](https://www.servocity.com/low-voltage-cutoff-switch/), [CellLog constructeur](https://www.hillrc.com/UploadFiles/CellLog_8S.pdf), [TinyBMS constructeur](https://enepaq.com/product/battery-management-system-bms-150a-set-tinybms-s516/), [Chargery constructeur](https://www.chargery.com/doc/Chargery_BMS8T_specification_V4.2.pdf), [Pololu](https://www.pololu.com/product/2813), [Sensata](https://www.sensata.com/sites/default/files/a/sensata-1-dc-series-d1d-dc-output-panel-mount-datasheet.pdf).

## Avis et expériences

- [Pololu, extinction d’un Pi,2021](https://forum.pololu.com/t/raspberry-pi-can-it-turn-itself-off-with-the-mini-pushbutton-power-switch/21371) : un utilisateur rapporte que le passage d’une polarité basse àune polarité haute de `gpio-poweroff` a permis l’arrêt avec son interrupteur Mini. Retour sur une autre carte et une ancienne génération de Pi ; pas une validation du2813 avec Pi5.
- [Pololu2813, fluctuation d’alimentation,2017](https://forum.pololu.com/t/problem-with-pushbutton-power-switch-item-2813-auto-on-with-power-fluctuation/13660) : signalement d’un allumage inattendu pendant une chute d’alimentation automobile. Témoignage individuel qui motive un essai des transitoires et du redémarrage ; ne pas généraliser àtous les exemplaires.
- Aucun avis n’existe pour notre carte V3 non fabriquée. Aucun banc d’essai utilisateur attribuable au D1D100 dans un robot2S équivalent n’a été identifié. Les courbes constructeur restent la base du dimensionnement, sans prétendre valider notre montage.

## Achat et coût

[Recherche Amazon Pololu2813](https://www.amazon.fr/s?k=Pololu+2813+HP), [Recherche Amazon CrydomD1D100](https://www.amazon.fr/s?k=Crydom+D1D100), [Recherche Amazon TLV6700](https://www.amazon.fr/s?k=TLV6700). **ASIN, vendeur, livraison, prix euro et stock non confirmés.** Les photos Pololu et sa CAO native ne prouvent pas la disponibilité Amazon. Fournisseurs constructeur/distributeurs àcomparer si Amazon reste la préférence.

La carte V3 exige des circuits précis, passifs0,1 %, connecteurs et fabrication. Le relais industriel et son refroidissement peuvent rendre la solution coûteuse. Aucun coût final ni respect des200 euros n’est annoncé. Une optimisation ultérieure peut remplacer l’étage industriel par une carte MOSFET conçue et qualifiée, avec ses propres contraintes ; ce remplacement n’est pas réalisé ici.

## Cotes et fidélité

Pololu: STEP officiel commun2812/2813, inchangé. Crydom: enveloppe57,3×44,5×22,6 mm et fixation reprises du plan fabricant, détails extérieurs estimés. Carte V3:54×32×1,6 mm choisis pour l’étude, quatre trousØ2,2 aux entraxes48×26. Les pistes de ce modèle ne sont pas le plan électrique. Aucun circuit interne de relais ni carte commerciale imaginaire n’est dessiné.
''')
    components=[
      ('surveillance-2s','Carte analogique de surveillance2S V3','Conception àfabriquer autour de2 TLV6700DDCR ; aucun microcontrôleur ajouté.',
       'Dimensions de projet 54×32×1,6 mm ; montage mécanique provisoire. Deux seuils par cellule, 4 VOS618A-8T, SN74LVC2G17DCKR, MCP1703AT-3302E/MB (SOT-89) et 3 BAT54-7-F. Aucun modèle commercial ni prix Amazon confirmé.',
       'https://www.ti.com/product/TLV6700'),
      ('interrupteur-pi','Interrupteur Pololu2813 HP','Une unité, uniquement pour branche Pi et commande du relais.',
       '4,5–32 V recommandés, 40 V absolus. PCB 20,3 × 25,4 mm ; quatre trous Ø2,18, plan constructeur. Essais fabricant à 12 V, air calme à 22 °C : 6 A pour une température MOSFET de 55 °C et 16 A pour 150 °C. Ces températures sont celles des MOSFET ; aucun seuil actif de limitation à 6 A n’est annoncé. Température réelle à 2S à vérifier. OFF haut supérieur à 1 V ; accessoires du kit non modélisés comme soudés.',
       'https://www.pololu.com/product/2813'),
      ('coupure-moteurs','Relais DC Sensata/CrydomD1D100','Une unité, version àvis standard, pour les deux ESC.',
       'Charge DC1-72 V recommandés,100 V absolus ;100 A sous conditions thermiques, pas sans dissipateur. Commande3,5-32 V et10-15 mA. Rds max5 mΩ ; modèle57,3×44,5×22,6 mm, masse75,5 g typique. Vis entrée#6-32 et sortie#8-32 UNC. VersionK et relaisAC non interchangeables.',
       'https://www.sensata.com/sites/default/files/a/sensata-1-dc-series-d1d-dc-output-panel-mount-datasheet.pdf')]
    for folder,title,role,facts,url in components:
        write(folder+'/README.md',f'# {title}\n\n**Choix préliminaire du13 octobre2026, non acheté et non testé.**\n\n{role}\n\n{facts}\n\n[Architecture et limites](../integration.md), [recherche et avis](../recherche-technique.md), [notice PDF du projet](../notices/notice-protection-batterie-v3.pdf), [notices originales](notices/README.md), [STEP et aperçu](3D/README.md), [sources structurées](sources.json).\n\n[Référence constructeur]({url}).\n')
        manifest=json.loads((BASE/folder/'assets.json').read_text(encoding='utf-8'))
        notices=[a for a in manifest['assets'] if a['file'].startswith('notices/') and 'sha256' in a]
        lines=['# Fiches et plans originaux','','Fichiers conservés sans modification ; origine et SHA256 dans [assets.json](../assets.json).','']
        lines += [f'- [{Path(a["file"]).name}]({Path(a["file"]).name}) - [origine]({a["url"]}).' for a in notices]
        if folder=='coupure-moteurs':lines += ['','La fiche est un document Sensata original hébergé par Farnell. Le téléchargement direct Sensata a renvoyé403 ; aucun contenu du PDF n’a été réécrit.']
        write(folder+'/notices/README.md','\n'.join(lines))
        write(folder+'/sources.json',json.dumps(dict(selected_on='2026-10-13',title=title,primary_source=url,
            purchased=False,hardware_measured=False,hardware_tested=False,manufacturing_ready=False,
            is_custom_design=folder=='surveillance-2s',amazon=dict(asin=None,france_offer_verified=False,price_eur=None,stock=None),
            assets='assets.json',CAD='3D/provenance.json',integration='../integration.md'),ensure_ascii=False,indent=2))
    bom=[
      dict(ref='U1,U2',part='TLV6700DDCR',quantity=2,role='Deux comparateurs locaux par cellule'),
      dict(ref='OP1-OP4',part='VOS618A-8T',quantity=4,role='WARN et HEALTHY de chaque cellule; bin CTR130-260 %'),
      dict(ref='U3',part='SN74LVC2G17DCKR',quantity=1,role='Deux tampons non inverseurs pour OFF'),
      dict(ref='U4',part='MCP1703AT-3302E/MB',quantity=1,role='SOT-89;3,3 V auxiliaire depuis batterie; pas alimentation du Pi'),
      dict(ref='D1-D3',part='BAT54-7-F',quantity=3,role='OU de commandes OFF; cathodes communes'),
      dict(ref='R_mesure',part='40,2k x4 /75k x2 /10k x4, 0,1 %',quantity=10,role='Deux ponts de seuil par cellule'),
      dict(ref='R_LED',part='1,5k,1 %',quantity=4,role='Courant LED optocoupleurs'),
      dict(ref='R_pull',part='47k x4 /100k x1',quantity=5,role='Collecteurs et OFF; valeurs àqualifier'),
      dict(ref='C_mesure',part='100nF',quantity=4,role='Filtrage entrées'),
      dict(ref='C_decouplage',part='100nF',quantity=3,role='TLVx2 et logique'),
      dict(ref='C_LDO',part='1uF x2, type selon datasheet',quantity=2,role='MCP entrée/sortie'),
      dict(ref='J1,J2',part='XH3 voies, header6 voies; références àarrêter',quantity=2,role='Mesure et logique; cotes CAO estimées'),
      dict(ref='SW1',part='Pololu2813 HP',quantity=1,role='Puissance branche Pi uniquement'),
      dict(ref='SSR1',part='Sensata/CrydomD1D100',quantity=1,role='Puissance deux ESC; refroidissement requis'),
      dict(ref='HS1',part='Sensata/Crydom HS251',quantity=1,role="Refroidissement du relais; enveloppe 40 A / 40 °C d'étude, non testée",documentation='../dissipateur-relais/README.md'),
      dict(ref='TIM1',part='Sensata/Crydom HSP-1; variante selon lot reçu',quantity=1,role='Une seule interface thermique, sans empilage de variantes')]
    write('nomenclature.json',json.dumps(dict(status='preliminary; no validated purchasing basket',items=bom,
      not_included_yet=['qualification thermique dissipateur HS251 et interface reçue','fusibles,TVS/diodes de suppression adaptés','faisceau,PCB et entretoises','schéma détaillé,ERC/DRC et routage'],total_price_eur=None),ensure_ascii=False,indent=2))
    write('notices/README.md','''# Documentation de projet

[Notice de l’étude V3](notice-protection-batterie-v3.pdf). Cette notice est rédigée pour le projet ; elle ne remplace pas les fiches TI, Vishay, Microchip, Diodes, Pololu ou Sensata.

Les originaux sont dans les sous-dossiers `notices` de chaque partie. Les pages, variantes et limites sont citées dans la notice. La carte3D reste une étude d’implantation, sans Gerber et sans fabrication autorisée par ce seul modèle.
''')
    print('Documents ready; thresholds:',calc['warning']['falling_typical_V'],calc['hard_cut']['falling_typical_V'])

if __name__=='__main__':main()
