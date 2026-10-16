"""Component dossier, stock accounting and deferred chassis decision."""
from pathlib import Path
import json, math, sys

ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/fixations-raspberry-pi-5'
AMAZON='https://www.amazon.fr/dp/B0DCS5C7SN'
PI='https://datasheets.raspberrypi.com/rpi5/raspberry-pi-5-mechanical-drawing.pdf'
ESSENTRA='https://essentracomponents.bynder.com/m/6e2e9b888468b393/original/2685970-pdf.pdf'
DATE='2026-10-14'
PARTS=[
 ('mf-6','Entretoise mâle-femelle','M2.5, corps 6 mm + mâle 6 mm',20,0,'entretoise-mf-m2-5-6-plus-6.step'),
 ('mf-8','Entretoise mâle-femelle','M2.5, corps 8 mm + mâle 6 mm',20,0,'entretoise-mf-m2-5-8-plus-6.step'),
 ('mf-10','Entretoise mâle-femelle','M2.5, corps 10 mm + mâle 6 mm',20,4,'entretoise-mf-m2-5-10-plus-6.step'),
 ('mf-15','Entretoise mâle-femelle','M2.5, corps 15 mm + mâle 6 mm',10,0,'entretoise-mf-m2-5-15-plus-6.step'),
 ('mf-20','Entretoise mâle-femelle','M2.5, corps 20 mm + mâle 6 mm',10,0,'entretoise-mf-m2-5-20-plus-6.step'),
 ('ff-6','Entretoise femelle-femelle','M2.5, corps 6 mm',20,0,'entretoise-ff-m2-5-6.step'),
 ('ff-10','Entretoise femelle-femelle','M2.5, corps 10 mm',20,0,'entretoise-ff-m2-5-10.step'),
 ('ff-15','Entretoise femelle-femelle','M2.5, corps 15 mm',15,0,'entretoise-ff-m2-5-15.step'),
 ('ff-20','Entretoise femelle-femelle','M2.5, corps 20 mm',20,0,'entretoise-ff-m2-5-20.step'),
 ('vis-8','Vis cruciforme','M2.5 x 8 mm sous tête',20,4,'vis-cruciforme-m2-5-8.step'),
 ('vis-12','Vis cruciforme','M2.5 x 12 mm sous tête',20,0,'vis-cruciforme-m2-5-12.step'),
 ('vis-20','Vis cruciforme','M2.5 x 20 mm sous tête',20,0,'vis-cruciforme-m2-5-20.step'),
 ('ecrou','Écrou hexagonal','M2.5',60,4,'ecrou-m2-5.step'),
 ('rondelle','Rondelle plate','M2.5',60,8,'rondelle-m2-5.step'),
]

def write(rel,s):
 p=BASE/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s.strip()+'\n',encoding='utf-8')
def dump(rel,v):write(rel,json.dumps(v,ensure_ascii=False,indent=2))
def block(path,marker,body):
 s=path.read_text(encoding='utf-8');tag=f'<!-- {marker} -->';end=f'<!-- /{marker} -->'
 new=tag+'\n\n'+body.strip()+'\n\n'+end
 if tag in s:
  a=s.index(tag);b=s.index(end,a)+len(end);s=s[:a]+new+s[b:]
 else:s=s.rstrip()+'\n\n'+new+'\n'
 path.write_text(s,encoding='utf-8')

def main():
 sys.stdout.reconfigure(encoding='utf-8');obs=json.loads((BASE/'observation-amazon.json').read_text(encoding='utf-8'))
 assets=json.loads((BASE/'assets.json').read_text(encoding='utf-8'))
 obs['uncertainties'][-1]='Les images haute définition confirment des corps MF et FF hexagonaux ; surplats réel à mesurer'
 dump('observation-amazon.json',obs)
 parts=[dict(id=i,component=k,specification=spec,bought_in_one_kit=q,used_in_study=u,reserve=q-u,step='3D/'+f) for i,k,spec,q,u,f in PARTS]
 assert sum(p['bought_in_one_kit'] for p in parts)==335
 assert sum(p['used_in_study'] for p in parts)==20
 dump('nomenclature.json',dict(date=DATE,kit=dict(brand='Ewwtrey',manufacturer='DJJRX',part='260018',asin='B0DCS5C7SN',
  quantity_to_buy=1,price_eur_vat_included=9.98,shipping_conditional=True,purchased=False,advertised_pieces=335),
  study_assembly_only=True,final_height_selected=False,total_used_in_study=20,total_reserve=315,parts=parts))
 calc=dict(date=DATE,hardware_tested=False,chassis_final_component=True,
  geometry=dict(board_holes_reference_mm=[[3.5,3.5],[61.5,3.5],[61.5,52.5],[3.5,52.5]],rectangle_mm=[58,49],
   board_hole_diameter_reference_mm=2.7,thread_nominal_mm=2.5,nominal_radial_clearance_mm=(2.7-2.5)/2,
   assumed_hex_surplats_mm=5,assumed_hex_corner_radius_mm=5/math.sqrt(3),
   reference_land_diameter_mm=6,nominal_corner_margin_mm=3-5/math.sqrt(3),
   reference_drawing_not_production_data=True),
  mounting_study=dict(body_mm=10,stud_mm=6,pcb_thickness_assumed_mm=1.6,panel_thickness_assumed_mm=2,
   washer_thickness_assumed_mm=.5,nut_height_assumed_mm=2,screw_under_head_mm=8,
   bottom_engagement_mm=8-2-.5,assumed_female_depth_mm=6.5,female_bottom_margin_mm=6.5-(8-2-.5),
   stud_protrusion_above_nut_mm=6-1.6-.5-2,
   body_base_z_mm=0,pcb_lower_face_z_mm=10,nut_lower_face_z_mm=12.1,stud_end_z_mm=16,
   sole_component_caos=True,no_chassis_no_pcb_solid=True,final_height_selected=False),
  candidates=[dict(body_height_mm=h,stud_mm=6,nut_end_z_study_mm=h+4.1,stud_end_z_mm=h+6) for h in [6,8,10,15,20]],
  warning='Toutes les cotes fines du kit et épaisseurs de montage sont des hypothèses. Ne certifie ni serrage, ni résistance, ni tenue aux chocs, ni dégagement réel au Pi/cooler/GPIO.')
 dump('calculs.json',calc)
 sources=[
  dict(id='amazon',kind='Fiche commerciale de la variante exacte, source primaire du vendeur',url=AMAZON,observed_on=DATE,
   supports=['Identité Ewwtrey/DJJRX/260018, ASIN et variante noire M2.5','335 pièces, longueurs, matière annoncée, prix/stock/session','Photos commerciales et avis multivariantes'],archive='observation-amazon.json',limitations='Pas de fiche de fabrication, cotes fines, tolérances, couple ou certification thermique.'),
  dict(id='pi-plan',kind='Fabricant de la carte',url=PI,observed_on=DATE,archive='notices/RaspberryPi-5-plan-mecanique-original.pdf',
   supports=['Quatre fixations Ø2.7, rectangle 58 x 49 mm, repères de 3.5 mm, zones dessinées Ø6'],limitations='Le fabricant déclare les dimensions approximatives, de référence et non utilisables comme données de production.'),
  dict(id='essentra',kind='Fabricant différent, documentation générique',url=ESSENTRA,observed_on=DATE,
   archive='notices/Essentra-filetages-plastiques-reference-original.pdf',supports=['Exemples de filetages M2.5 x 0.45 dans les tableaux de fixations plastiques'],
   limitations='Ne définit ni matière, ni dimensions de tête, ni couple, ni tolérances du kit Ewwtrey. Aucune interchangeabilité certifiée.'),
  dict(id='pihut',kind='Fournisseur de cartes, alternative non retenue',url='https://thepihut.com/products/m2-5-nylon-standoff-packs',observed_on=DATE,
   supports=['Usage de M2.5 pour fixer un Raspberry Pi ; variantes MF/FF disponibles'],limitations='Autre produit, ne cote pas Ewwtrey ; pas de chiffrage du panier britannique retenu.'),
  dict(id='adafruit',kind='Fabricant différent, alternative non retenue',url='https://www.adafruit.com/product/3299',observed_on=DATE,
   supports=['Assortiment de fixations en nylon M2.5 pour cartes'],limitations='Autre kit, aucune dimension ou certification transférée.'),
 ]
 dump('sources.json',dict(date=DATE,sources=sources,research_log=[
  dict(query='Ewwtrey B0DCS5C7SN notice',engine='Recherche web',result='Reprise de fiche commerciale trouvée, aucune notice originale propre au kit identifiée'),
  dict(query='B0DCS5C7SN youtube',engine='Recherche web',result='Aucun essai vidéo spécifique exploitable trouvé'),
  dict(query='B0DCS5C7SN Raspberry Pi forum dimensions standoff',engine='Recherche web',result='Aucun relevé dimensionnel sur forum du kit exact trouvé'),
  dict(query='Raspberry Pi 5 mécanique M2.5',engine='Documentation fabricant',result='Plan officiel téléchargé, p.1 inspectée'),
  dict(query='entretoise nylon M2.5',engine='Amazon.fr dans Chrome',result='Kit noir exact accessible, en stock, 9.98 EUR ; pas de commande')]))
 write('README.md',f'''# Fixations du Raspberry Pi 5 - Drone V3

Sélection du **14 octobre 2026** : **un kit Ewwtrey 335 pièces en nylon noir M2.5**, fabricant DJJRX, référence commerciale **260018**, ASIN **B0DCS5C7SN**.

[Acheter sur Amazon.fr]({AMAZON}) - **9,98 € TTC** au relevé, en stock, vendeur **QianHaiDian**, expédié par Amazon. Livraison gratuite annoncée dans la session Prime consultée ; coût et délai à revalider avant achat. Aucune commande effectuée.

Le kit fournit plusieurs hauteurs et la visserie associée pour fixer le Pi au futur châssis. **Le châssis sera conçu en dernier**, conformément à la décision utilisateur de ce jour. **10 mm est une hauteur de travail provisoire, pas le choix final.**

L'assemblage d'étude comporte quatre entretoises **MF 10+6 mm**, quatre écrous, huit rondelles et quatre vis **M2.5 x 8 mm** : **20 pièces sur 335**, réserve théorique de 315 pièces. Le devis facture le kit entier. Les autres tailles restent disponibles pour ajuster l'implantation.

## Documents et modèles

- [Notice V3 en PDF](notices/notice-fixations-pi-5-v3.pdf) : contenu, achat, cotes, montage provisoire, sources et contrôles.
- [Cotes et hypothèses](cotes.md), [devis daté](devis.md), [intégration](integration.md), [recherches et avis](recherche-technique.md).
- [Catalogue 3D](3D/README.md) : **15 STEP colorés** - neuf entretoises, trois vis, un écrou, une rondelle et un assemblage de quatre fixations. Filetages intérieurs et extérieurs hélicoïdaux, empreintes cruciformes et chanfreins reconstruits.
- [Photos originales](photos/README.md) ; [PDF originaux de référence](notices/README.md).
- Données : [nomenclature](nomenclature.json), [calculs](calculs.json), [sources](sources.json), [observation Amazon](observation-amazon.json) et [archives](assets.json).

## État de la sélection

Le Pi possède quatre trous de référence **Ø2,7 mm**, espacés de **58 x 49 mm**. Les deux trous dédiés au refroidisseur ne sont pas des points de fixation du châssis. Le plan du Pi est explicitement approximatif et non destiné à produire des données de fabrication.

Les longueurs du kit sont publiées ; surplats, profils de tête, diamètre des rondelles, profondeur de taraudage et tolérances ne le sont pas. Les modèles sont des **reconstructions détaillées avec hypothèses tracées**, sans mesures physiques ni CAO native du kit. La masse annoncée de 90 g et l'enveloppe 170 x 97 x 18 mm concernent l'article/lot ; elles ne décrivent pas les vingt pièces embarquées.

Le lot n'est pas un jeu d'écrous autofreinés. Couple, tenue aux chocs, vieillissement et température admissible ne sont pas qualifiés. Vérifier le lot, l'engagement des filetages et les dégagements autour du Pi, de la microSD, du cooler, du GPIO et des câbles lors de la conception finale.
''')
 inventory='\n'.join(f"| {p['component']} | {p['specification']} | {p['bought_in_one_kit']} | {p['used_in_study']} | {p['reserve']} |" for p in parts)
 write('devis.md',f'''# Devis d'achat indicatif - 14 octobre 2026

| Achat | Quantité | Prix TTC | Port | État |
| --- | ---: | ---: | --- | --- |
| [Ewwtrey 335 pièces, noir M2.5, B0DCS5C7SN]({AMAZON}) | 1 kit | **9,98 €** | Gratuit affiché dans la session Prime ; conditions à revalider | En stock au relevé ; non acheté |

Vendeur QianHaiDian, expédition Amazon. Livraison le 15 octobre 2026 annoncée au relevé ; ce n'est ni un engagement de notre part ni une garantie de disponibilité future. TVA applicable incluse dans le prix affiché.

**Coût des marchandises ajouté à la V3 : 9,98 € pour le kit entier**, pas un prix au prorata des seules pièces montées. Total livré : 9,98 € uniquement si la gratuité affichée s'applique ; sinon 9,98 € plus les frais réels. Pas de coût de fabrication de châssis ajouté ici. Aucun panier global ni nouveau total V3 établi.

## Contenu annoncé et allocation provisoire

MF = mâle-femelle ; FF = femelle-femelle. La longueur avant « +6 » est celle du corps, puis celle du goujon mâle. La longueur d'une vis se mesure sous la tête.

| Pièce | Taille annoncée | Dans le kit | Étude 10 mm | Réserve |
| --- | --- | ---: | ---: | ---: |
{inventory}
| **Total** | | **335** | **20** | **315** |

La réserve est théorique, selon le contenu annoncé, pas un inventaire de pièces reçues. Boîte de rangement incluse ; ni Pi, ni outil, ni châssis achetés avec ce lot. Tournevis adapté à vérifier parmi l'outillage existant avant un achat supplémentaire.

## Autres pistes consultées

La variante blanche du même assortiment est affichée à 8,98 € sur la famille Amazon ; non retenue et non achetée. Les packs The Pi Hut et l'assortiment Adafruit 3299 sont d'autres produits ; aucun panier complet de ces alternatives ni leurs frais France n'est comparé au prix de notre lot.
''')
 write('cotes.md',f'''# Cotes, repères et fidélité des modèles

Toutes les dimensions ci-dessous sont en millimètres. Aucun élément n'a été mesuré sur une pièce réelle.

| Élément | Valeur | Statut et origine |
| --- | --- | --- |
| Pi 5, quatre trous de fixation | Ø2,7 ; rectangle 58 x 49 | Plan officiel p.1, référence approximative |
| Pi, centres dans notre repère | (3,5;3,5), (61,5;3,5), (61,5;52,5), (3,5;52,5) | Déduits du plan ; origine bord gauche/bord inférieur du PCB |
| Zones circulaires aux fixations | Ø6 | Repère du plan ; ne garantit pas le dégagement en 3D |
| MF : corps + goujon | 6+6, 8+6, 10+6, 15+6, 20+6 | Illustration et description du kit exact |
| FF : corps | 6, 10, 15, 20 | Illustration et description du kit exact |
| Vis : longueur sous tête | 8, 12, 20 | Illustration et description du kit exact |
| Désignation du filetage | M2.5 | Publiée pour le kit |
| Pas CAO | 0,45 | Pas usuel d'étude, cohérent avec exemples Essentra ; non spécifié/mesuré sur ce lot |
| Entretoises : forme et surplats | Hexagonal ; 5,0 sur plats | Forme d'après photo de détails, surplats estimé |
| Tête de vis | Ø4,7 ; hauteur 2,0 ; empreinte cruciforme | Forme visible, dimensions et raccords estimés |
| Écrou | Surplats 5,0 ; hauteur 2,0 | Forme visible, dimensions estimées |
| Rondelle | Øextérieur 5,0 ; Øintérieur 2,7 ; épaisseur 0,5 | Dimensions estimées, aucune cotation fabricant trouvée |
| MF : taraudage borgne | Profondeur min(6,5 ; longueur corps - 2) | Hypothèse de CAO, avec fond plat non spécifié |
| FF : taraudage traversant | Sur toute la longueur | Hypothèse de CAO ; ne certifie pas le lot |
| Filetage intérieur | Jeu radial de reconstruction 0,03 | Hypothèse graphique de montage, pas une classe de tolérance |

Le profil des filetages comporte une vraie hélice droite, des flancs proches du profil métrique de 60 degrés, des crêtes tronquées et des fonds simplifiés. Les entrées sont chanfreinées ; détails de moulage, rayons exacts, amorces et bavures ne sont pas certifiés. **Ne pas employer ces STEP comme jauges, plans de production ou preuves de résistance.**

Les images haute définition de tailles et de détails confirment les corps MF et FF hexagonaux. Leur dimension surplats reste estimée à 5 mm. Vérifier la forme et les dimensions du lot à réception.

Les FF passent par une préparation en représentation spline STEP avant le contrôle final. L'écart de volume de cette conversion est tracé dans leur JSON (limite 0,1 %) ; le réimport final garde une limite de 0,01 %. Cela ne change pas le statut d'estimation des détails internes.

## Montage de travail à 10 mm

Le plancher futur est à z=0 dans l'assemblage, sans être dessiné. Entretoise MF : corps z=0 à 10, goujon z=10 à 16. Dessous de carte étudié z=10 ; épaisseur temporaire **1,6 mm**, pas une cote vérifiée du Pi retenu. Rondelle supérieure z=11,6 à 12,1 ; écrou z=12,1 à 14,1. Le goujon dépasse de **1,9 mm** dans cette hypothèse.

Au-dessous, épaisseur temporaire de panneau **2 mm**, non décidée pour le châssis. Rondelle inférieure z=-2,5 à -2 ; vis sous tête 8 mm, engagement d'étude **5,5 mm** : 8 - 2 - 0,5. Taraudage modélisé 6,5 mm : marge de fond **1 mm**. Mesurer la profondeur réelle avant de choisir une vis ; une vis en butée ne serre pas le panneau.

Le jeu radial nominal M2.5/Ø2.7 serait **0,10 mm**, sans tolérances. Avec un hexagone estimé à 5 mm surplats, rayon de sommet **2,887 mm** et marge nominale au cercle Ø6 **0,113 mm**. Cette petite marge est un calcul de référence, pas un contrôle des composants proches ni une qualification physique.

L'assemblage ne contient que les **20 pièces du kit**, disposées sur le rectangle de fixation du Pi. **Le PCB et le châssis sont intentionnellement absents.** Les épaisseurs servent à étudier l'engagement et à documenter les espaces vides ; elles ne figent aucune fabrication.

[Plan officiel]({PI}) et [hypothèses calculables](calculs.json). La hauteur finale et les trous du châssis seront définis lors de son étude, en dernier.
''')
 write('integration.md','''# Intégration des fixations - étude provisoire

Le châssis est le dernier composant à concevoir. Réserver quatre fixations aux coins du Pi, sans choisir maintenant l'implantation sur le véhicule, la hauteur finale ni l'épaisseur du châssis. Plusieurs hauteurs du kit servent à explorer ce choix ultérieur.

## Configuration étudiée

Quatre MF 10+6 mm, goujon mâle vers le haut. Une vis M2.5 x 8 et une rondelle par point attachent le corps au panneau futur. Le Pi repose sur les quatre corps ; une rondelle et un écrou par point retiennent la carte sur le goujon. Ce sont cinq pièces par point et vingt au total.

La CAO dessine les filetages en position d'engrènement ; elle ne dessine ni châssis ni PCB. Hauteur 10 mm, carte 1,6 mm, panneau 2 mm et rondelles 0,5 mm sont des hypothèses révisables. Engagement inférieur 5,5 mm et dépassement supérieur 1,9 mm ne valent que pour ces hypothèses. Voir cotes.md et calculs.json.

## Montage proposé après réception et étude du châssis

1. Hors alimentation, contrôler la variante M2.5 et le contenu du lot. Mesurer hauteurs, surplats, diamètre et épaisseur des rondelles, longueur des vis, pas, profondeur réelle des taraudages et épaisseur locale de carte. Les formes commerciales ne sont pas un plan de fabrication.
2. Vérifier l'accès à la microSD, au bouton du Pi, à l'USB caméra, au refroidisseur, au GPIO et à tous les câbles. Contrôler dessous de carte, appui des quatre corps et face d'appui des rondelles. Utiliser les quatre trous de carte ; les deux trous du cooler ont une autre fonction.
3. Choisir la hauteur finale et les vis avec un engagement suffisant sans fond de taraudage atteint, ni extrémité en contact avec un composant. Le châssis doit fournir quatre appuis coplanaires ; ne pas contraindre le PCB pour corriger un décalage de perçage.
4. Engager chaque filetage à la main. Immobiliser doucement le corps sur ses méplats, poser les rondelles et serrer progressivement les quatre points avec un petit outil adapté. Aucun couple fabricant chiffré du lot trouvé : ne pas lui appliquer un couple de vis acier.
5. Vérifier que la carte ne fléchit pas, que les pièces ne tournent pas librement et qu'aucune rondelle/vis ne gêne les connecteurs. Reprendre les mesures si un taraudage force ; ne pas agrandir les trous du Pi pour adapter un lot M3.
6. Après premiers essais progressifs, contrôler maintien, fissures, desserrage et frottements des câbles. La tenue dynamique doit être vérifiée sur le véhicule final ; une géométrie STEP valide n'est pas un essai de choc à 40 km/h.

Les rondelles répartissent localement l'appui ; elles ne transforment pas les écrous simples en écrous autofreinés. Ne pas attribuer de propriété de blocage, de classe thermique ou de qualité nylon 6/6 au lot sans données. Les fixations servent au Pi, pas aux moteurs, à la batterie ou aux organes de direction.

L'Active Cooler utilise ses propres clips fournis. Les dégagements Pi/cooler/GPIO restent ceux des études existantes ; ce dossier ne corrige ni ne valide automatiquement leurs modèles. Les fils doivent être maintenus par le maintien de faisceau afin de limiter les efforts sur la carte.
''')
 reviews='\n\n'.join(f"- **{r['author']}**, {r['date']}, {r['stars']}/5, {r['variant']} : {r['summary']} [Source]({r['url']})." for r in obs['reviews'])
 write('recherche-technique.md',f'''# Recherche technique et avis - 14 octobre 2026

## Identification et achat

La fiche Amazon.fr exacte a été ouverte dans Chrome, variante sélectionnée **Noir M2.5**. Marque Ewwtrey, fabricant DJJRX, numéro 260018, ASIN B0DCS5C7SN. Prix **9,98 € TTC**, état **en stock**, vendeur QianHaiDian, expédition Amazon. Gratuité de livraison et date du 15 octobre sont des affichages de session, à revalider. [Fiche directe]({AMAZON}). Les seuls faits utiles ont été consignés dans observation-amazon.json ; aucune adresse privée ni donnée de compte conservée.

Les quatorze lignes du contenu annoncé totalisent **335 pièces**. Une seule boîte suffit au montage de travail de quatre points ; quatre supports à 10 mm ne constituent pas le choix final de hauteur. Le kit garde les options 6, 8, 15 et 20 mm pour la conception du châssis à la fin.

## Documents et ambiguïtés

Quatre images commerciales originales téléchargées, dont l'illustration des tailles et la photo rapprochée. Aucune notice PDF ou CAO native propre à Ewwtrey/DJJRX/260018 identifiée dans la fiche consultée et les recherches par ASIN. La notice PDF de ce dossier est **rédigée pour le projet**, pas un document constructeur.

Le fabricant du Pi publie son [plan mécanique]({PI}) : quatre trous Ø2,7 et rectangle 58 x 49 mm. Le plan avertit que ces cotes sont approximatives, pour référence et non pour des données de production. Son repère Ø3 concerne des trous de cooler ; ne pas les substituer aux quatre fixations de carte.

Le [catalogue Essentra]({ESSENTRA}), fabricant différent, présente des exemples M2.5 x 0.45. Il justifie l'hypothèse usuelle de pas de la CAO ; **aucune cote de tête, matière, tolérance ni couple Essentra n'est attribué au kit Ewwtrey**. Le catalogue complet est archivé inchangé ; les pages pertinentes aux filetages plastiques sont listées dans notices/README.md.

L'illustration haute définition et la photo de détails confirment les MF et FF hexagonales. Les modèles gardent 5 mm surplats estimé. Profondeurs borgnes MF et traversants FF, profils, chanfreins et jeu radial sont des hypothèses explicites. Une préparation spline STEP des FF est tracée dans leurs JSON ; les contrôles finaux sont réalisés sur les fichiers réellement livrés.

Les affirmations commerciales de résistance à la chaleur et au desserrage ne donnent aucune valeur de température, de couple, de charge ou d'essai. Aucune qualification « nylon 6/6 », fibre de verre, classe feu ou autofreinage n'est retenue. Le format 170 x 97 x 18 mm et les 90 g concernent l'article entier, pas chaque entretoise ni la masse embarquée.

## Avis consultés

Affichage **4,6/5 sur 871 évaluations globales** : cette note regroupe plusieurs tailles et couleurs. Les commentaires réellement consultés sont résumés ci-dessous, sans utiliser le résumé automatique Amazon comme mesure ou preuve.

{reviews}

Ces retours permettent d'identifier des usages de montage électronique ; aucun ne valide notre Pi 5, son cooler, le connecteur GPIO ou la tenue sur le robot. La variante blanche et les commentaires M3/M4 ne certifient pas la variante noire.

## Forums, vidéos et points ouverts

Recherches par ASIN/nom et termes notice, Raspberry Pi, forum et YouTube : aucun relevé dimensionnel ou essai spécifique de ce kit exploitable trouvé. Il n'y a pas de cote manquante comblée par une valeur présentée comme mesurée.

À vérifier sur le lot : forme FF, pas, profondeurs, tailles des rondelles, qualité des filetages et quantité. À définir lors du châssis final : hauteur et vis, épaisseurs locales, appuis, accès et dégagements. À qualifier ensuite : maintien en vibrations/chocs et serrage sans déformation. La sélection commerciale reste documentée et non achetée.
''')
 write('photos/README.md','''# Images commerciales originales

Quatre JPEG Amazon téléchargés le 14 octobre 2026 depuis les URL réellement observées sur la fiche sélectionnée : kit complet, illustration des tailles, photo des pièces et détail des formes.

Fichiers « original » conservés sans modification. L'illustration des longueurs ne cote pas les surplats ou les rondelles. Les slogans des images ne sont pas des valeurs de température ou de résistance. Droits des images conservés à leurs titulaires ; usage documentaire interne du projet. URL, tailles et SHA256 dans ../assets.json.
''')
 write('notices/README.md',f'''# Notices et documents

- [Notice V3](notice-fixations-pi-5-v3.pdf) : document rédigé pour ce projet. Aucune notice constructeur du kit Ewwtrey identifiée ; ne pas confondre cette notice avec un certificat de fabricant.
- [Raspberry Pi 5, plan original](RaspberryPi-5-plan-mecanique-original.pdf) : une page, référence officielle téléchargée sans modification. Dimensions approximatives, non destinées à la production. [Source]({PI}).
- [Essentra, catalogue original de fixations plastiques](Essentra-filetages-plastiques-reference-original.pdf) : 106 pages, fabricant différent. Exemple M2.5 x 0.45 inspecté à la page PDF 39 (page imprimée 150). Autres mentions M2.5 repérées aux pages PDF 35, 37, 41, 45, 47, 48, 50, 52, 59, 71, 86, 87, 88, 93. Seul le pas métrique usuel sert de repère ; aucune cote/qualité de ces articles n'est transférée au kit. [Source]({ESSENTRA}).

Les archives originales sont associées à des SHA256 dans ../assets.json. Photos, fiche commerciale, avis et statut des recherches sont conservés dans les fichiers voisins. Aucun PDF manquant ou source inaccessible n'est remplacé par une « notice constructeur » fabriquée.
''')
 cat=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'))
 rows='\n'.join(f"| [{m['title']}]({m['file']}) | [{m['preview']['file']}]({m['preview']['file']}) | {m['validation']['solids']} | {m['bytes']/1024:.0f} Ko |" for m in cat['models'])
 write('3D/README.md',f'''# Modèles 3D des fixations du Pi 5

**15 STEP colorés en millimètres**, reconstruits depuis les longueurs publiées et les photos du kit Ewwtrey noir. Ni CAO native de ce kit, ni modèle issu de mesures physiques. Les profils intérieurs/extérieurs sont des hélices réelles ; les détails fins estimés sont tracés dans [cotes.md](../cotes.md), [catalogue.json](catalogue.json) et chaque JSON voisin.

| Modèle STEP | Aperçu | Solides | Taille |
| --- | --- | ---: | ---: |
{rows}

Le modèle d'assemblage dispose **20 pièces aux quatre points de fixation du Pi**, sur rectangle de référence 58 x 49 mm. Le PCB et le châssis sont volontairement absents ; les espaces qu'ils occuperaient correspondent à des épaisseurs provisoires. La hauteur 10 mm reste un exemple : **châssis conçu en dernier** et hauteur définitive à décider alors.

Noir nylon, chanfreins et empreintes cruciformes, formes hexagonales d'après la photo de détails. Le fournisseur ne publie pas les profondeurs internes et les cotes fines. Aucun plan de production ou fichier de jauge n'est revendiqué.

Génération : tools/build_pi_mount_step.py. Réimport CadQuery, couleurs STEP, solides et volumes contrôlés ; [contrôle FreeCAD indépendant](validation-freecad.json) sans interface graphique. Aucun essai dans FreeCAD GUI ou CAD View déclaré, aucune qualification mécanique. Les STEP du Pi, du cooler et du GPIO sont inchangés.
''')
 dump('3D/provenance.json',dict(date=DATE,kit_asin='B0DCS5C7SN',native_vendor_cad=False,physical_measured=False,
  sources=['../observation-amazon.json','../photos/Ewwtrey-longueurs-original.jpg','../photos/Ewwtrey-details-original.jpg','../notices/RaspberryPi-5-plan-mecanique-original.pdf'],
  nominal_published=['Lengths and quantities, commercial M2.5 designation','Pi mounting pattern, reference only'],
  estimated=['All fine fastener dimensions, material grade unknown','Pitch .45 assumed','Thread root/crest/clearance, entry bevels, head recess','MF blind depth and FF through bore','Assembly thicknesses, provisional 10mm height'],
  chassis_design_deferred=True,chassis_is_final_component=True,hardware_tested=False))
 table=ROOT/'Composants/README.md';s=table.read_text(encoding='utf-8')
 row='| [Fixations du Pi 5](fixations-raspberry-pi-5/README.md) | Ewwtrey 335 pièces nylon noir M2.5, B0DCS5C7SN | 9,98 € TTC | En stock au relevé du 14 octobre ; non acheté ; quinze STEP ; hauteur provisoire, châssis en dernier |'
 if '[Fixations du Pi 5](fixations-raspberry-pi-5/README.md)' not in s:
  anchor=next(line for line in s.splitlines() if line.startswith('| [Connecteur GPIO et faisceau]'))
  s=s.replace(anchor,anchor+'\n'+row,1);table.write_text(s,encoding='utf-8')
 block(table,'fixations-pi-v3','Les [fixations isolantes du Pi 5](fixations-raspberry-pi-5/README.md) retiennent le kit Ewwtrey noir M2.5, 335 pièces, 9,98 € TTC sur Amazon.fr au 14 octobre 2026. Notice, devis, cotes, avis, documents originaux et [quinze STEP](fixations-raspberry-pi-5/3D/README.md). Montage à 10 mm provisoire ; hauteur, appuis et vis à confirmer lorsque le châssis sera conçu, en dernier.')
 readme=ROOT/'ReadMe.md';block(readme,'fixations-pi-v3','Les [fixations du Pi 5](Composants/fixations-raspberry-pi-5/README.md) disposent du dossier complet et de quinze STEP détaillés : kit Ewwtrey M2.5 nylon noir, 335 pièces, 9,98 € TTC au relevé Amazon.fr du 14 octobre 2026. Exemple de quatre supports à 10 mm, hauteur provisoire. **Le châssis sera le dernier composant conçu**, selon le choix utilisateur ; implantation et dimensions de fabrication restent ouvertes.')
 spec=ROOT/'SPECIFICATIONS.md';s=spec.read_text(encoding='utf-8')
 old='| Fabrication | Châssis fabriqué, composants séparés ; pas de voiture RC complète |'
 new='| Fabrication | Châssis fabriqué, composants séparés ; pas de voiture RC complète ; conception du châssis en dernier, comme dernier composant (décision du 14 octobre 2026) |'
 if old in s:spec.write_text(s.replace(old,new,1),encoding='utf-8')
 block(ROOT/'Composants/raspberry-pi-5/integration.md','fixations-pi-v3','Les [fixations du Pi](../fixations-raspberry-pi-5/README.md) utilisent un kit Ewwtrey M2.5 nylon noir. Quatre supports MF 10+6 mm constituent seulement le montage de travail ; longueur des vis et hauteur finale à décider lors du châssis, conçu en dernier. Les quatre trous de carte et les deux trous dédiés au cooler ont des fonctions distinctes. Vérifier les dégagements avec tous les composants et câbles ; la validité des STEP ne qualifie pas le montage.')
 print('DOSSIER COMPLETE',len(parts),'types, kit335, allocation20, reserve315',flush=True)

if __name__=='__main__':main()
