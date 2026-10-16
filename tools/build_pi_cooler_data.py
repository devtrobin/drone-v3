"""Document the selected SC1148, verified French offer and qualification limits."""
from pathlib import Path
from html.parser import HTMLParser
import re,html,json,sys,hashlib
from collect_pi_cooler_refs import MAKER,PORTAL
from pi_cooler_text import fmt
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/refroidissement-raspberry-pi-5'
AMAZON='https://www.amazon.fr/dp/B0CLXZBR5P'
HARDWARE='https://www.raspberrypi.com/documentation/computers/raspberry-pi.html'

class Element(HTMLParser):
    def __init__(self,id):super().__init__(convert_charrefs=True);self.id=id;self.stack=[];self.text=[];self.done=False
    def handle_starttag(self,tag,attrs):
        if self.done:return
        if not self.stack and dict(attrs).get('id')==self.id:self.stack=[tag];return
        if self.stack and tag not in ['br','img','input','meta','link','hr','area','source','wbr']:self.stack.append(tag)
    def handle_endtag(self,tag):
        if self.stack and tag in self.stack:
            pos=len(self.stack)-1-self.stack[::-1].index(tag);self.stack=self.stack[:pos]
            if not self.stack:self.done=True
    def handle_data(self,data):
        if self.stack and not any(t in self.stack for t in ['script','style']):self.text.append(data)
def element(s,id):
    obj=Element(id);obj.feed(s);return re.sub(r'\s+',' ',' '.join(obj.text)).strip()
def dump(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def write(p,s):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.is_relative_to(BASE):s=fmt(s)
    p.write_text(s.rstrip()+'\n',encoding='utf-8')
def main():
    sys.stdout.reconfigure(encoding='utf-8');s=(BASE/'sources-web/Amazon-FR-B0CLXZBR5P.html').read_text(encoding='utf-8')
    title=element(s,'productTitle');price=element(s,'corePrice_feature_div');stock=element(s,'availability');rating=element(s,'averageCustomerReviews')
    seller=element(s,'tabular-buybox');seller=seller or element(s,'tabular-buybox-container')
    assert 'Raspberry Pi' in title and '6,99' in price and '5 exemplaire' in stock
    assert 'SC1148' in s and '05056561803357' in s and 'B0CLXZBR5P' in s
    offer=dict(checked_on='2026-10-14',ASIN='B0CLXZBR5P',manufacturer_part='SC1148',url=AMAZON,title=title,
        price_displayed_EUR=6.99,VAT_included_page_statement=True,availability_displayed=stock,
        rating_displayed=rating,merchant_panel_displayed=seller or None,
        delivery_condition='Livraison gratuite proposée pour une première commande, date affichée21octobre2026 ; à vérifier selon compte et adresse',
        order_made=False,shipping_cost_guaranteed=False,seller_independently_qualified=False,
        source_file='sources-web/Amazon-FR-B0CLXZBR5P.html',source_sha256=hashlib.sha256((BASE/'sources-web/Amazon-FR-B0CLXZBR5P.html').read_bytes()).hexdigest())
    dump(BASE/'achat-amazon.json',offer);print('OFFER',title,'6.99EUR',stock,'SELLER',seller[:300],flush=True)
    dump(BASE/'nomenclature.json',dict(selected_on='2026-10-14',reference='Raspberry Pi Active Cooler SC1148',quantity=1,ASIN='B0CLXZBR5P',
        price_displayed_EUR=6.99,shipping_cost_final_EUR=None,purchase_made=False,
        factory_components=['dissipateur aluminium anodisé','ventilateur radial avec son capot et trois vis','deux attaches blanches à ressort','pads thermiques préposés','cordon quatre fils et fiche'],
        extra_separate_purchases_required_for_basic_mount=False,actual_box_checked=False))
    dump(BASE/'sources.json',dict(checked_on='2026-10-14',reference='SC1148',quantity=1,manufacturer_product=MAKER,manufacturer_portal=PORTAL,
        mechanical_reference_mm=dict(width=63.5,length=42.5,total_height_with_clips=13.7,fan_footprint=[30,30],production_dimensions=False),
        electrical=dict(supply_V=5,header='Pi5 FAN JST-SH4pins,1mm',pins=[dict(pin=1,function='+5V',color='rouge'),dict(pin=2,function='PWM',color='bleu'),
            dict(pin=3,function='GND',color='noir'),dict(pin=4,function='TACH',color='jaune')],current_active_cooler_not_published_in_brief=True,
            USB_budget_shared_with_fan=True,case_fan_60mA_not_transferred_to_ActiveCooler=True),
        fan=dict(airflow_max_CFM=1.09,rpm_max_nominal=8000,rpm_tolerance_percent=15,MTTF_hours_at_25C=379000),
        primary_brief_edition='January2026',portal_plan_updated='2025-10-06',portal_brief_updated='2026-01-09',
        current_control_profile=dict(temperature_rising_C=[50,60,67.5,75],duty_percent=[30,50,70,100],hysteresis_C=5,source=HARDWARE,actual_OS_verified=False),
        Amazon_FR_page_verified=True,Amazon_FR_offer_observed=True,purchase_evidence='achat-amazon.json',assets='assets.json',
        manufacturer_STEP_found=False,model_3d_created=True,model_3d_manifest='3D/provenance.json',hardware_tested=False,
        installed_height_verified=False,video1080p60_validated_by_cooler=False))
    rows=[]
    for I in [.05,.10,.20,.40]:
        P=5*I;rows.append(dict(fan_current_example_A=I,fan_power_W=P,energy20min_Wh=P/3,energy45min_Wh=P*.75))
    dump(BASE/'calculs.json',dict(example_only=True,measured_fan_current_A=None,rated_fan_current_claimed=False,
        supply_V=5,current_examples=rows,USB_current_budget_shared=True,Pi_branch25W_study_already_includes_fan=True,
        autonomy_verified=False,airflow_m3_per_h_ideal_unit_conversion=1.09*.028316846592*60))
    write(BASE/'README.md',f'''# Refroidissement du Raspberry Pi5 - Active Cooler SC1148

**Référence retenue : Raspberry Pi Active Cooler officiel SC1148, une unité.** Dissipateur en aluminium anodisé avec ventilateur radial régulé, pads thermiques préposés, deux attaches à ressort et cordon quatre fils. Non acheté, non testé.

## Achat Amazon et devis

[Fiche Amazon.fr identifiée]({AMAZON}), ASIN **B0CLXZBR5P**. Relevé du **14octobre2026 : 6,99€ TTC**, stock affiché5 exemplaires. Le titre français est générique, mais les détails du produit indiquent **SC1148**, Raspberry Pi et le GTIN05056561803357. La fiche américaine correspond au même identifiant.

La page propose une livraison gratuite pour une première commande, au21octobre dans le contexte consulté ; **ce n’est pas un port garanti pour notre panier**. Vérifier au paiement vendeur, contenu, compte et frais. Aucune commande effectuée. [Relevé structuré et source archivée](achat-amazon.json).

## Documents et modèle

- [Notice PDF V3](notices/notice-active-cooler-pi5-v3.pdf) et [PDF fabricant originaux](notices/README.md).
- [Cotes publiées et estimations](cotes.md).
- [Intégration, brochage et contrôles](integration.md).
- [Recherche technique et avis](recherche-technique.md).
- [Photos originales et crédits](photos/README.md).
- [Quatre variantes STEP, aperçus et provenance](3D/README.md), dont une version d’implantation légère.
- [Nomenclature](nomenclature.json), [sources](sources.json), [calculs](calculs.json) et [validation du dossier](validation-dossier.json).

Le refroidisseur se branche sur **FAN**, pas sur les sorties PWM12/13/18 réservées aux deux ESC et au servo. Le ventilateur partage le budget des périphériques USB ; son courant doit être mesuré avec la caméra.

L’enveloppe du plan est **63,5×42,5mm**, hauteur **13,7mm attaches incluses**, ventilateur30×30mm. Ce sont des cotes de référence approximatives, explicitement impropres à produire directement des données de fabrication. La hauteur à réserver au-dessus du PCB et le chemin du cordon dépendent de la pose.

Le modèle reprend les ailettes et leur striation, le rotor visible, le capot, vis et clips, les ressorts hélicoïdaux, trois pads observés, le logo issu du plan et les quatre fils continus avec leur fiche. Les dimensions locales inconnues restent des estimations documentées.

[Fabricant]({MAKER}), [portail documentaire]({PORTAL}), [Pi5 retenu](../raspberry-pi-5/README.md).
''')
    write(BASE/'cotes.md','''# Cotes et fidélité du modèle

| Grandeur | Valeur | Origine / portée |
| --- | --- | --- |
| Enveloppe en plan |63,50×42,50mm | Plan Raspberry Pi, approximatif |
| Hauteur du dessin |13,70mm | Attaches incluses ; pas une hauteur installée au-dessus du PCB |
| Emprise du ventilateur |30×30mm | Plan de référence |
| Deux trous dédiés sur Pi |Ø3mm | Plan Pi ; distincts des quatre trous de châssisØ2,7 |
| Entraxes des clips dans la reconstruction |58×37mm | Lecture des deux plans ; aucun ajustement de production validé |
| Base CAO |1,4mm | Estimation |
| Ailettes segmentées |6colonnes×9rangées =54 | Structure observée dans plan/photos ; segments2,05×2,95 et hauteur7,8mm estimés |
| Pas des segments CAO |3,45mm enX /4,85mm enY | Estimation |
| Stries CAO |Pas0,85 /profondeur0,14 /hauteur0,18mm | Estimation de détails visibles |
| Rotor |30aubes courbes dans le modèle | Nombre et profil estimés, non donnés par le fabricant |
| Pads |3observés dessous ;17×17,14×10,8×8mm dans CAO | Formes et positions estimées ; épaisseurs0,5/1/1,5mm non publiées |
| ConnecteurFAN Pi |JST-SH,4voies, pas1mm | Documentation officielle |
| Fiche du cordon CAO |Boîtier2,8×5,9×3,6mm | Estimation ; pas une empreinte certifiée |
| Fils |Øgaine0,6mm /âme équivalente0,21mm | Estimation ; ni calibre ni longueur de remplacement garantis |
| Marquage |Contours vectoriels extraits du plan | Relief de lecture0,018mm ; gravure réelle non mesurée |

Les cotes libres du plan et les vues des photos ne donnent pas toutes les tolérances, la précharge des ressorts, l’épaisseur comprimée des pads, le volume interne du ventilateur ou son courant. Les modèles ne sont pas des plans de fabrication ni des calibres.

La variante complète ajoute un cordon en pose illustrative ; son enveloppe totale dépasse donc celle du module. Les variantes sans cordon l’omettent volontairement. Le modèlePi existant est conservé intact ; aucun assemblagePi/cooler n’est déclaré qualifié par ces seules cotes.

[Plan original](notices/RaspberryPi-ActiveCooler-plan-reference-original.pdf), [fiche constructeur](notices/RaspberryPi-ActiveCooler-fiche-actuelle-originale.pdf), [détails et contrôles de chaque STEP](3D/README.md).
''')
    write(BASE/'integration.md',f'''# Intégration V3 de l’Active Cooler

## Installation sur le Pi5

1. Batterie, alimentationPi et équilibrage débranchés ; stabiliser la carte. Vérifier ventilateur, pads et deux clips du produit reçu.
2. Retirer les papiers de protection des pads sous le module. Ne pas laisser de film entre pad et composant ; ne pas ajouter automatiquement de pâte ou une seconde couche.
3. Orienter selon le dessin sur la boîte et la notice fabricant. Aligner les deux attaches avec les **deux trous dédiés au dissipateur**, pas les trous de fixation du châssis. Éviter les ports et composants de la carte.
4. Appuyer régulièrement sur les deux têtes blanches jusqu’à l’encliquetage. Vérifier les clips par-dessous et que le métal ne touche pas de composant ou contact électrique hors des interfaces prévues.
5. Insérer la fiche dans **FAN**, dans le sens prévu, sans forcer. Si elle résiste, retirer et inspecter connecteur et fiche. Fixer le cordon pour qu’il ne touche ni le rotor ni une roue ou transmission.
6. Le fabricant recommande de laisser le montage en place : démontages répétés dégradent clips et pads. Un clip déformé ou mal retenu doit être remplacé. L’intervention de maintenance suit la notice du lot.

## Raccordement et commande

| BrocheFAN officielle | Fonction | Fil |
| --- | --- | --- |
|1 |+5V | Rouge |
|2 |PWM | Bleu |
|3 |GND | Noir |
|4 |Tachymètre | Jaune |

ConnecteurJST-SH,4voies, pas1mm. La vue de numérotation est celle de la documentation officielle : ne pas déduire un ordre à souder en regardant arbitrairement le côté opposé. La fiche livrée reste utilisée, aucun câble de remplacement construit ici.

Le contrôle dédiéFAN est distinct des PWMGPIO12/13/18 des moteurs et du servo. Aucun microcontrôleur supplémentaire ni raccord auBEC6V n’est nécessaire pour le ventilateur d’origine. Il reçoit son5V par la cartePi, dont la branche est déjà régulée par le PololuD24V90F5.

La documentationPi actuelle décrit, en température montante :50°C→30%,60°C→50%,67,5°C→70%,75°C→100%, arrêt sous50°C, hystérésis5°C en descente. Elle décrit aussi la détection tachymétrique à l’amorçage. **Ces paramètres dépendent du système, noyau et firmware reçus** ; relever le comportement réel. Le billet constructeur2023 ne citait que60/67,5/75°C : ne pas reprendre ses seuils comme une configuration2026 garantie. Aucune configuration appliquée.

## Alimentation et thermique

Le connecteurFAN partage la limitation de courant des périphériquesUSB. Le courant d’environ60mA publié pour le **ventilateur de boîtier officiel** ne donne pas celui de cetActiveCooler. La ficheSC1148 ne publie pas son courant dans les données consultées ; mesurer appel de démarrage et régime, avec la caméraUSB.

La branche5V de5A /25W d’étude inclut déjà Pi, caméra et refroidissement : ne pas ajouter une seconde fois la puissance du ventilateur au bilan global. Ce budget n’est pas une consommation mesurée. Ne relever les limites d’alimentationPi qu’après qualification de la source et du faisceau selon le dossierPi.

Prévoir admission au-dessus du rotor et sortie vers les ailettes dégagées. Ne pas enfermer le module sous une plaque pleine ni bloquer l’air avec un faisceau. Le refroidissement doit fonctionner robot immobile ; on ne suppose pas un courant d’air lié aux40km/h. Hauteur installée et jeux aux ports, supports, caméra et coque à vérifier sur matériel.

## Essais à réception

Confirmer référence, sens de fiche, pads et clips. Démarrer et vérifier la rotation/tachymètre. Mesurer tension5V à la carte et courant totalUSB/FAN, démarrage du ventilateur et effets des moteurs. Sur l’usage vidéo prolongé, enregistrer températureCPU, fréquence, signalement de sous-tension/throttling, régime et courant fan, cadence/latence vidéo et stabilité des impulsions moteurs. Essayer aussi robot immobile et dans le châssis final, sans overclocking supposé.

Les essais thermiques d’autres utilisateurs ne qualifient pas notre chaîne1080p60 ni son autonomie. L’ActiveCooler ne remplace pas l’arrêt sur perteWi-Fi ou blocage de la commande.

[Notice fabricant](notices/RaspberryPi-ActiveCooler-fiche-actuelle-originale.pdf), [documentationFAN]({HARDWARE}), [alimentationPi](../regulateur-alimentation/README.md), [dossierPi](../raspberry-pi-5/integration.md), [calculs](calculs.json).
''')
    write(BASE/'recherche-technique.md',f'''# Recherche et avis - Active Cooler SC1148

## Sources primaires et variantes

[Fabricant]({MAKER}), [portail]({PORTAL}), fiche publiéejanvier2026 et plan de référence archivé. Le portail indique mises à jour9janvier2026 /6octobre2025. **Débitmax1,09CFM**, vitessemax8000tr/min±15%, MTTF379000h à25°C (estimation de fiabilité, pas durée de vie garantie). Plusieurs vendeurs affichent1,4CFM : la valeur actuelle du fabricant prévaut.

Les URL historiquesdatasheets et les liensPIP téléchargent ici les **mêmes fichiers actuels**, SHA256 identiques. Le fichier local nommé « fiche-historique-originale » provient de l’ancienneURL, mais son contenu estjanvier2026, pas une édition2023. Les alias sont conservés pour documenter cette résolution ; cinqPDF téléchargés correspondent à deux contenus distincts, sans retouche.

Le plan présente un dessin simplifié d’entrée d’air, tandis que les photos montrent un rotor dans une ouverture circulaire. Le modèle suit les photos pour les détails et le plan pour les cotes disponibles. Les trois pads sont visibles sur une photo de dessousWaveshare, fournisseur du produit officiel ; toutes leurs dimensions restent estimées. AucunSTEP constructeur de ce refroidisseur trouvé dans le portail, ni CAO native adoptée sans provenance. PiSTEP existants conservés.

## Achat et retoursAmazon

[Amazon.fr]({AMAZON}) a pu être archivé après un premier accès refusé ; identitéSC1148 /GTIN et prix6,99€TTC affichés, stock5 au relevé14octobre2026. Le prix d’un bundlePi, celui d’un autre vendeur ou un total importDesertcart ne sont pas utilisés. L’ASIN trouvé viaDesertcart est ensuite confirmé par les détailsAmazon.com etAmazon.fr. Les champs « processeur/RAM/Ethernet » de ces reprises marchandes ne sont pas des fonctionnalités du refroidisseur.

La fiche française affiche4,7/5 et1242évaluations au relevé. Ce compteur peut agréger les pays et les versions de fiche ; il ne donne pas une statistique de panne de notre lot. Le widget ne fournit pas ici des témoignages individuels complets exploitables ; aucun avisAmazon inventé. Port et vendeur du panier final à vérifier ; les premières occurrences de « vendu par » dans la page peuvent concerner des produits associés, et ne sont pas utilisées pour identifier le vendeur du refroidisseur.

Olimex affiche5,00EUR mais «outofstock» au relevé, baseTVA/port français non établie : pas une offre de remplacement achetable à ce montant. Le prix choisi pour la ligneSC1148 est celui de la pageAmazon.fr, sans frais garantis.

## Essais indépendants et forums

- [JeffGeerling,2024, article avec mesures](https://www.jeffgeerling.com/blog/2024/water-cooling-overkill-pi-5/) : il rapporte unActiveCooler proche du bruit ambiant de son studio à5000tr/min. Mesure d’un testeur dans son montage, sans garantie de bruit ou de température dans notre châssis.
- [JeffGeerling, vidéo2023](https://www.youtube.com/watch?v=nBtOEmUqASQ) : chapitre10:17 consacré à la thermique et à l’ActiveCooler ; vidéo de référence identifiée, pas d’essai1080p60USB-versMac de notre robot. La pageYouTube est archivée ; aucun résultat non consulté n’en est déduit.
- [Forum officiel, bruit](https://forums.raspberrypi.com/viewtopic.php?p=2179285) : discussion sur niveaux de bruit mesurés et perceptions. Points d’attention pour vérifier le lot, sans garantie acoustique. Accès direct403, contenu consulté via rechercheWeb.
- [Forum officiel, boîtier](https://forums.raspberrypi.com/viewtopic.php?t=367026) : un utilisateur décrit une interférence avec le couvercle intérieur d’un boîtierPi. Ce n’est pas notre châssis, mais cela justifie de vérifier les dégagements au lieu de supposer un assemblage universel.
- [Billet constructeur thermique2023](https://www.raspberrypi.com/news/heating-and-cooling-raspberry-pi-5/) : essais de charge dans leurs conditions. La régulation décrite est ancienne ; le profil actuel est lu dans la [documentation matérielle]({HARDWARE}). Les60mA cités pour le ventilateur de boîtier ne sont pas transposés auSC1148.

## Informations non établies

CourantSC1148 réel, résistance thermique du module dans le châssis, niveau sonore normalisé, vibrations, épaisseurs comprimées des pads, classe de tolérance, profil exact du rotor, longueurs et sections du cordon, empreinte de fiche et hauteur installée au-dessus duPCB. Les vues détaillées sont des reconstructions, pas des mesures. Aucun essai embarqué, aucune validation1080p60 ni gain d’autonomie annoncé.

[Sources et archives](assets.json), [cotes](cotes.md), [intégration](integration.md), [modèles3D](3D/README.md).
''')
    assets=json.loads((BASE/'assets.json').read_text(encoding='utf-8'))['assets'];lines=['# Documents originaux de l’Active Cooler','','[NoticePDF V3](notice-active-cooler-pi5-v3.pdf).','',
        '| Original archivé | Source |','| --- | --- |']
    for a in assets:
        if a.get('status')=='downloaded' and a['file'].endswith('.pdf'):
            lines.append(f'| [{Path(a["file"]).name}]({Path(a["file"]).name}) | [URL]({a["url"]}) |')
    lines += ['','Les aliasPIP/datasheets sont identiques parSHA256 ; le fichier «historique» contient aussi la fichejanvier2026. Aucun ancien contenu n’est présenté comme une édition différente.',
        '', '[Intégrité et statuts](../assets.json), [recherche](../recherche-technique.md), [fiche](../README.md).']
    write(BASE/'notices/README.md','\n'.join(lines))
    write(BASE/'photos/README.md','''# Photos et crédits

`RaspberryPi-fiche-p2-1.jpeg` : image constructeur extraite sans retouche de la page2 duPDF actuel, créditRaspberryPiLtd. LePi représenté sert à la présentation du refroidisseur ; la variante4Go du robot n’est pas identifiée sur cette photo.

`Waveshare-produit-1.jpg`, `3.jpg`, `5.jpg`, `7.jpg` : vues de dessus, dessous et montage de l’ActiveCooler officiel, téléchargées intactes depuisWaveshare. Les numéros2/4/6/8 sont des vignettes. La vue3 montre les trois pads sous le dissipateur. Filigrane fournisseur préservé.

Aucune photo d’un composant reçu. Les images ne sont pas utilisées pour certifier une tolérance de fabrication. [URLs etSHA256](../assets.json), [recherche](../recherche-technique.md).
''')
    # Add current selection to the project and Pi documentation without touching CAD sources.
    p=ROOT/'Composants/README.md';text=p.read_text(encoding='utf-8');row=fmt('| [Refroidissement duPi5](refroidissement-raspberry-pi-5/README.md) | RaspberryPiActiveCoolerSC1148, préassemblé |6,99€TTC | Amazon.frB0CLXZBR5P, stock affiché au14octobre2026 ; non acheté ; quatreSTEP |')
    if 'refroidissement-raspberry-pi-5/README.md' in text:text=re.sub(r'^\| \[[^]]*\]\(refroidissement-raspberry-pi-5/README.md\).*$',lambda m:row,text,flags=re.M)
    if 'refroidissement-raspberry-pi-5/README.md' not in text:text=text.replace('\nPrix caméra et moteur', '\n'+row+'\n\nPrix caméra et moteur',1)
    write(p,text)
    p=ROOT/'ReadMe.md';text=p.read_text(encoding='utf-8');marker='<!-- active-cooler-sc1148-v3 -->'
    paragraph=fmt(f'Le [refroidissement duPi5](Composants/refroidissement-raspberry-pi-5/README.md) retient un ActiveCooler officielSC1148, préassemblé avec pads et clips. Amazon.frB0CLXZBR5P :6,99€TTC au14octobre2026, port conditionnel. Sources, avis, cotes, noticePDF et [quatreSTEP](Composants/refroidissement-raspberry-pi-5/3D/README.md), dont une version légère. Aucun montage testé ; courantUSB/FAN, thermique et dégagements à qualifier.')
    if marker not in text:text+=f'\n{marker}\n\n'+paragraph+'\n'
    else:text=re.sub(re.escape(marker)+r'\n\n[^\n]*(?:\n|$)',lambda m:marker+'\n\n'+paragraph+'\n',text,count=1)
    write(p,text)
    p=ROOT/'Composants/raspberry-pi-5/README.md';text=p.read_text(encoding='utf-8')
    text=text.replace("Refroidissement adapté à la charge vidéo et au châssis ; l'Active Cooler officiel est une piste, pas un accessoire déjà sélectionné ou chiffré.",
        fmt('Refroidissement retenu : [Active Cooler officielSC1148](../refroidissement-raspberry-pi-5/README.md),6,99€TTC au14octobre2026. Montage, courantFAN et thermique dans le châssis à qualifier.'))
    text=re.sub(r'^.*Refroidissement retenu :.*$',lambda m:fmt(m.group(0)),text,flags=re.M)
    write(p,text)
    p=ROOT/'Composants/raspberry-pi-5/integration.md';text=p.read_text(encoding='utf-8')
    if marker not in text:text+=f'\n{marker}\n\nLe [SC1148 sélectionné](../refroidissement-raspberry-pi-5/README.md) utilise le connecteurFAN dédié ; lesPWM12/13/18 restent réservés aux actionneurs. Sa [notice de montage et de qualification](../refroidissement-raspberry-pi-5/integration.md) inclut brochage, profil logiciel actuel et budgetUSB/FAN partagé.\n'
    text=re.sub(re.escape(marker)+r'\n\n[^\n]*(?:\n|$)',lambda m:fmt(m.group(0)),text,count=1)
    write(p,text)
    # Keep the generated CAD README readable without changing any CAD geometry.
    p=BASE/'3D/README.md';lines=p.read_text(encoding='utf-8').splitlines()
    for i,line in enumerate(lines):
        if line.startswith('| ') and line.count('|')==6:line=line.replace(' | ', ' : ',1)
        lines[i]=fmt(line)
    write(p,'\n'.join(lines))
    p=ROOT/'Composants/raspberry-pi-5/sources.json';d=json.loads(p.read_text(encoding='utf-8'))
    d['selected_cooling']=dict(reference='SC1148',documentation='../refroidissement-raspberry-pi-5/README.md',selected_on='2026-10-14',mounted=False)
    d['accessories_to_select']=[x for x in d.get('accessories_to_select',[]) if x!='refroidissement'];dump(p,d)
    print('DATA complete',flush=True)
if __name__=='__main__':main()
