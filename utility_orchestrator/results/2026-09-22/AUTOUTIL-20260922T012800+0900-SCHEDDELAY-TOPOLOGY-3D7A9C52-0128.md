# Utility Autonomous Result — Scheduler delay topology

- schema_version: 2
- assignment_mode: AUTONOMOUS_IDLE
- autonomous_task_id: `AUTOUTIL-20260922T012800+0900-SCHEDDELAY-TOPOLOGY-3D7A9C52`
- evidentiary_status: `NON_EVIDENTIARY`
- scientific_authority: `NONE`
- max_runs: 1

## Objective

Bounded read-only operational timing diagnostic to distinguish deterministic exact-time scheduler collision from broad fleet queue/serialization pressure. No scheduler mutation, no scientific workflow, and no research/scientific ref mutation were authorized or performed.

## Trigger / freshness

Control R27 recorded a third consecutive broad-delay scheduler-health observation, no exact-time overlap, and no evidence-based single SAFE_AUTO_FIX target. The Control-owned Utility pointer remained clean schema-v2 IDLE with no active assignment before work and again before persistence.

Fresh control-plane / repository context used for collision checks:

- Control: `CTRL-20260922T010052+0900-R27-5C8A21F4@70161c64b6760dafa773051dabd9d839b9443cd8`
- Evidence Analyst: `EVA-20260922T011108+0900-R49-7E3C21A5@7c154b6203347a4f212746e2cfe4ee7f1be2e5a4`
- MAIN: `MAIN-20260922T012600+0900-PRIMARY-FUNNEL21-SYSTEM-LOCALIZE-R49-CYCLE1-7E3C21A5@0ed81db895a5fff57a5a9c66e14554c8d2df79c3`, terminal for this run as `COMPLETED_STOP_PRE_OUTCOME`
- SUB: `SUB-20260922T003526+0900-NOOP-R48MAINOWNED-4F8C21A6`
- Relay: no fresh active continuation observed; MAIN R49 stopped before synthetic measurement and requires fresh Analyst review
- authoritative `main`: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`

The active R49 SYSTEM Architecture object was not used as a Utility target and none of its scientific contract/comparator/resource work was touched.

## Live phase topology

Current enabled SparkBrain scheduler phases observed from live definitions:

| Role | Nominal phase |
|---|---:|
| Evidence Analyst | hourly `:00` |
| MAIN PRIMARY | hourly `:15` |
| Methodology Calibration | hourly `:20` |
| Utility | hourly `:25` |
| External Research/Audit | selected hours `:30` |
| SUB | hourly `:35` |
| Relay | hourly `:45` |
| Control | selected hours `:50` |
| Current State Brief | selected hours `:55` |

There is no exact deterministic same-minute collision among these live core phases. However, busy hours contain a dense `:15 -> :55` chain with repeated 5-minute gaps.

## Current timing cross-check

Using scheduler-recorded last-run timestamps only as a coarse operational-lag indicator (not as a guaranteed queued/start timestamp), the latest visible runs were later than the immediately due nominal slot across many roles:

| Role | Approx. lag vs latest due slot |
|---|---:|
| Utility | +2m58s |
| MAIN prior scheduler record | +8m35s |
| SUB | +6m22s |
| Relay | +9m26s |
| Methodology | +6m12s |
| Evidence Analyst | +19m14s |
| Control | +14m09s |
| Current State Brief | +8m46s |
| External Research/Audit latest selected-hour run | +38m48s |

These figures are intentionally not interpreted as exact scheduler start delay because the automation runtime's `last_run_time` semantics may include execution timing rather than queue-start timing.

A stronger same-window durable observation exists for MAIN R49: its lease records `started_at=2026-09-22T01:19:00+09:00` for the nominal `:15` MAIN phase and `completed_at=01:26:00+09:00`. Thus this concrete MAIN run started about four minutes after nominal and occupied a seven-minute execution window that crossed both the nominal Methodology `:20` and Utility `:25` phases.

## Finding

Classification: `DENSE_PHASE_RUNTIME_OVERLAP_SUPPORTS_FLEET_QUEUE_PRESSURE_NO_SINGLE_PHASE_FIX_ESTABLISHED`

The current evidence does **not** support an exact-time collision diagnosis. It does support a more specific operational hypothesis than the prior generic broad-delay signal: normal multi-minute task runtimes are long enough to overlap the subsequent 5-minute phase-separated roles, so the nominally collision-free schedule can still create a rolling execution/queue-pressure band.

The pattern is fleet-wide rather than isolated to one role. Therefore shifting one task by a few minutes is not presently evidence-based: it could simply move contention to an adjacent phase. In particular, the current MAIN R49 01:19–01:26 execution overlapped both `:20` and `:25`, demonstrating why a five-minute phase separation is not equivalent to runtime isolation.

This strengthens Control R27's `NO_CHANGE` decision: no SAFE_AUTO_FIX target is established from this cross-section. A structural cadence/role redesign would exceed Utility authority and, where material, requires the existing Control/user-approval path.

## Recommended next operational evidence

Before any phase change, scheduler-health governance should collect or persist exact `nominal_due_at`, `queued_at` (if available), `started_at`, and `finished_at` for at least three comparable dense windows. The decision question should be whether delay accumulates monotonically through the `:15–:55` chain (shared queue/serialization), or is concentrated in one role independent of predecessor runtime. This can identify a real SAFE_AUTO_FIX target without speculative shifting.

No follow-up Utility request was appended because Control already owns scheduler-health governance and has the broad-delay issue open; duplicating that control-plane work would add churn rather than information.

## Funnel / integrity / ownership

- research candidate targeted: no
- Funnel v2.1 typing changed or interpreted: no
- PRE_FORMAL / FORMAL entered: no
- scientific workflow dispatched: no
- consumed/protected identity used: no
- main/research/evidence/control/preserve/formal/freeze ref mutated: no
- scheduler mutated: no
- scheduler registry mutated: no
- MAIN/SUB/Relay critical-path work touched: no
- Utility-owned persistence only: yes

## Stop

`COMPLETED_ONE_BOUNDED_AUTONOMOUS_DELAY_TOPOLOGY_DIAGNOSTIC_MAX_RUNS_REACHED`
