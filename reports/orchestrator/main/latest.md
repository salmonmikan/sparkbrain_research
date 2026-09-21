# MAIN PRIMARY — R43 canonical no-target reconciliation

**schema_version:** `2`  
**generation_id:** `MAIN-20260921T212004+0900-PRIMARY-FUNNEL21-HOLD-R43-6A8C21D5`  
**Evidence Analyst:** `EVA-20260921T205800+0900-R43-6E2A91C5 @ 5692a1b3f210ae2be2cef80266b6e4fc1c7a14d4`  
**Current candidate:** `NONE`  
**Layer / ceiling:** `NONE / NONE`  
**Lease:** `COMPLETED`

R43 consumed R42 and canonically closed `CAND-PREFORMAL-CROSS-GENERATION-HOLDOUT-EXPOSURE-INTEGRITY-01` as `HOLD / SYSTEM / preformal_eligible=false / HOLD_METHOD_LIMITED / TERMINAL_FOR_CURRENT_OBJECT / NOT_QUEUED`, with `preformal_readiness=NOT_APPLICABLE` and exploration cycle count `2`. The exact hold reasons are `SAFE_METADATA_INSUFFICIENT_TO_MACHINE_CHECK_EXPOSURE_OR_FEEDBACK`, `FINAL_AUTHORIZED_METADATA_ONLY_CYCLE2_COMPLETED_WITHOUT_PROTECTED_OUTCOME_ACCESS`, `NO_THIRD_RESCUE_PER_PROSPECTIVE_R42_MAPPING`, and `FUTURE_SCIENCE_REQUIRES_PROSPECTIVE_EXPOSURE_POLICY_BINDING`.

There is now no active MAIN prospective object. Funnel state is DISCOVERY `M0/S0`, ARCHITECTURE `active M0/S0, queued M0/S0`, PRE_FORMAL `eligible=0, READY=0`, FORMAL `EMPTY_HOLD` with no fresh one-way authority, and viable executable MECHANISM=`0`. Because `claim_ceiling` and lifecycle fields apply only to the current prospective object, MAIN does not inherit the predecessor's SYSTEM/hold/terminal dimensions into the no-target state; current-object fields are null while the predecessor canonicalization is recorded separately.

Independent refresh confirms stable `main=ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; exactly five authoritative `evidence/*` tags; zero `formal/*`, `sealed/*`, and tag-level `freeze/*`; unchanged STARTED/control and raw-preserve namespaces including H5 `058e90227cd48e1c10c6ecbaed01efdec1217d0e` / `ce5797eb584344db7a512e585506fb6c59ea475b`; historical conformance ref `research/main-outcome-blind-four-stage-pipeline-conformance-arch-20260921@168883bd316985537e404c6aad3a7ac03202e28a`; and PR #148/#149 open, unmerged, mergeable. Latest observed Analyst control-plane CI `35597662017@5692a1b3f210ae2be2cef80266b6e4fc1c7a14d4` completed successfully. No MAIN scientific workflow is active or dispatched.

Fresh SUB `SUB-20260921T203533+0900-NOOP-R42POSTMAIN-METHODHOLD-3C7A21E5` remains no-target and owns no overlapping candidate, so collision status is `NO_COLLISION`.

This run performs only R43 control-plane reconciliation. New counts are `FORMAL=0 / PRE_FORMAL=0 / MECHANISM Architecture=0 / SYSTEM Architecture=0 / identity consumption=0`. No research branch mutation, scientific workflow, STARTED, preserve, scoring, merge, protected-outcome read, immutable evidence/control/preserve mutation, SYSTEM→MECHANISM upgrade, or retroactive evidence invalidation occurred.

**Stop reason:** `R43_NO_ACTIVE_MAIN_OBJECT_INTENTIONAL_IDLE_NO_TARGET_DO_NOT_MANUFACTURE_ACTIVITY`.

Next action: remain intentionally idle until a fresh Evidence Analyst allocation follows a material mechanism-surface delta or independently motivated fresh integrity object. Do not run a third #31 cycle, implement a ledger under #31, manufacture a SYSTEM queue item, or enter PRE_FORMAL/FORMAL without fresh authority.
