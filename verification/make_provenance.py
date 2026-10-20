"""Write the provenance tables of every constraint and stated result, and the full-text checklist.

Basis of a statement:
    D  follows from what the parameter means (definition);
    C  modelling convention (a choice, stated as such);
    M  derived here from the model equations and checked with SymPy (IDs S.. in verify_constraints.py);
    Q  quoted: a result stated as in the cited source;
    A  adapted: a result of the cited source restated in our notation or setting, specialised, or combined
       with a derivation of ours.
Evidence for Q and A: F = full text read (location given), Ab = abstract only, T = title only,
N = not accessed. Statements of kind Q or A that rest on an abstract say no more than the abstract.

Outputs (in figure/):
    constraint_provenance.tex       main-text table: every statement except pure definitions, short form
    constraint_provenance_full.tex  supplementary longtable: all statements, basis, sources, corrections
    ../paper/fulltext_checklist.md  the literature statements whose full text should still be checked
Check status is read from constraint_checks.json, so run verify_constraints.py first.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIG = HERE if (HERE / 'lv_references.bib').exists() else HERE.parent      # site/verification or figure/tools
PAPER = FIG.parent / 'paper' if (FIG.parent / 'paper').is_dir() else FIG
checks = {c['id']: c for c in json.loads((FIG / 'constraint_checks.json').read_text(encoding='utf-8'))}
bib = (FIG / 'lv_references.bib').read_text(encoding='utf-8')
bibkeys = set(re.findall(r'@\w+\{([^,]+),', bib))
LAST_UPDATE = '19 October 2026'

# row: (id, statement, basis, explanation and source, check ids, evidence, correction history)
#   evidence: list of (key, level, location); level in F, Ab, T, N; location only for F
S = []


def sec(title, rows):
    S.append((title, rows))


sec('Prey growth ($T_1$)', [
 ('G1', r'$r>0$', 'D', r'Intrinsic growth rate: the prey increases at low density without predators.', '', [], ''),
 ('G2', r'$K>0$', 'D', r'Carrying capacity.', '', [], ''),
 ('G3', r'$\theta>0$; $\theta=1$ is the logistic law', 'D, M', r'Shape exponent of density dependence \cite{gilpin1973}.', 'S1', [], ''),
 ('G4', r'$\tau^{x}\ge 0$', 'D', r'Delay in self-limitation \cite{hutchinson1948}.', '', [], ''),
 ('G5', r'Without predators, $K$ is locally asymptotically stable iff $r\tau^{x}<\pi/2$; inconclusive at equality',
  'M', r'Roots of $\lambda+re^{-\lambda\tau}=0$: $-r$ at $\tau=0$; imaginary roots only at $\pm ir$ with $\sin r\tau=1$; transversal crossing at $r\tau=\pi/2$.',
  'S6', [], r'``Stable iff $r\tau<\pi/2$\textquotedblright{} did not separate local from global stability; now split into G5 and G5b. Second evaluation: the builder states G5 and G5b only when no harvest, immigration, seasonal forcing, prey competition, diffusion or noise changes the prey-only equation.'),
 ('G5b', r'Without predators, $K$ attracts all positive solutions for $r\tau^{x}\le\pi/2$', 'A',
  r"$x=K[1+z(t/\tau)]$ gives Wright's equation with $\alpha=r\tau$ (derived); Wright's conjecture proved in \cite{vandenberg2018}.",
  'S6b', [('vandenberg2018', 'F', r'arXiv:\allowbreak 1704.00029v1, Thm.~1.5')], 'Added at review; restricted as G5 at the second evaluation.'),
 ('G6', r'Gompertz: $r\ln(K/x)\to\infty$ as $x\to0^{+}$; not Lipschitz at 0 but solutions unique; $x=0$ neither reached nor left in finite time unless immigration, constant yield or herd behaviour act at $x=0$', 'M',
  r'Osgood: $\int_0 dx/[rx\ln(K/x)]=\infty$ \cite{gompertz1825}. Immigration gives $\dot x=I>0$ at $x=0$; constant yield and the herd term $x^{p}$ reach 0 in finite time.', 'S7,S7b,S8d,S21', [],
  'Uniqueness statement added at review; exceptions added at the second evaluation.'),
 ('G7', r'Strong Allee: $0<A<K$', 'M', r'Per-capita growth $r(1-x/K)(x-A)/K$ has value $-rA/K$ at 0 and zeros $A,K$ \cite{allee1931}.', 'S2a,S2c', [], ''),
 ('G8', r'Weak Allee: $-K<A\le 0$; $A\le -K$ removes the effect', 'M, C',
  r"Slope $r(K+A)/K^{2}$ at 0. The borderline $A=0$ is grouped with the weak case by convention.", 'S2b,S2d', [], ''),
 ('G9', r'Strong Allee, prey alone: origin locally stable, outcome depends on initial density; with prey immigration a small stable equilibrium replaces the origin', 'M',
  r'Follows from $g(0)<0$; with immigration $f(0)=I>0$ and the implicit function theorem.', 'S2a,S32a', [],
  r'Restricted to ``without predators\textquotedblright{}; the immigration case added at the second evaluation.'),
 ('G9b', r'Strong Allee with a predator: heteroclinic loops and a threshold curve separating overexploitation from coexistence', 'Q',
  r'\cite{wang2011allee}.', '', [('wang2011allee', 'Ab', '')], ''),
 ('G10', r'Additive Allee: strong iff $b<K$ and $rb<\mu<r(K+b)^{2}/(4K)$; weak iff $rb^{2}/K<\mu\le rb$ (the borderline $\mu=rb$ grouped with the weak case)', 'M',
  r"$g(0)=r-\mu/b$, $g'(0)=-r/K+\mu/b^{2}$, $\max_{x\ge0}r(1-x/K)(x+b)$; additive form from \cite{dennis1989}.",
  'S3a,S3b,S3c,S3d,S3e', [], r'``Strong iff $\mu>rb$\textquotedblright{} was wrong: $r=K=b=1$, $\mu=2$ gives decline at every density (S3e).'),
 ('G11', r'Fear: $r>d$', 'M', r'Low-density growth rate of the prey alone is $r-d$; model of \cite{wang2016fear}.', 'S4', [], ''),
 ('G12', r'$d\ge 0$, $c^{x}>0$, $k\ge 0$ ($k=0$: no fear)', 'D', r'Death rate, self-limitation and fear level \cite{wang2016fear}.', '', [], ''),
 ('G13', r'Perceived predation risk alone cut offspring production by 40\%', 'Q', r'Field experiment on song sparrows \cite{zanette2011}.', '',
  [('zanette2011', 'Ab', '')], ''),
 ('G13b', r'Fear model: high fear excludes periodic solutions; low fear allows subcritical Hopf bifurcation and bistability', 'Q',
  r'\cite{wang2016fear}.', '', [('wang2016fear', 'Ab', '')], ''),
 ('G14', r'$0\le\varepsilon<1$; $\omega=2\pi/T>0$', 'M', r'$\min_{t} r(1+\varepsilon\sin\omega t)=r(1-\varepsilon)$.', 'S5', [], ''),
 ('G15', r'Seasonal forcing: periodic solutions, multiple attractors and chaos', 'D, Q',
  r'Non-autonomous by construction; periodic solutions \cite{cushing1977}; multiple attractors and chaos \cite{rinaldi1993}.', '',
  [('cushing1977', 'T', ''), ('rinaldi1993', 'T', '')], r'``Quasi-periodic\textquotedblright{} removed: not supported by the titles.'),
 ('G16', r"$\alpha_{ii'}\ge 0$", 'D', r'Interspecific competition between prey.', '', [], ''),
 ('G17', r'Toxicant (T1.10): the prey alone persists only if $r_0-r_1C_0>0$', 'M',
  r'Prey alone: $x=x_0\exp[(r_0-r_1C_0)t]$, which tends to $0$ when $r_0-r_1C_0<0$; model of \cite{hallam1983}.', 'S42c', [], 'Added 19 October 2026 (audit of the entries table).'),
])

sec('Predation ($T_2$)', [
 ('P1', r'$a>0$', 'D', r'Attack rate (search efficiency) \cite{holling1959}.', '', [], ''),
 ('P2', r'$h>0$; maximal intake $1/h$', 'M', r'$\lim_{x\to\infty} ax/(1+ahx)=1/h$ \cite{holling1959}.', 'S9', [], ''),
 ('P3', r'One handling time shared by all food items: $D_j=1+\sum_k a_kh_kx_k$', 'M',
  r'Time budget $T=T_s(1+\sum_k a_kh_kx_k)$; applies to prey, predators eaten and additional food alike.', 'S12', [], ''),
 ('P4', r'Holling IV peaks at $\sqrt{G}$, $\sqrt{G}/(1-\phi)$ or $\xi+\sqrt{G}$', 'M', r'Group defence \cite{andrews1968,freedman1986}.',
  'S10a,S10b,S10c', [], r'The builder stated $\sqrt{G}$ for every case; corrected for the two refuge types.'),
 ('P5', r'Holling IV, one prey and one predator whose per-capita growth depends on prey density only: at most two interior equilibria; Bogdanov--Takens bifurcation', 'M, Q',
  r'Equilibria solve a quadratic; Bogdanov--Takens \cite{xiao2001siam}.', 'S10d', [('xiao2001siam', 'Ab', '')], 'Source added. Second evaluation: the builder stated it for every model with Holling IV, food webs included; now only under these conditions.'),
 ('P6', r'Ivlev: $\rho,\lambda>0$', 'D', r'\cite{ivlev1961}.', '', [], ''),
 ('P7', r'Beddington--DeAngelis, Crowley--Martin: $c\ge 0$, $c=0$ is Holling II', 'M',
  r'\cite{beddington1975,deangelis1975,crowley1989}.', 'S11a', [], ''),
 ('P8', r'Hassell--Varley: $0<\gamma<1$', 'M, C', r'$\gamma=0$: Holling II; $\gamma=1$: ratio dependence; the interval is a convention \cite{hassell1969}.', 'S11b', [], ''),
 ('P9', r'Mutual interference: $0\le\nu<1$; for $\nu>0$ solutions from $y=0$ are not unique, unless a predator Allee effect, a gestation delay, predator immigration or a Leslie--Gower predator equation keeps them unique', 'M',
  r'$\nu<1$ makes predation vanish without predators \cite{hassell1971}; explicit second solution from $y=0$. Predator Allee effect: gain of order $y^{2-\nu}$; delay: the gain uses $y(t-\tau)$ (method of steps); immigration: $\dot y>0$ at $y=0$; Leslie--Gower: logistic in $y$.',
  'S11c,S11d,S33', [], 'Non-uniqueness added at review; exceptions added at the second evaluation.'),
 ('P10', r'Ratio dependence: Lipschitz after extension by 0, not differentiable at $(0,0)$; in the basic model with one logistic prey and one predator the origin can attract all orbits', 'M, Q',
  r'Bounded partial derivatives; direction-dependent derivative. Sectors at the origin \cite{xiao2001rd}; global stability of the origin \cite{kuang1998}.',
  'S28,S28b', [('xiao2001rd', 'Ab', ''), ('kuang1998', 'Ab', '')],
  r'``Undefined at the origin\textquotedblright{} sharpened; ``blow-up techniques\textquotedblright{} removed (not in the abstracts). Second evaluation: the results on the origin are now stated only for the basic model.'),
 ('P11', r'Herd behaviour: $0<p<1$; $p=1/2$ for a planar herd', 'M', r'Edge of a disc-shaped herd scales as area$^{1/2}$ \cite{ajraldi2011}.', 'S8c',
  [('ajraldi2011', 'Ab', '')], ''),
 ('P12', r'Herd: not Lipschitz at 0; unique forward in time; prey can vanish in finite time, so not unique backward (not with prey immigration; with a fixed-number refuge the singular point is $x=\xi$)', 'M',
  r'$\dot x\le rx$; $\frac{d}{dt}x^{1-p}\to-(1-p)ay<0$; immigration gives $\dot x=I>0$ at $x=0$.', 'S8a,S8b,S8d,S30', [],
  r'``Uniqueness fails\textquotedblright{} was imprecise: forward uniqueness holds. Exceptions added at the second evaluation.'),
 ('P13', r'$0\le\phi<1$; $\xi\ge 0$', 'D', r'Protected fraction or number of prey \cite{maynardsmith1974,gonzalez2003}.', '', [], ''),
 ('P14', r'Fixed-number refuge ($\xi>0$) stabilises the Lotka--Volterra centre, a proportional one does not; refuges can destabilise other models', 'M, A',
  r'Proportional refuge rescales $a$; fixed number gives trace $-r\xi/(x^{*}-\xi)$. Attributed to \cite{maynardsmith1974}; caveat \cite{mcnair1986}.',
  'S29a,S29b', [('maynardsmith1974', 'N', ''), ('mcnair1986', 'Ab', '')], 'Earlier note replaced; McNair added.'),
 ('P15', r'$0\le\kappa<1$', 'D', r'Search efficiency lost to habitat complexity \cite{bairagi2011}.', '', [], ''),
 ('P16', r'$w\ge 0$; for $w>0$ with one food item, cooperation gives a component Allee effect for Holling I--IV and herd responses; with Beddington--DeAngelis iff $w>ac$; with Crowley--Martin near $y=0$ iff $w>ac(1+ahx)$, never at high $y$; never with ratio dependence; with Hassell--Varley or mutual interference only above a predator density; with additional food iff $e(1+a^{F}h^{F}\Lambda)>e^{F}a^{F}\Lambda h$', 'M',
  r'Sign of the $y$-derivative of the per-capita gain. With Leslie--Gower predators the gain does not contain the response.', 'S17,S31a,S31b,S31c,S31d,S31e,S31f', [],
  r'Second evaluation: the note claimed a component Allee effect for every response; interference can outweigh cooperation.'),
 ('P17', r'Cooperation can produce demographic Allee effects and predator collapse (stated where the per-capita gain increases with predator density)', 'Q', r'\cite{teixeiraalves2017}.', '',
  [('teixeiraalves2017', 'Ab', '')], r'``Bistability\textquotedblright{} replaced by the abstract\'s wording; restricted as P16 at the second evaluation.'),
 ('P18', r'Additional food: loss $ax/(1+ahx+a_Ah_AA)$, gain $(eax+e_Aa_AA)/(1+ahx+a_Ah_AA)$; $\eta=a_A/a$, $\alpha=h_A/h$, $e_A=e$ in Srinivasu et al.', 'M, A',
  r'Time budget (derived); quality--quantity parameterisation and the role of handling times from \cite{srinivasu2007}.', 'S12,S12b,S12c',
  [('srinivasu2007', 'Ab', '')], r'The form with one handling time ($\alpha=1$) and $e_A=e$ was replaced by the general form.'),
 ('P19', r'Holling II (T2.2): a predator with death rate $m$ persists only if $e/h>m$', 'M',
  r'Per-capita gain $e\,ax/(1+ahx)-m<e/h-m$ for all $x$, so the predator declines at every prey density when $e/h\le m$ (intake saturates at $1/h$, S9).', 'S9,S42f', [],
  'Added 19 October 2026 (audit of the entries table).'),
 ('P20', r'Power-law interactions (T2.16), $\beta<1$: the prey loss $axy^{\beta}$ is not Lipschitz at $y=0$, but the predator equation keeps the factor $y$, so $y=0$ is invariant and solutions from $y=0$ are unique (unlike T2.10)', 'M',
  r'$\dot y=y(ex^{p}-m-\delta y^{q})$ vanishes at $y=0$ with a finite $y$-derivative there; Gronwall then forces $y\equiv0$.', 'S43', [],
  'Added 20 October 2026 (referee report: an earlier draft grouped T2.16 with the non-unique case).'),
])

sec('Predator ($T_3$, $T_4$)', [
 ('N1', r'$e>0$; $e<1$ when densities are biomass or energy', 'M', r'Predation changes $x+y$ by $-(1-e)fy$.', 'S13a', [], ''),
 ('N2', r'$m>0$', 'D', r'Natural death rate.', '', [], ''),
 ('N3', r'$\psi>0$; predator Allee makes $y=0$ locally stable, unless predator immigration (a small stable equilibrium instead) or constant-yield harvest ($y=0$ reached in finite time); $T_3=e\,q(y)\,T_2$', 'M',
  r'Mate-finding factor $q=y/(y+\psi)$ \cite{courchamp2008}.', 'S16,S32b',
  [], r'Marked as an exception to Rule~1 ($\S$). Second evaluation: the note claimed local stability of $y=0$ also with predator immigration.'),
 ('N4', r'$\tau\ge 0$; initial data on $[-\tau,0]$; $T_3(t)=e\,s\,T_2(t-\tau)$', 'D', r'\cite{cushing1977book,kuang1993}.', '', [],
  r'Marked as an exception to Rule~1 ($\ddagger$).'),
 ('N5', r'Delay-dependent parameters: stability switches, often stable, unstable, stable again; oscillations in a window of maturation delays', 'Q',
  r'\cite{beretta2002,gourley2004}.', '', [('beretta2002', 'Ab', ''), ('gourley2004', 'Ab', '')], 'Source added.'),
 ('N6', r'$\delta^{J}\ge 0$; juvenile survival $\exp(-\delta^{J}\tau)$', 'M', r"Solution of $J'=-\delta^{J}J$ over the delay \cite{gourley2004}.", 'S15', [], ''),
 ('N7', r'$\delta\ge 0$', 'D', r'Density-dependent predator mortality \cite{bazykin1998}.', '', [], ''),
 ('N8', r"$\beta_{jj'}\ge 0$", 'D', r'Interference competition between predators.', '', [], ''),
 ('N9', r'Leslie--Gower: $s,\eta>0$; $\eta$ = predators supported per unit prey', 'M', r'Predator equilibrium $y=\eta x$ \cite{leslie1960}.', 'S18c', [], ''),
 ('N10', r'Leslie--Gower singular without prey; $C>0$ removes it', 'M', r'\cite{azizalaoui2003}.', 'S18a,S18b', [], ''),
])

sec('Predators eating predators', [
 ('Y1', r'$a^{y},h^{y},\rho^{y},\lambda^{y},\eta^{y}>0$', 'D', r'As for prey links, indexed by eaten and eating predator.', '', [], ''),
 ('Y2', r'$e^{y}>0$; $e^{y}<1$ when densities are biomass or energy', 'M', r'Mass balance as in N1.', 'S13a', [], ''),
 ('Y3', r'Cannibalism: $e^{y}_{ll}\le 1$ in any units; if violated, blow-up in finite time for $h=0$, at most exponential growth for $h>0$', 'M',
  r'Unstructured model: numbers proportional to biomass; net link $(e^{y}-1)a^{y}y^{2}/D$.', 'S13a,S14a,S14b,S14c', [],
  r'The blow-up was stated without the restriction $h=0$; with handling time it cannot occur (S14c).'),
 ('Y4', r'Cannibalism can stabilise and raise both standing stocks (one prey, one predator)', 'Q', r'\cite{kohlmeier1995}.', '', [('kohlmeier1995', 'Ab', '')],
  'Second finding added; restricted to one prey and one predator at the second evaluation.'),
 ('Y5', r'Intraguild predation: coexistence needs the intraguild prey to be the better competitor and the intraguild predator to gain substantially; most likely at intermediate productivity',
  'Q', r'\cite{holt1997}; review \cite{polis1989}.', '', [('holt1997', 'Ab', ''), ('polis1989', 'N', '')],
  r'``Only at intermediate productivity\textquotedblright{} and the missing second condition corrected.'),
 ('Y6', r'Holling II food chains can be chaotic', 'Q', r'\cite{hastings1991}.', '', [('hastings1991', 'Ab', '')], ''),
 ('Y7', r'Reciprocal predation between two predators: existence and stability of equilibria, Hopf bifurcation at the two positive equilibria', 'Q',
  r'\cite{almohanna2025}.', '', [('almohanna2025', 'Ab', '')], ''),
 ('Y8', r'No cannibalism with Leslie--Gower', 'C', r"Builder choice: the predator's capacity would depend on its own density.", '', [], ''),
 ('Y9', r'Refuge, habitat, cooperation, herd and group defence act on prey links only', 'C', r'Builder choice, stated in a note.', '', [], ''),
])

sec(r'Added terms ($\Phi$)', [
 ('H1', r'$q,E,H\ge 0$; $\ell$ constants $>0$', 'D', r'\cite{clark1976,brauer1979,gupta2013,chaudhuri1996}.', '', [], ''),
 ('H2', r'Effort harvest: prey alone persists iff $qE<r$ (without prey immigration)', 'M', r'Exponential, logistic, $\theta$-logistic and delayed logistic prey; equilibrium $K(1-qE/r)^{1/\theta}$.', 'S19a,S19b', [],
  r'Second evaluation: not stated with immigration, which keeps the prey alive at any effort.'),
 ('H3', r'Constant yield, logistic prey: a positive equilibrium needs $H\le rK/4$ and a stable one $H<rK/4$ (without prey immigration or seasonal forcing)', 'M', r'Maximum of $rx(1-x/K)$ is $rK/4$ at $K/2$; the larger equilibrium is stable \cite{brauer1979}.', 'S20,S20b', [],
  r'Second evaluation: not stated with immigration or seasonal forcing, which change the threshold.'),
 ('H4', r'Constant yield must stop at zero density', 'M', r'At $x=0$ the right side is $-H<0$.', 'S21', [], ''),
 ('H5', r'$I\ge 0$; immigration makes the Lotka--Volterra centre asymptotically stable (stated only for the classical model)', 'M, A',
  r'Trace $=-I/x^{*}<0$ (derived). Tahara et al.: analytic for linear predation, under stated conditions for types II and III.', 'S22',
  [('tahara2018', 'F', r'Eq.~(1), Case A1 ($\gamma=bc/2m$); Eq.~(4), Table~1 and Suppl.\ Tables S2--S5')],
  r'``For three types of functional response\textquotedblright{} (abstract) qualified after reading the full text. Second evaluation: shown only when the rest of the model is classical.'),
 ('H6', r'$\zeta\ge 0$ (prey kill predators without gain)', 'D', r'\cite{tang2015}.', '', [], ''),
 ('H7', r'Prey eat predators: $e^{x}>0$; $e^{x}<1$ in biomass units', 'M', r'$x+y$ changes by $-(1-e)axy-(1-e^{x})\zeta xy$.', 'S13b', [], ''),
 ('H8', r'$\vartheta\ge 0$, $g>0$', 'D', r'Toxic prey \cite{chattopadhyay2002}.', '', [], ''),
 ('H9', r'Predator harvesting ($\Phi_y$.1) with logistic prey and linear predation: the predator persists iff $m+q_2E_2<eaK$', 'M',
  r'Interior equilibrium $x^{*}=(m+q_2E_2)/(ea)$, $y^{*}=r(1-x^{*}/K)/a>0$ iff $x^{*}<K$; model of \cite{chaudhuri1996}.', 'S42a', [],
  'Added 19 October 2026 (audit of the entries table).'),
 ('H10', r'Anti-predator attack ($\Phi_y$.2): the predator cannot persist if $\zeta\ge ea$', 'M',
  r'Per-capita predator growth $(ea-\zeta)x-m\le -m<0$ for every $x\ge 0$; model of \cite{tang2015}.', 'S42b', [],
  'Added 19 October 2026 (audit of the entries table).'),
])

sec(r'New state variables ($\mathbf z$)', [
 ('Z1', r'Competing predators (z.9): with one prey, only the predator with the lowest break-even prey density ($m_i/(e_ia_i)$ for linear responses) persists at equilibrium', 'M, Q',
  r'At the prey level $x^{*}=m_1/(e_1a_1)$ where predator 1 is at equilibrium, predator 2 has per-capita growth $e_2a_2x^{*}-m_2<0$ iff $m_1/(e_1a_1)<m_2/(e_2a_2)$ (derived); the exclusion principle for saturating responses is \cite{hsu1978}, and \cite{armstrong1980} give the conditions for coexistence on one prey.', 'S42d',
  [('hsu1978', 'Ab', ''), ('armstrong1980', 'Ab', '')], 'Added 19 October 2026 (audit of the entries table).'),
 ('Z2', r'Metapopulation (z.16): the occupied fraction persists iff $c>\epsilon$', 'M',
  r'Equilibrium $p^{*}=1-\epsilon/c$ is positive iff $c>\epsilon$, and then stable ($\mathrm d\dot p/\mathrm dp=\epsilon-c<0$); $p=0$ is stable iff $c<\epsilon$; model of \cite{levins1969}.', 'S42e', [],
  'Added 19 October 2026 (audit of the entries table).'),
])

sec('Framework and general statements', [
 ('F1', r'$D^{x},D^{y}>0$; no-flux boundary conditions', 'D', r'\cite{skellam1951}.', '', [], ''),
 ('F2', r'Turing instability (one prey, one predator, no delay or seasonal forcing) iff $D^{x}D^{y}\mu_k^{2}-(D^{y}J_{11}+D^{x}J_{22})\mu_k+\det J<0$ for a no-flux eigenvalue $\mu_k>0$ of $-\Delta$ on $\Omega$; such a band exists iff $D^{y}J_{11}+D^{x}J_{22}>0$ and $(D^{y}J_{11}+D^{x}J_{22})^{2}>4D^{x}D^{y}\det J$; impossible for $J_{22}=0$; possible with $J_{22}<0$ (faster predator) or $J_{22}>0$ (faster prey)', 'M',
  r'Dispersion relation with $k^{2}=\mu_k$; self-limitation \cite{segel1972}; cooperation example. More species: an eigenvalue of $J-\mu_kD$ with positive real part.', 'S27a,S27b,S27c,S27d,S27e,S27f', [('segel1972', 'N', '')],
  r'``Turing patterns need predator self-limitation\textquotedblright{} was wrong: predator self-enhancement with faster prey diffusion also works (S27f). Second evaluation: the bounded-domain eigenvalue condition added; the two-species conditions are no longer stated for food webs, delays or seasonal forcing.'),
 ('F3', r'It\^o noise ($\sigma>0$), prey alone: stationary density iff $r>\sigma^{2}/2$ (logistic, $\theta$-logistic), $r-d>\sigma^{2}/2$ (fear, $c^{x}>0$), always (Gompertz); extinction a.s.\ when reversed; not stated with prey immigration or seasonal forcing. Positivity: not with constant yield, and the herd loss $x^{p}$ is not covered', 'M',
  r'Zero-flux stationary densities; comparison for $d\ln x$; noise as in \cite{rudnicki2003}.', 'S26a,S26b,S26c,S26d,S26e,S26f,S26g', [('rudnicki2003', 'N', '')],
  r'``Persists\textquotedblright{} was undefined and rested on the low-density drift only; now defined by the stationary density. Second evaluation: exceptions to positivity and to the prey-alone results added.'),
 ('F4', r'Non-negative orthant invariant, except with constant-yield harvest', 'M', r'Quasi-positivity of every term except $-H$.', 'S30,S21', [], ''),
 ('F5', r'Parameters non-negative unless their constraint says otherwise', 'D', r'The weak-Allee threshold $A$ may be negative.', '', [], 'General note corrected.'),
 ('F6', r'Regularity: Gompertz unique; herd unique forward only; interference not unique forward; ratio dependence Lipschitz; Leslie--Gower singular', 'M',
  r'Table~\ref{M-tab:regularity}.', 'S7b,S8d,S11d,S28b,S18a', [], r'Rule~4 listed three cases under one heading; now classified.'),
 ('F7', r'Demographic noise of order $N^{-1/2}$ sustains large quasi-cycles around a stable equilibrium', 'Q',
  r'Individual-level model; Volterra mean field with a stable equilibrium; resonant power spectrum \cite{mckane2005}.', '',
  [('mckane2005', 'F', r'arXiv:\allowbreak q-bio/\allowbreak 0501023, Eqs.~(3), (6), (9); Fig.~2')], ''),
])

sec('Classical results', [
 ('K1', r'Lotka--Volterra: centre at $(m/ea,\,r/a)$, first integral $H$', 'M', r'\cite{lotka1925,volterra1926}.', 'S23', [], ''),
 ('K2', r'Logistic prey, Holling I: interior equilibrium iff $m<eaK$, globally stable', 'M', r'$\dot V=-(er/K)(x-x^{*})^{2}\le 0$ and LaSalle.', 'S24', [], ''),
 ('K3', r'Rosenzweig--MacArthur: $x^{*}=m/[a(e-mh)]$, exists iff $e>mh$, $x^{*}<K$; then hyperbolic and stable iff $x^{*}>\tfrac12(K-1/ah)$, unstable below, weakly attracting at equality (K4)', 'M',
  r'Trace $\propto(x_{\rm hump}-x^{*})$; $\det J=mr[Ka(e-mh)-m]/(Kae)$ \cite{rosenzweig1963}.', 'S25a,S25b,S25c', [],
  r'The sign of $\det J$ was checked at random parameter values; now proved in general.'),
 ('K4', r'Supercritical Hopf at $x^{*}=x_{\rm hump}$; unique limit cycle beyond it; paradox of enrichment', 'M, Q',
  r'$16\omega^{2}\ell_1=-4\beta s/[(1+s)^{2}(1+2s)^{2}]$; cross-check with a second formula. Limit cycle \cite{cheng1981}; enrichment \cite{rosenzweig1971}.',
  'S25d0,S25d,S25e', [('cheng1981', 'Ab', ''), ('rosenzweig1971', 'Ab', '')],
  r'The sign of $\ell_1$ was sampled at 12 parameter sets; now proved in general.'),
])

sec('Entries added after the scoping review', [
 ('X1', r'Food-limited growth (T1.12): $c>0$; $c\to\infty$ gives the logistic law; the per-capita rate falls from $r$ at $x=0$ to $0$ at $x=K$, so the prey-only equilibrium stays $K$', 'D, M',
  r'Replacement rate at saturation $c$; form of \cite{smith1963}, Eq.~(5); values, limit and derivative of the per-capita rate.', 'S34a,S34b,S34c',
  [('smith1963', 'F', r'Eq.~(5) and definitions, pp.~652--653')], 'Added 19 October 2026 (scoping review, Stage C).'),
 ('X2', r'Sexual reproduction (T3.7): births in proportion to encounters of males and females, $cy^{2}$, with a Leslie--Gower loss $wy^{2}/(x+D)$', 'A',
  r'Top predator of the food chain in \cite{upadhyay1997}, written here for one prey and one predator.', '',
  [('upadhyay1997', 'F', r'Eq.~(1c) and text, p.~1934')], 'Added 19 October 2026.'),
 ('X3', r'Sexual reproduction (T3.7): the per-capita gain is positive iff $x>w/c-D$; if $x\ge x_0>w/c-D$ for all $t$, $y$ blows up in finite time', 'M',
  r'Comparison with $\dot y=ky^{2}$, $k=c-w/(x_0+D)>0$.', 'S35a,S35b', [], 'Added 19 October 2026.'),
 ('X4', r'Allelopathy ($\Phi_x$.7): a predator toxin kills prey at per-capita rate $\gamma xy^{2}$; between two competitors the per-capita rates are $\gamma_iN_1N_2$', 'Q',
  r'\cite{fitria2015,chattopadhyay1996}.', '',
  [('fitria2015', 'F', r'Eq.~(1), p.~59'), ('chattopadhyay1996', 'F', r'Eq.~(1), p.~287')], 'Added 19 October 2026.'),
 ('X5', r'Advection (S.7): logistic prey alone spread upstream iff $v<2\sqrt{rd_1}$', 'A',
  r'Upstream speed $c^{*}-v$ with the Fisher speed $c^{*}=2\sqrt{rd_1}$ \cite{hilker2010}.', '',
  [('hilker2010', 'F', r'Eqs.~(1)--(2) and invasion speeds, pp.~176--177')], 'Added 19 October 2026.'),
 ('X6', r'Spatial heterogeneity (S.8): with lethal boundaries, logistic prey with growth rate $r(\xi)$ of either sign persist if $1/d_1>\lambda_1^{+}(r)$; fragmenting favourable habitat hinders persistence', 'A',
  r'Stated in \cite{cantrell1989} for $\Delta u+\lambda u(m-u)=0$; here $\lambda=1/d_1$. Predator--prey version in \cite{du2004}.', '',
  [('cantrell1989', 'Ab', ''), ('du2004', 'F', r'model (1.1), p.~332')], 'Added 19 October 2026.'),
 ('X7', r'Feedback control (M.3), logistic prey: the equilibrium falls to $K/(1+cqK/f)$ and is locally asymptotically stable', 'M',
  r'Model of \cite{gopalsamy1993}; Jacobian at the equilibrium.', 'S36a,S36b',
  [('gopalsamy1993', 'F', r'model in the abstract and Sec.~1')], 'Added 19 October 2026.'),
 ('X8', r'Hybrid control (M.3): $\alpha F+(1-\alpha)\,\mathrm{id}$ keeps the fixed points and maps each eigenvalue $\lambda$ to $\alpha\lambda+1-\alpha$', 'M',
  r'Form of \cite{luo2003}.', 'S36c', [('luo2003', 'F', r'Eq.~(2), p.~776')], 'Added 19 October 2026.'),
 ('X9', r'Z-type control (M.3): the deviation $x-x_d$ from a target decays exponentially', 'Q',
  r'\cite{lacitignola2016}.', '', [('lacitignola2016', 'F', r'Sec.~2.1, Eq.~(2), p.~11')], 'Added 19 October 2026.'),
 ('X10', r'Economic profit constraint (M.4): with one harvested species and zero profit, the effort settles where rent vanishes, $x=c_x/p_x$', 'M',
  r'Bionomic equilibrium of \cite{gordon1954}; algebraic equation of \cite{zhang2009bioecon}.', 'S37',
  [('zhang2009bioecon', 'F', r'model (1), p.~579')], 'Added 19 October 2026.'),
 ('X11', r'Economic profit constraint (M.4): a singularity-induced bifurcation occurs at a critical profit', 'Q',
  r'\cite{zhang2009bioecon}.', '', [('zhang2009bioecon', 'F', r'abstract and Sec.~3')], 'Added 19 October 2026.'),
 ('X12', r'Mutualist of the prey (z.20): predation decreases with the mutualist, which gains from the prey and is self-limited; its effect on prey growth may have either sign', 'Q',
  r'\cite{rai1983}.', '', [('rai1983', 'F', r'hypotheses (H1), (G1), (P1), pp.~16--17')], 'Added 19 October 2026.'),
 ('X13', r'A protective population that lowers predation on the prey (human shield) is a special case of z.20', 'C',
  r'Our classification in the scoping review (Stage C).', '', [], 'Added 19 October 2026.'),
 ('X14', r'Scavenger (z.21): gains from kills and natural deaths at no cost to $x$ or $y$; self-limitation keeps it bounded; it may also prey on $x$', 'Q',
  r'\cite{nolting2008,previte2013}.', '',
  [('nolting2008', 'F', r'Eq.~(3), p.~217'), ('previte2013', 'F', r'Eq.~(3.1), p.~528')], 'Added 19 October 2026.'),
 ('X15', r'Sex structure (z.22): one sex produces both; the sexes share density dependence and are eaten alike', 'Q',
  r'Model of Liu (2005), quoted in \cite{xiong2007}.', '', [('xiong2007', 'F', r'model (1.1), p.~1214')], 'Added 19 October 2026.'),
 ('X16', r'Lateral dimorphism (z.23): with rates symmetric between morphs, the symmetric state is invariant', 'M',
  r'Model 1 of \cite{nakajima2004}.', 'S38', [('nakajima2004', 'F', r'Model~1, p.~693')], 'Added 19 October 2026.'),
 ('X17', r'Lateral dimorphism (z.23): when cross predation dominates, the morph frequencies oscillate around $1/2$, and a missing morph can invade', 'Q',
  r'\cite{takahashi1994,nakajima2004}.', '',
  [('nakajima2004', 'F', r'abstract, p.~692'), ('takahashi1994', 'Ab', '')], 'Added 19 October 2026.'),
 ('X18', r'Power-law interactions (T2.16): Gilpin--Ayala predator--prey systems raise each density in each per-capita rate to its own power (prey loss $ay^{\beta}$, predator gain $e\,x^{p}$, self-limitation $\delta y^{q}$)', 'Q',
  r'Discrete system of \cite{liao2007gilpin}; the continuous system of \cite{chen2005gilpin} as quoted there.', '',
  [('liao2007gilpin', 'F', r'systems (1.1) and (1.6), pp.~500--501')], 'Added 19 October 2026 (adjudication of the blind check).'),
 ('X19', r'Power-law interactions (T2.16): with $0<p<1$ the predator gain exceeds the prey loss at low prey density, so in biomass units the model creates biomass', 'M',
  r'Ratio gain/loss $=(e/a)x^{p-1}y^{1-\beta}\to\infty$ as $x\to0^{+}$ (Rule~2).', 'S39', [], 'Added 19 October 2026.'),
 ('X20', r'Independent numerical response (T3.8): the predator\'s demographic rates can be modelled as their own function of food availability (demographic numerical response)', 'Q',
  r'\cite{bayliss2002}.', '', [('bayliss2002', 'Ab', '')], 'Added 19 October 2026 (adjudication of the blind check).'),
 ('X21', r'Independent numerical response (T3.8): in biomass units the gain may not exceed the intake, $e\,g\le f$; a Monod--Haldane gain with a Beddington--DeAngelis loss violates this as $y\to\infty$', 'M',
  r'Rule~2; limit of $g/f$ as $y\to\infty$.', 'S40', [], 'Added 19 October 2026.'),
 ('X22', r'Starvation mortality (T4.4): extra death rate $T^{-1}\ln(\bar f/f)$ of a predator receiving the ration $f\le\bar f$; zero at satiation, decreasing in the ration, unbounded as $f\to0$', 'Q, M',
  r'Form of \cite{arditi1978}, adapted there from an ecosystem model; properties derived.', 'S41a',
  [('arditi1978', 'F', r'Eqs.~(10)--(13), pp.~179--180')], 'Added 19 October 2026 (adjudication of the blind check).'),
 ('X23', r'Starvation mortality (T4.4): at a constant ration $f_1$ and without births, the hunger term alone shrinks the predator by the factor $f_1/\bar f$ in time $T$', 'Q, M',
  r'Stated by \cite{arditi1978} as the reason for the form; verified.', 'S41b',
  [('arditi1978', 'F', r'Eq.~(14) and Fig.~3, pp.~180--181')], 'Added 19 October 2026.'),
 ('X24', r'Self- and cross-diffusion (S.2): self-diffusion $\alpha\ge0$ and cross-diffusion $\beta\ge0$', 'D',
  r'Broadened from cross-diffusion alone when the author adjudicated the blind check; model of \cite{shigesada1979}.', '', [],
  'S.2 broadened 19 October 2026.'),
 ('X25', r'Taxis (S.3): the prey-taxis term also models immature prey moving toward higher densities of mature prey', 'Q',
  r'\cite{li2023taxis}.', '', [('li2023taxis', 'F', r'model (3) and its explanation, p.~18593')], 'S.3 broadened 19 October 2026.'),
])

# ------------------------------------------------------------------ consistency
rows_all =[row for _, rows in S for row in rows]
cited = {k for row in rows_all for k in re.findall(r'\\cite\{([^}]+)\}', row[3]) for k in k.split(',')}
cited |= {k for row in rows_all for (k, _, _) in row[5]}
missing = sorted(cited - bibkeys)
assert not missing, f'keys missing from lv_references.bib: {missing}'
bad = [c for row in rows_all for c in row[4].split(',') if c and c not in checks]
assert not bad, f'unknown check ids: {bad}'
for row in rows_all:
    if re.search(r'\b[QA]\b', row[2]):
        assert row[5], f'{row[0]}: literature statement without evidence'

LEVEL = {'F': 'full text', 'Ab': 'abstract', 'T': 'title', 'N': 'not accessed'}


def status(ids):
    if not ids:
        return ''
    ok = all(checks[c]['pass'] for c in ids.split(','))
    return (r'\checkmark\,' if ok else r'\textbf{FAIL} ') + ids.replace(',', ', ')


def evidence(ev, short=False):
    out = []
    for k, lev, loc in ev:
        s = rf'\cite{{{k}}}: {LEVEL[lev]}'
        if lev == 'F' and loc:
            s += f' ({loc})'
        out.append(s)
    return '; '.join(out)


def esc(s):
    return s.replace("\\'", "'")


# ------------------------------------------------------------------ main-text table (no pure definitions)
main_rows = [(t, [r for r in rows if r[2] != 'D']) for t, rows in S]
n_main = sum(len(r) for _, r in main_rows)
cnt = {b: sum(1 for r in rows_all if b in [x.strip() for x in r[2].split(',')]) for b in 'DCMQA'}
lines = [
    r'% Generated by figure/tools/make_provenance.py -- edit the script, not this file.',
    r'\begingroup\small',
    r'\setlength{\LTcapwidth}{\textwidth}',
    r'\begin{longtable}{@{}>{\raggedright\arraybackslash}p{0.06\textwidth}>{\raggedright\arraybackslash}p{0.46\textwidth}>{\centering\arraybackslash}p{0.06\textwidth}>{\raggedright\arraybackslash}p{0.34\textwidth}@{}}',
    r'\caption{Provenance of the constraints and results stated in this review and in the model builder (all statements except pure definitions; '
    r'the full table, with definitions, explanations and the corrections made, is Table~\ref{S-tab:provenance-full} in the Supplement). '
    r'Basis: M, derived here and checked symbolically (check IDs, Supplement Table~\ref{S-tab:symbolic-checks}); C, convention; '
    r'Q, quoted from the source; A, adapted from the source; D, definition. Evidence for Q and A: the part of the source that was read. '
    r'Where the parameter table of the model builder uses other symbols than the text, the rows follow the builder (for example $\mu$ for $n$ in T1.3, '
    r'$\nu$ for $\mu$ in T2.10, $w$ for $\lambda$ in T2.14, $\psi$ for $\theta$ in T3.3, $\eta$ and $C$ for $n$ and $k$ in T3.5--T3.6, $\zeta$ for $\eta$ in $\Phi_y$.2). '
    rf'Last update: {LAST_UPDATE}.}}\label{{tab:constraint-provenance}}\\',
    r'\toprule ID & Constraint or result & Basis & Checks or evidence \\ \midrule \endfirsthead',
    r'\toprule ID & Constraint or result & Basis & Checks or evidence \\ \midrule \endhead',
    r'\bottomrule \endfoot',
]
for title, rows in main_rows:
    if not rows:
        continue
    lines.append(rf'\multicolumn{{4}}{{@{{}}l}}{{\textit{{{title}}}}}\\[2pt]')
    for (i, c, ty, basis, ids, ev, corr) in rows:
        parts = [p for p in (status(ids), evidence(ev)) if p]
        lines.append(f'{i} & {esc(c)} & {ty} & {"; ".join(parts)} \\\\')
    lines.append(r'\addlinespace')
lines += [r'\end{longtable}', r'\endgroup', '']
(FIG / 'constraint_provenance.tex').write_text('\n'.join(lines), encoding='utf-8', newline='\n')

# ------------------------------------------------------------------ supplementary table (everything)
lines = [
    r'% Generated by figure/tools/make_provenance.py -- edit the script, not this file.',
    r'\begingroup\footnotesize\sloppy',
    r'\setlength{\LTcapwidth}{\textwidth}',
    r'\begin{longtable}{@{}>{\raggedright\arraybackslash}p{0.05\textwidth}>{\raggedright\arraybackslash}p{0.2\textwidth}>{\centering\arraybackslash}p{0.05\textwidth}>{\raggedright\arraybackslash}p{0.23\textwidth}>{\raggedright\arraybackslash}p{0.16\textwidth}>{\raggedright\arraybackslash}p{0.16\textwidth}@{}}',
    r'\caption{Full provenance of every constraint and stated result, with the corrections made while tracing them. Basis: D, definition; C, '
    r'convention; M, derived and checked symbolically (Table~\ref{tab:symbolic-checks}); Q, quoted; A, adapted. Evidence: full text (with '
    r'location), abstract, title, or not accessed. Where the parameter table of the model builder uses other symbols than the main text, the rows '
    r'follow the builder (for example $\mu$ for $n$ in T1.3, $\nu$ for $\mu$ in T2.10, $w$ for $\lambda$ in T2.14, $\psi$ for $\theta$ in T3.3, '
    r'$\eta$ and $C$ for $n$ and $k$ in T3.5--T3.6, $\zeta$ for $\eta$ in $\Phi_y$.2). '
    rf'Last update: {LAST_UPDATE}.}}\label{{tab:provenance-full}}\\',
    r'\toprule ID & Statement & Basis & Explanation and source & Checks and evidence & Correction history \\ \midrule \endfirsthead',
    r'\toprule ID & Statement & Basis & Explanation and source & Checks and evidence & Correction history \\ \midrule \endhead',
    r'\bottomrule \endfoot',
]
for title, rows in S:
    lines.append(rf'\multicolumn{{6}}{{@{{}}l}}{{\textit{{{title}}}}}\\[2pt]')
    for (i, c, ty, basis, ids, ev, corr) in rows:
        parts = [p for p in (status(ids), evidence(ev)) if p]
        lines.append(f'{i} & {esc(c)} & {ty} & {esc(basis)} & {"; ".join(parts) or "--"} & {esc(corr) or "--"} \\\\')
    lines.append(r'\addlinespace')
lines += [r'\end{longtable}', r'\endgroup', '']
(FIG / 'constraint_provenance_full.tex').write_text('\n'.join(lines), encoding='utf-8', newline='\n')

# ------------------------------------------------------------------ full-text checklist (markdown)
def plain(s):
    s = re.sub(r'\\cite\{([^}]+)\}', lambda m: '[' + m.group(1) + ']', s)
    s = s.replace(r'\textquotedblright{}', '"').replace('``', '"').replace(r'\,', ' ').replace('~', ' ')
    return s.replace('\\allowbreak ', '')


md = ['# Full-text checklist for the literature statements', '',
      f'Generated by `figure/tools/make_provenance.py` on {LAST_UPDATE}. Each line is a statement of the review that rests on a',
      'source whose full text we could not read (closed access, or a repository behind a bot check). Please check the statement',
      'against the full text, note the theorem, equation, section or page that supports it, and change the evidence entry in',
      '`make_provenance.py` from `Ab`/`T`/`N` to `F` with that location. If the full text says something different, tell us and the',
      'statement will be corrected.', '',
      '| ID | Source | Current evidence | Statement to verify | Where to look |',
      '|---|---|---|---|---|']
WHERE = {
    'wang2011allee': 'main theorem on the threshold curve and heteroclinic loops',
    'zanette2011': 'results: offspring per year with predator playbacks vs controls',
    'wang2016fear': 'theorems on periodic solutions and Hopf bifurcation for large and small fear',
    'cushing1977': 'statement on periodic solutions under periodic coefficients',
    'rinaldi1993': 'bifurcation diagrams: multiple attractors and chaos',
    'xiao2001siam': 'theorem on the Bogdanov--Takens bifurcation of codimension 2',
    'xiao2001rd': 'theorem on the sectors of the origin',
    'kuang1998': 'theorems on global stability of each equilibrium, the origin included',
    'ajraldi2011': 'derivation of the square-root response and finite-time extinction',
    'maynardsmith1974': 'discussion of refuges protecting a fixed number vs a fixed proportion',
    'mcnair1986': 'conclusion that refuges can destabilise',
    'teixeiraalves2017': 'results on demographic Allee effects, persistence and collapse',
    'srinivasu2007': 'model equations: quality eta, handling ratio alpha, conversion of the additional food; results on handling times',
    'beretta2002': 'stability-switch criterion and the stable-unstable-stable sequence',
    'gourley2004': 'theorem on global attractivity for small and large delays',
    'kohlmeier1995': 'results on stabilisation and standing stocks',
    'holt1997': 'conditions for three-species coexistence and productivity',
    'polis1989': 'review of intraguild predation (context only)',
    'hastings1991': 'chaos in the three-species food chain',
    'almohanna2025': 'model equations (match with Phi_x.6 and Phi_y.4) and the Hopf theorems (authors\' own paper)',
    'segel1972': 'example of diffusion-driven instability with predator self-limitation',
    'rudnicki2003': 'the stochastic predator-prey model (context for E.1)',
    'cheng1981': 'theorem on uniqueness of the limit cycle',
    'rosenzweig1971': 'paradox of enrichment',
    'cantrell1989': 'theorem on persistence for lambda above the principal eigenvalue; discussion of fragmented habitat (scanned copy)',
    'takahashi1994': 'conditions for the oscillation of morph frequencies under cross predation',
    'bayliss2002': 'definition of the demographic numerical response and the forms used for it',
    'hsu1978': 'competitive exclusion of predators on one prey by the lowest break-even prey density (Michaelis-Menten responses)',
    'armstrong1980': 'conditions under which several consumers coexist on one resource (nonequilibrium coexistence)',
}
n_md = 0
for title, rows in S:
    for (i, c, ty, basis, ids, ev, corr) in rows:
        for k, lev, loc in ev:
            if lev == 'F':
                continue
            md.append(f'| {i} | {k} | {LEVEL[lev]} | {plain(c)} | {WHERE.get(k, "")} |')
            n_md += 1
md += ['', 'Statements already checked against the full text:', '']
for title, rows in S:
    for (i, c, ty, basis, ids, ev, corr) in rows:
        for k, lev, loc in ev:
            if lev == 'F':
                md.append(f'- {i} ({k}): {plain(c)} -- {plain(loc)}')
(PAPER / 'fulltext_checklist.md').write_text('\n'.join(md) + '\n', encoding='utf-8', newline='\n')

n_lit = sum(1 for r in rows_all if re.search(r'\b[QA]\b', r[2]))
n_lit_full = sum(1 for r in rows_all if re.search(r'\b[QA]\b', r[2]) and any(lev == 'F' for (_, lev, _) in r[5]))
n_full = sum(1 for r in rows_all for (_, lev, _) in r[5] if lev == 'F')
print(f'statements: {len(rows_all)} (main table {n_main}); basis counts {cnt}; literature-based {n_lit} '
      f'({n_lit_full} with full-text evidence), full-text evidence items {n_full}; checklist items {n_md}')
json.dump({'n_rows': len(rows_all), 'n_main': n_main, 'basis': cnt, 'n_lit': n_lit, 'n_lit_full': n_lit_full, 'n_full': n_full,
           'n_checklist': n_md},
          open(FIG / 'provenance_stats.json', 'w', encoding='utf-8', newline='\n'))
