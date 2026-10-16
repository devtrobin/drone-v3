<!-- integration-r2 -->
> **Complément d’intégration du16octobre2026 :** [étudeR2](../finalisation-theorique-r2/electricite.md) avecdirection6V dédiée, enveloppe40A etinterfacePWM isolée proposée. Les conditions de qualification ci-dessous restent applicables. Les parcours hauts etleurs descentes ne sont pas encore libérés.
<!-- /integration-r2 -->

<!-- surveillance-m1 -->
> **Suite active du 15 octobre 2026 :** [carte de surveillance M1](../carte-surveillance-electrique/README.md)
<!-- /surveillance-m1 -->

# Vérification et correction de l’alimentation V3

Révision du **15 octobre 2026**. La liaison de charge du pack G1 est sélectionnée. La protection et l’alimentation Pi sont corrigées dans les dossiers. La qualification complète reste ouverte : confirmations fabricant des supports et de la coupure DC, puis essais matériels. Aucun achat, montage ou essai physique réalisé.

| Point trouvé | Correction de conception |
| --- | --- |
| S65 XT60 et pack IC5 sans cordon de charge | Beez 2B BEEC1067 XT60–EC5 annoncé pour S65 ; IC5 accepte EC5 pour la puissance. Une rallonge XH 2S dédiée est ajoutée. |
| 44 A traités comme une consommation presque validée | Ancienne hypothèse de charge, sans mesure ni limite active. Étude continue : 15 A par ESC et budget commun de 36 A ; scénario court : deux fois 20 A pendant 2 s. |
| MIDI60 / 2 kA sans défaut du pack qualifié | Proposition JLLN050.T rapide 50 A / 20 kA DC, support LFT300601C et capot. Borne de défaut conditionnelle avec le positif avant F0. |
| ATO30 sur fils d’usine ESC16 AWG | Deux KLKD020.T rapides de 20 A ; régime continu étudié de 15 A par départ. Coupure plus exigeante, à qualifier au démarrage et aux conditions réelles. |
| Pi avec peu de marge en fin de batterie | KLKD010.T en entrée et Pololu D42V55F5 / 5571 : dropout typique ≈0,25 V à 5 A, tolérance de sortie ±3 %. |
| FLRY-B limité à 70 °C | LAPP HEAT180 SiF6 mm², classe 5, résistance et rayon documentés. Pose fixe protégée et ventilée. |
| 5 A supposés parfaitement répartis dans la prise Molex | Molex réservé à neuf signaux. Deux positifs et quatre retours courts en 18 AWG soudés aux pads du connecteur Pi. |
| Masse de logique pouvant doubler le retour par l’équilibrage | Logique indépendante après F0, avant ED80, retour D− ; comparateurs de cellule et optocoupleurs locaux. Protections des voies fines au futur schéma. |
| Plage du support Pi incompatible avec 18 AWG direct | Supports L60030M1PQ à pression : 12 AWG dans les bornes 10–14 AWG ; deux WAGO221-413 supplémentaires pour passer à 18 AWG côté Pi. |

Les rails 2315, ED80, D1D100 / HS251, UD80, moteurs, servo, caméra, Pi et le pack G1 IC5 restent sélectionnés. Les fils d’usine ESC et batterie ne sont pas dessoudés.

Le positif SPMXCA510 conserve ≥85 mm de conducteur, suivi d’un **raccord TE32151 et d’une extension LAPP6 mm² de ≥120 mm avant F0**, protégée mécaniquement et isolée par ATUM8/2 au raccord. Le négatif garde une TE130191 vers D−. La cosse M5 positive disparaît. Les minimums sont des exigences du calcul, pas une longueur arbitraire à raccourcir lors de l’implantation.

[Notice PDF](notices/verification-alimentation-v3.pdf) · [raccordements](integration.md) · [calculs](calculs.json) · [sélection active](selection-active.json) · [nomenclature](nomenclature.json) · [devis](devis.md) · [qualification](protocole-qualification.md) · [sources](notices/README.md).

## Charge

G1 avec prise d’équilibrage : compatible avec chargeur classique selon Horizon. S65 en LiPo Balance 2S /5 A /4,20 V par cellule :42 W maximum contre 65 W /6 A disponibles. BEEC1067 identifié à 6,90 EUR TTC et en stock sur le SKU exact du JSON public. Contrôle des contacts, de la section et de la polarité sur le lot avant charge. Un pack G2 ne remplace pas ce G1 dans cette architecture.

## Protections, courant et échauffement

La borne calculée est d’environ **16,4 kA**, en supposant 8,4 V, cuivre à 0 °C, les deux segments positifs minimaux avant F0 et leurs sections maximales admises. Résistance interne de batterie, fil négatif, raccord et résistance du fusible sont tous exclus. Elle n’est valide que si ces segments restent inévitables pour les défauts en aval ; elle ne couvre pas un court-circuit avant F0 ni les voies fines d’équilibrage.

Le JLLN50 et son support disposent de 20 kA DC publiés. Les KLKD disposent de 50 kA DC dans le cadre UL248-14 ; leur valeur photovoltaïque UL248-19 de 10 kA est distincte. Le support de branche est recommandé pour KLKD, mais sa tenue d’association en DC doit être confirmée ; un SCCR générique AC ne suffit pas.

Les énergies KLKD publiées à 20 kA /600 V DC sont comparées aux fils comme examen préliminaire. Elles ne sont pas un maximum garanti à 8,4 V. Les courbes moyennes ne permettent pas de garantir sélectivité totale ou survie du relais. Aucun fusible ne limite instantanément le courant à son calibre ; le logiciel PWM ne mesure pas l’intensité.

Repère thermique : table Blue Sea, conducteurs libres dans l’air, isolant 105 °C, air 30 °C :10 AWG60 A,6 mm²65 A,16 AWG25 A. Appliquer un facteur de comparaison prudent 0,90 à 40 °C donne 54 /58,5 /22,5 A. C’est un repère de conception sous ces hypothèses, pas une certification du lot. La pose groupée réduit fortement ces valeurs : elle est exclue pour ces liaisons. Vérifier les isolants d’usine et les températures réelles.

**Confirmations documentaires restantes :** terminaison fine brins admise par LFT ; tenue DC de L60030M1PQ avec KLKD ; enveloppe maximale de coupure aux courants et tensions réels. Aucun de ces points n’est déclaré validé par un simple nouveau choix de référence. Les supports restent des propositions avant achat.

## Alimentation Pi

Le nouveau Pololu dispose d’un plan et d’un STEP officiels archivés. Sa sortie 4,85–5,15 V et son dropout typique plus faible améliorent la marge. Critères de réception : boucle commune≤5 mΩ, chemin d’entrée Pi≤50 mΩ, VIN≥5,8 V et4,75–5,25 V aux pads Pi à 0–5 A. Ce sont des budgets à mesurer ; les tolérances et courbes typiques seules ne prouvent pas tous les transitoires.

Molex : neuf signaux, positions de puissance vides. Deux WAGO supplémentaires reprennent les fils 12 AWG admissibles au support Pi et les fils 18 AWG côté cartes. La soudure aux pads Pi exige accès dessous, isolation et maintien, à réserver dans le châssis final. Aucun réglageEEPROM5 A appliqué avant qualification de la source.

## Performances et documents historiques

37 Wh nominaux,29,6 Wh avec 80 % utilisables **supposés**. La puissance moyenne totale doit rester≤39,47 W pour 45 min à 20 km/h,≤88,8 W pour 20 min à 40 et≤177,6 W pour 10 min à 40. À44 A constants,5 Ah donneraient seulement 6,82 min sans réserve ni pertes. Les courants de conception ne sont pas une consommation moyenne de roulage.

Les objectifs 40 km/h /10–20 min et20 km/h /45 min sont conservés. Le courant ne se déduit pas du KV ou de la vitesse seule. Le régime 15 A par ESC est une enveloppe thermique, sans limite active mise en œuvre ni résultat de roulage.

Les anciens PDF et STEP restent intacts. Assemblages avec MIDI, deux cosses CP0 ou six fils de puissance dans Molex : versions historiques. Les anciens contrôles 303 PASS décrivent leur propre version et ne valident pas cette révision. Le STEP officiel du nouveau Pololu est la référence actuelle pour ce régulateur.

Schéma/routage de surveillance, support caméra, visserie finale et châssis restent pour la phase finale demandée. Les voies fines doivent recevoir leur protection au futur schéma ; aucune carte prête à fabriquer n’est produite ici.
