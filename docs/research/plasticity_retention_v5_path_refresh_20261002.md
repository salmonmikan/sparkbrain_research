# Prospective retention v5: writable cloud-path refresh

Status: `UNEXECUTED`, `EXPLORATORY_NONCANONICAL_NON_EVIDENTIARY`, scientific credit 0.
This is preparation only. It does not grant execution approval.

## Why a new prospective identity

The v4 source root and planned output were bound under `/workspace/shared`, which
was outside the writable roots exposed to this preparation worker when v5 was
initiated. The v4 output is absent; v4 was
not executed. The original v3 attempt remains consumed and its exact terminal
SHA-256 remains `70a54d6f1c6b23809853e14901561bbda4aede73a885422e55a7ab6964caf223`.
No attempt is replayed, no old freeze is rewritten, and no historical result is
reclassified. All existing freeze directories are preserved byte-for-byte.

The fresh prospective execution identity is `plasticity-retention-v5-20261002`.
Its source checkout is
`/workspace/scratch/f7f920cdcc9a/sparkbrain-retention-v5-20261002`,
and its planned absent output is
`/workspace/scratch/f7f920cdcc9a/plasticity-retention-run-v5-20261002`.
These are paths on the cloud computer, not the user's desktop.

## Exact bounded change

- `scripts/run_plasticity_retention.py`: fresh attempt ID and default `freeze-v5` directory
- `scripts/plasticity_retention_support.py`: fresh writable planned output path
- `tests/test_plasticity_retention_runner.py`: two synthetic cases reject a silently relocated source root or output root
- New `freeze-v5/manifest.json` and `freeze-v5/dependencies.json`; old freeze bytes remain unchanged

All other 195 source pins match v4-r3. Protocol, prepared inputs/jobs/prefixes,
production runtime, auditor, observations, seeds, arm configurations, margins,
resource limits and claim ceiling are unchanged. No dependency update is needed:
the interpreter executable and all 918 stdlib file hashes still match the original
inventory `4415be4c41f48275151ce266f517d75765d66f8b6b2e53a500ca335ae4aaff48`.

The new manifest SHA-256 is
`272ed83bd0a520d8fc80a6e54b6145eaae76333f8866cba0d780bae76746a0b9`.
It pins 198 source files. This freeze must be superseded by another new revision
if later integration changes any pinned source; never overwrite this snapshot.

## Model-free preparation validation

All 336 focused tests pass with Python 3.12.14. Repository-wide Ruff, immutable
input regeneration check, preservation archive audit, and new freeze readback
pass. The archive remains 204 files / 530,100 bytes with SHA-256
`407a1d81cf2161e32c93be57c2eecabba54d178a3bcd0fd723606aaf6d2b57b6`.

Commands used:

```sh
PYTHONHASHSEED=0 python -S -P -B scripts/run_plasticity_retention.py freeze
PYTHONHASHSEED=0 python -S -P -B scripts/run_plasticity_retention.py check-freeze
python -B -m pytest -q -p no:cacheprovider tests/test_plasticity_retention_contract.py tests/test_plasticity_retention_runner.py tests/test_plasticity_retention_verifier.py tests/test_retention_preflight_failure.py tests/test_plasticity_retention_preparation.py
python -B -m ruff check .
python -S -P -B scripts/prepare_plasticity_retention_inputs.py --check
python -S -P -B scripts/verify_retention_preflight_failure.py
```

Pytest and Ruff use the pre-existing development environment. Freeze and
preservation checks use the pinned base interpreter. These tests are synthetic
and model-free; no reserved suffix or ordinary-memory study baseline is evaluated.
No broad runtime/demo/benchmark sequence was run as part of this preparation.

## Remaining gates and one-shot execution

PR182 was merged as `a6aa0addfcd8f73b72a796ebd8c5625a0a2347dd`. Its 49-path
dependency set is reconciled into this preparation, retaining both results-ledger
entries and the equivalent synthetic output-isolation fix. All 198 v5 source pins
still match: no further freeze revision is needed. Independent model-free review
found no blocker in the path-only refresh. Any later affected pinned bytes require
a new, append-only freeze revision and renewed independent model-free source
review. Final-head CI and source review, publication
readback, output absence, all source/dependency pins and fresh explicit exact-freeze
execution approval remain required. v3 authority and v4 review do not authorize v5.

Three externally established authority JSON records are required: review,
publication and approval. Each binds the exact final source commit, manifest
SHA-256, output root, integer ceiling 768, nonempty record URL and recorded-by
identity. They respectively assert `source_review_approved`, `verified_published`
and `approved_for_execution`. Preserve original bytes and independently capture
their SHA-256 values before execution. Never infer approval from a generated file.

Proposed command, only after all gates and explicit parent clearance:

```sh
cd /workspace/scratch/f7f920cdcc9a/sparkbrain-retention-v5-20261002
PYTHONHASHSEED=0 python -S -P -B scripts/run_plasticity_retention.py run --output /workspace/scratch/f7f920cdcc9a/plasticity-retention-run-v5-20261002 --freeze artifacts/research/plasticity_retention_execution_20261001/freeze-v5 --review /workspace/scratch/f7f920cdcc9a/retention-v5-authority-20261002/review.json --publication /workspace/scratch/f7f920cdcc9a/retention-v5-authority-20261002/publication.json --approval /workspace/scratch/f7f920cdcc9a/retention-v5-authority-20261002/approval.json
```

If a later freeze revision is required, its separately approved directory and
hash must replace this proposed command's freeze argument prospectively.
The command has not been invoked and these authority records have not been minted.
Preflight all read-only checks before invoking `run`: the driver creates its output
directory before admission checks, so a failed invocation must never be treated as
permission for an automatic retry.

## Allocation and stopping conditions

The combined original-plus-new maximum remains 768 prediction/outcome pairs:
512 v05 and 256 H/R pairs across 26 sequential branches. No new prefix training,
extra probes, replay, retry, parameter search or baseline evaluations are allocated.
The allowed wrapper constructions/native loads/nested v05 constructions remain
26/18/36 respectively.

Limits remain 360 aggregate CPU seconds, 480 overall wall seconds, 512 MiB address
space per process, and 256 MiB output including its 4 MiB terminal reserve. v05
workers have 16 CPU/20 wall seconds; H/R workers have 3/5. Driver closure reserves
2 CPU/5 wall seconds within the aggregate allowance. Each stdout/stderr cap is
64 KiB. Offline enforcement is a Python socket audit hook, not OS network isolation.

Any integrity, measurement, logging, process or resource failure stops subsequent
admission and preserves partial data. No clean rerun follows failure. A completed
run requires independent data-only audit using independently captured final-source,
freeze and original authority-record pins, then durable publication/readback before
reporting a bounded finding. No scientific promotion follows CI, review or execution.
