<!-- alimentation-r2 -->
> **Sélection active révisée le 15 octobre 2026.** MIDI 60 A et support M5 retirés de la sélection active. Remplacement proposé : JLLN050.T 50 A et LFT300601C avec capot. Confirmation de la terminaison fine brins avant achat.
> [État électrique courant](../verification-alimentation/README.md) · [Raccordements](../verification-alimentation/integration.md). Les références différentes dans les documents ci-dessous sont historiques. Qualification matérielle non réalisée ; confirmations restantes explicites.
<!-- /alimentation-r2 -->

# Fusible principal et porte-fusible - Drone V3

**Sélection d'étude du 14 octobre 2026, non achetée et non testée.** Deux composants séparés :

| Composant | Référence retenue | Statut |
| --- | --- | --- |
| [Porte-fusible](porte-fusible/README.md) | Littelfuse **04980900ZXT**, MIDI/BF1, capot, goujons M5, écrous et rondelles | Support compact, sans fusible ni câbles |
| [Fusible principal](fusible-60a/README.md) | Littelfuse **0498060.M**, MIDI temporisé, **60 A / 32 V DC**, deux trous M5 | Calibre d'étude à confirmer avec les fils, la température et les mesures |

Le fusible principal protège le **faisceau de puissance**, à placer près du positif batterie, avant la distribution vers le relais moteurs et la branche Pi. Il ne constitue ni une limite de courant moteur à 40 A, ni une protection garantie des semi-conducteurs, ni une protection des petites branches sans fusibles adaptés. Les deux ESC de 30 A ne déterminent pas seuls son calibre.

Pourquoi 60 A pour l'étude : avec 40 A moteurs au total et une hypothèse de 25 W pour Pi + caméra, le courant principal atteint environ **44,39 A à 6,4 V**, rendement du régulateur supposé 90 % et réserve auxiliaire de 50 mA. La fiche récente recommande typiquement **48 A à 65 °C** pour le calibre 60 A. Cette marge reste conditionnelle ; aucun courant réel ou échauffement n'a été mesuré.

Le support annoncé pour 200 A ne rend pas les fils ou le montage aptes à 200 A. Le fusible impose une limite de tension de **32 V DC** à l'ensemble, compatible en tension avec le pack 2S de 8,4 V maximum.

[Notice PDF du projet](notices/notice-fusible-principal-v3.pdf), [montage et calculs](integration.md), [cotes](cotes.md), [recherches, alternatives et avis](recherche-technique.md), [sources](sources.json), [calculs structurés](calculs.json), [originaux et SHA256](assets.json), [quatre STEP détaillés](3D/README.md).

**Achat Amazon :** les recherches ont renvoyé une page de vérification, sans catalogue exploitable. Aucune offre exacte, ASIN, disponibilité française ou prix livré n'est confirmé. Les références sont documentées chez des distributeurs ; les prix observés hors France ne constituent pas un panier français validé. Aucune commande effectuée.
