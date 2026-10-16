"""M1P: engineering calculations, build conditions, bounded bench protocol.

No hardware results are produced. Vendor dimensions absent from the source
remain unknown; calibrated PDF geometry is explicitly an estimate.
"""
from pathlib import Path
import csv, hashlib, json, math, statistics, sys
import pymupdf

ROOT=Path(__file__).resolve().parents[1]
B=ROOT/'Composants/carte-surveillance-electrique'
Q=B/'verification'

def write(path,s):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(s.strip()+'\n',encoding='utf-8')

def dump(path,obj):write(path,json.dumps(obj,ensure_ascii=False,indent=2))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def dimensions():
    source=B/'notices/TI-TPS3700EVM-114-original.pdf'
    page=pymupdf.open(source)[4]
    draws=page.get_drawings()
    byid={d['seqno']:d for d in draws}
    outline=byid[1]['rect']
    center=lambda i:((byid[i]['rect'].x0+byid[i]['rect'].x1)/2,(byid[i]['rect'].y0+byid[i]['rect'].y1)/2)
    pairs=[(203,205),(207,209),(211,213),(215,217),(219,221),(223,225),(227,229),(231,233),(235,237),(237,239),(261,263),(265,267),(267,269)]
    scales=[2.54/math.dist(center(i),center(j)) for i,j in pairs]
    scale=statistics.median(scales)
    result=dict(part='TPS3700EVM-114 / PWR114 A',date='2026-10-15',source=str(source.relative_to(B)).replace('\\','/'),sha256=sha(source),page=5,
        method='Vector drawing, Fig 4, calibrated against thirteen 2.54 mm header pitches from TI BOM p8. Not an exact manufacturer mechanical drawing.',
        exact_documented=dict(header_pitch_mm=2.54,header_2pin_part='PEC02SAAN',header_3pin_part='PEC03SAAN'),
        inferred_NOT_certified=dict(board_xy_mm=[outline.width*scale,outline.height*scale],scale_mm_per_pdf_point=scale,scale_spread_relative=(max(scales)-min(scales))/scale,pitch_samples=len(pairs),
          drawing_tolerance_unknown=True,thickness_mm=None,maximum_assembled_height_mm=None,mounting_holes_mm=None),
        design_reservation_mm=[60,60,12],native_gerbers_available=False,exact_vendor_board_dimensions_verified=False,
        conclusion='Only connector pitch is exactly specified. Inferred outline about 51.05 x 48.26 mm is NOT a drilling or manufacturing datum. Keep 60 x 60 x 12 reservation; no module mounting holes invented. Modules on separate insulated bench stands, flying harnesses.')
    dump(B/'modules/cotes-ti.json',result)
    clip=pymupdf.Rect(185,340,425,568)
    page.get_pixmap(matrix=pymupdf.Matrix(3,3),clip=clip).save(B/'modules/TI-vue-routage-originale-page5.png')
    write(B/'modules/cotes-ti.md',f'''# Relevé des cotes TI - source et limite

**Les cotes exactes du contour, de l'épaisseur et de la hauteur assemblée ne sont pas publiées dans le guide accessible.** Les téléchargements publics SLVC413 renvoient HTTP 401. Le [registre](TI-SLVC413/tentatives-publiques.json) conserve les tentatives. Aucune connexion à un compte, commande ou demande au fabricant n'a été faite.

Le guide TI SLVU683A contient des vues vectorielles, utilisables pour contrôler le gabarit : treize entraxes de broches sont étalonnés au pas **2,54 mm**, donné explicitement dans la nomenclature TI p.8. Le contour dessiné donne **environ {result['inferred_NOT_certified']['board_xy_mm'][0]:.2f} x {result['inferred_NOT_certified']['board_xy_mm'][1]:.2f} mm**. Ce relevé est une **inférence**, sans tolérance de fabrication ; il ne devient pas une cote exacte parce que le calcul affiche plusieurs décimales. [Calcul reproductible](cotes-ti.json), [extrait constructeur](TI-vue-routage-originale-page5.png).

| Grandeur | Valeur utilisable | Origine / statut |
| --- | --- | --- |
| Pas J1-J11 | 2,54 mm | TI BOM p.8, spécifié |
| J1-J9 | 2 broches communes par connecteur | Schéma TI p.7 ; une broche par liaison suffit |
| J10/J11 | 3 broches au pas 2,54 | PEC03SAAN ; cavaliers 1-2 |
| Contour EVM | Environ 51,05 x 48,26 | Relevé du dessin ; non certifié |
| Épaisseur PCB / hauteur équipée | Inconnues exactement | Ne pas imposer 1,6 / 12 mm comme cotes fournisseur |
| Trous de fixation | Aucun entraxe validé | Les petits points de cuivre ne sont pas déclarés trous de montage |
| Enveloppe de conception | 60 x 60 x 12 par EVM | Réservation à confirmer à réception |

**Conséquence pour la fabrication :** J3/J4 de la porteuse sont des départs de câbles ; aucun trou, socle ni empreinte de porteuse ne dépend du contour TI. La porteuse peut être fabriquée seule pour le banc. Les EVM sont posés sur supports isolants séparés pendant les essais. Le support mécanique définitif attend le ZIP natif ou un relevé de la carte reçue ; ne pas percer les EVM.

Source primaire : [TI, guide SLVU683A](https://www.ti.com/lit/pdf/SLVU683), figures 3/4 et BOM. Pour fermer la cote exacte, archiver SLVC413 obtenu normalement depuis TI, extraire contour/perçages en unités natives et contrôler la révision PWR114 A ; à défaut relever largeur, longueur, épaisseur et hauteur maximale de l'exemplaire reçu, avec incertitude de mesure. La cote des connecteurs et de leurs fiches doit aussi être prise en compte.
''')
    return result

def coordination():
    # First-principles adiabatic screen; not an IEC/IPC qualification or fuse model.
    rho_mass=8960;cp=385;rho_e=1.724e-8;alpha=.00393
    start,limit=40,105
    factor=rho_mass*cp/(rho_e*alpha)*math.log((1+alpha*(limit-20))/(1+alpha*(start-20)))*1e-12
    def budget(w,t):return factor*(w*t)**2
    # Minimum barrel section: finished drill diameter 0.40, plating 0.020.
    via_area=math.pi*((.35/2+.020)**2-(.35/2)**2)
    original=budget(.2,.025);new=budget(.35,.055);signal=budget(.175,.055)
    # Bounded test fixture. All assumptions are acceptance requirements, not measurements.
    vmax=8.4;rmin=4.4;cap=470e-6;ccmax=.300;response=.010
    peak=vmax/rmin
    source_i2t=peak**2*response+cap*vmax**2/(2*rmin)
    obj=dict(revision='M1P',hardware_tested=False,vehicle_battery_release=False,
      copper=dict(nominal_um=70,minimum_finished_um=55,power_nominal_width_mm=.4,power_minimum_etched_width_mm=.35,signal_nominal_width_mm=.2,signal_minimum_etched_width_mm=.175,minimum_hole_wall_um=20,via_diameter_mm=.8,via_finished_drill_mm=.4,via_minimum_finished_drill_mm=.35),
      adiabatic_screen=dict(method='Integral of mass_density*cp*dT / rho_e(T), constant cp; section squared; no heat loss, no certified laminate/component model.',initial_C=start,limit_C=limit,
        constants=dict(density_kg_m3=rho_mass,cp_J_kgK=cp,rho20_ohm_m=rho_e,alpha_K_1=alpha),
        previous_trace_I2t_A2s=original,new_power_trace_I2t_A2s=new,new_signal_trace_I2t_A2s=signal,via_wall_I2t_A2s=factor*via_area**2,improvement_factor_power=new/original,
        not_guaranteed=['Manufacturing section and copper properties','Pin necks, pads, module traces and connector contacts','Steady state, solder, laminate and hot spots','Not a certified fuse let-through withstand rating']),
      fuses=dict(part='0454.500MR',nominal_A=.5,nominal_melting_I2t_A2s=.240,melting_is_not_max_total_clearing=True,interrupt_A_at125VDC=50,interrupt_A_at32VDC=300,
        specified_time_points=[dict(current_A=1,minimum_s=1,maximum_s=60,I2t_upper_at_constant_current_A2s=60),dict(current_A=1.5,minimum_s=.2,maximum_s=3,I2t_upper_at_constant_current_A2s=6.75),dict(current_A=4,minimum_s=.002,maximum_s=.1,I2t_upper_at_constant_current_A2s=1.6)],
        source='https://www.littelfuse.com/assetdocs/littelfuse-fuse-452-454-datasheet?assetguid=8c87aa93-80a7-4ea8-8749-a19ba03901c2',
        coordination_proven_for_LiPo=False,reason='No maximum total clearing envelope at actual 2S fault conditions, no guaranteed M5 fault output bound; no selectivity proof. Continuous thermal evidence absent.'),
      bench=dict(AUX_source_max_V=vmax,AUX_CC_setting_A=.250,AUX_CC_accepted_max_A=ccmax,CC_settle_max_s=response,series_resistor_ohm=4.7,series_resistor_min_ohm=rmin,
        resistor_min_rating_W=25,source_output_capacitance_before_resistor_max_F=cap,maximum_initial_limited_current_A=peak,
        screening_I2t_before_CC_settles_A2s=source_i2t,screening_margin_to_power_trace=new/source_i2t,screening_margin_to_signal_trace=signal/source_i2t,steady_resistor_power_W=ccmax**2*4.7*1.05,
        cell_simulator_limit_A=.020,cell_max_V=4.2,Pi_dummy_3V3_source_limit_A=.005,
        scope='Functional bench only, no destructive fault on powered module; no motor, Pi power load, charger or LiPo. Every source current limited. Short-circuit screening applies to AUX input path only, not magically through a switching converter.',
        source_characteristics_must_be_verified=True,hardware_results_exist=False),
      classifications=dict(FAUX='Vehicle branch backup, not a current limiter; still R2 conditions.',F1_F2='TRACO recommended 500mA slow, independent branches; no guaranteed operation on current-limited bench.',RA0_RA1_RA2='Passive current limitation only, not interruption or universal isolation-fault protection.'))
    dump(Q/'coordination-protections.json',obj)
    write(Q/'coordination-protections.md',f'''# Coordination des protections - conclusion M1P

**Fabrication de prototype et essais fonctionnels sur banc borné : préparés. Raccordement direct à la LiPo : non libéré.** Aucun essai réel ni certification de tenue n'est produit. [Calculs et hypothèses](coordination-protections.json).

## Correction de la porteuse

Les pistes d'alimentation passent de **0,20 à 0,40 mm**, les pistes de signaux restent **0,20 mm** pour les circuits à pas fin. Le cuivre spécifié passe de35 supposés à **70 micromètres nominaux, au moins55 micromètres finis**, et les vias de0,60/0,30 à **0,80/0,40 mm**, métallisation des parois **20 micromètres minimum**. Largeurs gravées minimales de calcul : **0,35 mm alimentation /0,175 mm signaux**. Les petites plages gardent leurs empreintes fabricant. Il faut une fabrication avec trous métallisés ; les Gerbers ne sont pas un parcours CNC.

Un calcul adiabatique du cuivre, de40 à105 °C, donne environ **{original:.3f} A²s pour l'ancienne section minimale** contre **{new:.3f} A²s pour l'alimentation**, soit **{new/original:.1f} fois** plus. Les signaux fins ont un critère de **{signal:.3f} A²s**. Il s'agit d'une comparaison de pistes uniformes, pas d'une qualification du PCB complet : tolérances, étranglements, broches, pastilles, composants et régime permanent restent distincts. Pour une durée longue, ignorer les pertes de chaleur surestime l'échauffement ; un dépassement du budget n'est donc pas une preuve de destruction.

## Ce que permettent réellement les fusibles

| Élément | Fonction | Conclusion vérifiée sur documents |
| --- | --- | --- |
| FAUX KLKD001.T / 1 A | Secours de la branche AUX, près de la dérivation | Ne limite pas le courant à 1 A. Support DC / énergie de coupure toujours sous conditions R2. |
| F1/F2 0454.500MR / 500 mA lents | Recommandation TRACO pour chaque entrée 5 V | Choix cohérent avec la recommandation ; coordination complète non prouvée. |
| RA0/RA1/RA2 100 ohms / 3 W | Limitation des trois fils de mesure au départ du pack | Calcul batterie seule : 8,4 / 90 = 93,3 mA ; 0,784 W. Ne couvre pas toutes les pannes d'isolement des sources 5 V. |

La fiche Littelfuse indique **0,240 A²s de fusion nominale**, calculée à 8 ms : ce n'est ni une borne maximale ni l'énergie totale de coupure. Le pouvoir de coupure annoncé est **50 A à 125 V DC et 300 A à 32 V DC**, pas une garantie de sélectivité entre fusibles. À deux fois le calibre (1 A), l'ouverture peut demander jusqu'à 60 s ; à 1,5 A jusqu'à 3 s ; à 4 A jusqu'à 0,1 s. Les deux derniers points donnent respectivement 6,75 et 1,60 A²s à courant constant : l'amélioration du cuivre ne ferme pas à elle seule toutes ces conditions.

M5 annonce une protection contre les courts-circuits, mais son courant « 1 A » est une capacité de sortie, **pas une borne garantie de courant de défaut**. Un court-circuit VIN/VOUT interne contournerait aussi son fonctionnement normal. Ne pas utiliser une limitation supposée du régulateur pour déclarer F1/F2 protégés contre tous les défauts.

## Mode banc retenu pour pouvoir fabriquer puis vérifier

- Source AUX isolée de la LiPo, **8,4 V maximum**, réglage CC **250 mA** ; valeur maximale acceptée 300 mA après10 ms. Ajouter **4,7 ohms / au moins25 W /5 % ou mieux** en série juste à sa sortie. Minimum de calcul **4,4 ohms**, tolérance et température comprises ; respecter la pose et la dissipation du modèle utilisé.
- La réserve capacitive de la source **avant** cette résistance doit être connue et au plus **470 microfarads**. Vérifier ces caractéristiques dans sa documentation ou sur charge fictive, avant de brancher la porteuse ; un bloc secteur ordinaire ne convient pas. Ne pas ajouter de gros condensateur au point J1.
- Avec ces hypothèses, pointe bornée à **{peak:.3f} A** par la résistance ; budget de contrôle entrée AUX **{source_i2t:.4f} A²s** avant CC, avec double comptage conservateur de la réserve capacitive. Marge au critère de piste uniforme environ **{new/source_i2t:.0f}**. Ce calcul ne se transfère pas automatiquement au secondaire du convertisseur M5.
- Deux simulateurs de cellules flottants et limités chacun à **20 mA / 4,2 V**. La source de rappel Pi simulée est limitée à **5 mA / 3,3 V**. Pas de batterie, chargeur, moteurs ou puissance Pi pendant la première campagne. [Câblage et séquence](banc-essais.md).
- Sous courant limité les fusibles peuvent ne jamais fondre : c'est attendu. Ils restent montés ; aucun pont ne les remplace. Les essais de coupure à fort courant de la LiPo sont hors de cette campagne.

## Fermeture pour la version véhicule

Il reste à obtenir une enveloppe maximale d'énergie totale de coupure aux conditions de défaut réelles, à comparer à chaque tronçon/connexion, **ou à ajouter une limitation électronique qualifiée** qui protège même en défaut interne de M5. Une eFuse n'est pas ajoutée au hasard : son état au démarrage, sa programmation, sa limite maximale, sa réponse rapide et son défaut en court-circuit doivent aussi être traités. Le module eFuse 2 Click / TPS259631 a été examiné ; il nécessite une configuration I2C et son stock constructeur est absent à la consultation. Il n'est donc pas déclaré substitut monté/validé.

Les confirmations R2 sur supports et fusibles de puissance restent ouvertes ; leur portée dépasse cette porteuse. Le [registre de libération](liberation-prototype.json) garde les deux états séparés. Le prochain travail mécanique peut employer la réservation 140 x 75 x 30, mais pas une implantation TI définitivement percée.

Sources primaires : [Littelfuse 452/454](https://www.littelfuse.com/assetdocs/littelfuse-fuse-452-454-datasheet?assetguid=8c87aa93-80a7-4ea8-8749-a19ba03901c2), [TRACO TMR1](https://www.tracopower.com/tmr1-datasheet), [Pololu 2831](https://www.pololu.com/product/2831), [Mikroe eFuse 2](https://www.mikroe.com/efuse-2-click). Les valeurs de matériaux dans le calcul sont des hypothèses d'ingénierie explicites ; aucune conformité normative n'en est déduite.
''')
    return obj

def bench():
    write(Q/'banc-essais.md','''# Campagne M1P - procédure prête, résultats à relever

**Réservée au prototype de banc. LiPo, chargeur, moteurs et alimentation de puissance Pi absents.** Ne pas commencer par des courts-circuits du PCB. Toute valeur mesurée est à inscrire dans [resultats-banc.csv](resultats-banc.csv), initialement vide de résultats.

## Matériel et références

Source AUX de laboratoire 0-8,4 V, CC réglée 250 mA, maximum accepté 300 mA après 10 ms, capacité de sortie documentée au plus 470 microfarads ; résistance série 4,7 ohms / au moins 25 W / 5 % au plus. Deux voies de simulation de cellule **galvaniquement isolées, capables d'absorber un petit courant de retour**, réglables 0-4,2 V / 20 mA. Une source 3,3 V / 5 mA pour les rappels Pi. Multimètres, thermocouples et oscilloscope à sonde différentielle adaptée. Un oscilloscope relié à la terre ne doit pas court-circuiter les références de cellules par ses pinces de masse.

Les références des instruments, résistances et limites réellement utilisées sont consignées avant essais. Une alimentation à sorties communes ne devient pas isolée par changement de câbles. Aucune propriété de limite transitoire n'est présumée parce que la façade affiche « 250 mA ».

## Câblage hors tension

1. Pi et Pololu 2813 débranchés. OFF charge fictive 10 kohms vers D-. WARN1/2 rappelés chacun par 47 kohms à la source 3,3 V limitée. DONE au repos bas par R9 ; entrée non laissée reliée à un générateur éteint inconnu.
2. Source AUX + -> résistance série au départ -> J1.1 ; source AUX - -> J1.2 / D-. Départ FAUX du véhicule non branché au banc. F1/F2 500 mA restent montés. M5 reçoit VIN/GND/VOUT via son faisceau J5 repéré.
3. Simulateur C1 : - = B0 ; + = B1. Simulateur C2 : - = B1 ; + = B2. Relier B0 au D- **en amont** de RA0, pour représenter la masse batterie. B0/B1/B2 -> trois RA 100 ohms au départ -> J2.1/2/3. Ne jamais relier B0_R directement à D-.
4. M1/M2 restent sur supports isolants séparés, dans leur réservation. J3/J4 de porteuse : 1 ISO5, 2 REF, 3 SENSE, 4 OUTA, 5 OUTB. Chaque fil va à la broche TI correspondante, pas à cinq broches adjacentes. Vérifier les six remplacements 0603 et cavaliers.
5. Contrôle de continuité point à point hors tension, puis contrôle visuel à la loupe : pas de pont entre références isolées, pas de boîtier ou entretoise métallique reliant les masses. Les résistances de limitation sont présentes avant tout branchement des simulateurs.

## Paliers et critères

| ID | Action | Critère / relevé |
| --- | --- | --- |
| B00 | Instruments sur charge fictive, sans PCB | 8,4 V maximum, CC <=300 mA après10 ms ; résistance >=4,465 ohms à froid et minimum garanti4,4 avec température ; capacité source <=470 microfarads documentée. Sinon arrêt de la campagne. |
| B01 | Hors tension, EVM adaptés | R1 79,6k / R2 634 / R3 10k ; R6 absent ; J10/J11 1-2 ; pins et boîtiers comparés à la BOM. |
| B02 | Source AUX7,4 V avant résistance, EVM/TMR non montés au départ | Relever J1 réellement obtenu,3V3_AUX (objectif3,20-3,40 V),5V_MON (4,80-5,20 V). OFF doit demander coupure ; pas d'échauffement anormal. |
| B03 | Ajouter un TMR, puis l'autre et ses EVM | Entrée de chaque TMR 4,5-5,2 V après démarrage ; éviter le maintien sous 4 V. Si montée non établie dans 100 ms, couper et diagnostiquer. Courant AUX stabilisé <200 mA ; pas de hausse de limite pour masquer un défaut. |
| B04 | Deux cellules simulées à 4,0 V | WARN1/2 <0,4 V ; OFF <0,4 V en régime établi ; relever ISO5_1/2 et courant AUX. |
| B05 | C1 descente 4,0 ->3,1 puis remontée ; C2 à4,0 | WARN haut >2,8 V vers3,560 ; OFF >1,5 V vers3,347 ; seuil dur descente accepté3,258-3,420 ; warning3,466-3,636. Relever retours/hystérésis, délais et absence d'oscillation. |
| B06 | Même séquence sur C2, C1 à4,0 | Mêmes critères ; vérifier que la voie correcte change et que l'autre demeure cohérente. |
| B07 | Faible déséquilibre, rampes lentes et échelons | Établir bruit et temporisation utile ; comparer niveaux aux seuils calculés. Aucun délai d'arrêt Linux garanti. |
| B08 | Couper M5, puis chaque alimentation TMR séparément | WARN haut et OFF >1,5 V tant que 3V3_AUX reste alimenté ; relever délais. Pi absent. |
| B09 | DONE bas puis3,3 V via source limitée | OFF >1,5 V sur DONE haut, courant conforme à la source ; aucun retour depuis AUX vers3V3_PI. |
| B10 | Débrancher WARN1/2 à l'autre bout du câble | WARN haut côté rappel Pi ; tester DONE/câbles séparément. |
| B11 | Ouvrir B0/B1/B2 un à un, sources limitées | Relever tous les états. B1 ouvert peut rester trompeur ; une absence d'alarme n'est pas une réussite de détection de fil ouvert. |
| B12 | Perdre AUX ou D- | Relever l'état ; OFF n'est pas garanti. Aucune conclusion d'arrêt d'urgence. |
| B13 | Endurance fonctionnelle 30 min à4,0 V simulés | Ambiante <=40 °C ; élévation des pistes/connecteurs <=10 °C ; chaque boîtier >=20 °C sous son maximum recommandé ; pas de dérive de tension ou odeur. Consigner températures. |
| B14 | RA seule, hors PCB et pack, sous8,4 V CC150 mA | Réglage de défaut batterie seule, courant <=94 mA siR>=90 ; puissance<=0,784 W ; température de corps et isolants compatibles avec leur spécification et la pose. Pas de court-circuit de LiPo. |

Aux paliers B02/B03, les optos non alimentés doivent demander OFF : ce niveau au démarrage est attendu. Les objectifs3V3/5V de banc ne remplacent pas une analyse complète des tolérances sur toute température. Les bornes de seuils ci-dessus sont celles du calcul de conception ; hors fenêtre, arrêter et diagnostiquer, ne pas ajuster pour masquer une erreur de câblage.

## Après réussite de cette campagne

Enregistrer courbes et relevés, photographier le montage, revoir chaque écart. Brancher ensuite le Pololu 2813 sur une alimentation de banc à charge fictive légère et mesurer OFF réel, réarmement pendant défaut et démarrage : la charge 10 kohms ne remplace pas ce contrôle. Puis le Pi sans moteurs, avec alimentation principale de banc séparée et son 5 V qualifié ; vérifier gpio-poweroff et le service d'arrêt sur l'OS retenu. Les essais GPIO ne sont pas encore implémentés sur une machine réelle.

**La réussite B00-B14 ne libère pas la LiPo ou le roulage.** La coordination de la chaîne véhicule et les transitoires moteur restent une campagne distincte. Ne pas faire un essai destructif d'énergie de court-circuit dans l'atelier avec une LiPo.
''')
    path=Q/'resultats-banc.csv'
    if not path.exists():
        with path.open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.writer(f,delimiter=';');w.writerow(['ID','Date','Instrument / réglage / incertitude','Mesure réelle','Unité','Critère appliqué','Résultat','Observations / trace'])
            for n in range(15):w.writerow([f'B{n:02}','','','','','','NON REALISE',''])

def main():
    sys.stdout.reconfigure(encoding='utf-8');Q.mkdir(exist_ok=True)
    dims=dimensions();calc=coordination();bench()
    s=json.loads((B/'selection.json').read_text(encoding='utf-8'))
    s.update(revision='M1P',manufacturing_ready=False,prototype_fabrication_ready=True,bench_procedure_ready=True,vehicle_battery_release=False,
      EVM_dimensions_status='Pitch 2.54 mm exact from TI BOM; board outline about 51.05 x 48.26 mm inferred from vector drawing, NOT exact. Native Gerbers still 401. Carrier has flying interfaces independent of EVM contour.',
      prototype_scope='Carrier PCB only, two layer industrial plated-hole fabrication, 70um nominal/55um minimum finished copper; bounded bench protocol mandatory; EVMs on separate insulated supports.')
    dump(B/'selection.json',s)
    records=[]
    for p in sorted((B/'notices').glob('*.pdf')):
        if p.name.startswith(('notice-','annexe-')):continue
        records.append(dict(file=str(p.relative_to(B)).replace('\\','/'),bytes=p.stat().st_size,sha256=sha(p),modified=False))
    dump(B/'notices/inventaire-originaux.json',records)
    write(B/'cotes.md','''# Cotes de conception M1P

| Élément | Dimension / preuve |
| --- | --- |
| Porteuse | 140 x 75 x 1,6 mm ; quatre trous Ø3,2 aux coordonnées (4,4), (136,4), (4,71), (136,71), origine coin PCB |
| Fabrication cuivre | 70 micromètres nominaux,55 finis minimum ; alimentation0,40 dessinée /0,35 gravée minimum ; signaux0,20 /0,175 minimum ; vias0,80 / trou fini0,40, paroi20 micromètres minimum |
| EVM TI, connecteurs | Pas exact2,54 mm, TI BOM ; contour environ51,05 x48,26 relevé, sans tolérance ni hauteur certifiées |
| EVM TI, réservation | 60 x60 x12 chacun ; pas un plan fournisseur. Supports séparés au banc ; aucun perçage EVM imposé |
| TMR1-0511 | Corps nominal17 x7,62 x11 ; tolérance corps±0,5 selon notice ; pose à vérifier |
| Pololu2831 | Nominal fabricant18 x13 x3,5 hors connecteurs ; gabarit18 x13 x5,5 |
| Trois AC03 au pack | Corps13 xØ4,8 nominal, pattesØ0,8 ; hors porteuse |
| FAUX extérieur | KLKD001.T /L60030M1PQ +SPL001, hors porteuse et hors réservation ; conditions R2 |

Réservation d'implantation **140 x75 x30 mm** pour porteuse+modules seulement, hors fiches/faisceaux/courbures, FAUX/support et résistances au pack. Les supports définitifs sont à concevoir plus tard ; ne pas convertir un gabarit en cote fournisseur. [Relevé TI traçable](modules/cotes-ti.md) et [conditions de fabrication prototype](fabrication/README.md).
''')
    # Repeated footer links were accidentally appended by the old finishing script.
    p=B/'README.md';t=p.read_text(encoding='utf-8')
    footer='[Cotes et pièces extérieures](cotes.md) · [Nomenclature complète d’assemblage](nomenclature-assemblage.csv) · [Contrôles KiCad](verification/controle-kicad.json) · [Contrôle indépendant FreeCAD](3D/validation-freecad.json).'
    t=t.replace(footer,'').strip()
    top='''<!-- prototype-m1p -->
> **M1P - porteuse libérée pour fabrication de prototype sur banc limité uniquement.** [Fabrication et fichiers](fabrication/README.md), [coordination chiffrée](verification/coordination-protections.md), [protocole B00-B14](verification/banc-essais.md), [registre](verification/liberation-prototype.json). Aucun essai matériel effectué. La connexion véhicule/LiPo n'est pas libérée. [Cotes TI](modules/cotes-ti.md) : pas2,54 exact ; contour relevé, cotes mécaniques exactes encore indisponibles.
<!-- /prototype-m1p -->

'''
    import re
    t=re.sub(r'<!-- prototype-m1p -->.*?<!-- /prototype-m1p -->\s*','',t,flags=re.S)
    write(p,top+t+'\n\n'+footer)
    p=B/'integration.md';t=p.read_text(encoding='utf-8')
    t=t.replace('Les pistes de 0,20 mm ont un usage de surveillance à faible courant ; le DRC ne garantit pas leur coordination en défaut.','La révision M1P porte les pistes à0,40 mm, le cuivre à70 micromètres nominaux (55 minimum) et les vias à0,80/0,40. La coordination est désormais analysée dans le document dédié : mode banc borné, pas de libération LiPo. Le DRC ne remplace pas cette analyse.')
    if '<!-- prototype-m1p -->' not in t:t='<!-- prototype-m1p -->\n> [M1P : conditions de fabrication et de banc](fabrication/README.md). Pour AUX, appliquer au banc le câblage limité du [protocole](verification/banc-essais.md), pas une LiPo. Le câblage ci-dessous reste la cible véhicule non libérée.\n<!-- /prototype-m1p -->\n\n'+t
    write(p,t)
    p=B/'verification/essais.md';write(p,'''# Essais M1P

Le protocole exécutable est désormais [banc-essais.md](banc-essais.md), paliers B00-B14. Les résultats sont à renseigner dans [resultats-banc.csv](resultats-banc.csv) ; ils sont **NON RÉALISÉS**. [Analyse des protections](coordination-protections.md), [registre de libération](liberation-prototype.json).

Les premiers essais sont sans LiPo ni moteurs, avec sources limitées et EVM sur supports isolants séparés. Après réussite : 2813 avec charge fictive, puis Pi, puis revue de la chaîne véhicule avant batterie et roulage. Une fabrication de prototype n'est pas une qualification d'exploitation.
''')
    print('M1P dimension evidence, calculations, BOM status and bench protocol prepared.',flush=True)

if __name__=='__main__':main()
