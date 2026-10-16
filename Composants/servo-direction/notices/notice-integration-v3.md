# Intégration V3 — Servomoteur de direction

**Document de projet, distinct des notices constructeur.** 13 octobre 2026. Montage décrit pour l’étude ; aucun essai exécuté.

Réserver GPIO18 (BCM), broche physique 12, fonction RP1 PWM0[2], en complément des GPIO12/13 proposés pour les ESC. Affectation non câblée. Régler 50 Hz et 1500 µs avec le palonnier désaccouplé, puis limiter d’abord la course autour du neutre. Ne pas appliquer 500–2500 µs : cette plage appartient à d’autres références/révisions. Calibrer les angles des roues, indépendamment des 280° annoncés pour le servo. Utiliser le palonnier 20T fourni ; un palonnier ou servo-saver 25T de servo standard ne convient pas. Le servo reste fixé au châssis et ne porte pas le poids des roues.

Les PDF originaux et leurs pages de référence sont liés dans la [fiche](../README.md). Confirmer les données de la variante reçue et les interfaces avant fabrication. [Modèles 3D d’étude et limites](../3D/README.md).
