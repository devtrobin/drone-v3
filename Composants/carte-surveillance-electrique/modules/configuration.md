# Adaptation des modules existants

## M1 et M2 - TPS3700EVM-114

La référence retenue est l'EVM-114 en SOT-23, pas l'EVM-202 WSON. Schéma TI SLVU683A, figure 6 p.7 et nomenclature p.8. Le manuel décrit une fenêtre d'usine autour de 12 V, impropre à notre usage sans modification.

| Élément de chaque EVM | Configuration M1 |
| --- | --- |
| R1 d'usine 2,21 Mohms | Remplacer par 79,6 kohms, 0603, 0,1 % |
| R2 d'usine 13,7 kohms | Remplacer par 634 ohms, 0603, 0,1 % |
| R3 d'usine 69,8 kohms | Remplacer par 10,0 kohms, 0603, 0,1 % |
| R4 et R5 | Conserver 100 kohms selon schéma et BOM ; contrôler la carte reçue (texte OUTB du manuel mentionne aussi 10 kohms) |
| R6 | Non monté ; ne jamais réunir les deux sorties |
| J10 | Cavalier 1-2 : **MONITOR SENSE** |
| J11 | Cavalier 1-2 : **VPU = VDD local isolé** |
| J1 VDD | 5 V isolé de M3 ou M4 |
| J2/J4/J6/J8 GND | Référence locale de la cellule ; aucune liaison directe à D- |
| J3 SENSE | B1_R pour M1 ; B2_R pour M2 |
| J5 OUTA | HARD_A1 / HARD_A2 : bas sous le seuil dur |
| J7 OUTB | WARN_B1 / WARN_B2 : bas au-dessus du seuil d'avertissement |
| J9 VEXT | Libre |

Chaque connecteur J1-J9 comporte deux broches déjà communes entre elles pour le même signal (schéma TI). Une seule suffit par liaison ; ce ne sont pas des paires signal/masse. Le câble de porteuse J3/J4 définit son propre ordre : **1 = ISO5, 2 = REF, 3 = SENSE, 4 = OUTA, 5 = OUTB**. Il ne se branche pas directement dans une rangée de l'EVM : cinq fils repérés vont aux connecteurs TI correspondants.

L'entrée INA+ est le nœud R1/R2 ; INB- est le nœud R2/R3. Conserver cette topologie en chaîne, sans inversion. OUTA court-circuite la LED HEALTHY à l'état bas ; OUTB allume la LED WARN_OK à l'état bas. Toutes les LED et remontées des EVM sont alimentées par le 5 V isolé, jamais par un GPIO.

Ces six remplacements de résistances nécessitent une reprise CMS 0603. Nettoyer et contrôler les valeurs ainsi que l'absence de ponts sous microscope. Aucun Gerber de TI n'est modifié ou revendiqué comme fichier propriétaire du projet.

## M3/M4 - Traco TMR 1-0511

Entrée 4,5-9 V, sortie régulée 5 V / 200 mA, sans charge minimale. **Entrée depuis le 5 V MON du Pololu**, pas directement depuis le pack : la faible marge entre 8,4 et 9 V ne suffit pas à absorber les transitoires moteur. Pins : 1 = -VIN, 2 = +VIN, 4 = +VOUT, 6 = -VOUT, aucune broche 5 sur le modèle à sortie simple. Respecter la vue de référence du plan ; pas de variante à sorties doubles.

Corps nominal 17 x 7,62 x 11 mm. Le plan constructeur demande d'éviter les pistes sous le convertisseur. Le routage conserve donc une zone sans piste sous le corps, avec sorties des pastilles vers l'extérieur. L'isolement fonctionnel empêche la masse du Pi de devenir un retour d'équilibrage ; il ne fait pas de la carte une protection de sécurité certifiée.

TRACO recommande un fusible lent 500 mA pour les modèles d'entrée 5 V, tout en demandant d'évaluer le besoin dans l'application finale. Le prototype prévoit deux emplacements de fusibles lents 500 mA en série avec les entrées TMR ; référence de base 0454.500MR (NANO2 CMS 2410, 125 V DC / 50 A), courbes à vérifier dans la nomenclature KiCad avant fabrication. FAUX 1 A protège le départ batterie et ne vaut pas validation de leur coordination.

## M5 - Pololu 2831 D24V10F5

Entrée AUX protégée, GND D-, sortie 5V_MON réservée aux TMR. Ne pas confondre avec le régulateur principal Pi D42V55F5. Employer les connexions repérées VIN/GND/VOUT par fils courts ; la liaison J5 de la porteuse est un connecteur de faisceau, pas l'empreinte directe du module. SHDN et PG restent libres. La référence 2830 est la variante 3,3 V et ne convient pas ici.
