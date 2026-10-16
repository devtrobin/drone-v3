# Plans R2

LePDF est le dossier de revue et les empilages axiaux sont dans leCSV. Les7DXF C01/C03/C04G-D/R212/R213/R214 sont des contours réels avec leurs perçages, exportés depuis lesSTEP puis réimportés pour comparer leur volume et leur position.

**Repère global de l’assemblage pour lesDXF**, unitésmm, Z0 dans chaque fichier. Les anciensDXF R1 de pièces isolées utilisaient leurs origines locales : ne pas les superposer sans tenir compte de cette différence. La surcouche-percages-r2 est un gabarit de report ; son calqueREFERENCE_NE_PAS_DECOUPER n’est pas un contour d’usinage.

C01 : convertir Xglobal en Xlocal de perçage depuis le bord gauche parXlocal=Xglobal+150. Les trous deC03 au-delà de±150 et les trous extérieurs deC04 ne sont pas des trous du plateauC01. Les empreintes non cotées des équipements restent à releverD05.

Les arbres et pièces usinées sont définis par lesSTEP, les stationsCSV et les exigences du document mécanique. Les filetages ne sont pas hélicoïdaux dans cesSTEP ; lireM4x0.7 etM5x0.8 dans la nomenclature. AucunG-code ni capacité d’usinage de l’atelier n’est supposé.
