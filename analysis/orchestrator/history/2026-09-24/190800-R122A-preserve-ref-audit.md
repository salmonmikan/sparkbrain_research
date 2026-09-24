# Evidence Analyst — R122A Candidate #35 preserve-ref audit amendment

- schema_version: `2`
- generation_id: `EVA-20260924T190300+0900-R122-R43-PROSPECTIVE-ATTRIBUTION-GATE`
- amendment_id: `R122A-CAND35-PRESERVE-REF-RESOLUTION`
- generated_at: `2026-09-24T19:08:00+09:00`
- authority_scope: `EVIDENCE_ANALYST_READ_ONLY_SCIENTIFIC_EXECUTION_APPEND_ONLY_CONTROL_PLANE_PERSISTENCE`
- new_scientific_result: `false`

## Fresh preserve-ref discrepancy

Independent current ref resolution does **not** find `refs/heads/preserve/cand35-r100-batch1-20260923` and does not find a matching `refs/tags/preserve/cand35*` ref. The currently resolvable Candidate #35 raw branch is `raw/cand35-r100-onebatch-20260923@afe4b7ad0f908f3b01eca9e391a2b05cb3be9a7a`.

Commit `afe4b7ad0f908f3b01eca9e391a2b05cb3be9a7a` is itself the commit whose message is `cand35 R100: preserve first bounded raw batch` and contains the preserved development raw payload/provenance. Thus the bytes remain reachable through the current raw branch, but the historical Audit/Theory control-plane text that names `preserve/cand35-r100-batch1-20260923@afe4...` is not a currently resolvable ref and must not be repeated as a current authoritative ref without qualification.

Classification: `GOVERNANCE_PROVENANCE_REFERENCE_DISCREPANCY_NO_SCIENTIFIC_REINTERPRETATION`. Candidate #35 is development-only/zero confirmatory credit and remains terminal SYSTEM. This does not reopen, rerun, rescore, retune, or reinterpret R100. No missing ref is recreated by Evidence Analyst because that would mutate scientific/preservation topology outside this role's allowed scope.

R122 state/latest must use the currently resolvable raw branch for closure provenance and record the historical preserve-ref claim as unresolved. Repository Steward may audit this discrepancy in its own governance lane if desired; Evidence Analyst assigns no scientific credit or scientific invalidation from this control-plane discrepancy alone.
