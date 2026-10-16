"""Write a task-local FreeCAD macro for execution in the installed GUI app.

Embedded FreeCADGui under offscreen Qt can fail native restore; the installed
FreeCAD executable has the fully initialized GUI and actual OpenGL context.
Usage: python tools/run_freecad_job.py compact_vehicle_previews.py [--render]
Launch the printed FCMacro with FreeCAD.exe (hidden background process).
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
script=ROOT/'tools'/sys.argv[1];assert script.is_file() and script.parent==(ROOT/'tools')
name=script.stem;log=ROOT/'tools/temp'/(name+'-app.log');error=ROOT/'tools/temp'/(name+'-app-error.txt')
macro=ROOT/'tools/temp'/(name+'.FCMacro')
macro.write_text(f'''import sys,os,traceback
from pathlib import Path
root=Path({str(ROOT)!r})
sys.path.insert(0,str(root/'tools'))
log=Path({str(log)!r}).open('w',encoding='utf-8')
sys.stdout=log;sys.stderr=log;sys.__stdout__=log
sys.argv={[str(script),*sys.argv[2:]]!r}
try:
    script=Path({str(script)!r})
    exec(compile(script.read_text(encoding='utf-8'),str(script),'exec'),{{'__name__':'__main__','__file__':str(script)}})
except BaseException:
    traceback.print_exc(file=log);log.flush()
    Path({str(error)!r}).write_text('See '+str(log),encoding='utf-8')
    os._exit(1)
''',encoding='utf-8')
print(macro)
