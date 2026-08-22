# C03 — Interactive Brain Lab

## Goal

Build a live, causal, inspectable visual laboratory for SparkBrain. Users must be able to observe real engine state, pause time, inject evidence, modify selected parameters, intervene on Sparks/connections, compare runs, and export exact traces.

## Prerequisite

C01 trace/state/control contracts accepted. C03 may run in parallel with C02 if it does not modify task metrics.

## Target architecture

- backend: FastAPI, Pydantic schemas, WebSocket/SSE frames;
- frontend: React + TypeScript + Vite;
- graph rendering: choose a maintained SVG/WebGL library after documenting license and scale trade-offs;
- static HTML replay remains supported as a dependency-free fallback.

## Required screens

1. **Brain field** — Sparks grouped by organ, active edges, firing, inhibition/excitation, Coalition membership.
2. **Timeline** — external/internal events, ignition markers, truth/prediction when available.
3. **Belief panel** — competing hypotheses, evidence provenance, contradiction, score components, stability, margin.
4. **Workspace** — slots, broadcasts, listeners, expiry/history.
5. **Inspector** — complete state for selected Spark/edge/Coalition.
6. **Experiment controls** — start/pause/step/reset/seed/speed/event injection.
7. **Intervention panel** — clamp/ablate Spark, edit edge weight, suppress organ, change threshold, then fork run.
8. **Comparison** — synchronized side-by-side traces from two configurations/interventions.
9. **Export** — trace JSON, checkpoint, screenshot/figure data, config, event manifest.

## Scientific UI rules

- displayed values come from trace/control APIs;
- smoothing or normalization is opt-in and labeled;
- layout position is not presented as biological anatomy;
- colors, sizes, and opacity have a visible legend;
- no-ignition and unresolved state are visually distinct from system failure;
- history/future frames must never leak into the current frame;
- interventions create a fork with parent run ID and exact patch;
- truth labels are hidden in a “blind analysis” mode.

## Performance targets

- canonical demo works at 60 FPS on a typical desktop;
- usable interaction with 2,000 Sparks and 10,000 static edges, rendering only active/relevant subsets where needed;
- backpressure or frame sampling must not alter engine execution;
- UI reconnect does not restart or mutate a run.

## Tests

- backend API schema/validation;
- deterministic pause/step behavior;
- checkpoint fork equivalence before intervention;
- UI end-to-end test for canonical scenario;
- visualizer never renders synthetic unseen IDs;
- export/import round trip;
- blind mode prevents truth leakage;
- accessibility: keyboard controls, text alternatives, contrast checks.

## Acceptance criteria

- `docker compose up` or documented two-command startup launches the lab;
- canonical scenario can be reproduced entirely from the UI;
- user can demonstrate CAT→TOY→CAT revision and inspect the exact supporting evidence;
- an edge-ablation fork changes behavior while preserving the parent trace;
- side-by-side comparison remains synchronized;
- all API/E2E tests pass;
- static visualizer remains functional;
- architecture, UI legend, and intervention semantics are documented.

## Non-goals

- aesthetic imitation of anatomical brain regions;
- generative 3D brain art detached from engine state;
- model training UI;
- scientific conclusions based solely on animation.
