# Modèles P1 - supports de vitesse

- [Une station assemblée](station-capteur-vitesse-p1.step), [aperçu](station-capteur-vitesse-p1.png).
- [Paire gauche/droite](paire-supports-vitesse-p1.step), [aperçu](paire-supports-vitesse-p1.png). Les stations sont espacées de100 mm pour présentation, **pas pour définir la voie du véhicule**. La gauche est tournée, pas un miroir des broches.
- [Pièces à fabriquer](pieces-supports-vitesse-p1.step), quatre solides séparés en position d'étude : équerre, porte-capteur, retenue, rotor.
- STL individuels : [équerre](P01-equerre.stl), [porte-capteur](P02-porte-capteur.stl), [retenue](P03-retenue.stl), [rotor](P04-rotor.stl). Chaque STL est posé sur son plan d'impression ; prévoir le traitement des ponts de la fourche, sans enfermer de supports dans le rotor.

Repère local : X axe roue ; rotorX0..8, face capteurX0. Capteur côtéX négatif ; sa face marquée regarde+X. Z0 plan de pose, axeZ24 nominal, capteur centréZ36. Le boîtier est reconstruit à partir du plan TI ; pattes raccourcies6 mm, petits rayons et couleurs indicatifs. AimantsØ3 x2 nominaux. Axe et vis de blocage sont des gabarits, sans filetage. Soudures, capteur actif interne, câblage et condensateur réel ne sont pas représentés ; poche réservée au découplage.

[Provenance](provenance.json), [contrôle FreeCAD](validation-freecad.json) et [contrôles de conception](../verification/conception.json). Les volumes de rotation continus et les passages d'aimants sont vérifiés ; champ magnétique et résistance matérielle non testés.
