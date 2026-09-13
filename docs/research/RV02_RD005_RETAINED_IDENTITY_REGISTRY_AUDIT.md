# RV02 RD005 retained identity registry audit

Date: 2026-09-14  
Reviewed authoritative RD005 head: `0c634a10d0a4b91e94ba12325ae96bac992bbdd1`  
Review type: automation technical/scientific-integrity audit; not an independent human identity  
Status: **PRE-D1 / REGISTRY INVENTORY PARTIALLY ESTABLISHED / AUTHORITATIVE_COMPLETE NOT YET JUSTIFIED**

## Scope

This audit advances only the prospective RD005 retained seed/world collision-registry boundary. It does not construct D1, execute a learner or probe, open capability output, create a source freeze, issue a seal/STARTED state, rerun RD003/RD004, or modify any frozen/preserved evidence.

The active RD005 package requires an `RD005CollisionRegistry` with durable provenance, exact consumed/reserved seed and world identities, and an explicit `authoritative_complete = true` assertion. That assertion is scientific provenance, not a convenience flag, so this audit does not set it merely from a selected text search.

## Reconciled current implementation state

The authoritative head already contains the post-PR-116 construction hardening. The construction-only runner now validates its input/package, verifies the exact source checkout before creating the output directory, uses a fresh no-clobber output identity, and contains no learner/probe/formal path. The source verifier also binds the caller repository root to the actual Git top-level and verifies the manifest-bound source files before construction output begins.

Accordingly, the earlier readiness records are stale where they list the absence of a construction-only wrapper or pre-output source gate as blockers. Those implementation gaps are no longer the immediate frontier. The retained-identity registry is now the first unresolved execution-critical gate.

## Retained identity evidence established by this audit

The following earlier RV02 evidence is durable and mutually consistent about the exposed-development world namespace:

1. `artifacts/research/rv02/development-feasibility-v1/manifest.json` records `ScaleStudyConfig` seed `92001`, scales `(1, 3, 10)`, and the six exposed development families.
2. `artifacts/research/rv02/rd001/manifest.json` records the same seed `92001`, scales `(1, 3, 10)`, and six-family matrix. RD001 is executed development evidence and must not be treated as fresh.
3. `artifacts/research/rv02/rd002/manifest.json` records the same seed `92001` and inherited exposed-development matrix. RD002 has a non-moving accepted-development preservation ref and must not be treated as fresh.
4. `docs/research/RV02_RD003_ONLINE_HIDDEN_ELIGIBILITY_PREREG.md` prospectively fixes reuse of the already exposed RV02 development worlds. RD003 attempt 001 is consumed and preserved; no rerun is permitted.
5. `docs/research/RV02_RD004_RELATIVE_PROBE_CLOCK_PREREG.md` explicitly inherits the same exposed RV02 development worlds and scales from RD003. RD004 attempt 001 is consumed and preserved; no rerun is permitted.
6. `src/sparkbrain/research/rv02_scale.py` canonically derives the six exact world identities for seed `92001`:

```text
rv02-development:92001:disjoint-routes
rv02-development:92001:shared-cue
rv02-development:92001:shared-prefix
rv02-development:92001:opposing-reversal
rv02-development:92001:dense-load
rv02-development:92001:capacity-pressure
```

Therefore seed `92001` and these six world identities are definitely members of the consumed/exposed identity set for any future authoritative collision registry.

## Why `authoritative_complete = true` remains fail-closed

The evidence above proves positive membership but does not, by itself, prove repository-wide completeness. The repository contains multiple historical RV02 development/smoke artifacts, execution bundles, moving research branches, and immutable freeze/preserve refs. A collision registry advertised as authoritative must demonstrate that all retained/reserved identities capable of colliding with RD005 were covered, rather than infer completeness from the currently convenient subset.

In particular:

- repository text search is not sufficient because arbitrary numeric occurrences are not seed identities;
- moving branch names are not themselves durable evidence of whether an identity was consumed;
- the invalid `smoke-v1-invalid` artifact cannot be promoted into scientific evidence merely to populate a registry;
- the prospective RD005 seed `92505` must not be silently classified as prior consumed evidence merely because it appears in the planned RD005 matrix; the freshness/reservation semantics for the prospective identity must remain explicit and non-circular;
- a registry must retain source paths/refs that allow an independent verifier to reconstruct why each seed/world identity is included.

For these reasons this review intentionally does **not** create an `RD005CollisionRegistry(authoritative_complete=True)` artifact yet.

## Required completion contract for the authoritative registry

Before the registry can be bound into a freeze-ready RD005 package, a dedicated registry artifact/builder should fail closed unless all of the following are true:

1. It enumerates the durable RV02 evidence classes that can establish consumed/reserved development identities (accepted/preserved executions, source freezes that crossed an execution boundary, and explicit prospective reservations where reservation semantics are unambiguous).
2. It records immutable provenance paths or refs for each identity source; selected moving research branches alone are insufficient.
3. It reconstructs seed/world identities from structured retained evidence where available, rather than grepping arbitrary numbers.
4. It proves that the known consumed seed `92001` and the six exact canonical world IDs above are present exactly once after normalization.
5. It rejects contradictions between manifests, preregistrations, result reports, and preserve/freeze refs rather than choosing one silently.
6. It treats invalid smoke evidence as diagnostic history only unless another durable record explicitly reserves its identity.
7. It makes the prospective RD005 `92505` reservation/freshness rule explicit without allowing the candidate to self-certify freshness.
8. Only after the evidence inventory is demonstrated complete may it emit the package object with `authoritative_complete = true` and a deterministic registry digest.

## Remaining pre-D1 gates after registry completion

Once the authoritative retained-identity registry is established, RD005 still requires:

1. a real exact-source SHA-256 manifest built at the final construction candidate commit;
2. exact Python runtime and construction-only command binding;
3. fresh exact-head technical/semantic review and green required CI;
4. a non-moving construction source freeze;
5. one construction-only D1 execution under the frozen contract;
6. raw D1 retention, independent construction-integrity verification, and review of that exact retained artifact identity;
7. only then, a separate prospectively fixed capability package/runner with outcome-blind scoring before capability output is opened.

The standing 2026-09-11 human-review waiver may replace a literal human-identity-only stop if needed, but it cannot waive registry completeness, exact source/runtime identity, stage separation, no-clobber, or evidence preservation.

## Decision

**CONTINUE PRE-D1 REGISTRY CONSTRUCTION; DO NOT FREEZE OR EXECUTE D1 YET.**

This audit narrows the authoritative retained set by proving that seed `92001` and the six canonical `rv02-development:92001:*` world identities are mandatory members. It does not falsely assert that this is the complete repository-wide registry. The next safe implementation frontier is a fail-closed registry builder/verifier tied to durable evidence sources, followed by exact source/runtime/package binding and review.
