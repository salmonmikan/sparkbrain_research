# SparkBrain External Research & Audit — Latest Handoff

Analysis time: 2026-09-17 10:32 JST  
Role: `INDEPENDENT_AUDITOR`

## Audit target

The highest-consequence new attack surface is C19-v2's pre-START scorer contract, not a completed scientific result. Repository-authoritative state is `research/c19-truth-free-symbolic-adapter-v2-20260917@66c8eafe9863ed1b2455cc833a3dc498ce7721b0`; its 90c936a7... scientific-semantics anchor remains the historical C19-v2 basis. The current branch records `PRESTART_PROTOCOL_SCORER_BINDING_REQUIRED`: official one-way execution had not STARTED, the official minimum replication had not been dispatched, and the planned formal identity remained unconsumed when two scorer ambiguities were detected.

The ambiguities are: (1) the quantile interpolation/convention was not prospectively fixed, and (2) the exact evaluator `target_payload` join key was not prospectively fixed. Evidence Analyst proposes a fresh successor protocol/package/identity with a named quantile convention and an exact canonical six-field evaluator-target join, while retiring the predecessor identity unSTARTED rather than rewriting or reusing it.

## Independent falsification attempts

### 1. Post-outcome tuning / silent repair

**Attack:** If scorer semantics were chosen after seeing official outcomes, or an already-started identity were silently repaired, the evidence would be invalid.

**Result:** This attack does not land. The repository records the ambiguity before STARTED and before official dispatch/scoring. No formal result exists to tune against. A fresh, prospectively frozen successor is scientifically legitimate provided the predecessor protocol remains historically immutable and the predecessor identity is never repurposed.

### 2. Evaluator leakage / target privilege

**Attack:** A join against evaluator `target_payload` can become label leakage if target truth or task semantics enter candidate/model feature construction rather than remaining evaluator-only provenance/scoring data.

**Result:** This is the main unresolved technical audit point. A six-field join is acceptable only as deterministic evaluator-side identity/provenance matching. The successor contract should prospectively assert one-to-one uniqueness and total coverage, reject duplicates/missing matches, and explicitly prohibit target truth from entering candidate/model features. I did not infer the six field names from incomplete evidence; they should be fixed verbatim in the successor contract rather than reconstructed ad hoc.

### 3. Quantile-definition ambiguity

**Attack:** Different quantile interpolation rules can change thresholding/scoring at small sample sizes or ties, creating an unregistered degree of freedom.

**Result:** The predecessor is not safely scorable as-is. The successor must freeze the exact quantile method plus edge/tie/NaN/empty behavior before STARTED. Small deterministic golden fixtures are the cleanest way to make the contract executable rather than merely textual.

### 4. Mechanistic overclaim after repair

**Attack:** Even a clean future C19 result could be overinterpreted as evidence for persistent dynamics.

**Result:** Unchanged from the prior scout: the frozen `direct_stateless` baseline does not receive the same I2 structural representation, and `explicit_state_probabilistic` is not representation-matched. Therefore a later I2>I1 result can support only the already narrow `truth_free_surface_structural_representation_gain_only` boundary until representation-matched static/shallow and explicit-state alternatives are prospectively tested. This is not a reason to alter the present C19 protocol.

## Audit classification

**`INCONCLUSIVE`** for the C19-v2 scientific claim/result: there is no valid official result yet to confirm or invalidate, and the predecessor scorer contract is under-specified for one-way formal scoring.

**Integrity-gate assessment: `ROBUST_SO_FAR`.** The pre-start gate detected the under-specification before any one-way identity was consumed. The correct next move is not to repair the predecessor in place, but to preserve it, retire its identity unSTARTED, and freeze a fresh successor before execution.

This is **not** `INVALID_EVIDENCE`, because no official evidence was produced under the ambiguous scorer. It is also **not** evidence of post-outcome tuning.

## Prospective hardening recommendations

For the fresh successor only, before STARTED:

1. Freeze the exact quantile definition/method, including ties, NaN and empty-set behavior.
2. Freeze the exact evaluator-target join fields and require uniqueness + totality assertions; duplicate or missing keys must fail closed.
3. Add deterministic golden scorer fixtures covering join success, duplicate rejection, missing-key rejection, and quantile edge cases.
4. Explicitly assert that target truth/labels remain evaluator-only and cannot enter I1/I2 candidate/model features.
5. Prefer an independent second scorer implementation or fixed golden-output checksum where practical, so scorer semantics can be verified before the one-way boundary.
6. Keep representation-matched exact-I2 stateless/shallow and explicit-state comparators as future prospective discriminators after a valid C19 formal result; do not retrofit them into the current frozen scientific question.

## Knowledge-flow contract

- `role`: `INDEPENDENT_AUDITOR`
- `genuinely_new_information`: `true` — new repository integrity event since the prior external handoff; the issue was first caught by the repository pre-start gate/Evidence Analyst and independently verified here.
- `affected_lines`: `C19_V2`, `C19_PROTOCOL_INTEGRITY`, `PROGRAMME_NOVELTY`
- `novelty_or_reduction_impact`: `NO_NEW_NOVELTY_SUPPORT; C19_REMAINS_UNRESOLVED; EXISTING_REPRESENTATION_MATCHED_REDUCTION_PRESSURE_REMAINS`
- `audit_classification`: `INCONCLUSIVE`
- `prospective_baselines_or_discriminators`: fresh successor with executable scorer contract; deterministic golden scorer fixtures; optional independent scorer-equivalence check; later exact-I2 representation-matched stateless/shallow and explicit-state comparators.
- `questions_for_evidence_analyst`:
  1. Is the predecessor scorer/protocol artifact preserved unchanged and explicitly marked retired-unSTARTED rather than repaired in place?
  2. Is `c19-external-v2-official-v1` permanently non-reusable/retired rather than repurposed for the successor?
  3. Does the successor freeze exact evaluator join fields with uniqueness and totality assertions before STARTED?
  4. Is target truth strictly evaluator-only and technically prevented from entering candidate/model features?
  5. Are quantile rules complete for ties, NaN and empty input, and covered by frozen golden fixtures?
- `questions_for_control_brain`:
  1. Should executable golden scorer fixtures become a generic readiness requirement for future one-way external protocols?
  2. Should unique/total evaluator-join assertions become a generic formal-execution gate?
  3. Keep C19's claim narrow and defer scaling until a valid formal result plus representation-matched nulls exist.
- `must_not_change_frozen_or_consumed`: all consumed A01/RV01/RV02/CX identities; rejected A01 Family-B/C exact objects; historical C19-v1/C06; C19-v2 scientific-semantics anchor at `90c936a7...`; the ambiguous predecessor protocol artifacts; predecessor `c19-external-v2-official-v1` must be retired unSTARTED and never repurposed; no outcome-conditioned scorer/threshold choices.

## Handoff

**Role performed:** `INDEPENDENT_AUDITOR`.  
**Genuinely new audit issue:** yes — a new pre-start scorer-contract ambiguity is now authoritative repository state, but it was caught before any formal result or identity consumption.  
**Top implication:** preserve the predecessor unchanged and freeze a fresh successor with executable quantile/join semantics and fail-closed golden fixtures before STARTED.  
**Affected lines:** C19-v2, C19 protocol integrity, programme novelty boundary.  
