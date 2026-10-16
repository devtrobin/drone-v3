# Cotes et fidélité du modèle

| Grandeur | Valeur | Origine / portée |
| --- | --- | --- |
| Enveloppe en plan |63,50 × 42,50 mm | Plan Raspberry Pi, approximatif |
| Hauteur du dessin |13,70 mm | Attaches incluses ; pas une hauteur installée au-dessus du PCB |
| Emprise du ventilateur |30 × 30 mm | Plan de référence |
| Deux trous dédiés sur Pi |Ø3 mm | Plan Pi ; distincts des quatre trous de châssis Ø2,7 |
| Entraxes des clips dans la reconstruction |58 × 37 mm | Lecture des deux plans ; aucun ajustement de production validé |
| Base CAO |1,4 mm | Estimation |
| Ailettes segmentées |6 colonnes × 9rangées =54 | Structure observée dans plan / photos ; segments 2,05 × 2,95 et hauteur 7,8 mm estimés |
| Pas des segments CAO |3,45 mm enX /4,85 mm enY | Estimation |
| Stries CAO |Pas 0,85 /profondeur 0,14 /hauteur 0,18 mm | Estimation de détails visibles |
| Rotor |30 aubes courbes dans le modèle | Nombre et profil estimés, non donnés par le fabricant |
| Pads |3observés dessous ; 17 × 17,14 × 10,8 × 8 mm dans CAO | Formes et positions estimées ; épaisseurs 0,5/1/1,5 mm non publiées |
| Connecteur FAN Pi |JST-SH,4voies, pas 1 mm | Documentation officielle |
| Fiche du cordon CAO |Boîtier 2,8 × 5,9 × 3,6 mm | Estimation ; pas une empreinte certifiée |
| Fils |Øgaine 0,6 mm /âme équivalente 0,21 mm | Estimation ; ni calibre ni longueur de remplacement garantis |
| Marquage |Contours vectoriels extraits du plan | Relief de lecture 0,018 mm ; gravure réelle non mesurée |

Les cotes libres du plan et les vues des photos ne donnent pas toutes les tolérances, la précharge des ressorts, l’épaisseur comprimée des pads, le volume interne du ventilateur ou son courant. Les modèles ne sont pas des plans de fabrication ni des calibres.

La variante complète ajoute un cordon en pose illustrative ; son enveloppe totale dépasse donc celle du module. Les variantes sans cordon l’omettent volontairement. Le modèle Pi existant est conservé intact ; aucun assemblage Pi / cooler n’est déclaré qualifié par ces seules cotes.

[Plan original](notices/RaspberryPi-ActiveCooler-plan-reference-original.pdf), [fiche constructeur](notices/RaspberryPi-ActiveCooler-fiche-actuelle-originale.pdf), [détails et contrôles de chaque STEP](3D/README.md).
