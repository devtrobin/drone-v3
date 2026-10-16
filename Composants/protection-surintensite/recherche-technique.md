# Recherche, ambiguïtés, prix et avis - 14 octobre 2026

## Choix comparés

| Solution | Points vérifiés | Choix |
| --- | --- | --- |
| **Littelfuse 04980900ZXT + 0498060.M** | MIDI à vis M5, compact ; dimensions, matière, temporisation et déclassement documentés | Retenu pour l'étude, calibre à qualifier |
| Littelfuse 04980903ZXT | Variante du support avec pattes de fixation externes | Possible, plus encombrante ; ne pas lui attribuer les cotes du 04980900ZXT |
| Blue Sea Systems 7720 | MIDI, 32 V DC, goujons câble M8 et fixation fusible M5 ; 70 g annoncés | Bien documenté, plus lourd et raccordements différents ; écarté pour ce robot compact |
| Petits supports génériques MIDI/MAXI | Offres et intitulés repérés, caractéristiques variables | Aucune référence précise retenue sans courbes, matériaux et dimensions vérifiés |

Source du Blue Sea : [fabricant 7720](https://www.bluesea.com/products/7720/AMI___MIDI_Safety_Fuse_Block). L'ASIN B004T1VYLA est indiqué par des références publiques ; la page Amazon.fr n'a pas été accessible. Ce numéro concerne **l'alternative Blue Sea**, pas le support Littelfuse.

## Amazon et prix

[Recherche du support](https://www.amazon.fr/s?k=Littelfuse+04980900ZXT), [recherche du fusible](https://www.amazon.fr/s?k=Littelfuse+0498060.M). Les réponses locales sont des **pages de vérification `bm-verify`**, pas des fiches produit. Elles ne prouvent aucune disponibilité. Aucun ASIN exact ni prix Amazon français n'est confirmé pour les deux références choisies.

La page internationale [TME du support](https://www.tme.eu/en/details/04980900zxt/car-fuseholders/littelfuse/) affichait 8,42 USD par unité lors de la consultation ; la page [Farnell UK du fusible](https://uk.farnell.com/littelfuse/0498060-m/automotive-fuse-time-delay-60a/dp/3516004) affichait 2,41 GBP HT à l'unité. Stock et devis français livré restent à revalider. Ces devises ne sont pas additionnées pour créer un faux budget en euros. Les nombres 330 ou 1 000 dans les documents désignent des conditionnements fabricant, pas le contenu nécessaire au robot ni forcément le minimum vendeur.

## Retours d'utilisateurs et vidéos

Les annonces eBay exactes `04980900ZXT` consultées indiquent **aucun avis produit**. La note du vendeur ne constitue pas un avis sur la tenue thermique du support. Aucune mesure indépendante exploitable pour ce couple de références, notre LiPo 2S et nos deux ESC n'a été trouvée sur YouTube ou dans les forums consultés.

Un [fil de forum esk8](https://forum.esk8.news/t/fuse-your-charge-ports-ft-the-smallest-user-serviceable-fuse-holder/17960?page=2), janvier 2020, discute du format MIDI et de ses cosses dans des montages à batterie/ESC. C'est un retour d'usage général, **pas un essai de notre référence**. Certaines affirmations du fil sur l'emplacement du fusible sont discutables ; le montage proposé suit le principe documenté par les fabricants : placement près de la source et protection des conducteurs. Aucune citation de ce fil n'est utilisée comme limite électrique.

## Ambiguïtés traitées

- Pouvoir de coupure : vieille fiche TME **1 000 A**, révision 2021 **2 000 A à 32 V DC**, révision 2024 consultée en ligne également 2 000 A. Conserver ces versions séparées, vérifier la fiche et le lot proposés par le vendeur.
- Hauteur du fusible : **8,0 mm pour 60 A**, 8,3 mm pour les calibres 100-200 A du plan. Le chiffre de famille marchand ne remplace pas le dessin.
- Couleur : boîtier **noir**, marquage de calibre **jaune** ; « yellow » n'implique pas un boîtier entièrement jaune.
- Support : les cotes fabricant donnent **largeur 27,3 / hauteur 24,9**, malgré les permutations dans certaines listes marchandes. Les variantes avec pattes sont différentes.
- Courant : 200 A est une capacité du support ; 60 A est un calibre de fusible ; 40 A est une enveloppe thermique proposée des moteurs. Ces trois nombres n'imposent pas le courant réel.
- Temporisation : un fusible 60 A peut laisser passer 120 A pendant 3 à 100 s selon son tableau. La coordination avec fils et relais ne se déduit pas du seul calibre.
- CAO officielle : Littelfuse propose un téléchargement après formulaire de coordonnées. **Aucun formulaire ni message n'est envoyé** ; les modèles livrés sont des reconstructions documentées, pas des fichiers fabricant.

## Sources principales

1. [Littelfuse MIDI 32 V, révision 2024 consultée](https://www.littelfuse.com/assetdocs/midi-32v-bolt-down-series-data-sheet?assetguid=b55e8034-180d-40f6-a0a7-bebc2d4a94f5).
2. [Révision 2021 archivée via Farnell/IHS](fusible-60a/notices/Littelfuse-MIDI-32V-revision-2021.pdf), pages 1-2.
3. [Plan et fiche du support, original via TME](https://www.tme.eu/Document/751067cde59f8870ba92d17db0ce52da/04980900ZXT.pdf), édition 2008.
4. [Catalogue Littelfuse 2012 archivé](porte-fusible/notices/Littelfuse-MIDI-498-plan-catalogue-2012.pdf), PDF page 164 / page imprimée 159.
5. [Fiche ancienne du fusible, original via TME](https://www.tme.eu/Document/c2a31dbed623c79f9b3491c387e36665/littelfuse_midi.pdf), ne pas mélanger ses ratings aux versions récentes.
6. [Formulaire CAO officiel Littelfuse](https://info.littelfuse.com/midi-498-series-3dmodel-landingpage).
7. [Principes de protection DC, Blue Sea Systems](https://www.bluesea.com/resources/96).

[Manifest des téléchargements, échecs et SHA256](assets.json). Les PDF d'origine sont inchangés ; la notice V3 est un document du projet distinct.
