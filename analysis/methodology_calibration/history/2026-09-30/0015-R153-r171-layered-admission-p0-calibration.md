# SparkBrain Methodology Calibration Audit R153

generation_id: `METHCAL-20260930T001533+0900-R153-R171-LAYERED-ADMISSION-P0-CALIBRATION`
produced_at: `2026-09-30T00:15:33+09:00`
overall_classification: `WELL_CALIBRATED`
new_scientific_result: false
authority_scope: `METHODOLOGY_ADVISORY_ONLY`

## Freshness

Main policy was re-fetched explicitly from `main@59fc994b39d0ba02682e972161bb46801592d25b`.
Human Directive freshness is unchanged at `ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d` / active-index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`; there is no directive delta from R152.

Current durable inputs:
- Evidence Analyst: R171, append-only history verified on `ops/evidence-analyst-handoff`.
- Control: append-only R128; `latest` remains R125 while `state` is R128.
- PRIMARY MAIN: append-only R196; `latest/state/lease` remain R195.
- Theory: R24.
- Literature: R50.
- Independent Audit: R13.
- prior Methodology: R152.
- Relay: unallocated.

## Overall calibration

The programme remains WELL_CALIBRATED. Evidence Analyst R171 resolves the main methodology question left open by R152 without either over-promoting Forge work or forcing unnecessary handoff latency.

R171 admits three FLY-0 layers only at their tested engineering scope:
1. typed ascending semantics `da0d6cae7c863ce3ded5e9fc2ea7306d6d78e2a1` as optional B/C input;
2. feedback-liveness `c67fad2891f8209b05edbf21e2d86ce50b2ad27b` as liveness semantics only, with no WORLD-commit authority and bounded retention/expiry required for long-running use;
3. repaired reconciliation gate `dde6270db4238ca78d1678a8826b8a463cd2d8dc` as an optional B/C consumer primitive only behind a separately validated upstream R24 proof issuer.

The repaired reconciliation gate closes Audit R13's consumer proof-identity defect at the bounded consumer scope: cross-transaction signal replay is rejected, conflicting sequence for the same transaction/signal is rejected, and checkpoint/restore preserves dedupe identity. The exact source still exposes `make_validation_proof()` as a caller-constructible helper, so R152's trust-boundary concern remains valid. R171 handles this correctly by explicitly forbidding consumer self-certification and requiring a separate validated upstream receipt validator.

Therefore:
- no new M1 gate is justified;
- no SB003 activation condition should be added;
- no mandatory review gate should be reintroduced;
- full R22/R23/R24 receipt reconciliation remains held only for the upstream validator and scoped acceptance;
- long-running composed liveness still needs bounded pending-state retention/expiry.

## SYSTEM_BUILD calibration

M1-002 remains exact head `2a21d3e879f1db4e81a58273180ad2124e823a5e`, freshly 1 ahead / 0 behind `main`, built and bounded-functionally-verified, with no open PR. The current blocker is the required PR-create route, not a new engineering defect or methodology gate.

SB003 remains `ALLOCATED_CONDITIONAL_INACTIVE` under unchanged activation conditions and rolling A/B/C authority. R171's layered admissions reduce future handoff latency while remaining bounded and prospective. This is the intended behavior under HUMAN-20260928-001 rather than OVERPERMISSIVE_ROLLING_AUTHORITY.

Forge/Utility parallel work remains non-colliding and NON_EVIDENTIARY. None of the admitted layers inherits scientific credit.

## Scientific boundary and comparator fairness

Canonical science remains 35/35 terminal, 0 active, 0 queued, with 8 consumed FORMAL identities. No historical result changes.

Component function, SYSTEM_BUILD viability, composition contribution and scientific novelty remain separated. The new admissions establish only bounded engineering reuse.

FLY-0 resource/comparator fairness remains SPLIT_BY_CLAIM_TYPE. Ordinary SYSTEM_BUILD reuse does not require biological fidelity or a full topology-superiority experiment. Any future claim of topology superiority, efficiency, biological equivalence, composition contribution or scientific novelty still requires a fresh prospective scientific object, matched comparators and zero inherited Forge/BUILD credit. Literature R50 continues to weaken novelty claims based only on structured-vs-rewired/random superiority.

No Revisit object is needed for known/ordinary engineering reuse.

## P0 / persistence

P0 `INC-GITHUB-MUTATION-RECURRENCE-20260928-001` remains OPEN / root cause UNKNOWN. MAIN R196 again records 5/5 `create_pull_request` refusals before GitHub, while other mutation paths can succeed intermittently. Repository-wide write loss and generic Contents failure remain unsupported.

Current pointer debt is operational, not scientific:
- Control: append-only R128 / latest R125 / state R128.
- MAIN: append-only R196 / latest-state-lease R195.
- Analyst: R171 durable and complete.

Append-only history remains primary authority; no stale-pointer science/build misallocation is observed. P0 repair must not be converted into an additional scientific or SYSTEM_BUILD review gate.

## Gate classifications

- FORMAL one-way integrity: KEEP.
- Development phase semantics: KEEP.
- BUILD/Forge zero scientific credit: KEEP.
- Mandatory SYSTEM_BUILD review: KEEP_AS_NON_GATE.
- M1 rolling authority: KEEP.
- SB003 conditional activation / rolling contract: KEEP.
- Typed ascending semantics: KEEP_ADMITTED_OPTIONAL_B_C.
- Feedback liveness: KEEP_ADMITTED_LIVENESS_ONLY; TIGHTEN retention/expiry if long-running.
- Repaired reconciliation consumer gate: KEEP_ADMITTED_OPTIONAL_B_C_BEHIND_TRUSTED_UPSTREAM_VALIDATOR.
- Upstream receipt validator: KEEP_OPTIONAL_NON_GATING; still required only if full receipt path is adopted.
- FLY-0 resource/comparator fairness: SPLIT_BY_CLAIM_TYPE.
- P0 moving-cache debt: CLARIFY_OPERATIONAL_NOT_SCIENCE_GATE.
- Revisit reuse boundary: KEEP.

PASS remains realistically reachable without weakening scientific standards.

No experiment was dispatched, no identity consumed, no scientific/build/evidence ref was mutated by Methodology, no PR/merge or scheduler change was performed, and no Work-backed execution was used.
