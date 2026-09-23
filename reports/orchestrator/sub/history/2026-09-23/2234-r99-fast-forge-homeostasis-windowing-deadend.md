# FAST FORGE history — v0.5 homeostasis windowing / elapsed-time invariance probe

- schema_version: `2`
- generation_id: `FORGE-20260923T223403+0900-V05-HOMEOSTASIS-WINDOWING-R99`
- produced_at: `2026-09-23T22:34:03+09:00`
- worker_role: `FAST_FORGE`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- overall_status: `FORGE_DEAD_END`
- selection_outcome: `BOUNDED_PROTOTYPE_COMPLETED`

## Freshness / independence

Re-fetched stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`, Evidence Analyst `EVA-20260923T210010+0900-R99-6F2B8C14@59dbcdc2e3541e78a64f64e16fa0be5ef38efc26`, latest MAIN/Relay `MAIN-20260923T215545+0900-RELAY-CAND35-PRESERVATION-R99-COMPLETED`, Literature R39, Methodology R91, Utility R99, and prior Forge history/state before selecting work.

MAIN owns Candidate #35 and its post-preservation review / response boundary; H7 remains the FORMAL-integrity family. Literature R39's reachable-state/off-manifold successor surface is therefore excluded. Candidate #34 terminal route work, prior Forge Assembly/receptor/action/prediction/concept probes, and protected/consumed identities were also excluded.

Selected target is a separate stable-main implementation surface: v0.5 `HomeostaticController` time/window semantics. No research or Forge branch was required because exact-source read-only arithmetic was sufficient.

## Forge object

### Question

Does the v0.5 homeostatic threshold state represent elapsed physical recovery time, or does it depend on how the same elapsed duration is segmented into `process_episode` observation windows?

### Why now

The current MAIN work is confined to Candidate #35 non-result preservation/review. Stable v0.5 homeostasis remains independently inspectable, is close to persistent-state/endogenous-recovery theory surfaces, and has not appeared in prior FAST FORGE history. The source exposes both `time_ms` and a per-window rate controller, making elapsed-time invariance a bounded falsifiable question.

### Source facts

`src/sparkbrain/v05/homeostasis.py` updates every unit once per `observe()` call. With no spikes for a never-active unit, `rate_ema` stays `0`, so each observation applies

`delta = 0.004 * (0 - 0.35) = -0.0014`

to `base_threshold`, clamped to `[0.35, 2.8]`. The supplied `time_ms` is only copied into the returned snapshot; it does not scale the EMA or threshold update.

`src/sparkbrain/v05/brain.py` calls `homeostasis.observe(...)` once per `process_episode(...)` when `learn_field=true`. `src/sparkbrain/v04/brain.py` advances an empty episode by `settle_ms`. The default v0.5 reservoir threshold is `0.76`.

### Prototype 1 — equal elapsed time, different episode segmentation

Read-only exact-equation synthetic comparison from a fresh no-pending-event state and a never-spiking reservoir unit:

- one empty episode with `settle_ms=9376 ms`: one homeostasis update, threshold `0.7600 -> 0.7586`;
- 293 empty episodes with `settle_ms=32 ms`: same total physical elapsed time `293*32 = 9376 ms`, but 293 homeostasis updates, threshold reaches the clamp floor `0.35`.

Thus the homeostatic state is not invariant to episode segmentation at fixed physical elapsed time.

### Prototype 2 — timestamp non-causality inside the controller

Because `time_ms` is not used in the update equation, repeated calls at the same supplied timestamp would still repeatedly modify threshold state. Conversely, a single call at a much later timestamp still performs only one controller step. This isolates the effect to call/window count rather than elapsed-time integration.

### Observation

The difference is real at the implementation level but completely expected from the declared per-window controller (`target_spikes_per_window`). It does not expose a new endogenous-memory mechanism. It says that any apparent slow recovery or sensitization attributed to this controller must be interpreted in episode/window units unless a fixed-duration window contract is imposed.

### Strongest ordinary reduction

Ordinary discrete-time homeostatic control / API segmentation effect. The controller is a per-observation EMA plus bounded threshold integrator, not a continuous-time state estimator.

### Disposition

`FORGE_DEAD_END` — ordinary timing/API semantics fully explain the effect. No Evidence Analyst promotion proposal, no Utility request, no code branch, no repository science mutation.

## MAIN collision / hard floor

Collision check: PASS. Explicitly avoided Candidate #35 scientific source, implementation branch, response helper, preservation wrapper, reachable-state successor surface, H7 runtime/scorer/preserver/formal path, Candidate #34 terminal object, PF-R1, and all consumed/frozen/evidence/formal/sealed/freeze/preserve identities.

Hard-floor actions: none. No PRE_FORMAL/FORMAL identity, STARTED, official TEST/scoring, protected/held-out access, candidate response generation/read, consumed-identity rerun/retune/rescore, scientific preserve/evidence mutation, workflow dispatch, research merge, or Forge branch creation.

## Metrics after this run

- runs: `11`
- prototypes attempted: `14`
- dead ends: `11`
- interesting retained: `0`
- promotion proposals: `0`
- later admissions: `0`
- duplicate/rescue rejects: `9`
- ownership collisions: `0`
- ordinary-reduction rejects: `11`
- idea-to-observation latency: `SAME_RUN`
