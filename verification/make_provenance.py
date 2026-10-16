"""Write constraint_provenance.tex: where every constraint and stated result of the model builder comes from.

Types:  D  follows from what the parameter means;
        M  derived from the model equations and checked with SymPy (IDs S.. in verify_constraints.py);
        C  modelling convention (a choice, stated as such);
        L  result reported in the literature, with how far it was checked (abstract, title, or not accessed).
Check status is read from constraint_checks.json, so run verify_constraints.py first.
"""
import json
import re
from pathlib import Path

FIG = Path(__file__).resolve().parent.parent
checks = {c['id']: c['pass'] for c in json.loads((FIG / 'constraint_checks.json').read_text(encoding='utf-8'))}
bib = (FIG / 'lv_references.bib').read_text(encoding='utf-8')
bibkeys = set(re.findall(r'@\w+\{([^,]+),', bib))

# (id, constraint or result, type, basis and source, check ids)
SECTIONS = [
 ('Prey growth ($T_1$)', [
  ('G1', r'$r>0$', 'D', r'Intrinsic growth rate: the prey increases at low density without predators \cite{verhulst1838,lotka1925}.', ''),
  ('G2', r'$K>0$', 'D', r'Carrying capacity \cite{verhulst1838}.', ''),
  ('G3', r'$\theta>0$; $\theta=1$ is the logistic law', 'D, M', r'Shape exponent of density dependence \cite{gilpin1973}.', 'S1'),
  ('G4', r'$\tau^{x}\ge 0$', 'D', r'Delay in self-limitation \cite{hutchinson1948}.', ''),
  ('G5', r'Without predators, $K$ is stable iff $r\tau^{x}<\pi/2$', 'M', r'Roots of $\lambda+re^{-\lambda\tau}=0$ first cross the imaginary axis at $\lambda=ir$, $r\tau=\pi/2$, with $\mathrm{Re}\,d\lambda/d\tau=r^{2}/(1+\pi^{2}/4)>0$ \cite{hutchinson1948}.', 'S6'),
  ('G6', r'Gompertz: per-capita rate $r\ln(K/x)\to\infty$ as $x\to0^{+}$', 'M', r'\cite{gompertz1825}.', 'S7'),
  ('G7', r'Strong Allee: $0<A<K$', 'M', r'Per-capita growth $g(x)=r(1-x/K)(x-A)/K$ has $g(0)=-rA/K$ and zeros $A,K$ \cite{allee1931,wang2011allee}.', 'S2a,S2c'),
  ('G8', r'Weak Allee: $-K<A\le 0$; $A\le -K$ removes the effect', 'M, C', r"$g'(0)=r(K+A)/K^{2}$. The borderline $A=0$ ($g(0)=0$) is grouped with the weak case by convention.", 'S2b,S2d'),
  ('G9', r'Strong Allee, prey alone: origin locally stable, outcome depends on initial densities', 'M', r'Follows from $g(0)<0$ (statement corrected to ``without predators\textquotedblright{}).', 'S2a'),
  ('G10', r'Additive Allee: strong iff $\mu>rb$; weak iff $rb^{2}/K<\mu<rb$ (needs $b<K$)', 'M', r"$g(0)=r-\mu/b$, $g'(0)=-r/K+\mu/b^{2}$; additive form from \cite{dennis1989}.", 'S3a,S3b,S3c'),
  ('G11', r'Fear: $r>d$', 'M', r'Low-density growth rate of the prey alone is $r-d$; model of \cite{wang2016fear} (abstract: cost of fear in prey reproduction).', 'S4'),
  ('G12', r'$d\ge 0$, $c^{x}>0$, $k\ge 0$ ($k=0$: no fear)', 'D', r'Death rate, self-limitation and fear level \cite{wang2016fear}.', ''),
  ('G13', r'Fear lowers prey births only; the predator gains nothing from it', 'D, L', r'Model structure \cite{wang2016fear}. Field evidence: perceived risk alone cut offspring production by 40\% \cite{zanette2011} (abstract).', ''),
  ('G14', r'$0\le\varepsilon<1$; $\omega=2\pi/T>0$', 'M', r'$\min_{t} r(1+\varepsilon\sin\omega t)=r(1-\varepsilon)>0$ iff $\varepsilon<1$.', 'S5'),
  ('G15', r'Seasonal forcing: periodic solutions, multiple attractors and chaos instead of equilibria', 'D, L', r'Non-autonomous by construction. Periodic solutions \cite{cushing1977}; multiple attractors and chaos \cite{rinaldi1993}. Checked against the titles only (the open copy of \cite{rinaldi1993} is no longer online); ``quasi-periodic\textquotedblright{} was removed from the note.', ''),
  ('G16', r"$\alpha_{ii'}\ge 0$", 'D', r'Interspecific competition between prey.', ''),
 ]),
 ('Predation ($T_2$)', [
  ('P1', r'$a>0$', 'D', r'Attack rate (search efficiency) \cite{holling1959}.', ''),
  ('P2', r'$h>0$; maximal intake $1/h$', 'M', r'$\lim_{x\to\infty} ax/(1+ahx)=1/h$ \cite{holling1959}.', 'S9'),
  ('P3', r'One handling time shared by all food items: $D_j=1+\sum_k a_kh_kx_k$', 'M', r'Time budget $T=T_s\bigl(1+\sum_k a_kh_kx_k\bigr)$ gives intake $a_ix_i/D_j$; applies to prey, predator food and additional food alike.', 'S12'),
  ('P4', r'$G>0$; response peaks at $\sqrt{G}$, $\sqrt{G}/(1-\phi)$ or $\xi+\sqrt{G}$', 'M', r'Holling IV / group defence \cite{andrews1968,freedman1986}. The builder stated $\sqrt{G}$ for every case; corrected for the two refuge types.', 'S10a,S10b,S10c'),
  ('P5', r'Holling IV: at most two interior equilibria; Bogdanov--Takens bifurcations', 'M, L', r'Equilibria solve a quadratic. Bogdanov--Takens: \cite{xiao2001siam} (abstract); source added.', 'S10d'),
  ('P6', r'Ivlev: $\rho,\lambda>0$', 'D', r'\cite{ivlev1961}.', ''),
  ('P7', r'Beddington--DeAngelis, Crowley--Martin: $c\ge 0$, $c=0$ is Holling II', 'M', r'\cite{beddington1975,deangelis1975,crowley1989}.', 'S11a'),
  ('P8', r'Hassell--Varley: $0<\gamma<1$', 'M, C', r'$\gamma=0$ gives Holling II and $\gamma=1$ the ratio-dependent form; the interval between them is a convention \cite{hassell1969}.', 'S11b'),
  ('P9', r'Mutual interference: $0\le\nu<1$', 'M', r'$\nu<1$ makes predation vanish without predators; $\nu=0$ is the classical term \cite{hassell1971}.', 'S11c'),
  ('P10', r'Ratio dependence: not defined at $(0,0)$; origin can attract all orbits', 'M, L', r'0/0 and direction-dependent derivative at the origin. Higher-order singular point with parabolic, elliptic and hyperbolic sectors \cite{xiao2001rd} (abstract); global stability conditions for each of the three equilibria, the origin included \cite{kuang1998} (abstract). ``Blow-up techniques\textquotedblright{} removed: not in either abstract.', 'S28'),
  ('P11', r'Herd behaviour: $0<p<1$; $p=1/2$ for a planar herd', 'M', r'The edge of a disc-shaped herd scales as area$^{1/2}$ \cite{ajraldi2011}.', 'S8c'),
  ('P12', r'Herd: $x^{p}$ not Lipschitz at 0; prey can vanish in finite time', 'M', r'$\frac{d}{dt}x^{1-p}\to-(1-p)ay<0$ as $x\to0$ \cite{ajraldi2011}.', 'S8a,S8b'),
  ('P13', r'$0\le\phi<1$; $\xi\ge 0$', 'D', r'Protected fraction or number of prey \cite{maynardsmith1974,gonzalez2003}.', ''),
  ('P14', r'Fixed-number refuge stabilises the Lotka--Volterra centre; a proportional refuge does not', 'M, L', r'Proportional refuge only rescales $a$ and keeps the first integral; fixed number gives trace $-r\xi/(x^{*}-\xi)<0$. Attributed to \cite{maynardsmith1974} (book, not accessed; result re-derived). Caveat from \cite{mcnair1986} (abstract): refuges can destabilise in more realistic models. The earlier note (``stabilises more strongly\textquotedblright{}) was replaced; source added.', 'S29a,S29b'),
  ('P15', r'$0\le\kappa<1$', 'D', r'Fraction of search efficiency lost to habitat complexity \cite{bairagi2011} (not accessed; publisher page behind a CAPTCHA).', ''),
  ('P16', r'$w\ge 0$; cooperation gives a component Allee effect', 'M', r'Per-capita gain $e(a+wy)x/(1+(a+wy)hx)$ increases with $y$.', 'S17'),
  ('P17', r'Hunting cooperation can produce demographic Allee effects and predator collapse', 'L', r'\cite{teixeiraalves2017} (abstract). Earlier wording (``bistability\textquotedblright{}) replaced by the abstract\'s statement.', ''),
  ('P18', r'Additional food: $\Lambda\ge 0$ constant; $a^{F},h^{F},e^{F}>0$; enters $D$ and $T_3$', 'D, M', r'\cite{srinivasu2007} (abstract: handling times decide the outcome). Under Leslie--Gower only $a^{F},h^{F}$ appear (no conversion term).', 'S12'),
 ]),
 ('Predator ($T_3$, $T_4$)', [
  ('N1', r'$e>0$; $e<1$ when densities are biomass or energy', 'M', r'Mass balance: predation changes $x+y$ by $-(1-e)fy$.', 'S13a'),
  ('N2', r'$m>0$', 'D', r'Natural death rate.', ''),
  ('N3', r'$\psi>0$; predator Allee makes $y=0$ locally stable', 'M', r'$\partial_y\bigl[\tfrac{y}{y+\psi}eFy-my\bigr]_{y=0}=-m$ \cite{courchamp2008}.', 'S16'),
  ('N4', r'$\tau\ge 0$; initial data on $[-\tau,0]$', 'D', r'\cite{cushing1977book,kuang1993}.', ''),
  ('N5', r'Delays: stability switches; often stable, unstable, stable again with delay-dependent survival', 'L', r'\cite{beretta2002} (abstract); window of oscillatory maturation delays \cite{gourley2004} (abstract). Source added.', ''),
  ('N6', r'$\delta^{J}\ge 0$; juvenile survival $\exp(-\delta^{J}\tau)$', 'M', r'Solution of $J\'=-\delta^{J}J$ over the delay \cite{gourley2004}.', 'S15'),
  ('N7', r'$\delta\ge 0$', 'D', r'Density-dependent predator mortality \cite{bazykin1998}.', ''),
  ('N8', r"$\beta_{jj'}\ge 0$", 'D', r'Interference competition between predators.', ''),
  ('N9', r'Leslie--Gower: $s,\eta>0$; $\eta$ = predators supported per unit prey', 'M', r'Predator equilibrium $y=\eta x$ \cite{leslie1948,leslie1960}.', 'S18c'),
  ('N10', r'Leslie--Gower singular without prey; $C>0$ removes it', 'M', r'\cite{azizalaoui2003}.', 'S18a,S18b'),
 ]),
 ('Predators eating predators', [
  ('Y1', r'$a^{y},h^{y},\rho^{y},\lambda^{y},\eta^{y}>0$', 'D', r'Same meaning as for prey links, indexed by eaten and eating predator.', ''),
  ('Y2', r'$e^{y}>0$; $e^{y}<1$ when densities are biomass or energy', 'M', r'Mass balance as in N1.', 'S13a'),
  ('Y3', r'Cannibalism: $e^{y}_{ll}<1$ always', 'M', r'Net effect of the link is $(e^{y}-1)a^{y}y^{2}/D$; with $e^{y}>1$ and no other food the predator blows up in finite time.', 'S14a,S14b'),
  ('Y4', r'Cannibalism can stabilise and raise both standing stocks', 'M, L', r'\cite{kohlmeier1995} (abstract); the second finding was added to the note.', 'S14a'),
  ('Y5', r'Intraguild predation: coexistence needs the intraguild prey to be the better competitor and the intraguild predator to gain substantially; most likely at intermediate productivity', 'L', r'\cite{holt1997} (abstract); review \cite{polis1989} (not accessed). The note said ``only at intermediate productivity\textquotedblright{} and omitted the second condition; corrected.', ''),
  ('Y6', r'Holling II food chains can be chaotic', 'L', r'\cite{hastings1991} (abstract).', ''),
  ('Y7', r'Reciprocal predation between two species', 'D, L', r'\cite{almohanna2025} (abstract: two predators preying on each other).', ''),
  ('Y8', r'No cannibalism with Leslie--Gower', 'C', r'Builder choice: the predator\'s capacity would depend on its own density.', ''),
  ('Y9', r'Refuge, habitat, cooperation, herd and group defence act on prey links only', 'C', r'Builder choice, stated in a note whenever predators eat predators.', ''),
 ]),
 ('Added terms ($\Phi$)', [
  ('H1', r'$q,E,H\ge 0$; $\ell$ constants $>0$', 'D', r'\cite{clark1976,brauer1979,gupta2013,chaudhuri1996}.', ''),
  ('H2', r'Effort harvest: prey alone persists iff $qE<r$', 'M', r'Exponential, logistic, $\theta$-logistic and delayed logistic prey without Allee or fear; equilibrium $K(1-qE/r)^{1/\theta}$ \cite{clark1976}.', 'S19a,S19b'),
  ('H3', r'Constant yield, logistic prey: $H<rK/4$', 'M', r'Maximum of $rx(1-x/K)$ is $rK/4$ at $K/2$ \cite{brauer1979}.', 'S20'),
  ('H4', r'Constant yield must stop at zero density', 'M', r'At $x=0$ the right side is $-H<0$.', 'S21'),
  ('H5', r'$I\ge 0$; immigration stabilises the Lotka--Volterra centre', 'M, L', r'Trace $=-I/x^{*}<0$; \cite{tahara2018} (abstract).', 'S22'),
  ('H6', r'$\zeta\ge 0$ (prey kill predators without gain)', 'D', r'\cite{tang2015}.', ''),
  ('H7', r'Prey eat predators: $e^{x}>0$; $e^{x}<1$ in biomass units', 'M', r'$x+y$ changes by $-(1-e)axy-(1-e^{x})\zeta xy$ \cite{almohanna2025}.', 'S13b'),
  ('H8', r'$\vartheta\ge 0$, $g>0$', 'D', r'Toxic prey \cite{chattopadhyay2002}.', ''),
 ]),
 ('Framework and general statements', [
  ('F1', r'$D^{x},D^{y}>0$; no-flux boundary conditions', 'D', r'\cite{skellam1951}.', ''),
  ('F2', r'Turing patterns need predator self-limitation and a large $D^{y}/D^{x}$', 'M', r'With $J_{22}=0$ (prey-dependent predator equation) Turing instability is impossible; $\delta y^{2}$, Beddington--DeAngelis and Leslie--Gower give $J_{22}<0$ \cite{segel1972} (not accessed).', 'S27a,S27b,S27c'),
  ('F3', r'It\^o noise: prey alone persists iff $r>\sigma^{2}/2$ (exponential, logistic, $\theta$), $r-d>\sigma^{2}/2$ (fear); always (Gompertz)', 'M', r'Drift of $d\ln x$ at low density \cite{rudnicki2003} (not accessed). The note gave $r>\sigma^{2}/2$ for every growth law; corrected.', 'S26a,S26b,S26c,S26d'),
  ('F4', r'Non-negative orthant invariant, except with constant-yield harvest', 'M', r'Every term is non-negative when its own density is zero (quasi-positivity), except $-H$.', 'S30,S21'),
  ('F5', r'Parameters non-negative unless their constraint says otherwise', 'D', r'The weak-Allee threshold $A$ may be negative; the general note was corrected.', ''),
 ]),
 ('Classical results shown by the builder', [
  ('K1', r'Lotka--Volterra: centre at $(m/ea,\,r/a)$, first integral $H$', 'M', r'\cite{lotka1925,volterra1926}.', 'S23'),
  ('K2', r'Logistic prey, Holling I: interior equilibrium iff $m<eaK$, globally stable', 'M', r'$\dot V=-(er/K)(x-x^{*})^{2}\le 0$ and LaSalle.', 'S24'),
  ('K3', r'Rosenzweig--MacArthur: $x^{*}=m/[a(e-mh)]$, exists iff $e>mh$, $x^{*}<K$; stable iff $x^{*}>\tfrac12(K-1/ah)$', 'M', r'Trace $=\tfrac{2rahx^{*}}{K(1+ahx^{*})}(x_{\rm hump}-x^{*})$, determinant $>0$ \cite{rosenzweig1963}.', 'S25a,S25b,S25c'),
  ('K4', r'Supercritical Hopf at $x^{*}=x_{\rm hump}$; unique limit cycle beyond it (paradox of enrichment)', 'M, L', r'First Lyapunov coefficient $<0$ at 12 random parameter sets in exact arithmetic (sampled, not a general proof); unique limit cycle \cite{cheng1981} (abstract); paradox of enrichment \cite{rosenzweig1971} (abstract). Sources added.', 'S25d0,S25d'),
 ]),
]

missing = sorted({k for _, rows in SECTIONS for row in rows for k in re.findall(r'\\cite\{([^}]+)\}', row[3]) for k in k.split(',')} - bibkeys)
assert not missing, f'keys missing from lv_references.bib: {missing}'
bad = [c for _, rows in SECTIONS for row in rows for c in row[4].split(',') if c and c not in checks]
assert not bad, f'unknown check ids: {bad}'


def status(ids):
    if not ids:
        return '--'
    ok = all(checks[c] for c in ids.split(','))
    span = ids.replace(',', ', ')
    return (r'\checkmark\ ' if ok else r'\textbf{FAIL} ') + span


n_rows = sum(len(r) for _, r in SECTIONS)
n_M = sum(1 for _, r in SECTIONS for row in r if 'M' in row[2])
lines = [
    r'% Generated by figure/tools/make_provenance.py -- edit the script, not this file.',
    r'% Needs: \usepackage{longtable,booktabs,array,amsmath,amssymb}',
    r'\begingroup\small',
    r'\setlength{\LTcapwidth}{\textwidth}',
    r'\begin{longtable}{@{}>{\raggedright\arraybackslash}p{0.06\textwidth}>{\raggedright\arraybackslash}p{0.29\textwidth}>{\centering\arraybackslash}p{0.05\textwidth}>{\raggedright\arraybackslash}p{0.38\textwidth}>{\raggedright\arraybackslash}p{0.11\textwidth}@{}}',
    r'\caption{Provenance of every constraint and stated result in this review and the model builder. Type: D, follows from the meaning of the parameter; M, derived from the model and checked symbolically (IDs S.. refer to \texttt{verify\_constraints.py}); C, modelling convention; L, result from the literature, with the extent of the check (abstract, title, or not accessed).}\label{tab:constraint-provenance}\\',
    r'\toprule ID & Constraint or result & Type & Basis and source & Check \\ \midrule \endfirsthead',
    r'\toprule ID & Constraint or result & Type & Basis and source & Check \\ \midrule \endhead',
    r'\bottomrule \endfoot',
]
for title, rows in SECTIONS:
    lines.append(rf'\multicolumn{{5}}{{@{{}}l}}{{\textit{{{title}}}}}\\[2pt]')
    for (i, c, ty, basis, ids) in rows:
        c, basis = c.replace("\\'", "'"), basis.replace("\\'", "'")   # raw strings keep the backslash of \'
        lines.append(f'{i} & {c} & {ty} & {basis} & {status(ids)} \\\\')
    lines.append(r'\addlinespace')
lines += [r'\end{longtable}', r'\endgroup', '']
(FIG / 'constraint_provenance.tex').write_text('\n'.join(lines), encoding='utf-8')
print(f'rows: {n_rows} (derived: {n_M}); checks referenced: {len({c for _, r in SECTIONS for row in r for c in row[4].split(",") if c})}')
