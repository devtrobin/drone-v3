"""Document the selected 12 AWG wire and keep ratings separate from V3 tests."""
from pathlib import Path
import json,math,sys
from collect_power_wire_refs import MAKER
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/cable-puissance-12awg'
AMAZON='https://www.amazon.com/dp/B01ABOPMEI'
def write(name,text):
    p=BASE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.strip()+'\n',encoding='utf-8')
def data(name,obj):write(name,json.dumps(obj,ensure_ascii=False,indent=2))
def main():
    sys.stdout.reconfigure(encoding='utf-8')
    write('README.md',f'''# Câble de puissance 12 AWG - BNTECHGO rouge et noir

Choix d'étude du **14 octobre 2026** : **BNTECHGO SW12G68008F10C2**, deux fils séparés en cuivre étamé multibrins avec isolation silicone. Lot **10 ft rouge + 10 ft noir**, soit **3,048 m par couleur / 6,096 m total**. ASIN **B01ABOPMEI**, titre et variante 12 AWG contrôlés sur [Amazon.com]({AMAZON}). Non acheté, non testé.

Ces fils servent aux raccordements courts **après chaque ATO30 vers son XT60H-F** et aux deux retours négatifs indépendants vers le MiniBus. Le tronc commun 6 mm² proposé reste une référence distincte à sélectionner et qualifier.

| Donnée annoncée | Valeur / source |
| --- | --- |
| Calibre | 12 AWG ; section nominale AWG ≈3,31 mm² |
| Construction BNTECHGO | **680 brins de Ø0,08 mm**, cuivre étamé ; pas aluminium cuivré |
| Faisceau métallique | **Ø2,41 mm**, section arrondie **3,4 mm²**, image technique BNTECHGO |
| Gaine | Silicone rouge ou noir, **Ø4,5 mm ±0,1** sur l'offre ; épaisseur nominale 1,05 mm sur l'image technique |
| Résistance annoncée | **5,06 Ω/km = 5,06 mΩ/m**, image BNTECHGO ; température et méthode d'essai non précisées |
| Température / tension annoncées | -60 à +200 °C / 600 V ; pas une capacité de courant certifiée pour notre montage |
| Courant de l'étude | 20 A par boucle ESC, hypothèse ; aucun courant continu admissible exact du lot sous nos conditions publié |

## Dossier

- [Intégration et procédure de préparation](integration.md), [cotes et provenance](cotes.md).
- [Recherche Amazon, prix, citation et avis](recherche-technique.md), [sources](sources.json), [archives et SHA256](assets.json).
- [Calculs](calculs.json), [nomenclature et besoin provisoire](nomenclature.json).
- [Notice PDF V3 et documents de comparaison](notices/README.md), [images originales](photos/README.md).
- [Six STEP colorés avec aperçus](3D/README.md) : implantation rouge/noir/paire courbée et trois modèles courts à **680 brins individuels chacun**.

## Achat et quantité

[Amazon.fr B01ABOPMEI](https://www.amazon.fr/dp/B01ABOPMEI) : **prix, vendeur, stock et livraison en France non confirmés**, accès direct bloqué. La fiche Amazon.com identifie le produit ; elle ne prouve pas une offre française livrable. Prix sur [le site BNTECHGO]({MAKER}) : **14,98 USD**, relevé le 14 octobre 2026, taxes et frais vers la France non confirmés ; aucune conversion présentée comme prix TTC livré.

Le lot suffit au besoin provisoire de quatre queues de 0,20 m (deux rouges et deux noires), soit **0,40 m par couleur**, avec réserve. Ces longueurs ne constituent pas une liste de coupe : déterminer les trajets et les raccords avant de couper. Les fils des porte-fusibles et ceux des ESC sont déjà inclus dans leurs composants et ne sont pas rachetés comme ces queues.

Le lot rouge/noir est choisi pour sa référence vérifiée ; des variantes plus courtes existent chez le fabricant mais leurs offres Amazon exactes ne sont pas validées ici. **B01AO7586O est du 14 AWG à la consultation : écarté**, même s'il est cité dans un forum parlant de 12 AWG.
''')
    write('cotes.md','''# Cotes et construction du câble

Pas de mesure de lot reçu. Source principale : image technique **BNTECHGO-original-2.jpg**, provenant de la page fabricant du lot choisi. La fiche Amazon.com B01ABOPMEI ajoute la tolérance extérieure ±0,1 mm. Le catalogue Junhao est une comparaison, pas la fiche de certification de BNTECHGO.

| Grandeur | Valeur | Statut |
| --- | ---: | --- |
| Ø extérieur de gaine | **4,50 ±0,10 mm** | Annonce du lot ; mesurer à réception |
| Ø du faisceau de brins | **2,41 mm** | Image technique BNTECHGO, tolérance non donnée |
| Épaisseur silicone | **1,05 mm nominale** | Image BNTECHGO ; (4,50-2,41)/2=1,045 mm, cohérent avec arrondi |
| Nombre / Ø de brins | **680 / 0,08 mm** | Fabricant, non compté sur échantillon |
| Section commerciale arrondie | **3,4 mm²** | Image technique |
| Section nominale 12 AWG | **≈3,31 mm²** | Désignation nominale, pas une mesure du produit |
| Somme théorique des disques Ø0,08 | **3,41805 mm²** | 680×π×0,08²/4 ; diamètre étamé, tolérances et torsade non pris en compte |
| Longueur achetée | **3 048 mm par couleur** | Conversion exacte 10 ft×304,8 mm ; deux fils séparés |
| Résistance annoncée | **5,06 Ω/km** | Image fabricant ; température et condition maximale non documentées |

Ne pas confondre diamètre de gaine, diamètre d'enveloppe du faisceau et diamètre équivalent d'un cuivre massif de 3,31 mm² (≈2,053 mm). Les espaces entre brins expliquent une enveloppe plus grande ; sa surface n'est pas une section de cuivre. Épaisseur d'étamage, pas de torsade, nombre de sous-faisceaux et rayon minimal de courbure du produit non publiés dans les sources consultées.

## Modèles 3D

Trois modèles d'implantation : fil rouge et fil noir droits sur une longueur illustrative de 100 mm ; deux fils séparés courbés dans le plan XZ. Gaine Ø4,5 et enveloppe du faisceau Ø2,41. Dans ces versions, le faisceau est plein pour l'implantation : **ne pas utiliser son volume comme volume de cuivre réel**.

Trois modèles courts : rouge, noir et gaine ouverte, **longueur illustrative 25 mm**, 680 solides cylindriques de Ø0,08 chacun, plus une gaine annulaire. Disposition rectiligne sur réseau idéal avec petit jeu ; arrangement et pas réel de torsade inconnus. Étamage représenté par une couleur argentée, sans inventer une épaisseur métallique. Les brins sont continus et indépendants ; ils ne sont pas remplacés par quelques gros fils.

Dénudages de 5 mm aux bouts et fenêtre latérale dans la vue de coupe **volontaires pour observation**, pas une longueur de préparation recommandée. Couleurs et marquage réel de gaine non mesurés ; impression de fabricant non reproduite en faux relief. Les modèles ne comprennent ni rouleau d'emballage, ni cosses, embouts, soudures ou connecteurs ; ces interfaces restent à définir.

Le modèle XT60H câblé précédent utilisait **une gaine Ø4,2 mm estimée**. Le câble maintenant choisi est **Ø4,5 ±0,1 mm** : contrôler le passage dans les capots du lot et les rayons réels. Les trous du capot XT60H reconstruits étaient eux aussi estimés ; aucune compatibilité de diamètre prouvée par la CAO. Ne pas considérer l'ancien modèle illustratif comme celui du câble acheté.
''')
    write('integration.md','''# Intégration des fils 12 AWG

| Repère de projet | Fil | Départ / arrivée | Longueur |
| --- | --- | --- | --- |
| CM1+ | Rouge | Sortie 5065 / ATO30 ESC1 → + XT60H-F1 | Après implantation ; exemple 0,20 m |
| CM2+ | Rouge | Sortie 5065 / ATO30 ESC2 → + XT60H-F2 | Après implantation ; exemple 0,20 m |
| CM1- | Noir | - XT60H-F1 → cosse D- N1 | Après implantation ; exemple 0,20 m |
| CM2- | Noir | - XT60H-F2 → cosse D- N3 | Après implantation ; exemple 0,20 m |

Un positif protégé par ESC et un retour négatif séparé. Les deux fils d'entrée 16 AWG / 75 mm des ESC et les fils 12 AWG des 5065 restent ceux de leurs kits. Ce câble ne remplace pas le tronc commun proposé 6 mm² et ne se branche pas sur les trois phases moteur, les GPIO ou l'USB.

## Interfaces

- **XT60H-F** : cuivre étamé à souder dans les godets selon référence AMASS et procédure applicable. Le 12 AWG correspond à la recommandation de câble ; gaine **Ø4,5 ±0,1 mm** et passage de capot à vérifier. Aucun brin supprimé pour gagner du diamètre.
- **Fil de sortie 5065 → queue rouge** : raccord à sélectionner pour les deux conducteurs souples réels. Ne pas considérer une soudure volante non retenue comme raccord final qualifié.
- **Retours vers MiniBus** : cosses à sertir adaptées au 12 AWG/section réelle et au goujon **#10-32**, passage et largeur à confirmer ; filetage UNF, pas M5. Références de cosses et outillage à sélectionner ensuite.
- **Si un fil entre dans le UD80A** : vérifier son acceptation en très fin multibrins et l'embout applicable. Ne pas pré-étamer à la soudure une extrémité sous une borne vissée ; l'étamage industriel de chaque brin est différent d'un faisceau rigidifié par soudure.

Les raccords, gaine de protection locale, embouts et retenue mécanique ne sont pas inclus dans le lot de fil. Les longueurs doivent conserver une marge de manipulation sans traction, rester hors engrenages/roues, arêtes et zones chaudes, et garder l'accès aux fusibles. Le silicone reste à protéger du frottement ; aucune résistance à l'abrasion ou traction admissible du lot mesurée.

## Préparation du projet

1. Batterie et équilibrage débranchés. Mesurer le chemin, prévoir les terminaisons et le maintien, puis seulement établir la liste de coupe.
2. Contrôler variante **12 AWG**, rouge/noir, diamètre, état et souplesse. Vérifier cuivre étamé déclaré ; aluminium cuivré différent et hors sélection. Contrôler la résistance sur une longueur connue si possible, en retirant la contribution des cordons de mesure.
3. Couper proprement ; régler le dénudage pour la borne/godet/raccord réel. Le 5 mm de la CAO est illustratif. Utiliser un outil adapté aux brins fins, inspecter sous grossissement : pas de brins coupés, entaillés ou perdus.
4. Pour godet soudé : passer le capot avant soudure, conserver tous les brins, éviter chauffe prolongée et remontée de soudure trop longue. Pour raccord serti : suivre notice cosse/raccord et matrice prescrite, sans ajouter une soudure non prévue.
5. Isoler et retenir le raccord, identifier chaque branche, puis contrôler continuité, isolement +/-, polarités et serrages selon les composants.
6. Première alimentation limitée et supervisée ; mesurer courant individuel, chute et températures en usage prévu. Observer moteurs, connecteurs, fusibles et fils d'origine, pas seulement le fil neuf.

## Courant et défauts

Le lot ne fournit pas un courant continu admissible garanti sous notre confinement. Les inscriptions 200 °C / 600 V ne prouvent pas 20 A ni la tenue des soudures/capots. Scénario individuel **20 A**, référence XT60H prudente **30 A** : hypothèses sans limitation active actuelle. La résistance de 5,06 Ω/km permet un exemple de pertes, pas une certification thermique ; résistance à chaud et courants RMS/pointes à mesurer.

Un ATO30 n'est pas un limiteur à 30 A. Coordination du câble, raccords et fils ESC 16 AWG avec le fusible et le courant prospectif LiPo à qualifier. Le 12 AWG neuf n'améliore pas automatiquement la tenue des fils d'origine ou celle du XT60 commun du pack. Pas d'essai volontaire de court-circuit de batterie.

[Prises XT60H](../connecteurs-alimentation/integration.md), [fusibles de branches](../protection-branches-moteurs/integration.md), [MiniBus et retours](../distribution-alimentation/integration.md), [répartiteur](../repartition-moteurs/integration.md).
''')
    write('recherche-technique.md',f'''# Recherche, citation et avis - BNTECHGO 12 AWG

Consultation du **14 octobre 2026**. Aucun achat ni contact avec le fabricant.

## Sélection et prix

Référence **SW12G68008F10C2**, deux fils rouge/noir 10 ft chacun. [Page BNTECHGO]({MAKER}) : **14,98 USD**, hors confirmation de taxes et livraison française. [Amazon.com B01ABOPMEI]({AMAZON}) : titre 12 AWG/10ft par couleur vérifié ; pas d'offre principale exploitable, prix et stock livré non confirmés. [Amazon.fr](https://www.amazon.fr/dp/B01ABOPMEI) : accès bloqué. Aucun prix TTC en euros ou délai France inventé.

| Variante / alternative | Résultat |
| --- | --- |
| **BNTECHGO 12 AWG, 2×10 ft, B01ABOPMEI** | Référence retenue pour l'étude, caractéristiques cohérentes entre fabricant et fiche Amazon |
| BNTECHGO B01AO7586O, lien forum | **14 AWG / 2×20ft à la consultation**, écarté ; ne pas copier l'ASIN du forum comme preuve du calibre |
| BNTECHGO 2×3 ft ou 2×5 ft | Variantes plus courtes décrites par le fabricant ; ASIN/offre exacte non validés ; comparer le prix total livré avant commande |
| TUOFENG B07KX9YNPZ, 2×10,5 m | Repérage tiers seulement, offre exacte et documentation du lot non validées ; quantité excessive pour les queues prévues |

## Informations complétées

L'image technique fabricant [archivée](photos/BNTECHGO-original-2.jpg) donne ce que le texte principal omet : **faisceauØ2,41, section3,4 mm², gaineØ4,5, épaisseur1,05 et résistance5,06 Ω/km**. La tolérance extérieure ±0,1 vient de la fiche Amazon exacte. Les valeurs 680/0,08 sont corroborées par les deux.

Le catalogue Junhao page 12 confirme qu'une construction proche existe, mais n'identifie pas le sous-traitant BNTECHGO : sa certification, ses matières et son emballage ne sont pas transférés. Le plan **ModalAI MCBL-00110 v4** mentionne du BNTECHGO rouge/noir 12 AWG avec XT60 : preuve d'utilisation dans un faisceau fabricant, pas homologation de notre lot ou du courant 20 A.

Pas de PDF technique officiel BNTECHGO exact trouvé ; conserver page et images fabricant et créer notre propre notice clairement identifiée. Accès au PDF HingTak refusé pour défaut de certificat SSL ; aucune désactivation de contrôle TLS. Aucun STEP natif trouvé.

## Citation courte

Image technique BNTECHGO : **« Conductor Resistance 5.06 Ω/km »**. Titre Amazon exact : **« 12 AWG Silicone Wire Red and Black Each 10ft »**. Valeurs annoncées, non mesurées ; température de référence de résistance non précisée.

## Avis et usage

| Source | Retour | Limite |
| --- | --- | --- |
| [BNTECHGO, Jeff Y., 3 mai 2018]({MAKER}) | Fil souple, soudure facile ; calibre de pince de dénudage mal adapté pouvant couper des brins ; pince auto-ajustable mieux adaptée dans son cas | Expérience utilisateur sur cette fiche, pas essai électrique indépendant |
| [BNTECHGO, Paolo, 20 septembre 2023]({MAKER}) | Apprécie la flexibilité et les brins étamés | Pas de section ni température mesurée |
| [R/C Tech, février 2025](https://www.rctech.net/forum/radio-electronics/1131751-where-buy-silicone-copper-wire.html?styleid=21) | Plusieurs utilisateurs disent employer BNTECHGO pour cordons de charge et apprécient la soudure/souplesse | Le lien ASIN visible renvoie au 14 AWG ; ne pas considérer ces messages comme essai exact B01ABOPMEI à 20 A |
| Amazon.com, fiche exacte | En-tête **4,7/5, 4 807 évaluations** à la consultation indexée | Note agrégée multi-variantes possible ; pas moyenne d'essais du lot reçu |

Recherche de vidéos et mesures indépendantes exactes effectuée ; **aucun essai YouTube vérifiable de B01ABOPMEI avec résistance/échauffement quantifiés trouvé**. Aucune vidéo prétendument visionnée ni mesure d'utilisateur inventée. L'avis de la variante 50ft évoquant 20 A au chargeur reste un usage différent et n'est pas une garantie V3.
''')
    write('notices/README.md','''# Notice et documents

- [Notice V3 du câble 12 AWG](notice-cable-puissance-12awg-v3.pdf) : sélection, cotes, montage, pertes et modèles ; document du projet, pas notice officielle BNTECHGO.
- [Catalogue Junhao original](Junhao-catalogue-comparaison.pdf), page 12 : construction voisine 680×0,08, comparaison uniquement ; ne certifie pas le lot BNTECHGO.
- [Plan ModalAI MCBL-00110 v4 original](ModalAI-MCBL00110-v4-cable-BNTECHGO-XT60.pdf) : exemple fabricant de câble XT60 avec fils BNTECHGO 12 AWG ; longueurs et pièces ne sont pas imposées au robot.

Aucun PDF de spécification officiel BNTECHGO exact obtenu. La page et les images techniques de la marque sont conservées, avec statuts d'accès ; c'est l'image technique exacte qui fournit les cotes et la résistance. Échec SSL du catalogue HingTak consigné, pas de faux PDF créé. [Sources](../sources.json), [archives](../assets.json), [recherche](../recherche-technique.md).
''')
    write('photos/README.md','''# Images originales BNTECHGO

- [Présentation rouge/noir](BNTECHGO-original-1.jpg), illustration fabricant, pas photo du lot reçu.
- [Image technique de la référence](BNTECHGO-original-2.jpg) : 680/0,08TS, Ø2,41, 5,06 Ω/km, 3,4 mm², épaisseur1,05, Ø4,5.
- [Flexibilité illustrée](BNTECHGO-original-3.jpg), sans rayon minimal coté.
- [Applications](BNTECHGO-original-4.jpg), illustration commerciale, pas validation de notre robot.

Images téléchargées inchangées depuis le CDN lié à la page BNTECHGO ; URL et SHA256 dans assets.json. Les modèles et aperçus sont dans le [dossier3D](../3D/README.md).
''')
    rows=[]
    for length in [.10,.20,.40]:
        for current in [10,20,30]:
            resistance=2*length*.00506
            rows.append(dict(one_way_length_m=length,current_A=current,loop_resistance_ohm=resistance,drop_V=current*resistance,
                loss_per_branch_W=current**2*resistance,loss_two_equal_branches_W=2*current**2*resistance))
    data('calculs.json',dict(checked_on='2026-10-14',hardware_tested=False,resistance_published_ohm_per_km=5.06,
        resistance_reference_temperature_C=None,resistance_is_guaranteed_maximum=False,source_image='photos/BNTECHGO-original-2.jpg',
        nominal_AWG_area_mm2=3.31,commercial_area_mm2=3.4,strand_disk_sum_mm2=680*math.pi*.08**2/4,
        copper_resistivity_example_20C_ohm_mm2_per_m=.0175,pure_copper_nominal_estimate_ohm_per_m=.0175/3.31,
        loop_examples=rows,excludes=['holder wires','ESC16AWG','contacts','splices','warming','lay and plating tolerance'],
        scenario_individual_current_A=20,current_limit_enforced=False,cable_ampacity_V3_qualified=False,
        fault_energy_qualified=False,XT60H_cap_fit_verified=False,proposed_lengths_are_not_cut_list=True))
    data('nomenclature.json',dict(checked_on='2026-10-14',purchased=False,reference='BNTECHGO SW12G68008F10C2',
        amazon_ASIN='B01ABOPMEI',kit_quantity_proposed=1,red_m=3.048,black_m=3.048,total_m=6.096,
        provisional_cuts=[dict(name=n,color=c,length_example_m=.2) for n,c in [('CM1+','red'),('CM2+','red'),('CM1-','black'),('CM2-','black')]],
        actual_cut_list_validated=False,example_installed_red_m=.4,example_installed_black_m=.4,
        example_red_spare_m=2.648,example_black_spare_m=2.648,model_strip_mm_is_instruction=False,
        price_FR_TTC_EUR=None,manufacturer_reference_USD=14.98,shipping_FR_verified=False,Amazon_FR_stock_verified=False,
        includes_connectors=False,includes_lugs=False,main_6mm2_wire_included=False,
        missing=['cut list after layout','12AWG splices and lug references','crimp tools','caps fit','current and thermal/fault qualification']))
    sources=[dict(id='brand',url=MAKER,type='brand_primary',supports='SW12G68008F10C2,2x10ft,680x0.08,materiaux,prixUSD et avis',local='sources-web/BNTECHGO-SW12G68008F10C2.html'),
        dict(id='image-brand',url='https://cdn11.bigcommerce.com/s-clng77kigt/product_images/uploaded_images/sw-12-3.jpg',type='brand_primary_image',local='photos/BNTECHGO-original-2.jpg',supports='Ø2.41,3.4mm2,5.06ohm/km,1.05,4.5'),
        dict(id='amazon-exact',url=AMAZON,type='marketplace_brand_listing',supports='titre12AWG,680x0.08,4.5+/-0.1,2x10ft',FR_stock_verified=False),
        dict(id='amazon-excluded',url='https://www.amazon.com/dp/B01AO7586O',type='marketplace_wrong_variant',supports='14AWG a la consultation ; exclu'),
        dict(id='junhao-comparison',url='https://en.junhaodx.com/Catalogue.pdf',type='other_manufacturer_comparison',local='notices/Junhao-catalogue-comparaison.pdf',supports='famillevoisinepage12;pas homologationBNTECHGO'),
        dict(id='modalai-example',url='https://storage.googleapis.com/modalai_public/modal_drawings/MCBL-00110%20Drawing%20v4.pdf',type='manufacturer_wiring_example',local='notices/ModalAI-MCBL00110-v4-cable-BNTECHGO-XT60.pdf',supports='usageBNTECHGO12AWGsurXT60, pas courantV3'),
        dict(id='forum',url='https://www.rctech.net/forum/radio-electronics/1131751-where-buy-silicone-copper-wire.html?styleid=21',type='firsthand_users',supports='cordonscharge/souplesse; lienvariante14AWG'),
        dict(id='AMASS-interface',url='https://www.china-amass.com/biao/283.html',type='connector_manufacturer',supports='conditions12AWGsurXT60H ;pas qualificationcable')]
    data('sources.json',dict(checked_on='2026-10-14',sources=sources,native_STEP_obtained=False,hardware_measured=False,
        official_BNTECHGO_PDF_obtained=False,exact_measured_youtube_test_found=False))
    data('releve-web.json',dict(checked_on='2026-10-14',exact_ASIN='B01ABOPMEI',title_observed='BNTECHGO 12 AWG Silicone Wire Red and Black Each 10ft Tinned Copper Wire',
        brand_store='BNTECHGO',gauge=12,announced_strands=680,outer_diameter_mm=4.5,diameter_tolerance_mm=.1,
        US_featured_offer_observed=False,FR_stock_verified=False,source_url=AMAZON,
        note='Observed through web-indexed page; saved direct-request HTML may be a challenge page, not proof of current delivery.'))
    print('DOCS 12AWG written',flush=True)
if __name__=='__main__':main()
