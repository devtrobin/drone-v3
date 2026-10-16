# Recherche technique, achat et retours d'utilisation

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

Les valeurs proviennent de [la fiche ATO aftermarket 2022](https://www.littelfuse.com/assetdocs/littelfuse-datasheet-ato?assetguid=bba6ed2a-96e5-4b07-ab5d-0e8d267c0bd1), et non d'une fiche ATOF 287 d'une autre révision. Le « 100 A de pointe » de l'ESC ne fournit pas sa durée. La nouvelle [fiche Hobbywing](https://www.hobbywing.com/en/products/quicrun-wp-16bl30-g2) confirme les deux entrées **16 AWG, 75 mm**, XT60. Leur tenue avec ATO30 est une information encore manquante, pas une compatibilité acquise.

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
| Répartition après relais | [UD80A569010](../repartition-moteurs/integration.md) retenu ; connexions, serrage du lot et tenue aux défauts à qualifier |
| Perte d'un seul moteur au défaut | Arrêt global supervisé à concevoir ; aucune détection de fusion fournie par ces pièces |

La fiche fabricant a été lue en ligne. Son téléchargement direct retourne 403 ; sa copie RSP de quatre pages, avec bannières distributeur et dernière page Mouser, est archivée **inchangée**. Les statuts des réponses Amazon et des téléchargements sont conservés dans [assets.json](assets.json). Aucun forum, vendeur ou fabricant contacté.
