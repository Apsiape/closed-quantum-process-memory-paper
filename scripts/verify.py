"""Check this distribution in place; no original repository or network is needed."""
from pathlib import Path
import argparse
import hashlib
import json
import re
from pypdf import PdfReader

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--rebuilt", type=Path, help="Compare a rebuilt PDF's page text and metadata")
args = parser.parse_args()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

manifest = root / "SHA256SUMS.txt"
assert b"\r" not in manifest.read_bytes(), "Manifest must use LF"
expected = set()
for line in manifest.read_text(encoding="utf-8").splitlines():
    digest, name = line.split("  ", 1)
    path = (root / name).resolve()
    assert path.is_relative_to(root) and name not in expected
    expected.add(name)
    assert sha(path) == digest, name
actual = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()
          and not any(x in p.relative_to(root).parts for x in [".git", "build", "__pycache__", ".lake"])}
assert actual == expected | {"SHA256SUMS.txt"}, "Missing or unexpected distribution files"

names = ["manuscript.md", "appendix-causal-balancing.md", "appendix-conventions.md"]
md = "\n".join((root / name).read_text(encoding="utf-8") for name in names)
complete = (root / "COMPLETE-PROOF.md").read_text(encoding="utf-8")
for name in names:
    assert (root / name).read_text(encoding="utf-8") in complete, name
tex = (root / "manuscript.tex").read_bytes().decode("utf-8")
labels = re.findall(r"\\label\{([^}]+)\}", tex)
refs = re.findall(r"\\(?:eqref|ref)\{([^}]+)\}", tex)
assert len(labels) == len(set(labels)) and set(refs) <= set(labels)
keys = re.findall(r"\\bibitem\{([^}]+)\}", tex)
cites = {k.strip() for group in re.findall(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}", tex)
         for k in group.split(",")}
assert len(keys) == len(set(keys)) == 35 and cites == set(keys)
assert len(re.findall(r"^\d+\. ", md, re.MULTILINE)) == len(keys)
statements = set(re.findall(r"^(Theorem|Lemma|Proposition|Corollary|Definition) ([\dAB]+\.\d+)",
                            md, re.MULTILINE))
envs = re.findall(r"\\begin\{(theorem|lemma|proposition|corollary|definition)\}", tex)
assert len(statements) == len(envs) == 23
for kind in {kind for kind, _ in statements}:
    assert envs.count(kind.lower()) == sum(k == kind for k, _ in statements)
urls = set(re.findall(r"\\href\{((?:https?://|mailto:)[^}]+)\}", tex))

def inspect_pdf(path):
    reader = PdfReader(path)
    assert reader.metadata.title == md.splitlines()[0].removeprefix("# ")
    assert reader.metadata.author == "Seth Douglas"
    pages = [p.extract_text() for p in reader.pages]
    assert len(pages) == 29 and all(p.strip() for p in pages)
    flat = re.sub(r"\s+", " ", "\n".join(pages))
    assert "??" not in flat and "seth.douglas@gmail.com" in pages[0]
    for kind, number in statements:
        assert re.search(kind + r"\s*" + re.escape(number) + r"(?!\d)", flat), (kind, number)
    for heading in ["AI assistance", "Complete causal balancing proof",
                    "Conventions, resources and references", "Primary bibliography and exact uses"]:
        assert heading in flat, heading
    links = set()
    for page in reader.pages:
        for ref in page.get("/Annots", []):
            action = ref.get_object().get("/A")
            if action and action.get("/URI"):
                links.add(str(action["/URI"]))
    assert urls <= links
    return pages

pages = inspect_pdf(root / "manuscript.pdf")
if args.rebuilt:
    rebuilt = args.rebuilt if args.rebuilt.is_absolute() else root / args.rebuilt
    assert inspect_pdf(rebuilt) == pages, "Rebuilt PDF page-text drift"
    print("PASS rebuilt PDF: exact extracted page text, metadata, statements and links")

mapping = json.loads((root / "SOURCE-MAP.json").read_text(encoding="utf-8"))
for name, item in mapping["files"].items():
    assert sha(root / name) == item["export_sha256"], name
    if item["operation"] == "exact-copy":
        assert item["source_sha256"] == item["export_sha256"], name
body = tex[tex.index("\\documentclass"):]
assert hashlib.sha256(body.encode("utf-8")).hexdigest().upper() == mapping["tex_body_sha256"]
zenodo = (root / "zenodo/README.md").read_text(encoding="utf-8")
assert "mixed-license-uploads" in zenodo and "CC BY 4.0" in zenodo and "MIT" in zenodo
assert "Douglas, Seth" in zenodo and "seth.douglas@gmail.com" in zenodo
release = json.loads((root / ".zenodo.json").read_text(encoding="utf-8"))
assert release["license"] == "other-open"
assert release["title"] == md.splitlines()[0].removeprefix("# ")
assert release["creators"] == [{"name": "Douglas, Seth"}]
assert release["upload_type"] == "publication" and release["publication_type"] == "preprint"
assert release["version"] == "1.1.0"
assert all(term in release["description"] for term in ["CC-BY-4.0", "MIT", "partial", "1.1.0"])
citation = (root / "CITATION.cff").read_text(encoding="utf-8")
assert citation.count("version: 1.1.0") == 2
assert citation.count("doi: 10.5281/zenodo.22788806") == 2
assert "repository-code: https://github.com/Apsiape/closed-quantum-process-memory-paper" in citation
for name in expected:
    path = root / name
    if path.suffix in {".md", ".tex", ".py", ".json", ".cff", ".txt"} and not name.startswith("LICENSES/"):
        content = path.read_text(encoding="utf-8")
        assert all(line == line.rstrip() for line in content.splitlines()), name
assert "HOLD" not in "\n".join(pages)
print(f"PASS {len(expected)} hashes; complete proof; 23 statements; 35 references; {len(urls)} links; 29 pages")
print("PASS source provenance, clean metadata, scoped licenses and portable layout")
print("PDF SHA256 " + sha(root / "manuscript.pdf"))
