# MAIN latest — R37 PRIMARY pipeline-integrity Architecture cycle 1

- schema_version: `2`
- generation: `MAIN-20260921T151412+0900-PRIMARY-FUNNEL21-SYSTEM-PIPELINE-R37-6F3A91C2`
- execution_mode: `PRIMARY`
- Evidence Analyst: `EVA-20260921T145812+0900-R37-4E8C21A6@64c7adf88f807407eb817f3b45d0eb269458f534`
- candidate: `CAND-PREFORMAL-RAW-PRESERVE-SCORER-PIPELINE-INTEGRITY-01`
- lane: `PREFORMAL_RAW_PRESERVE_SCORER_PIPELINE_INTEGRITY_ARCHITECTURE_STATIC_CYCLE1`
- layer / ceiling: `ARCHITECTURE_STUDY / SYSTEM`
- cycle: `1`
- canonical Funnel fields: `preformal_eligible=false`, `preformal_readiness=null`, `hold_class=null`, `hold_reason=null`, `terminal_state=ACTIVE`, `queue_state=ACTIVE`
- `system_priority_exception.used=false`; viable comparable MECHANISM=`0`
- stable source: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- lease: `COMPLETED`

## Static Architecture result

Prospective terminal observation: **`FOUR_STAGE_PIPELINE_FEASIBLE`**.

The repository already contains a complete repository-native precedent for the Analyst-required integrity sequence `RAW_GENERATOR -> DURABLE_RAW_PRESERVE_DIGEST -> FIXED_SCORER_EXACT_BLOB -> SCORED_PRESERVE`.

1. **RAW_GENERATOR — feasible.** The prior R33 PRE_FORMAL harness combines generation and scoring/classification in-process, which explains its canonical `NONCONFORMING_RAW_BEFORE_SCORE` status. The architecture boundary is nevertheless separable before `_classify_surface`; this cycle did not edit or rerun R33.
2. **DURABLE_RAW_PRESERVE_DIGEST — feasible.** H5's bound `preserve_h5_boundary.py` computes SHA-256 digests, creates a fresh no-clobber preservation branch from an exact base commit, copies and re-verifies bytes, pushes the preserve ref, verifies the remote commit, and emits preservation metadata. Repository instance: raw-preserve commit `ce5797eb584344db7a512e585506fb6c59ea475b`.
3. **FIXED_SCORER_EXACT_BLOB — feasible.** H5's one-way workflow independently re-fetches the preserved raw by exact preservation commit, verifies digests/cardinality and that raw has no score/classification fields, and only then calls the bound scorer. Its runner verifies exact package and bound contract/runner/preserver/workflow blobs before scoring.
4. **SCORED_PRESERVE — feasible.** H5 terminal evidence commit `61aff6d74b82b68a326f3d90505d70bcd4071fd5` stores scored report/bindings and explicitly binds the raw-preservation commit and raw SHA, demonstrating the final provenance-preserving scored layer.

This is a **NON_EVIDENTIARY SYSTEM Architecture observation only**. It does not rehabilitate the consumed R33 object, does not make any MECHANISM claim, and does not authorize pipeline implementation, PRE_FORMAL, FORMAL, STARTED, preservation, or scoring. No R33 scientific outcome was reopened or used to redesign science.

## Fresh repository integrity

`main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. The exact authoritative `evidence/*` set remains five annotated tags as rebound by R37; `formal/*`, `sealed/*`, and `freeze/*` tags remain empty. Existing STARTED/control and raw-preserve anchors are unchanged. No research branch was created or modified, no scientific workflow was dispatched, and no identity was consumed.

Run delta: **FORMAL evidence=0 / PRE_FORMAL development evidence=0 / MECHANISM Architecture=0 / SYSTEM Architecture=1 / new identity consumption=0**.

Stop: `R37_STATIC_SYSTEM_TERMINAL_FOUR_STAGE_PIPELINE_FEASIBLE_STOP_FRESH_ANALYST_REVIEW`.

Next: fresh Evidence Analyst must consume and canonicalize this static feasibility result. Until then, do not implement the four-stage pipeline, rerun/repair/rescore the R33 object, or start new scientific execution under this object.
