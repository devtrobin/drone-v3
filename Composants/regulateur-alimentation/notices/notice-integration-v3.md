# Notice d’intégration V3 — Régulateur de la branche Raspberry Pi

**Document de projet, distinct des notices originales constructeur.** 13 octobre 2026. Aucun essai matériel.

Raccorder la batterie sur **VIN/GND**, jamais sur VOUT. La cible de branche Pi est une capacité disponible de **5 A**, pas une consommation continue supposée. Mesurer d’abord la sortie sans la Pi, puis avec une charge de contrôle. Évaluer le module de 8,4 V jusqu’à la tension d’arrêt retenue, sous la charge réelle et pendant les accélérations moteurs. Utiliser un faisceau court de puissance, soudé aux grands pads ou aux borniers adéquats ; pas de fils Dupont ni de plaque d’essai pour porter 5 A. Isoler le dessous et conserver de l’air autour du régulateur.

L’intégration proposée utilise les **rails 5 V du connecteur 40 broches de la Pi (broches physiques 2 et 4)** et plusieurs masses, via un faisceau protégé à dimensionner ; ce n’est pas une GPIO de signal. Cette entrée demande des protections externes adaptées et interdit l’alimentation simultanée par une autre source. USB-C reste possible avec une interface de source correctement conçue, mais un simple câble ne crée pas une négociation PD. Le réglage `usb_max_current_enable=1` n’est envisageable qu’après validation de la capacité de la branche : il relève une limite USB, il n’améliore pas le convertisseur. Voir le dossier commun pour les deux possibilités et les contrôles. EN est tiré vers VIN : ne pas le relier directement à une GPIO 3,3 V. PG est collecteur/drain ouvert et demande un pull-up adapté ; son seuil ≈4,5 V ne remplace pas le contrôle de sous-tension de la Pi.

[Retour à la fiche](../README.md).
