> **M1P :** cuivre actualis? selon le PCB,70 microm?tres nominaux ; pistes alimentation0,40 / signaux0,20 ; vias0,80/0,40 et parois20 microm?tres. Le substrat est perc? pour tous les vias ; la pile cuivre/substrat repr?sente1,6 mm fini. Corps et couleurs restent reconstruits, cotes TI non certifi?es.

# Modèles STEP M1

| Modèle | Usage |
| --- | --- |
| [Porteuse détaillée](porteuse-surveillance-2s-m1-detaillee.step) · [aperçu](porteuse-surveillance-2s-m1-detaillee.png) | PCB 140 x 75, perçages, vrais tracés KiCad, plages et fûts ; corps de composants reconstruits au nominal |
| [Ensemble avec gabarits](ensemble-surveillance-2s-m1-gabarits.step) · [aperçu](ensemble-surveillance-2s-m1-gabarits.png) | Porteuse allégée pour l'implantation ; cadres bleus réservés aux EVM et brun au Pololu ; **ce sont des volumes de réservation, pas les modèles réels de ces cartes** |
| [Trois AC03 100 ohms](resistances-mesure-3x-ac03-100ohm.step) · [aperçu](resistances-mesure-3x-ac03-100ohm.png) | Géométrie nominale des résistances de mesure au pack ; pattes droites non coupées |

Toutes les géométries sont des reconstructions V3, pas des CAO fabricant. La carte suit son routage vérifié ; cuivre 35 micromètres supposé, profil des raccords de pistes et détails de boîtiers approximés. Couleurs, inscriptions, petits congés et contacts non cotés sont estimés. Pas d'électronique interne inventée. Pas de câbles coupés ou de faisceau partiellement représenté : les faisceaux sont absents et leurs interfaces sont documentées.

Le modèle d'ensemble avec gabarits utilise une porteuse simplifiée sans les pistes, plages et fûts métallisés : les volumes extérieurs des composants et les fixations sont conservés. Utiliser cette version légère pour l'implantation du châssis ; la version détaillée garde le cuivre visible pour examiner la carte.

CadQuery/OCP : réimport STEP, validité, nombre de solides, volumes, enveloppes et présence des couleurs. [Provenance](provenance.json). FreeCAD : import indépendant en mode sans interface, validité, fermeture des solides et comparaison des enveloppes ; [résultats](validation-freecad.json). Aucun essai dans l'interface FreeCAD/CAD View ni mesure matérielle revendiqué.

**Réservation 140 x 75 x 30 pour porteuse + modules seulement**, hors FAUX/support, résistances au pack et faisceaux. Cotes TI et supports à confirmer avant châssis. Le fichier le plus utile pour examiner la géométrie réelle du projet est la porteuse détaillée ; l'ensemble avec cadres sert à réserver la place des modules.
