# Predator–Prey Model Builder

A browser-based tool that assembles predator–prey models from biological extensions of the
Lotka–Volterra equations. It is the companion software of the review *Where mechanisms enter the
Lotka–Volterra equations: a structured review of predator–prey extensions, their parameter constraints,
and a model builder*.

**Use it online:** https://almohanna-ai.github.io/predator-prey-model-builder/

## What it does

Choose the number of prey and predator species (up to four each), who eats whom (including predators
eating predators and cannibalism), a growth law for each prey species, a functional response, and the
extensions of each term of the classical model. The builder supports a defined set of compatible
extensions (44 of the 90 reviewed fully and 3 in part; see the coverage table in the review) and disables
combinations that the review's rules do not define. It then writes:

- the model, in expanded form and, when the food web is complete, in indexed form;
- a table of variables and parameters with their meaning, admissible range and index set;
- notes on known results and on conditions such as singularities or loss of positivity; a note states a
  result from the literature only when the model built satisfies that result's assumptions;
- the supporting references, each verified against Crossref, OpenAlex or library catalogues.

The model, the table, the notes and the references can be copied as LaTeX and BibTeX, or downloaded as one
complete LaTeX document. The choices can be saved to a JSON file and loaded again, and changing the number
of species keeps the existing feeding links.

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
| `verification/verify_constraints.py` | 105 symbolic checks (SymPy) of the derived constraints and results: 101 valid for all admissible parameter values, 2 worked instances, 1 sampled cross-check and 1 self-test; results in `constraint_checks.txt` |
| `verification/make_provenance.py` | builds the tables that trace every constraint to its basis (derived, quoted, adapted, definition or convention) and record how much of each source was read (`constraint_provenance.tex`, `constraint_provenance_full.tex`) |
| `verification/lv_references.bib`, `reference_verification.md` | the bibliography and the record of how each reference was checked |

To rerun the checks: `pip install sympy`, then `python verification/verify_constraints.py` and
`python verification/make_provenance.py`.

## How to cite

Please cite the review and this software. See `CITATION.cff`; the archived version has the DOI
`DOI-TO-BE-ADDED` (Zenodo). <!-- replace after the first Zenodo release -->

## License

The builder and the scripts are released under the MIT License (see `LICENSE`). MathJax, in `mathjax/`,
is distributed under the Apache License 2.0.
