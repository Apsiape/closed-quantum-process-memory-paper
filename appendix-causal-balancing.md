# Appendix A. Complete causal balancing proof

This appendix proves Theorem 5.1 of the [manuscript](manuscript.md).
Fix the channel and one finite EXACT collision before any limit. Use sigma,v,g,h,a,b,R from
Theorem 5.1, with 0<=a<=sigma, g>=0 and b=a+g. All logs are base two and
D denotes half trace distance; in Lemma A.3 only, D denotes an integer
dimension and distances are written with an explicit norm.

## A.1. Adaptive spectral concentration

Lemma A.1. Let Lambda have finite output and H_Lambda=max_rho S(Lambda(rho)).
There is a fixed spectral projector on n successively produced, untouched
Lambda outputs with rank at most 2^[n(H_Lambda+gamma)] and rejected weight
at most exp(-c_Lambda n gamma^2), uniformly over adaptive controllers and
all finite reference dimensions. Deterministic spectral costs have zero loss.

Proof. Choose an entropy-maximizing output zeta. Its support contains every
output support: mixing an output with positive weight outside supp zeta into
zeta would increase entropy by a positive leading -t log t term. On the
common support the directional entropy derivative toward any output omega is
-Tr(omega-zeta)log zeta<=0. Thus

`Tr Lambda(rho)(-log zeta)<=S(zeta)=H_Lambda`.

Let z_j>0 be its eigenvalues and L_Lambda=max_j(-log z_j). Hypothetically
measure each spent output in this basis. Conditioned on earlier outcomes,
the next input is a density operator and its channel resource is fresh;
therefore X_i=-log z_(j_i) has conditional mean at most H_Lambda and lies
in [0,L_Lambda]. More explicitly, for a positive-probability hypothetical
history j_<i, let xi_(S_i K_i|j_<i) be the normalized conditional state just
before visit i, with K_i containing the controller and all its references.
Freshness makes the current dilation resource product with this joint state.
Writing rho_i(j_<i)=Tr_(K_i) xi_(S_i K_i|j_<i), one has

`Pr(j_i=j|j_<i)=<j|Lambda(rho_i(j_<i))|j>`,
`E[X_i|j_<i]=Tr Lambda(rho_i(j_<i))(-log zeta)<=H_Lambda`.

The conditional input may depend on the full history and be mixed because
of coherent entanglement; neither fact changes the channel-output formula.
Zero-probability histories may be omitted. These measurements are proof
devices, not information supplied to the controller. Conditional Hoeffding's
bound follows directly by iterating
E[exp(t(X_i-E[X_i|past]))|past]<=exp(t^2 L_Lambda^2/8), then minimizing
exp(-tn gamma+nt^2 L_Lambda^2/8) over t>=0. It gives

`Pr{sum X_i>n(H_Lambda+gamma)}<=exp(-2n gamma^2/L_Lambda^2)`.

Indeed E[exp(t(X_i-H_Lambda))|past]<=exp(t^2 L_Lambda^2/8)
for t>=0, which gives the iteration even when the conditional means vary.
Thus c_Lambda=2/L_Lambda^2 is independent of the tester; it need not be
uniform over different channels or witnesses with small positive eigenvalues.

This is conditional iteration of the bounded-variable exponential-moment
estimate underlying [Hoeffding's inequality](https://doi.org/10.1080/01621459.1963.10500830).
For completeness, the log moment-generating function of a variable in
[0,L] has second derivative equal to its variance in an exponentially tilted
law, at most L^2/4. Integrating twice from zero gives the centered bound
t^2 L^2/8, also for each conditional law. The application here selects one
spectral cost from the entropy-maximizing output, uniformly over controllers.

For L_Lambda=0 the event is empty. The hypothetical measurements commute
with subsequent service and controller operations up to the boundary just
before compression, because these operations do not touch spent outputs.
Thus the same probability is the rejected weight of the unmeasured state
at that boundary. No commutation with the later compressor or encoder is
asserted or needed. Every
accepted eigenstring has product zeta weight at least 2^[-n(H_Lambda+gamma)],
so there are at most 2^[n(H_Lambda+gamma)] such strings. This proves the
claim without iid inputs or a union bound over users.

For Lambda=Gamma_C, fresh tau cells therefore give a user-independent P_B
on the spent B^n cells with rank<=2^[n(v+gamma)] and loss_B<=exp(-c_B n gamma^2).
All physical basis changes and compressors depend only on this fixed witness,
n and gamma. The same lemma applies to untouched minimal environments of Phi.

For comparison, [Metger et al., Theorem 4.1 and Appendix A, v2](https://arxiv.org/html/2203.04989v2)
bound sequential smooth entropies. Their min-entropy theorem requires
Tr_(A_i R_i) M_i=R_i' Tr_(R_(i-1)); Appendix A Eq. (A.2) gives a
max-entropy form without that restriction. Such statewise bounds alone do
not specify one compression projector shared by every tester. Here the
fixed P_B preserves all complete adaptive tests in Definition 1.2 through
the trace-distance argument; A.2 additionally constructs simultaneous
support and spectral-cap cuts. We use the direct proof above, not an
entropy-accumulation citation to infer projector uniformity or seed freshness.

## A.2. The complete purified exterior

Lemma A.2. In an exact comparison block there are commuting proof projectors
on B^n,H,F^n whose success p is at least 1-loss_B-loss_E-loss_F, and whose
normalized pure projection obeys

`rank rho_hat_H<=K=2^[n(h+gamma)]`,
`||rho_hat_(B^n H)||_infinity<=2^[-n(sigma-gamma)]/p`.

Here H is a purification of the COMPLETE future-accessed exterior, excluding
the independent seed and current source. No rank bound on its raw mixed
marginal is asserted.

Proof. At a comparison boundary let E_raw contain the entire user and
references, all unused stock, and every other spectator that will be accessed
again. Exclude the seed Z, the n current source cells, and permanently parked
registers. The source tau^tensor n is independent of E_raw and Z jointly.
Purify E_raw to H=E_raw E' for analysis, and purify each source with F_i.
Dilate the tester's operations, retaining all its records in H. The final
B^n F^n H state is pure, and the F^n marginal stays tau_F^tensor n. The
device acts on neither F^n nor E'. These are comparison purifications, not
extra physical workspace or modifications of an actual inert purifier.

Run the same purified controller with fresh pure minimal dilations of Phi
instead. The resulting virtual state theta_(E^n H) is pure and its H
marginal equals the actual comparison H marginal: both provide exactly Phi
at every visit, including to reference-entangled inputs. Lemma A.1 gives a
virtual P_E of rank<=K and loss_E<=exp(-c_E n gamma^2). Define

`X_H=Tr_(E^n) [(P_E x I)|theta><theta|(P_E x I)]`.

Then 0<=X_H<=rho_H, since partial trace kills the cross terms between P_E
and I-P_E, and rank X_H<=rank P_E<=K. If P_H=supp X_H, then
Tr P_H rho_H>=Tr X_H>=1-loss_E. P_H may depend on the user and is only a
proof projector. An initially mixed spectator may have arbitrarily large
raw rank even when h=0; including E' before this argument is essential.

The positive eigenvalues of tau have finite logarithmic costs. The ordinary
lower-tail bound for independent source eigenstrings supplies P_F accepting
-log p_x>=n(sigma-gamma), with loss_F<=exp(-c_F n gamma^2), and

`P_F tau_F^tensor n P_F<=2^[-n(sigma-gamma)] P_F`.

Zero eigenvalues have zero probability and are omitted. Deterministic-cost
tails have zero loss. P_B, P_H and P_F act on distinct registers and commute;
the union bound gives the stated p. Crucially the virtual P_E is not applied
to the mixed-collision purification alongside a physical bath projector.

For every vector on F, the quadratic form of the F marginal after projecting
BH is at most its original value, because P_B P_H is a positive contraction.
Thus that unnormalized F marginal is <=tau_F^tensor n. After P_F and
normalization it is capped by 2^[-n(sigma-gamma)]/p. Purity transfers this
nonzero spectrum to B^n H. The normalized projected state has half distance
sqrt(1-p) from the original pure state. No independence of spectral events
is needed, and the factor 1/p cannot be suppressed.

## A.3. Second moment with a retained physical seed

Lemma A.3. Let C=M G, dim C=D, dim M=m, and rho_CH be normalized with
rank rho_H<=K and ||rho_CH||_infinity<=lambda. A uniform exact unitary
two-design V_z on C gives

`E_z ||Tr_G(V_z rho_CH V_z*)-pi_M x rho_H||_1<=sqrt(m^2 K lambda/D)`.

If an independent actual classical seed Z is retained, the half trace
distance of ZMH from pi_Z x pi_M x rho_H is at most half this expression.

Proof. For Delta_V=Tr_G(V rho_CH V*)-pi_M x rho_H, the two-copy Haar twirl
of Swap_M x I_(GG) equals alpha I+beta Swap_C. The untwirled operator has
trace D^2/m and trace against Swap_C equal to Dm; hence, for D>1,

`beta=D(m^2-1)/(m(D^2-1))<=m/D`, `alpha=1/m-beta/D`.

The swap trick and the cross term against pi_M x rho_H give exactly

`E Tr Delta_V^2=beta[Tr rho_CH^2-Tr rho_H^2/D]`.

Delta_V is supported on M x supp rho_H, of dimension at most mK.
Cauchy--Schwarz for its singular values, Jensen, and Tr rho_CH^2<=lambda
give the claimed trace-norm bound. If m=1, Delta_V=0 exactly, including D=1.
An exact two-design has these same second moments. This is the elementary
specialization underlying [Dupuis et al., Theorem 3.3 and Lemmas 3.4--3.5,
v3](https://arxiv.org/html/1012.6044v3); the factor 1/2 is explicit here.

For N qubits, the uniform Clifford group modulo global phases is such a
finite exact two-design, by [Dankert et al., Theorem 1, pp. 2--3,
v2](https://arxiv.org/pdf/quant-ph/0606161v2). Its size J_N has
log J_N<=2N(2N+1): each of 2N Pauli generators has at most 2^(2N+1)
signed images, and these images determine conjugation. For N=0 use J_0=1.
Initialize Z in pi_(J_N) offline and apply sum_z |z><z| x V_z. If Z is
independent of CH JOINTLY beforehand, the cq block trace-norm identity gives

`D(rho_ZMH,pi_Z x pi_M x rho_H)=(1/2)E_z ||Delta_(V_z)||_1`.

Keeping the random unitary choice in the output is also explicit in
[Dupuis et al., discussion after Corollary 3.2, v3](https://arxiv.org/html/1012.6044v3).
The additional accounting here charges this physical label and reuses it
across blocks through the joint comparison in Proposition A.5.

No one seed value is selected for all users. This is a guarantee for each
user on a physically retained mixed seed, with constants uniform over users.
The seed's inert purifier is not included in this reduced independence
claim; it is never accessed. Marginal independence of Z from C and from H
separately would not suffice.

## A.4. Exact integer wires and reversible preparation

Lemma A.4. Fix n>=1 and gamma>0. Define integer widths

`N=ceil[n(v+gamma)]`, `mi=ceil[n(sigma+2gamma)]`,
`mo=max(0,floor[n(sigma-a-6gamma)])`, `rp=ceil[3n gamma]+4`,
`c=mi-mo`, `d=N+rp-mi`, `z=c+d=N-mo+rp`,
`e=n ceil(log R)`, `w=max(0,e-N)`.

The full block can be implemented on permanent M,W of mo,w qubits and
one disjoint z-qubit tranche. The tranche starts with c mixed and d pure
qubits. Both preparation and encoding residues end in that tranche, which
is never accessed again. All dimensions in this statement are physical.

Proof. The typical-spectrum threshold is the usual source-coding ingredient;
see [Abeyesinghe et al., section VII and Appendix A, v1](https://arxiv.org/pdf/quant-ph/0606225v1).
Here the preparation is implemented as an injection of flat labels with
all its fibres retained on the counted wires below.
Zero-pad the R-dimensional cell to ceil(log R) qubits and extend U
unitarily outside its valid sector. From 0<=a<=sigma, g=v-sigma>=0 and
v<=log R, we have c,d>=0, mo<=mi, mo<=N, mi<=e+rp and z>=rp.
In particular d>=ng+2n gamma+3 and mi<=e+2n gamma+1<=e+rp.
Clipping mo changes its ideal leading term n(sigma-a) by at most
6n gamma+1. Consequently, uniformly over clipping,

`c=na+O(n gamma+1)`, `d=ng+O(n gamma+1)`, `z=nb+O(n gamma+1)`.

At opening, M and the fresh c mixed tranche qubits give exactly mi mixed
qubits, while all other local wires are pure. Their exact volume identity is

`mi+d+w=N+rp+w=e+rp+max(0,N-e)=mo+z+w`.                 (A.1)

In the eigenbasis of tau^tensor n, for strings with probabilities in
[2^(-n(sigma+gamma)),2^(-n(sigma-gamma))], assign floor(2^mi p_x) distinct
flat input labels to cell label x and different preparation-residue labels.
Each fibre uses at most 2^(3n gamma+1)<2^rp labels. There are at most
2^[n(sigma+gamma)] typical strings, so their total rounding deficit is
at most 2^[n(sigma+gamma)-mi]<=2^(-n gamma). The desired subdistribution
is pointwise below the target distribution. Send leftover labels injectively
to unused cell/residue pairs; mi<=e+rp guarantees capacity. Although these
labels can raise some marginal probabilities above target, total variation
is at most the missing subdistribution mass, giving

`delta_prep<=Pr{source atypical}+2^(-n gamma)`.

The two-sided source tail is <=2 exp(-c_tau n gamma^2), with deterministic
costs treated exactly. The injection of an orthonormal input set extends to
a unitary on the full local space in (A.1); any max(0,N-e) padding stays
pure. The complete local positive spectrum remains exactly 2^mi copies of
2^(-mi). Only its cell marginal is approximately nonflat.

Route the rp preparation-residue positions into the current tranche and
never touch them again. In the comparison run replace only the cell marginal
by tau^tensor n; all future-accessed exterior registers remain independent.
The preparation error is charged once for the entire block by contractivity,
even with adaptive service. This is a comparison of reduced states, not a
physical erasure or operation on the purifying systems.

Run each exact collision when its input arrives. At an interior visit,
hand back its output after that collision. At the final visit of a block,
perform the collision, then the bath-only closing gates described below,
and then release that visit's output, all before the next input arrives.
Bath-only unitaries preserve the joint reduced state of every user output
and reference, including the current output. On e cell positions and
max(0,N-e) padding, a
fixed unitary compresses supp P_B into N qubits C and w pure qubits W.
The rank bound in A.1 guarantees this embedding; complete its remaining
columns orthonormally. No projection is performed or success flag measured.
Split C into M of mo qubits and G of N-mo qubits, use Lemma A.3's controlled
encoder, and route M,W to their permanent positions. Park G beside the
preparation residue in the same tranche. The equality

`z=rp+(N-mo)`                                             (A.2)

proves that neither residue overlaps the other or any future stock. The
compression failure part remains coherently present on these same wires.

## A.5. Joint recycling, every prefix and the repeated unitary

Proposition A.5. The block above has a user-independent reduced-state error
epsilon_n<=A[exp(-c_0 n gamma^2)+2^(-c_1 n gamma)] for large n gamma^2,
returning M,W and the seed jointly independent of the entire future-accessed
exterior in the comparison state. Constants depend only on the fixed collision.

Proof. Apply Lemma A.2 to the exact comparison block. After compression its
projected W is pure and its normalized CH state has rank bound K and cap
lambda=2^[-n(sigma-gamma)]/p. Before encoding the seed is independent of
CH jointly: preparation and service have not touched it, and the proof cuts
can be chosen without referring to it. In particular the comparison input
is pi_Z tensor rho_(source,exterior), with source and exterior also in
product. Its purification and P_H may depend on the tester but not on Z;
P_B depends only on the fixed collision. Applying these proof cuts therefore
preserves the product with pi_Z. This is the joint hypothesis of Lemma A.3,
including all unused stock and future-accessed spectators in the exterior.
For mo>0,

`2mo+n(h+gamma)-n(sigma-gamma)-N<=-11n gamma`,

since sigma-2a+h-v=0. Lemma A.3 therefore bounds the projected joint
half distance by 2^(-11n gamma/2)/(2 sqrt p). For mo=0 it is zero.
Add sqrt(1-p) for smoothing the initial pure comparison, and another for
replacing its projected H marginal by its original H marginal. W is pure
on the projected branch, so it is included jointly in the same estimate.
Tracing the mathematical E' then gives the bound on the physical exterior.
Including preparation once yields

`epsilon_n<=delta_prep+2 sqrt(loss_B+loss_E+loss_F)`
`             +2^(-11n gamma/2)/(2 sqrt p)`                (A.3)

when mo>0; omit the last term otherwise. With p>=1/2 the asserted bound
follows, absorbing square roots into fixed positive constants.

For L full blocks the boundary comparison is

`rho_(user,ideal) x pi_Z x pi_M x |0><0|_W`
`     x (all unused mixed/pure tranches) x (pure tail cells)`.  (A.4)

Old tranches are omitted only from this trace-distance metric; their full
dimensions remain allocated. Initially the actual reduced state is (A.4),
so e_0=0. Fix any adaptive tester, apply the SAME next-block CPTP map to its
actual state and (A.4), and contract their distance. The uniform local bound
then gives e_(j+1)<=e_j+epsilon_n. Thus actual learning of the seed and
correlations with recycled M are charged to e_j. Freshness is used only in
the comparison run, where the next source and seed are jointly independent
of the complete exterior. There is no assumption about independence of errors.

At a prefix inside a block before its closing encoder, the user error is
<=e_j+delta_prep. The closing bath-only gates can be performed after the last
collision and before handing back that visit's output, preserving immediate
service. Fewer than n tail visits use preallocated pure minimal-Stinespring
cells, exactly implementing Phi; these are part of the initial bath. Thus
the entire horizon and every prefix obey the conservative bound
delta_T<=L epsilon_n+delta_prep. When the final segment consists only of pure
tail cells, no extra preparation term is needed. Stopping is handled by
extending a stopped tester with dummy inputs while keeping its records and
stop flag, then tracing the continuation. This is unconditional; no rare-event
postselection estimate follows.

All opening, collision, closing and routing steps for visit t form a fixed
unitary V_t on the system and allocated non-clock bath. A pure counted
(T+1)-dimensional clock implements the SAME unitary each visit:

`W_T=sum_(t=0)^T |t+1 mod (T+1)><t|_clock x V_t`.          (A.5)

Choose the unused V_T arbitrarily unitary. Orthogonality of clock sectors
and unitarity of each V_t prove W_T is unitary. Starting at 0, the first T
visits do not wrap. All control resides in this fixed hardware. There is no
bound on gate count or latency, but the next input never arrives before the
previous output is handed back.

## A.6. Actual spectrum and the every-horizon limit

Proposition A.6. The construction has the exact initialization and separate
limits asserted in Theorem 5.1.

Proof. Set L=floor(T/n) and
t_tail=(T-Ln)ceil(log k), where k=rank J_Phi is the minimal environment
dimension. Zero-padding each pure tail cell and unitary completion are counted.
The exact numbers of allocated data qubits and initially mixed data qubits are

`A_T=mo+w+Lz+t_tail`, `K_T=Lc+mo`.                        (A.6)

Since d>=0, K_T<=A_T. With the clock and the one reused seed,

`R_T=(T+1)J_N 2^A_T`,
`omega_T=|0><0|_clock x pi_(J_N) x pi_(2^K_T) x |0><0|_rest`,
`P_T=J_N 2^K_T`, `S(omega_T)=log J_N+K_T`.                (A.7)

Its positive eigenvalues are exactly 1/P_T repeated P_T times, with
R_T-P_T zeros. Its minimal inert purifier has dimension P_T and is never
accessed. The witness entropy sigma is an intermediate preparation parameter;
it is not substituted for the actual entropy in (A.7).

For every sufficiently large integer T take n=floor(T^(1/3)) and
gamma=n^(-1/4). Fixed-witness constants have already been chosen. Then
n gamma^2=sqrt n, so the exponential in (A.3) beats the polynomial number
L of blocks; the other exponent is of order n^(3/4). Thus

`L epsilon_n+delta_prep->0`, `A_T/T->b`, `K_T/T->a`,
`log J_N/T=O_C(n^2/T)->0`,
`(mo+w+t_tail)/T=O_C(n/T)->0`, `log(T+1)/T->0`.

Slack costs O(T gamma), rounding costs O(T/n), and the seed O_C(n^2)
bits; all are sublinear. Finitely many smaller horizons use preallocated
exact pure cells and a counted clock. Consequently for every fixed witness
and every tolerance there is a finite threshold after which EVERY horizon
has small error and small rate discrepancies, including the separate seed
and mixed-data limits. No effective or witness-uniform threshold is asserted.

The same integers handle mo=0, g=0, a=0, R=1 and N>e. For example pure
tau forces sigma=a=0; its mixed slack consumption is o(T). An identity
collision with an arbitrary mixed spectator has g=h=a=b=0 and its startup
stock is O_C(n). These checks use no negative register widths.

The argument uses encoder-only FQSW, with its would-be message parked and
counted; see manuscript section 5 for attribution. All original proof steps
needed beyond that ingredient have been supplied above. This concludes
the proof of Theorem 5.1.
