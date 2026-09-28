# Theory Synthesis R14 — M1-002 robustness does not require a new integration design

- schema_version: 2
- generation_id: THEORY-20260928T093233+0900-R14-NO-PROPOSAL-M1-002-ROBUSTNESS-6C2F91A4
- produced_at: 2026-09-28T09:32:33+09:00
- producer_run_id: external-theory-auto-THEORY-20260928T093233+0900-R14-NO-PROPOSAL-M1-002-ROBUSTNESS-6C2F91A4
- authority_scope: NON_EVIDENTIARY_NONCANONICAL_THEORY_SYNTHESIS_ZERO_EXECUTION_AUTHORITY
- supersedes_generation_id: THEORY-20260928T073157+0900-R13-FLY-HIERARCHICAL-INTEGRATION-DESIGN-4F7A2C91
- role: THEORY_SYNTHESIS_ARCHITECT
- schedule_slot: 09:30 JST
- role_resolution_source: SCHEDULED_OCCURRENCE
- genuinely_new_information: false
- new_sparkbrain_scientific_result: false
- theory_status: NO_PROPOSAL
- retained_design_id: ID-SB-FLY-HIERARCHICAL-SENSORIMOTOR-LOOP-001
- retained_secondary_design_id: ID-SB-LATENT-SCOPE-PLURAL-REVISION-001
- revisit_status: NO_REVISIT_PROPOSAL

## Freshness and authority

The Human Directive index remains at `8ce979b9ec0bc7eede5225c0403698f8886d3e8d` with active-index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`, unchanged from Theory R13. Applicable directives read were HUMAN-20260928-001, HUMAN-20260928-002 and HUMAN-20260927-002.

Current Control R105 and Evidence Analyst R164 retain M1-002 as a MAIN-only NON_EVIDENTIARY_BUILD and require fresh Analyst exact-head reconciliation before PR or merge. No SB003, Relay or scientific allocation exists.

## New input inspected

M1-002 now exists at `system-build/m1-post-integration-robustness-20260928@2a21d3e879f1db4e81a58273180ad2124e823a5e`, directly parented by the required M1 base `59fc994b39d0ba02682e972161bb46801592d25b`.

Utility independently verified exact-head CI run `36361950457` successful for Python 3.11 and 3.13. The branch changes only a robustness test, documentation and the validation manifest; no runtime source, algorithm, threshold, routing topology, public field or resource ceiling changed.

The fixed harness covers nominal 64-cycle invariants, checkpoint continuation at 1/8/31/63, rollback at all seven existing fault points at early/middle/late positions, and duplicate/conflict/pending identity paths within 267 of 512 allowed committed cycles.

## Theory synthesis decision

No new scientific theory or integration design is proposed.

M1-002 operationalizes acceptance properties already required by M1 and already listed in Theory R13:

- deterministic multi-step continuity;
- exact checkpoint/replay;
- whole-step rollback;
- identity-safe no-write behavior;
- observable bounded resource usage.

Because the runtime component map and interfaces are unchanged, the harness does not create a new explanatory gap or design primitive. It strengthens engineering confidence in the existing loop but does not change the theory content.

## Retained integration design

Theory R13's `ID-SB-FLY-HIERARCHICAL-SENSORIMOTOR-LOOP-001` remains the sole primary post-M1 integration proposal:

- bounded world and event adapter;
- plural local sensorimotor modules;
- M1 supervisor;
- descending modulation;
- ascending feedback;
- deterministic action arbitration;
- atomic world-step transaction.

M1-002 is not added as a new component. Its harness is a reusable acceptance pattern for any later Analyst-authorized integration, including a possible SB003-equivalent, but it is not a dependency and does not authorize that build.

The retained replacement ladder remains simple modular FSM/reactive, reduced connectome-constrained LIF, degree-preserving rewired and random sparse. The retained interaction ablations separately remove descending modulation, ascending feedback, local recurrence, cross-module arbitration and fixed high-level scheduling.

## Claims explicitly not made

This run does not claim:

- scientific evidence or novelty;
- composition contribution;
- topology superiority;
- biological fidelity or fly-brain reproduction;
- whole-system superiority;
- energy efficiency;
- SB003 admission or build authority;
- a revisit trigger for A01, RV02, H9/C07 or any terminal object.

## Next boundary

Evidence Analyst should reconcile M1-002 exact head `2a21d3e879f1db4e81a58273180ad2124e823a5e`, tree `2237f3b1e8ac72d193fc2c3879f2b67f71d302e0` and CI run `36361950457` before any PR/merge continuation.

Theory creates no review gate, performs no execution and leaves the existing M1 and FLY-0 tracks running in parallel.
