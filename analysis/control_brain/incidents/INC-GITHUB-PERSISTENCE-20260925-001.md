# INC-GITHUB-PERSISTENCE-20260925-001

status: OPEN_P0
updated_at: 2026-09-26T18:52:06+09:00
owner: CONTROL_BRAIN

## Current evidence

- Repository-wide GitHub write outage is not supported.
- User-directed full fresh-thread scheduler migration is active; old scheduler instances are intentionally disabled.
- Fresh-thread Relay R146 successfully mutated the SB001 build branch, durably published MAIN state/history/lease, and current-head CI succeeded.
- The same fresh-thread Relay had two pre-GitHub refusals when attempting to post a Codex re-review request comment.
- Therefore old-thread state alone cannot explain all scheduler mutation refusals. Failure remains selective by automation runtime/action path or mutation context.
- Exact fresh-thread `create_pull_request` health remains unresolved because PR #152 was created before the migration.
- Evidence Analyst durable scientific authority remains R136 and is exact-head-bound to pre-review-fix SB001 head `5b86dfa6...`.
- PR #152 current head is `e9b93456...`, open/mergeable with successful CI, but it awaits fresh review/re-check and Analyst rebinding.

## Current authority

Append-only histories remain primary where caches are stale:
- Analyst R136
- Methodology R125
- MAIN current shared stream R146 (Relay execution)
- Steward G21
- Literature R44 / Theory R5 / Audit R10

## Recovery posture

Keep the fresh-thread replacement fleet enabled and validate worker-by-worker. Do not create another Analyst replacement yet: the user-initiated full migration already supplies a fresh Analyst instance and its first run should be observed. Keep PR #152 unmerged until the new head receives fresh Analyst authority and current-head review/re-check.

P0 remains open until relevant writer/action classes are demonstrated healthy or a stable workaround is established. Scientific hard floor is unchanged.
