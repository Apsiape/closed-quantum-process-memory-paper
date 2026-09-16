# Bath dimension and initial entropy for closed repeated use of a quantum channel

Seth Douglas | [seth.douglas@gmail.com](mailto:seth.douglas@gmail.com)

This preprint studies a closed device that supplies repeated uses of a fixed
quantum channel against adaptive inputs. It charges both the entire bath
dimension and the actual entropy of its initial state, including retained seeds,
clocks, work registers and residues.

Read [the complete paper](manuscript.pdf), including both appendices and the
bibliography. The rate region is `s >= 0`, `r + s >= h`, `r - s >= kappa`, under
the definitions and limits stated in the paper. The proofs do not assume
efficient circuit synthesis or a finite optimizer for the extension cost.

## Contents

- `manuscript.md`, `appendix-causal-balancing.md`, `appendix-conventions.md`:
  authoritative mathematical prose.
- `manuscript.tex`, `manuscript.pdf`: the complete typeset paper.
- `COMPLETE-PROOF.md`: all three Markdown sources assembled without abridgment.
- `ancillary/`: finite diagnostics, Lean sources, pinned dependency information,
  coverage documentation and recorded kernel output.
- `scripts/`: portable build and package-verification helpers.
- `CITATION.cff`, `zenodo/`: citation metadata and separately scoped upload templates.
- `SOURCE-MAP.json`, `SHA256SUMS.txt`: source provenance and file-integrity records.

## Reproduce the paper and checks

Use Python 3.10 or newer, NumPy for numerical diagnostics, and pypdf for PDF
verification. Install dependencies through your normal environment management;
these helpers perform no installation or network access. Building the paper
also requires `pdflatex` with the packages named in manuscript.tex. Poppler is
needed only if you want to render page images for a new visual review.

From this directory:

```
python scripts/verify.py
python scripts/build.py
python scripts/verify.py --rebuilt build/manuscript.pdf
python -B ancillary/test_axiom_guard.py
```

The build makes three TeX passes into ignored `build/`, leaving the distributed
PDF untouched. The verifier checks the original distribution hashes, complete
source assembly, statement/citation counts, links and author metadata. With
`--rebuilt`, it also compares extracted page text to the distributed PDF;
timestamps and PDF identifiers can prevent byte-identical rebuilds. A changed
manuscript additionally requires visual inspection; text checks are not layout
certification. Use operating-system resource limits appropriate to your machine.

To run one finite diagnostic, for example:

```
cd ancillary
python gad_interior_example.py
```

Appendix B.4 states every diagnostic's finite dimensions, seeds, tolerances and
limitations. In this distribution, run those commands inside `ancillary/`.
They are sanity checks, not proofs of the optimization or asymptotic claims.

### Partial Lean coverage

[ancillary/COVERAGE.md](ancillary/COVERAGE.md) describes the precise formal scope.
The checked declarations establish a finite complex-density-matrix bath-only
closing identity, with arbitrary correlations and finite references, and six
natural-number accounting lemmas. The complete rate-region theorem, entropy
bounds, Gram repair, concentration and compiler are not Lean-formalized.

Lean 4.30.0 and the exact mathlib/package revisions are pinned in ancillary/.
The wrapper uses an existing compatible package cache and never downloads or
updates it. Recorded checks list only standard foundational axioms; no scientific
axiom or admission is accepted. Read the coverage file before attempting a kernel
rerun, and write new logs outside this distribution's checksummed files.

## Citation, licenses and provenance

Use [CITATION.cff](CITATION.cff) for the manuscript citation. The concept DOI
[10.5281/zenodo.22779672](https://doi.org/10.5281/zenodo.22779672) resolves to the
latest archived version; version 1.0.0 is
[doi:10.5281/zenodo.22779673](https://doi.org/10.5281/zenodo.22779673), and the
version DOI of 1.1.0 is recorded in CITATION.cff once assigned. The
[GitHub releases](https://github.com/Apsiape/closed-quantum-process-memory-paper/releases)
also provide each PDF directly. Release archives are immutable; subsequent
citation-only updates on main do not change a deposited version. No affiliation
or ORCID is asserted. The [Zenodo instructions](zenodo/README.md) explain the
aggregate Other (Open) category and explicit scoped licenses used for GitHub
ingestion. Separate records or DOIs are not required.

The manuscript and appendices are CC BY 4.0. Original Python/Lean code and its
software documentation are MIT-licensed. Full texts are in LICENSES/; third-party
material and dependencies retain their own rights. These are scoped licenses,
not blanket relicensing or dual licensing of every file.

AI-assisted development and independent AI-session checks are disclosed in the
paper; those checks are not human external peer review. SOURCE-MAP.json records
the exact scientific inputs and the nonrendering TeX-header cleanup used here.
No mathematical body text or distributed PDF bytes were changed for packaging.

The checksum manifest covers distributed files only. Build products and caches
are ignored; modified sources require a regenerated manifest and renewed checks.

## Revision history

- **1.1.0 (2026-09-16).** Proposition 7.5: the lower witness is now the exact
  rational input diag(7/12, 5/12), giving `kappa >= H_2(7/12) - H_2(1/3) =
  0.061572`. Version 1.0.0 displayed `0.045566` for the maximally mixed input, a
  decimal rounded up from 0.0455659970..., so the stated lower bound exceeded
  the proved one by three parts in a billion; the improvement of the witness was
  observed by N. Mghirbi. The upper witness is shown to be attained, the
  entropy-exchange lower bound is sharpened, Proposition 7.4 receives a direct
  proof from Definition 1.3, the derivations of the constants in the proof of
  Theorem 4.1 are written out (no constant changes), a small-error quantifier is
  added at the stability display, Theorem 2.1 is restated unconditionally, a
  conclusion section and one related-work comparison (Kotowski and Kotowski) are
  added, notation collisions are resolved (Slepian-Wolf receiver `N`, damping
  parameter `nu`), the exponents in Appendix A use parentheses instead of
  brackets, and two bibliography identifiers are corrected. No theorem statement
  changes. Three independent blind AI-session reviews of version 1.0.0 preceded
  these repairs; they are not human peer review.
- **1.0.0 (2026-09-15).** Initial release,
  [doi:10.5281/zenodo.22779673](https://doi.org/10.5281/zenodo.22779673).
