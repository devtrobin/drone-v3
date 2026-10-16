<!-- alimentation-r2 -->
> **Sélection active révisée le 15 octobre 2026.** Positif CP0+ préparé sans cosse M5 vers le support classe T ; négatif CP0− avec une TE 130191 vers D−. Une seule cosse 130191 active, pas deux. Les STEP et l’ancien PDF avec deux cosses sont historiques.
> [État électrique courant](../verification-alimentation/README.md) · [Raccordements](../verification-alimentation/integration.md). Les références différentes dans les documents ci-dessous sont historiques. Qualification matérielle non réalisée ; confirmations restantes explicites.
<!-- /alimentation-r2 -->

# Cordon principal batterie vers distribution - IC5

**Choix du 15 octobre 2026 : batterie 2S avec une prise plus forte montée d’usine.** Proposition d’étude : **Spektrum Smart G1 SPMX50002S30H5**, 7,4 V /5 000 mAh /IC5, avec un **cordon SPMXCA510 pré-câblé en 10 AWG**. Aucun achat ni essai matériel.

| Élément actif | Dossier | Quantité | Achat |
| --- | --- | ---: | --- |
| IC5 véhicule + deux fils 10 AWG inclus | [SPMXCA510](cordon-ic5-spektrum/README.md) | 1 cordon | [Freakware](https://www.freakware.de/en/p/ic5-geraeteanschluss-kabel-4-100mm-10awg-spektrum-spmxca510-a167682.htm) |
| Cosses de puissance M5 | [TE 130191](cosses-te-130191/README.md) | 2 | [DigiKey](https://www.digikey.fr/fr/products/detail/te-connectivity-amp-connectors/130191/1864623) |
| Gaine adhésive | [ATUM 8/2](isolation-atum/README.md) | 2 coupes ≈20 mm | même barre déjà prévue |
| Batterie 2S révisée | [Spektrum G1 IC5](../batterie/spektrum-g1-ic5/README.md) | 1 pack | [RC Team](https://www.rcteam.com/products/spektrum-accu-lipo-smart-74v-5000mah-30c-ic5) |

[Notice PDF et originaux](notices/README.md) · [Montage](integration.md) · [Cotes IC5](cordon-ic5-spektrum/cotes.md) · [Devis, sources et avis](revision-batterie-ic5.md) · [Modèles STEP](3D/README.md) · [Sélection structurée](selection-active.json) · [Nomenclature](nomenclature.json) · [Contrôles](verification.json).

Le 510 arrive pré-câblé. Deux cosses et deux manchons le terminent vers l’entrée MIDI et D- N2. Les fils 6 mm² après MIDI, via ED80 et vers l’UD80 A, restent distincts. Aucun adaptateur XT60 en propulsion et aucun lot de fil acheté en double.

Le choix IC5 repose sur son emploi documenté sur un Spektrum Firma 100 A : c’est une **inférence d’ingénierie**, sans ampacité garantie de notre cordon. Le scénario 44,39 A, les fils d’usine du pack, l’échauffement et la coordination du MIDI 60 A restent à qualifier.

Prix partiels : batterie 49,99 EUR, cordon 9,89 EUR avec taxe locale affichée, deux cosses 1,344 EUR TTC indicatifs. **Sous-total indicatif 61,224 EUR**, hors gaine, port et outils, avec TVA/livraison France à revalider. Les références G1/510 sont arrêtées chez le fabricant ; des offres distributeurs existent encore. Aucune offre Amazon exacte n’a été validée pour ces deux références.

Le S65 peut être conservé avec la G1 à équilibrage, charge initiale 5 A ; **cordon/adaptateur de charge IC5 distinct à sélectionner avant charge**. Ne pas substituer une G2. Énergie nominale 37 Wh contre 38,48 Wh pour la Zeee (-3,85 %), sans preuve d’autonomie.

Châssis, support caméra, surveillance et visserie finale restent pour la fin. [Variante XT60 non retenue](variante-xt60-non-retenue.md) : huit fichiers initiaux gardés pour comparaison ; pas un achat supplémentaire. Les cosses nues et la référence ATUM sont communes.
