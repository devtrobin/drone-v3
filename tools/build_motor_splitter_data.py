"""Build documentation and calculations for the exact UD80A motor splitter."""
from pathlib import Path
import json,sys,pymupdf
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/repartition-moteurs'
NVENT='https://www.nvent.com/en-us/ERIFLEX/products/EFSUD-80A'
MANUAL='https://nvent.widen.net/content/vhxyvvgeqg/original/ip7802.pdf'
def write(name,text):
    p=BASE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.strip()+'\n',encoding='utf-8')
def data(name,d):write(name,json.dumps(d,ensure_ascii=False,indent=2))
def main():
    sys.stdout.reconfigure(encoding='utf-8')
    write('README.md',f'''# Répartition positive après relais - nVent ERIFLEX UD-80A

Sélection d'étude du **14 octobre 2026** : **une unité UD-80A, article 569010**, non achetée et non testée. Bloc unipolaire à capot bleu articulé, **80 A IEC / 85 A UL/CSA**, une entrée et six sorties toutes communes. Nous utilisons **une arrivée et deux sorties** vers les porte-fusibles moteurs ; quatre sorties restent en réserve.

| Caractéristique fabricant | Valeur |
| --- | --- |
| Fonction | Répartition passive du positif, pas une coupure ni une protection contre les surintensités |
| Enveloppe nominale H × W × D | 69 × 30 × 46 mm, pattes comprises |
| Masse publiée | 0,07 kg, environ 70 g, hors fils et fixations |
| Entrée métrique | 1 × 6–16 mm², conducteur multibrins compact selon fiche |
| Sorties métriques | 2 × 2,5–16 et 4 × 2,5–6 mm² ; variantes de connexion selon notice |
| Protection du boîtier | IP20 ; pas une protection contre l'eau ou les poussières fines |
| Conducteur / boîtier | Cuivre étamé / thermoplastique ; capot inclus |
| Montage | Sur panneau ou rail DIN ; fixation directe au châssis proposée |

Le courant du scénario moteur est **40 A total**, hypothèse non mesurée. Le bloc offre une marge nominale, sous réserve des fils, de l'ambiante et des raccordements réels. Le calibre 80 A n'impose pas une limite de courant au robot.

## Dossier

- [Intégration, affectation des sorties et montage](integration.md), [calculs](calculs.json), [nomenclature](nomenclature.json).
- [Cotes, comparaison des sources et limites](cotes.md), [recherche, prix, citation et retours d'utilisation](recherche-technique.md).
- [Notice PDF du projet et originaux fabricant](notices/README.md), [photos et plans](photos/README.md).
- [Cinq STEP et contrôles FreeCAD](3D/README.md) : **original constructeur conservé intact**, implantation, sans capot, éclaté et capot séparé.
- [Sources](sources.json), [archives et SHA256](assets.json).

## Achat

[Recherche Amazon.fr exacte](https://www.amazon.fr/s?k=Eriflex+UD-80A+569010) : **aucune offre exacte ni ASIN vérifié**, réponse directe vide. Ne pas assimiler un UKK80 générique à cette référence ou lui attribuer la CAO/certification nVent.

Alternative d'achat identifiée chez [RS France, code 277-6180](https://fr.rs-online.com/web/p/blocs-de-distribution/2776180) : **17,61 € HT / 21,13 € TTC** affichés le 14 octobre 2026, stock annoncé sur la page ; frais de traitement/livraison à vérifier. Prix daté, pas panier payé ni garantie de disponibilité future. Conditionnement fabricant : une unité, avec capot ; aucun câble, embout ou rail DIN supposé inclus.

La [fiche constructeur]({NVENT}) et la [notice IP7802]({MANUAL}) sont archivées. Les valeurs IEC et UL de serrage/dénudage diffèrent pour les grosses bornes ; la notice de montage distingue les tableaux et les points à confirmer sur le lot.
''')
    write('integration.md',f'''# Implantation et raccordement V3

```mermaid
flowchart LR
 D[MiniBus positif P3] -->|Cuivre 6 mm2 proposé| S[D1D100 : +2 puis 1]
 S -->|Une seule cosse sur sortie SSR| J[UD80A 569010 : entrée IN]
 J --> O1[Sortie petite S1 : fil 12 AWG du 5065]
 J --> O2[Sortie petite S4 : fil 12 AWG du 5065]
 O1 --> F1[ATO30 puis ESC arrière 1]
 O2 --> F2[ATO30 puis ESC arrière 2]
```

Le bloc distribue **le positif commuté après le relais**, pas le positif permanent du MiniBus et pas le négatif. Ses sept connexions sont électriquement communes. Repères IN/S1–S4/L1–L2 définis pour le projet, **pas des inscriptions constructeur**. Aucun empilage de deux cosses sur la borne 1 du D1D100 nécessaire dans cette proposition.

| Repère V3 | Interface | Affectation |
| --- | --- | --- |
| IN | Grande entrée 6–16 mm² | Arrivée depuis borne 1 du D1D100, cuivre 6 mm² proposé |
| S1 | Première petite sortie 2,5–6 mm² | Fil d'arrivée 12 AWG du porte-fusible ESC1 |
| S4 | Quatrième petite sortie 2,5–6 mm² | Fil d'arrivée 12 AWG du porte-fusible ESC2 |
| S2, S3 | Deux petites sorties restantes | Réserves sans conducteur |
| L1, L2 | Grandes sorties 2,5–16 mm² | Réserves sans conducteur |

Le 12 AWG est environ 3,31 mm² nominal, dans la plage métrique des petites sorties. Les fils 16 AWG des ESC font environ 1,31 mm² : **ils ne vont pas directement dans ces sorties de minimum 2,5 mm²**. Les porte-fusibles et prolongements restent intercalés selon le dossier moteurs. Un fil par orifice utilisé ; pas de doublage improvisé dans un embout ou une borne.

Ne pas substituer un embout 4 mm² au 12 AWG sans vérifier son adaptation au conducteur et à la borne. Choisir un embout et un sertissage pour la section réelle et la classe des brins. La fiche d'entrée cite le multibrins compact ; l'acceptation de notre fil souple exact et de son embout doit être vérifiée avec la notice du lot. La possibilité générale « avec ou sans embout » ne dispense pas de cette vérification.

## Montage et serrage

Valeurs de la [notice officielle IP7802_M]({MANUAL}), tableau **IEC page 1**, retenues pour préparer l'étude européenne :

| Groupe | Sections IEC | Couple de borne | Dénudage publié |
| --- | --- | ---: | ---: |
| Entrée IN | 6–16 mm² | 3,5 N·m | 17,0 mm |
| Grandes sorties L1/L2 | 2,5–16 mm² | 3,5 N·m | 17,0 mm |
| Petites sorties S1–S4 | 2,5–6 mm² | **1,2 N·m** | **10,2 mm** |

La page **UL/CSA 2** indique 19,5 in-lb (environ **2,20 N·m**) et 0,36 pouce (**9,14 mm**) pour entrée/grandes sorties ; 10,6 in-lb (**1,20 N·m**) et 0,40 pouce (**10,16 mm**) pour les petites. Ce ne sont pas des conversions équivalentes du tableau IEC pour les grosses bornes. Garder les régimes séparés, vérifier le marquage/la notice reçue et résoudre l'écart avant câblage de l'entrée ; ne pas mélanger couple IEC et longueur UL.

La notice demande de **serrer aussi les vis des orifices inutilisés** au couple de leur groupe. Elle demande de maintenir le câble d'entrée à environ **15 cm du bloc**. Prévoir une retenue mécanique compatible avec notre implantation ; ni traction du faisceau ni charge sur la petite vis de borne. Aucune graisse ou traitement supplémentaire ajouté sans prescription applicable.

Fixation directe au panneau proposée pour éviter un rail DIN supplémentaire. La notice donne un repère de fixation **54 mm** et une cote **4,5 mm**, avec annotation **M5** ; la géométrie exacte et le passage de la vis doivent être contrôlés sur la pièce. Ne pas transformer automatiquement la cote 4,5 en un perçage de dégagement M5 garanti. Visserie, isolant de support et méthode de retenue restent à sélectionner. Ouverture du capot et accès à l'outil doivent rester possibles.

Batterie et prise d'équilibrage débranchées : dénuder selon le groupe et le régime applicable, ne pas blesser les brins, insérer entièrement et contrôler l'absence de cuivre exposé. Serrer avec un outil adapté et contrôlé ; refermer le capot. L'IP20 ne permet pas une exposition à l'eau ni au copeau conducteur.

## Courant, température et défauts

Scénario : **40 A total**, deux départs supposés 20 A. Capacité nominale IEC 80 A, soit charge nominale 50 %. Déclassement publié pour viser 85 °C de fonctionnement : 80 A jusqu'à 40 °C ambiants, **60 A à 60 °C**, **53,6 A à 65 °C**, **46,4 A à 70 °C**, **37,6 A à 75 °C**. Ces valeurs multiplient le coefficient fabricant par 80 A dans ses conditions ; elles ne prouvent pas 80 A avec notre câble 6 mm² ou n'importe quel montage.

Le scénario 40 A ne rentre plus à 75 °C selon cette seule courbe. Viser l'air local de l'étude V3, 40 °C, puis mesurer températures, courants et chutes des trois connexions utilisées. Résistance de contact et pertes exactes du bloc non publiées dans les documents consultés ; ne pas inventer un rendement ou une autonomie.

Le tronc et les fils d'arrivée avant les ATO30 restent **coordonnés avec le principal MIDI 60 A**, pas protégés par les ATO situés plus loin. Rapprocher les deux porte-fusibles de la dérivation et garder leurs arrivées très courtes, isolées et retenues. La section 12 AWG de ces arrivées ne devient pas automatiquement protégée par le principal : revoir sa tenue au défaut et le chemin réel.

Le fabricant publie **Icw 3 kA / 1 s**, **Ipk 22 kA** et **SCCR jusqu'à 100 kA** ; ces grandeurs sont distinctes. Le bloc est passif et ne coupe pas ce courant. La notice UL relie le SCCR 100 kA à une protection par fusible **200 A Class J ou T**, 600 V maximum ; cette association **n'est pas notre MIDI 60 A**. Ne pas transférer cette qualification au faisceau V3, aux ATO à 1 000 A ou au SSR. Aucune tenue globale LiPo ou sélectivité démontrée ici.

## Qualification à effectuer

Vérifier référence/lot, régime de serrage, dénudage, brins et embouts ; continuité des sept connexions, polarités et isolement hors tension. Première alimentation limitée après contrôle du schéma. Mesurer la somme des courants, les chutes aux trois bornes utilisées, l'échauffement et la tenue sous vibration sur l'usage prévu. Contrôler freinage/régénération et la perte d'un seul départ avec le système d'arrêt supervisé à concevoir. Aucun essai de court-circuit volontaire du pack.

[Relais et surveillance](../protection-batterie/integration.md), [deux protections ESC](../protection-branches-moteurs/integration.md), [distribution principale](../distribution-alimentation/integration.md), [fusible principal](../protection-surintensite/integration.md).
''')
    write('cotes.md','''# Cotes et provenance

**Aucun matériel mesuré.** Référence UD-80A / 569010 ; original STEP obtenu via le service CAD lié à la page fabricant, format AP214, entrée ZIP E10106602.step.

| Donnée | Valeur | Provenance / portée |
| --- | --- | --- |
| Enveloppe nominale H/W/D | 69 / 30 / 46 mm | Fiche nVent 2023, p2 ; pattes comprises |
| Repère de fixation | 54 mm | Instruction IP7802_M, p1 |
| Cote de fixation indiquée | 4,5 mm, annotation M5 | Instruction ; passage de la vis et géométrie sur pièce à confirmer |
| Masse nominale | 0,07 kg | Fiche ; accessoires et câbles exclus |
| Entrée / sorties | 1 / 6 communes | Fiche et plans : deux grandes sorties, quatre petites |
| Matériaux | Cuivre étamé, thermoplastique | Référence produit ; détails de grade de chaque pièce non tous publiés |
| Capot | Bleu transparent, articulé/amovible | Photographies et fiche fabricant ; inclus |
| Fils, embouts, vis de panneau | Absents de la CAO | Choix du faisceau ultérieur |

Les enveloppes précises issues du STEP et des exports sont consignées dans [catalogue.json](3D/catalogue.json). Elles diffèrent légèrement des valeurs commerciales arrondies ; réserver aussi l'accès à l'outil, les fils et l'ouverture du capot. Le STEP officiel contient **trois solides** : il ne présente pas toutes les vis et petites formes comme des pièces séparées. Il n'est pas un dossier de fabrication ou une simulation électrique.

Repère natif : X hauteur fabricant, Y profondeur, Z largeur, centre non nul. Repère d'implantation V3 : X largeur, Y longueur de fixation, Z profondeur depuis le plan arrière. Rotation autour de (1,1,1) de +120°, puis translation définie dans les JSON. Les dérivés gardent les formes officielles ; couleurs de lecture attribuées et capot bleu rendu opaque. L'original reste intact, avec les styles exportés par le fabricant.

Vue sans capot : retrait du solide officiel correspondant. Vue éclatée : capot décalé de Z+22 mm ; présentation séparée, pas trajectoire garantie de charnière. Aucune géométrie interne supplémentaire inventée. Une intersection de volume d'environ 5,10 mm³ entre socle et capot est héritée de l'assemblage fabricant et conservée, sans correction de forme ; ce n'est pas une preuve d'ajustement sur pièce. Les calculs d'enveloppe utilisent le calcul précis OpenCascade sans triangulation pour les surfaces courbes ; imports indépendants FreeCAD contrôlés.

La photo RS montre un marquage historique ERICO / 690 V ; la photo nVent et la fiche actuelle indiquent ERIFLEX / 1 000 V AC/DC IEC. Cette variation est conservée comme provenance de révision ; ne pas recopier un ancien marquage sur un modèle prétendument mesuré. Les dimensions de colis Graybar et les bornes Amazon UKK80 génériques ne servent pas de cotes de cette référence.
''')
    write('recherche-technique.md',f'''# Recherche, alternatives, prix et témoignages

Recherche du **14 octobre 2026**. Le besoin est une jonction positive après SSR, pour deux départs protégés, avec capacité publiée supérieure ou égale à 60 A et une arrivée 6 mm². Une unité **nVent ERIFLEX UD-80A / 569010** est retenue pour l'étude.

| Solution examinée | Résultat |
| --- | --- |
| **UD-80A, 569010** | 80 A IEC, capot, arrivée 6–16 mm² et sorties adaptées au 12 AWG des supports ; fixation panneau, notice et CAO officielles disponibles |
| UKK80 générique | Annonces et tableaux marchands 80/85 A, variantes et dimensions différentes ; pas d'identification constructeur fiable pour une offre Amazon exacte, non assimilé au nVent |
| Blue Sea 2315 déjà retenu | 100 A documentés, mais 106,68 mm de long et environ 80 g ; un troisième bus n'est pas ajouté ici |
| Blue Sea 2303/2307 | 150 A, quatre goujons 1/4-20 ; cosses et encombrement supplémentaire, non retenu pour cette jonction |
| Mini PowerPost / empilage sur SSR | Connexions et capacité dépendant des cosses ; notre proposition évite un empilage non qualifié sur le relais |
| Répartiteur de charge à MOSFET ou diodes | Fonction différente et souvent 12/24 V ; ne remplace pas une jonction passive pour notre 2S et sa régénération |

## Achat et conditionnement

Requêtes Amazon : `Eriflex UD-80A 569010`, `répartiteur unipolaire 80 A`, `UKK80`, variantes Blue Sea. [Recherche Amazon.fr exacte](https://www.amazon.fr/s?k=Eriflex+UD-80A+569010) : réponse directe vide, **aucun ASIN exact, stock, vendeur ou prix vérifié**. L'icône Amazon affichée sur ejoker correspond au paiement, pas à une preuve de vente sur Amazon. Aucune commande effectuée.

Alternative française précise : [RS 277-6180](https://fr.rs-online.com/web/p/blocs-de-distribution/2776180), référence fabricant 569010, **17,61 € HT / 21,13 € TTC** affichés, stock annoncé. Frais de traitement/livraison non inclus dans ce prix validé ; ne pas prétendre une livraison gratuite pour une commande isolée. Repère étranger : Iconopower annonce 17,15 USD, hors conditions France. Le conditionnement fabricant est **une pièce**, avec capot. Aucun rail, embout ou conducteur supposé fourni.

## Documents qui lèvent les ambiguïtés

- [Fiche fabricante 2023 via RS](notices/nVent-UD80A-fiche-FR-2023-via-RS.pdf) : 80 A IEC / 85 A UL, plages distinctes entrée/sorties, nominal 69×30×46 mm, 70 g, IP20 et déclassement.
- [Notice IP7802_M]({MANUAL}), deux pages : tableau IEC et tableau UL, dénudage, couples, serrage des orifices inutilisés, maintien de l'entrée vers 15 cm, fixation et condition de SCCR. Couples/dénudages des grosses bornes divergent entre régimes ; ne pas les mélanger et vérifier la notice reçue.
- [Spécification UD 2022](notices/nVent-UD-specifications.pdf) : composition générale, bornes et capot, ambiantes selon IEC/UL/CSA ; ce document de famille n'est pas une preuve de grade ou de performance de chaque lot.
- Catalogue P1215C et fiches 2020 sont conservés comme références historiques ; ni une température marchande « minimum 30 °C » ni une longueur Graybar de colis ne remplacent les documents fabricant.
- La page nVent contient un module CAD dynamique public. Le service proposé a fourni un **ZIP AP214**, dont le STEP est conservé intact. Pas d'authentification, de compte ou de contact fabricant utilisé.

Citation courte, fiche nVent française : **« Capot à charnière articulée et amovible »**. Le capot inclus est modélisé séparément ; il protège les doigts selon IP20, sans étanchéité annoncée.

## Retours utilisateurs et vidéos

[Forum PLCtalk, discussion « SCCR in the feeder »](https://www.plctalk.net/forums/threads/sccr-in-the-feeder.125932/), **rupej, 11 août 2020, message nº8**, dit utiliser souvent le UD-80A et interroge son SCCR. **jraef, message nº9**, renvoie à la notice et à la protection Class J/T. Témoignage d'usage industriel, pas test de notre robot ; l'information de coordination est corroborée par la notice officielle, pas acceptée sur le seul forum.

Iconopower affiche 5/5 avec **un avis intitulé « test3 » signé Iconopower Admin** en 2016. Ce n'est pas un retour utilisateur indépendant et il est exclu de l'appréciation de fiabilité. Aucun taux de panne, mesure de chute ou essai thermique V3 trouvé.

Recherches YouTube par `Eriflex UD80A`, `UD-80A installation` : aucun essai exact attribuable à cette référence apportant courant/thermique/défaut LiPo identifié. Aucune vidéo non visionnée utilisée comme preuve. Aucun forum, vendeur ou fabricant contacté.

## Points encore à qualifier

Serrage/dénudage du régime applicable au lot, compatibilité du fil d'entrée souple et de l'embout, passage des vis de panneau, retenue du faisceau et place d'ouverture. Mesurer chutes et échauffement avec notre courant et les câbles réels. Le SCCR 100 kA conditionnel ne qualifie ni notre MIDI, ni les ATO à 1 000 A, ni le SSR. La sélection n'établit aucune vitesse ou autonomie physique.
''')
    temps=[30,35,40,45,50,55,60,65,70,75];coeff=[1,1,1,.94,.88,.82,.75,.67,.58,.47]
    data('calculs.json',dict(checked_on='2026-10-14',status='study, not measured',motor_total_assumed_A=40,individual_motor_assumed_A=20,
        current_limit_enforced=False,nominal_current_IEC_A=80,nominal_current_UL_A=85,nominal_IEC_loading_fraction=40/80,
        derating=[dict(ambient_C=t,coefficient=d,computed_IEC_allowance_A=80*d,scenario40A_within_nominal=40<=80*d) for t,d in zip(temps,coeff)],
        terminal_operating_target_C=85,manufacturer_ambient_context='inside enclosure',rating_with_6mm2_actual_wire_validated=False,
        holder_12AWG_nominal_mm2=3.31,ESC16AWG_nominal_mm2=1.31,small_output_min_mm2=2.5,
        IEC_preparation=dict(input_torque_Nm=3.5,input_strip_mm=17,large_output_torque_Nm=3.5,large_output_strip_mm=17,small_output_torque_Nm=1.2,small_output_strip_mm=10.2),
        UL_table=dict(input_large_torque_in_lb=19.5,input_large_torque_converted_Nm=19.5*.112984829,input_large_strip_in=.36,input_large_strip_converted_mm=.36*25.4,
            small_torque_in_lb=10.6,small_torque_converted_Nm=10.6*.112984829,small_strip_in=.4,small_strip_converted_mm=.4*25.4),
        large_terminal_IEC_UL_difference_resolved_on_received_lot=False,contact_resistance_published_ohm=None,power_loss_guaranteed=False,
        short_circuit=dict(Icw_A=3000,Icw_seconds=1,Ipk_A=22000,SCCR_A=100000,SCCR_condition='IP7802 UL:200A ClassJ orT fuse,600Vmax',SCCR_transferred_to_MIDI60A=False,V3_combined_qualification=False)))
    data('nomenclature.json',dict(checked_on='2026-10-14',status='selected for study, not purchased',items=[dict(ref='JM1',part='nVent ERIFLEX UD-80A',article='569010',quantity_installed=1,
        included='one block with hinged blue cover',connections_used=3,reserved_outputs=4,amazon_exact_asin=None,amazon_fr_offer_confirmed=False)],
        french_alternative=dict(seller='RS France',code='277-6180',price_each_HT_EUR=17.61,price_each_TTC_EUR=21.13,shipping_included=False,stock_page_announced=True,checked_on='2026-10-14'),
        additional_parts=['one power cable SSR1 to IN,6mm2 proposed','matching single lug on SSR terminal1','appropriate conductor ferrules/crimp tooling if used','panel fasteners and cable retention'],
        install_on_panel_proposed=True,DIN_rail_added_to_bom=False,total_delivered_price_eur=None))
    sources=[('manufacturer',NVENT,'manufacturer','exact attributes, photos, manual andCADdownloadmodule read from archivedpublicHTML'),
        ('manual',MANUAL,'manufacturer_instruction','IP7802_M IEC/UL tables andSCCRcondition'),
        ('datasheet2023','https://docs.rs-online.com/e8ac/A700000010539200.pdf','manufacturer_document_via_distributor','FR2023threepages; cotes/derating/ranges'),
        ('spec2022','https://nvent.widen.net/content/ngmdxkxgcd/original/pi-ud_blocks_specs.pdf','manufacturer_family_specification','revision2022-11-15; material/ambientcontexts'),
        ('CAD','https://noproxy-download.nvent.com/api/traceparts/download?part_number=UD-80A&format=19&brand=ERIFLEX','manufacturer_CAD_download','zipE10106602.step intact; geometries reused forderivatives'),
        ('RSFrance','https://fr.rs-online.com/web/p/blocs-de-distribution/2776180','distributor_offer','17.61HT/21.13TTC; stockannounced; deliverynotincluded'),
        ('Amazon','https://www.amazon.fr/s?k=Eriflex+UD-80A+569010','marketplace_search','noexactofferorASINverified'),
        ('forum','https://www.plctalk.net/forums/threads/sccr-in-the-feeder.125932/','first_hand_user_forum','rupej2020-08-11#8 usesUD80A; jraef#9 refersinstruction; noRCtest'),
        ('reviewexcluded','https://www.iconopower.com/Single_Pole_Distribution_Block_p/569010.htm','merchant','admin test3 reviewexcluded;17.15USDforeignreference'),
        ('historicalFR','https://res.cloudinary.com/sonepar-fr/raw/upload/s--hVva9jzD--/v1/documents/3058/569010_FICHE.pdf','manufacturer_document_via_distributor','2020two-page reference,70g andderating'),
        ('RSphoto','https://media.rs-online.com/f_auto%2Cq_auto%2Cbo_1.5px_solid_white%2Cb_auto%2Cc_pad%2Cdpr_2%2Ch_399%2Cw_710/c_pad%2Ch_399%2Cw_710/Y2776180-01?pgw=1','merchant_photo','historicalERICO690Vmark; notlatestfactory marking')]
    data('sources.json',dict(checked_on='2026-10-14',sources=[dict(id=i,url=u,type=t,support=s) for i,u,t,s in sources],native_vendor_step_obtained=True,
        manufacturer_contacted=False,hardware_measured=False,exact_youtube_test_found=False,amazon_fr_offer_verified=False))
    notices=['# Notices et documents originaux','', '[Notice de projet V3](notice-repartition-moteurs-v3.pdf) : sélection, câblage, cotes et qualification. Document rédigé pour le projet ; ne remplace pas la notice du lot.','',
        '| Document archivé inchangé | Pages |','| --- | ---: |']
    for path in sorted((BASE/'notices').glob('*.pdf')):
        if path.name=='notice-repartition-moteurs-v3.pdf':continue
        notices.append(f'| [{path.stem}]({path.name}) | {len(pymupdf.open(path))} |')
    notices+=['','À lire en priorité : **IP7802_M**, pages 1–2, pour le montage ; **fiche FR 2023**, pages 2–3, pour connexions et déclassement. La spécification UD 2022 est un document de famille ; le catalogue P1215C possède 56 pages. Les copies Graybar FR/DE/EN sont conservées telles que fournies.',
        '', 'Aucun document original retouché. URL, SHA256 et statuts dans [assets.json](../assets.json).']
    write('notices/README.md','\n'.join(notices))
    write('photos/README.md','''# Photos et plans de référence

- [Photo fabricant nVent](nVent-UD80A-produit-original.webp), produit ERIFLEX, capot bleu transparent.
- [Photo commerciale RS](RS-569010-original.jpg), marquage ERICO historique ; photo de variante/révision, pas une mesure sur le lot acheté.
- [Plan de face](nVent-UD80A-plan-face.webp), [profil](nVent-UD80A-plan-profil.webp), [connexions](nVent-UD80A-plan-connexions.webp) issus de la page fabricant.

Fichiers conservés inchangés. Les axes H/W/D sont définis par le constructeur ; seuls nominal 69/30/46 et fixation 54/4,5 sont cotés dans les documents consultés. [Sources et empreintes](../assets.json), [cotes et réserves](../cotes.md). Aucune image générée utilisée comme preuve.
''')
    cat=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'));lines=['# CAO nVent UD-80A et vues V3','',
        '**Cinq STEP en millimètres. Géométrie fabricant obtenue via son service CAD public.** Original préservé intact, dérivés d’implantation.','',
        '| Modèle | STEP | Aperçu | Taille |','| --- | --- | --- | ---: |']
    for m in cat['models']:lines.append(f"| {m['title']} | [STEP]({m['file']}) | [PNG]({m['preview']['file']}) | {m['bytes']/1e6:.2f} Mo |")
    lines+=['','Les formes du fabricant sont conservées. L’original garde ses styles ; les dérivés attribuent des couleurs de lecture et rendent le capot bleu opaque. La vue éclatée déplace seulement le capot. Pas de fils, embouts, vis de châssis ou géométrie interne supplémentaire inventée.',
        '', 'Le modèle natif ne détaille pas toutes les vis comme pièces séparées. Enveloppe CAO précise dans les JSON ; cotes commerciales arrondies et réserves dans [cotes.md](../cotes.md).',
        '', '[Contrôles FreeCAD sans interface](validation-freecad.json), [sources](../sources.json), [archives ZIP et empreintes](../assets.json). Validité, solides fermés, enveloppes et réimports vérifiés ; aucun essai GUI FreeCAD/CAD View ou matériel revendiqué.']
    write('3D/README.md','\n'.join(lines));print('Dossier,calculs,sources,index written',flush=True)
if __name__=='__main__':main()
