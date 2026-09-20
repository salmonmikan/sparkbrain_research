# SparkBrain Research Orchestrator MAIN — Funnel v2.1 explicit hold

- timestamp: `2026-09-20T15:14:32+09:00`
- worker_role: `main`
- execution_mode: `PRIMARY`
- generation_id: `MAIN-20260920T151432+0900-PRIMARY-FUNNEL21-HOLD-A84D6C2F`
- consumed Analyst generation: `EVA-20260920T150234+0900-R15-8F3C1A72`
- consumed Analyst state commit: `095caeb07c23094bf9fc68c8e7022f88d45baa74`
- Analyst branch tip observed: `ad8290dfab6d79be984f960d48dcf34a8213aefb`
- research_layer: `NONE`
- main_lane: `LOWER_FUNNEL_MAIN_HOLD_NO_COHERENT_CENTRAL_OBJECT`
- lease: `COMPLETED` after persistence finalization

## Decision

Fresh Analyst authority still allocates no MAIN scientific object. Architecture is EMPTY_HOLD with active/queued MECHANISM=0/SYSTEM=0; PRE_FORMAL has eligible=0 and READY=0; FORMAL has no fresh identity, STARTED, TEST/scorer, or preserve authority. Current-object Funnel-v2.1 fields are therefore intentionally null rather than collapsed into a generic HOLD. `system_priority_exception.used=false`.

The material delta is SUB `CAND-V05-NONLEARNING-EVAL-ORDER-DEPENDENCE-01`, a SYSTEM Discovery object. Exact research head `4ed6de26ac0bf584189823a64abf6532b3291f59` and CI run `35492181051` were independently re-fetched; CI is `completed/success`. The prospectively fixed forward-vs-reverse comparison matched exactly at the supported 220 ms spacing for the selected keyed observables and aggregate metrics. Analyst disposition is `REJECT`, `claim_ceiling=SYSTEM`, `preformal_eligible=false`, `terminal_state=TERMINAL_FOR_CURRENT_OBJECT`, `queue_state=NOT_QUEUED`. This is NON_EVIDENTIARY reproducibility/testbed information only, not a global order-invariance result.

## Integrity / refs

Stable `main` independently re-fetched as `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. Five authoritative `evidence/*` refs remain exact. Matching `formal/*`, `sealed/*`, and `freeze/*` tag prefixes are empty. H5 control STARTED remains `058e90227cd48e1c10c6ecbaed01efdec1217d0e`; H5 raw preserve remains `ce5797eb584344db7a512e585506fb6c59ea475b`. PR #148 and PR #149 remain open/unmerged. No ref disagreement, collision anomaly, or allocation ambiguity was found, so FAST PATH was sufficient.

## Funnel snapshot

Material portfolio is MECHANISM=4 / SYSTEM=6. Terminal current objects=9, nonterminal hold=1. `CAND-H7-RESP-01` remains the only nonterminal MECHANISM hold and is still `preformal_eligible=false` / `NOT_READY` because no native executable responsibility-sensitive object, supported reachability, fixed equal-privilege comparator, and fixed falsifier exist. Rolling theory-backward selection is 2/3; no quota-driven mechanism work is authorized.

## Execution / evidence status

MAIN performed no scientific branch mutation, workflow/experiment dispatch, PRE_FORMAL work, MECHANISM Architecture study, SYSTEM Architecture study, FORMAL identity/TEST/STARTED/acquisition/preserve/scoring, research merge, or Utility request. New FORMAL scientific evidence=0; PRE_FORMAL development evidence=0; MECHANISM Architecture observations=0; SYSTEM Architecture observations=0. No identity was consumed in this run.

## Stop / next action

stop_reason: `ANALYST_STOP_NO_CURRENT_MAIN_OBJECT_NO_COHERENT_CENTRAL_OBJECT`

MAIN remains intentionally scientifically idle. Next action is to consume a fresh Analyst generation only when it prospectively allocates a coherent executable MECHANISM object or a high-value SYSTEM object, then re-read exact claim ceiling, readiness, hold dimensions, SYSTEM-priority exception, refs, identities, and collision state before any mutation or dispatch. SUB keeps independent bounded Discovery ownership.

Persistence: lease was acquired first; state/latest/history/final lease are MAIN-owned control-plane writes only on `ops/orchestrator-run-report`.
