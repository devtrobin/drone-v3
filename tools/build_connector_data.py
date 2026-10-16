"""Write connector selection, sourced dimensions, integration and calculations."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/connecteurs-alimentation'
AMASS='https://www.china-amass.com/biao/283.html'
CAT='https://www.china-amass.com/public/upload/20260207/7fa24f5a6f35ec66c7a115c07a34ab06.pdf'
OLD='https://www.shoptronica.com/ficheros/XT60H.pdf'
AMAZON='https://www.amazon.com/dp/B074PN6N4K'
def write(name,text):
    p=BASE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.strip()+'\n',encoding='utf-8')
def data(name,obj):write(name,json.dumps(obj,ensure_ascii=False,indent=2))
def main():
    sys.stdout.reconfigure(encoding='utf-8')
    write('README.md',f'''# Connecteurs des deux départs moteurs - AMASS XT60H

Choix d'étude du **14 octobre 2026** : **deux XT60H-F, contacts femelles, avec capots arrière**, côté faisceau, complémentaires aux XT60 à contacts mâles des deux Hobbywing WP16BL30 G2. La [photo constructeur conservée](photos/Hobbywing-WP16BL30-G2-contacts-originaux.jpg) montre les broches mâles ; contrôler cette interface et ses polarités à réception. Aucun achat ni essai matériel réalisé.

| Élément | Quantité à ajouter | Fonction |
| --- | ---: | --- |
| [XT60H-F et son capot](xt60h-f/README.md) | **2** | Positif après chaque ATO30 et négatif séparé vers D- ; départs ESC1 et ESC2 |
| [XT60H-M de référence](xt60h-m/README.md) | **0 obligatoire** | Interface déjà montée sur les ESC ; CAO de l'accouplement, pièces de rechange si lot par paires |
| Capots | 2 pour les F utilisés | Vérifier leur présence dans l'offre ; le catalogue fabricant les décrit comme optionnels |

Ces deux prises ne sont ni un connecteur de phases moteur ni un remplacement du XT60 de la batterie. Leurs deux pôles portent **le courant d'un seul ESC**. Les calibres des ESC et fusibles n'imposent pas le courant réellement traversé.

## Documentation et fichiers

- [Notice PDF et documents AMASS originaux](notices/README.md).
- [Cotes et différences de révision](cotes.md), [intégration et procédure de montage](integration.md).
- [Recherche Amazon, citation et avis utilisateurs](recherche-technique.md), [sources](sources.json), [archives et empreintes](assets.json).
- [Calculs et limites de courant](calculs.json), [nomenclature](nomenclature.json).
- [Huit STEP colorés avec aperçus et contrôles FreeCAD](3D/README.md) : F, M, sans capot, capot séparé, accouplement, éclaté et F câblé illustratif.

## Achat proposé

Lot **SoloGood / AMASS, 10 paires XT60H**, ASIN **B074PN6N4K**, [fiche Amazon.com]({AMAZON}). Titre et boutique SoloGood retrouvés dans la page consultée ; variante 10 paires à revérifier avant commande. [Lien Amazon.fr par ASIN](https://www.amazon.fr/dp/B074PN6N4K) et [recherche française](https://www.amazon.fr/s?k=AMASS+XT60H+capot) : **prix, vendeur, stock et livraison en France non confirmés**, pages directes bloquées. Aucune disponibilité française inventée.

Le besoin réel est de deux femelles, pas dix paires. Si ce lot est retenu et conforme, il annonce dix F et dix M ; deux F et leurs capots utilisés, huit F et dix M en réserve. Vérifier les **vingt capots** attendus, la couleur et l'authenticité sur l'offre exacte. Une petite quantité de F seuls avec capots peut coûter moins cher : [AMASS XT60H-F chez TME](https://www.tme.eu/fr/details/xt60h-f/connecteurs-dc/amass/), prix total rendu à comparer. Aucun prix exploitable relevé, aucun total budgétaire attribué.

## Courant retenu pour l'étude

La fiche historique V1.2 indique **30 A RC / 60 A MC**, sans durée d'impulsion publiée. Le catalogue fabricant **2026**, page 15, indique **35 A MAX, 12 AWG, Δ < 85 °C**, et 100 cycles ; la page produit exprime Δ < 85 K. Ces différences sont documentées, sans additionner les meilleures valeurs des révisions. Le « 60 A continu » des annonces commerciales n'est pas adopté.

Nous conservons une référence prudente de **30 A par prise**, avec un scénario **20 A par ESC non mesuré et non limité activement**. Ni cette référence ni le fusible ATO30 ne qualifient les pointes, les fils 16 AWG d'origine, ou le défaut LiPo. La paire XT60 du pack voit environ **44,39 A dans le scénario commun**, au-delà de cette référence de 30 A : cette interface reste à qualifier ou revoir séparément.
''')
    write('xt60h-f/README.md',f'''# AMASS XT60H-F - complément côté faisceau

Deux prises à contacts femelles, chacune avec capot isolant. Côté source, après le fusible de son ESC. Le suffixe **F désigne les contacts métalliques femelles** : certaines annonces appellent pourtant la forme extérieure « fiche mâle ». Décider à partir des contacts et de la référence AMASS, pas de ce mot isolé.

Dimensions actuelles nominales hors fils : **24,95 × 16,40 × 9,20 mm**, catalogue AMASS 2026 p.15 ; page produit arrondie à 25,00 mm de longueur. Ancienne V1.2 : 23,50 mm. Lot réel à mesurer. [Modèle assemblé](../3D/amass-xt60h-f-detaille.step), [sans capot](../3D/amass-xt60h-f-sans-capot.step), [câblé illustratif](../3D/amass-xt60h-f-cable-12awg-illustration.step).

[Dossier commun](../README.md), [cotes](../cotes.md), [montage](../integration.md), [notices](../notices/README.md). [Offre Amazon identifiée]({AMAZON}), stock et livraison France non confirmés.
''')
    write('xt60h-m/README.md','''# AMASS XT60H-M - interface de référence

Contacts métalliques mâles, broches dorées fendues, côté contrôleur selon l'ancienne fiche AMASS. Les deux ESC choisis sont déjà équipés de XT60 à broches mâles selon la photo Hobbywing ; **aucun ajout de deux M au panier n'est nécessaire** pour conserver ces prises. Le fabricant Hobbywing publie la famille XT60, sans garantir le sous-type exact H-M ni la révision AMASS.

Le modèle M sert à l'étude d'accouplement ; il ne reproduit pas une prise Hobbywing mesurée. Dimensions nominales AMASS 2026 : **23,85 × 16,40 × 9,20 mm** ; ancienne V1.2 : 23,80 mm ; page produit arrondie : 23,90 mm. [Modèle assemblé](../3D/amass-xt60h-m-detaille.step), [sans capot](../3D/amass-xt60h-m-sans-capot.step).

[Dossier commun](../README.md), [cotes](../cotes.md), [montage](../integration.md), [notices](../notices/README.md). Ne pas transformer cette pièce de référence CAO en achat obligatoire ou laisser des broches reliées à une source accessible.
''')
    write('cotes.md',f'''# Cotes, révisions et fidélité 3D

Unités : mm. Pas de mesure du lot physique. [Catalogue fabricant 2026]({CAT}), page imprimée 15, index PDF 14 ; [fiche historique V1.2]({OLD}), F page 1 / M page 2 ; [plan de la page produit](photos/AMASS-plan-page-produit.png).

| Dimension | Catalogue 2026 | Page produit | Fiche V1.2 |
| --- | --- | --- | --- |
| Longueur F, capot compris hors fils | **24,95** | 25,00 | 23,50 |
| Longueur M, capot compris hors fils | **23,85** | 23,90 | 23,80 |
| Largeur maximale | **16,40** | 16,40 | 16,40 |
| Épaisseur maximale | **9,20** | 9,20 | 9,20 |
| Entraxe contacts | Non coté dans la vue courante | Non coté | **7,20**, conservé comme hypothèse courante |
| Longueur V1.2 entre arrière du contact et face avant | Pas transposée | Pas cotée | F20,20 / M20,50 |
| Segment avant indiqué V1.2 F | Pas transposé | Pas coté | **7,70** ; pas la hauteur générale |

Pour une réservation d'implantation, **25 × 16,4 × 9,2 mm pour F**, hors débattement de prise, longueur de fils, rayon de courbure et tolérances. Les 0,05 mm entre arrondi et catalogue ne sont pas une tolérance publiée. L'ancienne cote 20,2/20,5 ne désigne pas automatiquement le corps plastique complet.

## Construction des STEP

Les enveloppes F24,95 et M23,85 suivent **une même révision : catalogue 2026**. Profil extérieur détrompé, deux contacts métalliques séparés, logements femelles creux, broches mâles fendues, godets ouverts à souder, collerette, capot arrière creux, trous de sortie de fils, rainures de prise et fenêtres de clips. Marquages simplifiés gravés XT60H-F/M et +/-. Couleurs de lecture : PA jaune, capot gris sombre, contacts dorés ; pas de mesure colorimétrique.

Les diamètres internes, lèvres, fentes, épaisseurs, rayons, clips et gravures ne sont pas cotés intégralement dans les sources : **détails estimés**, pas CAO fabricant. Le Ø3,5 de contact, le godet Ø3,3, l'entraxe de la fiche V1.2 et la répartition des longueurs avant/capot sont des hypothèses d'implantation actuelle. Aucun résultat électrique déduit du volume de métal représenté.

Repère des pièces : X = entraxe des contacts, Y = épaisseur, Z = axe de connexion, face avant z=0, fils vers +Z. Capot isolé : face avant z=0. La paire accouplée est illustrée avec **7,5 mm d'engagement estimé**, sans collision volumique ; pas un ajustement qualifié. La vue éclatée décale les contacts et capots pour lecture, pas une instruction de démontage des contacts moulés.

Le modèle câblé représente du cuivre équivalent **3,31 mm²** avec une gaine Ø4,2 mm estimée, pas un fil acheté ni son nombre réel de brins. Soudure et fins dénudées illustratives. Dimensions du faisceau à arrêter après implantation. Les symboles + et - de la CAO ne remplacent pas la vérification des inscriptions, du point de vue avant/arrière et de la polarité réelle au multimètre.

## Données électriques séparées

| Source | Courant | Autres valeurs |
| --- | --- | --- |
| AMASS V1.2 | 30 A RC / 60 A MC, durée MC non publiée | 0,50 mΩ CR ; 1 000 usages ; 12 AWG ; PA UL94 V0 ; laiton doré ; -20 à +120 °C |
| AMASS catalogue 2026 p.15 | 35 A MAX (12 AWG / Δ < 85 °C) | 100 cycles ; IP40 ; tenue 500 V DC ; -20 à +120 °C ; UL94 V0 |
| Page fabricant courante | 35 A MAX (12 AWG / Δ < 85 K) | PA / laiton doré ; 100 cycles ; 48 h brouillard salin ; isolation ≥2 000 MΩ |

La page HTML imprime « ≤1.2MΩ » à la ligne résistance de contact : unité incohérente avec l'isolation et l'usage. **Ne pas recopier 1,2 MΩ comme résistance de contact.** Aucun plafond moderne en mΩ n'est adopté sans fiche de spécification du lot. Le lien LCSC 2023C0 redirige vers une visionneuse et n'a pas fourni de PDF original exploitable dans cette collecte ; il n'est pas utilisé pour combler cette erreur d'unité. Pour les calculs, 0,50 et 1,20 mΩ sont seulement deux valeurs d'analyse explicitement conditionnelles.

500 V est une valeur de tenue du document courant, pas un besoin du robot alimenté en 2S. IP40 n'est pas une étanchéité à l'eau. Ni PA120 °C ni Δ85 K ne fixent une température acceptable des soudures, câbles et interfaces du robot.
''')
    write('integration.md','''# Intégration et notice de montage des deux prises

```mermaid
flowchart LR
 S[Relais D1D100 sortie 1] --> J[UD80A : deux sorties positives]
 J --> F1[5065 + ATO30 ESC1]
 J --> F2[5065 + ATO30 ESC2]
 F1 -->|Positif| C1[XT60H-F départ 1]
 F2 -->|Positif| C2[XT60H-F départ 2]
 N[MiniBus D- N1 et N3] -->|Deux retours négatifs séparés| C1
 N --> C2
 C1 --- E1[XT60 mâle existant ESC1]
 C2 --- E2[XT60 mâle existant ESC2]
```

Le + de chaque F vient de **la sortie de son propre ATO30**. Le - revient individuellement vers N1 ou N3 du MiniBus D-. Les deux pôles d'une prise portent le même courant de boucle ; ne pas partager une seule prise pour les deux ESC. N2 reste le retour batterie et N4 l'électronique. Les trois prises de phases 3,5 mm entre ESC et moteur restent distinctes.

## Fils et limites

AMASS recommande **12 AWG**, environ **3,31 mm²** de cuivre. Cette section convient nominalement aux fils du Blue Sea 5065 ; les ESC conservent leurs fils **16 AWG / 75 mm** d'origine. Pour les queues à souder et les retours de ces prises, proposition de 12 AWG court, longueur après implantation. Les anciens exemples de 4 mm² restent des comparaisons de pertes, **pas une autorisation de forcer du 4 ou 6 mm² dans un godet XT60H**. Si un tronçon de 4 mm² est nécessaire, choisir ensuite un raccord de transition qualifié ; ne pas éliminer des brins pour faire entrer un fil.

Le tronc commun 6 mm² arrive au répartiteur ; il ne passe pas dans les deux nouveaux XT60H. Les raccords 5065-vers-F et D--vers-F, cosses, gaine et maintien du faisceau restent à sélectionner. Le capot isole les godets, mais aucune force de traction admissible n'est publiée : prévoir une retenue des fils par le châssis, sans utiliser la soudure comme ancrage.

Référence de fil maintenant proposée : [BNTECHGO SW12G68008F10C2, 12 AWG rouge/noir](../cable-puissance-12awg/integration.md), ASIN B01ABOPMEI. Gaine **Ø4,5 ±0,1 mm annoncée**, contre Ø4,2 estimée dans l'ancien modèle câblé : vérifier le passage des capots du lot, dont les perçages CAO étaient également estimés. Les modèles illustratifs anciens restent distincts ; mesurer avant fixation ou modification de capot.

Scénario : **20 A par ESC**, référence de travail **30 A par prise**. Aucun dispositif ne garantit aujourd'hui cette limite individuelle ; 40 A total peut se répartir 30+10, 35+5 ou autrement. Les 100 A de pointe de l'ESC ne sont pas une capacité démontrée du raccord. Le fusible ATO30 peut laisser durer une surcharge ; il n'est pas un limiteur à 30 A. Valider courant RMS, pointes, baisse de tension et échauffement sur la durée prévue, y compris démarrage et freinage.

## Préparation et soudure

1. Débrancher batterie **et prise d'équilibrage** ; aucune soudure ni mesure d'ohmmètre sur le faisceau alimenté. Travailler sur les prises neuves détachées, sans couper ou modifier les fils du pack.
2. Identifier les contacts : **F = logements femelles, M = broches mâles**. Lire les +/-, dessiner le raccord selon la vue choisie ; avant et arrière s'inversent visuellement. Ne pas déduire la polarité de la couleur du plastique.
3. Faire passer les fils dans le capot avant soudure. Présenter le cuivre dans le godet pour régler le dénudage, tous les brins à l'intérieur sans cuivre libre hors de la protection. Aucune longueur ou température de soudage fabricant exacte confirmée : régler selon fil, alliage, outil et procédure applicable au lot.
4. Souder chaque conducteur séparément, éviter pont d'étain et chauffe prolongée du PA. Un connecteur complémentaire **neuf et totalement hors tension** peut maintenir l'alignement pendant l'opération ; ne pas utiliser une batterie comme gabarit.
5. Laisser refroidir ; examiner remplissage, brins, isolation, position des contacts et état du boîtier. Vérifier que les godets sont isolés entre eux et entièrement couverts ; clipser sans forcer le capot. Toute soudure froide, plastique déformé ou contact mobile impose de reprendre la pièce.
6. Maintenir les fils près de la prise avec une retenue dédiée, garder l'accès à la prise et aux fusibles. Débrancher en tenant les corps, sans tirer sur les fils. Protéger les F alimentées des objets métalliques et débris.

Ce protocole du projet n'est pas une notice AMASS officielle de soudage. La vidéo SoloGood identifiée montre le sujet exact, mais son simple référencement ne prouve pas une température, un temps ou une qualification V3. Aucun couple de serrage pour ces godets soudés ; les bornes vissées du répartiteur et du MiniBus suivent leurs propres notices.

## Vérifications

Hors tension : continuité de chaque + vers **son** fusible, chaque - vers D-, isolement +/-, polarités et séparation des deux branches. Mesurer la polarité de la source avant tout raccordement des ESC, après préparation d'une première alimentation limitée et supervisée. Vérifier emboîtement complet, contacts tenus, capots et efforts de traction raisonnables sur le faisceau fini.

Mesurer chute de tension de la paire accouplée et températures des deux pôles, soudures et fils sous les usages représentatifs ; noter ambiante et durée. Une résistance mesurée inclut les points de prise de mesure : séparer les contributions par mesure quatre fils si nécessaire. Inspecter après vibrations et cycles de branchement. Pas de test volontaire de court-circuit de LiPo.

L'interface XT60 batterie reste distincte : scénario commun **44,39 A**, révision inconnue. Elle doit être qualifiée ou remplacée avec une chaîne compatible pack/chargeur adaptée ; les deux prises d'ESC ne résolvent pas ce point. Les performances de 40 km/h et d'autonomie ne sont pas validées par cette sélection.

[Protections des moteurs](../protection-branches-moteurs/integration.md), [répartiteur](../repartition-moteurs/integration.md), [distribution](../distribution-alimentation/integration.md), [batterie](../batterie/README.md).
''')
    write('recherche-technique.md',f'''# Recherche, achat, citation et retours

Consultation du **14 octobre 2026**. Références publiques ; aucune commande, aucun essai du lot, aucune note commerciale considérée comme homologation électrique.

## Offres Amazon

| Candidat | Référence / lien | Résultat |
| --- | --- | --- |
| **SoloGood / AMASS, 10 paires XT60H, capots** | [Amazon.com B074PN6N4K]({AMAZON}) / [Amazon.fr](https://www.amazon.fr/dp/B074PN6N4K) | Titre et boutique retrouvés via page indexée Amazon.com ; proposition d'achat, stock/prix/livraison France non confirmés |
| Finware, 10 paires annoncées | [B01FXU61HW](https://www.amazon.fr/dp/B01FXU61HW) | ASIN repéré par republication commerciale, page directe inaccessible ; variante, authenticité et prix non confirmés |
| Lots génériques XT60H | [Recherche française](https://www.amazon.fr/s?k=AMASS+XT60H+capot) | Refuser la substitution d'une version XT60 sans capot ou d'un lot sans fiche exacte |

Pas de prix TTC français vérifiable. Le tarif tiers importé ou converti n'est pas pris pour le coût Amazon France. Comparer le total livré d'un petit lot (au moins deux F avec capots) à celui de dix paires. [TME F](https://www.tme.eu/fr/details/xt60h-f/connecteurs-dc/amass/) identifie AMASS et la référence ; disponibilité/prix exacts à vérifier. Le vocabulaire « fiche mâle ; femelle » mélange la forme extérieure et le contact : utiliser F/M AMASS.

## Information manquante résolue

- **Sens de la prise ESC** : [photo Hobbywing](https://www.hobbywing.com/en/products/quicrun-wp-16bl30-g2) et [original local](photos/Hobbywing-WP16BL30-G2-contacts-originaux.jpg), contacts mâles visibles ; le faisceau reçoit F. La page ESC n'identifie pas la version AMASS exacte.
- **Courant** : [AMASS page courante]({AMASS}) et [catalogue 2026]({CAT}) donnent 35 A sous conditions 12 AWG/Δ ; [V1.2]({OLD}) donne 30/60, sans durée MC. Les 60/100 A marchands ne remplacent pas ces fiches.
- **Capot** : option dans le catalogue actuel ; présence obligatoire à confirmer dans le lot acheté. Pas de remplacement automatique par un XT60 de forme proche.
- **Dimensions** : actuel F24,95/M23,85, anciennes F23,50/M23,80 ; page produit arrondie F25/M23,9. Différences conservées dans les cotes.
- **CAO** : téléchargements fabricant consultés, aucun STEP exact obtenu. Les STEP livrés sont des reconstructions détaillées avec estimations explicites.
- **Unité de résistance** : typo apparente MΩ sur page AMASS, pas adoptée. LCSC 2023C0 ne fournit pas ici de PDF exploitable après redirection ; aucune donnée complémentaire prétendument archivée.

## Citation courte

Catalogue AMASS 2026, page 15 : **« 35A MAX(12AWG/△<85℃) »**. Cette condition publiée n'autorise pas un échauffement de 85 °C dans notre montage. Fiche historique : **« Recommend USE BATTERY »** pour F et **« CONTROLLER »** pour M. Textes très courts attribués, sources originales dans les notices.

## Utilisateurs et vidéo

| Source | Retour observé | Portée |
| --- | --- | --- |
| [RCCrawler, Genuine Connectors, 28 juin 2020](https://www.rccrawler.com/forums/threads/genuine-connectors.619280/) | Inspector86 préfère la variante H et son capot qui s'enclenche ; high plains drifter décrit les marquages AMASS et un maintien supérieur dans son expérience | Usage déclaré et intérêt du capot ; authenticité d'un lot neuf et capacité de courant non prouvées |
| [DashCamTalk, câbles PowerCell / B-130X, janvier 2023](https://dashcamtalk.com/forum/threads/7500-mah-96-wh-blackboxmycar-powercell-8-blackvue-b-130x-thinkware-ivolt-xtra-bab-95.48162/page-2) | Utilisateurs disent fabriquer des câbles avec le lot B074PN6N4K ; discussion distingue XT60 à deux pôles et XT60I à troisième contact | Corrobore l'usage du lot pour confection de câbles ; chargeurs différents, pas essai moteur V3 |
| [SoloGood, How to solder Amass XT60H connector](https://www.youtube.com/watch?v=dDZxkl8b3hs), 8 octobre 2019 | Vidéo exacte identifiée, chaîne du vendeur, description et titre consultés | Démonstration à consulter ; pas une vidéo indépendante ni un essai thermique mesuré ; contenu visuel complet non visionné ici |
| Amazon.com B074PN6N4K | En-tête 4,7/5 observé via page indexée | Agrégat possiblement multi-variantes ; aucun avis individuel détaillé ni effectif fiable retenu |

Les désaccords de forums sur copies et sertissage ne servent pas à établir une certification. Pas de reprise du conseil communautaire interdisant tout cuivre étamé : cuivre étamé et aluminium cuivré sont différents. Ni température de fer ni courant continuel déduits d'un commentaire.
''')
    write('notices/README.md','''# Notices - connecteurs XT60H

- [Notice V3 : sélection, câblage, cotes, montage et réserves](notice-connecteurs-xt60h-v3.pdf) : document du projet, quatre pages, pas notice officielle AMASS.
- [AMASS XT60H-F/M V1.2, copie originale via Shoptronica](AMASS-XT60H-F-M-V1.2-via-Shoptronica.pdf), deux pages : dessins, 30 A RC / 60 A MC et usage F/M.
- [Catalogue AMASS XT 2026 original](AMASS-catalogue-XT-2026-original.pdf), 45 pages ; XT60H page imprimée 15 / index 14 : cotes actuelles et 35 A MAX sous conditions.
- [Catalogue AMASS 2024 original](AMASS-catalogue-3G-2024-original.pdf), 43 pages ; XT60H page imprimée 13 / index 12 : comparaison historique.

Sources PDF téléchargées inchangées, SHA256 dans assets.json. Accès Marutsu et LCSC non exploitable, consigné sans faux PDF ni lien local inexistant. La température/temps de soudage, tolérances, tenue à la traction et durée MC n'ont pas été confirmés sur une procédure du lot. [Recherche](../recherche-technique.md), [cotes](../cotes.md).
''')
    write('photos/README.md','''# Photos et plan de référence

- [Photo Hobbywing : WP16BL30 G2 et contacts mâles](Hobbywing-WP16BL30-G2-contacts-originaux.jpg), copie intacte du dossier moteur, source constructeur.
- [Plan F/M de la page AMASS actuelle](AMASS-plan-page-produit.png), F25,00/M23,90 ; cotes arrondies différentes du catalogue 2026.
- [Photo de détail AMASS, godets et capot](AMASS-produit-2.jpg), jaune et gris : illustration constructeur, pas photo du lot Amazon reçu.

Les autres images brutes de la page fabricant sont conservées et décrites dans assets.json avec URL et empreinte. Aucune photographie utilisée comme plan coté ou preuve de section interne. Les aperçus CAO sont dans le [dossier 3D](../3D/README.md).
''')
    sources=[
        dict(id='amass-current',url=AMASS,type='manufacturer',supports='35A, conditions, materiaux, dimensions arrondies, erreur unite CR signalee'),
        dict(id='amass-catalog-2026',url=CAT,type='manufacturer_pdf',local='notices/AMASS-catalogue-XT-2026-original.pdf',pages='15 imprimee / index14',supports='F24.95/M23.85,16.4,9.2,35A/12AWG/Delta,100cycles,capot optionnel'),
        dict(id='amass-legacy',url=OLD,type='manufacturer_pdf_on_distributor',local='notices/AMASS-XT60H-F-M-V1.2-via-Shoptronica.pdf',supports='F/M usage,7.2pitch,30/60A,0.5mohm,cotes anciennes'),
        dict(id='hobbywing',url='https://www.hobbywing.com/en/products/quicrun-wp-16bl30-g2',type='manufacturer',local='photos/Hobbywing-WP16BL30-G2-contacts-originaux.jpg',supports='XT60,16AWG75mm et photo contacts males'),
        dict(id='amazon',url=AMAZON,type='marketplace',supports='titre10paires et boutiqueSoloGood',availability_FR_confirmed=False,price_FR_EUR=None),
        dict(id='tme',url='https://www.tme.eu/fr/details/xt60h-f/connecteurs-dc/amass/',type='distributor',supports='reference AMASS F ; prix/stock non confirmes'),
        dict(id='forum-rc',url='https://www.rccrawler.com/forums/threads/genuine-connectors.619280/',type='firsthand_user_forum',supports='capot, marquage et maintien ; pas amperage certifie'),
        dict(id='forum-dashcam',url='https://dashcamtalk.com/forum/threads/7500-mah-96-wh-blackboxmycar-powercell-8-blackvue-b-130x-thinkware-ivolt-xtra-bab-95.48162/page-2',type='firsthand_user_forum',supports='fabrication de cables avec cet ASIN, XT60 distinctXT60I'),
        dict(id='video-sologood',url='https://www.youtube.com/watch?v=dDZxkl8b3hs',type='seller_video',published='2019-10-08',supports='titre et description seulement',full_visual_review=False),
    ]
    data('sources.json',dict(checked_on='2026-10-14',sources=sources))
    # Sensitivity, not a measured or guaranteed resistance ceiling for current lot.
    rows=[]
    for i in [10,20,30,40]:
        for r in [.0005,.0012]:rows.append(dict(current_A=i,resistance_per_pole_assumed_ohm=r,
            loop_drop_V=2*i*r,loop_loss_W=2*i*i*r,two_ESC_branches_total_W=4*i*i*r))
    common=40+25/(6.4*.9)+.05
    data('calculs.json',dict(checked_on='2026-10-14',hardware_tested=False,limits_enforced=False,
        scenario_individual_ESC_A=20,scenario_motors_total_A=40,working_reference_per_connector_A=30,
        current_catalogue_A=35,current_catalogue_conditions='12AWG / delta<85degC(K on product page), not V3 qualification',
        historical_MC_A=60,historical_MC_duration_s=None,example_resistance_scope='analysis per mated pole only;0.5legacy CR not clarified per assembly;1.2 sensitivity not guaranteed',
        contact_loss_examples=rows,common_battery_current_scenario_A=common,common_battery_XT60_qualified=False,
        added_tail_proposal_AWG=12,added_tail_nominal_mm2=3.31,original_ESC_AWG=16,original_ESC_lead_mm=75,
        previous_4mm2_example_is_not_a_terminal_fit=True,connector_prospective_fault_qualified=False,
        fuse30A_is_current_limiter=False,regeneration_qualified=False,all_currents_assumed=True))
    data('nomenclature.json',dict(checked_on='2026-10-14',purchased=False,
        vehicle_need=[dict(reference='AMASS XT60H-F',quantity=2,cap_required=True),dict(reference='XT60 male on ESC',additional_quantity=0,already_in_motor_kit=True)],
        candidate_lot=dict(asin='B074PN6N4K',brand_store='SoloGood',announced_pairs=10,expected_F=10,expected_M=10,
            expected_caps=20,actual_contents_verified=False,F_installed=2,F_spares=8,M_spares=10,
            price_TTC_EUR=None,Amazon_FR_stock_confirmed=False,shipping_FR_confirmed=False),
        wires_and_splices_selected=False,pdf_notice='notices/notice-connecteurs-xt60h-v3.pdf'))
    print('DOCS connectors written',flush=True)
if __name__=='__main__':main()
