# SparkBrain Scheduler Common Policy

## Freshness and source precedence

At the beginning of every run, fetch `AGENTS.md@main`, this file, `SCIENTIFIC_INTEGRITY.md@main`, the current role file, applicable active Human Directives, and the minimum current state needed for the task.

Use this precedence for conflicts:
1. platform/tool safety and actual repository permissions;
2. immutable scientific integrity constraints;
3. later explicit user Human Directives;
4. narrower current role authority;
5. repository-wide scheduler policy;
6. procedural skill guidance.

Never broaden authority because a lower-precedence document is more permissive.

## Human Directive freshness handshake

Before selecting, interpreting, or applying any Human Directive, every scheduler run must complete this order:

1. fetch `AGENTS.md@main`, `COMMON.md@main`, `SCIENTIFIC_INTEGRITY.md@main`, the current role file, and `ACTIVE_POLICY.md@main`;
2. fetch `ops/human_directives/active.md` explicitly from ref `ops/human-directives`;
3. record the current Human Directive branch/index identity needed for freshness (branch head and/or exact index blob/ref as available);
4. when the role has durable prior state, compare the current index identity with the previous generation and identify newly active or materially changed directives;
5. derive the applicable directive set from the current index, not from memory, copied prompts, or a hard-coded list;
6. fetch only directive bodies relevant to the current role/task/incident, plus directives explicitly referenced by current higher-priority authority;
7. only then make role decisions, allocate work, or mutate repository/scheduler state.

A copied directive inside a scheduler prompt is not proof that the directive is still current. Prompt-local copies should be treated only as temporary routing hints and removed when durable main policy/skills cover the behavior.

If the authoritative active index cannot be fetched, or if a material directive conflict cannot be resolved under the normal precedence rules, fail closed for the current run only. Do not self-suspend the recurring scheduler.

For stateful roles, durable state should record when applicable:
- `directive_index_head` / exact active-index identity;
- `previous_directive_index_head`;
- newly active/materially changed directives;
- applicable directives actually read;
- each material Control/Analyst disposition or interpretation.

When a newly active or materially changed directive affects the current decision, the user-facing report must mention that directive and the applied disposition/interpretation. If there is no directive delta, routine reports need not repeat the whole directive set.
## Branch semantics

- `main`: stable shared repository policy, common runtime, stable docs/interfaces and reusable outcome-independent tooling.
- `research/*`: scientific development/frontier objects.
- `system-build/*`: integration development.
- `forge/*`: rough noncanonical exploration.
- `ops/*`: mailboxes, moving pointers, durable run history and operational state. They are not repository snapshots and must not be merged/rebased merely to follow `main`.
- immutable/freeze/sealed/formal/evidence refs: one-way scientific anchors.

Always read repository policy from `main`; never merge/rebase a working branch merely to receive policy changes.

## Scheduler stop authority

Only Control Brain in `CONTROL_BRAIN` mode may decide and apply recurring SparkBrain scheduler suspension. This authority is non-delegable.

Every other worker, including Relay, Analyst, Forge, Utility, Methodology, External Science, Brief, canaries, and Repository Steward mode:
- may fail closed or stop the current run;
- may report that scheduler suspension appears advisable;
- must not disable, pause, delete, retire, expire, alter recurrence to suppress, or create a persistent self-suspension latch for itself or another scheduler.

`STOP`, `IDLE`, `NO_OP`, `WAITING_EXTERNAL`, completion, collision avoidance, and exhausted retries apply to the current run/work item unless Control explicitly changes scheduler state.

Control itself must never disable/delete/replace its own recurring scheduler automatically.

## User authorization for in-scope GitHub operations

GitHub operations already permitted by the worker's current role, scope, Human Directives and scientific restrictions are user-authorized. Do not invent an additional per-run confirmation requirement solely because the run is scheduled or unattended.

This does not bypass OpenAI/platform safety, GitHub permissions/rulesets, scientific hard floors, or narrower prohibitions. If a tool/platform actually refuses an action, preserve and report the real refusal.

## GitHub mutation reliability contract

For every already-authorized GitHub persistence/publication purpose, including final publication and P0 incidents:
- same-purpose mutation: at most 5 total attempts (the initial attempt plus up to 4 retries), shared across tools/routes for that purpose;
- stop after verified success; this is a ceiling, not a requirement to exhaust attempts;
- existing role authority and actual platform/GitHub permissions remain unchanged; a refusal does not authorize an alternate path that bypasses the refused boundary;
- before every retry, re-fetch the target ref/head and any state needed for a safe mutation;
- stale SHA/head/CAS/concurrency failures require a fresh rebuild against the new state;
- never force-push or overwrite a newer generation;
- for idempotence-sensitive actions, verify whether the previous attempt succeeded before retrying;
- after success, independently read back the relevant ref/files/PR and verify;
- after 5 failures, fail closed for the current run and report the observed failure layer/class and attempt count;
- this retry budget applies only to persistence/publication, not to scientific experiment execution, scoring, or result-bearing workflow dispatch; separate execution authority remains required;
- retries never authorize rerunning, retuning, rescoring, or redispatching consumed scientific/FORMAL work.

Prefer one atomic multi-file publication where tooling supports it. Append-only history is durable authority; moving latest/state pointers are caches unless a role-specific contract says otherwise.

## Science vs integration

Always keep these four questions distinct:
1. component function;
2. SYSTEM_BUILD/integration viability;
3. composition/interaction contribution;
4. scientific novelty.

SYSTEM_BUILD and Forge observations are non-evidentiary unless a fresh prospective scientific object is separately created under Analyst authority. Build success is not scientific novelty. Component reduction does not automatically reduce the integrated system.

## Minimal-context rule

Read only the state necessary for the current role and task. Do not recursively ingest all historical Human Directives, all scheduler prompts, or every ops branch when an active index/current generation is sufficient. Expand into history only when needed to resolve a conflict, provenance issue, or integrity question.
