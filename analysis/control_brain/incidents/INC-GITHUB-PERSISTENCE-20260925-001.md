# INC-GITHUB-PERSISTENCE-20260925-001

Status: OPEN_P0
Owner: SparkBrain Control Brain
Priority source: HUMAN-20260925-002
Opened: 2026-09-25 JST
Last updated: 2026-09-25T20:58:00+09:00

## Scope

GitHub persistence / mutation inconsistency across SparkBrain scheduled workers.

## Confirmed facts

- GitHub repository reads, refs, branch inspection, PR search, and CI reads are functioning.
- Repository Steward has recently completed history/latest/state persistence successfully.
- Manual Control direct writes from this chat succeeded on 2026-09-25:
  - append-only Control R75 history commit: 7ec669d1fc7d90b418c8bc0f7fb5f1500d6cabad
  - Control latest reconciliation commit: 472d57019db19133d49a6a815593349ef219cd9a
  - Control state reconciliation commit: 35422924e286f2feeffa180b5dd997b568121d99
- Therefore a repository-wide GitHub write-permission outage is not supported by current evidence.
- Scheduled MAIN has repeatedly failed to create the accepted SB001 reviewed-integration PR before a GitHub PR is created.
- Several scheduled streams have shown invocation newer than durable publication, or append-only history newer than moving latest/state.
- A single successful direct/manual write does not close this incident.

## Current hypothesis boundary

Supported:
- failure is path/worker/runtime dependent rather than a global repository write outage;
- partial persistence / stale pointer / optimistic-concurrency / execution-safety-layer behavior remain plausible classes.

Not yet established:
- exact root cause;
- whether all scheduled GitHub mutations fail uniformly;
- whether stale SHA conflicts, shared-branch collisions, or execution safety refusal are primary vs secondary contributors.

## Current fleet controls

- MAIN: enabled; critical-path owner for accepted SB001 integration.
- Utility: enabled temporarily as diagnostic canary; classify as RESTARTING_DIAGNOSTIC until its next durable run is validated.
- Relay: DEPENDENCY_WAIT_SUSPEND. Restart only after safe MAIN handoff + mutation/publication path bounded + first durable post-restart generation can be checked.
- Control: enabled and incident owner; must not disable itself.
- Other current legitimate workers remain enabled unless they demonstrate a material write hazard requiring fault suspension.

## Persistence rules during incident

1. Complete append-only history is primary durable authority.
2. latest/state are moving pointers/caches.
3. Re-fetch branch head and blob SHA immediately before mutation.
4. Prefer one atomic multi-file commit if available and safe.
5. Otherwise use bounded CAS-style retry on stale head/SHA conflict.
6. Never force-push.
7. Never overwrite a newer concurrent generation.
8. Record when possible:
   - write_attempt
   - write_error_class
   - branch_head_before
   - branch_head_after
   - retry_count
   - persistence_complete
9. Single later success is not incident closure.

## Completion criteria

Do not close P0 until all are true:
1. principal root cause(s) identified or sufficiently bounded;
2. affected partial durable streams reconciled;
3. safe write path or bounded workaround established;
4. affected worker canary or real generation persists durably;
5. authority of append-only history vs moving pointers cannot mislead science/build allocation;
6. workers restart after objective restart conditions;
7. same failure pattern is absent across multiple relevant runs.

## Immediate next diagnostics

- validate Utility next post-restart durable generation;
- compare successful Steward/manual-Control path against failing scheduled MAIN/Control paths;
- inspect exact error class when a scheduled write fails, without collapsing runtime-safety refusal into GitHub permission failure;
- reconcile moving pointers only from verified complete append-only generations;
- keep accepted SB001 head unchanged while PR mutation path is unresolved.
