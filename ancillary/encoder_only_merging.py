"""Finite controls for the priority reduction, not a proof of adaptive coding."""
import json
from fractions import Fraction
import numpy as np


def unitary(rng, d):
    q, r = np.linalg.qr(rng.normal(size=(d, d)) + 1j*rng.normal(size=(d, d)))
    return q @ np.diag(np.diag(r)/np.abs(np.diag(r)))


def mh_marginal(psi):
    m, g, f, h = psi.shape
    x = psi.transpose(0, 3, 1, 2).reshape(m*h, g*f)
    return x @ x.conj().T


def main():
    rng = np.random.default_rng(20260908)
    worst = 0.0
    cases = 0
    for m, g, f, h in [(2, 2, 2, 2), (2, 3, 2, 3), (3, 2, 3, 2)]:
        for _ in range(12):
            psi = rng.normal(size=(m, g, f, h)) + 1j*rng.normal(size=(m, g, f, h))
            psi /= np.linalg.norm(psi)
            decoder = unitary(rng, g*f)
            decoded = np.einsum('ab,mbh->mah', decoder, psi.reshape(m, g*f, h))
            decoded = decoded.reshape(m, g, f, h)
            residual = np.linalg.norm(mh_marginal(psi)-mh_marginal(decoded), ord='fro')
            worst = max(worst, float(residual))
            assert residual < 1e-12
            cases += 1
    # Exact arithmetic: standard FQSW split gives C4's two linear balances.
    counts = 0
    for sigma in range(5):
        for gain in range(5):
            for h in range(gain, 2*sigma+gain+1):
                v = sigma+gain
                parked = Fraction(v+h-sigma, 2)
                capital = Fraction(v+sigma-h, 2)
                a, b = Fraction(h-gain, 2), Fraction(h+gain, 2)
                assert parked == b and capital == sigma-a
                assert parked+capital == v and sigma-capital == a
                counts += 1
    print(json.dumps({"decoder_omission_cases": cases,
                      "maximum_marginal_frobenius_residual": worst,
                      "exact_rate_balance_cases": counts,
                      "scope": "finite marginal identity and rational rate arithmetic only"}, indent=2))


if __name__ == '__main__':
    main()
