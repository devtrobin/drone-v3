<!-- alimentation-r2 -->
> **Sélection active révisée le 15 octobre 2026.** ATO 30 A / Blue Sea 5065 retirés de la sélection active. Deux KLKD020.T 20 A proposés. Régime continu de dimensionnement : 15 A par ESC ; scénario court 20 A par ESC, 2 s, à tester. Les objectifs de vitesse/autonomie sont conservés.
> [État électrique courant](../verification-alimentation/README.md) · [Raccordements](../verification-alimentation/integration.md). Les références différentes dans les documents ci-dessous sont historiques. Qualification matérielle non réalisée ; confirmations restantes explicites.
<!-- /alimentation-r2 -->

# Protection des deux départs moteurs

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
