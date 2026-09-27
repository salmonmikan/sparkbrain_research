# MAIN PRIMARY R163 — RD006 v4 preserved-output return-alignment audit

generated_at: 2026-09-27T23:33:06+09:00
generation_id: MAIN-20260927T233306+0900-PRIMARY-R163-RD006-V4-RETURN-ALIGNMENT-AUDIT
execution_mode: PRIMARY
work_mode: SCIENCE
status: RESULT_EXPOSED_DEVELOPMENT_V4_PRESERVED_AUDIT_WAIT_ANALYST
candidate_id: RV02-RD006-EXTERNAL-LEARNING-REACHABILITY-A
revision: v4-preserved-output-return-alignment-audit
claim_ceiling: SYSTEM
analyst_allocation: EVA-20260927T230711+0900-R157-RD006-V4-POSTRESULT-RECONCILIATION
new_scientific_result: false
scientific_credit: 0

## Authority and collision check

Current main policy, the applicable Human Directives, Analyst R157, MAIN R162,
Control R97, the MAIN lease and Relay collision state were re-fetched. Analyst
R157 remained durable at `ff5246652823ab1c036f489ce3b410ffec37483f` and
allocated exactly one read-only diagnostic over preserved v4 result head
`50112626ef6a4da364e3fa9268e8feb0d723ea7f`. MAIN remained R162 at
`b314b3d08e51a17b0466730784c238d6287716b2`; no competing Relay execution was
present.

No result-bearing execution, rerun, retune, rescore, artifact mutation or result
reclassification was authorized or performed.

## Preserved identity and audit publication

- preserved result head: `50112626ef6a4da364e3fa9268e8feb0d723ea7f`
- preserved result tree: `ef12cc8279b3043ef6dfc2577f155ed4e3bdbb15`
- final audit head: `abbadcd1a803199501a33379d4e9030967a9655c`
- final audit tree: `1642d3e5b849daeed134d9c8cf50ea3ac4a0d107`
- exact-head CI: run `36326067694`, success on Python 3.11 and 3.13
- audit payload SHA-256:
  `0883e5ffc271f2a32eadb232178ef529f7256188f602869d8b5790a603bd55a5`
- rendered audit JSON SHA-256:
  `37cce402dcdd1a816117eca68284ccde48afea26923e2cad359aebf9aa2512a1`
- deterministic gzip audit SHA-256:
  `7eea2a1dff11986e4431366da013ddcea170c190c21c609254ea575552baf589`

Publication used four attempts. Attempt 1 stopped before ref update because the
connector response was parsed incorrectly; readback confirmed the branch was
unchanged. Attempt 2 published commit `31c06fb8d6261535b42ef000a8f5e72873384a8b`
but exact-head CI exposed lint and test-path syntax defects. Attempt 3 published
repair `f24cc2f5a3a3720806bd561a086583d68e00f785`; CI exposed five remaining
line-length violations. Attempt 4 published the final repair, passed independent
readback and exact-head CI. The audit JSON and report content hashes were unchanged
by the two code-only repairs.

## Exhaustive ON-clock classification

All 416 planned ON clocks received one mutually exclusive classification. The
400 inspected clocks were derived only from preserved bytes; the 16 unobserved
opposing-reversal ON clocks were marked ceiling-censored without inferring a
dynamic outcome.

| Cause | Count |
| --- | ---: |
| No second source in preserved construction | 184 |
| No second hidden spike | 205 |
| Multiple spikes but no two eligible current-target edges | 11 |
| Eligible edge but lag outside 0.5–6.5 ms | 0 |
| Eligible identities split across adjacent clocks | 0 |
| Ceiling-censored | 16 |

Seven inspected ON clocks had exactly one eligible hidden source and 393 had
none. No clock had two. The minimum deficit to the fixed gate was one, the
maximum was two, and the summed deficit over inspected ON clocks was 793. The
seven one-source clocks are the same shared-prefix/opposing-reversal surface
retained in the v3 audit; the prior single adjacent-clock classification moves
to a current-target edge failure in v4.

## PORT-to-hidden descriptive linkage

All 58 update target spikes were located by target source identity and target
time inferred from source return time plus recorded lag. Fifty-one target sources
spiked again later; six later appeared as dynamically eligible. Those six occur
only in shared-prefix and opposing-reversal.

This does not identify incremental PORT-to-hidden causality. Hidden spike rows do
not carry the update target event ID, and there is no matched counterfactual
trajectory with a particular update removed. Concurrent network state and other
ordinary updates remain live explanations.

## Trace sufficiency and disposition

The trace is sufficient for return-clock structural/firing/edge/lag/eligibility
classification, immediate-adjacent-clock checks and descriptive same-source
recurrence. It is insufficient for the 16 censored outcomes, a direct hidden
event-ID join, update-removal counterfactuals or the causal contribution of a
specific update.

Disposition: `NO_PROPOSAL`. The preserved bytes do not isolate one fresh
scientific invariant without mixing live explanations. The v4 result remains
`D0_INCONCLUSIVE_BOUNDED_EXPLOSION` with zero confirmatory credit.

RD005 remains consumed and untouched. RD006 v1/v2/v3/v4 remain closed. No
E0/E1/ES, v5 dynamics, second matrix, ceiling change, scale expansion, reservoir
comparison, capability scoring or held-out work was executed or authorized.

stop_reason:
`R157_READ_ONLY_AUDIT_PUBLISHED_NO_PROPOSAL_WAIT_FRESH_ANALYST`

next_action: Evidence Analyst reconciles exact audit head
`abbadcd1a803199501a33379d4e9030967a9655c`.

scheduler_state_changed: false
