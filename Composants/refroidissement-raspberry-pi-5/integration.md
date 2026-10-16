# Intégration V3 de l’Active Cooler

## Installation sur le Pi 5

1. Batterie, alimentation Pi et équilibrage débranchés ; stabiliser la carte. Vérifier ventilateur, pads et deux clips du produit reçu.
2. Retirer les papiers de protection des pads sous le module. Ne pas laisser de film entre pad et composant ; ne pas ajouter automatiquement de pâte ou une seconde couche.
3. Orienter selon le dessin sur la boîte et la notice fabricant. Aligner les deux attaches avec les **deux trous dédiés au dissipateur**, pas les trous de fixation du châssis. Éviter les ports et composants de la carte.
4. Appuyer régulièrement sur les deux têtes blanches jusqu’à l’encliquetage. Vérifier les clips par-dessous et que le métal ne touche pas de composant ou contact électrique hors des interfaces prévues.
5. Insérer la fiche dans **FAN**, dans le sens prévu, sans forcer. Si elle résiste, retirer et inspecter connecteur et fiche. Fixer le cordon pour qu’il ne touche ni le rotor ni une roue ou transmission.
6. Le fabricant recommande de laisser le montage en place : démontages répétés dégradent clips et pads. Un clip déformé ou mal retenu doit être remplacé. L’intervention de maintenance suit la notice du lot.

## Raccordement et commande

| Broche FAN officielle | Fonction | Fil |
| --- | --- | --- |
|1 |+5 V | Rouge |
|2 |PWM | Bleu |
|3 |GND | Noir |
|4 |Tachymètre | Jaune |

Connecteur JST-SH,4voies, pas 1 mm. La vue de numérotation est celle de la documentation officielle : ne pas déduire un ordre à souder en regardant arbitrairement le côté opposé. La fiche livrée reste utilisée, aucun câble de remplacement construit ici.

Le contrôle dédié FAN est distinct des PWMGPIO12/13/18 des moteurs et du servo. Aucun microcontrôleur supplémentaire ni raccord au BEC6 V n’est nécessaire pour le ventilateur d’origine. Il reçoit son 5 V par la carte Pi, dont la branche est déjà régulée par le PololuD24V90F5.

La documentation Pi actuelle décrit, en température montante :50 °C→30 %,60 °C→50 %,67,5 °C→70 %,75 °C→100 %, arrêt sous 50 °C, hystérésis 5 °C en descente. Elle décrit aussi la détection tachymétrique à l’amorçage. **Ces paramètres dépendent du système, noyau et firmware reçus** ; relever le comportement réel. Le billet constructeur 2023 ne citait que 60/67,5/75 °C : ne pas reprendre ses seuils comme une configuration 2026 garantie. Aucune configuration appliquée.

## Alimentation et thermique

Le connecteur FAN partage la limitation de courant des périphériques USB. Le courant d’environ 60 mA publié pour le **ventilateur de boîtier officiel** ne donne pas celui de cet Active Cooler. La fiche SC1148 ne publie pas son courant dans les données consultées ; mesurer appel de démarrage et régime, avec la caméra USB.

La branche 5 V de 5 A /25 W d’étude inclut déjà Pi, caméra et refroidissement : ne pas ajouter une seconde fois la puissance du ventilateur au bilan global. Ce budget n’est pas une consommation mesurée. Ne relever les limites d’alimentation Pi qu’après qualification de la source et du faisceau selon le dossier Pi.

Prévoir admission au-dessus du rotor et sortie vers les ailettes dégagées. Ne pas enfermer le module sous une plaque pleine ni bloquer l’air avec un faisceau. Le refroidissement doit fonctionner robot immobile ; on ne suppose pas un courant d’air lié aux 40 km / h. Hauteur installée et jeux aux ports, supports, caméra et coque à vérifier sur matériel.

## Essais à réception

Confirmer référence, sens de fiche, pads et clips. Démarrer et vérifier la rotation / tachymètre. Mesurer tension 5 V à la carte et courant total USB / FAN, démarrage du ventilateur et effets des moteurs. Sur l’usage vidéo prolongé, enregistrer température CPU, fréquence, signalement de sous-tension / throttling, régime et courant fan, cadence / latence vidéo et stabilité des impulsions moteurs. Essayer aussi robot immobile et dans le châssis final, sans overclocking supposé.

Les essais thermiques d’autres utilisateurs ne qualifient pas notre chaîne 1080p60 ni son autonomie. L’Active Cooler ne remplace pas l’arrêt sur perte Wi-Fi ou blocage de la commande.

[Notice fabricant](notices/RaspberryPi-ActiveCooler-fiche-actuelle-originale.pdf), [documentation FAN](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html), [alimentation Pi](../regulateur-alimentation/README.md), [dossier Pi](../raspberry-pi-5/integration.md), [calculs](calculs.json).
