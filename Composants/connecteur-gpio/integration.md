<!-- vitesse-r1 -->
> **Extension capteurs de vitesse du15octobre2026 :** faisceau actuel à13 contacts montés,18 à provisionner avec5 de réserve. Ajouts : pins16/18 (GPIO23/24),17 (3,3 V) et25 (GND). La puissance5 V reste séparée. [Raccordement actuel](../capteurs-vitesse/integration.md). Les modèles et notices GPIO antérieurs sont des instantanés.
<!-- /vitesse-r1 -->

<!-- alimentation-r2 -->
> **Sélection active révisée le 15 octobre 2026.** Molex conservé pour neuf signaux. Six positions de puissance non câblées dans cette prise. Alimentation Pi séparée : deux positifs et quatre retours courts en 18 AWG soudés aux pads du connecteur Pi ; les anciens quinze fils et leur STEP sont historiques.
> [État électrique courant](../verification-alimentation/README.md) · [Raccordements](../verification-alimentation/integration.md). Les références différentes dans les documents ci-dessous sont historiques. Qualification matérielle non réalisée ; confirmations restantes explicites.
<!-- /alimentation-r2 -->

# Montage et raccordement du GPIO V3

Le plan utilise les **numéros physiques du Pi**, vu de dessus. Le logement femelle vu depuis sa face d’accouplement se lit en miroir. Aligner le repère de broche 1 du fabricant sur la broche 1 du Pi, puis vérifier au multimètre ; ne pas se fier uniquement à la couleur ni à une photographie. Ce boîtier est non polarisé et peut être décalé ou retourné sur une embase nue.

## Affectation proposée

| Broche physique Pi | Fonction | Couleur | Destination |
| ---: | --- | --- | --- |
| 1 | 3,3 V Pi | vert | Alimentation des remontées WARN du circuit de surveillance |
| 2 | 5 V régulés A | rouge | Entrée depuis VOUT du D24V90F5 |
| 4 | 5 V régulés B | rouge | Deuxième entrée depuis le même VOUT ; pas une seconde source |
| 6 | GND alimentation A | noir | Retour régulateur, chemin de puissance électronique |
| 9 | GND alimentation B | noir | Retour régulateur |
| 11 | GPIO17 / WARN1 | blanc, repéré | Collecteur optocoupleur cellule 1, remontée 47 kΩ à 3,3 V Pi |
| 12 | GPIO18 / PWM servo | jaune, repéré | Signal de position FT90M ; puissance fournie par BEC1 à 6 V |
| 13 | GPIO27 / WARN2 | blanc, repéré | Collecteur optocoupleur cellule 2, remontée 47 kΩ à 3,3 V Pi |
| 14 | GND alimentation C | noir | Retour régulateur |
| 15 | GPIO22 / DONE | bleu | Vers la diode de la logique OFF du circuit de surveillance |
| 20 | GND alimentation D | noir | Retour régulateur |
| 32 | GPIO12 / PWM ESC gauche | jaune, repéré | Entrée accélérateur du variateur gauche ; seuil 3,3 V à vérifier |
| 33 | GPIO13 / PWM ESC droit | jaune, repéré | Entrée accélérateur du variateur droit ; seuil 3,3 V à vérifier |
| 34 | GND signal ESC gauche | noir | Référence de commande ; aucun courant de propulsion prévu |
| 39 | GND signal ESC droit | noir | Référence de commande ; aucun courant de propulsion prévu |

Les 25 autres cavités restent sans contact. Les fils WARN blancs et PWM jaunes portent des repères distincts aux deux extrémités. Le point milieu B1 du pack et l’entrée OFF brute du Pololu ne rejoignent aucune cavité GPIO. DONE arrive à la logique avec la diode prévue dans le dossier surveillance ; ce n’est pas un branchement GPIO vers le relais de puissance.

## Servo et deux ESC

Conserver une masse de référence cohérente avec les retours de puissance séparés. Aucun courant de propulsion ne doit utiliser les fils de commande ou les pistes du Pi. Le signal du FT90M peut utiliser le 3,3 V publié pour cette révision ; confirmer le lot. La compatibilité du seuil logique des WP16BL30 G2 doit être mesurée avant leur raccordement ; ce faisceau passif ne convertit pas les niveaux.

Le premier BEC, réglé à 6 V, alimente uniquement la puissance du servo selon le montage à finaliser. Le second positif BEC est isolé. Le +6 V ne rejoint ni pin 1, ni pins 2/4, ni PWM. Les cordons RC d’origine restent utilisés côté actionneurs ; sens, détrompage et connecteurs aval ne sont pas spécifiés par les fils ouverts du STEP. La voie jaune de programmation Hobbywing reste distincte de l’accélérateur.

## Branche 5 V du Pi

Deux fils rouges alimentent pins 2 et 4 depuis le **même** VOUT du D24V90F5. Quatre fils noirs reviennent au régulateur par pins 6/9/14/20. Les courants d’étude seraient 2,5 A par rouge et 1,25 A par noir à partage égal ; ce partage n’est pas garanti. La famille SL est donnée jusqu’à 3 A sous conditions, ce qui ne certifie pas l’embase du Pi, les sertissages, le faisceau groupé ni une branche complète de 5 A.

Couper l’alimentation si un conducteur parallèle est absent ou défectueux ; ne pas supposer qu’un seul rouge peut porter 5 A. Mesurer courant de chaque chemin, chute de tension à la carte et températures en charge vidéo. Garder les protections externes existantes et qualifier la source avant toute déclaration EEPROM de 5 A. Aucun courant du moteur ou du servo dans ces six fils d’alimentation.

## Préparation du connecteur

1. Débrancher batterie, port d’équilibrage et alimentation du Pi. Établir une liste de coupe après implantation ; garder du mou sans boucle vers les roues, engrenages ou ventilateur.
2. Vérifier référence des contacts en vrac, fil multibrin 22 AWG et diamètre de gaine réel. Réaliser un échantillon de sertissage selon la notice de l’outillage retenu. La procédure Molex indique 2,54–3,17 mm de dénudage ; ne pas étamer les brins avant sertissage.
3. Contrôler la retenue du cuivre, de l’isolant et l’absence de brins libres. Pour l’outillage prescrit, la notice donne 39,2 N minimum à 22 AWG lors de l’essai de traction sans contribution du sertissage isolant. Ces valeurs ne certifient pas une pince générique.
4. Insérer chaque contact depuis l’arrière du boîtier jusqu’à sa retenue, contrôler par traction légère et comparer la table fil par fil. Les cinq contacts de réserve ne sont pas montés sans fonction.
5. Tester la continuité de chaque chemin et l’absence de court-circuit entre rails et signaux. Vérifier spécialement pins 1/2/4, les 25 cavités libres, les BEC et B1. Le débranchement du faisceau se fait par le boîtier, pas en tirant les fils.
6. Poser verticalement sur le header hors tension. Retenir mécaniquement le faisceau sur le châssis ; un collier sur les fils ne verrouille pas automatiquement l’accouplement. Aucune tenue aux vibrations garantie sur l’embase nue.

## Dégagements et réception

Les fils sont dirigés vers l’extérieur du bord GPIO, avec une montée avant courbure pour préserver le refroidisseur. Le jeu de 0,72 mm est une lecture d’étude, pas une tolérance garantie ; voir les cotes. La géométrie des contacts est estimée. Essayer d’abord sans moteurs armés : source, signal neutre, trois PWM puis caméra active. Le connecteur n’ajoute ni watchdog ni arrêt matériel : vérifier toujours perte de commande, gel logiciel et freinage.

[Pi et PWM](../raspberry-pi-5/integration.md), [surveillance et coupure](../protection-batterie/integration.md), [refroidissement](../refroidissement-raspberry-pi-5/integration.md), [régulateur](../regulateur-alimentation/README.md).

<!-- terminaisons-commande-v3 -->

Les [trois prises JR et bornes de commande](../connecteurs-commande/integration.md) complètent les extrémités ouvertes du faisceau : broches 32/33/12 pour les trois PWM distincts ; GND 34/39 pour les ESC. Une seule sortie BEC 6 V rejoint le servo, aucune sortie BEC vers le Pi. La prise droite est à deux contacts, cavité centrale vide.

Les broches 2/4 et GND 6/9/14/20 rejoignent les [bornes 5 V et GND](../liaisons-alimentation-surveillance/integration.md) depuis le régulateur. Les fichiers 3D précédents restent des vues datées à fils ouverts ; leur numérotation ne change pas. WARN/DONE et leur protection finale seront arrêtés avec le schéma de surveillance différé.

<!-- /terminaisons-commande-v3 -->
