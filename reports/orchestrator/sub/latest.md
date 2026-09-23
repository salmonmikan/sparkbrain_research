# FAST FORGE latest — TH-001 Q0-vs-QI split reduced by ordinary adaptation

- schema_version: `2`
- generation_id: `FORGE-20260924T064230+0900-TH001-Q0-QI-ADAPTATION-KILL`
- produced_at: `2026-09-24T06:42:30+09:00`
- worker_role: `FAST_FORGE`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- overall_status: `FORGE_DEAD_END`
- selection_outcome: `ANALYST_APPROVED_THEORY_PROBE_EXECUTED_AND_REDUCED`
- theory_id: `TH-001-INTERVENTION-STABLE-CAUSAL-QUOTIENT`

## Freshness / gating

Stable main, Evidence Analyst R107, MAIN/Relay, Methodology R99, Theory/Literature/Audit, Utility, Revisit ledger, terminal/current candidates and prior Forge history were re-fetched before work. R107 explicitly retained TH-001 as `THEORY_FORGE_TEST` and supplied the bounded discriminator: choose a privilege-matched Q0-equivalent history pair, apply the same frozen local intervention, and test whether QI refinement survives ordinary-state reductions. Methodology R99 independently confirmed that the prior recurrence toy stays killed but was not a valid execution of this Q0-vs-QI discriminator.

Revisit remains 34/34 classified with `REVISIT_TRIGGERED=0` and no `REVISIT_FORGE_TEST`. MAIN remains H7-only; H7 is scientifically READY but currently operationally blocked before identity/START by unavailable launch-trigger capability. Forge did not touch that blocker or any H7 science/controller/runtime/scorer/preserver/protected surface.

## Selected Theory probe

An isolated branch `forge/20260924-th001-q0-qi-adaptation-a` was created from stable main. The synthetic v0.4 prototype uses two histories that are exactly equivalent under a predeclared future environment (Q0): both produce only unit 0 at 100 ms. One history had unit 1 spike at t=0, leaving ordinary residual adaptation at t=100; the other history was quiet. The same fixed local intervention current 0.825 was then applied to unit 1 in both histories.

Under the intervention (QI), the quiet history produced unit 1 at 100 ms and its fixed downstream unit at 104 ms; the warm history produced neither. Thus QI did split an explicitly Q0-equivalent pair.

The split is nevertheless exactly predicted by ordinary adaptive-threshold dynamics. Quiet threshold is 0.80. The warm history's ordinary adaptation is `0.16 * exp(-100/90) = 0.052670878049264895`, giving threshold `0.8526708780492649`. The fixed current 0.825 lies strictly between these values, so quiet must spike and warm must not. The downstream 4 ms response is then predicted by the fixed nonplastic edge (weight 1.0, delay 4 ms). A compact recent-spike/adaptation register is sufficient at this tested boundary.

CI completed successfully for Python 3.11 and 3.13, including lint, local readiness, pytest and bundle validation.

## Disposition

`FORGE_DEAD_END`: the bounded discriminator generated a QI refinement, but every split is prospectively and quantitatively explained by ordinary adaptation plus fixed edge transmission, satisfying Analyst R107's kill criterion. This reduces this bounded Theory probe only; it is not scientific evidence and does not establish a universal falsification of every possible ISCQ surface.

No promotion proposal. No Utility request. No Revisit probe.

Full technical record: `reports/orchestrator/sub/history/2026-09-24/0642-r107-th001-q0-qi-adaptation-kill.md`.

Cumulative metrics: runs `18`, prototypes attempted `19`, Theory probes/kills/survivors `2/2/0`, Revisit probes/kills/survivors `0/0/0`, dead ends `15`, interesting retained `1`, promotion proposals `1`, later admissions `0`, duplicate/rescue rejects `10`, ownership collisions `0`, ordinary-reduction rejects `15`, Analyst promotion deferrals `1`, latency `SAME_RUN_PROTOTYPE_TO_OBSERVATION`.

No hard-floor action occurred. PRE_FORMAL/FORMAL identities, STARTED, protected targets, official scoring, consumed/immutable evidence, terminal objects and evidence/formal/sealed/freeze/preserve refs were untouched.