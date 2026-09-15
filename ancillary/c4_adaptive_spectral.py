"""Finite C4 adaptive spectral/support controls, not an asymptotic certificate.

Seed 20260909; tolerance 1e-8; q=R=2, n=3, four user qubits.
The virtual complement test uses a cross-entropy upper budget, NOT a numerical
claim to have found h. All pure vectors have dimension 1024 (well below 2 GiB).
"""
from itertools import product
import json
import numpy as np

RNG = np.random.default_rng(20260909)
TOL = 1e-8
DIMS = [2] * 10  # S1,S2,S3,Q,B1,F1,B2,F2,B3,F3
BS, FS, HS = [4, 6, 8], [5, 7, 9], [0, 1, 2, 3]
TAU = np.diag([.8, .2])
SWAP = np.eye(4)[[0, 2, 1, 3]]
U = np.sqrt(.75) * np.eye(4) + .5j * SWAP
OMEGA = np.array([np.sqrt(.8), 0, 0, np.sqrt(.2)])


def apply(vec, axes, op):
    rest = [j for j in range(len(DIMS)) if j not in axes]
    order = axes + rest
    mat = vec.reshape(DIMS).transpose(order).reshape(2**len(axes), -1)
    return (op @ mat).reshape([2]*10).transpose(np.argsort(order)).reshape(-1)


def reduced(vec, axes):
    rest = [j for j in range(len(DIMS)) if j not in axes]
    mat = vec.reshape(DIMS).transpose(axes+rest).reshape(2**len(axes), -1)
    return mat @ mat.conj().T


def haar(d):
    mat = RNG.normal(size=(d, d)) + 1j*RNG.normal(size=(d, d))
    q, r = np.linalg.qr(mat)
    return q @ np.diag(np.diag(r)/np.abs(np.diag(r)))


def channel(rho, mode):
    out = U @ np.kron(rho, TAU) @ U.conj().T
    if mode == "bath":
        return np.einsum("abad->bd", out.reshape(2, 2, 2, 2))
    # Isometry S -> S B F for the fixed purification of tau.
    iso = np.zeros((8, 2), complex)
    for s, a, b, f in product(range(2), repeat=4):
        iso[4*a+2*b+f, s] = U[2*a+b, 2*s+f]*np.sqrt(TAU[f, f])
    out = (iso @ rho @ iso.conj().T).reshape(2, 4, 2, 4)
    return np.einsum("abad->bd", out)


def spec(mode):
    zeta = np.diag([.6, .4]) if mode == "bath" else channel(np.eye(2)/2, mode)
    vals, basis = np.linalg.eigh(zeta)
    assert min(vals) > 0
    costs = -np.log2(vals)
    observable = (basis * costs) @ basis.conj().T
    # The adjoint observable's largest eigenvalue bounds every conditional mean.
    adj = np.empty((2, 2), complex)
    for i, j in product(range(2), repeat=2):
        e = np.zeros((2, 2), complex)
        e[j, i] = 1
        adj[i, j] = np.trace(channel(e, mode) @ observable)
    budget = np.linalg.eigvalsh(adj)[-1]
    if mode == "bath":
        assert abs(budget + np.sum(np.diag(zeta)*np.log2(np.diag(zeta)))) < TOL
    return basis, costs, budget


def tensor_power(mat, n=3):
    out = np.array([[1.]])
    for _ in range(n):
        out = np.kron(out, mat)
    return out


def control():
    worst = 0.
    nodes, cases, nonproduct = 0, 0, 0
    joint_success = []
    for case in range(4):
        user = haar(16)[:, 0]
        initial = np.kron(np.kron(np.kron(user, OMEGA), OMEGA), OMEGA)
        feedback = [haar(8), haar(8)]
        final = initial.copy()
        for i in range(3):
            final = apply(final, [i, BS[i]], U)
            if i < 2:
                final = apply(final, [i, i+1, 3], feedback[i])
        rho_h = reduced(final, HS)
        virtual = None
        for mode in ["bath", "complement"]:
            basis, costs, budget = spec(mode)
            measured = [[BS[i]] if mode == "bath" else [BS[i], FS[i]] for i in range(3)]
            branches = {(): initial}
            for i in range(3):
                nxt = {}
                for history, vec in branches.items():
                    weight = np.vdot(vec, vec).real
                    if weight < 1e-15:
                        continue
                    input_state = reduced(vec, [i])/weight
                    collided = apply(vec, [i, BS[i]], U)
                    actual = reduced(collided, measured[i])/weight
                    residual = np.linalg.norm(actual-channel(input_state, mode))
                    worst = max(worst, residual)
                    assert residual < TOL
                    mean = np.sum(costs * np.diag(basis.conj().T @ actual @ basis).real)
                    assert mean <= budget + TOL
                    nodes += 1
                    for outcome in range(len(costs)):
                        ket = basis[:, outcome]
                        child = apply(collided, measured[i], np.outer(ket, ket.conj()))
                        if i < 2:
                            child = apply(child, [i, i+1, 3], feedback[i])
                        nxt[history+(outcome,)] = child
                branches = nxt
            axes = sum(measured, [])
            allbasis = tensor_power(basis)
            deferred = np.diag(allbasis.conj().T @ reduced(final, axes) @ allbasis).real
            sequential = np.array([np.vdot(branches[x], branches[x]).real
                                   for x in product(range(len(costs)), repeat=3)])
            worst = max(worst, np.max(np.abs(deferred-sequential)))
            assert np.max(np.abs(deferred-sequential)) < TOL
            dist = sequential.reshape([len(costs)]*3)
            marg = [dist.sum(axis=tuple(k for k in range(3) if k != j)) for j in range(3)]
            iid = np.einsum("i,j,k->ijk", *marg)
            nonproduct += int(np.linalg.norm(dist-iid) > 1e-5)
            total_cost = np.array([sum(costs[list(x)]) for x in product(range(len(costs)), repeat=3)])
            if mode == "bath":
                selected = total_cost <= 3*(budget+.02)
                pb = (allbasis * selected) @ allbasis.conj().T
                assert sum(selected) <= 2**(3*(budget+.02)) + TOL
            else:
                # Deliberately severe finite spectral cutoff; no tail claim.
                selected = np.zeros(64, bool)
                selected[np.argsort(total_cost)[:8]] = True
                pe = (allbasis * selected) @ allbasis.conj().T
                virtual = apply(final, axes, pe)
            cases += 1
        sub_h = reduced(virtual, HS)
        ev, eigvec = np.linalg.eigh(sub_h)
        support = ev > 1e-11
        assert sum(support) <= 8
        ph = (eigvec*support) @ eigvec.conj().T
        assert np.linalg.eigvalsh(rho_h-sub_h)[0] >= -TOL
        assert np.trace(ph@rho_h).real + TOL >= np.trace(sub_h).real
        sigma = -np.sum(np.diag(TAU)*np.log2(np.diag(TAU)))
        p_f = np.diag(tensor_power(TAU))
        pf = np.diag(-np.log2(p_f) >= 3*(sigma-.1))
        projected = apply(apply(apply(final, BS, pb), HS, ph), FS, pf)
        p = np.vdot(projected, projected).real
        assert p > 1e-8
        losses = sum(1-np.trace(proj@reduced(final, axes)).real
                     for proj, axes in [(pb, BS), (ph, HS), (pf, FS)])
        assert p + TOL >= 1-losses
        unnormalized_f = reduced(projected, FS)
        cap_matrix = pf @ tensor_power(TAU) @ pf
        assert np.linalg.eigvalsh(cap_matrix-unnormalized_f)[0] >= -TOL
        cap = 2**(-3*(sigma-.1))/p
        assert np.linalg.eigvalsh(unnormalized_f/p)[-1] <= cap+TOL
        normed = projected/np.sqrt(p)
        assert abs(abs(np.vdot(final, normed))**2-p) < TOL
        # Purity transfers the cap to B^n H; use a Schmidt matrix, not a huge density.
        order = FS+BS+HS
        mat = normed.reshape(DIMS).transpose(order).reshape(8, -1)
        assert abs(np.linalg.svd(mat, compute_uv=False)[0]**2
                   - np.linalg.eigvalsh(unnormalized_f/p)[-1]) < TOL
        joint_success.append(float(p))
    assert nonproduct == cases
    print(json.dumps({"seed": 20260909, "tolerance": TOL, "cases": cases,
                      "conditional_nodes": nodes, "nonproduct_distributions": nonproduct,
                      "max_residual": float(worst), "joint_projection_probabilities": joint_success,
                      "max_vector_dimension": 1024,
                      "scope": "finite adaptive and operator-support identities only"}, indent=2))


if __name__ == "__main__":
    control()
