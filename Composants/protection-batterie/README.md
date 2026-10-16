<!-- surveillance-m1 -->
> **15 octobre 2026 - ce concept TLV6700 est historique.** La [surveillance M1 à modules existants](../carte-surveillance-electrique/README.md) définit désormais les seuils, les reprises EVM, les protections fines et le routage. WARN M1 est actif haut ; ne pas reprendre ici la polarité de l’ancien concept. Les Pololu 2813 et D1D100 restent dans la chaîne R2.
<!-- /surveillance-m1 -->

<!-- alimentation-r2 -->
> **Sélection active révisée le 15 octobre 2026.** Modifier l’alimentation de la logique indépendante : depuis le positif après F0 mais avant ED80, à travers une protection auxiliaire à dimensionner, retour vers D−. B0/B1/B2 ne rejoignent que les voies locales isolées ; aucune masse de puissance par l’équilibrage.
> [État électrique courant](../verification-alimentation/README.md) · [Raccordements](../verification-alimentation/integration.md). Les références différentes dans les documents ci-dessous sont historiques. Qualification matérielle non réalisée ; confirmations restantes explicites.
<!-- /alimentation-r2 -->

# Surveillance et coupure de batterie - V3

**Etude préliminaire du 13 octobre 2026. Non achetée, non fabriquée, non testée.** Aucun module Amazon vérifiable réunissant mesure par cellule, alerte Pi, coupure indépendante et courant des deux moteurs n’a été identifié. Le panier français et le coût total restent ouverts.

La proposition comporte trois parties, chacune dans son dossier :

| Partie | Choix d’étude | Rôle |
| --- | --- | --- |
| [Surveillance 2S](surveillance-2s/README.md) | Carte analogique V3, 2 TLV6700, 4 optocoupleurs et logique | Surveiller chaque cellule ; avertir le Pi puis demander la coupure sans logiciel |
| [Interrupteur Pi](interrupteur-pi/README.md) | Pololu 2813 HP | Couper la branche du régulateur Pi et la commande du relais moteurs |
| [Coupure moteurs](coupure-moteurs/README.md) | Sensata/Crydom D1D100, version à vis | Porter le courant des deux ESC ; refroidissement à dimensionner |

La carte de surveillance est **une conception à fabriquer**, pas une carte du commerce. Son STEP représente une implantation d’étude ; les pistes ne constituent pas un routage validé. Le choix du relais industriel est une référence techniquement documentée, avec un coût et un encombrement à comparer avant achat. Ce choix ne garantit pas le budget initial de 200 euros.

Seuils typiques calculés en descente : **avertissement 3,566 V/cellule**, **coupure 3,353 V/cellule**. Ils incluent l’hystérésis du TLV6700. Les seuils exacts, les délais et le comportement sous charge restent à mesurer. Deux fenêtres de seuil distinctes permettent une extinction normale ; elles ne garantissent pas un temps fixe disponible pour l’arrêt Linux.

[Architecture et branchements proposés](integration.md), [recherche et alternatives](recherche-technique.md), [nomenclature](nomenclature.json), [calculs](calculs.json), [notice PDF du projet](notices/notice-protection-batterie-v3.pdf), [trois modèles STEP et aperçus](3D/README.md).

Les sources constructeur sont conservées sans modification, avec SHA256 dans les `assets.json` de chaque partie. La notice de projet est distincte de leurs fiches techniques. Aucune configuration ou commande n’est appliquée à une Raspberry Pi.

Suite de l'étude : le [HS251 avec une interface HSP-1](../dissipateur-relais/README.md) est proposé pour le D1D100, avec une notice et une CAO séparées. L'enveloppe de travail de 40 A au total / 40 °C d'air local reste à qualifier ; elle ne reprend pas automatiquement le calibre 100 A du relais.
