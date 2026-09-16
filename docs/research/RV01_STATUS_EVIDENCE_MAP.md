# RV01 current status and evidence map

Status date: 2026-09-16

This document is a canonical status/evidence index for RV01. It consolidates already-consumed development evidence and repository pointers only. It does not define a new experiment, successor, threshold, scorer, or formal claim.

## Current interpretation

RV01 R01-17 (`rv01-r01-17-real-delay-causal-timing-v1`) is consumed exposed-development evidence with classification `SUPPORTED_REAL_DELAY_CAUSAL_TIMING`.

The result supports the component-level claim that learned physical delay can causally shift downstream event timing under the preregistered R01-17 construction. All five scored development worlds were classified as `REAL_DELAY_SUPPORT_CELL`, with route preservation, exact SHAM replay, valid arm binding, delay displacement above the preregistered 0.5 ms minimum, and downstream arrival shifts above the preregistered 0.5 ms minimum.

This result has **development authority only**. It has no held-out or formal authority.

The current conservative reduction is ordinary local adaptive-delay plasticity: the R01-17 result does not by itself establish a new SparkBrain-specific computational principle. It demonstrates a real causal timing effect for this component while remaining compatible with a simpler local adaptive-delay mechanism.

No fresh prospective RV01 successor contract is currently verified. Do not infer or design a successor from the consumed R01-17 outcome in this status document.

## Consumed / no-rerun boundary

R01-17 identity:

- `rv01-r01-17-real-delay-causal-timing-v1`

This identity crossed STARTED and is consumed. Same-identity rerun, repair, retuning, rescoring under changed rules, or reinterpretive rescue is forbidden.

Earlier RV01 R01-16 construction/capability identities are also consumed and remain outside any R01-17 retry path.

## Authoritative source and one-way refs

Current RV01 research branch after preregistration merge:

- `research/rv01-endogenous-transition@98be60268845487ce51e76b8a7687552a5dbc51f`

Exact R01-17 frozen source and STARTED source:

- `freeze/rv01-r01-17-real-delay-source-20260915@5ecb459b609b393ff837f57cc138f1eb44c1b255`
- `control/rv01-r01-17-real-delay-started-20260915@5ecb459b609b393ff837f57cc138f1eb44c1b255`

Raw preserved evidence:

- `preserve/rv01-r01-17-real-delay-raw-20260915@fceb3663c7a880d82593e6c1efe52fcd1ad0c00a`
- workflow run recorded by preservation commit: `34978554838`

Scored preserved evidence:

- `preserve/rv01-r01-17-real-delay-scored-20260915@d4737d52ecbb2306d9f00f99366f0ad6424327be`
- score path: `artifacts/rv01/r01-17/development/rv01-r01-17-real-delay-causal-timing-v1/score.json`
- raw suite SHA-256: `7d6642bf16364c2a67acdf979324d0da59dcd7bbdc508c5f8773b6c654803dc2`
- score SHA-256: `b76f3c7b3ec29f97ea69de30c6fb0e3c171c1eaa0e80699bf8055c3586ded76e`

## R01-17 scored development result

Frozen classification:

- `SUPPORTED_REAL_DELAY_CAUSAL_TIMING`
- `phase: development`
- `formal_authority: false`
- `held_out_authority: false`

Scored seeds: `141800` through `141804`.

Across all five worlds:

- `delay_eligible: true`
- `route_preserved: true`
- `sham_exact: true`
- `arm_binding_valid: true`
- disposition: `REAL_DELAY_SUPPORT_CELL`

The per-edge learned delay displacements were approximately 1.51–2.19 ms across the five worlds. Downstream arrival shifts accumulated along the chain and remained above the fixed 0.5 ms causal-shift minimum.

## Protocol and review pointers

Prospective protocol:

- `docs/research/RV01_R01_17_REAL_DELAY_PREREGISTRATION_20260915.md`

Pre-execution readiness review:

- `docs/research/RV01_R01_17_FREEZE_READINESS_REVIEW_20260915.md`

These documents define the prospective R01-17 contract and review state. The preserved raw/scored refs above are authoritative for the consumed execution outcome.

## Relationship to R01-16

R01-17 was created as a distinct prospective exposed-development identity after R01-16 left the delay component unresolved because the realized delay intervention was only roundoff-scale. R01-17 did not repair, rerun, or reinterpret the consumed R01-16 identity.

R01-17 prospectively required a physically meaningful learned-delay displacement and a downstream causal timing shift, while matching learned weights between F0 and FD and retaining exact SHAM replay. The positive R01-17 development result therefore resolves the narrow component question that a real learned delay can alter causal arrival timing under the fixed construction.

It does **not** upgrade RV01 into a broader formal novelty claim.

## What is supported, unresolved, and closed

Supported at development level:

- a real learned physical-delay change occurred in the fixed R01-17 construction;
- resetting learned delay while retaining learned weights changed downstream causal arrival timing;
- the preregistered SHAM and arm-binding checks passed in all five development worlds.

Not established by R01-17:

- held-out or formal generalization;
- a uniquely SparkBrain-specific mechanism;
- superiority over simpler local adaptive-delay plasticity;
- a new prospective RV01 successor.

Closed for the consumed R01-17 identity:

- rerun;
- retuning;
- changed thresholds or scoring rules;
- same-identity rescue.

## Next-state boundary

RV01 currently has no verified fresh prospective successor. Any new RV01 experiment must be defined as a distinct prospective identity under a new contract before execution. This status map must not be used as permission to derive an outcome-responsive successor from the consumed R01-17 result.
