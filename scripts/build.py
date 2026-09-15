"""Build manuscript.tex from the distribution root; never overwrite its PDF."""
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[1]
out = root / "build"
out.mkdir(exist_ok=True)
for _ in range(3):
    result = subprocess.run([
        "pdflatex", "-interaction=nonstopmode", "-halt-on-error",
        "-output-directory=" + str(out), str(root / "manuscript.tex")],
        cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, timeout=40)
    if result.returncode:
        print(result.stdout[-12000:])
        raise SystemExit(result.returncode)
log = (out / "manuscript.log").read_text(errors="replace")
for marker in ["undefined references", "undefined on input", "Overfull", "multiply defined"]:
    assert marker not in log, marker
print("PASS: three TeX passes; build/manuscript.pdf; no undefined references or overfull boxes")
