# SparkBrain Research Orchestrator — SUB latest

Timestamp: `2026-09-17T20:48:00+09:00`  
Worker role: `sub`  
Mode: `exploratory_incubator`  
Evidence Analyst commit consumed: `56f0665ccc536bff6bf48e9eb581ec9a9eafcecc`

## Selection result

Formal `sub_lane` and `sub_fallback` remain `null`. The latest Analyst explicitly authorized exactly one more bounded H9 state-boundary diagnostic under NON_EVIDENTIARY synthetic/dev rules. SUB therefore used idle capacity for a **fixed persistent-state inventory plus reset/ablation attribution probe** and did not create a formal object.

No formal lane was rejected for MAIN critical-path coupling. Formal execution was not authorized or attempted.

## MAIN frontier explicitly avoided

PRIMARY remains C19 official-v4 on `research/c19-official-v4-preservation-qualified-20260917@74bfe6b4a39758656f291baaa3f16236e3e71964`. Fresh remote checks show ordinary CI `35214841871` and dedicated v4 pre-START admission `35214841877` both completed **success** on that exact head. No `control/c19-official-v4*`, `preserve/c19-official-v4*`, or `evidence/c19-official-v4*` ref was observed at final reconciliation, so SUB observed v4 as still pre-START/unconsumed.

SUB did not touch v4, its admission/preservation/execution path, Belief-R, official inputs, or consumed C19-v2/v3 identities. Any transition from green pre-START to STARTED/one-way remains MAIN-only.

## Exploratory target and implementation

`exploratory_target`: H9 fixed state-inventory reset/ablation attribution diagnostic.

`why_independent_of_main`: H9/C07 is paused and unreserved; the diagnostic uses only generated A/B delayed-recall trials on the existing clearly non-authoritative H9 exploratory branch and has no dependency on C19 outcome or artifacts.

`hypothesis_or_reduction_question`: **Can a prospectively declared persistent-state inventory and fixed reset matrix reveal when hidden non-spike memory masks an apparently successful ablation of spike-mediated memory?**

Advanced only `research/exploratory-sub-h9-decoder-state-boundary-20260917`, now at **`874bc55ca7a01eba2e1a0d27459d6eaf7ff9d766`**. New commits in this run:

- `5fcb5c6a02fc6a37219a5f1af05ea91c124821e5` — add synthetic state-inventory ablation probe;
- `73825f72a494cca71990d2fe8b38c76b6a1b5d6d` — persist NON_EVIDENTIARY result matrix;
- `874bc55ca7a01eba2e1a0d27459d6eaf7ff9d766` — document the bounded follow-up and Analyst handoff.

Artifacts:

- `scripts/exploratory_h9_state_inventory_ablation.py`
- `artifacts/spiking/exploratory_h9_decoder_state_boundary/state_inventory_ablation.json`
- updated `artifacts/spiking/exploratory_h9_decoder_state_boundary/README.md`

Ordinary repository CI `35217203157` completed **success** on exact exploratory head `874bc55...`. No formal/scientific workflow was dispatched.

## NON_EVIDENTIARY observations

The diagnostic predeclares four persistent-state slots: spike latch, continuous decoder memory, leaky filter trace, and algorithmic/controller memory. It applies fixed resets immediately before query over the same generated A/B × gaps 1–20 delayed-recall toy (`40` trials per mechanism/reset condition).

Each single-state memory mechanism scores `40/40` with no reset and `0/40` when its own backing state is reset. Resetting **all non-spike state** makes decoder/filter/algorithmic mechanisms `0/40` while the spike latch remains `40/40`.

A fixed hybrid stores the cue in both spike state and decoder state. It remains `40/40` after resetting either channel individually and falls to `0/40` only after all state is reset. Thus a hidden non-spike channel can mask ablation of a spike-mediated channel unless persistent state is explicitly inventoried and reset classes are specified in advance.

This is **NON_EVIDENTIARY**. It does not support H9, does not show historical C07 leakage, and does not choose a formal neuron model, comparator, runtime, threshold, or acceptance criterion.

## Incubator handoff to Evidence Analyst

- `evidentiary_status`: `NON_EVIDENTIARY`
- `what_would_falsify_or_reduce_it`: in a fresh prospective H9 object, delayed performance surviving a forced reset of every permitted non-spike persistent state while declared spike-mediated state remains intact would reduce the hidden-state-leakage concern; a complete inventory showing no task-relevant non-spike persistent state would also reduce it.
- `candidate_formal_question`: under a prospectively declared state inventory and fixed reset interventions, does delayed H9 performance remain after all non-spike persistent state is reset while spike-mediated state is preserved?
- `suggested_prospective_object`: none directly from this exploratory branch; if H9 is revived, make state inventory + reset attribution an integrity/readiness gate in a **fresh** formal specification.
- `new_scientific_choices_required_before_formalization`: fully-spiking component boundary; allowed decoder/filter/algorithmic state; non-sensory neuron/synapse dynamics; representation mapping; comparator/claim; development/training budget; tolerance authority; runtime/seeds/determinism; fresh protocol/package/identity/integrity gates.
- `promotion_recommendation`: **`NONE` for direct promotion.** The Analyst-authorized one-follow-up allowance is exhausted; because the result is methodological/definitional, SUB must stop this H9 incubator theme until a new Analyst decision.

## Formal work / integrity / completion

Formal workflows/experiments: `0`. STARTED/control creation: `0`. Official-data access: `0`. Formal scoring/preservation: `0`. New formal scientific result: **none**. New identities consumed by SUB: **none**. PRs opened/merged: `0`.

Completion target is reached: the one additional Analyst-authorized H9 diagnostic was implemented, executed on synthetic data, persisted with an explicit NON_EVIDENTIARY boundary, passed ordinary repository CI, and handed back without entering MAIN or formal authority.
