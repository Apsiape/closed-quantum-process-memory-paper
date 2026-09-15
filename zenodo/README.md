# Preparing a Zenodo record

This combined manuscript-and-code package can be described in one record. Zenodo
supports mixed-license uploads: declare both CC BY 4.0 and MIT and explain their
file-specific scope. Separate records or DOIs are not required.

Suggested record fields:

- Title: Bath dimension and initial entropy for closed repeated use of a quantum channel
- Resource type: Publication / Preprint
- Creator: Douglas, Seth
- Public contact in the description: seth.douglas@gmail.com
- Description: Manuscript and reproducibility materials for the dimension and
  actual initial-entropy rate region of a closed device serving repeated uses of
  one fixed quantum channel against adaptive inputs. Lean coverage is partial:
  a finite quantum closing identity and six arithmetic lemmas, not the full
  entropy or asymptotic theorem. AI assistance is disclosed in the manuscript.

Declare CC BY 4.0 for the manuscript and its representations:

- manuscript.pdf
- manuscript.tex
- manuscript.md
- appendix-causal-balancing.md
- appendix-conventions.md
- COMPLETE-PROOF.md
- LICENSES/CC-BY-4.0.txt

Declare MIT for original code in ancillary/ and scripts/ and its accompanying
software documentation. Include LICENSES/MIT.txt and the top-level LICENSE.md.
Third-party dependencies and imported rights are not relicensed.

The same combined archive is suitable for GitHub and manually described Zenodo
staging. There is no root .zenodo.json: automatic multi-license ingestion has not
been validated, so the license fields should be entered and checked in the UI.
Dependencies and internal research reports are not included.

Supply a genuine DOI, optional release version and actual publication date only
when available. No affiliation or ORCID is supplied. Do not infer identifiers or
a public release version from these local filenames.

Reference: https://help.zenodo.org/docs/deposit/describe-records/licenses/#mixed-license-uploads .
Nothing here calls the API or creates a record.
