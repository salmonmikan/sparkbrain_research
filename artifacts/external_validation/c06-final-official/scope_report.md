# C06 Final Scope Report

## Completed scope

- Loaded the committed C04 main checkpoint and the C05 seed-101 causal Transformer and
  explicit-state checkpoints through repository APIs.
- Added a strict C05 encoder-state contract and a reproducible dev-only adapter manifest.
- Evaluated all 1,744 pinned official Belief-R pairs once, zero-shot, with network access
  blocked in the runner.
- Evaluated the disjoint Track B group test split after Track B dev-only output-map selection.
- Evaluated premise permutation, delayed decisive correction, same-ID duplicate,
  deterministic restatement, correlated-source, and irrelevant-distractor Track C stresses.
- Reported BU, BM, BREU, revision rates, coverage, Brier/ECE calibration, error taxonomy,
  and causal/remove/duplicate/irrelevant prediction deltas.
- Retained attribution as `null` / not available because the connected checkpoints do not
  expose citations to input evidence IDs.

## Result boundary

Spark reached BU 0.039106, BM 0.089552, and BREU 0.064329 at final coverage 0.227064.
This is below the direct and chance conditions, which both reached BREU 0.25. The explicit
condition abstained on every original Belief-R step. These are negative external results;
they do not support CL-007 or an external-generalization claim.

Direct, explicit, and Spark received the same official examples, visible observations,
two-step context, and example budget. Tokenization, parameter counts, and scientific compute
were not matched. Oracle was target-visible and is an evaluator-only upper bound.

## Excluded scope

- No official Belief-R example was used for training, fitting, calibration, thresholding,
  model choice, label-map selection, early stopping, or development splitting.
- No upstream GitHub code was cloned, imported, copied, or executed.
- No official question, premise, choice text, or dataset row is committed.
- No model was retrained and no failed C05 quality/compute-matching result was rewritten.
- No CL-007 evidence-grade increase, biological claim, or energy claim is made.
