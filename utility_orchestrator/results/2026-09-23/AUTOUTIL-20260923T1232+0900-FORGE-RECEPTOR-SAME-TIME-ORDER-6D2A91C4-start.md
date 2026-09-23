# Utility autonomous Fast Forge support — start

schema_version: 2
assignment_mode: AUTONOMOUS_IDLE
autonomous_task_id: AUTOUTIL-20260923T1232+0900-FORGE-RECEPTOR-SAME-TIME-ORDER-6D2A91C4
status: RUNNING
max_runs: 1
evidentiary_status: NON_EVIDENTIARY
scientific_authority: NONE
fast_forge_support: true

objective: >-
  Independently test on source-level synthetic/dev semantics whether same-time,
  same-channel receptor pulses are permutation-invariant, or whether stable tie
  ordering creates a transient output-order artifact. Any observation must first
  be reduced against ordinary sequential implementation semantics.

trigger_source: >-
  Fresh Fast Forge receptor/suppression run ended in two ordinary-reduction dead
  ends with no Utility request. This diagnostic is a distinct second path on the
  receptor-local public/dev surface and does not duplicate the priming or
  suppression probes.

ownership_checks:
  evidence_analyst: EVA-20260923T105725+0900-R92-6B8E31D4
  main: MAIN-20260923T121719+0900-PRIMARY-CAND34-PREFORMALR2-R92-RECONCILE-AUTHORITY-CONTRACT
  relay_previous: MAIN-20260923T115328+0900-RELAY-CAND34-PREFORMALR2-R92-BLOCKED-AUTHORITY-INTEGRITY
  fast_forge: FORGE-20260923T114344+0900-R92-RECEPTOR-SUPPRESSION-DEADENDS
  control: CTRL-20260923T115056+0900-R41-4C156929
  utility_assignment_pointer: CLEAN_SCHEMA_V2_IDLE
  collision_found: false

exact_refs:
  stable_main: ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d
  analyst_commit: a05ab3f655a23eabd84c910ba337d64a948c168a
  orchestrator_commit: 92806ba4042af799d26cae17cd14f55faf84bdaf
  control_commit: 27b6531b6b3a1d941a484aeee012d5c59fe63d79
  forge_branch: forge/20260923-receptor-suppression-probes-a
  forge_head: c366c4054d2834003fcca20d49b8fc9ad4203edc
  receptor_source_blob: 86c1cfea1ea70cada5c277d8f5047c32ea611a5c

allowed_actions:
  - read public/dev receptor implementation and contracts
  - one bounded same-timestamp permutation diagnostic
  - persist Utility-owned terminal record

forbidden_actions:
  - candidate34 PRE_FORMAL or candidate35 canonical work
  - H7 or PF-R1 preservation/formal work
  - scientific identities, scoring, protected outcomes, evidence/preserve refs
  - workflow result dispatch, scheduler mutation, research merge

stop_condition: >-
  Stop after determining whether the pulse permutation changes transient receptor
  outputs and whether any difference is fully explained by stable tie ordering and
  sequential state updates.
