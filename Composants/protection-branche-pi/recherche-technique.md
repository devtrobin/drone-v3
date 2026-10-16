# Recherche et ambiguïtés - départ Pi

Recherche du **14 octobre 2026**. Deux pièces retenues pour l'étude, aucun achat, aucune mesure matérielle.

## Sélection et alternatives

**Blue Sea 5065 + Littelfuse ATO 7,5 A.** Le support est identifié par son ASIN Amazon.com et accepte le format ATO/ATC ; la référence Littelfuse choisie dispose de ses propres cotes, courbes et déclassement. Le 5065 à fils 12 AWG n'impose pas d'utiliser un fusible de 30 A : 30 A est sa capacité maximale publiée, 7,5 A le calibre du départ étudié.

| Alternative | Résultat de la recherche |
| --- | --- |
| Littelfuse FHM1BP / 0FHM0001XP | MINI, 14 AWG, jusqu'à 20 A ; documentation et plan de famille disponibles. Pas de fiche Amazon exacte exploitable trouvée. Comparaison PDF archivée ; pas la géométrie retenue |
| Blue Sea 5064 | Support ATO/ATC à fils 12 AWG, sans le même capot/joint présenté pour le 5065 ; non retenu |
| Supports génériques et lots de fusibles | Références/sections/limites parfois incomplètes ; leurs courbes ne remplacent pas la fiche Littelfuse exacte |
| ATO 5 A / 10 A | 5 A trop juste dans le scénario chaud ; 10 A augmente le courant toléré sans besoin démontré. 7,5 A reste conditionnel aux essais et au faisceau |

## Achat et prix observés

- **Support : ASIN B004ZIUA62** confirmé par le titre Amazon.com, Blue Sea 5065. Amazon.fr renvoie une vérification automatique ; pas d'offre, vendeur, stock, prix TTC ou livraison française validés. Une fiche sur Amazon.com ne prouve pas la disponibilité en France.
- **Fusible : 0ATO07.5V / ATO7.5**, carte alternative 0ATO07.5VP / ATO7.5BP. Recherche Amazon par ces noms sans offre exacte ou ASIN confirmé. La page Canadian Tire recoupe le pack de cinq ; contrôler le conditionnement du fournisseur retenu.
- Hodges Marine affiche **15,01 USD** pour le support ; DigiKey **1,35 USD** pour un fusible unitaire. Repères étrangers consultés, hors livraison et fiscalité France, non convertis en euros.
- PKYS affiche 9,78 USD avec des éléments de disponibilité contradictoires dans la page ; pas de stock déduit. Skysat s'affiche en GBP dans la page /en-gb : aucun prix EUR extrapolé. Aucun achat réalisé.

## Informations manquantes ou divergentes

1. Le fabricant 5065 annonce ATO/ATC, fils 12 AWG, 30 A maximum et fusible séparé. Sa page ne propose **aucun plan ni manuel autonome**. Le catalogue 2024, PDF pages 60/72, complète le contexte. La notice fournie est celle du projet.
2. « Waterproof » n'est pas un indice IP chiffré. Skysat mentionne IP66, mais la fiche Blue Sea 5065 et sa ligne de catalogue ne le confirment pas. Le IP66 du **5021** sur la même page n'est pas repris pour le 5065.
3. PKYS, Peter Kennedy, **1er novembre 2017**, donne un trou approximatif de 3/16 pouce et un centre à 5/32 de trois bords, en citant une vis #10. Ces approximations ne donnent ni une tolérance ni une garantie de passage M5. La CAO Ø5,0 est explicitement une estimation.
4. Skysat donne **38 × 25 × 15**, sans plan ni clarification de l'oreille. Autres sites : dimensions de colis incompatibles, 7 × 7 × 6 pouces ou 4 × 2 × 1. Aucune de ces valeurs n'est devenue une cote fabricant. Le modèle propose 37,5 × 38 × 15 hors fils, à relever sur la pièce reçue.
5. Photo exacte : **deux fils rouges du même côté**, joint orange à nervures et capot séparé. Les fils ne sont pas une paire positif/négatif. Longueur livrée et diamètre d'isolant non confirmés ; longueur CAO illustrative. PKYS décrit du cuivre étamé marin ; nombre de brins réel inconnu.
6. Fusible : plan 2022 **19,1 × 5,1 × 18,8**. La hauteur marchande DigiKey 12,19 semble désigner le corps ; la hauteur totale suit le plan. La cote 14,5 est la largeur extérieure des lames, pas leur entraxe : **10,4 mm déduits** de lames de 4,1.
7. Fiche actuelle de famille 287/297 non assimilée automatiquement à la référence aftermarket **0ATO07.5V** : les tableaux de la fiche exacte 2022 sont utilisés, notamment 10,91 mΩ et 60 A²s. Les variantes MINI et Smart Glow ne sont pas les composants modélisés.
8. Pololu 2813 : les 6 A associés à 55 °C décrivent la température MOSFET dans un essai 12 V / ambiante 22 °C. Ce n'est pas une coupure à 6 A ou une garantie à 55 °C ambiants. La fiche ne prévoit pas de limitation active de courant.
9. **Pouvoir de coupure 1 000 A** de l'ATO et coordination avec la LiPo à vérifier. Un principal de 60 A ne garantit ni sélectivité ni tenue combinée accrue ; pas de courant prospectif établi ici. Le calibre restera provisoire jusqu'à qualification.

## Avis, forums et vidéos

- [Sailboat Owners, message #2 du 23 mai 2014](https://forums.sailboatowners.com/threads/what-are-you-using-as-a-bilge-pump-fuse-holder.162517/) : **Maine Sail** dit utiliser le Blue Sea 5065 pour protéger le fil allant du bus batterie au commutateur de pompe. Usage réel voisin, sans courant ou température mesurés ; pas une validation du robot. Les autres messages parlent aussi d'autres supports et ne lui sont pas attribués.
- [Avis eBay exacts 5065](https://www.ebay.com.au/urw/Blue%2BSea%2BSystems%2BWaterproof%2BIn-line%2BFuse%2BHolder%2B5065/product-reviews/721379242?_itm=391693814716) : cinq avis consultés, notamment 13 septembre 2018 et 23 septembre 2025, appréciant installation et qualité perçue ; deux avis de mars 2026. Aucun protocole d'étanchéité, mesure d'échauffement ou essai électrique précis.
- Canadian Tire affiche **4,6/5 et 151 avis**, mais plusieurs calibres et variantes partagent la page. Cette note ne qualifie pas le 7,5 A exact. Le champ « 8 A » du marchand est ignoré au profit du **7,5 A** fabricant ; les dimensions de carte d'emballage ne servent pas au fusible.
- Recherche Google/YouTube ciblée « Blue Sea 5065 » et « ATO7.5BP » : **aucune vidéo d'essai exact exploitable trouvée**. Aucun retour utilisateur n'est transformé en preuve de pouvoir de coupure.

## Documents et modèles

La copie RSP de la fiche ATO 2022 comporte des bannières RSP et une page Mouser ; elle est conservée telle que diffusée, sans modification locale. Catalogue Littelfuse 2013 via RS et fiche FHM de comparaison archivés. Le catalogue Blue Sea 2024 déjà téléchargé est référencé depuis son dossier de distribution pour éviter une copie de 28 Mo. [Notices](notices/README.md), [empreintes et statuts d'archives](assets.json).

Aucune CAO native, aucun plan officiel du 5065 et aucune mesure de lot obtenus. Six STEP reconstruits, détails inconnus signalés et contrôles numériques conservés. Leur géométrie ne certifie ni l'étanchéité, ni la pression électrique des contacts, ni les performances du fusible.
