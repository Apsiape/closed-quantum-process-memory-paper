"""Finite control for the interior example of manuscript Proposition 7.5.

Checks the generalized amplitude damping channel at gamma=1/2, p=3/4:
trace preservation of its four Kraus operators, unitarity of the exchange
block, that the explicit qubit collision (U, tau=diag(p,1-p)) reproduces the
channel on random mixed inputs, the two analytic endpoints of the bracket, and
the lower bound of Proposition 7.4 on a grid.

Tensor basis: system first, bath second. NumPy floating-point diagnostics.
These are finite checks of one channel; they prove no theorem of the paper.
The strict inequalities in Proposition 7.5 are established analytically there,
not by these decimals.
"""
import numpy as np

TOL = 1e-8
RNG = np.random.default_rng(20260910)
GAMMA = 0.5
P = 0.75


def adj(a):
    return a.conj().T


def h2(x):
    if x <= 0.0 or x >= 1.0:
        return 0.0
    return -x * np.log2(x) - (1 - x) * np.log2(1 - x)


def entropy(rho):
    vals = np.linalg.eigvalsh((rho + adj(rho)) / 2)
    vals = vals[vals > 1e-12]
    return float(-(vals * np.log2(vals)).sum())


def kraus(gamma, p):
    k0 = np.sqrt(p) * np.diag([1.0, np.sqrt(1 - gamma)]).astype(complex)
    k1 = np.zeros((2, 2), complex)
    k1[0, 1] = np.sqrt(p * gamma)
    k2 = np.sqrt(1 - p) * np.diag([np.sqrt(1 - gamma), 1.0]).astype(complex)
    k3 = np.zeros((2, 2), complex)
    k3[1, 0] = np.sqrt((1 - p) * gamma)
    return [k0, k1, k2, k3]


def collision_unitary(gamma):
    # Fixes |00> and |11>; rotates the span of |01>, |10> in that order.
    u = np.eye(4, dtype=complex)
    block = np.array([[np.sqrt(1 - gamma), -1j * np.sqrt(gamma)],
                      [-1j * np.sqrt(gamma), np.sqrt(1 - gamma)]])
    idx = [1, 2]
    for a, ia in enumerate(idx):
        for b, ib in enumerate(idx):
            u[ia, ib] = block[a, b]
    return u, block


def apply_collision(u, tau, rho):
    joint = u @ np.kron(rho, tau) @ adj(u)
    joint = joint.reshape(2, 2, 2, 2)
    out_sys = np.einsum('ikjk->ij', joint)
    out_bath = np.einsum('kikj->ij', joint)
    return out_sys, out_bath


def random_state(rng):
    g = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    rho = g @ adj(g)
    return rho / np.trace(rho).real


def main():
    ks = kraus(GAMMA, P)
    resid_tp = np.linalg.norm(sum(adj(k) @ k for k in ks) - np.eye(2))
    u, block = collision_unitary(GAMMA)
    resid_block = np.linalg.norm(adj(block) @ block - np.eye(2))
    resid_u = np.linalg.norm(adj(u) @ u - np.eye(4))
    tau = np.diag([P, 1 - P]).astype(complex)

    worst_channel = 0.0
    worst_bath_entropy = 0.0
    worst_gain = -np.inf
    worst_lower = -np.inf
    states = [np.eye(2, dtype=complex) / 2,
              np.diag([1.0, 0.0]).astype(complex),
              np.diag([0.0, 1.0]).astype(complex)]
    states += [random_state(RNG) for _ in range(2000)]
    s_tau = h2(P)
    for rho in states:
        direct = sum(k @ rho @ adj(k) for k in ks)
        out_sys, out_bath = apply_collision(u, tau, rho)
        worst_channel = max(worst_channel, np.linalg.norm(direct - out_sys))
        worst_bath_entropy = max(worst_bath_entropy, entropy(out_bath))
        worst_gain = max(worst_gain, entropy(out_bath) - s_tau)
        worst_lower = max(worst_lower, entropy(rho) - entropy(direct))

    mixed_out = sum(k @ (np.eye(2, dtype=complex) / 2) @ adj(k) for k in ks)
    excited_out = sum(k @ np.diag([0.0, 1.0]).astype(complex) @ adj(k) for k in ks)
    ceiling = 1.0 - h2(P)
    floor_at_mixed = 1.0 - h2(0.625)
    h_lower = h2(0.375)

    print('trace-preservation residual %.3e' % resid_tp)
    print('exchange-block unitarity residual %.3e' % resid_block)
    print('collision unitarity residual %.3e' % resid_u)
    print('max channel deviation over %d inputs %.3e'
          % (len(states), worst_channel))
    print('Phi(I/2) diagonal %s' % np.round(np.real(np.diag(mixed_out)), 12))
    print('Phi(|1><1|) diagonal %s' % np.round(np.real(np.diag(excited_out)), 12))
    print('max sampled active bath entropy %.6f (ceiling 1)' % worst_bath_entropy)
    print('max sampled gain of this collision %.6f (analytic ceiling %.6f)'
          % (worst_gain, ceiling))
    print('max sampled S(rho)-S(Phi(rho)) %.6f (analytic instance %.6f)'
          % (worst_lower, floor_at_mixed))
    print('h lower bound from the pure excited input %.6f' % h_lower)
    print('bracket %.6f <= kappa <= %.6f < %.6f <= h'
          % (floor_at_mixed, ceiling, h_lower))

    assert resid_tp < TOL and resid_block < TOL and resid_u < TOL
    assert worst_channel < TOL
    assert abs(np.real(mixed_out[0, 0]) - 0.625) < TOL
    assert abs(np.real(excited_out[0, 0]) - 0.375) < TOL
    assert worst_bath_entropy <= 1.0 + TOL
    assert worst_gain <= ceiling + TOL
    assert worst_lower >= floor_at_mixed - TOL
    assert 0.0 < floor_at_mixed <= ceiling < h_lower
    print('PASS')


if __name__ == '__main__':
    main()
