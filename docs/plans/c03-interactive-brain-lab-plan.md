# C03 Interactive Brain Lab Plan

## Objective

Deliver a local-only causal laboratory that exposes real SparkBrain state, deterministic control, intervention forks, synchronized comparison, and exact exports without changing Phase-0 task metrics or the C01 reference contract.

## Architecture

- Add an optional `lab` dependency extra for FastAPI, Uvicorn, and their runtime contracts; keep `[project].dependencies` empty so the CPU reference engine remains dependency-free.
- Bind the server to `127.0.0.1` by default and reject non-loopback hosts in the supported launcher.
- Keep run state in-process and persist exports only under an explicit local artifact root.
- Serve a bundled dependency-free HTML/CSS/JavaScript frontend from the package. Do not use a CDN, hosted font, analytics, remote image, SaaS session, or runtime fetch outside the loopback API.
- Preserve the existing static trace visualizer as the dependency-free fallback and regression oracle.

## Control contract

- A run owns a reference brain, immutable event manifest, current event index, status, trace, parent run ID, and exact intervention patch.
- `step` consumes exactly one external manifest event and records exactly one frame.
- `run` consumes remaining events; `pause` changes control state only; `reset` reconstructs the same seeded parent scenario.
- Event injection validates target, finite strength/time, and event budget before scheduling.
- Interventions always fork from a serialized checkpoint. The parent is never mutated. Supported patches are Spark clamp/ablation, organ suppression, edge-weight edit/ablation, and threshold edit.
- Comparison aligns two trace timelines by frame index and exposes only frames at or before the requested synchronized cursor.

## API and screens

- REST covers create/list/state/graph/trace, start/pause/step/reset, event injection, fork intervention, comparison, export, and import.
- SSE provides frame notifications with bounded sampling; reconnect reads current state and never restarts execution.
- The single-page frontend contains the nine required surfaces: Brain field, Timeline, Belief panel, Workspace, Inspector, Experiment controls, Intervention panel, Comparison, and Export.
- Blind mode removes truth from every API/UI frame. Legends label functional layout, colors, activation sizing, firing, inhibition, Coalition membership, ignition, and unresolved/no-ignition.

## Validation

- Unit/API tests: schema rejection, deterministic pause/step/reset, exact checkpoint fork equivalence, parent preservation, behavior-changing edge ablation, export/import, synchronized comparison, blind-mode truth removal, SSE reconnect non-mutation, and unknown-ID rejection.
- UI/E2E tests: static asset contract, keyboard-accessible controls, text alternatives, visible focus/contrast metadata, canonical CAT to TOY to CAT flow, evidence inspection, and no remote assets.
- Performance tests and a repeatable measurement script: canonical frame payload budget and a synthetic 2,000-Spark/10,000-edge relevant-subset payload. UI frame sampling must not execute or mutate the engine.
- Full gate: local readiness, Ruff, pytest, canonical demo, Phase-0 benchmark, static visualizer, bundle validation, and loopback startup smoke.

## Documentation and artifacts

- Add `docs/BRAIN_LAB.md` for startup, bind address, artifact paths, offline use, UI legend, blind mode, intervention semantics, comparison, performance limits, and static fallback.
- Update `SOFTWARE_ARCHITECTURE.md`, `PROJECT_STATUS.md`, and append a C03 entry to `RESULTS_LEDGER.md`.
- Generate a local performance JSON artifact and retain exact commands/results without scientific claims based on animation.

## Completion boundary

C03 is complete only when all C03 acceptance criteria are exercised by local tests or explicitly documented as a measured limitation. No training UI, anatomical imitation, remote access mode, or scientific inference from visualization is included.
