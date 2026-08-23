# Clean-room CPU reproduction

## Setup boundary

Python/package acquisition may use the network. The tested candidate snapshot is
`requirements-release.lock`; provenance and platform limitations are recorded separately.
External dataset acquisition is separate and is not needed by the primary smoke subset. After
setup, disconnect or otherwise block network access before running the commands below.

## Two validation modes

- **Repository mode:** `.git` and Git commands are available. Validation checks tracked-file
  completeness and requires recorded source revisions to be ancestors of `HEAD`.
- **Archive mode:** the extracted package has no `.git`. Validation uses the fixed release
  metadata and `PACKAGE_MANIFEST.json` as its source of truth, verifies cross-file revision
  agreement and every packaged file hash, and does not invoke Git.

Archive mode is a deliberate validation mode, not a fallback that suppresses Git errors.
Missing or malformed metadata, revision disagreement, unexpected files, cache files, symlinks,
or hash mismatches fail with a human-readable error.

## Offline command

Run from either the repository root or the extracted `sparkbrain_research_v0_2/` directory:

```bash
python scripts/local_readiness_check.py
python scripts/reproduce_release.py --offline --output ../sparkbrain-reproduced-release
python scripts/validate_release.py --preparation-only
python -m pytest -q
```

The output path must be outside the extracted archive root and must not exist yet. This stricter
contract permits a single atomic directory rename on Windows. Archive validation requires the
extracted tree to match its manifest exactly; writing the
reproduction output inside that tree would correctly be reported as unexpected content.
Reproduction preflight completes before publication, generation occurs in a temporary directory,
and the completed output is published atomically. A failure does not leave a partial
`status: pass` run manifest.

## Expected result

`reproduce_release.py` exits zero and emits `status: pass`. The primary Markdown table and SVG
hashes exactly match `artifacts/release/primary_subset.json`. Timing and platform fields are
descriptive and are not hash-frozen. `validate_release.py --preparation-only` reports preparation
PASS while public status remains `blocked`; before the owner chooses a license, the sole public
blocker is the owner license decision.

## Private review bundle

The private ChatGPT review bundle is a separate packaging layer:

```bash
python scripts/build_review_bundle.py --output <REVIEW_ZIP> --source-date-epoch <UTC_EPOCH>
```

The ZIP has root `sparkbrain_research_v0_2/`. Its embedded
`REVIEW_BUNDLE_MANIFEST.json` lists every ZIP entry except the manifest itself, including
`PACKAGE_MANIFEST.json`, `RELEASE_METADATA.json`, and the private-review notice. The adjacent
`<REVIEW_ZIP>.sha256` file records the ZIP SHA-256. The builder validates deterministic ordering,
timestamp and file mode, Unicode filenames, duplicates, traversal, symlinks, CRC, and per-entry
hashes. A private review bundle is not a public release and does not bypass the project-license
gate.

## Full versus smoke

The frozen primary subset is deliberately small. It is not the full C02 suite, C04 training,
matched C05 baselines, external C06 evaluation, C07 multi-world study, or C08 exploration. A
passing smoke is reproducibility engineering for selected evidence, not independent scientific
replication, and it does not raise a claim grade.
