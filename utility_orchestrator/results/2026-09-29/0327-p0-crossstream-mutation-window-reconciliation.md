# Utility P0 cross-stream mutation-window reconciliation

generation_id: AUTOUTIL-20260929T032701+0900-P0-CROSSSTREAM-WINDOW-RECON-71C4E9A2
status: COMPLETED
mode: AUTONOMOUS_IDLE
evidentiary_status: NON_EVIDENTIARY_OPERATIONAL_DIAGNOSTIC_ONLY
incident: INC-GITHUB-MUTATION-RECURRENCE-20260928-001

## Freshness / ownership

- Human Directive index head: `8ce979b9ec0bc7eede5225c0403698f8886d3e8d`
- active-index blob: `1ba1e173344f36e14d0e21e6f3e823254e031f7d`
- directive delta versus prior Utility durable state: none
- Utility assignment: schema-v2 clean IDLE
- Control: R117
- Evidence Analyst durable authority: R168
- MAIN: R182
- Relay allocated: false
- M1-002 owner: MAIN
- M1-002 exact head: `2a21d3e879f1db4e81a58273180ad2124e823a5e`
- base main: `59fc994b39d0ba02682e972161bb46801592d25b`

## Bounded diagnostic

No new PR canary was issued. This run reconciled the current production failure window and repository-side policy state.

Fresh observations:

1. MAIN R182 exhausted five `create_pull_request` attempts with five explicit `PRE_GITHUB_PLATFORM_SAFETY_REFUSAL` observations. Its durable MAIN report/state publication nevertheless succeeded, and no M1-002 PR is present.
2. The M1-002 source branch still points exactly to `2a21d3e879f1db4e81a58273180ad2124e823a5e`; `main` remains `59fc994b39d0ba02682e972161bb46801592d25b`. No open PR matched M1-002, BUILD-SB-M1-002, or the exact source SHA.
3. Evidence Analyst R169 persistence request `EA-R169-20260929T025526JST` is absent and request-branch head remains `1e459a06c100907f1a1f31d1ba625e17266bb4c0`, consistent with the reported five pre-GitHub request-publication refusals. Durable Analyst authority therefore remains R168.
4. Control R117 atomic publication succeeded at head `08d49d5086726b5b7e409abdd58a00ae2a478790`, including reconciliation of Control's prior moving-pointer debt.
5. This Utility scheduled run successfully created its own STARTED record through the GitHub contents write path at commit `a086bcf50e6d90bbb08caaa76728918658057190`. Therefore generic scheduled GitHub writes and generic contents-file creation are not globally unavailable in the same broad time window.
6. Fresh repository metadata reports `pull_request_creation_policy=all` and repository permissions `admin/maintain/push/triage/pull=true`. Active ruleset `protection_main` targets only the default branch, requires a PR with zero approving reviews, allows squash merge, forbids deletion/non-fast-forward, and has no bypass actors.

## Disposition

The new high-value observation is the within-window contrast:

- Utility contents-file write: success;
- Control atomic Git-data publication: success;
- MAIN report/state publication: success;
- MAIN PR creation: 5/5 pre-GitHub refusal;
- Analyst request-file publication on its persistence mailbox: reported 5/5 pre-GitHub refusal and still absent.

This further rejects a repository-wide outage and also rejects a generic "all scheduled Contents API writes are blocked" explanation.

The recurrent PR-create action remains the strongest common failure surface, but Analyst mailbox refusal shows the incident is not limited to PR creation. The evidence is most consistent with an action/path/ref/content/execution-context-sensitive intermittent pre-GitHub mutation problem. Root cause remains UNKNOWN; no internal platform classifier or HTTP failure is inferred.

## Recommendation to Control

Stop spending diagnostic cycles on generic repository permission/ruleset checks unless those settings change. Prioritize recovery experiments that distinguish mutation purpose/action and execution context while preserving standard scheduled-task execution only. Production M1-002 PR-create recovery remains the highest-value acceptance path; generic file-write canaries now have low information gain.

No MAIN, SYSTEM_BUILD, science, workflow, scheduler, PR, immutable/formal/evidence, or non-Utility state was mutated.
