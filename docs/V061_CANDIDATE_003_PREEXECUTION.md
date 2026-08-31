# v0.6.1 Candidate-003 Pre-execution Contract

## Purpose

Candidate-003 is the first fresh confirmatory generation after the candidate-002 one-way execution failure. Candidate-002 remains permanently retired and is used only by explicit regression tests.

## Freshness boundary

```text
world generation: v06-confirmatory-candidate-003
confirmatory seeds: 2000-2009
qualification quarantine: 100-109
retired candidate-002 quarantine: 1000-1009
world families: 5
conditions: 8
evidence domains: 9
expected executions: 400
expected evidence records: 3600
expected resource records: 400
```

The candidate-003 generator derives every deterministic world from the new generation identifier and fresh seed. Its world-grid hash must differ from the retired candidate-002 grid hash.

## Timing correction

The anonymous boundary path processes scheduled internal events without forcing the Field clock to an evaluator horizon before external world consequences are returned. Ordinary silence advancement and strict rejection of backwards external timestamps remain unchanged.

Regression tests verify the complete 22-world candidate-002 timing-risk set and the original seed-1001 failure path. Those retired worlds are not part of candidate-003 evidence.

## One-way execution

Normal CI ignores `.github/confirmatory/**` push-only marker commits. The formal candidate-003 workflow is triggered only by the first marker at:

```text
.github/confirmatory/v06-candidate-003-execute-v1.json
```

The marker must be the sole change in a direct child of the frozen source commit. The workflow rejects reruns, validates the detached source SHA, independently rebuilds and approves the freeze bundle, writes `STARTED.json`, executes the 400-cell matrix once, locks raw evidence before scoring, and uploads all success or failure artifacts.

No candidate-003 capability adapter may be executed before this one-way marker. Structural world-generation, hashing, manifest, schedule, schema, and source-contract tests remain candidate-blind.
