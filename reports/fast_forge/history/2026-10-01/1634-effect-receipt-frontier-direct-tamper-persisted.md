# Fast Forge — direct tamper coverage persisted

forge_id: FORGE-FLY0-EFFECT-RECEIPT-FRONTIER-GATE
status: FORGE_INTERESTING
evidentiary_status: NON_EVIDENTIARY
canonical_status: NONCANONICAL
scientific_credit: 0
recommended_handoff: NONE_PENDING_EXACT_HEAD_CI_AND_FRESH_ANALYST_RECONCILIATION

Authority was refreshed from current durable policy/state. The gate-level direct tamper test is now present. It mutates observed_token on a copied committed WorldEffectRecord and requires EFFECT_JOIN_REJECTED, no binding, no state advance, and unchanged reconciler/frontier checkpoints.

Test publication succeeded on attempt 4 after three pre-GitHub refusals. Commit: 8e8a31bde26d9640770d30cf999f22447948a8d1. Test blob after readback: fd3018fa239ae863aea5091abf1793264328025f.

Exact-head CI is not yet observed on available workflow/status surfaces, so handoff remains blocked pending CI and fresh Evidence Analyst reconciliation. Previous focused-green head remains 74536fb9e3063c48d68080e392121175037e3215 with CI 36812964770.

Scientific credit remains zero. P0 remains open with root cause unknown. No canonical science, consumed FORMAL identity, immutable evidence, or scheduler state was changed.
