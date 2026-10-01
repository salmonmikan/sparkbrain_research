# M1 outcome identity boundary: bounded exploratory diagnostic

Status: **EXPLORATORY / NONCANONICAL / NON_EVIDENTIARY**. Scientific credit: **0**.
Date: 2026-10-01 UTC. Runtime source: `3cb955cd42474b36d2d37617e5390d08656c06f1`.

Publication edition: the [complete retained bundle](../artifacts/exploratory/m1-outcome-identity-20261001T1458Z/README.md)
contains the immutable original `REPORT.md` and all raw/provenance bytes. This reader-facing
edition adds navigation and publication context only; runtime observations and limitations are
unchanged. Artifact paths below are relative to the extracted bundle root unless linked otherwise.

## Result

The corrected eight-case diagnostic confirms the source-predicted boundary in both
constructed contexts. At exactly repeated routing features, a fresh opposite-sign outcome
is rejected by SB002's intentional `identical_observation_conflict` contract. The complete
supported serialized pre-outcome state is restored. The direct Pilot API retains its
original pending observation, so the fourth fresh observation is rejected.

A fixed routing-only offset of `0.000001` permits the opposite-sign outcome to commit
on the same learned route in both contexts. This is **not successful adaptation**: the
predictive bank splits, route-local supports tie, and the fourth observation abstains.

No runtime defect, scientific support, robustness, natural-noise behavior, comparative
performance, composition contribution or novelty is established. No runtime change is proposed
as an automatic consequence of this result.

## Fixed cases and observed outcomes

Each case starts with a fresh default `IntegratedM1Pilot`, bootstraps signal/routing `0.0`
with outcome `+0.8`, then `0.45` with outcome `-0.8`. Probe sensory signal remains exactly
the target; only routing can receive the fixed offset. Times are 0, 1, 2, 3. All receipt
magnitudes are 0.8. Each case then re-delivers its probe receipt once and attempts the fourth
observation without supplying another fresh outcome.

| Target | Arm | Probe result | Probe route | Fourth observation |
|---|---|---|---|---|
| 0.0 | original | commits | scope-00000001 | act_alpha |
| 0.0 | exact reversal | identical_observation_conflict | no commit | pending-event rejection |
| 0.0 | near-alias reversal | commits | scope-00000001, unchanged | abstain |
| 0.0 | null perturbation | commits | scope-00000001, unchanged | act_alpha |
| 0.45 | original | commits | scope-00000002 | act_beta |
| 0.45 | exact reversal | identical_observation_conflict | no commit | pending-event rejection |
| 0.45 | near-alias reversal | commits | scope-00000002, unchanged | abstain |
| 0.45 | null perturbation | commits | scope-00000002, unchanged | act_beta |

Route tokens are literal identities for this fixed arrival order, not semantic class names.
This matrix is a constructed boundary check, not an accuracy or success-rate sample.

### Exact reversal

- Both first delivery and retry raise `RuntimeError: scope revision rejected: identical_observation_conflict`
- Predictive hypotheses, scoped router/support/evidence/identity state, reference-brain checkpoint,
  compositor event/receipt bindings, trace, sequence and pending state are equal to the pre-outcome values
- Sequence remains 2; only the two bootstrap outcomes are committed
- The third observation remains pending; the fourth raises
  `later outcome must resolve the pending event before another observe`
- The rejected receipt never enters the committed receipt ledger; its second delivery is a retry,
  not duplicate committed evidence

### Near-alias reversal

- Both probes keep their pre-probe route token and commit sequence 3
- The explicit predictive bank creates `state-003` with the opposite outcome at the same sensory context;
  the two bootstrap states remain unchanged
- The affected route has alpha support 0.8 and beta support 0.8, probabilities 0.5/0.5,
  confidence 0.5, margin 0.0 and no selected candidate
- The fourth observation is accepted but returns `abstain`, reason
  `predictive_competing_hypotheses_ambiguous`, prediction null, route candidate null

### Original and null controls

All four probes commit, the exact re-delivery returns the same prior revision without state
change or sequence increment, and the fourth action agrees with the original candidate.
The near-alias receipt re-deliveries are likewise state-neutral. Each successful probe case
has three newly committed outcomes. Its fourth observation is intentionally left pending by
the fixed stopping rule; this is distinct from the exact-reversal cases retaining the third.

## Full-state verification and reproducibility

Every call has before/after inspection plus full parsed canonical payloads from the supported
`PilotCheckpointManager.save` and `ScopeRevisionCheckpointManager.save` APIs. This includes
the direct v032 `reference-brain.json`, predictive `pilot-state.json` and `sb002-state.json`.
The reference serializer retains fields absent from inspection, including CoalitionGate stability
and signatures and RNG state. No serializer field was discarded for state comparisons.

At each of 128 snapshots per process, two separate no-clobber checkpoint saves were read back,
compared in full and checked against unchanged inspection/state hash. All repeated-save and
state-neutrality checks passed. Each rejected call had equal complete serialized components
and compositor inspection fields before/after. This is stronger than inspection-hash equality alone,
but remains a claim about the supported serialization contract, not arbitrary uncaptured process state.

Both corrected processes pass all 29 frozen read-only verification checks. One fresh process
using `PYTHONHASHSEED=37` reproduces the primary `PYTHONHASHSEED=1` process. Each output directory
contains 973 files: all 972 non-environment files are byte-identical. The sole differing file,
`environment.json`, differs only in `pythonhashseed`. Raw calls SHA-256 for both:

`dc37ae6df77da579b75fa6795374265f77cea407a7c15def790b223e6ee6cd29`

This reproduction is a tooling determinism check and provides no independent scientific evidence.

## Preserved failed first attempt and honest budget

The first isolated source archive omitted repository-relative schema assets. All 32 observation
attempts failed with a missing `schemas/trace-v0.3.schema.json`; all 32 outcome deliveries lacked
a pending observation. No bootstrap or probe outcome committed, so the identity question was
not tested. All raw records and supported checkpoints are retained in `run1/`.

The original read-only verifier then raised TypeError because it assumed the probe action existed.
Its original source, logs and manifest remain unchanged. The first environment metadata also
understated dependencies as standard-library-only; corrected metadata records jsonschema and its
installed dependencies. These are packaging/reporting defects in this diagnostic, not M1 defects.

The parent authorized a science-invariant correction under a fresh r2 exploratory attempt.
R2 adds unchanged pinned schemas, a failure-safe verifier and regression/dependency checks,
correct dependency metadata and fresh r2 event/receipt IDs. Every scalar, arm, time, threshold,
default and bootstrap order remains unchanged. Exact source blob matching and matrix equivalence
except fresh identities were verified before r2 execution. The failed attempt was not overwritten
and its unused reproduction was not run.

| Attempt | Observation attempts | Outcome-delivery attempts | Newly committed outcomes |
|---|---:|---:|---:|
| Original packaging failure | 32 | 32 | 0 |
| Corrected r2 primary | 32 | 32 | 22 |
| Corrected r2 reproducibility | 32 | 32 | 22 |
| Total actual calls | 96 | 96 | 44 |

Repeated receipt deliveries are included in attempts, not counted as new commits. Equal attempted
calls are not a claim of equal computational work. No formal/consumed scientific identity was used.

## Pilot versus Session boundary

Only `IntegratedM1Pilot.observe` and `apply_outcome` were executed. The Session distinction is
**source-backed only**: `IntegratedM1Session.cycle` saves before obtaining the observation and
restores both pilot and world if any inner step raises. Consequently the direct-Pilot retained-pending
result is not a demonstrated Session deadlock or system-wide liveness failure. No Session cycle,
modified world or PR #164 acceptance harness was executed in this diagnostic.

Relevant pinned source:
- [Exact-observation consistency guard](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/system_build/causal_scope_revision.py#L539-L614)
- [M1 outcome sign mapping and rollback](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/system_build/integrated_m1.py#L444-L525)
- [Session whole-cycle rollback](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/system_build/integrated_m1.py#L633-L663)
- [Existing intentional transaction contract](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/docs/SYSTEM_BUILD_M1.md#L46-L63)

## Provenance and artifact map

- `freeze/`: original prospective protocol, driver, matrix, policy snapshots, source and failure-prone verifier
- `run1/`: complete retained packaging-failure attempt; `FAILED_ATTEMPT.json` summarizes its limitation
- `r2-freeze/`: corrected prospective contract, source plus schemas, matrix, driver, verifier, six preflight tests
- `r2-run1/`, `r2-run37/`: corrected primary and reproduction, full checkpoints and records
- `FINAL_VERIFICATION.json`: frozen verifier results and exact whole-file reproduction comparison
- Process logs and original/corrected test logs are retained separately

Original freeze manifest SHA-256:
`c7f81d594765d93949730fa188335d84f4f3133d90773b2f676453ab510c80b8`

Corrected r2 freeze manifest SHA-256:
`f3c9a2a334df87cf6820c017bcbdcdcb9dc8a801d294264f09675f96c91e36c8`

These are local pre-execution freezes and locally recorded timestamps, not an externally
timestamped preregistration. Subsequent Git publication preserves the evidence but does not
retrospectively create external prospective registration.

Runtime is CPython 3.12.14 on Linux x86-64, CPU-only. Installed validation dependencies:
jsonschema 4.26.0, referencing 0.37.0, attrs 26.1.0, rpds-py 2026.6.3,
jsonschema-specifications 2025.9.1. The driver invokes no network service.
No package was installed and no external compute was purchased for this diagnostic.

Core commands, executed from this artifact directory:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=1 python freeze/driver.py --output run1
PYTHONDONTWRITEBYTECODE=1 python freeze/verify_results.py --run1 run1 --output primary-verification.json
# Original verifier failure is retained; fresh r2 correction was frozen before the next calls
cd r2-freeze
python -m ruff check --no-cache --config source/pyproject.toml driver.py test_driver.py verify_results.py
PYTHONDONTWRITEBYTECODE=1 python -m unittest -v test_driver
cd ..
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=1 python r2-freeze/driver.py --output r2-run1
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=37 python r2-freeze/driver.py --output r2-run37
PYTHONDONTWRITEBYTECODE=1 python r2-freeze/verify_results.py --run1 r2-run1 --run37 r2-run37 --output FINAL_VERIFICATION.json
```

The executable used was the pre-existing cloud venv shown in each environment file. Output paths
are no-clobber; the commands above document actual invocations and will not overwrite existing data.

## Historical diagnostic authority, completion and limits

Fresh preflight fetched current AGENTS/policy from main, then active Human Directives at
head `8ce979b9ec0bc7eede5225c0403698f8886d3e8d`, index blob
`1ba1e173344f36e14d0e21e6f3e823254e031f7d`. Analyst R177, Control R153 and MAIN R222
were read for collision avoidance. PR #164 and its HOLD MERGE remained separate. No scheduler,
Control/Analyst/MAIN state, shared status ledger, repository file, protected evidence or remote ref
was written during the diagnostic execution. The original task assumed no scheduler-role
authority and created no PR. These are historical pre-publication facts: subsequent explicit
user authorization permits same-repository evidence publication and a cohesive PR with the
source runtime map. The bundled original report remains unchanged.

Scoped driver Ruff and six corrected preflight tests pass. The full repository suite, standard demo,
benchmark, local-readiness script, bundle validator and M1 acceptance suite were not run because
the task was a fixed standalone diagnostic without production source changes. No broader project
acceptance claim is made.

The bounded matrix and its single corrected reproduction are complete. Execution has stopped.
The next decision is whether exact-feature candidate consistency is the intended integrated
capability boundary for genuine changed outcomes. Any alternative contract or architecture requires
a separately authorized fresh design; no automatic repair, expanded grid or scientific promotion follows.

## Publication validation

The publication wrapper includes a readable frozen runner/test/verifier surface, transparent SHA-256
manifests, the complete 11,449,912-byte archive as 22 checksum-bound binary transport chunks,
and a standard-library read-only bundle verifier.
The verifier executes no archived source and does not re-run the diagnostic. Its local validation
passed: all 3,319 archived file hashes, all 43 review-copy byte comparisons, both frozen manifests,
192-call accounting and 972-file corrected non-environment reproduction matched. The later helper
also independently compares 2,304 physical checkpoint payload files against raw records and
recomputes all 16 corrected-run case checks, including near-alias ties and fourth-action behavior.
The frozen 29-check verifier remains unchanged and is coupled to the driver's `same_state` helper;
it did not explicitly assert every near-alias detail, and its process could exit zero while
a printed acceptance boolean was false. The publication helper imports no archived driver/runtime
code, explicitly asserts every acceptance boolean, and exits nonzero on validation failure.
It refuses optimized Python `-O`. Six synthetic corruption tests cover intact/missing/corrupt chunks,
checkpoint/raw mismatches and false acceptance booleans without dynamics. Scoped Ruff for the
added helper passed. A separate retrospective read-only review corroborated all 768 physical
checkpoint save sets, snapshots/hashes, call continuity, frozen manifests, all 176 corrected source
files against Git, and reported near-alias/control outcomes. It is post-run artifact review,
not another experiment or independent scientific confirmation.
Broader repository validation and exact published-head CI are
the responsibility of the publication pass and must be reported separately rather than inherited
from these diagnostic checks.

### Repository publication checks, 2026-10-01 UTC

The cloud CPU publication worktree passed the configured repository suite: **654 passed,
392 scientific/reproduction/external tests deselected**. Two added pytest checks validate
only retained artifact bytes and invoke the six synthetic corruption tests. The production
runtime and frozen diagnostic files remain unchanged. The standard regression suite also
exercises existing runtime fixtures; those regression calls are separate from the diagnostic
call-budget table and are not additional executions of its matrix.

Ruff, local readiness, the seven-frame standard demo, the 40-episode/30-step benchmark
(240 model/episode rows), and bundle validation (88 required files) passed. Python was
3.12.14 in the existing cloud CPU environment. A pre-existing, non-failing Starlette/httpx
warning remains. No package installation or new runtime dependency was needed.
Exact published-head CI and Codex review are separate PR integration checks; these local
results do not claim those checks have already completed.
