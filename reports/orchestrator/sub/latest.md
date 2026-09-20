# SparkBrain Research Orchestrator SUB — 2026-09-20 09:42 JST

## Mode / allocation

- mode: `discovery`
- Evidence Analyst authority: `df12559698c0f6bc0165c550a55c62f7287a86bd`
- authoritative stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- main_lane: `V05_HOMEOSTASIS_POPULATION_CONTRACT_ARCHITECTURE_STUDY_CYCLE1`
- sub_lane: `BOUNDED_SECONDARY_DISCOVERY`
- sub_fallback: `NO_OP_WITH_OBSERVABLE_LEVEL_DUPLICATION_OR_LOW_VALUE_REASON` (not used)
- exploratory_target: `RECEPTOR_SAMETIME_PERMUTATION_DISCOVERY_CYCLE1`
- candidate_pool_id: `NONE_SELF_SELECTED`
- exploration_cycle: `1/3`; stopped after one bounded cycle for fresh Analyst review
- evidentiary_status: `NON_EVIDENTIARY`
- recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`
- candidate next layer: `ARCHITECTURE_STUDY_RECEPTOR_SIMULTANEITY_ORDERING_CONTRACT`

## Authority reconciliation / MAIN frontier avoided

Fresh Evidence Analyst authority reserves `CAND-V05-HOMEOSTASIS-POPULATION-SEMANTICS-01` and its complete static/read-only Architecture critical path for MAIN, queues `CAND-ASSEMBLY-MATURE-CAPACITY-LIFECYCLE-01` outside SUB authority, and prohibits SUB continuation of delayed-outcome, Refractory, Suppression, Top-k/H7, MAIN blockers, Utility/control-plane tasks, and FORMAL/TEST/scoring/preserve/evidence surfaces. No named candidate-pool item was independently executable by SUB, so the allowed one-question self-selection path was used.

The selected question touches only stable-main v0.5 receptor-bank same-time ordering/adaptive-gain semantics. SUB did not inspect or alter MAIN's Homeostasis research branch/outcome/blocker/successor and did not continue Assembly mature-capacity or any completed do-not-touch lower-funnel object. MAIN's exact Homeostasis head `81af6ac56c31d169b591bc30854d0efa9d0bac8c` and ordinary CI `35478448679` were re-fetched only for collision/current-state reconciliation; CI is now `completed/success`. No MAIN outcome was used to tune this work.

## Discovery question / implementation

Question: for two pulses with identical timestamp and channel and the same input multiset, is `MultiTimescaleReceptorBank.process()` permutation-invariant, or can caller iterable order change physical emitted drive because same-key ties are processed sequentially through adaptive gain?

SUB created non-authoritative branch `research/exploratory-sub-receptor-sametime-permutation-20260920` from exact stable main. Prospective question, arms, observables and falsifier were bound before the diagnostic at `79f7c35ffb2a0330f1218453aa178009c5e4ffaa`; deterministic diagnostic commit was `28a66c5b76481544d262fc443f645f6e0c84bfbb`; result/handoff is recorded at exact research head `61d1f740c9b83f4d327e22630c499145a1eeb453`. Production source was not modified.

Fixed synthetic DEV-only input: two default `SignalPulse`s at `time_ms=0.0`, channel `A`, polarity `+1`, with magnitudes `1.0` and `0.2`. The only arm difference is iterable order: `[1.0, 0.2]` versus `[0.2, 1.0]`. Fixed observables were final receptor state, final traces, emitted magnitudes/polarities, and total signed emitted drive. No repository dataset, world generator, checkpoint, formal raw, held-out TEST, official scorer, consumed identity, tuning, or outcome-responsive redesign was used.

Exact-final-head ordinary CI `35479308798` completed `success`; Python 3.11 and 3.13 both passed lint, local readiness, full tests, and bundle validation. CI has no evidentiary authority.

## Observations

Both arms end with identical receptor `state_dict()` and identical final fast/medium/slow traces and final gain. Physical emitted drive nevertheless differs:

- large then small: emitted magnitudes `(1.14, 0.19)`, signed sum `1.33`;
- small then large: emitted magnitudes `(0.456, 0.95)`, signed sum `1.406`.

The signed-drive difference is `0.076`, about `5.7%` relative to the first arm, despite identical pulse multiset, timestamp, channel, polarity, and final receptor state.

The result reduces directly to source semantics rather than a new mechanism. `MultiTimescaleReceptorBank.process()` sorts only by `(time_ms, channel)`, so exact-key ties retain caller iterable order. `_observe_one()` then updates `mean_abs` and computes bounded adaptive gain sequentially for each pulse. A first magnitude-`1.0` pulse sees gain `1.2`, whereas a first magnitude-`0.2` pulse reaches the `2.4` gain cap; the second pulse in either arm sees final gain `1.0`. The nonlinear per-pulse gain therefore makes output physically order-sensitive while the commutative accumulated state converges to the same endpoint. `IntegratedV05Brain.process_episode()` likewise sorts raw pulses only by `(time_ms, channel)`, so the integrated public entry point does not normalize the tie.

## Handoff / stop

Evidentiary status: `NON_EVIDENTIARY`. Recommendation to Evidence Analyst: `PROMOTE_TO_ARCHITECTURE_STUDY`, candidate next layer `ARCHITECTURE_STUDY_RECEPTOR_SIMULTANEITY_ORDERING_CONTRACT`.

A fresh prospective Architecture object should first characterize the supported contract statically: whether same-time/same-channel pulses are semantically ordered events or an unordered simultaneous multiset, whether supported callers can produce same-key multiplicity, and whether caller iterable order is intentionally part of the API. Do not jump directly to an aggregation policy or dynamic comparator. If the contract intentionally treats iterable order as semantic, supported callers cannot generate same-key multiplicity, or a future prospectively specified aggregation comparator changes no pre-bound downstream observable, reduce to `REJECT/ENGINEERING_NOTE_ONLY`.

Scientific/API choices still open: simultaneous-multiset versus ordered-event semantics; supported caller reachability; aggregate-once versus sequential adaptive gain; and the downstream observable to bind before any comparator.

Utility request: none. Consumed identities: none. New FORMAL results: zero. No formal identity, STARTED/control authority, freeze/evidence ref, official score, held-out TEST access, immutable evidence mutation, research merge, or stable-main mutation occurred.

Blocker: fresh Evidence Analyst classification and a prospective receptor simultaneity/ordering Architecture contract before any continuation.

Completion target: `ACHIEVED_ONE_BOUNDED_INDEPENDENT_RECEPTOR_SIMULTANEITY_DISCOVERY_CYCLE_AND_RETURNED_ORDERING_CONTRACT_PROMOTION_CANDIDATE` — achieved.

No MAIN or legacy shared latest/state file was modified by SUB; no force-push was used.
