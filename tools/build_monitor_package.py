"""Reproducible engineering dossier for the module-based 2S monitor, revision M1.

No measurements, purchase, production approval or vendor CAD are implied.
"""
from pathlib import Path
import csv, hashlib, itertools, json, shutil, sys

ROOT=Path(__file__).resolve().parents[1]
B=ROOT/'Composants/carte-surveillance-electrique'

def write(rel,text):
    p=B/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.strip()+'\n',encoding='utf-8')
def js(rel,data):write(rel,json.dumps(data,ensure_ascii=False,indent=2))

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if (B/'selection.json').exists() and json.loads((B/'selection.json').read_text(encoding='utf-8')).get('revision')=='M1P':
        raise SystemExit('Historical M1 builder: do not overwrite M1P. Use prepare_monitor_prototype.py and the dedicated KiCad/STEP/PDF builders.')
    for x in ['KiCad','3D','notices','modules','references','logiciel','verification']: (B/x).mkdir(parents=True,exist_ok=True)
    old=ROOT/'Composants/protection-batterie/surveillance-2s'
    assets=[]
    for f in ['Vishay-VOS618A-datasheet.pdf','Microchip-MCP1703A-datasheet.pdf','TI-SN74LVC2G17-datasheet.pdf','Diodes-BAT54-datasheet.pdf']:
        src=old/'notices'/f;dst=B/'notices'/f;shutil.copy2(src,dst)
        assets.append(dict(file='notices/'+f,copied_from=str(src.relative_to(ROOT)),sha256=hashlib.sha256(dst.read_bytes()).hexdigest(),modified=False))
    for src in (ROOT/'Composants/verification-alimentation/notices').glob('Littelfuse-KLKD-2021*'):
        dst=B/'notices'/src.name;shutil.copy2(src,dst)
        assets.append(dict(file='notices/'+src.name,copied_from=str(src.relative_to(ROOT)),sha256=hashlib.sha256(dst.read_bytes()).hexdigest(),modified=False))
    js('assets-reutilises.json',assets)
    # Solve the two loaded divider nodes; biases at BOTH comparator inputs matter.
    rows=[]
    for label,idx,bottom in [('hard',0,10634),('warning',1,10000)]:
        vals=[]
        for a,b,c,v,ia,ib in itertools.product([.999,1.001],[.999,1.001],[.999,1.001],[.387,.400],[-25e-9,25e-9],[-15e-9,15e-9]):
            r1,r2,r3=79600*a,634*b,10000*c
            g11,g22,g12=1/r1+1/r2,1/r2+1/r3,-1/r2
            det=g11*g22-g12*g12
            k=[g22/r1/det,-g12/r1/det][idx]
            off=[(-g22*ia+g12*ib)/det,(g12*ia-g11*ib)/det][idx]
            vals.append((v-off)/k)
        rows.append(dict(function=label,falling_nominal_V=.3945*90234/bottom,rising_nominal_V=.400*90234/bottom,
                         falling_corner_min_V=min(vals),falling_corner_max_V=max(vals),
                         with_sense_network_conservative_min_V=min(vals)-.017,with_sense_network_conservative_max_V=max(vals)+.017))
    js('calculs.json',dict(revision='M1',date='2026-10-15',hardware_tested=False,
        divider=dict(R1_ohm=79600,R2_ohm=634,R3_ohm=10000,tolerance=.001,input_bias_A_nA=25,input_bias_B_nA=15,
                     equation='Va=(R2+R3)/Rtotal*Vcell; Vb=R3/Rtotal*Vcell; corners solve both input bias currents',
                     note='Use VIT- 387..400 mV from TPS3700 Rev G, not only 1% positive threshold accuracy.'),thresholds=rows,
        sense_protection=dict(ohm_per_wire=100,count=3,part='AC03000001000JAC00',rated_W=3,
          current_at8_4V_with90ohm_mA=8.4/90*1000,power_at8_4V_with90ohm_W=8.4**2/90,
          normal_divider_current_max_uA=4.2/(90234*.999)*1e6,conservative_measurement_error_V=.017,
          assumptions='One resistor at pack end in EACH B0/B1/B2 conductor; no other circuit on protected balance connector; 90..110 ohm thermal allowance, 120 ohm effective measurement path bound including leads; unprotected stubs mechanically enclosed; resistor not fuse.'),
        power=dict(traco_no_load_typical_mA_at5V_each=40,independent_5V_typical_no_load_W=.4,
          study_allowance_battery_W=.7,energy_for45min_Wh=.525,fraction_of37Wh_percent=.525/37*100,
          warning='Allowance is not measured power or runtime guarantee. Disconnect pack AND balance for storage.'),
        OFF=dict(input_network_ohm=10000,high_threshold_V=1,buffer_supply_V=3.3,diode_OR=True,
                 qualification='Strong buffer, not a 47k pullup driving OFF directly; measure OFF and restart inhibition.')))
    items=[
      dict(ref='M1,M2',part='TPS3700EVM-114',quantity=2,role='Comparateur de fenêtre, une carte par cellule',url='https://www.ti.com/tool/TPS3700EVM-114',price=None,currency=None,availability='Référence active, état réel du stock TI masqué/ambigu sans connexion ; à confirmer avant commande'),
      dict(ref='M3,M4',part='TMR 1-0511',quantity=2,role='DC/DC isolé régulé 5 V, 200 mA',url='https://fr.rs-online.com/web/p/convertisseurs-dc-dc/7813178',price=9.28,currency='EUR_HT',availability='9,28 EUR HT affichés dans catalogue RS ; page exacte non archivée (403), panier à revalider'),
      dict(ref='M5',part='Pololu D24V10F5 / 2831',quantity=1,role='5 V auxiliaire avant les deux TMR, sans liaison au 5 V Pi',url='https://www.pololu.com/product/2831',price=12.95,currency='USD',availability='Actif, commandes différées possibles ; stock immédiat non garanti'),
      dict(ref='U1-U4',part='VOS618A-8T',quantity=4,role='Isolation des quatre états de tension',url='https://www.vishay.com/docs/83465/vos618a.pdf'),
      dict(ref='U5',part='SN74LVC2G17DCKR',quantity=1,role='Deux tampons Schmitt non inverseurs vers OFF',url='https://www.ti.com/product/SN74LVC2G17'),
      dict(ref='U6',part='MCP1703AT-3302E/MB',quantity=1,role='3,3 V indépendant, entrée AUX protégée',url='https://www.microchip.com/en-us/product/MCP1703A'),
      dict(ref='D1-D3',part='BAT54-7-F',quantity=3,role='OU des deux défauts matériels et de DONE',url='https://www.diodes.com/datasheet/download/BAT54.pdf'),
      dict(ref='RA0,RA1,RA2',part='AC03000001000JAC00',quantity=3,role='100 ohms / 3 W / 5 %, au départ des trois fils de mesure',url='https://www.vishay.com/en/product/28730/'),
      dict(ref='M1.R1,M2.R1',part='TNPW060379K6BEEA',quantity=2,role='79,6 kohms / 0,1 %, remplacement sur EVM',url='https://www.vishay.com/docs/28758/tnpw_e3.pdf'),
      dict(ref='M1.R2,M2.R2',part='TNPW0603634RBEEA',quantity=2,role='634 ohms / 0,1 %, remplacement sur EVM',url='https://www.vishay.com/docs/28758/tnpw_e3.pdf'),
      dict(ref='M1.R3,M2.R3',part='TNPW060310K0BEEA',quantity=2,role='10 kohms / 0,1 %, remplacement sur EVM',url='https://www.vishay.com/docs/28758/tnpw_e3.pdf'),
      dict(ref='FAUX',part='KLKD001.T',quantity=1,role='Fusible auxiliaire 1 A, à la dérivation après F0 et avant ED80',url='https://www.littelfuse.com/assetdocs/klkd-datasheet?assetguid=7b52eebb-c7cc-43df-a8da-9682a338e0f6'),
      dict(ref='HFAUX',part='L60030M1PQ + SPL001',quantity=1,role='Support et écran auxiliaire ; transition 14/12 AWG vers 22 AWG par WAGO 221-413',url='../supports-branches-rapides/README.md'),
    ]
    js('selection.json',dict(revision='M1',selected_on='2026-10-15',purchased=False,hardware_tested=False,
        manufacturing_ready=False,existing_modules_count=5,additional_microcontroller=False,items=items,
        scope='Deux seuils par cellule, alertes logiques Pi et demande OFF indépendante. Pas de courant, température ou pourcentage de charge mesurés.',
        previous_design='../protection-batterie/surveillance-2s/README.md',carrier_mm=[140,75,1.6],reserved_assembly_mm=[140,75,30],
        EVM_dimensions_status='Enveloppes de réservation 60 x 60 x 12 mm, pas des cotes TI certifiées. Gerbers TI publics référencés, téléchargement refusé 401. Contrôle réel requis.',
        amazon=dict(exact_fr_offer_verified=False,asin=None,price=None)))
    write('README.md', '''# Carte de surveillance électrique 2S - M1

15 octobre 2026. **Dossier de conception de prototype, non acheté, non fabriqué, non testé.**

Choix : **deux Texas Instruments TPS3700EVM-114**, alimentés par **deux Traco TMR 1-0511 isolés**, et un **Pololu D24V10F5 2831** pour leur 5 V auxiliaire. Le Raspberry Pi 5 reste la seule carte de commande. Une carte porteuse regroupe alimentation, optocoupleurs, logique OFF et connecteurs ; elle ne porte aucun courant moteur ou courant d'alimentation du Pi.

Les modules TI existent déjà, avec schéma et routage constructeur. Ils ne sont pas prêts à brancher sur une LiPo 2S : remplacer R1/R2/R3 sur chaque module, régler les cavaliers et réaliser les liaisons indiquées. Ce compromis évite de redessiner les comparateurs et les convertisseurs, tout en gardant une protection par cellule indépendante de Linux. Coût et volume sont supérieurs au premier concept entièrement intégré.

| Livrable | Accès |
| --- | --- |
| Architecture, raccordements et limites | [Intégration](integration.md) |
| Adaptation exacte des modules | [Réglages](modules/configuration.md) |
| Notice illustrée | [PDF](notices/notice-carte-surveillance-v3.pdf) |
| Schéma et routage éditables | [Projet KiCad](KiCad/README.md) |
| Modèles STEP, provenance et réservations | [CAO](3D/README.md) |
| Sources, achats, avis et devis | [Recherche](recherche-et-devis.md) |
| Calculs et hypothèses | [JSON](calculs.json) |
| Nomenclature | [Sélection](selection.json), [CSV porteuse](KiCad/nomenclature.csv) |
| Procédure de vérification | [Essais](verification/essais.md) |

**Avertissement typique 3,560 V/cellule ; coupure typique 3,347 V/cellule.** Les tolérances et l'hystérésis sont calculées séparément. Un intervalle de tension ne garantit pas un délai d'extinction Linux. WARN est maintenant **actif à l'état haut** : sous-tension ou perte du signal lumineux. L'ancien dossier TLV6700 reste une archive et ne doit plus définir le câblage actif.

Carte porteuse : **140 x 75 x 1,6 mm**. Réservation globale : **140 x 75 x 30 mm**, hors fiches et courbures de câble. Les EVM sont représentés par des gabarits conservateurs de 60 x 60 mm ; leurs dimensions exactes et leurs supports restent à confirmer. Cette réservation sert au travail d'implantation, pas à percer le châssis définitif.

La protection auxiliaire FAUX et les trois résistances au départ de l'équilibrage font partie de l'ensemble. **La prise d'équilibrage protégée est réservée à la surveillance ; jamais au chargeur.** Les confirmations de coordination DC de l'audit alimentation R2 restent ouvertes. Lire les conditions avant toute fabrication ou mise sous tension.
''')
    write('modules/configuration.md','''# Adaptation des modules existants

## M1 et M2 - TPS3700EVM-114

La référence retenue est l'EVM-114 en SOT-23, pas l'EVM-202 WSON. Schéma TI SLVU683A, figure 6 p.7 et nomenclature p.8. Le manuel décrit une fenêtre d'usine autour de 12 V, impropre à notre usage sans modification.

| Élément de chaque EVM | Configuration M1 |
| --- | --- |
| R1 d'usine 2,21 Mohms | Remplacer par 79,6 kohms, 0603, 0,1 % |
| R2 d'usine 13,7 kohms | Remplacer par 634 ohms, 0603, 0,1 % |
| R3 d'usine 69,8 kohms | Remplacer par 10,0 kohms, 0603, 0,1 % |
| R4 et R5 | Conserver 100 kohms selon schéma et BOM ; contrôler la carte reçue (texte OUTB du manuel mentionne aussi 10 kohms) |
| R6 | Non monté ; ne jamais réunir les deux sorties |
| J10 | Cavalier 1-2 : **MONITOR SENSE** |
| J11 | Cavalier 1-2 : **VPU = VDD local isolé** |
| J1 VDD | 5 V isolé de M3 ou M4 |
| J2/J4/J6/J8 GND | Référence locale de la cellule ; aucune liaison directe à D- |
| J3 SENSE | B1_R pour M1 ; B2_R pour M2 |
| J5 OUTA | HARD_A1 / HARD_A2 : bas sous le seuil dur |
| J7 OUTB | WARN_B1 / WARN_B2 : bas au-dessus du seuil d'avertissement |
| J9 VEXT | Libre |

Chaque connecteur J1-J9 comporte deux broches déjà communes entre elles pour le même signal (schéma TI). Une seule suffit par liaison ; ce ne sont pas des paires signal/masse. Le câble de porteuse J3/J4 définit son propre ordre : **1 = ISO5, 2 = REF, 3 = SENSE, 4 = OUTA, 5 = OUTB**. Il ne se branche pas directement dans une rangée de l'EVM : cinq fils repérés vont aux connecteurs TI correspondants.

L'entrée INA+ est le nœud R1/R2 ; INB- est le nœud R2/R3. Conserver cette topologie en chaîne, sans inversion. OUTA court-circuite la LED HEALTHY à l'état bas ; OUTB allume la LED WARN_OK à l'état bas. Toutes les LED et remontées des EVM sont alimentées par le 5 V isolé, jamais par un GPIO.

Ces six remplacements de résistances nécessitent une reprise CMS 0603. Nettoyer et contrôler les valeurs ainsi que l'absence de ponts sous microscope. Aucun Gerber de TI n'est modifié ou revendiqué comme fichier propriétaire du projet.

## M3/M4 - Traco TMR 1-0511

Entrée 4,5-9 V, sortie régulée 5 V / 200 mA, sans charge minimale. **Entrée depuis le 5 V MON du Pololu**, pas directement depuis le pack : la faible marge entre 8,4 et 9 V ne suffit pas à absorber les transitoires moteur. Pins : 1 = -VIN, 2 = +VIN, 4 = +VOUT, 6 = -VOUT, aucune broche 5 sur le modèle à sortie simple. Respecter la vue de référence du plan ; pas de variante à sorties doubles.

Corps nominal 17 x 7,62 x 11 mm. Le plan constructeur demande d'éviter les pistes sous le convertisseur. Le routage conserve donc une zone sans piste sous le corps, avec sorties des pastilles vers l'extérieur. L'isolement fonctionnel empêche la masse du Pi de devenir un retour d'équilibrage ; il ne fait pas de la carte une protection de sécurité certifiée.

TRACO recommande un fusible lent 500 mA pour les modèles d'entrée 5 V, tout en demandant d'évaluer le besoin dans l'application finale. Le prototype prévoit deux emplacements de fusibles lents 500 mA en série avec les entrées TMR ; référence de base 0454.500MR (NANO2 CMS 2410, 125 V DC / 50 A), courbes à vérifier dans la nomenclature KiCad avant fabrication. FAUX 1 A protège le départ batterie et ne vaut pas validation de leur coordination.

## M5 - Pololu 2831 D24V10F5

Entrée AUX protégée, GND D-, sortie 5V_MON réservée aux TMR. Ne pas confondre avec le régulateur principal Pi D42V55F5. Employer les connexions repérées VIN/GND/VOUT par fils courts ; la liaison J5 de la porteuse est un connecteur de faisceau, pas l'empreinte directe du module. SHDN et PG restent libres. La référence 2830 est la variante 3,3 V et ne convient pas ici.
''')
    write('integration.md','''# Intégration électrique - surveillance M1

## Source indépendante

Positif **après F0 JLLN050.T, avant ED80** -> FAUX KLKD001.T / 1 A près de la dérivation -> AUX de J1. Retour J1 vers D-. Support FAUX proposé L60030M1PQ + écran SPL001, même famille que les protections R2 ; ses bornes n'acceptent pas directement le fil 22 AWG. Utiliser une courte liaison 12 ou 14 AWG admise au support, puis une WAGO 221-413 pour le départ 22 AWG. Un fil par borne. La qualification DC support/fusible et l'énergie de coupure à 8,4 V restent à obtenir ; aucun résultat antérieur n'est transformé en validation matérielle.

M5 fournit le 5V_MON des deux DC/DC isolés. Le MCP1703A fournit séparément le 3V3_AUX à la logique OFF, directement depuis AUX. Ainsi une panne de M5 ou d'un TMR éteint les optocoupleurs HEALTHY et demande OFF tant que le 3V3_AUX est présent. La perte commune d'AUX, du LDO ou du retour D- **n'est pas garantie de provoquer OFF**. Ce montage n'est pas une chaîne de sécurité certifiée ni un arrêt d'urgence.

## Équilibrage : mesure seulement

Au plus près de la sortie du pack, intercaler **100 ohms / 3 W dans chacun des trois fils B0, B1, B2**. Aucune portion longue de fil fin non protégée en amont ; les petits tronçons restant avant résistances doivent être séparés et enfermés mécaniquement. La fabrication du pack n'est pas modifiée. Cette terminaison est une pièce de faisceau à fabriquer, repérée SURVEILLANCE UNIQUEMENT. Ne pas étouffer thermiquement les corps de résistances sous une gaine groupée : prévoir leur fixation et ventilation hors contact de la LiPo. Leur thermique en défaut est à tester.

J2 : **1 B0_R, 2 B1_R, 3 B2_R**. REF1 = B0_R ; SENSE1 = B1_R. REF2 = B1_R ; SENSE2 = B2_R. Les résistances limitent un défaut situé en aval à moins de 94 mA dans le scénario conservateur 8,4 V / 90 ohms, avec moins de 0,79 W dans une résistance. Elles ne sont pas des fusibles et ne déconnectent pas le défaut. Aucun courant d'alimentation Pi, moteur, servo ou LED opto ne circule dans ces trois fils. La prise de charge 2S reste directe et distincte ; ne jamais utiliser cette dérivation résistive pour la charge ou l'équilibrage S65.

Une perte du point milieu B1 peut répartir artificiellement la tension entre les deux réseaux : **la détection certaine de fil ouvert n'est pas fournie**. Contrôle des trois tensions au branchement et maintien du connecteur requis. Une future détection active de fils ouverts demanderait une autre architecture.

## Interface du Pi et OFF

J6 : 1 = 3V3_PI (pin physique 1), 2 = WARN1 (GPIO17/pin11), 3 = WARN2 (GPIO27/pin13), 4 = DONE (GPIO22/pin15), 5 = GND (D-, point système existant). Le signal GND de surveillance utilise une dérivation du retour de référence existant ; ne pas prendre B0_R comme masse.

WARN1/2 sont **hauts en avertissement**, y compris en perte d'alimentation locale ; bas lorsque la cellule est au-dessus du seuil de retour. Rappels 47 kohms au 3,3 V du Pi seulement. Aucune remontée 5 V ou 3V3_AUX sur un GPIO. La perte d'un câble WARN reste un défaut lisible si le rappel est conservé côté Pi : placer les deux 47 kohms au plus près du connecteur GPIO côté Pi, et non uniquement à l'autre extrémité du câble. La porteuse comporte des emplacements marqués DNP pour les rappels WARN ; voir nomenclature de montage.

HEALTHY1/2 utilisent des optocoupleurs distincts et deux rappels 47 kohms au 3V3_AUX. Une LED HEALTHY éteinte remonte une entrée Schmitt ; sa sortie demande OFF par BAT54. DONE rejoint OFF par sa propre BAT54, avec rappel 100 kohms à GND. J7 : 1 OFF, 2 GND -> OFF/GND Pololu 2813. Aucune connexion à ON/CTRL. Le Pololu 2813 ne porte toujours pas le courant moteur ; VSW commande son régulateur Pi et l'entrée du D1D100 selon l'alimentation R2.

Le faisceau GPIO garde ses 13 contacts. Pas d'I2C, pas de SPI, pas d'ADC numérique : le Pi reçoit des **états de seuils**, pas une tension en volts, une intensité, une température ou un pourcentage de charge.

## Séquence et logiciel restant

1. Contrôle au voltmètre des deux cellules et de la polarité ; brancher la surveillance, puis mise sous tension manuelle.
2. Attendre des états cohérents et le neutre ESC ; ne pas armer au démarrage si WARN est haut ou flottant.
3. WARN haut maintenu selon un filtrage logiciel à définir après essais : arrêt des moteurs, arrêt de la vidéo/enregistrement, demande d'extinction Linux.
4. GPIO22 devient haut à la fin de poweroff et demande OFF. Si le seuil dur est atteint avant, la logique analogique demande OFF sans attendre Linux.
5. Le réarmement reste manuel et doit être inhibé tant qu'une cellule est trop basse ; tester le bouton Pololu pendant un défaut maintenu.

La documentation des overlays Raspberry Pi propose gpio-poweroff ; sa disponibilité et sa séquence Pi 5/OS doivent être vérifiées sur le système choisi. Aucun overlay n'est appliqué et aucun service d'arrêt n'est déployé. Le dossier logiciel décrit le contrat, pas un arrêt système testé.

**Débrancher la batterie principale ET l'équilibrage pour le stockage.** Les DC/DC consomment chacun typiquement 40 mA à vide sous 5 V, même après l'arrêt du Pi. L'étude réserve 0,7 W de puissance pack pour l'ensemble, soit environ 0,525 Wh en 45 minutes ; ce budget n'est pas une mesure. Ajouter environ 0,083 à 0,109 A pour 8,4 à 6,4 V aux scénarios de courant R2 qui ne comprenaient pas encore cette nouvelle réalisation. Le courant à vide maximum des TMR et les pertes réelles doivent être mesurés.

C7/C8 sont des 2,2 microfarads X7R / 25 V, afin de laisser de la marge au minimum de 1 microfarad effectif du MCP1703A ; vérifier tolérance, température et polarisation DC. La tenue I²t des pistes auxiliaires, des vias, des fils et des fusibles FAUX/F1/F2 ainsi que les courts-circuits amont/aval du Pololu restent à analyser avec les confirmations R2. Les pistes de 0,20 mm ont un usage de surveillance à faible courant ; le DRC ne garantit pas leur coordination en défaut.
''')
    write('recherche-et-devis.md','''# Recherche, achat, avis et devis - 15 octobre 2026

## Choix et alternatives examinées

TPS3700EVM-114 : schéma, BOM, routage et procédure publics, seuils analogiques autonomes, pas de microcontrôleur. L'adaptation des résistances 0603 est nécessaire ; le module de 12 V n'est pas directement compatible. Les alimentations isolées permettent une mesure des cellules sans retour par D- ni charge des cellules par les optocoupleurs.

INA219 et INA260 : utiles pour des mesures de bus, mais ne donnent pas à eux seuls une protection autonome des deux cellules ; leurs shunts usuels ne conviennent pas au courant commun d'étude. ADS1115 seul : mesure numérique possible, mais pas de chaîne de coupure indépendante complète. MAX17048 : une cellule, pas le pack 2S. BQ76905EVM : vrai moniteur 2-5S, intéressant pour une version avec mesures numériques et détection de fils ouverts, mais reconfiguration des FET/masse et du firmware nécessaire. CellLog 8S : fonctionnalités proches du besoin, offre ProgressiveRC consultée marquée épuisée. Pololu S9V11F3S5CMA : coupure UV existante, mais hystérésis d'environ 14 % et quatre modules pour deux seuils par cellule ; moins adapté aux seuils proches de notre première étude. Aucun BMS 2S générique sans documentation de seuils, de référence de masse et de courant n'est substitué à la chaîne de puissance R2.

## Achat et coût

| Référence | Qté | Prix constaté / état | Achat |
| --- | ---: | --- | --- |
| TPS3700EVM-114 | 2 | Prix et disponibilité France à confirmer ; page TI contient des états de stock contradictoires et demande connexion | [TI](https://www.ti.com/tool/TPS3700EVM-114), [DigiKey France](https://www.digikey.fr/fr/products/detail/texas-instruments/TPS3700EVM-114/3182032) |
| TMR 1-0511 | 2 | 9,28 EUR HT / pièce dans catalogue RS consulté ; 18,56 HT / environ 22,27 TTC à 20 %, hors port | [RS 781-3178](https://fr.rs-online.com/web/p/convertisseurs-dc-dc/7813178), [TME](https://www.tme.eu/fr/details/tmr1-0511/convertisseurs-dc-dc/traco-power/tmr-1-0511/) |
| Pololu 2831 D24V10F5 | 1 | 12,95 USD fabricant ; stock et livraison France non établis, commandes différées possibles | [Pololu](https://www.pololu.com/product/2831) |
| Semi-conducteurs, passifs, connecteurs, FAUX/support, PCB | Selon BOM | Panier distributeur et coût fabrication à chiffrer, aucune valeur inventée | Voir selection.json et nomenclature.csv |

Pas de total TTC global vérifié : monnaies, ports et lignes non chiffrées ne sont pas additionnés artificiellement. Aucun achat effectué. Recherche Amazon.fr sur les références exactes : aucune offre française exacte et vérifiable trouvée. Les modules spécialisés sont proposés chez leurs fabricants/distributeurs, sans inventer d'ASIN. Le devis est donc **partiel**.

## Sources techniques et retours

- [TI EVM](https://www.ti.com/tool/TPS3700EVM-114), [guide SLVU683A](https://www.ti.com/lit/pdf/SLVU683), [fiche TPS3700 Rev G](https://www.ti.com/lit/ds/symlink/tps3700.pdf).
- [TI E2E : réglage R1/R2/R3](https://e2e.ti.com/support/power-management-group/power-management/f/power-management-forum/1540899/tps3700evm-114-r1-r2-r3-value) : réponse TI orientant vers le calculateur de ponts ; pas un essai du robot.
- [TI E2E : limite des sorties](https://e2e.ti.com/support/power-management-group/power-management/f/power-management-forum/1570835/tps3700-higher-output-voltage-will-damage-chip) : ne pas dépasser la plage de sortie du circuit. Ici sorties locales autour de 5 V, isolées du Pi.
- [TRACO TMR 1](https://www.tracopower.com/tmr1-datasheet) : fiche récupérée datée du 2 juillet 2026, pas les anciens résumés des marchands ; courant à vide typique 40 mA par module, brochage p.4 et absence de charge minimale.
- [Pololu 2831](https://www.pololu.com/product/2831), schéma public et caractéristiques du 5 V ±4 %.
- [Vishay AC](https://www.vishay.com/docs/28730/ac_ac-at_ac-ni.pdf), [TNPW](https://www.vishay.com/docs/28758/tnpw_e3.pdf), VOS618A et notices de logique archivées.

Aucun avis utilisateur ou essai YouTube vérifié sur cet ensemble précis n'a été trouvé. Aucune note ou validation thermique déduite de retours d'un autre module. Les fichiers assets*.json indiquent les téléchargements réussis, empreintes et erreurs. Le ZIP Gerber TI SLVC413 a renvoyé HTTP 401 ; les vues de routage du PDF restent disponibles, mais aucune dimension exacte d'EVM n'en est certifiée.
''')
    write('verification/essais.md','''# Vérification avant fabrication, alimentation puis roulage

La validation de fichiers ne vaut pas validation du circuit réel.

1. Avant commande : disponibilité des références, réception et dimensions exactes des EVM ; pas et ordre des connecteurs, boîtiers, fusibles 500 mA, empreintes et supports. Résoudre les points fabricant de l'audit R2, en particulier tenue DC et énergie de coupure de FAUX/support. Valider le choix des fusibles TMR et la réaction de M5 à un court-circuit.
2. Revue du schéma : distinction AUX/D-/B0_R/B1_R/B2_R/ISO5 ; ordre physique de chaque faisceau ; aucune alimentation GPIO depuis le secondaire ou 3V3_AUX. Comparer la netlist exportée au contrat de connexions, ERC et DRC natifs. Contrôler la règle sans piste sous les TMR. Les cavaliers et changements sur les EVM doivent être vérifiés séparément du DRC porteuse.
3. Banc limité en courant, sans batterie ni moteurs : deux simulateurs de cellules flottants en série, source AUX indépendante. Tester seuils de chaque cellule en montée et descente, cellule déséquilibrée, chute brusque et lente, temps de réponse et courant de mesure. Vérifier la polarité WARN active haute et la logique LED HEALTHY shuntée par OUTA. Confirmer la marge de CTR, les températures et les niveaux OFF.
4. Défauts : débrancher chaque alimentation/module/opto, chaque fil B0/B1/B2, câble WARN et DONE ; observer et documenter les défauts non détectés, notamment point milieu ouvert et perte commune d'AUX/LDO. Tester le maintien de coupure pendant appuis bouton et le retour des tensions après coupure. Pas de promesse de comportement sûr pour toutes les pannes.
5. Protection de mesure : essayer 8,4 V limités en courant sur le défaut représentatif de chaque résistance 100 ohms, mesurer son échauffement stabilisé et celui des isolants environnants. Vérifier dissipation et montage au voisinage du pack. Ne pas court-circuiter une vraie LiPo pour cet essai. Aucun résultat matériel produit à ce stade.
6. Pi 5 : vérifier WARN au démarrage, arrêt demandé avec vidéo/Wi-Fi actifs, GPIO22 à poweroff, reboot, Pi figé et Pi non alimenté. Mesurer absence de retour de courant sur GPIO hors tension. Développer et tester le service d'arrêt avant autonomie.
7. Puis seulement essais avec puissance moteur progressive : transitoires et freinage, état de la source AUX, température, parasites, cohérence des seuils et arrêt complet. Les relais, fusibles principaux et chutes de câbles suivent toujours les conditions R2.

La prochaine étape mécanique est le support caméra, puis les supports des capteurs, le châssis et enfin la visserie finale. Les fixations de la carte devront conserver l'accès aux cavaliers et aux connecteurs et ne pas fermer les zones isolées par des entretoises métalliques.
''')
    write('logiciel/contrat-interface.md','''# Contrat GPIO M1 - logiciel non déployé

GPIO17 et GPIO27 : entrées, rappels externes 47 kohms au 3,3 V du Pi côté Pi ; bas = état au-dessus du seuil de retour, haut = avertissement/perte de lumière. L'ancien concept était actif bas : inverser explicitement le traitement avant usage. Démarrer avec la propulsion inhibée.

GPIO22 : sortie inactive basse pendant fonctionnement ; haute en fin de poweroff via diode vers OFF. Base de configuration officielle à vérifier pour Pi 5 et OS choisi : `dtoverlay=gpio-poweroff,gpiopin=22`. Ne pas l'activer sans banc ; les effets sur reboot et remise en marche doivent être vérifiés. Aucune écriture sur un Pi n'a été effectuée.

Le service de supervision devra utiliser l'API GPIO compatible Pi 5, détecter une entrée haute, interdire l'accélération, arrêter vidéo et fichiers, puis demander poweroff. Anti-parasitage et temporisation doivent suivre les mesures de banc ; un retard logiciel n'agit jamais sur la coupure analogique dure. Pas de tension numérique ni de pourcentage de charge fourni par ces deux entrées.
''')
    print('Wrote M1 dossier and calculations; KiCad/CAD/PDF produced by dedicated builders.')

if __name__=='__main__':main()
