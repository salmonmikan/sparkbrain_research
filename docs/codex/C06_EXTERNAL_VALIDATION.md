# C06 — External Belief-Revision and Relational Validation

## Goal

Test whether the learned SparkBrain architecture generalizes beyond its synthetic worlds, especially when new evidence should sometimes change a prior conclusion and sometimes leave it unchanged.

## Prerequisites

Minimum viable C04 learned backend and C05 matched harness.

## Dataset tracks

### Track A — Belief-R

- obtain dataset through its official source and document version/license;
- preserve premise sequence and delta-reasoning structure;
- define a mapping from propositions/evidence to Spark state without using answer labels at inference;
- compare direct models, explicit-belief baselines, and SparkBrain;
- measure update-needed and no-update subsets separately.

### Track B — relational/non-monotonic stream

Use or construct a licensed task with explicit entities, relations, additions, retractions, contradictions, and irrelevant facts. CLUTRR-like relational generalization may be included, but a non-monotonic stream is required.

### Track C — adversarial evidence order

Generate order permutations, delayed corrections, duplicate paraphrases, and correlated source variants around external examples without contaminating labels.

## Required metrics

- final answer accuracy;
- revision precision/recall;
- no-update retention accuracy;
- false revision rate;
- switch latency measured at premise steps;
- calibration and abstention/no-ignition utility;
- contradiction sensitivity;
- evidence attribution fidelity;
- context-length degradation;
- entity cross-talk.

## Evaluation rules

- freeze adapters and prompts on dev data;
- do not use an LLM to generate labels for the test set without independent verification;
- separate language encoder contribution from Spark dynamics with ablations;
- report data leakage checks and overlap searches;
- manually audit a stratified sample of evidence traces;
- keep copyrighted datasets out of the repository when redistribution is not allowed; provide acquisition scripts and checksums.

## Acceptance criteria

- at least one official external dataset adapter is reproducible;
- update-needed and no-update cases are both reported;
- direct and explicit-state baselines are included;
- language-encoder-only and Spark-dynamics ablations isolate contribution;
- errors are categorized rather than only aggregated;
- causal interventions show whether changing/removing cited evidence changes the belief as expected;
- claim grades are updated only to the level supported by results.

## Non-goals

- broad natural-language AGI evaluation;
- cherry-picking only update-needed cases;
- using benchmark answers inside routing features;
- claiming human-like belief revision from one dataset.
