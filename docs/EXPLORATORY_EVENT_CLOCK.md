# Independent legacy evaluation-clock diagnostic

Status: executed; **EXPLORATORY / NON_EVIDENTIARY**. This file is the task-specific status and results record. PR CI and final-head review are separate integration gates.

## Question

Does an unrelated, zero-strength internal event affect admission in the legacy `sparkbrain.engine.SparkBrain` when the genuine evidence and its timestamps are unchanged?

PR #165 showed that retained Workspace capacity and admission differ in the fixed legacy gate. This follow-on isolates one narrower mechanism: global Coalition stability is counted in hypothesis-triggered evaluations. It does not change the runtime or test the M1, v03, v032, v05, SYSTEM_BUILD, or FLY-0 paths.

## Prospective scope and controls

The protocol was committed before model execution at `3a6aebfc5a00f4b3088ba7bd551957e4223e46ae`. The runner and tests were checkpointed and independently read back from GitHub at `2a5d4c0faac1f09128a32f0e8a92f6dddf26f4f7` before the first test or grid execution.

All 1,080 deterministic cells were retained:
- Three genuine-event strengths: 0.1, 0.43, 0.6
- One or two source identities, always with two distinct evidence IDs and events
- Stability requirement: 1, 2, 4
- Temporal coherence bonus: 0, 0.06
- Padding time gaps: 0, 0.01, 1
- Per combination: no variable padding, or 1/2/4 events sent to an empty hypothesis, an empty sensory Spark, or REWARD

Every arm uses one identical three-Spark engine, with no edges or broadcast listeners and firing threshold 100. Genuine events occur at t=0 and t=0.01. Padding strength is zero, has no evidence ID, and is explicitly internal. The empty hypothesis is removed from the active set before ranking; it never becomes a competitor. All arms finish with a common zero-reward time marker at t=0.01 + 4×gap, so final time is matched without a final Coalition reevaluation.

The primary contrast was fixed beforehand: strength 0.6, two sources, stability requirement 4, coherence bonus 0, and gap 0. Sensory and reward controls match padding times, priorities, and processed-event count. They do not match executed Spark-update work, which is reported separately.

Source review predicted the effects below before execution. This is a constructed implementation diagnostic, not blinded discovery or confirmatory evidence.

## Observations

### 1. Evaluation count can satisfy the stability gate

In the primary cell, two genuine observations leave the incumbent at stability 2, with score 1.4135088895. Score, margin, and source-diversity gates already pass, but the required stability is 4.

| Variable padding | Final stability | First ignition |
|---|---:|---|
| None | 2 | none |
| 1 unrelated hypothesis event | 3 | none |
| 2 unrelated hypothesis events | 4 | t=0.01 |
| 4 unrelated hypothesis events | 6 | t=0.01 |
| 1, 2, or 4 sensory events | 2 | none |
| 1, 2, or 4 reward events | 2 | none |

Thus two unrelated zero-strength hypothesis events produce first ignition without adding support, activating the padding Spark, introducing competition, or advancing elapsed time. The corresponding sensory/reward controls do not.

### 2. The coherence bonus is a distinct route

For strength 0.43, two sources, default stability requirement 2, and default bonus 0.06, the score after genuine evidence is 1.1670147042, below threshold 1.18. One same-time hypothesis padding event increases stability 2→3 and score to 1.2270147042, causing first ignition.

With the bonus set to zero, the same genuine evidence and all tested same-time padding counts remain below threshold and do not ignite. The bonus saturates at stability 4 even when the counter later reaches 6. This separates a score-threshold effect from the primary hard-stability effect.

### 3. Null and adverse controls remain visible

- All 540 one-source cells retain no ignition. The strength-0.6, zero-bonus primary control passes the score gate and isolates insufficient diversity. At strength 0.43, losing a source also removes the diversity bonus, so that condition has two blockers
- All 360 weak-evidence cells retain no ignition
- Neither sensory nor reward padding produces a first ignition in any cell; strong-evidence conditions may already have ignited before padding
- In the primary strength-0.6/stability-4/zero-bonus case, spacing padding by one second lets decay prevent ignition, unlike the same-time case
- Six cells show a repeated ignition after a prior genuine-evidence ignition. These are recorded separately and are not credited as padding-induced first onset
- A focused integrity test with padding but no genuine evidence produces no Coalition, stability credit, or ignition

There are 24 cells with first ignition during hypothesis padding and 48 corresponding treatment-versus-control onset differences across the 648 matched contrasts. These are counts of constructed cells, not success probabilities, independent samples, or evidence of general prevalence.

All 648 contrasts preserve identical genuine inputs, processed-event counts, and final horizons within each matched pair. Support dictionaries remain unchanged by padding in every episode.

## What this establishes and what remains open

The pinned legacy engine is sensitive to the count of unrelated hypothesis-triggered evaluations through both the hard stability gate and the temporal-coherence score. Its counter should not be interpreted as elapsed persistence or a count of new independent supporting observations.

This is not by itself a defect determination: evaluation-count semantics may be intentional. No runtime fix, architectural superiority, external-task performance, biological equivalence, novelty, energy efficiency, or M1 behavior is established. No scientific claim grade or formal identity changes.

A useful next question is whether event-local or elapsed-time stability can preserve intended repeated-evidence behavior while eliminating this constructed cross-task coupling under an explicit matched budget. That would require a separately scoped protocol and implementation; it is not tested here.

## Provenance and reproduction

- Base: `18ff183983a2657d7199a708e4d3398550d7740c`
- Executed source checkpoint: `2a5d4c0faac1f09128a32f0e8a92f6dddf26f4f7`
- Protocol SHA-256: `778a37f8507879f6a84f68ce0d00980542cb59932aa9b321e98f15392f088ebc`
- Runner SHA-256: `8a36eb7d8f4e40c1363aeaa3ea8e455495358c1fcc04ae1f04d4f4659fd04b70`
- Raw JSONL: 1,080 complete rows, 9,806,601 bytes; SHA-256 `00bf97d0ae8f72045abcc831ec534386a4c0d70ea764a446ed9d65bab47f2f4d`
- Summary SHA-256: `06e3706bab25d266804e8338557ee51580f11f9c8e8b132fe9fe33f77bd9a473`
- Manifest SHA-256: `8acc629a4c1ad0856796f601125c3e3eec98ed31c6991c05715438f810bc3c44`

The repository stores complete raw and summary bytes as lossless gzip files with mtime=0, alongside the uncompressed manifest and a transport manifest. The runner emits the original uncompressed three-file bundle; its manifest hashes those uncompressed bytes. Compression changes transport only.

```bash
PYTHONHASHSEED=1 PYTHONPATH=src python scripts/exploratory_event_clock.py --output /tmp/event-clock-1 --source-commit 2a5d4c0faac1f09128a32f0e8a92f6dddf26f4f7
PYTHONHASHSEED=37 PYTHONPATH=src python scripts/exploratory_event_clock.py --output /tmp/event-clock-37 --source-commit 2a5d4c0faac1f09128a32f0e8a92f6dddf26f4f7
diff -qr /tmp/event-clock-1 /tmp/event-clock-37
gzip -dc artifacts/exploratory/event_clock/raw_episodes.jsonl.gz > /tmp/retained-event-clock.jsonl
gzip -dc artifacts/exploratory/event_clock/summary.json.gz > /tmp/retained-event-clock-summary.json
cmp /tmp/retained-event-clock.jsonl /tmp/event-clock-1/raw_episodes.jsonl
cmp /tmp/retained-event-clock-summary.json /tmp/event-clock-1/summary.json
```

Two fresh processes with PYTHONHASHSEED 1 and 37 produced byte-identical raw, summary, and manifest files. Runtime sources are checked against exact Git blob pins before execution. Observer projections never enter dynamics; serialized state is checked unchanged across observation. Stored Coalition values carry their actual evaluation timestamp, separate from the final-horizon analytic projection.

## Cloud CPU validation, 2026-10-01

Python 3.12.14, full-history cloud checkout. This did not run on the user's personal computer.

| Check | Result |
|---|---|
| Focused event-clock tests | 17 passed |
| Repository configured pytest | 651 passed; 392 scientific/reproduction/external tests deselected |
| local_readiness_check | passed |
| ruff check . | passed |
| run_demo | passed, 7 frames |
| checkpoint_demo | identical normalized state after restore |
| replay_trace | passed, 7 frames, final belief cat |
| run_benchmark --episodes 40 --steps 30 | passed, 240 model/episode rows |
| validate_bundle | passed, 88 required files |

The first configured-suite attempt stopped in collection because optional torch/numpy imports were missing, including imports in deselected suites. After installing numpy 2.5.3, official CPU torch 2.13.0+cpu, and snntorch 1.0.0 in the dedicated cloud environment, the configured suite passed. CUDA was unavailable. A pre-existing non-failing Starlette/httpx deprecation warning remains. These checks do not claim execution of the 392 excluded tests.

Independent source review found no blocking correctness issue in the successful-run protocol. The failure path retains completed raw rows and error/count metadata, but a failure.json does not itself repeat the successful manifest's source/runtime hashes; external source provenance would need to accompany any future implementation-failure bundle. No full-grid failure occurred here.

## Collision boundary

The preflight inspected main policy, authoritative Human Directive index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d` on `ops/human-directives` head `8ce979b9ec0bc7eede5225c0403698f8886d3e8d`, Analyst R177, Control R153, PR #164, and current FLY-0 Forge branches.

Only dedicated event-clock protocol, runner, tests, artifacts, and this report are proposed. Shared status/ledger files were intentionally left alone while PR #164 was reconciling a status-file conflict; this report preserves the independent task's status and result. No scheduler, Control/Analyst authority, active integration work, protected evidence, formal ref, or runtime source was changed.
