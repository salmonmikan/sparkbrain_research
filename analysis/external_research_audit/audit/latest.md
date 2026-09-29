# Independent Audit R13 — FLY-0 reconciliation admission gate

generation_id: `AUD-20260929T222507+0900-R13-FLY0-RECONCILIATION-GATE-7C4A91E3`
new_scientific_result: false

Exact source/test head `41e021fef824e0bc899184c9d102d69a19e58255` is CI-green in run `36563852129` on Python 3.11/3.13.

The gate is SYNTHESIS_OK as a bounded transaction-admission/idempotence primitive, but its generic “consumer-side exactly-once” wording is too broad: deduplication is keyed only by transaction ID. The same exact signal can be reconciled again under a different transaction ID and higher sequence, advancing the watermark and potentially suppressing a legitimate subsequent outcome as out-of-order. Same transaction + same signal + conflicting sequence is also silently treated as a duplicate rather than an inconsistent proof.

Full R24/R22 promotion therefore remains INSUFFICIENT_SYSTEM_TEST. Add canonical proof identity / cross-transaction signal dedupe and adversarial replay tests, while retaining the separate upstream receipt validator required by Theory R24.

No science changes. Control R125 / Analyst R170 remain authoritative; M1 is not stopped and SB003 remains `ALLOCATED_CONDITIONAL_INACTIVE`. Scientific credit remains 0.

History: `analysis/external_research_audit/audit/history/2026-09-29/2230-INDEPENDENT_AUDITOR.md`
