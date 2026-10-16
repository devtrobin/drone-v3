# Modèles 3D de la direction et des transmissions

**29 modèles STEP, dans 14 dossiers de composants.** Les caméra, moteurs, variateurs, Pi 5 et roues existants ne sont pas régénérés.

Les modèles reprennent les dimensions publiées disponibles et complètent les détails visibles par des estimations explicites. Les pièces à fabriquer sont des études paramétriques, pas des plans validés d’usinage.

| Dossier | Modèles | Documentation 3D |
| --- | --- | --- |
| servo-direction | 6 | [STEP, aperçus et provenance](../../servo-direction/3D/README.md) |
| biellettes-direction/rotules | 1 | [STEP, aperçus et provenance](../../biellettes-direction/rotules/3D/README.md) |
| biellettes-direction/chapes | 1 | [STEP, aperçus et provenance](../../biellettes-direction/chapes/3D/README.md) |
| biellettes-direction/tiges | 1 | [STEP, aperçus et provenance](../../biellettes-direction/tiges/3D/README.md) |
| roulements | 1 | [STEP, aperçus et provenance](../../roulements/3D/README.md) |
| axes-avant | 1 | [STEP, aperçus et provenance](../../axes-avant/3D/README.md) |
| moyeux | 1 | [STEP, aperçus et provenance](../../moyeux/3D/README.md) |
| fusees-avant | 5 | [STEP, aperçus et provenance](../../fusees-avant/3D/README.md) |
| transmission-arriere/pignon-moteur | 1 | [STEP, aperçus et provenance](../../transmission-arriere/pignon-moteur/3D/README.md) |
| transmission-arriere/engrenages-54dents | 1 | [STEP, aperçus et provenance](../../transmission-arriere/engrenages-54dents/3D/README.md) |
| transmission-arriere/pignon-intermediaire | 1 | [STEP, aperçus et provenance](../../transmission-arriere/pignon-intermediaire/3D/README.md) |
| arbres-transmission | 2 | [STEP, aperçus et provenance](../../arbres-transmission/3D/README.md) |
| paliers-transmission | 2 | [STEP, aperçus et provenance](../../paliers-transmission/3D/README.md) |
| fixations-train-roulant | 5 | [STEP, aperçus et provenance](../../fixations-train-roulant/3D/README.md) |

[Vue d’ensemble des 29 modèles](apercu-composants.png). Chaque tuile a sa propre échelle ; les tailles relatives ne représentent pas l’implantation.

[Contrôle FreeCAD](validation-freecad.json), [catalogue structuré](catalogue.json), [sélection et notices](../README.md).

Génération : `tools/temp/cad-env/Scripts/python.exe tools/build_running_gear_step.py`. Sélection optionnelle `--group gears` ou `--group servo`, etc. Chaque STEP reste de taille modérée et peut être versionné directement dans Git ; aucune règle ne l’ignore.
