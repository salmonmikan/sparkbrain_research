# CX01 Implementation Status

Status: **STRUCTURAL HELD-OUT CORRECTION UNDER REVIEW — no new formal candidate opened**

## Current scientific boundary

Historical evidence remains unchanged:

```text
v0.6.1 Candidate-003: CONSUMED
Primary:              NOT SUPPORTED
G3/G4/G5:             SUPPORTED
```

CX01 development evidence also remains development-only:

```text
30 worlds × 7 comparators = 210 executions
G3    15 / 30
G4    15 / 30
G5    15 / 30
G6    20 / 30
G7    20 / 30
G8-P  20 / 30
G8-R  25 / 30
CYCLE all comparators 0 / 5
```

No threshold, comparator, development world, or development training schedule has been changed to improve those outcomes.

## Candidate-001 disposition

The first CX01 outcome-blind package was rejected before STARTED:

```text
freeze ref:    freeze/cx01-001
source SHA:    f2c5ead5afda7d731033d585511ea68dc066a162
candidate:     cx01-candidate-001
seeds:         269810..269819
verdict:       REJECTED PRE-START
seal:          NOT ISSUED
STARTED:       NOT CREATED
formal run:    NOT EXECUTED
```

Reason: fresh numerical seeds mostly produced development-equivalent world structures under anonymous token relabeling. Candidate-001 and seeds `269810..269819` are permanently non-formal and may never be reused as confirmatory evidence.

`freeze/cx01-001` remains unchanged as the auditable rejected freeze record.

## Structural-heldout protocol v2

Current implementation branch:

```text
research/cx01-structural-heldout-generator
PR #23
```

Protocol version:

```text
cx01-comparator-protocol-2
```

The correction is formal-only. `src/sparkbrain/comparison/cx01/worlds.py` and the historical development grid remain unchanged.

Implemented v2 controls:

| Control | Status |
|---|---|
| Separate formal-only world generator | IMPLEMENTED |
| Token-renaming-invariant structural signature | IMPLEMENTED |
| Development-structure overlap rejection | IMPLEMENTED |
| Minimum five unique structures/family | IMPLEMENTED |
| Outcome-blind analytical identifiability audit | IMPLEMENTED |
| Deterministic exact-source-SHA-bound seed selection | IMPLEMENTED |
| Candidate-001 generation/seed rejection | IMPLEMENTED |
| Protocol-v1 candidate rejection | IMPLEMENTED |
| Structure audit hash in freeze manifest | IMPLEMENTED |
| Identifiability audit hash in freeze manifest | IMPLEMENTED |
| Seed-selection hash in freeze manifest | IMPLEMENTED |
| Formal runner revalidates all three before capability | IMPLEMENTED |
| Frozen scorer revalidates candidate world hashes | IMPLEMENTED |
| Frozen scorer recomputes training transcript hashes | IMPLEMENTED |
| Prepare bundle emits seed/structure/identifiability audit files | IMPLEMENTED |
| New formal candidate | **NOT SELECTED / NOT OPENED** |
| Independent seal | **NOT ISSUED** |
| STARTED | **NOT CREATED** |
| Formal capability | **NOT EXECUTED** |

## Formal-only structural variation

The v2 generator varies more than anonymous labels:

- HIGH_ORDER: history topology, lag values, exposure counts;
- TIMING: longer token prefix plus seed-dependent matched-duration timing signatures;
- CYCLE: new seven-phase recurrent contingency schedules and exposure counts;
- BRANCH: longer prefix topology, new exposure ratios, new lags;
- SELECTIVITY: longer matched disjoint paths, new timing/exposure values;
- LOOP: longer cue/provenance topology, new timing/exposure values.

Any candidate world token-renaming-equivalent to a development world fails closed before capability.

## Formal candidate selection contract

Future formal seeds are not chosen manually. For a fixed source SHA and generation ID, the selector deterministically derives high-range seed blocks and may skip a block only if:

- CandidateSpec validation fails;
- structural-heldout audit fails; or
- analytical identifiability audit fails.

Comparator models and capability outcomes are unavailable to this selection procedure.

The selected block and selection hash are retained in `formal_seed_selection.json` and `freeze_manifest.json`.

## Development invariance checkpoint

At source commit `94dfbf286362e75460b593acd96299b938d1458d`, the unchanged development workflow completed successfully and the resulting 210 rows were compared directly with the exact-parent baseline artifact.

For all 210 records, the following were identical:

```text
kind
family
seed
world_hash
training_transcript_hash
evidence
decision
```

Resource wall/CPU/memory measurements remain descriptive and are intentionally not byte-stability requirements.

A final invariance comparison is still required for the exact PR #23 merge SHA before a new source freeze is declared.

## Next boundary

The required sequence is:

```text
PR #23 review + green CI
  -> merge to research/cx01-comparator-extension
  -> exact merged SHA: repository CI + 210 development matrix + semantic invariance
  -> create freeze/cx01-002 at that exact SHA
  -> deterministic source-SHA-bound selection for cx01-candidate-002
  -> prepare outcome-blind candidate/audit/manifest package
  -> independent review by a genuinely separate reviewer
  -> independent execution seal
  -> persistent STARTED
  -> one-way formal execution
  -> immutable raw lock
  -> frozen scoring
```

No formal capability may be opened before the independent seal. After STARTED there is no repair, retuning, threshold change, world change, comparator change, or same-candidate rerun.
