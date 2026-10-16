"""Extract named official STEP members after verifying their archives."""
from pathlib import Path
import hashlib, zipfile

OUT=Path(__file__).resolve().parents[1]/'Composants/raspberry-pi-5/3D'
SOURCES=[
    ('raspberry-pi-5-officiel-avec-graphismes.zip','1b38b554a317411bc60604f066ae004273e6c857778ecf997925ea0b56b44e0b','rpi-5b_with_graphics.step','raspberry-pi-5-officiel-avec-graphismes.step'),
    ('raspberry-pi-5-officiel-sans-graphismes.zip','6841637b4cfa97637bf34b529bfe896f24d9634b2c40b57a156781f55d88f06f','rpi-5b_no_graphics.step','raspberry-pi-5-4go-ultra-detaille.step'),
]

def main():
    for filename,expected,member,destination in SOURCES:
        archive=OUT/filename
        assert hashlib.sha256(archive.read_bytes()).hexdigest()==expected,filename
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            target=OUT/destination
            contents=z.read(member)
            if not target.exists() or hashlib.sha256(target.read_bytes()).digest()!=hashlib.sha256(contents).digest():
                temporary=target.with_suffix('.extracting')
                temporary.write_bytes(contents)
                temporary.replace(target)
            assert (OUT/'LICENSE-constructeur.txt').read_bytes()==z.read('LICENSE.txt')
        print(destination,target.stat().st_size,'bytes')

if __name__=='__main__':main()
