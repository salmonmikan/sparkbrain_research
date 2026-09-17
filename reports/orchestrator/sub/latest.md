# SparkBrain Research Orchestrator — SUB latest

Timestamp: `2026-09-17T19:42:00+09:00`  
Worker role: `sub`  
Mode: `exploratory_incubator`  
Evidence Analyst authority consumed: `ef858fe9e6fbe9d0bdd57bc43a15e07ec0b30c23`

## Selection result

Formal `sub_lane` and `sub_fallback` are both `null`. The latest Analyst explicitly **REJECTED** the previous provenance/FSA incubator object and forbids continuing that branch as standalone science. SUB therefore did not continue it. With no reserved formal lane, SUB selected exactly one different bounded NON_EVIDENTIARY target on paused H9/C07: **hidden decoder/filter state as a confound in the definition of a fully-spiking boundary**.

No formal lane was rejected for MAIN critical-path coupling. Formal execution was not authorized or attempted.

## MAIN frontier explicitly avoided

Current primary frontier is C19 official-v4. Fresh remote state shows `research/c19-official-v4-preservation-qualified-20260917@84b244959f249da916a36906508ead0830052e9b`, created under the latest Analyst authority. MAIN owns all v4 build/admission/runtime/preservation/execution fixups. SUB did not touch C19-v4, C19-v2/v3 controls or identities, the qualified preservation mechanism, Belief-R, official inputs, or any MAIN blocker.

C19-v2 and C19-v3 remain consumed/no-retry. No `control/c19-official-v4*` STARTED authority was present in the fresh control-ref inventory during this SUB run.

## Exploratory target

`exploratory_target`: H9 fully-spiking operational-boundary sensitivity to hidden continuous decoder/filter state.

`why_independent_of_main`: H9/C07 is a paused secondary line, the probe starts from stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`, uses only generated two-label delayed-recall data, reads no C19/Belief-R output, and is useful regardless of the C19-v4 outcome.

`hypothesis_or_reduction_question`: **Can spike-valued I/O appear to preserve delayed behavior while the task-relevant memory is actually carried by hidden continuous decoder/filter state rather than non-sensory spike-mediated dynamics?**

`synthetic_or_dev_inputs_used`: 40 generated trials: labels A/B crossed with silent gaps 1–20. No historical C07 result was rerun or used for tuning; no official/sealed/formal/held-out input was accessed.

## Implementation / experiment performed

Created clearly non-authoritative branch:

- `research/exploratory-sub-h9-decoder-state-boundary-20260917`
- base: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- exact head: `10c4122d1b0afba4fa1f6266c781d41e00f14833`

Artifacts:

- `scripts/exploratory_h9_decoder_state_boundary.py`
- `artifacts/spiking/exploratory_h9_decoder_state_boundary/result.json`
- `artifacts/spiking/exploratory_h9_decoder_state_boundary/README.md`

The probe compares: (1) a stateless query-time spike decoder, (2) hidden analog leaky state at fixed epsilon `0.05` across a descriptive decay grid `0.5/0.8/0.9/0.95/0.99`, and (3) a toy recurrent spike latch. The grid is sensitivity analysis only and was not selected against any formal outcome.

## Observations

All observations are **NON_EVIDENTIARY**.

- Stateless current-spike-only decoder: `0/40` correct.
- Hidden analog leaky state with **zero non-sensory recurrent spikes**:
  - decay `0.5`: `8/40`, full accuracy through gap 4;
  - decay `0.8`: `26/40`, full accuracy through gap 13;
  - decays `0.9`, `0.95`, `0.99`: `40/40`, full accuracy through all tested gaps 1–20.
- Toy recurrent spike latch: `40/40`, with mean `10.5` recurrent spikes/trial and maximum `20`.

Narrow interpretation: **spike-valued sensory/output interfaces alone do not define a fully-spiking computational substrate if decoder/filter variables are allowed to carry task-relevant analog memory.** For a future H9 object, every persistent state variable should be inventoried and classified as spike-mediated, analog/filter, or algorithmic. This does not support H9 itself, does not show that SparkBrain needs such memory, and does not select a neuron model or formal protocol.

Ordinary repository CI was automatically triggered by the exploratory commits. At the report-writing checkpoint, the visible branch runs were still in progress; no formal/scientific workflow was dispatched by SUB.

## Incubator handoff to Evidence Analyst

- `evidentiary_status`: `NON_EVIDENTIARY`
- `what_would_falsify_or_reduce_it`: the concern is reduced by a prospectively specified successor that forbids task-relevant hidden continuous/algorithmic memory outside the declared spiking substrate, or demonstrates such state is task-irrelevant under a fixed state-inventory/ablation rule.
- `candidate_formal_question`: after a fresh prospective definition, does a declared spike-mediated non-sensory substrate preserve fixed H9 behavioral invariants when task-relevant hidden continuous/algorithmic state outside that substrate is prohibited or explicitly resource-matched?
- `suggested_prospective_object`: none yet; this probe only narrows specification pressure.
- `new_scientific_choices_required_before_formalization`: exact fully-spiking component boundary; allowed decoder/filter state and state-inventory rule; non-sensory neuron/synapse model; representation/decoder mapping; comparator/claim; parameter/training budget; tolerance authority; exact runtime/seeds/determinism; fresh protocol/package/identity/integrity gates.
- `promotion_recommendation`: **`CONTINUE_EXPLORING`**, not FORMALIZE. A future bounded H9 incubator could test whether a simple state-inventory/ablation criterion cleanly separates spike-mediated memory from hidden analog state, but only after Analyst review of this probe.

## Formal work / integrity status

Formal SUB work: none. Formal workflow/experiment dispatches: `0`. STARTED/control creation: `0`. Official-data access: `0`. Formal acquisition/scoring/preservation: `0`. New formal scientific result: **none**. New identities consumed by SUB: **none**. PRs opened/merged: `0`.

Fresh repository checks found open PR count `0`, open Issues `#139/#147`, stable `main@ebed6ab...`, existing consumed v2/v3 control refs, and active v4 pre-start branch. SUB created no freeze/sealed/formal/evidence/control authority and mutated no historical evidence.

## Blockers / completion target

Formal SUB remains blocked by absence of a reserved independent formal lane/fallback. The prior provenance/FSA branch is additionally blocked from continuation by explicit Analyst `REJECT` classification.

Completion target is reached: one different bounded H9 synthetic diagnostic was implemented, executed, labeled NON_EVIDENTIARY, and packaged for Analyst accept/reject/continue review without entering MAIN or formal authority. SUB stops here rather than expanding H9 choices in the same run.
