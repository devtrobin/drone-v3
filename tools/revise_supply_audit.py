"""Initial R2 migration script, retained as work provenance.

Reviewed final documents also contain later manual refinements: do not use this
bootstrap script to overwrite them. Use build_supply_audit_pdf.py to rebuild PDFs
and verify_supply_audit.py to check the current documented selection.
Historical documents and CAD stay intact.
"""
from pathlib import Path
import sys, json, math, shutil, hashlib
ROOT=Path(__file__).resolve().parents[1]
C=ROOT/'Composants'; BASE=C/'verification-alimentation'
DATE='2026-10-15'
def write(path,text):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text.strip()+'\n',encoding='utf-8')
def js(path,obj): write(path,json.dumps(obj,ensure_ascii=False,indent=2))

PARTS=[
 dict(folder='fusible-principal-classe-t',ref='JLLN050.T',qty=1,name='Littelfuse JLLN 50 A, classe T rapide',rating='160 V DC ; pouvoir de coupure 20 kA DC pour les calibres 35–60 A',source='https://www.littelfuse.com/assetdocs/jlln-datasheet?assetguid=3a7bc9bf-d932-4401-bdc7-b39f302195cf',buy='https://www.mouser.fr/c/?q=JLLN050.T',status='Sélection d’étude ; offre française exacte à confirmer'),
 dict(folder='support-fusible-classe-t',ref='LFT300601C + LFT30060FBC',qty=1,name='Support Littelfuse classe T 60 A et capot',rating='Support 60 A pour cartouche JLLN 35–60 A ; tenue DC 20 kA dans le certificat CSA ; capot séparé',source='https://www.littelfuse.com/assetdocs/lft-datasheet?assetguid=56b8955c-9cf7-4814-a923-97a4406bfa77',buy='https://www.mouser.com/en/ProductDetail/Littelfuse/LFT300601C?qs=Vv6sT79n3zTFrkdp10UQdA%3D%3D',status='Stock américain affiché ; prix/livraison France non confirmés'),
 dict(folder='fusibles-branches-rapides',ref='KLKD020.T × 2 ; KLKD010.T × 1',qty=3,name='Littelfuse KLKD rapides pour les branches',rating='Deux 20 A pour ESC ; un 10 A pour entrée Pi ; 600 V DC / 50 kA DC selon UL 248-14, distinct des 10 kA photovoltaïques UL 248-19',source='https://www.littelfuse.com/assetdocs/klkd-fuse-datasheet?assetguid=7b52eebb-c7cc-43df-a8da-9682a338e0f6',buy='https://www.mouser.fr/c/?q=KLKD020.T',status='Références identifiées ; devis français non confirmé'),
 dict(folder='supports-branches-rapides',ref='L60030M1PQ + capot SPL001',qty=3,name='Supports Littelfuse Midget 10 × 38 mm',rating='30 A, 600 V AC/DC ; pression sous vis, 10–14 AWG cuivre multibrin, 2,3 N·m. Utiliser la pression sous vis, pas les languettes rapides limitées à20 A. Bloc recommandé pour KLKD ; association DC à confirmer.',source='https://www.littelfuse.com/de/assetdocs/powr-gard-catalog?assetguid=85d36235-a32b-4608-bfed-f9878aa43af0',buy='https://www.mouser.fr/c/?q=L60030M1PQ',status='Référence précise ; prix France et tenue DC de l’association à confirmer'),
 dict(folder='cable-principal-silicone-6mm2',ref='LAPP 0054104 rouge ; 0054001 noir',qty=None,name='ÖLFLEX HEAT 180 SiF, 1 × 6 mm²',rating='Cuivre étamé classe 5 ; silicone −50 à +180 °C en pose fixe ; Ø5 mm ; résistance maximale 3,39 Ω/km à 20 °C ; rayon fixe 6 × diamètre',source='https://e.lapp.com/jp/p/temperature-resistant-cables/oelflex-heat-180-sif-1x6-ye-0054005',buy='https://mauser.pt/016-0348/lapp-olflex-heat-180-sif-0054104-fio-de-silicone-para-altas-temperaturas-6mm2-vermelho',status='Provision 2 m par couleur ; prix et stock exacts non confirmés'),
 dict(folder='regulateur-alimentation/d42v55f5',ref='Pololu 5571 / D42V55F5',qty=1,name='Pololu D42V55F5, 5 V / 6 A nominal',rating='5 V ±3 % ; dropout typique ≈0,25 V à 5 A ; courant continu dépendant de la thermique. Version 5 V, pas 5,3 V.',source='https://www.pololu.com/product/5571',buy='https://www.pololu.com/product/5571',status='47,95 USD fabricant affichés ; stock consulté, livraison/TVA France non confirmées'),
]

def calculations():
 # Constant-power Pi input, all resistances are ACCEPTANCE BUDGETS, not measurements.
 rows=[]
 for vpack in (6.4,6.6,7.4,8.4):
  for imot in (30,40):
   power=5.15*5/0.80; rq=0.05; rc=0.005; ictrl=0.015
   v=vpack-imot*rc
   for _ in range(100):
    ib=power/v+ictrl; v=vpack-(imot+ib)*rc-ib*rq
   rows.append(dict(Vpack_V=vpack,motors_A=imot,Pi_VIN_V=v,Pi_branch_A=ib,main_A=imot+ib,main_loss_W=(imot+ib)**2*rc,Pi_input_path_loss_W=ib**2*rq))
 rho0=0.01724*(1-20*0.00393)
 # Only positive wire BEFORE F0 is credited, no return wire or fuse resistance.
 rmin=rho0*(0.085/6.0+0.120/6.64); fault=8.4/rmin
 k=100; areas=[5.26,6.0,3.31,1.31,0.823,150*math.pi*(0.08**2)/4]
 return dict(date=DATE,hardware_measured=False,goals_unchanged=True,
  normal_design=dict(motor_branch_continuous_A=15,total_motor_continuous_A=30,main_continuous_budget_A=36,ambient_max_C=40,peak_study_per_motor_A=20,peak_study_duration_s=2,active_current_limiter_implemented=False),
  Pi_assumptions=dict(output_max_V=5.15,output_current_A=5,efficiency_min_study=0.80,common_loop_R_max_acceptance_ohm=0.005,Pi_input_path_R_max_acceptance_ohm=0.05,dropout_typical_at5A_V=0.25,dropout_design_margin_V=0.20,minimum_VIN_acceptance_V=5.8),
  supply_rows=rows,
  fault_bound=dict(conditional=True,voltage_max_V=8.4,temperature_min_C=0,credited_positive_segments=[dict(ref='SPMXCA510 positive wire',length_min_m=0.085,section_max_acceptance_mm2=6.0),dict(ref='LAPP6 extension before F0',length_min_m=0.120,section_max_acceptance_mm2=6.64)],positive_wire_R_min_ohm=rmin,source_fault_upper_A=fault,main_fuse_AIC_DC_A=20000,main_holder_withstand_DC_A=20000,branch_fuse_AIC_DC_A=50000,battery_internal_R_assumed_ohm=0,return_wire_resistance_credited=False,fuse_resistance_credited=False,alternate_power_returns_forbidden=True,does_not_protect_unfused_balance_wiring=True),
  short_wire_screening=dict(k_assumed_A_sqrt_s_per_mm2=k,initial_temperature_limit_C=85,final_temperature_limit_C=160,scope='Conservative copper screening for short faults; not a low-overload thermal proof',wires=[dict(area_mm2=s,allowable_I2t_A2s=(k*s)**2) for s in areas],KLKD020_total_clearing_I2t_A2s=1151,KLKD010_total_clearing_I2t_A2s=455,manufacturer_I2t_test='20 kA at 600 V DC; not a guaranteed maximum at 8.4 V',coordination_proven_at_our_voltage=False),
  charge=dict(battery='SPMX50002S30H5 G1 only',S65='SK-100152',lead='BEEC1067',balance='3-RAL2S, additional dedicated cable',current_A=5,cells=2,end_per_cell_V=4.2,power_max_W=42,S65_power_W=65,S65_current_max_A=6,lead_length_m=0.12,lead_supplier_section_published=False,charge_wiring_physical_checked=False),
  energy=dict(nominal_Wh=37,usable_fraction_assumption=0.8,usable_Wh=29.6,average_power_limits_W=dict(at20kmh_45min=29.6/.75,at40kmh_20min=29.6/(20/60),at40kmh_10min=29.6/(10/60)),runtime_at44A_nominal_minutes=5/44*60))

def main():
 sys.stdout.reconfigure(encoding='utf-8'); calc=calculations();js(BASE/'calculs.json',calc)
 PARTS.insert(-1,dict(folder='raccord-extension-cordon-ic5',ref='TE SOLISTRAND 32151',qty=1,name='Raccord bout à bout du positif IC5',rating='Cuivre non isolé ; 12–10 AWG / 2,62–6,64 mm² de chaque côté ; longueur14,35 mm, canon intérieur3,28 mm. Sertissage SOLISTRAND et ATUM8/2 sur environ35–40 mm.',source='https://www.te.com/en/product-32151.html',buy='https://www.mouser.fr/c/?q=TE%2032151',status='Prix France non confirmé ; compatible nominalement avec10 AWG et6 mm²'))
 PARTS.insert(-1,dict(folder='raccords-entree-pi-wago',ref='WAGO 221-413',qty=2,name='Répartition de la branche Pi côté batterie',rating='Deux bornes séparées, positif et GND ; acceptent12 AWG et18 AWG selon le dossier WAGO existant. Elles évitent de serrer18 AWG hors de la plage10–14 du support Midget.',source='https://www.wago.com/221-413',buy='https://www.gotronic.fr/cat-bornes-de-connexion-wago-0-5-a-2-5-mm2.htm',status='Prix antérieur0,75 EUR TTC/pièce àrevalider ; deux ajouts, hors répartition5 V déjà prévue'))
 js(BASE/'selection-active.json',dict(date=DATE,revision='alimentation-r2',battery='SPMX50002S30H5 G1 2S IC5',cord='SPMXCA510 10 AWG',main_fuse='JLLN050.T',main_holder='LFT300601C + LFT30060FBC',motor_fuses=['KLKD020.T','KLKD020.T'],Pi_input_fuse='KLKD010.T',branch_holders='L60030M1PQ × 3, association DC still to confirm',main_wire='LAPP 0054104 / 0054001 6 mm²',Pi_regulator='D42V55F5 / 5571',Pi_feed='Two +5 V and four GND 18 AWG wires, <=50 mm, soldered to Pi header PCB pads; no power through Molex contacts',charger='S65 retained + BEEC1067 + dedicated 2S balance extension',normal_main_budget_A=36,models_status='Previous complete harnesses and GPIO power model are historical; native D42V55Fx CAD is current regulator reference',hardware_tested=False,ready_for_power_on=False,full_fuse_coordination_validated=False,remaining_manufacturer_confirmations=['LFT acceptance of fine-stranded conductor/termination','L60030M1PQ + KLKD DC assembly withstand','Maximum clearing energy at 8.4 V and relevant fault currents'],deferred='Surveillance schematic/routing and mechanical integration with final chassis'))
 js(BASE/'nomenclature.json',dict(date=DATE,items=PARTS,removed_from_active=['Littelfuse MIDI 0498060.M 60 A','04980900ZXT M5 holder','ATO 30 A × 2','ATO 7.5 A × 1','Blue Sea 5065 × 3','AUPROTEC FLRY-B 6 mm² power runs','D24V90F5 / 2866','Molex power contacts on pins 2/4/6/9/14/20'],reused=['Pack G1 IC5','SPMXCA510','Blue Sea 2315 × 2','Albright ED80','D1D100 + HS251 + HSP-1','UD80A','BNTECHGO 12 AWG ESC branches','Existing lugs within their section and stud ranges','BNTECHGO 18 AWG for Pi','WAGO 221','Molex 40-way housing and 9 signal contacts'],purchased=False))
 write(BASE/'README.md',REPORT)
 write(BASE/'integration.md',INTEGRATION)
 write(BASE/'protocole-qualification.md',TESTS)
 write(BASE/'devis.md',QUOTE)
 write(BASE/'notices/README.md',NOTICES)
 for item in PARTS:
  folder=C/item['folder']; folder.mkdir(parents=True,exist_ok=True)
  if item['folder']=='regulateur-alimentation/d42v55f5':continue
  write(folder/'README.md',f"# {item['name']}\n\nSélection corrigée du 15 octobre 2026, non achetée et non testée.\n\n**Référence : {item['ref']}**. Quantité : {item['qty'] if item['qty'] is not None else 'provision 2 m par couleur, à couper après implantation'}.\n\n{item['rating']}\n\n[Source constructeur]({item['source']}) ; [achat ou recherche par référence]({item['buy']}). {item['status']}. Aucune offre Amazon.fr exacte confirmée.\n\nLa [notice de correction](../verification-alimentation/notices/verification-alimentation-v3.pdf), l’[intégration](../verification-alimentation/integration.md) et les [calculs](../verification-alimentation/calculs.json) détaillent le choix et ses limites. Les confirmations fabricant nécessaires sont listées séparément des futurs essais. Les STEP des pièces précédentes ne représentent pas cette nouvelle référence.\n")
  js(folder/'selection.json',dict(date=DATE,**item,hardware_tested=False,model_created=False))
 # Native replacement regulator, exact original bytes retained.
 reg=C/'regulateur-alimentation/d42v55f5';(reg/'3D').mkdir(parents=True,exist_ok=True);(reg/'notices').mkdir(exist_ok=True)
 shutil.copyfile(BASE/'references/Pololu-D42V55Fx-original.step',reg/'3D/pololu-d42v55fx-officiel.step')
 shutil.copyfile(BASE/'notices/Pololu-D42V55Fx-plan-original.pdf',reg/'notices/Pololu-D42V55Fx-plan-original.pdf')
 write(reg/'README.md',REGULATOR)
 js(reg/'selection.json',PARTS[-1])
 js(reg/'3D/provenance.json',dict(source='https://www.pololu.com/file/0J2181/d42v55fx-step-down-voltage-regulator.step',sha256=hashlib.sha256((reg/'3D/pololu-d42v55fx-officiel.step').read_bytes()).hexdigest(),original_unchanged=True,family_CAD=True,selected_electrical_variant='D42V55F5 / 5571',hardware_measured=False))
 write(reg/'3D/README.md','''# CAO officielle Pololu D42V55Fx

[STEP original](pololu-d42v55fx-officiel.step) et [plan constructeur](../notices/Pololu-D42V55Fx-plan-original.pdf), conservés sans modification. Référence de la famille donnée par Pololu sur la page de ressources du 5571. Le choix électrique est la variante **5 V**, pas la 5,3 V. Le modèle du D24V90F5 reste historique.

Les bornes, fils soudés, maintien et implantation finale ne sont pas définis par ce STEP. Aucun faux modèle de circuit interne n’est ajouté.
''')
 # Separate, fully specified charge package.
 charge=C/'cordon-charge-s65-ic5';(charge/'references').mkdir(parents=True,exist_ok=True)
 for filename in ('Beez2B-BEEC1067-stock.json','Beez2B-photo-0.jpg','Beez2B-photo-1.jpg'):
  src=BASE/'references'/filename
  if src.exists():shutil.copyfile(src,charge/'references'/filename)
 write(charge/'README.md',CHARGE)
 write(charge/'notice-montage.md',CHARGE_INSTALL)
 js(charge/'selection.json',dict(date=DATE,ref='BEEC1067',brand='Beez2B',qty=1,length_announced_mm=120,price_EUR_TTC=6.90,availability_observed=True,url='https://www.rcteam.com/products/beez2b-cable-de-charge-xt60-vers-ec5-beec1067',balance_extension_ref='INTERMODEL 3-RAL2S',balance_extension_additional_qty=1,balance_extension_price_EUR_TTC_previous=1.40,partial_total_EUR=8.30,Amazon_exact_offer_verified=False,compatible_S65_announced=True,compatible_IC5_power_via_EC5=True,Smart_data_used=False,current_initial_A=5,lot_polarity_checked=False,hardware_tested=False))
 # Update machine selection from the previous task without erasing its evidence.
 old=C/'cordon-principal-batterie/selection-active.json';obj=json.loads(old.read_text(encoding='utf-8'))
 obj.update(supply_revision='../verification-alimentation/selection-active.json',main_fuse='JLLN050.T 50 A replaces MIDI60',positive_termination='SPMXCA510 positive >=85 mm + TE32151 + LAPP6 extension >=120 mm before LFT300601C; M5 lug removed',negative_termination='One TE130191 to D- N2',charger='SkyRC S65 + BEEC1067 XT60/EC5 + dedicated 2S balance extension',full_fuse_coordination_validated=False,branch_fuses='KLKD020.T ×2 and KLKD010.T ×1',fuse_coordination_validated=False,current_44A_basis='Former worst load hypothesis, not continuous operating consumption or active limit',active_complete_cord_CAD=False)
 js(old,obj)
 # GPIO becomes a signals-only removable harness.
 gpio=C/'connecteur-gpio/brochage.json';obj=json.loads(gpio.read_text(encoding='utf-8'))
 archived=C/'connecteur-gpio/brochage-historique-15-contacts.json'
 if not archived.exists():shutil.copyfile(gpio,archived)
 powerpins={2,4,6,9,14,20}; obj['pins']=[p for p in obj['pins'] if p['physical_pin'] not in powerpins]
 obj['unused_pins']=sorted(set(obj['unused_pins'])|powerpins)
 obj.update(revised_on=DATE,power_through_Molex=False,signal_contacts_used=9,separate_power_PCB_solder_pads=[2,4,6,9,14,20],signal_connector_empty_at_power_pins=True,supply_revision='../verification-alimentation/integration.md')
 js(gpio,obj)
 nom=C/'connecteur-gpio/nomenclature.json';obj=json.loads(nom.read_text(encoding='utf-8'))
 for part in obj['parts']:
  if '16-02-0103' in part['reference']:part.update(quantity=14,installed=9,spares=5)
 obj.update(revised_on=DATE,connector_populated_contacts=9,provisional_sum_USD_at_unit1_prices=2.95+14*0.25+29.95,power_wires_in_this_removable_connector=False)
 js(nom,obj)
 # Explicit current/historical separation at every affected entry point.
 notes={
 'cordon-principal-batterie':'Positif CP0+ préparé sans cosse M5 vers le support classe T ; négatif CP0− avec une TE 130191 vers D−. Une seule cosse 130191 active, pas deux. Les STEP et l’ancien PDF avec deux cosses sont historiques.',
 'chargeur-batterie':'S65 conservé pour le pack G1 5 Ah : charge LiPo Balance 2S, 5 A, 42 W maximum. Cordon BEEC1067 et rallonge 2S dédiée sélectionnés ; les anciennes valeurs Zeee 5,2 Ah / 5,2 A sont historiques.',
 'protection-surintensite':'MIDI 60 A et support M5 retirés de la sélection active. Remplacement proposé : JLLN050.T 50 A et LFT300601C avec capot. Confirmation de la terminaison fine brins avant achat.',
 'protection-branche-pi':'ATO 7,5 A / Blue Sea 5065 retirés de la sélection active. Nouveau départ : KLKD010.T 10 A et support Midget. Ce calibre d’entrée ne donne pas 10 A à la Pi.',
 'protection-branches-moteurs':'ATO 30 A / Blue Sea 5065 retirés de la sélection active. Deux KLKD020.T 20 A proposés. Régime continu de dimensionnement : 15 A par ESC ; scénario court 20 A par ESC, 2 s, à tester. Les objectifs de vitesse/autonomie sont conservés.',
 'cable-principal-6mm2':'AUPROTEC FLRY-B 70 °C retiré des liaisons de puissance actives. LAPP SiF 6 mm² sélectionné pour mieux documenter classe, résistance et température. Le dossier et ses STEP restent historiques.',
 'regulateur-alimentation':'D24V90F5 retiré de la sélection active : D42V55F5 / Pololu 5571, 5 V ±3 %, dropout plus faible. CAO officielle dans le sous-dossier d42v55f5 ; vérifier le brochage, différent de l’ancien modèle.',
 'connecteur-gpio':'Molex conservé pour neuf signaux. Six positions de puissance non câblées dans cette prise. Alimentation Pi séparée : deux positifs et quatre retours courts en 18 AWG soudés aux pads du connecteur Pi ; les anciens quinze fils et leur STEP sont historiques.',
 'faisceau-puissance':'Appliquer le tableau de raccordements révisé : classe T, branches Midget, fil LAPP 6 mm², 18 AWG Pi et neuf signaux GPIO. Les nomenclatures, PDF et assemblages précédents restent des instantanés.',
 'cosses-puissance':'Le CP0+ ne reçoit plus de cosse 130191. Une seule TE 130191 reste sur CP0−. La cosse M5 de sortie MIDI disparaît ; les cosses ED80 M6 / D+ / SSR restent utilisées selon les nouvelles bornes.',
 'alimentation':'Pack actif Spektrum G1 2S IC5 5 Ah / 37 Wh, énergie utilisable supposée 29,6 Wh. Régulateur actif D42V55F5. S65 + BEEC1067 + équilibrage dédié. Les calculs Zeee précédents ne sont plus ceux de la batterie active.',
 'protection-batterie':'Modifier l’alimentation de la logique indépendante : depuis le positif après F0 mais avant ED80, à travers une protection auxiliaire à dimensionner, retour vers D−. B0/B1/B2 ne rejoignent que les voies locales isolées ; aucune masse de puissance par l’équilibrage.',
 'liaisons-alimentation-surveillance':'Ajouter une rallonge 3-RAL2S réservée au chargeur, distincte de celle de surveillance. Les fils 18 AWG sont réutilisés pour la puissance Pi. Déplacer la masse de logique vers D− ; les fils d’équilibrage ne deviennent pas un retour de puissance.',
 'coupure-manuelle':'ED80 conservé, après le nouveau F0 classe T et avant D+. La logique de surveillance alimentée avant ED80 et les voies de cellule restent à débrancher pour stockage. ED80 coupe les charges, pas une protection universelle du pack.',
 'moteur':'Moteurs et ESC conservés. Fils d’usine 16 AWG non remplacés à l’aveugle. Deux fusibles rapides 20 A, 15 A continus par départ pour le dimensionnement ; accepter le lot et tester le démarrage, le freinage et la thermique avant roulage.',
 'distribution-alimentation':'D+ / D− conservés. F0 devient classe T 50 A. Masse de logique et retours des commandes SSR sur D−, sans parallèle de puissance par B0 d’équilibrage.',
 'repartition-moteurs':'UD80 conservé : arrivée 6 mm² LAPP et départs selon le nouveau tableau. Ne pas substituer du 10 AWG nominal à son minimum IEC 6 mm².',
 }
 for folder,note in notes.items():
  path=C/folder/'README.md'
  if not path.exists():continue
  content=path.read_text(encoding='utf-8')
  marker='<!-- alimentation-r2 -->'; end='<!-- /alimentation-r2 -->'
  if marker in content:content=content[content.index(end)+len(end):].lstrip()
  # Previous active-battery banner is replaced by the more complete revision.
  if content.startswith('> **Révision du 15 octobre 2026'):
   content=content.split('\n\n',1)[1]
  prefix=f'{marker}\n> **Sélection active révisée le 15 octobre 2026.** {note}\n> [État électrique courant](../verification-alimentation/README.md) · [Raccordements](../verification-alimentation/integration.md). Les références différentes dans les documents ci-dessous sont historiques. Qualification matérielle non réalisée ; confirmations restantes explicites.\n{end}\n\n'
  write(path,prefix+content)
  js(C/folder/'revision-alimentation.json',dict(date=DATE,current_source='../verification-alimentation/selection-active.json',note=note,old_project_PDFs_and_complete_CAD_historical=True))
  integration=C/folder/'integration.md'
  if integration.exists():
   oldtext=integration.read_text(encoding='utf-8')
   if marker in oldtext:oldtext=oldtext[oldtext.index(end)+len(end):].lstrip()
   write(integration,prefix+oldtext)
 # Make old complete-model status visible next to the files, not just at root.
 for folder in ['cordon-principal-batterie/3D','cordon-principal-batterie/cordon-ic5-spektrum/3D','connecteur-gpio/3D','alimentation/3D','faisceau-puissance/3D','regulateur-alimentation/3D']:
  path=C/folder/'README.md'
  if path.exists():
   oldtext=path.read_text(encoding='utf-8')
   header='> **Révision électrique du 15 octobre 2026 :** les assemblages complets avec MIDI, deux cosses CP0 ou alimentation par contacts Molex sont historiques. Les pièces unitaires conservées restent utilisables comme références géométriques. Consulter la sélection active avant toute implantation.\n\n'
   if not oldtext.startswith(header):write(path,header+oldtext)
 # Root and component index: preserve earlier narrative in a named archive.
 rootreadme=next(p for p in ROOT.glob('*.md') if p.name.lower()=='readme.md')
 archive=ROOT/'archives/README-avant-correction-alimentation-2026-10-15.md'
 if not archive.exists():archive.parent.mkdir(exist_ok=True);shutil.copyfile(rootreadme,archive)
 write(rootreadme,ROOT_README)
 index=C/'README.md';oldtext=index.read_text(encoding='utf-8')
 banner='> **État actif de l’alimentation : révision du 15 octobre 2026.** [Audit et corrections](verification-alimentation/README.md), [cordon de charge S65–IC5](cordon-charge-s65-ic5/README.md). Les anciens calibres MIDI/ATO, le FLRY-B et le D24V90F5 restent des choix historiques ; suivre la nomenclature révisée.\n\n'
 if not oldtext.startswith(banner):write(index,banner+oldtext)
 print('Supply revision written; component files updated; no hardware qualification claimed.',flush=True)

from supply_audit_text import REGULATOR, CHARGE, CHARGE_INSTALL, ROOT_README, QUOTE, NOTICES, TESTS, INTEGRATION, REPORT
if __name__=='__main__': main()
