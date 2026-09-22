# SparkBrain Methodology Calibration Audit — R63

- schema_version: `2`
- generation_id: `METHCAL-20260922T182145+0900-R63-7C31F2A8`
- produced_at: `2026-09-22T18:21:45+09:00`
- supersedes: `METHCAL-20260922T172329+0900-R62-A6D4C219`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- overall_classification: `MIXED_CALIBRATION`

## Material update

The strongest new calibration evidence is a pre-identity exact-binding observability defect, not a scientific-integrity breach. Evidence Analyst R70 records H7's FORMAL-R1 implementation head as `ca35c51a7d366a37f7d11d0434d05420274969aa` and treats that exact head's generic CI as the reviewed implementation anchor. Independent repository refresh shows that the same implementation branch had already advanced before R70 was produced to `67ed8fad1d861463e4129d44efbb2540affd1889`.

The three commits after `ca35c51a...` only add/fix `h7_formal_r1_preflight.py` and its tests. They are consistent with `SCIENCE_INVARIANT_REPAIR`: runtime/seed/binding checks, path validation and a test error-message match. No scientific metric, threshold/tolerance, comparator definition, intervention, seed policy, resource/privilege contract, hypothesis, falsifier or success criterion was changed, and no result-bearing execution or FORMAL identity was consumed.

Therefore development iteration is calibrated here, but the control plane needs a sharper distinction between **mutable branch tip**, **reviewed/CI-qualified exact head**, and the future **identity-candidate frozen SHA**. A field named `implementation_head` must not silently function as all three. Before any FORMAL identity is minted, the current branch tip must be freshly reconciled, reviewed and frozen to one exact SHA. This is `TIGHTEN`, not evidence invalidation.

## Authoritative refresh / hard floor

Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. The authoritative annotated `evidence/*` set remains unchanged and tag-form `formal/*`, `sealed/*`, `freeze/*` remain empty. No consumed FORMAL identity was rerun, retuned or rescored; no historical PASS/FAIL was rewritten.

Evidence Analyst R70 keeps fresh FORMAL authority at `0` and explicitly stops identity creation, STARTED, protected evaluation and result-bearing FORMAL execution. H7 remains `MECHANISM / RESULT_EXPOSED_DEVELOPMENT / ACTIVE`; candidate 33 is now `ARCHITECTURE_STUDY / SYSTEM / OPEN_DEVELOPMENT / ACTIVE / QUEUED`. Candidate 32 remains terminal and is not reopened.

Control-approved PF-R1 durable-byte preservation is still not observed as executed. That remains a hard pre-identity development-provenance gate, not scientific evidence.

## Gate-by-gate calibration

| Gate | Classification |
|---|---|
| hard FORMAL integrity floor | `KEEP` |
| development-phase axis on active paths | `KEEP` |
| end-to-end through fresh consumed FORMAL | `INSUFFICIENT_EVIDENCE` |
| RESULT_EXPOSED same-object SCIENCE_INVARIANT_REPAIR | `KEEP` |
| preidentity preflight/path/hash-plumbing repair classification | **`KEEP`** |
| post-result SCIENCE_AFFECTING change → explicit version/fresh successor | `KEEP` |
| repeated dev rerun/retune non-independent accounting | `INSUFFICIENT_EVIDENCE` |
| prior-result semantic/hash lineage | `KEEP` |
| durable RESULT_EXPOSED raw/result byte preservation | `TIGHTEN` |
| **mutable branch tip vs reviewed exact-head observability** | **`TIGHTEN`** |
| **FORMAL identity requires freshly reconciled reviewed exact SHA** | **`TIGHTEN`** |
| methodology gap blocks FORMAL identity until resolved/reviewed | `KEEP` |
| cycle 3 as automatic terminal cap | `RELAX` |
| cycle 3 mandatory reassessment | `KEEP` |
| PRE_FORMAL as development surface | `KEEP` |
| `preformal_eligible` distinct from READY | `KEEP` |
| READY = well-defined/informative next test | `KEEP` |
| `HIDDEN_SECOND_FORMAL_GATE` | `false` / `KEEP` |
| current-object `claim_ceiling` | `KEEP` |
| same-object SYSTEM→MECHANISM uplift ban | `KEEP` |
| fresh terminal SYSTEM successor distinctness/non-rescue | `KEEP` |
| fresh SYSTEM→MECHANISM successor admission | `INSUFFICIENT_EVIDENCE` |
| `TERMINAL_FOR_CURRENT_OBJECT` topic scope | `KEEP` |
| duplicate/non-independent standby suppression | **`KEEP`** |
| successor potential ≠ automatic admission | `KEEP` |
| classification-completeness gating | `KEEP` |
| MAIN MECHANISM priority | `KEEP` |
| prospective SYSTEM-priority exception | `KEEP` |
| first genuine MAIN SYSTEM-over-comparable-MECHANISM exception | `INSUFFICIENT_EVIDENCE` |
| one-in-three theory-backward supply / quality floor | `KEEP` |
| `NO_COHERENT_MECHANISM_TARGET` liveness semantics | `KEEP` |
| SYSTEM architecture/testbed/reproducibility value | `KEEP` |
| PRE_FORMAL raw-before-score | `KEEP` |
| future FORMAL exact source/protocol/package/runtime/input/evaluator binding | `TIGHTEN` |
| FORMAL preserve-before-read / immutable evidence | `TIGHTEN` |
| comparator-equivalence verifier independence | `TIGHTEN` |
| protected/adaptive evaluation validity | `TIGHTEN` |

## Mandatory questions

1. **Development phase end-to-end?** Consistent through RESULT_EXPOSED PRE_FORMAL, preidentity implementation and a fresh OPEN SYSTEM successor; fresh consumed-FORMAL end-to-end remains unobserved.
2. **Cycle 3 a hard cap?** No. H7 continues beyond cycle 3 under prospective information-gain reassessment.
3. **Repair split correct?** Yes in the new live case: the three post-`ca35c51a...` commits are preflight/path/test plumbing and do not alter scientific criteria.
4. **Rerun/retune laundering?** None observed; repeated result-bearing development remains untested.
5. **Prior result preserved after exposure?** Semantic/hash lineage yes; PF-R1 byte durability remains incomplete/pending approved Utility preservation.
6. **FORMAL one-way integrity?** Unchanged; no fresh identity is consumed.
7. **Fresh SYSTEM→MECHANISM successors?** Candidate 33 remains a legitimate fresh SYSTEM→SYSTEM successor. Genuine SYSTEM→MECHANISM remains unobserved.
8. **PRE_FORMAL development or hidden FORMAL?** Development; `HIDDEN_SECOND_FORMAL_GATE=false`.
9. **Terminal/candidate supply calibrated?** Improved. Candidate 33 advances while duplicate standby supply is retired rather than manufactured. MECHANISM supply is still thin.
10. **PASS reachable without weakening standards?** Yes, conditionally. Current head/review reconciliation and durable PF-R1 provenance must close before identity.

## Funnel / supply / observability

R70 reports `33 = MECHANISM 13 / SYSTEM 20`, classification completeness `33/33`, `ACTIVE=2 / TERMINAL_FOR_CURRENT_OBJECT=31`. Candidate 33 is queued in SYSTEM Architecture; H7 remains the sole active MECHANISM formalization lineage. Development phases remain `OPEN_DEVELOPMENT=3 / RESULT_EXPOSED_DEVELOPMENT=30 / canonical CONSUMED_ONE_WAY=0`; seven historical official scientific identities remain separately one-way.

Mechanism supply health: `SINGLE_ACTIVE_MECHANISM_FORMALIZATION_LINEAGE_PLUS_ONE_SYSTEM_ARCHITECTURE_SUCCESSOR; QUALITY_FLOOR_INTACT_BUT_MECHANISM_SUPPLY_REMAINS_THIN`.

Funnel classification completeness remains good. The new observability defect is narrower: exact-head state must distinguish `branch_tip_observed_sha`, `reviewed_exact_head_sha`, review/CI status and eventual `identity_candidate_sha` so mutable development commits cannot be mistaken for an already reviewed frozen execution target.

R70 correctly retires the phenomenon-first H3 standby as duplicate/insufficiently distinct and leaves no replacement. That is positive evidence against candidate manufacture under supply pressure.

## Development iteration calibration

The current branch movement is precisely the kind of iteration HUMAN-20260922-005 should permit before consumption. Adding fail-closed runtime, seed-collision and binding checks and repairing path/test behavior is not outcome-responsive scientific tuning. The defect is only that the mailbox state does not cleanly expose which exact SHA has been reviewed versus which SHA is merely the latest mutable development tip.

This does not authorize rewriting or replaying any consumed identity. It also does not justify freezing the current tip automatically: a fresh review must reconcile it first.

## Risks

False-positive risk: `LOW_TO_MODERATE_WATCH`. If a future one-way identity were minted from a mutable/unreviewed tip while the authority record still names an older reviewed head, unreviewed implementation could enter the confirmatory path. No such consumption has occurred.

False-negative/opportunity-cost risk: `MODERATE_WATCH_IMPROVING`. Candidate 33 has advanced to SYSTEM Architecture and duplicate supply was filtered, but the viable MECHANISM queue remains essentially one H7 lineage.

Moving-goalpost/rescue risk: `LOW_TO_MODERATE_WATCH`. The observed branch changes are science-invariant and preidentity; the stress point remains any future result-responsive science-affecting revision.

Over-terminalization risk: `LOW_TO_MODERATE_WATCH_IMPROVING`. Candidate 32 stays closed while candidate 33 progresses as a distinct SYSTEM successor.

## PASS reachability

PASS remains realistically reachable without weakening evidence standards. Before any H7 FORMAL identity, the programme should (1) durably preserve PF-R1 development bytes or explicitly establish equivalent durable re-auditability, (2) reconcile the current mutable implementation tip against the reviewed contract/preflight, (3) record one exact reviewed `identity_candidate_sha`, and only then permit fresh one-way authority. Clean PASS still requires prospective frozen binding, untouched evaluation, raw-before-score, preserve-before-read, immutable evidence, dependence-aware inference and valid protected/adaptive evaluation.

## Prospective recommendations

Add explicit machine-readable separation among `branch_tip_observed_sha`, `reviewed_exact_head_sha`, `reviewed_at`, `review_status`, and `identity_candidate_sha`. Any branch movement after review must clear identity readiness until the new exact tip is reviewed; science-invariant changes may remain in the same development revision, but they still require renewed exact-head binding before consumption.

Execute the already-approved bounded PF-R1 byte-preservation Utility request rather than creating a duplicate. Keep candidate 33 at SYSTEM ceiling through Architecture and keep candidate 32 terminal. Continue filtering duplicate standby/successor supply instead of converting potential into automatic admission.

## Utility / integrity / confidence

No new Utility request is created. Existing `UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE` is `CONTROL_APPROVED_NOT_YET_EXECUTED` and directly covers the unresolved development-byte gap.

Hard floor: `CONFIRMED / DO NOT RELAX`.

Confidence: `HIGH` for the exact-head observability finding and science-invariant classification of the observed preflight commits; `HIGH` for current hard-floor integrity; `LOW/UNOBSERVED` for a genuine SYSTEM→MECHANISM successor and fresh consumed-FORMAL end-to-end run.

Questions for Control/Analyst: before identity, will R70's reviewed `ca35c51a...` anchor be explicitly reconciled with current branch tip `67ed8fad...` and one exact `identity_candidate_sha` frozen? Will future state separate observed branch tip from reviewed head? Will PF-R1 exact bytes be durably preserved before identity? Will candidate 33 remain SYSTEM-auditability-only through Architecture and will duplicate standby supply remain noncanonical?
