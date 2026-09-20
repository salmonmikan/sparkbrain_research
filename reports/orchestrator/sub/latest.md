# SparkBrain Research Orchestrator SUB — 2026-09-20 15:56 JST

## Generation / authority

- schema_version: `2`
- generation_id: `SUB-20260920T155600+0900-THEORY-ENDOCONT-4C7A2E91`
- produced_at: `2026-09-20T15:56:00+09:00`
- producer_run_id: `SUB-RUN-20260920T153750+0900-ENDOCONT-4C7A2E91`
- authority_scope: `BOUNDED_SECONDARY_DISCOVERY_ONLY_NON_EVIDENTIARY`
- supersedes_generation_id: `SUB-20260920T144110+0900-SYSTEM-EVALORDER-6F2C91A8`
- Evidence Analyst: `EVA-20260920T150234+0900-R15-8F3C1A72`, state handoff `095caeb07c23094bf9fc68c8e7022f88d45baa74`, branch tip `ad8290dfab6d79be984f960d48dcf34a8213aefb`
- MAIN: `MAIN-20260920T151432+0900-PRIMARY-FUNNEL21-HOLD-A84D6C2F`, lane `LOWER_FUNNEL_MAIN_HOLD_NO_COHERENT_CENTRAL_OBJECT`, mailbox commit observed `8af4b20aa8e3386197a53317eaf4885942d509b3`
- Control Brain: `CTRL-20260920T145000+0900-R14-7B3E2D91@14285844f80fa844b5aaac9ccf4d2fed95b6fb35`, strategy only
- previous SUB: `SUB-20260920T144110+0900-SYSTEM-EVALORDER-6F2C91A8@656e478ff9146a3d5561c1f2482becc1252bf2d0`
- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`

Authority, MAIN ownership/state and stable main were re-read before mutation and before persistence. No material supersede or collision occurred. MAIN remained scientifically idle under the explicit lower-funnel hold.

## Mode / target

- mode: `discovery`
- discovery_mode: `THEORY_BACKWARD_MECHANISM_DISCOVERY`
- target: `V05_ENDOGENOUS_CONTINUATION_DISCOVERY_CYCLE1`
- proposed candidate: `CAND-V05-ENDOGENOUS-CONTINUATION-01`
- candidate_pool_id: `NONE_SELF_SELECTED`
- cycle: `1/3`, stopped after reduction
- evidentiary_status: `NON_EVIDENTIARY`
- recommendation: `REJECT`
- next layer: `NONE`

Pre-selection theory-backward rolling window was Assembly partial=`MECHANISM`, delayed reward=`MECHANISM`, evaluation order=`SYSTEM` (`2/3`). Current selection was not quota-forced; endogenous input-free continuation was chosen as a distinct central mechanism discriminator. Post-selection last-three is delayed reward=`MECHANISM`, evaluation order=`SYSTEM`, endogenous continuation=`MECHANISM` (`2/3`). `theory_backward_exception=null`.

## MAIN frontier avoided

SUB did not execute held `CAND-H7-RESP-01`, reopen terminal objects, touch MAIN blockers/successors, FORMAL/TEST/scoring, consumed/frozen identities, immutable evidence, preserve/control refs, or stable main. It did not rescue prior Assembly feedback/partial-completion, delayed reward, evaluation-order, Temporal, Top-k, topology, refractory, cross-cascade, homeostasis, receptor-ordering, checkpoint, suppression or mature-capacity objects.

## Question / implementation

Question: can a supported v0.5 brain, after a driven functional DEV episode, generate a later input-free internal continuation from persistent state that reaches lower-field spikes/patterns and potentially Assembly/prediction/action behavior?

Reduction/falsifier: no empty-step continuation reduces the current mechanism; if continuation occurs, a pre-bound matched comparator clears only the pending field-event queue to test ordinary finite recurrent carryover.

Non-authoritative branch: `research/exploratory-sub-endogenous-continuation-20260920`. Prospective binding `edd8dc67f1b1ab22fc8b2914cab774c1aadf49de`; initial diagnostic `8df025745b803fbfac326072b0283719b59ec082`; science-invariant harness correction `d039f0012b0cbe3826146ed76ae6b791b4abe848`; final research head `af201c25d3a5e7f1fde15b07b82aa0aad77cbd3f`.

DEV-only inputs: default `IntegratedV05Brain`, 16 training episodes at seed 907, then one fixed `jitter` DEV probe shifted prospectively to start 100 ms after current time. Driven and empty probes used `learn_assembly=false`, `learn_field=false`, `explore_action=false`. No formal/sealed TEST, official scorer, repository evidence dataset or consumed identity was used; production source was unchanged.

## Observation / reduction

Driven probe: 9 lower-field spikes, 1 internal pattern, mature `assembly-0001`, prediction `outcome-0`, action `action-0`.

Immediately following empty-input step: 0 lower-field spikes, 0 internal patterns, no mature Assembly, no prediction, field queue 0 before and 0 after. It returned literal `withhold`, which stable `AssemblyActionPolicy` defines as the default null-activation output (`assembly_id=null`), not an endogenous causal action.

The first diagnostic CI `35494974118` failed only because the exploratory harness incorrectly expected action `None`; the failure already showed no internal continuation and an empty queue. The correction changed only that expectation to the stable API contract and added queue assertions, without changing science inputs or terminal. Corrected CI `35495129863` passed Python 3.11/3.13. Final exact-head CI `35495326487` on `af201c25...` also passed both Python versions through lint, readiness, full tests and bundle validation.

Mapped terminal: `NO_INPUT_FREE_CONTINUATION_AT_DEFAULT_SETTLE_WITH_DEFAULT_WITHHOLD_ONLY`. Queue-clear comparator was unnecessary because the queue was already empty and continuation absent. No cycle-2 rescue/tuning is performed.

## Typing / readiness / hold

- proposed claim_ceiling: `MECHANISM`
- proposed preformal_eligible: `false`
- readiness claim_type: `mechanism`
- supported_reachability: `DRIVEN_FUNCTIONAL_STATE_REACHED; INPUT_FREE_CONTINUATION_NOT_REACHED_ON_FIXED_PROBE`
- functional_consequence: `ABSENT_INPUT_FREE_INTERNAL_CONTINUATION`
- ordinary reductions specified/controlled: `PENDING_FIELD_QUEUE_CARRYOVER`
- reductions unresolved: `NONE_FOR_CURRENT_FIXED_PROBE`
- comparator status: `CONDITIONAL_QUEUE_CLEAR_NOT_REQUIRED_BECAUSE_QUEUE_ALREADY_EMPTY_AND_CONTINUATION_ABSENT`
- support breadth: `ONE_FIXED_DEFAULT_SUPPORTED_CONFIG; SEED_907; 16_TRAINING_EPISODES; ONE_JITTER_DEV_PROBE; ONE_IMMEDIATE_EMPTY_STEP`
- falsifier: `NO_INPUT_FREE_CONTINUATION_OR_COMPLETE_QUEUE_CARRYOVER_REDUCTION`
- open choices: any broader seed/config/timing/self-trigger question requires a fresh candidate and prospective contract
- formal claim ceiling: `NONE_FOR_CURRENT_NEGATIVE_RESULT`
- readiness status: `NOT_READY`
- hold_class: `null`
- hold_reason: `null`
- terminal_state: `TERMINAL_FOR_CURRENT_OBJECT`
- queue_state: `NOT_QUEUED`

## Integrity / completion

Utility request: none. Consumed identities this run: none. New FORMAL results: zero. No STARTED/control authority, formal/freeze/evidence ref, official score, sealed TEST access, immutable evidence mutation, research merge or stable-main mutation occurred.

Blocker: fresh Evidence Analyst classification/closure only.

Completion target `ACHIEVED_ONE_THEORY_BACKWARD_ENDOGENOUS_CONTINUATION_DISCOVERY_CYCLE_AND_REDUCED_TO_NO_INPUT_FREE_INTERNAL_CONTINUATION_AT_DEFAULT_SETTLE` — achieved.

History: `reports/orchestrator/history/2026-09-20/1556-sub.md`.
