# Recherche, alternatives et retours utilisateurs

Recherche du13 octobre2026. La proposition reste une étude ; les recherches Amazon.fr ciblées n’ont pas permis d’identifier une offre vérifiable réunissant toutes les fonctions. Les liens ci-dessous sont des recherches, pas des ASIN confirmés ni un panier validé.

| Solution examinée | Constat technique | Décision |
| --- | --- | --- |
| ServoCity Low Voltage Cutoff Switch |2S: coupure fixe6 V pour le pack,15 A continus à6 V ; pas de mesure individuelle ni alerte Pi documentée | Ecarté pour cette fonction |
| BMS génériques2S | Références/courants et seuils hétérogènes ; communication et extinction Linux rarement documentées | Ne pas assimiler un marquage commercial à une validation |
| Junsi CellLog8S | Notice complète, mesure2-8S et sortie collecteur ouvert ; offre Amazon actuelle non établie et disponibilité ancienne incertaine | Référence de comparaison, pas achat retenu |
| Enepaq TinyBMS s516 actuel | Constructeur:4-16S,9-75 V ; incompatible avec notre2S | Ecarté malgré des fiches anciennes ambiguës |
| Chargery BMS8T | Pour2-3S, la notice V4.2 exige une alimentation externe15-30 V ; contacteur séparé | Ecarté pour l’intégration compacte |
| Pololu2813 sur tous les moteurs |16 A correspond à150°C et non àune limite froide ;6 A à55°C selon essai fabricant12 V | Ecarté de la puissance moteur ; retenu sur la branche Pi |
| Crydom D1D100 | Sortie DC1-72 V recommandés,100 A avec conditions thermiques ; commande3,5-32 V ; datasheet et plan | Référence d’étude pour la branche moteur, prix et dissipateur àfinaliser |

Sources des exclusions : [ServoCity](https://www.servocity.com/low-voltage-cutoff-switch/), [CellLog constructeur](https://www.hillrc.com/UploadFiles/CellLog_8S.pdf), [TinyBMS constructeur](https://enepaq.com/product/battery-management-system-bms-150a-set-tinybms-s516/), [Chargery constructeur](https://www.chargery.com/doc/Chargery_BMS8T_specification_V4.2.pdf), [Pololu](https://www.pololu.com/product/2813), [Sensata](https://www.sensata.com/sites/default/files/a/sensata-1-dc-series-d1d-dc-output-panel-mount-datasheet.pdf).

## Avis et expériences

- [Pololu, extinction d’un Pi,2021](https://forum.pololu.com/t/raspberry-pi-can-it-turn-itself-off-with-the-mini-pushbutton-power-switch/21371) : un utilisateur rapporte que le passage d’une polarité basse àune polarité haute de `gpio-poweroff` a permis l’arrêt avec son interrupteur Mini. Retour sur une autre carte et une ancienne génération de Pi ; pas une validation du2813 avec Pi5.
- [Pololu2813, fluctuation d’alimentation,2017](https://forum.pololu.com/t/problem-with-pushbutton-power-switch-item-2813-auto-on-with-power-fluctuation/13660) : signalement d’un allumage inattendu pendant une chute d’alimentation automobile. Témoignage individuel qui motive un essai des transitoires et du redémarrage ; ne pas généraliser àtous les exemplaires.
- Aucun avis n’existe pour notre carte V3 non fabriquée. Aucun banc d’essai utilisateur attribuable au D1D100 dans un robot2S équivalent n’a été identifié. Les courbes constructeur restent la base du dimensionnement, sans prétendre valider notre montage.

## Achat et coût

[Recherche Amazon Pololu2813](https://www.amazon.fr/s?k=Pololu+2813+HP), [Recherche Amazon CrydomD1D100](https://www.amazon.fr/s?k=Crydom+D1D100), [Recherche Amazon TLV6700](https://www.amazon.fr/s?k=TLV6700). **ASIN, vendeur, livraison, prix euro et stock non confirmés.** Les photos Pololu et sa CAO native ne prouvent pas la disponibilité Amazon. Fournisseurs constructeur/distributeurs àcomparer si Amazon reste la préférence.

La carte V3 exige des circuits précis, passifs0,1 %, connecteurs et fabrication. Le relais industriel et son refroidissement peuvent rendre la solution coûteuse. Aucun coût final ni respect des200 euros n’est annoncé. Une optimisation ultérieure peut remplacer l’étage industriel par une carte MOSFET conçue et qualifiée, avec ses propres contraintes ; ce remplacement n’est pas réalisé ici.

## Cotes et fidélité

Pololu: STEP officiel commun2812/2813, inchangé. Crydom: enveloppe57,3×44,5×22,6 mm et fixation reprises du plan fabricant, détails extérieurs estimés. Carte V3:54×32×1,6 mm choisis pour l’étude, quatre trousØ2,2 aux entraxes48×26. Les pistes de ce modèle ne sont pas le plan électrique. Aucun circuit interne de relais ni carte commerciale imaginaire n’est dessiné.
