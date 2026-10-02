# Retention preflight failure and prospective v4 recovery

Status: `EXPLORATORY_NONCANONICAL_NON_EVIDENTIARY`; scientific credit 0.
The first approved invocation failed before worker/model admission. It provides
no result about retention, novel learning, eligibility carry or the C/L hypothesis.
This change preserves that failure and prepares a separately reviewed attempt.

## Retained first attempt

The sole reported invocation used source
`2977aefc06d80291bb65c36b4b3bac0499084d0f`, published by [PR181](https://github.com/salmonmikan/sparkbrain_research/pull/181)
and merged as `2682b895435f79c9723934e2c116e440719304d8`. Its freeze-v3 SHA-256 is
`cc4dffcea78d8d82d3f5a6fc42d5474e97387b0dbcbab0377c9895233cb41834`.
The [exact invocation record](../../artifacts/research/plasticity_retention_preflight_failure_20261002/invocation.json)
retains the command, cloud checkout, output root, tool outcome and UTC window.

An explicit relative `--freeze` reached `gate()` unchanged. The gate combined
absolute source paths with relative freeze-file paths and called
`path.relative_to(ROOT)`. This raised `ValueError` for the dependencies file before
gate return, prefix extraction, pair reservation or any worker launch. The
[original terminal](../../artifacts/research/plasticity_retention_preflight_failure_20261002/result.json)
is exactly 752 bytes with SHA-256
`70a54d6f1c6b23809853e14901561bbda4aede73a885422e55a7ab6964caf223`.
It records zero reserved pairs, zero completed jobs and an empty job-cost list.

The [independent audit](../../artifacts/research/plasticity_retention_preflight_failure_20261002/independent_audit.md)
combines verified source call order with the retained terminal and file inventory.
Given the reported invocation, it supports zero worker launches, model imports,
constructors, checkpoint loads, runtime methods and H/R prediction/update rows.
Missing journals or a zero completed-pair lower bound alone would not prove this.
Source/dependency checks and Git subprocesses did consume computation. This is
source-backed admission evidence, not whole-host process attestation.

The terminal samples 0.858863051 aggregate CPU seconds, 0.7888285939989146 wall
seconds and 25,536 KiB driver peak RSS before terminal closure. These are not
complete process-lifetime measurements. The retained output is 752 bytes; adding
nominal terminal reserves would only describe headroom, not measured closure cost.

The checksum-bound [transport](../../artifacts/research/plasticity_retention_preflight_failure_20261002/transport_manifest.json)
contains all 204 preservation files, including the original terminal, invocation,
three original authority records and their separately captured hashes, independent
audit, all 193 frozen sources, dependency inventory and original manifest.
The 530,100-byte canonical archive SHA-256 is
`407a1d81cf2161e32c93be57c2eecabba54d178a3bcd0fd723606aaf6d2b57b6`.
No original output, approved source checkout or freeze-v3 bytes were changed.
The original identity remains consumed; its `UNEXECUTED` manifest field describes
the pre-execution source snapshot, not its subsequent attempt history.

## Prospective v4 attempt

The narrow repair resolves the directory inside `gate()` before any inventory
iteration or Git-relative calculation. Static dummy-gate regressions exercise
both absolute and equivalent relative paths and require identical bindings with
model admission disabled. Changing a command-line flag alone is insufficient.

The new identity is `plasticity-retention-v4-20261002`, with output root
`/workspace/shared/plasticity-retention-run-v4-20261002` and `freeze-v4-r3/`.
It requires fresh exact-source review, source publication and execution approval;
the original three authority records cannot authorize this identity. The original
attempt admitted 0 pairs and the prospective attempt has a maximum of 768, so the
combined model allocation remains 768. The runner independently pins the prior
failure bytes and records this boundary in its new manifest and terminal.

The current source-only v4-r3 manifest SHA-256 is
`7ecbf934df4ee25f65f196c732bfadcd1497a6a8a3ac8ff28193085b0facf1f3`.
It pins 198 source files and the unchanged 918-file interpreter/dependency
inventory, whose SHA-256 remains
`4415be4c41f48275151ce266f517d75765d66f8b6b2e53a500ca335ae4aaff48`.

The initial, unexecuted v4 snapshot is retained at `freeze-v4/` with SHA-256
`23f9b2f646268926793b01b9bb0e8b712c72115cb0c2bae5341469ff2c809b86`.
It is superseded because a synthetic freeze test needed to isolate its planned
output path under the test's temporary directory. Otherwise a real retained run
could make the unrelated fixture fail. Revision 2 changes only that fixture line
and the runner's default freeze location; it changes no experiment behavior,
output identity, allocation, inputs or scientific parameters. This prospective
source revision is not another execution attempt.

Revision 2 remains retained with SHA-256
`05165533ee6e1c5fda7fedcfc4a7c932659c7c095405041be245531490d37ed5`.
Review identified that the completed-run auditor did not check the new terminal
attempt/accounting fields. Revision 3 binds both fields to the independently
pinned freeze, requires exact string/integer types, and returns the audited
accounting values. Ten synthetic corruption cases cover deletion, replacement,
and false/float/string aliases. This changes data auditing only; no runtime,
input, parameter, allocation or scientific margin changes.

The [protocol](plasticity_retention_protocol_20261001.md), input bytes, labels,
jobs, seeds, C/L/G/Fw/H/R definitions, margins and resource limits are unchanged.
The existing 26 branches allocate 512 v0.5 pairs plus 256 ordinary-memory pairs.
All delays remain fixed, inherited prefixes were exposed in earlier development,
and changing eligibility decay also changes update gain. A successful new run
would still be conditional exploratory evidence, not default-model equivalence,
general retention or scientific promotion. No reserved suffix or H/R baseline
was evaluated during recovery preparation.

## Reproduction and validation

The data-only preservation verifier independently pins the archive, original
terminal and freeze, verifies every retained member and source, compares direct
copies, and reproduces the canonical archive bytes. It never imports the runtime,
replays the failed attempt or evaluates baselines:

```bash
python -S -P -B scripts/verify_retention_preflight_failure.py
python -B -m pytest -q tests/test_plasticity_retention_contract.py tests/test_plasticity_retention_runner.py tests/test_plasticity_retention_verifier.py tests/test_retention_preflight_failure.py tests/test_plasticity_retention_preparation.py
python -m ruff check .
python -S -P -B scripts/prepare_plasticity_retention_inputs.py --check
PYTHONHASHSEED=0 python -S -P -B scripts/run_plasticity_retention.py check-freeze
```

All 334 focused tests pass with Python 3.12.14, along with repository-wide Ruff,
the unchanged preparation check, preservation verifier and freeze readback.
Pytest/Ruff use the existing development virtual environment; freeze commands use
the pinned base interpreter with `-S -P -B`. The broader model-running local
readiness/demo/benchmark sequence is intentionally not invoked during this
model-free preparation. Ordinary CI remains required separately. The new output
root was absent at freeze/check time; the original terminal hash still matches.

The original [runner preparation report](plasticity_retention_runner_20261002.md)
remains a historical source-preparation record. This dated report records the
later failure and superseding preparation without rewriting that history.
