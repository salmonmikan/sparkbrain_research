# SparkBrain Utility Orchestrator Request Bus

This branch is a control-plane mailbox for cross-scheduler requests and Utility Orchestrator assignments.
It is NOT a scientific source of truth and MUST NOT be treated as a repository snapshot.

## Flow

1. Any active SparkBrain scheduler may append a request under `utility_orchestrator/requests/YYYY-MM-DD/`.
2. Requests are proposals only. They do not grant execution authority.
3. Control Brain reads the queue, deduplicates/conflict-resolves, and records a disposition:
   `ACCEPT | MODIFY | DEFER | REJECT | DUPLICATE | SUPERSEDED`.
4. Only Control Brain may publish the active assignment in `utility_orchestrator/assignment/current.md`.
5. SparkBrain Utility Orchestrator executes only the current Control-approved assignment.
6. Utility writes results/checkpoints under `utility_orchestrator/results/` and may append a follow-up request, but may not self-approve it.

## Request write authority

Every active SparkBrain scheduler may CREATE a new request file on this branch.
Schedulers MUST NOT edit/delete another scheduler's request, rewrite prior requests, or write/modify Control decisions or the active assignment.

Suggested request fields:
- request_id
- requester
- created_at
- objective
- reason / expected information gain
- suggested_mode
- dependency / independence notes
- requested authority
- must_not
- expiry
- dedupe_key

The request bus may not be used to evade a scheduler's own scientific-integrity or authority restrictions.

## Global hard floor

No Utility assignment or request may authorize:
- rerun/retune/rescore of consumed identities;
- mutation of immutable/frozen/formal/evidence artifacts;
- held-out/evaluator leakage;
- silent post-outcome repair;
- direct scheduler mutation by Utility itself;
- bypass of Evidence Analyst formal authorization or one-way scientific integrity.

Control Brain may broadly reconfigure the Utility scheduler itself, but the hard floor remains binding.
