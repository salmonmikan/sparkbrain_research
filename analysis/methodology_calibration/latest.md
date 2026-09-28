# SparkBrain Methodology Calibration Audit — Latest R141

- schema_version: `2`
- generation_id: `METHCAL-20260928T141807+0900-R141-FLY0-VERIFIED-CALIBRATION`
- generated_at: `2026-09-28T14:18:07+09:00`
- history_path: `analysis/methodology_calibration/history/2026-09-28/1418-R141-fly0-verified-calibration.md`
- overall_classification: `WELL_CALIBRATED`
- new_scientific_result: `false`

M1-002 remains bounded-functionally verified and blocked only on the operational PR route.
FLY-0 now has verified bounded causal use of Observation and prior LocalFeedback at
`8e0b7c859a1f96fbf303173ed6dc974938cca8cc`, but activity/resource/delay matching
and the complete matched replacement ladder remain incomplete. Treat the result as
component function only; no topology, composition, efficiency, biological-fidelity,
novelty or scientific claim is established. Mandatory SYSTEM_BUILD review remains a
non-gate and the scientific hard floor is unchanged.
