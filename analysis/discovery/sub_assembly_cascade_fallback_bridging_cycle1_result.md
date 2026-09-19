# EXPLORATORY / NON_EVIDENTIARY — SUB assembly cascade-fallback bridging cycle 1 result

- mode: `discovery`
- exploratory_target: `ASSEMBLY_CASCADE_FALLBACK_BRIDGING_DISCOVERY_CYCLE1`
- candidate_pool_id: `NONE_SELF_SELECTED`
- exploration_cycle: `1/3`
- evidentiary_status: `NON_EVIDENTIARY`
- recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`

## Why independent of MAIN

Fresh Evidence Analyst authority `6e37598f6c92dbe6b6a88d6083db93bd0f022b10` assigns MAIN to `CAND-V05-UNIT-SUPPRESSION-TRANSIENT-SEMANTICS-01` static contract characterization. This Discovery was bound from stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d` and touched only v0.5 assembly-pattern extraction. It did not inspect or continue MAIN's suppression object, replay the prior suppression diagnostic, continue v0.5 config binding / Temporal / Top-k / H7, or access formal/TEST/scoring/identity/preserve/evidence surfaces.

## Question / reduction question

Question: when one episode contains multiple temporally separated cascades, each with only one eligible non-receptor spike after receptor exclusion, does `patterns_from_step(...)` synthesize one fallback `ActivityPattern` spanning those distinct cascades even though no individual cascade can form a pattern?

Reduction question: if so, is the observation fully explained by the current fallback control flow, or is an additional memory/assembly mechanism needed?

## Inputs used

- stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d` only;
- `src/sparkbrain/v05/assemblies.py@a0a8c41e21db68cafc08ace8dac50b7a56607a52`;
- `src/sparkbrain/v05/brain.py@652552f8dc6a53a68e441f593e9bfd82cebb9f7c` only to verify the extractor is assembly-facing;
- synthetic `CascadeEvent` / `SpikeEvent` objects only.

No repository dataset, trained checkpoint, retained/confirmatory/held-out TEST input, formal raw result, official scorer, consumed identity, or MAIN Architecture outcome artifact was opened or used.

## Implementation / experiment performed

The prospectively fixed diagnostic used two explicit cascades separated by 20 ms. Each cascade contained one receptor spike (`unit 0`) plus one reservoir spike (`unit 101` at 1 ms, `unit 102` at 21 ms). Calling `patterns_from_step(..., excluded_unit_ids=(0,))` therefore leaves one eligible internal spike per cascade, below `pattern_from_spikes`' two-spike minimum for each cascade independently.

A control adds a second eligible internal spike to the first cascade so that cascade-specific extraction succeeds. A small assembly-facing check feeds the synthetic fallback pattern through `TemporalAssemblyMemory(mature_episodes=3)` across three distinct synthetic episode IDs.

Diagnostic commit `828a8090c748be1f2ea61e037964f26b2f3bc4c6` passed ordinary CI run `35465122000` on Python 3.11 and 3.13, including lint, local readiness, tests, and bundle validation. CI has no evidentiary role.

## Observations

With one eligible internal spike in each of the two distinct cascades, cascade-local extraction yields no pattern. Because the `patterns` list is then empty, the current implementation falls back to `pattern_from_spikes(spike_rows, ...)` over **all** eligible internal spikes in the step. The diagnostic therefore produces exactly one pattern with:

- `source_cascade_id = None`;
- `ordered_units = (101, 102)`;
- `unit_ids = (101, 102)`;
- `start_ms = 1.0` and `end_ms = 21.0`.

Thus the fallback pattern spans both explicitly separate cascade windows. When the first cascade is given two eligible internal spikes, a cascade-specific pattern is produced and the cross-cascade fallback is not invoked.

The assembly-facing check confirms this is not merely provenance/hash bookkeeping: the bridged fallback is a normal `ActivityPattern` accepted by `TemporalAssemblyMemory`, and three repeated synthetic episodes mature the corresponding candidate at `episode_count = 3`. `IntegratedV05Brain.process_episode()` likewise forwards every returned pattern above `min_pattern_spikes` into `assemblies.observe(...)`.

The immediate mechanism is completely reduced to current extractor control flow; no new memory mechanism is needed. The research-relevant question is instead segmentation semantics: a fallback intended to recover an episode-level internal pattern can erase explicit cascade boundaries exactly when all cascade-local internal responses are individually sparse.

## What would falsify or reduce it

Reduce to `REJECT/ENGINEERING_NOTE_ONLY` if the supported v0.5 contract explicitly defines fallback patterns as episode-level composites that are allowed to bridge distinct cascades, and a fresh DEV-only comparison shows that preserving cascade boundaries does not materially change assembly candidate formation or downstream prediction/action observables.

Also reduce if current supported runtime states cannot actually produce two or more distinct cascades with fewer than two eligible reservoir spikes each after receptor exclusion.

## Candidate next research layer

`ARCHITECTURE_STUDY_ASSEMBLY_SEGMENTATION_SEMANTICS`, subject to fresh Evidence Analyst promotion only.

A fresh prospective Architecture study should bind a small DEV-only family containing matched episodes where total internal spikes are identical but segmentation differs: (a) multiple sparse cascades, (b) one cascade with the same internal spike sequence, and (c) a boundary-preserving comparator that emits no cross-cascade fallback. Fix candidate-count/maturation and one downstream prediction/action observable before execution.

## Scientific / semantic choices still open

- whether an `ActivityPattern` is intended to be cascade-local or may be episode-global when cascade-local extraction is sparse;
- whether `source_cascade_id=None` is sufficient to distinguish fallback composites from ordinary cascade-derived patterns before memory formation;
- whether the extractor should preserve segmentation, emit multiple partials, or deliberately define an episode-level composite fallback;
- whether downstream behavior differs enough to justify architecture work rather than documentation only.

No cycle 2 is authorized or attempted here. Any continuation must be freshly specified prospectively by Evidence Analyst; this exploratory result cannot be relabeled as formal evidence.