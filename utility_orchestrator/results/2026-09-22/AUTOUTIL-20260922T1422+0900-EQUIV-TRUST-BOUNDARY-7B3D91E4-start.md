# Utility autonomous task start

schema_version: 2
autonomous_task_id: AUTOUTIL-20260922T1422+0900-EQUIV-TRUST-BOUNDARY-7B3D91E4
assignment_mode: AUTONOMOUS_IDLE
status: RUNNING
started_at: 2026-09-22T14:22:00+09:00
max_runs: 1
evidentiary_status: NON_EVIDENTIARY
scientific_authority: NONE

objective: >-
  Reconcile the now-completed CI + fresh Repository Steward G10 review for the isolated
  generic equivalence-certificate prototype, and bound the exact remaining trust-boundary
  ambiguity and smallest safe non-scientific follow-up without changing the tool, main,
  H7, candidate state, or scheduler.

trigger_source: >-
  Existing Utility request UTIL-20260922-0934-EQUIV-CERT-CI-STEWARD-REVIEW plus fresh
  Steward G10, which confirms CI is green but defers promotion because declared-digest
  equivalence, producer provenance, raw-to-digest derivation, and process isolation are
  not equivalent authorities.

ownership_checks:
  assignment_pointer: schema-v2 clean IDLE / active_assignment_id=null
  evidence_analyst_generation: EVA-20260922T140541+0900-R63-E8C421B7
  evidence_analyst_ref: ops/evidence-analyst-handoff@9f90816657aa08754827e35976c9fa35b5d7c09a
  control_generation: CTRL-20260922T124800+0900-R33-E7C421B6
  control_ref: ops/control-brain-handoff@c41db58a5cc87e5460f143ce07c4256d7238d577
  sub_generation: SUB-20260922T133738+0900-PRENOOP-R62-NOFRESHDELTA-6C8A21F4
  main_latest_durable_generation_observed: MAIN-20260922T125400+0900-RELAY-H7-DEVR1-ARCH-C2-C7F421A9
  relay_latest_durable_state_observed: MAIN-20260922T125400+0900-RELAY-H7-DEVR1-ARCH-C2-C7F421A9_BLOCKED_PENDING_R62_VERSIONED_R2
  live_main_h7_ref: research/main-h7-dev-r2-comparator-protocol-closure-r63-cycle3@d6655549c179caf391d4b43bd2ebea49f2bfc82b
  collision_found: false
  main_critical_dependency: false

allowed_actions:
  - Read-only inspect the Utility verifier module/tests and repository callsites/usages.
  - Read current Control/Analyst/Steward/mailbox records and exact refs.
  - Classify what VALID_EQUIVALENT actually proves and identify the smallest safe naming/contract boundary for later reviewed integration.
  - Persist Utility-owned state/results only.

forbidden_actions:
  - No mutation of the equivalence-certificate branch or any source/test/docs branch.
  - No H7 or other research-candidate action.
  - No scientific workflow dispatch, result-bearing measurement, rerun, rescore, or consumed identity use.
  - No Funnel typing/readiness mutation, PRE_FORMAL, FORMAL, merge, protected-ref mutation, or scheduler mutation.
  - No self-approval of the existing Utility request and no duplicate Control decision.

stop_condition: >-
  Stop after one exact read-only trust-boundary/callsite reconciliation and record whether
  the prototype is safe to describe as declared-certificate equivalence, which names or
  fields are overbroad, and the smallest reviewed follow-up that would remove ambiguity.

funnel_v2_1_preservation:
  candidate_touched: false
  preserved_fields: NOT_APPLICABLE_NO_RESEARCH_CANDIDATE_TOUCHED
  typing_or_readiness_changed: false
