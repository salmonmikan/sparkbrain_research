# SparkBrain Methodology Calibration Audit — 2026-09-21 14:22 JST

schema_version: `2`  
generation_id: `METHCAL-20260921T142240+0900-R37-01D67C87`  
produced_at: `2026-09-21T14:22:40+09:00`  
authority_scope: `METHODOLOGY_ADVISORY_ONLY`  
supersedes_generation_id: `METHCAL-20260921T131711+0900-R36-3A8D6F21`

## Result

`MATERIAL_CALIBRATION_UPDATE`

Overall classification remains **`MIXED_CALIBRATION`**.

The material change is an audit-trace defect, not a scientific-gate change. Fresh repository inspection shows the prior R36 `state.json` explicit `authoritative_refs.evidence_tags` list (`evidence/exp-001-*`) does not match the current authoritative repository refs; a matching-ref query for `tags/evidence/exp-001` is empty. Current repository truth is still five annotated evidence refs, but with exact names/tag-object SHAs now rebound in R37 state. This **does not prove evidence-tag mutation**; absent independent ref-history evidence, it establishes that Methodology's exact-ref persistence was inaccurate/stale and must be tightened.

Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. Fresh `formal/*=0`, `sealed/*=0`, tag-based `freeze/*=0`. Current annotated evidence refs are the C19/C19-R2/H5/NI01/PD01 five-ref set and are stored with their tag-object SHAs in `state.json`.

Designated Evidence Analyst is `EVA-20260921T135900+0900-R36-6C3A91E7@6e760daf8b1316489e5565bd799d3f462de390f4`; Control is `CTRL-20260921T125000+0900-R22-7C3A91E4@db53217770b72596bc4beaa3f8c34abea6473311`. Canonical funnel remains `29/29` complete, `MECHANISM=13 / SYSTEM=16`, Architecture `M0/S1`, PRE_FORMAL eligible=`0`, READY=`0`, viable executable MECHANISM=`0`.

The active SYSTEM Architecture object remains `CAND-PREFORMAL-RAW-PRESERVE-SCORER-PIPELINE-INTEGRITY-01`; no PRIMARY cycle result yet demonstrates the prospective four-stage sequence `raw generation -> durable raw preserve+digest -> fixed scorer exact-blob read -> scored preserve`. Thus raw-before-score, preserve-before-score, and durable raw preservation remain **`TIGHTEN`**. READY semantics remain **`KEEP`**, the first READY->PRE_FORMAL transition remains consistent with development readiness, and `HIDDEN_SECOND_FORMAL_GATE=false`.

Fresh SUB opened `NTE-20260921-R34-POST-REPLAY-v1` with check_count=`1`, no candidate/branch/workflow/probe/identity consumption, and the event excluded from candidate/conversion denominators. `NO_COHERENT_MECHANISM_TARGET` remains **`KEEP`** with no escape-hatch evidence. Rolling actual scientific selections remain `MECHANISM / SYSTEM / SYSTEM = 1/3`.

No genuine SYSTEM-over-comparable-MECHANISM priority exception has occurred; first live use remains `INSUFFICIENT_EVIDENCE`. Producer canonical HOLD-enum conformance remains `TIGHTEN`. Scientific admission, novelty/reduction/comparator, stop/reframe, claim-ceiling, fresh-successor, classification-completeness, and candidate-supply gate classifications otherwise remain unchanged.

New gate: **`methodology_authoritative_reference_trace_accuracy = TIGHTEN`**. Each future methodology generation should independently bind exact ref names plus tag-object SHAs; mismatches must be surfaced, not carried forward or silently normalized.

PASS reachability remains **`PRE_FORMAL_REACHED_CLEAN_PASS_PENDING_PROSPECTIVE_PIPELINE_CONFORMANCE`**. Mechanism supply is **`QUALITY_FLOOR_HEALTHY_M13_S16_NO_VIABLE_EXECUTABLE_MECHANISM_OPEN_NO_TARGET_EPISODE_CHECK1_SMALL_N`**. Moving-goalposts risk remains LOW; confidence is HIGH on current state and MODERATE on the historical cause of the ref-name discrepancy.

No Utility request. Hard floor remains **`CONFIRMED / DO NOT RELAX`**. Historical R33 PRE_FORMAL remains terminal; no same-identity rerun/repair/rescore is authorized.
