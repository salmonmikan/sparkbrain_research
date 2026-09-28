# Theory Synthesis Architect — bounded descending-modulation authority contract

generation_id: THEORY-20260929T033117+0900-R20-DESCENDING-MODULATION-AUTHORITY
produced_at: 2026-09-29T03:31:17+09:00
producer_run_id: EXTERNAL_SCIENCE_TRIROLE-20260929T033117+0900
role: THEORY_SYNTHESIS_ARCHITECT
schedule_slot: 03:30 JST
role_resolution_source: PREVIOUS_CANONICAL_SLOT
start_drift: +00:01:17
authority_scope: NON_EVIDENTIARY_NONCANONICAL_THEORY_SYNTHESIS_ZERO_EXECUTION_AUTHORITY
supersedes: THEORY-20260929T013443+0900-R19-SEMANTIC-SURFACE-CONTRACT
design_id: ID-SB-FLY-HIERARCHICAL-SENSORIMOTOR-LOOP-001
design_revision: 5
genuinely_new_information: true
new_sparkbrain_scientific_result: false
status: INTEGRATION_DESIGN_PROPOSAL
revisit_status: NO_REVISIT_PROPOSAL

## Target capability

Define the next safe interface for a possible SB003-class integration: high-level SparkBrain state may modulate a local sensorimotor controller through one explicit, bounded and replayable descending contract, while fast local control remains inside the local controller. This proposal is independent of the unresolved M1-002 PR path and does not allocate SB003.

## Why this refinement is warranted

R19's semantic-surface requirement is now implemented on Forge exact source f93483b927470f48a311fe9ef711ca770648da7c. The current Forge record reports checkpoint schema v2 binding the semantic-surface contract/version and fingerprint, topology fingerprint where applicable, deterministic randomization seed, causal-cut configuration and delay/event budgets. CI 36459501642 is green on Python 3.11 and 3.13 with four-way bounded target/replay/cut checks.

The next integration question is therefore the authority boundary between high-level state and the local controller. If that boundary stays implicit, a later integration can accidentally collapse the intended hierarchy by placing fine-grained local control into the high-level interface.

Literature R48 and the current fly-inspired directive support distributed local control plus higher-level coordination as engineering inspiration. They do not establish biological equivalence or a unique SparkBrain mechanism.

## Proposed design

Introduce a versioned ModulationFrame between the M1-level state/prediction/scope/revision layer and the local sensorimotor controller.

Permitted fields are limited to declared high-level variables:
- schema/version and frame identity;
- monotonic sequence or epoch;
- bounded intent/mode such as approach, avoid, track, explore or ignore, or another explicit enum;
- optional declared target semantic channel/side where the bounded world exposes it;
- bounded gain/bias parameters with validated ranges;
- effective horizon or TTL;
- source high-level state/checkpoint token for provenance.

The interface excludes undeclared fine-grained local-control instructions, opaque callbacks and arbitrary internal-controller commands.

The local controller consumes semantic sensory surface + valid ModulationFrame + local state and emits bounded local action. The high-level system maps persistent state/prediction/scope/revision to a ModulationFrame.

The loop becomes:
WORLD -> semantic sensory surface -> local sensorimotor loop -> high-level SparkBrain state -> bounded ModulationFrame -> local sensorimotor action -> WORLD.

High-level update cadence may be coarser than the local controller, but the exact ratio remains an explicit engineering parameter rather than a biological claim.

## Checkpoint and rollback contract

A composed checkpoint should bind, in addition to the current semantic-surface/topology provenance:
- modulation-contract schema/version;
- frame identity/sequence;
- bounded parameter values;
- TTL/effective horizon;
- source high-level state token;
- local-controller state required for exact replay;
- world/scenario seed and causal-cut configuration.

Transactional rollback restores high-level state, modulation state and local-controller state to one mutually consistent snapshot. Unknown, malformed, stale or expired frames fail closed under one declared deterministic policy: neutral modulation or bounded stop.

## Component map and provenance

- High-level state/prediction/scope/revision: existing M1/SYSTEM_BUILD substrate; zero inherited scientific credit.
- Structured fly-inspired local controller: current FLY-0 Forge input; NON_EVIDENTIARY/NONCANONICAL.
- Semantic-surface contract: R19 design implemented/hardened by Forge; engineering provenance only.
- Ordinary hierarchical reactive/FSM controller: established reference replacement using the same interfaces.
- Checkpoint/replay/rollback and causal cuts: existing SYSTEM_BUILD/Forge engineering primitives.

Known reductions are retained: hierarchical/decentralized local control, behavior-mode selection, finite-state/reactive control and explicit modulation buses are established engineering patterns. Their use is a design primitive, not novelty evidence.

## Acceptance tests

A future SYSTEM_BUILD port should require prospectively:
1. neutral modulation reproduces the local-controller baseline deterministically;
2. declared modulation variables affect behavior only through the declared contract;
3. a structural/sentinel test detects and rejects any bypass of the declared high-level-to-local interface;
4. cutting descending modulation removes high-level behavioral influence while neutral local behavior remains available;
5. cutting local sensory feedback degrades/removes local compensation while a valid modulation frame can remain present;
6. checkpoint/restore/replay is exact with modulation state included;
7. rollback is atomic across high-level, modulation and local-controller state;
8. stale, mismatched, malformed or expired frames are deterministically rejected or neutralized;
9. the same modulation interface is exercised across structured, semantic-surface degree-rewired, semantic-surface random-sparse and ordinary reactive/FSM replacements;
10. current-head CI and declared delay/resource envelopes remain green.

## Replacement and interaction tests

Replacement tests keep the world-facing semantic surface and ModulationFrame fixed while swapping structured, semantic-surface degree-rewired, semantic-surface random-sparse and ordinary reactive/FSM local controllers.

Interaction ablations include descending-modulation cut, high-level-to-frame neutralization, local sensory-feedback cut, and optionally bounded modulation-delay perturbation.

These can support component-function or interaction diagnostics inside NON_EVIDENTIARY build work. They do not establish scientific novelty.

## Alternative established architecture

A conventional hierarchical reactive/FSM or subsumption-style controller, where a high-level layer selects a bounded behavior mode and a local controller executes it, is the primary established system-level alternative. An options-like hierarchical controller is another reference form where appropriate.

## Known limitations

A small intent vocabulary may be too coarse. Gain/bias and TTL parameters can become hidden tuning degrees of freedom unless ranges/update rules are explicit. Synthetic-world semantic channels do not imply biological neuron-class semantics. Timing ratios are engineering choices unless separately studied. Current reactive-vs-topology native activity counters are not fully commensurate, so efficiency/topology claims remain out of scope. Durable Analyst authority remains R168 and SB003 is not allocated.

## Claims explicitly not made

This proposal does not establish biological fidelity/equivalence, fly-like topology necessity/superiority, emergence, compute or energy efficiency, composition contribution, whole-system superiority, external validity or scientific novelty. Scientific credit is zero.

## Build value if no novelty exists

The contract is useful even if every mechanism is established: it keeps high-level modulation distinct from local control, makes descending influence independently ablatable, keeps local controllers replaceable, and gives checkpoint/replay/rollback an explicit cross-layer transaction boundary.

## Suggested SYSTEM_BUILD scope

Do not allocate or dispatch SB003 here. If Evidence Analyst later durably allocates an SB003-class build after current M1 sequencing conditions are satisfied, the smallest next slice should port the already-green semantic-surface/checkpoint Forge component and add only the bounded ModulationFrame boundary plus the acceptance/ablation tests above.

The design is independent of unknown future MAIN outcomes: it can be specified and tested against an abstract or mocked high-level modulation source. Actual build ownership, activation order and merge authority remain with Analyst/MAIN/Control.

No experiment, result-bearing workflow, scientific ref, build ref, scheduler state, consumed identity or immutable evidence is changed.
