# Utility Autonomous Task Start

- schema_version: 2
- assignment_mode: AUTONOMOUS_IDLE
- autonomous_task_id: `AUTOUTIL-20260922T0624+0900-EQUIV-SCHEMA-91C4B6E2`
- status: `IN_PROGRESS`
- evidentiary_status: `NON_EVIDENTIARY`
- scientific_authority: `NONE`
- max_runs: `1`

## Objective

Characterize the outcome-independent equivalence-verifier / exact-binding / matched-resource schema and tooling that exists on stable main, identify machine-checkable coverage and prospective gaps, and return a bounded reusable tooling recommendation without touching any candidate, outcome, or scientific workflow.

## Trigger / source

- Control-owned Utility pointer is clean schema-v2 `IDLE` with `active_assignment_id: null`.
- No fresh Utility request was selected.
- Evidence Analyst R54 reports no active or queued Architecture object and no Utility request.
- Control R29 explicitly identifies a generic outcome-independent equivalence-verifier schema/tooling investigation as potentially useful bounded NON_EVIDENTIARY Utility work, with candidate #32 repair/reopening forbidden.

## Fresh ownership / source refs before start

- Utility assignment pointer: `IDLE@6fe8c6da7192a3021eea9e2c4a94b1a1251e6da7`
- Evidence Analyst: `EVA-20260922T060636+0900-R54-4E7C21A9`
- Control: `CTRL-20260922T045653+0900-R29-7C4E91B2@582a8b32ac8336b84c0aaa372c83258f7962fba5`
- Stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- MAIN/SUB ownership: Analyst R54 records MAIN R53 and SUB R53 completed intentional-idle/no-target runs; current allocation has no active or queued object.
- Relay ownership: Control R29 records no active MAIN continuation authority and no Relay ownership collision.

## Allowed actions

Read stable-main repository contracts, verifier/tooling code, tests, workflow definitions, and documentation; map existing machine-verifiable equivalence/binding/resource coverage; report bounded prospective schema/tooling recommendations.

## Forbidden actions

No candidate #32 repair or reopening; no candidate creation/reclassification; no PRE_FORMAL/FORMAL work; no scientific/evidence workflow dispatch; no protected/consumed identity access as task target; no immutable/formal/evidence/control/preserve mutation; no scheduler mutation; no research branch/PR merge; no hidden MAIN dependency.

## Stop condition

Stop after one bounded read-only repository characterization and append-only Utility result. If the task would require scientific outcome access, active-owner work, or candidate-specific repair, stop without proceeding.

## Funnel v2.1

No research candidate is touched; preservation fields are not applicable.
