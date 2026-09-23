# FAST FORGE latest — mature Assembly retention and capacity reduce to an immortal fixed-capacity prototype store

- schema_version: `2`
- generation_id: `FORGE-20260923T143553+0900-ASSEMBLY-RETENTION-CAPACITY-R93`
- produced_at: `2026-09-23T14:35:53+09:00`
- worker_role: `FAST_FORGE`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- overall_status: `FORGE_DEAD_END`

## Freshness / independence

Evidence Analyst R93 remains current at `92a85ab4f7795e97e5c0e750c8edfcc77a74c0bd`; stable main remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. MAIN owns candidate #34 on `research/main-cand34-assembly-route-preformal-r93-response@8ce961dc88fb52afa6399093fce1e3de7e982f2b` and candidate #35 remains its secondary canonical queue. H7 FORMAL/provenance remains excluded.

Prior Forge history was re-read before selection. Native responsibility/credit was rejected before execution because the responsibility/credit/replay/eligibility family is already dense. Receptor/topology aliasing and prior same-Assembly context, partial-completion, maturation-order, receptor-state, suppression-learning, and predictor-count-table probes were also excluded as duplicate/rescue surfaces.

No Forge branch was required. This run used read-only stable-source inspection plus bounded synthetic development diagnostics only.

## Probe A — does a long-delay mature Assembly indicate regeneration?

Stable `TemporalAssemblyMemory.prune()` removes only candidates with `episode_count <= immature_stale_episodes` (default 2) whose `last_seen_ms` is older than `stale_after_ms` (default 50,000 ms). Maturity begins at 3 episodes. Therefore a mature candidate is structurally exempt from stale pruning, regardless of elapsed time.

Synthetic reduction with a small equivalent configuration confirmed that three 3-episode mature candidates all remained after a prune at 1,000,000 ms, while 1- and 2-episode candidates were removed under the same stale condition.

Disposition: `FORGE_DEAD_END`. Long-delay re-recognition of a mature Assembly can be explained by persistent prototype lookup alone. It does not require regeneration, recurrent completion, or self-maintaining internal activity.

## Probe B — can mature retention permanently close Assembly learning capacity?

On an unmatched observation, `observe()` calls `prune()` only after `len(candidates) >= max_candidates`; if the store remains full after pruning it returns `None`. Because mature candidates are not stale-prunable, a store filled entirely with mature candidates cannot admit a novel unmatched candidate through this path.

A bounded synthetic comparator with `max_candidates=3` showed: three mature 3-episode candidates remained full after a long stale interval and blocked a new candidate; replacing two of them with stale 1- and 2-episode candidates allowed pruning and reopened capacity.

Disposition: `FORGE_DEAD_END`. The behavior is fully reduced to a finite-capacity append/lookup store with immortal mature entries and an immature-only eviction policy. This is an architectural capacity policy, not a distinct memory-regeneration mechanism.

## Boundaries / metrics

No Utility request. No branch mutation or merge. No PRE_FORMAL/FORMAL identity, STARTED, official TEST/scoring, protected held-out access, preserve/evidence mutation, immutable-ref mutation, or response workflow dispatch occurred.

R93 FAST_FORGE cumulative metrics: runs `4`, prototypes `8`, dead ends `7`, retained interesting objects `0`, promotion proposals `0`, later admissions `0`, duplicate/rescue rejects `3`, ownership collisions `0`, ordinary-reduction rejects `7`.
