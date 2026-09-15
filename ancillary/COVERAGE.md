# Partial Lean verification

The checked sources prove a finite-dimensional quantum closing identity, not the
paper's entropy bounds, causal compiler or asymptotic rate region.

## Exact quantum statement

`ActiveBath.lean` proves
`Tr_B[(I_A tensor U) rho (I_A tensor U*)] = Tr_B[rho]`
for every finite complex positive-semidefinite trace-one matrix rho on A times B
and every square U with `U* U = I`. A may contain every retained output and any
finite reference. Initial user-bath correlations are unrestricted. The result is
an exact equality, not a trace-distance approximation. It supports the bath-only
closing identity in Appendix A.4; it does not construct the closing operation or
causal schedule.

All declarations are in namespace `ClosedMemory`.

| Declarations | Scope |
| --- | --- |
| `Density`, `basisState` | Legal complex quantum states, including a concrete nonvacuity witness. |
| `partialTrace`, `bathLift`, `conjugate` | Explicit matrix sums, identity-on-user lift and conjugation. |
| `partialTrace_positive`, `partialTrace_trace`, `userState` | Reduced-state positivity and normalization. |
| `bathLift_adjoint`, `bathLift_isometry` | Algebra of the lifted isometry. |
| `conjugate_positive`, `conjugate_trace`, `closeBath` | Legality of the closed global state. |
| `bathBlock`, `bathBlock_conjugate`, `partialTrace_close` | Block reduction and exact partial-trace invariance. |
| `closing_preserves_complete_user` | End-to-end closing identity for density matrices. |

`BlockAccounting.lean` adds six elementary natural-number accounting statements.
Its additive-error inequality is not a quantum trace-distance or asymptotic theorem.

## Coverage of the paper

| Paper result | Formal coverage |
| --- | --- |
| Theorem 2.2 | None: entropy, continuity and the complete adaptive converse are unformalized. |
| Theorem 3.1 | None: privacy lifting, approximation, minimax and limit order are unformalized. |
| Theorem 4.1 and Lemma 4.2 | None: amplified Gram repair, norm estimates and flagged exactification are unformalized. |
| Theorem 5.1, Appendix A.1-A.3 | None: adaptive concentration, exterior compression and robust decoupling are unformalized. |
| Appendix A.4-A.5 | Partial: exact bath-only marginal invariance and the six arithmetic statements; preparation, joint seed decorrelation, continuity and induction are unformalized. |
| Appendix A.6 | Arithmetic only: no spectrum, entropy or limiting theorem. |
| Theorem 2.1 and Section 6 | None: the full rate region and all-horizon diagonal selection are unformalized. |
| Channel examples | None in Lean; finite Python diagnostics are not optimization or asymptotic proofs. |

## Reproduction and dependency checks

The recorded run used Lean 4.30.0, commit
`d024af099ca4bf2c86f649261ebf59565dc8c622`, and mathlib commit
`c5ea00351c28e24afc9f0f84379aa41082b1188f`.
`lean-toolchain` and `dependencies.lock.json` record the complete pinned package
environment. Dependencies are not distributed. The read-only package cache
supplied to the wrapper must come from a compatible project, with that project's
`lake-manifest.json` two directories above `.lake/packages`.

From ancillary/, with an existing compatible cache and a writable log directory:

```
python run_checked.py --packages PATH_TO_LAKE_PACKAGES --log PATH_TO_WRITABLE_LOG/NEW-CHECK.txt ActiveBath.lean BlockAccounting.lean
```

Use operating-system memory and time limits. The recorded kernel run succeeded
with one Lean thread, a 768 MiB process-job memory cap and a 170-second wall limit.
Choose log output outside checksummed source files; the optional build/ directory
is excluded by the package verifier.

`LEAN-CHECK.txt` preserves the successful kernel output. Its warning locations
record the source layout used for that run; they do not require that layout here.
Eight quantum and six arithmetic dependency queries report only `propext`,
`Classical.choice` and `Quot.sound`, standard Lean foundations rather than added
scientific assumptions. No `sorry`, `admit` or scientific axiom is present.

`run_checked.py` checks versions and package pins and validates every printed
dependency closure using `axiom_guard.py`. It rejects missing or duplicate reports
and unexpected axioms. `python -B test_axiom_guard.py` checks the recorded source
sets and negative controls without rerunning Lean.

The `noncomputable` section permits abstract real/complex operations and classical
finite indexing; it neither weakens the statement nor supplies an analytic axiom.
Full formalization would additionally require entropy, spectral calculus,
Schatten/diamond norms, continuity, channel dilation, concentration/decoupling and
asymptotic quantifier management. No full-paper formal verification is claimed.
