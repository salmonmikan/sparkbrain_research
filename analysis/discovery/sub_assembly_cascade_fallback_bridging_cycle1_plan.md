# EXPLORATORY / NON_EVIDENTIARY — SUB assembly cascade-fallback bridging cycle 1 plan

- mode: `discovery`
- exploratory_target: `ASSEMBLY_CASCADE_FALLBACK_BRIDGING_DISCOVERY_CYCLE1`
- candidate_pool_id: `NONE_SELF_SELECTED`
- exploration_cycle: `1/3`
- evidentiary_status: `NON_EVIDENTIARY`
- stable_main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`

## Why independent of MAIN

Fresh Evidence Analyst authority `6e37598f6c92dbe6b6a88d6083db93bd0f022b10` assigns MAIN to `CAND-V05-UNIT-SUPPRESSION-TRANSIENT-SEMANTICS-01` static contract characterization. This Discovery touches only v0.5 assembly-pattern extraction at the cascade/fallback boundary. It must not inspect or continue MAIN's suppression object, replay the prior suppression pulse diagnostic, continue v0.5 config binding / Temporal / Top-k / H7, or access formal/TEST/scoring/identity/preserve/evidence surfaces.

## Prospectively fixed question

When one episode contains multiple temporally separated cascades, each with only one non-receptor/internal spike after receptor exclusion, does `patterns_from_step(...)` synthesize one fallback `ActivityPattern` spanning spikes from different cascades even though no individual cascade contains enough internal spikes to form a pattern?

Reduction question: if observed, is the effect completely explained by the current fallback control flow (`if not patterns: pattern_from_spikes(all_internal_spikes)`), or is an additional assembly/memory mechanism required?

## Fixed synthetic diagnostic

Use two explicit `CascadeEvent` objects separated by 20 ms. Each cascade contains exactly one receptor spike and one reservoir spike; call `patterns_from_step(..., excluded_unit_ids=(0,))`, so each cascade contributes only one eligible internal spike and therefore cannot individually produce an `ActivityPattern` (minimum two spikes).

Fixed reservoir spikes: unit 101 at 1.0 ms and unit 102 at 21.0 ms. Fixed receptor spikes: unit 0 at 0.0 ms and 20.0 ms. The diagnostic records whether the function emits a fallback pattern, whether its `source_cascade_id` is `None`, whether it contains both reservoir units, and whether its time span crosses the two cascade windows.

Control: add a second eligible internal spike to the first cascade and verify that cascade-specific extraction succeeds and the cross-cascade fallback is not used.

## Stop / interpretation rule

One bounded cycle only. If the behavior is exactly implied by the current fallback implementation and is only an extraction/segmentation semantics issue, do not rescue-tune it. Return `REJECT` if it cannot affect a supported assembly-facing observable beyond bookkeeping; return `PROMOTE_TO_ARCHITECTURE_STUDY` only if the current extractor can construct an assembly-facing pattern that bridges explicitly distinct cascades and therefore changes candidate formation semantics. No production patch is authorized.