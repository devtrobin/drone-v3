<!-- alimentation-r2 -->
> **Sélection active révisée le 15 octobre 2026.** D+ / D− conservés. F0 devient classe T 50 A. Masse de logique et retours des commandes SSR sur D−, sans parallèle de puissance par B0 d’équilibrage.
> [État électrique courant](../verification-alimentation/README.md) · [Raccordements](../verification-alimentation/integration.md). Les références différentes dans les documents ci-dessous sont historiques. Qualification matérielle non réalisée ; confirmations restantes explicites.
<!-- /alimentation-r2 -->

# Distribution électrique - deux MiniBus 2315

Sélection d'étude du **14 octobre 2026**, non achetée et non testée : **deux Blue Sea Systems 2315**, chacun avec quatre goujons et son capot **2713 inclus**. Un bornier distribue le positif après le fusible principal ; l'autre collecte les retours négatifs. Les quatre bornes d'un même bornier sont **toutes reliées entre elles**.

| Caractéristique publiée | Valeur |
| --- | --- |
| Calibre continu | 100 A par bornier, pas par sortie indépendante |
| Tension maximale DC | 48 V ; pack V3 : 8,4 V maximum |
| Bornes | Quatre goujons **#10-32 UNF**, Ø nominal 4,826 mm ; pas 0,79375 mm |
| Barre / socle / capot | Cuivre C110 étamé / polycarbonate renforcé / polycarbonate transparent |
| Plan, longueur et largeur | 106,68 × 22,86 mm |
| Hauteur avec capot | **31,75 mm minimum**, pas une enveloppe maximale garantie |
| Fixation au châssis | Deux trous acceptant #10 ou M5 ; entraxe 90,49 mm |
| Masse publiée | 0,08 kg l'unité avec capot ; environ 160 g pour deux, hors fils |

Ce choix offre des cotes et une intensité documentées. Il ajoute une masse à prendre en compte dans le châssis. Le scénario principal actuel est de **44,39 A**, entièrement fondé sur des hypothèses : il n'établit ni la consommation réelle ni l'autonomie. Un bornier de 100 A n'impose aucune limitation de courant et ne remplace pas un fusible.

## Dossiers et livrables

- [Bornier 2315](bornier-2315/README.md) et [capot 2713 inclus](capot-2713/README.md).
- [Intégration et affectation des bornes](integration.md), [cotes publiées et estimations](cotes.md).
- [Recherche, comparaison, prix et avis](recherche-technique.md), [sources](sources.json), [archives et empreintes](assets.json).
- [Notice PDF V3 et originaux](notices/README.md), [photos de référence](photos/README.md).
- [Cinq modèles STEP, aperçus et contrôles](3D/README.md), [calculs](calculs.json), [nomenclature](nomenclature.json).

## Achat

**ASIN B000OTJ8A0 confirmé par la fiche Amazon.com** consultée via recherche web : titre 2315, quatre goujons, capot. [Lien Amazon.com](https://www.amazon.com/dp/B000OTJ8A0), [lien Amazon.fr à vérifier](https://www.amazon.fr/dp/B000OTJ8A0), [recherche française par référence](https://www.amazon.fr/s?k=Blue+Sea+2315).

L'offre Amazon.fr, le vendeur, le prix TTC, le stock et la livraison en France ne sont **pas confirmés**. Les téléchargements directs Amazon ont renvoyé une vérification automatique, conservée comme telle. Aucun achat effectué. Repère hors Amazon : Hodges Marine affichait **26,40 USD par unité**, soit 52,80 USD pour deux, hors traitement fiscal et livraison en France ; ce n'est pas un devis français.

Le conditionnement retenu est **deux ensembles 2315**, pas un kit double positif/négatif. Ne pas commander deux capots supplémentaires : ils sont inclus. Cosses, câbles, fixations de châssis et fusibles de branches restent à choisir. **Les départs plus fins ne sont pas protégés par le seul MIDI principal de 60 A.**

Le serrage présente un écart entre pages constructeur : 2315 indique 1,69 N·m sous « screw terminal torque », 2305 indique 2,03 N·m pour les goujons. Le dossier conserve cet écart ; la notice du lot doit le trancher avant montage.
