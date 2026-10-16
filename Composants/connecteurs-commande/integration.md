# Intégration - Connecteurs et faisceau de commande

14 octobre 2026. Aucune mise en service effectuée.

1. Les numéros suivants sont les broches physiques du Pi : 32 / GPIO12 pour le PWM de l’ESC gauche, 33 / GPIO13 pour l’ESC droit et 12 / GPIO18 pour le servo. Les masses de signal gauche et droite sont les broches 34 et 39. Les trois PWM restent indépendants.

2. Prise gauche : contact GND vers une borne WAGO 221-413 de masse ; les deux autres ports de cette borne rejoignent la broche 34 et la masse du servo. Le contact central BEC rejoint une autre borne 413, réservée au 6 V du servo. Le contact de signal rejoint GPIO12. La prise du servo reçoit donc GND, ce seul BEC et GPIO18.

3. Prise droite : deux contacts seulement, GND vers la broche 39 et signal vers GPIO13. La cavité centrale reste vide dans la prise fabriquée ; la sortie positive du BEC droit reste isolée côté ESC. Vérifier l’orientation et le repérage réels avant branchement.

4. Régler le BEC gauche à 6 V et contrôler ses pointes sous charge du servo. Ne pas relier les deux BEC, ni envoyer 6 V sur le 5 V ou le 3,3 V du Pi. Un cordon Y standard entièrement câblé unirait les signaux : il ne convient pas à ce raccordement.

5. Sertir les contacts sur les fils 22 AWG avec un outil adapté. Vérifier le sertissage et la retenue, puis encliqueter le boîtier dans le capot selon la procédure Pololu. Tester continuité et absence de court-circuit hors tension. Le nom « mâle » désigne ici les contacts, car les noms commerciaux RC sont parfois inversés.

6. Réutiliser le lot de fil Adafruit 3175 et les contacts Molex du faisceau GPIO existant. Les trois bornes 413 sont comptées une seule fois : une dans ce dossier pour GND servo, deux dans l’ensemble des liaisons pour 5 V et BEC 6 V. Les longueurs finales seront déterminées avec le châssis ; les queues courtes des STEP servent à l’implantation.

7. La compatibilité du seuil haut 3,3 V des ESC reste à vérifier. Les données du FT90M indiquent une plage de signal compatible, à confirmer sur le lot reçu. Mesurer les PWM pendant la charge vidéo et tester démarrage, perte de commande et réarmement. Aucun essai matériel n’est réalisé.

[Composants et achat](README.md), [modèles](3D/README.md), [notice PDF](notices/notice-connecteurs-commande-v3.pdf).
