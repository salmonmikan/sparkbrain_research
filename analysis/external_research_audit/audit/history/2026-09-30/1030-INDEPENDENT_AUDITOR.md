# Independent Audit R14 — recovery-epoch resynchronization monotonicity

generation_id: `AUD-20260930T103330+0900-R14-RESYNC-WATERMARK-MONOTONICITY`
new_scientific_result: false

The narrow recovery-epoch lineage fence is SYNTHESIS_OK at exact validated head `4c5147a5c39b6c5da8320226de3ddc75d30de6b1` / CI `36620923633`, but authoritative resynchronization remains INSUFFICIENT_SYSTEM_TEST.

`RecoveryEpochFencedReconciliation.resynchronize()` constructs a fresh bounded horizon before resynchronizing, so the pre-resynchronization watermark is not checked. After sequence N has been reconciled, a same-session resynchronization at M<N can move WORLD state and the watermark backward while advancing the recovery epoch. The focused recovery-epoch tests do not cover this case.

Theory R26 already requires monotonic anchor coverage. Before authoritative resynchronization composition, reject same-WORLD/session anchors below the pre-resync watermark with exact state/epoch preservation. A true sequence reset must use an explicit new WORLD/session namespace. Add an adversarial N then M<N resync test and verify no M<k<N receipt can become post-resync forward progress.

Current authority after blind target fixation: Control append-only R132; Evidence Analyst R174; Theory R26; Literature R52; prior Audit R13. R174's narrow optional lineage-fence admission is not invalidated. M1 is not stopped; SB003 remains `ALLOCATED_CONDITIONAL_INACTIVE`; scientific credit remains 0. P0 remains OPEN / root cause UNKNOWN.
