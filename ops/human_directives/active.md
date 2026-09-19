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

## HUMAN-20260919-002 — Defer repository protection rules for now

Human status: `OPEN`  
Created: `2026-09-19 JST`

### Intent

As a human-side governance preference, **defer application of GitHub repository protection rules / rulesets for now**.

This includes the currently discussed protection gap around `main` and authoritative ref/tag namespaces. The absence of protection may continue to be reported as a governance fact or risk, but it should **not currently be treated as an action item to implement protection rules**.

### Requested operating posture

- Do not create or apply branch protection rules / repository rulesets merely to close the currently reported protection gap.
- Do not make protection-rule deployment a prerequisite for research, Discovery, Architecture Study, Pre-formal, Formal, repository promotion, or ordinary governance work.
- Control Brain and Repository Steward may continue to report that protections are absent and may note concrete risks caused by that absence.
- Reconsider implementation only after a new explicit human instruction, or after a materially changed risk condition is surfaced for human review.
- This directive does not authorize weakening scientific one-way integrity, immutable evidence discipline, or consumed-identity boundaries.

### Required independent review

This is a human-originated governance preference, not scientific evidence.

Control Brain should classify it under the normal Human Directive process as `ACCEPT`, `MODIFY`, `DEFER`, or `REJECT`. If it disagrees because of a concrete material repository-integrity risk, it should state that risk explicitly rather than silently applying protection rules.

## HUMAN-20260919-003 — Concern about stalled primary research throughput

Human status: `OPEN`  
Created: `2026-09-19 JST`

### Concern

The human side is concerned that **major SparkBrain research has remained effectively stalled**, even though scheduler activity, audit work, literature review, governance, and methodology checking continue to run.

The concern is not a request to lower scientific standards or to manufacture formal experiments. It is a concern that the programme may have become too effective at stopping weak work and insufficiently effective at generating, characterizing, and maturing new research objects.

### Requested operating posture

- Preserve the strict FORMAL one-way integrity bar.
- Treat prolonged absence of MAIN/SUB research progress as a real programme-throughput concern, not merely as healthy restraint, when safe lower-layer work exists.
- Prefer substantive DISCOVERY, ARCHITECTURE_STUDY, and PRE_FORMAL work over additional low-value governance cleanup when the latter does not materially improve scientific safety.
- Use the new research funnel actively to generate and mature candidate objects rather than waiting passively for a fully formed formal object to appear.
- Track whether candidate-pool throughput is producing promotion, rejection, or informative reframing rather than repeated no-op cycles.
- Do not interpret this concern as permission to rescue consumed lines, weaken comparator fairness, expose held-out targets, bypass prospective specification, or fabricate novelty.

### Priority relationship to protection rules

This concern is one reason for HUMAN-20260919-002: repository protection-rule deployment should remain deferred for now so that it does not become a competing governance project while core research throughput is weak.

Protection gaps may still be reported as risks, but the human preference is to prioritize **scientifically meaningful forward motion** unless a concrete repository-integrity risk materially changes the tradeoff.

### Required independent review

This is a human-originated strategic concern, not scientific evidence and not automatic execution authority.

Control Brain should independently classify it as `ACCEPT`, `MODIFY`, `DEFER`, or `REJECT`, and should explicitly explain how it will balance research throughput against scientific-integrity constraints.

