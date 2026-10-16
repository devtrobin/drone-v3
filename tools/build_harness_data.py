"""Component dossiers, explicit provenance, wiring quantities and study calculations."""
from pathlib import Path
import json,os,math,sys
from urllib.parse import quote_plus
from collect_harness_refs import KLAUKE,AUPROTEC
from harness_text import format_text
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants';COMMON=BASE/'faisceau-puissance'
TE='https://www.te.com/en/product-NB11802001.html'
HTT='https://www.hellermanntyton.com/products/cable-ties-inside-serrated/t18r/111-01919'
HTM='https://www.hellermanntyton.com/au/products/cable-tie-mounts/mb2/151-28210'
ANCOR='https://docs.navico.com/view/362211770/'
PARTS=[
 dict(id='ancor312303',folder='cosses-puissance/ancor-312303',reference='Ancor 312303',role='Cosses jaunes des fils 12 AWG sur les goujons MiniBus #10',quantity=3,mandatory=2,conditional=1,pack=3,
  maker=ANCOR+'24/',amazon_query='Ancor 312303',spec='12–10 AWG, plage catalogue 3–5 mm² ; œillet #10 ; cuivre étamé, joint brasé, isolation thermorétractable avec adhésif.',
  usage='Deux cosses sur les retours CM1− et CM2− en D− N1/N3. La troisième peut raccorder le fil 12 AWG du 5065 Pi à D+ P4 ; elle ne concerne pas automatiquement le retour électronique N4, dont la section doit être arrêtée.',
  dimensions=[['Section admise','3–5 mm² / 12–10 AWG','Catalogue fabricant'],['Taille de goujon','#10, appelée 4,8 mm au catalogue','Taille nominale de vis, pas diamètre du trou'],['Alésage du modèle','5,2 mm','Estimation ; passage sur #10 Ø4,826 à vérifier'],['Enveloppe CAO','24 × 9,6 × 5,9 mm','Estimation complète'],['Rétraction annoncée','135 °C','Catalogue fabricant ; température de la gaine, pas consigne du pistolet']],
  source_files=['notices/Ancor-catalogue-2020-original.pdf'],source_pages='PDF 2020 p.26 ; catalogue en ligne 2024 p.24',
  fit='Section nominale compatible avec le 12 AWG BNTECHGO ; très fins brins, diamètre de gaine 4,5 ±0,1 mm, outil et sertissage à qualifier. La compatibilité avec du 6 mm² n’est pas annoncée.'),
 dict(id='klauke95r4',folder='cosses-puissance/klauke-95r4',reference='Klauke 95R4',role='Cosses 6 mm² des deux bornes de puissance du relais',quantity=2,mandatory=2,conditional=0,pack=100,
  maker=KLAUKE,amazon_query='Klauke 95R4',spec='Cuivre recuit EN13600 étamé ; section 6 mm² ; trou M4 de 4,3 mm ; trou de contrôle de l’insertion ; gamme pour conducteurs fins classe 5.',
  usage='Une sur l’arrivée en relais +2 ; une sur le départ relais 1 vers l’entrée du UD-80A. Les vis #8-32 UNC du relais sont conservées : œillet M4 désigne le passage, pas un nouveau filetage.',
  dimensions=[['d1 / a / b','4 / 9 / 9,5 mm','Tableau Klauke actuel'],['d2 / d4','4,3 / 6 mm','Alésage de vis / diamètre extérieur canon'],['c1 / c2 / l','5 / 5,5 / 18 mm','Repères du dessin de famille'],['Longueur reconstruite','23 mm = c1 + l','l part du centre du trou sur le dessin archivé'],['Paume / inspection','2 mm / Ø1,4 mm','Estimation ; valeurs non publiées']],
  source_files=['notices/Klauke-catalogue-via-PowerCables.pdf'],source_pages='PDF archivé p.14 / imprimée 12 ; outillage PDF p.40 / imprimée38',
  fit='Ø4,3 > diamètre nominal #8 4,166 mm. Vérifier la largeur 9,5 mm, le dégagement des cloisons, l’appui et la longueur utile de vis du relais. Le fil AUPROTEC doit correspondre à une classe de conducteur acceptée : ce point n’est pas certifié par sa page commerciale.'),
 dict(id='klauke95r5',folder='cosses-puissance/klauke-95r5',reference='Klauke 95R5',role='Cosses 6 mm² sur MIDI M5 et MiniBus #10',quantity=5,mandatory=4,conditional=1,pack=100,
  maker=KLAUKE,amazon_query='Klauke 95R5',spec='Cuivre recuit EN13600 étamé ; section 6 mm² ; trou M5 de 5,3 mm ; trou de contrôle ; conducteur fin classe 5 dans la gamme.',
  usage='Deux pour MIDI sortie → D+ P2 ; une sur D+ P3 → relais +2 ; une sur D− N2. Une cinquième serait sur l’entrée MIDI si l’interface batterie retenue utilise ce câble 6 mm². Cette interface reste ouverte.',
  dimensions=[['d1 / a / b','4 / 9 / 9,5 mm','Tableau fabricant'],['d2 / d4','5,3 / 6 mm','Trou de vis / diamètre extérieur canon'],['c1 / c2 / l','6 / 6 / 19 mm','Repères du dessin de famille'],['Longueur reconstruite','25 mm = c1 + l','À distinguer de l seule'],['Paume / inspection','2 mm / Ø1,4 mm','Estimation CAO']],
  source_files=['notices/Klauke-catalogue-via-PowerCables.pdf'],source_pages='PDF archivé p.14 / imprimée12 ; tableau fabricant actuel95R5',
  fit='Trou de 5,3 mm proposé pour M5 Ø5 et #10 Ø4,826. Conserver les écrous M5×0,8 MIDI et #10-32 UNF MiniBus respectivement ; ne pas les permuter. Appui de cosse et couple du lot à contrôler.'),
 dict(id='ancor309203',folder='raccords-12awg',reference='Ancor 309203',role='Manchons sertis pour les deux rallonges positives après ATO30',quantity=2,mandatory=2,conditional=0,pack=3,
  maker=ANCOR+'25/',amazon_query='Ancor 309203',spec='Raccord droit 12–10 AWG / 3–5 mm² ; cuivre étamé, joint brasé, gaine jaune avec adhésif ; pack3.',
  usage='Un raccord par départ entre la sortie 12 AWG du 5065 ATO30 et la queue BNTECHGO positive vers XT60H-F. Les connexions des entrées 16 AWG d’usine des ESC sont conservées.',
  dimensions=[['Section de chaque fil','12–10 AWG / 3–5 mm²','Catalogue fabricant'],['Diamètre / longueur CAO','Ø6,1 × 30 mm','Estimation complète'],['Canon dans CAO','Øint3,3 ; Øext4,8 ; L15 mm','Estimation complète'],['Température de rétraction','135 °C annoncés','Catalogue fabricant']],
  source_files=['notices/Ancor-catalogue-2020-original.pdf'],source_pages='PDF2020 p.27 ; catalogue2024 p.25 ; outil PDF2020 p.54',
  fit='Un seul fil par côté ; ne pas mettre deux fils ou du 6 mm² dans un logement annoncé 3–5 mm². Le sertissage du fil silicone à brins de 0,08 mm et la tenue de sa gaine restent à vérifier.'),
 dict(id='teatum8',folder='gaine-thermoretractable',reference='TE / Raychem ATUM-8/2-0-STK (NB11802001)',role='Isolation des canons nus des cosses 6 mm²',quantity=1,mandatory=1,conditional=0,pack=1,
  maker=TE,amazon_query='Raychem ATUM-8/2-0-STK',spec='Gaine noire double paroi 4:1 ; Øint fourni ≥8 mm ; libre rétreint ≤2 mm ; paroi totale rétreinte 1,0 ±0,3 mm, adhésif nominal0,5 mm ; STK1,2 m.',
  usage='Passer les morceaux avant le sertissage des sept cosses nues prévues, dont une conditionnelle côté batterie. Huit coupes de 20 mm, réserve comprise, sont une estimation d’approvisionnement ; les longueurs définitives suivent les canons reçus et le recouvrement sur la gaine du fil.',
  dimensions=[['Øint fourni / libre rétreint','8 mm min / 2 mm max','Plan TE A2,2023'],['Paroi totale / adhésif','1,0 ±0,3 / 0,5 nominal mm','Après rétraction libre'],['Retrait longitudinal','0 à −15 %','Plan TE A2 actuel ; ne pas reprendre −10 % par défaut'],['Longueur STK','1,2 m','Fiche TE05/24 ; conditionnement distributeur à confirmer'],['Températures','Début80 °C ; pleine rétraction110 °C ; service−55..+110 °C','Fiche TE05/24']],
  source_files=['notices/TE-ATUM-fiche-via-Raytronics.pdf'],source_pages='Plan TE A2 et fiche05/24 consultés en ligne ; PDF Raytronics secondaire conservé',
  fit='8 mm passe nominalement au-dessus du canon Klauke Ø6 ; 2 mm libre peut se resserrer sur la gaine Ø4,7. L’état final sur ces surfaces n’a ni Ø2 ni la paroi libre de1mm. Vérifier diamètre de la transition, accès, recouvrement, chauffe locale et état du PVC. Ne pas couvrir la paume de contact.'),
 dict(id='htt18r',folder='maintien-faisceau/colliers',reference='HellermannTyton T18R 111-01919',role='Colliers PA66 naturels pour l’intérieur',quantity=12,mandatory=0,conditional=12,pack=100,
  maker=HTT,amazon_query='HellermannTyton 111-01919 T18R',spec='100 ×2,5 mm ; épaisseur1mm ; PA66 naturel ; 80N résistance minimale de boucle ; faisceau1,5–22mm ; non réutilisable ; non stabilisé UV.',
  usage='Quantité d’étude12, à arrêter après implantation. Maintien sur embases MB2 sans écraser la gaine ; prévoir une boucle de service et retenir les fils avant les raccords.',
  dimensions=[['Sangle','100 ×2,5 ×1,0 mm','Fiche actuelle111-01919'],['Tête nominale actuelle','4,8 ×4,45 ×3,7 mm','Page fabricant, variante111-01919'],['Plan famille2025','T1,1±0,2 ; tête4,8 ; hauteur3,5±0,2mm','Document générique différent, pas fusionné aux cotes actuelles'],['Plage / tenue','Øfaisceau1,5–22 mm ; 80N','80N n’est pas la force de pose'],['Couleur / température','Naturel ; −40..+85 °C','Ne pas acheter la variante noire en la confondant']],
  source_files=['notices/HT-T18R-11101919-fiche-originale.pdf','notices/HT-T18R-plan-original.pdf'],source_pages='Fiche créée9Oct2026 ; dessin famille rev10.1 du5Dec2025',
  fit='Compatible avec la plage T18–T50 annoncée du MB2 et sa largeur maximale de collier5mm. Dents, verrou et pose CAO estimés ; aucune force de serrage qualifiée. Réservé à l’usage intérieur retenu.'),
 dict(id='htmb2',folder='maintien-faisceau/embases',reference='HellermannTyton MB2 151-28210',role='Embases noires à une vis M4',quantity=8,mandatory=0,conditional=8,pack=100,
  maker=HTM,amazon_query='HellermannTyton MB2 151-28210',spec='20,5 ×12,5 ×3,3 mm ; trouØ5mm pour fixation M4 ; collier≤5mm ; PA66 noir ; passage deux directions ; pas de semelle adhésive.',
  usage='Quantité d’étude8, à répartir après implantation. Vis M4, rondelle et éventuel écrou séparés ; leur longueur dépend de l’épaisseur du châssis et du dégagement sous celui-ci.',
  dimensions=[['Enveloppe L/W/H','20,5±0,5 /12,5±0,5 /3,3±0,2mm','Plan141622 ancien ; nominal actuel concordant'],['Trou F','Ø5,0±0,2mm','Plan141622'],['D / E / G / H','2,5 /5,0 /10,0 /1,7mm (±0,2)','Repères du plan, pas tous les noms de champs web'],['Collier / vis','Largeur max5mm / visM4','Page actuelle'],['Trou et rayons CAO','Position du trou et arrondis reconstitués','Plan sans toutes les coordonnées']],
  source_files=['notices/HT-MB2-plan-original.pdf'],source_pages='Plan14162215Oct2002 ; page actuelle151-28210',
  fit='Collier T18R2,5mm admis nominalement. Les 5mm du trou sont un jeu pour une visM4 ; ne pas choisir une visM5 par cette seule cote. Vérifier fixation sur le châssis et éviter un chemin de frottement.'),
 dict(id='auprotec6',folder='cable-principal-6mm2',reference='AUPROTEC FLRY-B 6,00 mm² rouge / noir',role='Câble principal et liaison relais → entrée UD-80A',quantity=4,mandatory=0,conditional=4,pack=None,
  maker=AUPROTEC,amazon_query='AUPROTEC FLRY B 6 mm2 rouge noir',spec='Cuivre ECu nu recuit99,99 % annoncé ; PVC ShoreA90 ; Øextérieur env4,7mm ; brins maxØ0,300mm, nombre non publié ; −40..+70 °C ; 50VAC/60VDC.',
  usage='Provision d’étude2m rouge et2m noir, pas liste de coupe. Le SKU fabricant réellement consulté044906 est une couronne rouge6m ; SKU du lot2m et variante noire exacte à confirmer. Ne pas déduire un prix au mètre ni une offre rouge/noir du seul SKU6m.',
  dimensions=[['Section / OD','6,00mm² / envØ4,7mm','Page fabricantFLRY-B6'],['Brins','Ømax0,300mm ; nombre et toronnage inconnus','Ne pas inventer un nombre de brins'],['Température / tension','−40..+70 °C ; 50VAC/60VDC','Page fabricant ; les annonces+85/+105 ne sont pas retenues'],['Âme du modèle','Cylindre d’aire6mm², Øéquivalent2,764mm','Représentation pédagogique, pas OD cuivre réel'],['Longueur / dénudage CAO','100/10mm ; coupe40mm','Exemples, pas consignes de montage']],
  source_files=['sources-web/AUPROTEC-FLRYB6.html'],source_pages='Page primaire rouge6m044906 archivée ; famille noir à vérifier dans l’offre achetée',
  fit='6mm² respecte nominalement le minimum6mm² de l’entrée UD-80A. 10AWG≈5,26mm² ne le respecte pas. Classe du cuivre, acceptation fine brins, embout éventuel et longueur de dénudage UD du lot restent à confirmer. Ne pas enfiler ce câble dans un XT60 sans accord de ses cotes et spécifications.')]

def dump(p,obj):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def write(p,text):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.is_relative_to(COMMON) or any(p.is_relative_to(BASE/i['folder']) for i in PARTS):text=format_text(text)
    p.write_text(text.rstrip()+'\n',encoding='utf-8')
def rel(target,start):return Path(os.path.relpath(target,start)).as_posix()

def main():
    sys.stdout.reconfigure(encoding='utf-8');COMMON.mkdir(parents=True,exist_ok=True)
    for item in PARTS:
        f=BASE/item['folder'];common=rel(COMMON/'README.md',f);notice=rel(COMMON/'notices/notice-faisceau-puissance-v3.pdf',f)
        quantity_unit=' m' if item['id']=='auprotec6' else ''
        item['amazon_search']='https://www.amazon.fr/s?k='+quote_plus(item['amazon_query']);item['amazon_FR_verified']=False;item['price_EUR_TTC']=None
        dump(f/'sources.json',dict(checked_on='2026-10-14',selection=item,manufacturer_source_verified=True,hardware_measured=False,
            model_3d_created=True,model_3d_manifest='3D/provenance.json',source_archive_manifest=rel(COMMON/'assets.json',f),
            exact_reviews_verified=False,qualification_complete=False))
        write(f/'README.md',f'''# {item['reference']}

**{item['role']}.** Choix d’étude V3, non acheté et non testé.

{item['spec']}

## Utilisation et quantité

{item['usage']}

Besoin proposé : **{item['quantity']}{quantity_unit}** ({item['mandatory']}{quantity_unit} ferme pour les raccordements décrits, {item['conditional']}{quantity_unit} conditionnel ou d’implantation). Conditionnement fabricant indiqué : **{item['pack'] or 'selon variante'}**, sans garantie du conditionnement vendeur.

## Achat et sources

[Source fabricant]({item['maker']}) ; [recherche Amazon.fr par référence]({item['amazon_search']}). **Aucune offre Amazon.fr exacte, aucun prix TTC ou délai confirmé.** Une recherche n’est pas une fiche produit et n’atteste pas du stock. Les équivalents éventuels doivent être contrôlés, pas acceptés par couleur.

{item['source_pages']}. [Archives et recherche]({rel(COMMON/'recherche-technique.md',f)}).

## Montage et compatibilité

{item['fit']}

[Cotes et limites](cotes.md), [notice de préparation du faisceau]({notice}), [modèles STEP, aperçus et provenance](3D/README.md), [nomenclature et raccordements]({common}).
''')
        rows=['# Cotes et fidélité - '+item['reference'],'','Toutes les dimensions sont en millimètres sauf indication.','',
            '| Grandeur | Valeur | Statut |','| --- | --- | --- |']
        rows += ['| '+' | '.join(r)+' |' for r in item['dimensions']]
        rows+=['',item['fit'],'','La CAO reprend les cotes documentées disponibles et indique les détails estimés dans chaque JSON. Il ne s’agit pas de CAO native ni d’un relevé du matériel. Les versions en coupe sont volontaires.','',f'[Source fabricant]({item["maker"]}), [fiche](README.md).']
        write(f/'cotes.md','\n'.join(rows))
        write(f/'notices/README.md',f'# Notice - {item["reference"]}\n\n[Notice V3 commune]({rel(COMMON/"notices/notice-faisceau-puissance-v3.pdf",f/"notices")}). Elle couvre les repères, quantités, préparation, outillage et contrôles.\n\nLes PDF sources sont conservés sans modification dans le [dossier commun]({rel(COMMON/"notices/README.md",f/"notices")}) : {item["source_pages"]}.\n\nLa notice du projet ne remplace pas les instructions du lot reçu.')
        write(f/'avis-utilisateurs.md',f'# Avis et retours - {item["reference"]}\n\nAucun avis de la référence exacte sur un lot Amazon.fr confirmé, aucune note chiffrée extrapolée. Voir la [recherche commune]({rel(COMMON/"recherche-technique.md",f)}). Les témoignages génériques Ancor concernent la famille, pas notre montage ni ses courants.\n\n[Source fabricant]({item["maker"]}) pour les caractéristiques ; [fiche composant](README.md).')
    connections=[
        dict(wire='CP1+',path='MIDI sortie → D+ P2',color='rouge',section=6,ends=['95R5','95R5'],status='hors interface batterie'),
        dict(wire='CP2+',path='D+ P3 → relais +2',color='rouge',section=6,ends=['95R5','95R4'],status='hors interface batterie'),
        dict(wire='CP3+',path='relais1 → UD-80A IN',color='rouge',section=6,ends=['95R4','borne UD / embout à qualifier'],status='borne lot à qualifier'),
        dict(wire='CP0+',path='interface batterie → MIDI entrée',color='rouge',section=6,ends=['interface ouverte','95R5 conditionnelle'],status='interface batterie non arrêtée'),
        dict(wire='CP0-',path='interface batterie → D− N2',color='noir',section=6,ends=['interface ouverte','95R5'],status='interface batterie non arrêtée'),
        dict(wire='CM1-',path='XT60H-F1 → D− N1',color='noir',section='12AWG',ends=['XT60 soudé','Ancor312303'],status='sertissage à qualifier'),
        dict(wire='CM2-',path='XT60H-F2 → D− N3',color='noir',section='12AWG',ends=['XT60 soudé','Ancor312303'],status='sertissage à qualifier'),
        dict(wire='CM1+',path='5065 ATO30 ESC1 → XT60H-F1',color='rouge',section='12AWG',ends=['Ancor309203','XT60 soudé'],status='sertissage à qualifier'),
        dict(wire='CM2+',path='5065 ATO30 ESC2 → XT60H-F2',color='rouge',section='12AWG',ends=['Ancor309203','XT60 soudé'],status='sertissage à qualifier')]
    dump(COMMON/'nomenclature.json',dict(checked_on='2026-10-14',parts=PARTS,connections=connections,
        purchase_made=False,exact_total_EUR=None,battery_interface_final=False,hardware_qualified=False,
        excluded=['manchon3-5mm2 sur6mm2','substitution10AWG pour entree UD minimum6','ecrou M5 sur#10-32','classe6 supposée pour câble FLRY-B']))
    I=40+25/(6.4*.9)+.05;rho=.01724
    rows=[]
    for length in [.20,.25,.50]:
        R=2*length*rho/6;rows.append(dict(one_way_length_m=length,current_A=I,loop_resistance_ohm=R,drop_V=I*R,loss_W=I*I*R))
    dump(COMMON/'calculs.json',dict(section_main_mm2=6,main_current_study_A=I,main_current_formula='40+25/(6.4*0.9)+0.05',
        copper_rho_assumed_ohm_mm2_per_m_at_20C=rho,resistance_measured=False,cable_ampacity_verified=False,loops=rows,
        stud_passages=[dict(part='95R4',hole_mm=4.3,stud_major_nominal_mm=4.1656),dict(part='95R5 M5',hole_mm=5.3,stud_major_nominal_mm=5),dict(part='95R5 #10',hole_mm=5.3,stud_major_nominal_mm=4.826)],
        shrink=dict(expanded_inside_min_mm=8,free_recovered_max_mm=2,lug_barrel_OD_mm=6,wire_OD_approx_mm=4.7,installed_fit_verified=False)))
    table=['| Composant | Besoin d’étude | Dossier |','| --- | --- | --- |']
    for i in PARTS:table.append(f'| {i["reference"]} | {i["quantity"]}'+(' m' if i['id']=='auprotec6' else '')+f' | [Documentation]({rel(BASE/i["folder"]/"README.md",COMMON)}) |')
    write(COMMON/'README.md','''# Faisceau de puissance - Drone V3

**Huit références d’étude**, réparties par composant : trois cosses, un raccord droit, une gaine adhésive, un collier, une embase et une famille de fil principal. Aucun achat effectué ; les offres Amazon.fr, variantes et prix TTC restent à confirmer.

'''+ '\n'.join(table)+'''

Le câble principal est retenu en section nominale **6 mm²**. Les manchons Ancor 12–10 AWG ont une plage publiée **3–5 mm²** et servent uniquement aux queues moteurs 12 AWG. Les cosses 95R4/95R5 concernent le 6 mm². Les écrous et vis restent ceux des appareils : M5 MIDI, #10-32 MiniBus et #8-32 relais.

[Notice PDF](notices/notice-faisceau-puissance-v3.pdf), [raccordements et préparation](integration.md), [recherche et avis](recherche-technique.md), [nomenclature](nomenclature.json), [calculs](calculs.json), [quatorze STEP colorés](3D/README.md), [validation du dossier](validation-dossier.json).

La prise commune XT60 de la batterie demeure à qualifier pour le scénario 44,39 A ; le remplacement des fils par du 6 mm² ne prouve pas sa tenue. Les deux XT60H-F des branches moteurs sont distinctes de cette prise. Aucun courant d’étude n’est une limite imposée par le matériel.

Les longueurs, quantités de maintien et accessoires de visserie seront arrêtés après implantation. Aucun des STEP ne sert de calibre de sertissage ni de plan d’usinage validé.
''')
    lines=['# Raccordements et notice de montage du projet','','| Repère | Chemin | Section / couleur | Terminaisons | Statut |','| --- | --- | --- | --- | --- |']
    for c in connections:lines.append(f'| {c["wire"]} | {c["path"]} | {c["section"]} /{c["color"]} | '+ ' ; '.join(c['ends'])+' | '+c['status']+' |')
    lines += ['', '''Les sorties UD S1/S4 utilisent les fils 12 AWG déjà inclus dans les 5065 ; il ne faut pas rajouter un autre fil dans le même port. Le 5065 Pi peut recevoir la troisième312303 sur son arrivée D+P4. Le retour électronique D−N4 et les petits fils de commande ont une section encore à définir. D+P1 reste libre.

## Quantités de terminaisons

Deux Ancor312303 pour les retours moteurs, avec une troisième conditionnelle pour P4 ; deux309203 plus un spare dans le pack3 ; deux95R4 ; quatre95R5 hors extrémité positive de l’interface pack, plus une cinquième conditionnelle en entrée MIDI. Sept gaines de cosse prévues si cette cinquième est retenue. Un stock de huit morceaux20mm inclut une réserve, mais ne constitue pas la liste de coupe.

## Préparation et outillage

1. Débrancher pack et équilibrage. Positionner les pièces et relever les chemins ; choisir les longueurs sans tension sur les connexions et prévoir maintien et dégagement.
2. Vérifier références, matières, section, diamètre de gaine, passage des œillets, largeur d’appui et état. Mesurer le lot ; aucun brin retiré pour faire entrer un fil.
3. Passer capots et gaines avant terminaison. Régler le dénudage sur le canon réel et la procédure de l’outil ; 10mm du modèle du fil est illustratif. Aucun dénudage de17mm appliqué automatiquement à une cosse de9mm.
4. Ancor : outil à cliquet pour cosses thermorétractables, plage12–10AWG jaune. Le catalogue2020 p.54 cite **703010** pour heat-shrink ; la double pince703030 y est destinée aux nylon/vinyle. Un sertissage de cuivre et une rétraction de gaine sont deux opérations distinctes. Sur un manchon, terminer chaque côté séparément selon l’outil ; ne pas sertir seulement le centre.
5. Klauke : outil/matrice pour cosses tubulairesCu standard6mm², selon la table fabricant PDFp.40. La K2 figure parmi les outils0,75–16mm² ; faire confirmer la combinaison95R4/95R5, câble réel et procédure du lot. Ne pas prendre par défaut une matrice de cosse isolée Ancor.
6. Sertir sans ajouter de soudure non prévue. Contrôler insertion et absence de brins libres ; sur Klauke utiliser le trou de contrôle. Faire des éprouvettes avec le fil réel et contrôler tenue, section du sertissage et résistance avant les raccords définitifs. La force d’essai suit le système documenté, aucune force universelle inventée.
7. Ancor : rétraction135°C annoncée. ATUM : début80°C, rétraction complète110°C. Ces valeurs ne sont pas la consigne du pistolet. Chauffer localement selon le lot, préserver le PVC et les éléments voisins, puis inspecter l’adhésif et la gaine. Ne pas masquer les surfaces de contact et ne pas réchauffer un pack branché.
8. Monter une seule cosse prévue par borne du relais, sans empilement arbitraire. Garder les vis et écrous d’origine et suivre le couple indiqué pour le lot de chaque appareil. Ne pas remplacer une #8-32 par une M4 ou une #10-32 par une M5.
9. UD-80A : admission des fins brins et embout à confirmer. La fiche IEC décrit17mm/3,5Nm ; l’alternativeUL décrit9,14mm/2,2Nm. Suivre les instructions du lot et du système choisi. Ni une moyenne ni l’application aux cosses n’est justifiée. Un embout n’est pas encore une référence sélectionnée.
10. Fixer les MB2 avec visM4 adaptées au châssis ; vis non incluses présumées. Poser les T18R sans écraser le câble, couper la queue proprement, protéger les arêtes et garder les fils hors roues, courroies, engrenages et ailettes chaudes. Ne pas serrer les colliers à80N : c’est une résistance de boucle annoncée.
11. Contrôler continuité, polarité, isolement, serrages et aucun contact de puissance exposé. Vérifier ensuite sous alimentation supervisée et limitée adaptée, courant et chutes de tension, température des câbles, cosses, prises et protections durant l’usage réel. Les ATO30 et le MIDI60 ne limitent pas le courant à20/44A.

## Dimensionnement restant à qualifier

Le scénario utilise20A par ESC,40A total moteurs, et44,39A commun avec Pi et surveillance. Le 6mm² est une section d’étude ; ni son ampacité dans l’implantation ni sa protection en défaut ne sont validées par le tableau de résistivité. L’interface communeXT60 du pack, les pointes, les fils16AWG d’usine et la coordination des fusibles restent à qualifier. Aucun godet XT60 n’est agrandi, aucun pack modifié.

Le servo reçoit un seul BEC6V ; l’autre positifBEC est isolé. Les phases moteurs, fils de commande et liaison caméra ne sont pas concernés par ces raccords de puissance.

Les notices antérieures sont des états datés. Cette sélection complète leurs mentions « cosses/raccords à choisir » sans déclarer le matériel testé.

[Dossier commun](README.md), [nomenclature](nomenclature.json), [calculs](calculs.json), [notice PDF](notices/notice-faisceau-puissance-v3.pdf).
''']
    write(COMMON/'integration.md','\n'.join(lines))
    write(COMMON/'recherche-technique.md',f'''# Recherche, ambiguïtés et avis - 14 octobre2026

## Sources primaires

- [Ancor catalogue2024 p.24]({ANCOR}24/) et [p.25]({ANCOR}25/) : références et plage3–5mm². Catalogue2020 conservé via ProjectK : PDFp.26,27,54 ; matière, gaine et outillage. Les mesures extérieures exactes des312303/309203 ne sont pas publiées dans les sources consultées.
- [Klauke tableau actuel]({KLAUKE}) : huit cotes des95R4/95R5. Catalogue fabricant ancien viaPowerCables conservé : PDFp.14, plan de famille et valeurs6mm² concordantes. Le dessin montre **l depuis centre trou**. Une fiche marchande qui appelle l18mm une longueur totale ne remplace pas ce repère ; enveloppes CAO23/25mm. Le tableau ancien4mm² présente une différence de l avec l’actuel, sans incidence sur nos lignes6mm². Outil tableauPDFp.40.
- [TE NB11802001]({TE}), [planATUM4:1A2](https://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocFormat=pdf&DocLang=English&DocNm=ATUM_4_to_RATIO_STANDARD_SIZES&DocType=Customer+Drawing&PartCntxt=NB11802001), [ficheTE05/24](https://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocFormat=pdf&DocLang=English&DocNm=atum-tubing&DocType=Data+Sheet&PartCntxt=NB11802001) consultés via recherche web. Téléchargements directs403, pas de faux original local. La fiche **Raytronics est secondaire**, conservée en complément ; ses tolérances plus simples ne remplacent pas la paroi1±0,3 et le retrait0..−15% du planTE. HIS-A9/3 a été envisagée, non retenue ; aucune de ses valeurs n’est mélangée à ATUM8/2.
- [T18R111-01919]({HTT}), fiche9Oct2026 et dessin famille10.1 de2025 archivés. Variante **naturelle**, pas noire ; cotes du plan générique légèrement différentes de la page actuelle, signalées. DessinMB2 [141622](https://www.hellermanntyton.com/shared/assets/CAD_141622.pdf) archivé ; [page actuelle]({HTM}) concordante pour l’enveloppe, trou5mm et visM4. Pas une embase adhésive carrée. Les petites imagesKlauke de la page sont des vignettes57×57 ; on n’en déduit pas des cotes.
- [AUPROTEC FLRY-B6rouge6m044906]({AUPROTEC}) archivé : cuivreECu99,99% annoncé, PVC, Øenv4,7mm,−40..+70°C, brinsmax0,300mm. Nombre et construction exacte de brins inconnus. Les autres noms FLY,10AWG ou annonces +85/+105°C ne prouvent pas la même variante. Les modèles gardent une âme équivalente sans brins inventés.

## Recherche d’achat

Des recherches par référence ont été faites sur Amazon.fr pour chaque composant. Pages vides ou challenges antirobot : **aucun stock, prix, vendeur ou livraison française attesté**. Les liens de chaque fiche ouvrent une recherche, pas une offre confirmée. L’ASIN candidat AUPROTEC **B00HDGB6GG** apparaît dans des reprises marchandes pour rouge5m ; pages Amazon.com/fr bloquées, référence exacte non vérifiée. Ce n’est pas le SKU primaire044906 rouge6m et ce n’est pas une paire rouge/noir.

Le conditionnement constructeur100 de Klauke/T18R/MB2 ne prouve pas l’obligation d’acheter100 chez un distributeur. Rechercher la vente au détail adaptée au besoin et l’offre exacte avant budget ; aucun total artificiel n’est calculé avec des prix d’autres pays. Pour ATUM, TE indique une référence active mais vente directe indisponible lors de consultation ; cela ne décrit pas le stock de tous les distributeurs.

## Retours d’utilisateurs et vidéo

Recherche par SKU et par famille, notamment forums et YouTube. Aucun essai spécifique312303/309203 avec filBNTECHGO680brins, ni qualification de notre faisceau à44,39A trouvé. Aucun avis exact exploitable pour95R4/95R5,ATUM8/2,T18R111-01919,MB2 ou varianteFLRYB retenue.

[GarageJournal,2019](https://www.garagejournal.com/forum/threads/knipex-crimpers-for-heat-shrink-splice-connectors.415007/) rapporte l’utilisation de raccords et cosses Ancor avec une pince à cliquet qui préserve leur gaine. [YBW,2021](https://forums.ybw.com/threads/recommendations-for-heat-shrink-crimp-connectors.563339/) est favorable à la familleAncor et discute son prix. Ces retours génériques ne confirment ni notre référence précise ni la performance électrique ; aucun procédé artisanal du forum n’est adopté comme notice. Aucun score utilisateur inventé ni transfert d’avis d’une autre référence. Les recommandations de montage sont fondées sur les documents fabricant, pas sur ces témoignages.

## Limites des modèles et de l’étude

Tous les STEP sont des reconstructions colorées, pas des fichiers natifs. Cotes Ancor et détails de serrures/dents estimés ; paume, transition et inspectionKlauke estimées autour des cotes publiées. ATUM : deux états libres et une coupe, pas simulation de la pose. Fils droits et dénudages sont illustratifs. Modèles sans défauts géométriques ne prouvent pas tenue mécanique, section réellement livrée, qualité de cuivre, isolation ou ampacité.

[Archives avecSHA256 et statuts](assets.json), [raccordements](integration.md), [catalogue3D](3D/README.md).
''')
    assets=json.loads((COMMON/'assets.json').read_text(encoding='utf-8'))['assets']
    orig=['# Notices et documents sources','','[Notice V3 de préparation du faisceau](notice-faisceau-puissance-v3.pdf). Document du projet ; les sources suivantes sont conservées inchangées.','','| Archive | Nature |','| --- | --- |']
    for a in assets:
        if a['status']=='downloaded' and a['file'].endswith('.pdf'):
            kind='Fiche secondaire Raytronics' if 'Raytronics' in a['file'] else 'Document fabricant, directement ou via miroir public'
            orig.append(f'| [{Path(a["file"]).name}]({Path(a["file"]).name}) | {kind} |')
    orig+=['','[URLs, intégrité, refus de téléchargement](../assets.json), [recherche et variantes](../recherche-technique.md). Les PDFTE actuels ont été consultés en ligne mais leurs téléchargements directs ont été refusés ; ne pas présenter la ficheRaytronics comme un originalTE.','']
    write(COMMON/'notices/README.md','\n'.join(orig))
    dump(COMMON/'sources.json',dict(checked_on='2026-10-14',references=[dict(reference=i['reference'],url=i['maker']) for i in PARTS],
        exact_Amazon_FR_offers_verified=False,price_TTC_verified=False,hardware_tested=False,source_archives='assets.json',current_TE_documents_web_verified=True))
    write(COMMON/'photos/README.md','# Images sources\n\nLes images Klauke sont les petites vignettes de la page constructeur, archivées sans modification. Elles ne constituent pas des plans cotés. La vignette initialement appelée « plan-famille » est un logoUL : exclue de toute reconstruction. Les dimensions viennent du tableau actuel et du dessin de famille dans le catalogue.\n\n[Archives](../assets.json), [recherche](../recherche-technique.md).')
    # Update only current textual indexes; historical PDF documents retain their dates.
    for path,prefix in [(BASE/'README.md',''),(ROOT/'ReadMe.md','Composants/')]:
        text=path.read_text(encoding='utf-8');marker='<!-- faisceau-puissance-v3 -->'
        if marker not in text:
            text+=f'\n{marker}\n\nLe [faisceau de puissance]({prefix}faisceau-puissance/README.md) complète la sélection : cosses Ancor12AWG, cosses Klauke6mm², manchons, ATUM8/2, colliers, embases et fil FLRY-B6mm². Huit dossiers, notice, sources, cotes et [quatorze STEP]({prefix}faisceau-puissance/3D/README.md). Les mentions antérieures « à choisir » sont complétées par cette étude datée du14octobre2026 ; offresAmazon.fr, implantation, interface batterie et qualification matérielle restent ouvertes.\n'
            write(path,text)
    for folder in ['cable-puissance-12awg','connecteurs-alimentation','protection-branches-moteurs','distribution-alimentation','repartition-moteurs','protection-surintensite']:
        path=BASE/folder/'integration.md'
        if not path.exists():path=BASE/folder/'README.md'
        text=path.read_text(encoding='utf-8');marker='<!-- faisceau-puissance-v3 -->'
        if marker not in text:write(path,text+f'\n{marker}\n\nComplément du14octobre2026 : [cosses, raccords, gaine, maintien et câble principal]({rel(COMMON/"README.md",path.parent)}), avec [raccordements et notice de préparation]({rel(COMMON/"integration.md",path.parent)}). Sélection d’étude, sans achat ni qualification matérielle.\n')
    print('DATA',len(PARTS),'component dossiers; connections',len(connections),'; current',round(I,3),flush=True)
if __name__=='__main__':main()
