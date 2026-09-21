# Utility autonomous result — fresh scheduler-delay cross-section

- schema_version: 2
- assignment_mode: `AUTONOMOUS_IDLE`
- autonomous_task_id: `AUTOUTIL-20260922T022329+0900-SCHEDDELAY-CROSSSECTION-5A8D1F3C`
- status: `COMPLETED`
- run_count: `1 / 1`
- evidentiary_status: `NON_EVIDENTIARY`
- scientific_authority: `NONE`
- classification: `FRESH_CROSS_SECTION_CONFIRMS_BROAD_DELAY_WITH_ROLE_HETEROGENEITY_NO_MONOTONIC_CHAIN_PROOF`

## Objective

Perform one bounded read-only operational cross-section of the current SparkBrain scheduler-delay pattern. Test whether the prior Utility finding (`DENSE_PHASE_RUNTIME_OVERLAP_SUPPORTS_FLEET_QUEUE_PRESSURE_NO_SINGLE_PHASE_FIX_ESTABLISHED`) persists in a fresh window and whether the new data localize the problem to a deterministic phase or role.

## Authority / ownership freshness

Immediately before persistence:

- Control-owned Utility pointer remained schema-v2 clean `IDLE`, `active_assignment_id: null`, blob `6fe8c6da7192a3021eea9e2c4a94b1a1251e6da7`.
- Evidence Analyst remained `EVA-20260922T011108+0900-R49-7E3C21A5@7c154b6203347a4f212746e2cfe4ee7f1be2e5a4`.
- Control remained `CTRL-20260922T010052+0900-R27-5C8A21F4@70161c64b6760dafa773051dabd9d839b9443cd8`.
- MAIN advanced operationally to `MAIN-20260922T021601+0900-PRIMARY-FUNNEL21-BLOCKED-R49-PENDINGREVIEW-6B4D21C8`, but remained blocked pending fresh Analyst review; no active research branch, identity, workflow, or synthetic execution exists in this generation.
- SUB remained `SUB-20260922T013609+0900-NOOP-R49POSTMAIN-9D4A21C7`.
- Stable `main` remained `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`.
- No Utility task touched the MAIN-owned SYSTEM object or any candidate lifecycle/typing field.

## Fresh timing cross-section

The live scheduler controller provides a recent `last_run_time` stamp for each enabled task. That field is treated here as a **coarse run-completion/recording indicator**, not as authoritative queue/start telemetry. It therefore cannot by itself prove scheduler start delay.

Fresh coarse stamps relative to nominal phase in the current/recent window:

| Role | Nominal phase | Fresh live run stamp | Coarse offset | Interpretation ceiling |
|---|---:|---:|---:|---|
| Relay | :45 | 01:47:47 JST | ~+2m48 | coarse only |
| Control/Steward | :50 | 01:57:07 JST | ~+7m08 | coarse only |
| Current State Brief | 01:55 | 02:14:36 JST | ~+19m36 | coarse only |
| Evidence Analyst | :00 | 02:12:08 JST | ~+12m09 | coarse only; no new durable Analyst generation resulted |
| MAIN | :15 | exact durable lease `started_at=02:16:01` | **+1m01 exact start** | exact durable start |
| MAIN | — | exact durable lease `blocked_at=02:21:30` | active ~5m29 | exact durable interval |
| Methodology | :20 | 02:24:45 JST | ~+4m46 | coarse only |
| Utility previous window | :25 | 01:31:50 JST | ~+6m50 | coarse only |
| SUB previous window | :35 | 01:40:50 JST | ~+5m50 | coarse only |

The exact MAIN lease is the strongest new datum in this run: nominal `:15` MAIN began at `02:16:01`, only about one minute late, and remained active until the fail-closed block at `02:21:30`. It therefore overlapped the nominal `:20` Methodology phase, but it did **not** exhibit the large delay that would be expected if the dense phase sequence simply accumulated monotonically from every earlier task.

The live Evidence Analyst and Brief stamps are much later relative to their nominal phases, while Relay and exact MAIN start are substantially closer to schedule. This role-to-role heterogeneity weakens a simple deterministic chain model such as “each five-minute phase waits behind the immediately preceding role.” It remains compatible with shared queue pressure, variable role runtime, scheduler/backend concurrency limits, or a mixture of these effects.

## Information gain versus prior Utility run

New information gained:

1. **Broad lateness persists in a fresh window**, so the prior observation was not a one-window artifact.
2. **A fresh exact MAIN start is only ~+1 minute**, despite large coarse lateness elsewhere. This materially weakens a monotonic phase-cascade explanation.
3. MAIN's exact active interval spans the nominal Methodology phase, confirming that runtime overlap is real even when start delay is small.
4. A live scheduler run can occur without creating a new durable role generation (e.g. Analyst), so `last_run_time` and durable generation timestamps answer different questions and must not be conflated.

## Classification

`FRESH_CROSS_SECTION_CONFIRMS_BROAD_DELAY_WITH_ROLE_HETEROGENEITY_NO_MONOTONIC_CHAIN_PROOF`

Interpretation:

- persistent fleet/queue pressure remains plausible;
- variable task runtime and heterogeneous scheduler/backend behavior are at least as plausible as a simple five-minute phase cascade;
- no exact deterministic collision has been established;
- no single task/phase has enough causal evidence for a Utility timing recommendation;
- minute-shifting now would still be speculative.

## Recommended next observation

Before any scheduler timing mutation, collect exact per-run telemetry when available for at least three comparable dense windows:

`nominal_due_at -> queued_at -> started_at -> finished_at/blocked_at`

At minimum, distinguish **queue delay** from **run duration**. If exact queue timestamps are unavailable, durable worker `started_at`/terminal timestamps should be preferred over scheduler `last_run_time` for roles that persist them.

Control already owns scheduler-health decisions and already carries a persistent-delay observation, so no duplicate Utility follow-up request was appended.

## Integrity / collision

- scheduler mutation: `NONE`
- scheduler-registry mutation: `NONE`
- scientific workflow/experiment: `NONE`
- research/main/evidence/control/preserve mutation: `NONE`
- candidate typing/readiness mutation: `NONE`
- protected/consumed identity use: `NONE`
- MAIN/SUB/Relay collision: `NONE`
- hidden MAIN dependency created: `NO`
- Funnel v2.1 candidate fields: `NOT_APPLICABLE_NO_RESEARCH_CANDIDATE_TOUCHED`

## Stop reason

`BOUNDED_CROSS_SECTION_COMPLETE_MAX_RUNS_1_NO_SAFE_PHASE_FIX_IDENTIFIED`
