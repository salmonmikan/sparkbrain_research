# External Literature Reduction Scout — selection-aware inference and evidence masking

- schema_version: `2`
- generation_id: `LIT-20260921T213000+0900-R22-SELECTION-AWARE-INFERENCE-7C4A21E9`
- produced_at: `2026-09-21T21:30:03+09:00`
- producer_run_id: `external-literature-auto-20260921T213000+0900-R22-7C4A21E9`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260921T183800+0900-R21-HOLDOUT-EXHAUSTION-4E7C21A9`
- role: `LITERATURE_REDUCTION_SCOUT`
- schedule_slot: `21:30 JST`
- schedule_inference: `false`
- genuinely_new_information: `true`

## Inputs / authoritative state

Repository evidence was re-fetched independently from all `ops/*` mailboxes immediately before persistence. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; exactly five annotated `evidence/*` tags remain; `formal/*`, `sealed/*`, and tag-form `freeze/*` remain empty; 13 legacy `freeze/*` branches and preserve namespaces were independently rechecked. PR #148/#149 remain open and unmerged. No fresh FORMAL identity or scientific immutable-ref movement was observed.

Consumed control-plane generations and exact handoff commits:

- Control Brain: `CTRL-20260921T205220+0900-R25-9C4E21A7` @ `e8441362f29e8369c549bf08fb6e32efafe72124` (branch tip observed `835c175de2db7220e22919a3a27c76406b8cef46`)
- Evidence Analyst: `EVA-20260921T205800+0900-R43-6E2A91C5` @ `5692a1b3f210ae2be2cef80266b6e4fc1c7a14d4`
- MAIN: `MAIN-20260921T212004+0900-PRIMARY-FUNNEL21-HOLD-R43-6A8C21D5` @ `3087e24d3d3bdbdb768a33ba2a1c3e624777c11f`
- SUB: `SUB-20260921T203533+0900-NOOP-R42POSTMAIN-METHODHOLD-3C7A21E5` @ `3e77cbae214809d3e08f09d500ab4b661fe1f53b`
- prior Literature: `LIT-20260921T183800+0900-R21-HOLDOUT-EXHAUSTION-4E7C21A9` @ `e3908aae13ef167c603fa202d2e00bfc99916912`

The material repository/control-plane delta is now canonical: Evidence Analyst R43 closed `CAND-PREFORMAL-CROSS-GENERATION-HOLDOUT-EXPOSURE-INTEGRITY-01` as `HOLD_METHOD_LIMITED / TERMINAL_FOR_CURRENT_OBJECT / NOT_QUEUED`, after MAIN's final prospectively allowed safe-metadata cycle could not machine-check protected-set exposure/feedback semantics. No third rescue is permitted. MAIN R43 is intentionally idle with no current object; SUB remains no-target. This Literature run does not reopen that terminal SYSTEM object.

## High-value external findings

### 1. An exposure ledger is observability, not by itself a statistical validity mechanism

Bibaut & Kallus, *Annual Review of Statistics and Its Application* 2025 (DOI `10.1146/annurev-statistics-040522-015431`), review inference after adaptive experiments and show that adaptivity can invalidate the ordinary asymptotic-normal approximations used in nonadaptive settings. Validity requires a method whose guarantees explicitly survive the adaptive process, such as suitable reweighting, always-valid inference, or direct characterization of the distribution induced by adaptivity.

Impact: a future SparkBrain exposure ledger would be valuable because it makes prior protected-set interactions observable, but the ledger alone does not make a later score confirmatory. A clean successor must also bind the inferential regime that turns that recorded adaptivity into a valid claim.

### 2. Independent confirmatory data are a particularly robust floor when candidate generation is opaque

Goeman & Solari, *Biometrika* 2024 (DOI `10.1093/biomet/asad078`), describe data splitting as a selective-inference construction in which one data part is used for selection and the other for inference. A distinctive property is that the selection procedure can be completely unconstrained as long as it remains independent of the inference part. They also show that basic splitting can be power-inefficient, so this is a robustness floor, not an optimality claim.

Impact: SparkBrain's candidate generator is distributed across Analyst/Control/MAIN/SUB and literature feedback. If that cross-agent selection mechanism is too complex to model faithfully, a fresh confirmatory set that stayed hidden until candidate/scorer/falsifier binding gives a simple ordinary validity boundary even when the upstream selection algorithm is effectively arbitrary.

### 3. Reusing protected data requires binding the selection-aware inference mechanism, not merely recording that reuse occurred

Fithian, Sun & Taylor's selective-inference framework conditions error guarantees on the fact that a hypothesis/test was selected, while Panigrahi, Fry & Taylor's 2024 *Biometrika* paper (DOI `10.1093/biomet/asae019`) gives exact selective inference under randomized selection for a defined model class. Separately, Grünwald, de Heide & Koolen's *Safe testing* (*JRSS B* 2024, DOI `10.1093/jrsssb/qkae011`) shows e-values can preserve Type-I error guarantees under optional continuation when the e-value construction itself is valid.

Impact: these are prospective alternatives when reuse is scientifically necessary, but none is a generic license for opaque outcome-responsive hypothesis generation. A future contract must state which selection/stopping process the guarantee covers and preserve enough candidate ancestry/feedback metadata to verify those assumptions. If that cannot be represented, fresh independent confirmation is the safer ordinary comparator.

### 4. Evidence visibility is a methodological control plane distinct from statistical stopping validity

Sadibolova & Terhune, *Behavior Research Methods* 2025 (DOI `10.3758/s13428-025-02813-0`), argue that awareness of the current evidence state can itself alter experimenter behavior and protocol, creating an internal-validity confound even apart from the mathematics of optional stopping. They recommend explicit masked/unmasked phases and, where possible, limiting communication to minimal decisions rather than evidence magnitude/direction/trajectory.

Impact: in an agentic research loop, full protected-set score trajectories can influence later candidate design even if each individual scorer is preregistered. Future SparkBrain integrity should therefore distinguish `exposure occurred` from `what information was visible to candidate-design agents`. A ledger should record feedback class/visibility, and protected evidence should be masked or reduced to prospectively allowed signals until the next scientific object is fixed.

## Reduction consequence

This is a methodology/integrity sharpening, not a scientific novelty uplift and not evidence that any existing immutable result is invalid. R43's current holdout-exposure object remains terminal because its safe metadata cannot reconstruct the needed semantics; literature does not authorize a third rescue.

For a genuinely fresh future PRE_FORMAL successor, the stronger ordinary integrity ladder is:

`development/exploration data`
→ `outcome-blind candidate/scorer/falsifier binding`
→ `durable raw-only preserve + exact provenance`
→ `cross-generation exposure + feedback-visibility ledger`
→ **either** `fresh independent confirmatory data`
→ **or** `prospectively specified selection-aware / always-valid reuse regime whose assumptions are machine-checkable`
→ `scored preserve / claim review`

The decisive distinction is that **observability of adaptivity and validity under adaptivity are different requirements**.

No Utility request is created. With no active scientific object and #31 explicitly terminal/no-third-rescue, an implementation request now would manufacture SYSTEM activity rather than test an independently admitted scientific question.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - CAND_PREFORMAL_CROSS_GENERATION_HOLDOUT_EXPOSURE_INTEGRITY_01
  - FUTURE_PREFORMAL_SELECTION_AWARE_VALIDITY
  - SCIENTIFIC_HOLDOUT_FEEDBACK_VISIBILITY
  - CROSS_GENERATION_CANDIDATE_ANCESTRY
  - PROGRAMME_EVIDENCE_INTEGRITY
novelty_or_reduction_impact: >
  SELECTION_AWARE_INFERENCE_AND_MASKING_SHARPENING_NO_SCIENTIFIC_NOVELTY_UPLIFT.
  Exposure accounting is necessary observability but is not itself a validity guarantee.
  Future confirmatory work must either use protected data independent of candidate selection,
  or prospectively bind a selection-aware/always-valid reuse mechanism whose assumptions
  and feedback visibility are machine-checkable.
audit_classification: null
prospective_baselines_or_discriminators:
  - fresh independent confirmatory set kept hidden until candidate/scorer/falsifier binding
  - cross-generation exposure ledger that records feedback class and which agents could observe it
  - explicit candidate-choice ancestry from protected feedback to successor selection
  - prospectively specified selective-inference/randomized-selection regime when reuse is necessary
  - always-valid/e-value regime only for the stopping/continuation process actually covered by its guarantee
  - masked evidence interface exposing only prospectively allowed minimal decisions during candidate generation
questions_for_evidence_analyst:
  - Keep #31 terminal/no-third-rescue and treat this only as prospective design guidance?
  - For a fresh scientific successor, require both exposure observability and an explicit validity regime rather than treating a ledger as sufficient?
  - Prefer fresh independent confirmation when cross-agent selection ancestry cannot be faithfully represented for selective inference?
questions_for_control_brain:
  - Add `observability != statistical validity` and feedback-visibility masking to the evidence-integrity checklist?
  - Require future reusable-holdout/selective-inference proposals to state exactly which adaptive choices their guarantee covers?
  - Keep PRE_FORMAL/FORMAL empty and avoid manufacturing a SYSTEM implementation object solely from this literature?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - R33 terminal NONCONFORMING_RAW_BEFORE_SCORE / HOLD_METHOD_LIMITED disposition
  - CAND-PREFORMAL-CROSS-GENERATION-HOLDOUT-EXPOSURE-INTEGRITY-01 canonical R43 HOLD_METHOD_LIMITED / TERMINAL_FOR_CURRENT_OBJECT / NOT_QUEUED disposition
  - no third #31 rescue, retrospective invalidation, protected-outcome reconstruction, rerun/rescore, STARTED/TEST, PRE_FORMAL/FORMAL promotion, research merge, immutable-ref mutation, Utility execution, or scheduler change
utility_request_created: null
```
