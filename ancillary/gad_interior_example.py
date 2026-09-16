"""Finite control for the interior example of manuscript Proposition 7.5.

Checks the generalized amplitude damping channel at damping nu=1/2 (the code
variable is DAMPING), p=3/4: trace preservation of its four Kraus operators,
unitarity of the exchange block, that the explicit qubit collision
(U, tau=diag(p,1-p)) reproduces the channel on random mixed inputs, the two
analytic endpoints of the bracket, the exact rational lower witness
diag(7/12,5/12) with output diag(2/3,1/3), the attained upper witness
diag(1/4,3/4) whose bath output is I/2, the mixed-input entropy-exchange value
at diag(1/3,2/3), and diagonal grid searches for the best input-space lower
bound and for the entropy exchange.

Tensor basis: system first, bath second. NumPy floating-point diagnostics.
These are finite checks of one channel; they prove no theorem of the paper.
The strict inequalities in Proposition 7.5 are established analytically there,
not by these decimals. The displayed decimals are checked here for rounding
direction only.
"""
import numpy as np

TOL = 1e-8
RNG = np.random.default_rng(20260910)
DAMPING = 0.5
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


def kraus(nu, p):
    k0 = np.sqrt(p) * np.diag([1.0, np.sqrt(1 - nu)]).astype(complex)
    k1 = np.zeros((2, 2), complex)
    k1[0, 1] = np.sqrt(p * nu)
    k2 = np.sqrt(1 - p) * np.diag([np.sqrt(1 - nu), 1.0]).astype(complex)
    k3 = np.zeros((2, 2), complex)
    k3[1, 0] = np.sqrt((1 - p) * nu)
    return [k0, k1, k2, k3]


def channel(ks, rho):
    return sum(k @ rho @ adj(k) for k in ks)


def complementary(ks, rho):
    # Environment output of the Kraus dilation: entries Tr(K_a rho K_b^*).
    out = np.zeros((len(ks), len(ks)), complex)
    for a, ka in enumerate(ks):
        for b, kb in enumerate(ks):
            out[a, b] = np.trace(ka @ rho @ adj(kb))
    return out


def collision_unitary(nu):
    # Fixes |00> and |11>; rotates the span of |01>, |10> in that order.
    u = np.eye(4, dtype=complex)
    block = np.array([[np.sqrt(1 - nu), -1j * np.sqrt(nu)],
                      [-1j * np.sqrt(nu), np.sqrt(1 - nu)]])
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


def diag_state(a):
    return np.diag([a, 1.0 - a]).astype(complex)


def h2_vec(x):
    x = np.clip(x, 1e-300, 1 - 1e-16)
    return -x * np.log2(x) - (1 - x) * np.log2(1 - x)


def main():
    ks = kraus(DAMPING, P)
    resid_tp = np.linalg.norm(sum(adj(k) @ k for k in ks) - np.eye(2))
    u, block = collision_unitary(DAMPING)
    resid_block = np.linalg.norm(adj(block) @ block - np.eye(2))
    resid_u = np.linalg.norm(adj(u) @ u - np.eye(4))
    tau = np.diag([P, 1 - P]).astype(complex)

    worst_channel = 0.0
    worst_bath_entropy = 0.0
    worst_gain = -np.inf
    worst_lower = -np.inf
    worst_exchange = 0.0
    states = [np.eye(2, dtype=complex) / 2,
              diag_state(1.0), diag_state(0.0),
              diag_state(7 / 12), diag_state(3 / 5), diag_state(1 / 4),
              diag_state(1 / 3)]
    states += [random_state(RNG) for _ in range(2000)]
    s_tau = h2(P)
    for rho in states:
        direct = channel(ks, rho)
        out_sys, out_bath = apply_collision(u, tau, rho)
        worst_channel = max(worst_channel, np.linalg.norm(direct - out_sys))
        worst_bath_entropy = max(worst_bath_entropy, entropy(out_bath))
        worst_gain = max(worst_gain, entropy(out_bath) - s_tau)
        worst_lower = max(worst_lower, entropy(rho) - entropy(direct))
        worst_exchange = max(worst_exchange, entropy(complementary(ks, rho)))

    mixed_out = channel(ks, np.eye(2, dtype=complex) / 2)
    excited_out = channel(ks, diag_state(0.0))
    rational_out = channel(ks, diag_state(7 / 12))
    mghirbi_lower = entropy(diag_state(3 / 5)) - entropy(channel(ks, diag_state(3 / 5)))
    _, tight_bath = apply_collision(u, tau, diag_state(1 / 4))
    exchange_third = entropy(complementary(ks, diag_state(1 / 3)))

    ceiling = 1.0 - h2(P)
    floor_rational = h2(7 / 12) - h2(1 / 3)
    floor_at_mixed = 1.0 - h2(0.625)
    h_lower = h2(0.375)

    # Diagonal grid searches. On diagonal inputs the channel acts as
    # diag(a,1-a) -> diag(3/8+a/2, 5/8-a/2).
    grid = np.linspace(0.0, 1.0, 1000001)
    lower_curve = h2_vec(grid) - h2_vec(3 / 8 + grid / 2)
    i_lower = int(lower_curve.argmax())
    grid_lower_max, grid_lower_arg = float(lower_curve[i_lower]), float(grid[i_lower])
    coarse = np.linspace(0.0, 1.0, 20001)
    exchange_curve = np.array([entropy(complementary(ks, diag_state(a))) for a in coarse])
    i_ex = int(exchange_curve.argmax())
    grid_exchange_max, grid_exchange_arg = float(exchange_curve[i_ex]), float(coarse[i_ex])

    print('trace-preservation residual %.3e' % resid_tp)
    print('exchange-block unitarity residual %.3e' % resid_block)
    print('collision unitarity residual %.3e' % resid_u)
    print('max channel deviation over %d inputs %.3e'
          % (len(states), worst_channel))
    print('Phi(I/2) diagonal %s' % np.round(np.real(np.diag(mixed_out)), 12))
    print('Phi(|1><1|) diagonal %s' % np.round(np.real(np.diag(excited_out)), 12))
    print('Phi(diag(7/12,5/12)) diagonal %s' % np.round(np.real(np.diag(rational_out)), 12))
    print('max sampled active bath entropy %.6f (ceiling 1)' % worst_bath_entropy)
    print('max sampled gain of this collision %.7f (analytic ceiling %.7f)'
          % (worst_gain, ceiling))
    print('bath output entropy at diag(1/4,3/4): %.12f (attains the ceiling)'
          % entropy(tight_bath))
    print('max sampled S(rho)-S(Phi(rho)) %.7f' % worst_lower)
    print('  rational witness diag(7/12,5/12): H2(7/12)-H2(1/3) = %.7f' % floor_rational)
    print('  Mghirbi witness diag(3/5,2/5): %.7f' % mghirbi_lower)
    print('  maximally mixed input: 1-H2(5/8) = %.10f' % floor_at_mixed)
    print('  diagonal grid maximum %.7f at a = %.5f' % (grid_lower_max, grid_lower_arg))
    print('entropy exchange: pure excited input H2(3/8) = %.7f' % h_lower)
    print('  mixed input diag(1/3,2/3): %.7f' % exchange_third)
    print('  diagonal grid maximum %.7f at a = %.5f' % (grid_exchange_max, grid_exchange_arg))
    print('  max over the %d sampled inputs %.7f' % (len(states), worst_exchange))
    print('analytic bracket %.7f <= kappa <= %.7f < %.7f <= h'
          % (floor_rational, ceiling, h_lower))
    print('paper displays 0.061572 <= kappa <= 0.188722 < 0.954434 <= h,'
          ' each rounded toward validity')

    assert resid_tp < TOL and resid_block < TOL and resid_u < TOL
    assert worst_channel < TOL
    assert abs(np.real(mixed_out[0, 0]) - 0.625) < TOL
    assert abs(np.real(excited_out[0, 0]) - 0.375) < TOL
    assert np.linalg.norm(rational_out - diag_state(2 / 3)) < TOL
    assert worst_bath_entropy <= 1.0 + TOL
    assert worst_gain <= ceiling + TOL
    assert abs(entropy(tight_bath) - 1.0) < TOL
    assert np.linalg.norm(tight_bath - np.eye(2) / 2) < TOL
    assert worst_lower >= floor_rational - TOL
    assert worst_lower <= grid_lower_max + TOL
    assert 0.0 < floor_at_mixed < mghirbi_lower < floor_rational <= grid_lower_max
    assert floor_rational <= ceiling < h_lower
    assert 0.061214 <= mghirbi_lower < 0.061215
    assert 0.061572 <= floor_rational < 0.061573
    assert 0.061597 <= grid_lower_max < 0.061599 and abs(grid_lower_arg - 0.58671) < 2e-5
    assert 0.188721 < ceiling <= 0.188722
    assert 0.954434 <= h_lower < 0.954435
    assert 1.148402 <= exchange_third < 1.148403
    assert 1.148985 < grid_exchange_max < 1.148987 and abs(grid_exchange_arg - 0.35586) < 1e-4
    assert worst_exchange <= grid_exchange_max + TOL
    print('PASS')


if __name__ == '__main__':
    main()
