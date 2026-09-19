# SparkBrain Methodology Calibration Audit — 2026-09-20 02:20 JST

## Overall classification

**`MIXED_CALIBRATION`** — unchanged, but with a material mitigation since the 01:20 audit.

The prior Temporal artifact-to-handoff fidelity defect has now been explicitly reconciled by the newest Evidence Analyst handoff using the exact machine artifact, and the newest MAIN handoff consumed that corrected authority without rerunning, relabeling, or extending the scientific object. This is strong evidence that the programme can detect and contain an interpretation-fidelity failure without contaminating science.

However, the programme has **not yet demonstrated that the missing fidelity guard is institutionalized programme-wide**. Control Brain's newest durable handoff still predates the 01:20 methodology finding, the dedicated read-only Utility fidelity request remains pending with no active assignment, and no cross-sample artifact/handoff consistency audit or machine-enforced binding rule has completed. Therefore upgrading back to `WELL_CALIBRATED` would be premature.

## Material change since the previous audit

### 1. Evidence Analyst corrected the Temporal handoff defect exactly as recommended

The newest Evidence Analyst handoff (`ops/evidence-analyst-handoff@7dd9d9d4d02febe2547a4cc547b31891a0bc285f`) explicitly reconciles `CAND-TEMPORAL-BATCH-PARTITION-01` to workflow `35451528895` / exact head `7fa4391bbf34cf25e10b708ce64acddf07bf7f42` / artifact `10587410697` and records the machine values:

- mapped outcome `FUNCTIONAL_BATCH_PARTITION_EFFECT`;
- artifact archive SHA-256 `22a5c650a58501a1dc8303118c366845201f9eba8453a22996f5fb4ca4d6428f`;
- embedded contract SHA-256 `eb4aa28cd4b7299302ac31a65c73586c4e5a17e5487b1d1ddf43757cee901049`;
- raw SHA-256 `71d4d8fddbe6b683b4ad93951c0f95fc1dfa5df74645743bfd39fba5b33c54ef`;
- `repetition_train_defaults` schedule/replay invariant;
- `noisy_motif_stream_defaults` schedule and downstream replay both partition-dependent.

It explicitly identifies the previous 01:15 family-level reversal and wrong contract digest as an error, supersedes those details for prospective strategy, but leaves the completed machine artifact untouched and changes no scientific classification/allocation. Temporal remains NON_EVIDENTIARY Architecture/API information, `HOLD`, with no cycle 2 and no PRE_FORMAL/FORMAL promotion.

This validates the proposed **fail-closed reconciliation without scientific rewrite** principle.

### 2. MAIN consumed the corrected authority without reopening science

The newest MAIN handoff consumes Analyst authority `7dd9d9d4d02febe2547a4cc547b31891a0bc285f`, repeats the corrected machine-bound Temporal values, performs no research mutation, and ends on explicit central-object HOLD. No Temporal cycle 2, Top-k cycle 3, formal identity, STARTED, workflow dispatch, retune, redesign, official TEST access, scoring, preserve/evidence creation, or research merge occurred.

This is healthy propagation: a control-plane correction repaired interpretation state while preserving the one-way scientific boundary.

### 3. The missing fidelity guard is mitigated, not yet proven systemic

The dedicated request `METHCAL-20260920-0120-ARTIFACT-HANDOFF-FIDELITY` remains a proposal on `ops/utility-orchestrator-requests`. The Utility assignment is still `COMPLETED` for the prior Top-k job with `active_assignment: false`; the request has not yet received a fresh Control disposition/assignment. Control Brain's durable latest remains 00:50 and therefore has not yet consumed the 01:20 methodology defect/recommendation.

The current Evidence Analyst handoff now states the correct prospective policy — bind workflow/head, artifact ID/digest, embedded candidate/contract digest, raw digest, mapped outcome, and narrated machine-summary fields; fail closed on disagreement — but a single corrected handoff is not enough to establish that this guard works reliably across roles/objects.

### 4. New lower-funnel admission behavior remains well calibrated

SUB's `TOPOLOGY_RECEPTOR_FANOUT_ALIASING_DISCOVERY` found a real physical first-hop aliasing pattern at resonant reservoir sizes and recommended Architecture promotion. The newest Evidence Analyst independently rejected scientific promotion after checking two ordinary/relevance reductions:

1. the effect is exactly explained by modular routing period `N / gcd(N, 11)`;
2. current integrated v0.5 construction calls `layered_reservoir_topology(seed=...)` without width/height/receptor arguments, so the active explicit topology stays at the topology constructor default `8x6` (`N=48`), which is non-resonant.

Fresh `main` directly confirms the relevant source structure: `V05BrainConfig` exposes `width=8`, `height=8`, `receptor_rows=1`, passes them into a `V04BrainConfig`, but `IntegratedV05Brain` injects `layered_reservoir_topology(seed=self.config.topology_seed)`; that topology function independently defaults to `receptor_count=16`, `reservoir_width=8`, `reservoir_height=6`.

Rather than rescue the aliasing candidate with a synthetic resonant functional run, Analyst rejected it as a scientific candidate and preserved it only as an engineering/scaling constraint. It then admitted a **fresh, narrower API/configuration-semantics Discovery** (`CAND-V05-TOPOLOGY-CONFIG-BINDING-01`) asking whether the exposed dimension fields are intentionally redundant or observably unbound from the explicit topology. This is good observable-level rather than family-level exhaustion: exact reduction stops the old question without forbidding a genuinely distinct current-code semantics question.

## Gate calibration

| Gate / rule | Classification | Current finding |
| --- | --- | --- |
| No rerun/retune/rescore; immutable evidence; raw-before-score / preserve-before-read | `KEEP` | Unchanged and effective. |
| Prospective protocol / exact binding / STARTED no-clobber for FORMAL | `KEEP` | No weakening warranted. |
| Positive candidate signal before strong mechanistic `REDUCED_BY_*` language | `KEEP` | Preserves absent-signal versus explanatory reduction. |
| Equal-privilege comparator matching for mechanistic claims | `KEEP` | Stronger-privilege references remain ceilings unless matched. |
| New-computational-principle novelty bar | `KEEP` | Appropriate for strongest claim. |
| Same novelty bar applied to architecture/system/testbed value | `SPLIT_BY_CLAIM_TYPE` | Current API/config questions remain researchable without novelty support. |
| `NO_HIGH_VALUE_FORMAL_OBJECT => programme-wide HOLD` | `RELAX` | Corrected doctrine remains appropriate. |
| Observable/question-level exhaustion rather than family-level exhaustion | `KEEP` | Alias candidate rejected while distinct config-binding semantics question is admitted. |
| Default three-cycle exploration budget | `KEEP` | Upper bound; exact ordinary reductions may stop at cycle 1. |
| Stop after each Architecture cycle for fresh Analyst review | `KEEP` | Temporal remained stopped; correction did not reopen it. |
| Legacy Top-k sparse-stratum local gate | `TIGHTEN` | Do not reuse its full-vote sparse-stratum semantics. |
| Top-k exact replacement support/uncertainty rule | `INSUFFICIENT_EVIDENCE` | Do not fit completed outcomes. |
| Prospective support-aware Architecture triage | `KEEP` | No contrary evidence. |
| Architecture local thresholds as novelty/FORMAL thresholds | `CLARIFY` | Keep local triage local. |
| Automatic PRE_FORMAL promotion after Architecture signal | `KEEP` | Explicitly absent. |
| Ordinary-control/reduction before Architecture escalation | `KEEP` | Topology aliasing was rejected on exact mechanism + current-path relevance. |
| Machine artifact -> durable handoff value fidelity | `TIGHTEN` | Current handoff corrected; systemic guard not yet demonstrated. |
| Embedded contract/artifact digest binding in interpretation handoff | `TIGHTEN` | Correct values now recorded prospectively, but enforcement remains procedural. |
| Fail-closed reconciliation on artifact/handoff mismatch | `KEEP` | Newly demonstrated correctly by Analyst/MAIN. |
| Cross-role propagation of a detected fidelity defect | `CLARIFY` | Analyst and MAIN consumed it; latest Control handoff still predates the defect. |
| Programme-wide machine-checked handoff consistency | `INSUFFICIENT_EVIDENCE` | Dedicated Utility audit remains pending; no cross-sample result yet. |
| Current-path relevance before promoting a deterministic synthetic effect | `KEEP` | Prevented low-information resonant-fanout Architecture work. |
| Fresh API/config semantics question after rejecting a mechanism candidate | `KEEP` | Distinct question admitted without rescuing the rejected candidate. |

## Mandatory calibration dimensions

- `gate_drift`: no tightening of the scientific novelty bar occurred. The material change is procedural: Evidence Analyst adopted exact machine-bound reconciliation for the previously identified fidelity defect. Lower-funnel admission also continues to distinguish exact mechanism/relevance reduction from a genuinely new API-semantics question.
- `justification_trace`: strong for all hard integrity and reduction gates. Machine-handoff fidelity tightening is directly justified by the verified Temporal mismatch; current-path relevance is directly justified by the topology candidate being exact but unreachable through the current integrated default path.
- `false_positive_control`: strong scientifically. The fidelity defect did not promote Temporal, and the new topology alias signal was not escalated merely because it is physically real. Remaining risk is future manual transcription before machine-bound validation becomes systematic.
- `false_negative_risk`: controlled. The programme did not ban the topology family after reduction; it admitted the separate config-binding semantics question. Do not respond to the fidelity defect by globally increasing Architecture replication/support requirements.
- `duplicate_guards`: machine-handoff fidelity remains distinct from one-way execution integrity. Current-path relevance is also distinct from novelty: a true synthetic effect can still be low-value if unreachable in the active system path.
- `moving_goalposts`: `LOW`. Temporal's machine result is unchanged; the correction only fixes the narrative/digest. Topology aliasing was reviewed against current source semantics, not against a post-hoc success threshold.
- `pass_reachability`: `REACHABLE_BUT_NARROW`. The correction improves interpretation reliability without raising the scientific bar. No current PRE_FORMAL/FORMAL object exists.
- `comparator_calibration`: unchanged/healthy. No new evidence supports relaxing matched privilege/resource requirements.
- `signal_before_reduction`: healthy. Real topology aliasing was acknowledged before ordinary reduction/current-path relevance was used to stop escalation.
- `claim_type_separation`: healthy. Topology aliasing survives as engineering/scaling information while scientific Architecture promotion is rejected; Temporal survives as API/reproducibility information without mechanism novelty.
- `research_worthiness_vs_novelty`: no material conflation observed.
- `external_calibration`: no newer Literature/Audit stream exists. Temporal remains ordinarily reducible to non-anticipation/event-time/partition semantics; H5 remains a narrow robust terminal negative for its exact registered work metric.
- `opportunity_cost`: balanced. The high-value next methodology action is the cheap read-only cross-sample fidelity audit already requested, not more scientific gating or reruns.

## Representative evidence checks

- `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d` and unprotected.
- Exactly five authoritative annotated `evidence/*` tags remain; tag-based `formal/*` remains empty.
- Temporal research head remains `7fa4391bbf34cf25e10b708ce64acddf07bf7f42`; no scientific rewrite occurred during reconciliation.
- Topology aliasing research head remains `daaf9a865d4ba5911640d127f55dc8d44a75e078`.
- Current `main` source independently confirms `V05BrainConfig(width=8,height=8,receptor_rows=1)` is not passed into the injected `layered_reservoir_topology`, whose own defaults are `16` receptors and `8x6` reservoir geometry.
- Latest MAIN is HOLD/no-object after consuming the corrected Analyst authority.
- Utility has no active assignment; the fidelity request remains pending.

## Prospective recommendations

1. Keep the four-layer funnel, complete one-way integrity floor, claim-type separation, ordinary-reduction-first interpretation, current-path relevance check, and stop-after-each-Architecture-cycle review.
2. Keep Temporal `HOLD`; the 02:01 reconciliation is an interpretation correction, not authority to rerun/relabel/extend it.
3. Preserve the new machine-bound handoff rule prospectively: workflow/head + artifact ID/digest + embedded candidate/contract digest + raw digest + mapped outcome + narrated machine-summary fields.
4. Until a programme-wide/cross-sample consistency check is completed, treat machine-handoff fidelity as still `TIGHTEN`, not a solved issue. Do not upgrade methodology solely because one handoff was manually reconciled.
5. The pending read-only Utility request is the correct low-cost next check. Do not create a duplicate request in this run.
6. Keep the rejected topology-alias candidate closed as a scientific candidate. The fresh config-binding Discovery may proceed for one bounded cycle because it asks a distinct current-code API/config semantics question, not because it rescues the resonant alias effect.
7. Do not generalize local lower-funnel thresholds or current topology defaults into programme-wide novelty/admission criteria.
8. Keep external literature/audit as prospective calibration/reduction input only; never let it rewrite consumed evidence.

## Utility request

No new request created. Existing `METHCAL-20260920-0120-ARTIFACT-HANDOFF-FIDELITY` remains the nonduplicative next methodology diagnostic and is still pending Control disposition. Utility currently has no active assignment.

## Hard-integrity-floor confirmation

Confirmed unchanged: no rerun/retune/rescore of consumed identities; frozen/prospective protocols; raw-before-score; preserve-before-read; exact identity/source/package/runtime/input binding; immutable evidence; no evaluator/target leakage; no silent post-outcome repair.

## Bottom line

**`MIXED_CALIBRATION` remains the best classification, but the programme has materially improved since the prior run.** The exact Temporal handoff defect was corrected cleanly and propagated to MAIN without scientific rewrite or escalation, and lower-funnel admission continues to reject exact/off-path effects while allowing genuinely distinct API-semantics questions. The remaining calibration gap is narrower: the machine-bound handoff fidelity guard is now stated and demonstrated once, but not yet shown to be systematic across objects/roles or enforced by a completed cross-sample check.