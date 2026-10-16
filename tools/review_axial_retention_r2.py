from pathlib import Path
import json,hashlib,urllib.request,sys
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Composants/finalisation-theorique-r2'
refs=[('Beneri-DIN471.html','https://www.beneri.com/en/prodotto/din-471'),('HPC-circlips-DIN471.pdf','https://shop.hpceurope.com/pdf/frPDFauto/CYS.pdf')]
sources=json.loads((B/'sources.json').read_text(encoding='utf-8'))
for filename,url in refs:
    row=dict(file=None,url=url,note='DIN471-5: anneau0.6, gorgeØ4.8 +0/-0.05, m0.70H13 ; projetresserrem0.70..0.73 ; nminimum0.3. ProfilCADdesoreillesreconstruit.',archived=False)
    p=B/'references'/filename
    if '--fetch' in sys.argv:
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
            data=urllib.request.urlopen(req,timeout=25).read()
            if filename.endswith('.pdf'):assert data.startswith(b'%PDF')
            p.write_bytes(data)
        except Exception as e:row['error']=str(e)
    if p.exists():row.update(file='references/'+filename,archived=True,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    sources=[s for s in sources if s['url']!=url]+[row]
(B/'sources.json').write_text(json.dumps(sources,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
d=ROOT/'Composants/retenues-axiales';d.mkdir(exist_ok=True)
(d/'README.md').write_text('''# Retenues axiales R2

Quatre circlips achetés **DIN 471-5 en acier à ressort**, fabricant Beneri ou équivalent documenté. Deux retiennent les arbres intermédiaires et deux les rotors Hall, en face d’épaulements monoblocs. Les petits colliers hypothétiques ne sont plus utilisés.

Gorge Ø4.80 +0/-0.05 mm, largeur choisie0.70..0.73mm, anneau nominal0.60mm ; la ficheBeneri donne une distance de bout minimale0.3mm. Le projet garde1mm sur l’intermédiaire. Contrôler la fermeture du circlip dans la gorge et le jeu axial, sans l’ouvrir excessivement.

[Définition et stations](../finalisation-theorique-r2/mecanique.md) · [Modèle d’encombrement](../finalisation-theorique-r2/3D/R225_circlip_DIN471_5.step) · [Données fabricant](https://www.beneri.com/en/prodotto/din-471) · [Fiche HPC](https://shop.hpceurope.com/pdf/frPDFauto/CYS.pdf).

Le profil des oreilles du STEP est reconstruit : il ne sert pas à fabriquer l’anneau. Choisir un circlip traçable, inspecter la gorge tournée et vérifier le montage sous écran. Aucun achat ou essai matériel réalisé.
''',encoding='utf-8')
print('RETENUES',[(r['url'],r['archived']) for r in sources if r['url'] in [v for k,v in refs]])
