"""Focused failure controls for the dependency guard; no Lean theorem claims."""
from pathlib import Path
from axiom_guard import check_axiom_output

root = Path(__file__).resolve().parent
record = (root / "LEAN-CHECK.txt").read_text(encoding="utf-8")
for name in ["ActiveBath.lean", "BlockAccounting.lean"]:
    source = (root / name).read_text(encoding="utf-8")
    part = record.split("CHECK " + name, 1)[1].split("EXIT 0", 1)[0]
    assert check_axiom_output(source, part) == source.count("#print axioms")
source = "#print axioms target\n"
good = "'N.target' depends on axioms: [propext, Classical.choice, Quot.sound]\n"
assert check_axiom_output(source, good) == 1
assert check_axiom_output(source, "'N.target' does not depend on any axioms") == 1
bad_cases = [
    (source, good.replace("Quot.sound", "fabricatedEntropyTheorem")),
    (source, ""),
    (source, good + good),
    (source, good + "sorryAx"),
    (source + "axiom unusedScientificClaim : True\n", good),
    ("", good),
]
for src, output in bad_cases:
    try:
        check_axiom_output(src, output)
    except ValueError:
        pass
    else:
        raise AssertionError("Guard accepted invalid dependency output")
print("PASS: both recorded source dependency sets; allowed/empty sets; six rejection controls")
