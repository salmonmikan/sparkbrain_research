# Utility Autonomous Task Start

- schema_version: `2`
- assignment_mode: `AUTONOMOUS_IDLE`
- autonomous_task_id: `AUTOUTIL-20260922T0824+0900-EQUIV-CERT-PROTOTYPE-A42D7C19`
- status: `RUNNING`
- run_count: `1`
- max_runs: `1`
- evidentiary_status: `NON_EVIDENTIARY`
- scientific_authority: `NONE`

## Objective

Build and locally validate at most one isolated, candidate-agnostic equivalence-certificate verifier prototype that combines exact identity binding, privilege/resource-envelope equality, independent-producer attestation, and ordered semantic-stream/checkpoint comparison into a fail-closed tooling contract. The prototype may return only contract/tooling verdicts and has no candidate, Funnel, PRE_FORMAL, FORMAL, or scientific-claim authority.

## Trigger / source

Control R30 explicitly identified an isolated candidate-independent equivalence-certificate/tooling prototype as a legitimate Utility direction, provided it remains bounded, NON_EVIDENTIARY, independent, and does not become a hidden MAIN dependency. Evidence Analyst R56 reports Architecture active/queued `0/0`, PRE_FORMAL eligible/READY `0/0`, no active scientific target, and no Utility request.

## Ownership / freshness checks

- Control-owned assignment pointer: clean schema-v2 `IDLE`; `active_assignment_id: null`; blob `6fe8c6da7192a3021eea9e2c4a94b1a1251e6da7`.
- Evidence Analyst: `EVA-20260922T075818+0900-R56-8B3D21F6`; no active/queued Architecture object and no Utility request.
- MAIN: R55 intentional no-target idle per Analyst R56 / SUB R55 reconciliation.
- SUB: `SUB-20260922T073500+0900-NOOP-R55INTENTIONALIDLE-5A8C21F7`; no target, no successor, no Utility request.
- Relay: no separate fresh Relay-owned scientific object or continuation authority surfaced by the current Analyst/Control ownership view.
- Control: `CTRL-20260922T065500+0900-R30-6F4C21A8`.
- authoritative stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`.
- collision found: `false`.
- main-critical dependency: `false`.

## Allowed actions

- Independently re-read stable-main implementation/test primitives relevant to exact binding and equivalence checking.
- Create one isolated Utility-owned development branch from the exact stable-main SHA.
- Add a small pure-data verifier prototype and synthetic unit tests only.
- Run local, outcome-independent tooling tests against synthetic fixtures.
- Persist Utility-owned state/result metadata.

## Forbidden actions

No candidate selection/reinterpretation; no Funnel typing/readiness changes; no PRE_FORMAL/FORMAL action; no scientific workflow dispatch; no consumed/protected identity target; no held-out/evaluator/target data; no research frontier/main/evidence/control/preserve/freeze/sealed/formal mutation; no scheduler mutation; no research PR merge; no scientific result interpretation.

## Stop condition

Stop after one bounded prototype/test pass, or immediately on authority/ownership supersession, collision, dependency on scientific outcomes, or need to touch protected identities/artifacts. Do not self-extend.
