# Contrat GPIO M1 - logiciel non déployé

GPIO17 et GPIO27 : entrées, rappels externes 47 kohms au 3,3 V du Pi côté Pi ; bas = état au-dessus du seuil de retour, haut = avertissement/perte de lumière. L'ancien concept était actif bas : inverser explicitement le traitement avant usage. Démarrer avec la propulsion inhibée.

GPIO22 : sortie inactive basse pendant fonctionnement ; haute en fin de poweroff via diode vers OFF. Base de configuration officielle à vérifier pour Pi 5 et OS choisi : `dtoverlay=gpio-poweroff,gpiopin=22`. Ne pas l'activer sans banc ; les effets sur reboot et remise en marche doivent être vérifiés. Aucune écriture sur un Pi n'a été effectuée.

Le service de supervision devra utiliser l'API GPIO compatible Pi 5, détecter une entrée haute, interdire l'accélération, arrêter vidéo et fichiers, puis demander poweroff. Anti-parasitage et temporisation doivent suivre les mesures de banc ; un retard logiciel n'agit jamais sur la coupure analogique dure. Pas de tension numérique ni de pourcentage de charge fourni par ces deux entrées.
