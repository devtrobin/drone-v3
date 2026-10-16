<!-- finalisation-r2 -->
> **ÉtudeR2 du16octobre2026 :** [définition mécanique etimplantation révisées](../finalisation-theorique-r2/README.md). Les anciens arbres50mm etFT90M ne sont plus la définition nominaleR2 ; les réservations/interfaces non mesurées restent conditionnelles. Conserver les modèles/documents ci-dessous comme référencesA2-R1.
<!-- /finalisation-r2 -->

# Supports réglables des capteurs de vitesse - P1

> **Implantation A2-R1 :** [châssis et plans](../chassis/README.md). Pieds sur le dessus du plateau Z11, axes de roues Z31,5 : régler H à 20,5 mm, soit la tête abaissée de 3,5 mm par rapport au STEP P1 nominal. Trous de pied X±74, Y435/455 ; rotors sur les sorties de roues, faces intérieures X±103. L'empilage réel et les essais restent à qualifier ; les STEP P1 d'origine sont conservés.

Deux stations identiques, une par roue arrière : **équerre à fourche, porte-capteur coulissant, petite retenue frontale, rotor porte-aimants**. Quatre pièces à fabriquer par côté, huit pour le véhicule. Modèles de test démontables ; aucun châssis définitif ni visserie finale.

[Notice et plan coté PDF](notices/notice-supports-capteurs-vitesse-p1.pdf) · [STEP, STL et aperçus](3D/README.md) · [Cotes](cotes.json) · [Nomenclature](nomenclature.csv) · [Plans](plans/README.md) · [Contrôles géométriques](verification/conception.json).

Le rotor se monte sur **l'axe de sortie roueØ5**, à1 tour de rotor par tour de roue, pas sur un arbre intermédiaire. Réserver **11 mm de longueur d'axe** autour du rotor8 mm, ainsi qu'un dégagement radialØ32. L'empilage réel avec roulements, couronnes et moyeu sera défini avec le châssis ; aucun arbre existant n'est déclaré compatible sans ce contrôle.

Deux aimantsØ3 x2 à180° sont chargés dans les canaux internes par l'alésage, avant montage sur l'axe. Une fois l'axe inséré sur toute la largeur, il bloque l'entrée des aimants. Les parois du rotor les entourent, dont0,6 mm côté capteur. Une petite quantité de colle compatible peut les immobiliser au rayon12, mais elle n'est pas la seule barrière contre l'éjection. Deux vis M3x8 opposées bloquent le rotor sur l'axe ; taraudages et endurance à vérifier, puis retenue axiale définitive avec le train roulant.

Face plane du Hall tournée vers le rotor. Réglage initial **2,5 mm entre face plane Hall et face extérieure rotor**, soit environ3,1 mm jusqu'à la face de l'aimant enfouie. La retenue de1,5 mm avance devant les bords du capteur : son jeu mécanique initial est1 mm. Ce réglage est un point de départ, **pas une portée de détection garantie**. La fourche dégage l'axe ; deux lumières verticales adaptent sa hauteur de18 à30 mm **par rapport au plan de fixation**, pas au sol. La hauteur nominale24 mm ne fixe donc pas la hauteur du futur châssis.

Le boîtier Hall est logé sans serrer ses pattes. Une poche au-dessous réserve le découplage100 nF et les soudures isolées. Les pattes sont représentées raccourcies à6 mm pour dégager l'axe ; décider leur longueur et leur formage après présentation réelle. Rappels et GPIO restent ceux du [dossier capteurs](../capteurs-vitesse/integration.md), aucun changement électrique.

Essayer d'abord à la main : absence de contact sur360°, rotor bloqué, capteur retenu, fils éloignés des pièces tournantes. Obtenir **deux fronts descendants et un retour haut entre aimants** par tour, puis contrôler progressivement sous écran à vitesse croissante. L'acier de l'axe, les vis et les moteurs peuvent modifier le champ. La rétention, l'équilibrage, le glissement et la détection à40 km/h ne sont pas qualifiés par la CAO.

PETG proposé pour prototypage ; rotor dense, contrôler canaux et parois avant usage. Pas de support d'impression enfermé dans les canaux. Les STEP permettent une adaptation de fabrication, mais le rotor monobloc à canaux internes n'est pas directement une pièce à fraiser en une seule prise. Prix de matière et quincaillerie à chiffrer, aucun panier d'achat ni achat effectué.

Sources : [TI DRV5033](https://www.ti.com/lit/ds/symlink/drv5033.pdf), [supermagnete S-03-02-N](https://www.supermagnete.fr/aimants-disques-neodyme/disque-magnetique-3mm-2mm_S-03-02-N), notices originales conservées dans [capteurs-vitesse](../capteurs-vitesse/notices/README.md). Les pièces électroniques, les aimants, la transmission et leurs modèles d'origine sont conservés.
