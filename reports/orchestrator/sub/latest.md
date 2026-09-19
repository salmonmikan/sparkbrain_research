# SparkBrain Research Orchestrator SUB — 2026-09-20 07:50 JST

## Mode / allocation

- mode: `discovery`
- Evidence Analyst authority: `7e7d425948a86d0eec306b1a75bfc07165d9afa1`
- authoritative stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- main_lane: `REFRACTORY_CURRENT_ACCOUNTING_ARCHITECTURE_STUDY_CYCLE1`
- sub_lane: `BOUNDED_SECONDARY_DISCOVERY`
- sub_fallback: `NO_OP_WITH_OBSERVABLE_LEVEL_DUPLICATION_OR_LOW_VALUE_REASON` (not used)
- exploratory_target: `ASSEMBLY_MATURE_CAPACITY_LOCKOUT_DISCOVERY_CYCLE1`
- candidate_pool_id: `NONE_SELF_SELECTED`
- exploration_cycle: `1/3`; stopped after one bounded cycle for fresh Analyst review
- evidentiary_status: `NON_EVIDENTIARY`
- recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`

## Authority reconciliation / MAIN frontier avoided

Fresh Analyst authority reserved `CAND-REFRACTORY-CURRENT-ACCOUNTING-01` and its complete Architecture critical path for MAIN, queued the delayed-outcome candidate outside SUB authority, and allowed SUB at most one independent bounded Discovery. The named candidate pool contained no independently executable SUB object, so SUB used the permitted one-question self-selection path.

The selected target is limited to stable v0.5 `TemporalAssemblyMemory` capacity/pruning semantics. SUB did not work MAIN's Refractory branch, comparator, blocker, outcome, or successor; did not continue the queued delayed-outcome candidate; did not touch suppression Utility work, completed Assembly cross-cascade work, Temporal/topology-config work, Top-k, H7, consumed identities, FORMAL/TEST/scoring/identity/preserve/evidence surfaces, or immutable evidence.

During final reconciliation, MAIN independently reached terminal `FUNCTIONAL_REFRACTORY_ACCOUNTING_EFFECT` and stopped for fresh Evidence Analyst review. The Evidence Analyst tip remained `7e7d425948a86d0eec306b1a75bfc07165d9afa1`; no changed allocation invalidated this independent SUB target.

## Discovery question / implementation

Question: when `TemporalAssemblyMemory` reaches `max_candidates` with only mature stale candidates, does the current prune policy deny a genuinely dissimilar new pattern indefinitely, while an otherwise matched immature stale candidate is reclaimable?

SUB created non-authoritative branch `research/exploratory-sub-assembly-capacity-lockout-20260920` from exact stable main. The fixed question/diagnostic were prospectively bound at `d45926e153b638e1ba980cdb108fb8d3d8137439`, the deterministic diagnostic was added at `ced4850fcf7dc7d4aa02b21f3ebc118abb112456`, and the result/handoff was recorded on exact research head `3cac844ca6a80725c87d7e681c23b703f35150c2`.

Fixed synthetic configuration: `similarity_threshold=0.66`, `mature_episodes=2`, `max_candidates=2`, `stale_after_ms=10.0`, `immature_stale_episodes=1`. Fixed P1 `(1,2)`, P2 `(3,4)`, P3 `(5,6)` all use relative bins `(0,1)` and have pairwise `pattern_similarity=0.2`, below the fixed match threshold.

`MATURE_SATURATED` matures P1 and P2 across two distinct episodes each, then presents P3 at `100.0 ms` and again at `1000.0 ms`. `IMMATURE_RECLAIMABLE` matures P1, observes P2 once, then presents P3 at `100.0 ms`. No production source, repository dataset, world generator, checkpoint, formal raw, held-out TEST, official scorer, consumed identity, or MAIN outcome artifact was used to design/run the diagnostic.

Exact-final-head ordinary CI `35474327443` on `3cac844ca6a80725c87d7e681c23b703f35150c2` completed `success`; Python 3.11 and 3.13 both passed lint, local readiness, full tests, and bundle validation. CI has no evidentiary role.

## Observations

In `MATURE_SATURATED`, the two slots are `assembly-0001 / pattern-p1 / episode_count=2` and `assembly-0002 / pattern-p2 / episode_count=2`. P3 returns `None` at `100.0 ms` and again at `1000.0 ms`; both mature candidates remain and P3 never acquires a slot.

In `IMMATURE_RECLAIMABLE`, P2 has `episode_count=1`; at `100.0 ms` it is stale and is removed, allowing P3 to enter as `assembly-0003`. Remaining candidates are `assembly-0001` and `assembly-0003`.

The observation is fully reduced to current resource policy. When a new dissimilar pattern arrives at capacity, `observe()` invokes `prune()`, while `prune()` only removes stale candidates whose `episode_count <= immature_stale_episodes`. Mature candidates therefore lie outside this reclamation path. Default configuration preserves the same structural relation (`mature_episodes=3`, `immature_stale_episodes=2`), but this cap-two synthetic probe does not establish that supported/default workloads actually saturate the default `max_candidates=256`.

This is functionally stronger than metadata-only divergence because a new dissimilar pattern receives no candidate/activation path once every slot is mature in the fixed probe. It does not establish real-world prevalence, downstream behavioral impairment, or scientific novelty.

## Handoff / stop

Evidentiary status remains `NON_EVIDENTIARY`. Recommendation to Evidence Analyst: `PROMOTE_TO_ARCHITECTURE_STUDY`, specifically `ARCHITECTURE_STUDY_ASSEMBLY_CAPACITY_AND_LIFELONG_PLASTICITY_SEMANTICS`; not PRE_FORMAL or FORMAL.

A fresh prospective Architecture object should first bind whether `max_candidates` is a hard lifetime mature-memory cap or an active working-set resource budget. If promoted, use DEV-only streams that fill mature capacity before a genuinely novel pattern, compare current mature retention against an identity-neutral/resource-matched turnover comparator, and pre-bind resource budget plus one downstream Assembly prediction/action learnability observable.

Reduce to `REJECT/ENGINEERING_NOTE_ONLY` if permanent mature retention is the supported contract with no ongoing acquisition requirement, if supported workloads cannot plausibly approach mature saturation, or if a fresh resource-matched turnover comparator changes no pre-bound downstream learnability observable.

Scientific/API choices still open: whether mature assemblies are permanent; whether they may age/compact/evict; what turnover comparator is identity-neutral/resource-matched; what supported DEV horizon makes saturation relevant; and which downstream observable should represent retained capacity for new learning. SUB does not continue to cycle 2 without fresh Analyst promotion.

Utility request: none. Consumed identities: none. New formal results: zero. No formal identity, STARTED/control authority, freeze/evidence ref, official score, held-out TEST access, immutable evidence mutation, research merge, or main mutation occurred.

Blocker: fresh Evidence Analyst classification and prospective assembly-capacity/lifecycle Architecture contract before any continuation.

Completion target: `ACHIEVED_ONE_BOUNDED_INDEPENDENT_ASSEMBLY_CAPACITY_DISCOVERY_CYCLE_AND_RETURNED_RESOURCE_SEMANTICS_PROMOTION_CANDIDATE` — achieved.

Append-only SUB history snapshot: `reports/orchestrator/history/2026-09-20/0750-sub.md` at `a2381ee51087c0da69708b485bc920242ebdf82f`. No MAIN or legacy shared latest/state file was modified by SUB; no force-push was used.