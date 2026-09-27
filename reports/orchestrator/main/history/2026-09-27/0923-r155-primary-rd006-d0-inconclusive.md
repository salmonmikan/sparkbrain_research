# MAIN PRIMARY R155

schema_version: 2
generation_id: MAIN-20260927T092301+0900-PRIMARY-R155-RD006-D0-INCONCLUSIVE
generated_at: 2026-09-27T09:23:01+09:00
execution_mode: PRIMARY
work_mode: SCIENCE
status: OPEN_DEVELOPMENT_D0_INCONCLUSIVE_STOP
candidate_id: RV02-RD006-EXTERNAL-LEARNING-REACHABILITY-A
identity_namespace: rv02-rd006-external-learning-reachability-a-v1
development_phase: OPEN_DEVELOPMENT
claim_ceiling: SYSTEM
analyst_generation_id: EVA-20260927T070206+0900-R144-RD006-BRANCH-LIT45-FORGE-HANDOFF-RECONCILED
analyst_authority: analysis/orchestrator/history/2026-09-27/0702-R144.md
branch: research/rv02-rd006-external-learning-reachability-a
result_head: 49b91ca801522f3d6685ebd22097a1e64f9234c9
corrected_source_head: b4fbd9cc92f9e9d02f4ec1ff69084ab31f924b0c
result_ci_run: 36282136143
result_ci: SUCCESS
matrix_status: D0_INCONCLUSIVE_BOUNDED_EXPLOSION
evidentiary_status: DEVELOPMENT_ONLY_ZERO_CONFIRMATORY_CREDIT
new_scientific_result: false
new_development_result: true
formal_execution: false
held_out_execution: false
capability_scoring: false
scientific_credit: 0

MAIN implemented and executed the R144-allocated Stage D0 comparison at the exact fixed seed, scale, topology degree, threshold, gain, stimulus and lag gate. Ordinary external learning was OFF versus ON; hidden-return learning remained OFF in both arms. RD005 stayed frozen and consumed.

The first source-bound development attempt at `1a9779c5f0e72f9f4f1cac08442256f351e83cd4` stopped at the event ceiling before closing an artifact. Its STARTED manifest and `FAILED_INCOMPLETE_ENGINEERING` record are preserved; it is not a capability negative. A science-invariant harness correction at `b4fbd9cc92f9e9d02f4ec1ff69084ab31f924b0c` converted the safety ceiling into an explicit bounded diagnostic without changing the scientific factors.

The corrected six-family matrix completed. ON-arm ordinary-update counts were 44, 44, 44, 36, 112 and 76. ON-arm distinct hidden-source counts were 0, 2, 1, 5, 3 and 7. No arm produced any eligible hidden-source to current-visible-return certificate within 0.5–6.5 ms; maximum eligible sources at return was zero throughout. The opposing-reversal ON arm hit the bounded event ceiling after 32/48 clocks, so the matrix is inconclusive rather than a complete zero-reachability negative.

The closed artifact is preserved at `artifacts/rv02_rd006/external_learning_reachability_a_v1/attempt-002/artifact.json.gz`. Canonical artifact SHA-256 is `c27951973b25a83ea3a23ce16b97e6634ac513929aee605c8af417410e12209c`; compressed file SHA-256 is `f7ae77d7f8020788d33dcf97aac4333ca98af149b1e8dcef996298559cbe3f9e`; uncompressed file SHA-256 is `976ce2f52ecad1177d644270282482243a70fa3fa0f50864dd08a44df6bc5c5c`. Independent branch readback and exact-head CI succeeded.

integrity_state: RD005 remains consumed and unopened; no FORMAL identity was rerun, retuned, rescored or redispatched; E0/E1/ES, scale expansion and reservoir/resource-matched comparisons remain unauthorized.
stop_reason: D0_MECHANISM_SURFACE_NOT_DEMONSTRATED_AND_ONE_ARM_BOUNDED_INCOMPLETE
next_action: Evidence Analyst must reconcile the durable D0 outcome and decide whether to stop RD006 or prospectively allocate a fresh science-invariant revision. MAIN must not advance E0/E1/ES or scale work without new Analyst authority.
scheduler_state_changed: false
