# Utility Autonomous Result — Workflow Trigger / Write Isolation

- schema_version: 2
- assignment_mode: `AUTONOMOUS_IDLE`
- autonomous_task_id: `AUTOUTIL-20260922T0724+0900-WORKFLOW-TRIGGER-ISOLATION-6C3A91D7`
- status: `COMPLETED`
- run_count: 1
- max_runs: 1
- evidentiary_status: `NON_EVIDENTIARY`
- scientific_authority: `NONE`
- classification: `LEGACY_PUSH_TRIGGERED_WRITE_CAPABLE_BRIDGES_SELF_DISARMED_BUT_TRIGGER_ISOLATION_GAP_CONFIRMED`

## Scope

Static, read-only characterization of GitHub Actions trigger and write-capability isolation at stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. No workflow was dispatched. No candidate, result, scorer, protected outcome, or scientific identity was used as a task target. Historical CX01 workflow definitions and existence of their durable no-clobber anchors were inspected only as generic tooling/control-flow examples.

## Fresh authority / ownership check before terminal persistence

- assignment/current: clean schema-v2 `IDLE`, `active_assignment_id: null`, blob `6fe8c6da7192a3021eea9e2c4a94b1a1251e6da7`
- Evidence Analyst: `EVA-20260922T065809+0900-R55-5A8C21F7@11e84b37dd8739c38f538f1231aab7234356c5d0`
- Control: `CTRL-20260922T065500+0900-R30-6F4C21A8@fc5297050c93bb67a9b69aae24179ce7d8888c15`
- MAIN/SUB: R54 terminal intentional idle / no-target; no active or queued Architecture allocation
- Relay: no separate durable continuation authority
- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- material supersession: false
- ownership collision: false

## Static workflow map

Stable main contains seven workflows.

| Workflow | Trigger | Effective capability | Static isolation assessment |
|---|---|---|---|
| `ci.yml` | all push + pull_request | test/lint/read-only checkout; no explicit write permission | Broad trigger but non-mutating. No scientific launch/preserve capability. |
| `create-authoritative-tag.yml` | `workflow_dispatch` only | `contents: write`, annotated authoritative tags | Strong trigger isolation: explicit manual dispatch, exact 40-char target SHA, namespace validation, no-force/no-replace, remote peeled-SHA verification, per-tag concurrency. |
| `cx01-formal-one-way.yml` | `workflow_dispatch` only | `contents: read`; default-branch job intentionally exits 1 | Strong default-branch fail-closed registration guard. Actual formal implementation must live at frozen source revision and match the requested SHA. |
| `cx01-dispatch-probe-target.yml` | `workflow_dispatch` only | read-only harmless probe | Isolated target. |
| `cx01-dispatch-capability-probe.yml` | push to `main` when either probe workflow file changes | `actions: write`, dispatches harmless target | Operational trigger coupling remains: workflow-definition edits automatically exercise Actions dispatch capability. Harmless target, but this is not least-trigger design. |
| `cx01-candidate-002-launch-bridge.yml` | push to `main` when this workflow file changes | `actions: write` + `contents: write`; can create control/STARTED branch and dispatch formal workflow | Material legacy trigger-isolation gap. Strong internal exact-binding and no-clobber guards exist, but a workflow-definition edit is itself an automatic attempt to enter a one-way launch path. |
| `cx01-candidate-002-preserve-evidence.yml` | push to `main` when this workflow file changes | `actions: read` + `contents: write`; can create preservation branch | Material legacy trigger-isolation gap. Strong fixed-run/artifact/hash checks and no-clobber preservation-branch guard exist, but a workflow-definition edit automatically invokes a write-capable evidence-preservation path. |

## Current fail-closed state of the legacy bridges

The durable control anchor `control/cx01-candidate-002-started-20260913` exists at `8216d41a57e6933443d38dfc8d93f9188e423d0c`. Therefore the launch bridge's explicit branch-absence precondition is currently false and a later accidental trigger should stop before creating a second STARTED state or dispatching the formal workflow.

The durable preservation anchor `preserve/cx01-candidate-002-formal-34742073336` exists at `6d45928827209cd763a2879494d85838df38b96f`. Therefore the preservation workflow's branch-absence precondition is currently false and a later accidental trigger should stop rather than move/recreate that evidence anchor.

These guards materially reduce present replay risk. They do not remove the structural coupling between ordinary main workflow-file changes and write-capable / dispatch-capable jobs.

## Finding

The repository has **good operation-level fail-closed controls but incomplete trigger-level separation**. The strongest reusable patterns are already present: manual `workflow_dispatch` for authoritative tag creation, exact immutable identity checks, no-force/no-clobber anchors, and a default-branch formal registration workflow that deliberately cannot execute formal capability.

The reusable gap is narrower: there is no repository-wide policy/linter preventing a workflow with `push` triggers from simultaneously holding `actions: write` or `contents: write` and entering control/preserve/formal/evidence paths. Three current files demonstrate the shape: the harmless dispatch-capability probe plus the two legacy CX01 launch/preserve bridges. The two scientific-history bridges are currently self-disarmed by durable anchors, but their trigger form remains structurally weaker than the newer manual-dispatch/fail-closed patterns.

## Prospective reusable hardening direction

A candidate-agnostic static workflow policy could fail CI when a workflow combines automatic `push`/`pull_request` triggers with elevated `actions: write` / `contents: write` **and** performs workflow dispatch, authoritative ref creation, or writes under control/preserve/formal/evidence semantics, unless an explicit narrowly reviewed exception is present. This can be implemented as ordinary tooling and should carry no Funnel or scientific authority.

Any later edit that retires or changes the legacy bridges should itself be separately reviewed for event semantics; this Utility run does not mutate those workflows.

## Funnel v2.1 preservation

No current research candidate was targeted or modified. No Funnel typing/readiness field was interpreted or changed. Historical workflow definitions were inspected only as tooling artifacts. Therefore the required candidate-field preservation record is `NOT_APPLICABLE_NO_CURRENT_RESEARCH_CANDIDATE_TOUCHED`.

## Integrity checks

- workflow dispatch: false
- scheduler mutation: false
- scheduler-registry mutation: false
- scientific workflow / experiment: false
- research/main/evidence/control/preserve mutation: false
- consumed/protected identity used as autonomous task target: false
- candidate typing/readiness mutation: false
- PR merge: false
- development tooling branch created: false
- hidden MAIN dependency created: false

## Stop / follow-up

Stop reason: `BOUNDED_STATIC_WORKFLOW_TRIGGER_ISOLATION_CHARACTERIZATION_COMPLETE_MAX_RUNS_1`.

No follow-up request is appended in this run. Control already carries generic integrity/tooling hardening as prospective programme work. If implementation is later desired, a fresh bounded authority should create an isolated candidate-agnostic workflow-policy checker; it should not modify or exercise historical result-bearing workflows as part of validation.
