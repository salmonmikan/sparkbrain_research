# Active Scheduler Policy Router

This file is a routing document, not the source of truth for time-varying Human Directives.

## Always read

- `AGENTS.md@main`
- `docs/scheduler/COMMON.md@main`
- `docs/scheduler/SCIENTIFIC_INTEGRITY.md@main`
- the current role file under `docs/scheduler/roles/`

## Human Directives

The authoritative Human Directive stream is routed through `ops/human_directives/active.md` on ref `ops/human-directives`. Read that active index **before selecting any directive by ID**. Record the current index/ref identity for freshness, compare it with prior durable state when available, identify newly active/materially changed directives, then fetch only directives whose scope applies to the current role/task plus any directive explicitly referenced by current higher-priority Control/Analyst authority.

If the active index is unavailable, stale identity cannot be established, or a material conflict cannot be resolved, fail closed for the current run rather than falling back to remembered directive IDs.

Scheduler prompts should not permanently duplicate time-varying directives once equivalent behavior is represented in current main policy, role policy, procedural skills, and durable Control/Analyst state.

Current policy families that must be discovered from the active directive stream rather than copied indefinitely into scheduler prompts include:
- GitHub persistence/P0 recovery;
- SYSTEM_BUILD review policy;
- fleet recovery / stop-authority policy;
- future user-approved scheduler governance changes.

Do not treat this routing file as proof that a historical directive is still active. Use current durable directive state.
