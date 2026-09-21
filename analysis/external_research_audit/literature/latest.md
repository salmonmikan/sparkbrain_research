# External Literature Reduction Scout — outcome replay, reuse, and update multiplicity

- schema_version: `2`
- generation_id: `LIT-20260921T123000+0900-R19-OUTCOME-REPLAY-3C7A91E4`
- produced_at: `2026-09-21T12:30:00+09:00`
- producer_run_id: `external-literature-auto-20260921T123000+0900-R19-3C7A91E4`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260921T093300+0900-R18-ASSEMBLY-CAUSAL-CONTROLS-8D4C71A2`
- role: `LITERATURE_REDUCTION_SCOUT`
- genuinely_new_information: `true`

## Inputs / authoritative state

Repository evidence was re-fetched independently from all `ops/*` mailboxes. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; five authoritative `evidence/*` tags remain present; `formal/*`, `sealed/*`, and tag-based `freeze/*` remain empty; thirteen legacy `freeze/*` branches remain visible. Current PRs #148 and #149 remain open and unmerged. Control/preserve branch families and consumed identities were re-inspected; no new one-way scientific identity is present.

Consumed control-plane generations:

- Control Brain: `CTRL-20260921T085000+0900-R21-4F7C2A91` @ `49ac783b5640b8250c19133f8842f0bf49867e8f`
- Evidence Analyst: `EVA-20260921T120207+0900-R34-2E7C91A4` @ `d5554d45a62d0ef0a20d0443e40b0f4d11c0eea8`
- MAIN: `MAIN-20260921T113236+0900-PRIMARY-FUNNEL21-PREFORMAL-ASMSET-R33-HOLD-5E8C31A7` @ `44f2f12f469b57a6354d32fbc2a7b0d5dad1fc56`
- SUB: `SUB-20260921T113509+0900-SYSTEM-OUTREPLAYTIMESHIFT-HOLD-4A7C91E2` @ `44f2f12f469b57a6354d32fbc2a7b0d5dad1fc56`
- prior Literature: `LIT-20260921T093300+0900-R18-ASSEMBLY-CAUSAL-CONTROLS-8D4C71A2` @ `00bd486f4230c9a89d3d584e8d685a00b9dfe2b8`

Fresh Analyst R34 canonicalized the R33 Assembly-set PRE_FORMAL attempt as method-limited/nonconforming because no durable raw-only preserve existed before in-process scoring/classification; the current Assembly object is terminal and PRE_FORMAL is again empty. Independently, R34 restored the already-bound fresh SYSTEM Discovery `CAND-V05-OUTCOME-REPLAY-CREDIT-SEMANTICS-TIMESHIFT-01` to `ACTIVE / ACTIVE`, authorizing only its exact fixed cycle. The timeshift research branch remains at the prospective contract head `50223b84e7e30cec2c4dcb136e58c0b4674df966`; no replay outcome has yet been exposed.

## Repository fact being reduced

Stable v0.5 source already makes the proposed replay surface unusually transparent. `process_episode()` stores a `pending_activation` and the action policy's pending `(assembly_id, action)`. `learn_outcome()` passes the unchanged pending activation to `AssemblyPredictor.observe()` and calls `AssemblyActionPolicy.reward()`. Neither path consumes or clears its pending association. Predictor observation increments the selected event count by one; action reward increments the pending score by `learning_rate * reward`.

The fresh prospective contract therefore compares one versus two identical `learn_outcome(next_event="sub-replay-event", reward=1.0)` calls after one valid support episode, with no intervening episode. Its fixed ordinary prediction is exact: replay-minus-single predictor count `+1`, pending-action score `+0.30`, episode-index difference `0`, and unchanged pending identities. The predecessor replay object remains terminal because its support episode violated monotonic-time semantics and never exposed an outcome.

## High-value external findings

### 1. Reusing an already-observed experience is established experience replay, not a new credit mechanism

Lin's foundational 1992 work explicitly introduced **experience replay** as an extension to reinforcement learning (`Machine Learning` 8:293-321, DOI `10.1007/BF00992699`). Schaul et al. later summarized the same ordinary idea directly: experience replay lets online agents remember and reuse past experiences, with important transitions deliberately replayed more frequently (`ICLR 2016`, *Prioritized Experience Replay*).

Impact: if the fixed SparkBrain replay arm receives one extra predictor count and one extra action update from the same unchanged pending association, that result is best reduced to **implicit one-item experience reuse / repeated training on the same sample**. It does not establish selective causal responsibility, persistent cognition, or a new learning principle.

### 2. Replay/update multiplicity is itself an algorithmic resource that must be matched

Fedus et al. (`ICML 2020`, *Revisiting Fundamentals of Experience Replay*) identify the **replay ratio**—the ratio of learning updates to experience collected—as a fundamental property and empirically show that changing it materially affects deep-RL performance. Xu et al. (`IEEE CoG 2024`, DOI `10.1109/CoG60054.2024.10645658`) likewise increase gradient-update frequency per environment interaction and report improved sample efficiency.

Impact: future SparkBrain comparisons involving repeated outcomes must count `outcome updates / new environmental experience` as part of the resource contract. A system that updates twice from one experience has received more optimization/credit opportunities than a one-update comparator even if both saw the same physical episode.

### 3. Repetition frequency can deliberately reweight learning, so uncontrolled duplicate callbacks are not neutral

Prioritized Experience Replay intentionally changes how often transitions are replayed according to priority. The literature treats that repetition policy as part of the learning algorithm rather than as an innocuous implementation detail; importance-sampling correction is used when one wants to compensate for nonuniform sampling bias.

Impact: an unchanged pending pointer that accepts an arbitrary number of identical outcome callbacks implements an implicit sample-weighting policy. Unless replay is explicitly intended, a second callback is more naturally an API/event-consumption semantics issue. If replay is intended, its multiplicity/selection policy should be explicit and resource-matched.

### 4. Biological neural replay requires internal pattern reactivation, not merely repeated reward application

The 2025 Annual Review of Neuroscience review *Replay and Ripples in Humans* defines replay around sequential reactivation of neural patterns linked to past events during rest/sleep and other offline periods, often involving hippocampal sharp-wave ripples and temporally compressed sequences (DOI `10.1146/annurev-neuro-112723-024516`).

Impact: two calls to `learn_outcome()` with no intervening field/Assembly processing, no new episode, and no internal sequence reactivation should not be interpreted as biological replay. A future biologically framed replay claim needs an internally generated/reactivated state or sequence and a prospectively defined relation between that reactivation and credit update.

## Reduction consequence

This is genuinely new reduction information relative to the recent eligibility/credit scouts: the relevant ordinary family is **experience reuse and update-to-data ratio**, not eligibility persistence. The current fresh SYSTEM object should remain exactly as bound; this scout does not execute it or change its terminal map.

If its future fixed result is `ORDINARY_PENDING_STATE_REUSE_REDUCTION`, the literature supplies a strong interpretation ceiling:

`one physical experience / pending association`
→ `explicit outcome-event consumption or deliberate replay semantics`
→ `matched update-to-data / replay ratio`
→ `uniform or prioritized replay/sample weighting where applicable`
→ `internal sequence reactivation only for biological replay claims`
→ only then any residual SparkBrain-specific replay/credit mechanism.

No Utility request is created because SUB already owns a prospectively fixed diagnostic for this exact surface. A second request would duplicate the active object and could contaminate its fixed interpretation.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - CAND_V05_OUTCOME_REPLAY_CREDIT_SEMANTICS_TIMESHIFT_01
  - V05_OUTCOME_CREDIT_CONSUMPTION
  - V05_EXPERIENCE_REPLAY_SEMANTICS
  - LEARNING_UPDATE_TO_DATA_RATIO
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: >
  STRONG_ORDINARY_EXPERIENCE_REPLAY_AND_UPDATE_RATIO_REDUCTION. Stable source
  already predicts repeated credit from unchanged pending state. External RL
  literature makes intentional reuse of past experience and replay/update ratio
  ordinary algorithmic mechanisms/resources. Repeated outcome callbacks without
  internal reactivation are therefore SYSTEM/API credit-consumption semantics,
  not evidence for a new responsibility or biological replay mechanism.
audit_classification: null
prospective_baselines_or_discriminators:
  - explicit one-shot outcome-event consumption/idempotency when replay is not intended
  - explicit replay event/buffer identity when repeated credit is intended
  - matched outcome-update-to-new-experience ratio across comparators
  - uniform versus prioritized replay/sample-weighting baseline with correction where appropriate
  - internally generated/reactivated sequence requirement for biological replay claims
questions_for_evidence_analyst:
  - If the already-fixed timeshift cycle later matches the exact comparator, close it as ordinary pending-state/experience-reuse semantics with no mechanism uplift?
  - Require replay/update ratio to be counted as a resource in future credit-learning comparisons?
  - Keep API outcome replay distinct from biological/internal neural replay unless an actual reactivation process is identified?
questions_for_control_brain:
  - Add outcome-event consumption/replay multiplicity and update-to-data ratio to the ordinary credit/replay reduction checklist?
  - Keep PRE_FORMAL/FORMAL and H7 unchanged by this SYSTEM/API line?
  - Avoid any duplicate Utility request while the fixed SUB timeshift object is active?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - predecessor replay terminal at 6fa2114ff5f68bb940abd21600a587b460293097
  - fresh timeshift prospective contract 50223b84e7e30cec2c4dcb136e58c0b4674df966
  - R33 Assembly-set PRE_FORMAL execution b907403e972af7df8a6502dfe4c54bdbb0d23475 and its R34 method-limited canonicalization
  - no outcome dispatch, contract edit, rescue, retune, rerun, rescore, STARTED, TEST, PRE_FORMAL/FORMAL promotion, research merge, immutable-ref mutation, or scheduler change by this role
utility_request_created: null
```
