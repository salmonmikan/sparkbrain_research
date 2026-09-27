# MAIN PRIMARY R160 — RD006 v3 preserved-result causal-opportunity audit

schema_version: 2
generation_id: MAIN-20260927T183500+0900-PRIMARY-R160-RD006-V3-CAUSAL-AUDIT
generated_at: 2026-09-27T18:35:00+09:00
execution_mode: PRIMARY
work_mode: SCIENCE
status: RESULT_EXPOSED_DEVELOPMENT_CAUSAL_AUDIT_COMPLETE_WAIT_ANALYST
candidate_id: RV02-RD006-EXTERNAL-LEARNING-REACHABILITY-A
development_phase: RESULT_EXPOSED_DEVELOPMENT
revision: v3-preserved-result-causal-opportunity-audit
claim_ceiling: SYSTEM
analyst_generation_id: EVA-20260927T180100+0900-R152-RD006-V3-POSTRESULT-CAUSAL-AUDIT
new_scientific_result: false
new_development_diagnostic: true
scientific_credit: 0

## Authority and scope

Evidence Analyst R152 authorized one read-only audit of the exact preserved R159
artifact. No dynamics, rerun, retune, rescore, replacement matrix, artifact mutation,
parameter change, capability scoring or held-out access occurred.

The preserved v3 result remains `D0_INCONCLUSIVE_BOUNDED_EXPLOSION`. The audit was
appended to the existing execution branch without changing the result commit or the
artifact bytes.

## Exact refs and verification

- branch: `research/rv02-rd006-external-learning-reachability-a-v3-d0-execution`
- preserved execution source: `8867c0565e25a0c76749c12eec7f4c03238b7aef`
- preserved result: `540fa54f45a8cdc467eb2695270035cb9332f2fb`
- audit head: `b22b58bccdf9538c6f1c741592db4f415d404262`
- audit report:
  `docs/research/RV02_RD006_V3_PRESERVED_CAUSAL_OPPORTUNITY_AUDIT_20260927.md`
- audit payload SHA-256:
  `19d160df7d7e53d3bf8f038e6d5d314026a47f645c488615d146f78661b3c564`
- audit gzip SHA-256:
  `f7515e286b6fc9a60b4553df5b6a4b78e7c9c88f9d29d5850cf69dfed1a9767c`
- original result artifact gzip SHA-256 remained:
  `ad7dc60af79681a30d67f1c0d2a4e39607a8984122f52bf9a65949950772b3f9`
- exact-head CI: `36309642259`, Python 3.11 and 3.13 success
- local static-audit tests: 5 passed
- scoped ruff: passed

Research publication used one atomic Git Data commit/ref-update attempt. Independent
readback verified the branch head, parent, tree, four new blobs and both gzip hashes.

## Exhaustive preserved-clock classification

All 832 planned clocks were assigned exactly one mutually exclusive cause. The 816
inspected clocks were classified from preserved bytes. The 16 unobserved bounded-arm
clocks were identified from the paired preserved OFF schedule and marked only as
ceiling-censored.

| Cause | OFF | ON | Total |
| --- | ---: | ---: | ---: |
| no other source in preserved construction | 188 | 184 | 372 |
| no second hidden spike | 228 | 205 | 433 |
| second spike lacked eligible edge to current target | 0 | 10 | 10 |
| eligible edge but lag outside fixed window | 0 | 0 | 0 |
| eligible sources only on adjacent clocks | 0 | 1 | 1 |
| ceiling-censored | 0 | 16 | 16 |

Complete and bounded cells were kept separate:

- OFF complete: 416 clocks;
- ON complete: 368 clocks;
- ON bounded (`opposing-reversal`): 32 inspected plus 16 censored clocks.

The minimum observed deficit to the fixed two-source gate was one source. Seven ON
clocks had one eligible source; all other inspected clocks were two short. The total
deficit over inspected clocks was 1,625 source-clock opportunities. Censored clocks
were excluded.

The ten same-clock multi-spike failures split into seven complete
`capacity-pressure / ON` clocks and three pre-ceiling `opposing-reversal / ON`
clocks. No second spiking source failed only because of the 0.5–6.5 ms lag window.

The sole adjacent-clock case was `opposing-reversal / ON` event
`rd006-v2-ext-000030`: sources 36 and 37 were eligible on the immediately preceding
and following clocks, not together at the current clock.

## Recommendation boundary

The audit recommends at most one fresh prospective revision with exactly one changed
invariant: `ORDINARY_EXTERNAL_LEARNER_TRACE_BOUNDARY`. Such a revision would allow
prospectively specified `PORT_TO_HIDDEN` ordinary external updates while keeping
hidden-return learning disabled. The two-source gate, lag window, v3 topology and
schedule, threshold, gain, stimulus and resource ceilings would remain fixed.

This recommendation does not authorize implementation or execution. It is a fresh
learner-boundary hypothesis, not a v3 rescue or a prediction of success.

E0/E1/ES, another v3 matrix, ceiling changes, topology/timing changes, scale or
reservoir comparisons and capability scoring remain unauthorized.

stop_reason: PRESERVED_V3_CAUSAL_AUDIT_COMPLETE_WAIT_FRESH_ANALYST_RECONCILIATION
next_action: Evidence Analyst reconciliation of the audit and successor recommendation.
scheduler_state_changed: false
