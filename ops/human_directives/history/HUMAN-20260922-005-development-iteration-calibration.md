# HUMAN-20260922-005 — Development iteration calibration

Created: `2026-09-22 JST`  
Origin: explicit human approval following scheduler-policy revision planning

## Intent

Relax over-conservative development restrictions across SparkBrain while preserving the strict one-way scientific integrity of FORMAL evidence.

The programme should distinguish ordinary research-development iteration from post-outcome manipulation of consumed scientific evidence.

The guiding rule is:

> **Development is flexible; evidence is rigid.**

## Three development phases

Every material current object should expose a development phase orthogonal to Funnel layer and terminal/hold state:

1. `OPEN_DEVELOPMENT`
   - scientific/development contract is still being formed or debugged;
   - bounded rerun, repair, retune, instrumentation change, comparator implementation refinement, threshold/tolerance design, resource alignment, and additional cycles are allowed;
   - all changes and information used to make them must be durably recorded.

2. `RESULT_EXPOSED_DEVELOPMENT`
   - a meaningful development/scientific result has been observed;
   - science-invariant repair and tooling fixes may continue on the same object;
   - science-affecting redesign may continue only as an explicitly versioned development revision or fresh successor, preserving prior results rather than overwriting or reclassifying them;
   - development observations are not independent evidence merely because multiple revisions/reruns exist.

3. `CONSUMED_ONE_WAY`
   - FORMAL/consumed scientific identity;
   - rerun, retune, rescore, protocol/metric/comparator/threshold/tolerance mutation, and same-identity rescue remain prohibited unless the prospective FORMAL protocol itself explicitly authorized the action before outcome exposure.

These phases are orthogonal to `ACTIVE / HOLD / TERMINAL_FOR_CURRENT_OBJECT`.

## Cycle policy

Replace the practical interpretation of “max 3 cycles” as a hard stop with:

> **cycle 3 = mandatory reassessment, not automatic terminalization.**

After cycle 3, another development cycle may be authorized when there is concrete prospective information gain, such as:
- a genuinely new observable;
- a new ordinary reduction/comparator question;
- an independently identified methodology defect;
- a new intervention or measurement surface;
- a new implementation/tooling capability that changes what can be learned.

Additional cycles must not merely tune toward a desired result.

## Repair classification

Separate repairs into:

### `SCIENCE_INVARIANT_REPAIR`
Examples:
- lint/import/format/build issues;
- workflow syntax;
- path/serialization/logging/hash plumbing;
- implementation defects whose intended scientific behavior was already fixed and whose correction does not alter hypothesis, comparator, metric, threshold, intervention, resource/privilege contract, scoring semantics, or held-out exposure.

These may be repaired and rerun within the same development object, including after non-result-bearing output.

### `SCIENCE_AFFECTING_CHANGE`
Examples:
- metric/scorer meaning;
- threshold or tolerance with scientific decision meaning;
- comparator definition;
- seed/exclusion policy;
- intervention;
- scientific resource/privilege contract;
- hypothesis or success/falsifier criteria.

Before meaningful result exposure these may be revised normally with versioning.
After meaningful result exposure they must not rewrite the prior result. Continue only as an explicit development revision or fresh successor with the prior result preserved.

## Development rerun / retune

Discovery, Architecture Study, and PRE_FORMAL are development layers and may use iterative rerun/retune when scientifically useful.

Such iterations:
- must be logged;
- must not be counted as independent confirmatory evidence;
- must not retroactively change prior PASS/FAIL/INCONCLUSIVE classifications;
- must not consume or reuse a protected FORMAL identity;
- must lead to a fresh frozen/untouched identity and evaluation surface before FORMAL evidence is claimed.

PRE_FORMAL should function as a real development surface rather than a second FORMAL gate.

## Tolerance changes

Tolerance changes are not universally prohibited.

They are allowed during development when motivated by numerical/model/measurement semantics and recorded prospectively for the next revision.

A tolerance may not be relaxed after seeing a FORMAL/consumed result in order to convert a failure into a pass. Historical outcomes remain bound to the contract under which they were produced.

## SYSTEM to MECHANISM

Same-object post-outcome promotion from SYSTEM to MECHANISM remains prohibited.

However, a SYSTEM result may actively motivate a **fresh MECHANISM successor** when a genuinely new mechanistic residual/question can be stated.

Evidence Analyst should explicitly consider fresh-successor potential at SYSTEM terminalization rather than treating SYSTEM terminalization as topic death.

A fresh successor requires:
- new candidate ID/object;
- fresh prospective mechanism question;
- fresh reduction/comparator/falsifier contract;
- fresh development-phase state.

This is a branch in research, not a retroactive upgrade.

## Terminal semantics

`TERMINAL_FOR_CURRENT_OBJECT` means only that the current prospective question/contract/object is complete.

It must not be interpreted as permanently closing the entire phenomenon/topic family.

Fresh successors are allowed when they contain materially new information, intervention, observable, mechanism question, privilege/resource contract, or independently motivated methodological capability.

Control/Analyst should distinguish legitimate successor research from same-object rescue laundering.

## Scheduler-role implications

- Control Brain: treat over-terminalization and candidate starvation as throughput risks; enforce the phase distinction and protect only the true one-way floor.
- Evidence Analyst: persist development phase, make cycle-3 a reassessment point, allow legitimate development revisions, and explicitly review fresh-successor potential.
- MAIN: allow iterative development in Discovery/Architecture/PRE_FORMAL under Analyst authority; preserve prior results when science-affecting revisions occur.
- SUB: same principle for bounded Discovery/secondary work; do not force termination solely from cycle count.
- Relay: continue same-object work for clearly science-invariant repairs; stop for science-affecting redesign unless a fresh Analyst-authorized development revision already exists.
- Methodology: audit outcome-responsive manipulation rather than treating iteration itself as suspect.

## Hard floor retained

The following remain unchanged:
- no rerun/retune/rescore of consumed FORMAL identities;
- no mutation/retargeting of immutable/formal/sealed/evidence artifacts;
- no held-out/evaluator leakage;
- no post-FORMAL threshold/metric/comparator/tolerance change to rescue a result;
- no rewriting an old FAIL/PASS under a new criterion;
- no evidence-tag/ref retargeting;
- raw-before-score, preserve-before-read, exact binding, no-clobber/STARTED and matched privilege/resource requirements remain in force where applicable.

## Required independent review

Control Brain and Methodology should independently evaluate this directive and may tighten only where a concrete integrity risk is identified.

The default interpretation should not be “iteration is dangerous”; it should be “outcome-responsive alteration of consumed evidence is dangerous.”
