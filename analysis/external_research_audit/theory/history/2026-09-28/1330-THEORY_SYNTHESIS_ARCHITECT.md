# Theory Synthesis Architect — gated ascending-state integration refinement

- schema_version: `2`
- generation_id: `THEORY-20260928T132946+0900-R15-GATED-ASCENDING-REFINEMENT-6E3A91C4`
- produced_at: `2026-09-28T13:29:46+09:00`
- producer_run_id: `external-theory-auto-THEORY-20260928T132946+0900-R15-GATED-ASCENDING-REFINEMENT-6E3A91C4`
- authority_scope: `NON_EVIDENTIARY_NONCANONICAL_THEORY_SYNTHESIS_ZERO_EXECUTION_AUTHORITY`
- supersedes_generation_id: `THEORY-20260928T093233+0900-R14-NO-PROPOSAL-M1-002-ROBUSTNESS-6C2F91A4`
- role: `THEORY_SYNTHESIS_ARCHITECT`
- schedule_slot: `13:30 JST`
- role_resolution_source: `EARLY_GRACE`
- genuinely_new_information: `true`
- new_sparkbrain_scientific_result: `false`
- theory_status: `INTEGRATION_DESIGN_PROPOSAL_REFINEMENT`
- design_id: `ID-SB-FLY-HIERARCHICAL-SENSORIMOTOR-LOOP-001`
- design_revision: `2`
- revisit_status: `NO_REVISIT_PROPOSAL`

## Freshness and authority

The Human Directive index is unchanged from Theory R14: `ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d`, blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`. No directive delta is present. Current Analyst R167 keeps M1-002 at `2a21d3e879f1db4e81a58273180ad2124e823a5e` as bounded-functionally verified but blocked operationally on PR creation. FLY-0 remains Forge-only, NON_EVIDENTIARY/NONCANONICAL, with no SB003 allocation. Control append-only R109 is the freshest durable Control record; its moving-pointer debt is operational only.

## Why refine R13

The prior interaction ablation found that Observation and ascending LocalFeedback were not causal for the bounded FLY-0 trajectory. The source-only Forge prototype at `f41aad9a726b985ea654900eb8a7c807d558fc08` now makes prior feedback gate the next modulation, but it uses a hard matched-motor-event dominance test and still lacks tests, CI, documentation and durable handoff.

Literature R47 adds a stronger reduction target: hierarchical ascending feedback, compact behavioral-state/self-motion summaries, selective/predictive gating of self-generated sensory feedback, and explicit sensorimotor delay are established design primitives. Therefore the next useful design is not merely “more bottom-up traffic”; it is a compact, causally consumed, context-gated and delay-accounted ascending-state path with an ordinary hierarchical replacement comparator.

## Integration design refinement

### Target capability

Local action/world outcomes are encoded into a compact ascending state that can causally alter the next high-level M1 modulation in a bounded task where that information matters. Expected self-generated movement can be selectively gated, while persistent/error-like state remains available. Feedback delay is explicit and matched across comparisons.

### Component map

1. `BOUNDED_WORLD`
2. `EVENT_ADAPTER`
3. `PLURAL_LOCAL_MODULES`
4. `ASCENDING_STATE_ENCODER`
5. `CONTEXTUAL_PREDICTIVE_GATE`
6. `DELAY_BUDGET_LEDGER`
7. `M1_SUPERVISOR`
8. `DESCENDING_MODULATION`
9. `ACTION_ARBITER`
10. `TRANSACTION_COORDINATOR`

The loop is:

`WORLD -> event_adapter -> local_modules[] -> local action/outcome -> ascending_state_encoder -> contextual_predictive_gate -> m1_supervisor -> descending_modulation -> local_modules[] -> action_arbiter -> ACTION -> WORLD`

The transaction coordinator spans the complete step. Gate state, feedback age/delay, local state, M1 state and action receipts must be checkpoint-visible and replayable.

A minimal ascending state may contain only prospective runtime information such as local pose/error proxy, self-motion/delta, confidence/saturation, action receipt and feedback age/delay. It must never expose held-out/evaluator truth.

### Why the added pieces matter

- `ASCENDING_STATE_ENCODER` gives an explicit causal object rather than an opaque raw-traffic channel.
- `CONTEXTUAL_PREDICTIVE_GATE` separates predictable self-generated delta from state/error information still useful to the supervisor.
- `DELAY_BUDGET_LEDGER` makes latency a visible fairness/resource variable instead of a hidden comparator advantage.
- An ordinary hierarchical reactive/FSM controller using the same encoder/gate/delay envelope is required as the default reduction comparator.

### Acceptance tests for any later Analyst-authorized build

1. Use a deterministic bounded perturbation where the next supervisor modulation genuinely depends on post-action local state; cutting ascending state must causally change or stall a predeclared decision/trajectory.
2. Verify expected movement delta can be suppressed while persistent/error-like information remains available. Compare contextual gating with pass-through/raw-forward and fixed-gate baselines.
3. Expose and match feedback delay budgets. Include a bounded delay perturbation and fail closed or explicitly report unmatched delay envelopes.
4. Checkpoint/restore/replay must exactly reproduce gate state, delay/age, local state, M1 state, receipts and action trace.
5. Malformed, stale, contradictory or over-budget feedback must produce full no-write rollback, including hidden gate/delay state.
6. The replacement ladder must include an ordinary hierarchical reactive/FSM controller under the same encoder/gate/delay envelope. Structured, degree-preserving rewired and random-sparse topology comparisons are interpretable only after unit/edge/input-output/activity/resource/delay mismatches are matched or reported.

### Suggested replacement and interaction tests

Replace FLY-0 with an ordinary modular reactive/FSM controller; replace gated summary with raw feedback; replace contextual gating with pass-through/fixed gating; remove ascending state; replace adaptive M1 modulation with a fixed schedule; and only then compare topology variants under matched exposure. Ablate observation input, ascending state, gate, descending modulation, local action, arbitration, and matched feedback delay separately.

### Established alternative architecture

A hierarchical state-space or model-predictive supervisor over conventional reactive/FSM local controllers with explicit local state estimation and predictive feedback gating is the default reduction target, not a straw baseline.

## Limitations and claim boundary

The current `f41aad9...` prototype is unverified and implements only a hard motor-event gate. The simple movement task remains solvable by ordinary reactive control. Resource/activity/delay matching and the replacement ladder are incomplete. Literature similarity does not specify the exact causal computation and does not establish biological fidelity.

No biological equivalence, fly-brain reproduction, topology superiority, energy efficiency, emergent cognition, whole-system superiority, composition contribution or scientific novelty is claimed. Forge/BUILD observations remain non-evidentiary.

## Suggested SYSTEM_BUILD scope

Theory does not allocate SB003. First, Forge should verify the source-only bottom-up prototype with tests/CI/durable handoff and close activity/resource/delay/comparator gaps. If Evidence Analyst later admits a bounded SB003-equivalent build, the smallest useful scope is the ascending-state encoder + contextual gate + delay ledger + ordinary hierarchical comparator around the existing M1 supervisor and bounded world, without modifying M1-002 or A01/RV02/H9/C07 evidence.

This refinement does not stop M1-002, create a mandatory review gate, reopen any consumed object, allocate a build ID or authorize execution.

## Evidence boundary

`NO_REVISIT_PROPOSAL`. No experiment, result-bearing workflow, one-way identity, scientific mutation, scheduler change or build allocation occurred. This design is NON_EVIDENTIARY/NONCANONICAL and is not scientific evidence.
