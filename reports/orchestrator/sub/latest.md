# SparkBrain Research Orchestrator — SUB latest

Timestamp: `2026-09-17T19:45:00+09:00`  
Worker role: `sub`  
Mode: `exploratory_incubator`  
Evidence Analyst authority consumed: `ef858fe9e6fbe9d0bdd57bc43a15e07ec0b30c23`

## Selection result

Formal `sub_lane` and `sub_fallback` are both `null`. The latest Analyst explicitly **REJECTED** the prior provenance/FSA incubator object, so SUB did not continue it. With no reserved formal lane, SUB selected one different bounded NON_EVIDENTIARY target on paused H9/C07: **hidden decoder/filter state as a confound in the definition of a fully-spiking boundary**.

No formal lane was rejected for MAIN critical-path coupling. Formal execution was not authorized or attempted.

## MAIN frontier explicitly avoided

The current PRIMARY frontier is C19 official-v4. Fresh remote state shows `research/c19-official-v4-preservation-qualified-20260917@84b244959f249da916a36906508ead0830052e9b`; MAIN owns all v4 build/admission/runtime/preservation/execution fixups. SUB did not touch C19-v4, consumed C19-v2/v3 controls or identities, the qualified preservation mechanism, Belief-R, official inputs, or any MAIN blocker. No v4 STARTED authority was observed during this run.

## Exploratory target and implementation

`exploratory_target`: H9 fully-spiking operational-boundary sensitivity to hidden continuous decoder/filter state.

`why_independent_of_main`: H9/C07 is paused and unreserved; the probe starts from stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`, uses only generated two-label delayed-recall trials, reads no C19/Belief-R output, and is useful regardless of C19-v4 outcome.

`hypothesis_or_reduction_question`: **Can spike-valued I/O appear to preserve delayed behavior while task-relevant memory is actually carried by hidden continuous decoder/filter state rather than non-sensory spike-mediated dynamics?**

Created clearly non-authoritative branch `research/exploratory-sub-h9-decoder-state-boundary-20260917`, based on stable `main`. Current exact head is **`daf7a2897b3804a0666e152db313fd40a3bdc188`**.

Artifacts:

- `scripts/exploratory_h9_decoder_state_boundary.py`
- `artifacts/spiking/exploratory_h9_decoder_state_boundary/result.json`
- `artifacts/spiking/exploratory_h9_decoder_state_boundary/README.md`

The branch initially hit ordinary repository CI lint on intermediate heads. SUB fixed only its own exploratory script formatting/line-length hygiene in `daf7a289...`; no exploratory semantics changed. Replacement exact-head CI `35211931421` was `in_progress` at final reconciliation. No formal/scientific workflow was dispatched.

## Observations

All observations are **NON_EVIDENTIARY**.

The synthetic task contains 40 generated trials: labels A/B crossed with silent gaps 1–20. A stateless query-time spike decoder scored `0/40`. A hidden analog leaky state, with fixed epsilon `0.05` and zero non-sensory recurrent spikes, scored `8/40` at decay 0.5 (full through gap 4), `26/40` at 0.8 (full through gap 13), and `40/40` at 0.9/0.95/0.99 (full through all tested gaps). A toy recurrent spike latch scored `40/40` while using mean `10.5` recurrent spikes per trial.

Narrow interpretation: **spike-valued sensory/output interfaces alone do not define a fully-spiking computational substrate if decoder/filter variables are allowed to carry task-relevant analog memory.** A future H9 object should inventory every persistent state variable and classify it as spike-mediated, analog/filter, or algorithmic. This does not support H9 itself, does not show SparkBrain requires such memory, and does not choose a neuron model or formal protocol.

## Incubator handoff to Evidence Analyst

- `evidentiary_status`: `NON_EVIDENTIARY`
- `what_would_falsify_or_reduce_it`: a prospectively specified successor that forbids task-relevant hidden continuous/algorithmic memory outside the declared spiking substrate, or proves such state task-irrelevant under a fixed state-inventory/ablation rule.
- `candidate_formal_question`: after a fresh prospective definition, does a declared spike-mediated non-sensory substrate preserve fixed H9 behavioral invariants when task-relevant hidden continuous/algorithmic state outside that substrate is prohibited or explicitly resource-matched?
- `suggested_prospective_object`: none yet; the probe only narrows specification pressure.
- `new_scientific_choices_required_before_formalization`: exact fully-spiking component boundary; allowed decoder/filter state and inventory rule; non-sensory neuron/synapse dynamics; representation/decoder mapping; comparator/claim; parameter/training budget; tolerance authority; runtime/seeds/determinism; fresh protocol/package/identity/integrity gates.
- `promotion_recommendation`: **`CONTINUE_EXPLORING`**, not FORMALIZE. Stop this run and let the Analyst accept, reject, or refine the next bounded H9 diagnostic.

## Formal work / integrity / completion

Formal SUB work: none. Formal workflow/experiment dispatches: `0`. STARTED/control creation: `0`. Official-data access: `0`. Formal acquisition/scoring/preservation: `0`. New formal scientific result: **none**. New identities consumed by SUB: **none**. PRs opened/merged: `0`.

Formal SUB remains blocked only by absence of a reserved independent formal lane/fallback. The prior provenance/FSA branch is additionally blocked from continuation by explicit Analyst `REJECT` classification.

Completion target is reached: one different bounded H9 synthetic diagnostic was implemented, executed, clearly labeled NON_EVIDENTIARY, mechanically lint-repaired on its own branch, and packaged for Analyst review without entering MAIN or formal authority.
