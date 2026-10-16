> **Révision électrique du 15 octobre 2026 :** les assemblages complets avec MIDI, deux cosses CP0 ou alimentation par contacts Molex sont historiques. Les pièces unitaires conservées restent utilisables comme références géométriques. Consulter la sélection active avant toute implantation.

# Modèles 3D de l’alimentation

**Trois composants et un cordon secteur accessoire : quatre STEP.** Caméra, moteurs, ESC, Pi, roues et train roulant existants ne sont pas régénérés.

[Batterie](../../batterie/3D/README.md), [régulateur Pololu officiel](../../regulateur-alimentation/3D/README.md), [chargeur et cordon](../../chargeur-batterie/3D/README.md).

[Vue d’ensemble](apercu-alimentation.png). Chaque modèle a sa propre échelle.

[Catalogue](catalogue.json), [validation FreeCAD](validation-freecad.json), [architecture et énergie](../README.md).

Génération : `tools/temp/cad-env/Scripts/python.exe tools/build_power_step.py`. Contrôles : `D:/FreeCAD/bin/python.exe tools/validate_power_freecad.py`. Les STEP sont versionnables et ne sont pas ignorés par Git.
