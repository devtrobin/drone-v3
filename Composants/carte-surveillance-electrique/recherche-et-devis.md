# Recherche, achat, avis et devis - 15 octobre 2026

## Choix et alternatives examinées

TPS3700EVM-114 : schéma, BOM, routage et procédure publics, seuils analogiques autonomes, pas de microcontrôleur. L'adaptation des résistances 0603 est nécessaire ; le module de 12 V n'est pas directement compatible. Les alimentations isolées permettent une mesure des cellules sans retour par D- ni charge des cellules par les optocoupleurs.

INA219 et INA260 : utiles pour des mesures de bus, mais ne donnent pas à eux seuls une protection autonome des deux cellules ; leurs shunts usuels ne conviennent pas au courant commun d'étude. ADS1115 seul : mesure numérique possible, mais pas de chaîne de coupure indépendante complète. MAX17048 : une cellule, pas le pack 2S. BQ76905EVM : vrai moniteur 2-5S, intéressant pour une version avec mesures numériques et détection de fils ouverts, mais reconfiguration des FET/masse et du firmware nécessaire. CellLog 8S : fonctionnalités proches du besoin, offre ProgressiveRC consultée marquée épuisée. Pololu S9V11F3S5CMA : coupure UV existante, mais hystérésis d'environ 14 % et quatre modules pour deux seuils par cellule ; moins adapté aux seuils proches de notre première étude. Aucun BMS 2S générique sans documentation de seuils, de référence de masse et de courant n'est substitué à la chaîne de puissance R2.

## Achat et coût

| Référence | Qté | Prix constaté / état | Achat |
| --- | ---: | --- | --- |
| TPS3700EVM-114 | 2 | Prix et disponibilité France à confirmer ; page TI contient des états de stock contradictoires et demande connexion | [TI](https://www.ti.com/tool/TPS3700EVM-114), [DigiKey France](https://www.digikey.fr/fr/products/detail/texas-instruments/TPS3700EVM-114/3182032) |
| TMR 1-0511 | 2 | 9,28 EUR HT / pièce dans catalogue RS consulté ; 18,56 HT / environ 22,27 TTC à 20 %, hors port | [RS 781-3178](https://fr.rs-online.com/web/p/convertisseurs-dc-dc/7813178), [TME](https://www.tme.eu/fr/details/tmr1-0511/convertisseurs-dc-dc/traco-power/tmr-1-0511/) |
| Pololu 2831 D24V10F5 | 1 | 12,95 USD fabricant ; stock et livraison France non établis, commandes différées possibles | [Pololu](https://www.pololu.com/product/2831) |
| Semi-conducteurs, passifs, connecteurs, FAUX/support, PCB | Selon BOM | Panier distributeur et coût fabrication à chiffrer, aucune valeur inventée | Voir selection.json et nomenclature.csv |

Pas de total TTC global vérifié : monnaies, ports et lignes non chiffrées ne sont pas additionnés artificiellement. Aucun achat effectué. Recherche Amazon.fr sur les références exactes : aucune offre française exacte et vérifiable trouvée. Les modules spécialisés sont proposés chez leurs fabricants/distributeurs, sans inventer d'ASIN. Le devis est donc **partiel**.

## Sources techniques et retours

- [TI EVM](https://www.ti.com/tool/TPS3700EVM-114), [guide SLVU683A](https://www.ti.com/lit/pdf/SLVU683), [fiche TPS3700 Rev G](https://www.ti.com/lit/ds/symlink/tps3700.pdf).
- [TI E2E : réglage R1/R2/R3](https://e2e.ti.com/support/power-management-group/power-management/f/power-management-forum/1540899/tps3700evm-114-r1-r2-r3-value) : réponse TI orientant vers le calculateur de ponts ; pas un essai du robot.
- [TI E2E : limite des sorties](https://e2e.ti.com/support/power-management-group/power-management/f/power-management-forum/1570835/tps3700-higher-output-voltage-will-damage-chip) : ne pas dépasser la plage de sortie du circuit. Ici sorties locales autour de 5 V, isolées du Pi.
- [TRACO TMR 1](https://www.tracopower.com/tmr1-datasheet) : fiche récupérée datée du 2 juillet 2026, pas les anciens résumés des marchands ; courant à vide typique 40 mA par module, brochage p.4 et absence de charge minimale.
- [Pololu 2831](https://www.pololu.com/product/2831), schéma public et caractéristiques du 5 V ±4 %.
- [Vishay AC](https://www.vishay.com/docs/28730/ac_ac-at_ac-ni.pdf), [TNPW](https://www.vishay.com/docs/28758/tnpw_e3.pdf), VOS618A et notices de logique archivées.

Aucun avis utilisateur ou essai YouTube vérifié sur cet ensemble précis n'a été trouvé. Aucune note ou validation thermique déduite de retours d'un autre module. Les fichiers assets*.json indiquent les téléchargements réussis, empreintes et erreurs. Le ZIP Gerber TI SLVC413 a renvoyé HTTP 401 ; les vues de routage du PDF restent disponibles, mais aucune dimension exacte d'EVM n'en est certifiée.
