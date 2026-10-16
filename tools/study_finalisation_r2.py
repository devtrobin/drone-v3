"""Independent planar linkage solution for the R2 design review (mm, radians)."""
import math,json
import numpy as np
from scipy.optimize import brentq, minimize_scalar

W=340.; L=390.; B=40.; H=20.

def end(side,t,a):
    return np.array([side*W/2,55.])+np.array([[-math.cos(t)*side,-math.sin(t)],[ -math.sin(t)*side,math.cos(t)]])@np.array([a,B])

def drag_end(t,a):
    v=np.array([a+4,B+8]);c,s=math.cos(t),math.sin(t)
    return np.array([-W/2,55.])+np.array([[c,-s],[s,c]])@v

def other(t,a):
    p=end(-1,t,a); ell=W-2*a
    f=lambda u: float(np.linalg.norm(end(1,u,a)-p)-ell)
    return brentq(f, t-.6, t+.6)

def loss(a):
    errors=[]
    for t in np.linspace(.002,math.radians(22),40):
        u=other(t,a)
        # Positive rotation turns right, right wheel is the inner wheel.
        ideal=math.atan2(L,L/math.tan(t)-W)
        errors.append(math.degrees(u-ideal))
    return max(abs(x) for x in errors)

def calculate():
    a=float(minimize_scalar(loss,bounds=(5,24),method='bounded').x)
    a=round(a,2)
    neutral=drag_end(0,a); q0=np.array([0.,80.+H]); drag=float(np.linalg.norm(neutral-q0))
    def phi(t):
        f=lambda p: float(np.linalg.norm(drag_end(t,a)-np.array([-H*math.sin(p),80+H*math.cos(p)]))-drag)
        return brentq(f,-1.4,1.4)
    rows=[]
    for t in np.linspace(-.55,.55,1101):
        try:u=other(float(t),a); p=phi(float(t))
        except ValueError:continue
        if max(abs(t),abs(u))>math.radians(25) or abs(p)>math.radians(60):continue
        dt=1e-5; dp=(phi(t+dt)-phi(t-dt))/(2*dt)
        du=(other(t+dt,a)-other(t-dt,a))/(2*dt)
        rows.append(dict(left_deg=math.degrees(t),right_deg=math.degrees(u),servo_deg=math.degrees(p),jacobian_sum=(1+abs(du))/abs(dp)))
    return dict(pivot_track_mm=W,wheel_track_mm=400,wheelbase_mm=L,arm_inward_mm=a,arm_rear_mm=B,horn_mm=H,
      tierod_ball_centers_mm=W-2*a,draglink_ball_centers_mm=drag,max_ackermann_error_deg=loss(a),rows=rows,
      servo_deg_range=[min(x['servo_deg'] for x in rows),max(x['servo_deg'] for x in rows)],
      max_jacobian_sum=max(x['jacobian_sum'] for x in rows))

if __name__=='__main__':
    c=calculate(); print(json.dumps({k:v for k,v in c.items() if k!='rows'},indent=2));
    print(c['rows'][0]);print(c['rows'][-1])
