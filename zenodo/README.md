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

The root .zenodo.json configures GitHub release ingestion as a preprint.
Zenodo's importer accepts one license category; **Other (Open)** represents this
mixed-license package, with CC-BY-4.0 and MIT file scopes explicitly stated in
the description and notes. LICENSE.md and the full license texts remain
authoritative; this category does not change or combine their legal terms.
After ingestion, verify the displayed metadata. The editor can additionally
display both scoped license entries. Dependencies and internal research reports
are not included.

Version 1.1.0 (2026-09-16) supersedes 1.0.0 (2026-09-15); both are versions of
one Zenodo concept record, 10.5281/zenodo.22779672. Supply a version DOI only
after assignment. The publication date is assigned by ingestion. No affiliation
or ORCID is supplied.

Reference: https://help.zenodo.org/docs/deposit/describe-records/licenses/#mixed-license-uploads .
Nothing here calls the API or creates a record.
