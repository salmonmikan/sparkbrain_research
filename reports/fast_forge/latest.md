# SparkBrain Fast Forge — continuous scope-revision interaction ablation

- schema_version: 2
- generation_id: FORGE-20260927T194635+0900-CONTINUOUS-SCOPE-REVISION-ABLATION-CI-CLEAN
- produced_at: 2026-09-27T19:46:35+09:00
- forge_id: FORGE-CONTINUOUS-SCOPE-REVISION-ABLATION-A
- status: FORGE_INTERESTING
- recommended_handoff: SYSTEM_BUILD_INPUT
- branch: forge/20260927-continuous-scope-revision-ablation-a
- exact_prototype_head: 30b3179752200c5b5c1a04d64d412c00578aa9f1
- ci_run: 36313445949
- ci_result: SUCCESS
- evidentiary_status: NON_EVIDENTIARY_NONCANONICAL_FORGE
- scientific_credit: 0
- new_scientific_result: false

Added a continuous synthetic interaction-ablation harness for the retained R6 integration loop. Both arms run the same internal scope router, allocator, coverage guard and transaction boundary. The connected arm stores evidence in the selected scope; the cut arm redirects the same evidence to one Assembly-wide overlay.

Across an A/B/A/B return stream, both arms created/reused the same two scopes and committed 4/4 steps. Connected queries recovered A for the A context and B for the B context. The cut arm abstained for both after contradictory support mixed globally. In a single-context control, both arms selected A.

New tests passed 6/6 and the related chain passed 65/65 locally. Exact prototype head `30b3179752200c5b5c1a04d64d412c00578aa9f1` passed GitHub CI `36313445949` on Python 3.11 and 3.13 with lint, readiness, full tests and bundle validation.

This reduces to ordinary context-keyed state separation versus a shared accumulator. It is a hand-constructed fixture with fixed uncalibrated components, no established system comparator, no resource match and no noise/overlap stress. Usefulness does not establish general composition contribution or scientific novelty.

RD006 R153/R161, SB001 and all scientific refs remain untouched.

History: reports/fast_forge/history/2026-09-27/1946-continuous-scope-revision-ablation-ci-clean.md

