# Régulateur actif : Pololu D42V55F5 / 5571

Remplace le D24V90F5 dans la sélection du 15 octobre 2026. **Sortie 5 V, pas 5,3 V.** [Source Pololu](https://www.pololu.com/product/5571). Prix fabricant affiché : 47,95 USD ; TVA, livraison France et offre Amazon.fr non confirmées. Non acheté et non testé.

La sortie annoncée est 5 V ±3 %, soit 4,85–5,15 V. L’entrée nominale est 5–60 V, sous réserve du dropout ; le courant continu typique est de 5–8 A selon les conditions. À 5 A, la courbe officielle donne un dropout d’environ 0,25 V. Le rendement de 80–95 % est typique. Ces courbes ne garantissent pas la tenue thermique dans le véhicule.

PCB nominal 25,4 × 25,4 mm. Le [plan original](notices/Pololu-D42V55Fx-plan-original.pdf) définit les interfaces. VIN, GND, VOUT, EN, PG : ne pas recopier le raccordement FB de l’ancien modèle. Prendre la puissance aux grands pads. La [CAO officielle](3D/README.md) est conservée sans modification.

La liaison Pi utilise deux positifs et quatre retours courts en 18 AWG, soudés aux pads du connecteur Pi. Le Molex reste réservé aux signaux. Critères de réception : VIN ≥5,8 V et 4,75–5,25 V mesurés aux pads Pi, à 0–5 A, y compris démarrage et échelons. Aucun montage effectué.

[Révision électrique](../../verification-alimentation/README.md) et [raccordements](../../verification-alimentation/integration.md).
