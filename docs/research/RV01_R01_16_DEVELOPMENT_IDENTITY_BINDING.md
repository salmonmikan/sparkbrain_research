# RV01 R01-16 development identity binding

Date: 2026-09-12  
Status: **PROSPECTIVE / DEVELOPMENT-ONLY / EXECUTION DISABLED**

This record advances `rv01-r01-16-propagation-factorization-v1` only through a fresh, deterministic development namespace. It does not run training or probes, does not inspect capability output, does not create or consume a held-out/formal candidate, and does not modify R01-15 evidence.

## Parent scientific boundary

The binding is subordinate to:

- `RV01_R01_16_PROPAGATION_FACTORIZATION_PREREGISTRATION.md`;
- `RV01_R01_16_PREREGISTRATION_AMENDMENT_001.md`.

The amendment's causal-reachability certificate and exact sequence decision rule remain mandatory. A merely structurally changed but causally unreachable connection cannot be counted as a behavioral negative.

## Fresh namespace

The prospective development seeds are fixed as:

```text
141700
141701
141702
141703
141704
```

World-generation salt:

```text
rv01-r01-16-fresh-world-grid-v1
```

The grid is the complete Cartesian product of the inherited five `InterferenceFamily` geometries and these five seeds at the inherited scale of 96 anonymous units: **25 development identities**. Family omission or seed substitution is prohibited after capability opens.

R01-15 namespaces remain excluded:

```text
consumed development: 141500..141504
reserved held-out:    141600..141609
```

Repository code searches performed before this binding found no exact occurrences of `141700`, `141701`, `141702`, `141703`, or `141704` in the currently indexed repository source. That textual observation is not treated as a complete scientific collision proof. The source contract therefore requires a future capability-enabling layer to call `assert_no_seed_collisions()` with the complete retained consumed/reserved seed registry and fail closed on any collision before world construction or capability.

## Bound source contract

`src/sparkbrain/research/rv01_r01_16_identity.py` now fixes:

- protocol identity;
- five development seeds;
- fresh world salt;
- 96-unit scale;
- complete ordered family × seed identity grid;
- deterministic identity hashes;
- immediate R01-15 exclusion ranges;
- an explicit fail-closed collision check against a caller-supplied complete retained registry;
- `formal_authority = false` and `held_out_authority = false`.

The module intentionally contains no Field construction, learner, probe runner, scorer, source freeze, workflow, execution seal, or formal path.

## What remains before development capability

Before any R01-16 development probe may execute, a separately reviewed layer must:

1. bind the exact deterministic family geometry construction for all 25 identities without changing this seed/salt grid;
2. retain and hash the complete consumed/reserved seed registry used by the collision check;
3. construct the pre/post training connection inventories and common checkpoint without opening probe output;
4. reconstruct the amendment-001 reachability certificate for every planned world/probe cell;
5. retain queue-integrity evidence and fail closed on stale propagation arrivals;
6. establish at least two independently generated causally reachable worlds for any factor that will receive a causal classification;
7. bind the complete fixed development matrix and raw artifact schema;
8. pass CI and independent technical/semantic review before a one-shot development source freeze is considered.

Development execution remains closed by this record. Held-out/formal execution remains separately prohibited and would require a fresh disjoint candidate plus candidate-specific authorization.
