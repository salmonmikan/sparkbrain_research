# Evidence Analyst R168 — FLY-0 composed causal replacement exists but fails current-head CI

generation_id: EVA-20260928T231445+0900-R168-FLY0-COMPOSED-CI-FAILURE
generated_at: 2026-09-28T23:14:45+09:00
role: EVIDENCE_ANALYST
mode: READ_ONLY_ADJUDICATION
directive_delta: none
new_scientific_result: false

## Freshness and authority

Human Directive index remains ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d with active-index blob 1ba1e173344f36e14d0e21e6f3e823254e031f7d, identical to durable R167.

Current durable Control authority is append-only R115 at commit 77b03725f1cc91f6f5fcb85c8a4a5c1e6d42751d. Control latest/state caches remain behind at R112, which is pointer debt only; append-only R115 governs.

Prior failed R168 intent EA-R168-20260928T220643JST is absent from the request mailbox and has no durable authority. R167 receipt remains persistence_complete=true.

## Canonical science

Canonical science is unchanged: 35/35 terminal, active 0, scientifically queued 0, consumed FORMAL identities 8. No result-bearing execution is authorized and no scientific object is reopened.

## Integrated Prototype Milestone 1

M1-002 remains the current critical-path build at exact head 2a21d3e879f1db4e81a58273180ad2124e823a5e against main 59fc994b39d0ba02682e972161bb46801592d25b, 1 ahead / 0 behind, with no PR. MAIN R179 remains built=true and bounded_functionally_verified=true; comparatively_supported=false; composition_contribution=NOT_ESTABLISHED; scientifically_novel=false; scientific_credit=0.

Existing exact-head PR / conditional-merge authority is retained. The blocker remains the open P0 PR-create production path, not a bounded-functionality or scientific defect. No additional mandatory review gate is introduced.

## FLY-0 material update

A new noncanonical Forge commit 5541043d53bbcde26fc930cb054a1158fb90a727 adds a composed causal-replacement loop and focused tests on top of durable FLY-0 handoff 8bcb7323df35248e3e3c8b3e6f0eaca3f8d30f63. The new surface puts structured, rewired, random_sparse and reactive variants on one loop while independently cutting Observation and ascending LocalFeedback. This directly targets the previously identified gap between bottom-up causal-cut testing and the matched replacement ladder.

However current-head CI run 36434348027 is not clean. Python 3.11 completed with failure. Five focused failures are in tests/test_forge_fly0_composed_causal_replacement.py: intact target/replay fails for rewired and random_sparse; feedback-cut first-step expectation fails for rewired and random_sparse; the aggregate report therefore fails its all-variants target assertion. Python 3.13 is still in progress at adjudication time.

This is a concrete ordinary engineering defect in the composed Forge path. It does not affect M1-002, canonical science, or prior terminal scientific results.

## FLY-0 disposition

SB003 remains UNALLOCATED.

The composed-path structural gap is narrower because the intended combined diagnostic now exists, but it has not passed its own current-head acceptance. Before Analyst may treat this exact composed asset as SYSTEM_BUILD input, require a repaired exact head with:
- structured / rewired / random_sparse / reactive all reaching the bounded target under the same composed loop;
- exact checkpoint/replay across all four variants;
- independent Observation cut and ascending-feedback cut remaining causal/fail-closed across all four variants;
- bounded event and delay contracts preserved;
- exact-current-head CI green on supported Python lanes.

Strict native internal activity/resource commensurability remains required only for strong resource/efficiency/topology-superiority claims, not for ordinary NON_EVIDENTIARY integration. The CPython common-work counter remains SOURCE_ONLY and is not an SB003 engineering gate.

Ordinary reactive success remains a reduction comparator; no fly-like topology necessity/superiority, biological fidelity, compute/energy efficiency, composition contribution, external validity, novelty or scientific credit is established.

## Rolling SYSTEM_BUILD / next actions

M1-002 remains GO under its existing exact-head conditional-merge authority, subject to fresh-state checks and repository PR requirements. The P0 mutation failure is operational and should not be converted into a science gate.

Parallel FLY-0 work is GO only for noncanonical repair/verification of commit 5541043d53bbcde26fc930cb054a1158fb90a727 or a clearly superseding Forge head. SB003 allocation is STOP until that composed acceptance is clean and Milestone 1 sequencing/collision is rechecked.

Next bounded milestones:
1. recover M1-002 PR creation, merge only the exact authorized head after required checks, and verify post-merge acceptance;
2. repair and re-verify the FLY-0 composed four-variant causal-replacement path;
3. after M1-002 post-merge acceptance and a green exact FLY-0 composed head, re-evaluate BUILD-SB-003-FLYLIKE-SENSORIMOTOR-PILOT for a bounded NON_EVIDENTIARY rolling contract;
4. any scientific topology claim requires a fresh prospective scientific object with zero inherited BUILD/Forge credit.

## P0

INC-GITHUB-MUTATION-RECURRENCE-20260928-001 remains OPEN. Repository-wide outage is not supported; PR-create is the strongest recurring failure surface while other mutation paths are intermittent. Root cause remains UNKNOWN.

No scheduler definition/state change is authorized or performed by Evidence Analyst.
