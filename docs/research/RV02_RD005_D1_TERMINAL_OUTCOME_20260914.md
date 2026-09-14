# RV02 RD005 D1 terminal outcome audit

Date: 2026-09-14  
Status: **D1 CONSTRUCTION IDENTITY CONSUMED — TERMINAL FAILURE PRESERVED — CAPABILITY UNOPENED**

## Scope

This record is a post-outcome audit only. It does not modify the frozen RD005 source/package contract, does not repair the consumed D1 identity, and does not authorize a retry of the same construction input.

## Exact identities and evidence anchors

- exact source Git SHA: `c60b7fd8d3889ee969f505d921e7d31c990871e6`
- non-moving source freeze: `freeze/rv02-rd005-d1-source-c60b7fd8-20260914`
- source manifest SHA-256: `46b75901f831358263bfb940535204a7743286353f1cc61336183c7bbf65a87`
- construction input SHA-256: `96634541dc29b00be9f19b5819d45f541af69348ab6c1b0da6b48e943221700a`
- retained collision registry SHA-256: `8ab433385577406720661d72af6cc5c6e52594b9b3a3a4bb45f388fa98fdf115`
- package plan SHA-256: `df1c9cadf4213cac1aa32bf4bf1816f3af99ec1c142808532451d00a3b62cb29`
- execution binding SHA-256: `6ffffb11dafc8e2eebb678387751561ca881658b450de19fdf4e05403230f43f`
- exact preflight control ref: `control/rv02-rd005-d1-preflight-c60b7fd8-20260914`
- exact preflight commit: `096ddb8c65f342866839a2cb135d45e36ec1aabf`
- STARTED control ref: `control/rv02-rd005-d1-started-96634541-20260914`
- STARTED commit: `2535b6312a091f7da4efa10c064c285bdeda7eaf`
- immutable outcome preserve ref: `preserve/rv02-rd005-d1-96634541-20260914`
- preserve commit: `d1fdd67ea197b879c52942c4a34e7d39a0a40698`
- bound runtime: `CPython 3.11.15`
- fresh prospective seed used by this consumed identity: `92505`

Human-review gate was transparently handled as `HUMAN_REVIEW_WAIVED_BY_USER_2026-09-11`; no independent human reviewer identity is claimed. The one-way execution was covered by `GLOBAL_EXPERIMENT_FORMAL_EXECUTION_PREAUTHORIZATION_2026-09-13`.

## Execution and preserved outcome

The exact D1 construction command crossed STARTED once under the frozen contract. The bound construction terminated with exit code `1` and preserved `FAILED.json` rather than silently repairing or retrying.

The preserved top-level terminal condition is:

`RD005 construction stopped before capability: verified D1 matrix is not ready`

The preserved machine-readable result classifies the outcome as `D1_CONSTRUCTION_FAILED_TERMINAL_IDENTITY_CONSUMED`, with `retry_same_identity_allowed=false`, `capability_output_opened=false`, and `learner_or_probe_executed=false`. Lower-level construction diagnostics are retained in the immutable construction artifact; this audit intentionally does not promote an unverified nested diagnostic into the authoritative terminal condition.

This is therefore a negative **construction / gate-reachability** result for this exact identity. It is not a scored confirmatory result for H1/H4/K1/K2, because the preregistered capability stage was never opened.

## Concurrent-launch reconciliation

Two Actions runs were created from the same one-shot control-plane push. The run that won the one-way race created the STARTED ref and executed the construction. The concurrent run reached the STARTED step only after that ref existed and failed before execution. Thus the STARTED guard prevented a duplicate construction execution; only one run consumed the exact D1 identity.

Consuming run: `34831458943`.  
Non-consuming concurrent run blocked before execution: `34831449412`.

## Integrity decision

- **DO NOT RETRY** construction input `96634541dc29b00be9f19b5819d45f541af69348ab6c1b0da6b48e943221700a`.
- **DO NOT MODIFY** the source freeze, STARTED ref, preserve ref, or raw terminal evidence.
- **DO NOT OPEN RD005 CAPABILITY** from this consumed identity; its D1 gate was not reached successfully.
- Any continued RV02 work must use a prospectively distinct experiment/candidate identity, with a newly defined and frozen contract. The failure may motivate future prospective design, but it must not be repaired in place or treated as an unconsumed preflight.
