# MAIN history — upstream-generation freshness block

- schema_version: `2`
- generation_id: `MAIN-20260921T231231+0900-PRIMARY-FUNNEL21-BLOCKED-R44-STALEUPSTREAM-8D4C21A7`
- produced_at: `2026-09-21T23:12:31+09:00`
- status: `BLOCKED`
- analyst: `EVA-20260921T220541+0900-R44-7A3C21E8@fca9a4b0adb259b76a518605f611ff79e0c48680`
- superseding control: `CTRL-20260921T230354+0900-R26-8D4C21A7@0e38771af4dacefab079a9389dece4c6a48f1240`
- superseding audit: `AUD-20260921T223000+0900-R5-H5-DEADWORK-5E8C21A4@c65c53c5c6491754248c7f8a7d35fbb4ad5bfb48`
- superseding methodology: `METHCAL-20260921T222227+0900-R45-B7E2C491@ac7afaa0add8af8aebb1be08798d1e3df4d3c8c0`

Control R26 explicitly reports that Analyst R44 has not consumed Control R26, Audit R5, or Methodology R45. MAIN therefore stopped under generation-freshness fail-closed semantics instead of directly translating upstream strategy/audit material into a scientific allocation.

Current-object fields remain null because Analyst R44 has no active canonical candidate. No PRE_FORMAL, FORMAL, Architecture study, successor creation, research mutation, scientific workflow, STARTED creation, preserve, scoring, evidence mutation, or identity consumption occurred.

Fresh repository checks found stable `main=ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; five unchanged authoritative `evidence/*` tags; zero tag-form `formal/*`, `sealed/*`, and `freeze/*`; unchanged H5 STARTED/raw-preserve anchors; PR #148/#149 open, unmerged, mergeable; and SUB R44 still no-target with no ownership collision.

Layer accounting: FORMAL `0`, PRE_FORMAL `0`, MECHANISM Architecture `0`, SYSTEM Architecture `0`, new identity consumption `0`.

Stop reason: `MATERIAL_SUPERSEDING_UPSTREAM_GENERATIONS_NOT_YET_CONSUMED_BY_EVIDENCE_ANALYST_FAIL_CLOSED`.

Next action: wait for a fresh Evidence Analyst generation that consumes Control R26, Audit R5, and Methodology R45, then re-fetch all exact refs before any acquisition or mutation.
