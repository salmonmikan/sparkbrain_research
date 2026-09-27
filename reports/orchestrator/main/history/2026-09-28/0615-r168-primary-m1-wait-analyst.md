# MAIN PRIMARY R168 - M1 exact-head authority wait

- Generated at: `2026-09-28T06:15:00+09:00`
- Generation: `MAIN-20260928T061500+0900-PRIMARY-R168-M1-WAIT-ANALYST`
- Execution mode: `PRIMARY`
- Work mode: `SYSTEM_BUILD`
- Build ID: `BUILD-SB-M1-001-INTEGRATED-CONTINUOUS-REVISION-PILOT`

## Freshness and authority

- Policy main: `fe2bd06139fa36b7a8b28d55bebd795db924749f`
- Human Directive index head: `8ce979b9ec0bc7eede5225c0403698f8886d3e8d`
- Human Directive index blob: `1ba1e173344f36e14d0e21e6f3e823254e031f7d`
- Directive delta from MAIN R167: none
- Durable Evidence Analyst head: `195ca2d230928c7cada86e51d4f04b25904ffc04`
- Durable Analyst generation: `EVA-20260928T045927+0900-R161-M1-ROLLING-CONTRACT-SB002-INTEGRITY`
- Current Control head: `c155cf09495a25bff87868aaba1b90bb06459310`
- Current Control generation: `CTRL-20260928T055408+0900-R103-M1-BUILT-WAIT-ANALYST`

The current active directives and Control state continue to prioritize Integrated Prototype Milestone 1. They do not replace the Analyst allocation or remove its explicit final stop boundary.

## Exact working object

- Branch: `system-build/ipm1-continuous-revision-20260928`
- Head: `512f21a6134b5d68351e33a7c6eecb8fa3e4550c`
- Tree: `10d252a52abdafed7806fc81b39ee8ba126713a9`
- Exact-head CI: run `36348434677`
- Python 3.11: success
- Python 3.13: success
- Open PR from the branch: none

All four R161 rolling milestones remain complete. The exact branch identity and CI are unchanged from R167. No new defect, branch drift, or competing Relay allocation was observed.

## Decision

R161 explicitly requires MAIN to stop after M1.4 at the final exact head and return to Evidence Analyst before creating a PR or merging. No newer durable Analyst generation exists. MAIN therefore performed no code change, PR creation, merge, workflow dispatch, scientific execution, or branch mutation.

This is a concrete unavailable-authority boundary, not generalized caution and not a mandatory-review wait. Mandatory code review is not being used as a gate.

## Classification

- built: `true`
- bounded functionally verified: `true`
- comparatively supported: `false`
- composition contribution: `NOT_ESTABLISHED`
- scientifically novel: `false`
- scientific credit: `0`
- evidentiary status: `NON_EVIDENTIARY_BUILD`
- new build result this generation: `false`
- new scientific result: `false`

FLY-0 remains isolated Forge work with no SB003 allocation and is not mixed into M1.

## Stop and next action

Stop reason: `R161_FINAL_M1_4_EXACT_HEAD_BOUNDARY_NO_NEW_DURABLE_ANALYST_AUTHORITY`.

Next action: Evidence Analyst must reconcile exact head `512f21a6134b5d68351e33a7c6eecb8fa3e4550c` and explicitly dispose PR/merge authority. If a fresh durable authorization appears, MAIN may act only on the exact authorized identity and repository rules.

