# FAST FORGE history — pre-semantic concept graph closure probe

- schema_version: `2`
- generation_id: `FORGE-20260923T213223+0900-V03-CONCEPT-CLOSURE-R99`
- produced_at: `2026-09-23T21:32:23+09:00`
- worker_role: `FAST_FORGE`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- status: `FORGE_DEAD_END`

## Freshness and ownership

Re-fetched Evidence Analyst R99, current MAIN H7 blocked-sidecar report, candidate #35 ownership, Literature R39, Independent Audit R8, Methodology R90, Utility R99 state, Control R43, stable main, and prior Forge state before selection. H7 integrity remediation and candidate #35 preserve-before-read/provenance work remain MAIN-owned. Candidate #34 remains terminal for the exposed object. No protected or one-way surface was touched.

Literature R39 is genuinely new but is specifically about candidate #35 intervention realism/reachable-state causal abstraction, so Forge did not appropriate that MAIN/immediate-successor surface. A separate central-theory scan found one bounded independent pre-semantic formation question in stable `v03_seed`: whether the proto-concept former can create apparently compositional multi-member candidates from pairwise closure alone.

## Forge object

- forge_id: `FORGE-V03-CONCEPT-GRAPH-CLOSURE-01`
- question: Can `OnlineConceptFormer` create a multi-member proto-concept when not all member pairs ever co-occur, and does any residual remain beyond ordinary overlap-coefficient graph clustering?
- why_now: independent central-theory/pre-semantic surface, no MAIN dependency, not a rerun of #34/#35/H7, and not present in prior Forge dead-end inventory.
- branch: `null` (read-only exact-source inspection plus synthetic exact-logic diagnostics; no repository code mutation)

### Prototype A — bridge closure

Exact stable-source rule inspected at `src/sparkbrain/v03_seed/concepts.py`: pair association is `pair_count / min(feature_count_left, feature_count_right)` and eligible edges above threshold are collapsed with connected components.

Synthetic diagnostic: observe `{A,B}` three times, then `{B,C}` three times under defaults. Final marginals are `A=3, B=6, C=3`; pair counts are `AB=3, BC=3, AC=0`. The implementation-level calculation yields `assoc(AB)=1.0`, `assoc(BC)=1.0`, `assoc(AC)=0.0`, yet connected-component closure creates one `(A,B,C)` candidate with mean pair strength `2/3`.

Observation: a 3-member candidate can exist although A and C never co-occurred.

### Prototype B — rare-subset association

Synthetic diagnostic: observe `{A}` 97 times, then `{A,B}` three times. Final marginals are `A=100, B=3`, pair count `AB=3`. Because the denominator is the smaller marginal, `assoc(AB)=3/min(100,3)=1.0`; a two-member `(A,B)` candidate is admitted although only 3% of A observations include B.

Observation: the association behaves as an overlap/subset coefficient, not mutual predictiveness or symmetric conditional co-occurrence.

## Ordinary reduction

Strongest reduction: ordinary overlap-coefficient edge construction plus graph connected-component transitive closure. Prototype A is exactly the expected chaining/percolation behavior of thresholded pairwise graphs; prototype B is exactly the expected behavior of dividing intersection count by the smaller marginal. No additional semantic/compositional mechanism is required.

The source already describes these outputs as proto-concept candidates rather than semantic concepts. These diagnostics therefore expose a bookkeeping/clustering property, not a residual mechanism.

## Disposition

- status: `FORGE_DEAD_END`
- dead_end_reason: `ORDINARY_OVERLAP_COEFFICIENT_PLUS_CONNECTED_COMPONENT_CLOSURE_FULLY_EXPLAINS_OBSERVATIONS`
- promotion_reason: `null`
- promotion_proposal: `false`
- Utility request: `null`
- MAIN collision check: `PASS_NO_COLLISION`

No canonical candidate ID, claim ceiling, PRE_FORMAL readiness, lifecycle state, evidence authority, scientific preserve authority, or FORMAL authority was created.

## Exact refs

- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- exact inspected source blob: `src/sparkbrain/v03_seed/concepts.py@4567f97914438eb559d8b9c0619a8759a666d097`
- Evidence Analyst: `EVA-20260923T210010+0900-R99-6F2B8C14@59dbcdc2e3541e78a64f64e16fa0be5ef38efc26`
- MAIN durable latest generation: `MAIN-20260923T205800+0900-PRIMARY-H7-FORMAL-R5-R98-BLOCKED-SIDECAR` (`reports/orchestrator/main/latest.md` blob `e4bd27d3188e66563084e449a608aa8c179c52fd`)
- candidate #35 exact head avoided: `research/main-cand35-queue-free-subthreshold-architecture-r96-cycle3@8ea6581544c642ad74f1a95955ab2c5f795afccc`
- H7 exact science head avoided: `research/main-h7-formal-r5-runtime-identity-r88-cycle12@2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`
- Literature R39: `741becd60d3e7dc8f97cedf1347c42c769092011`
- Independent Audit R8 latest blob: `0afe416906713bc4b04eec34cd8a0035ecacbc1f`
- Methodology R90: `ac7214f842c04f97d666ed4a1056ac3904427e61`
- Utility R99: `30b5cf5ed45cd4aa4919720897949f6ee1434bdc`
- Control R43: `1592c3b52a8a545aa2503fd4618c0a761921ef1e`
- previous Forge state blob: `1ac1997bdac3263b44aa467eb397707a46bc76f8`

## Hard floor

No PRE_FORMAL/FORMAL identity, STARTED, official TEST/scoring, held-out/protected target access, candidate #35 response, consumed identity rerun/retune/rescore, evidence/formal/sealed/freeze/preserve mutation, scientific branch mutation, research merge, or result-bearing workflow occurred.

Cumulative metrics after this run: runs `10`, prototypes attempted `12`, dead ends `10`, interesting retained `0`, promotion proposals `0`, later admissions `0`, duplicate/rescue rejects `9`, ownership collisions `0`, ordinary-reduction rejects `10`.
