# SparkBrain Methodology Calibration Audit — Latest R145

- schema_version: `2`
- generation_id: `METHCAL-20260929T001532+0900-R145-FLY0-COMPARATOR-SEMANTIC-SURFACE`
- generated_at: `2026-09-29T00:15:32+09:00`
- history_path: `analysis/methodology_calibration/history/2026-09-29/0015-R145-fly0-comparator-semantic-surface.md`
- overall_classification: `WELL_CALIBRATED`
- material_change: `true`
- new_scientific_result: `false`

FLY-0 has a material comparator-fairness clarification. Current head `a3c50403f7c7863b8a78b5ce8f3937eee1113215` is CI-green only because it now exposes the rewired/random-sparse baseline incapability; it is not a repaired four-way acceptance.

The concrete defect is that the structured topology preserves bilateral left/right sensorimotor surfaces while the rewired/random-sparse controls currently preserve role/resource summaries without preserving source/target side. This conflates topology change with task-interface change. Prospectively, comparator randomization must preserve the task-relevant input/output semantic surface in addition to the declared degree/resource envelope.

Analyst R168 correctly keeps SB003 unallocated and routes the defect to Forge repair. This is ordinary known-defect handling, not a mandatory review gate. M1-002 remains independently blocked only by the operational PR-create path. Strict internal activity/resource commensurability remains claim-typed and is not a default gate for ordinary NON_EVIDENTIARY integration.

Canonical science and all one-way hard floors are unchanged.
