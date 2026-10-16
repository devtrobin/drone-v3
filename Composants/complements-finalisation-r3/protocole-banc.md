# Recette à réaliser sur matériel

1. Contrôler pièces et références sur le relevé de réception. Monter à blanc et régler les jeux de roulements ; faire tourner à la main, puis présenter les câbles sans batterie. Contrôler gaine, arêtes, portée des garnitures et accès au boutonED80.
2. Sur les interfacesPWM non reliées aux actionneurs, vérifier chaque adaptateur à l’ohmmètre, son brochage et l’absence de pont de masse direct entre côtés. Alimenter en 3.3 V côtéPi et 5 V côtélocal avec sources de laboratoire limitées initialement à 20mA par canal ; mesurer 3.3 V du LDO et état bas par défaut.
3. Observer à l’oscilloscope les signaux en entrée et sortie ; tester extinction de chaque alimentation, redémarrage duPi, absence d’impulsions et commande valide figée. Ne pas déduire l’arrêt moteur du seul suffixeF. Reprendre le protocole de surveillanceM1P existant, dont les conditions restent applicables.
4. Tester la branche de direction sur alimentation limitée adaptée, sansLiPo, avec le servo désaccouplé d’abord. Régler 6 V et le neutre, mesurer courants transitoires et tension au connecteur. Puis appliquer progressivement la charge prévue en surveillant température et chutes. Ne pas maintenir le servo bloqué ni forcer les butées pour le calibrer.
5. Mesurer résistances de boucle à quatre fils et chutes sous charges bornées, depuis 8.4 V jusqu’au seuil minimal prévu. Confirmer le fusible et l’UBEC à partir des résultats et des confirmations fabricant. Aucun essai de court-circuit direct du pack n’est demandé.
6. Peser le montage complet et la charge avant. Le calculR2 reste limité à 9 kg et 45% à l’avant. Faire les essais roulants progressivement après qualification, puis mesurer vidéo, autonomie et vitesse sur un site approprié.

Ces opérations sont un protocole, pas des essais réalisés. Aucun achat, envoi de message fabricant ni assemblage physique n’est exécuté par ce dossier.
