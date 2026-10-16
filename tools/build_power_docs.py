"""Project documentation for the battery, Pi supply and charger choices.

Do not promote an inaccessible Amazon France page to a verified offer. Prices
remain null; manufacturer CAD and measured hardware are different evidence.
"""
from pathlib import Path
from urllib.parse import quote_plus
import json,math,hashlib

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'Composants'
DATE='2026-10-13'
DATA=[
 dict(folder='batterie',title='Batterie de propulsion et d’électronique',reference='Zeee 2S1P 7,4 V 5 200 mAh 80C — boîtier rigide, XT60',
      asin='B08DCYVHSF',amazon_us='https://www.amazon.com/dp/B08DCYVHSF',quantity='Une batterie embarquée ; référence Amazon vendue en lot de deux. La seconde est une réserve, sans mise en parallèle.',
      primary='https://zeeebattery.com/products/zeee-2s-lipo-battery-5200mah-7-4v-80c-xt60-plug',
      facts={'Configuration':'LiPo standard 2S1P, 7,4 V nominal, 8,4 V pleine charge ; pas LiHV',
             'Capacité / énergie annoncée':'5 200 mAh / 38,48 Wh par batterie ; capacité réelle non mesurée',
             'Dimensions fabricant':'138 × 47 × 25 mm, tolérance annoncée ±2 mm ; fils et connecteurs hors boîtier',
             'Masse approximative':'250 g par pack annoncés',
             'Prises':'Puissance XT60 ; prise d’équilibrage 3 voies visible, famille JST-XH à vérifier sur le pack reçu',
             '80C':'Notation commerciale annoncée ; aucun essai indépendant de courant continu pour cet ASIN n’est validé',
             'Limites cellule publiées':'Ne pas dépasser 4,2 V ; ne pas descendre sous 3,2 V par cellule. Une tension totale ne surveille pas chaque cellule.',
             'Usage':'Un seul pack alimente les deux ESC et la branche Pi ; servo sur le BEC d’un seul ESC réglé à 6 V'},
      why='La 2S conserve le dimensionnement moteur/transmission existant. Le pack de 5,2 Ah offre une réserve d’énergie supérieure aux scénarios de 2,2 et 3 Ah, avec une masse annoncée raisonnable pour l’hypothèse de véhicule de 2 kg. La coque rigide convient à une intégration sur véhicule, à protéger et fixer sans écraser les fils.',
      unknowns=['Capacité et Wh réellement utilisables, résistance interne et déséquilibre cellule par cellule',
                'Autonomie avec caméra et Pi actives, tension pendant accélérations et vieillissement',
                'Longueurs, sections et genres réels des connecteurs ; contenu du manuel papier fourni',
                'Prix du lot, vendeur, livraison et disponibilité Amazon France'],
      reviews=[dict(url='https://www.reddit.com/r/rccars/comments/13supw9/',access='Extraits indexés seulement ; fil complet indisponible',
                    finding='Un utilisateur rapporte une capacité inférieure à la valeur affichée sur un pack Zeee 2S. La variante, les conditions et l’étalonnage ne permettent pas d’attribuer un chiffre garanti à notre ASIN.'),
               dict(url='https://www.msuk-forum.co.uk/forums/topic/244741-what-lipos-are-you-using/',access='Extraits indexés ; accès complet 403',
                    finding='Des utilisateurs de 5 200 mAh 2S rigides rapportent un bon rapport prix/usage ; un fil d’équilibrage jugé court est signalé. Retours individuels, pas des mesures d’autonomie V3.'),
               dict(url='https://www.rctalk.com/forum/threads/what-is-your-favorite-lipo-battery.129416/page-3/',access='Extraits indexés',
                    finding='Un témoignage critique décrit une chute de tension sous charge sur des packs Zeee, tandis que d’autres sont satisfaits. Prévoir une mesure de tension pendant les pointes plutôt que conclure à partir de la marque.')],
      notice='Choisir le mode **LiPo standard 2S**, charge équilibrée, fin normale à **4,20 V par cellule**. Le choix conservateur de projet est **2,6 A au premier contrôle (0,5C)** puis au plus **5,2 A (1C)** uniquement si la notice du pack livré le permet. Vérifier tension et polarité avant raccordement. La batterie se charge hors véhicule, isolée de la propulsion et du régulateur. Ne pas laisser la charge sans surveillance ; respecter le manuel fabricant livré et celui du chargeur. Pour le stockage, utiliser le mode LiPo STORAGE du chargeur, nominalement autour de 3,8 V/cellule, et surveiller l’état du pack.',
      notice_extra='Le fabricant annonce un manuel dans le lot, mais aucun PDF original téléchargeable de cette variante n’a été identifié. Ce dossier conserve les instructions publiques du fabricant et une notice **de projet**, sans attribuer à Zeee une notice synthétique de sites tiers. Les limites de charge sont celles de la notice livrée en cas de divergence.',
      modeling='Reconstruction extérieure d’un seul pack : coque, joint, étiquettes vectorielles, fils continus, prise XT60 et connecteur d’équilibrage. Cotes du corps documentées ; longueurs de fils, prises, moulures et graphismes estimés. Pas de cellules internes ou de BMS fictifs.'),
 dict(folder='regulateur-alimentation',title='Régulateur de la branche Raspberry Pi',reference='Pololu D24V90F5 — article 2866, sortie fixe 5 V',
      asin='B01M9C9Q1E',amazon_us='https://www.amazon.com/dp/B01M9C9Q1E',quantity='Un régulateur embarqué pour Pi 5, caméra et refroidissement ; pas pour les moteurs.',
      primary='https://www.pololu.com/product/2866',
      facts={'Type':'Abaisseur synchrone DC-DC ; sortie nominale fixe 5 V, précision publiée ±4 %',
             'Entrée':'5–38 V annoncés ; limite basse effective = sortie + dropout dépendant du courant',
             'Courant':'Nom de produit « 9 A » ; débit continu réel selon tension, température et refroidissement. Pas 9 A garantis partout.',
             'Lecture des courbes fabricant':'Vers 5 A de sortie, dropout ≈1 V ; courbe continue ≈6,7 A à 6,5 V d’entrée. Lectures approximatives, pas des garanties.',
             'Cotes':'PCB nominal 40,64 × 20,32 mm ; épaisseur 1,57 mm ; enveloppe CAO officielle relevée dans sa provenance',
             'Fixation':'Quatre trous Ø2,18, entraxes 35,56 ×15,24 mm ; tolérances fabricant de perçage ±0,1 et bord ±0,3 mm',
             'Connexions':'VIN, GND, VOUT, EN, PG, FB ; prendre la puissance aux grands pads, pas au petit VOUT près de FB',
             'Rendement':'80–95 % typiques suivant charge/tension ; utiliser 90 % comme hypothèse de calcul, pas comme valeur mesurée',
             'USB-C / PD':'Aucun port USB-C ni source USB Power Delivery dans ce régulateur',
             'Protections intégrées':'Inversion d’entrée, courts-circuits/surintensité, température, démarrage progressif et verrouillage basse tension selon fabricant'},
      why='Sa courbe de courant procure de la marge par rapport à une branche Pi de 5 A, y compris aux tensions d’une 2S. Le dropout lu à 5 A est compatible avec une entrée de 6,4 V en régime nominal, mais les creux dus aux moteurs doivent être mesurés. Sa CAO officielle fournit une référence mécanique bien plus précise qu’une reconstruction du circuit.',
      unknowns=['Tension du module reçu (plage théorique 4,8–5,2 V) et chute jusqu’à la Pi sous charge',
                'Pointes, démarrage, ondulation, rendement et température avec Wi-Fi/caméra/moteurs actifs',
                'Faisceau protégé et raccordement Pi : étude proposée, aucun câblage validé',
                'Offre Amazon France, vendeur, authenticité et prix livré'],
      reviews=[dict(url='https://forum.pololu.com/t/powering-a-raspberry-pi-5/26012',access='Fil complet lu, septembre–octobre 2024',
                    finding='Le support Pololu considère les D24V90F5 et D24V50F5 comme des candidats pour une Pi, avec préférence pour une famille plus récente. La discussion souligne l’absence de négociation PD et le réglage de limite USB. Il ne s’agit pas d’un essai Pi 5 + caméra + moteurs.'),
               dict(url='https://forums.raspberrypi.com/viewtopic.php?p=2269299',access='Texte public consulté',
                    finding='Un utilisateur obtient un démarrage Pi 5 avec un autre convertisseur 5 V/5 A, mais conserve un avertissement d’alimentation. Témoignage utile sur la négociation ; aucune validation de notre Pololu ni de notre 2S.')],
      notice='Raccorder la batterie sur **VIN/GND**, jamais sur VOUT. La cible de branche Pi est une capacité disponible de **5 A**, pas une consommation continue supposée. Mesurer d’abord la sortie sans la Pi, puis avec une charge de contrôle. Évaluer le module de 8,4 V jusqu’à la tension d’arrêt retenue, sous la charge réelle et pendant les accélérations moteurs. Utiliser un faisceau court de puissance, soudé aux grands pads ou aux borniers adéquats ; pas de fils Dupont ni de plaque d’essai pour porter 5 A. Isoler le dessous et conserver de l’air autour du régulateur.',
      notice_extra='L’intégration proposée utilise les **rails 5 V du connecteur 40 broches de la Pi (broches physiques 2 et 4)** et plusieurs masses, via un faisceau protégé à dimensionner ; ce n’est pas une GPIO de signal. Cette entrée demande des protections externes adaptées et interdit l’alimentation simultanée par une autre source. USB-C reste possible avec une interface de source correctement conçue, mais un simple câble ne crée pas une négociation PD. Le réglage `usb_max_current_enable=1` n’est envisageable qu’après validation de la capacité de la branche : il relève une limite USB, il n’améliore pas le convertisseur. Voir le dossier commun pour les deux possibilités et les contrôles. EN est tiré vers VIN : ne pas le relier directement à une GPIO 3,3 V. PG est collecteur/drain ouvert et demande un pull-up adapté ; son seuil ≈4,5 V ne remplace pas le contrôle de sous-tension de la Pi.',
      modeling='STEP natif fourni par Pololu pour la famille commune D24V60F5/D24V90F5, conservé sans modification. Géométrie, marquages et couleurs du constructeur préservés ; pas de pistes internes ni de schéma électrique déduits du dessin.'),
 dict(folder='chargeur-batterie',title='Chargeur équilibré de la batterie',reference='SkyRC S65 — SK-100152, 65 W / 6 A, secteur intégré',
      asin=None,amazon_us=None,quantity='Un chargeur à l’atelier, hors du véhicule ; il n’entre pas dans la masse embarquée.',
      primary='https://www1.skyrc.com/s65?from=nav',
      facts={'Alimentation':'100–240 V AC ; chargeur secteur avec cordon, distinct du S65neo et des B6 sans alimentation',
             'Charge':'0,1–6 A, puissance maximale 65 W ; notre 2S à 5,2 A et 8,4 V demande au plus 43,68 W côté batterie',
             'Batteries lithium':'LiPo/LiIon/LiFe/LiHV de 2 à4 cellules ; choisir LiPo pour le pack Zeee standard',
             'Équilibrage':'300 mA/cellule max selon notice originale V2.10 et page fabricant ; ne pas recopier 1 A de fiches tierces',
             'Décharge':'0,1–2 A, limitée à 10 W ; cela limite fortement une décharge d’un gros pack',
             'Dimensions retenues':'118 ×115 ×45 mm dans la notice fabricant V2.10, page PDF24, et page fabricant actuelle',
             'Cote alternative rencontrée':'117 ×105 ×55 mm dans des fiches distributeurs : divergence conservée, aucune mesure physique',
             'Masse / affichage':'315 g annoncés, LCD 2×16 rétroéclairé bleu, quatre boutons',
             'Connectique':'XT60 en face avant, port d’équilibrage XH 2–4S et prise de sonde thermique ; genre physique des contacts à vérifier',
             'Contenu manuel':'Chargeur + cordon secteur, PDF23 ; rallonges de charge/équilibrage non annoncées dans ce contenu'},
      why='Il couvre la batterie 2S de 5,2 Ah avec charge équilibrée, stockage et lecture des cellules. Sa puissance et son courant permettent le réglage de 5,2 A sans être limités par le plafond de 65 W à 8,4 V. Sa notice originale et plusieurs photos permettent de modéliser l’extérieur sans ouvrir un appareil secteur.',
      unknowns=['Offre Amazon précise et ASIN du S65 non identifiés : ne pas inventer un lien produit',
                'Version du boîtier reçue face à la divergence de cotes des distributeurs',
                'Genre physique des contacts XT60, longueur des fils et nécessité de rallonges/adaptation d’équilibrage',
                'Temps réel de charge/stockage, exactitude tensions et courant sur l’exemplaire reçu'],
      reviews=[dict(url='https://rccrawler-france.com/threads/chargeur-et-accus.36258/',access='Fil complet lu, 27 août 2024',
                    finding='Un participant utilise un petit SkyRC depuis 2018 et le juge polyvalent et simple ; il renvoie au S65. La référence exacte de son appareil ancien n’est pas prouvée : retour de famille, pas banc d’essai S65.'),
               dict(url='https://www.studiosport.fr/chargeur-skyrc-s65-a18474.html',access='Avis utilisateur indexé daté du 30 juillet 2019',
                    finding='Un utilisateur du S65 apprécie le mode Balance et souhaiterait un interrupteur marche/arrêt. Témoignage isolé ; ne pas ajouter un interrupteur imaginaire au modèle.'),
               dict(url='https://breizh-modelisme.com/chargeur-lipo-pour-batterie-1s-2s-3s-4s-et-6s/30032581-chargeur-skyrc-s65-pour-lipo-2-4s-65w-100152-xt60.html',access='Avis affichés sur la fiche consultée',
                    finding='Un acheteur signale que le câble de charge adapté à sa batterie est à prévoir séparément. Confirmer les accessoires de l’offre choisie plutôt que supposer tous les câbles inclus.')],
      notice='Brancher le cordon secteur puis régler **LiPo BALANCE CHG, 2S, 2,6 A pour le premier contrôle**, après vérification des caractéristiques du pack. Utiliser au plus 5,2 A si le manuel Zeee livré autorise 1C. Contrôler le nombre de cellules détectées et le réglage 4,20 V/cellule avant validation. La charge équilibrée demande la liaison de puissance **et** la liaison d’équilibrage ; respecter le repérage du port XH illustré PDF12. Si un cordon est nécessaire, le connecter au chargeur avant la batterie et débrancher dans l’ordre inverse selon la notice. Ne pas charger une batterie connectée au robot. La sonde thermique montrée par le constructeur n’est pas annoncée comme fournie.',
      notice_extra='Le PDF original V2.10 est conservé inchangé. Pages utiles : PDF4 pour les ports, PDF12 pour les branchements et la charge équilibrée, PDF23 pour le contenu, PDF24 pour les caractéristiques. Réglage STORAGE pour le stockage ; le chargeur n’est pas une protection de décharge embarquée. Les notes fabricant mentionnent parfois des prises banane par héritage rédactionnel : le S65 modélisé comporte bien une prise XT60 frontale, pas de prises banane ajoutées.',
      modeling='Reconstruction extérieure du S65 à l’échelle 118×115×45 mm : coque profilée, joint, afficheur, boutons, ports, grilles et ventilateur visibles. La coque réelle, ses tolérances et les détails locaux sont à mesurer. Pas de circuits internes secteur inventés. Cordon secteur représenté séparément, trajet/longueur estimés.'),
]


def write(folder,name,text):
    p=BASE/folder/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.rstrip()+'\n',encoding='utf-8')


def main():
    for item in DATA:
        folder=item['folder'];root=BASE/folder
        assets=json.loads((root/'assets.json').read_text(encoding='utf-8'))
        manifest=root/'3D/provenance.json';has3d=manifest.exists()
        lines=['# '+item['title'],'',f'Choix d’étude du **13 octobre 2026** : **{item["reference"]}**. Non acheté, non testé.',
               '',item['quantity'],'',item['why'],'','## Caractéristiques et cotes','', '| Donnée | Valeur / statut |','| --- | --- |']
        lines += [f'| {k} | {v} |' for k,v in item['facts'].items()]
        lines += ['','## Achat Amazon et disponibilité','']
        if item['asin']:
            lines += [f'ASIN identifié : **{item["asin"]}**, [fiche Amazon.com consultée]({item["amazon_us"]}). [Même identifiant sur Amazon.fr](https://www.amazon.fr/dp/{item["asin"]}) : accès indisponible dans cette session, présence commerciale française et achat livrable **non confirmés**.']
        else:
            lines += ['[Recherche Amazon.fr SkyRC S65 SK-100152](https://www.amazon.fr/s?k=SkyRC+S65+SK-100152). Une offre Amazon.de Marketplace est référencée par [Geizhals](https://geizhals.de/skyrc-s65-ac-2-4s-6a-65w-ladegeraet-sk-100152-02-a3309283.html), mais la redirection est bloquée. **ASIN et offre française non confirmés** ; ce lien de recherche n’est pas une offre vérifiée.']
        lines += ['', '**Aucun prix en euros, vendeur, stock ou frais livrés n’est inventé.** Les deux identifiants confirmés le sont sur Amazon.com ; un changement de domaine ne prouve pas une offre en France.',
                  '', '## Documents et modèle','', '[Notice d’intégration du projet](notices/notice-integration-v3.md), [recherche, avis et informations manquantes](recherche-technique.md), [sources structurées](sources.json), [photos constructeur](photos/README.md), [liste des originaux](assets.json).',
                  '', '[Modèles STEP, aperçus et provenance](3D/README.md).' if has3d else 'Modélisation 3D en préparation.',
                  '', f'[Référence technique fabricant]({item["primary"]}). [Architecture et dimensionnement de l’alimentation](../alimentation/README.md).','']
        write(folder,'README.md','\n'.join(lines))
        write(folder,'notices/notice-integration-v3.md','# Notice d’intégration V3 — '+item['title']+'\n\n**Document de projet, distinct des notices originales constructeur.** 13 octobre 2026. Aucun essai matériel.\n\n'+item['notice']+'\n\n'+item['notice_extra']+'\n\n[Retour à la fiche](../README.md).')
        research=['# Recherche et avis — '+item['reference'],'',
            'Recherche sur le Web et dans les notices fabricant, boutiques et forums. Aucun avis, cote ou mesure manquante n’a été créé pour compléter artificiellement la fiche.','',
            '## Retours utilisateurs','']
        for review in item['reviews']:
            research += [f'- [Témoignage / discussion]({review["url"]}) — {review["access"]}. {review["finding"]}']
        research += ['','Ces retours ont des variantes et des conditions différentes. Ils orientent les contrôles ; ils ne valident ni les objectifs d’autonomie ni l’exemplaire commandé.',
                     '', '## Informations manquantes et méthode de contrôle','']+['- '+u for u in item['unknowns']]
        research += ['', '## Référence 3D','',item['modeling'], '', '[Retour à la fiche](README.md).']
        write(folder,'recherche-technique.md','\n'.join(research))
        notices=[a for a in assets['assets'] if a['file'].startswith('notices/') and 'sha256' in a]
        index=['# Notices et plans conservés','','Documents originaux téléchargés sans modification ; sommes SHA256 dans [assets.json](../assets.json).','']
        index += [f'- [{Path(a["file"]).name}]({Path(a["file"]).name}) — [source originale]({a["url"]}).' for a in notices]
        index += ['','[Notice d’intégration de projet](notice-integration-v3.md).', '', item['notice_extra']]
        write(folder,'notices/README.md','\n'.join(index))
        photos=[a for a in assets['assets'] if a['file'].startswith('photos/') and 'sha256' in a]
        photo_index=['# Photos et illustrations constructeur','',
            'Originaux conservés sans modification. Certaines illustrations sont des schémas ou courbes commerciales ; elles ne constituent pas des mesures sur notre matériel.',
            '', 'URLs et sommes SHA256 dans [assets.json](../assets.json).','']
        photo_index += [f'- [{Path(a["file"]).name}]({Path(a["file"]).name}) — [source originale]({a["url"]}).' for a in photos]
        photo_index += ['', '[Retour à la fiche](../README.md).']
        write(folder,'photos/README.md','\n'.join(photo_index))
        source=dict(selected_on=DATE,reference=item['reference'],purchased=False,hardware_measured=False,
            hardware_tested=False,model_3d_created=has3d,model_3d_manifest='3D/provenance.json' if has3d else None,
            amazon=dict(asin=item['asin'],identity_verified_marketplace='amazon.com' if item['asin'] else None,
                reference_url=item['amazon_us'],france_offer_verified=False,price_eur=None,shipping_eur=None,
                seller=None,stock=None,status='France product pages/search blocked; no validated French purchase basket'),
            primary_source=item['primary'],specifications=item['facts'],assets='assets.json',
            reviews=item['reviews'],unknowns=item['unknowns'])
        write(folder,'sources.json',json.dumps(source,ensure_ascii=False,indent=2))
    folder='alimentation';capacity=5.2;voltage=7.4;fraction=.8;energy=voltage*capacity
    calcs=dict(capacity_Ah_advertised=capacity,voltage_V_nominal=voltage,energy_Wh_nominal=energy,
        usable_fraction_assumed=fraction,energy_Wh_usable_assumed=energy*fraction,
        maximum_total_W_45min=energy*fraction/.75,maximum_total_W_20min=energy*fraction/(20/60),
        maximum_total_W_10min=energy*fraction/(10/60),no_autonomy_guarantee=True,
        pi_branch_output_W_at_5A=25,pi_branch_efficiency_assumed=.90,
        pi_branch_battery_W_at_5A=25/.90,battery_A_at_6_4V_at_5A_pi=25/.90/6.4,
        charger_battery_W_at_5_2A_full_charge=8.4*5.2,
        charging_current_A_first_control=2.6,charging_current_A_max_proposed_if_pack_manual_allows_1C=5.2)
    write(folder,'dimensionnement.json',json.dumps(calcs,ensure_ascii=False,indent=2))
    lines=['# Alimentation et charge — V3','',
        'Trois dossiers : [batterie Zeee 2S 5 200 mAh](../batterie/README.md), [régulateur Pololu D24V90F5](../regulateur-alimentation/README.md), [chargeur SkyRC S65](../chargeur-batterie/README.md). Sélection de conception ; aucune commande ou installation physique.',
        '', 'Les références batterie et régulateur sont identifiées sur Amazon.com. Amazon.fr bloque les pages et sa disponibilité ne peut pas être déduite. Le S65 est documenté et signalé sur Amazon.de par un comparateur, sans ASIN fiable récupéré. Le panier Amazon France, les prix et les frais restent à vérifier.',
        '', '## Énergie et autonomie','',
        'Un seul pack annoncé 5,2 Ah ×7,4 V donne **38,48 Wh nominaux**. Avec la fraction utilisable **supposée** de 80 %, **30,784 Wh**. La réserve de 20 % n’est pas une mesure ni un seuil de coupure. Le second pack du lot reste hors véhicule : échanger les batteries ne valide pas une autonomie sur une charge.',
        '', '| Objectif | Puissance totale moyenne maximale, scénario 80 % |', '| --- | ---: |',
        f'| 45 min à20 km/h | {calcs["maximum_total_W_45min"]:.2f} W |',
        f'| 20 min à40 km/h | {calcs["maximum_total_W_20min"]:.2f} W |',
        f'| 10 min à40 km/h | {calcs["maximum_total_W_10min"]:.2f} W |',
        '', 'Ce total comprend moteurs, ESC, direction, Pi, caméra, refroidissement et pertes. À titre d’hypothèse, une branche Pi/caméra consommant 10 W à la batterie laisserait environ **31,05 W** pour propulsion et direction au point 45 min. Une capacité mesurée plus faible, un arrêt plus précoce ou davantage de frottement réduit cette marge. Les courants 30 A des ESC et 9 A du régulateur sont des capacités, pas la consommation permanente du véhicule.',
        '', 'À5 A de sortie Pi, le régulateur fournit 25 W ; avec 90 % de rendement supposés, il prélève 27,78 W, soit **4,34 A à6,4 V**. Un fusible de branche placé à l’entrée ne doit donc pas être dimensionné par simple recopie du courant de sortie. Les sections, pointes, chutes et protections du faisceau doivent être mesurées et dimensionnées.',
        '', '## Distribution prévue','',
        '```mermaid','flowchart LR','    B[Batterie Zeee 2S] --> D[Distribution protégée à concevoir]',
        '    D --> S[Crydom D1D100, etude]','    S --> EG[ESC gauche]','    S --> ED[ESC droit]',
        '    D --> HP[Pololu 2813 HP, etude]','    HP --> R[Pololu 5 V]','    HP -.->|Commande VSW| S',
        '    R --> PI[Pi 5 et caméra]','    EG -->|BEC 6 V, un seul| S[Servo FT90M]',
        '    C[SkyRC S65, hors véhicule] -.->|Charge batterie déconnectée| B','```',
        '', 'La [surveillance et la coupure 2S](../protection-batterie/README.md) ont maintenant un dossier d’étude : carte analogique V3 à fabriquer, interrupteur Pololu pour la branche Pi et relais Crydom pour les moteurs. Ces éléments ne sont pas qualifiés au banc. Distribution, fusibles, faisceau, dissipateur et protections contre les transitoires restent à définir. Le régulateur ne protège pas à lui seul la LiPo contre une décharge profonde.',
        '', '## Liaison du régulateur à la Pi','',
        'Le Pololu n’annonce pas de source USB PD. Deux possibilités documentées : USB-C avec une interface de source et un câble de puissance appropriés ; ou rails 5 V du connecteur 40 broches avec protections externes et fils courts. Pour l’étude, la seconde est proposée. Ce schéma est fonctionnel : le faisceau et ses protections restent à dimensionner et vérifier avant mise sous tension.',
        '', 'Broches physiques Pi proposées : 2 et4 (5 V), plusieurs GND dont6 et9, repérage à vérifier. Il s’agit des rails d’alimentation, pas de GPIO de commande ; la batterie 7,4/8,4 V et les BEC6/7,4 V restent hors de ces rails. Ne pas utiliser de plaque d’essai pour la puissance ni alimenter la Pi simultanément depuis deux sources.',
        '', 'Le [livre blanc officiel Raspberry Pi, page PDF9](../regulateur-alimentation/notices/Raspberry-Pi-5-alimentation-USB-PD-livre-blanc-2026.pdf) précise deux réglages possibles après validation de la branche : `PSU_MAX_CURRENT=5000` dans l’EEPROM déclare la capacité de la source, tandis que `usb_max_current_enable=1` dans `config.txt` relève le plafond USB partagé à1,6 A. Le premier entraîne aussi le second automatiquement. Ils ne créent ni courant supplémentaire ni négociation PD. Tenir compte du budget partagé caméra/ventilateur et mesurer la tension à la Pi. Aucun réglage n’a été appliqué.',
        '', '## Charge et arrêt basse tension','',
        'S65 en mode LiPo BALANCE 2S, fin4,20 V/cellule. Le choix initial de2,6 A reste sous1C ; la valeur5,2 A ne s’utilise qu’avec la notice du pack reçu. La charge requiert les deux liaisons, puissance et équilibrage ; vérifier genre des prises et alignement XH. Aucun adaptateur ou prolongateur n’est supposé inclus.',
        '', 'L’étude de [protection 2S](../protection-batterie/integration.md) propose deux voies locales par cellule : avertissement typique à 3,566 V, puis demande indépendante de coupure à 3,353 V en descente. Tolérances, hystérésis et essais sont documentés ; aucune protection réelle n’est validée. Le minimum fabricant de 3,2 V et les creux sous charge imposent une marge. La fenêtre de tension ne garantit pas un délai fixe d’arrêt Linux. Le port d’équilibrage sert à la mesure, pas à la puissance.',
        '', '## Contrôles avant validation des objectifs','',
        'Mesurer capacité et Wh utilisables, température, tension par cellule et pointes. Tester le régulateur en charge et pendant l’accélération des deux moteurs ; contrôler sous-tension Pi, stabilité de la caméra et courant USB. Faire ensuite des parcours distincts à20 et40 km/h, vidéo active, sur un espace approprié. Les avis recueillis n’attestent ni ces performances ni notre exemplaire.',
        '', '[Calculs structurés](dimensionnement.json), [modèles 3D](3D/README.md), [index composants](../README.md).','']
    write(folder,'README.md','\n'.join(lines))
    print('Documented battery, regulator and charger; usable study energy',energy*fraction,'Wh')


if __name__=='__main__':main()
