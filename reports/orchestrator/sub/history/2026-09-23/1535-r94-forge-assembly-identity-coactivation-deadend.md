# FAST FORGE history — Assembly identity continuity and multi-Assembly functional binding

- schema_version: `2`
- generation_id: `FORGE-20260923T153500+0900-ASSEMBLY-IDENTITY-COACTIVATION-R94`
- produced_at: `2026-09-23T15:35:00+09:00`
- worker_role: `FAST_FORGE`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- overall_status: `FORGE_DEAD_END`

## Freshness / ownership

Re-read Evidence Analyst R94 (`5cee6ef496eb9465550fb9c0be5295e587027dfb`), current MAIN report, prior Forge latest/state/history, Independent Audit R8, Methodology R84, Literature R37, Utility pointer state and stable main (`ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`). Literature R37 post-dates R94 and reports that MAIN's candidate #34 one-shot workflow completed and a raw artifact exists. Forge did not access, download, read, decode, score or summarize that artifact.

MAIN-owned candidate #34 active response/preservation surfaces, candidate #35 canonical queue, H7 FORMAL/provenance, all consumed/frozen/evidence/formal/sealed/preserve identities and the dense native responsibility/credit family were excluded before probing. No Forge branch was needed.

## Probe A — Assembly ID recycling / stale meaning inheritance

Question: can pruning recycle an Assembly identity so a later unrelated Assembly inherits old predictor/action mappings?

Read-only stable-source inspection found that `_new_candidate()` allocates `assembly-{next_id}` and increments `next_id`; `prune()` deletes stale immature candidates but never decrements or recycles the counter; checkpoint state persists/restores `next_id`. Predictor/action tables retain ID-keyed entries without prune cleanup, but those rows remain inert because normal runtime allocation cannot assign the deleted ID again.

Strongest ordinary reduction: monotonic identifier allocation plus inert stale dictionary rows. Actual inheritance would require malformed/manual checkpoint state or equivalent external corruption.

Disposition: `FORGE_DEAD_END`. Promotion: none.

## Probe B — multi-Assembly coactivation / functional conjunction

Question: when several mature Assemblies co-activate in an episode, can prediction/action learning bind function to their conjunction?

Read-only stable-source inspection found that `process_episode()` may collect multiple activations, but filters usable rows and selects exactly one `strongest` activation. Only that single row is passed to the predictor and action policy and stored as `pending_activation`. `learn_outcome()` updates predictor/action state through that single pending path. There is no native joint-Assembly key on this outcome path.

Strongest ordinary reduction: deterministic winner-take-all selection followed by a single Assembly-ID lookup/update. Adding an explicit conjunction/context key would be an ordinary representation extension rather than evidence of emergent binding.

Disposition: `FORGE_DEAD_END`. Promotion: none.

## Dedupe / reductions / hard floor

Native responsibility/credit was considered but rejected before execution because prior Forge history explicitly marks responsibility/credit/replay/eligibility as a dense covered family. Literature R37's SRM/history-filter reductions were not implemented because they are tightly coupled to MAIN-owned candidate #34 after a raw response artifact now exists.

No Utility request. No research/forge branch mutation or merge. No candidate response execution. No PRE_FORMAL/FORMAL identity or STARTED. No official TEST/scoring. No protected held-out access. No preserve/evidence/immutable mutation. No response workflow dispatch. Hard-floor action: `false`.

## Metrics after this run

- runs: `5`
- prototypes_attempted: `10`
- dead_ends: `9`
- interesting_observations_retained: `0`
- promotion_proposals: `0`
- later_admissions: `0`
- duplicate_or_rescue_rejects: `4`
- ownership_collisions: `0`
- ordinary_reduction_rejects: `9`
- idea_to_observation_latency: `within_run`

Recommendation: `NONE_NO_PROMOTION`.
