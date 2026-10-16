# Cotes - Texas Instruments DRV5033AJQLPG

Source : [fiche originale](../notices/TI-DRV5033-original.pdf).

| Paramètre | Valeur / statut |
| --- | --- |
| Alimentation | 2,5 à 38 V ; alimentation V3 à 3,3 V du Pi |
| Sortie | Drain ouvert actif bas, rappel externe nécessaire ; pas une sortie analogique |
| Broches LPG | 1 = VCC ; 2 = GND ; 3 = OUT. Suivre la vue TI, pas le brochage DBZ |
| Seuil AJ, module du champ | BOP : 3 / 6,9 / 12 mT min / typ / max ; BRP : 1 / 3,5 / 5 mT |
| Fréquence et délai | Bande passante 20 kHz min / 30 kHz typ ; délai de sortie 25 µs max sous conditions TI |
| Courant | 2,7 mA typ à 25 °C ; 3,6 mA max à 125 °C selon table TI |
| Boîtier | LPG0003A : largeur 3,9-4,1 ; corps haut 3,05-3,25 ; épaisseur 1,42-1,62 mm |
| Pattes | Pas 1,27 ±0,05 mm ; longueur sous corps 15,1-15,5 mm ; métal étamé |
| Compléments | Un rappel 10 kΩ et un 100 nF par capteur ; aucun module adaptateur acheté |

Le capteur est nu, sans PCB, câble ni aimant. Le TO-92 LPG est une forme plate chanfreinée, pas le demi-cylindre TO-92 générique. Les rayons, l’épaisseur du marquage +QLAJ et les nuances sont estimés ; la puce et ses connexions internes ne sont pas documentées.

Chaque STEP possède un JSON de provenance avec les cotes retenues et les estimations. Les cotes maximales d’enveloppe ne deviennent pas des valeurs nominales mesurées.
