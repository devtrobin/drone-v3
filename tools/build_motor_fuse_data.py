"""Maintain the motor-branch component dossiers, provenance and study calculations."""
from pathlib import Path
import json,sys,hashlib
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/protection-branches-moteurs'
FUSE_URL='https://www.littelfuse.com/assetdocs/littelfuse-datasheet-ato?assetguid=bba6ed2a-96e5-4b07-ab5d-0e8d267c0bd1'
def write(name,text):
    p=BASE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.strip()+'\n',encoding='utf-8')
def data(name,obj):write(name,json.dumps(obj,ensure_ascii=False,indent=2))
def main():
    sys.stdout.reconfigure(encoding='utf-8')
    write('README.md','''# Protection des deux départs moteurs

Sélection d'étude du **14 octobre 2026**, non achetée et non testée : **deux porte-fusibles Blue Sea 5065** et **deux fusibles Littelfuse ATO 30 A verts**, référence **0ATO030.V / ATO30**. Un support et un fusible par variateur Hobbywing WP16BL30 G2, sur son positif batterie ; aucun fusible dans les trois phases moteur.

| Pièce | Quantité embarquée | Référence et portée |
| --- | ---: | --- |
| [Porte-fusible](porte-fusible/README.md) | 2 | 5065 ; un circuit ATO/ATC, fils 12 AWG, calibre maximal fabricant 30 A ; même référence que pour le Pi |
| [Fusible](fusible-30a/README.md) | 2 | Littelfuse 0ATO030.V ; 30 A / 32 V DC ; pouvoir de coupure 1 000 A à 32 V DC ; calibre d'étude |

Le scénario d'étude reprend **40 A moteurs au total** et ajoute une hypothèse de **20 A sur chacun des deux départs**. Cette répartition n'est pas garantie en virage ou en cas de roue bloquée. Les « 30 A continus / 100 A de pointe » des ESC sont des annonces de capacité, pas une consommation mesurée ni une limitation garantie.

La fiche ATO 2022 recommande typiquement **23 A à 65 °C** pour le 30 A, contre **19 A pour le 25 A**. Le 30 A est retenu pour l'étude à 20 A par départ ; il ne permet pas de qualifier un fonctionnement continu à 30 A dans un compartiment chaud.

**Point restant majeur :** les fils d'entrée des ESC sont annoncés en **16 AWG, 75 mm**, soit environ 1,31 mm² nominal. Leur tenue thermique et aux défauts avec un ATO 30 A n'est pas démontrée. Les sections, les pointes, le courant prospectif de la LiPo, les contacts et la coordination doivent être validés avant montage. Le fusible ne garantit pas de sauver les semi-conducteurs du variateur.

## Contenu du dossier

- [Intégration, raccordement et essais](integration.md), [calculs](calculs.json), [nomenclature](nomenclature.json).
- [Cotes, provenance et estimations](cotes.md), [recherche, prix et avis](recherche-technique.md), [sources](sources.json), [archives](assets.json).
- [Notice PDF V3 et fiches archivées](notices/README.md).
- [Cinq STEP détaillés, aperçus et contrôles FreeCAD](3D/README.md).

Support : [Amazon.com B004ZIUA62](https://www.amazon.com/dp/B004ZIUA62), référence déjà identifiée dans le dossier Pi ; [offre Amazon.fr](https://www.amazon.fr/dp/B004ZIUA62) non confirmée dans cette recherche. Fusible : [recherche Amazon.fr ATO30BP](https://www.amazon.fr/s?k=Littelfuse+ATO30BP), **pas d'ASIN exact vérifié**. Le pack de cinq **0ATO030.VP / ATO30BP** permettrait d'en installer deux et d'en conserver trois ; aucun lot n'est commandé.

Les deux supports ajoutés ici portent le nombre prévu de 5065 à **trois** avec celui du Pi. Le fusible Pi reste brun 7,5 A et doit rester identifié séparément des deux verts 30 A.
''')
    write('porte-fusible/README.md','''# Porte-fusible moteur - Blue Sea 5065

**Deux unités prévues**, une pour chaque ESC. Référence identique au [porte-fusible Pi](../../protection-branche-pi/porte-fusible/README.md), avec un calibre différent.

Le [fabricant](https://www.bluesea.com/products/5065) publie : fusibles ATO ou ATC, deux fils 12 AWG et fusible **vendu séparément** ; calibre maximum **30 A**. Ce chiffre ne constitue pas une courbe thermique complète ni un limiteur de courant. Aucun plan coté, STEP natif, résistance de contact ou indice IP chiffré applicable au 5065 n'a été obtenu.

La photo de référence montre un socle noir, un capot emboîté avec oreille, un joint orange à nervures et **deux fils rouges du même côté**. Ils sont l'entrée et la sortie du positif, sans retour négatif. Fixation et retenue du câble seront adaptées au châssis après mesure du support réel.

[Amazon.fr](https://www.amazon.fr/dp/B004ZIUA62), ASIN B004ZIUA62 : prix TTC, stock, vendeur et livraison non confirmés. Le support seul est annoncé, pas un kit avec fusible. Référence Amazon.com identifiée précédemment ; les réponses obtenues ici sont des pages de vérification automatique, archivées comme telles.

[Documentation et PDF](../notices/README.md), [cotes](../cotes.md), [intégration](../integration.md), [avis et prix](../recherche-technique.md), [modèle détaillé](3D/README.md), [photo et provenance](photos/README.md).
''')
    write('fusible-30a/README.md',f'''# Fusible moteur - Littelfuse ATO 30 A

**Deux fusibles embarqués**, un par départ. Référence exacte : **0ATO030.V / ATO30**, corps **vert**, **30 A / 32 V DC**. Conditionnement carte : **0ATO030.VP / ATO30BP**, cinq unités selon les sources commerciales recoupées ; deux utilisées et trois de rechange si ce pack est acheté.

[Fiche fabricant aftermarket 2022]({FUSE_URL}) : pouvoir de coupure **1 000 A à 32 V DC**, PA66, contacts étamés, masse **1,4 g ±5 % par fusible**. Les références ATOF 287, MINI, MAXI, JCASE, SmartGlow et les kits assortis ne sont pas assimilés à cette référence.

| Donnée typique, fiche 2022 | Valeur |
| --- | --- |
| Résistance à froid | 1,97 mΩ |
| Chute dans les conditions d'essai fabricant | 84 mV |
| I²t de fusion avant l'arc | 1 500 A²s, pas une énergie totale de coupure garantie |
| Section d'essai | 4 mm², pas une homologation du faisceau réel |
| Courant recommandé à 20 / 65 / 85 °C | 27 / 23 / 21 A, avec conditions de la fiche |
| Enveloppe de référence | 19,1 × 5,1 × 18,8 mm |

Le calibre 30 A est une **sélection d'étude**, sans mesure de courant moteur. Il ne donne ni coupure immédiate à 30 A, ni garantie de protection rapide des ESC. Ne pas dépasser 30 A dans le support 5065 pour compenser un démarrage qui fait fondre le fusible.

[Recherche Amazon.fr](https://www.amazon.fr/s?k=Littelfuse+ATO30BP) : pas d'offre exacte ni d'ASIN vérifié. [DigiKey, référence exacte](https://www.digikey.com/en/products/detail/littelfuse-inc/0ATO030-V/2519124), repère étranger 1,43 USD/unité, hors conditions françaises ; pas une commande.

[Notice PDF et fiche archivées](../notices/README.md), [intégration](../integration.md), [cotes](../cotes.md), [avis et alternatives](../recherche-technique.md), [STEP et aperçu](3D/README.md).
''')
    write('integration.md','''# Protection individuelle des deux alimentations ESC

```mermaid
flowchart LR
 B[Pack 2S positif] --> F[MIDI principal 60 A : étude]
 F --> D[MiniBus D+ P3]
 D -->|Tronc commun : étude 6 mm2| S[D1D100 borne +2 puis borne 1]
 S --> J[UD80A 569010 : répartition positive]
 J --> F1[5065 + ATO30 : ESC1]
 J --> F2[5065 + ATO30 : ESC2]
 F1 --> E1[Entrée XT60 ESC arrière 1]
 F2 --> E2[Entrée XT60 ESC arrière 2]
 E1 --> M1[Moteur arrière 1 : trois phases]
 E2 --> M2[Moteur arrière 2 : trois phases]
 E1 --- N[MiniBus D- : N1 et N3]
 E2 --- N
```

Les deux fusibles se trouvent **après le relais commun**, un sur chaque positif ESC, **au début de la dérivation**. Les retours négatifs vont séparément vers N1 et N3 du MiniBus D-. Les phases moteur restent reliées directement à leur variateur ; ne pas y insérer ces fusibles.

Le [nVent ERIFLEX UD-80A / 569010](../repartition-moteurs/integration.md) est retenu pour répartir le positif en sortie de la borne 1 du D1D100. Une arrivée 6 mm² proposée et deux petites sorties vers les fils 12 AWG des supports ; un seul conducteur par borne utilisée. Une seule cosse sur la borne SSR dans cette proposition. Quatre sorties restent sans conducteur. Connexions, serrage, retenue et tenue aux défauts à qualifier ; le bloc ne remplace pas les fusibles.

Le tronc commun pack/principal/D+/SSR/répartition doit rester dimensionné et coordonné avec le principal 60 A. Proposition existante : cuivre **6 mm²**, à qualifier. Les arrivées jusqu'aux petits fusibles ne sont pas protégées par ceux-ci : segments courts, isolés et retenus, sans réduction de section non qualifiée. Aucun troisième fusible commun aux moteurs n'est ajouté ici ; sa nécessité devra être revue si la section du tronc commun est réduite.

## Calibre et scénario

Hypothèses séparées : **40 A moteurs au total**, **20 A par ESC** pour cette sélection, air local du relais **40 °C** dans l'étude HS251. Ce ne sont ni des courants mesurés, ni des limites imposées par notre logiciel ou par les fusibles. Un total de 40 A ne garantit pas 20 A maximum sur chaque roue.

| Calibre ATO | Charge typique recommandée à 20 °C | À 65 °C | À 85 °C |
| --- | ---: | ---: | ---: |
| 20 A | 18 A | 15 A | 14 A |
| 25 A | 23 A | 19 A | 18 A |
| **30 A, étude** | **27 A** | **23 A** | **21 A** |

Fiche aftermarket Littelfuse du 15 novembre 2022 ; essais selon connexions et sections indiquées, marge thermique fabricant annoncée. Le 25 A manque de marge à 20 A et 65 °C ; le 30 A est retenu pour l'étude. Les 65 et 85 °C sont des points de comparaison, pas une température visée. Le support est lui aussi limité au calibre 30 A : pas d'augmentation automatique possible.

L'entrée de l'ESC alimentant le servo porte aussi la consommation de son **BEC réglé à 6 V**. Les 20 A de ce départ doivent inclure cette charge et les pertes. Le positif BEC du second ESC reste isolé ; aucun BEC vers le 5 V du Pi.

## Fils et pertes

Le constructeur Hobbywing annonce deux fils d'entrée **16 AWG de 75 mm**, rouge et noir, avec XT60. 16 AWG correspond à environ **1,31 mm² nominal**, contre environ **3,31 mm²** pour le 12 AWG des supports. Ne pas assimiler ces sections ni conclure que l'isolant accepte une température donnée sans son marquage réel.

Les [deux prises XT60H-F avec capots](../connecteurs-alimentation/integration.md) complètent les XT60 à contacts mâles déjà montés sur les ESC. Proposer des queues courtes **12 AWG, environ 3,31 mm²**, compatibles nominalement avec la recommandation AMASS, après chaque ATO30 et sur chaque retour négatif. Les anciens **4 mm²** restent un exemple de pertes ou un tronçon à raccorder par une transition qualifiée : ne pas les forcer dans les godets ni retirer des brins. Longueurs, raccords, isolant et retenue restent à choisir. Cela ne rend pas automatiquement les courts fils 16 AWG de l'ESC aptes au courant ou à l'énergie de défaut d'un ATO30. Leur coordination avec la courbe de coupure et les mesures thermiques reste un critère obligatoire ; réduire le scénario ou revoir la protection si la tenue n'est pas démontrée.

À froid, pour un ATO30 de résistance typique 1,97 mΩ : **20 A → 39,4 mV / 0,788 W par fusible** ; deux fusibles à 20 A → **1,576 W**, hors contacts, fils et chauffage. À 30 A sur un fusible : **59,1 mV / 1,773 W**. Les 84 mV de la fiche correspondent à ses propres conditions d'essai, pas à la simple résistance froide multipliée par le calibre.

Le [BNTECHGO 12 AWG SW12G68008F10C2](../cable-puissance-12awg/README.md) est proposé pour les nouvelles queues : résistance annoncée 5,06 Ω/km, température de référence non précisée. Exemple de boucle 0,20 m positif + 0,20 m retour à 20 A : **40,48 mV / 0,8096 W**, hors pigtails, raccords et échauffement. Cette résistance annoncée ne valide pas un courant admissible ou une tenue au défaut. Les exemples 4 mm² ci-dessous restent des comparaisons.

Exemple calculé pour deux branches neuves identiques, chacune 0,20 m de positif et 0,20 m de retour en cuivre 4 mm² à 20 °C, résistivité supposée 0,0175 Ω·mm²/m : **1,75 mΩ / 35 mV / 0,700 W par boucle à 20 A**. Ajouter les fils 12 AWG du support, les 16 AWG de l'ESC, les connecteurs, les raccords et la température réelle. Les 100 mm représentés dans la CAO ne sont pas une longueur de câble livrée.

## Pointes, défauts et coordination

| Rapport au calibre | Courant ATO30 | Fenêtre d'ouverture publiée |
| --- | ---: | --- |
| 110 % | 33 A | Au moins 360 000 s ; pas de maximum |
| 135 % | 40,5 A | 0,75 à 600 s |
| 160 % | 48 A | 0,25 à 50 s |
| 200 % | 60 A | 0,15 à 5 s |
| 350 % | 105 A | 0,08 à 0,5 s |
| 600 % | 180 A | 0,1 s maximum |

Un fusible 30 A **ne limite pas le courant à 30 A**. À 100 A, la fiche ne donne pas de fenêtre tabulée exacte : ne pas réutiliser celle de 105 A comme une garantie. La durée des « 100 A de pointe » de l'ESC n'est pas publiée ; passage des impulsions et vieillissement du fusible restent à étudier avec le courant d'entrée enregistré et les critères du fabricant.

Pouvoir de coupure **1 000 A à 32 V DC** : établir le courant prospectif de la LiPo et de chaque boucle. Repère purement ohmique **8,4 V / 1 000 A = 8,4 mΩ**. Ne pas inclure la résistance du fusible de branche lui-même pour justifier sa capacité à interrompre le courant prospectif ; ne pas déduire ce courant du marquage « 80C » et ne pas provoquer un court-circuit du pack.

L'I²t typique **1 500 A²s** est celui de fusion avant l'arc. Il ne garantit ni l'énergie totale laissée passer, ni la tenue de l'ESC ou du SSR. Le MIDI principal 60 A ne qualifie pas automatiquement une association avec cet ATO à 1 000 A. Le rapport nominal 60/30 ne prouve pas la sélectivité : celle-ci exige des courbes et données de coordination adaptées. La limite de 40 A continu de l'étude thermique du relais ne devient pas une protection contre 60 A cumulés parce que deux ATO30 sont installés.

## Freinage et arrêt

Vérifier le freinage/régénération, les condensateurs ESC et les transitoires lorsque le relais ou un seul fusible ouvre. Une fusion sur un seul départ peut supprimer la propulsion et le freinage commandé d'une roue, pendant que l'autre fonctionne encore. Ces fusibles n'ordonnent pas à eux seuls l'arrêt du second moteur : prévoir la détection et un arrêt global supervisé au niveau du système. Aucun capteur de courant ou retour de fusion n'est inclus ici.

Un fusible n'est pas un interrupteur d'usage : remplacement uniquement sur pack et prise d'équilibrage débranchés, après recherche de la cause. Ne pas le retirer sous charge.

## Pose et qualification

1. Contrôler références exactes, deux fusibles verts 30 A distincts du brun Pi 7,5 A, lot, cosses, isolant et sections. Mesurer dimensions du support avant perçage.
2. Raccorder chaque support uniquement en série sur son positif, après la répartition commune ; sertir les raccords et retenir les câbles hors des pièces mobiles. Le fusible doit être au début de sa dérivation. Aucun empilage de cosses SSR supposé validé.
3. Vérifier continuité, polarités, isolement et BEC, batterie débranchée ; premier essai avec alimentation limitée, roues dégagées et réglages prudents.
4. Mesurer séparément les deux courants d'entrée et leur somme pendant démarrage, accélération, virage, freinage et marche arrière, puis sur l'usage long. Contrôler chute de tension et échauffement de chaque fusible/contact, fils 16 AWG, XT60 et relais. Ne pas bloquer volontairement le rotor sans protocole adapté.
5. Qualifier courant prospectif, sections, tenue aux défauts, pointes et coordination, ainsi que le comportement lors de la perte d'une seule propulsion. L'autonomie et 40 km/h restent à démontrer.

[Moteurs et notices](../moteur/README.md), [distribution](../distribution-alimentation/integration.md), [principal](../protection-surintensite/integration.md), [Pi](../protection-branche-pi/integration.md), [surveillance et relais](../protection-batterie/integration.md), [refroidissement](../dissipateur-relais/integration.md).
''')
    write('cotes.md','''# Cotes des protections moteurs

Repères du **14 octobre 2026** ; aucune pièce physique mesurée. Les fichiers STEP sont des reconstructions d'extérieur, pas des plans pour fabriquer des fusibles ou garantir le contact.

| Élément | Cote utilisée | Provenance / limite |
| --- | --- | --- |
| ATO, enveloppe totale | 19,1 × 5,1 × 18,8 mm | Plan fabricant aftermarket 2022, cotes de référence |
| Lame, largeur / épaisseur | 4,1 / 0,65 mm | Plan fabricant |
| Lame, dépassement | 6,5 mm | Plan fabricant |
| Deux lames, largeur extérieure | 14,5 mm | Ce n'est pas leur entraxe |
| Entraxe des lames | 10,4 mm | Déduit : 14,5 - 4,1 ; centres X ±5,2 |
| Masse fusible seul | 1,4 g ±5 % | Fabricant ; 2,8 g pour deux, hors supports |
| Support avec oreille, hors fils | 37,5 × 38 × 15 mm | **Estimation CAO**, photo 5065, pas une cote publiée |
| Trou de support | Ø5,0 mm | **Estimation CAO** ; mesure revendeur ≈3/16 pouce, soit 4,7625 mm |
| Centre du trou CAO | X -21,03 / Y 22,53 mm | **Position estimée**, mesurer avant perçage |
| Fils de support | 12 AWG | Fabricant, environ 3,31 mm² nominal |
| Fils en CAO | Ø4,3 ; longueur extérieure 100 ; bouts nus 8 mm | **Illustration**, diamètre et longueur livrés non confirmés |
| Brins en CAO | 19 × Ø0,47 mm par fil | **Illustration**, aire 3,296 mm², nombre réel inconnu |
| Entrée ESC | 16 AWG ; 75 mm rouge et noir | Fiche Hobbywing G2 actuelle ; environ 1,31 mm² nominal |
| Pose de deux supports | Centres X -26 et +26 mm | **Implantation d'étude**, aucune entraxe de montage imposé |

Le support reprend la géométrie documentée dans [le dossier Pi](../protection-branche-pi/cotes.md) : socle, capot creux, oreille, guides, joint orange à nervures et contacts femelles approchés. Les deux fils rouges continus sortent du même côté. Leurs bouts nus sont les terminaisons représentées, pas des interruptions accidentelles.

Le fusible vert comporte deux lames avec chanfreins, dépouilles de corps, poches, deux points de test et marquage « 30 ». Les petites formes, rayons, police et teinte sont estimés. Le PA66 réel translucide est rendu opaque ; l'élément interne calibré n'est pas inventé. Aucune étanchéité ou pression de contact n'est validée par la CAO.

Les dimensions DigiKey 19,05 × 5,08 × 12,19 mm concernent une description de corps ; elles ne remplacent pas les 18,8 mm totaux du plan. Les cotes marchandes de la carte de cinq fusibles et les tailles de colis ne servent pas de cotes de pièce.

Repères : support X largeur, Y insertion, Z épaisseur, fils vers -Y. Fusible isolé Z hauteur ; montage par rotation X -90°, translation (0,4,7,5). Vue éclatée : capot Y+36 mm. Assemblage double : quatre fils libres, sans raccord électrique commun, cosses ou XT60.
''')
    write('recherche-technique.md',f'''# Recherche technique, achat et retours d'utilisation

Recherche du **14 octobre 2026**. Deux départs indépendants de WP16BL30 G2 ; choix de composants pour l'étude, aucun achat et aucune mesure matérielle.

## Choix et comparaison

| Solution | Résultat de l'étude |
| --- | --- |
| **Blue Sea 5065 + Littelfuse ATO30** | Choix retenu : support déjà documenté pour le Pi, 12 AWG et calibre maximum 30 A ; fusible à fiche exacte et cotes disponibles |
| ATO20 sur ce même support | Courant recommandé 18 A à 20 °C et 15 A à 65 °C : insuffisant au scénario 20 A par départ |
| ATO25 | 23 A à 20 °C, 19 A à 65 °C : trop juste au scénario chaud |
| ATO30 | 27 / 23 / 21 A à 20 / 65 / 85 °C : choix d'étude ; qualification des fils 16 AWG et du défaut de LiPo encore nécessaire |
| ATO35 ou 40 | Au-delà du calibre maximum 30 A annoncé pour le 5065 : non retenu |
| Fusible unique pour les deux ESC | Ne constitue pas à lui seul la protection individuelle des dérivations plus fines ; non retenu comme remplacement des deux départs |
| MINI/FHM 14 AWG déjà étudié | Support de comparaison limité à 20 A ; non retenu pour notre scénario 20 A continu chaud |
| Disjoncteur automatique générique | Courbes et pouvoir de coupure non vérifiés pour une référence précise ; aucun modèle retenu |

Les valeurs proviennent de [la fiche ATO aftermarket 2022]({FUSE_URL}), et non d'une fiche ATOF 287 d'une autre révision. Le « 100 A de pointe » de l'ESC ne fournit pas sa durée. La nouvelle [fiche Hobbywing](https://www.hobbywing.com/en/products/quicrun-wp-16bl30-g2) confirme les deux entrées **16 AWG, 75 mm**, XT60. Leur tenue avec ATO30 est une information encore manquante, pas une compatibilité acquise.

## Recherche Amazon et prix

| Référence | Recherche / observation | État |
| --- | --- | --- |
| Blue Sea 5065 | [Amazon.com B004ZIUA62](https://www.amazon.com/dp/B004ZIUA62), [Amazon.fr](https://www.amazon.fr/dp/B004ZIUA62) | ASIN identifié dans la recherche Pi ; nouvelles réponses automatiques de vérification, offre française non confirmée |
| Littelfuse ATO30BP | [Recherche Amazon.fr](https://www.amazon.fr/s?k=Littelfuse+ATO30BP) et recherches par 0ATO030.V/VP | Aucun ASIN exact ni prix français validé |
| 0ATO030.V, distributeur exact | [DigiKey](https://www.digikey.com/en/products/detail/littelfuse-inc/0ATO030-V/2519124) | 1,43 USD à l'unité affiché ; deux = 2,86 USD, hors livraison/fiscalité France |
| ATO30BP, carte de cinq | [Canadian Tire](https://www.canadiantire.ca/en/pdp/littelfuse-ato-blade-fuse-5-pk-0201571p.0201581.html) | Référence 30 A et cinq unités confirmées ; 6,29 dollars canadiens affichés, pas un devis France |
| Support 5065, repère antérieur | [Hodges Marine](https://www.hodgesmarine.com/blu5065-blue-sea-5065-waterproof-inline-fuse-holder-atoa.html) | 15,01 USD relevés dans le dossier Pi du même jour ; deux = 30,02 USD, prix à revalider |

Repère de coût étranger, deux supports + deux fusibles unitaires : **32,88 USD**, hors frais et conditions françaises, pas un budget validé. Le lot de cinq est une autre option d'achat : ne pas additionner son prix et celui de deux fusibles unitaires. La variante 00940418ZP trouvée via recherche possède un assortiment avec un seul ATO30 : elle ne couvre pas nos deux départs et n'est pas retenue.

## Avis, forum et vidéos

- [Maine Sail, forum Sailboat Owners, message nº2 du 23 mai 2014](https://forums.sailboatowners.com/threads/what-are-you-using-as-a-bilge-pump-fuse-holder.162517/) indique employer le **5065** sur son bus batterie. Il distingue la protection du fil et celle de la pompe. Ce témoignage ne donne ni courant mesuré, ni température, ni essai de court-circuit LiPo.
- [Canadian Tire, page ATO30BP](https://www.canadiantire.ca/en/pdp/littelfuse-ato-blade-fuse-5-pk-0201571p.0201581.html) affiche **4,6/5 et 172 avis**, regroupés sur plusieurs calibres. Citation courte de Joed53 : **« Good quality, no duds. »** Son commentaire évoque une teinte bleue, donc il n'est pas retenu comme essai spécifique du vert 30 A. Les avis généraux portent sur fonctionnement et qualité perçue ; ils ne valident pas les courbes ou le pouvoir de coupure.
- Les cinq avis qualitatifs eBay du 5065 déjà consignés [dans le dossier Pi](../protection-branche-pi/recherche-technique.md) ne comportent pas de protocole thermique à 20 A. La page n'a pas pu être rechargée ici ; ne pas les présenter comme de nouveaux essais.
- Requêtes YouTube : `Blue Sea 5065`, `Littelfuse ATO 30 test`. Aucun essai attribuable à notre combinaison exacte avec WP16BL30 G2 et LiPo 2S, donnant courant d'entrée, température ou comportement au défaut, n'a été identifié. Aucune vidéo non visionnée n'est utilisée comme preuve.

## Informations manquantes et décisions

| Point | Traitement |
| --- | --- |
| Encombrement exact et trou du 5065 | Photo archivée et estimations explicitement signalées ; mesure sur réception avant perçage |
| Indice IP, contacts, longueur de fils | Aucun chiffre fabricant obtenu pour le 5065 ; le nom commercial « waterproof » n'est pas converti en IP66 |
| Pointes et consommation de chaque ESC | À mesurer séparément ; 40 A total ne garantit pas 20 A par roue |
| Fils 16 AWG et isolant réel | Coordination ATO30 à démontrer, sans supposer un isolant 200 °C |
| Pouvoir de coupure 1 000 A | Courant prospectif LiPo à établir ; principal MIDI non assimilé à une association série qualifiée |
| Sélectivité et SSR | Rapport 60/30 insuffisant ; I²t de fusion seul insuffisant pour garantir la tenue des semi-conducteurs |
| Répartition après relais | UD80A569010 retenu ; connexions, serrage du lot et tenue aux défauts à qualifier |
| Perte d'un seul moteur au défaut | Arrêt global supervisé à concevoir ; aucune détection de fusion fournie par ces pièces |

La fiche fabricant a été lue en ligne. Son téléchargement direct retourne 403 ; sa copie RSP de quatre pages, avec bannières distributeur et dernière page Mouser, est archivée **inchangée**. Les statuts des réponses Amazon et des téléchargements sont conservés dans [assets.json](assets.json). Aucun forum, vendeur ou fabricant contacté.
''')
    write('notices/README.md','''# Documentation des protections moteurs

- [Notice V3, protection des deux départs](notice-protection-branches-moteurs-v3.pdf) : sélection, raccordement, cotes, défauts et qualification. Document du projet ; ce n'est pas une notice constructeur.
- [Fiche ATO 2022, copie diffusée via RSP](Littelfuse-ATO-fiche-originale-via-RSP.pdf) : quatre pages ; bannières RSP et dernière page Mouser conservées telles que fournies. Pages 1–3 fabricant : références, cotes et courbes.
- [Catalogue Littelfuse aftermarket 2013, copie via RS](Littelfuse-catalogue-aftermarket-2013-via-RS.pdf) : références et conditionnements ; PDF page 8, page imprimée 6.
- [Catalogue Blue Sea déjà archivé](../../distribution-alimentation/notices/README.md) : consulter les pages 60 et 72 pour le 5065 ; le tableau ne lui attribue pas l'IP66 du 5021.
- [Notice du WP16BL30 G2 déjà archivée](../../moteur/notices/README.md), avec fiche web actuelle référencée dans les sources.

Aucune notice séparée ou plan coté officiel du 5065 n'a été obtenu. Le lien constructeur de la fiche ATO fonctionne dans la consultation web, mais son téléchargement direct a été refusé. Les copies locales sont conservées sans retouche ; empreintes et provenance dans [assets.json](../assets.json).
''')
    write('porte-fusible/photos/README.md','''# Photo de référence du Blue Sea 5065

[Photo commerciale Amazon](Amazon-5065-original.jpg), ASIN B004ZIUA62, conservée sans modification depuis le dossier Pi. Source : https://m.media-amazon.com/images/I/51mfLfEM4UL._AC_SL1000_.jpg.

Socle et capot noirs, joint orange, oreille latérale et deux fils rouges du même côté. Aucun fusible, raccord ou vis de châssis inclus sur cette photo. Elle permet d'approcher la forme extérieure, sans valider les cotes, la longueur des fils, la compression du joint ou l'étanchéité. SHA256 dans [les archives](../../assets.json).
''')
    for folder,label in [('porte-fusible','Porte-fusible Blue Sea 5065'),('fusible-30a','Fusible Littelfuse ATO30')]:
        model='bluesea-5065-porte-fusible-detaille' if folder=='porte-fusible' else 'littelfuse-0ato030-v-detaille'
        write(folder+'/3D/README.md',f'''# {label} - modèle détaillé

[STEP]({model}.step), [aperçu]({model}.png), [provenance et contrôles]({model}.json).

Solides nommés et couleurs ; reconstruction extérieure non mesurée. [Cotes et estimations](../../cotes.md), [cinq modèles et assemblages](../../3D/README.md). Le support reprend la géométrie de la branche Pi ; le fusible est vert et marqué 30. Aucun élément interne calibré de fusible inventé.
''')
    curves=[(1.10,360000,None),(1.35,.75,600),(1.60,.25,50),(2,.15,5),(3.5,.08,.5),(6,None,.1)]
    data('calculs.json',dict(checked_on='2026-10-14',status='study; no hardware tested',
        assumptions=dict(total_motor_current_A=40,individual_ESC_input_current_A=20,distribution_balanced_assumed=True,
            limits_enforced=False,SSR_local_ambient_study_C=40,fuse_rating_A=30,cold_fuse_resistance_ohm=.00197,
            added_branch_wire_area_mm2=4,example_oneway_length_m=.20,copper_resistivity_20C_ohm_mm2_m=.0175),
        derating_source_revision='ATO aftermarket 2022-11-15',derating_A={20:[18,15,14],25:[23,19,18],30:[27,23,21]},derating_ambient_C=[20,65,85],
        fuse_losses=[dict(input_A=i,typical_cold_drop_V=i*.00197,typical_cold_loss_W=i*i*.00197) for i in [10,20,25,30]],
        two_fuses_at20A_loss_W=2*20**2*.00197,example_added_4mm2_loop=dict(length_total_m=.4,resistance_20C_ohm=.0175*.4/4,drop20A_V=20*.0175*.4/4,loss20A_W=400*.0175*.4/4,excludes='holder pigtails, ESC16AWG, contacts, connectors and warming'),
        time_current_table=[dict(ratio=r,current_A=30*r,min_s=lo,max_s=hi) for r,lo,hi in curves],
        interrupting_rating=dict(A=1000,V_DC=32,prospective_current_verified=False,reference_pack_max_V=8.4,reference_loop_R_ohm=8.4/1000,exclude_branch_fuse_resistance=True),
        typical_melting_I2t_A2s=1500,total_clearing_I2t_verified=False,selectivity_verified=False,
        holder_12AWG_nominal_mm2=3.31,ESC16AWG_nominal_mm2=1.31,ESC_input_lead_published_length_mm=75,
        XT60H_tail_proposal_AWG=12,XT60H_tail_nominal_mm2=3.31,added_4mm2_is_loss_example_not_godet_fit=True,
        XT60H_reference='AMASS XT60H-F with cap, two proposed; contact current unqualified',
        original_ESC_wires_protection_verified=False,inrush_verified=False,main_SSR_thermal_envelope_verified=False,amazon_fr_offers_verified=False))
    data('nomenclature.json',dict(checked_on='2026-10-14',status='study; not ordered',items=[
        dict(ref=['PFM1','PFM2'],part='Blue Sea5065',quantity_installed=2,includes='holder, cap and12AWG pigtails; fuse separate',amazon_asin_previously_identified='B004ZIUA62',amazon_fr_offer_confirmed=False),
        dict(ref=['FM1','FM2'],part='Littelfuse0ATO030.V / ATO30',quantity_installed=2,rating_A=30,color='green',amazon_exact_asin=None)],
        purchase_options=dict(fuses='two individual units OR one0ATO030.VP / ATO30BP five-pack; three spares for this pack',holders='two new5065; three total planned including Pi'),
        price_eur_delivered=None,foreign_reference_USD=dict(holder_each=15.01,fuse_individual_each=1.43,sum_for_two_of_each=32.88,validated_french_quote=False),
        connectors_proposed=dict(reference='AMASS XT60H-F with caps',quantity=2,existing_ESC_males_retained=True),
        missing=['qualification of selected nVent UD80A569010 splitter andconnections after SSR','branch wiring, qualification of selected XT60H-F, crimped joints and retention','qualification of ESC16AWG, inrush, fault current and coordination','global stop on loss of one motor']))
    sources=[
        ('holder','https://www.bluesea.com/products/5065','manufacturer','ATO/ATC,12AWG,maximum30A; fuse separate; no standalone plan or numeric IP obtained'),
        ('ATO2022',FUSE_URL,'manufacturer','exact0ATO030.V/VP, cotes, curves, derating, resistance and1kA; revision2022-11-15'),
        ('ATO-RSP','https://rspsupply.com/images/downloads/Littelfuse/0/Littelfuse%200ATO020.VP/Specification%20Document.pdf','manufacturer_document_mirror','unchanged2022datasheet withRSP banners andMouser last page'),
        ('ESC','https://www.hobbywing.com/en/products/quicrun-wp-16bl30-g2','manufacturer','16AWG75mm input,XT60,30A/100A announcement; peak duration unknown'),
        ('Amazon-holder-US','https://www.amazon.com/dp/B004ZIUA62','marketplace','ASIN previously identified; challenge response this task'),
        ('Amazon-holder-FR','https://www.amazon.fr/dp/B004ZIUA62','marketplace','challenge response; stock/price/delivery not confirmed'),
        ('Amazon-fuse-FR','https://www.amazon.fr/s?k=Littelfuse+ATO30BP','marketplace_search','no exact listing orASIN validated'),
        ('price-fuse','https://www.digikey.com/en/products/detail/littelfuse-inc/0ATO030-V/2519124','authorized_distributor','exact reference;1.43USD/one; dimensions body not total envelope'),
        ('pack-review','https://www.canadiantire.ca/en/pdp/littelfuse-ato-blade-fuse-5-pk-0201571p.0201581.html','merchant_and_first_hand_reviews','ATO30BPfive-pack;6.29CAD;4.6/172 aggregated multiple ratings; no exact thermal validation'),
        ('holder-forum','https://forums.sailboatowners.com/threads/what-are-you-using-as-a-bilge-pump-fuse-holder.162517/','first_hand_forum','MaineSail2014-05-23#2 explicitlyuses5065; noRC measurements'),
        ('holder-dimensions','https://shop.pkys.com/Blue-Sea-5065--Waterproof-In-Line-Fuse-Holder-for-ATOATC-Fuses_p_2716.html','merchant_measurements_previously_read','approx2017hole3/16in,edge5/32in; not factorycotes; provenance inPi dossier'),
        ('holder-price','https://www.hodgesmarine.com/blu5065-blue-sea-5065-waterproof-inline-fuse-holder-atoa.html','merchant_previously_read','15.01USD reference fromsame-dayPi study; recheck beforebuying')]
    data('sources.json',dict(checked_on='2026-10-14',sources=[dict(id=i,url=u,type=t,support=s) for i,u,t,s in sources],
        native_step_obtained=False,hardware_measured=False,manufacturer_contacted=False,exact_youtube_measurement_found=False,amazon_fr_exact_basket_verified=False))
    cat=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'))
    lines=['# Modèles 3D des protections moteurs','','**Cinq STEP, millimètres, solides nommés et couleurs.** Deux références, cinq vues et assemblages ; aucun matériel mesuré.','',
        '| Modèle | STEP | Aperçu | Taille |','| --- | --- | --- | ---: |']
    for m in cat['models']:
        folder='../'+m['folder'].split('protection-branches-moteurs/')[1]+'/3D/' if m['folder']!='protection-branches-moteurs' else './'
        lines.append(f"| {m['title']} | [STEP]({folder+m['file']}) | [PNG]({folder+m['preview']['file']}) | {m['bytes']/1e6:.2f} Mo |")
    lines+=['','Le support reprend la reconstruction 5065 de la branche Pi : socle, capot creux avec oreille, joint orange, contacts femelles approchés et deux fils rouges continus. Fils et brins de longueur illustrative ; absence de cosses et raccords. Le fusible ATO30 est vert, marqué 30 et reprend les cotes de référence fabricant.',
        '', 'Support, contacts et petites formes de moulage estimés ; PA66 translucide réel rendu opaque. Pas d’élément interne calibré de fusible inventé. Vue éclatée : capot Y+36. Pose double : supports X±26, sans raccord de répartition ni faisceau final.',
        '', '[Cotes et limites](../cotes.md), [intégration](../integration.md), [contrôles FreeCAD sans interface](validation-freecad.json). Réimports CadQuery : validité, volumes, enveloppes, solides, couleurs et absence de chevauchement. Aucun test GUI FreeCAD/CAD View revendiqué ; fichiers hors gitignore.']
    write('3D/README.md','\n'.join(lines))
    print('Dossiers, sources, nomenclature, calculations and3Dindex written',flush=True)
if __name__=='__main__':main()
