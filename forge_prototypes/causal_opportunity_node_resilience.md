# Causal-opportunity internal-event resilience — Forge prototype

Status: `FORGE_PROTOTYPE`  
Evidence: `NON_EVIDENTIARY / NONCANONICAL`  
Scientific credit: `0`

## Target capability

After a caller-supplied complete trace receives a causal-opportunity
certificate, measure whether its treatment-to-readout routes share one internal
event or contain two or more internally event-disjoint routes. Return one
deterministic minimum internal-event cut.

## Ordinary reduction

The implementation is node splitting plus maximum-flow/minimum-cut on a
validated time-respecting event graph. It is ordinary graph analysis, not
causal inference, learning, memory, or a novel cognitive mechanism.

## Claim boundary

Internal-event redundancy describes only the supplied trace. It does not
establish causal effect, trace completeness, component or actor redundancy,
hidden-path absence, readout sensitivity, real-task capability, composition
contribution, comparative support, or scientific novelty.

## Collision boundary

This prototype extends a separate Forge diagnostic. It does not implement or
modify SB002 routing, revision, rollback or checkpointing; RD005/RD006 dynamics;
Candidate #35; or scientific/evidence refs.
