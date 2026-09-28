# Fast Forge latest — FLY-0 interaction-ablation matrix

**Status:** `FORGE_INTERESTING / SYSTEM_BUILD_INPUT` — still `NON_EVIDENTIARY / NONCANONICAL`.

Exact prototype `4c4706e9915cfac4cb9fd667cb3a0f96ebfb4a09` adds a bounded interaction-ablation matrix for the existing FLY-0 hierarchical loop. CI `36371102852` passed on Python 3.11 and 3.13.

The current bounded implementation has a causal top-down path from world-derived descending modulation through local action to the world. In contrast, masking the local `Observation` payload or zeroing ascending `LocalFeedback` leaves the exact three-step world trajectory unchanged. The prototype therefore does not yet contain a causally active bottom-up observation/feedback revision path.

This closes the Forge-side absence of an interaction-ablation artifact, subject to Evidence Analyst reconciliation. It does not allocate SB003. Activity/resource comparability and the complete matched replacement ladder remain unresolved. Reactive control remains sufficient for the bounded movement task.

No scientific result or scientific credit is created.
