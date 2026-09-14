# RV02 RD005 authoritative retained identity registry technical review

Date: 2026-09-14  
Review type: automation technical/scientific-integrity review; not an independent human identity  
Human-review gate: `USER_AUTHORIZED_REVIEW_GATE_OVERRIDE / HUMAN_REVIEW_WAIVED_BY_USER_2026-09-11`  
Scope: prospective pre-D1 identity provenance only; no D1/capability/formal execution  
Decision: **REGISTRY CONSTRUCTION ACCEPTED, SUBJECT TO GREEN CI AND EXACT-HEAD MERGE**

## Reviewed boundary

This review supersedes only the unresolved completeness decision in `RV02_RD005_RETAINED_IDENTITY_REGISTRY_AUDIT.md`. It does not rewrite that audit and does not modify any frozen or preserved RV02 evidence.

The reviewed implementation adds:

- `docs/research/RV02_RD005_RETAINED_IDENTITY_REGISTRY.json`;
- `src/sparkbrain/research/rv02_rd005_retained_registry.py`;
- fail-closed unit tests;
- exact-source-manifest binding of the registry implementation and the retained evidence used to reconstruct it.

## Completeness basis

The retained repository evidence root `artifacts/research/rv02` was enumerated directly before this review. Its exact top-level inventory is:

1. `README.md`
2. `development-feasibility-v1/`
3. `local-execution-history.bundle`
4. `rd001/`
5. `rd002/`
6. `rd003/`
7. `rd004/`
8. `smoke-v1-invalid/`
9. `smoke-v2/`

The builder requires this exact inventory. A later added or removed top-level retained-evidence class causes registry reconstruction to fail and requires a new audit rather than being silently omitted.

Structured manifests from development-feasibility-v1, smoke-v2, RD001 and RD002 all reconstruct seed `92001`. The retained invalid smoke manifest also uses the same namespace; it is classified as invalid scientific evidence but remains collision-relevant history. Canonical `development_worlds(...)` reconstruction yields exactly the six `rv02-development:92001:*` world identities committed in the registry specification.

RD003 prospectively states that it reuses the already exposed RV02 development worlds. RD004 states that it inherits the same exposed worlds and records RD003 attempt 001 as a consumed frozen execution. Therefore neither RD003 nor RD004 introduces a separate seed/world namespace beyond the reconstructed `92001` set.

## Immutable-anchor verification

The following non-moving anchors were re-fetched from GitHub before recording the registry:

- `preserve/rv02-rd002-accepted-development` -> `24af1858cb4a8930039b85442583d2bf535a3a49`
- `freeze/rv02-rd003-development-source` -> `79a949568b2a9a8ee18c40e9b356c564422c0127`
- `preserve/rv02-rd003-attempt-001` -> `cfe0903b6f2e1d16a6b5581ae004502dabdf62b5`
- `freeze/rv02-rd004-development-source` -> `75268dd804f0ef113869be172adf575ac22523a0`
- `preserve/rv02-rd004-attempt-001` -> `2efaf81119a32087b2102bbdbff1af61cbc6bf16`

These refs remain evidence anchors and must not be moved, deleted or rewritten.

## Freshness and non-circularity

Prospective RD005 seed `92505` is not inserted into the prior registry. Its freshness is established only by absence from the independently reconstructed retained set. The registry specification explicitly forbids self-certification, and the builder rejects a specification that changes that rule.

The resulting prior collision set is therefore:

- consumed/reserved seed identities: `{92001}`;
- consumed/reserved world identities: the six canonical `rv02-development:92001:*` identities.

This decision does **not** mean seed `92505` has been consumed. No construction or execution boundary is crossed by registry creation.

## Fail-closed properties reviewed

The implementation rejects:

- any unreviewed addition/removal under the retained RV02 evidence root;
- protocol/config drift in the retained structured manifests;
- disagreement between reconstructed and declared seed/world identities;
- changed immutable-ref declarations relative to the reviewed anchor set;
- loss of the README's invalid-smoke classification;
- loss of RD003/RD004 exposed-world inheritance provenance;
- prospective RD005 self-certification or insertion into the prior registry;
- collision of fresh seed `92505` with the reconstructed prior set.

The package source-manifest contract is extended so the registry code/spec/audit/review, relevant preregistrations, retained manifests, README and local execution-history bundle must all be hashed by the final exact RD005 source manifest.

## Remaining gates

Acceptance of the authoritative retained registry removes the registry-completeness blocker only after this exact PR head passes required CI and is exact-head merged. RD005 still must not execute D1 until all of the following are completed on a later exact candidate head:

1. build the real SHA-256 source manifest for that exact Git commit;
2. bind exact Python runtime and construction-only command;
3. perform fresh technical/semantic review of the final bound package;
4. create a non-moving construction source freeze;
5. execute construction-only D1 exactly once under the frozen contract;
6. preserve and independently verify the raw D1 construction artifact;
7. only after retained D1 review, prospectively define and freeze any capability-stage runner/scoring package.

## Review decision

**ACCEPT the registry design and completeness argument for the current retained RV02 evidence inventory, contingent on green CI and exact-head merge.**

No capability result has been observed, no candidate has been consumed, no formal identity has been rerun, and no frozen/preserved evidence has been modified by this review.
