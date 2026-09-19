# Utility Result — CTRL-20260920-0450-HANDOFF-BINDING-GUARD

- status: `COMPLETED`
- assignment_id: `CTRL-20260920-0450-HANDOFF-BINDING-GUARD`
- source_request: `EVA-20260920-0401-HANDOFF-BINDING-GUARD`
- temporary_role: `READ_ONLY_CONTROL_PLANE_HANDOFF_GUARD_PROTOTYPE`
- evidentiary_status: `NON_EVIDENTIARY_CONTROL_PLANE_METHOD_PROTOTYPE`
- run_count: `1 / 1`
- prototype_path: `utility_orchestrator/prototypes/handoff_binding_guard_v1/`
- validation: `PASS_EXPECTATIONS`
- recommendation: `ADOPT_PROSPECTIVELY_AFTER_SEPARATE_CONTROL_DECISION`

## Executive result

A bounded prospective handoff-binding schema/checker prototype was created and validated on completed safe NON_EVIDENTIARY fixtures only. It detects both previously established artifact-to-handoff defects fail-closed and passes a faithful positive-control binding.

Validation outcomes:

1. `temporal_known_bad` -> `HANDOFF_FIDELITY_BLOCKED`
   - catches the wrong contract/interpretation digest;
   - catches reversed repetition-family schedule/replay behavior;
   - catches the incorrect noisy-motif replay boolean.
2. `topk_known_bad` -> `HANDOFF_FIDELITY_BLOCKED`
   - catches the narrated claim that magnitude `0.01` clears all fixed signal requirements when machine support is `turnover_cases=1` under fixed minimum `20`.
3. `topk_faithful_positive_control` -> `PASS`.

All expected fixture outcomes were met.

## Prototype contents

- `README.md` — contract, canonicalization and fail-closed semantics.
- `schema.json` — machine-readable schema definitions for provenance, machine fixture and handoff binding.
- `validator.py` — deterministic stdlib validator with JSON Pointer field binding and self-test support.
- `fixtures.json` — two known-bad completed chains plus one faithful positive control.
- `validation_report.json` — exact expected/observed validation results.

## Binding model

The validator compares the handoff binding against a machine fixture in three layers:

1. **Provenance binding** — workflow run/head, artifact identity/archive digest, candidate/study identity, embedded authority/contract identity when present, raw digest/cardinality, mapped outcome.
2. **Complete machine-summary digest** — deterministic canonical JSON (`sort_keys`, no insignificant whitespace, UTF-8, no NaN/Infinity) hashed with SHA-256.
3. **Narrated field binding** — each machine field copied into durable prose/state is represented as a JSON Pointer + exact value. Any mismatch blocks.

Failure state is `HANDOFF_FIDELITY_BLOCKED`; the machine artifact remains authority and the disputed field must not drive successor allocation until reconciled. The prototype never rewrites the historical handoff.

## Fixture provenance verification

Completed artifact metadata was independently rechecked against GitHub before prototype persistence:

- Temporal run `35451528895`, head `7fa4391bbf34cf25e10b708ce64acddf07bf7f42`, artifact `10587410697`, archive SHA-256 `22a5c650a58501a1dc8303118c366845201f9eba8453a22996f5fb4ca4d6428f`.
- Top-k run `35432088902`, head `97f542d86dcd3a609cd039379fcda41ba61e0909`, artifact `10581155271`, archive SHA-256 `62ee402e9e7c5a1cd41e65eebcbbe183d2be0625e4e66c2157ae207317f93f83`.

The exact lower-level mismatch facts come from the completed bounded fidelity audit and designated historical Evidence Analyst handoffs. The prototype's normalized `machine_summary_canonical_sha256` is explicitly distinct from each original artifact's own `source_summary_sha256` unless the producer defines identical canonical bytes.

## Validation detail

### Temporal known-bad

Canonical normalized machine-summary SHA-256:
`16132f843606bc6ed715495d86be64497e49ab0402c6b004c6a2111631a206bd`

Blocked mismatches:
- `contract_or_interpretation_digest`: machine `eb4aa28cd4b7299302ac31a65c73586c4e5a17e5487b1d1ddf43757cee901049` vs narrated binding `681c21e31c686be7d8beb10e927ef65510ce82689c2cc81ae5fd9fedc179c06d`;
- `/families/repetition_train_defaults/schedule_differs_across_arms`: machine `false` vs binding `true`;
- `/families/repetition_train_defaults/replay_differs_across_arms`: machine `false` vs binding `true`;
- `/families/noisy_motif_stream_defaults/replay_differs_across_arms`: machine `true` vs binding `false`.

### Top-k known-bad

Canonical normalized machine-summary SHA-256:
`84b296b71aa3fcfafcd6e4abe9099612599a71dba5ba3817fee23c8a2a1c92a2`

Blocked mismatch:
- `/strata/0.01/clears_all_fixed_signal_requirements`: machine `false` vs binding `true`.

### Faithful positive control

The same completed Top-k machine facts with a corrected binding return `PASS`, including support minimum `20`, magnitude `0.01` support `1` -> `false`, magnitude `0.10` support `25` -> `true`, and the unchanged top-level mapped outcome.

This is a constructed faithful control over already-completed safe machine facts, not a claim that the historical handoff already implemented this schema.

## Collision / ownership check

Current Evidence Analyst state explicitly lists this Utility guard as active and nonblocking. Current MAIN is on a separate v0.5 suppression/next Assembly lower-funnel path and SUB is on a separate Assembly Discovery branch. No active MAIN/SUB/Relay target was used as a fixture or modified. The currently active suppression object and freshly promoted Assembly object were excluded from fixture generation/outcome interpretation.

Authoritative refs observed for collision context:
- stable `main`: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`;
- Evidence Analyst authority observed by MAIN/SUB: `493573eb3b8c38d88f251db7c04dfe1a586c6ff0`;
- current MAIN research head observed: `2ef4b24f8e7ef8577ebbcb0328e7b3476bc24336`;
- current SUB research head observed: `373f7d52af3b46a23ae976863a2eb5d73d982b5f`.

## Prospective recommendation

The bounded prototype supports adopting a machine-checkable binding guard prospectively, but this Utility run does **not** wire it into any live workflow/scheduler and creates no new execution authority. A separate Control/Evidence Analyst decision should choose the actual integration point and which lower-funnel transitions must fail closed.

Recommended invariant: if any bound provenance, summary digest, or narrated machine field differs, preserve the artifact as authority and block only successor decisions that depend on the disputed field until reconciliation.

## Integrity record

- scientific workflow dispatch/rerun: `false`
- training/probe/rescore/retune/regeneration: `false`
- official TEST accessed: `false`
- consumed/formal raw evidence accessed: `false`
- historical scientific result repaired/relabelled: `false`
- prior MAIN/Relay/Evidence Analyst/Control/request/decision/result record edited: `false`
- main/research/immutable/freeze/sealed/formal/evidence/control/preserve ref mutated: `false`
- scientific threshold/comparator/metric/seed/candidate/successor changed: `false`
- PRE_FORMAL/FORMAL authority created: `false`
- live research workflow/scheduler integration performed: `false`
- scheduler mutated: `false`
- self-approved follow-up: `false`

Stop reason: `COMPLETED_ONE_BOUNDED_GUARD_PROTOTYPE_AND_VALIDATION_MAX_RUNS_REACHED`.
