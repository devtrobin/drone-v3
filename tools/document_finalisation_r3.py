"""Traceable R3 closure report; real measurements and approvals are never inferred."""
from pathlib import Path
import json,csv,math,hashlib,re,sys
from scipy.optimize import root
import pymupdf
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit
from reportlab.lib.colors import HexColor
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Composants/complements-finalisation-r3';V=B/'verification';P=B/'plans';A=ROOT/'Assemblage/R3';T=ROOT/'tools/temp/finalisation-r3'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t.strip()+'\n',encoding='utf-8')
def dump(p,o):write(p,json.dumps(o,indent=2,ensure_ascii=False))
def csvout(p,rows):
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');w.writeheader();w.writerows(rows)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def display(t):
    t=str(t)
    if 'http' in t:return t
    t=re.sub(r'(?<=[a-zéèà])(?=\d)',' ',t)
    return re.sub(r'(?<=\d)(?=(?:mm|kg|µF|ohms|kohms|tr/min|V|A|W|N|MPa|ShoreA)\b)',' ',t)

GATES=[
 ('D01','Ouvert - fournisseur','Angle Losi, régime et endurance du couple Losi/KHK non publiés pour notre service. La table KHK est une référence à 600 tr/min, pas une qualification à 25 578 tr/min.'),
 ('D02','Identification définie ; essais requis','Association retenue pour étude : Pololu 3429 FT5335M + palonnier 3431, trou à rayon20 à reprendreØ3.2. Ne pas substituer la version25T. Courants transitoires et alimentation6V restent à qualifier.'),
 ('D03','Partiellement documenté','LFT30060 : tenue20kA DC explicitement listée au certificat CSA. Restent les brins fins/terminaisons, le couple L60030M+KLKD enDC et les enveloppes maximales de coupure à8.4V.'),
 ('D04','Mesure à réception','Relever fond hexagonal et face d’écrou des roues. Ajuster entretoises et extrémités d’axes avant le tournage final.'),
 ('D05','Plans partiels ; mesure à réception','Plan LFT30060 trouvé. TI publie SLVC413 mais le téléchargement répond401 ici ; aucune cote exacte TI n’en est déduite. Contrôler aussi UBEC, supports de fusibles, interfaces et accès.'),
 ('D06','Partie fixe conçue ; terminaisons à présenter','Quatre parcours3D et huit brides sur armature démontable définis. Les points extrêmes sont des approches. Les descentes terminales et le débit final se font aprèsD03/D05 ; elles ne sont pas déclarées entièrement raccordées.'),
 ('D07','Câblage de banc défini ; essais requis','Netlist de trois canaux avec brochage exact ISO7710FDR et MCP1703A-3302E/DB. Montage sur adaptateurs séparés ; aucun nouveauPCB/Gerber. Réactions électriques non mesurées.'),
 ('D08','Association de puissance non validée','Le scénario6.4V/30A moteurs/1A servo donne5.975V à l’entréeUBEC. Un abaisseur ne peut alors tenir6V. Le coupleFT5335M+UBEC doit être revu ; l’alternativeHitec documentée n’est pas intégrée ni déclarée interchangeable.'),
 ('P01-P04','Pratique','Pesée et charge avant, montage à blanc, échauffement/endurance, banc électrique limité, puis vitesse/autonomie/vidéo. Les objectifs ne deviennent pas des mesures par simulation.')]

def electrical():
    routes=load(B/'parcours.json');old=load(ROOT/'Composants/finalisation-theorique-r2/routage/parcours.json')
    lengths={r['code']:r['longueur_axe_mm']/1000 for r in routes};lengths.update({r['code']:r['centreline_mm']/1000 for r in old if r['code'] in ['P01','P02']})
    common=sum(lengths[n] for n in ['P01','P02','P03','P04']);prop=sum(lengths[n] for n in ['P05','P06'])
    rho=.017241;thermal=1+.00393*(80-20)
    Rc=common*rho/6*thermal+.002 # Contact budget is an acceptance assumption, not measured.
    Rp=prop*rho/6*thermal+.0015+.001 # SSR1.5mohm assumption + contacts1mohm.
    scenarios=[]
    for pack in [6.4,6.6,7.4,8.4]:
        for name,motor,servo in [('travail',30,1),('pointe_etude',40,12)]:
            def residual(v):
                vp,vu=v;ip=25.75/.8/vp;iservo=6*servo/.8/vu;vd=pack-(motor+iservo+ip)*Rc
                return [vp-vd+ip*.05,vu-vd+(motor+iservo)*Rp]
            sol=root(residual,[pack-.5,pack-.6]);assert sol.success
            vp,vu=map(float,sol.x);ip=25.75/.8/vp;ise=6*servo/.8/vu
            scenarios.append(dict(pack_V=pack,scenario=name,moteurs_A=motor,servo_sortie_A=servo,Pi_entree_V=round(vp,3),UBEC_entree_V=round(vu,3),commun_A=round(motor+ip+ise,2),Pi_seuil_5_8V_respecte=vp>=5.8,servo_6V_regule_non_prouve=True))
    dump(B/'calculs-electriques-r3.json',dict(assumptions_only=True,wire_temperature_C=80,common_wire_m=common,propulsion_only_wire_m=prop,common_copper_R20_ohm=common*rho/6,common_copper_R80_ohm=common*rho/6*thermal,common_contacts_acceptance_ohm=.002,propulsion_contacts_acceptance_ohm=.001,SSR_R_assumed_ohm=.0015,Pi_branch_R_acceptance_ohm=.05,efficiencies_assumed=.8,servo12A_is_test_scenario_not_published_maximum=True,old5mohm_common_budget_not_retained_as_demonstrated=True,full_protection_coordination_proven=False,untrimmed_terminal_allowances_not_included=True,servo_UBEC_pair_not_validated_over_complete_voltage_envelope=True,scenarios=scenarios))
    csvout(B/'scenarios-tension.csv',scenarios)
    nets=[]
    def pin(ref,pin,net,value):nets.append(dict(reference=ref,broche=str(pin),net=net,valeur=value))
    for p,n in [(1,'3V3_PI'),(2,'GND_PI'),(3,'PWM_G_PI'),(4,'PWM_D_PI'),(5,'PWM_S_PI')]:pin('J_PI',p,n,'Bornier banc uniquement, aucun courant actionneur')
    for ch in ['G','D','S']:
        g='GND_'+ch;v='3V3_'+ch;vin='VIN_LOCAL_'+ch;ins='IN_'+ch;outs='OUT_ISO_'+ch;pwm='PWM_LOCAL_'+ch
        for p,n in [(1,'3V3_PI'),(2,ins),(3,'3V3_PI'),(4,'GND_PI'),(5,g),(6,outs),(7,'NC'),(8,v)]:pin('U_'+ch,p,n,'ISO7710FDR SOIC8-D')
        for p,n in [(1,vin),(2,g),('TAB',g),(3,v)]:pin('L_'+ch,p,n,'MCP1703A-3302E/DB SOT223')
        for r,val,a,b in [('RIN','220ohm','PWM_'+ch+'_PI',ins),('RPDIN','10kohm',ins,'GND_PI'),('ROUT','220ohm',outs,pwm),('RPDOUT','10kohm',pwm,g),('CPI','100nF','3V3_PI','GND_PI'),('CISO','100nF',v,g),('CLIN','10uF25V',vin,g),('CLOUT','10uF25V',v,g)]:
            pin(r+'_'+ch,1,a,val);pin(r+'_'+ch,2,b,val)
        for p,n in [(1,vin),(2,g),(3,pwm)]:pin('J_'+ch,p,n,'Bornier banc : VIN local, GND local, signal ; pas ordre Futaba présumé')
    csvout(B/'interface-pwm-netlist-r3.csv',nets)
    for ch in ['G','D','S']:
        u={r['broche']:r['net'] for r in nets if r['reference']=='U_'+ch};l={r['broche']:r['net'] for r in nets if r['reference']=='L_'+ch}
        assert u['1']==u['3']=='3V3_PI' and u['4']=='GND_PI' and u['7']=='NC'
        assert l['1']=='VIN_LOCAL_'+ch and l['2']==l['TAB']=='GND_'+ch and l['3']==u['8']
    dump(V/'brochage.json',dict(three_ISO_D8_pinmaps_checked=True,MCP_SOT223_pin1='VIN',MCP_SOT223_pin2_and_tab='GND',MCP_SOT223_pin3='VOUT',no_direct_signal_ground_bridge=True,actual_adapter_continuity_not_tested=True,rows=len(nets),not_a_PCB_ERC=True))
    dump(B/'interface-pwm-bom-r3.json',dict(ISO7710FDR=3,MCP1703A_3302E_DB=3,R220ohm=6,R10kohm=6,C100nF=6,C10uF25V=6,SOIC8_adapters_independent_pads=3,SOT223_adapters_independent_pads=3,prototype_only=True,no_new_Gerbers=True,actuator_power_must_bypass_interface=True))
    return scenarios

def docs():
    write(B/'README.md','''# Compléments de finalisation R3

La R3 ajoute une réalisation nominale de la partie fixe du faisceau : armature démontable, huit brides garnies, entretoises anti-écrasement, quatre cordons courbes et visserie calculée. Elle approfondit les recherches fabricant et définit le câblage du prototype PWM. **Elle ne ferme pas les confirmations fournisseur ni les mesures physiques encore absentes. Le véhicule complet n’est pas déclaré prêt à alimenter.**

[PDF de revue](plans/dossier-complements-r3.pdf) · [Notice mécanique et cotes](notice-mecanique.md) · [Électricité](electricite.md) · [Points restants](conditions-restantes.md) · [Pièces STEP](3D/) · [Plans DXF](plans/) · [Assemblage FreeCAD](../../Assemblage/R3/drone-v3-r3-faisceau.FCStd).

- Les huit brides immobilisent les parcours fixes. Les points extrêmes des câbles sont des **points d’approche**, distincts des bornes exactes à relever. Les conducteurs s’arrêtent donc volontairement avant certains appareils dans la CAO.
- [Longueurs](longueurs-cables.csv) : rayons sur axe30mm, cuivre6mm², enveloppeØ6.5. Débits bruts avec réserve de raccordement ; couper définitivement après présentation, sans stocker la réserve en boucle contre les pièces chaudes.
- [Visserie R3](visserie-r3.csv) à ajouter à la [visserie R2](../visserie-finale/README.md). Aucune fixation fournisseur inconnue n’est comptée comme certaine.
- [Sources](sources.json), [netlist PWM](interface-pwm-netlist-r3.csv), [scénarios de tension](scenarios-tension.csv), [rapports](verification/).

L’association mécanique de direction identifiée est **Pololu3429 + palonnier3431**, sans achat. **L’alimentationFT5335M+UBEC6V n’est pas validée en fin de pack** : voir [l’anomalie et l’alternative documentée](alimentation-direction-a-revoir.md). FS5A reste suspendu à la qualification de cette branche. Le support de fusible principal a une tenue DC documentée ; les autres points de coordination restent explicitement ouverts.

La [révision R2](../finalisation-theorique-r2/README.md) et ses modèles détaillés antérieurs sont conservés. L’assemblage R3 est une **vue légère d’étude**, pas une nouvelle version ultra détaillée de tous les composants.
''')
    write(B/'notice-mecanique.md','''# Notice mécanique de l’armature R3

Repère du projet enmm : X transversal, Y de l’avant vers l’arrière, Z vers le haut ; sol0, dessus du plateau11. Les STEP sont dans ce repère global. Les DXF de gabarits utilisent une origine locale indiquée dans le rapport DXF ; ne pas les superposer directement aux anciens plans.

## Matières et débit

- Quatre montants R301 : tube aluminium10x30x1.5, L122, basZ14, hautZ136. CentresX±151 ; Y150 et355. Tube ouvert en haut et en bas.
- Deux rails R303 : tube aluminium30x10x1, L325, Y50..375, Z136..146. CentresX±151.
- Deux traverses R304 : même tube30x10x1, L272, X−136..136 ; centresY60 et335. Les deux extrémités sont en contact avec les faces intérieures des rails.
- Quatre éclisses R305 : aluminium40x30x3, centresX±141/Y60 ou335, sous-faceZ146. Quatre trousØ3.4 aux entraxes20x16.
- Six consoles R306 : plats aluminium3mm, trois60x20, un65x20 et deux20x115, sous-faceZ146. Les deux dernières avancent les bridesP06 de95mm depuis la traverseY335 ; leur table de perçage est en coordonnées globales.
- Huit brides : POM-C, bases12x24x7 et capots12x24x5 ; usiner l’alésageØ7.2 en réunissant les deux demi-pièces. Deux trousØ3.4, entraxe16. Une garniture silicone50ShoreA nominal0.5, largeur10, longueur~21.5 par bride ; la CAO représente0.35 comprimé. Les faces POM servent de butée de serrage.
- Bouchons de montants R312 : aluminium6.9x26.9x12, taraudageM4x0.7 ; retenue transversaleM3 àYlocal+8/Z130. La retenue ne traverse pas l’axe de la visM4.
- Entretoises R310 dans rails/traverses : aluminiumL8, OD5.5/ID3.4 pourM3, OD7/ID4.5 pourM4. Entretoises R313 dans montants : OD8/ID4.5 L7. Mettre les entretoises avant de fermer les tubes.

Choisir une matière aluminium dont Re≥200MPa est attesté pour les pièces sollicitées ; sinon recalculer à partir du certificat matière. L’étude simplifiée porte sur20N au total sur les supports de câbles, pas sur une personne s’appuyant dessus ni un choc de véhicule.

## Montage et accès

Les montants se fixent par deuxM4 horizontales sur les ailes verticales des longerons L01 existants. Ajouter quatre trousØ4.5 par longeron : Y142,158,347,363 ; Z25 ; axeX. Une calePOM1mm par vis couvre le jeu entre face extérieure du longeronX±145 et face du montantX±146. Ne pas ajouter de trous au plateauC01 pour cette armature.

Perçages, taraudages et positions : [table complète](plans/percages-globaux-r3.csv), [pièces](pieces.json), STEP et DXF associés. Une visM4x20 se visse dans le bouchon à travers le rail ; sa pénétration nominale est9.2mm. Les bouchons sont retenus parM3 décalées. Monter les éclisses, puis les consoles, entretoises et brides. Sur les tubes, le rectangle du DXF est un repère de gabarit de perçage, pas une instruction de découper une tôle.

Ébavurer les arêtes, casser les angles au contact des mains et des câbles. Vérifier que chaque entretoise est réellement prise entre les deux parois du tube avant serrage. Serrer les brides jusqu’au contact des faces POM ; vérifier retenue axiale, absence de pincement de gaine et température après essai. Les couples de serrage des bornes électriques restent ceux du fabricant.

L’armature se démonte indépendamment du support caméra. Les écrous des brides placées au-dessus des tubes restent accessibles avant mise en place de l’électronique. Ce montage nominal ne remplace pas la vérification de l’accès avec l’outillage réel.
''')
    write(B/'electricite.md','''# Revue électrique R3

## Protections et données nouvelles

La fiche officielle JLLN donne pour50A160VDC et20kA de pouvoir de coupure. Le certificat CSA Littelfuse mentionne explicitement les LFT30060 à60A avec tenue20kADC ; ce point est documenté et n’est plus déduit d’un SCCR alternatif. Cela ne démontre ni la coordination de tout le véhicule ni l’énergie maximale de coupure à8.4V.

Les bornes «solid/stranded» n’acceptent pas automatiquement tous les câbles silicone à brins très fins. Ne pas ajouter arbitrairement un embout serti et le considérer homologué. Restent à confirmer : terminaison pour nos conducteurs, association L60030M+KLKD enDC et maximum d’énergie de coupure pour les défauts pertinents. Le principalJLLN050 et FS5A ne sont pas augmentés en calibre pour masquer une pointe non qualifiée.

Le plan officiel OL-LFT30060 est identifié dans la ficheLFT, page3. Les autres implantations non cotées restent des réservations sur cassettes démontables. Les fichiers TI SLVC413 sont publiés sur la page de l’EVM ; le téléchargement a répondu401 dans cet environnement. Aucune dimension TI exacte ni nouveau trou n’a été inventé à partir d’une image sans échelle.

## Servo défini pour l’étude

Retenir ensemble Pololu3429 (FT5335M) et3431 (palonnier compatible). Le dessin du palonnier donne des trous au pas5mm, dont un àR20 ; reprendre ce trou deØ2.5 àØ3.2 pour la liaisonM3, sans toucher aux cannelures. Les données de cette variante ne sont pas fusionnées avec celles du FT5335M25T d’une autre page.

Pololu indique des pointes **supérieures à9A à7.4V**. Ce n’est ni une valeur maximale garantie, ni une mesure à6V. La fiche historique4/6A ne suffit donc plus à borner toutes les pointes. La brancheUBEC30603003 et le fusibleFS5A restent à qualifier à6V. Le scénario12A de sortie utilisé dans les calculs est une épreuve choisie, pas une nouvelle spécification fabricant. Vérifier aussi le cordon et le connecteur d’usine du servo sous ce service. Le couple35kg.cm à6V publié est un couple de blocage, pas un couple permanent.

Le servo reste alimenté aprèsSSR, comme enR2, afin qu’une coupure analogique dure supprime aussi cette charge. Aucun BEC d’ESC n’est mis en parallèle avec l’UBEC ni avec le5V Pi.

## Résistance et tension

Les longueurs3D R3 remplacent les quatre anciens corridors hauts. [Calculs](calculs-electriques-r3.json) et [table de scénarios](scenarios-tension.csv) distinguent le chemin communIC5/F0/ED80/D+ et les deux cordons supplémentaires versSSR/UD80. Le courantPi ne traverse pasP05/P06. La résistivité est corrigée à80°C pour l’étude ; les résistances de contact et rendements sont des hypothèses d’acceptation, pas des mesures.

Le budget commun historique5mΩ n’est plus traité comme prouvé. Mesurer la résistance de boucle à quatre fils et les chutes sous charge, puis vérifierPiVIN≥5.8V selon le protocole du régulateur. Les pointes les plus défavorables en fin de pack ne sont pas garanties ; ne pas annoncer une tenue6V du servo sur la seule mention «2S» de l’UBEC. Les queues de raccordement sont à inclure dans la mesure finale.

## Prototype PWM à trois canaux

[Netlist complète](interface-pwm-netlist-r3.csv) et [nomenclature](interface-pwm-bom-r3.json). Trois ISO7710FDR SOIC8-D indépendants : 1et3=3V3_PI ;2=entrée via220ohms ;4=GND_PI ;5=GND local ;6=sortie via220ohms ;7=NC ;8=3V3 local. Rappel10kohms sur l’entrée après la résistance et sur le signal de sortie.100nF sur chaque alimentation de chaqueISO.

Trois **MCP1703A-3302E/DB SOT223** : **1=VIN ;2etTAB=GND ;3=VOUT** selon la table3-1 Microchip. Ce n’est pas le brochage d’un AMS1117. Chaque régulateur reçoit le BEC/UBEC de son actionneur et fournit3.3V au côté sortie correspondant. Deux10µF25V par LDO, polarité à respecter. Les adaptateurs doivent avoir des pastilles séparées ; tester leur continuité hors tension.

Le bornierJ_PI ne transporte que3.3V,GND et troisPWM. Les borniersJ_G/J_D/J_S sont explicitement ordonnés VINlocal/GNDlocal/signal ; cela ne présume pas l’orientation d’une priseFutaba. **La puissance du servo et des ESC contourne les adaptateurs**. Le circuit ne certifie pas une isolation globale : les retours d’alimentation rejoignentD− ailleurs ; la barrière évite de créer un retour parallèle par les petits fils de commande.

Le suffixeF donne un état par défaut bas ; un PWM valide resté figé doit encore être détecté par la stratégie de surveillance. Aucun nouveauPCB/Gerber n’est livré ; le prototype à fils sur adaptateurs doit être testé avant une éventuelle carte dédiée.

Sources : [Pololu3429](https://www.pololu.com/product/3429), [palonnier3431](https://www.pololu.com/product/3431), [LFT](https://www.littelfuse.com/assetdocs/lft-datasheet?assetguid=56b8955c-9cf7-4814-a923-97a4406bfa77), [certificatCSA](https://www.littelfuse.com/assetdocs/csa-6225-01-007316?assetguid=203ad805-7e22-463f-997a-2431bbdfbbd1), [ISO7710](https://www.ti.com/lit/ds/symlink/iso7710.pdf), [MCP1703A local](../carte-surveillance-electrique/notices/Microchip-MCP1703A-datasheet.pdf).
''')
    write(B/'conditions-restantes.md','# État après compléments R3\n\n'+'\n\n'.join('## '+i+' - '+s+'\n\n'+t for i,s,t in GATES))
    write(B/'alimentation-direction-a-revoir.md','''# Alimentation de direction : anomalie à résoudre

Le calcul nominal à6.4V pack,30A moteurs et1A de sortie servo donne environ5.975V à l’entrée de l’UBEC, sous les hypothèses de câblage/contact/température affichées. Le point d’étude de pointe descend plus bas. **Un abaisseur ne peut fournir6V à partir de moins de6V. Le couple FT5335M+Hobbywing6V ne peut donc pas être déclaré compatible avec toute l’enveloppe retenue.** Ce n’est pas un détail à remplacer par une simple mention «à tester».

Les composants visibles dans l’assemblage restent les réservations de l’étudeR2 ; la R3 livre l’armature et les parcours, sans annoncer la branche de direction prête à acheter. Les corrections possibles demandent une nouvelle sélection d’alimentation/servo ou une limitation de fonctionnement explicitement calculée ; relever le fusible ne corrige pas ce problème.

Une alternative a été documentée : **Hitec D950TW36950S**, avec [fiche originaleV2.2](references/Hitec-D950TW-datasheet.pdf) et [STEP constructeur original](references/Hitec-D950TW-original.stp). Le fabricant publie40x20x38mm,68g,25TØ6,21kg.cm de blocage à4.8V. Ce couple de blocage n’est pas un couple permanent ; le couple au rendement optimal est seulement4.2kg.cm à4.8V. Le corps et les fixations diffèrent du FT5335M ; ce n’est pas une substitution mécanique directe.

La page fabricantUS annonce4.8..8.4V ; la ficheV2.2 indique3.5..8.4V mais recommande l’utilisation au maximum de tension seulement sur une courte durée. **L’alimentation directe sur2S pleine n’est donc pas retenue automatiquement.** Un palonnier25T de rayon20 et une alimentation adaptée doivent être fixés avant intégration. Aucun changement silencieux de cette pièce n’a été introduit dans la CAO.

Les petits régulateurs examinés ne sont pas validés sur leur seul courant typique annoncé : vérifier aussi tension minimale, tolérance de sortie, pertes du câble d’usine, transitoires et thermique. Le PDF permet de reprendre cette sélection avec des exigences explicites plutôt que de mélanger des variantes.

Sources : [HitecUS](https://hitecrcd.com/d950tw-wide-voltage-titanium-gear-25t-digital-coreless-servo/), [HitecEU et CAD](https://shop.hitec-europe.eu/collections/standard-servos/products/servo-d950tw). Aucun achat ni essai effectué.
''')
    dump(B/'conditions-restantes.json',[dict(id=i,statut=s,condition=t) for i,s,t in GATES])
    write(B/'releve-reception.csv','piece;grandeur;unite;valeur_mesuree;document_ou_lot\nRoue;fond hexagonal et face écrou;mm;;\nFT5335M Pololu3429;cannelure et tension du lot;texte;;\nFT5335M Pololu3429;pointe réelle à6V;A;;\nLFT300601C;bornes et fixation;mm;;\nL60030M1PQ;bornes et fixation;mm;;\nTPS3700EVM-114;contour et épaisseur assemblée;mm;;\nUBEC30603003;sortie àVin minimal sous charge;V;;\nVéhicule;masse totale;kg;;\nVéhicule;charge avant;pourcent;;')
    write(B/'protocole-banc.md','''# Recette à réaliser sur matériel

1. Contrôler pièces et références sur le relevé de réception. Monter à blanc et régler les jeux de roulements ; faire tourner à la main, puis présenter les câbles sans batterie. Contrôler gaine, arêtes, portée des garnitures et accès au boutonED80.
2. Sur les interfacesPWM non reliées aux actionneurs, vérifier chaque adaptateur à l’ohmmètre, son brochage et l’absence de pont de masse direct entre côtés. Alimenter en3.3V côtéPi et5V côtélocal avec sources de laboratoire limitées initialement à20mA par canal ; mesurer3.3V du LDO et état bas par défaut.
3. Observer à l’oscilloscope les signaux en entrée et sortie ; tester extinction de chaque alimentation, redémarrage duPi, absence d’impulsions et commande valide figée. Ne pas déduire l’arrêt moteur du seul suffixeF. Reprendre le protocole de surveillanceM1P existant, dont les conditions restent applicables.
4. Tester la branche de direction sur alimentation limitée adaptée, sansLiPo, avec le servo désaccouplé d’abord. Régler6V et le neutre, mesurer courants transitoires et tension au connecteur. Puis appliquer progressivement la charge prévue en surveillant température et chutes. Ne pas maintenir le servo bloqué ni forcer les butées pour le calibrer.
5. Mesurer résistances de boucle à quatre fils et chutes sous charges bornées, depuis8.4V jusqu’au seuil minimal prévu. Confirmer le fusible et l’UBEC à partir des résultats et des confirmations fabricant. Aucun essai de court-circuit direct du pack n’est demandé.
6. Peser le montage complet et la charge avant. Le calculR2 reste limité à9kg et45% à l’avant. Faire les essais roulants progressivement après qualification, puis mesurer vidéo, autonomie et vitesse sur un site approprié.

Ces opérations sont un protocole, pas des essais réalisés. Aucun achat, envoi de message fabricant ni assemblage physique n’est exécuté par ce dossier.
''')
    write(P/'README.md','''# Plans R3

Les DXF sont des gabarits de la **face supérieure** réellement extraite des STEP. L’origine locale de chacun figure dans [le rapport de comparaison](../verification/dxf.json), sous `local_origin_global_mm`. Unitésmm. Les éclisses et consoles sont des plats3mm à découper ; les contours des rails/traverses représentent un tube déjà débité, à percer, et ne sont pas des développés de tôle.

[Perçages globaux](percages-globaux-r3.csv) · [Cotes et montage](../notice-mecanique.md) · [PDF](dossier-complements-r3.pdf). Les modèles3D et la notice définissent les trous horizontaux, bouchons, demi-brides et entretoises ; ne pas extrapoler ces opérations depuis un seul DXF de face.
''')
    write(A/'README.md','''# Assemblage R3 - partie fixe du faisceau

[FreeCAD natif](drone-v3-r3-faisceau.FCStd) · [STEP](drone-v3-r3-faisceau.step) · [NoticeR3](../../Composants/complements-finalisation-r3/README.md) · [Vue isométrique](apercu-r3-isometrique.png) · [Vue de dessus](apercu-r3-dessus.png).

Vue légère de l’assemblageR2 avec armature, huit brides et quatre parcoursR3. Les deux longeronsL01 sont percés pour les nouveaux montants dans cette révision seulement. Les autres fichiersR2 sont conservés. Les points extrêmes des conducteurs sont des approches, pas des bornes fournisseur exactes ; leur arrêt avant certains appareils est volontaire.

Les modèles détaillésR1 ne contiennent ni les correctionsR2 ni ces complémentsR3. Cette vue ne constitue pas une qualification mécanique/électrique du véhicule complet.
''')

class PDF:
    def __init__(self):
        pdfmetrics.registerFont(TTFont('R3F','C:/Windows/Fonts/arial.ttf'));pdfmetrics.registerFont(TTFont('R3B','C:/Windows/Fonts/arialbd.ttf'))
        self.c=canvas.Canvas(str(P/'dossier-complements-r3.pdf'),pagesize=(842,595));self.n=0;self.y=0
        self.c.setTitle('Drone V3 - Compléments de finalisation R3')
    def foot(self):
        self.c.setFillColor(HexColor('#64748b'));self.c.setFont('R3F',8);self.c.drawString(30,18,'Drone V3 | R3 | 17 octobre 2026 | étude nominale, matériel non testé');self.c.drawRightString(812,18,str(self.n))
    def page(self,title):
        if self.n:self.foot();self.c.showPage()
        self.n+=1;self.y=518;c=self.c;c.setFillColor(HexColor('#12304a'));c.rect(0,553,842,42,fill=1,stroke=0);c.setFillColor(HexColor('#ffffff'));c.setFont('R3B',17);c.drawString(30,568,title);c.setFont('R3F',9);c.setFillColor(HexColor('#475569'));c.drawString(30,537,'Complément à R2 ; mesures et confirmations encore nécessaires')
    def text(self,t,size=10,bold=False):
        t=display(t)
        lines=simpleSplit(t,'R3B' if bold else 'R3F',size,782);self.c.setFont('R3B' if bold else 'R3F',size);self.c.setFillColor(HexColor('#182536'))
        for line in lines:self.c.drawString(30,self.y,line);self.y-=size+4
        self.y-=9
    def table(self,head,rows,widths,size=9):
        for i,row in enumerate([head]+rows):
            blocks=[simpleSplit(display(v),'R3B' if i==0 else 'R3F',size,w-10) for v,w in zip(row,widths)];height=max(len(b) for b in blocks)*(size+3)+10
            if self.y-height<45:self.page('Suite - tableau')
            self.c.setFillColor(HexColor('#dce8f0' if i==0 else '#f1f5f9' if i%2 else '#ffffff'));self.c.rect(30,self.y-height,sum(widths),height,fill=1,stroke=0);x=30
            for block,w in zip(blocks,widths):
                self.c.setFillColor(HexColor('#182536'));self.c.setFont('R3B' if i==0 else 'R3F',size)
                for j,l in enumerate(block):self.c.drawString(x+5,self.y-14-j*(size+3),l)
                x+=w
            self.y-=height
        self.y-=10
    def save(self):self.foot();self.c.save()

def pdf(scenarios):
    p=PDF();geom=load(V/'geometrie.json');dims=load(V/'dimensionnement-supports.json');routes=load(B/'parcours.json')
    p.page('Drone V3 - Compléments de finalisation R3')
    p.text('La partie fixe des quatre cordons principaux et ses supports sont conçus. Les interfaces fournisseur, les terminaisons et les essais encore absents restent explicitement ouverts.',12,True)
    p.table(['Volet','Ajout R3','Ce que cela ne valide pas'],[
      ['Mécanique','Armature démontable, brides garnies, bouchons et entretoises anti-écrasement','Aucun dimensionnement au choc ni appui d’une personne'],
      ['Intégration','Quatre parcours courbes intégrés ; contrôles de collisions nominaux','Points d’approche distincts des bornes exactes et des queues terminales'],
      ['Électricité','Variante servo définie, sources vérifiées, netlist complète du bancPWM','Fusibles, thermiques et transitoires non qualifiés sur matériel'],
      ['Visserie','Longueurs supplémentaires calculées, gabarits de perçage','Fixations propres aux composants encore non cotés']], [95,345,342],10)
    p.text('Le véhicule complet n’est pas déclaré prêt à alimenter. Les STEP R3 constituent une vue légère d’étude ; les modèles ultra détaillés antérieurs restent des versions R1.',10)
    p.text(f"Pièces propres à l’armature : environ {dims['new_custom_parts_estimated_g']:.0f} g hors visserie ; cuivre et gaine des quatre câbles : environ {dims['four_cables_estimated_g']:.0f} g hors queues. La masse complète doit rester dans l’enveloppe R2 de9kg et45% à l’avant.",10)
    p.page('Assemblage et accès')
    image=A/'apercu-r3-isometrique.png'
    if image.exists():p.c.drawImage(str(image),75,90,width=690,height=425,preserveAspectRatio=True,anchor='c',mask='auto')
    p.y=73;p.text('Armature fixée aux deux longerons. Traverses àY60/Y335 ; faisceaux au-dessus des équipements. Les câbles s’arrêtent volontairement aux points d’approche avant raccordement réel.',9)
    p.page('Cotes de fabrication - armature et brides')
    p.table(['Pièce','Qté','Matière / définition'],[
      ['R301 montants',4,'Tube Al10x30x1.5 L122 ; X±151, Y150/355, Z14..136'],
      ['R303 rails',2,'Tube Al30x10x1 L325 ; X±151 ; Y50..375 ; Z136..146'],
      ['R304 traverses',2,'Tube Al30x10x1 L272 ; X−136..136 ; Y60/335'],
      ['R305 éclisses',4,'Al40x30x3 ; quatre trousØ3.4 entraxes20x16'],
      ['R306 consoles',6,'Al3mm ; trois60x20, une65x20 et deux20x115 ; table globale et DXF'],
      ['R307/R308 brides',8,'POM-C12x24x7 +12x24x5 ; alésage communØ7.2 ; trousM3 entraxe16'],
      ['R309 entretoises',16,'POM-C OD6/ID3.4 ; longueurs individualisées dans STEP/visserie'],
      ['R310 / R313',44,'Al, anti-écrasement : railsL8 ; montantsL7 ; ne pas les omettre'],
      ['R311 garnitures',8,'Silicone nominal0.5, largeur10, longueur~21.5 ; compression représentée0.35'],
      ['R312 bouchons',4,'Al6.9x26.9x12 ; M4 axial ; retenueM3 décaléeY+8/Z130']], [170,40,572],9)
    p.text(f"Étude simplifiée sous20N au total, aluminium Re≥200MPa : montant {dims['post_stress_MPa']:.2f}MPa / flèche {dims['post_deflection_mm']:.3f}mm ; traverse {dims['crossbar_stress_MPa']:.2f}MPa / {dims['crossbar_deflection_mm']:.3f}mm ; console déportée sous10N : {dims['offset_console_stress_MPa']:.1f}MPa / {dims['offset_console_deflection_mm']:.2f}mm. Sans analyse de choc, fatigue ni déformation locale des perçages.",9)
    p.page('Routage et longueurs')
    p.table(['Cordon','Liaison','Axe mm','Brut mm'],[[r['code'],r['net'],r['longueur_axe_mm'],r['brut_approvisionnement_mm']] for r in routes],[70,450,120,142],11)
    p.text('Cuivre6mm² ; gaine représentéeØ6.5 ; rayon d’axe30mm. Les bruts comprennent une réserve à recouper : ils ne sont pas des longueurs finales de raccordement.',10)
    p.table(['Bride','Position axe X/Y/Z (mm)','Axe du câble'],[['1–2','60/60/160 ; 0/60/160','X'],['3–4','−180/220/160 ; −180/240/160','Y'],['5','−180/260/175','Y'],['6–7','0/240/160 ; 60/240/160','X'],['8','108/300/160','Y']],[80,552,150],10)
    p.text(f"Contrôle nominal : {geom['pairs']} paires examinées, aucune intersection volumique inattendue entre les ajouts R3 et la scène importée. Les interfaces internes de tous les anciens équipements ne sont pas recalculées. Le chemin vers les bornes réelles doit encore être présenté.",10)
    p.page('Visserie supplémentaire R3')
    rows=list(csv.DictReader((B/'visserie-r3.csv').open(encoding='utf-8-sig'),delimiter=';'))
    p.table(['Repère','Vis','Qté','Empilage / longueur retenue mm'],[[r['code'],r['reference'],r['quantite'],str(r['empilage_mm'])+' + rondelles'+str(r['rondelles_mm'])+' + écrou'+str(r['ecrou_mm'])+' ; L='+r['longueur_retenue_mm']] for r in rows],[85,240,40,417],9)
    p.text('Longueur sous tête. Les engagements et écrous sont dans leCSV. Ajouter cette liste à la visserieR2 ; respecter les entretoises anti-écrasement. Les tubes se percent avant montage des cassettes et appareils.',10)
    p.page('Recherches fabricant - décisions et limites')
    p.text('Transmission : KHK confirme module0.5 et angle20°. La ligne SS0.5-54A donne2.67N.m en flexion et0.32N.m en durabilité de surface ; SS0.5-24B donne0.93/0.059N.m. Les conditions catalogue utilisent notamment600tr/min, une géométrie d’appairage et une durée de vie définies. Ces nombres ne qualifient pas le montage à25 578tr/min moteur. L’angle de pression du Losi n’a pas été trouvé dans sa fiche officielle.',10)
    p.text('Direction : l’association Pololu3429 +3431 évite de mélanger la variante17T et la page25T. Le trouR20 du palonnier est identifié ; repriseØ3.2 pourM3. Le couple publié35kg.cm à6V est un couple de blocage. Les pointes >9A annoncées par Pololu sont à7.4V et ne constituent pas un maximum garanti à6V.',10)
    p.text('Protections : le certificatCSA identifie la tenue20kADC duLFT30060. La ficheLFT donne les plages de fil et couples de serrage ; cela ne vaut pas acceptation automatique de brins très fins avec embout. L’associationDC L60030M+KLKD et l’énergie maximale à8.4V restent à confirmer.',10)
    p.text('TI : lien officiel SLVC413 trouvé ; téléchargement refusé401 ici. Les réservations60x60 restent des réservations, sans trouTI inventé. Le planLFT30060 est disponible dans la fiche officielle, page3.',10)
    p.page('Direction - association électrique à revoir')
    p.text('Anomalie : le scénario6.4V pack,30A moteurs et1A servo donne5.975V à l’entrée de l’UBEC. Un abaisseur ne peut pas alors maintenir6V. Le coupleFT5335M+Hobbywing6V n’est pas validé sur toute l’enveloppe ; il faut revoir la sélection ou définir une restriction de fonctionnement.',11,True)
    p.text('Alternative documentée, non intégrée : HitecD950TW36950S. FicheV2.2 et STEP constructeur téléchargés. Corps40x20x38mm,68g,25TØ6 ; couple de blocage21kg.cm à4.8V, distinct du couple au rendement optimal4.2kg.cm. Fixations et palonnier différents : aucune substitution directe déclarée.',10)
    p.text('La fiche indique3.5..8.4V mais recommande une courte utilisation à tension maximale. La pageUS annonce4.8..8.4V. Une alimentation directe sur2S pleine n’est donc pas retenue automatiquement. Une alimentation et un palonnier adaptés restent à choisir avant intégration.',10)
    p.text('Les réservationsFT5335M/UBEC visibles dans la vueR3 conservent l’implantationR2 pour l’étude du faisceau. Elles ne constituent pas une sélection électrique définitivement validée. Le pointD08 l’indique séparément des essais physiques ordinaires.',10)
    p.page('Tension sous charge - scénarios, pas mesures')
    p.text('Hypothèses : fils à80°C, contacts communs2mΩ, contacts propulsion1mΩ, SSR1.5mΩ, branchePi50mΩ, rendements80%, Pi25.75W de sortie. Servo travail1A à6V ; pointe d’étude12A à6V choisie pour le calcul, pas une limite fabricant.',10)
    p.table(['Pack V','Cas','Commun A','Pi VIN V','UBEC VIN V'],[[r['pack_V'],r['scenario'],r['commun_A'],r['Pi_entree_V'],r['UBEC_entree_V']] for r in scenarios],[80,220,140,170,172],10)
    p.text('Critère d’entréePi : ≥5.8V selon l’étude précédente. Une valeur UBEC d’entrée supérieure à6V ne démontre pas sa régulation6V sous pointe. Mesurer les transitoires, les chutes et l’échauffement. FS5A reste candidat suspendu à ces résultats ; ne pas relever son calibre sans revoir toute la branche.',10)
    p.page('Prototype PWM - brochage exact à câbler trois fois')
    p.table(['Composant / boîtier','Broche','Net ou fonction'],[
      ['ISO7710FDR SOIC8-D','1 et3','3.3V Pi ; 100nF versGND_PI'],['ISO7710FDR','2','PWM Pi via220ohms ; rappel10kohms côtéIN'],['ISO7710FDR','4','GND_PI'],['ISO7710FDR','5','GND local de l’actionneur'],['ISO7710FDR','6','Signal vers actionneur via220ohms ; rappel10kohms local'],['ISO7710FDR','7','NC'],['ISO7710FDR','8','3.3V du LDO local ; 100nF versGND local'],['MCP1703A-3302E/DB SOT223','1','VIN du BEC/UBEC local ; 10µF25V versGND local'],['MCP1703A SOT223','2 etTAB','GND local, pas le brochage d’un AMS1117'],['MCP1703A SOT223','3','3.3V local ; 10µF25V versGND local']],[270,70,442],9)
    p.text('CanalG : GPIO12 broche32 ; canalD : GPIO13 broche33 ; servoS : GPIO18 broche12. Les domainesG/D/S restent séparés sur les adaptateurs. La puissance des actionneurs contourne ces adaptateurs. La netlist complète et la nomenclature sont livrées ; aucun PCB/Gerber supplémentaire n’est annoncé.',10)
    p.text('Banc initial sans actionneur niLiPo : sources limitées20mA par canal. Contrôler continuité, tensions et signaux à l’oscilloscope. Le défaut bas ne détecte pas à lui seul unPWM valide figé.',10)
    p.page('Conditions pour poursuivre et recette')
    p.table(['Point','État','Reste à établir'],[[i,s,t] for i,s,t in GATES],[60,200,522],8.7)
    p.text('Aucun achat, essai physique ni message fabricant envoyé. Les questions et le relevé sont prêts ; les réponses absentes ne sont pas remplacées par des valeurs supposées.',9)
    p.page('Sources et fichiers à utiliser')
    for title,url in [('Servo3429','https://www.pololu.com/product/3429'),('Palonnier3431','https://www.pololu.com/product/3431'),('KHK catalogue2025','https://khkgears.net/pdf/2025/spur-gears.pdf'),('LFT et cotes','https://www.littelfuse.com/assetdocs/lft-datasheet?assetguid=56b8955c-9cf7-4814-a923-97a4406bfa77'),('CSA supportLFT','https://www.littelfuse.com/assetdocs/csa-6225-01-007316?assetguid=203ad805-7e22-463f-997a-2431bbdfbbd1'),('TI EVM et Gerbers','https://www.ti.com/tool/TPS3700EVM-114'),('ISO7710','https://www.ti.com/lit/ds/symlink/iso7710.pdf')]:
        p.text(title,10,True);p.text(url,8.5)
    p.text('La fiche Microchip DS20005122C, table3-1 page12, est conservée dans le dossier de surveillance. Les archives téléchargées, leurs empreintes et les échecs de téléchargement figurent dans sources.json. Ne pas confondre fichier introuvable localement et information réellement confirmée.',9)
    p.save()
    doc=pymupdf.open(P/'dossier-complements-r3.pdf');renders=[];T.mkdir(exist_ok=True)
    for i,page in enumerate(doc):
        spans=[s['bbox'] for b in page.get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for s in l['spans']]
        assert all(x0>=18 and x1<=830 and y0>=8 and y1<=589 for x0,y0,x1,y1 in spans),(i,'overflow')
        target=T/f'pdf-page-{i+1:02d}.png';page.get_pixmap(matrix=pymupdf.Matrix(1.25,1.25)).save(target);renders.append(str(target.relative_to(ROOT)))
    dump(V/'pdf.json',dict(page_count=len(doc),renders=renders,all_text_within_pages=True,visual_review_pending=True,sha256=sha(P/'dossier-complements-r3.pdf')))
    print('PDF',len(doc),'pages',flush=True)

def main():
    sys.stdout.reconfigure(encoding='utf-8');scenarios=electrical();docs()
    for folder in [B,A]:
        for p in folder.glob('*.md'):
            text=p.read_text(encoding='utf-8');write(p,'\n'.join(l if '](' in l or '`' in l else display(l) for l in text.splitlines()))
    pdf(scenarios)
if __name__=='__main__':main()
