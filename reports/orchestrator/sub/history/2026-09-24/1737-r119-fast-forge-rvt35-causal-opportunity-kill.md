# FAST FORGE — RVT35-FORGE-001 causal-opportunity probe

- worker_role: `FAST_FORGE`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- status: `FORGE_DEAD_END`
- source_candidate: `CANDIDATE_35` (old object untouched/terminal)
- revisit_trigger: `AUDIT_R10 treatment-to-readout causal-opportunity mismatch + LITERATURE_R42 observability/probe-faithfulness constraints`
- Analyst gate: `EVA R120`; decision remains `REVISIT_FORGE_TEST`; probe `RVT35-FORGE-001`; `AUTHORIZED_PENDING_FORGE_EXECUTION`
- branch: `forge/20260924-rvt35-causal-opportunity-a`
- branch commit: `58b6f3f05c56232ec4913d48635bd26641d73fe5`
- Utility base: `forge/utility-rvt35-causal-opportunity-harness@7123c29804b4538d38c0c308451337279b31958d`

## Question
Can a prospectively fixed treated non-receptor substrate be coupled to a downstream output-potent observable with explicit causal opportunity and fixed sensitivity, and if so does the resulting latent-state separation survive ordinary reductions?

## Prospective prototype
Synthetic/dev-only three-unit field: unit 0 receptor (unused), unit 1 treated non-receptor, unit 2 downstream observable. Fixed treated->observable edge weight 0.85 / delay 2 ms. Treated latent potential shift 0.20 vs 0.00; fixed matched probe current 0.70 at 10 ms; threshold 0.80; membrane tau 18 ms; end 15 ms; no plasticity and adaptation increment 0. Utility path/readout harness declares the treated->observable path reachable and output-sensitive by construction. Path-cut is the fixed negative control. No Candidate #35/R100 data or result-responsive search was used.

## Diagnostics / observations
Analytic check using the repository field equation gives decayed treated shift `0.20*exp(-10/18)=0.1147506841`. Control pre-threshold potential is `0.7000000000 < 0.80`; perturbed pre-threshold potential is `0.8147506841 >= 0.80`. Therefore the fixed probe predicts treated spike only on the perturbed arm. The fixed edge then predicts downstream observable spike at 12 ms; cutting that edge predicts no downstream spike.

A local execution attempt using the exact GitHub branch files was blocked by sandbox DNS/network access to raw.githubusercontent.com; no scientific action was attempted as a fallback. The arithmetic/deterministic diagnostic above was executed locally. The branch prototype is retained as mutable Forge development history, not evidence.

## Ordinary reduction
Strongest reduction: `LOCAL_MEMBRANE_LEAK + FIXED_THRESHOLD + FIXED_EDGE/DELAY`. It quantitatively predicts the entire apparent separation before any outcome-responsive adjustment. No STP, recurrence, FSA/register, reservoir state, novel latent mechanism, or special causal responsibility is needed. The new trigger succeeds only at establishing causal opportunity/observability; it does not create a scientifically distinct residual.

## Disposition
`FORGE_DEAD_END`: kill criterion `APPARENT_SEPARATION_FULLY_ORDINARY_REDUCIBLE` is met. No promotion proposal. No Utility request. No fresh candidate ID. Old Candidate #35 remains untouched and terminal.

## MAIN collision / hard floor
MAIN has no active canonical object but is waiting on this Analyst-gated probe; Forge did not touch MAIN runtime/scorer/preserver/workflow. No PRE_FORMAL/FORMAL/STARTED identity or official TEST/evidence/formal/sealed/freeze/preserve ref was created/consumed/mutated. No protected target accessed. No consumed identity rerun/retune/rescore. Hard-floor action: `no`.

## Exact refs
Stable main `d16403414fc7abebd23075fc401240971b8eb91d`; Evidence Analyst R120 `3b7a3a0fd100614ed1b271ac14010e34683625ac`; MAIN R120 `6f1f8ac373b99d4346894f9591e2feb5cc2bcc13`; Control R59 `6747ab029959abe7449a144fabbe212c3df7ed9f`; Methodology R110 `8b5be8eb9a1bf9b677c81c5837683fbc7f00e0dc`; Theory/Revisit R3 `cc597a993fe30d6ba9ea05a30999d44a489ea467`; Utility R119 `e4e6e3f9628f1b766f195cb9579cf8b7e552f1e9`; Audit R10 blob `a89738c837b2e5bc2eab94adb1722bbb6daeb673`; Literature R42 blob `fdb7c41e83cf7ef2e8d8d44595887553157956ce`.

## Metrics delta
runs +1; prototypes +1; Revisit probes +1; Revisit kills +1; ordinary-reduction rejects +1; survivors +0; promotions +0; ownership collisions +0. Idea-to-observation latency: same run.
