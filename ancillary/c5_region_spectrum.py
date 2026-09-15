"""Bounded C5 controls: actual spectra and retained-partner adaptive dynamics.

These finite checks do not prove an asymptotic diagonal or a universal theorem.
Seed 20260909, tolerance 1e-9. No bath dimension above 192 is allocated.
"""
from fractions import Fraction
from math import floor, log2

import numpy as np


RNG = np.random.default_rng(20260909)
TOL = 1e-9


def unitary(d):
    z = RNG.normal(size=(d, d)) + 1j * RNG.normal(size=(d, d))
    q, r = np.linalg.qr(z)
    diag = np.diag(r)
    return q @ np.diag(diag.conj() / np.abs(diag))


def apply(rho, u, axes, dims):
    """Conjugate density on selected ordered factors, preserving all others."""
    order = list(axes) + [i for i in range(len(dims)) if i not in axes]
    inv = np.argsort(order)
    n = len(dims)
    d = u.shape[0]
    rem = rho.shape[0] // d
    perm = order + [i + n for i in order]
    x = rho.reshape(dims + dims).transpose(perm).reshape(d, rem, d, rem)
    x = np.einsum("ia,arbs,jb->irjs", u, x, u.conj(), optimize=True)
    sd = [dims[i] for i in order]
    return x.reshape(sd + sd).transpose(list(inv) + list(inv + n)).reshape(rho.shape)


def trace_last(rho, d):
    rem = rho.shape[0] // d
    return np.trace(rho.reshape(rem, d, rem, d), axis1=1, axis2=3)


def entropy(rho):
    ev = np.linalg.eigvalsh(rho)
    ev = ev[ev > 1e-12]
    return float(-np.dot(ev, np.log2(ev)))


def initializer(k, j, ell):
    """B=(seed, mixed data, pure qubit), P=ell partner qubits."""
    b, p = j * 2**k * 2, 2**ell
    state = np.zeros((b * p, b * p), dtype=complex)
    rank = j * 2 ** (k - ell)
    for seed in range(j):
        for rest in range(2 ** (k - ell)):
            v = np.zeros(b * p, dtype=complex)
            for a in range(p):
                data = a * 2 ** (k - ell) + rest
                bi = (seed * 2**k + data) * 2
                v[bi * p + a] = 1 / np.sqrt(p)
            state += np.outer(v, v.conj()) / rank
    return state, b, p, rank


def spectrum_and_dynamics():
    residual = 0.0
    cases = 0
    largest = 0
    for k in range(3):
        for j in (1, 3):
            for ell in range(k + 1):
                omega, b, p, rank = initializer(k, j, ell)
                marginal = trace_last(omega, p)
                expected = np.kron(np.eye(j * 2**k) / (j * 2**k), np.diag([1., 0.]))
                target_ev = np.r_[np.zeros(b * p - rank), np.full(rank, 1 / rank)]
                local = [np.linalg.norm(marginal - expected),
                         np.max(np.abs(np.linalg.eigvalsh(omega) - target_ev)),
                         abs(entropy(omega) - (log2(j) + k - ell))]
                assert rank <= b * p
                # A reference and two entangled inputs, with coherent feedback
                # between calls. The same arbitrary bath unitary is repeated.
                user = RNG.normal(size=8) + 1j * RNG.normal(size=8)
                user /= np.linalg.norm(user)
                psi = np.outer(user, user.conj())
                old = np.kron(psi, marginal)
                new = np.kron(psi, omega)
                dims_old, dims_new = [2, 2, 2, b], [2, 2, 2, b, p]
                collision, feedback = unitary(2 * b), unitary(4)
                for u, axes in ((collision, [1, 3]), (feedback, [1, 2]),
                                (collision, [2, 3])):
                    old = apply(old, u, axes, dims_old)
                    new = apply(new, u, axes, dims_new)
                    local.append(np.linalg.norm(trace_last(new, p) - old))
                residual = max(residual, *local)
                largest = max(largest, new.shape[0])
                assert max(local) < TOL, (k, j, ell, local)
                cases += 1
    print(f"PASS: {cases} actual-spectrum/two-visit coherent-feedback cases; "
          f"max residual {residual:.4g}; largest density dimension {largest}")


def integer_region():
    cases = 0
    for h in (Fraction(0), Fraction(1, 3), Fraction(1), Fraction(2)):
        for ratio in (Fraction(0), Fraction(1, 2), Fraction(1)):
            kappa = h * ratio
            s0, r0 = (h - kappa) / 2, (h + kappa) / 2
            for s in (Fraction(0), s0 / 2, s0, s0 + Fraction(2, 3)):
                for t in (1, 3, 11, 100):
                    for fluct in (-2, 0, 3):
                        stock = max(0, floor(s0 * t) + fluct)
                        if s <= s0:
                            ell = min(stock, floor((s0 - s) * t))
                            assert 0 <= ell <= stock
                            # Two floors plus bounded stock fluctuation; the
                            # uniform finite remainder checks clipping at s=0.
                            assert abs(Fraction(ell) - (s0 - s) * t) <= abs(fluct) + 2
                            assert r0 + s0 - s == h - s
                        else:
                            extra = floor((s - s0) * t)
                            assert 0 <= (s - s0) * t - extra < 1
                            assert r0 + s - s0 == kappa + s
                        assert max(h - s, kappa + s) >= s
                        cases += 1
    print(f"PASS: {cases} exact rational region/clipping cases")


if __name__ == "__main__":
    spectrum_and_dynamics()
    integer_region()
