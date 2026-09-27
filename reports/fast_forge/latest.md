# SparkBrain Fast Forge — scope-revision boundary stress probe

- schema_version: 2
- generation_id: `FORGE-20260927T204727+0900-SCOPE-REVISION-BOUNDARY-STRESS-CI-CLEAN`
- produced_at: `2026-09-27T20:47:27+09:00`
- forge_id: `FORGE-SCOPE-REVISION-BOUNDARY-STRESS-A`
- status: `FORGE_INTERESTING`
- recommended_handoff: `SYSTEM_BUILD_INPUT`
- branch: `forge/20260927-scope-revision-boundary-stress-a`
- exact_prototype_head: `89a51ba5a9506afc0f0f77b7ecccca224cd42ce4`
- ci_run: `36316697157`
- ci_result: `SUCCESS`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- scientific_credit: 0
- new_scientific_result: false

The prior connected-versus-cut scope-revision ablation was extended with three fixed boundary cases. Under moderate overlap and small within-cluster jitter, both arms formed the same two scopes; the connected arm recovered A/B while the cut arm abstained, and both rejected an ambiguous midpoint. With observations inside the fixed reuse radius, only one scope formed and the connected arm failed to recover B. With one conflicting A-cluster label, the connected arm retained the two per-scope majorities while the cut arm returned the global majority for both contexts.

New tests passed 5/5, the related chain passed 49/49 and all Forge tests passed 114/114 locally. Ruff, compileall, readiness and bundle validation passed. Exact prototype head `89a51ba5a9506afc0f0f77b7ecccca224cd42ce4` passed GitHub CI `36316697157` on Python 3.11 and 3.13 with lint, readiness, full tests and bundle validation.

This reduces to nearest-centroid routing with a reject option and per-key evidence accumulation. The within-radius failure is an explicit limitation: the prototype is not general latent-cause discovery. It remains hand-built, uncalibrated and unmatched against system comparators; no general composition contribution, robustness or scientific novelty is established.

RD006 v4, SB001, MAIN/Relay ownership and all scientific refs remain untouched.

History: `reports/fast_forge/history/2026-09-27/2047-scope-revision-boundary-stress-ci-clean.md`
