# Modèles 3D des protections moteurs

**Cinq STEP, millimètres, solides nommés et couleurs.** Deux références, cinq vues et assemblages ; aucun matériel mesuré.

| Modèle | STEP | Aperçu | Taille |
| --- | --- | --- | ---: |
| Littelfuse ATO30 : fusible vert 30 A | [STEP](../fusible-30a/3D/littelfuse-0ato030-v-detaille.step) | [PNG](../fusible-30a/3D/littelfuse-0ato030-v-detaille.png) | 1.05 Mo |
| Blue Sea 5065 : support sans fusible | [STEP](../porte-fusible/3D/bluesea-5065-porte-fusible-detaille.step) | [PNG](../porte-fusible/3D/bluesea-5065-porte-fusible-detaille.png) | 1.00 Mo |
| Depart moteur : 5065 et ATO30 ferme | [STEP](./ensemble-moteur-ato30-ferme-etude.step) | [PNG](./ensemble-moteur-ato30-ferme-etude.png) | 2.07 Mo |
| Depart moteur : capot eclate | [STEP](./ensemble-moteur-ato30-ouvert-etude.step) | [PNG](./ensemble-moteur-ato30-ouvert-etude.png) | 2.07 Mo |
| Deux departs ESC independants : pose etude | [STEP](./deux-protections-moteurs-ato30-etude.step) | [PNG](./deux-protections-moteurs-ato30-etude.png) | 4.13 Mo |

Le support reprend la reconstruction 5065 de la branche Pi : socle, capot creux avec oreille, joint orange, contacts femelles approchés et deux fils rouges continus. Fils et brins de longueur illustrative ; absence de cosses et raccords. Le fusible ATO30 est vert, marqué 30 et reprend les cotes de référence fabricant.

Support, contacts et petites formes de moulage estimés ; PA66 translucide réel rendu opaque. Pas d’élément interne calibré de fusible inventé. Vue éclatée : capot Y+36. Pose double : supports X±26, sans raccord de répartition ni faisceau final.

[Cotes et limites](../cotes.md), [intégration](../integration.md), [contrôles FreeCAD sans interface](validation-freecad.json). Réimports CadQuery : validité, volumes, enveloppes, solides, couleurs et absence de chevauchement. Aucun test GUI FreeCAD/CAD View revendiqué ; fichiers hors gitignore.
