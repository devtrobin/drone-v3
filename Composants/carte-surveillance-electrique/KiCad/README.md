# KiCad - Surveillance 2S M1

Ouvrir [surveillance-2s-m1.kicad_pro](surveillance-2s-m1.kicad_pro). [Schéma](surveillance-2s-m1.kicad_sch), [PCB routé](surveillance-2s-m1.kicad_pcb), [schéma vectoriel](vues/surveillance-2s-m1.svg), [routage](vues/routage.svg), [montage](vues/montage.svg), [dessus](vues/cuivre-dessus.svg), [dessous](vues/cuivre-dessous.svg), [CSV porteuse](nomenclature.csv), [CSV assemblage complet](../nomenclature-assemblage.csv).

41 composants/connexions sur porteuse, dont R7/R8 DNP ; 26 nets ; PCB 140 x 75 x 1,6, deux couches. Pistes 0,20, isolement minimal 0,15, cuivre supposé 35 micromètres, vias 0,60/0,30. Ces règles ne sont pas une procédure d'usinage CNC. Les empreintes locales Nano454 et TMR1 et les symboles de blocs sont inclus ; les autres empreintes sont celles des bibliothèques standard KiCad 10. Les symboles de blocs représentent les fonctions et pins des interfaces, pas les composants internes des modules commerciaux.

**Contrôle KiCad 10.0.7 : ERC 0, DRC 0, aucun élément non connecté, aucune divergence de parité schéma/PCB.** Netlist XML comparée indépendamment aux connexions attendues. Rapports complets dans [verification](../verification/controle-kicad.json), sans exclusions ajoutées pour masquer les défauts. Les recommandations du fabricant et le montage réel restent à qualifier.

J3/J4 et J5 sont des départs de faisceaux vers les modules, pas des empreintes où enficher directement un EVM ou un Pololu. Les résistances de seuil restent sur les deux EVM, hors porteuse. RA0/RA1/RA2 au pack et FAUX près de sa dérivation ne sont pas placés sur ce PCB. R7/R8 sont achetées mais montées côté Pi ; leurs pads porteuse restent vides.

Génération reproductible depuis la racine V3 : `D:/KiCAD/bin/python.exe tools/build_monitor_kicad.py`. Contrôles : `tools/temp/cad-env/Scripts/python.exe tools/check_monitor_kicad.py`. Les paramètres et la connectivité sont dans le script et les JSON. Les vues de cuivre sont des documents de revue ; il faut une revue d'empreintes et les essais décrits avant de libérer une fabrication. Aucun Gerber n'est présenté comme validé pour production.
