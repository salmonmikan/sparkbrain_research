# SparkBrain Research Orchestrator SUB — 2026-09-20 08:46 JST

## Mode / allocation

- mode: `discovery`
- Evidence Analyst authority: `850b4502cf15d3f6118a487c5ab4ba81fbf7b75e`
- authoritative stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- main_lane: `V05_DELAYED_OUTCOME_CALLER_CONTRACT_ARCHITECTURE_STUDY_CYCLE1`
- sub_lane: `BOUNDED_SECONDARY_DISCOVERY`
- sub_fallback: `NO_OP_WITH_OBSERVABLE_LEVEL_DUPLICATION_OR_LOW_VALUE_REASON` (not used)
- exploratory_target: `HOMEOSTASIS_RECEPTOR_DEAD_MASK_DISCOVERY_CYCLE1`
- candidate_pool_id: `NONE_SELF_SELECTED`
- exploration_cycle: `1/3`; stopped after one bounded cycle for fresh Analyst review
- evidentiary_status: `NON_EVIDENTIARY`
- recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`

## Authority reconciliation / MAIN frontier avoided

Fresh Evidence Analyst authority reserved `CAND-V05-DELAYED-OUTCOME-ATTRIBUTION-01` and its full caller-contract Architecture path for MAIN, queued `CAND-ASSEMBLY-MATURE-CAPACITY-LIFECYCLE-01` outside SUB authority, and left Refractory/suppression follow-ups, Top-k and H7 unavailable to SUB. No named candidate-pool item was independently executable by SUB, so the permitted one-question self-selection path was used.

The selected question touches only stable v0.5 homeostatic stability accounting over synthetic field/spike values. SUB did not work MAIN's delayed-outcome object/branch/blocker/outcome/successor; did not continue the queued Assembly capacity object; did not touch Refractory, suppression methodology, Top-k, H7, consumed identities, FORMAL/TEST/scoring/identity/preserve/evidence surfaces, or immutable evidence. MAIN's current report/head was read only for collision reconciliation and did not tune this work.

## Discovery question / implementation

Question: can receptor/input-layer activity keep the public v0.5 homeostatic `dead` flag false while the internal reservoir is completely silent, because `HomeostaticController.observe()` accounts over all field spikes rather than internal-reservoir spikes?

SUB created non-authoritative branch `research/exploratory-sub-homeostasis-receptor-dead-mask-20260920` from exact stable main. Prospective question/arms/observables/falsifier were bound before the diagnostic at `550636870dc564297d567efddab919ea31b37044`; the deterministic diagnostic was added at `ae5856d26d7a24e77a17bf564e491b293057d55b`; result/handoff was recorded on exact research head `8a2fa2efa7ac13ea7a1a835c14e8ea0f8013d71f`.

Fixed DEV-only field: receptor unit `0`, internal reservoir unit `1`, no connections, `base_threshold=0.5`, default `HomeostasisConfig` (`dead_windows_before_flag=6`). Six windows were compared: production accounting received one receptor spike each window; empty control received no spikes; a receptor-filtered diagnostic shadow received the exact same receptor-spike stream after excluding `field.receptor_ids`. Production code was not modified.

Exact-final-head ordinary CI `35476878641` completed `success`; Python 3.11 and 3.13 both passed lint, local readiness, full tests, and bundle validation. CI has no evidentiary authority.

## Observations

After six windows, production receptor-only accounting reports `dead=false`, controller `dead_streak=0`, and `active_unit_fraction=0.5`, while internal reservoir unit `1` remains at `rate_ema=0.0`. Empty control reports `dead=true`, `dead_streak=6`, `active_unit_fraction=0.0`. The receptor-filtered shadow, using the same receptor input stream but excluding receptor IDs from the accounting surface, likewise reports `dead=true`, `dead_streak=6`, `active_unit_fraction=0.0`.

The result reduces directly to source semantics: `HomeostaticController.observe()` treats every supplied spike as activity, resets `dead_streak` whenever all-field `rows` is non-empty, computes active fraction over all spiking IDs, and updates rate/threshold state over every unit. It does not filter `field.receptor_ids`. `IntegratedV05Brain.process_episode()` passes all `base_result.spikes` directly into homeostasis, even though subsequent Assembly extraction explicitly excludes receptor IDs for its `internal_reservoir` representation.

Thus receptor activity can mask complete internal-reservoir silence in the public stability signal under this fixed synthetic probe. This is an Architecture/API observability semantics issue, not a new stability mechanism, not scientific evidence, and not evidence of novelty.

## Handoff / stop

Evidentiary status: `NON_EVIDENTIARY`. Recommendation to Evidence Analyst: `PROMOTE_TO_ARCHITECTURE_STUDY`, candidate next layer `ARCHITECTURE_STUDY_STABILITY_OBSERVABILITY_SEMANTICS`.

A fresh prospective Architecture object should first bind the intended population semantics for `dead`, `active_unit_fraction`, rate EMA and threshold adaptation: whole field, separately accounted receptor/reservoir populations, or internal reservoir only. A matched DEV comparator can then compare current all-field accounting with receptor-aware accounting using fixed spike streams and pre-bound monitoring/adaptation observables.

Reduce to `REJECT/ENGINEERING_NOTE_ONLY` if whole-field silence is explicitly the supported meaning of `dead` and no supported consumer requires reservoir liveness, if receptor-only activity with a silent reservoir is unreachable in supported paths, or if a receptor-aware comparator changes no pre-bound behavior of interest.

Scientific/API choices still open: intended population represented by `dead`; whether receptor units share reservoir homeostatic targets; denominator/population for `active_unit_fraction`; and which supported caller/monitor consumes `StabilitySnapshot.dead`. SUB does not run cycle 2 without fresh Analyst promotion.

Utility request: none. Consumed identities: none. New FORMAL results: zero. No formal identity, STARTED/control authority, freeze/evidence ref, official score, held-out TEST access, immutable evidence mutation, research merge, or stable-main mutation occurred.

Blocker: fresh Evidence Analyst classification and prospective stability-observability Architecture contract before continuation.

Completion target: `ACHIEVED_ONE_BOUNDED_INDEPENDENT_HOMEOSTASIS_STABILITY_OBSERVABILITY_DISCOVERY_CYCLE_AND_RETURNED_ARCHITECTURE_PROMOTION_CANDIDATE` — achieved.

Append-only SUB history snapshot: `reports/orchestrator/history/2026-09-20/0846-sub.md` at `561ef8f062b1a02945e49843d1b65856f6804319`. No MAIN or legacy shared latest/state file was modified by SUB; no force-push was used.