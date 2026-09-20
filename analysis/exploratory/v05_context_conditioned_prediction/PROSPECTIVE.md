# EXPLORATORY / NON_EVIDENTIARY — v0.5 context-conditioned prediction discovery

## Prospective contract

- discovery_mode: `THEORY_BACKWARD_MECHANISM_DISCOVERY`
- candidate: `CAND-V05-CONTEXT-CONDITIONED-PREDICTION-01`
- cycle: `1/3`
- claim_ceiling: `MECHANISM`
- preformal_eligible_pre_outcome: `true`
- evidentiary_status: `NON_EVIDENTIARY`
- stable_base: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- analyst_authority: `EVA-20260920T180852+0900-R17-152262F6@4dc5a5b43f26789f32567eb69cbb4a26b9cd6825`
- main_generation_observed: `MAIN-20260920T181208+0900-PRIMARY-FUNNEL21-HOLD-4F2C91A7`
- previous_sub_generation: `SUB-20260920T173914+0900-NOOP-ANALYSTWAIT-CA15738F`

Question: after balanced training in which the same mature current Assembly X is followed by different outcomes depending on the immediately preceding mature Assembly context A versus B, can the native v0.5 prediction component emit different predictions for the same X activation solely as a function of that immediately preceding Assembly context?

This is a theory-backward discriminator for persistent internal/context state causing later cognitive behavior beyond a matched current-state lookup. It is independent of MAIN because MAIN has no active scientific object under Analyst R17, and it does not reopen H7, delayed-outcome attribution, pre-semantic transfer, endogenous continuation, or any terminal/formal identity.

## Control R15 terminal/API semantic preflight — completed before outcome-bearing execution

Exact stable-main source surfaces were read before this contract was written:

- `src/sparkbrain/v05/contracts.py` blob `048b93cddb16dbe9276a0e2c0f972406291c1cb2`: `PredictionDecision` public fields are exactly `assembly_id`, `value`, `confidence`; `AssemblyActivation` public fields include `assembly_id`, `mature`, and `suppressed`.
- `src/sparkbrain/v05/prediction.py` blob `9805031fb8db235d2f3cf4c81421b896d2597af4`: `AssemblyPredictor.predict(activation)` returns a `PredictionDecision`; `observe(activation, value)` records counts keyed by `activation.assembly_id`; `predict` chooses from that table and has no documented/implemented context argument.

Terminal predicates below are therefore bound to `PredictionDecision.value`, `PredictionDecision.assembly_id`, and `AssemblyPredictor.state_dict()["counts"]`. No accessor, categorical mapping, terminal label, comparator, training count, or outcome label may be changed after the first outcome-bearing execution. A terminal-relevant mismatch discovered after outcome exposure forces immediate method-limit STOP; no same-object repaired scientific closure.

## Fixed synthetic construction

Use three direct development-only mature, unsuppressed `AssemblyActivation` objects with distinct IDs `assembly-A`, `assembly-B`, and `assembly-X`. All use fixed similarity `1.0`, occurrences/episode_count `3`, and fixed dummy unit IDs. This component-level probe intentionally isolates the native prediction memory from field/receptor/Assembly-formation confounds.

Training schedule is fixed at eight X-outcome observations:

1. Four context-A trials: call `predict(A)` as the immediately preceding context exposure, then `observe(X, "future-A")`.
2. Four context-B trials: call `predict(B)` as the immediately preceding context exposure, then `observe(X, "future-B")`.

The global current-Assembly X outcome counts are therefore exactly balanced: `future-A=4`, `future-B=4`.

Evaluation uses no learning:

- arm A: call `predict(A)`, then `predict(X)`;
- arm B: call `predict(B)`, then `predict(X)`.

Also snapshot predictor state before and after each evaluation context call to detect any hidden predictive-state mutation.

## Prospectively fixed ordinary reduction

A matched first-order current-Assembly lookup ignores preceding context and predicts from the stored X outcome-frequency table only. For equal counts, it uses the repository predictor's exact deterministic tie behavior over the sorted labels. If both native evaluation arms equal this comparator, the apparent mechanism reduces to ordinary current-Assembly frequency lookup.

## Prospectively fixed terminals

- `CONTEXT_CONDITIONED_PREDICTION_SURVIVES_FIRST_ORDER_LOOKUP`: X-after-A and X-after-B emit different non-null `PredictionDecision.value` values matching `future-A` and `future-B` respectively while the fixed first-order comparator cannot do so. Stop for fresh Analyst review; no automatic PRE_FORMAL action.
- `FIRST_ORDER_CURRENT_ASSEMBLY_LOOKUP_EXPLAINS`: X-after-A and X-after-B are identical and equal the fixed current-Assembly frequency comparator. Reject the current mechanism object; terminal for current object.
- `NO_USABLE_X_PREDICTION`: X produces no prediction despite the fixed eight observations. Reject the current mechanism object unless this is traced to a pre-outcome mechanical harness/API defect before any outcome is exposed.
- `POST_OUTCOME_TERMINAL_SEMANTIC_DEFECT`: any terminal-relevant accessor/representation assumption proves wrong after outcome exposure. Stop immediately as method-limited; do not repair and rerun this object for scientific closure.

## STOP conditions

Stop after the first mapped terminal. Do not tune labels, counts, ordering, comparator, activations, or terminal predicates. Do not use cycle 2 as rescue tuning. Any stronger sequential/stateful successor requires a fresh candidate ID and fresh prospective contract.
