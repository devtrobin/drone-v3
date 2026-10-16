# Notices et plans conservés

Documents originaux téléchargés sans modification ; sommes SHA256 dans [assets.json](../assets.json).

- [Raspberry-Pi-5-alimentation-USB-PD-livre-blanc-2026.pdf](Raspberry-Pi-5-alimentation-USB-PD-livre-blanc-2026.pdf) — [source originale](https://pip-assets.raspberrypi.com/categories/685-app-notes-guides-whitepapers/documents/RP-009856-WP-1-USB%2520Power%2520delivery%2520on%2520Raspberry%2520Pi%25205.pdf).
- [Pololu-D24V60F5-D24V90F5-plan-cote.pdf](Pololu-D24V60F5-D24V90F5-plan-cote.pdf) — [source originale](https://www.pololu.com/file/0J1581/step-down-voltage-regulator-d24vxf5-dimensions.pdf).
- [Pololu-D24V60F5-D24V90F5-percages.dxf](Pololu-D24V60F5-D24V90F5-percages.dxf) — [source originale](https://www.pololu.com/file/0J915/reg15b02-drill.dxf).

[Notice d’intégration de projet](notice-integration-v3.md).

L’intégration proposée utilise les **rails 5 V du connecteur 40 broches de la Pi (broches physiques 2 et 4)** et plusieurs masses, via un faisceau protégé à dimensionner ; ce n’est pas une GPIO de signal. Cette entrée demande des protections externes adaptées et interdit l’alimentation simultanée par une autre source. USB-C reste possible avec une interface de source correctement conçue, mais un simple câble ne crée pas une négociation PD. Le réglage `usb_max_current_enable=1` n’est envisageable qu’après validation de la capacité de la branche : il relève une limite USB, il n’améliore pas le convertisseur. Voir le dossier commun pour les deux possibilités et les contrôles. EN est tiré vers VIN : ne pas le relier directement à une GPIO 3,3 V. PG est collecteur/drain ouvert et demande un pull-up adapté ; son seuil ≈4,5 V ne remplace pas le contrôle de sous-tension de la Pi.
