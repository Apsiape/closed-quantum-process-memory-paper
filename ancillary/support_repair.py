"""Independent finite reconstruction of C3 / RETURN-131 sections 1--2.

NumPy floating-point diagnostics, not a universal proof or diamond-norm test.
Tensor basis: system first, bath second; Choi vec uses system row then input.
"""
import json
import numpy as np

TOL = 1e-8
RNG = np.random.default_rng(20260908)


def norm(a):
    return float(np.linalg.norm(a, 2))


def adj(a):
    return a.conj().T


def positive_sqrt(a):
    vals, vecs = np.linalg.eigh((a + adj(a)) / 2)
    assert vals.min() > -TOL
    return (vecs * np.sqrt(np.maximum(vals, 0))) @ adj(vecs)


def complete_columns(j, positions, size):
    # The prescribed columns are an isometry; SVD supplies its orthocomplement.
    u, _, _ = np.linalg.svd(j, full_matrices=True)
    out = np.zeros((size, size), complex)
    out[:, positions] = j
    other = [x for x in range(size) if x not in positions]
    out[:, other] = u[:, j.shape[1]:]
    assert norm(adj(out) @ out - np.eye(size)) < TOL
    return out


def case(kraus, bath_dim, perturbation):
    q, k, r = kraus[0].shape[0], len(kraus), bath_dim
    # Target collision on bath input |0>; all other columns completed unitarily.
    target_j = sum(np.kron(a, np.eye(r)[:, i:i+1]) for i, a in enumerate(kraus))
    u = complete_columns(target_j, [s*r for s in range(q)], q*r)
    x = RNG.normal(size=(q*r, q*r)) + 1j*RNG.normal(size=(q*r, q*r))
    h = x + adj(x)
    eig, vec = np.linalg.eigh(h)
    u = (vec * np.exp(1j*perturbation*eig)) @ adj(vec) @ u

    basis = np.stack([a.reshape(-1) for a in kraus], axis=1)
    projector = basis @ np.linalg.pinv(basis)
    blocks = u.reshape(q, r, q, r).transpose(0, 2, 1, 3).reshape(q*q, r*r)
    projected = (projector @ blocks).reshape(q, q, r, r).transpose(0, 2, 1, 3).reshape(q*r, q*r)
    leakage = u - projected
    e = np.trace((adj(leakage) @ leakage).reshape(q, r, q, r), axis1=0, axis2=2)
    ev, eb = np.linalg.eigh(e)
    # Deliberately exercise both sectors, not only an identity/empty cutoff.
    cutoff = 0.002
    assert ev[0] < cutoff < ev[-1]
    good = eb[:, ev <= cutoff]
    bad = eb[:, ev > cutoff]
    d0 = good.shape[1]
    p, qb = good @ adj(good), bad @ adj(bad)
    eps = np.sqrt(q*cutoff)
    assert 0 < eps <= 1
    vp = projected @ np.kron(np.eye(q), good)
    delta = adj(vp) @ vp - np.eye(q*d0)

    # Gram map L(E_ab)=A_a^* A_b and a full-space extension of its right inverse.
    lm = np.stack([(adj(a) @ b).reshape(-1) for a in kraus for b in kraus], axis=1)
    rm = np.linalg.pinv(lm)
    cb = max(1.0, sum(norm(rm[:, i].reshape(k, k)) for i in range(q*q)))
    # Bound follows by summing coefficient/block norms; independent of d0.
    db = delta.reshape(q, d0, q, d0).transpose(0, 2, 1, 3).reshape(q*q, d0*d0)
    rd = (rm @ db).reshape(k, k, d0, d0).transpose(0, 2, 1, 3).reshape(k*d0, k*d0)
    inverse_residual = norm(lm @ rm @ db - db)
    t = cb*(2*eps + eps*eps)
    gram = (t*np.eye(k*d0) - rd)/(1+t)
    gs = positive_sqrt(gram)
    cs = [gs[:, a*d0:(a+1)*d0] for a in range(k)]
    w = sum(np.kron(a, c) for a, c in zip(kraus, cs))
    # Good output sectors B and C^k tensor PB; bad sector C^k tensor QB.
    # Embed the latter two into one C^k tensor B without measuring the cutoff.
    good_extra = np.kron(np.eye(q), np.kron(np.eye(k), good)) @ w
    top = projected @ np.kron(np.eye(q), p) / np.sqrt(1+t)
    bottom = good_extra @ np.kron(np.eye(q), adj(good))
    for aidx, a in enumerate(kraus):
        flag = np.eye(k)[:, aidx:aidx+1]
        bottom += np.kron(a, np.kron(flag, qb))
    # Stack bath sectors within each system row, not outside the system tensor.
    repaired = np.concatenate([top.reshape(q, r, q*r), bottom.reshape(q, k*r, q*r)], axis=1).reshape(q*(k+1)*r, q*r)
    rb = repaired.reshape(q, (k+1)*r, q, r).transpose(0, 2, 1, 3).reshape(q*q, (k+1)*r*r)

    # Noncommuting initialization: almost pure with a small coherent rotation.
    init = np.zeros(r, complex)
    init[0], init[1] = np.cos(0.01), np.sin(0.01)
    tau = (1-1e-7)*np.outer(init, init.conj()) + 1e-7*np.eye(r)/r
    padded = np.zeros(((k+1)*r, (k+1)*r), complex)
    padded[:r, :r] = tau
    commutator = norm(tau @ p - p @ tau)
    weight_bad = float(np.trace(tau @ qb).real)
    leak_weight = float(np.trace(tau @ e).real/q)
    old = np.zeros_like(repaired).reshape(q, (k+1)*r, q*r)
    old[:, :r, :] = u.reshape(q, r, q*r)
    old = old.reshape(repaired.shape)
    # Hilbert-Schmidt purification distance for maximally mixed system probe.
    initial_sqrt = np.kron(np.eye(q)/np.sqrt(q), positive_sqrt(tau))
    vector_distance = float(np.linalg.norm((repaired-old) @ initial_sqrt))
    aeps = eps + t/2 + np.sqrt((t + 2*eps + eps*eps)/(1+t))
    bound = aeps + 2*np.sqrt(weight_bad)
    checks = {
        "isometry": norm(adj(repaired) @ repaired - np.eye(q*r)),
        "kraus_support": norm((np.eye(q*q)-projector) @ rb),
        "right_inverse": inverse_residual,
        "gram_hermiticity": norm(gram-adj(gram)),
        "spectrum": float(np.max(np.abs(np.linalg.eigvalsh(padded)[-r:] - np.linalg.eigvalsh(tau)))),
    }
    assert max(checks.values()) < TOL, checks
    assert norm(leakage @ np.kron(np.eye(q), p)) <= eps + TOL
    assert weight_bad <= q*leak_weight/cutoff + TOL
    assert vector_distance <= bound + TOL
    assert commutator > 1e-6, "Test did not exercise noncommuting tau/P"
    # Complete the full repair to an active-only unitary; purifier not used.
    positions = [s*(k+1)*r+b for s in range(q) for b in range(r)]
    complete_columns(repaired, positions, q*(k+1)*r)
    return {"R": r, "perturbation": perturbation, "good_rank": d0,
            "bad_rank": r-d0, "commutator": commutator,
            "cutoff_epsilon": float(eps), "weighted_leakage": leak_weight,
            "purified_probe_distance": vector_distance,
            "distance_bound": bound, "residuals": checks}


def main():
    gamma = 0.36
    families = {
        "amplitude_damping": [np.diag([1., np.sqrt(1-gamma)]), np.array([[0., np.sqrt(gamma)], [0., 0.]])],
        "dephasing": [np.diag([1., 0.]), np.diag([0., 1.])],
    }
    results = []
    for name, family in families.items():
        for r in (2, 3, 4):
            for perturbation in (1e-5, 1e-3):
                results.append({"family": name, **case(family, r, perturbation)})
    print(json.dumps({"status": "PASS", "finite_cases": len(results),
                      "seed": 20260908, "tolerance": TOL, "numpy": np.__version__,
                      "maximum_identity_residual": max(max(x["residuals"].values()) for x in results),
                      "minimum_cutoff_commutator": min(x["commutator"] for x in results),
                      "scope": "finite matrix reconstruction only; no diamond or asymptotic certification",
                      "cases": results}, indent=2))


if __name__ == "__main__":
    main()
