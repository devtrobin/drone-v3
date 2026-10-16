# Montage et qualification thermique

Le D1D100 reste câblé conformément à [l'étude de protection](../protection-batterie/integration.md). Le HS251 et le HSP-1 n'ajoutent aucune connexion de commande ; les fixations ne constituent pas un chemin de courant moteurs prévu.

1. Débrancher le pack et nettoyer les deux surfaces de contact, planes et sans bavures. Contrôler les taraudages #8-32 UNC, le kit fourni et la profondeur utile avant de choisir une autre longueur de vis. Ne pas substituer automatiquement des M4.
2. Identifier la variante **HSP-1** reçue. La fiche 2018 donne une version grise de 0,076 mm. Le PCN du 14 décembre 2023 décrit un matériau rose JRFT-FC200 avec deux films à retirer ; l'annexe préliminaire consultée donne 0,127 mm. Les fiches marchands mélangent parfois les révisions et même la couleur.
3. Utiliser **un seul pad, sans pâte supplémentaire**. Pour la variante rose, suivre la notice fournie avec le lot : retirer le film transparent, poser et chasser doucement les bulles, puis retirer le film bleu avant le montage du relais. Le PCN décrit un délai de 5 minutes ; son annexe préliminaire évoque une heure pour certaines conditions de pose. La procédure du lot et du fabricant doit trancher cet écart. Aucun film d'emballage ne doit rester entre les métaux.
4. Centrer les encoches et mettre les deux vis en contact avant de serrer progressivement et alternativement à **2,2 N·m**, selon les limites concordantes HS251/D1D100. Les valeurs des bornes électriques sont distinctes, voir la notice du relais.
5. Prévoir une fixation du dissipateur au châssis qui conserve l'accès aux vis et à l'air. Le fabricant recommande des ailettes et canaux verticaux pour favoriser la convection naturelle. La pose à plat dans la CAO est un repère d'intégration : elle ne valide pas une implantation enfermée ou une convection réelle. Aucun débit d'air lié à la vitesse du véhicule n'est supposé.

## Calcul de travail

Le courant est celui qui traverse le relais, **somme instantanée des deux branches ESC**. En présence d'impulsions, la dissipation résistive dépend du courant efficace : `P ≈ R × I_rms²`, et non du carré du seul courant moyen. La valeur de travail R = 0,005 Ω vient de la fiche D1D100 ; son évolution avec la température et les transitoires nécessitent une mesure.

| Courant traversant le relais | Pertes à 5 mΩ | Chute résistive équivalente | Jonction estimée à Ta = 40 °C* |
| ---: | ---: | ---: | ---: |
| 10 A | 0,50 W | 0,050 V | 41,5 °C |
| 20 A | 2,00 W | 0,100 V | 45,9 °C |
| 30 A | 4,50 W | 0,150 V | 53,4 °C |
| 40 A | 8,00 W | 0,200 V | 63,8 °C |
| 60 A | 18,00 W | 0,300 V | 93,5 °C ; **hors enveloppe proposée** |

*Modèle stationnaire simplifié : `Tj ≈ Ta + P × (2,5 + 0,2 + 0,27)` en °C. Les 0,2 °C/W d'interface sont une **hypothèse de travail**, pas une valeur garantie du HSP-1 ; les 0,27 °C/W jonction-semelle viennent du D1D100. Ce modèle ne représente ni la montée en température, ni le confinement, ni la dispersion du montage ou la variation de Rds.

La courbe D1D100 de la fiche originale, page 4, donne environ **50 A à 40 °C avec 3 °C/W**, puis diminue avec l'air ambiant. Elle fournit un contrôle plus prudent pour notre choix de 2,5 °C/W. La lecture est graphique, pas une nouvelle limite garantie. **60 A cumulés continus et 100 A ne sont pas qualifiés par cette sélection.** Pour 100 A à 40 °C, le constructeur indique un dissipateur de 0,5 °C/W dans sa courbe. Une augmentation de courant impose un nouveau dimensionnement.

À 30 A constants pendant 45 minutes, les pertes du relais représenteraient 3,375 Wh ; à 40 A, 6 Wh. Ces scénarios ne sont pas une consommation prédite du robot et n'établissent pas son autonomie.

## Essais avant de figer l'implantation

Mesurer courant efficace et pointes, tension aux bornes du relais, température de la semelle/dissipateur et air local avec le montage réel. Commencer par un essai à courant réduit, puis reproduire les usages longue durée et les pointes, sans extrapoler un essai bref à 45 minutes. Vérifier les limites du relais, du pad reçu et des pièces voisines, la stabilité thermique et la marge à l'ambiante la plus chaude prévue. Une sonde sur le dissipateur ne mesure pas directement la jonction ; toute température de jonction déduite reste une estimation.

Le dossier [calculs.json](calculs.json) conserve les hypothèses numériques. La carte de surveillance, les fusibles, les transitoires et le faisceau restent des travaux distincts de [l'étude de protection](../protection-batterie/README.md).
