# FAST FORGE — receptor-memory / assembly-suppression probes

- schema_version: `2`
- generation_id: `FORGE-20260923T114344+0900-R92-RECEPTOR-SUPPRESSION-DEADENDS`
- produced_at: `2026-09-23T11:43:44+09:00`
- worker_role: `FAST_FORGE`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- overall_status: `FORGE_DEAD_END`

## Freshness / ownership

Re-fetched stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`, Evidence Analyst R92 at `a05ab3f655a23eabd84c910ba337d64a948c168a`, current MAIN lease, Literature R35, Audit R8, Methodology R79, Utility PF-R1 status, terminal exploratory branches and Forge history before work.

MAIN owns candidate #34 PRE_FORMAL R2 on `research/main-cand34-assembly-route-preformal-r92-cycle4@1f9c6cec8be0af900a801de17dcc91e57dd71d7a`; candidate #35 is queued for MAIN Architecture R1 non-result; H7/PF-R1 remains critical-path/formal-provenance work. No separate Relay branch was observed. None of those surfaces were modified, executed, scored or depended upon.

Forge branch: `forge/20260923-receptor-suppression-probes-a@c366c4054d2834003fcca20d49b8fc9ad4203edc`, based directly on stable main. Branch CI run `35811319345` completed success for Python 3.11 and 3.13, including lint, local readiness, full pytest and bundle validation. This is development validation only.

## Prototype 1 — receptor-memory cue priming

- forge_id: `FORGE-RECEPTOR-MEMORY-PRIMING-A`
- question: Can silent state in `MultiTimescaleReceptorBank` materially amplify a later identical weak cue, and is any residual richer than the declared fast/medium/slow/gain filter?
- why_now: candidate #35 explicitly excludes receptor-bank memory and targets physical field `UnitState`; receptor-bank persistent state is therefore an independent layer rather than a hidden dependency on #35.
- implementation: actual stable v0.5 receptor code was probed with one channel, prime magnitude `1.0`, later cue magnitude `0.10`, and gaps `10`, `120`, `1000 ms`. A separately coded closed-form comparator used the exact declared time constants/gain/novelty equations.
- observation: fresh cue emitted magnitude `0.228`; after priming the same cue produced `0.5562423166417022` at 10 ms, `0.49106890868271347` at 120 ms, and `0.2285379965673357` at 1000 ms. Every probed value matched the ordinary closed-form receptor recurrence to `1e-12` absolute tolerance.
- ordinary_reduction: explicit deterministic multi-timescale receptor filtering (`tau=5/22/120 ms` plus `180 ms` gain state), derivative/novelty terms and gain clamp fully account for the effect.
- status: `FORGE_DEAD_END`
- dead_end_reason: persistent cue priming is real at the implementation level but contains no residual beyond the already-declared filter/register state. It does not justify a fresh scientific candidate.

## Prototype 2 — suppressed Assembly learning / silent maturation

- forge_id: `FORGE-ASSEMBLY-SUPPRESSION-SILENT-MATURATION-A`
- question: Does Assembly suppression stop learning, or only mute readout, such that an immature Assembly can mature while suppressed and reappear already mature after unsuppression?
- why_now: this is a bounded causal-intervention semantic check independent of MAIN's active edge/timing route object. No prior branch name or source-history search showed this exact Assembly-suppression/learning interaction; prior unit-suppression latent-state work is a different intervention.
- implementation: stable `TemporalAssemblyMemory` was given one pattern. After one episode the immature candidate was suppressed; two further distinct episodes were observed with `learn=true`; suppression was then removed and the same pattern was queried with `learn=false`.
- observation: the suppressed candidate continued accumulating episode history and reached the configured three-episode maturity threshold while still suppressed. After unsuppression it immediately returned as mature with `episode_count=3`.
- ordinary_reduction: `suppress()` only adds the Assembly ID to a readout mask; `observe(..., learn=true)` updates occurrences/episode IDs regardless of suppression. The retained canonical `causal_ablation` path evaluates suppressed Assemblies with `learn=false`, so this semantic does not create a hidden contamination in that existing ablation.
- status: `FORGE_DEAD_END`
- dead_end_reason: this is an API/intervention-semantics fact, not a distinct scientific mechanism. It can matter when designing future learning-on suppression experiments, but no canonical promotion is warranted from this probe.

## Disposition

- promotion_proposals: `0`
- Utility request: `NONE`
- Forge branches merged to main/research: `NO`
- hard-floor action: `NO`
- PRE_FORMAL/FORMAL identity created or consumed: `NO`
- STARTED / official scorer / protected held-out touched: `NO`
- evidence/formal/sealed/freeze/preserve ref mutation: `NO`

## Metrics since R92 FAST_FORGE gate activation

- runs_observed: `1`
- prototypes_attempted: `2`
- dead_ends: `2`
- interesting_objects_retained: `0`
- promotion_proposals: `0`
- later_admissions: `0`
- duplicate_or_rescue_rejects: `0`
- ownership_collisions: `0`
- ordinary_reduction_rejects: `2`
- first executable probe latency from run start: approximately `433 s`
- both-probe CI confirmation latency from run start: approximately `614 s`

Exact source refs used: `src/sparkbrain/v05/receptors.py@86c1cfea1ea70cada5c277d8f5047c32ea611a5c`, `src/sparkbrain/v05/assemblies.py@a0a8c41e21db68cafc08ace8dac50b7a56607a52`, and `src/sparkbrain/v05/evaluation.py@efd52d236708aea3bf23b6139d8717b1ac1d0559` on stable main.
