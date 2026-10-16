# Modèles 3D des fixations du Pi 5

**15 STEP colorés en millimètres**, reconstruits depuis les longueurs publiées et les photos du kit Ewwtrey noir. Ni CAO native de ce kit, ni modèle issu de mesures physiques. Les profils intérieurs/extérieurs sont des hélices réelles ; les détails fins estimés sont tracés dans [cotes.md](../cotes.md), [catalogue.json](catalogue.json) et chaque JSON voisin.

| Modèle STEP | Aperçu | Solides | Taille |
| --- | --- | ---: | ---: |
| [Entretoise MF M2.5 | 6+6 mm](entretoise-mf-m2-5-6-plus-6.step) | [entretoise-mf-m2-5-6-plus-6.png](entretoise-mf-m2-5-6-plus-6.png) | 1 | 894 Ko |
| [Entretoise MF M2.5 | 8+6 mm](entretoise-mf-m2-5-8-plus-6.step) | [entretoise-mf-m2-5-8-plus-6.png](entretoise-mf-m2-5-8-plus-6.png) | 1 | 1013 Ko |
| [Entretoise MF M2.5 | 10+6 mm](entretoise-mf-m2-5-10-plus-6.step) | [entretoise-mf-m2-5-10-plus-6.png](entretoise-mf-m2-5-10-plus-6.png) | 1 | 1049 Ko |
| [Entretoise MF M2.5 | 15+6 mm](entretoise-mf-m2-5-15-plus-6.step) | [entretoise-mf-m2-5-15-plus-6.png](entretoise-mf-m2-5-15-plus-6.png) | 1 | 1049 Ko |
| [Entretoise MF M2.5 | 20+6 mm](entretoise-mf-m2-5-20-plus-6.step) | [entretoise-mf-m2-5-20-plus-6.png](entretoise-mf-m2-5-20-plus-6.png) | 1 | 1049 Ko |
| [Entretoise FF M2.5 | 6 mm](entretoise-ff-m2-5-6.step) | [entretoise-ff-m2-5-6.png](entretoise-ff-m2-5-6.png) | 1 | 571 Ko |
| [Entretoise FF M2.5 | 10 mm](entretoise-ff-m2-5-10.step) | [entretoise-ff-m2-5-10.png](entretoise-ff-m2-5-10.png) | 1 | 916 Ko |
| [Entretoise FF M2.5 | 15 mm](entretoise-ff-m2-5-15.step) | [entretoise-ff-m2-5-15.png](entretoise-ff-m2-5-15.png) | 1 | 1248 Ko |
| [Entretoise FF M2.5 | 20 mm](entretoise-ff-m2-5-20.step) | [entretoise-ff-m2-5-20.png](entretoise-ff-m2-5-20.png) | 1 | 1394 Ko |
| [Vis nylon M2.5 x 8 | empreinte cruciforme](vis-cruciforme-m2-5-8.step) | [vis-cruciforme-m2-5-8.png](vis-cruciforme-m2-5-8.png) | 1 | 609 Ko |
| [Vis nylon M2.5 x 12 | empreinte cruciforme](vis-cruciforme-m2-5-12.step) | [vis-cruciforme-m2-5-12.png](vis-cruciforme-m2-5-12.png) | 1 | 812 Ko |
| [Vis nylon M2.5 x 20 | empreinte cruciforme](vis-cruciforme-m2-5-20.step) | [vis-cruciforme-m2-5-20.png](vis-cruciforme-m2-5-20.png) | 1 | 1262 Ko |
| [Ecrou hexagonal nylon M2.5 | filetage interieur](ecrou-m2-5.step) | [ecrou-m2-5.png](ecrou-m2-5.png) | 1 | 311 Ko |
| [Rondelle nylon M2.5 | dimensions estimees](rondelle-m2-5.step) | [rondelle-m2-5.png](rondelle-m2-5.png) | 1 | 11 Ko |
| [Pi 5 | quatre fixations nylon | pose provisoire 10 mm](quatre-fixations-pi-5-10mm-etude.step) | [quatre-fixations-pi-5-10mm-etude.png](quatre-fixations-pi-5-10mm-etude.png) | 20 | 8116 Ko |

Le modèle d'assemblage dispose **20 pièces aux quatre points de fixation du Pi**, sur rectangle de référence 58 x 49 mm. Le PCB et le châssis sont volontairement absents ; les espaces qu'ils occuperaient correspondent à des épaisseurs provisoires. La hauteur 10 mm reste un exemple : **châssis conçu en dernier** et hauteur définitive à décider alors.

Noir nylon, chanfreins et empreintes cruciformes, formes hexagonales d'après la photo de détails. Le fournisseur ne publie pas les profondeurs internes et les cotes fines. Aucun plan de production ou fichier de jauge n'est revendiqué.

Génération : tools/build_pi_mount_step.py. Réimport CadQuery, couleurs STEP, solides et volumes contrôlés ; [contrôle FreeCAD indépendant](validation-freecad.json) sans interface graphique. Aucun essai dans FreeCAD GUI ou CAD View déclaré, aucune qualification mécanique. Les STEP du Pi, du cooler et du GPIO sont inchangés.
