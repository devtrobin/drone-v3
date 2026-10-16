"""Navigation, research provenance and reviewable remaining requirements."""
from pathlib import Path
import json,hashlib,re,shutil
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Composants/complements-finalisation-r3';V=B/'verification'
def dump(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def write(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t.strip()+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def prepend(p,marker,text):
    old=p.read_text(encoding='utf-8');start='<!-- '+marker+' -->';end='<!-- /'+marker+' -->'
    old=re.sub(re.escape(start)+r'.*?'+re.escape(end)+r'\s*','',old,flags=re.S)
    write(p,start+'\n'+text.strip()+'\n'+end+'\n\n'+old)
def run():
    sources=json.loads((B/'sources.json').read_text(encoding='utf-8'))
    for r in sources:
        if 'verified_via_web' in r:
            r['content_verified_via_web']=r['id'] in ['Littelfuse-LFT.pdf','Littelfuse-CSA.pdf','Littelfuse-JLLN.pdf']
            r.pop('verified_via_web',None)
        if r['id']=='TI-TPS3700EVM-gerbers.zip':r.update(public_link_verified=True,downloaded=False,PCB_dimensions_extracted=False)
    for name,rel,url in [
      ('Microchip-MCP1703A-original.pdf','Composants/carte-surveillance-electrique/notices/Microchip-MCP1703A-datasheet.pdf','https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/MCP1703A-250-mA-16V-Low-IQ-LDO-Regulator-DS20005122C.pdf'),
      ('TI-ISO7710-original.pdf','Composants/finalisation-theorique-r2/references/TI-ISO7710.pdf','https://www.ti.com/lit/ds/symlink/iso7710.pdf'),
      ('Hobbywing-UBEC-original.pdf','Composants/finalisation-theorique-r2/references/Hobbywing-UBEC10ACar.pdf','https://hobbywing.oss-cn-shenzhen.aliyuncs.com/pdf/pdfen/UBEC10ACar.pdf')]:
        src=ROOT/rel;dest=B/'references'/name;shutil.copy2(src,dest)
        sources=[r for r in sources if r['id']!=name]
        sources.append(dict(id=name,url=url,file='references/'+name,archived=True,sha256=sha(dest),copied_unchanged_from=rel,note='Original manufacturer document previously archived in this project'))
    dump(B/'sources.json',sources)
    h=B/'references/Hitec-D950TW-original.stp'
    dump(V/'alternative-hitec.json',dict(alternative_only=True,selected_for_assembly=False,manufacturer_CAD_sha256=sha(h),CAD_imported_in_CadQuery=True,solids=16,valid=True,power_at8_4V_continuously_not_validated=True,not_interchangeable_with_FT5335M=True))
    dump(B/'exigences-branche-direction.json',dict(status='Sélection électrique à reprendre D08',range_pack_V=[6.4,8.4],regulated_output_required_for_FT5335M_V=6,converter_must_support_VIN_below_VOUT_in_studied_scenarios=True,servo_work_torque_before_R2_factor2_Nm=1.177576958038984/2,servo_peak_design_torque_with_R2_factor2_Nm=1.177576958038984,do_not_substitute_stall_torque_for_continuous_torque=True,require_minimum_terminal_voltage_after_wire_and_connector_drop=True,current_transients_must_be_bounded=True,main_and_FS_fuse_coordination_required=True,all_servos_without_microcontroller=True,hardware_received=False,user_confirmed_no_parts_received_on='2026-10-17'))
    write(B/'questions-fabricants-non-envoyees.md','''# Questions techniques préparées - aucun message envoyé

## KHK / Horizon-Losi / Hobbywing

Confirmer l’angle de pression de LOS212054, son appairage avec SS0.5-54A20°, puis la charge radiale admissible de l’axe2435Ø2mm. Pour les deux couples16→54 et24→54, fournir une durée de service/régime admissible au point moteur25578tr/min, intermédiaire7579tr/min, roue3368tr/min, en précisant couple, lubrification et montage. Les couples catalogue600tr/min ne sont pas transposés directement.

## Littelfuse

Confirmer la terminaison de fils silicone à brins très fins et les références d’embouts admises, ou imposer des conducteurs compatibles. Confirmer le couple L60030M1PQ/KLKD en courant continu aux défauts de l’étude. Fournir une borne maximale d’énergie totale de coupure de JLLN050 et des KLKD concernés à8.4V, couvrant aussi les défauts intermédiaires. La tenue20kADC du LFT30060 est déjà référencée au certificatCSA ; distinguer cette information de la coordination complète.

## Alimentation de direction

L’association FT5335M/UBEC6V n’est pas validée quand la tension d’entrée disponible passe sous6V. La demande porte sur une solution adaptée à cette plage, pas sur une confirmation impossible d’un abaisseur élevant la tension. Préciser le courant maximal/transitoire, le comportement au démarrage, la tolérance et la tenue de sortie au bout du faisceau. L’alternativeHitecD950TW et son avertissement à8.4V sont documentés séparément.

## Texas Instruments et plans d’équipements

Le lien public SLVC413 est identifié, mais le téléchargement a répondu401 ici. Obtenir l’archive officielle ou les cotes de contour/épaisseur et les connecteurs de la révision livrée. Vérifier les plans des supports et leurs capots ; les points d’approche du faisceau se finissent sur ces bornes réelles.
''')
    write(B/'3D/README.md','''# Pièces nominales R3

Chaque STEP est dans le repère global du véhicule. Le fichier `complement-r3.step` contient déjà toutes les pièces de ce dossier : ne pas l’ajouter avec les fichiers unitaires au même assemblage.

Les deux L01_R3 remplacent les longerons correspondants de R2 dans la vue R3 ; ils ne s’y ajoutent pas. Les gabarits et limites d’équipements conservés sont des réservations. Les quatre conducteurs s’arrêtent à des points d’approche avant raccordement réel.

[Notice](../notice-mecanique.md) · [Assemblage](../../../Assemblage/R3/README.md) · [Liste de pièces](../pieces.json). Les filetages sont spécifiés, sans hélice détaillée. Le STEP constructeur Hitec dans `references` est une alternative documentée ; il n’est pas installé sur le véhicule.
''')
    prepend(ROOT/'ReadMe.md','complements-r3','''> **Compléments du17octobre2026 :** [dossierR3](Composants/complements-finalisation-r3/README.md), [assemblageFreeCADR3](Assemblage/R3/drone-v3-r3-faisceau.FCStd). Partie fixe du faisceau définie et contrôlée ; [anomalie d’alimentation de direction](Composants/complements-finalisation-r3/alimentation-direction-a-revoir.md) et confirmations fournisseur encore ouvertes. Aucune pièce reçue, aucun essai physique réalisé.''')
    prepend(ROOT/'Composants/README.md','complements-r3','''> **RévisionR3 :** [armature, cordons, visserie et revue électrique](complements-finalisation-r3/README.md). La brancheFT5335M+UBEC6V n’est pas validée sur toute la plage2S ; les réservations3D ne constituent pas un panier validé.''')
    prepend(ROOT/'SPECIFICATIONS.md','complements-r3','''> **RevueR3 du17octobre2026 :** objectifs40km/h,45min à20km/h et1080p60 inchangés. [DossierR3](Composants/complements-finalisation-r3/README.md) ; [conditions restantes](Composants/complements-finalisation-r3/conditions-restantes.md). L’alimentation de direction doit être revue pour couvrir les chutes en fin de pack ; aucune réduction implicite de performance ou d’autonomie n’est actée.''')
    prepend(ROOT/'PLAN-CONCEPTION.md','complements-r3','''> **ÉtatR3 du17octobre2026 :** partie fixe des quatre cordons, armature démontable et huit brides définies ; plans et assemblage dans le[dossierR3](Composants/complements-finalisation-r3/README.md). Restent des travaux documentaires/de conceptionD01/D03/D08, des terminaisons à présenter et la recette physique. La conception complète n’est pas déclarée terminée.''')
    prepend(ROOT/'Assemblage/README.md','complements-r3','''> [AssemblageR3 avec partie fixe du faisceau](R3/README.md). Les vues détailléesR1 et l’étudeR2 sont conservées ; R3 est une vue légère avec les ajouts. Les points extrêmes des câbles sont des approches, pas des raccordements fournisseur certifiés.''')
    dump(V/'etat-liberation.json',dict(review_date='2026-10-17',user_confirmed_no_parts_received=True,fixed_harness_and_supports_nominally_defined=True,terminal_tails_and_fittings_fully_defined=False,all_supplier_dimensions_exact=False,servo_power_pair_validated=False,complete_fuse_coordination_proven=False,full_vehicle_manufacturing_released=False,vehicle_power_on_released=False,physical_tests_done=False,remaining_conditions='../conditions-restantes.json'))
if __name__=='__main__':run()
