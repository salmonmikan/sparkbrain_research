# RV02 RD005 post-verifier readiness review

Date: 2026-09-12  
Originally reviewed source head: `aaa2e1f1f24c9e5dcc4fd31a65a465784fd2ea33`  
Status: **PRE-D1 / TOPOLOGY PROVENANCE FIX REQUIRED / EXECUTION DISABLED**

## Scope

This review covers the prospective RD005 exposed-development construction path after integration of the first independent fail-closed artifact verifier. It performs no RD005 learner/probe execution, consumes no capability candidate, creates no source freeze, and does not touch RD003/RD004 preserved evidence.

## What is currently bound

The development source contains the preregistered RD005 gate construction, the fixed seed-92505 six-family × three-scale 18-cell construction matrix, retained ordinary pre-capability trace schema, and an independent verifier.

The verifier reconstructs, from retained artifact inputs rather than trusting ready flags alone:

- the fixed 18-cell world/family/scale identity;
- the first qualifying retained ordinary clock;
- latest eligible spikes and deterministic visible targets;
- outcome-blind external return events;
- deterministic ES source rotation;
- E1/ES gate-reachability certificates.

It runs no learner or probe and grants no held-out/formal authority.

## Review findings that keep the line fail-closed

Independent review found two important boundaries that the initial readiness wording understated.

### 1. D1 construction artifact must precede any capability runner

The preregistered fixed-matrix plan requires the canonical D1 construction artifact to be generated, retained, and reviewed **before** a later capability runner is allowed to consume it. Therefore the next executable wrapper, when eventually frozen, must be **construction-only**. It may build/retain the fixed D1 construction artifact and run construction-integrity verification, but it must contain no learner/probe capability path.

A future capability runner is a later stage and must consume an already retained/reviewed D1 artifact identity. Construction and capability must not be collapsed into a single one-shot execution.

### 2. The integrated verifier does not yet independently prove topology provenance

At source head `aaa2e1f...`, the verifier checks the fixed cell/family/scale/world/evidence identity and independently reconstructs gate semantics, but it does not independently regenerate the authoritative topology and initial connection state. A self-consistent retained `topology_sha256` and `connection_rows_sha256` can therefore pass even if the underlying topology/connection payload was fabricated.

That is a source-integrity blocker before D1 can be treated as reviewable construction evidence. A separate fix line now targets authoritative regeneration from the fixed `ScaleStudyConfig(seed=92505)` + canonical world + scale and the fixed pre-training gained connection constructor. Until that fix is merged and reviewed, non-empty verifier inventory must not be used as capability authority.

## Readiness decision

The line may continue through **execution-disabled package/schema work and topology-provenance repair**, but it is not yet suitable for a D1 construction source freeze, D1 construction execution, or any learner/probe capability execution.

The blockers are:

1. **Topology/connection provenance repair.** Independently regenerate canonical topology and initial gained connection state and compare retained digests against that authoritative regeneration.
2. **Complete collision-registry binding.** Bind an authoritative complete consumed/reserved seed and world-identity registry. Repository text search or an arbitrary caller list is insufficient evidence of freshness.
3. **Exact construction source manifest.** Enumerate and SHA-256 pin the construction builder, gate, repaired verifier, inherited world/topology constructors, preregistration/matrix documents, tests, and construction-only wrapper.
4. **Construction-only no-clobber one-shot wrapper.** The first wrapper must create a fresh output identity, refuse overwrite/retry, record exact source/ref/Python metadata, preserve raw D1 output even on failure, and contain no learner/probe path.
5. **D1 retention and review.** Run only the frozen construction-only D1 wrapper, retain its canonical artifact, independently verify topology/gate provenance, and review the exact artifact identity before any capability runner is authored or enabled.
6. **Later capability package separation.** Only after D1 review may a separate development capability runner/package be prepared. Its outcome-blind scoring/result schema must be fixed before capability output is opened.
7. **Final exact-head reviews.** Every prospective freeze must re-fetch the exact candidate head and confirm CI/review against that exact SHA. The user's standing human-review-only waiver can replace a literal reviewer-identity stop, but cannot waive topology provenance, source identity, D1-before-capability ordering, or one-shot integrity.

## Scientific integrity constraints retained

The following remain prohibited:

- rerunning RD003 or RD004 consumed candidates;
- modifying any `freeze/*` or `preserve/*` evidence anchor;
- changing RD005 seed `92505`, fixed 18-cell matrix, return offset, E1/ES definitions, or reachability rules in response to later output;
- treating unreachable cells as successful negatives;
- using construction traces as capability outcomes;
- authoring a capability wrapper that constructs and consumes D1 in the same execution;
- creating a held-out/formal candidate from this development identity;
- issuing any formal execution seal or `STARTED` state.

## Next safe stage

The immediate safe stages are the topology-provenance verifier repair and execution-disabled package/schema preparation. After those are merged, prepare a **construction-only** D1 source manifest and no-clobber one-shot wrapper, then review/freeze that construction source before any D1 run.

No D1 construction execution, learner/probe capability execution, held-out execution, formal execution, seal issuance, or `STARTED` state is authorized by this review.
