# MAIN history — candidate #35 Architecture R1 cycle 1 relay

- schema_version: `2`
- generation: `MAIN-20260923T175200+0900-RELAY-CAND35-ARCHR1-R95-WAITING-CI`
- execution_mode: `RELAY`
- authority: Evidence Analyst R95 (`EVA-20260923T165919+0900-R95-71C4A8E2`)
- supersedes MAIN generation: `MAIN-20260923T172900+0900-PRIMARY-CAND35-ARCHR1-R95-WAITING-CI`
- canonical object: `CAND-35-QUEUE-FREE-SUBTHRESHOLD-STATE-CAUSAL-PRIMING`
- layer: `ARCHITECTURE_STUDY`
- development phase/revision: `OPEN_DEVELOPMENT / ARCHITECTURE-R1-NONRESULT`
- claim ceiling: `SYSTEM`
- preformal eligible/readiness: `false / NOT_READY`
- hold class/reason: `null / null`
- terminal state: `NONTERMINAL`
- cycle/reassessment: `1 / same prospectively authorized Architecture R1 non-result cycle`
- system-priority exception: `NO_COHERENT_MECHANISM_TARGET`, preserved exactly
- canonical branch/head after repair: `research/main-cand35-queue-free-subthreshold-architecture-r95-cycle1@c640cb3a42faf1f49bee568c1cc167c03fb63646`
- disposition: `WAITING_EXTERNAL`

## Freshness / collision reconciliation

Relay re-fetched the current Evidence Analyst generation, MAIN state/lease, exact candidate #35 research branch, and Fast Forge boundary before mutation. PRIMARY was `WAITING_EXTERNAL`, not `RUNNING`, and remote reconciliation showed no post-handoff foreign mutation of the candidate #35 object. Fast Forge remains noncanonical and excludes candidate #35 canonical work. No same-object ownership collision was present.

Immediately before the research mutation, Evidence Analyst remained materially unchanged at R95 and MAIN remained on the same waiting generation. After the repair, the Analyst generation, MAIN lease, and exact research branch were re-fetched again: R95 remained unchanged, MAIN had not concurrently advanced, and the research branch contained exactly the Relay repair commit as the child of the prior waiting head.

## External CI diagnosis

The previously awaited exact-head generic CI `35837060130` completed `failure` on `58d73aa7c0ad19d0a4e4f84bdbcaaf385e58f751`. Both matrix jobs stopped at Ruff lint before readiness/tests. The only reported defect was:

- `E501 Line too long (103 > 100)` in `tests/test_v05_subthreshold_architecture.py` within `_internal_unit_ids`.

No candidate response, scientific test, PRE_FORMAL action, FORMAL action, scoring, protected evaluation, or result-bearing workflow occurred in that failed CI.

## Repair / change classification

Classification: `SCIENCE_INVARIANT_REPAIR / LINT_ONLY_LINE_WRAPPING`.

Relay changed only formatting of the existing tuple-comprehension helper in `tests/test_v05_subthreshold_architecture.py`, splitting the same expression across lines. The selected units, ordering, filtering, count semantics, test assertions, candidate question, cue/reset/cap meaning, observable, comparator, threshold/tolerance, seed/exclusion policy, intervention, resource/privilege contract, falsifier and success criteria are unchanged.

No scientific contract or response-bearing code was redesigned. No prior result was interpreted to choose this repair.

The exact repaired research head is `c640cb3a42faf1f49bee568c1cc167c03fb63646`.

## New exact-head CI / waiting state

Push of the lint-only repair started generic CI `35839346480` on exact head `c640cb3a42faf1f49bee568c1cc167c03fb63646`. At final observation for this Relay persistence, the run remained `in_progress` with no conclusion. It is non-result-bearing.

Relay therefore stops at `WAITING_EXTERNAL`. Expected next MAIN/Relay action is to re-fetch the latest Evidence Analyst generation, MAIN lease, exact research branch and CI `35839346480`. If the exact-head CI is green and R95 remains materially unchanged, close Architecture R1 implementation readiness and return the non-result construction to Evidence Analyst without executing a candidate response. If CI fails, diagnose the exact failure and continue only if the required repair is clearly science-invariant; otherwise fail closed for fresh Analyst authority.

## Funnel / evidentiary status

The Analyst-owned Funnel fields are preserved exactly:

- `claim_ceiling=SYSTEM`
- `preformal_eligible=false`
- `preformal_readiness=NOT_READY`
- `hold_class=null`
- `hold_reason=null`
- `terminal_state=NONTERMINAL`
- `system_priority_exception=NO_COHERENT_MECHANISM_TARGET`
- `development_phase=OPEN_DEVELOPMENT`
- `development_revision=ARCHITECTURE-R1-NONRESULT`

New scientific result: `false`.

- candidate response observations: `0`
- PRE_FORMAL development evidence: `0`
- FORMAL evidence: `0`
- confirmatory credit: `0`
- official scoring: `false`
- result-bearing workflow dispatched: `false`

This Relay advancement is implementation hygiene only and is not evidence that queue-free subthreshold state causally primes a later weak-cue response.

## Prior-result / hard-floor preservation

Candidate #34 D34-Q002 remains preserved unchanged and repeat/retune/rescore remains forbidden. Official consumed FORMAL identities are unchanged. No FORMAL identity or STARTED marker was created or consumed; no concealed/protected evaluation was accessed; no scientific preserve/evidence/formal/sealed/freeze ref was created or mutated; no historical PASS/FAIL was rewritten; no Forge code or observation was reused.

## Stop reason / next MAIN action

Stop reason: `WAITING_EXTERNAL_EXACT_HEAD_CI_AFTER_SCIENCE_INVARIANT_LINT_REPAIR`.

Next MAIN action: re-fetch Analyst/Main generations, exact candidate #35 branch and CI `35839346480`; if green under unchanged R95, mark Architecture R1 non-result implementation readiness complete and return to Evidence Analyst. Do not execute the candidate response or perform same-object SYSTEM-to-MECHANISM uplift.
