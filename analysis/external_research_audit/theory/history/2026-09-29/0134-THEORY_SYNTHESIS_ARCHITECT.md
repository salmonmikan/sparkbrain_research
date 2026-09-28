# Theory Synthesis Architect — semantic-surface contract for FLY-0 comparators

generation_id: `THEORY-20260929T013443+0900-R19-SEMANTIC-SURFACE-CONTRACT`
produced_at: 2026-09-29T01:34:43+09:00
role: THEORY_SYNTHESIS_ARCHITECT
authority_scope: NON_EVIDENTIARY_NONCANONICAL_THEORY_SYNTHESIS_ZERO_EXECUTION_AUTHORITY
supersedes: THEORY-20260928T213100+0900-R18-NO-PROPOSAL-CURRENT-STATE
design_id: ID-SB-FLY-HIERARCHICAL-SENSORIMOTOR-LOOP-001
design_revision: 4
genuinely_new_information: true
new_sparkbrain_scientific_result: false
status: INTEGRATION_DESIGN_PROPOSAL

## Target capability

Make the FLY-0 replacement family functionally comparable on one explicit task-facing sensorimotor surface before any later SB003 consideration, without turning comparator fairness into a new M1 gate.

## Why this refinement is warranted

Methodology R145 identifies a concrete confound: the structured variant preserves left/right sensorimotor meaning while the current rewired/random-sparse controls preserve role/resource summaries without preserving source/target side. Literature R48 independently strengthens the same boundary: bilateral/body-part semantics can be functionally meaningful, and degree preservation alone does not guarantee a matched neural-network null.

The current green FLY-0 diagnostic therefore means the mismatch is exposed, not that four-way acceptance is repaired.

## Proposed design

Introduce a small `SEMANTIC_SURFACE_CONTRACT` at the world/component boundary.

For the current bounded FLY-0, each task-facing channel must declare at least:
- direction: sensory/input or motor/output;
- functional role;
- side: left/right/neutral where applicable;
- world-signal/action meaning;
- declared delay/resource envelope class.

Topology variants may change internal connectivity, but the primary replacement variants must not silently remap these task-facing semantics.

The primary comparator family becomes:
1. structured fly-inspired topology;
2. semantic-surface-preserving degree-rewired topology;
3. semantic-surface-preserving random-sparse topology;
4. ordinary hierarchical reactive/FSM replacement on the same external surface.

For graph controls, randomization should preserve the declared `source_role + target_role + source_side + target_side` class for the current FLY-0. Add finer body-part/channel classes only if the bounded world actually exposes them; do not require biological labels that the task does not use.

Retain the existing role/degree-only rewiring as a separate `COARSE_DESTRUCTIVE_NULL`. It remains useful to ask what happens when task semantics are also disrupted, but it must not be labeled a functionally matched replacement.

R16's split resource accounting remains in force:
- COMMON_RESOURCE_LEDGER for semantically identical wrapper work;
- VARIANT_ACTIVITY_LEDGER for native counters;
- RESOURCE_ENVELOPE_GUARD;
- CLAIM_BOUNDARY_METADATA.

Strict native-activity commensurability remains claim-typed and is not required merely to use the component in NON_EVIDENTIARY SYSTEM_BUILD.

Checkpoint/replay should bind:
- replacement variant;
- semantic-surface contract/version;
- randomization seed;
- delay/resource envelope;
- world seed/scenario;
- causal-cut configuration.

## Acceptance tests

A bounded repaired FLY-0 is ready for Analyst reconsideration only if, on the exact candidate head:
- all four primary variants expose the same declared sensory/motor channel semantics;
- rewired/random-sparse construction preserves the required source/target role+side classes;
- all four primary variants satisfy the already-authorized bounded intact progression target;
- checkpoint/restore/replay is exact under the bound contract;
- Observation cut and ascending-feedback cut are evaluated only on baseline-capable intact variants and retain their intended causal interpretation;
- common resource/delay guards remain within the declared envelope;
- current-head CI is green.

The coarse destructive null is reported separately and does not participate in four-way functional-match acceptance.

## Suggested replacement / interaction tests

Replacement:
- structured vs semantic-preserving rewired;
- structured vs semantic-preserving random sparse;
- structured vs ordinary hierarchical reactive/FSM;
- semantic-preserving rewired vs coarse role-only destructive null as a diagnostic contrast.

Interaction ablations:
- descending modulation disabled;
- Observation edge/cut disabled;
- ascending-feedback edge/cut disabled;
- checkpoint/replay across each primary variant.

## Alternative established architecture

A conventional hierarchical reactive/FSM controller with the same world-facing sensorimotor contract and SparkBrain only supplying high-level modulation remains the simplest system-level alternative. It must stay in the replacement ladder.

## Claims explicitly not made

This proposal does not establish biological fidelity/equivalence, topology superiority/necessity, compute or energy efficiency, composition contribution, whole-system superiority, external validity, or scientific novelty.

## Build value if no novelty exists

Even if the structured topology proves scientifically unexceptional, the semantic-surface contract is useful engineering: it prevents task-interface changes from being mistaken for topology effects, gives checkpoint/replay a stable embodiment boundary, and makes later component replacement safer.

## Suggested SYSTEM_BUILD scope

Do not allocate SB003 here. If Analyst later promotes a repaired FLY-0, the smallest SB003-equivalent slice should reuse the semantic-surface contract, the R16 resource split, the ordinary-reactive replacement, and the existing causal cuts. This proposal does not alter M1-002 sequencing and is not a review gate.

No experiment, result-bearing workflow, scientific ref, build ref, scheduler state, consumed identity, or immutable evidence is changed.
