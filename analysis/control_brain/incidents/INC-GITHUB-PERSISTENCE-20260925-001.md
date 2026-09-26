# INC-GITHUB-PERSISTENCE-20260925-001

Status: OPEN_P0
Owner: SparkBrain Control Brain
Last reconciled: 2026-09-26T10:52:31+09:00

## Current bounded facts
- Repository-wide GitHub write outage is not supported.
- Complete append-only history is primary authority; moving latest/state are caches.
- Control R76 atomic publication succeeded.
- Repository Steward G21 atomic publication succeeded.
- Evidence Analyst R136, Methodology R124 and MAIN R140 demonstrate prior history/pointer publication debt.
- MAIN R140 also records two normal reviewed SB001 PR creation attempts blocked before PR creation by the execution-safety layer.
- A brand-new isolated scheduler canary created branch `ops/persistence-canary-p0` successfully, but that branch still equals `main@d16403414fc7abebd23075fc401240971b8eb91d` and its required diagnostic state file is absent. Atomic canary publication/readback therefore failed.
- Because a new scheduler instance also failed its publication success contract, old scheduler-instance corruption alone is insufficient as root cause.

## Root-cause boundary
Principal supported class: automation-runtime/action-path/context-dependent mutation refusal. Non-atomic multi-write publication can amplify a runtime refusal into partial history/latest/state debt. Stale head/SHA or scheduler identity may coexist but do not explain all observed pre-GitHub/runtime refusals.

## Recovery posture
The user has approved temporary canaries and bounded blue-green worker replacement, excluding automatic Control self-replacement. Production blue-green rollout is HOLD because the required new-scheduler canary did not succeed. Current affected workers remain intentionally suspended. No failed/expired Utility assignment may be replayed.

## Completion criteria
Do not close P0 until a safe mutation/publication path is sufficiently bounded, partial authority debt cannot mislead allocation, at least one relevant isolated canary completes atomic publication/readback, restarted/replacement persistence workers validate their first durable generation, and the same failure pattern is absent across multiple relevant runs.
