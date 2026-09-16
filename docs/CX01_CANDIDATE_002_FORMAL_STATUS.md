# CX01 Candidate-002 Formal Status and Evidence Map

Status: **TERMINAL-CONSUMED / FORMAL NEGATIVE**

This document is the current canonical status/evidence map for CX01 Candidate-002. Historical pre-execution documents such as `docs/CX01_IMPLEMENTATION_STATUS.md` and `docs/CX01_FORMAL_RUNBOOK.md` remain preserved as protocol/history records, but their statements that Candidate-002 is not yet opened are no longer current.

## Scientific disposition

Candidate identity:

```text
cx01-candidate-002
```

Formal run:

```text
run_id: cx01-formal-34f627d0cc819c2f02d25d88
execution_count: 420
```

The frozen formal scoring policy required all comparator families to satisfy the minimum per-family pass fraction of `0.80`, with privilege matching and training-transcript matching required. The preserved analysis reports `supported: false` for every evaluated comparator decision:

- `g3-first-order-anchor`
- `g4-assembly-anchor`
- `g5-typed-anchor`
- `g6-variable-order`
- `g7-htm-temporal-memory`
- `g8-spiking-temporal-memory-prediction`
- `g8-spiking-temporal-memory-replay`

Every comparator has at least one required family with pass fraction `0.0`, so none satisfies the non-compensatory all-family formal support criterion.

**Interpretation:** Candidate-002 is a valid formal negative for this exact frozen candidate/comparator/protocol contract. This does not by itself establish a programme-wide negative result for SparkBrain, nor does it license reinterpretation of other research lines.

## Terminal integrity boundary

A persistent STARTED record exists for Candidate-002. Therefore this candidate is consumed.

The following are prohibited:

- rerunning Candidate-002;
- retuning thresholds, comparators, worlds, schedules, privileges, or scoring for this identity;
- rescoring altered evidence as though it were the same formal candidate;
- silently repairing the candidate after outcome exposure;
- reusing the same identity as a successor attempt.

Any future CX01 formal attempt requires a distinct prospective identity and the full prospective integrity path before capability exposure.

## Authoritative evidence map

| Role | Ref / commit |
| --- | --- |
| Moving CX01 research line at consolidation base | `research/cx01-comparator-extension@0687c8db3efb8180c8599d32235751b93f3c1f77` |
| Exact source freeze | `freeze/cx01-002-source@e8483968ce43076b4c3fd04c76e62106e2031769` |
| Outcome-blind package freeze | `freeze/cx01-002-package@c104be281285d52a732d5366fe36209d5688d973` |
| Persistent STARTED/control | `control/cx01-candidate-002-started-20260913@8216d41a57e6933443d38dfc8d93f9188e423d0c` |
| Formal preserved evidence | `preserve/cx01-candidate-002-formal-34742073336@6d45928827209cd763a2879494d85838df38b96f` |
| Preserved formal analysis | `preserved-evidence/cx01/candidate-002/run-34742073336/analysis.json` |

The preserved analysis binds the formal result to policy version `cx01-formal-scoring-policy-1`, raw aggregate hash `015cb66912071cd3ea287cc5bff43e6c77d436edd0a0c6085fa8e93e816f3d5a`, and policy hash `5cc3fe30c978f95e2ddbd0834eafd8963c37e0ccccb1dcc32915556577fcc76a`.

## Scope of this consolidation

This is documentation-only status consolidation. It does not create or modify a scientific candidate, STARTED marker, workflow run, freeze/preserve ref, score, or immutable evidence. No new scientific result is claimed here.

The purpose is to make the consumed formal-negative state and its exact evidence pointers unambiguous for later analysis and governance while leaving all historical protocol documents and immutable evidence untouched.
