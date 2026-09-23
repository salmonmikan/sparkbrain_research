# FAST FORGE latest — v0.5 homeostasis windowing dead end

- schema_version: `2`
- generation_id: `FORGE-20260923T223403+0900-V05-HOMEOSTASIS-WINDOWING-R99`
- produced_at: `2026-09-23T22:34:03+09:00`
- worker_role: `FAST_FORGE`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- overall_status: `FORGE_DEAD_END`
- selection_outcome: `BOUNDED_PROTOTYPE_COMPLETED`

## Freshness / independence

Stable main remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. Evidence Analyst R99 remains current. MAIN/Relay completed Candidate #35's bounded non-result preservation/provenance wrapper at implementation head `5bc64fbd8fd2f3e8d804d18e0a0ad0d58b5a3e4c` without candidate response exposure and now requires fresh Analyst review. H7 remains outside Forge. Literature R39's off-manifold/reachable-state work is Candidate #35/immediate-successor territory and was excluded. Methodology R91 and Utility R99 add no separate Forge-owned scientific target.

Forge selected a separate stable-main v0.5 homeostasis timing question not present in prior Forge history.

## Probe

Question: does v0.5 homeostatic threshold recovery encode elapsed physical time, or episode/window count?

Two read-only exact-source diagnostics were performed without a Forge branch:

1. For a never-spiking reservoir unit (`base_threshold=0.76`), every empty `HomeostaticController.observe()` applies `0.004*(0-0.35)=-0.0014`. One empty 9376 ms episode therefore yields threshold `0.7586`, while 293 empty 32 ms episodes cover the same 9376 ms but drive the threshold to its `0.35` floor.
2. The controller's `time_ms` argument is copied into the snapshot but does not enter the EMA/threshold update; repeated calls at an identical timestamp would still change state, while a single much-later call still changes it once.

`IntegratedV05Brain.process_episode()` invokes the controller once per learning episode, while the v0.4 field advances an empty episode by `settle_ms`.

## Reduction / disposition

The observation is fully explained by ordinary discrete-time per-window homeostatic control and API segmentation. The configuration itself names the target `target_spikes_per_window`; this is not a new endogenous-memory mechanism. Any recovery/sensitization interpretation on this path must be stated in observation-window units unless the caller fixes window duration.

Disposition: `FORGE_DEAD_END`. No Evidence Analyst promotion proposal. No Utility request. No code branch or repository science mutation.

MAIN collision check passed. No hard-floor action occurred: no PRE_FORMAL/FORMAL identity, STARTED, official TEST/scoring, protected target access, Candidate #35 response, consumed-identity rerun/retune/rescore, scientific preserve/evidence mutation, workflow dispatch, or research merge.

Cumulative metrics: runs `11`, prototypes attempted `14`, dead ends `11`, interesting retained `0`, promotion proposals `0`, later admissions `0`, duplicate/rescue rejects `9`, ownership collisions `0`, ordinary-reduction rejects `11`.
