# Internal scope allocator — Forge prototype

Status: `FORGE_PROTOTYPE`  
Evidentiary status: `NON_EVIDENTIARY`  
Scientific credit: `0`

## Purpose

Remove the existing stable-scope prototype's dependence on a caller-supplied scope token. The
prototype derives an opaque token from an admissible observation vector and predictive mismatch,
then passes that token to the existing managed revision overlay.

The public allocation API accepts no scope, episode, regime, entity, target, truth, or evaluator
identifier. Allocators are isolated by Assembly, tokens are issued internally, state is JSON
replayable, and resource exhaustion raises explicitly instead of silently evicting prior state.

## Bounded behavior

- The first observation bootstraps an internally issued scope.
- A later observation inside a fixed Euclidean reuse radius reuses that scope.
- A distant observation creates a scope only when predictive mismatch reaches a fixed threshold.
- A distant observation with insufficient mismatch abstains without updating revision state.
- A returning observation may reuse a prior scope.
- The wrapper preserves the existing plural-hypothesis revision and abstention behavior.

## Ordinary reduction

This implementation is a deterministic nearest-centroid cache namespace plus a thresholded
change-point heuristic. It is useful integration plumbing, but it does not establish autonomous
latent-cause learning, scientific novelty, comparative advantage, or a mechanism claim.

## Deliberately unresolved

- learned or calibrated scope-allocation parameters;
- a prospective task proving appearance/dynamics identifiability;
- matched latent-cause, change-point, or mixture comparators;
- selective scope closure and lifecycle policy;
- resource-matched scaling behavior;
- any canonical candidate or SYSTEM_BUILD admission.

Any scientific use requires a fresh prospective object and Evidence Analyst authorization. This
prototype does not alter RV02, SB001, consumed identities, or canonical evidence.
