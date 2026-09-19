# MAIN PRIMARY — suppression semantics Architecture cycle 1 invalid diagnostic stop

Timestamp: `2026-09-20 05:18 JST`  
Worker role: `main`  
Execution mode: `PRIMARY`  
Evidence Analyst authority: `493573eb3b8c38d88f251db7c04dfe1a586c6ff0`  
Research layer: `ARCHITECTURE_STUDY`  
Candidate: `CAND-V05-UNIT-SUPPRESSION-TRANSIENT-SEMANTICS-01`

## Reconciliation

The inherited RELAY checkpoint was collected successfully. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`, active research head remains `research/main-v05-unit-suppression-transient-semantics-arch-study-20260920@2ef4b24f8e7ef8577ebbcb0328e7b3476bc24336`, and fresh Evidence Analyst authority remains `493573eb3b8c38d88f251db7c04dfe1a586c6ff0`. SUB remains independent and was not absorbed.

FAST PATH escalated to **FULL RECONCILIATION** after artifact/source verification found a diagnostic integrity anomaly. Reconciliation confirmed five authoritative `evidence/*` annotated tags, zero tag-based `formal/*`, `sealed/*`, and `freeze/*`, 13 preserved legacy `freeze/*` branches, preserve branch `ops/a01-md-001-preserve-once@465b8afe73aa6ff9dad2fa67d1f954a3ec689097`, Control branch `ops/control-brain-handoff@98155846394925730997fc35389fd6ad1b53f710`, and PR #148/#149 still open/unmerged.

## Exact workflow / artifact

Architecture workflow `35465512928` completed `success` on exact head `2ef4b24f8e7ef8577ebbcb0328e7b3476bc24336`; ordinary CI `35465512894` also completed `success` on the same head. Artifact `10591265966` was retrieved. Its downloaded archive SHA-256 exactly matches GitHub's digest: `d4dd67e97132229fc60c1cf13b6dbc9366bfa22a2568aa7de116667b41d33669`. `summary.json` binds the same workflow/head/Analyst/source scope and records raw SHA-256 `220eb06b051273680726b8f0f4ad318a95863fcc1e9909daeb23ffd745ec6805`; the downloaded raw file independently hashes to that value.

The artifact emitted `AMBIGUOUS_CONTRACT`, but that emitted class is **not accepted as a valid Architecture observation**.

## Diagnostic integrity defect

The prospectively bound harness detects threshold restoration with the literal check `"unit.base_threshold = threshold" in restore_source`. The exact blob-bound stable source actually restores the saved threshold as `self.base.field.units[unit_id].base_threshold = threshold`; its apply path stores `original[unit_id] = unit.base_threshold` before setting `unit.base_threshold = 1e9`.

Accordingly, the artifact's raw fact `restore_restores_original_base_threshold=false` is mechanically false for the exact bound source. That false fact propagates to `implementation_state_preserving=false` and causes the fixed mapper to fall through to `AMBIGUOUS_CONTRACT`.

Because the defect was discovered **after outcome-bearing material existed**, the Analyst's prospective no-post-outcome-fix rule applies. MAIN did not patch, rerun, retune, rescore, or assign a repaired alternative semantic class. The attempted cycle is disposed as **`INVALID_DIAGNOSTIC / DISCARD_STOP`** pending fresh Evidence Analyst review.

## Evidentiary status / ownership

New FORMAL scientific evidence: **none**.  
New PRE_FORMAL development evidence: **none**.  
Accepted new ARCHITECTURE_STUDY observation: **none**; cycle 1 was attempted but discarded as invalid diagnostic.  

No official TEST, formal identity, STARTED, scorer, preserve/evidence mutation, consumed-identity mutation, immutable evidence change, research merge, same-run repair, or Utility request occurred. The harness defect remains MAIN critical path and was not offloaded. SUB retains only its independent bounded Discovery lane.

Stop reason: **`POST_OUTCOME_STATIC_HARNESS_FALSE_NEGATIVE_INVALID_DIAGNOSTIC_DISCARD_STOP`**.

Final lease: **`BLOCKED`** pending fresh Evidence Analyst review. A later MAIN run may mechanically fix/rebind/re-execute only if fresh prospective authority explicitly permits it.
