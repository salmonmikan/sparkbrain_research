# HUMAN-20260922-008 — Fast Forge / Slow Science throughput architecture

Human status: `OPEN`  
Created: `2026-09-22 JST`

## Concern

SparkBrain's audit, methodology, evidence-integrity, and control-plane machinery has become substantially stronger, but research throughput and code-generation speed have fallen.

The human side wants to recover aggressive exploratory implementation speed **without weakening the scientific evidence bar**.

The core distinction is:

> **Rough exploration is allowed to be rough. Scientific evidence is not.**

The current concern is that development/exploration work may be carrying too much of the same procedural burden that is appropriate only near PRE_FORMAL / FORMAL promotion.

## Proposed direction — Fast Forge / Slow Science

Introduce an explicitly non-evidentiary fast implementation/exploration lane before the canonical scientific funnel.

Conceptually:

```
Central theory / unresolved phenomena
        ↓
FAST FORGE
rough code / prototypes / synthetic probes / speculative implementation
        ↓
promotion proposal
        ↓
Evidence Analyst promotion gate
        ↓
canonical scientific candidate
        ↓
Discovery / Architecture / PRE_FORMAL / FORMAL
        ↑
Methodology / Audit
```

This is a proposal for scheduler/control-plane review, **not direct authority to change scheduler definitions yet**.

## Forge semantics

Forge should be an intentionally permissive development surface.

Allowed in Forge, subject to safety/repository constraints:

- rough mechanism prototypes;
- speculative implementations;
- synthetic/dev probes;
- instrumentation;
- exploratory comparators and reductions;
- temporary diagnostics;
- multiple competing implementations of the same broad idea;
- iterative rerun/retune/rewrite;
- parameter exploration;
- rapid abandonment of dead ends;
- code that is useful primarily to learn whether an idea is worth formalizing.

Forge may create several prototypes in one run when this improves information gain. A rough target of up to approximately three bounded prototypes per run may be evaluated, but this should not become a quota.

Forge output should be treated as **research material**, not scientific support.

Suitable Forge-level states may include:

- `FORGE_PROTOTYPE`
- `FORGE_OBSERVATION`
- `FORGE_INTERESTING`
- `FORGE_DEAD_END`
- `FORGE_PROMOTION_PROPOSED`

These are deliberately outside canonical candidate classification.

## What Forge should NOT require

Do not require every Forge object to carry the full canonical candidate machinery.

In particular, Forge should normally not need:

- canonical candidate ID;
- final `claim_ceiling`;
- `preformal_eligible`;
- PRE_FORMAL readiness;
- full HOLD taxonomy;
- formal claim ceiling;
- formal evidence interpretation.

The builder should be allowed to build first and let the promotion gate classify later.

This does not prevent lightweight provenance such as idea ID, branch, implementation, commands, observations, obvious reductions, and reproduction notes.

## Hard separation from evidence

Forge must not become a weak backdoor into scientific evidence.

Forge must not:

- create or consume FORMAL / PRE_FORMAL one-way identities;
- create official TEST / STARTED / evidence / formal / sealed artifacts;
- mutate immutable or consumed evidence;
- use held-out/formal evaluator information for tuning;
- claim scientific novelty or mechanistic distinctness from Forge observations;
- retroactively upgrade a Forge observation into confirmatory evidence;
- treat repeated exploratory reruns as independent scientific replications.

If a Forge result is interesting, promotion requires a **fresh prospective canonical object**.

## Promotion gate

Evidence Analyst should act as the boundary between rough exploration and canonical science.

Only Forge objects explicitly proposed for promotion need strong review.

Promotion review should ask:

- Is this genuinely distinct from terminal/consumed work?
- Is it merely an ordinary API/config/resource effect?
- Is the scientific question falsifiable?
- What are the strongest ordinary reductions?
- Is this SYSTEM or MECHANISM?
- Is a fresh candidate ID justified?
- Is the test reachable without outcome-responsive redesign?
- Does the question retain information value if the result is negative?

If admitted, create a fresh candidate ID and normal Funnel v2.1 fields.

The Forge object itself should remain exploratory history and should not be relabeled into evidence.

## Promotion implementation rule

Interesting Forge code may be reused or ported when appropriate, but the canonical scientific object must re-establish prospectively:

- hypothesis/question;
- comparator;
- metric;
- falsifier;
- resources/privilege;
- seed/input selection where relevant;
- protocol and identity;
- evidence-integrity requirements appropriate to its layer.

The existence of a working Forge implementation is not itself scientific support.

## Scheduler / role options to evaluate

Control Brain, Evidence Analyst, Methodology, MAIN, SUB, and Utility should independently evaluate how best to operationalize the concept rather than assuming one exact scheduler mapping.

The human side currently sees the following as promising options:

### Option A — SUB becomes primarily Fast Forge

Re-orient SUB from cautious one-question-at-a-time Discovery toward high-throughput independent rough implementation.

SUB remains independent of MAIN critical path.

### Option B — Utility acts as parallel Forge capacity

When not explicitly assigned higher-priority work, Utility may implement a second independent prototype or tooling path generated by Forge/Analyst.

This should complement HUMAN-20260921-004 rather than create conflicting ownership.

### Option C — MAIN becomes more purely canonical science

MAIN focuses on admitted Discovery / Architecture / PRE_FORMAL / FORMAL work and does less speculative implementation.

### Option D — Audit on promotion

Methodology and heavy review should focus on:

- Forge -> canonical candidate promotion;
- Architecture -> PRE_FORMAL;
- PRE_FORMAL -> FORMAL;
- material methodology changes;

rather than attempting to inspect every exploratory implementation step.

Periodic methodology runs may remain as a backstop.

### Option E — Multiple bounded prototypes per Forge cycle

Allow several small competing prototypes/diagnostics in one Forge run, with rapid discard of low-value lines.

## Relationship to existing directives

This proposal should be interpreted together with, not as a silent replacement for:

- HUMAN-20260919-003 — stalled primary research throughput concern;
- HUMAN-20260921-004 — Utility autonomy expansion;
- HUMAN-20260922-005 — development iteration calibration;
- HUMAN-20260922-007 — SUB autonomous research expansion.

In particular:

- HUMAN-005 supports flexible development while preserving rigid evidence;
- HUMAN-007 says no-target should trigger question formation rather than immediate idle;
- HUMAN-004 provides potential spare parallel implementation capacity;
- HUMAN-008 proposes a clearer architectural separation between rough building and scientific promotion.

If these directives conflict operationally, Control should explicitly reconcile them rather than simply stacking all permissions.

## Repository isolation

Evaluate use of a clearly noncanonical namespace such as:

- `forge/*`
- `scratch/forge/*`

for rough exploration.

Forge branches should be disposable/rewriteable according to normal development rules and must not be confused with immutable evidence refs.

Do not force all Forge work into `main`.

## Throughput objective

The programme should optimize exploratory breadth and implementation latency before promotion.

Candidate metrics to evaluate include:

- Forge prototypes/day;
- working prototypes/day;
- distinct ideas/day;
- idea -> executable-code latency;
- Forge promotion proposals/day;
- admitted canonical candidates/week;
- Forge attempts per admitted candidate;
- MAIN idle / low-value polling rate;
- SUB no-target / NO_OP rate;
- Utility idle rate;
- audit/promotion wait time;
- proportion of Forge work directly related to central-theory questions.

A high Forge rejection/dead-end rate is acceptable.

The goal is not to minimize rejection. The goal is to cheaply eliminate many possibilities and surface a small number of high-value candidates.

## Suggested rollout

Evaluate a staged rollout rather than immediately rewriting the entire research fleet.

### Phase 1 — Shadow Forge

For approximately 1–2 days or an equivalent bounded observation window:

- add Forge behavior without weakening canonical Funnel rules;
- allow rough prototypes;
- measure prototype/code throughput;
- do not automatically promote Forge results;
- observe collisions and ownership problems.

### Phase 2 — Promotion Gate

If Phase 1 is healthy:

- enable explicit `FORGE_PROMOTION_PROPOSED`;
- have a later fresh Analyst generation decide admission;
- create fresh canonical candidate IDs only after promotion review.

### Phase 3 — Audit thinning / scheduler calibration

Only after observing real throughput data, evaluate whether:

- Methodology cadence;
- Relay cadence;
- Utility polling;
- Analyst cadence;
- or other scheduler density

can be reduced or made more event-driven without harming scientific integrity.

Any substantial cadence/role/prompt change remains subject to the current scheduler-health governance and user-approval boundary unless independently classified as an already-authorized safe timing change.

## Requested scheduler review

Before implementation, scheduled agents should explicitly assess the proposal.

### Control Brain

Classify this directive as `ACCEPT / MODIFY / DEFER / REJECT` and evaluate:

- expected throughput gain;
- ownership/collision risk;
- whether SUB, Utility, or a distinct mode should own Forge;
- scheduler impact;
- relation to existing Human Directives;
- safe staged rollout.

### Evidence Analyst

Evaluate:

- whether Forge can remain outside canonical candidate denominators;
- promotion criteria;
- contamination/rescue risks;
- fresh-object requirements;
- whether rough implementation can safely precede claim classification.

### Methodology

Audit:

- whether this separation reduces hidden over-conservatism;
- whether promotion-only auditing preserves false-positive control;
- leakage / cherry-picking risk;
- whether exploratory tuning can be cleanly separated from later prospective testing;
- whether the proposed rollout keeps PRE_FORMAL / FORMAL credible.

### MAIN / SUB / Utility / Relay

Report operational consequences:

- what work can move into Forge;
- what must remain canonical;
- what role collisions would arise;
- whether multi-prototype execution is practical;
- whether current branch/report conventions support the separation cleanly.

## Required independent review

This is a human-originated research-process proposal, not scientific evidence and not direct execution authority.

Do **not** modify scheduler semantics solely because this file exists.

Control Brain should independently review the directive through the normal Human Directive process. If accepted or modified, route the resulting interpretation through the normal Control -> Analyst -> worker / Methodology structure before implementation.

The desired outcome of this directive's first stage is an informed scheduler/control-plane decision about whether and how to implement Fast Forge / Slow Science.
