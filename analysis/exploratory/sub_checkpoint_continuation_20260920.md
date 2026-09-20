# EXPLORATORY / NON_EVIDENTIARY — checkpoint continuation equivalence

Mode: SUB Discovery  
Target: `V05_CHECKPOINT_CONTINUATION_EQUIVALENCE_DISCOVERY_CYCLE1`  
Cycle: `1/3`  
Base: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`  
Evidence Analyst authority: `ops/evidence-analyst-handoff@639a5f7baba926502965bc9fea4cdcfb9f749068` (`LEGACY_GENERATION_UNKNOWN`; no generation metadata present in the consumed handoff/state)  
MAIN collision boundary: do not inspect or continue `CAND-V05-RECEPTOR-SIMULTANEITY-ORDERING-01`, receptor simultaneity/ordering, queued Assembly lifecycle, Homeostasis, delayed-outcome, Refractory, Suppression, Top-k/H7, or any FORMAL/TEST/scoring/preserve/evidence surface.

## Prospective question

Does a v0.5 checkpoint round-trip preserve deterministic *future execution*, not only equality of the immediately restored `state_dict()`? In particular, after a warmup prefix, do an uninterrupted brain and a checkpoint-restored brain produce identical next-step outputs and identical post-outcome state when given the same subsequent DEV-only episodes and scalar rewards?

This is a reproducibility/continuation diagnostic, not a scientific claim. A mismatch would indicate an omitted or inconsistently restored runtime state component. Equality would reduce this candidate to ordinary checkpoint correctness and end the cycle.

## Fixed inputs

Use only synthetic/development `training_episodes(seed=777, count=6)`. No held-out/formal TEST input, repository evidence bundle, official scorer, consumed identity, threshold tuning, or outcome-responsive redesign.

Warmup: episodes 0..3. For each warmup episode, call `process_episode`, then `learn_outcome(next_event=episode.future_event, reward=1.0 if action == rewarded_action else -0.35)`.

Checkpoint after episode 3 and restore into a second brain. First assert immediate `state_dict()` equality.

Continuation: episodes 4..5, applied identically to original and restored brains. For each continuation episode compare:

1. `V05StepResult.as_dict()` before learning the outcome;
2. `state_dict()` immediately after the step;
3. after applying the same outcome/reward rule to both, `state_dict()` again.

## Fixed interpretation

- If every comparison is equal, reject/reduce: checkpoint serialization is sufficient for this bounded deterministic continuation path; recommendation `REJECT`.
- If immediate restored state is equal but later step/result/state diverges, return `PROMOTE_TO_ARCHITECTURE_STUDY` for checkpoint/runtime continuation semantics.
- If the diagnostic cannot validly exercise the supported checkpoint path, return `REJECT` as invalid/uninformative rather than tuning the setup.

No cycle 2 in this run. Any follow-up must be freshly reviewed by Evidence Analyst.
