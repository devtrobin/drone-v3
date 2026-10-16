"""Readable French technical spacing while preserving links, markup and SKUs."""
import re
def format_text(value):
    chunks=re.split(r'(<[^>]*>|https?://[^\s<>]+|\]\([^)]*\)|`[^`]*`)',str(value))
    out=[]
    for s in chunks:
        if s.startswith(('<','http','](', '`')):out.append(s);continue
        s=re.sub(r'([a-zàâäéèêëîïôöùûüç]{2,})(?=\d)',r'\1 ',s)
        s=re.sub(r'\b(fil|fils|cuivre|gaine|famille|commune|commun|fixation|longueur|outils|Données|documents|copie|lot|plan|standard|tubulaires|classe|étude|appairage|index|vis|candidat)(?=[A-ZØ])',r'\1 ',s)
        s=re.sub(r'(ATUM|T18R|MB2|ECu|IEC|UL|PDF|TE)(?=\d)',r'\1 ',s)
        s=re.sub(r'(?<=\d)(?=(?:AWG|mm|cm|m\b|km|°C|A\b|VAC|VDC|V\b|W\b|N\b|Nm\b|STEP|brins|colliers|embases))',' ',s)
        s=re.sub(r'(?<=\d)(?=(?:Oct|Dec|octobre))',' ',s)
        s=re.sub(r'(?<=mm²)(?=[a-zA-Zà-ÿ])',' ',s)
        s=re.sub(r'(?<=[a-zà-ÿ])(?=Ø)',' ',s)
        s=re.sub(r'([×≤≥±])(?=[\d−-])',r'\1 ',s)
        s=re.sub(r'à(?=[−-]?\d)','à ',s)
        for a,b in [('FLRY-B6','FLRY-B 6'),('AUPROTECFLRY','AUPROTEC FLRY'),('HellermannTytonT18R','HellermannTyton T18R'),
            ('HellermannTytonMB2','HellermannTyton MB2'),('Ømax','Ø max'),('Øint','Ø int'),('80N','80 N'),('PDFp.','PDF p.'),('et54','et 54'),('et40','et 40'),
            ('UD-80 A','UD-80A'),('BNTECHGO680','BNTECHGO 680'),('14et 40','14 et 40')]:s=s.replace(a,b)
        out.append(s)
    return ''.join(out)
