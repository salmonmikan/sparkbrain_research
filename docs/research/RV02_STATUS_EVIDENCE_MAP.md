# RV02 current status and evidence map

Status as of 2026-09-16: **secondary line; RD005 D1 exact construction identity consumed with a terminal construction failure; capability unopened; no prospective successor is defined here.**

This document is a docs-only consolidation of already-existing RV02 source, control, preservation, and post-outcome audit records. It does not change experiment code, protocols, thresholds, candidate parameters, scorer logic, workflow state, or any immutable evidence anchor.

## Current mutable research baseline

The current live RV02 development branch verified for this consolidation is:

- `research/rv02-development-feasibility`
- head: `8176b91f5d427f3bdfccae2fac2c01b60a771403`

That branch records development-feasibility work only. Its publication commit explicitly reports 36/36 development cells and 24 focused tests while making **no formal or resource-matched superiority claim**. Relevant source documents include:

- `docs/research/RV02_DEVELOPMENT_FEASIBILITY_CONTRACT.md`
- `docs/research/RV02_FIELD_SCALE_STUDY_PLAN.md`

The historical `research/rv02-distal-delay` name referenced by older control-plane analysis is not present in the current remote branch inventory and is therefore not treated as the current mutable RV02 authority by this map.

## RD005 D1 exact consumed identity

The exact consumed construction-input identity is:

`96634541dc29b00be9f19b5819d45f541af69348ab6c1b0da6b48e943221700a`

Authoritative anchors re-verified from the current remote repository:

| Role | Ref / identity | Exact commit or digest |
| --- | --- | --- |
| Source freeze | `freeze/rv02-rd005-d1-source-c60b7fd8-20260914` | `c60b7fd8d3889ee969f505d921e7d31c990871e6` |
| Source manifest | — | `46b75901f831358263bfb940535204a7743286353f1cc61336183c7bbf65a87` |
| Construction input | — | `96634541dc29b00be9f19b5819d45f541af69348ab6c1b0da6b48e943221700a` |
| Preflight control | `control/rv02-rd005-d1-preflight-c60b7fd8-20260914` | `096ddb8c65f342866839a2cb135d45e36ec1aabf` |
| STARTED boundary | `control/rv02-rd005-d1-started-96634541-20260914` | `2535b6312a091f7da4efa10c064c285bdeda7eaf` |
| Raw outcome preserve | `preserve/rv02-rd005-d1-96634541-20260914` | `d1fdd67ea197b879c52942c4a34e7d39a0a40698` |
| Post-outcome audit | `review/rv02-rd005-d1-terminal-outcome-20260914` | `a02768b18fa290f249b7c488c896fad79f9ca409` |

The post-outcome audit document is:

- `docs/research/RV02_RD005_D1_TERMINAL_OUTCOME_20260914.md` on `review/rv02-rd005-d1-terminal-outcome-20260914`

The preserved raw terminal evidence is under:

- `artifacts/rv02/rd005/development/construction-96634541dc29b00be9f19b5819d45f541af69348ab6c1b0da6b48e943221700a/`

## Authoritative outcome

The one-way D1 construction crossed STARTED once and preserved a failure instead of being repaired or retried. The terminal condition is:

`RD005 construction stopped before capability: verified D1 matrix is not ready`

The preserved result marks the identity as terminal and non-retryable. Capability output was not opened and learner/probe execution did not occur.

Therefore the correct current interpretation is narrow:

- this is a **negative construction / gate-reachability result for this exact D1 identity**;
- it is **not** a scored formal or held-out confirmatory result for the later RD005 capability hypotheses;
- the exact construction identity is consumed and must not be rerun, retuned, silently repaired, or reopened;
- the source freeze, STARTED ref, preserve ref, and raw failure evidence remain immutable evidence anchors.

A concurrent Actions launch was blocked by the STARTED guard before duplicate execution, so only one run consumed the exact D1 identity.

## Current scientific status

RV02 currently contributes a useful negative constraint rather than a surviving positive mechanism claim: the consumed RD005 D1 construction did not reach the capability stage under its frozen contract. Earlier development-feasibility evidence remains development evidence and does not override that terminal one-way outcome.

No distinct prospective RV02 successor identity or frozen successor protocol is defined by the current Evidence Analyst handoff or by this consolidation. Any continued RV02 experiment must therefore be a newly specified, prospectively distinct candidate/identity with its own outcome-blind contract. This document intentionally does **not** propose such a successor.

## Integrity boundary

This consolidation changes documentation only. In particular it does not:

- modify `research/rv02-development-feasibility`;
- move or rewrite any `freeze/*`, `control/*`, or `preserve/*` ref;
- alter RD005 source/package/input bindings;
- create STARTED or dispatch a workflow;
- consume a new identity;
- score or reinterpret unopened capability output;
- define a new candidate, mechanism, TTL, magnitude, conditioner, timestamp, threshold, or scorer rule.

The purpose is solely to make the current RV02 state auditable from one canonical map while preserving every one-way and immutable boundary.
