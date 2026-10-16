# Recherche, choix et limites

Consultation du 15 octobre 2026. Les données électriques proviennent de TI, les cotes des plans constructeur, les données de l’aimant de la fiche de l’article exact. Les pages RS servent au chiffrage et aux conditionnements, pas à remplacer une spécification fabricant.

- DRV5033AJQLPG actif dans l’addendum TI daté du 24 juin 2026 ; circuit principal SLIS152G de septembre 2016. Choix AJ TO-92 en vrac ; ne pas commander un FA ou un SOT-23 par confusion. Le capteur est plus sensible à la proximité magnétique qu’à la vitesse de rotation elle-même.
- Le support TI E2E « Hall sensing distance » explique que la portée dépend de l’aimant et renvoie au calcul du champ. Aucun entrefer universel de plusieurs centimètres n’est transféré à nos disques de 3 mm. Archive HTML conservée. Ce retour constructeur concerne la physique de détection, pas un essai de notre robot.
- Recherche forum et YouTube sur DRV5033 et vitesse de roue : aucun essai identifié et vérifié reproduisant nos capteurs, aimants, roues et implantation. Aucun avis utilisateur, score ou citation n’est inventé. Les notes Trusted Shops du marchand ne sont pas des avis sur S-03-02-N.
- Recherche Amazon.fr des références exactes : pages de contrôle d’accès reçues, sans offre produit vérifiée. Elles sont distinguées des documents techniques dans assets.json. Les liens de recherche ne garantissent ni référence ni stock. Fournisseurs spécialisés proposés en remplacement de la piste Amazon.
- RS : catégorie France pour le capteur 900-9807, fiche pour la résistance 683-2939 et le condensateur 146-3570. Leurs pages ont été consultées via recherche web ; les téléchargements directs refusent 403. Prix de panier, frais et stock final à revalider. L’affichage TTC de la résistance ne correspond pas au HT : calcul à TVA 20 % conservé séparément.
- Aimant : page et PDF donnent 0,11 g arrondi et 0,1074 g respectivement. Le calcul centrifuge utilise 0,11 g. Le minimum de commande de 20 EUR chez supermagnete est pris en compte ; on ne présente pas le lot à 4,80 EUR comme une commande isolée réalisable.
- La fiche KEMET spécifique remplace la description RS générique qui évoque C0G. Ce composant est X7R. Le lien de la fiche a fourni un STEP natif, archivé sans modification.

## Vérifications physiques nécessaires

Contrôler référence, polarités, brochage et résistances hors tension. Alimenter d’abord les deux voies seules sous 3,3 V limité en courant ; mesurer OUT haut et bas. Vérifier au moins deux états hauts et deux états bas par tour, aux jeux minimum et maximum, moteurs à l’arrêt puis en fonctionnement. Refaire le contrôle en freinage et sous charge électrique, Wi-Fi et vidéo actifs. Vérifier la tenue mécanique des aimants et le dégagement avant rotation rapide.

Comparer les fronts horodatés à un générateur/oscilloscope ou compteur de référence. Le budget RC à 1 nF de charge de ligne et 10 kΩ est une hypothèse (temps de montée 10-90 % ≈22 µs), pas une mesure de câble ni une garantie Linux. Mesurer la largeur minimale des impulsions et le retour haut ; les 112 Hz seuls ne suffisent pas à établir la marge de capture. Déterminer les délais d’alerte et la calibration au roulage.

Les modèles sont extérieurs : aucune structure de puce, piste, épaisseur de revêtement magnétique ou cellule céramique non publiée n’est inventée. L’ensemble reste non acheté, non fabriqué et non testé.
