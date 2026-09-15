"""Finite hostile controls for C3, including the exactification interface.

Seed 20260909. All distances halved; normalized Choi coordinates are A,Q.
No diamond norm optimization, infinite-dimensional optimization or asymptotic
theorem is checked. Uses existing elementary matrix helpers, not audit verdicts.
"""
import json
import numpy as np
from support_repair import adj, complete_columns, norm, positive_sqrt

RNG = np.random.default_rng(20260909)
TOL = 1e-8


def entropy(x):
    ev = np.linalg.eigvalsh((x+adj(x))/2)
    assert ev.min() >= -TOL
    ev = ev[ev > 1e-14]
    return float(-np.sum(ev*np.log2(ev)))


def trace_distance(x, y):
    return float(np.sum(np.abs(np.linalg.eigvalsh((x-y+adj(x-y))/2)))/2)


def choi(kraus):
    q = kraus[0].shape[0]
    return sum(np.outer(a.reshape(-1), a.reshape(-1).conj()) for a in kraus)/q


def collision_kraus(j, tau, q):
    r = len(tau)
    rout = len(j)//q
    weighted = (j @ np.kron(np.eye(q), positive_sqrt(tau))).reshape(q, rout, q, r)
    return [weighted[:, b, :, f] for b in range(rout) for f in range(r)]


def partial_input(j, q):
    return np.trace(j.reshape(q, q, q, q), axis1=0, axis2=2)


def bath_output(j, tau, rho):
    q, r = len(rho), len(j)//len(rho)
    out = (j @ np.kron(rho, tau) @ adj(j)).reshape(q, r, q, r)
    return np.trace(out, axis1=0, axis2=2)


def purified(j, tau, rho):
    q, rin, rout = len(rho), len(tau), len(j)//len(rho)
    return np.einsum('absc,qs,cf->qabf', j.reshape(q, rout, q, rin),
                     positive_sqrt(rho).T, positive_sqrt(tau))


def conditional_from_pure(x):
    q, _, r, f = x.shape
    matrix = x.transpose(0, 1, 3, 2).reshape(q*q*f, r)
    reduced = matrix @ adj(matrix)
    fmat = x.transpose(3, 0, 1, 2).reshape(f, -1)
    return entropy(reduced)-entropy(fmat @ adj(fmat))


def beta(q, error):
    e = min(1.0, error)
    if e == 0:
        return 0.0
    t = e/(1+e)
    return 4*e*np.log2(q)+(1+e)*(-t*np.log2(t)-(1-t)*np.log2(1-t))


def flagged(u, tau, v, probability, q):
    r, k = len(tau), len(v)//q
    total = r+k
    out = np.zeros((q*total, q*total), complex)
    first = [s*total+b for s in range(q) for b in range(r)]
    second = [s*total+r+b for s in range(q) for b in range(k)]
    out[np.ix_(first, first)] = u
    out[np.ix_(second, second)] = v
    init = np.zeros((total, total), complex)
    init[:r, :r] = (1-probability)*tau
    init[r, r] = probability
    return out, init


def case(name, family, scale):
    q, k = family[0].shape[0], len(family)
    # Two independent initially usable bath positions force matrix amplification.
    r, initial_good = 2*k+1, 2
    target = np.zeros((q*r, q*initial_good), complex)
    for aidx, a in enumerate(family):
        target += np.kron(a, np.eye(r)[:, aidx*initial_good:(aidx+1)*initial_good])
    positions = [s*r+b for s in range(q) for b in range(initial_good)]
    u = complete_columns(target, positions, q*r)
    h = RNG.normal(size=u.shape)+1j*RNG.normal(size=u.shape)
    h += adj(h)
    eig, vec = np.linalg.eigh(h)
    u = (vec*np.exp(1j*scale*eig)) @ adj(vec) @ u
    basis = np.stack([a.reshape(-1) for a in family], axis=1)
    projection = basis @ np.linalg.pinv(basis)
    blocks = u.reshape(q, r, q, r).transpose(0, 2, 1, 3).reshape(q*q, r*r)
    v = (projection @ blocks).reshape(q, q, r, r).transpose(0, 2, 1, 3).reshape(q*r, q*r)
    leakage = u-v
    e = np.trace((adj(leakage) @ leakage).reshape(q, r, q, r), axis1=0, axis2=2)
    eps = 0.01 if scale == 1e-5 else 0.0001
    values, vectors = np.linalg.eigh(e)
    good = vectors[:, values <= eps*eps/q]
    bad = vectors[:, values > eps*eps/q]
    d0 = good.shape[1]
    assert d0 >= 2 and bad.shape[1] > 0
    p, qb = good @ adj(good), bad @ adj(bad)
    vp = v @ np.kron(np.eye(q), good)
    defect = adj(vp) @ vp-np.eye(q*d0)
    gram_map = np.stack([(adj(a) @ b).reshape(-1) for a in family for b in family], axis=1)
    right = np.linalg.pinv(gram_map)
    constant = max(1.0, sum(norm(right[:, n].reshape(k, k)) for n in range(q*q)))
    block_defect = defect.reshape(q, d0, q, d0).transpose(0, 2, 1, 3).reshape(q*q, d0*d0)
    repaired_defect = (right @ block_defect).reshape(k, k, d0, d0).transpose(0, 2, 1, 3).reshape(k*d0, k*d0)
    defect_bound = 2*eps+eps*eps
    t = constant*defect_bound
    gram = (t*np.eye(k*d0)-repaired_defect)/(1+t)
    gs = positive_sqrt(gram)
    w = sum(np.kron(a, gs[:, n*d0:(n+1)*d0]) for n, a in enumerate(family))
    top = v @ np.kron(np.eye(q), p)/np.sqrt(1+t)
    bottom = np.kron(np.eye(q), np.kron(np.eye(k), good)) @ w @ np.kron(np.eye(q), adj(good))
    bottom += sum(np.kron(a, np.kron(np.eye(k)[:, n:n+1], qb)) for n, a in enumerate(family))
    rout = (k+1)*r
    repaired = np.concatenate([top.reshape(q, r, q*r), bottom.reshape(q, k*r, q*r)], axis=1).reshape(q*rout, q*r)
    old = np.zeros((q, rout, q*r), complex)
    old[:, :r, :] = u.reshape(q, r, q*r)
    old = old.reshape(repaired.shape)

    # Nonflat full-rank tau with deliberate coherence across the actual cutoff.
    # The kernel of E can exceed the original two target-initialization columns.
    # Keep those original columns after projection, rather than selecting an
    # arbitrary kernel eigenbasis that could implement a different face channel.
    usable, _ = np.linalg.qr(p @ np.eye(r)[:, :initial_good])
    angle = 50*scale
    first = np.cos(angle)*usable[:, 0]+np.sin(angle)*bad[:, 0]
    tau = 0.7*np.outer(first, first.conj())+0.3*np.outer(usable[:, 1], usable[:, 1].conj())
    floor = 1e-8 if scale == 1e-5 else 1e-12
    tau = (1-floor)*tau+floor*np.eye(r)/r
    padded = np.zeros((rout, rout), complex)
    padded[:r, :r] = tau
    commutator = norm(tau @ p-p @ tau)
    assert commutator > 1e-8
    bad_weight = float(np.trace(tau @ qb).real)
    leakage_weight = float(np.trace(tau @ e).real/q)
    target_choi = choi(family)
    old_choi = choi(collision_kraus(u, tau, q))
    new_choi = choi(collision_kraus(repaired, tau, q))
    eta_upper = min(1.0, q*trace_distance(old_choi, target_choi))
    residuals = [norm(adj(repaired) @ repaired-np.eye(q*r)),
                 norm(gram-adj(gram)), norm(gram_map @ right @ block_defect-block_defect),
                 norm((np.eye(q*q)-projection) @ new_choi),
                 norm(partial_input(new_choi, q)-np.eye(q)/q),
                 abs(leakage_weight-float(np.trace((np.eye(q*q)-projection) @ old_choi).real)),
                 abs(entropy(padded)-entropy(tau))]
    assert norm(repaired_defect) <= constant*norm(defect)+TOL
    assert norm(leakage @ np.kron(np.eye(q), p)) <= eps+TOL
    assert bad_weight <= q*q*leakage_weight/(eps*eps)+TOL
    aeps = eps+t/2+np.sqrt((t+defect_bound)/(1+t))
    uniform_vector_bound = aeps+2*np.sqrt(bad_weight)
    uniform_channel_bound = aeps+2*q*np.sqrt(eta_upper)/eps
    max_gain_difference, max_pure_distance, max_coherence = 0., 0., 0.
    inputs = [np.eye(q)/q, np.diag([1.]+[0.]*(q-1))]
    for _ in range(3):
        x = RNG.normal(size=(q, q))+1j*RNG.normal(size=(q, q))
        rho = x @ adj(x)
        inputs.append(rho/np.trace(rho))
    for rho in inputs:
        original, repaired_pure = purified(old, tau, rho), purified(repaired, tau, rho)
        distance = np.linalg.norm(original-repaired_pure)
        assert distance <= uniform_vector_bound+TOL
        assert distance <= uniform_channel_bound+TOL
        pure_distance = np.sqrt(max(0., 1-abs(np.vdot(original, repaired_pure))**2))
        gain_before = entropy(bath_output(u, tau, rho))-entropy(tau)
        gain_after = entropy(bath_output(repaired, tau, rho))-entropy(tau)
        residuals += [abs(gain_before-conditional_from_pure(original)),
                      abs(gain_after-conditional_from_pure(repaired_pure))]
        assert abs(gain_after-gain_before) <= beta(q, pure_distance)+TOL
        coherence = repaired @ np.kron(rho, p @ tau @ qb) @ adj(repaired)
        max_coherence = max(max_coherence, norm(coherence))
        max_gain_difference = max(max_gain_difference, abs(gain_after-gain_before))
        max_pure_distance = max(max_pure_distance, pure_distance)
    assert max_coherence > 1e-8

    # The theorem permits any valid diamond upper bound at this stage.
    # q times normalized Choi half-distance is a conservative such bound.
    # An extreme target face may already be exactly repaired; then using a
    # roundoff-sized correction weight would divide noise by noise. A larger
    # valid error bound deliberately exercises the nonzero correction branch.
    bar_eta = max(1e-3, min(1.0, q*trace_distance(new_choi, target_choi)))
    mu = np.linalg.eigvalsh(target_choi)[-k]
    f = 2*bar_eta/(mu+2*bar_eta)
    theta_choi = (target_choi-(1-f)*new_choi)/f
    vals, vecs = np.linalg.eigh((theta_choi+adj(theta_choi))/2)
    assert vals.min() >= -TOL
    theta_kraus = [np.sqrt(q*val)*vecs[:, i].reshape(q, q) for i, val in enumerate(vals) if val > 1e-10]
    kt = len(theta_kraus)
    assert kt <= k
    theta_j = sum(np.kron(a, np.eye(kt)[:, n:n+1]) for n, a in enumerate(theta_kraus))
    theta_u = complete_columns(theta_j, [s*kt for s in range(q)], q*kt)
    repaired_u = complete_columns(repaired, [s*rout+b for s in range(q) for b in range(r)], q*rout)
    exact_u, exact_tau = flagged(repaired_u, padded, theta_u, f, q)
    exact_choi = choi(collision_kraus(exact_u, exact_tau, q))
    expected_spec = np.r_[(1-f)*np.linalg.eigvalsh(tau), f, np.zeros(len(exact_tau)-r-1)]
    residuals += [norm(exact_choi-target_choi),
                  norm(partial_input(theta_choi, q)-np.eye(q)/q),
                  float(np.max(np.abs(np.sort(expected_spec)-np.linalg.eigvalsh(exact_tau)))),
                  abs(entropy(exact_tau)-entropy(np.diag([f, 1-f]))-(1-f)*entropy(tau))]
    theta_tau = np.diag([1.]+[0.]*(kt-1))
    for rho in inputs:
        exact_gain = entropy(bath_output(exact_u, exact_tau, rho))-entropy(exact_tau)
        repaired_gain = entropy(bath_output(repaired, tau, rho))-entropy(tau)
        theta_gain = entropy(bath_output(theta_u, theta_tau, rho))
        residuals.append(abs(exact_gain-(1-f)*repaired_gain-f*theta_gain))
        assert theta_gain <= np.log2(k)+TOL
    assert max(residuals) < TOL, residuals
    return {"family": name, "q": q, "k": k, "R": r, "good_rank": d0,
            "scale": scale, "tau_min_eigenvalue": float(np.linalg.eigvalsh(tau)[0]),
            "original_half_diamond_upper_bound": eta_upper,
            "cutoff_commutator": commutator, "retained_coherence": max_coherence,
            "correction_weight": f, "exact_bath_dimension": len(exact_tau),
            "max_sample_gain_change": max_gain_difference, "max_sample_pure_distance": max_pure_distance,
            "maximum_residual": max(residuals)}


def negative_controls():
    family = [np.diag([1., 0.8]), np.array([[0., 0.6], [0., 0.]])]
    basis = np.stack([a.reshape(-1) for a in family], axis=1)
    p = basis @ np.linalg.pinv(basis)
    v = family[0]+0.3*family[1]
    polar = v @ np.linalg.inv(positive_sqrt(adj(v) @ v))
    polar_leakage = np.linalg.norm((np.eye(4)-p) @ polar.reshape(-1))
    assert polar_leakage > 0.01
    lm = np.stack([(adj(a) @ b).reshape(-1) for a in family for b in family], axis=1)
    r_positive = (np.linalg.inv(lm) @ np.diag([1., 0.]).reshape(-1)).reshape(2, 2)
    minimum = float(np.linalg.eigvalsh(r_positive)[0])
    assert minimum < -1
    # Even very small f does not imply uniformly small initial-entropy change.
    # Exact symbolic entropy formula, with log R specified instead of allocating R.
    f, log_r = 1e-4, 1000000
    entropy_change = entropy(np.diag([f, 1-f]))-f*log_r
    assert entropy_change < -99
    return {"polar_support_leakage": float(polar_leakage),
            "right_inverse_positive_input_min_eigenvalue": minimum,
            "flag_f": f, "symbolic_log2_R": log_r,
            "initial_entropy_change_bits": entropy_change}


def main():
    g = 0.36
    families = {
        "amplitude_damping": [np.diag([1., np.sqrt(1-g)]), np.array([[0., np.sqrt(g)], [0., 0.]])],
        "dephasing": [np.diag([1., 0.]), np.diag([0., 1.])],
        "two_pauli_face": [np.eye(2)/np.sqrt(3), np.array([[0., 1.], [1., 0.]])/np.sqrt(3), np.diag([1., -1.])/np.sqrt(3)],
        "qutrit_dephasing": [np.diag(np.eye(3)[i]) for i in range(3)],
    }
    results = [case(name, family, scale) for name, family in families.items() for scale in (1e-5, 1e-8)]
    print(json.dumps({"status": "PASS", "seed": 20260909, "tolerance": TOL,
                      "numpy": np.__version__, "cases": len(results), "input_checks": 5*len(results),
                      "maximum_residual": max(x["maximum_residual"] for x in results),
                      "minimum_cutoff_commutator": min(x["cutoff_commutator"] for x in results),
                      "largest_unitary_dimension": max(x["q"]*x["exact_bath_dimension"] for x in results),
                      "negative_controls": negative_controls(), "details": results,
                      "scope": "finite matrices and symbolic entropy arithmetic only; no full theorem or diamond optimization"}, indent=2))


if __name__ == "__main__":
    main()
