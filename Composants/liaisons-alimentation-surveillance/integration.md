<!-- alimentation-r2 -->
> **Sélection active révisée le 15 octobre 2026.** Ajouter une rallonge 3-RAL2S réservée au chargeur, distincte de celle de surveillance. Les fils 18 AWG sont réutilisés pour la puissance Pi. Déplacer la masse de logique vers D− ; les fils d’équilibrage ne deviennent pas un retour de puissance.
> [État électrique courant](../verification-alimentation/README.md) · [Raccordements](../verification-alimentation/integration.md). Les références différentes dans les documents ci-dessous sont historiques. Qualification matérielle non réalisée ; confirmations restantes explicites.
<!-- /alimentation-r2 -->

# Intégration - Liaisons alimentation et mesure2S

14 octobre 2026. Aucune mise en service effectuée.

1. Le grand pad VOUT du D24V90F5 rejoint, par un fil 18 AWG rouge, une borne 221-413 de 5 V. Ses deux autres ports rejoignent les broches physiques 2 et 4 du Pi par les fils 22 AWG existants. Le grand pad GND rejoint une 221-415 par un fil 18 AWG noir ; les quatre sorties 22 AWG rejoignent les broches 6, 9, 14 et 20.

2. Les bornes distinctes du projet portent respectivement 5 V, GND d’alimentation Pi, BEC 6 V et GND servo. Tous les ports d’une même borne sont reliés : ne jamais mélanger ces potentiels dans une borne. Réserver un conducteur par port, dénuder 11 mm, lever, insérer à fond et refermer. Contrôler visuellement puis par traction ; ne pas étamer la partie serrée.

3. Le fil BNTECHGO possède 150 brins annoncés de 0,08 mm : leur section calculée vaut 0,754 mm², inférieure au nominal AWG18 d’environ 0,823 mm². Pour une boucle de 2 x 0,20 m à 5 A, avec ρ cuivre = 0,0175 Ω·mm²/m à 20 °C, la chute idéale vaut 0,0464 V et la perte 0,232 W. Contacts, soudures, fils GPIO et échauffement sont exclus de ce calcul.

4. Le partage du courant entre les broches 2 et 4 et entre les quatre masses n’est pas garanti. La sortie fixe 5 V ±4 % peut déjà descendre à 4,8 V avant le faisceau. Mesurer tension au Pi, courant et températures en charge, notamment lors des accélérations. Aucun branchement simultané d’une alimentation USB-C ; pas de réglage à 5 A déclaré avant qualification.

5. La rallonge INTERMODEL 3-RAL2S possède trois positions, type XH annoncé et longueur de 20 cm. Confirmer le type de la prise batterie et l’ordre des broches au voltmètre : B0 est le moins total, B1 le point milieu et B2 le plus total. B1 ne rejoint jamais GND du Pi. Cette prise sert à la mesure des cellules, jamais à alimenter moteur, servo ou Pi.

6. L’embase JST B3B-XH-A est réservée à la future carte de surveillance. Le catalogue JST donne un pas de 2,50 mm ; une annonce « XH 2,54 » ne certifie pas un produit JST. Les calibres et diamètres de fils de la rallonge ne sont pas publiés ; les détails correspondants du STEP sont estimés. Le schéma final définira polarité de carte, protection des fils de mesure et absence de retour par les signaux lors de la coupure.

7. La liaison principale pack vers MIDI et D− reste conditionnelle à la qualification du XT60 réel de la batterie. L’hypothèse de courant commun 44,39 A dépasse l’hypothèse prudente de 30 A continus retenue pour le XT60H. Le fil 6 mm² et l’ED80 ne changent pas cette limite ; aucun adaptateur ni modification du pack n’est validé. Les départs ESC 12 AWG sont déjà documentés.

8. Réutiliser les provisions de fils 22 AWG, 6 mm², cosses et gaines déjà présentes dans la nomenclature. Ajouter le lot 18 AWG pour les liaisons de sortie du régulateur ; 0,20 m par couleur reste une provision, pas une longueur de coupe. Le câble USB de 1 m est inclus avec la caméra : aucun second achat proposé.

[Composants et achat](README.md), [modèles](3D/README.md), [notice PDF](notices/notice-liaisons-alimentation-surveillance-v3.pdf).
