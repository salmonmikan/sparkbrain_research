# SparkBrain Research Orchestrator SUB — 2026-09-20 19:46 JST

## Generation / authority

- schema_version: `2`
- generation_id: `SUB-20260920T194640+0900-SYSTEM-ASMORDER-BA8FDEBE`
- produced_at: `2026-09-20T19:46:40+09:00`
- producer_run_id: `SUB-RUN-20260920T194640+0900-ASMORDER-BA8FDEBE`
- authority_scope: `SUB_BOUNDED_NON_EVIDENTIARY_SYSTEM_DISCOVERY_AND_CONTROL_PLANE_PERSISTENCE`
- supersedes_generation_id: `SUB-20260920T184410+0900-THEORY-CONTEXTPRED-7A4C2E91`
- Evidence Analyst: `EVA-20260920T190536+0900-R18-AC1DB49E@fec9320a8e8c868f4df91dafb1af75c640ae995a`
- MAIN: `MAIN-20260920T191546+0900-PRIMARY-FUNNEL21-HOLD-R18-8C2F41D7`, lane `LOWER_FUNNEL_MAIN_HOLD_NO_COHERENT_CENTRAL_OBJECT`, active object `NONE`
- Control Brain: `CTRL-20260920T165000+0900-R15-6C2F8A41@64611f391391844d60659732a50a22cf009a5797`, strategy only
- previous SUB: `SUB-20260920T184410+0900-THEORY-CONTEXTPRED-7A4C2E91`
- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`

## Decision

- mode: `discovery`
- discovery_mode: `SYSTEM_DISCOVERY`
- target: `V05_ASSEMBLY_CLUSTER_ORDER_DEPENDENCE_DISCOVERY_CYCLE1`
- proposed candidate: `CAND-V05-ASSEMBLY-CLUSTER-ORDER-DEPENDENCE-01` (`SUB_PROPOSED_NOT_YET_ANALYST_CANONICAL`)
- exploration_cycle: `1/3`
- evidentiary_status: `NON_EVIDENTIARY`
- proposed claim_ceiling: `SYSTEM`
- proposed preformal_eligible: `false`
- recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`

Analyst R18 had no formal SUB lane, no fallback object, and no usable authorized candidate-pool target; MAIN had no active scientific object. One bounded autonomous SYSTEM Discovery was therefore selected. It avoids H7, all Analyst-terminal objects, FORMAL/TEST/scoring, consumed/frozen identities, preserve/control/evidence refs, and stable-main mutation.

## Theory-backward accounting

Before this selection the last three autonomous safe nonduplicative selections were endogenous continuation=`MECHANISM`, pre-semantic function transfer=`MECHANISM`, context-conditioned prediction=`MECHANISM` (`3/3`). After this SYSTEM selection the rolling window is pre-semantic function transfer=`MECHANISM`, context-conditioned prediction=`MECHANISM`, Assembly cluster order=`SYSTEM` (`2/3`). Supply v2.1 remains satisfied; `theory_backward_exception=null`.

## Question / prospective semantics

Question: can `TemporalAssemblyMemory` assign a different candidate partition to the same multiset of DEV patterns solely because the immutable first-seen prototype differs with presentation order?

Before outcome, stable-main `assemblies.py` semantics were read and terminal observables fixed: candidate count and pattern-to-assembly assignments. The contract was committed at `7e2646cfb1a83f5cbbec0b22c5dcf2a706f8022d`.

The fixed bridge triad used threshold `0.66`, bins `(0,1,2,3)`, A=`(1,2,3,4)`, B=`(1,2,3,5)`, C=`(1,2,4,5)`. Fixed similarities: A-B=`0.7625`, B-C=`0.7625`, A-C=`0.6250`. Arms were the same multiset in orders `A->B->C` and `B->A->C`.

## Implementation / observations

Branch: `research/exploratory-sub-assembly-cluster-order-20260920`.

The first test-head CI `35505600594` stopped at lint before Local readiness/Test in both Python jobs, so it exposed no scientific outcome. Only import formatting was corrected at `fca8ad5a5214cc9ca67c157ef45c5d129a3f66d7`; no scientific input, comparator, terminal, or threshold changed. Corrected CI `35505715764` completed success.

Observed terminal: `ORDER_DEPENDENT_CLUSTER_PARTITION`.

- `A->B->C`: A/B share the first candidate, C forms a second candidate => `2` candidates.
- `B->A->C`: B is the immutable prototype and both A and C join it => `1` candidate.

This is explained by first-prototype anchoring: existing candidate prototypes are not updated when later patterns join, so a non-transitive bridge configuration is insertion-order-sensitive. Result/final research head is `6f14715a856f3ae308d9dbe2d5bb35534823372c`; exact-head CI `35505873447` completed success on Python 3.11/3.13 with lint, local readiness, tests, and bundle validation green.

## Funnel v2.1 proposal

- proposed claim_ceiling: `SYSTEM`
- proposed preformal_eligible: `false`
- preliminary readiness: `N/A_FOR_SYSTEM_OBJECT`
- proposed hold_class: `null`
- proposed hold_reason: `null`
- proposed terminal_state: `ACTIVE`
- proposed queue_state: `QUEUED`
- candidate next research layer: `ARCHITECTURE_STUDY_ASSEMBLY_CLUSTER_ORDER_DEPENDENCE_CONTRACT`
- recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`

The Architecture study should prospectively test supported integrated reachability of bridge-like pattern sets, define whether presentation order is intended clustering semantics, quantify partition sensitivity, and test whether partition changes cause downstream prediction/action differences. No clustering patch or threshold/prototype tuning should be made against this observed result.

Reduction/falsifier for a fresh Architecture object: reduce the concern if prospectively fixed integrated probes show bridge-like sets are unreachable under supported Assembly generation, or if order is explicitly intended semantics and no downstream functional consequence survives a matched comparator.

## Completion

Utility request: none. Consumed identities: none. New FORMAL results: zero. Cycle 2 was not used. Blocker: fresh Evidence Analyst classification/promotion decision only.

Completion target `ACHIEVED_ONE_BOUNDED_SYSTEM_ASSEMBLY_CLUSTER_ORDER_DISCOVERY_CYCLE_AND_FOUND_FIRST_PROTOTYPE_ORDER_DEPENDENT_PARTITION` — achieved.
