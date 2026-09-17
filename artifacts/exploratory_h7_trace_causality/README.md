# EXPLORATORY / NON_EVIDENTIARY — H7 trace-causality bypass probe

This artifact is hypothesis-generation material only. It is **not** formal scientific evidence, does not satisfy any H7 gate, and must not be promoted into a programme claim. It uses only a fixed synthetic 64-example world; no formal, sealed, official, held-out, C19, R1, Belief-R, or consumed-identity data are accessed.

## Question

Can stable route IDs and perfect baseline prediction coexist with weak trace-to-output causal faithfulness when an unreported bypass carries the same task signal?

## Fixed toy

- 64 deterministic binary-label examples.
- The visible traced route is stable under a nuisance view in every example.
- The traced route votes correctly with weight `1.0`.
- A hidden bypass, when present, carries the same target signal with weight `1.5`.
- Fixed bypass coverage grid: `0, 0.25, 0.50, 0.75, 1.00`.
- Two interventions are measured: delete the traced route; replace it with the wrong route.

## Observation

Baseline accuracy and route-ID stability remain `1.0` at every bypass coverage. As bypass coverage rises from `0` to `1`, deletion and wrong-route-replacement accuracy rise from `0` to `1`, so both causal-sensitivity measures fall from `1.0` to `0.0`.

The constructed counterexample therefore separates **trace stability** from **trace causal necessity**: an apparently stable, semantically neat route can become causally dispensable when an unreported predictive path exists.

## Interpretation boundary

This does **not** show that SparkBrain learned routing is unfaithful, nor that H7 is false. It is a trace-completeness/specification warning. Low deletion sensitivity can also arise from legitimate redundancy, so a future formal test must distinguish redundant-but-complete explanations from misleading or incomplete traces rather than treating deletion alone as definitive.

## Candidate prospective question

Under prospectively declared allowed bypass/residual paths and matched predictive quality, do stable learned route IDs/evidence paths remain causally faithful under route/evidence deletion and counterfactual replacement on held-out routing cases?

Before any formalization, independently and prospectively fix at least: exact route semantics; what counts as a reported trace path; allowed bypass/residual channels; necessity, sufficiency and completeness metrics; held-out routing construction; deletion/replacement intervention rules; stable-ID/role metric; semantic-label reliability criterion; comparators; training/tuning budget; seeds/runtime/determinism; success/failure thresholds; and a fresh protocol/package/identity/integrity contract.

Promotion recommendation from SUB: `CONTINUE_EXPLORING` only after Evidence Analyst classification. Do not automatically formalize or continue this theme from the exploratory branch.
