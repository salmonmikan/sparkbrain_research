# FAST FORGE latest — Assembly identity continuity and multi-Assembly functional binding reduce to ordinary implementation semantics

- schema_version: `2`
- generation_id: `FORGE-20260923T153500+0900-ASSEMBLY-IDENTITY-COACTIVATION-R94`
- produced_at: `2026-09-23T15:35:00+09:00`
- worker_role: `FAST_FORGE`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- overall_status: `FORGE_DEAD_END`

## Freshness / independence

Evidence Analyst R94 is current at `5cee6ef496eb9465550fb9c0be5295e587027dfb`; stable main remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. MAIN owns candidate #34 and its one-shot PRE_FORMAL R2 result/preservation boundary; candidate #35 remains the secondary canonical queue and H7 FORMAL/provenance remains excluded. Literature R37 is newer than the Analyst report and was re-read before persistence; it reports that the #34 one-shot workflow has completed and that its raw artifact must remain unread until durable preservation. Forge did not access that workflow artifact or any #34 response surface.

Prior Forge state/history was re-read. Native responsibility/credit was explicitly rejected before execution because the responsibility/credit/replay/eligibility family is already dense. Receptor/topology aliasing, same-Assembly contextual action, partial-completion, maturation-order, receptor-state, suppression-learning, predictor-count-table, and mature-retention/capacity probes were excluded as duplicate/rescue surfaces.

No Forge branch was required. This run used read-only stable-source inspection only.

## Probe A — can pruning recycle an Assembly identity and inherit stale downstream meaning?

`TemporalAssemblyMemory._new_candidate()` allocates `assembly-{next_id}` and increments `next_id`. `prune()` can delete stale immature candidates, but it does not decrement or recycle `next_id`; checkpoint serialization persists and restores that monotonic counter. Predictor counts and action scores are keyed by Assembly ID and do not have explicit prune cleanup, but a later normally created Assembly cannot receive a deleted ID.

Disposition: `FORGE_DEAD_END`. Stale downstream table rows can remain inert, but ordinary runtime evolution does not rebind them to a new Assembly. Producing inheritance would require malformed/manual state that violates the normal monotonic identifier lifecycle, reducing the idea to checkpoint/API corruption rather than a scientific phenomenon.

## Probe B — can simultaneous Assemblies jointly acquire functional meaning at the v0.5 outcome layer?

`process_episode()` may collect multiple Assembly activations, but it constructs `usable` and then chooses exactly one `strongest` activation by similarity, episode count and Assembly ID. Only that single activation is passed to the predictor and action policy and stored as `pending_activation`; `learn_outcome()` subsequently updates prediction/action state only through that pending single Assembly/action path.

Disposition: `FORGE_DEAD_END`. At this layer, simultaneous Assembly coactivity is reduced to a deterministic winner-take-all selector followed by a single Assembly-ID lookup/update. A conjunction or distributed functional binding cannot be inferred from this path itself; adding joint-state/context keys would be an ordinary representation change, not evidence of a new mechanism.

## Ordinary reductions / boundaries

Probe A reduces to monotonic identifier allocation plus inert stale dictionary rows. Probe B reduces to winner-take-all selection plus single-key lookup/credit. Neither leaves a distinct bounded mechanism residual suitable for promotion.

No Utility request. No code or branch mutation, merge, candidate-response execution, PRE_FORMAL/FORMAL identity, STARTED, official TEST/scoring, protected held-out access, preserve/evidence mutation, immutable-ref mutation, or response workflow dispatch occurred.

R94 FAST_FORGE cumulative metrics: runs `5`, prototypes `10`, dead ends `9`, retained interesting objects `0`, promotion proposals `0`, later admissions `0`, duplicate/rescue rejects `4`, ownership collisions `0`, ordinary-reduction rejects `9`, idea-to-observation latency `within_run`.
