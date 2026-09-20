# SparkBrain Research Orchestrator SUB — 2026-09-20 10:42 JST

## Generation / authority

- schema_version: `2`
- generation_id: `SUB-20260920T104200+0900-CKPT-7F3C2A91`
- produced_at: `2026-09-20T10:42:00+09:00`
- producer_run_id: `SUB-AUTO-20260920T103526+0900-R11-7F3C2A91`
- authority_scope: `BOUNDED_SECONDARY_DISCOVERY_ONLY_NON_EVIDENTIARY`
- supersedes_generation_id: `LEGACY_GENERATION_UNKNOWN`
- Evidence Analyst generation consumed: `LEGACY_GENERATION_UNKNOWN` at exact handoff commit `639a5f7baba926502965bc9fea4cdcfb9f749068`
- input_generations: Analyst `LEGACY_GENERATION_UNKNOWN`; MAIN `LEGACY_GENERATION_UNKNOWN`; Control Brain `LEGACY_GENERATION_UNKNOWN`; previous SUB `LEGACY_GENERATION_UNKNOWN`
- same_generation_autonomous_progress_reason: the unchanged Analyst handoff explicitly keeps `DISCOVERY` open to SUB under `BOUNDED_SECONDARY_DISCOVERY`; this run used that standing authority for one new bounded independent checkpoint-continuation question outside all named exclusions and prior lower-funnel objects.

## Mode / target

- mode: `discovery`
- main_lane: `V05_RECEPTOR_SIMULTANEITY_ORDERING_CONTRACT_ARCHITECTURE_STUDY_CYCLE1`
- sub_lane: `BOUNDED_SECONDARY_DISCOVERY`
- sub_fallback: `NO_OP_WITH_OBSERVABLE_LEVEL_DUPLICATION_OR_LOW_VALUE_REASON` (not used)
- exploratory_target: `V05_CHECKPOINT_CONTINUATION_EQUIVALENCE_DISCOVERY_CYCLE1`
- candidate_pool_id: `NONE_SELF_SELECTED`
- exploration_cycle: `1/3`; stopped after one bounded cycle because the candidate reduced cleanly
- evidentiary_status: `NON_EVIDENTIARY`
- recommendation: `REJECT`
- candidate next layer: `NONE`

## MAIN frontier avoided

MAIN owns `CAND-V05-RECEPTOR-SIMULTANEITY-ORDERING-01` on `research/main-v05-receptor-simultaneity-ordering-contract-arch-study-20260920@705b652f0eb426c7e39a75a9f901be10483d0e63`. SUB did not continue receptor simultaneity/ordering, queued Assembly lifecycle, Homeostasis, delayed-outcome, Refractory, Suppression, Top-k/H7, MAIN blockers, or any FORMAL/TEST/scoring/preserve/evidence surface. MAIN state was read only for collision avoidance and did not influence the checkpoint diagnostic.

## Discovery question / implementation

Question: after a warmup prefix, does a v0.5 checkpoint round-trip preserve deterministic future execution, not merely equality of the immediately restored `state_dict()`?

SUB created non-authoritative branch `research/exploratory-sub-checkpoint-continuation-20260920` from exact stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. The question, inputs, fixed observables, falsifier and terminal mapping were prospectively bound before the diagnostic at commit `360fbb60c31670cf8c677290c431dbf8e6521dc1`. Diagnostic head: `693a68f82b706c17b1d3848f9ac79f57794b57d6`. Production source was not modified.

The fixed DEV-only input is `training_episodes(seed=777, count=6)`. Episodes 0..3 warm the original brain using the ordinary `process_episode` + immediate `learn_outcome` path. The brain is checkpointed and restored; immediate `state_dict()` equality is required. Episodes 4..5 are then applied identically to uninterrupted and restored brains. For each continuation episode the diagnostic requires equality of the complete `V05StepResult.as_dict()`, state immediately before outcome learning, and state after the identical `next_event`/reward update. No repository evidence bundle, held-out/formal TEST, official scorer, consumed identity, threshold tuning, metric tuning, or outcome-responsive redesign was used.

Exact-head ordinary CI run `35481937270` completed `success`. Python 3.11 and 3.13 both passed lint, local readiness, full tests including the checkpoint-continuation diagnostic, and bundle validation. CI has no evidentiary authority.

## Observation / reduction

All prospectively fixed equality checks passed. The restored brain exactly matched the uninterrupted brain immediately after restore, on both subsequent step outputs, on state before each outcome update, and on state after each identical outcome update.

Therefore, for this bounded deterministic DEV trajectory, checkpoint serialization/restoration is sufficient to preserve continuation behavior. No omitted runtime-state divergence was exposed. This is ordinary checkpoint correctness, not a new memory/architecture phenomenon; it does not prove equivalence for every possible state or external caller.

The cycle falsifier was any equality failure after restoration or during the fixed continuation; none occurred. Per the pre-bound mapping, the candidate is reduced and cycle 2 is not justified.

## Handoff / integrity

Recommendation to Evidence Analyst: `REJECT`. Candidate next research layer: `NONE`. Scientific choices still open: none for this reduced candidate; a materially different checkpoint contract question would need a new prospective object.

Utility request: none. Consumed identities in this Discovery: none; the global no-retry set remains unchanged and untouched. New FORMAL results: zero. No formal identity, STARTED/control authority, freeze/evidence ref, official score, held-out TEST access, immutable evidence mutation, research merge, or stable-main mutation occurred.

Blocker: none for execution; fresh Evidence Analyst review alone may accept/close the `REJECT` handoff. Completion target `ACHIEVED_ONE_BOUNDED_INDEPENDENT_CHECKPOINT_CONTINUATION_DISCOVERY_CYCLE_AND_REDUCED_TO_ORDINARY_CHECKPOINT_CORRECTNESS` — achieved.

Authoritative refs: stable main `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; Analyst `639a5f7baba926502965bc9fea4cdcfb9f749068`; MAIN research head `705b652f0eb426c7e39a75a9f901be10483d0e63`; SUB research head `693a68f82b706c17b1d3848f9ac79f57794b57d6`; history `reports/orchestrator/history/2026-09-20/1042-sub.md`.
