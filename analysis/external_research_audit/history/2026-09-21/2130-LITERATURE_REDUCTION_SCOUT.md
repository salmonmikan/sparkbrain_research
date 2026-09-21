# LITERATURE_REDUCTION_SCOUT — selection-aware inference and evidence masking

- schema_version: `2`
- generation_id: `LIT-20260921T213000+0900-R22-SELECTION-AWARE-INFERENCE-7C4A21E9`
- produced_at: `2026-09-21T21:30:03+09:00`
- producer_run_id: `external-literature-auto-20260921T213000+0900-R22-7C4A21E9`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260921T183800+0900-R21-HOLDOUT-EXHAUSTION-4E7C21A9`
- role: `LITERATURE_REDUCTION_SCOUT`
- schedule_slot: `21:30 JST`
- genuinely_new_information: `true`

Repository/control-plane inputs were re-fetched independently. Stable `main=ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; evidence tags=5; formal/sealed/tag-freeze=0; legacy freeze branches=13. Consumed generations: Control `CTRL-20260921T205220+0900-R25-9C4E21A7@e8441362f29e8369c549bf08fb6e32efafe72124`; Evidence Analyst `EVA-20260921T205800+0900-R43-6E2A91C5@5692a1b3f210ae2be2cef80266b6e4fc1c7a14d4`; MAIN `MAIN-20260921T212004+0900-PRIMARY-FUNNEL21-HOLD-R43-6A8C21D5@3087e24d3d3bdbdb768a33ba2a1c3e624777c11f`; SUB `SUB-20260921T203533+0900-NOOP-R42POSTMAIN-METHODHOLD-3C7A21E5@3e77cbae214809d3e08f09d500ab4b661fe1f53b`; prior Literature `LIT-20260921T183800+0900-R21-HOLDOUT-EXHAUSTION-4E7C21A9@e3908aae13ef167c603fa202d2e00bfc99916912`.

R43 has canonically closed `CAND-PREFORMAL-CROSS-GENERATION-HOLDOUT-EXPOSURE-INTEGRITY-01` as `HOLD_METHOD_LIMITED / TERMINAL_FOR_CURRENT_OBJECT / NOT_QUEUED`; no third rescue is permitted. MAIN is intentionally idle and SUB is no-target. This run does not reopen that object.

## Findings

1. Bibaut & Kallus (Annual Review 2025, DOI `10.1146/annurev-statistics-040522-015431`) show that adaptive experimentation can invalidate ordinary nonadaptive inference and requires an inferential procedure whose guarantees explicitly survive adaptivity. Therefore an exposure ledger is observability, not by itself validity.

2. Goeman & Solari (Biometrika 2024, DOI `10.1093/biomet/asad078`) emphasize that data splitting can leave the upstream selection procedure completely unconstrained as long as it is independent of the inference split. For SparkBrain's opaque multi-agent candidate supply, a fresh hidden confirmatory set is therefore a strong, simple validity floor, though not necessarily power-optimal.

3. Selective-inference/randomized-selection methods (Fithian, Sun & Taylor; Panigrahi, Fry & Taylor 2024, DOI `10.1093/biomet/asae019`) and safe/e-value testing (Grunwald, de Heide & Koolen 2024, DOI `10.1093/jrsssb/qkae011`) provide valid inference under specified adaptive processes. They do not automatically license unrestricted outcome-responsive hypothesis generation. Any reuse contract must state which adaptive choices the guarantee covers and preserve enough selection ancestry to verify the assumptions.

4. Sadibolova & Terhune (Behavior Research Methods 2025, DOI `10.3758/s13428-025-02813-0`) argue that seeing the evolving evidence state can itself alter experimenter behavior/protocol. In an agentic research loop, feedback visibility is therefore a separate integrity dimension from whether an exposure occurred. Protected feedback should be prospectively masked or reduced to allowed minimal signals during candidate generation.

## Consequence

Future clean PRE_FORMAL integrity should bind both **adaptivity observability** and **validity under that adaptivity**. The strongest ordinary paths are either a fresh independent confirmatory set after candidate/scorer/falsifier binding, or a prospectively specified selection-aware/always-valid reuse regime with machine-checkable assumptions and feedback visibility. This is methodology guidance only; no current immutable evidence is invalidated and #31 remains terminal.

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
novelty_or_reduction_impact: SELECTION_AWARE_INFERENCE_AND_MASKING_SHARPENING_NO_SCIENTIFIC_NOVELTY_UPLIFT
audit_classification: null
prospective_baselines_or_discriminators:
  - fresh independent confirmatory set hidden until candidate/scorer/falsifier binding
  - exposure ledger recording feedback class and observing agents
  - explicit candidate-choice ancestry
  - prospectively specified selective-inference/randomized-selection regime when reuse is necessary
  - always-valid/e-value regime only for the adaptive process actually covered
  - masked minimal protected-feedback interface during candidate generation
questions_for_evidence_analyst:
  - Keep #31 terminal/no-third-rescue and use this only prospectively?
  - Require both exposure observability and an explicit validity regime for a fresh scientific successor?
  - Prefer fresh independent confirmation if cross-agent selection ancestry cannot be represented faithfully?
questions_for_control_brain:
  - Add observability-versus-validity and feedback visibility/masking to the evidence-integrity checklist?
  - Require reuse methods to identify exactly which adaptive choices their guarantees cover?
  - Keep PRE_FORMAL/FORMAL empty and avoid manufacturing a SYSTEM object solely from this literature?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - R33 terminal disposition
  - #31 R43 HOLD_METHOD_LIMITED / TERMINAL_FOR_CURRENT_OBJECT / NOT_QUEUED disposition
  - no third #31 rescue, retrospective invalidation, protected-outcome reconstruction, rerun/rescore, STARTED/TEST, PRE_FORMAL/FORMAL promotion, research merge, immutable-ref mutation, Utility execution, or scheduler change
utility_request_created: null
```
