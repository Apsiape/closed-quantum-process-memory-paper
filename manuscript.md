# Bath dimension and initial entropy for closed repeated use of a quantum channel

Seth Douglas

seth.douglas@gmail.com

## Abstract

We study finite closed devices that serve repeated uses of a fixed quantum
channel while returning each output immediately and tolerating arbitrary adaptive
inputs. One bath, one initial state and one unitary are fixed before the user;
no reset, discard, fresh ancilla or uncounted controller is available. This
differs from the fixed-memory exact single-use marginal repeatability of Rybar
and Ziman: we allow horizon-dependent hardware and require vanishing complete
error against adaptive users. Active dimension and actual initial
entropy form distinct resources. Writing r for the limiting bath dimension per
use, log R_T/T, and s for the limiting initial entropy per use, S(omega_T)/T,
we characterize the rate region as s>=0, r+s>=h and r-s>=kappa, where h is
maximum entropy exchange and kappa is a smoothed independent-reference
extension cost, an ordered limit that is not asserted to be computable, whose
exact form at each fixed full-rank input is an affine transform of the
zero-leakage quantum privacy funnel; the minimum dimension rate is
(h+kappa)/2. The
proof combines entropy budgets, a uniform collision-gain formulation, active
support repair, and a closed adaptive implementation of encoder-only fully
quantum Slepian--Wolf recycling. The implementation counts the entire bath,
including its seed, clock, workspace and permanently parked residues, and
achieves actual initial entropy rates. The entropy-exchange functional, the
privacy funnel, the minimax step and the Slepian--Wolf split are established
ingredients; what is added here is the closed contract, a support repair that
preserves the positive initial spectrum with a bath-independent gain penalty,
and the counted adaptive implementation.

## 1. Introduction and model

A quantum channel is normally charged once. Fix a CPTP map Phi and a single
use costs a dilation: an environment of dimension at most q^2 if it starts
pure, or some other finite bath if it may start mixed. Serving T inputs in
sequence is a different question, and the difference is not merely a factor
of T: the closed cost is still linear in T, but its coefficient, and the trade
between dimension and initial entropy, are what a single-use dilation does not
determine. A
device that has already produced outputs must have somewhere to keep what
producing them left behind. If it may reset its bath between visits, discard a
spent cell, or draw a fresh ancilla, the question collapses to the single-use
one: use one dilation T times and let the rest arrive from outside. Those three
permissions are exactly what a closed implementation lacks. Reset consumes a
supply of pure states, discard needs a place to put what is discarded, and a
fresh ancilla is a resource that somebody prepared. Charging all of them means
fixing one finite Hilbert space and one finite initial state in advance and
asking what fits inside.

Definition 1.1 is that contract. For each horizon T the device is one active
bath B_T of dimension R_T, one user-independent initial state omega_T on it,
and one unitary W_T applied at every visit; all three are chosen before the
user and may depend on Phi and T. The output is handed back before the next
input arrives. The tester is adaptive, may retain every output, and may hold
arbitrary finite references, so the error of Definition 1.2 compares complete
final states, not single-use marginals. Nothing inside is free: the seed, the
clock, the workspace, the records and every register parked permanently after
use are all part of R_T. The one object outside is a purifier of omega_T,
which the device may never touch and which is therefore never a resource.

Two numbers describe such a device, and they are not interchangeable. The
first is log R_T, the dimension it occupies. The second is S(omega_T), the
actual entropy of the state it was initialized in. A rank count lies between
them: S(omega)<=log rank(omega)<=log R, with equality throughout only for a
flat positive spectrum, so neither dimension nor rank determines the other
number. The four-dimensional example after Definition 1.4 separates all three.
Initial entropy is the right second axis because the contract makes it a
resource that can be spent: a device may be handed a mixed initializer, and
what it is charged is the entropy of that initializer, not the provenance of
the randomness, which lies outside this contract and is not identified here
with work or energy. The region below then charges that convenience back.
Past the corner, every further bit of initial entropy costs a bit of dimension,
since r>=kappa+s there.

Theorem 2.1 characterizes what is achievable. Writing r for the dimension rate
and s for the actual initial entropy rate, the closed region is s>=0,
r+s>=h(Phi) and r-s>=kappa(Phi), and the least dimension rate is (h+kappa)/2,
attained with initial entropy rate (h-kappa)/2 and a spectrum flat on its
support. Both channel quantities are intrinsic. The first, h, is Schumacher's
entropy exchange maximized over inputs. The second, kappa, is an infimum of
S(QA|Z) over finite extensions whose reference stays exactly in product with
the auxiliary, smoothed in the output error, with the positive-error limit
taken before the full-rank input supremum; Corollary 4.3 identifies the
positive-error limit at each fixed full-rank input with
S(chi_rho)-P_q^(psi_EQ)(0), an affine transform of the zero-leakage quantum
privacy funnel. Kappa is the supremum of these limits. Two
resources, two channel quantities, one closed region.

The closest antecedent contract is Rybar and Ziman's repeatable quantum memory
channel: one fixed finite memory, initializer and unitary, required to produce
the same single-use marginal at every repetition, for uncorrelated inputs.
Rybar and Ziman also discuss finite n-repeatability and a finite-cell
construction. Here we optimize dimension and actual initialization entropy
as the horizon grows, while requiring vanishing complete error against
arbitrary adaptive quantum users.
The gap between the contracts is not cosmetic. One fair shared bath bit
controlling I or Z is a legitimate marginal dephasing repeater in their sense,
and Proposition 8.1 shows its complete service error is at least 1-2^(1-T),
already 1/2 at T=2. No resolution of their original question is claimed here.

The contributions, in decreasing operational significance, are these. First,
the characterization itself under the closed contract, together with its
converse Theorem 2.2, which assumes no entropy-rate limit, constrains the same
actual initialization through two separate legal experiments, and holds at
every finite horizon with constants explicit in that horizon's own error.
Second, the active support repair of Theorem 4.1: an approximate finite
collision is corrected so that its Choi support lies inside the target's, with
the positive initial spectrum unchanged and a gain penalty depending only on
the fixed channel, not on the bath dimension, the initial spectrum or any
auxiliary dimension; the subsequent flagged exactification changes the spectrum
explicitly and says so, and with Theorem 3.1 it gives kappa_exact=kappa.
Third, the implementation of Theorem 5.1 and Appendix A, which turns the
encoder-only fully quantum Slepian--Wolf split into a device obeying
Definition 1.1: spectral concentration uniform over adaptive controllers, one
physical seed reused across every block and returned jointly independent of the
whole future-accessed exterior, reversible flat-stock preparation on exact
integer wires, and every residue allocated and counted in one closed bath.
The entropy-exchange functional, the privacy funnel, the classical minimax
step, the Slepian--Wolf split with its half-sum rates and the decoupling second
moment are established ingredients, cited at their uses; the contract they are
assembled under, and the repair and allocation needed to meet it, are the
implementation tasks addressed here.

The characterization has real limits, stated where they arise. The quantity
kappa is an ordered limit of an infimum with no attainment, no bound on the
auxiliary dimension, and no assertion of computability or of continuity in Phi;
the thresholds in section 6 are finite but not effective. Proposition 7.4
supplies a lower bound on kappa that is an optimization over the input space
alone, and Proposition 7.5 brackets a single-qubit channel with 0<kappa<h, so
the non-degenerate case 0<kappa<h occurs and the two degenerate edges are not
the only cases. Nothing here bounds circuit size or latency, requires the bath
to be returned, or extends beyond one fixed memoryless channel visited once
per input.

Section 2 states the region and proves the converse. Section 3 identifies
kappa with an optimum over physical approximate collisions, section 4 repairs
such a collision into an exact one and derives the privacy-funnel form, and
section 5 with Appendix A builds an all-horizon device from one exact witness.
Section 6 assembles the region from these, section 7 gives worked channels and
the limits above, and section 8 compares the contract with neighbouring ones.

Definition 1.1 (closed causal device). Fix a CPTP map Phi from operators on
S=C^q to operators on A=C^q. For every integer horizon T>=1, a device consists
of a finite active bath B_T of dimension R_T, a density operator omega_T on it,
and a unitary W_T:S B_T -> A B_T, with S and A identified between visits.
All three may depend on Phi and T and are chosen before the user. Initially
omega_T is in product with the user's entire state. A mathematical purifier F
is inaccessible forever; it is an analysis device only, the device never acts
on it, so it is not charged, and the cost of a mixed omega_T enters through
S(omega_T). Each visit applies this same W_T and hands A back
before the next input arrives. All device seeds, clocks, stock, work wires,
records and permanently parked residues are part of B_T. Offline preparation
and unrestricted fixed hardware are allowed. No device reset, discard, fresh
online ancilla, external randomness, purifier operation or uncounted controller
is allowed. There is no bath-return requirement, marginal or independent.

Here active bath means the entire allocated device Hilbert space B_T,
including registers parked permanently after use; active dimension is R_T.
The inaccessible purifier is excluded. A close antecedent is the unitary
memory model of [Rybar and Ziman, sections II--III, v1](https://arxiv.org/pdf/0808.3851v1).
Their infinite-repeatability definition fixes one finite device for exact
single-use marginals with uncorrelated inputs; they also discuss finite
n-repeatability and preallocated cells. Here we optimize horizon-dependent
resources while approximating the complete process against adaptive inputs. Section 8 gives
an explicit separation; no resolution of their original question is claimed.

Definition 1.2 (complete error and rates). A tester has arbitrary finite user
memory and references, may retain all outputs, and applies arbitrary adaptive
quantum operations between visits. Let rho_T^real(U) and rho_T^ideal(U) be its
complete final states when connected to the device or T independent Phi calls.
With D(rho,sigma)=||rho-sigma||_1/2, set

`delta_T=sup_U D(rho_T^real(U),rho_T^ideal(U))`,
`c_seq(Phi)=inf_(families with delta_T->0) limsup_(T->infinity) log R_T/T`.

The supremum includes all finite reference sizes. All-horizon means a device
for every positive integer T, with error tending to zero along all integers.
An achievable finite rate pair has actual limits log R_T/T->r and
S(omega_T)/T->s; the rate region is the closure of these pairs. Along such a
family R_T grows exponentially in T; r is the exponent per use, not a memory
size. Logs and
entropies are base two, S(rho)=-Tr rho log rho, with 0 log 0=0.
An unconditional stopped experiment is covered by padding its continuation
with dummy inputs. No bound conditional on a rare stopping outcome is promised.
Batch access to all inputs would remove the immediate-output requirement and
is a different task.

Definition 1.3 (intrinsic costs). For a minimal pure Stinespring dilation
V:S -> A E of Phi, write Phi^c(rho)=Tr_A V rho V* and
`h(Phi)=max_rho S(Phi^c(rho))`. This maximizes the established entropy exchange
of [Schumacher, section V A, summary (iii), p. 2622](https://doi.org/10.1103/PhysRevA.54.2614).
Complementary dilations differ by environment isometries, so this number is
independent of the minimal choice. Let
`|Omega_q>=q^(-1/2) sum_i |i,i>` and
`J_Phi=(id x Phi)(|Omega_q><Omega_q|)`; thus Tr J_Phi=1 and
Tr_A J_Phi=I_Q/q. For rho>0 choose
`|psi_rho>=(I x sqrt(q rho))|Omega_q>`, whose Q marginal is rho^T in this
basis, and put chi_rho=(id x Phi)(|psi_rho><psi_rho|). For e>0 define

`k_(rho,e)=inf S(QA|Z)_sigma`,
`sigma_QZ=rho^T x sigma_Z exactly`, `D(sigma_QA,chi_rho)<=e`,
`kappa(Phi)=sup_(rho>0) lim_(e down 0) k_(rho,e)`.

The infimum runs over normalized states on QAZ and every finite Z; there is
no uniform dimension bound or attainment assertion. Here S(X|Y)=S(XY)-S(Y).
The value k_(rho,e) is nonincreasing in e and lies between
S(rho)-log q and S(chi_rho), so its positive-error limit exists and is finite.
The positive-error limit is taken with rho fixed, before the full-rank
supremum. Equality with the exact-extension value at e=0 requires the
stability argument after Theorem 4.1; it is not an assumption of this definition.

The exact fixed-input optimization is already related to a named entropy
functional. Write K0(rho) for the same infimum with sigma_QA=chi_rho exactly.
For psi_QAE=(id x V)psi_rho, all finite QA extensions are obtained by a channel
E->Z, and the product constraint is I(Q;Z)=0. Thus

`K0(rho)=S(chi_rho)-P_q^(psi_EQ)(0)`,

where P_q is the quantum privacy funnel of [Datta, Hirche and Winter,
section V, Eq. (22), v3](https://arxiv.org/html/1810.03644v3#S5), with their
X=E, Y=Q, R=A and W=Z. Its objective I(YR;W) becomes I(QA;Z), and
S(QA|Z)=S(chi_rho)-I(QA;Z). Their subscript q denotes quantum, not the
dimension here. Supremum and infimum range over all finite auxiliary
dimensions; neither attainment nor a dimension bound is asserted.
Section 4 supplies the additional positive-error stability for this paper's
fixed channel. The known functional and the FQSW split credited in section 5
are ingredients in the closed adaptive rate characterization proved below.

Definition 1.4 (finite collision). A finite unitary U on S B and a state tau_B
give Phi_C(rho)=Tr_B U(rho x tau)U* and the ACTIVE bath channel
Gamma_C(rho)=Tr_A U(rho x tau)U*. Define
`f_C(rho)=S(Gamma_C(rho))-S(tau)`, `g_C=max_rho f_C(rho)` and
`kappa_exact=inf_(Phi_C=Phi) g_C`. Gamma_C excludes the inert purifier.
Channel distance is Ddiamond(Psi,Phi)=||Psi-Phi||_diamond/2, equivalently the
supremum half trace distance on reference-entangled inputs. The exact finite
collision and its spectrum are fixed before invoking a block limit.
Mixed-environment realizations and their unitary column constraints were
studied by [Terhal et al., Eqs. (6)--(8), v2](https://arxiv.org/pdf/quant-ph/9806095v2).
Repeated system--bath interactions also appear in
[Scarani et al., Eqs. (1)--(2), v1](https://arxiv.org/pdf/quant-ph/0110088v1):
their thermalization model supplies identically prepared bath qubits that
each interact once with the same system. Our finite collision is one such
unitary building block; its repeated-service implementation must allocate
and count every cell within Definition 1.1's horizon-dependent closed bath.

For example, a four-dimensional bath initialized with eigenvalues
(3/4,1/4,0,0) has log dimension 2, log rank 1, actual entropy H_2(1/4)
approximately 0.8113, and entropy deficit 2-H_2(1/4) approximately 1.1887.
Its minimal purifier dimension is 2, but those inert degrees of freedom are
not available workspace. In general only S(omega)<=log rank(omega)<=log R
holds; equality of entropy and log rank requires a flat positive spectrum.

Conventions, register tables and the bibliography are collected in
[Appendix B](appendix-conventions.md). The proofs below use no theorem
about finite-tracial closure and none about processes with more than one
visit per input.

## 2. Main theorem and converse

Theorem 2.1 (rate region). By Theorems 2.2, 3.1, 4.1 and 5.1, proved below,
the rate region of Definition 1.2 is exactly
`s>=0, r+s>=h, r-s>=kappa`. The minimum
dimension rate is `(h+kappa)/2`, attained with actual entropy `(h-kappa)/2` and
a spectrum that is flat on its support. For q=1 all intrinsic costs and the minimum rate vanish.

Theorem 2.2 (same-spectrum converse). Every vanishing-error all-horizon
family satisfies liminf (log R_T-S(omega_T))/T>=kappa and
liminf (log R_T+S(omega_T))/T>=h. No entropy-rate limit is assumed.

Proof. The entropy-decrease budget has the antecedent of
[Rybar and Ziman, section III, Eq. (3.7)](https://arxiv.org/pdf/0808.3851v1).
The reference-conditioned telescope below strengthens its increment to the
intrinsic extension cost. Fix a horizon simulator and its actual user-independent omega_T, with
inert purifier F. Feed fresh purified copies of one full-rank rho and retain
Y_t=Q_t A_t. Before each visit B_(t-1) F Y_<t is pure. Q_t is independent of
F Y_<t, and tracing the active operation preserves this product exactly.
Global purity and the service error delta_T give

`S(B_t)-S(B_(t-1))=S(Y_t|F Y_<t)>=k_(rho,delta_T)`,
`log R_T-S(omega_T)>=T k_(rho,delta_T)`.

Explicitly, Z_t=F Y_<t is finite and Q_t Z_t is exactly product, since the
visit acts only on its complement S_t B_(t-1). The QA marginal is within
delta_T of chi_rho by the complete service guarantee and partial trace.
Thus Y_t Z_t is a feasible extension even though dim Z_t grows with T.
The telescope starts at S(B_0)=S(omega_T) and ends at S(B_T)<=log R_T.

Two points about that extension each deserve a sentence. First, the service
guarantee bounds the complete final state at horizon T, whereas the telescope
reads the state just after visit t. The two agree here because this tester
never touches Y_(<=t) again and every later visit acts on S_(t') B_(t'-1)
alone, so the Q_t A_t marginal is frozen from visit t onward and inherits the
horizon-T bound. Second, Z_t contains the purifier F, which Definition 1.1
makes permanently inaccessible. That is not a use of a forbidden resource. The
auxiliary Z of Definition 1.3 is a mathematical extension of a state, not a
register that anybody operates, and k_(rho,e) is an infimum over all such
states, so the bound needs only that one finite state on Q_t A_t Z_t with the
two stated properties exists. No step here prepares, reads, measures or acts
on F; a device or tester that did so would violate Definition 1.1.

For each fixed rho, take the positive-error limit and then the full-rank input
supremum. Even if some delta_T vanish exactly, eventually delta_T<=e for each
e>0, which supplies the required lower bound without identifying k_(rho,0).

In a separate legal run, feed purified copies of an input attaining h. The
ideal user entropy is Th, while purity and subadditivity give
S(Y^T)=S(B_T F)<=log R_T+S(omega_T). Entropy continuity on the q^(2T)-dimensional
user system gives

`log R_T+S(omega_T)>=Th-2 delta_T T log q-H_2(delta_T)`.

Both testers constrain the same numerical initialization entropy because the
device is fixed before either tester is chosen. Their final bath states can
differ. For each zeta>0 the two eventual inequalities hold simultaneously,
so adding them gives liminf log R_T/T>=(h+kappa)/2. This proves the converse
part of Theorem 2.1, even if S(omega_T)/T oscillates. The entropy-continuity
bound used here is [Audenaert, Theorem 1](https://arxiv.org/pdf/quant-ph/0610146v1),
in its eventual small-distance regime. The remaining implication is proved in
section 6.

## 3. Intrinsic gain and physical witnesses

Theorem 3.1 (uniform collision gain). One has
`kappa=lim_(eta down 0) inf_(Ddiamond(Phi_C,Phi)<=eta) g_C`.

Proof. Let C_eta be the finite collisions
within half-diamond distance eta of Phi, and define a_eta(rho)=inf_(C in C_eta)
f_C(rho), b_eta=inf_(C in C_eta) max_rho f_C(rho). These sets are nonempty:
a pure minimal Stinespring isometry extends to a finite square collision.

Fix full-rank rho and a feasible sigma_QAZ. Purify it on QAZC. Its product
QZ marginal has rank q rank(sigma_Z), so dim C>=rank(sigma_Z). Purification
uniqueness gives an isometry S B0 -> A C from psi_rho x Omega_B0Z, where
dim B0=rank(sigma_Z). Embed B0 into a bath of dimension dim C and complete
this isometry to a square active-only unitary. Initial positive eigenvalues
are those of sigma_Z; the added dimensions have zero weight. Z remains inert.
Purity gives f_C(rho)=S(QA|Z)_sigma. In matching Schmidt coordinates, any
normalized pure reference-input vector has the form (X x I)psi_rho with
||X||^2<=1/lambda_min(rho). Trace-norm contraction under this congruence gives
Ddiamond(Phi_C,Phi)<=e/lambda_min(rho). Conversely a collision in C_eta yields
a feasible extension at error eta. Therefore

`a_(e/lambda_min(rho))(rho)<=k_(rho,e)<=a_e(rho)`.

Their positive-error limits coincide for each FIXED rho. No eigenvalue bound
uniform in rho is used. The Q marginal is rho^T in a fixed canonical basis;
its eigenvalues equal those of the physical input.

Finite convex combinations of gain FUNCTIONS are physical: B=direct_sum B_j,
tau=direct_sum p_j tau_j and U=direct_sum U_j give
f_C(rho)=sum p_j f_Cj(rho) for all rho, with channel error at most eta if
all branches lie in C_eta. Actual initial entropy is H(p)+sum p_j S(tau_j),
and active dimension is sum dim B_j. H(p) cancels in gain because the same
sector probabilities remain at the output. It continues to count in storage.
The maximum of the mixed gain can be smaller than the average separate maxima.

For fixed eta, every f_C is continuous and concave on the compact q-state
space. Put a=sup_rho a_eta(rho). Epsilon-optimal pointwise choices and a finite
open subcover supply f_1,...,f_N with min_j f_j(rho)<a+epsilon for every rho.
The downward set D={x: some rho has x_j<=f_j(rho) for all j} is closed by
subsequence compactness of the input states and convex by concavity. The
point (a+epsilon,...,a+epsilon) is outside D by the finite cover. Strict
finite-dimensional separation gives a normal with nonnegative coordinates:
a negative coordinate would be unbounded above on a downward ray of D.
Normalize that nonzero normal to weights summing to one, giving
max_rho sum p_j f_j(rho)<a+epsilon. The physical flagged collision realizes
this function, so weak minimax supplies b_eta=sup_rho a_eta(rho). There is
no infinite mixture, bath compactness, attainment assumption or finite size bound.

Finally S(rho)-log q<=f_C(rho)<=S(rho)+log q by entropy inequalities on A B.
These bounds are independent of the bath. The infimum a_eta is concave, so
rho_t=(1-t)rho+t I/q satisfies a_eta(rho_t)>=a_eta(rho)-3t log q. Thus at
each eta the full-rank supremum equals the all-input supremum, without assuming
boundary continuity. Shrinking error sets increase their infima, and hence

`lim_(eta down 0) b_eta = sup_(eta>0) sup_(rho>0) a_eta(rho)`
`= sup_(rho>0) sup_(eta>0) a_eta(rho) = kappa`.

Only two suprema have been interchanged. This yields finite approximate
collisions uniformly over inputs at every positive accuracy and gain slack.
It yields no exact witness at zero error and no uniform bound on witness
dimension or spectrum. Pointwise lifting uses purification uniqueness and the
semilocalization mechanism of [Eggeling, Schlingemann and Werner, section III](https://arxiv.org/pdf/quant-ph/0104027v1).
After physical flags convexify gain functions, the uniform step is an instance
of classical minimax: [Sion, Theorem 4.2 (Kneser--Fan), p. 175](https://msp.org/pjm/1958/8-1/pjm-v8-n1-p14-p.pdf).
The compact side is the input state space, and evaluation is concave in the
input and affine in the gain function. The finite separation proof above
makes this application explicit. The error conversion and limit order then
give the collision interpretation needed here.

## 4. Active repair and exactification

Theorem 4.1 (active support repair and exactification). For a fixed Phi
with Choi rank k, every sufficiently eta-close finite collision (U,tau) on
R bath dimensions admits a support-repaired collision on (k+1)R dimensions
with the same positive initial spectrum, Choi support contained in that of
Phi, channel error at most eta+e_eta, and gain increase at most beta_q(e_eta),
where e_eta=O_Phi(eta^(1/6)). A further counted flagged correction implements
Phi exactly, on at most (k+1)R+k dimensions, with gain increase tending to
zero uniformly in R and tau. Combining this repair with Theorem 3.1 gives
kappa_exact=kappa. The small-error threshold and constants may depend on
the fixed Phi (including k, C_Phi and its positive Choi eigenvalue mu),
but not on R, tau or the auxiliary dimension.

Lemma 4.2 (amplified Gram completion). The fixed Kraus span admits the
following almost-isometry completion with an auxiliary-dimension-independent
constant. Uniform amplification bounds for maps into a fixed matrix algebra
are standard, including [Smith's lemma](https://doi.org/10.1112/jlms/s2-27.1.157).
We give an explicit trace-slice bound and use it to complete the Gram defect
within the prescribed Kraus span. Fix a minimal Kraus
family A_a for Phi, K=span A_a and D=span A_a* A_b. The Gram map
L(E_ab)=A_a* A_b maps I_k to I_q. A Hermiticity-preserving right inverse R_map
on D can be expressed as a finite sum of trace functionals times fixed
Hermitian matrices. The slice inequality bounds every amplification R_map x id
by one constant C_Phi independent of the auxiliary dimension. Explicitly,
choose Hermitian bases H_l of D, Hermitian preimages C_l, and trace-duals F_l.
Then R_map(X)=sum_l Tr(F_l X)C_l and one may take
C_Phi=max(1,sum_l ||F_l||_1 ||C_l||_infinity). Diagonalizing F_l expresses
each amplified slice as a signed sum of diagonal compressions of X; each
compression has norm at most ||X||. This proves the bound at every dimension.
Positivity of R_map is neither asserted nor needed.

For V=sum A_a x B_a with Delta=V*V-I and ||Delta||<=d, set t=C_Phi d and
G=(tI-(R_map x id)(Delta))/(1+t)>=0. Its square-root block columns C_a obey
C_a* C_b=G_ab. Thus W=sum A_a x C_a has
W*W=(L x id)(G)=(tI-Delta)/(1+t). The stacked map
[V/sqrt(1+t);W] is therefore an exact isometry whose coefficients stay in K.
Polar normalization need not preserve K and is not used. Here the block
columns C_a map the input bath H0 into C^k H0, and
||W||<=sqrt((t+d)/(1+t)), completing the lemma's proof.

Proof of Theorem 4.1. The coefficient projection below is an offline matrix
construction; the device does not measure a Choi projector. Throughout this
proof epsilon is a cutoff parameter, distinct from the smoothing error e of
Definition 1.3.

For an eta-close mixed collision U,tau implementing Psi, choose a bath
eigenbasis tau=sum_j lambda_j |j><j| and write
U=sum_(b,j) U_bj tensor |b><j|. If Pi_K is Hilbert--Schmidt projection
of system matrices onto K, set V=sum_(b,j) Pi_K(U_bj) tensor |b><j|
and L0=U-V. The channel Kraus operators are sqrt(lambda_j) U_bj;
the projection itself is unweighted and the spectrum enters their Choi
sum through lambda_j. Let P_K
be the projector onto the vectorized Kraus span, the support of J_Phi.
Normalized Choi leakage is
p=Tr((I-P_K)J_Psi)=Tr((I x tau)L0*L0)/q<=eta. Set E=Tr_S L0*L0. The
positive-operator inequality X<=q I x Tr_S X and the cutoff
`P=1_[0,epsilon^2/q](E)` give

`||L0(I x P)||<=epsilon`, `Tr(tau(I-P))<=q^2 eta/epsilon^2`.

For completeness the domination follows by applying Cauchy--Schwarz to the q
vectors X^(1/2)(|i>xi_i), then bounding each diagonal block X_ii by their sum.
The cutoff-weight bound follows from E>=(epsilon^2/q)(I-P) and
Tr(tau E)=qp. Neither estimate assumes [tau,P]=0. Repair V on S PB with
the Gram construction
and use the target's pure Stinespring map on S (I-P)B, retaining the complete
bad-bath input via |psi>|b> -> sum_a A_a|psi>|a>|b> in the sector
C^k (I-P)B, orthogonal to B and C^k PB used by the good map. The resulting
isometry has bath output
B_hat=B direct_sum (C^k x B), dimension (k+1)R. Initialize tau_hat=tau direct_sum 0
and complete the initialized columns to an active-only unitary. The old positive
spectrum is unchanged, the old F remains inert, and the system channel's Choi
support lies in the target face. Off-diagonal cutoff coherences are retained
in the global output; no pinching, measurement or discard occurs.

With d_epsilon=2epsilon+epsilon^2, t_epsilon=C_Phi d_epsilon and
a_epsilon=epsilon+t_epsilon/2+sqrt((t_epsilon+d_epsilon)/(1+t_epsilon)), the
joint purified output distance is at most a_epsilon+2q sqrt(eta)/epsilon,
uniformly over inputs. Here ||Delta||<=d_epsilon on the good sector because
V(I x P)=U(I x P)-L_0(I x P) with U an isometry and ||L_0(I x P)||<=epsilon,
so ||(I x P)(V*V-I)(I x P)||<=2epsilon+epsilon^2. The good-input operator
distance is at most a_epsilon: on that sector
V/sqrt(1+t_epsilon)-U=(V-U)/sqrt(1+t_epsilon)+(1/sqrt(1+t_epsilon)-1)U has
norm at most epsilon+t_epsilon/2, since U is an isometry and
1-1/sqrt(1+t)<=t/2, while the W block contributes at most
sqrt((t_epsilon+d_epsilon)/(1+t_epsilon)). Taking epsilon=eta^(1/3) gives
e_eta=O_Phi(eta^(1/6)). The bad component of the same initial purification
has vector norm at most q sqrt(eta)/epsilon; two isometries differ on it by at
most twice that norm.
Pure-state half distance is bounded by vector distance. Thus cutoff coherences
are controlled without removing them. At eta=0 retain the original collision.
Both gains equal S(QA|F) on a q-dimensional input purification. Thus the
conditional-entropy bound of [Winter, Lemma 2, v6](https://arxiv.org/html/1507.07775v6)
gives sup_rho |f_C_hat-f_C|<=beta_q(e_eta), where
beta_q(e)=4e log q+(1+e)H_2(e/(1+e)), for sufficiently small e_eta<=1.
The bound involves dim QA=q^2; it has no bath or purifier dimension factor.

Let mu be the smallest positive eigenvalue of J_Phi and bar_eta=eta+e_eta.
Inside its support, ||J_Psi_hat-J_Phi||_infinity<=2bar_eta and
J_Phi>=mu P_K. Therefore f=2bar_eta/(mu+2bar_eta) ensures
J_Phi-(1-f)J_Psi_hat>=0. Its partial trace is f I/q, so division by f
defines a CPTP correction Theta of Kraus rank at most k. A counted direct-sum
collision implements Phi=(1-f)Psi_hat+f Theta exactly and obeys

`g_exact<=g_C+beta_q(e_eta)+f log k`.

Indeed g_exact<=(1-f)(g_C+beta_q(e_eta))+f log k, and
g_C>=f_C(pi_q)>=0 by entropy conservation and subadditivity.
This uses the function-level flag identity. At zero error the
correction is omitted. Final active dimension is at most (k+1)R+k. If the
original positive eigenvalues are lambda_i, the exact collision's eigenvalues
are ((1-f)lambda_i,f), with entropy H_2(f)+(1-f)S(tau). Thus spectrum preservation
belongs to support repair; exactification changes the spectrum explicitly.
The initial entropy itself need not change uniformly little as R grows.
That last sentence describes the repair; it is not a gap in what the repair
hands on. Theorem 5.1 accepts any fixed finite exact collision together with
whatever finite spectrum that collision actually has. It nowhere asks the
exact witness's spectrum to be close to the approximate one's, and it uses no
bound on eigenvalue ratios, on bath dimension or on concentration constants.
Section 6 selects a witness and fixes all of its dimensions, spectra and
constants for each m before any horizon is chosen, so a spectrum that jumps at
exactification costs nothing in the diagonal that follows.

Choose a sufficiently small fixed eta for each gain slack, use Theorem 3.1 to choose
one finite approximate witness, and exactify it. The uniform penalty gives
kappa_exact<=kappa; exact witnesses belong to every feasible set of
Theorem 3.1, giving
the reverse inequality. No horizon is selected in this argument. An exact
pure Stinespring collision has gain h, so replacing any witness with gain
above h by this pure collision yields exact witnesses with 0<=g<=h and
g->kappa. These, with their actual arbitrary finite spectra, are the inputs
Theorem 5.1 accepts. This closes the proof of Theorem 4.1 without using
Theorem 5.1 or a horizon limit.

Corollary 4.3 (pointwise smoothing and privacy funnel). Using the lifting
construction in Theorem 3.1 and the pointwise repair in Theorem 4.1, for
each fixed full-rank rho one has

`lim_(e down 0) k_(rho,e)=K0(rho)`,
`kappa=sup_(rho>0) [S(chi_rho)-P_q^(psi_EQ)(0)]`.

To justify the exact mapping in Definition 1.3, purify any exact extension
on QAZC. Uniqueness of purification gives an isometry from supp psi_E to
ZC; tracing C and extending the map arbitrarily outside that support gives
a channel E->Z. Conversely such a channel yields an extension, proving the
claimed parametrization even when psi_E is singular.

For stability, fix ell=lambda_min(rho)>0. Any e-feasible extension lifts
to a finite collision C at error at most eta=e/ell, with its objective equal
to f_C(rho). The support repair above changes this pointwise gain by at most
beta_q(e_eta). Let w_eta be the final correction weight. Function-level
flag mixing, f_Theta(rho)<=log k, and f_C(rho)>=S(rho)-log q>=-log q give

`f_exact(rho)<=f_C(rho)+beta_q(e_eta)+w_eta(log k+log q)`.

The exact collision supplies an exactly feasible extension. Taking arbitrarily
small optimization slack at each positive e below the Phi-dependent threshold
of Theorem 4.1, applied at eta=e/ell, therefore gives

`k_(rho,e)<=K0(rho)<=k_(rho,e)+beta_q(e_(e/ell))+w_(e/ell)(log k+log q)`.

The two penalties vanish at fixed Phi and rho independently of the extension
dimension. This proves the equality before taking the full-rank supremum.
No infimum is interchanged with a limit, and no finite auxiliary-dimension
bound, optimizer, or uniformity as ell tends to zero is asserted. The
pointwise lower bound is needed here; g_C>=0 alone would not suffice.
This reformulation follows from this paper's repair, not from the prior
privacy-funnel definition, and does not alter the order in Definition 1.3.

## 5. Causal balancing of a fixed exact collision

Theorem 5.1 (fixed exact witness). Fix one finite exact collision C=(U,tau)
for Phi, with full active cell dimension R. Write sigma=S(tau),
v=max_rho S(Gamma_C(rho)), g=v-sigma and suppose g<=h. Then an all-horizon
family in Definition 1.1 achieves vanishing complete adaptive error and
actual rate limits

`r=b=(h+g)/2`, `s=a=(h-g)/2`.

Its complete initial positive spectrum is flat. More specifically it has a
pure clock, a maximally mixed seed of dimension J_T, K_T mixed data qubits,
and pure remaining data, with log J_T/T->0 and K_T/T->a separately.
No uniform bound on the fixed witness's dimension, eigenvalue ratios,
concentration constants or circuit complexity is imposed.

Proof. Feeding pi_q and using total entropy conservation gives v>=sigma.
For a purified input, BF is a complementary output and F has entropy sigma;
h<=v+sigma. Hence 0<=a<=sigma, b=a+g and v<=log R. These are the only resource
inequalities used to allocate the construction.

[Appendix A](appendix-causal-balancing.md) supplies the complete proof.
Lemma A.1 gives uniform adaptive spectral concentration. Lemma A.2 transfers
the virtual minimal-environment support to a purification of the complete
exterior and retains the normalization in the simultaneous projector bound.
Lemma A.3 proves the second moment with the physical seed still present.
Lemma A.4 constructs the nonflat cell marginal reversibly from flat stock
on exact integer wires. Proposition A.5 proves joint recycling and every
prefix's error with disjoint parked residues. Proposition A.6 counts the
clock, actual spectrum and every-horizon limit. All are proved in this paper.

The encoder is the sender's unitary from fully quantum Slepian--Wolf:
sender=C, retained share=M, message=G, receiver=N and reference=H; the
receiver is written N here to keep F for the purifiers of Definition 1.1 and
Appendix A.
Its decoder acts on GN, so omitting that decoder leaves MH unchanged.
The physical device parks and counts G. The split and its half-sum rates
are established prior ingredients, specifically Abeyesinghe et al.,
Theorems IV.1--IV.2, Lemma IV.5 and Eq. (30), pp. 6--9, with the asymptotic
rate choice following Eq. (35) in section VII, in
[the mother protocol, v1](https://arxiv.org/pdf/quant-ph/0606225v1).
The present appendix supplies the adaptive spectral control, reversible
flat-stock preparation and counted reuse of seed and workspace needed to
turn this split into the stated closed device. These implementation steps
are part of the operational synthesis.

## 6. Assembling the region

Proof of Theorem 2.1. The argument uses Theorems 2.2, 3.1, 4.1 and 5.1.

First apply the converse bounds of Theorem 2.2 to an arbitrary all-horizon
family, writing
x_T=log R_T/T and y_T=S(omega_T)/T. For each zeta>0, eventually BOTH
x_T-y_T>=kappa-zeta and x_T+y_T>=h-zeta. Their common actual initialization
therefore gives 2x_T>=h+kappa-2zeta, regardless of whether y_T converges.
Thus liminf x_T>=(h+kappa)/2 and c_seq has this lower bound. For rate-limit
pairs, s>=0, r+s>=h and r-s>=kappa follow and survive closure. The definition
gives 0<=kappa<=h: S(QA|Z)>=S(rho)-log q is nonnegative at rho=I/q, while
the exact trivial-Z extension has entropy S(chi_rho)<=h.

Theorems 3.1 and 4.1 give kappa_exact=kappa. For each m>=1
select a finite EXACT collision with gain <kappa+1/m. Replace it by a pure
exact Stinespring collision of gain h if its gain exceeds h. Then
kappa<=g_m<=h and 0<=g_m-kappa<1/m. This also handles kappa=h without
assuming attainment. Set a_m=(h-g_m)/2 and b_m=(h+g_m)/2. All dimensions,
spectra and concentration constants are fixed separately for each m.

Theorem 5.1 supplies, for each
fixed witness, all-horizon devices with error delta_(m,T)->0 and rates
(b_m,a_m). Their exact initialization is

`omega_(m,T)=|0><0|_clock tensor pi_(J_(m,T)) tensor pi_(2^K_(m,T)) tensor |0><0|_rest`,
`R_(m,T)=(T+1) J_(m,T) 2^A_(m,T)`,
`S(omega_(m,T))=log J_(m,T)+K_(m,T)`.

Here 0<=K_(m,T)<=A_(m,T) are integers. Theorem 5.1 proves separately that
log J_(m,T)/T->0 and K_(m,T)/T->a_m. Choose a finite H_m such that for
EVERY T>=H_m, the error and each of

`|log R_(m,T)/T-b_m|`, `|S(omega_(m,T))/T-a_m|`,
`log J_(m,T)/T`, `|K_(m,T)/T-a_m|`

are at most 1/m. Take T_1=max(1,H_1) and
T_(m+1)=max(H_(m+1),T_m+1). For T>=T_1 select the complete m-th device
with m=m(T)=max{j:T_j<=T}; use exact pure preallocated cells for earlier T.
Since T_m>=m, this maximum is finite; for every M, T>=T_M implies m(T)>=M.
Thus m(T)->infinity over all horizons. Every selected T lies beyond H_m,
so the bounds hold throughout T_m<=T<T_(m+1). With

`r0=(h+kappa)/2`, `s0=(h-kappa)/2`,

the actual rate errors are at most 3/(2m(T)), the adaptive error is at most
1/m(T), K_T/T->s0, and log J_T/T->0. The separate seed threshold is needed
for the region proof; it must not be inferred merely from total-rate limits.
Hardware and its actual initializer are selected before the user for each T;
no witness changes online. Each elementary collision implements EXACT Phi,
so there is no accumulated T eta term. This proves c_seq=r0 with actual
entropy rate s0. No effective thresholds or witness-size bound are claimed
for this achievability half. The converse half is the half that constrains
an actual device: for every finite horizon, Theorem 2.2's two inequalities
hold with explicit constants in terms of that horizon's own error delta_T,
although the extension-cost term k_(rho,delta_T) itself is an infimum that is
not asserted to be computable. Only the thresholds H_m above are
non-effective.

The selected base family has P_T=J_T 2^K_T equal positive eigenvalues 1/P_T
and R_T-P_T zeros. To reach 0<=s<=s0 put d=s0-s and
l_T=min(K_T,floor(dT)). Then l_T/T->d, including the clipped endpoint s=0.
Replace l_T of the initially mixed data qubits by halves of Bell pairs with
l_T NEW, counted active partner qubits P. Keep the other initial factors
unchanged and extend the repeated unitary to W_T tensor I_P. The new old-bath
marginal is EXACTLY omega_T. Partial trace over P commutes with every device
and adaptive-user operation, so the entire original marginal process and its
complete adaptive error are unchanged. This uses a new offline initializer,
not an operation on the original inaccessible purifier.

Exactly, the new dimension is R_T 2^l_T, its positive rank is
P_T^-=J_T 2^(K_T-l_T), and its positive spectrum is 1/P_T^- repeated P_T^-
times, with zeros elsewhere. Its entropy is S(omega_T)-l_T. Therefore the
limiting pair is (r0+d,s0-d)=(h-s,s). At s=0 the remaining entropy is
log J_T+max(K_T-floor(s0 T),0)=o(T); a zero entropy RATE does not require
exactly pure finite-horizon initialization. Partners remain counted and untouched,
and a purifier of the new initializer remains inaccessible.

For s>=s0 instead append n_T=floor((s-s0)T) unused maximally mixed qubits
in product, extending W_T by identity. Dimension and positive rank both
multiply by 2^n_T and entropy increases by n_T. The positive spectrum remains
flat and the user process is unchanged. This gives (kappa+s,s). For any
r>=r_min(s)=max(h-s,kappa+s), append floor((r-r_min(s))T) unused pure
qubits. This increases dimension, leaves positive rank and entropy unchanged,
and adds only zero eigenvalues. All rounding errors vanish after division by T.

Every finite rate pair in the stated region is thus realized with actual
rate limits; the set is already closed. At each finite horizon, rank<=dimension
and S<=log R hold: internal purification decreases rank and increases dimension,
mixed padding multiplies both equally, and pure padding only increases dimension.
Asymptotically r>=s follows from kappa>=0. At q=1 the trivial bath-free device
and padding realize r>=s>=0. If kappa=h, s0=0; if kappa=0, r0=s0=h/2.
Both endpoints are covered by the same integer constructions.

The dependency order is acyclic: Theorem 2.2 is an independent converse;
the fixed-error minimax of Theorem 3.1 precedes the exactification of
Theorem 4.1; Theorem 5.1 acts on one fixed exact witness without Theorems 3.1
and 4.1; the all-horizon diagonal then combines these inputs. Internal
purification and padding are last. The encoder-only FQSW attribution of
section 5 remains in force. This completes the proof of Theorem 2.1.

## 7. Examples and limitations

Proposition 7.1 (unitary channels). For Phi(rho)=V rho V*, h=kappa=0
and the minimum memory rate is zero.

Proof. A minimal environment is one-dimensional, so h=0. Every feasible
extension has S(QA|Z)>=S(rho)-log q, which is nonnegative at rho=pi_q.
Taking a trivial Z gives kappa<=h, hence kappa=0. The bath-free repeated V
implements all visits exactly and has both rates zero.

Proposition 7.2 (qubit dephasing). For Delta(rho)=(rho+Z rho Z)/2,
h=1, kappa=0, and Theorem 2.1 gives the corner r=s=1/2.

Proof. A minimal dilation copies the computational-basis label into a qubit
environment. Its output entropy is the binary entropy of the input diagonal,
maximized at one. A fair classical bath bit controlling I or Z implements
Delta. Its active marginal stays pi_2 for every input, so g=0. Theorem 3.1
and kappa>=0 imply kappa=0.

There is also a direct exact streaming realization of the corner. Put
m=ceil(T/2), initialize m bath qubits in pi_(2^m), and choose T distinct
binary-independent Pauli generators from X_1,Z_1,...,X_m,Z_m. At visit t
use the system computational bit to control the t-th generator P_t on the
bath. For a history x in {0,1}^T, its ordered bath word is
P(x)=P_T^(x_T)...P_1^(x_1). Distinct histories give distinct Pauli words
up to phase and
Tr(P(x)P(y)*)/2^m=delta_(x,y). Expanding any purified adaptive tester in
computational histories, its retained user vectors are weighted by precisely
this Gram matrix after tracing the bath. All cross-history terms vanish,
exactly as for fresh dephasing records; this proves complete adaptive
service, including reference-entangled inputs. A pure (T+1)-state clock
compiles these gates into one repeated unitary as in (A.5).
Thus log R=m+log(T+1) and S(omega)=m, with no discard. This is the
counted streaming specialization of the orthogonal-unitary construction in
[Boes et al., Lemma 1, v3](https://arxiv.org/pdf/1804.03027v3), not a claim
to originate its square-root dephasing memory saving. The subsequent
[2020 erratum](https://journals.aps.org/prx/pdf/10.1103/PhysRevX.10.029901)
corrects section V/Theorem 3's expander result, which is not used here;
it does not modify the dephasing lemma cited above.

Proposition 7.3 (pure replacement). For Phi(rho)=|0><0| Tr rho on C^q,
h=kappa=log q and c_seq=log q.

Proof. A minimal dilation maps |psi> to |0>_A |psi>_E, so h=log q.
For any feasible extension,
S(QA|Z)>=S(rho)-S(sigma_A). Its A marginal is within e of |0><0|,
hence S(sigma_A)->0 at fixed q by entropy continuity. At rho=pi_q this
gives kappa>=log q, while kappa<=h gives equality. Specializing the preallocated
cell construction of [Rybar and Ziman, section III](https://arxiv.org/pdf/0808.3851v1), preallocate T pure
q-dimensional cells and swap each arriving input into its designated cell,
returning |0>; retain all cells and count the pure clock. This exact device
has log R=T log q+log(T+1) and S(omega)=0. Its bath grows with T, as it
must: Theorem 2 of Rybar and Ziman excludes a fixed finite memory for this
nonunital channel. No mixed-replacement or
other companion classification is needed for this example.

Proposition 7.4 (a lower bound on kappa over the input space alone). For
every channel Phi,

`kappa(Phi)>=max_rho [S(rho)-S(Phi(rho))]`.

Proof. Fix rho>0 and any e-feasible extension sigma in Definition 1.3, with
q>=2. The chain rule and the conditional form of Araki--Lieb give

`S(QA|Z)=S(Q|Z)+S(A|QZ)>=S(rho)-S(sigma_A)`,

using S(Q|Z)=S(rho) from the exact product sigma_QZ=rho^T x sigma_Z and
S(A|QZ)>=-S(A). Since D(sigma_QA,chi_rho)<=e and Tr_Q chi_rho=Phi(rho), the
marginal sigma_A is within half distance e of Phi(rho), so
[Audenaert, Theorem 1, v1](https://arxiv.org/pdf/quant-ph/0610146v1) gives
S(sigma_A)<=S(Phi(rho))+e log(q-1)+H_2(e). Hence
k_(rho,e)>=S(rho)-S(Phi(rho))-e log(q-1)-H_2(e). Letting e->0 at fixed rho
and then taking the supremum over full-rank rho gives
kappa>=sup_(rho>0) [S(rho)-S(Phi(rho))], which equals the maximum over all
states by continuity of the bracket and density of the full-rank states; the
maximum exists by compactness. This uses neither Theorem 3.1 nor Theorem 4.1.

The same bound holds for every finite EXACT collision C=(U,tau), by the
entropy-conservation and subadditivity budget of
[Rybar and Ziman, section III, Eq. (3.7)](https://arxiv.org/pdf/0808.3851v1):
U(rho x tau)U* on A B is unitarily equivalent to rho x tau, so
S(AB)=S(rho)+S(tau), while subadditivity gives
S(AB)<=S(Phi(rho))+S(Gamma_C(rho)). Subtracting S(tau),

`f_C(rho)>=S(rho)-S(Phi(rho))` for every rho,

hence g_C>=max_rho [S(rho)-S(Phi(rho))]. This second route bounds kappa_exact
directly and reaches kappa only through Theorems 3.1 and 4.1.

Unlike Definition 1.3, the right-hand side is an optimization over the
q-dimensional state space alone: no auxiliary system, no smoothing and no
order of limits enter it. It is exactly the universal parallel work rate at
trivial Hamiltonians of [Faist, Berta and Brandao, Theorem 5.1 and Eq. (5.4),
v3](https://arxiv.org/html/1911.05563v3), so the entropy-deficit rate of a
closed device is at least that thermodynamic work rate; section 8 compares the
two contracts. The bound reproduces the three examples above exactly: it is
zero for a unitary channel, zero for dephasing because a unital channel never
decreases entropy, and log q for the pure replacer.

Proposition 7.5 (an interior corner). For 0<=nu,p<=1 let Phi_(nu,p) on
q=2 have the generalized amplitude damping operators

`K_0=sqrt(p) diag(1,sqrt(1-nu))`, `K_1=sqrt(p nu) |0><1|`,
`K_2=sqrt(1-p) diag(sqrt(1-nu),1)`, `K_3=sqrt((1-p)nu) |1><0|`,

which satisfy sum_a K_a* K_a=I; the damping parameter is written nu to keep
gamma for the concentration slack of Appendix A. At nu=1/2 and p=3/4,

`0<H_2(7/12)-H_2(1/3)<=kappa<=1-H_2(3/4)<H_2(3/8)<=h`,

that is 0.061572<=kappa<=0.188722 and h>=0.954434, each decimal rounded
towards the side that keeps the inequality valid. Hence 0<kappa<h.

Proof. Trace preservation is the diagonal identity
p+(1-p)(1-nu)+(1-p)nu=1 and p(1-nu)+p nu+(1-p)=1.
For the lower bound, the channel acts on diagonal inputs by
Phi(diag(a,1-a))=diag(3/8+a/2,5/8-a/2), so rho=diag(7/12,5/12) has output
exactly diag(2/3,1/3), and Proposition 7.4 at this rho gives
kappa>=H_2(7/12)-H_2(1/3)>0 through the entropy-decrease budget credited
there. The maximally mixed input, with Phi(I/2)=diag(5/8,3/8), gives only
1-H_2(5/8)=0.04556..., and is not the maximiser of the bracket in
Proposition 7.4; N. Mghirbi (private communication, 2026) observed that
diag(3/5,2/5) already improves it to 0.061214. A numerical search over all
qubit inputs, rerun by the script named in Appendix B.4, finds the maximum
0.061598 at diag(0.58671,0.41329), so the rational witness above is within
0.00003 of the best bound this proposition can give for the channel.

For the upper bound, exhibit an exact collision. Take B=C^2, tau=diag(p,1-p),
and the unitary U fixing |00> and |11> and acting on the ordered pair
|01>,|10> by

`[[sqrt(1-nu),-i sqrt(nu)],[-i sqrt(nu),sqrt(1-nu)]]`.

That block is unitary, so U is. Writing U=sum_(b,j) U_bj tensor |b><j| as
in section 4, its weighted bath matrix elements sqrt(lambda_j) U_bj are
U_00=diag(1,sqrt(1-nu)), U_11=diag(sqrt(1-nu),1),
U_10=-i sqrt(nu)|0><1| and U_01=-i sqrt(nu)|1><0|, weighted by
sqrt(p) and sqrt(1-p); these are the four operators above up to individual
phases, so Phi_C=Phi exactly. This is a lawful finite collision in the sense of
Definition 1.4: tau is user independent, U acts on system and active bath
only, and log dim B=1 with S(tau)=H_2(p). Because dim B=2, its active output
entropy is at most one for EVERY input, whatever the off-diagonal entries, so
g_C<=1-H_2(3/4). This bound is attained: the input diag(1/4,3/4) sends the
active bath output of this collision to I/2, so g_C=1-H_2(3/4) exactly and
the witness cannot be improved. Theorems 3.1 and 4.1 give
kappa=kappa_exact<=g_C.

For h, the minimal dilation of a pure input has system and environment with
the same nonzero spectrum, so h>=S(Phi(|1><1|))=H_2(3/8), since
Phi(|1><1|)=diag(3/8,5/8). A mixed input does better: at diag(1/3,2/3) the
complementary output has entropy 1.148402 (also observed by N. Mghirbi; the
numerical maximum is 1.148986 at diag(0.35586,0.64414)), so in fact h>1,
although the analytic bound suffices here. Strictness follows from H_2 being
strictly increasing on (0,1/2): H_2(3/8)>H_2(1/4)=H_2(3/4)>1/2>1-H_2(3/4).

This locates the corner without computing kappa. Two consequences are already
visible from the bracket. Since kappa>0, no device for this channel has a
vanishing entropy-deficit rate, so r=s is impossible and the minimum dimension
rate (h+kappa)/2 strictly exceeds h/2. Since kappa<h, the optimal initial
entropy rate s0=(h-kappa)/2 is strictly positive, so the cheapest device is
strictly mixed rather than pure. The bracket also gives g_C<=h for this
witness, so Theorem 5.1 applies to it directly and produces an explicit
all-horizon family. The finite arithmetic behind the displayed decimals is
rerun by the script named in Appendix B.4; the strict inequalities above are
analytic and use no optimizer.

The quantity c_seq measures complete operating storage. It is not identified
with a universal unavoidable terminal residual rate under unrestricted growth
of a working bank. A construction's parked-residue rate does not establish
such an equality. The theorem asserts no efficient witness search, circuit
bound, bath return, independent return, spatial additivity, or service law for
arbitrary multi-visit processes. It concerns one fixed memoryless channel.

## 8. Related work and distinct zero-cost statements

Rybar and Ziman's [Repeatable quantum memory channels, arXiv:0808.3851v1,
sections II--IV](https://arxiv.org/pdf/0808.3851v1) is a close physical
comparison. After Eq. (2.3) they assume product inputs. Their section III
repeatability definition fixes one memory, initializer and unitary for all
repetitions and requires the same single-use marginal channel at every
step. Theorem 1 supplies finite random-unitary repeaters; Theorem 2 rules
out nonunital finite-memory repeaters. Their conclusion leaves general
unital, non-random-unitary repeatability open and acknowledges correlations
between outputs and effects of measurements. These are statements of that
2008 paper, not a claim about the current status of its question.

Proposition 8.1 (shared-seed separation). One fair bath bit controlling I or Z
on every qubit is such a marginal dephasing repeater, but its complete
service error against independent dephasing is at least 1-2^(1-T).

Proof. For any product input list, the bath bit's probabilities remain
(1/2,1/2), so each individual output has dephasing's marginal. For T inputs
|+>, the joint output is
`(|+><+|^tensor T+|-><-|^tensor T)/2`.
Independent dephasing produces pi_(2^T). Both states are diagonal in the X
basis. Summing the two occupied-string discrepancies and the other 2^T-2
discrepancies gives half distance 1-2^(1-T). The event that all X outcomes
agree attains it, already 1/2 for T=2. No feedback is needed to distinguish
the contracts. In particular, the finite shared seed is not a small-error
device for Definition 1.2.

Our device may depend on T and has vanishing complete adaptive error.
Those quantifiers and its joint service requirement differ from fixed finite
exact marginal repeatability. Finite n-repeatability and the n-cell
permutation construction are also in Rybar--Ziman; horizon dependence alone
is not a new distinction. Theorem 2.1 is not asserted to resolve
Rybar--Ziman's question or an unspecified asymptotic adaptive version.

The resource distinctions can be stated precisely from the core theorem:

| Statement | Meaning and consequence |
|---|---|
| Zero initial entropy | S(omega_T)=0 at a specified finite horizon; stronger than its entropy being sublinear. |
| Zero initial entropy rate | s=0; the region requires r>=h. Exact purity at every horizon is not implied. |
| Zero entropy deficit | log R_T-S(omega_T)=0 at a specified horizon, equivalently omega_T=pi_(R_T). |
| Zero entropy-deficit rate | r-s=0; under Theorem 2.1 this is possible iff kappa=0, with r=s>=h/2. |
| Zero memory rate | r=0; then s=0 and h=0. In the square-channel setting this is possible exactly for unitary channels. |
| Exact finite tracial factorization | One exact finite weighted-tracial dilation exists, with fixed finite algebra and weights. |
| Finite-tracial approximation closure | Arbitrarily accurate finite tracial dilations exist; no bounded dimension or exact attained dilation follows. |

For the unitary characterization in this table, if h=0 every complementary
output is pure. Convexity forces these outputs to be the same pure state,
since a mixture of distinct pure states has positive entropy. The dilation
therefore factors as an isometry S->A tensor that pure state. Equal input
and output dimensions make the isometry unitary; Proposition 7.1 gives the
converse.

A finite weighted-tracial dilation means B=direct_sum_j C^(d_j),
tau=direct_sum_j p_j pi_(d_j), and a unitary preserving these sectors.
It implements sum_j p_j Tr_(B_j) U_j(rho x pi_(d_j))U_j*. Each sector's
output bath entropy is <=log d_j and pi_q attains equality in every sector,
so g=0 by the block entropy identity. Theorem 3.1 therefore implies that
membership in this approximation closure gives kappa=0. The reverse
implication requires an additional gain-to-tracial approximation argument
and is not a consequence proved in this paper.

Allowing weighted direct sums is a broader exact convention than a single
maximally mixed matrix bath. Their approximation closures coincide: for
large D choose nonnegative integers m_j with sum_j m_j d_j=D and
m_j d_j/D approaching p_j (for example take D along multiples of the d_j,
and approximate the weights rationally). Replicate U_j on m_j copies.
The half-diamond channel discrepancy is at most the total variation in
weights. This observation supplies approximation, not exact attainment
for irrational weights.

The distinction is substantive prior mathematics. [Musat--Rordam, v4,
Theorem 4.1](https://arxiv.org/html/1806.10242v4) gives Schur channels in the
finite-factorization closure with no exact finite-dimensional factorization,
in dimensions 2n+1 for n>=5. We cite that theorem for this distinction,
without re-proving its operator-algebraic dependency chain. Likewise
[Lie, Son, Boes, Ng and Wilming, published Proposition 6 and Eq. (12)](https://journals.aps.org/prl/pdf/10.1103/lm3h-c5f5)
relate informational equilibrium to weighted-tracial dilations and
factorizable channels. These structural and equilibrium ingredients are
prior work. No companion finite-tracial-closure equivalence or quantitative
modulus is imported into the results proved here.

Pointwise product-reference lifting uses the Stinespring uniqueness mechanism
in [Eggeling, Schlingemann and Werner, section III](https://arxiv.org/pdf/quant-ph/0104027v1).
The uniform optimization and smoothing order in section 3 are written
separately. Ordinary dilation continuity, as in
[Kretschmann, Schlingemann and Werner, Definition 1 and Theorem 1](https://arxiv.org/pdf/0710.2495v1),
does not itself impose a comparison acting only on the active bath with an
already fixed inert purifier and positive initial spectrum. This is a
difference in the stated contract, not proof of originality of Theorem 4.1.

In particular, purifying a mixed initializer gives a dilation into A B F.
The environmental comparison in ordinary Stinespring continuity can act on
the joint B F; it need not factor as an operation on B tensored with I_F.
Theorem 4.1 instead preserves the old positive spectrum at the support-repair
stage and completes columns inside the target Kraus span, with a gain bound
uniform in the bath size. The final flagged exactification changes the
spectrum. These are the precise extra requirements in the comparison.

For factorization background, [Haagerup and Musat, Definition 1.3 and
Theorem 2.2, v1](https://arxiv.org/pdf/1009.0778v1) characterize matrix Markov
maps through unitary dilations with a tracial von Neumann algebra. Their
finite von Neumann algebra need not be finite dimensional; our device bath
must be. This is background to the closure/attainment distinction above,
not a historical claim that they originated all factorization terminology.

The privacy-funnel comparison in Definition 1.3 identifies the exact
pointwise cost, with its smoothing equality supplied by section 4. The classical
privacy funnel originates with [Makhdoumi et al.](https://arxiv.org/abs/1402.1774);
Datta, Hirche and Winter supply the quantum definition used here. Other
channel entropies answer different questions. In particular, [Gour and Wilde,
Proposition 6, Theorem 10 and Proposition 24, v3](https://arxiv.org/html/1808.06980v3)
give a channel entropy and a universal parallel channel-merging theorem.
Their protocol allows operations on both output and environment shares,
free one-way classical communication, and measures net entanglement gain.
Its channel entropy is -log q for a unitary and zero for a pure replacer;
our kappa is respectively zero and log q. Their universal merging result
is a close antecedent, but its resource accounting and access differ from ours.

FQSW attribution is explicit in section 5. Its encoder and the universal
merging/QRST constructions, including [Bennett et al., Theorem 3, v5](https://arxiv.org/html/0912.5537v5),
provide the relevant splitting machinery. Our immediate-output construction
runs exact collisions before encoding spent cells. It must additionally
control adaptive spectra and allocate actual flat stock, seed, work and
all residues in one closed bath; communication or net entanglement rates
alone do not count that allocation.

[Baghali Khanian and Leung, section II, Definition 3 and Theorems 6 and 8,
v1](https://arxiv.org/html/2504.07068v1) strengthen the reverse-Shannon
comparison by allowing a general mixed source/reference and preserved
encoder-side information, unifying feedback and non-feedback simulation.
Their input is a specified source tensor power, and the rates charge a
transmitted register and entanglement. Their assisted optimum and unassisted
bounds do not allocate all encoder/decoder environments inside one closed
sequential bath. Transferring that machinery to Definition 1.1 still requires
the adaptive compression, timing and complete storage accounting of Appendix A.

[Devetak and Yard, main region and Eqs. (1)--(2), v2](https://arxiv.org/pdf/quant-ph/0612050v2)
place FQSW in state redistribution: the resources are quantum communication
and net entanglement for many identical copies of a specified state with
accessible sender and receiver shares. Those resource rates do not by
themselves price the complete retained bath of Definition 1.1.

[Faist and Renner, Main Result and Eq. (2), v2](https://arxiv.org/pdf/1709.00506v2)
characterize a specified process on a specified input, preserving its
reference correlations, by coherent relative entropy with an information
battery and Gibbs-preserving free operations. This is a work resource
comparison; it does not impose our whole-bath dimension charge or one
device serving all adaptive testers.

[Faist, Berta and Brandao, Theorem 5.1 and Eq. (5.4), v3](https://arxiv.org/html/1911.05563v3)
give a universal parallel thermodynamic implementation with work rate
max_rho [S(rho)-S(Phi(rho))] for trivial Hamiltonians. Their battery and
free-operation accounting includes a partial-trace implementation, so it
does not charge the entire retained bath of Definition 1.1. The two models
are nevertheless comparable in one direction: Proposition 7.4 shows that our
entropy-deficit rate r-s is at least that work rate, for every channel. The mixed-bath
model of Terhal et al. already imposes the unitary column constraints;
its finite single-use environment analysis does not state this repeated rate
region. [Lie and Jeong, Theorems 1, 5--6, v2](https://arxiv.org/pdf/2010.14795v2)
study randomness-utilizing implementations with input-independent bath
output. That restriction is absent here, and their no-secret recovery acts
on a purifier that our device cannot access.

Quantum strategy memory in [Bisio et al., Definitions 3--4 and Theorem 3](https://arxiv.org/pdf/1112.3853v1)
permits free classical memory and local CPTP implementation; Definition 1.1
charges those physical resources.

[Lie and Jeong, Proposition 2, Corollary 10 and Theorem 11](https://arxiv.org/html/2104.00300v1#S3)
study implementations returning a catalyst for every input. Their entropy
bounds specialize to s>=h/2 and r+s>=h for a returned catalyst implementing
the tensor-power channel. Definition 1.1 imposes no such return; its region
also permits s=0 and r=h. Their catalytic block decomposition does not
identify every zero-gain collision: a SWAP with a maximally mixed bath has
g=0 but returns the input state to the bath. No reverse closure implication
is imported here.

[Kotowski and Kotowski](https://arxiv.org/abs/2606.08784) implement a unital
channel on a d-dimensional system with a fresh ancilla of dimension k and
success probability of order k/log d, shown optimal up to constants, and
simulate highly noncommutative channels with one auxiliary qubit. Their
protocol may fail with a flag and draws a fresh ancilla at every use;
Definition 1.1 removes both permissions, since the device must succeed at
every visit with one bath that is never replenished, so neither cost measure
bounds the other and nothing is imported.

Dimension and entropy need not have the same minimizer in quantum models
of classical stochastic processes, as shown by
[Loomis and Crutchfield](https://arxiv.org/abs/1808.08639) and
[Liu et al.](https://arxiv.org/abs/1810.09668). Those costs concern a stationary
information-bearing memory; here actual initial entropy is priced together
with the entire closed device. In the quantum-input setting,
[Chang, Berk and Gu, Theorem 3 and Appendix B.5](https://arxiv.org/html/2608.25878v1#S4)
bound stationary recurrent memory by temporal excess entropy. Their bound
vanishes for a memoryless channel, and their recurrent step may be an arbitrary
CPTP operation. Definition 1.1 instead counts the entire closed apparatus
needed to supply repeated calls. These comparisons explain the operational
content of the dimension--initial-entropy characterization. Known entropy,
minimax and decoupling ingredients do not by themselves supply the complete
closed implementation; combining them under this contract is what the paper
adds. None of the works cited above states a rate region for the closed
contract of Definition 1.1.

## 9. Conclusion and open questions

Under the closed contract a single-use dilation question becomes a rate region
in two resources, bath dimension per use and initial entropy per use, with h
fixing their sum and kappa fixing their difference. Three questions are left
open here. Computability: kappa is an ordered limit of an infimum over
extensions of unbounded dimension, and no algorithm, finite witness bound or
continuity in Phi is asserted; Proposition 7.4 gives only a lower bound that
is easy to evaluate, and Proposition 7.5 leaves a gap of a factor of about
three between that bound and the exhibited upper bound. Efficiency: the
all-horizon device of Theorem 5.1 is built from a witness that is not
constructed, and no circuit-size or latency claim is made; the streaming
realization for dephasing shows that some corners admit explicit efficient
devices, and which channels do is open. The contract: immediate output return,
one visit per input and a memoryless target are all load-bearing here. Devices
that deliver outputs on a schedule rather than immediately, and testers with
bounded persistent quantum memory rather than unrestricted references, are
separate questions that this paper does not address.

## AI assistance

AI systems assisted with proof exploration, manuscript preparation and checking.
Additional independent AI sessions audited the arguments and their relationship
to prior work. These sessions were not human external peer review. The scope
of the separate, partial Lean verification is stated in Appendix B.4.

## Appendices and bibliography

[Appendix A](appendix-causal-balancing.md) is the complete proof of
Theorem 5.1. [Appendix B](appendix-conventions.md) contains the normalization
and register tables, the finite verification scope, and the bibliography.
Together with sections 1--9 these are the complete paper.
