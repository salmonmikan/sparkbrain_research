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

Validation reports four explicit classes: `integrity_problems`, `preparation_problems`,
`owner_blockers`, and `evidence_blockers`. `--preparation-only` exits zero only when the first,
second, and fourth classes are empty. The unselected owner license may remain as the sole
`owner_blockers` entry with `status: blocked` and `preparation_status: pass`.

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

The order is part of the contract. The validator checks a pristine extracted tree before the
runtime pytest phase. Pytest disables its cache provider and puts `tmp_path` data in a sibling
directory without requiring a manual environment variable. Python may
still create an interpreter cache while importing the test bootstrap, so a later pristine audit
must use a newly extracted copy. Initial archive cache content remains forbidden; runtime cache
is never included in `PACKAGE_MANIFEST.json` or a release ZIP.

Before output or staging creation, reproduction performs this preflight order:

1. output-path guard;
2. metadata schema/hash/version/count validation;
3. manifest hashes and repository/archive completeness;
4. cross-file source-revision agreement;
5. required generated-evidence and primary-subset validation;
6. primary input hash validation;
7. local readiness, in-memory rendering, staged hash validation, and atomic rename.

## Expected result

`reproduce_release.py` exits zero and emits `status: pass`. The primary Markdown table and SVG
hashes exactly match `artifacts/release/primary_subset.json`. Timing and platform fields are
descriptive and are not hash-frozen. `validate_release.py --preparation-only` reports preparation
PASS with empty integrity/preparation/evidence classes while public status remains `blocked`;
before the owner chooses a license, the sole public blocker is the owner license decision. Any
manifest, metadata, revision, provenance, or tree tamper returns `status: invalid`, preparation
FAIL, exit 1, and no traceback.

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

### v0.3 source review bundle

For a Git checkout used to regenerate v0.3 source bytes, set `core.autocrlf=false` before
checkout. The source manifest and deterministic private-review ZIP bind actual file bytes; line
ending conversion would create a different source snapshot. This setting is not needed to inspect
an already extracted no-Git review bundle.

Before the final v0.3 package manifest is generated, the source-only private review layer uses:

```bash
python scripts/build_v03_private_review_bundle.py --output <REVIEW_ZIP> --source-date-epoch <UTC_EPOCH> --source-revision <FULL_GIT_SHA>
```

The bundle embeds `SOURCE_MANIFEST.json`, `REVIEW_BUNDLE_MANIFEST.json`, and the private-review
notice under `sparkbrain_research_v0_3/`. Its manifest is sufficient to verify every selected
file after extraction without `.git`; it does not make the snapshot a public release. The final
v0.3 no-Git reproduction archive remains a separate C20 artifact generated only after the source
revision and release evidence are fixed.

## Full versus smoke

The frozen primary subset is deliberately small. It is not the full C02 suite, C04 training,
matched C05 baselines, external C06 evaluation, C07 multi-world study, or C08 exploration. A
passing smoke is reproducibility engineering for selected evidence, not independent scientific
replication, and it does not raise a claim grade.
