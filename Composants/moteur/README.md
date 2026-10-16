<!-- alimentation-r2 -->
> **Sélection active révisée le 15 octobre 2026.** Moteurs et ESC conservés. Fils d’usine 16 AWG non remplacés à l’aveugle. Deux fusibles rapides 20 A, 15 A continus par départ pour le dimensionnement ; accepter le lot et tester le démarrage, le freinage et la thermique avant roulage.
> [État électrique courant](../verification-alimentation/README.md) · [Raccordements](../verification-alimentation/integration.md). Les références différentes dans les documents ci-dessous sont historiques. Qualification matérielle non réalisée ; confirmations restantes explicites.
<!-- /alimentation-r2 -->

# Moteur — Hobbywing QuicRun 2435SL G3, 4 500 KV

**Modèle retenu par l'utilisateur pour sa compacité ; non acheté.** Deux moteurs et deux variateurs sont retenus pour les deux roues arrière ; les deux roues avant non motrices assurent la direction. La transmission reste à dimensionner.

## Documents du dossier

- [Notice officielle du moteur, PDF](notices/QuicRun-2435SL-G3-notice-constructeur.pdf).
- [Notice officielle du variateur G2, PDF](notices/QuicRun-WP16BL30-G2-notice-constructeur.pdf).
- [Index des notices et sections utiles](notices/README.md).
- [Recherche technique : ambiguïtés, retours utilisateurs et essais à prévoir](recherche-technique.md).
- [Photos de référence et crédits](photos/README.md).
- [Sources, caractéristiques structurées et empreintes des fichiers](sources.json).

Les notices sont conservées dans leur version anglaise officielle, sans modification. La fiche et la recherche ci-dessous sont en français.

- [Modèles 3D détaillés du moteur et du variateur — deux fichiers STEP colorés](3D/README.md).

## Offre de référence

- [Kit Amazon.fr — ASIN B0FM6D1F1W](https://www.amazon.fr/dp/B0FM6D1F1W), variante **2435SL 4500KV**.
- Contenu annoncé : **un moteur et un variateur QuicRun WP16BL30 G2**. Ce n'est pas un kit complet du véhicule.
- Prix relevé le **12 octobre 2026** : **66,34 € TTC par kit**, livraison standard gratuite et frais d'importation inclus affichés.
- Vendeur / expéditeur : Amazon US ; offre en stock lors de la consultation. Prix et disponibilité à revalider avant commande.
- Batterie, chargeur, quatre roues, moyeux, réduction, supports et mécanisme de direction avant à ajouter. Carte de programmation séparée ; réglage possible par le bouton SET du variateur.

## Caractéristiques constructeur

| Donnée | Valeur publiée |
| --- | --- |
| Type | Brushless sans capteur, rotor quatre pôles |
| Régime par volt | 4 500 KV, régime à vide ; pas une puissance |
| Batterie compatible moteur | LiPo 2–3S ; scénario initial V3 : 2S, 7,4 V nominal |
| Corps moteur | Ø24 × 36 mm |
| Masse moteur | 61,2 g |
| Axe | Ø2 mm, longueur sortie 12 mm |
| Fixation | Entraxes 14, 16 et 17 mm selon les trous ; M2,5 / M3, profondeur des trous 4 mm |
| Courant à vide publié | 2,1 A ; conditions de mesure non précisées dans le tableau, pas une consommation de roulage |
| Variateur du kit | WP16BL30 G2, 30 A continus annoncés ; LiPo 2–3S |
| Fonctions du variateur | Marche avant, freinage proportionnel et marche arrière selon configuration |
| Encombrement variateur | 33,4 × 26,8 × 15,1 mm ; 38,5 g avec fils et connecteurs |
| BEC du variateur | 6 / 7,4 V : ne pas l'utiliser directement comme alimentation USB 5 V |

Le courant BEC est contradictoire : **1,5 A dans la notice du 11 mars 2025**, **2 A dans la fiche constructeur actuelle**. La [recherche technique](recherche-technique.md) conserve cet écart ; la variante livrée devra être contrôlée.

La mention **15 A** du champ générique Amazon ne définit ni un courant minimal obligatoire, ni la consommation moyenne du véhicule. Le courant dépend de la charge, du régime et de la commande. Dimensionner les pointes et mesurer les Wh consommés en roulage avec vidéo active.

## Architecture retenue : deux moteurs arrière et direction avant

Instruction utilisateur : **deux moteurs à l'arrière et aucun à l'avant ; les deux roues avant servent uniquement à la direction**. La bille avant est abandonnée.

Chaque roue arrière possède son **moteur, son variateur et sa réduction**. Un variateur brushless sensorless standard n'est pas prévu pour commander deux moteurs indépendamment. Le [servo et les biellettes](../direction-et-transmission/README.md) sont documentés ; la géométrie finale du train avant reste à établir.

La quantité de conception est **deux kits moteur + variateur** ; aucun achat n'a été effectué. La coordination des vitesses arrière en virage reste à définir : les deux roues parcourent des distances différentes, et une commande identique ne garantit pas des vitesses adaptées.

| Scénario au prix relevé | Coût moteur(s) + variateur(s) |
| --- | ---: |
| Un kit : un moteur, un variateur | 66,34 € |
| Deux kits : architecture retenue, prix historique à revérifier | 132,68 € |

Les axes moteur ne serviront pas directement d'axes porteurs des roues. La [réduction d'étude](../transmission-arriere/README.md) utilise deux étages par roue, i=7,59375. Compatibilité d'appairage, charge radiale du petit pignon et performances en charge restent à vérifier ; les axes de sortie et supports sont à fabriquer.

Les 40 km/h et les autonomies restent des objectifs. Le train avant, l'adhérence, les vibrations et la stabilité doivent être vérifiés avant de valider cette architecture à grande vitesse.

## Sources et prochaines informations

- [Notice officielle moteur](https://www.hobbywing.com/en/uploads/file/20230426/edf26f2966fcb92587538360159162a2.pdf).
- [Fiche officielle variateur](https://www.hobbywing.com/en/products/quicrun-wp-16bl30-g2).
- [Notice officielle variateurs G2](https://www.hobbywing.com/en/uploads/file/20250320/b9addd01e22cb5be3ff28e6f25db2a5f.pdf).
- [Registre des sources et du choix](sources.json).

À déterminer : masse et adhérence réelles, validation de réduction, fixation, batterie, consommation, freinage et arrêt sur perte de liaison. Deux moteurs et quatre roues HobbyPark de 63 mm sont retenus. Les modèles 3D existants sont des reconstructions documentées ; aucun essai matériel n'est encore réalisé pour ce moteur.

[Retour à l'index des composants](../README.md).
