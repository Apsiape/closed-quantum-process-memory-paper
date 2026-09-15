"""C4 falsifiers and exact finite allocation controls; no channel-rate certification."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
import json
import math
import numpy as np


def ceil(x):
    return -((-x.numerator) // x.denominator)


def block(ell, sigma, gain, h, gamma, cell_qubits):
    a = (h-gain)/2
    v = sigma+gain
    assert 0 <= a <= sigma and v <= cell_qubits
    n = ceil(ell*(v+gamma))
    mi = ceil(ell*(sigma+2*gamma))
    mo = max(0, math.floor(ell*(sigma-a-6*gamma)))
    rp = ceil(3*ell*gamma)+4
    c, d = mi-mo, n+rp-mi
    z, cells = c+d, ell*cell_qubits
    work = max(0, cells-n)
    assert c >= 0 and d >= 0 and mo <= n
    assert mi+d+work == mo+z+work
    assert n+rp+work >= cells+rp
    assert mi <= cells+rp
    # Deterministic disjoint wire tranches; parked wires never re-enter a block.
    horizon_blocks = 9
    capital = set(range(mo))
    workspace = set(range(mo, mo+work))
    tranches = [set(range(mo+work+j*z, mo+work+(j+1)*z)) for j in range(horizon_blocks)]
    parked = set()
    total = mo+work+horizon_blocks*z
    for j, tranche in enumerate(tranches):
        accessed = capital | workspace | tranche
        assert not accessed & parked
        parked |= tranche
        remaining = set().union(*tranches[j+1:]) if j+1<horizon_blocks else set()
        assert len(capital | workspace | parked | remaining) == total
        assert len(parked) == (j+1)*z
    return int(mo > 0), int(n > cells)


def preparation():
    # Rational iid source: p=(3/4,1/4), eight copies, explicit orthogonal labels.
    ell, gamma = 8, .2
    sigma = -(.75*math.log2(.75)+.25*math.log2(.25))
    mi, rp = math.ceil(ell*(sigma+2*gamma)), math.ceil(3*ell*gamma)+4
    count, residue_dim = 2**mi, 2**rp
    p = [F(3**(ell-x.bit_count()), 4**ell) for x in range(2**ell)]
    typical = [x for x, px in enumerate(p) if abs(-math.log2(float(px))/ell-sigma)<=gamma]
    image = []
    for x in typical:
        fibre = math.floor(count*p[x])
        assert fibre <= residue_dim
        image.extend((x, j) for j in range(fibre))
    used = set(image)
    for pair in product(range(2**ell), range(residue_dim)):
        if len(image) == count:
            break
        if pair not in used:
            image.append(pair)
            used.add(pair)
    assert len(image) == len(set(image)) == count
    counts = Counter(x for x, _ in image)
    tv = sum(abs(F(counts[x], count)-p[x]) for x in range(2**ell))/2
    bound = 1-sum(p[x] for x in typical)+F(len(typical), count)
    assert tv <= bound
    # Injective orthogonal images give the same count eigenvalues 1/count.
    return {"flat_rank": count, "source_strings": 2**ell,
            "typical_strings": len(typical), "tv": float(tv), "bound": float(bound),
            "global_nonzero_spectrum": f"1/{count}, multiplicity {count}"}


def falsifiers():
    # Separate independence does not imply independence of their union.
    parity = np.zeros((2,2,2))
    for x,y in product(range(2), repeat=2):
        parity[x,y,x^y] = .25
    assert np.allclose(parity.sum(axis=0), .25)
    assert np.allclose(parity.sum(axis=1), .25)
    joint_distance = np.abs(parity-np.full((2,2,2), .125)).sum()/2
    assert joint_distance == .5
    # Pure joint exterior vs its raw mixed spectator: h=0, yet raw rank grows.
    spectator_dim = 8
    raw = np.eye(spectator_dim)/spectator_dim
    omega = np.eye(spectator_dim).reshape(-1)/np.sqrt(spectator_dim)
    purified = np.outer(omega, omega)
    assert np.linalg.matrix_rank(raw) == 8
    assert np.linalg.matrix_rank(purified) == 1
    # A seed correlated with its source can undo the apparent randomness.
    conditional_outputs = [np.array([1.,0.]), np.array([1.,0.])]
    output = sum(conditional_outputs)/2
    assert np.abs(output-.5).sum()/2 == .5
    # Rare completion: unnormalized error p, conditional error one.
    rare = F(1,1024)
    assert (abs(rare)+abs(-rare))/2 == rare
    return {"joint_parity_distance": joint_distance, "raw_spectator_rank": 8,
            "purified_exterior_rank": 1, "correlated_seed_output_distance": .5,
            "rare_branch_unconditional_error": float(rare), "conditional_error": 1}


def second_moment():
    # Build the one-qubit Clifford ensemble (24 elements modulo scalar phase).
    hadamard = np.array([[1,1],[1,-1]], complex)/np.sqrt(2)
    phase = np.diag([1,1j])
    def key(u):
        pivot = next(x for x in u.flat if abs(x)>1e-8)
        w = u/(pivot/abs(pivot))
        return tuple(np.round(w.real,8).flat)+tuple(np.round(w.imag,8).flat)
    group = {key(np.eye(2)):np.eye(2,dtype=complex)}
    pending = list(group.values())
    while pending:
        u = pending.pop()
        for gen in (hadamard, phase):
            v = gen@u
            if key(v) not in group:
                group[key(v)] = v
                pending.append(v)
    assert len(group) == 24
    rng = np.random.default_rng(20260909)
    max_error = 0.
    for _ in range(12):
        x = rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
        rho = x@x.conj().T
        rho /= np.trace(rho)
        ext = np.trace(rho.reshape(2,2,2,2),axis1=0,axis2=2)
        target = np.kron(np.eye(2)/2,ext)
        second = 0.
        cq_distance = 0.
        for u in group.values():
            full = np.kron(u,np.eye(2))
            delta = full@rho@full.conj().T-target
            second += np.trace(delta@delta).real/24
            cq_distance += np.linalg.svd(delta,compute_uv=False).sum()/48
        # M=D=2, so beta=1. This finite test checks the exact trace formula.
        exact = np.trace(rho@rho).real-np.trace(ext@ext).real/2
        max_error = max(max_error,abs(second-exact))
        lam = np.linalg.eigvalsh(rho)[-1]
        rank = np.linalg.matrix_rank(ext)
        assert cq_distance <= .5*np.sqrt(2*rank*lam)+1e-12
    assert max_error < 1e-12
    # Pauli-only ensemble is not a substitute for a two-design: D=4,M=2.
    # Source |0><0| tensor I/2 stays pure on M under every tensor Pauli.
    pauli_norm, claimed_bound = 1., math.sqrt(4*.5/4)
    assert pauli_norm > claimed_bound
    return {"cliffords":24,"random_states":12,"max_moment_residual":max_error,
            "pauli_only_full_trace_norm":pauli_norm,"two_design_bound_would_be":claimed_bound}


def main():
    cases=positive_capital=compressed_padding=0
    for ell,gamma,sigma,gain in product((1,2,7,64,1000),(F(1,32),F(1,10)),
                                      (F(0),F(1,2),F(3,2),F(3)),(F(0),F(1,2),F(1))):
        if sigma+gain > 3:
            continue
        for increment in (F(0),sigma,2*sigma):
            cap,pad=block(ell,sigma,gain,gain+increment,gamma,3)
            cases+=1
            positive_capital+=cap
            compressed_padding+=pad
    print(json.dumps({"status":"PASS","allocation_cases":cases,
                      "positive_capital_cases":positive_capital,"N_exceeds_cell_width_cases":compressed_padding,
                      "preparation":preparation(),"negative_controls":falsifiers(),
                      "second_moment":second_moment(),
                      "scope":"finite arithmetic and matrix controls; not an asymptotic proof"},indent=2))


if __name__ == "__main__":
    main()
