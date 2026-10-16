<!-- prototype-m1p -->
> **M1P - porteuse libérée pour fabrication de prototype sur banc limité uniquement.** [Fabrication et fichiers](fabrication/README.md), [coordination chiffrée](verification/coordination-protections.md), [protocole B00-B14](verification/banc-essais.md), [registre](verification/liberation-prototype.json). Aucun essai matériel effectué. La connexion véhicule/LiPo n'est pas libérée. [Cotes TI](modules/cotes-ti.md) : pas2,54 exact ; contour relevé, cotes mécaniques exactes encore indisponibles.
<!-- /prototype-m1p -->

# Carte de surveillance électrique 2S - M1

15 octobre 2026. **Dossier de conception de prototype, non acheté, non fabriqué, non testé.**

Choix : **deux Texas Instruments TPS3700EVM-114**, alimentés par **deux Traco TMR 1-0511 isolés**, et un **Pololu D24V10F5 2831** pour leur 5 V auxiliaire. Le Raspberry Pi 5 reste la seule carte de commande. Une carte porteuse regroupe alimentation, optocoupleurs, logique OFF et connecteurs ; elle ne porte aucun courant moteur ou courant d'alimentation du Pi.

Les modules TI existent déjà, avec schéma et routage constructeur. Ils ne sont pas prêts à brancher sur une LiPo 2S : remplacer R1/R2/R3 sur chaque module, régler les cavaliers et réaliser les liaisons indiquées. Ce compromis évite de redessiner les comparateurs et les convertisseurs, tout en gardant une protection par cellule indépendante de Linux. Coût et volume sont supérieurs au premier concept entièrement intégré.

| Livrable | Accès |
| --- | --- |
| Architecture, raccordements et limites | [Intégration](integration.md) |
| Adaptation exacte des modules | [Réglages](modules/configuration.md) |
| Notice illustrée | [PDF](notices/notice-carte-surveillance-v3.pdf) |
| Schéma et routage éditables | [Projet KiCad](KiCad/README.md) |
| Modèles STEP, provenance et réservations | [CAO](3D/README.md) |
| Sources, achats, avis et devis | [Recherche](recherche-et-devis.md) |
| Calculs et hypothèses | [JSON](calculs.json) |
| Nomenclature | [Sélection](selection.json), [CSV porteuse](KiCad/nomenclature.csv) |
| Procédure de vérification | [Essais](verification/essais.md) |

**Avertissement typique 3,560 V/cellule ; coupure typique 3,347 V/cellule.** Les tolérances et l'hystérésis sont calculées séparément. Un intervalle de tension ne garantit pas un délai d'extinction Linux. WARN est maintenant **actif à l'état haut** : sous-tension ou perte du signal lumineux. L'ancien dossier TLV6700 reste une archive et ne doit plus définir le câblage actif.

Carte porteuse : **140 x 75 x 1,6 mm**. Réservation porteuse + modules : **140 x 75 x 30 mm**, hors FAUX/support, résistances au pack, fiches et courbures de câble. Les EVM sont représentés par des gabarits conservateurs de 60 x 60 mm ; leurs dimensions exactes et leurs supports restent à confirmer. Cette réservation sert au travail d'implantation, pas à percer le châssis définitif.

La protection auxiliaire FAUX et les trois résistances au départ de l'équilibrage font partie de l'ensemble. **La prise d'équilibrage protégée est réservée à la surveillance ; jamais au chargeur.** Les confirmations de coordination DC de l'audit alimentation R2 restent ouvertes. Appliquer les conditions M1P pour fabriquer un prototype et le mettre sous tension au banc ; la cible v?hicule reste non lib?r?e.

[Cotes et pièces extérieures](cotes.md) · [Nomenclature complète d’assemblage](nomenclature-assemblage.csv) · [Contrôles KiCad](verification/controle-kicad.json) · [Contrôle indépendant FreeCAD](3D/validation-freecad.json).
