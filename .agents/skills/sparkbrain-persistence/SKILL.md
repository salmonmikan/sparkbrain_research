---
name: sparkbrain-persistence
description: Persist SparkBrain scheduler state, history, leases, build records, or operational records to GitHub safely, including P0 retry/readback and the Evidence Analyst GitHub Actions persistence bridge.
---

# SparkBrain persistence workflow

Use only inside the invoking role's existing authority.

## General safe-write contract

1. Re-fetch the exact target branch/ref head and target files needed for a safe write.
2. Prefer append-only history plus moving cache pointers.
3. Prefer one atomic multi-file commit where supported.
4. Never force-push or overwrite a newer generation.
5. During an active P0 incident, allow at most THREE TOTAL ATTEMPTS for the same mutation purpose.
6. Before every retry, re-fetch target branch/ref and required file/blob/head/PR/workflow state and rebuild against fresh state.
7. Never blindly replay a stale SHA/head mutation.
8. For idempotence-sensitive actions, verify whether the previous attempt already succeeded before retrying.
9. After apparent success, independently read back relevant branch/ref/files/PR state.
10. Publication is complete only after readback verification.
11. After three failures, fail closed for the current run and report actual observed failure layer/class plus attempt count.
12. Never disable the recurring scheduler merely because the write failed.
13. GitHub retries never authorize rerunning/retuning/rescoring/redispatching consumed scientific/FORMAL execution.

## Failure classification

When possible distinguish:
- no tool/action invocation;
- platform/runtime/safety refusal before GitHub;
- authentication/permission/tool availability;
- GitHub validation/conflict/rate failure;
- stale SHA/head/CAS conflict;
- partial publication/pointer debt;
- readback verification failure.

Do not invent HTTP codes, request IDs or safety reasons that were not observed.

## Role-owned publication

Use the branch/path contract in the invoking role document.

Append-only history is durable authority where that role specifies it. Moving `latest`, `state`, and `lease` files are caches/pointers unless the role contract says otherwise.

## Evidence Analyst GitHub Actions persistence bridge — current P0 design

When the active Human Directive requires the bridge, Evidence Analyst must use the following exact operational contract.

### Request branch and target

- Request branch: `ops/evidence-persistence-requests`
- Request namespace: `ops/persistence_requests/evidence-analyst/<request_id>.json`
- Target branch: `ops/evidence-analyst-handoff`
- Target history namespace: `analysis/orchestrator/history/YYYY-MM-DD/<name>.md`
- Target latest cache: `analysis/orchestrator/latest.md`
- Target state cache: `analysis/orchestrator/state.json`
- Receipt: `analysis/orchestrator/persistence_receipts/<request_id>.json`

The request branch is a mailbox and never scientific source of truth.

### Request JSON contract

Construct exactly one append-only request with:
- `schema_version: 1`
- `request_id`: unique ASCII identifier using letters, digits, dot, underscore or hyphen only
- `role: "EVIDENCE_ANALYST"`
- `persistence_only: true`
- `target_branch: "ops/evidence-analyst-handoff"`
- `expected_target_head`: exact lowercase 40-character SHA observed immediately before request publication
- `generation: "R<number>"`
- `history_path`: new append-only Analyst history path
- `history_content`: complete intended history content
- `latest_content`: complete intended latest.md content
- `state_content`: complete intended state.json serialized as a JSON string

The request file path must exactly match:
`ops/persistence_requests/evidence-analyst/<request_id>.json`.

### Scheduler-side mutation minimization

For one normal Analyst generation, scheduler-side persistence should perform only ONE GitHub mutation purpose: creation of that append-only request file.

After a request is accepted, do not separately create/update Analyst history/latest/state from the scheduler. The GitHub Action owns target-branch persistence for that request.

### Request retry / idempotence

Apply the three-total-attempt contract to creation of the same request file.

Before every retry:
- re-fetch request branch;
- re-fetch the exact request path;
- re-fetch target branch head.

If the exact request already exists with identical content, treat request publication as successful rather than creating a duplicate.

If target branch head changes before request publication completes:
- do not rewrite the old request with a new expected head;
- do not silently rebind generated content to the new head;
- fail closed for that generation and re-evaluate from fresh repository state on the next run.

Never overwrite an existing request file.

After apparent request success, read back the exact request and verify its contents.

If request creation is refused/fails three times, fail closed for the run and do not bypass the bridge with ad-hoc direct target writes.

### GitHub Action semantics

The Action performs persistence only. It does not create scientific authority, interpret outcomes, execute experiments, or alter scientific rules.

Expected Action behavior:
- verify `expected_target_head`;
- refuse an existing history path;
- write history + latest + state + durable receipt in one target-branch commit where implementation supports it;
- push non-force;
- read back remote head/files.

The request plus receipt provide operational provenance. Canonical scientific authority is the verified append-only Analyst history on the target branch.

### Completion criteria

Request-file existence alone is not publication completion.

Publication is complete only after independently re-fetching the target branch and verifying:
1. intended append-only history exists;
2. latest.md corresponds to that generation;
3. state.json corresponds to that generation;
4. receipt exists for request_id;
5. receipt has `persistence_complete=true`;
6. request_id/request-SHA binding matches the request;
7. target state does not show a conflicting newer generation silently overwritten.

If the Action has not finished in the current run, perform no direct target mutation. Report WAITING_EXTERNAL with request_id/path and verify next run.

## Pending-request reconciliation first

Before minting a new Analyst generation during the bridge incident:
- inspect the request mailbox for prior unresolved Analyst requests;
- inspect target receipts;
- re-fetch target branch.

A request is only pending persistence intent.

If a prior request succeeded, reconcile target latest/state/history before new analysis.

If a request exists without a receipt and the Action may still be running, report WAITING_EXTERNAL instead of minting another generation.

If target moved or the request demonstrably failed, do not silently rebind the old payload. Re-evaluate from fresh repository state.

A failed request never authorizes rerun/retune/rescore of consumed science.
