# SparkBrain Human Directives

This directory on the `ops/human-directives` branch is the durable **human-originated intent/proposal channel** for the SparkBrain programme.

It is intentionally separate from scientific evidence, Control Brain strategy, Evidence Analyst interpretation,
and Orchestrator execution reports.

## Authority semantics

A Human Directive is **not an automatic command** and is **not scientific evidence**.

Human intent may be incomplete, mistaken, stale, unsafe for scientific integrity, or inferior to a better
repository/research plan. Therefore every active directive must be independently reviewed by Control Brain.

Control Brain may classify a directive as exactly one of:

- `ACCEPT` — the intent is sound enough to pass downstream for normal planning.
- `MODIFY` — preserve the underlying human goal but change scope, sequencing, implementation, or ownership.
- `DEFER` — valid or potentially valid, but not worth acting on yet because evidence, timing, cost, or conflicts make delay preferable.
- `REJECT` — do not execute; explain why the proposal conflicts with evidence, integrity, repository doctrine, research value, or current constraints.

An `ACCEPT` or `MODIFY` decision is still not direct execution authority. It must flow through the normal
Control Brain -> Evidence Analyst -> appropriate execution/governance lane.

## Independence and integrity

Human directives must never override:

- immutable/frozen/formal/evidence results;
- consumed identity / no-rerun boundaries;
- prospective protocol integrity;
- evidence-over-strategy precedence;
- MAIN/SUB collision rules;
- repository safety rules.

If a directive conflicts with current evidence, Control Brain must prefer the evidence and may reject the directive.

## Write policy

Scheduled agents and control-plane workers treat this branch as **read-only**.

They must not rewrite, reinterpret, close, or delete human directives on this branch.
Writes are reserved for explicit human-originated actions, including an assistant acting on an explicit user request.

Control Brain records its disposition on `ops/control-brain-handoff`, not here.

## Files

- `ops/human_directives/active.md` — current human-originated proposals that should be considered.
- `ops/human_directives/history/` — append-only snapshots/details of human directives.
- this file — channel semantics and governance contract.

## Reconsideration

A rejected or deferred directive should not be repeatedly re-opened every cycle unless at least one of these changes:

- the human directive itself changes;
- material repository/scientific evidence changes;
- the blocker or opportunity cost changes;
- Control Brain explicitly records a reason to reconsider.

Human intent informs the programme. It does not bypass the programme's ability to disagree.
