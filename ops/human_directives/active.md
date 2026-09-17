# Active Human Directives

## HUMAN-20260918-001 — Promote reusable CX comparator assets toward main

Human status: `OPEN`  
Created: `2026-09-18 JST`

### Intent

The reusable comparator/model infrastructure developed under CX/CX01 should not remain stranded only on
research branches if it is stable and useful independently of the CX01 scientific outcome.

The desired end state is to make appropriate CX comparison assets available from the stable shared substrate
(`main`) for future reduction/comparator research.

### Candidate reusable assets

Review for promotion, rather than assuming promotion:

- G3 / G4 / G5 comparator implementations where still useful;
- G6 Variable-Order Markov comparator;
- G7 HTM / HTM-inspired Temporal Memory comparator;
- G8 spiking temporal-memory comparator;
- common architecture-neutral event / contract / adapter interfaces;
- snapshot / restore facilities;
- generic resource / privilege accounting;
- generic fairness / comparison infrastructure;
- reusable comparator tests and fixtures independent of a consumed scientific result.

### Explicitly not requested for promotion by default

- Candidate-002 scientific conclusions or terminal-result interpretation;
- raw/scored/formal evidence;
- consumed-identity state;
- candidate-specific frozen thresholds/scorers;
- candidate-specific one-way execution workflows;
- STARTED/control semantics tied to the CX01 experiment;
- result-dependent code whose utility disappears if the original hypothesis is negative.

### Human preference

Do not force a wholesale merge of `research/cx01-comparator-extension`.

Prefer an audit of outcome-independent reusable components, followed by a small integration branch / PR into
`main` if Control Brain and downstream governance conclude that promotion is worthwhile.

### Required independent review

This is a human proposal, not a command.

Control Brain must independently classify this directive as `ACCEPT`, `MODIFY`, `DEFER`, or `REJECT`,
and may reject it if current evidence, opportunity cost, integration risk, or repository doctrine argues against it.
