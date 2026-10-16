"""Build native KiCad schematic and routed module carrier. Run KiCad Python.

The EVMs and Pololu regulator connect through labelled flying harnesses, NOT
through an invented pin-compatible module socket. Native ERC/DRC are separate.
"""
from pathlib import Path
import csv, heapq, json, math, random, sys, uuid
import pcbnew as pcb
import kicad_symbols as light

ROOT=Path(__file__).resolve().parents[1]
B=ROOT/'Composants/carte-surveillance-electrique'
D=B/'KiCad';K=Path('D:/KiCAD');NAME='surveillance-2s-m1'
W,H=140,75
TRACK_WIDTH=.4
SIGNAL_WIDTH=.2
POWER_NETS={'AUX','GND','5V_MON','TMR_IN1','TMR_IN2','ISO5_1','ISO5_2','3V3_AUX'}
VIA_DIAMETER=.8
VIA_DRILL=.4
COPPER_NOMINAL_UM=70
NS=uuid.UUID('980f5c06-89b8-4872-a2bc-d25b260063ef')
def uid(s):return str(uuid.uuid5(NS,s))
def mm(x):return pcb.FromMM(x)
def v(x,y):return pcb.VECTOR2I(mm(x),mm(y))

def components():
    C=[]
    def add(r,val,sym,fp,nets,x,y,a=0,dnp=False):
        C.append(dict(ref=r,value=val,sym=sym,fp=fp,nets={str(i):n for i,n in nets.items()},xy=[x,y],angle=a,dnp=dnp))
    con=lambda n:f'Connector_JST:JST_XH_B{n}B-XH-A_1x0{n}_P2.50mm_Vertical'
    add('J1','AUX apres FAUX 1A','Conn2',con(2),{1:'AUX',2:'GND'},10,62)
    add('J2','Equilibrage PROTEGE','Conn3',con(3),{1:'B0_R',2:'B1_R',3:'B2_R'},10,10)
    for ch,x in [(1,38),(2,102)]:
        ref='B0_R' if ch==1 else 'B1_R';sense='B1_R' if ch==1 else 'B2_R'
        add('J'+str(ch+2),'EVM114 C'+str(ch),'EVM',con(5),{1:f'ISO5_{ch}',2:ref,3:sense,4:f'HARD_A{ch}',5:f'WARN_B{ch}'},x-5,10)
        add('M'+str(ch+2),'TMR 1-0511','TMR','Monitor:TMR1',{1:'GND',2:f'TMR_IN{ch}',4:f'ISO5_{ch}',6:ref},x-7,34)
        add('F'+str(ch),'0454.500MR 500mA T','Fuse','Monitor:Nano454', {1:'5V_MON',2:f'TMR_IN{ch}'},x-13,25)
        # HEALTHY LED: anode shunted by OUTA below hard threshold, cathode local REF.
        add('R'+str(ch*2-1),'2k2 1%','R','Resistor_SMD:R_0805_2012Metric',{1:f'ISO5_{ch}',2:f'HARD_A{ch}'},x+9,20)
        add('U'+str(ch*2-1),'VOS618A-8T HEALTHY','Opto','Package_SO:SSOP-4_4.4x2.6mm_P1.27mm', {1:f'HARD_A{ch}',2:ref,3:'GND',4:f'FAULT{ch}'},x+15,34)
        add('R'+str(ch*2),'2k2 1%','R','Resistor_SMD:R_0805_2012Metric',{1:f'ISO5_{ch}',2:f'WARN_LED{ch}'},x+21,20)
        add('U'+str(ch*2),'VOS618A-8T WARN_OK','Opto','Package_SO:SSOP-4_4.4x2.6mm_P1.27mm', {1:f'WARN_LED{ch}',2:f'WARN_B{ch}',3:'GND',4:f'WARN{ch}'},x+27,34)
        add('R'+str(4+ch),'47k','R','Resistor_SMD:R_0805_2012Metric',{1:'3V3_AUX',2:f'FAULT{ch}'},x+9,46)
        add('R'+str(6+ch),'47k DNP - cote Pi','R','Resistor_SMD:R_0805_2012Metric',{1:'3V3_PI',2:f'WARN{ch}'},x+22,46,dnp=True)
        add('C'+str(ch),'100nF X7R 25V','C','Capacitor_SMD:C_0805_2012Metric',{1:sense,2:ref},x-6,17)
        add('C'+str(ch+2),'1uF X7R 25V','C','Capacitor_SMD:C_0805_2012Metric',{1:f'ISO5_{ch}',2:ref},x+1,27)
        add('C'+str(ch+4),'1uF X7R 25V','C','Capacitor_SMD:C_0805_2012Metric',{1:f'TMR_IN{ch}',2:'GND'},x-15,31)
    add('J5','FAISCEAU Pololu2831','Buck',con(3),{1:'AUX',2:'GND',3:'5V_MON'},25,62)
    add('J6','Signaux Raspberry Pi','Pi',con(5),{1:'3V3_PI',2:'WARN1',3:'WARN2',4:'DONE',5:'GND'},93,64)
    add('J7','Vers OFF2813','Conn2',con(2),{1:'OFF',2:'GND'},124,64)
    add('U5','SN74LVC2G17DCKR','Buf','Package_TO_SOT_SMD:SOT-363_SC-70-6',{1:'FAULT1',2:'GND',3:'FAULT2',4:'BUF2',5:'3V3_AUX',6:'BUF1'},70,51)
    add('U6','MCP1703AT-3302E/MB','LDO','Package_TO_SOT_SMD:SOT-89-3',{1:'GND',2:'AUX',3:'3V3_AUX'},49,62)
    for n,x,net in [(1,66,'BUF1'),(2,77,'BUF2'),(3,86,'DONE')]:
        add('D'+str(n),'BAT54-7-F','Diode','Package_TO_SOT_SMD:SOT-23',{1:net,3:'OFF'},x,60)
    add('R9','100k DONE','R','Resistor_SMD:R_0805_2012Metric',{1:'DONE',2:'GND'},87,53)
    add('R10','100k OFF','R','Resistor_SMD:R_0805_2012Metric',{1:'OFF',2:'GND'},124,56)
    for n,val,a,b,x,y in [(7,'2u2 X7R 25V','AUX','GND',43,56),(8,'2u2 X7R 25V','3V3_AUX','GND',56,58),
                              (9,'100nF X7R 25V','3V3_AUX','GND',69,56),(10,'10uF X5R 25V','AUX','GND',18,54),
                              (11,'10uF X5R 25V','5V_MON','GND',33,54)]:
        add('C'+str(n),val,'C','Capacitor_SMD:C_0805_2012Metric',{1:a,2:b},x,y)
    return C

def custom_symbol(name,pins):
    # A functional boundary with actual pin names, rather than a generic unlabeled box.
    n=max(sum(p[2]=='L' for p in pins),sum(p[2]=='R' for p in pins));h=(n+1)*2.54/2
    out=[f'(symbol "{name}" (pin_names (offset 0.5)) (in_bom yes) (on_board yes)',
         '(property "Reference" "U" (at 0 0 0) (effects (font (size 1 1))))',
         f'(property "Value" "{name}" (at 0 0 0) (effects (font (size 1 1))))',
         f'(symbol "{name}_0_1" (rectangle (start -8.89 {h}) (end 8.89 {-h}) (stroke (width 0.254) (type default)) (fill (type background))))',
         f'(symbol "{name}_1_1"']
    index={'L':0,'R':0}
    for num,title,side,kind in pins:
        x=-12.7 if side=='L' else 12.7;y=h-2.54-index[side]*2.54;index[side]+=1
        angle=0 if side=='L' else 180
        out.append(f'(pin {kind} line (at {x} {y} {angle}) (length 3.81) (name "{title}" (effects (font (size .8 .8)))) (number "{num}" (effects (font (size .8 .8)))))')
    return light.parse(' '.join(out)+'))')

def schematic(C):
    types={'R':('Device','R'),'C':('Device','C'),'Fuse':('Device','Fuse'),
           'Conn2':('Connector_Generic','Conn_01x02'),'Conn3':('Connector_Generic','Conn_01x03')}
    syms={n:light.get_symbol(K,*pair,n) for n,pair in types.items()}
    definitions={
      'EVM':[(1,'VDD ISO5','L','power_in'),(2,'GND local','L','passive'),(3,'SENSE','L','input'),(4,'OUTA HARD','R','open_collector'),(5,'OUTB WARN_OK','R','open_collector')],
      'TMR':[(1,'-VIN','L','power_in'),(2,'+VIN','L','power_in'),(4,'+VOUT ISO','R','power_out'),(6,'-VOUT ISO','R','passive')],
      'Opto':[(1,'A','L','passive'),(2,'K','L','passive'),(3,'E','R','passive'),(4,'C','R','open_collector')],
      'Buf':[(1,'1A','L','input'),(3,'2A','L','input'),(5,'VCC','L','power_in'),(2,'GND','L','power_in'),(6,'1Y','R','output'),(4,'2Y','R','output')],
      'LDO':[(1,'GND','L','power_in'),(2,'VIN','L','power_in'),(3,'VOUT','R','power_out')],
      'Buck':[(1,'VIN','L','power_in'),(2,'GND','L','passive'),(3,'5V_MON','R','power_out')],
      'Pi':[(1,'3V3 PI','L','power_out'),(2,'WARN1 HI','R','input'),(3,'WARN2 HI','R','input'),(4,'DONE','L','output'),(5,'GND','L','passive')],
      'Diode':[(1,'A','L','passive'),(3,'K','R','passive')]}
    syms.update({n:custom_symbol(n,p) for n,p in definitions.items()})
    (D/'Monitor.kicad_sym').write_text('(kicad_symbol_lib (version 20250114) (generator monitor_m1)\n'+'\n'.join(light.dump(s) for s in syms.values())+')\n',encoding='utf-8')
    root=uid('sheet');out=[f'(kicad_sch (version 20250114) (generator "monitor_m1") (uuid "{root}") (paper "A2")',
      '(title_block (title "Surveillance 2S M1 - modules existants et porteuse") (date "2026-10-15") (rev "M1") (comment 1 "Prototype non teste - FAUX et resistances au pack obligatoires") (comment 2 "WARN actif HAUT - 5V_MON distinct du 5V Pi"))',
      '(lib_symbols '+' '.join(light.dump(s).replace(f'(symbol "{n}"',f'(symbol "Monitor:{n}"',1) for n,s in syms.items())+')']
    # Grid of electrically named component blocks, with enough space for every label.
    for i,c in enumerate(C):
        x=30.48+(i%5)*116.84;y=30.48+(i//5)*38.1
        s=syms[c['sym']];pp=light.pin_positions(s)
        out.append(f'(symbol (lib_id "Monitor:{c["sym"]}") (at {x} {y} 0) (unit 1) (in_bom yes) (on_board yes) (dnp {"yes" if c["dnp"] else "no"}) (uuid "{uid(c["ref"])}") '
          f'(property "Reference" "{c["ref"]}" (at {x} {y-13.97} 0) (effects (font (size 1 1)))) '
          f'(property "Value" "{c["value"]}" (at {x} {y-11.43} 0) (effects (font (size .9 .9)))) '
          f'(property "Footprint" "{c["fp"]}" (at {x} {y} 0) (effects (font (size 1 1)) (hide yes))) '
          f'(instances (project "{NAME}" (path "/{root}" (reference "{c["ref"]}") (unit 1)))))')
        for num,(px,py) in pp.items():
            if num not in c['nets']:continue
            a=(round(x+px,4),round(y-py,4)); direction=-1 if px<0 else 1
            if px==0:
                end=(a[0],a[1]+(-5.08 if py>0 else 5.08))
            else:end=(round(a[0]+direction*5.08,4),a[1])
            out.append(f'(wire (pts (xy {a[0]} {a[1]}) (xy {end[0]} {end[1]})) (stroke (width 0) (type default)) (uuid "{uid(c["ref"]+num+"wire")}"))')
            out.append(f'(label "{c["nets"][num]}" (at {end[0]} {end[1]} 0) (effects (font (size .8 .8)) (justify {"left" if direction>0 else "right"} bottom)) (uuid "{uid(c["ref"]+num+"label")}"))')
    # Explicit source flags, not hidden suppression of ERC.
    flag=light.get_symbol(K,'power','PWR_FLAG','PWR_FLAG')
    (D/'Monitor.kicad_sym').write_text('(kicad_symbol_lib (version 20250114) (generator monitor_m1)\n'+'\n'.join(light.dump(s) for s in [*syms.values(),flag])+')\n',encoding='utf-8')
    text=light.dump(flag).replace('(symbol "PWR_FLAG"','(symbol "Monitor:PWR_FLAG"',1)
    out[2]=out[2][:-1]+' '+text+')'
    for i,net in enumerate(['AUX','GND','TMR_IN1','TMR_IN2']):
        x=30.48+i*55.88;y=393.7
        out.append(f'(symbol (lib_id "Monitor:PWR_FLAG") (at {x} {y} 0) (unit 1) (in_bom no) (on_board no) (uuid "{uid("flag"+net)}") '
          f'(property "Reference" "#FLG0{i+1}" (at {x} {y-5.08} 0) (effects (font (size 1 1)) (hide yes))) '
          f'(property "Value" "PWR_FLAG" (at {x} {y-2.54} 0) (effects (font (size 1 1)))) '
          f'(instances (project "{NAME}" (path "/{root}" (reference "#FLG0{i+1}") (unit 1))))) '
          f'(label "{net}" (at {x} {y} 0) (effects (font (size 1 1)) (justify left bottom)) (uuid "{uid("flaglabel"+net)}"))')
    notes='Modules TI raccordes par faisceaux J3/J4, pas par une embase directe. Modifier R1/R2/R3 et cavaliers : voir configuration.md.\nB0_R/B1_R/B2_R : uniquement APRES 100 ohms / 3 W au pack. 3V3_PI : rappels WARN cote Pi.\nRA0/RA1/RA2, FAUX, M1/M2/M5 et les rappels Pi sont hors porteuse. Schema fonctionnel des interfaces, pas schema interne des modules.'
    out.append(f'(text {json.dumps(notes)} (at 215.9 381 0) (effects (font (size 1.1 1.1)) (justify left top)) (uuid "{uid("notes")}"))')
    out.append('(embedded_fonts no))')
    (D/(NAME+'.kicad_sch')).write_text('\n'.join(out),encoding='utf-8')
    (D/'sym-lib-table').write_text('(sym_lib_table (version 7) (lib (name "Monitor") (type "KiCad") (uri "${KIPRJMOD}/Monitor.kicad_sym") (options "") (descr "Symboles du prototype M1")))',encoding='utf-8')

def board(C):
    b=pcb.BOARD();b.GetDesignSettings().SetBoardThickness(mm(1.6));b.SetCopperLayerCount(2)
    nets={}
    for n in sorted({n for c in C for n in c['nets'].values()}):
        z=pcb.NETINFO_ITEM(b,'/'+n);b.Add(z);nets[n]=z
    pads=[];keep=[]
    for c in C:
        lib,name=c['fp'].split(':')
        if lib=='Monitor' and name=='Nano454':
            f=pcb.FOOTPRINT(b)
            for num,x in [(1,-2.85),(2,2.85)]:
                p=pcb.PAD(f);p.SetNumber(str(num));p.SetAttribute(pcb.PAD_ATTRIB_SMD);p.SetShape(pcb.PAD_SHAPE_ROUNDRECT)
                p.SetSize(v(2.2,3));p.SetRoundRectRadiusRatio(.1)
                ls=pcb.LSET()
                for layer in [pcb.F_Cu,pcb.F_Paste,pcb.F_Mask]:ls.AddLayer(layer)
                p.SetLayerSet(ls);p.SetPosition(v(x,0));f.Add(p)
            for layer,margin in [(pcb.F_Fab,0),(pcb.F_CrtYd,.5)]:
                s=pcb.PCB_SHAPE(f);s.SetShape(pcb.SHAPE_T_RECT);s.SetStart(v(-3.05-margin,-1.35-margin));s.SetEnd(v(3.05+margin,1.35+margin));s.SetWidth(mm(.1));s.SetLayer(layer);f.Add(s)
            f.SetFPID(pcb.LIB_ID('Monitor','Nano454'))
        elif lib=='Monitor':
            f=pcb.FOOTPRINT(b)
            for num,x in [(1,0),(2,2.54),(4,7.62),(6,12.7)]:
                p=pcb.PAD(f);p.SetNumber(str(num));p.SetAttribute(pcb.PAD_ATTRIB_PTH);p.SetShape(pcb.PAD_SHAPE_CIRCLE)
                p.SetSize(v(1.7,1.7));p.SetDrillSize(v(.9,.9));p.SetLayerSet(pcb.LSET.AllCuMask());p.SetPosition(v(x,0));f.Add(p)
            for layer in [pcb.F_Fab,pcb.F_CrtYd]:
                s=pcb.PCB_SHAPE(f);s.SetShape(pcb.SHAPE_T_RECT);s.SetStart(v(-2.15,-2.5));s.SetEnd(v(14.85,5.12));s.SetWidth(mm(.1));s.SetLayer(layer);f.Add(s)
            # No copper beneath the back of the body; pin fanouts leave through the front.
            xx,yy=c['xy'];keep.append([xx-2.4,yy+.9,xx+15.1,yy+5.5])
            f.SetFPID(pcb.LIB_ID('Monitor','TMR1'))
        else:
            f=pcb.FootprintLoad(str(K/'share/kicad/footprints'/(lib+'.pretty')),name)
            assert f,c['fp']
            f.SetFPID(pcb.LIB_ID(lib,name))
        f.SetReference(c['ref']);f.SetValue(c['value']);f.Value().SetVisible(False)
        f.SetUuid(pcb.KIID(uid(c['ref'])));f.SetPath(pcb.KIID_PATH('/'+uid('sheet')+'/'+uid(c['ref'])))
        if c['dnp']:f.SetDNP(True)
        b.Add(f);f.SetPosition(v(*c['xy']));f.SetOrientationDegrees(c['angle'])
        f.Reference().SetVisible(False)
        for p in f.Pads():
            n=p.GetNumber()
            if n in c['nets']:p.SetNet(nets[c['nets'][n]])
            else:continue
            pos=p.GetPosition();size=p.GetSize();bounds=p.GetBoundingBox()
            pads.append(dict(ref=c['ref'],num=n,net=c['nets'][n],x=pcb.ToMM(pos.x),y=pcb.ToMM(pos.y),
              sx=pcb.ToMM(bounds.GetWidth()),sy=pcb.ToMM(bounds.GetHeight()),hole=pcb.ToMM(p.GetDrillSize().x),tht=p.GetAttribute()==pcb.PAD_ATTRIB_PTH))
            pads[-1]['bounds']=[pcb.ToMM(bounds.GetX()),pcb.ToMM(bounds.GetY()),pcb.ToMM(bounds.GetRight()),pcb.ToMM(bounds.GetBottom())]
            pads[-1]['shape']=int(p.GetShape());pads[-1]['size_local_mm']=[pcb.ToMM(size.x),pcb.ToMM(size.y)];pads[-1]['angle']=p.GetOrientationDegrees();pads[-1]['corner_radius_mm']=pcb.ToMM(p.GetRoundRectCornerRadius())
            poly=p.GetEffectivePolygon(pcb.F_Cu)
            pads[-1]['polygons']=[[[pcb.ToMM(o.CPoint(i).x),pcb.ToMM(o.CPoint(i).y)] for i in range(o.PointCount())] for o in [poly.COutline(j) for j in range(poly.OutlineCount())]]
        if lib=='Monitor':
            local=D/'Monitor.pretty';local.mkdir(exist_ok=True)
            pcb.PCB_IO_MGR.FindPlugin(pcb.PCB_IO_MGR.KICAD_SEXP).FootprintSave(str(local),f)
    for i,(x,y) in enumerate([(4,4),(136,4),(4,71),(136,71)]):
        f=pcb.FootprintLoad(str(K/'share/kicad/footprints/MountingHole.pretty'),'MountingHole_3.2mm_M3')
        f.SetReference('H'+str(i+1));f.SetBoardOnly(True);f.SetExcludedFromBOM(True);f.Reference().SetVisible(False);f.Value().SetVisible(False);b.Add(f);f.SetPosition(v(x,y))
    for a,z in [((0,0),(W,0)),((W,0),(W,H)),((W,H),(0,H)),((0,H),(0,0))]:
        s=pcb.PCB_SHAPE();s.SetShape(pcb.SHAPE_T_SEGMENT);s.SetStart(v(*a));s.SetEnd(v(*z));s.SetWidth(mm(.05));s.SetLayer(pcb.Edge_Cuts);b.Add(s)
    for text,x,y in [('SURVEILLANCE 2S M1 - PROTOTYPE',70,70),('J2 B0/B1/B2_R',17,4),('EVM C1 / faisceau',46,5),('EVM C2 / faisceau',109,5),('WARN HAUT = ALERTE',111,72)]:
        t=pcb.PCB_TEXT(b);t.SetText(text);t.SetPosition(v(x,y));t.SetTextSize(v(.9,.9));t.SetTextThickness(mm(.13));t.SetLayer(pcb.F_SilkS);b.Add(t)
    # Functional keepout is persisted natively and in exported layout data.
    for x1,y1,x2,y2 in keep:
        z=pcb.ZONE(b);z.SetIsRuleArea(True);z.SetLayerSet(pcb.LSET.AllCuMask());z.SetDoNotAllowTracks(True);z.SetDoNotAllowVias(True);z.SetDoNotAllowZoneFills(True)
        o=z.Outline();o.NewOutline()
        for x,y in [(x1,y1),(x2,y1),(x2,y2),(x1,y2)]:o.Append(mm(x),mm(y))
        b.Add(z)
    return b,nets,pads,keep

def route(b,nets,pads,keep):
    # Conservative grid + layer transitions; final native DRC remains authoritative.
    step=.1;tw=TRACK_WIDTH;clear=.17;nx,ny=round(W/step)+1,round(H/step)+1
    def cell(x,y,l=0):return (round(x/step),round(y/step),l)
    hard=set()
    for x1,y1,x2,y2 in keep:
        for x in range(round((x1-.2)/step),round((x2+.2)/step)+1):
            for y in range(round((y1-.2)/step),round((y2+.2)/step)+1):
                hard.add((x,y,0));hard.add((x,y,1))
    for hx,hy in [(4,4),(136,4),(4,71),(136,71)]:
        for x in range(round((hx-2.8)/step),round((hx+2.8)/step)+1):
            for y in range(round((hy-2.8)/step),round((hy+2.8)/step)+1):
                if math.hypot(x*step-hx,y*step-hy)<2.5:
                    hard.add((x,y,0));hard.add((x,y,1))
    widths={n:(TRACK_WIDTH if n in POWER_NETS else SIGNAL_WIDTH) for n in nets}
    padareas={}
    for width in [SIGNAL_WIDTH,TRACK_WIDTH]:
        padarea={n:set() for n in nets}
        for p in pads:
            margin=width/2+clear+.04;x1,y1,x2,y2=p['bounds']
            for x in range(round((x1-margin)/step),round((x2+margin)/step)+1):
                for y in range(round((y1-margin)/step),round((y2+margin)/step)+1):
                    for l in ([0,1] if p['tht'] else [0]):padarea[p['net']].add((x,y,l))
        padareas[width]=padarea
    grouped={n:[p for p in pads if p['net']==n] for n in nets}
    rng=random.Random(714);best=None
    for attempt in range(8):
        occ={n:set() for n in nets};segments=[];vias=[];fails=[]
        order=sorted(nets,key=lambda n:(n=='GND',-len(grouped[n])))
        if attempt:rng.shuffle(order);order.sort(key=lambda n:n=='GND')
        for n in order:
            tw=widths[n];padarea=padareas[tw]
            pp=grouped[n];connected=pp[:1];remaining=pp[1:]
            blocked=hard|set().union(*(padarea[k]|occ[k] for k in nets if k!=n))
            while remaining:
                _,a,z=min(((math.hypot(a['x']-z['x'],a['y']-z['y']),a,z) for a in connected for z in remaining),key=lambda t:t[0])
                start,end=cell(a['x'],a['y']),cell(z['x'],z['y'])
                # Pad centers may fall within their own copper, never foreign copper.
                heap=[(0,0,start)];dist={start:0};parent={};limit=0
                while heap:
                    _,cost,pos=heapq.heappop(heap)
                    if pos==end:break
                    if cost!=dist.get(pos):continue
                    limit+=1
                    if limit>450000:break
                    x,y,l=pos
                    for dx,dy,dl in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1)]:
                        nxt=(x+dx,y+dy,1-l if dl else l)
                        if not (10<nxt[0]<nx-10 and 10<nxt[1]<ny-10) or nxt in blocked:continue
                        extra=1
                        if dl:
                            # A via requires extra radial clearance on BOTH layers.
                            ok=True
                            for ox,oy in [(0,0),(3,0),(-3,0),(0,3),(0,-3),(2,2),(2,-2),(-2,2),(-2,-2)]:
                                if (x+ox,y+oy,0) in blocked or (x+ox,y+oy,1) in blocked:ok=False;break
                            if not ok:continue
                            extra=35
                        nc=cost+extra
                        if nc<dist.get(nxt,1e20):
                            dist[nxt]=nc;parent[nxt]=pos
                            h=abs(nxt[0]-end[0])+abs(nxt[1]-end[1])+35*(nxt[2]!=end[2])
                            heapq.heappush(heap,(nc+h,nc,nxt))
                if end not in parent:
                    fails.append([n,a['ref'],z['ref']]);connected.append(z);remaining.remove(z);continue
                path=[end]
                while path[-1]!=start:path.append(parent[path[-1]])
                path.reverse();points=[(a['x'],a['y'],0)];last=None
                for j in range(1,len(path)):
                    aa,bb=path[j-1],path[j]
                    if aa[2]!=bb[2]:
                        points.append((aa[0]*step,aa[1]*step,aa[2]));points.append((bb[0]*step,bb[1]*step,bb[2]));vias.append((n,bb[0]*step,bb[1]*step));last=None
                    else:
                        direct=(bb[0]-aa[0],bb[1]-aa[1])
                        if last and direct!=last:points.append((aa[0]*step,aa[1]*step,aa[2]))
                        last=direct
                points.append((z['x'],z['y'],0))
                segments.extend((n,p,q) for p,q in zip(points,points[1:]) if p!=q and p[2]==q[2])
                for x,y,l in path:
                    for dx in range(-8,9):
                        for dy in range(-8,9):
                            if math.hypot(dx,dy)*step<tw/2+TRACK_WIDTH/2+clear+.06:occ[n].add((x+dx,y+dy,l))
                for vn,vx,vy in vias:
                    if vn!=n:continue
                    for dx in range(-7,8):
                        for dy in range(-7,8):
                            if math.hypot(dx,dy)*step<VIA_DIAMETER/2+tw/2+clear+.06:
                                for l in [0,1]:occ[n].add((round(vx/step)+dx,round(vy/step)+dy,l))
                connected.append(z);remaining.remove(z)
        print('attempt',attempt,'unrouted',len(fails),fails,flush=True)
        if best is None or len(fails)<len(best[2]):best=(segments,vias,fails)
        if not fails:break
    # Consolidate layer transitions landing on plated holes, and near-duplicate vias.
    unique=[]
    for n,x,y in sorted(set((n,round(x,3),round(y,3)) for n,x,y in best[1])):
        target=next(((p['x'],p['y']) for p in pads if p['tht'] and p['net']==n and math.hypot(x-p['x'],y-p['y'])<p['hole']/2+.45),None)
        if target is None:target=next(((xx,yy) for nn,xx,yy in unique if nn==n and math.hypot(x-xx,y-yy)<.66),None)
        if target is not None:
            for l in [0,1]:
                if math.hypot(x-target[0],y-target[1])>1e-6:best[0].append((n,(x,y,l),(target[0],target[1],l)))
        else:unique.append((n,x,y))
    best=(best[0],unique,best[2])
    for n,a,z in best[0]:
        t=pcb.PCB_TRACK(b);t.SetStart(v(a[0],a[1]));t.SetEnd(v(z[0],z[1]));t.SetWidth(mm(widths[n]));t.SetLayer(pcb.F_Cu if a[2]==0 else pcb.B_Cu);t.SetNet(nets[n]);b.Add(t)
    for n,x,y in set(best[1]):
        t=pcb.PCB_VIA(b);t.SetPosition(v(x,y));t.SetWidth(mm(VIA_DIAMETER));t.SetDrill(mm(VIA_DRILL));t.SetViaType(pcb.VIATYPE_THROUGH);t.SetLayerPair(pcb.F_Cu,pcb.B_Cu);t.SetNet(nets[n]);b.Add(t)
    return dict(segments=best[0],vias=best[1],unrouted=best[2],width=TRACK_WIDTH,signal_width=SIGNAL_WIDTH,width_by_net=widths,clearance=clear,via_diameter=VIA_DIAMETER,via_drill=VIA_DRILL,copper_nominal_um=COPPER_NOMINAL_UM)

def main():
    D.mkdir(parents=True,exist_ok=True);C=components();b,n,p,k=board(C);schematic(C)
    project={'meta':{'filename':NAME+'.kicad_pro','version':1},'board':{'design_settings':{'rules':{'min_clearance':.15,'min_track_width':SIGNAL_WIDTH,'min_copper_edge_clearance':.5,'min_through_hole_diameter':VIA_DRILL,'min_hole_clearance':.25},'rule_severities':{},'track_widths':[SIGNAL_WIDTH,TRACK_WIDTH]}},
             'net_settings':{'classes':[{'name':'Default','clearance':.15,'track_width':SIGNAL_WIDTH,'via_diameter':VIA_DIAMETER,'via_drill':VIA_DRILL}],'version':3}}
    (D/(NAME+'.kicad_pro')).write_text(json.dumps(project,indent=2),encoding='utf-8')
    (D/'fp-lib-table').write_text('(fp_lib_table (version 7) (lib (name "Monitor") (type "KiCad") (uri "${KIPRJMOD}/Monitor.pretty") (options "") (descr "Empreinte TMR selon plan constructeur")))',encoding='utf-8')
    r=route(b,n,p,k);pcb.SaveBoard(str(D/(NAME+'.kicad_pcb')),b)
    (D/'connectivite-attendue.json').write_text(json.dumps({c['ref']:c['nets'] for c in C},indent=2),encoding='utf-8')
    (D/'implantation.json').write_text(json.dumps(dict(revision='M1P',board_mm=[W,H,1.6],components=C,pads=p,keepouts=k,routing=r),indent=2),encoding='utf-8')
    with (D/'nomenclature.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f,delimiter=';');w.writerow(['Repere','Valeur','Empreinte','Montage'])
        for c in C:w.writerow([c['ref'],c['value'],c['fp'],'DNP - rappel a monter cote Pi' if c['dnp'] else 'Prototype a qualifier'])
    assert not r['unrouted'],r['unrouted']
    print('Saved',len(C),'components',len(n),'nets',len(r['segments']),'segments',len(r['vias']),'vias',flush=True)
if __name__=='__main__':main()
