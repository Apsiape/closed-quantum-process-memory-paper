"""Exact finite control: repeated dephasing marginals need not be independent.

The counted bath is one classical fair bit, controlling I or Pauli Z on
each arriving |+> qubit. No reset occurs. In the X basis, the user outputs
are all the bath bit. Ideal independent dephasing gives independent fair
bits. These states are diagonal in the same orthonormal basis, so their
half-trace distance is exactly the classical total variation computed here.

Coverage: q=R=2, T=1,...,12, at most 4096 probability entries. Fractions
give exact arithmetic; there is no random seed or floating-point tolerance.
This is a contract counterexample, not a numerical proof of C1--C5.
"""

from fractions import Fraction
import json


def check(horizon):
    count = 1 << horizon
    shared = [Fraction(0) for _ in range(count)]
    shared[0] = shared[-1] = Fraction(1, 2)
    ideal = Fraction(1, count)
    assert sum(shared) == 1
    for position in range(horizon):
        # Every individual output is exactly the correct dephased marginal.
        zero = sum(p for x, p in enumerate(shared) if not (x >> position) & 1)
        assert zero == Fraction(1, 2)
    distance = sum(abs(p - ideal) for p in shared) / 2
    expected = 1 - Fraction(2, count)
    assert distance == expected
    # The retained classical event "all X outcomes agree" distinguishes them.
    assert shared[0] + shared[-1] - 2 * ideal == distance
    return {"T": horizon, "half_trace_distance": str(distance)}


if __name__ == "__main__":
    results = [check(t) for t in range(1, 13)]
    assert results[1]["half_trace_distance"] == "1/2"
    print(json.dumps({"status": "PASS", "q": 2, "bath_dimension": 2,
                      "arithmetic": "exact rational", "cases": results}, indent=2))
