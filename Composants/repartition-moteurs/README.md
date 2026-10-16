<!-- alimentation-r2 -->
> **Sélection active révisée le 15 octobre 2026.** UD80 conservé : arrivée 6 mm² LAPP et départs selon le nouveau tableau. Ne pas substituer du 10 AWG nominal à son minimum IEC 6 mm².
> [État électrique courant](../verification-alimentation/README.md) · [Raccordements](../verification-alimentation/integration.md). Les références différentes dans les documents ci-dessous sont historiques. Qualification matérielle non réalisée ; confirmations restantes explicites.
<!-- /alimentation-r2 -->

# Répartition positive après relais - nVent ERIFLEX UD-80A

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

La [fiche constructeur](https://www.nvent.com/en-us/ERIFLEX/products/EFSUD-80A) et la [notice IP7802](https://nvent.widen.net/content/vhxyvvgeqg/original/ip7802.pdf) sont archivées. Les valeurs IEC et UL de serrage/dénudage diffèrent pour les grosses bornes ; la notice de montage distingue les tableaux et les points à confirmer sur le lot.
