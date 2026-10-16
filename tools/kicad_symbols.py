"""Small S-expression/symbol helpers, adapted from Drone V1's KiCad builder."""
import json,re
class Atom(str):pass
def parse(text):
    stack=[];roots=[]
    for t in re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',text):
        if t=='(':
            n=[];(stack[-1] if stack else roots).append(n);stack.append(n)
        elif t==')':stack.pop()
        else:stack[-1].append(json.loads(t) if t.startswith('"') else Atom(t))
    assert not stack and len(roots)==1
    return roots[0]
def dump(x):
    if isinstance(x,list):return '('+' '.join(map(dump,x))+')'
    return str(x) if isinstance(x,Atom) else json.dumps(x,ensure_ascii=False)
def child(n,k):return next((x for x in n if isinstance(x,list) and x[0]==k),None)
def children(n,k):return [x for x in n if isinstance(x,list) and x[0]==k]
def get_symbol(kicad,library,name,target):
    lib=parse((kicad/'share/kicad/symbols'/(library+'.kicad_sym')).read_text(encoding='utf-8'))
    syms={s[1]:s for s in children(lib,'symbol')}
    def flatten(key):
        s=parse(dump(syms[key]));parent=child(s,'extends')
        if parent:
            base=flatten(parent[1]);props={p[1]:p for p in children(base,'property')};props.update({p[1]:p for p in children(s,'property')})
            s=[Atom('symbol'),key]+[x for x in base[2:] if not (isinstance(x,list) and x[0]=='property')]+list(props.values())
        return s
    out=flatten(name);out[1]=target
    for s in children(out,'symbol'):s[1]=target+'_'+'_'.join(s[1].split('_')[-2:])
    return out
def pin_positions(symbol):
    r={}
    for unit in children(symbol,'symbol'):
        for p in children(unit,'pin'):
            at=child(p,'at');r[child(p,'number')[1]]=(float(at[1]),float(at[2]))
    return r
