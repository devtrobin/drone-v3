# CAO A2-R1

- [Châssis nu](chassis-a2-r1-nu.step) : structure, cassettes, portique, cales et patin ; [aperçu](chassis-a2-r1-nu.png).
- [Implantation avec composants allégés](chassis-a2-r1-implante.step) : roues, électronique, Hall, caméra et réservations ; [aperçu](chassis-a2-r1-implante.png).
- C01.step àC19.step : pièces plates seules, repère local du DXF et de pieces.json. G/D gardent leurs identifiants distincts.

Les noms «reserve»,«gabarit» et«enveloppe» identifient les équipements non représentés au détail ou non cotés. Ne pas les envoyer à usiner. Pi/cooler sont volontairement simplifiés ; les gros fichiers détaillés d’origine ne sont pas copiés dans l’assemblage. Les gabarits d’engrenages n’ont pas de dents et ne libèrent aucun empilage interne.

Les anciennes pièces ne sont pas écrasées : provenance etSHA256 dans [manifest](provenance.json). [Contrôles indépendants FreeCAD](validation-freecad.json) et [cohérence des fichiers](../verification/fichiers.json). Les contrôles CAO ne sont pas des essais matériels.
