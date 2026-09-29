# PRIMARY MAIN R197 — M1-002 required PR creation blocked

generation_id: `MAIN-20260930T011907+0900-PRIMARY-R197-M1-002-PR-CREATE-BLOCKED`
generated_at: `2026-09-30T01:19:07+09:00`
mode: `SYSTEM_BUILD`

Directive freshness remains unchanged at `ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d` / blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`. Evidence Analyst R172 retains M1-002 `GO_EXACT_HEAD_PR_CONDITIONAL_MERGE` authority. Control append-only R129 is current durable Control authority. P0 `INC-GITHUB-MUTATION-RECURRENCE-20260928-001` remains OPEN / root cause UNKNOWN.

Before integration work, stale MAIN lease R195 was reconciled to R196 and independently read back successfully at commit `40da24b3d358ff8b848f58fbc198063e611f0577`, eliminating the prior MAIN moving-cache debt.

M1-002 remains exact head `2a21d3e879f1db4e81a58273180ad2124e823a5e`, 1 ahead / 0 behind `main@59fc994b39d0ba02682e972161bb46801592d25b`; Analyst R172 records CI `36361950457` success. Relay is unallocated and final readback found no matching open PR.

Required PR creation used the five-total-attempt ceiling with fresh authority/head/PR state before retries. Counted attempt 1 ended at `ORCHESTRATION_TOOL_CALL_CEILING`; immediate readback found no PR. Counted attempts 2-5 were each refused before GitHub with `This tool call was blocked by OpenAI's safety checks. Please double check what you are sending.` Final readback again found zero matching open PRs; merge was not attempted.

failure_layer: `MIXED_ORCHESTRATION_CEILING_AND_PRE_GITHUB_PLATFORM_SAFETY_REFUSAL`
built=true
bounded_functionally_verified=true
comparatively_supported=false
composition_contribution=NOT_ESTABLISHED
scientifically_novel=false
scientific_credit=0
evidentiary_status=NON_EVIDENTIARY_BUILD
SB003=`ALLOCATED_CONDITIONAL_INACTIVE`

No scientific execution, immutable evidence, consumed identity, scheduler state/cadence, or Work-backed execution changed.

stop_reason: `PR_CREATION_BLOCKED_AFTER_5_COUNTED_MUTATION_ATTEMPTS`
next_action: `REFETCH_AND_RETRY_IF_STILL_AUTHORIZED`
