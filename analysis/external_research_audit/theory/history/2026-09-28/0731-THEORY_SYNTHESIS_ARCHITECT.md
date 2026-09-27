# Theory Synthesis Architect — hierarchical local sensorimotor integration design

- schema_version: `2`
- generation_id: `THEORY-20260928T073157+0900-R13-FLY-HIERARCHICAL-INTEGRATION-DESIGN-4F7A2C91`
- produced_at: `2026-09-28T07:31:57+09:00`
- producer_run_id: `external-theory-auto-THEORY-20260928T073157+0900-R13-FLY-HIERARCHICAL-INTEGRATION-DESIGN-4F7A2C91`
- authority_scope: `NON_EVIDENTIARY_NONCANONICAL_THEORY_SYNTHESIS_ZERO_EXECUTION_AUTHORITY`
- supersedes_generation_id: `THEORY-20260928T012709+0900-R12-NO-PROPOSAL-SB002-ALLOCATION-84D1B6C2`
- role: `THEORY_SYNTHESIS_ARCHITECT`
- schedule_slot: `07:30 JST`
- role_resolution_source: `SCHEDULED_OCCURRENCE`
- genuinely_new_information: `true`
- new_sparkbrain_scientific_result: `false`

## Freshness and disposition

The current Human Directive branch/index identity is `8ce979b9ec0bc7eede5225c0403698f8886d3e8d` / `1ba1e173344f36e14d0e21e6f3e823254e031f7d`. Relative to Theory R12, the branch is three commits ahead and adds `HUMAN-20260928-001` and `HUMAN-20260928-002`; both bodies were read. The interpretation is to support post-M1 integration in parallel, preserve the build-to-science boundary, and keep FLY-0 isolated until Evidence Analyst allocation.

M1 has since been squash-merged through PR #163 into `main` at `59fc994b39d0ba02682e972161bb46801592d25b` (tree `7c5c86300a0097cd20b76076eeecb748b3c11134`) with successful PR and post-merge CI. This is a material engineering-state change, not scientific evidence. Durable Analyst R162 still requires post-integration reconciliation and authorizes neither SB003 nor scientific execution.

## Primary proposal

- design_id: `ID-SB-FLY-HIERARCHICAL-SENSORIMOTOR-LOOP-001`
- status: `INTEGRATION_DESIGN_PROPOSAL`
- target_capability: connect the integrated M1 state/revision loop to plural bounded local sensorimotor modules through descending modulation and ascending state feedback, closing deterministic action→world→observation continuity without making the local loop a hidden scientific mechanism.

### Component map and provenance

1. `bounded_world`: deterministic world fixture and action/observation clock; ordinary SYSTEM_BUILD infrastructure.
2. `event_adapter`: converts bounded world observations into explicit event packets with sequence/provenance metadata; reference engineering component.
3. `local_modules[]`: plural body/action-specific local sensorimotor modules. Initial candidates are the isolated FLY-0 structured fixture, a simple modular finite-state/reactive controller, and a reduced connectome-constrained LIF reference. FLY-0 remains Forge-owned and noncanonical unless separately admitted.
4. `m1_supervisor`: the merged M1 persistent-state, plural-scope, competition/abstention, prediction/action and selective-revision loop; NON_EVIDENTIARY_BUILD.
5. `descending_modulation`: bounded high-level goal/mode signal from M1 to each local module; no direct micro-control requirement.
6. `ascending_feedback`: explicit local state, confidence, saturation, latency and action trace returned to M1 for later observation/revision.
7. `action_arbiter`: deterministic bounded arbitration among local proposals, including abstention and fail-closed conflict.
8. `transaction_coordinator`: one observation/action/world transition across M1, local modules, arbiter and checkpoint-visible sequence state, with atomic rollback.

Known reductions: local sensory-effector loops, ascending/descending coordination, modular premotor organization and connectome-constrained spiking sensorimotor models are established design primitives. The proposal therefore claims synthesis/build value only. It does not treat fly-inspired structure as a novel principle.

### Interfaces and state loop

`WORLD → event_adapter → local_modules[] → ascending_feedback → m1_supervisor → descending_modulation → local_modules[] → action_arbiter → ACTION → WORLD`, with `transaction_coordinator` spanning the complete step and M1 checkpoint/replay spanning all externally visible state.

Each component is used for a specific separation: local modules provide low-latency bounded control; M1 supplies persistent context and selective revision; ascending feedback prevents the local controller from becoming opaque; descending modulation avoids high-level micromanagement; the arbiter exposes conflict/abstention; and the transaction coordinator preserves replay and rollback.

### Known limitations

- FLY-0 is hand-authored, synthetic and tested only as a deterministic pulse fixture; it is not a fly connectome or biological model.
- The current FLY-0 observation uses one degree-preserving rewire and one random graph; it cannot support topology-specific inference.
- M1 integration establishes bounded function, not comparative advantage, composition contribution or novelty.
- Body/action semantics, temporal scale separation and multi-module arbitration remain prospective.
- A connectome-constrained LIF replacement still depends on explicit modeling assumptions and is not biological ground truth.

### Acceptance tests for a later Analyst-authorized SYSTEM_BUILD

1. A deterministic bounded world completes multi-step action→world→observation cycles with at least two local modules and an explicit M1 modulation surface.
2. Checkpoint/restore/replay reproduces exact same-history opaque tokens, action trace, local state and M1 state.
3. Invalid event, module timeout, arbitration conflict, resource overflow or rejected revision produces complete no-write rollback across the whole step.
4. Structured, degree-preserving rewired, random sparse and simple modular-controller replacements share declared unit/edge or separately normalized compute/activity/delay envelopes; mismatches are reported, not hidden.
5. Ascending feedback contains only prospective runtime state and never exposes held-out/evaluator information.
6. Resource, latency, activity exposure, abstention and action-error traces remain inspectable per module and per world step.

### Suggested replacement and interaction tests

- Replace FLY-0 with a simple modular finite-state/reactive controller and with a reduced connectome-constrained LIF controller.
- Ablate descending modulation, ascending feedback, local recurrence and cross-module arbitration separately.
- Replace high-level M1 modulation with a fixed schedule to test whether the closed loop needs adaptive supervisor state.
- Compare plural body/action modules against one generic recurrent module under matched world exposure.

Alternative established architecture: a hierarchical state-space or model-predictive supervisor over conventional reactive/PID or finite-state local controllers. This is the default reduction target, not an inferior straw baseline.

### Claim boundary and build value

Scientific claims explicitly not made: biological fidelity, fly-brain reproduction, topology superiority, energy efficiency, emergent cognition, whole-system superiority, composition contribution, or scientific novelty.

Build value if no novelty exists: continuous embodiment, explicit time-scale separation, modular fault isolation, replaceable local controllers, visible causal interfaces, and a bounded platform for later prospective questions.

Suggested SYSTEM_BUILD scope: after post-integration Analyst reconciliation, consider one independent SB003-equivalent build that adds the adapter, ascending/descending interfaces, two local modules, arbiter and transaction coverage without modifying A01, RV02, H9/C07 evidence or consumed identities. Exact ID, ownership and admission remain Analyst decisions.

Independence: the proposal uses the now-merged M1 interface and does not depend on unknown future MAIN outcomes. It does not authorize continuation, allocate SB003, promote FLY-0 or require a mandatory review gate.

## Revisit and evidence boundary

`NO_REVISIT_PROPOSAL`. Existing terminal objects remain closed. No experiment, result-bearing workflow, one-way identity, scientific mutation, scheduler change or build allocation occurred. This design is not scientific evidence.
