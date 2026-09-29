# Evidence Analyst R173 — upstream validator admission and bounded-horizon boundary

generation_id: EVA-20260930T020101+0900-R173-UPSTREAM-VALIDATOR-ADMISSION-R25-HORIZON
generated_at: 2026-09-30T02:01:01+09:00
role: EVIDENCE_ANALYST
mode: READ_ONLY_ADJUDICATION
new_scientific_result: false
scientific_execution_authorized: false

## Freshness and persistence reconciliation

Main policy was re-fetched explicitly from main@59fc994b39d0ba02682e972161bb46801592d25b. Human Directive freshness is unchanged at ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d / active-index blob 1ba1e173344f36e14d0e21e6f3e823254e031f7d; there is no directive delta from durable R172.

Durable Analyst authority before this generation is verified R172 at ops/evidence-analyst-handoff@c7eeb100609dc9419e340752ff2fe2f924cd2f79. Request EA-R172-20260930T005826JST is present on ops/evidence-persistence-requests@5eb26843a02304c276719862cce385c04f420143; receipt binds that request commit, workflow 36595994907 and persistence_complete=true. No newer Analyst persistence request exists before this generation.

Current append-only Control authority is R129 on ops/control-brain-handoff@a48bd4d0284eed9a05b9a564f41df33166184f05; latest is R129 while state remains R128, so append-only history is authority and state lag is cache debt only. PRIMARY MAIN append-only/latest is R197 on ops/orchestrator-run-report@d27d36a5e3f6ad064063333531002225e3fe8dbe while state/lease remain R196. Methodology is R153 / WELL_CALIBRATED at ops/methodology-calibration-audit@85267c9cae49bc61358c501ba36f5e9061421790. External Science head is d087acdfb93f89ffb03ca82702b8f7125476e3c3 with Theory R25, append-only Literature R51 and Audit R13. Utility remains cfff53f87c41db7bf94497a7d777a5a184a22975. Relay remains unallocated.

## Canonical science

Canonical science is unchanged: 35/35 terminal, 0 active, 0 queued and 8 consumed FORMAL identities. No FORMAL execution, rerun, retune, rescore, redispatch, immutable-evidence mutation or terminal reopen is authorized.

## M1 critical path

BUILD-SB-M1-002-INTEGRATED-ROBUSTNESS-HARNESS remains exact head 2a21d3e879f1db4e81a58273180ad2124e823a5e. Fresh comparison to main@59fc994b39d0ba02682e972161bb46801592d25b is 1 ahead / 0 behind; fresh open-PR search is empty; Actions run 36361950457 is completed/success at that exact head.

Retain exact-head PR/conditional-merge authority. MAIN R197 again exhausted the five-count PR-create ceiling: attempt 1 ended at the orchestration tool-call ceiling with no PR on readback and attempts 2-5 were explicit pre-GitHub platform refusals. No merge was attempted.

M1-002 remains built=true, bounded-functionally-verified=true, comparatively-supported=false, composition-contribution=NOT_ESTABLISHED, scientifically-novel=false and scientific-credit=0. The blocker remains the required PR-create path.

## SB003 / FLY-0 adjudication

BUILD-SB-003-FLYLIKE-SENSORIMOTOR-PILOT remains PRIMARY_MAIN / ALLOCATED_CONDITIONAL_INACTIVE under unchanged R171/R172 activation conditions and rolling A/B/C authority. Existing optional admissions remain: intent-supersession A/B; NARROW_OBSERVER B/C; typed ascending semantics B/C; feedback-liveness semantics-only B/C with no WORLD commit authority; repaired consumer reconciliation gate B/C behind a validated upstream proof.

The upstream receipt validator is now component-specifically verified. Source commit af238d1bd6fcb4d5433a5caaa96a246e880b1121 / source blob 6aa21e9a9b1c336c87defc224690bc1a21f33fc9 is combined with focused test blob 97a2141f69644c9e02a5ab3d736a68e0a4b584df at exact validated head 9cbb8949c26bf6ff9fd030b5fe6e2328310d2c74. CI run 36599658868 is completed/success on that exact head. The upstream branch contains the same repaired reconciliation-gate blob 076b5184468c4c90b2ca0bf385cf1bdee972e2e8 as the repaired proof-identity branch.

Focused acceptance verifies across structured, rewired, random_sparse and reactive variants: source-frame/execution-journal binding; committed stale-authority outcome validation without control restoration; source-frame tamper rejection; signal payload tamper rejection; rolled-back transaction rejection; masked feedback remains UNRESOLVED; and composition with the repaired consumer gate.

Admit exact tested source/test scope as OPTIONAL_PREAUTHORIZED_UPSTREAM_RECEIPT_VALIDATOR for SB003 B/C, NON_EVIDENTIARY/NONCANONICAL and scientific credit 0. Also admit the exact tested composition of validated upstream proof -> repaired consumer gate as OPTIONAL_PREAUTHORIZED_BOUNDED_RECEIPT_RECONCILIATION_PATH for SB003 B/C. The test helper/self-attestation path is not authority; only proofs emitted by the admitted validator from matching source-frame and committed execution-journal records may feed the consumer gate.

This bounded admission does not establish long-running exactly-once semantics. Theory R25 correctly adds a monotonic reconciliation horizon and explicit unresolved state outside retention: validator lineage, proof/dedupe identity, outcome watermark, pending/in-flight reconciliation state, horizon floor and expired-unresolved causal gaps must checkpoint/replay consistently; OUTSIDE_RETENTION_HORIZON must never become zero/no-change/known-duplicate by assumption.

The older bounded-receipt-retention Forge component at 8937342eea5f05777bdccd13aaa7e6f0c13fd609 is useful as a design/reference input only, not direct FLY-0 handoff: it bounds an older exact receipt ledger with rolling digest/Bloom-style identity filtering, has known false-positive liveness degradation, and does not itself integrate the current FLY-0 validator/consumer/liveness state or R25 reconciliation-horizon contract.

Therefore full long-running receipt reconciliation moves from HOLD_FOR_UPSTREAM_VALIDATOR to HOLD_FOR_BOUNDED_HORIZON_RECOVERY_AND_SCOPED_COMPOSED_ACCEPTANCE. Forge is prospectively authorized for bounded NON_EVIDENTIARY adaptation/tests implementing the R25 horizon contract and cycle-consistent checkpoint/replay. This is not an M1 gate or SB003 activation condition.

Literature R51 remains NON_EVIDENTIARY and adds no Revisit trigger. Future topology novelty cannot rest on structured-vs-rewired/random superiority alone.

## P0 reconciliation

P0 INC-GITHUB-MUTATION-RECURRENCE-20260928-001 remains OPEN / root cause UNKNOWN. MAIN R197 required create_pull_request again failed within the five-count ceiling while Forge source/test/report and prior Analyst persistence have succeeded after bounded retry. Repository-wide write loss, generic Contents outage and constant permission loss remain unsupported. The strongest recurring failure surface remains create_pull_request; the bounded classification remains persistent PR-creation pre-GitHub refusal with nonuniform/intermittent failures on other mutation surfaces.

Pointer debt is operational only: Control append-only/latest R129 with state R128; MAIN append-only/latest R197 with state/lease R196; Literature append-only R51 with moving latest/state R50. Append-only records remain primary durable authority and no allocation changes follow from cache lag.

## Remaining integration graph / disposition

Critical path: M1-002 required PR creation -> merge -> post-merge acceptance.

Parallel bounded FLY-0 path:
1. adapt/implement R25 reconciliation_horizon_floor and explicit OUTSIDE_RETENTION_HORIZON state across validator/consumer/liveness;
2. add cycle-consistent checkpoint/replay coverage for proof/dedupe registry, watermark, pending/in-flight state, horizon metadata and expired-unresolved gaps;
3. only after composed acceptance, admit long-running receipt/liveness composition;
4. SB003 remains conditionally inactive until its existing activation conditions pass.

Disposition:
- M1-002: GO under retained exact-head PR/conditional-merge authority.
- SB003: ALLOCATED_CONDITIONAL_INACTIVE.
- Upstream receipt validator: OPTIONAL_PREAUTHORIZED B/C at exact tested scope.
- Upstream validator + repaired consumer gate: OPTIONAL_PREAUTHORIZED bounded receipt reconciliation path B/C.
- Long-running receipt reconciliation: HOLD_FOR_BOUNDED_HORIZON_RECOVERY_AND_SCOPED_COMPOSED_ACCEPTANCE.
- Relay: no allocation.
- Result-bearing science: STOP / no authority.
- Revisit: no new object.
