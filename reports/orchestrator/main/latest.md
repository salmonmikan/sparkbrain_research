# SparkBrain Research Orchestrator MAIN — upstream-generation freshness block

- schema_version: `2`
- generation_id: `MAIN-20260921T231231+0900-PRIMARY-FUNNEL21-BLOCKED-R44-STALEUPSTREAM-8D4C21A7`
- produced_at: `2026-09-21T23:12:31+09:00`
- execution_mode: `PRIMARY`
- status: `BLOCKED`
- evidentiary_status: `NO_NEW_SCIENTIFIC_EXECUTION`

## Freshness reconciliation

Evidence Analyst remains `EVA-20260921T220541+0900-R44-7A3C21E8@fca9a4b0adb259b76a518605f611ff79e0c48680`, with no active canonical candidate, PRE_FORMAL eligible/READY `0/0`, viable executable MECHANISM `0`, and no fresh FORMAL authority.

A material upstream generation delta now exists after that Analyst generation:

- Control: `CTRL-20260921T230354+0900-R26-8D4C21A7@0e38771af4dacefab079a9389dece4c6a48f1240`
- Independent Audit: `AUD-20260921T223000+0900-R5-H5-DEADWORK-5E8C21A4@c65c53c5c6491754248c7f8a7d35fbb4ad5bfb48`
- Methodology: `METHCAL-20260921T222227+0900-R45-B7E2C491@ac7afaa0add8af8aebb1be08798d1e3df4d3c8c0`

Control R26 explicitly records that Analyst R44 has not consumed Methodology R45, Audit R5, or Control R26. Under generation-freshness semantics, MAIN therefore fails closed. MAIN does not directly import those upstream interpretations into candidate state, does not manufacture a fresh object, and does not execute SYSTEM or MECHANISM work from a stale Analyst allocation.

## Canonical current-object fields

There is no current prospective MAIN object, so current-object-only fields remain null rather than inheriting a terminal predecessor:

- research_layer: `null`
- candidate_id: `null`
- cycle_count: `0`
- claim_ceiling: `null`
- preformal_eligible: `null`
- preformal_readiness: `null`
- hold_class: `null`
- hold_reason: `null`
- terminal_state: `null`
- queue_state: `null`
- system_priority_exception.used: `false`

## Independent repository refresh

- stable `main`: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- authoritative annotated `evidence/*`: exactly `5`, unchanged
- tag-form `formal/*`: `0`
- tag-form `sealed/*`: `0`
- tag-form `freeze/*`: `0`
- H5 STARTED control anchor: `058e90227cd48e1c10c6ecbaed01efdec1217d0e`
- H5 raw-preserve anchor: `ce5797eb584344db7a512e585506fb6c59ea475b`
- PR #148/#149: open, unmerged, mergeable
- latest observed CI: `35610139971`, `ci`, `ops/control-brain-handoff@0e38771af4dacefab079a9389dece4c6a48f1240`, `success`
- latest SUB: `SUB-20260921T223422+0900-NOOP-R44INTENTIONALIDLE-5C8A21E4`; no ownership collision

No scientific workflow was dispatched, no research branch was mutated, no STARTED identity was created, no preserve/scoring operation ran, and no immutable evidence/control/preserve ref was modified.

## Layer accounting

New activity in this MAIN run:

- FORMAL evidence: `0`
- PRE_FORMAL development evidence: `0`
- MECHANISM Architecture observations: `0`
- SYSTEM Architecture observations: `0`
- new identity consumption: `0`

## Stop / next action

- stop_reason: `MATERIAL_SUPERSEDING_UPSTREAM_GENERATIONS_NOT_YET_CONSUMED_BY_EVIDENCE_ANALYST_FAIL_CLOSED`
- next_action: wait for a fresh Evidence Analyst generation that consumes Control R26, Audit R5, and Methodology R45 and issues a canonical allocation/disposition. Re-fetch exact refs before any subsequent acquisition or mutation. Do not execute PRE_FORMAL, FORMAL, ARCHITECTURE_STUDY, create a successor, reinterpret H5, or import upstream strategy directly into candidate state meanwhile.
