# FAST FORGE — TH-001 Q0-vs-QI adaptation reduction

- schema_version: `2`
- generation_id: `FORGE-20260924T064230+0900-TH001-Q0-QI-ADAPTATION-KILL`
- produced_at: `2026-09-24T06:42:30+09:00`
- worker_role: `FAST_FORGE`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- overall_status: `FORGE_DEAD_END`
- theory_id: `TH-001-INTERVENTION-STABLE-CAUSAL-QUOTIENT`
- probe_class: `ANALYST_APPROVED_THEORY_FORGE_TEST`

## Freshness / authority

Before selection, Forge re-fetched stable main, Evidence Analyst, MAIN/Relay ownership, current Theory/Revisit stream, Literature, Independent Audit, Methodology, Utility, terminal/current candidates, and prior Forge history. Stable main was `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. Evidence Analyst R107 at `247a2e6349ada02a6fdb4a362318570b6dd74e90` explicitly retained TH-001 as `THEORY_FORGE_TEST` and supplied the bounded Q0-vs-QI probe specification. Methodology R99 independently corrected the earlier over-broad whole-theory kill: the prior recurrent-loop toy remains killed, but it did not instantiate the frozen Q0-vs-QI discriminator. Revisit remained 34/34 classified with zero triggered objects and no `REVISIT_FORGE_TEST`.

MAIN owns H7 only. H7 science/controller/launch/identity/START/runtime/scorer/preserver/protected-evaluator surfaces were excluded. Candidate #34 and #35 terminal/same-object rescue surfaces were excluded. No current MAIN outcome was required for this Theory probe.

## Forge object

- forge_id: `FORGE-TH001-Q0QI-20260924-A`
- question: Among two histories that are exactly equivalent under a predeclared ordinary future environment (Q0), can the same fixed local intervention split their downstream futures (QI), and if so does an ordinary state variable already predict the split?
- why_now: Analyst R107 explicitly supplied this bounded discriminator after determining that the prior recurrence prototype was non-diagnostic for TH-001 rather than a whole-theory falsification.
- branch: `forge/20260924-th001-q0-qi-adaptation-a`
- branch_base: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- prototype_commit: `e2dbe3a5a0db812f777b789a6878af8a0d3eee0f`
- prototype_path: `tests/forge/test_th001_q0_qi_adaptation_probe.py`

## Prototype / prospective discriminator

The synthetic v0.4 field uses three units. Unit 0 receives the fixed future environment; unit 1 is a local latent/intervention target; unit 2 is downstream of unit 1 through one fixed nonplastic edge (weight 1.0, delay 4 ms). All relevant base thresholds are 0.80.

Two histories are created before the frozen future:

1. `warm`: unit 1 receives one pulse at t=0 and spikes once, leaving only ordinary decaying adaptation by t=100 ms.
2. `quiet`: unit 1 has no prior spike.

The predeclared unperturbed future Q0 is the same environment pulse at t=100 ms targeted to unit 0 only. The predeclared local intervention is the same direct current 0.825 to unit 1 at t=100 ms in both histories. The downstream observable is the spike signature through t=110 ms.

## Diagnostics / observations

CI run `35923832947` completed successfully on Python 3.11 and 3.13, including lint, local readiness, pytest and bundle validation.

Observed / asserted Q0 signatures:

- warm Q0: `((100.0, 0),)`
- quiet Q0: `((100.0, 0),)`

Thus the selected pair is behaviorally equivalent on the declared unperturbed future surface.

Observed / asserted QI signatures under the identical local intervention:

- warm QI: `((100.0, 0),)`
- quiet QI: `((100.0, 0), (100.0, 1), (104.0, 2))`

So the intervention does force a QI split at this toy surface.

## Ordinary reduction first

The split is exactly predicted by an ordinary variable already present in the implementation: adaptive threshold state.

- quiet threshold at intervention: `0.80`
- warm residual adaptation at 100 ms: `0.16 * exp(-100/90) = 0.052670878049264895`
- warm threshold at intervention: `0.8526708780492649`
- fixed intervention current: `0.825`

Therefore `0.80 < 0.825 < 0.852670878...`: quiet must spike and warm must not. No unexplained intervention-sensitive state is required. Once quiet unit 1 spikes, the fixed ordinary edge weight `1.0 > 0.80` predicts unit 2's spike exactly 4 ms later. At this boundary, even a compact recent-spike/adaptation register is sufficient to distinguish the histories for intervention response.

Strongest ordinary reduction: standard leaky/adaptive threshold dynamics plus fixed local edge transmission; equivalently a small register/FSA that tracks the adaptation-relevant recent-spike state.

## Disposition

Status: `FORGE_DEAD_END`.

Dead-end reason: the bounded TH-001 discriminator does produce `QI > Q0` in the constructed toy, but every observed split is prospectively and quantitatively predicted by ordinary adaptation plus fixed edge dynamics. This meets Analyst R107's kill criterion for the bounded probe. There is no residual requiring a SparkBrain-specific intervention-stable mechanism at this surface.

This kills/reduces this bounded Theory probe only. It does not create scientific evidence, does not canonicalize or promote TH-001, and does not prove that every possible intervention-stable quotient is trivial on every future surface.

Promotion proposal: none.
Utility request: none.
Revisit probe: none.

## MAIN collision / hard floor

Explicitly avoided:
- H7 science/controller/component/runtime/scorer/preserver/launch/identity/START/protected-evaluator/workflow/authority surfaces;
- Candidate #34 same-object temporal-route rescue;
- Candidate #35 same-object/null/reachability/STP rescue;
- consumed/frozen/FORMAL identities, authoritative evidence and preserve refs;
- protected held-out/evaluator targets.

Hard-floor action occurred: `NO`.
No PRE_FORMAL/FORMAL identity was created or consumed; no STARTED, official TEST/scoring, protected access, evidence/formal/sealed/freeze/preserve mutation, consumed-evidence mutation, result-bearing canonical workflow dispatch, terminal reopen, research branch mutation, or merge occurred.

## Exact refs

- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- Evidence Analyst R107: `ops/evidence-analyst-handoff@247a2e6349ada02a6fdb4a362318570b6dd74e90`
- MAIN/Relay mailbox observed: `ops/orchestrator-run-report@e5a1927352b0671456dd8c1166cccea72a510817`
- Methodology R99: `ops/methodology-calibration-audit@26d2b175154e156bf989d0c61045e8eb288fea1b`
- Theory/Literature/Audit: `ops/external-research-audit-handoff@226d812c96df3d71186ba5a4fb2ac1b27c0d6e25`
- Utility observed: `ops/utility-orchestrator-requests@d4b9804aeb6d2f88534bff6326f7fb2b2798dff3`
- Forge branch: `forge/20260924-th001-q0-qi-adaptation-a@e2dbe3a5a0db812f777b789a6878af8a0d3eee0f`
- CI: workflow run `35923832947`, success on Python 3.11 and 3.13

## Metrics after this run

- runs: `18`
- prototypes_attempted: `19`
- Theory probes / kills / survivors: `2 / 2 / 0`
- Revisit probes / kills / survivors: `0 / 0 / 0`
- dead_ends: `15`
- interesting_observations_retained: `1`
- promotion_proposals: `1`
- later_admissions: `0`
- duplicate_or_rescue_rejects: `10`
- ownership_collisions: `0`
- ordinary_reduction_rejects: `15`
- Analyst promotion deferrals: `1`
- idea_to_observation_latency: `SAME_RUN_PROTOTYPE_TO_OBSERVATION`
