# SparkBrain Control Brain — Manual Directive Application

- schema_version: `2`
- generation_id: `CTRL-20260925T205800+0900-R75-MANUAL-P0`
- produced_at: `2026-09-25T20:58:00+09:00`
- producer_run_id: `manual-chat-directive-apply-20260925-2058`
- authority_scope: `CONTROL_BRAIN_STRATEGY_GOVERNANCE_AND_INCIDENT_CONTROL`
- supersedes_generation_id: `CTRL-20260925T125000+0900-R74`
- invocation_kind: `MANUAL_IMMEDIATE_RESPONSE`

## Human Directive dispositions

- HUMAN-20260925-002: **ACCEPT / IMMEDIATE APPLY**
  - Priority: P0 / highest operational priority until completion criteria are met.
  - Control Brain is incident owner.
  - Incident-scoped scheduler prompt mutation authority is active.
  - Cadence, scheduler creation/deletion, and scientific standards are unchanged.
- HUMAN-20260925-001: MODIFY remains in force as zero-credit research/design guidance; subordinated operationally to P0 persistence resolution.
- Existing FORMAL/evidence hard floor remains unchanged.

## Incident

- incident_id: `INC-GITHUB-PERSISTENCE-20260925-001`
- status: `OPEN_P0`
- primary symptoms:
  - append-only history newer than moving latest/state in several streams;
  - scheduler invocation without expected durable publication;
  - MAIN PR creation/mutation refusal despite healthy GitHub reads;
  - worker-dependent write behavior; Repository Steward recently completed history/latest/state successfully.
- current bounded hypothesis: repository-wide GitHub write loss is not supported; failure is more consistent with worker/runtime/tool mutation path differences, concurrency/stale-pointer behavior, or execution safety-layer refusal.
- root cause: not yet closed/bounded enough to resolve incident.

## Immediate control actions

1. Utility Orchestrator enabled for bounded persistence/runtime diagnosis.
   - operational_state: `RESTARTING_DIAGNOSTIC`
   - restart/validation condition: first post-enable run must produce expected durable history and pointer/cache behavior or concrete error telemetry.
   - on material failure: return to `FAULT_SUSPENDED`; do not enter rapid restart loop.
2. Relay remains disabled.
   - class: `DEPENDENCY_WAIT_SUSPEND`
   - reason: no safe MAIN READY_FOR_RELAY handoff; re-running the same blocked mutation path adds little information.
   - restart conditions: MAIN safe handoff + mutation/publication path sufficiently bounded + first post-restart durable generation can be validated.
   - restart_owner: Control Brain.
3. MAIN remains enabled because accepted SB001 integration work is actionable and MAIN owns the critical path.
4. Evidence Analyst, Methodology, Fast Forge, External Science, Current State Brief, and Control remain enabled so work discovery, integrity audit, and independent incident evidence continue.
5. No cadence changes were made.

## Persistence remediation policy now active

- append-only generation history is primary durable authority when complete;
- latest/state are moving pointers/caches and must never silently override a newer complete history generation;
- re-fetch branch head and current blob SHA immediately before mutation;
- use bounded CAS/retry for stale SHA/head conflicts;
- never force-push to win a race;
- prefer one atomic multi-file commit when available and safe;
- do not overwrite a newer concurrent generation;
- record where possible: write_attempt, write_error_class, branch_head_before, branch_head_after, retry_count, persistence_complete.
- a single later successful write does not close the incident.

## Science / build state

Canonical science is unchanged: 35/35 terminal, 14 MECHANISM / 21 SYSTEM, active 0, scientific queue 0. Consumed FORMAL identities remain immutable; no rerun/retune/rescore.

BUILD-SB-001 remains accepted bounded NON_EVIDENTIARY_BUILD at the accepted exact head. Built/functionally verified within bounded acceptance: yes. Comparatively supported: no. Composition contribution: not established. Scientific novelty/credit: none. Reviewed integration PR remains pending because the mutation path has not yet succeeded.

## Next incident actions

- push incident-scoped persistence instructions into current legitimate scheduler prompts without changing cadence or scientific semantics;
- use Utility's next run as an independent diagnostic/canary;
- compare successful Repository Steward write path vs failing Control/MAIN/other worker paths;
- reconcile stale moving pointers from newer complete append-only histories only after authoritative generation validation;
- retain incident OPEN until completion criteria in HUMAN-20260925-002 are satisfied.
