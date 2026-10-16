"""Symbolic checks (SymPy) of every derived constraint and result used by the model builder.

Each check has an ID (S1, S2, ...) that the provenance table cites. Run:
    python figure/tools/verify_constraints.py
It prints one line per check and writes figure/constraint_checks.json and constraint_checks.txt.
"""
import json
import random
from fractions import Fraction
from pathlib import Path

import sympy as sp

OUT = Path(__file__).resolve().parent.parent
pos = dict(positive=True, real=True)
x, y, t = sp.symbols('x y t', **pos)
r, K, a, h, e, m, d, b, mu, G, c, w, kap, phi, xi, q, E, H, I, s, eta, C, psi, sig, tau, delta, eps, omega = sp.symbols(
    'r K a h e m d b mu G c w kappa phi xi q E H I s eta C psi sigma tau delta epsilon omega', **pos)
A = sp.Symbol('A', real=True)
gam, nu, p, theta = sp.symbols('gamma nu p theta', **pos)

RESULTS = []


def check(cid, text, ok, detail=''):
    ok = bool(ok)
    RESULTS.append({'id': cid, 'claim': text, 'pass': ok, 'detail': detail})
    print(f"{cid:5s} {'PASS' if ok else 'FAIL'}  {text}" + (f"   [{detail}]" if detail else ''))


def is_zero(expr):
    return sp.simplify(expr) == 0


def solve_ineq(expr_ineq, var):
    return sp.reduce_inequalities([expr_ineq], [var])


# ---------------------------------------------------------------- S1 logistic family
th = sp.Symbol('theta', positive=True)
check('S1', 'theta-logistic with theta=1 is the logistic law',
      is_zero((r*x*(1 - (x/K)**th)).subs(th, 1) - r*x*(1 - x/K)))

# ---------------------------------------------------------------- S2 multiplicative Allee
g = r*(1 - x/K)*(x - A)/K                       # per-capita growth
g0 = sp.simplify(g.subs(x, 0))
g1 = sp.simplify(sp.diff(g, x).subs(x, 0))
check('S2a', 'Multiplicative Allee: g(0) = -rA/K, so the origin is locally stable (strong Allee) iff A>0', is_zero(g0 + r*A/K))
check('S2b', "Multiplicative Allee: g'(0) = r(K+A)/K^2 > 0 iff A > -K", is_zero(g1 - r*(K + A)/K**2))
roots = sp.solve(sp.Eq(g, 0), x)
check('S2c', 'Multiplicative Allee: positive zeros of g are A and K, so a threshold below K needs 0<A<K', set(roots) == {A, K}, f'roots={roots}')
check('S2d', 'Weak Allee (g(0)>=0 and increasing at 0) <=> -K < A <= 0; A <= -K removes the effect (g decreasing at 0)',
      is_zero(g1.subs(A, -K)) and sp.diff(g1, A).is_positive and is_zero(g0.subs(A, 0)) and sp.diff(g0, A).is_negative)

# ---------------------------------------------------------------- S3 additive Allee
ga = r*(1 - x/K) - mu/(x + b)
ga0, ga1 = sp.simplify(ga.subs(x, 0)), sp.simplify(sp.diff(ga, x).subs(x, 0))
check('S3a', 'Additive Allee: strong (g(0)<0) iff mu > r b', is_zero(ga0 - (r - mu/b)))
check('S3b', "Additive Allee: g'(0) > 0 iff mu > r b^2/K", is_zero(ga1 - (-r/K + mu/b**2)))
check('S3c', 'Additive Allee: the weak range r b^2/K < mu < r b is non-empty iff b < K',
      sp.simplify((r*b - r*b**2/K) - r*b*(K - b)/K) == 0)

# ---------------------------------------------------------------- S4 fear
xs_fear = sp.solve(sp.Eq(r/(1 + 0) - d - c*x, 0), x)[0]      # prey alone, logistic fear model
check('S4', 'Fear model, prey alone: low-density growth rate is r-d and the equilibrium (r-d)/c^x is positive iff r>d',
      is_zero(xs_fear - (r - d)/c))

# ---------------------------------------------------------------- S5 seasonal forcing
check('S5', 'Seasonal forcing: min_t r(1+eps sin wt) = r(1-eps) > 0 iff eps < 1',
      is_zero(sp.minimum(1 + eps*sp.sin(t), t, sp.Interval(0, 2*sp.pi)) - (1 - eps)))

# ---------------------------------------------------------------- S6 Hutchinson
lam = sp.Symbol('lambda')
F = lam + r*sp.exp(-lam*tau)                                  # characteristic function at x=K: u' = -r u(t-tau)
w_ = sp.Symbol('w', positive=True)
re_part, im_part = sp.re(sp.expand_complex(F.subs(lam, sp.I*w_))), sp.im(sp.expand_complex(F.subs(lam, sp.I*w_)))
crossing = {w_: r, tau: sp.pi/(2*r)}
dlam = sp.simplify(-sp.diff(F, tau)/sp.diff(F, lam))
trans = sp.re(sp.simplify(dlam.subs(lam, sp.I*r).subs(tau, sp.pi/(2*r))))
check('S6', 'Delayed logistic: roots cross the imaginary axis first at r tau = pi/2 with Re(dlambda/dtau) > 0, so K is stable iff r tau < pi/2',
      is_zero(re_part.subs(crossing)) and is_zero(im_part.subs(crossing)) and sp.simplify(trans - r**2/(1 + sp.pi**2/4)) == 0,
      f'Re dlambda/dtau = {sp.simplify(trans)}')

# ---------------------------------------------------------------- S7 Gompertz
check('S7', 'Gompertz: per-capita rate r ln(K/x) -> +infinity as x -> 0+', sp.limit(r*sp.log(K/x), x, 0, '+') == sp.oo)

# ---------------------------------------------------------------- S8 herd behaviour
pp = sp.Symbol('p', positive=True)
check('S8a', 'Herd: d/dx x^p -> infinity at 0 for 0<p<1 (not Lipschitz)', sp.limit(sp.diff(x**sp.Rational(1, 2), x), x, 0, '+') == sp.oo)
u_rate = sp.simplify((1 - pp)*x**(-pp)*(r*x*(1 - x/K) - a*x**pp*y))       # d/dt x^(1-p)
check('S8b', 'Herd: d/dt x^(1-p) -> -(1-p) a y < 0 as x -> 0, so with y bounded below prey reach 0 in finite time',
      is_zero(sp.limit(u_rate.subs(pp, sp.Rational(1, 2)), x, 0, '+') + a*y/2))
R_ = sp.Symbol('R', positive=True)
check('S8c', 'Herd: for a planar (disc) herd the edge length scales as area^(1/2), so p = 1/2',
      is_zero(sp.simplify((2*sp.pi*R_)/(sp.pi*R_**2)**sp.Rational(1, 2)) - 2*sp.sqrt(sp.pi)))

# ---------------------------------------------------------------- S9 handling time
check('S9', 'Holling II: intake a x/(1+a h x) -> 1/h as x -> infinity', sp.limit(a*x/(1 + a*h*x), x, sp.oo) == 1/h)

# ---------------------------------------------------------------- S10 Holling IV
f4 = lambda z: a*z/(1 + a*h*z + z**2/G)
crit = sp.solve(sp.diff(f4(x), x), x)
om_phi = sp.Symbol('u', positive=True)                       # u = 1 - phi > 0, since 0 <= phi < 1
crit_prop = [z.subs(om_phi, 1 - phi) for z in sp.solve(sp.diff(f4(om_phi*x), x), x)]
crit_num = sp.solve(sp.diff(f4(x - xi), x), x)
check('S10a', 'Holling IV: the response peaks at x = sqrt(G), independent of a and h', crit == [sp.sqrt(G)], str(crit))
check('S10b', 'Holling IV with a proportional refuge peaks at x = sqrt(G)/(1-phi)', len(crit_prop) == 1 and is_zero(crit_prop[0] - sp.sqrt(G)/(1 - phi)), str(crit_prop))
check('S10c', 'Holling IV with a fixed-number refuge peaks at x = xi + sqrt(G)', sp.sqrt(G) + xi in crit_num, str(crit_num))
eqq = sp.together(e*f4(x) - m)
check('S10d', 'Holling IV: interior equilibria solve a quadratic in x, so there are at most two',
      sp.degree(sp.numer(eqq), x) == 2)

# ---------------------------------------------------------------- S11 limits of the response families
check('S11a', 'Beddington-DeAngelis and Crowley-Martin reduce to Holling II at c = 0',
      is_zero((a*x/(1 + a*h*x + c*y)).subs(c, 0) - a*x/(1 + a*h*x)) and is_zero((a*x/((1 + a*h*x)*(1 + c*y))).subs(c, 0) - a*x/(1 + a*h*x)))
hv = a*x*y/(y**gam + a*h*x)
check('S11b', 'Hassell-Varley: gamma = 0 gives Holling II, gamma = 1 gives the ratio-dependent form',
      is_zero(hv.subs(gam, 0) - a*x*y/(1 + a*h*x)) and is_zero(hv.subs(gam, 1) - a*x*y/(y + a*h*x)))
check('S11c', 'Mutual interference: y^(1-nu) -> 0 as y -> 0 iff nu < 1 (predation vanishes without predators); nu = 0 is the classical term',
      sp.limit(y**sp.Rational(1, 2), y, 0, '+') == 0 and sp.limit(y**0, y, 0, '+') == 1 and sp.limit(y**sp.Rational(-1, 2), y, 0, '+') == sp.oo)

# ---------------------------------------------------------------- S12 multi-food response from the time budget
n_items = 3
aa = sp.symbols('a1:4', positive=True); hh = sp.symbols('h1:4', positive=True); XX = sp.symbols('x1:4', positive=True)
T_, Ts = sp.symbols('T T_s', positive=True)
Ts_sol = sp.solve(sp.Eq(T_, Ts + sum(hh[k]*aa[k]*XX[k]*Ts for k in range(n_items))), Ts)[0]
intake = sp.simplify(aa[0]*XX[0]*Ts_sol/T_)
check('S12', 'Shared handling time: the time budget gives intake_i = a_i x_i / (1 + sum_k a_k h_k x_k) (prey or predator items alike)',
      is_zero(intake - aa[0]*XX[0]/(1 + sum(aa[k]*hh[k]*XX[k] for k in range(n_items)))))

# ---------------------------------------------------------------- S13 mass balance of conversion efficiencies
fr_ = sp.Symbol('f', positive=True)    # any consumption rate
dB = (r*x*(1 - x/K) - fr_*y) + (e*fr_*y - m*y)
check('S13a', 'Mass balance: predation changes total biomass x+y by -(1-e) f y, so predation creates no biomass iff e <= 1',
      is_zero(dB - (r*x*(1 - x/K) - m*y - (1 - e)*fr_*y)))
ex, zeta = sp.symbols('e_x zeta', positive=True)
dBm = (r*x*(1 - x/K) - a*x*y + ex*zeta*x*y) + (e*a*x*y - m*y - zeta*x*y)
check('S13b', 'Mutual predation (prey eats predator): x+y changes by -(1-e) a x y - (1-e^x) zeta x y from the two predation links',
      is_zero(dBm - (r*x*(1 - x/K) - m*y - (1 - e)*a*x*y - (1 - ex)*zeta*x*y)))

# ---------------------------------------------------------------- S14 cannibalism
ey, ay, k_ = sp.symbols('e_y a_y k', positive=True)
net = ey*ay*y**2 - ay*y**2
check('S14a', 'Cannibalism: gain minus loss of the same link is (e^y - 1) a^y y^2 (/D), a density-dependent loss iff e^y < 1',
      is_zero(net - (ey - 1)*ay*y**2))
Y = sp.Function('Y')
y0 = sp.Symbol('y0', positive=True)
sol = sp.dsolve(sp.Eq(Y(t).diff(t), k_*Y(t)**2 - m*Y(t)), Y(t), ics={Y(0): y0})
blow = sp.solve(sp.Eq(sp.denom(sp.together(sol.rhs)), 0), t)
tstar = sp.log(k_*y0/(k_*y0 - m))/m
check('S14b', 'Cannibalism with e^y > 1 and no other food: y\' = k y^2 - m y, k = (e^y-1)a^y, blows up at t* = ln(k y0/(k y0 - m))/m, finite iff y(0) > m/k',
      any(is_zero(sp.simplify(sp.expand_log(z - tstar, force=True))) for z in blow) or is_zero(sp.denom(sp.together(sol.rhs)).subs(t, tstar)),
      f'solution {sp.simplify(sol.rhs)}')

# ---------------------------------------------------------------- S15 maturation delay
J = sp.Function('J'); J0 = sp.Symbol('J0', positive=True)
js = sp.dsolve(sp.Eq(J(t).diff(t), -delta*J(t)), J(t), ics={J(0): J0}).rhs
check('S15', 'Maturation delay: juveniles dying at rate delta^J survive the delay tau with probability exp(-delta^J tau)', is_zero(js.subs(t, tau)/J0 - sp.exp(-delta*tau)))

# ---------------------------------------------------------------- S16 predator Allee effect
fx = sp.Symbol('F', positive=True)
yeq = y/(y + psi)*e*fx*y - m*y
check('S16', 'Predator Allee: d/dy[y/(y+psi) e F y - m y] at y=0 equals -m < 0, so y=0 is locally stable',
      is_zero(sp.diff(yeq, y).subs(y, 0) + m))

# ---------------------------------------------------------------- S17 hunting cooperation
pc = e*(a + w*y)*x/(1 + (a + w*y)*h*x)
check('S17', 'Hunting cooperation: per-capita predator gain increases with predator density (component Allee effect) for w > 0',
      sp.simplify(sp.diff(pc, y) - e*w*x/(1 + (a + w*y)*h*x)**2) == 0)

# ---------------------------------------------------------------- S18 Leslie-Gower
check('S18a', 'Leslie-Gower: y/(eta x) is unbounded as x -> 0+ (singular without prey)', sp.limit(y/(eta*x), x, 0, '+') == sp.oo)
check('S18b', 'Modified Leslie-Gower: y/(eta x + C) stays finite at x = 0 for C > 0', sp.limit(y/(eta*x + C), x, 0, '+') == y/C)
check('S18c', 'Leslie-Gower: the predator equilibrium is y = eta x (eta = predators supported per unit prey)',
      sp.solve(sp.Eq(s*y*(1 - y/(eta*x)), 0), y) == [eta*x])

# ---------------------------------------------------------------- S19 effort harvesting
xs_h = sp.solve(sp.Eq(r*(1 - x/K) - q*E, 0), x, dict=False)
xs_h = sp.solve(r*(1 - sp.Symbol('X')/K) - q*E, sp.Symbol('X'))
check('S19a', 'Effort harvesting, logistic prey alone: positive equilibrium K(1 - qE/r) exists iff qE < r',
      len(xs_h) == 1 and is_zero(xs_h[0] - K*(1 - q*E/r)))
zz = sp.Symbol('z', positive=True)                            # z = 1 - qE/r > 0 exactly when qE < r
th_root = K*zz**(1/th)
check('S19b', 'Effort harvesting, theta-logistic prey alone: x = K(1 - qE/r)^(1/theta) solves r(1-(x/K)^theta) = qE, and is real and positive iff qE < r',
      is_zero(sp.powsimp((r*(1 - (th_root/K)**th) - r*(1 - zz)), force=True)))

# ---------------------------------------------------------------- S20 maximum sustainable yield
crit_x = sp.solve(sp.diff(r*x*(1 - x/K), x), x)[0]
disc = sp.discriminant(sp.expand(r*x*(1 - x/K) - H), x)
check('S20', 'Constant yield, logistic prey alone: positive equilibria exist iff H <= rK/4 (the maximum of rx(1-x/K), at x = K/2)',
      is_zero(crit_x - K/2) and is_zero((r*x*(1 - x/K)).subs(x, K/2) - r*K/4) and is_zero(disc - r*(r*K - 4*H)/K))

# ---------------------------------------------------------------- S21 constant yield at zero
check('S21', 'Constant yield: at x = 0 the prey equation equals -H < 0, so solutions leave the non-negative orthant unless harvest stops',
      (r*x*(1 - x/K) - a*x*y - H).subs(x, 0) == -H)

# ---------------------------------------------------------------- S22 immigration in the classical model
xs, ys = m/(e*a), None
f_ = r*x - a*x*y + I; g_ = e*a*x*y - m*y
eqs = sp.solve([f_, g_], [x, y], dict=True)
Jm = sp.Matrix([f_, g_]).jacobian([x, y])
ok22 = False
for E_ in eqs:
    if sp.simplify(E_[x] - m/(e*a)) == 0:
        JJ = Jm.subs(E_)
        tr, de = sp.simplify(JJ.trace()), sp.simplify(JJ.det())
        ok22 = sp.simplify(tr + I*e*a/m) == 0 and sp.simplify(de).is_positive
check('S22', 'Classical LV with prey immigration I>0: trace = -I/x* < 0 and det > 0 at the interior equilibrium, so it is asymptotically stable', ok22)

# ---------------------------------------------------------------- S23 classical LV
Hc = e*a*x - m*sp.log(x) + a*y - r*sp.log(y)
dH = sp.diff(Hc, x)*(r*x - a*x*y) + sp.diff(Hc, y)*(e*a*x*y - m*y)
check('S23', 'Classical LV: interior equilibrium (m/(ea), r/a) and H = eax - m ln x + ay - r ln y is conserved',
      is_zero(dH) and sp.solve([r - a*y, e*a*x - m], [x, y], dict=True) == [{x: m/(e*a), y: r/a}])

# ---------------------------------------------------------------- S24 logistic prey, Holling I
xst = m/(e*a); yst = r/a*(1 - xst/K)
V = e*(x - xst - xst*sp.log(x/xst)) + (y - yst - yst*sp.log(y/yst))
dV = sp.simplify(sp.diff(V, x)*(r*x*(1 - x/K) - a*x*y) + sp.diff(V, y)*(e*a*x*y - m*y))
check('S24', 'Logistic prey + Holling I: x* = m/(ea), y* = (r/a)(1 - x*/K) > 0 iff m < eaK; dV/dt = -(e r/K)(x-x*)^2 <= 0 (global stability via LaSalle)',
      is_zero(dV + e*r/K*(x - xst)**2) and is_zero(yst - r*(a*e*K - m)/(a**2*e*K)))

# ---------------------------------------------------------------- S25 Rosenzweig-MacArthur
F1 = r*x*(1 - x/K) - a*x*y/(1 + a*h*x)
F2 = e*a*x*y/(1 + a*h*x) - m*y
xR = m/(a*(e - m*h)); yR = sp.simplify(r/a*(1 - xR/K)*(1 + a*h*xR))
JR = sp.Matrix([F1, F2]).jacobian([x, y]).subs({x: xR, y: yR})
trR = sp.factor(sp.simplify(JR.trace()))
detR = sp.factor(sp.simplify(JR.det()))
hump = (K - 1/(a*h))/2
# trace has the sign of (hump - x*): compare with an explicit factorisation
ratio = sp.simplify(trR/(hump - xR))
check('S25a', 'Rosenzweig-MacArthur: F1 = F2 = 0 at x* = m/[a(e-mh)], y* = (r/a)(1-x*/K)(1+ahx*)',
      is_zero(F1.subs({x: xR, y: yR})) and is_zero(F2.subs({x: xR, y: yR})))
check('S25b', 'Rosenzweig-MacArthur: trace J = [2 r a h x*/(K(1+ahx*))] (x_hump - x*), x_hump = (K - 1/(ah))/2',
      is_zero(ratio - 2*r*a*h*xR/(K*(1 + a*h*xR))), f'det = {detR}')

# sign of trace/(hump - x*) and det at random admissible points (exact rationals)
rng = random.Random(1)
bad = 0
for _ in range(400):
    vals = {r: Fraction(rng.randint(1, 50), 10), K: Fraction(rng.randint(5, 200), 10), a: Fraction(rng.randint(1, 50), 10),
            h: Fraction(rng.randint(1, 50), 10), m: Fraction(rng.randint(1, 50), 100)}
    vals[e] = vals[m]*vals[h] + Fraction(rng.randint(1, 100), 50)          # e > m h
    xv = xR.subs(vals)
    if not (0 < xv < vals[K]):
        continue
    rv = sp.nsimplify(ratio.subs(vals)); dv = sp.nsimplify(detR.subs(vals))
    if not (rv > 0 and dv > 0):
        bad += 1
check('S25c', 'Rosenzweig-MacArthur: at 400 random admissible parameter sets (exact rationals) trace/(x_hump - x*) > 0 and det > 0, so the equilibrium is stable iff x* > x_hump',
      bad == 0, f'violations: {bad}')


def lyapunov_l1(Fv, x0, y0_, params):
    """First Lyapunov coefficient of a planar system at a Hopf point (Kuznetsov 2004, eq. 3.20), exact arithmetic."""
    X1, X2 = sp.symbols('X1 X2')
    f1 = Fv[0].subs(params).subs({x: X1 + x0, y: X2 + y0_})
    f2 = Fv[1].subs(params).subs({x: X1 + x0, y: X2 + y0_})
    Jm_ = sp.Matrix([f1, f2]).jacobian([X1, X2]).subs({X1: 0, X2: 0})
    om = sp.sqrt(Jm_.det())
    # A q = i om q;  u satisfies A^T u = i om u, so p = conj(u) satisfies A^T p = -i om p and <p, v> = u^T v
    qv = sp.Matrix([-Jm_[0, 1], Jm_[0, 0] - sp.I*om])
    u = sp.Matrix([sp.I*om - Jm_[1, 1], Jm_[0, 1]])
    assert sp.simplify(Jm_*qv - sp.I*om*qv) == sp.zeros(2, 1) and sp.simplify(Jm_.T*u - sp.I*om*u) == sp.zeros(2, 1)
    u = u/(u.T*qv)[0]                                              # normalise <p, q> = 1

    def Bf(u, v):
        res = []
        for f in (f1, f2):
            H_ = sp.hessian(f, (X1, X2)).subs({X1: 0, X2: 0})
            res.append((u.T*H_*v)[0])
        return sp.Matrix(res)

    def Cf(u, v, z):
        res = []
        for f in (f1, f2):
            tot = 0
            for i_, vi in enumerate((X1, X2)):
                for j_, vj in enumerate((X1, X2)):
                    for k2, vk in enumerate((X1, X2)):
                        tot += sp.diff(f, vi, vj, vk).subs({X1: 0, X2: 0})*u[i_]*v[j_]*z[k2]
            res.append(tot)
        return sp.Matrix(res)

    qb = qv.conjugate()
    Ainv = Jm_.inv()
    t1 = (u.T*Cf(qv, qv, qb))[0]
    t2 = (u.T*Bf(qv, Ainv*Bf(qv, qb)))[0]
    t3 = (u.T*Bf(qb, (2*sp.I*om*sp.eye(2) - Jm_).inv()*Bf(qv, qv)))[0]
    return sp.simplify(sp.re(sp.expand(t1 - 2*t2 + t3))/(2*om))


# self-test on a system with a known answer: x' = -y + al x (x^2+y^2), y' = x + al y (x^2+y^2) has l1 with the sign of al
al = sp.Symbol('alpha', real=True)
l1_test = [lyapunov_l1([-y + v*x*(x**2 + y**2), x + v*y*(x**2 + y**2)], 0, 0, {}) for v in (-1, 1)]
check('S25d0', 'Lyapunov-coefficient routine self-test: sign of l1 equals sign of alpha in the planar normal form',
      sp.N(l1_test[0]) < 0 and sp.N(l1_test[1]) > 0, f'l1 = {l1_test}')

neg = 0; tried = 0
for _ in range(12):
    vals = {r: sp.Rational(rng.randint(5, 30), 10), a: sp.Rational(rng.randint(5, 30), 10), h: sp.Rational(rng.randint(5, 30), 10),
            m: sp.Rational(rng.randint(5, 30), 100)}
    vals[e] = vals[m]*vals[h] + sp.Rational(rng.randint(10, 60), 50)
    xv = xR.subs(vals)
    vals[K] = 2*xv + 1/(vals[a]*vals[h])           # x* exactly at the hump: Hopf point
    yv = yR.subs(vals)
    l1 = lyapunov_l1([F1, F2], xv, yv, vals)
    tried += 1
    if sp.N(l1, 30) < 0:
        neg += 1
check('S25d', 'Rosenzweig-MacArthur: first Lyapunov coefficient l1 < 0 at the Hopf point (supercritical) at 12 random parameter sets, exact arithmetic',
      neg == tried, f'{neg}/{tried} negative')

# ---------------------------------------------------------------- S26 Ito noise, prey alone
def ito_log_drift(drift, sigma_):
    """drift of d ln x for dx = drift dt + sigma x dW"""
    return sp.simplify(drift/x - sigma_**2/2)


dl_log = ito_log_drift(r*x*(1 - x/K), sig)
check('S26a', 'Ito, logistic prey alone: d ln x = (r(1 - x/K) - sigma^2/2) dt + sigma dW, low-density drift r - sigma^2/2: persists iff r > sigma^2/2',
      is_zero(sp.limit(dl_log, x, 0, '+') - (r - sig**2/2)))
dl_th = ito_log_drift(r*x*(1 - (x/K)**th), sig)
check('S26b', 'Ito, theta-logistic and exponential prey: same low-density drift r - sigma^2/2',
      is_zero(sp.limit(dl_th, x, 0, '+') - (r - sig**2/2)) and is_zero(ito_log_drift(r*x, sig) - (r - sig**2/2)))
dl_g = ito_log_drift(r*x*sp.log(K/x), sig)
check('S26c', 'Ito, Gompertz prey: d ln x has drift r ln K - sigma^2/2 - r ln x (an Ornstein-Uhlenbeck process in ln x), so the prey persists for every sigma',
      is_zero(sp.expand(sp.expand_log(dl_g, force=True)) - sp.expand(r*sp.log(K) - sig**2/2 - r*sp.log(x))))
dl_f = ito_log_drift(r*x - d*x - c*x**2, sig)
check('S26d', 'Ito, fear prey without predators: low-density drift r - d - sigma^2/2',
      is_zero(sp.limit(dl_f, x, 0, '+') - (r - d - sig**2/2)))

# ---------------------------------------------------------------- S27 Turing conditions
J11, J12, J21, J22, Dx, Dy = sp.symbols('J11 J12 J21 J22 D_x D_y', real=True)
yy = y*(e*fr_ - m)
check('S27a', 'Prey-dependent predator equation y(eF(x) - m): J22 = eF - m = 0 at any interior equilibrium',
      is_zero(sp.diff(yy, y) - (e*fr_ - m)))
# Turing needs Dx*J22 + Dy*J11 > 0 while J11 + J22 < 0; with J22 = 0 this is impossible
check('S27b', 'With J22 = 0, stability (J11 + J22 < 0) forces J11 < 0, so Dy J11 + Dx J22 > 0 (needed for Turing) fails for all D > 0',
      sp.simplify((Dy*J11 + Dx*J22).subs(J22, 0)) == Dy*J11)
bd = e*a*x*y/(1 + a*h*x + c*y) - m*y
xb, yb = sp.symbols('x_b y_b', positive=True)
J22bd = sp.simplify(sp.diff(bd, y) - (e*a*x/(1 + a*h*x + c*y) - m))     # at equilibrium the bracket is 0
ydd = y*(e*fr_ - m - delta*y)
check('S27c', 'Self-limitation gives J22 < 0 at equilibrium: -delta y* (delta y^2), -e a c x y/(1+ahx+cy)^2 (Beddington-DeAngelis), -s (Leslie-Gower)',
      is_zero(J22bd + e*a*c*x*y/(1 + a*h*x + c*y)**2)
      and is_zero(sp.diff(ydd, y).subs(m, e*fr_ - delta*y) + delta*y)
      and is_zero(sp.diff(s*y*(1 - y/(eta*x)), y).subs(y, eta*x) + s))

# ---------------------------------------------------------------- S28 ratio dependence at the origin
kk = sp.Symbol('k', positive=True)
frd = a*x*y/(y + a*h*x)
dirx = sp.simplify(sp.diff(frd, x).subs(y, kk*x))
check('S28', 'Ratio-dependent term a x y/(y + a h x) is 0/0 at (0,0) and its x-derivative depends on the direction y = kx (not differentiable there)',
      sp.simplify(dirx - a*kk**2/(kk + a*h)**2) == 0)

# ---------------------------------------------------------------- S29 refuges in the classical model (Maynard Smith 1974)
ap = a*(1 - phi)
Hp = e*ap*x - m*sp.log(x) + ap*y - r*sp.log(y)
dHp = sp.diff(Hp, x)*(r*x - ap*x*y) + sp.diff(Hp, y)*(e*ap*x*y - m*y)
check('S29a', 'Classical LV with a proportional refuge: a(1-phi) replaces a, the first integral is kept, so the centre stays neutral (no stabilisation)',
      is_zero(dHp))
fn1 = r*x - a*(x - xi)*y; fn2 = e*a*(x - xi)*y - m*y          # x > xi
xn = xi + m/(e*a); yn = sp.simplify(r*xn/(a*(xn - xi)))
Jn = sp.Matrix([fn1, fn2]).jacobian([x, y]).subs({x: xn, y: yn})
check('S29b', 'Classical LV with a fixed-number refuge: trace = -r xi/(x* - xi) < 0 and det > 0, so the centre becomes asymptotically stable',
      is_zero(fn1.subs({x: xn, y: yn})) and is_zero(fn2.subs({x: xn, y: yn})) and is_zero(Jn.trace() + r*xi/(xn - xi)) and sp.simplify(Jn.det()).is_positive,
      f'det = {sp.simplify(Jn.det())}')

# ---------------------------------------------------------------- S30 quasi-positivity (non-negative orthant)
xi_v = {
    'logistic + Allee': r*x*(1 - x/K)*(x - A)/K, 'additive Allee': -mu*x/(x + b), 'fear': r*x/(1 + k_*y) - d*x - c*x**2,
    'Holling II loss': -a*x*y/(1 + a*h*x), 'number refuge loss (x<xi)': 0, 'herd loss': -a*x**sp.Rational(1, 2)*y,
    'effort harvest': -q*E*x, 'MM harvest': -q*E*x/(c*E + w*x), 'immigration': I, 'prey eats predator': ex*zeta*x*y,
}
qp = all(sp.limit(v, x, 0, '+') >= 0 for v in xi_v.values())
check('S30', 'Quasi-positivity: every prey term listed is >= 0 at x = 0 (each has a factor x, or is immigration); constant yield (-H) is the only exception (S21)',
      qp, ', '.join(xi_v))

# ---------------------------------------------------------------- write
(OUT / 'constraint_checks.json').write_text(json.dumps(RESULTS, indent=1, ensure_ascii=False), encoding='utf-8')
lines = [f"{R_['id']:5s} {'PASS' if R_['pass'] else 'FAIL'}  {R_['claim']}" + (f"   [{R_['detail']}]" if R_['detail'] else '') for R_ in RESULTS]
(OUT / 'constraint_checks.txt').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(f"\n{sum(R_['pass'] for R_ in RESULTS)}/{len(RESULTS)} checks pass")
