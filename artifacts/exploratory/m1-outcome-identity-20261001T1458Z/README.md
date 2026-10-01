# M1 outcome-identity diagnostic: complete evidence bundle

**EXPLORATORY / NONCANONICAL / NON_EVIDENTIARY; scientific credit 0.**

The [report](../../../docs/EXPLORATORY_M1_OUTCOME_IDENTITY.md) documents an intentional
transaction/identity boundary. Exact opposite-sign outcomes reject with full supported-state
rollback. A fixed routing-only offset of 0.000001 commits on the same route but leads to tied
support and later abstention. The direct Pilot API was exercised; Session rollback is source-only.

## Contents

- `chunks/bundle.tar.gz.part-000` through `part-021`: ordered binary chunks of the complete
  original archive, without changing any archive byte
- `TRANSPORT.json`: index, name, byte length and SHA-256 for each chunk, plus original archive identity
- `BUNDLE.json`: exact archive identity, source/protocol/freeze pins, inventory and copy map
- `review/`: byte-identical readable copies of reports, frozen runner/tests/verifier/matrices,
  manifests, failure provenance, test logs and run summaries from the archive
- `verify_bundle.py`: read-only standard-library audit of the archive, all member hashes,
  readable copies, freeze identities, call accounting and corrected byte reproduction
- `verify_reproduction.py`: portable read-only comparison of fresh runs with retained
  semantic/state records, with narrowly declared execution-provenance exceptions

Concatenating the 22 chunks in listed order yields the exact original 11,449,912-byte gzip
archive, containing 3,319 files totaling 64,819,728 file bytes. Each chunk is at most 512 KiB.
Archive SHA-256:
`9b69d389eff5967d4d61b9b10174636ad544e298d7c84b6a9e3f67a306bda6cc`

Runtime source pin: `3cb955cd42474b36d2d37617e5390d08656c06f1`.
Both original and corrected source snapshots are contained in the archive. Production source
and defaults are unchanged. The corrected snapshot adds the unchanged repository schemas.

## Verify without executing the experiment

From repository root, with Python 3.11+:

```sh
PYTHONDONTWRITEBYTECODE=1 python artifacts/exploratory/m1-outcome-identity-20261001T1458Z/verify_bundle.py
```

This verifies each chunk, reconstructs the archive in memory, reads it without extraction, and
invokes no SparkBrain observation/outcome API, network service, scheduler, science workflow or
remote write. The helper independently reads all 2,304 physical checkpoint payload files and
compares them with their raw-record payloads. It recomputes all 16 corrected-run case checks,
including exact conflicts, near-alias support/probability ties, fourth-action abstention and controls.

The original frozen verifier is retained unchanged. It reused the driver's `same_state` helper
and did not explicitly assert every reported near-alias detail; its 29 checks are coupled
verification, and its process could exit zero while a printed acceptance boolean was false.
This later publication helper imports neither the archived driver nor the runtime, explicitly
asserts every acceptance boolean, and exits nonzero on validation failure. It refuses Python `-O`.
Six small synthetic corruption tests exercise intact/missing/corrupt chunk transport,
physical-checkpoint/raw mismatches and false acceptance booleans without changing the retained
bundle or executing dynamics:

```sh
cd artifacts/exploratory/m1-outcome-identity-20261001T1458Z
PYTHONDONTWRITEBYTECODE=1 python -m unittest -v test_verify_bundle
```

## Preserved failure and total budget

The original attempt omitted the trace schema from its isolated source package. It committed
zero outcomes, and its verifier then failed on an absent probe action. Every failed record,
checkpoint, frozen script and log remains inside `bundle.tar.gz`, under `run1/` and `freeze/`.
The defect belongs to diagnostic packaging/verifying, not the M1 runtime.

The separately authorized, prospectively frozen r2 correction preserves all matrix parameters
and uses fresh diagnostic IDs. It adds missing unchanged schemas and failure-safe verification.

| Attempt | Observation attempts | Outcome-delivery attempts | New commits |
|---|---:|---:|---:|
| Original packaging failure | 32 | 32 | 0 |
| Corrected r2 primary | 32 | 32 | 22 |
| Corrected r2 reproduction | 32 | 32 | 22 |
| Total | 96 | 96 | 44 |

Total public-API attempts: **192**, including the failed original attempt. Re-deliveries are
attempts, not fresh committed evidence. This is no formal/consumed identity rerun.

## Reproduce into fresh output directories

The completed fixed study is stopped. Verification above inspects its evidence without
executing the runtime. The optional recipe below performs a new local reproduction with
the unchanged frozen driver; it is not independent scientific confirmation and does not
replace or overwrite any retained attempt. Historical invocations remain in the archived
report. Use Python 3.11+ and the repository development environment (including jsonschema,
unittest and Ruff); original dependency versions are in `review/r2-run1/environment.json`.

After verifying the bundle above, run this POSIX-shell block from repository root. Each
invocation creates a fresh staging directory, and both driver output directories and the
verifier output file start absent. The archive's existing `r2-run1`, `r2-run37` and
`FINAL_VERIFICATION.json` are preserved inside the extracted evidence directory.

```sh
set -eu
artifact="$PWD/artifacts/exploratory/m1-outcome-identity-20261001T1458Z"
staging="$(mktemp -d "${TMPDIR:-/tmp}/m1-outcome-repro.XXXXXX")"
cat "$artifact"/chunks/bundle.tar.gz.part-* > "$staging/bundle.tar.gz"
tar -xzf "$staging/bundle.tar.gz" -C "$staging"
evidence="$staging/m1-outcome-identity-20261001T1458Z"
runs="$staging/fresh-runs"
mkdir "$runs"
cd "$evidence/r2-freeze"
PYTHONDONTWRITEBYTECODE=1 python -m unittest -v test_driver
python -m ruff check --no-cache --config source/pyproject.toml driver.py test_driver.py verify_results.py
cd "$evidence"
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=1 python r2-freeze/driver.py --output "$runs/primary"
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=37 python r2-freeze/driver.py --output "$runs/reproduction"
PYTHONDONTWRITEBYTECODE=1 python r2-freeze/verify_results.py --run1 "$runs/primary" --run37 "$runs/reproduction" --output "$runs/verification.json"
PYTHONDONTWRITEBYTECODE=1 python "$artifact/verify_reproduction.py" \
  --verification "$runs/verification.json" \
  --primary "$runs/primary" --replica "$runs/reproduction" \
  --retained-root "$evidence"
printf 'Fresh reproduction retained at %s\n' "$runs"
```

The final comparator checks all recorded inputs, actions, revisions, supported checkpoint
and snapshot bytes, and exception types/messages against the retained evidence. It binds the
extracted retained files to the published artifact manifest and validates each run's own raw
call digest before comparing. Two consistently wrong fresh runs cannot pass merely by agreeing
with each other.

This is portable semantic/state reproduction, not whole-directory byte identity. Only root
`environment.json` and the declared traceback text in known exception fields are treated as
execution provenance: an expected error's absolute source paths change after extraction.
Raw tracebacks and environment files remain untouched. `COMPLETED.json` may have a different
raw-call digest only after that digest has been independently validated against its own run.
All other fields and physical checkpoint/snapshot bytes remain exact comparisons; numerical
differences are reported as mismatches, not normalized away.

Failures leave the fresh outputs available for inspection; do not delete or rewrite the
original evidence to make a retry succeed. None of these reproduction commands was rerun
merely to publish this documentation repair.

## Validation and boundaries

Six corrected preflight tests and scoped Ruff pass. Both corrected processes pass all 29 frozen
checks. Their 973-file directories differ only in declared hashseed metadata; the other 972 files
are byte-identical. Checkpoints retain full supported serialized reference-brain and component
payloads, not inspection hashes alone.

No Session execution, PR #164 acceptance run, broader benchmark, full-repository acceptance,
runtime change, scientific promotion or automatic repair is claimed. Policy preflight snapshots
are historical provenance, not current authorization or scheduler state.

The freezes were local pre-execution snapshots, not an externally timestamped preregistration.
Later Git publication does not retrospectively establish external prospective registration.
A separate post-run read-only review corroborated all 768 physical checkpoint save sets,
snapshots/hashes, call continuity, frozen manifests, all 176 corrected source files against Git,
and reported near-alias/control outcomes. This is retrospective artifact review, not another
experiment or independent scientific confirmation.
