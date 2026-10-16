<!-- alimentation-r2 -->
> **Sélection active révisée le 15 octobre 2026.** ATO 7,5 A / Blue Sea 5065 retirés de la sélection active. Nouveau départ : KLKD010.T 10 A et support Midget. Ce calibre d’entrée ne donne pas 10 A à la Pi.
> [État électrique courant](../verification-alimentation/README.md) · [Raccordements](../verification-alimentation/integration.md). Les références différentes dans les documents ci-dessous sont historiques. Qualification matérielle non réalisée ; confirmations restantes explicites.
<!-- /alimentation-r2 -->

# Protection du départ Raspberry Pi

Sélection d'étude du **14 octobre 2026**, non achetée et non testée : **un porte-fusible Blue Sea Systems 5065** et **un fusible Littelfuse ATO 7,5 A**, référence unitaire **0ATO07.5V**. Conditionnement possible : **0ATO07.5VP / ATO7.5BP**, carte de cinq fusibles, un embarqué et quatre de rechange si ce lot est acheté.

Le porte-fusible est placé **au début du départ positif Pi**, avant le Pololu 2813. Sa fonction est de protéger ce départ contre les surintensités ; il ne constitue pas une protection garantie des semi-conducteurs ou une coupure instantanée à 7,5 A.

| Pièce | Caractéristiques retenues | Achat |
| --- | --- | --- |
| [Porte-fusible 5065](porte-fusible/README.md) | Un circuit ATO/ATC ; maximum fabricant 30 A ; deux fils 12 AWG ; fusible séparé | ASIN **B004ZIUA62** confirmé sur Amazon.com ; offre Amazon.fr non confirmée |
| [Fusible ATO 7,5 A](fusible-7-5a/README.md) | 32 V DC ; pouvoir de coupure 1 000 A à 32 V DC ; corps brun | Pas d'offre Amazon exacte ni d'ASIN confirmé ; recherche par référence conservée |

## Dossier

- [Intégration et qualification](integration.md), [calculs](calculs.json), [cotes et estimations](cotes.md).
- [Recherche, ambiguïtés, prix et retours utilisateurs](recherche-technique.md), [sources](sources.json), [archives](assets.json).
- [Notice PDF V3 et documents de référence](notices/README.md).
- [Six STEP détaillés et aperçus](3D/README.md), avec provenance et contrôles FreeCAD sans interface.
- [Nomenclature](nomenclature.json) : deux références distinctes ; aucune pièce commandée.

Le courant d'entrée d'étude vaut **4,36 A** pour 25 W au 5 V, un rendement supposé de 90 %, un pack à 6,4 V et 15 mA de commande SSR. Il peut augmenter avec un rendement inférieur, les pertes et les pointes au démarrage. Le tableau Littelfuse ne recommande plus que 4 A pour un ATO 5 A à 65 °C, contre 6 A pour le 7,5 A : **7,5 A retenu pour l'étude**, à qualifier sur le faisceau réel.

**La tenue aux défauts reste à établir.** Vérifier le courant prospectif vis-à-vis des 1 000 A du fusible, les sections et la coordination. Le MIDI principal 60 A ne garantit pas que le petit ATO bénéficie de son propre pouvoir de coupure supérieur. Aucun calibre supérieur n'est autorisé automatiquement si le démarrage fait fondre le fusible.

La référence 5065 est identifiée sur [Amazon.com](https://www.amazon.com/dp/B004ZIUA62), mais [Amazon.fr](https://www.amazon.fr/dp/B004ZIUA62) ne fournit pas d'offre exploitable dans cette recherche. [Recherche Amazon.fr du fusible exact](https://www.amazon.fr/s?k=Littelfuse+ATO7.5BP). Prix TTC et livraison française à vérifier. Repères étrangers consultés : support **15,01 USD** chez Hodges Marine ; fusible unitaire **1,35 USD** chez DigiKey, hors livraison et fiscalité France. Ce ne sont pas des devis français.
