# SparkBrain Methodology Calibration Audit — Latest

- schema_version: `2`
- generation_id: `METHCAL-20260927T161705+0900-R131-RD006-V3-D0-GATE-CALIBRATION`
- generated_at: `2026-09-27T16:17:05+09:00`
- history_path: `analysis/methodology_calibration/history/2026-09-27/1617.md`
- overall_classification: `SLIGHTLY_TOO_PERMISSIVE`
- new_scientific_result: `false`

Evidence Analyst R150 is otherwise well bounded: exact v3 head, one fixed 12-cell OFF/ON matrix, unchanged resources/ceilings, raw preservation, no capability score or held-out access, and stop for fresh reconciliation.

One material ambiguity must be tightened before interpretation. R150's gate says “two distinct structurally connected hidden sources” in the fixed lag window, while the original D0 contract requires two distinct hidden sources to actually spike and have eligible non-negative edges to the current scheduled visible-return target. Because the static preflight already guarantees structural paths, a structural-only reading would make the dynamic gate tautological.

Count dynamic eligibility only from actual hidden spikes plus eligible edges and observed fixed-window lags; keep static-path counts separate. After meaningful matrix exposure, move v3 to RESULT_EXPOSED_DEVELOPMENT. Gate opening remains development diagnostic only and creates no capability, learning-contribution, composition or novelty credit.

SB001 remains NON_EVIDENTIARY_BUILD. Theory R9 remains NO_PROPOSAL / NO_REVISIT_PROPOSAL. RD005 remains consumed and RD006 v1/v2 remain closed. P0 remains closed as recovered.

No new SparkBrain scientific result.
