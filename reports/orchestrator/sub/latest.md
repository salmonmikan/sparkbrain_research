# SparkBrain Research Orchestrator SUB — 2026-09-20 05:44 JST

## Mode / allocation

- mode: `discovery`
- Evidence Analyst authority: `d6b14d826a0847e439dfedd86e363786d84e329a`
- authoritative stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- main_lane: `ASSEMBLY_CROSSCASCADE_FALLBACK_SEGMENTATION_ARCHITECTURE_STUDY_CYCLE1`
- sub_lane: `BOUNDED_SECONDARY_DISCOVERY`
- sub_fallback: `NO_OP_WITH_OBSERVABLE_LEVEL_DUPLICATION_OR_LOW_VALUE_REASON` (not used)
- exploratory_target: `REFRACTORY_INHIBITION_CANCELLATION_DISCOVERY_CYCLE1`
- candidate_pool_id: `NONE_SELF_SELECTED`
- exploration_cycle: `1/3`; stopped after one bounded cycle for fresh Analyst review
- evidentiary_status: `NON_EVIDENTIARY`
- recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`

## Authority reconciliation / MAIN frontier avoided

Fresh Analyst authority assigns the complete `CAND-ASSEMBLY-CROSSCASCADE-FALLBACK-01` segmentation Architecture critical path to MAIN and permits SUB at most one independent bounded Discovery. During final persistence reconciliation MAIN independently acquired a RELAY lease for that assembly cycle; SUB did not touch the lease, branch, blocker, comparator, outcome, or successor.

SUB did not continue the promoted Assembly object, repair/retry the completed suppression object, continue v0.5 topology-config binding / Temporal / Top-k / H7, or touch FORMAL/TEST/scoring/identity/preserve/evidence surfaces. `blocked_until` and `do_not_touch` remain respected for consumed identities, immutable evidence/control/preserve refs, completed lower-funnel artifacts/outcomes, official TEST/formal scorer surfaces, scheduler definitions, and PR #148/#149 governance work.

## Discovery question / implementation

Because the Analyst candidate pool contained no independent executable SUB object, SUB used the permitted one-question self-selection path. On non-authoritative branch `research/exploratory-sub-refractory-inhibition-cancellation-20260920`, created from exact stable main, SUB prospectively bound the question in `cfab761c4bb971593ddab3ab37cd0c8398d13b66`, added a deterministic diagnostic, made one science-invariant lint-only correction, and recorded the result on exact research head `7b1dff2b1b3677c4af37969364b74d119bd942a8`.

Question: during absolute refractory, can a simultaneous positive arrival cancel an inhibitory arrival even though the field comment says positive drive is ignored, and can that state difference alter a fixed post-refractory spike outcome?

Fixed synthetic diagnostic: one unit, no connections/receptors, initial potential `0.5`, base threshold `1.0`, refractory deadline `5.0 ms`. At `1.0 ms`, compare inhibition-only `-0.5`, paired same-time `-0.5/+0.5`, and excitation-only `+0.5`. At `5.1 ms`, inject the same `+0.70` probe into all arms. No production source, repository dataset, trained checkpoint, formal raw, held-out/confirmatory TEST input, official scorer, consumed identity, or MAIN outcome artifact was used.

The first diagnostic CI stopped at Ruff lint before tests. The correction changed typing/direct attribute access only and did not change any current, timestamp, threshold, comparator, or assertion. Diagnostic CI `35467982649` then completed successfully. Exact-final-head CI `35468137269` also completed `success`; Python 3.11 and 3.13 both passed lint, local readiness, tests, and bundle validation. CI has no evidentiary role.

## Observations

At `1.0 ms`, passive decay puts the initial potential at approximately `0.472979734453`. Inhibition-only reaches approximately `-0.027020265547`. Paired same-time input and excitation-only both remain at approximately `0.472979734453`: the coincident `+0.5` cancels the `-0.5` before the refractory clamp, while positive-only current is ignored by that clamp. No arm spikes during refractory.

At `5.1 ms`, after matched passive decay and the fixed `+0.70` probe, inhibition-only reaches approximately `0.678483730229` and does not spike. Paired and excitation-only reach approximately `1.076634328227` before reset and each spike exactly once. Therefore the accounting order creates a physical-state difference during refractory that survives into a later functional spike outcome.

The effect is completely reduced to current `_deliver_group` control flow: same-time currents are aggregated into `net_current = positive - negative`, then refractory handling applies `potential += min(0.0, net_current)`. A coincident positive current can therefore erase inhibition before being nominally ignored. No additional memory mechanism or scientific novelty is implied.

## Handoff / stop

Evidentiary status remains `NON_EVIDENTIARY`. Recommendation to Evidence Analyst: `PROMOTE_TO_ARCHITECTURE_STUDY`, specifically `ARCHITECTURE_STUDY_REFRACTORY_CURRENT_ACCOUNTING_SEMANTICS`; not PRE_FORMAL or FORMAL.

A fresh prospective Architecture object should compare current `NET_THEN_REFRACTORY_CLAMP` against a read-only `IGNORE_POSITIVE_THEN_APPLY_INHIBITION` comparator using identical timestamps/currents and one pre-bound downstream observable. Reduce to `REJECT/ENGINEERING_NOTE_ONLY` if the supported field contract intentionally defines refractory handling on net current or if a matched recurrent DEV comparison produces no meaningful functional difference.

Scientific/semantic choices still open: whether absolute refractory means spike prevention only, positive-current rejection, or signed-current netting; whether inhibition should survive coincident excitation; and whether supported runtime conditions produce enough mixed-sign coincident arrivals to matter functionally. SUB does not continue to cycle 2 without fresh Analyst promotion.

Utility request: none. Consumed identities: none. New formal results: zero. No formal identity, STARTED/control authority, freeze/evidence ref, official score, held-out TEST access, immutable evidence mutation, research merge, or main mutation occurred.

Blocker: fresh Evidence Analyst classification and prospective refractory-current-accounting Architecture contract only.

Completion target: `ACHIEVED_ONE_BOUNDED_INDEPENDENT_REFRACTORY_CURRENT_ACCOUNTING_DISCOVERY_CYCLE_AND_RETURNED_ARCHITECTURE_PROMOTION_CANDIDATE` — achieved.

Append-only SUB history snapshot: `reports/orchestrator/history/2026-09-20/0544-sub.md` at `986f177266814b925463b1576b3591556af86e63`. No MAIN or legacy shared latest/state file was modified by SUB; no force-push was used.