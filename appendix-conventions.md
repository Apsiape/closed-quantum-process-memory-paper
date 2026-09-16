# Appendix B. Conventions, resources and references

Companion to the [manuscript](manuscript.md) and [Appendix A](appendix-causal-balancing.md).
This appendix records conventions, registers, reproducible finite checks and
the bibliography. It adds no claims.

## B.1. Normalization and finite objects

| Symbol | Convention |
|---|---|
| S,A,Q | Input, immediate output and purification reference; dimension q each. |
| rho_Q | rho^T for the canonical purification (I x sqrt(q rho))Omega_q; spectra and minimum eigenvalues agree with rho. |
| J_Phi | Trace-one Choi state, Tr_A J_Phi=I_Q/q; k=rank J_Phi<=q^2. |
| D, Ddiamond | Half trace norm and half diamond norm; range [0,1] for states/channels. |
| S,H_2 | Base-two von Neumann and binary entropy; 0 log 0=0. |
| pi_d | I_d/d, with d actual integer Hilbert dimension. |
| k_(rho,e) | All normalized finite-QAZ extensions with exact QZ product, QA error <=e; auxiliary dimension unrestricted. |
| kappa | Full-rank input supremum after the positive-error limit at fixed rho; Corollary 4.3 derives the exact privacy-funnel form using Theorems 3.1 and 4.1, without attained witnesses. |
| K0(rho), P_q | Exact fixed-input extension infimum and quantum privacy-funnel supremum with X=E,Y=Q,R=A,W=Z; unrestricted finite auxiliary dimension. The prior subscript q means quantum. |
| Gamma_C | Active bath output only; no inert purifier included. |
| r,s | Actual limits log R_T/T and S(omega_T)/T for vanishing-error all-horizon families. |
| Entropy deficit | log R_T-S(omega_T); neither entropy nor log rank. |
| Appendix A constants | May depend on a single fixed finite exact collision; uniform in tester, finite reference dimension and horizon. |
| Reused letters | F is the inert purifier of the actual initializer (Definition 1.1) and, as F^n in Appendix A, the purifier of the comparison stock; the Slepian--Wolf receiver is written N. C names both a finite collision (U,tau) and the Slepian--Wolf sender register. k is the Choi rank; k_(rho,e) is the smoothed extension cost. nu in Proposition 7.5 is a damping parameter; gamma in Appendix A is the concentration slack. |

The q=1 case is scalar and is directly realized without a bath. In
Theorem 4.1 one uses the smallest POSITIVE target Choi eigenvalue, never a
kernel inverse. Square input/output dimensions are needed for the
support-isometry unitary completion in Theorems 3.1 and 4.1. All finite internal direct sums and zero padding
are included in the active dimension.

## B.2. Physical and proof registers of Appendix A

| Register | Size / initialization | Action and charge |
|---|---|---|
| Full B_T | R_T=(T+1)J_N 2^A_T | Every active device register below is included. |
| Clock | T+1; pure | Cyclic shift controls the fixed per-visit unitaries; log(T+1) charged. |
| Z | J_N; pi_(J_N) | One retained seed reused for every block; log J_N charged in dimension and entropy. |
| M | mo qubits; maximally mixed | Permanent recycled capital, returned jointly in the reduced comparison. |
| W | w qubits; pure | Permanent workspace; returned pure jointly up to the block error. |
| Tranche j | z=c+d qubits; c mixed and d pure | Distinct for every full block. Preparation residue rp and encoding residue N-mo fill it permanently. |
| Working cells | e=n ceil(log R) positions during a block | Obtained by routing within the exact local wires, not a separate free bank. |
| Compressor padding | max(0,N-e) pure positions | Included in identity (A.1); handles N>e. |
| Tail | (T-Ln)ceil(log k) pure qubits | Preallocated exact pure-Stinespring cells; retained after use. |
| Actual F | Minimal dimension J_N 2^K_T | Purifies the complete initializer and is forever inert; not an active resource. |
| Proof F^n | Purifies comparison tau^tensor n | Not the actual repeated stock initializer and never an operated register. |
| H=E_raw E' | Purification of the complete comparison exterior | Includes all future-accessed spectators before its rank bound; E' is mathematical only. |
| Virtual E^n | Fresh minimal environments in a comparison | Produces support projector P_H; virtual P_E is never a physical compression operation. |

Only the reduced boundary distance omits parked tranches and inaccessible
purifiers. Their omission from a metric does not delete any actual bath
dimensions. Exact initialization is P_T equal eigenvalues 1/P_T, where
P_T=J_N 2^K_T<=R_T; its remaining R_T-P_T eigenvalues are zero.

## B.3. Scope of the statements

The physical contract for every statement in this paper is Definitions
1.1--1.4. Nothing below uses a theorem about finite-tracial closure, about
the strength of a physical record, about feedback-assisted protocols, about
computability, or about processes with more than one visit per input.
Propositions 7.1--7.5 and 8.1 are proved here under those same definitions.
No external classification of generalized amplitude damping, arbitrary mixed
replacers or unequal pure-output sectors is used.

Four shortcuts are deliberately avoided and are used nowhere above: raw
mixed-history rank in place of purified-exterior support, merely marginal seed
freshness, uniform initial-entropy continuity under a small flag, and attained
witnesses.

## B.4. Reproducible diagnostics and their limits

The scripts named below accompany this paper in ancillary/; run the Python
commands from that directory. In the repository they are in verification/python/.
For Lean, use the wrapper command in ancillary/COVERAGE.md with an already
installed compatible package cache; the table names its target files, not
standalone commands with configured imports. They print their results; all are bounded
finite controls. They do not prove unbounded auxiliary optimizations,
arbitrary adaptive asymptotics, or any theorem of this paper. Seeds and
dimensions are explicit in the scripts.

| Command in the ancillary bundle | Finite coverage |
|---|---|
| python c2_lifting_mixing.py | 24 lifts, 20 flagged probes; q=2,3, R=2,3,4; seed 20260908; tolerance 1e-8. |
| python c3_exactification.py | 8 cases, 40 probes; q=2,3, original R=5,7; largest unitary 93; seed 20260909; tolerance 1e-8. |
| python c4_adaptive_spectral.py | 8 nonproduct distributions, 112 conditional nodes; q=R=2, n=3; vector dimension <=1024; seed 20260909; tolerance 1e-8. |
| python c5_region_spectrum.py | 12 spectrum/feedback cases, 576 rational cases; seed 20260909; tolerance 1e-9; density dimension <=768. |
| python support_repair.py | 12 small-matrix cases; seed 20260908; tolerance 1e-8. |
| python block_invariant.py | 300 integer allocations, 1024-label preparation, joint-freshness and rare-stop negative controls, 12 states over 24 Cliffords. |
| python encoder_only_merging.py | 36 partial-trace decoder-omission identity checks and 125 rational balances; seed 20260908; no decoupling or compiler validation. |
| python rz_contract_negative_control.py | Exact rational q=R=2, T=1,...,12 marginal/joint separation; no random seed or numerical tolerance. |
| python gad_interior_example.py | Proposition 7.5: trace preservation, exchange-block unitarity, 2007 inputs reproducing the channel, both analytic endpoints, the exact rational lower witness, the attained upper witness, the mixed-input entropy-exchange value and diagonal grid searches for both; seed 20260910; tolerance 1e-8. |
| BlockAccounting.lean (via documented wrapper) | Six elementary natural-number accounting lemmas only. |
| ActiveBath.lean (via documented wrapper and pinned mathlib) | Finite complex density matrices and exact bath-only closing invariance for the complete user marginal. |

The Lean files report their axioms and use only standard foundations
(propext, Quot.sound and Classical.choice), with no sorry or added scientific
axiom. ActiveBath defines positive-semidefinite trace-one complex matrices,
proves that partial trace and unitary closing preserve legal states, and proves
exact invariance of the complete user marginal under a bath-only unitary,
including arbitrary user-bath correlations and finite references. This supports
only the closing identity in Appendix A.4, not construction of the compiler.
Coverage is partial: entropy, trace distance and the asymptotic theorem are not
formalized. No numerical telescope suite for Theorem 2.2 is claimed. The ancillary
coverage matrix and pinned dependency record give exact reproduction details.

## B.5. Primary bibliography and exact uses

1. K. M. R. Audenaert, *A Sharp Fannes-type Inequality for the von Neumann Entropy*,
   [arXiv:quant-ph/0610146v1](https://arxiv.org/pdf/quant-ph/0610146v1), Theorem 1.
   Entropy continuity for Theorem 2.2 and pure replacement, in the
   half-distance convention.
2. T. Eggeling, D. Schlingemann and R. F. Werner, *Semicausal operations are
   semilocalizable*, [arXiv:quant-ph/0104027v1](https://arxiv.org/pdf/quant-ph/0104027v1),
   section III, unnumbered theorem and Eqs. (10)--(21). Stinespring uniqueness
   and the structural pointwise lifting antecedent; not the uniform
   optimization of Theorem 3.1.
3. D. Kretschmann, D. Schlingemann and R. F. Werner, *A Continuity Theorem for
   Stinespring's Dilation*, [arXiv:0710.2495v1](https://arxiv.org/pdf/0710.2495v1),
   Definition 1 and Theorem 1. Comparison of contracts, not an active/inert
   spectrum-preserving repair theorem used as a black box in Theorem 4.1.
4. A. Winter, *Tight uniform continuity bounds for quantum entropies:
   conditional entropy, relative entropy distance and energy constraints*,
   [arXiv:1507.07775v6](https://arxiv.org/html/1507.07775v6), section II, Lemma 2.
   The bound used in Theorem 4.1 depends on dim QA=q^2, not dim F.
5. F. Dupuis, M. Berta, J. Wullschleger and R. Renner, *One-shot decoupling*,
   [arXiv:1012.6044v3](https://arxiv.org/html/1012.6044v3), Theorem 3.3 and
   Lemmas 3.4--3.5; Theorem 3.1 and discussion after Corollary 3.2 for retaining
   the random unitary choice. The second moment is rederived in Lemma A.3.
6. C. Dankert, R. Cleve, J. Emerson and E. Livine, *Exact and approximate
   unitary 2-designs: Constructions and applications*,
   [arXiv:quant-ph/0606161v2](https://arxiv.org/pdf/quant-ph/0606161v2),
   Theorem 1 and Clifford twirl proof, pp. 2--3. Finite exact second moments.
7. A. Abeyesinghe, I. Devetak, P. Hayden and A. Winter, *The mother of all
   protocols: Restructuring quantum information's family tree*,
   [arXiv:quant-ph/0606225v1](https://arxiv.org/pdf/quant-ph/0606225v1),
   Theorems IV.1--IV.2, Lemma IV.5 and Eq. (30), pp. 6--9; section VII,
   Eq. (35) and following rate choice; Appendix A for typical spectra.
   Encoder-only FQSW split and half-sum rates; omitting the receiver decoder
   preserves MH.
8. P. Boes, H. Wilming, R. Gallego and J. Eisert, *Catalytic quantum randomness*,
   [arXiv:1804.03027v3](https://arxiv.org/pdf/1804.03027v3), Lemma 1 and section
   III A. Orthogonal-unitary dephasing and marginal repeated-use comparison.
   See also [Erratum, Phys. Rev. X 10, 029901 (2020)](https://journals.aps.org/prx/pdf/10.1103/PhysRevX.10.029901),
   correcting section V/Theorem 3's expander result, which this paper does
   not use; the dephasing lemma is unaffected.
9. T. Rybar and M. Ziman, *Repeatable quantum memory channels*,
   [arXiv:0808.3851v1](https://arxiv.org/pdf/0808.3851v1), after Eq. (2.3),
   section III definition, Theorems 1--2, Eq. (3.7), finite n-repeatability
   and the cell-permutation construction; section IV conclusion.
   Phys. Rev. A 78, 052114 (2008). Entropy-budget and preallocated-cell
   antecedents, in addition to the fixed-memory marginal-repeatability comparison.
10. M. Musat and M. Rordam, *Non-closure of quantum correlation matrices and
    factorizable channels that require infinite dimensional ancilla*,
    [arXiv:1806.10242v4](https://arxiv.org/html/1806.10242v4), Theorem 4.1.
    Finite factorization closure is distinct from finite exact attainment.
11. S. H. Lie, J. Son, P. Boes, N. H. Y. Ng and H. Wilming, *Thermal Operations
    from Informational Equilibrium*, [Phys. Rev. Lett. 137, 030403 (2026)](https://journals.aps.org/prl/pdf/10.1103/lm3h-c5f5),
    [arXiv:2507.16637](https://arxiv.org/abs/2507.16637),
    published July 13, 2026, Proposition 6 and Eq. (12). Prior equilibrium/
    tracial-factorization interpretation; no quantitative companion modulus
    is adopted. The former arXiv v1 Proposition 4/Eqs. (13)--(15) numbering
    is not the published numbering.
12. C. H. Bennett, I. Devetak, A. W. Harrow, P. W. Shor and A. Winter,
    *The Quantum Reverse Shannon Theorem and Resource Tradeoffs for Simulating
    Quantum Channels*, [arXiv:0912.5537v5](https://arxiv.org/html/0912.5537v5),
    Theorem 3. Comparison of communication/entanglement and closed storage.
13. A. Bisio, G. M. D'Ariano, P. Perinotti and M. Sedlak, *Memory cost of
    quantum protocols*, [arXiv:1112.3853v1](https://arxiv.org/pdf/1112.3853v1),
    Definitions 3--4 and Theorem 3. Quantum interstep memory with free classical
    storage and local CPTP operations differs from all retained closed storage.
14. B. Schumacher, *Sending entanglement through noisy quantum channels*,
    [Phys. Rev. A 54, 2614--2628 (1996)](https://doi.org/10.1103/PhysRevA.54.2614),
    section V A, summary (iii), p. 2622. Established entropy exchange,
    maximized in Definition 1.3.
15. N. Datta, C. Hirche and A. Winter, *Convexity and Operational Interpretation
    of the Quantum Information Bottleneck Function*,
    [arXiv:1810.03644v3](https://arxiv.org/html/1810.03644v3#S5), section V,
    Eq. (22), with section III Eqs. (5)--(7) for the purification convention.
    Exact fixed-input privacy-funnel correspondence; smoothing stability is
    derived in manuscript section 4, not taken from this source.
16. M. Sion, *On general minimax theorems*,
    [Pacific J. Math. 8, 171--176 (1958)](https://msp.org/pjm/1958/8-1/pjm-v8-n1-p14-p.pdf),
    Theorem 4.2 (Kneser--Fan), p. 175. One compact side suffices after
    physical convexification of gain functions.
17. W. Hoeffding, *Probability Inequalities for Sums of Bounded Random Variables*,
    [J. Amer. Statist. Assoc. 58, 13--30 (1963)](https://doi.org/10.1080/01621459.1963.10500830).
    Bounded-variable exponential-moment ingredient; its conditional iteration
    and elementary moment bound are derived in Lemma A.1. No source theorem
    number is assigned to that adaptive application.
18. B. M. Terhal, I. L. Chuang, D. P. DiVincenzo, M. Grassl and J. A. Smolin,
    *Simulating quantum operations with mixed environments*,
    [arXiv:quant-ph/9806095v2](https://arxiv.org/pdf/quant-ph/9806095v2),
    Eqs. (6)--(8). Mixed bath implementation and its unitary column constraints.
19. G. Gour and M. M. Wilde, *Entropy of a quantum channel*,
    [arXiv:1808.06980v3](https://arxiv.org/html/1808.06980v3), Proposition 6,
    section III, Theorem 10 and Proposition 24. Universal parallel merging
    with accessible environment share and net entanglement accounting;
    its channel entropy is distinct from kappa.
20. P. Faist, M. Berta and F. G. S. L. Brandao, *Thermodynamic Implementations
    of Quantum Processes*, [arXiv:1911.05563v3](https://arxiv.org/html/1911.05563v3),
    Theorem 5.1 and Eq. (5.4). Universal parallel work-rate comparison at
    trivial Hamiltonians; free implementation does not charge all retained bath.
21. S. H. Lie and H. Jeong, *Randomness for quantum channels: Genericity of
    catalysis and quantum advantage of uniformness*,
    [arXiv:2010.14795v2](https://arxiv.org/pdf/2010.14795v2), Theorems 1, 5--6.
    Input-independent bath-output restriction and purifier-assisted recovery
    distinguish its randomness model from the present contract.

22. U. Haagerup and M. Musat, *Factorization and dilation problems for
    completely positive maps on von Neumann algebras*,
    [arXiv:1009.0778v1](https://arxiv.org/pdf/1009.0778v1), Definition 1.3
    and Theorem 2.2; Comm. Math. Phys. 303, 555--594 (2011).
    Tracial factorization background; finite algebra does not mean finite dimension.
23. T. Metger, O. Fawzi, D. Sutter and R. Renner, *Generalised entropy
    accumulation*, [arXiv:2203.04989v2](https://arxiv.org/html/2203.04989v2),
    Theorem 4.1 and Appendix A Eqs. (A.1)--(A.2).
    Smooth-entropy comparison in A.1; not a replacement for its fixed projector.
24. P. Faist and R. Renner, *Fundamental Work Cost of Quantum Processes*,
    [arXiv:1709.00506v2](https://arxiv.org/pdf/1709.00506v2), Main Result
    and Eq. (2); Phys. Rev. X 8, 021011 (2018).
    Specified-input, reference-preserving process work and information battery.
25. I. Devetak and J. Yard, *The exact cost of redistributing multipartite
    quantum states*, [arXiv:quant-ph/0612050v2](https://arxiv.org/pdf/quant-ph/0612050v2),
    main region and Eqs. (1)--(2), p. 2; Phys. Rev. Lett. 100, 230501 (2008).
    Known-source communication/net-entanglement comparison. The v2 posting
    is from 2020; the first preprint is from 2006.
26. V. Scarani, M. Ziman, P. Stelmachovic, N. Gisin and V. Buzek,
    *Thermalizing Quantum Machines: Dissipation and Entanglement*,
    [arXiv:quant-ph/0110088v1](https://arxiv.org/pdf/quant-ph/0110088v1),
    Eqs. (1)--(2), pp. 1--2; Phys. Rev. Lett. 88, 097905 (2002).
    Fresh-cell repeated-interaction antecedent, not closed adaptive storage rates.

27. Z. Baghali Khanian and D. Leung, *Quantum Reverse Shannon Theorem Revisited*,
    [arXiv:2504.07068v1](https://arxiv.org/html/2504.07068v1), section II,
    Definition 3 and Theorems 6 and 8. Specified mixed-source/reference
    simulation with encoder-side information; communication and entanglement
    are the charged resources.

28. R. R. Smith, *Completely Bounded Maps between C*-Algebras*,
    [J. London Math. Soc. (2) 27, 157--166 (1983)](https://doi.org/10.1112/jlms/s2-27.1.157).
    Standard finite-codomain amplification bound; not the active support-repair package.
29. S. H. Lie and H. Jeong, *Correlational Resource Theory of Catalytic Quantum
    Randomness under Conservation Law*, [arXiv:2104.00300v1](https://arxiv.org/html/2104.00300v1),
    Proposition 2, Corollary 10 and Theorem 11. Catalyst-return comparison;
    no identification of all zero-gain collisions.
30. A. Makhdoumi, S. Salamatian, N. Fawaz and M. Medard,
    *From the Information Bottleneck to the Privacy Funnel*,
    [arXiv:1402.1774](https://arxiv.org/abs/1402.1774). Classical origin;
    the quantum definition used here is Datta--Hirche--Winter Eq. (22).
31. S. Loomis and J. P. Crutchfield, *Strong and Weak Optimizations in Classical
    and Quantum Models of Stochastic Processes*, [arXiv:1808.08639](https://arxiv.org/abs/1808.08639),
    section V and weak-minimality counterexample. Distinct stationary-memory costs.
32. Q. Liu, T. J. Elliott, F. C. Binder, C. Di Franco and M. Gu,
    *Optimal stochastic modelling with unitary quantum dynamics*,
    [arXiv:1810.09668](https://arxiv.org/abs/1810.09668);
    Phys. Rev. A 99, 062110 (2019). Competing dimension
    and entropy costs for quantum models of classical stochastic processes.
33. D. D. C. Chang, G. D. Berk and M. Gu,
    *How much randomness in a quantum process can be explained using memory?*,
    [arXiv:2608.25878v1](https://arxiv.org/html/2608.25878v1), section IV,
    Theorem 3 and Appendix B.5. Stationary recurrent CPTP memory comparison.
34. M. Kotowski and M. Kotowski, *Randomized simulation of quantum channels using
    small ancilla*, [arXiv:2606.08784](https://arxiv.org/abs/2606.08784).
    Heralded single-use simulation with a small fresh ancilla; contract
    comparison only, in section 8.
35. S. Douglas, *Closed Mixed-Apparatus Compression of Schur Channels:
    Exact-Approximate Separation and Scheduled Delivery*,
    [doi:10.5281/zenodo.22785669](https://doi.org/10.5281/zenodo.22785669) (2026).
    Companion note on scheduled rather than immediate delivery; cited in
    section 9 for scope only.

The bibliography is a bounded ingredient and contract comparison, not an
exhaustive literature survey. Imported primary theorems are cited at their
specific uses. The original arguments are in the manuscript and Appendix A.
