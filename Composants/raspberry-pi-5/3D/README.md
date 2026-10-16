# Raspberry Pi 5 : STEP et versions de travail

Mis à jour le **13 octobre 2026** après signalement d'une ouverture impossible du STEP complet dans FreeCAD et CAD View. Le matériel retenu reste la **Pi 5, 4 Go** ; la variante mémoire et la révision exacte du modèle constructeur ne sont pas certifiées.

## Quel fichier ouvrir ?

| Fichier | Usage |
| --- | --- |
| [Encombrement simplifié](raspberry-pi-5-encombrement-simplifie.step) | Le plus petit fichier, à ouvrir en premier si les autres bloquent. Pièces principales représentées par leurs boîtes d'encombrement et couleurs. Les trous, courbes et cavités sont absents : ce fichier sert au placement, pas à la fabrication. |
| [Pièces principales, formes exactes](raspberry-pi-5-implantation-legere.step) | Environ 51 Mo, 95 pièces. Les formes des pièces retenues sont conservées ; petits éléments et graphismes omis. Plus détaillé que le modèle d'encombrement, mais encore lourd. |
| [Officiel sans graphismes](raspberry-pi-5-4go-ultra-detaille.step) | Environ 78 Mo. Le chemin historique est conservé, mais son contenu est désormais la variante officielle **sans graphismes de surface**, identique au membre `rpi-5b_no_graphics.step` de son archive. |
| [Officiel avec graphismes](raspberry-pi-5-officiel-avec-graphismes.step) | Ancien fichier de 142 Mo, déplacé sans modification. Référence détaillée avec graphismes ; import potentiellement long. |
| [ZIP sans graphismes](raspberry-pi-5-officiel-sans-graphismes.zip) | Source officielle intégrale et licence. |
| [ZIP avec graphismes](raspberry-pi-5-officiel-avec-graphismes.zip) | Source officielle intégrale et licence, environ 25 Mo. |
| [Dessus](vue-dessus.png), [dessous](vue-dessous.png), [perspective](vue-isometrique.png), [connecteurs](vue-connecteurs.png) | Aperçus du modèle **complet avec graphismes**, pas du modèle simplifié. |
| [Aperçu d'encombrement](vue-encombrement-simplifie.png) | Vue des boîtes approximatives du petit STEP, explicitement distinguée des aperçus détaillés. |
| [Provenance du modèle complet](provenance.json) | Empreintes et inventaire du modèle avec graphismes. |
| [Validation des versions de travail](validation-versions-travail.json) | Contrôles de réimport du STEP léger, inventaire des éléments conservés et omis. |
| [Licence originale](LICENSE-constructeur.txt) | MIT, Raspberry Pi Ltd 2026. |

## Vérification et limites

Le STEP complet avec graphismes est identique octet par octet à la source constructeur. Il contient **3 467 solides et 83 152 faces** et a passé la validation géométrique OpenCascade. Cela ne constituait pas un essai dans FreeCAD ou CAD View : l'ancienne mention « directement ouvrable » était trop affirmative. La cause précise du problème signalé dans ces logiciels n'est pas établie.

La variante officielle sans graphismes s'importe ici avec OpenCascade en environ **47 à 70 secondes**. Elle contient **2 689 solides et 45 689 faces** et conserve les composants et couleurs natifs sans les graphismes de la variante complète. Les ouvertures dans les interfaces de FreeCAD et de CAD View restent à confirmer sur le poste utilisateur.

Le modèle d'implantation dérive de cette variante. Il conserve les éléments contenant des solides, dont le plus grand côté d'enveloppe atteint 4 mm et dont le volume d'enveloppe atteint 1 mm³. Les formes retenues ne sont pas remplacées par des boîtes. Cette sélection omet de petits composants et certains petits contacts : consulter les modèles officiels pour un dégagement local précis. Le registre donne toutes les omissions, la taille du fichier et les contrôles de validité et d'enveloppe après réimport, dont l'écart aux limites globales du modèle officiel lié aux omissions. La variante d'encombrement remplace les mêmes éléments par des boîtes et perd donc les détails locaux, notamment les trous de fixation.

Enveloppe totale, ports compris : **88,50 × 57,63 × 18,98 mm**. Le PCB a une cote de référence de **85 × 56 mm**. Comparer les modèles et le [plan mécanique](../notices/Raspberry-Pi-5-plan-mecanique.pdf) à la carte réelle avant fabrication définitive.

Le STEP des pièces principales a passé le réimport et la validation : **95 solides, 10 216 faces**, écart de placement inférieur à 10⁻⁴ mm par rapport aux pièces retenues. Les détails omis réduisent certaines limites d'enveloppe d'au plus **0,45 mm** par rapport au modèle officiel. Le fichier d'encombrement de **1,67 Mo** a également passé le réimport et le contrôle de ses 95 solides. Les deux modèles simplifiés ne suffisent donc pas pour fixer des jeux au dixième de millimètre.

Les micro-pistes sous le vernis et certaines inscriptions de fabricants de puces ne sont pas représentées dans la CAO complète. Aucun circuit interne ni netlist n'est inventé. Les couleurs sont celles de la CAO, pas des textures photographiques. La licence ne garantit ni l'exactitude ni la correspondance avec la dernière révision.

## Git et reproduction

**L'ancien chemin `raspberry-pi-5-4go-ultra-detaille.step` n'est plus ignoré.** Le STEP sans graphismes de 78 Mo et le STEP léger peuvent être suivis directement dans Git. Seule la copie avec graphismes de 142 Mo reste ignorée ; son ZIP intégral est conservé pour la reconstruire. Aucun commit ni envoi du dépôt n'a été effectué.

Depuis la racine de `drone-v3`, extraire les deux sources sans dépendance CAO :

```powershell
python tools/extract_pi5_sources.py
```

Régénérer le modèle d'implantation avec l'environnement CadQuery/OpenCascade du projet :

```powershell
tools/temp/cad-env/Scripts/python.exe tools/prepare_pi5_working_step.py
```

Le [script du modèle complet](../../../tools/prepare_pi5_step.py) conserve la préparation XCAF et les aperçus avec graphismes. Les dépendances et caches de `tools/temp` restent ignorés.

Source : [portail constructeur Pi 5](https://pip.raspberrypi.com/categories/892-raspberry-pi-5), variantes « No Graphics small file » et « With Graphics large file », mises à jour au 11 juin 2026. URLs et empreintes dans les registres locaux.

[Retour à la fiche composant](../README.md).
