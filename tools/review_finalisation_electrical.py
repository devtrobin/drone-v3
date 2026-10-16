"""Final electrical review: fail-safe servo feed, extension and open conditions."""
from pathlib import Path
import json,csv,hashlib
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Composants/finalisation-theorique-r2';V=B/'verification'
def dump(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
routes=json.loads((B/'routage/parcours.json').read_text(encoding='utf-8'))
for r in routes:
    if r['code']=='P02':r['wire']='10 AWG puis6mm², extensionnégative160mm àprésenter'
dump(B/'routage/parcours.json',routes)
with (B/'routage/longueurs-cables.csv').open('w',encoding='utf-8-sig',newline='') as f:
    rows=[{k:v for k,v in r.items() if k!='points_mm'} for r in routes];w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');w.writeheader();w.writerows(rows)
wires=[
 ('BAT+','F0_IN','10AWG≥85 +TE32151 +SiF≥120','P01','Avantfusible, isoler/protéger'),
 ('BAT-','D-','10AWG +TE32151 +SiF6mm² +95R5','P02','Extension160mm candidate, ne pas utiliser cosse12AWG sur6mm²'),
 ('F0_OUT','ED80_IN','SiF6mm²','P03','Points de bornes/ancrages àfinaliser'),
 ('ED80_OUT','D+','SiF6mm²','P04','Points de bornes/ancrages àfinaliser'),
 ('D+','FP10 /2813 /D42V55F5 /Pi','12AWG puis18AWG','BranchePi','5A sortieàqualifier, aucunBEC surPi'),
 ('D+','SSR+2','SiF6mm²','P05','D1D100 polarité etthermique àvérifier'),
 ('SSR1','UD80','SiF6mm²','P06','Commun moteurs +servo, courant etchute àmesurer'),
 ('UD80','F1/F2 /XT60 /ESC','12AWG','M_G/M_D','15A continus de dimensionnement parESC'),
 ('UD80','FS5 /UBEC6V /servo','12AWG danssupport puis18AWG','S01 etarrivéeFS','Servo aussi coupé lors arrêtSSR, tenue6V en fin de packnonprouvée'),
 ('D-','ESC_G /ESC_D /UBEC','Retours de puissance dédiés','N_G/N_D','Aucun retour parGPIO ouchâssis'),
 ('F0_OUT','FAUX /M1P AUX','Selon schémaM1P','AUX','Logique indépendante, conditionsM1P conservées'),
 ('Pi3V3 /GND','ISO7710F entréesG/D/S','22AWG','Molex13contacts','Aucunpont sur les3domaines desortie'),
 ('BEC_G6V','LDO3V3 /ISOsortieG','22AWG local','ISO_G','GNDlocalESC_G seulement'),
 ('BEC_D6V','LDO3V3 /ISOsortieD','22AWG local','ISO_D','GNDlocalESC_D seulement'),
 ('UBEC6V','LDO3V3 /ISOsortieS','22AWG local','ISO_S','GNDlocalservo seulement')]
with (B/'routage/raccordements-r2.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f,delimiter=';');w.writerow(['origine','destination','conducteurs','parcours','condition']);w.writerows(wires)
# Estimate common wire resistance from the candidate route, without turning
# an assumed contact/holder resistance into a measured fact.
length=sum(r['centreline_mm'] for r in routes if r['code'] in ['P01','P02','P03','P04'])/1000
res20=.017241*length/6
dump(V/'revue-electrique-r2.json',dict(servo_feed_after_SSR=True,servo_off_on_hard_undervoltage=True,Pi_warning_polarity_unchanged='activeHIGH',power_and_signal_domains_separated_in_proposed_interface=True,common_candidate_wire_path_m=length,common_copper_only_R20_ohm=res20,common_old_R_budget_ohm=.005,contacts_fuses_ED80_not_included_in_wire_R=True,total_loop_budget_not_proven=True,UBEC_6V_at_end_of_pack_not_proven=True,negative_extension_added=True,main_fault_bound_unchanged_conditionally_A=16402.605867658778,full_protection_coordination_proven=False,new_interface_PCB_routed=False,ready_for_vehicle_power=False,hardware_tested=False))
dump(B/'routage/complements-nomenclature-electrique.json',dict(direction=dict(servo='FT5335M,révisionàconfirmer',converter_candidate='Hobbywing30603003',fuse_candidate='KLKD005.T',holder_candidate='L60030M1PQ',feed='UD80 aprèsSSR'),negative_extension=dict(TE32151_additional=1,SiF6mm2_negative_provision_mm=160,ATUM8_2_required=True,lug_95R5_additional=1,old_TE130191_no_longer_used_on_main_negative=True),isolation=dict(ISO7710FDR=3,MCP1703A3302=3),purchase_released=False))
sources=json.loads((B/'sources.json').read_text(encoding='utf-8'))
url='https://www.pololu.com/product/4981'
if not any(r['url']==url for r in sources):sources.append(dict(file=None,url=url,note='Alternative examined but not selected:6V ±4%,2.5A typical does not establish compatibility with the old6A peak servo revision.',archived=False,consulted_via_web='2026-10-16'))
dump(B/'sources.json',sources)
# Tie the successful geometry report to the unchanged delivered STEP.
data=json.loads((V/'synthese.json').read_text(encoding='utf-8'));step=ROOT/'Assemblage/R2/drone-v3-r2-etude.step'
data.update(assembly_step_sha256=hashlib.sha256(step.read_bytes()).hexdigest(),mass_study_updated_without_geometry_change_kg=9)
dump(V/'synthese.json',data)
print('REVUE ELECTRIQUE ENREGISTREE',length,'m, cuivreseul',res20,'ohm')
