# EXPLORATORY / NON_EVIDENTIARY — SUB v0.5 topology config binding cycle 1 result

- mode: `discovery`
- exploratory_target: `V05_TOPOLOGY_DIMENSION_BINDING_DISCOVERY_CYCLE1`
- candidate_pool_id: `CAND-V05-TOPOLOGY-CONFIG-BINDING-01`
- exploration_cycle: `1/3` (Analyst-bounded to stop after this cycle)
- evidentiary_status: `NON_EVIDENTIARY`
- recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`

## Why independent of MAIN

MAIN is on `LOWER_FUNNEL_MAIN_HOLD_PENDING_FRESH_OBJECT` with no active execution object. This check touches only current-main v0.5 public/configuration semantics and a development-only constructor instantiation. It does not continue Temporal batching, Top-k, H7, the rejected stride-11 aliasing candidate, any consumed identity, or any formal/TEST/scoring/preserve/evidence surface.

## Question / reduction question

Do `V05BrainConfig.width`, `height`, and `receptor_rows` bind the actual integrated v0.5 topology, or are they accepted/persisted dimension-like configuration fields whose runtime topology effect is bypassed by explicit `layered_reservoir_topology(seed=...)` injection?

Reduction question: can the discrepancy be dismissed as intentional fixed-topology semantics that are already documented/tested, or does the current public/configuration surface leave an actionable API/configuration mismatch?

## Inputs used

- current stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d` only;
- `src/sparkbrain/v05/brain.py`;
- `src/sparkbrain/v05/topology.py`;
- `src/sparkbrain/v04/brain.py`;
- `src/sparkbrain/v05/__init__.py`;
- `configs/v05_reference.json`;
- current v0.5 tests/evaluation callsites;
- development-only constructor configs `(8,8,1)` and `(12,10,2)` with identical topology seed `41`.

No retained dataset, trained checkpoint, confirmatory/formal TEST input, scorer, preserved raw result, or consumed identity was opened or used.

## Implementation / experiment

The prospective question was bound before the diagnostic. A single exploratory pytest instantiates `IntegratedV05Brain` twice and records the declared v0.5 config, nested v0.4 config, actual field unit IDs/count, receptor IDs/count, reservoir count, and connection count. No production source was modified.

## Observations

Current source exposes `V05BrainConfig` from the public v0.5 package and includes `width`, `height`, and `receptor_rows` in the retained v0.5 reference configuration. `IntegratedV05Brain` copies these values into `V04BrainConfig`, but simultaneously injects `layered_reservoir_topology(seed=self.config.topology_seed)` without passing any of those dimensions. `IntegratedV04Brain` uses an explicitly supplied topology instead of constructing its config-sized grid.

The alternate configuration `(width=12,height=10,receptor_rows=2)` is therefore accepted and retained both by the v0.5 config and nested v0.4 config, while the actual integrated field remains the same default layered topology as `(8,8,1)`: 64 total units = 16 receptors + 48 reservoir units, with identical unit IDs, receptor IDs, and connection count under the same topology seed.

Repository search found no current v0.5 test or integrated callsite that binds these three dimension fields into `layered_reservoir_topology`. Current reference/evaluation paths use the fixed topology defaults. I did not find documentation explicitly stating that these exported dimension fields are intentionally metadata-only or intentionally ignored by the v0.5 integrated topology.

This is not a new scientific mechanism and does not revive the rejected resonant fanout-aliasing candidate. It is a configuration/API-semantics mismatch: accepted dimension-like configuration can disagree with actual runtime geometry.

## Falsifier / reduction boundary

Reduce to `REJECT/NO_ACTION` if a current supported contract is identified that explicitly defines v0.5 topology geometry as fixed and the inherited dimension fields as intentionally non-operative compatibility metadata. Otherwise the mismatch is actionable at Architecture/API correctness level.

A future Architecture study need not run scientific stimuli. It should prospectively define the intended geometry contract and test supported non-default configs/checkpoint round trips against actual topology metadata. It must not use resonant stride-11 behavior as a rescue signal.

## Candidate next research layer

`ARCHITECTURE_STUDY` / API correctness only, subject to fresh Evidence Analyst promotion.

## Scientific / semantic choices still open

- whether `width/height` are intended to parameterize reservoir dimensions, total field dimensions, or be removed/deprecated for v0.5;
- whether `receptor_rows` should map to a receptor count/geometry in the layered topology or be explicitly unsupported;
- checkpoint/backward-compatibility semantics for existing configs that persist these fields;
- whether validation should reject unsupported non-default geometry rather than silently accept it.

No cycle 2 is authorized here. Stop for fresh Analyst review.
