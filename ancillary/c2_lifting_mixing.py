"""Finite C2 controls, not a minimax/limit proof.

Seed 20260908; q=2,3; bath R=2,3,4; tolerance 1e-8.
Checks purification lifting, actual mixed spectrum and flagged gain functions.
Largest density matrix in these controls has dimension 36.
"""
import json
import numpy as np

RNG = np.random.default_rng(20260908)
TOL = 1e-8


def adj(x):
    return x.conj().T


def unitary(n):
    z = RNG.normal(size=(n, n)) + 1j * RNG.normal(size=(n, n))
    u, r = np.linalg.qr(z)
    return u @ np.diag(np.diag(r) / np.abs(np.diag(r)))


def entropy(x):
    ev = np.linalg.eigvalsh((x + adj(x)) / 2)
    assert ev.min() >= -TOL
    ev = ev[ev > 1e-13]
    return float(-np.sum(ev * np.log2(ev)))


def reduced(vector, dims, keep):
    other = [i for i in range(len(dims)) if i not in keep]
    x = vector.reshape(dims).transpose(list(keep) + other)
    x = x.reshape(int(np.prod([dims[i] for i in keep])), -1)
    return x @ adj(x)


def collision_outputs(u, tau, rho):
    q, r = len(rho), len(tau)
    out = (u @ np.kron(rho, tau) @ adj(u)).reshape(q, r, q, r)
    return np.trace(out, axis1=1, axis2=3), np.trace(out, axis1=0, axis2=2)


def block_diag(arrays):
    result = np.zeros((sum(len(a) for a in arrays),) * 2, complex)
    start = 0
    for a in arrays:
        result[start:start+len(a), start:start+len(a)] = a
        start += len(a)
    return result


def flagged(us, taus, weights, q):
    rs = [len(t) for t in taus]
    total = sum(rs)
    u = np.zeros((q * total, q * total), complex)
    start = 0
    for uj, r in zip(us, rs):
        indices = [a * total + start + b for a in range(q) for b in range(r)]
        u[np.ix_(indices, indices)] = uj
        start += r
    tau = block_diag([p * t for p, t in zip(weights, taus)])
    return u, tau


def lifting(q, r, rank, small):
    # Use Schmidt coordinates on Q. S has an independently rotated basis.
    lam = np.full(q, (1-small)/(q-1))
    lam[-1] = small
    v = unitary(q)
    rho = (v * lam) @ adj(v)
    weights = RNG.uniform(0.2, 1.0, rank)
    weights /= weights.sum()
    tau = np.diag(np.r_[weights, np.zeros(r-rank)])
    u = unitary(q*r)
    # xi has order Q,A,B,Z; Z is never operated on.
    xi = np.zeros((q, q, r, rank), complex)
    for i in range(q):
        for z in range(rank):
            basis = np.zeros(r)
            basis[z] = 1
            xi[i, :, :, z] = (u @ np.kron(v[:, i], basis)).reshape(q, r) * np.sqrt(lam[i]*weights[z])
    sigma = reduced(xi, (q, q, r, rank), (0, 1, 3))
    product = reduced(xi, (q, q, r, rank), (0, 3))
    product_error = np.linalg.norm(product - np.kron(np.diag(lam), np.diag(weights)))

    # Forget the original purification. Purify the actual extension afresh.
    ev, eb = np.linalg.eigh(sigma)
    selected = ev > 1e-11
    c = int(np.sum(selected))
    assert c >= rank
    new_xi = (eb[:, selected] * np.sqrt(ev[selected])).reshape(q, q, rank, c)
    # Divide Schmidt coefficients: columns labelled (input Schmidt i, bath z).
    j_schmidt = new_xi.transpose(1, 3, 0, 2).reshape(q*c, q*rank)
    j_schmidt /= np.sqrt(np.kron(lam, weights))[None, :]
    j = j_schmidt @ np.kron(adj(v), np.eye(rank))
    isometry_error = np.linalg.norm(adj(j) @ j - np.eye(q*rank))
    # Complete in the active bath only, padding initial tau with zeros.
    left, _, _ = np.linalg.svd(j, full_matrices=True)
    positions = [a*c+b for a in range(q) for b in range(rank)]
    remainder = [i for i in range(q*c) if i not in positions]
    lifted = np.zeros((q*c, q*c), complex)
    lifted[:, positions] = j
    lifted[:, remainder] = left[:, q*rank:]
    new_tau = np.diag(np.r_[weights, np.zeros(c-rank)])
    unitary_error = np.linalg.norm(adj(lifted) @ lifted - np.eye(q*c))
    # Check the entire extension, not only its selected-input A marginal.
    lifted_xi = np.zeros((q, q, c, rank), complex)
    for i in range(q):
        for z in range(rank):
            basis = np.zeros(c)
            basis[z] = 1
            lifted_xi[i, :, :, z] = (lifted @ np.kron(v[:, i], basis)).reshape(q, c) * np.sqrt(lam[i]*weights[z])
    lifted_sigma = reduced(lifted_xi, (q, q, c, rank), (0, 1, 3))
    extension_error = np.linalg.norm(lifted_sigma-sigma)
    original_a, original_b = collision_outputs(u, tau, rho)
    new_a, new_b = collision_outputs(lifted, new_tau, rho)
    conditional = entropy(sigma) - entropy(np.diag(weights))
    residuals = [product_error, isometry_error, unitary_error, extension_error,
                 np.linalg.norm(original_a-new_a),
                 abs(entropy(new_b)-entropy(new_tau)-conditional),
                 abs(entropy(original_b)-entropy(tau)-conditional),
                 abs(entropy(new_tau)-entropy(tau))]
    assert max(residuals) < TOL, residuals
    return max(residuals)


def mixing():
    q, rs = 2, (2, 3, 4)
    us = [unitary(q*r) for r in rs]
    taus = [np.diag(np.arange(1, r+1) / sum(range(1, r+1))) for r in rs]
    weights = np.array([0.13, 0.37, 0.5])
    u, tau = flagged(us, taus, weights, q)
    hp = entropy(np.diag(weights))
    residual = abs(entropy(tau)-hp-sum(p*entropy(t) for p, t in zip(weights, taus)))
    for _ in range(20):
        x = RNG.normal(size=(q, q)) + 1j*RNG.normal(size=(q, q))
        rho = x @ adj(x)
        rho /= np.trace(rho)
        a, b = collision_outputs(u, tau, rho)
        branches = [collision_outputs(uj, tj, rho) for uj, tj in zip(us, taus)]
        expected_a = sum(p*ab[0] for p, ab in zip(weights, branches))
        expected_b = block_diag([p*ab[1] for p, ab in zip(weights, branches)])
        expected_gain = sum(p*(entropy(ab[1])-entropy(tj)) for p, ab, tj in zip(weights, branches, taus))
        residual = max(residual, np.linalg.norm(a-expected_a), np.linalg.norm(b-expected_b),
                       abs(entropy(b)-entropy(tau)-expected_gain))
    assert residual < TOL
    return residual


def negative_controls():
    # A small weighted error at a nearly pure probe is not uniform channel error.
    errors = []
    for t in (1e-2, 1e-4, 1e-6):
        psi = np.array([np.sqrt(1-t), 0, 0, np.sqrt(t)])
        other = psi * np.array([1, -1, 1, -1])
        delta = np.outer(psi, psi)-np.outer(other, other)
        e = float(np.sum(np.abs(np.linalg.eigvalsh(delta)))/2)
        assert abs(e-2*np.sqrt(t*(1-t))) < TOL
        assert 1 <= e/t + TOL
        errors.append(e)
    assert errors[-1] < 0.003  # id and Z still have half-diamond distance one.

    # Two opposite amplitude-damping probes have distinct gain maximizers.
    gamma = 0.25
    u0 = np.eye(4)
    u0[np.ix_([1, 2], [1, 2])] = [[np.sqrt(1-gamma), np.sqrt(gamma)],
                                                   [-np.sqrt(gamma), np.sqrt(1-gamma)]]
    u1 = u0 @ np.kron(np.array([[0., 1.], [1., 0.]]), np.eye(2))
    pure = np.diag([1., 0.])
    uf, tf = flagged([u0, u1], [pure, pure], [0.5, 0.5], 2)
    _, bout = collision_outputs(uf, tf, np.eye(2)/2)
    mixed_max = entropy(bout)-entropy(tf)
    branch_max = entropy(np.diag([gamma, 1-gamma]))
    assert abs(mixed_max-entropy(np.diag([gamma/2, 1-gamma/2]))) < TOL
    assert mixed_max < branch_max-0.2
    return {"weighted_errors_id_vs_Z": errors, "half_diamond_id_vs_Z": 1,
            "max_of_average_gains": mixed_max, "average_of_max_gains": branch_max}


def main():
    cases = [(q, r, rank, small) for q in (2, 3) for r in (2, 3, 4)
             for rank in (1, 2) for small in (0.07, 0.001)]
    lifting_residual = max(lifting(*case) for case in cases)
    mix_residual = mixing()
    controls = negative_controls()
    print(json.dumps({"status": "PASS", "seed": 20260908, "tolerance": TOL,
                      "numpy": np.__version__, "lifting_cases": len(cases),
                      "flagged_inputs": 20, "max_lifting_residual": lifting_residual,
                      "max_flagged_residual": mix_residual,
                      "negative_controls": controls,
                      "scope": "finite identities only; no minimax, limit, novelty or full-theorem certification"}, indent=2))


if __name__ == "__main__":
    main()
