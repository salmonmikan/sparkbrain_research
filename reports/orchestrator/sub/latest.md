# FAST FORGE latest — two bounded dead ends

- schema_version: `2`
- generation_id: `FORGE-20260923T114344+0900-R92-RECEPTOR-SUPPRESSION-DEADENDS`
- produced_at: `2026-09-23T11:43:44+09:00`
- worker_role: `FAST_FORGE`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- overall_status: `FORGE_DEAD_END`

## Freshness / independence

Evidence Analyst R92 remains current at `a05ab3f655a23eabd84c910ba337d64a948c168a`. Stable main remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. MAIN currently owns candidate #34 PRE_FORMAL R2 on `research/main-cand34-assembly-route-preformal-r92-cycle4@1f9c6cec8be0af900a801de17dcc91e57dd71d7a`; candidate #35 is queued for MAIN Architecture R1; H7/PF-R1 remains critical-path/formal-provenance work. Forge touched none of them.

Forge used only `forge/20260923-receptor-suppression-probes-a@c366c4054d2834003fcca20d49b8fc9ad4203edc`, branched from stable main. Development CI `35811319345` completed success on Python 3.11 and 3.13 through lint, readiness, full tests and bundle validation.

## Probe 1 — receptor-bank persistent cue priming

A `1.0` prime followed by an identical `0.10` cue produced emitted magnitudes `0.5562423166417022` at 10 ms and `0.49106890868271347` at 120 ms, versus `0.228` in a fresh bank; by 1000 ms it returned to `0.2285379965673357`. The entire effect matched a separately coded closed-form application of the declared 5/22/120 ms receptor traces, 180 ms gain state, derivative/novelty terms and gain clamp to `1e-12` absolute tolerance.

Disposition: `FORGE_DEAD_END`. The persistent response is fully explained by the explicit deterministic receptor filter/register state. No promotion proposed.

## Probe 2 — Assembly suppression permits silent maturation

An immature Assembly was suppressed after its first episode. Two further distinct episodes with `learn=true` still accumulated into the same candidate; it reached the three-episode maturity threshold while suppressed. After unsuppression, a `learn=false` query returned it immediately as mature with `episode_count=3`.

Disposition: `FORGE_DEAD_END`. Stable `TemporalAssemblyMemory.suppress()` is a readout mask, not a learning freeze; `observe(..., learn=true)` continues updating the candidate. The retained canonical `causal_ablation` path uses `learn=false` while suppression is active, so this does not expose a hidden defect in that current ablation. No promotion proposed.

## Boundaries / metrics

No Utility request. No merge to main/research. No PRE_FORMAL/FORMAL identity, STARTED, official scoring, protected held-out access, preserve/evidence mutation, or immutable-ref mutation occurred.

R92 FAST_FORGE metrics now: runs `1`, prototypes `2`, dead ends `2`, retained interesting objects `0`, promotion proposals `0`, later admissions `0`, duplicate/rescue rejects `0`, ownership collisions `0`, ordinary-reduction rejects `2`.
