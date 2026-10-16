# Predator–Prey Model Builder

A browser-based tool that assembles predator–prey models from biological extensions of the
Lotka–Volterra equations. It is the companion software of the review *Where mechanisms enter the
Lotka–Volterra equations: a structured review of predator–prey extensions, their parameter constraints,
and a model builder*.

**Use it online:** https://almohanna-ai.github.io/predator-prey-model-builder/

## What it does

Choose the number of prey and predator species (up to four each), who eats whom (including predators
eating predators and cannibalism), a growth law for each prey species, a functional response, and the
extensions of each term of the classical model. The builder then writes:

- the model, in expanded form and, when the food web is complete, in indexed form;
- a table of variables and parameters with their meaning, admissible range and index set;
- notes on known results and on conditions such as singularities or loss of positivity;
- the supporting references, each verified against Crossref, OpenAlex or library catalogues.

Everything can be copied as LaTeX and BibTeX.

## Running it

The page needs no installation and makes no network requests: open `index.html` in a recent web browser,
or serve the folder locally, for example with `python -m http.server`. Mathematical typesetting uses the
copy of MathJax 3.2.2 in `mathjax/`.

## Contents

| Path | Content |
|---|---|
| `index.html` | the builder (one self-contained page) |
| `mathjax/` | MathJax 3.2.2 (Apache License 2.0, see `mathjax/LICENSE`) |
| `src/` | source page and the script that injects the verified references into it |
| `verification/verify_constraints.py` | 57 symbolic checks (SymPy) of the derived parameter constraints; results in `constraint_checks.txt` |
| `verification/make_provenance.py` | builds the table that traces every constraint to its basis (`constraint_provenance.tex`) |
| `verification/lv_references.bib`, `reference_verification.md` | the bibliography and the record of how each reference was checked |

To rerun the symbolic checks: `pip install sympy`, then `python verification/verify_constraints.py`.

## How to cite

Please cite the review and this software. See `CITATION.cff`; the archived version has the DOI
`DOI-TO-BE-ADDED` (Zenodo). <!-- replace after the first Zenodo release -->

## License

The builder and the scripts are released under the MIT License (see `LICENSE`). MathJax, in `mathjax/`,
is distributed under the Apache License 2.0.
