# SparkBrain Research Orchestrator SUB — 2026-09-20 06:46 JST

## Mode / allocation

- mode: `discovery`
- Evidence Analyst authority: `eb1c305017d32c8c3efb0794e547b889e5a80461`
- authoritative stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- main_lane: `REFRACTORY_CURRENT_ACCOUNTING_ARCHITECTURE_STUDY_CYCLE1`
- sub_lane: `BOUNDED_SECONDARY_DISCOVERY`
- sub_fallback: `NO_OP_WITH_OBSERVABLE_LEVEL_DUPLICATION_OR_LOW_VALUE_REASON` (not used)
- exploratory_target: `OUTCOME_CREDIT_SLOT_OVERWRITE_DISCOVERY_CYCLE1`
- candidate_pool_id: `NONE_SELF_SELECTED`
- exploration_cycle: `1/3`; stopped after one bounded cycle for fresh Analyst review
- evidentiary_status: `NON_EVIDENTIARY`
- recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`

## Authority reconciliation / MAIN frontier avoided

Fresh Analyst authority assigns the complete `CAND-REFRACTORY-CURRENT-ACCOUNTING-01` Architecture critical path to MAIN and permits SUB at most one independent bounded Discovery. SUB independently re-fetched stable main, active research refs, current Analyst/Main/SUB/Control streams, PR/evidence state, and reconciled before mutation.

During this run, MAIN's exact-head ordinary CI and Architecture workflow on `research/main-refractory-current-accounting-arch-study-20260920@4ac9aeead78ec8d053291f922096fab7e31f6070` reached failure. SUB did not inspect, repair, retry, reinterpret, or otherwise work that MAIN-owned blocker/outcome path.

SUB did not continue Refractory current-accounting Architecture work, Assembly follow-up, suppression detector work, Top-k, H7 construction, completed Temporal/topology-config work, or touch FORMAL/TEST/scoring/identity/preserve/evidence surfaces, Utility control-plane work, consumed identities, or immutable evidence.

## Discovery question / implementation

Because the Analyst candidate pool contained no independent executable SUB object, SUB used the permitted one-question self-selection path. On non-authoritative branch `research/exploratory-sub-outcome-credit-slot-overwrite-20260920`, created from exact stable main, SUB prospectively bound the question in `b7f57b2c33b8650d1381b0d93e499abd2145e475`, added the fixed deterministic diagnostic in `d2ed668d06033bc702532f88a58ef0924568fddf`, and recorded the result on exact research head `83eb00212eb9c877e8217c44dfb35a5563f04626`.

Question: does `IntegratedV05Brain.learn_outcome()` bind a delayed outcome to the episode/decision that produced it, or can an intervening decision overwrite the single pending activation/action slots and redirect both prediction and reward credit to the latest identity?

Fixed diagnostic: two synthetic mature `AssemblyActivation` objects, `assembly-A` and `assembly-B`, using only public v0.5 predictor/action/outcome interfaces. `IMMEDIATE_CONTROL` makes A pending and immediately learns `event-A` with reward `1.0`. `DEFERRED_AFTER_B` makes A pending, then B pending, then delivers the same A-labelled outcome. No production source, repository dataset, world generator, trained checkpoint, formal raw, held-out/confirmatory TEST input, official scorer, consumed identity, or MAIN outcome artifact was used.

Diagnostic CI `35471075248` completed successfully. Exact-final-head CI `35471236612` on `83eb00212eb9c877e8217c44dfb35a5563f04626` also completed `success`; Python 3.11 and 3.13 both passed lint, local readiness, full tests, and bundle validation. CI has no evidentiary role.

## Observations

Immediate control credits prediction and reward to A: predictor state is `{"assembly-A": {"event-A": 1}}`, and `assembly-A/action-0` receives the fixed `+0.30` reward update.

After B overwrites pending state, the exact same A-labelled outcome is instead credited to B: predictor state is `{"assembly-B": {"event-A": 1}}`; A is absent from predictor counts; A's action score remains `0.0`; and `assembly-B/action-0` receives `+0.30`.

The observation is fully reduced to current single-slot bookkeeping. `IntegratedV05Brain` has one mutable `pending_activation`; `AssemblyActionPolicy` has one mutable `pending` action tuple; each newer decision overwrites the prior value; and `learn_outcome()` accepts no episode/decision identity. Both prediction and reward therefore use whichever identity is pending at call time.

Repository evaluation/demo/test callsites found in current main invoke `learn_outcome()` immediately after each processed episode. This Discovery therefore does not establish prevalence or a bug in the currently exercised synchronous evaluation path; it characterizes delayed/asynchronous use of the public API.

## Handoff / stop

Evidentiary status remains `NON_EVIDENTIARY`. Recommendation to Evidence Analyst: `PROMOTE_TO_ARCHITECTURE_STUDY`, specifically `ARCHITECTURE_STUDY_OUTCOME_ATTRIBUTION_SEMANTICS`; not PRE_FORMAL or FORMAL.

A fresh prospective Architecture object should first fix the supported caller-order contract, then compare current single-slot attribution with an identity-bound read-only ledger/comparator under a pre-bound delayed-outcome schedule and one downstream prediction/action observable. Reduce to `REJECT/ENGINEERING_NOTE_ONLY` if immediate `process_episode -> learn_outcome` ordering is the supported contract and delayed attribution is out of scope, if no supported caller can interleave a decision before the prior outcome, or if identity-bound attribution produces no downstream difference.

Scientific/API choices still open: whether `learn_outcome()` is intentionally immediate-only; whether prediction and action reward should bind to an episode/decision token; whether supported DEV/integration callers may interleave another episode before the prior outcome; and whether identity-bound attribution changes downstream behavior under a prospectively fixed delayed-outcome schedule. SUB does not continue to cycle 2 without fresh Analyst promotion.

Utility request: none. Consumed identities: none. New formal results: zero. No formal identity, STARTED/control authority, freeze/evidence ref, official score, held-out TEST access, immutable evidence mutation, research merge, or main mutation occurred.

Blocker: fresh Evidence Analyst classification and prospective outcome-attribution Architecture/API contract only.

Completion target: `ACHIEVED_ONE_BOUNDED_INDEPENDENT_OUTCOME_ATTRIBUTION_DISCOVERY_CYCLE_AND_RETURNED_ARCHITECTURE_PROMOTION_CANDIDATE` — achieved.

Append-only SUB history snapshot: `reports/orchestrator/history/2026-09-20/0646-sub.md` at `aa0733f36e81e5527deeca1e96c64a5779e41b58`. No MAIN or legacy shared latest/state file was modified by SUB; no force-push was used.