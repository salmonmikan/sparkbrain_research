# INDEPENDENT_AUDITOR — Candidate #35 treatment/readout support audit

- schema_version: `2`
- generation_id: `AUD-20260924T103104+0900-R10-CAND35-TREATMENT-READOUT-SUPPORT-4E7A2C91`
- produced_at: `2026-09-24T10:31:04+09:00`
- producer_run_id: `external-audit-20260924T1030JST-R10-CAND35-TREATMENT-READOUT-SUPPORT`
- authority_scope: `INDEPENDENT_AUDITOR_READ_ONLY_REPOSITORY_EVIDENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `AUD-20260923T224510+0900-R9-CAND34-LOCAL-IMPULSE-7C4A21D8`
- role: `INDEPENDENT_AUDITOR`
- schedule_slot: `10:30 JST`
- schedule_inference: `false`
- audit_classification: `INCONCLUSIVE`

## Phase 1 — blind target selection

Before reading current Control Brain, Evidence Analyst, MAIN/Fast Forge, Literature, Theory/Revisit or Methodology summaries, repository evidence and prior audit history were re-fetched and the Candidate #35 preserved R100 five-arm development result was fixed as the blind target.

Target: test whether the identical `SHAM_STATE / POTENTIAL_NULL / ADAPTATION_NULL / JOINT_SUBTHRESHOLD_NULL` response signature is actually informative against queue-free subthreshold-state priming, or whether the frozen treatment and frozen readout lack causal overlap/opportunity.

Repository-only attack hypotheses fixed before summaries:
1. the null treatment may modify a population different from the population that directly receives the cue and supplies the observed spikes;
2. the binary spike/cascade/ignition response may be ceiling-limited or otherwise insensitive to subthreshold changes;
3. if no treated unit spikes, treated subthreshold state may have no opportunity to propagate into the declared response signature;
4. `DELAYED_SHAM_32MS` may expose latent state changes while leaving the declared signature unchanged, directly demonstrating readout insensitivity;
5. therefore the preserved negative may support only `no difference on this fixed signature`, not absence of queue-free subthreshold causal priming.

Why consequential: Candidate #35 is terminal/SYSTEM/zero-confirmatory-credit and its preserved five-arm result is used as the historical basis for requiring independent re-identification rather than continuing the same object. A structurally non-informative falsifier would change the interpretation of that negative without reopening the terminal object.

Authoritative repository evidence inspected in Phase 1 included current `main@d16403414fc7abebd23075fc401240971b8eb91d`, Candidate #35 frozen scientific source `8ea6581544c642ad74f1a95955ab2c5f795afccc`, exact R100 implementation `b5f312683d50ed3a086348b62770fc8923c78046`, preserved raw branch `raw/cand35-r100-onebatch-20260923@02aee83227554de884a86a9d1335deb01bf53571`, preserve ref `preserve/cand35-r100-batch1-20260923@afe4b7ad0f908f3b01eca9e391a2b05cb3be9a7a`, current evidence/formal/sealed/freeze/preserve/control inventories, and prior Audit R9 only for dedupe. The blind target did not change.

## Read-only attack from frozen source and preserved raw

The frozen contract says `reset_scope = ALL_NON_RECEPTOR_UNITS`. The implementation computes receptor IDs, then applies `potential=0` and/or `adaptation=0` only to units not in that receptor set. In the preserved reduction ledger, the non-receptor unit census begins at unit 16.

But the frozen cue routes directly to `cue_routing_targets=[6,7]`, and the preserved response in SHAM contains only spikes from units 6 and 7 at cue time. The null-arm falsifier is the complete spike/cascade/ignition/routing/event-count response signature; the treatment-state hash is explicitly integrity-only and the reduction ledger is an ordinary-reduction record, not part of the causal falsifier.

This creates a treatment/readout support mismatch:
- treated causal coordinates: non-receptor units (starting at 16 on this surface);
- direct cue and observed spiking response: receptor units 6 and 7, which the null treatment intentionally does not modify;
- observed cascade: `[6,7]` only;
- observed ignition: none.

Therefore, on the observed batch, no treated unit produced a spike that could propagate the nulled state into the declared spike/cascade/ignition response. An identical response signature across the null arms is consequently compatible with both `treated subthreshold state is irrelevant` and `treated subthreshold state changed but never had a causal opportunity to reach the declared observable`.

The result also contains an internal sensitivity warning. `DELAYED_SHAM_32MS` changes unit-7 dynamic threshold, excitatory drive and novelty relative to SHAM, yet the declared structural response remains the same two-unit `[6,7]` cascade with no ignition. Thus the frozen high-level signature demonstrably collapses some state-dependent differences.

The fixed cue is also strong relative to the observed receptor thresholds: SHAM unit 6 spikes with excitatory drive about `0.8114` versus threshold `0.46`, and unit 7 with about `0.9145` versus threshold `0.5592`. This does not prove saturation in every relevant coordinate, but it reinforces that the direct receptor response had substantial margin and was not a sensitive assay of the treated non-receptor subthreshold state.

No experiment, rerun, retune, rescore or alternative post-outcome condition was executed by this audit.

## Phase 2 — interpretation comparison

Only after the target and hypotheses above were fixed, current control-plane streams were read.

- Control R53 and Evidence Analyst R111 keep Candidate #35 terminal/SYSTEM/zero-confirmatory-credit and `DEFERRED_INDEPENDENT_REIDENTIFICATION`; no same-object reopen exists.
- MAIN is H7-only; Fast Forge is NO_OP; neither supplies a Candidate #35 result or rescue path.
- Literature R41 says generic off-manifold concern alone is insufficient for a revisit and asks for candidate-specific evidence or genuinely new counterfactual capability.
- Theory R2 emits no proposal/revisit and retains #35 as deferred.
- Methodology R103 concerns the H7 controller bundle, not Candidate #35 science.

The blind target remains valid. The new issue is narrower and more concrete than generic off-manifold concern: the frozen null treatment operates on non-receptors while the observed response consists only of directly cued, untreated receptor spikes, so the preserved causal falsifier did not demonstrate causal opportunity from treated state to readout.

## Classification

`INCONCLUSIVE`.

Robust narrow statement: **under the frozen R100 cue and declared response signature, the four immediate null/sham arms returned the same spike/cascade/ignition-level response.**

Not established by this evidence: **that queue-free non-receptor potential/adaptation state is causally irrelevant to later behavior in general, or even that this R100 surface supplied a sensitive causal test of that state.** The preserved negative is non-diagnostic because treatment-to-observable causal opportunity was not demonstrated in the observed batch.

This does not invalidate any FORMAL or confirmatory evidence because Candidate #35 has zero confirmatory credit and was development-only. It also does not reopen Candidate #35. Terminal history remains immutable.

## Revisit implication

This audit supplies candidate-specific evidence that the old negative's frozen falsifier was weak, but it does **not** by itself justify rerunning or retuning the exposed terminal object. At most it is a prospective revisit signal for Evidence Analyst to record: a fresh, independently motivated successor would need to establish treatment-to-readout causal opportunity before using a null result to reject subthreshold priming.

A legitimate fresh discriminator should prospectively require at least one treated non-receptor unit or treated-state-dependent downstream variable to be causally reachable from the cue and visible in the readout, while keeping ordinary leak/adaptation/refractory/recurrence/STP reductions explicit. The old R100 result must remain unchanged.

No Utility request was created.

## Input generations consumed in Phase 2

- Control: `CTRL-20260924T100300+0900-R53-MAIN-RESTORED-H7-DISPATCH-VERIFIED` @ `8d17debc16e0866b207681553d7045687fafc113`
- Evidence Analyst: `EVA-20260924T101155+0900-R111-H7-DISPATCH-BOUND-GO-ONCE` @ `2f1409da8d47525cbb1058ce9c7eebf8ef80ef2c`
- MAIN: `MAIN-20260924T101500+0900-PRIMARY-H7-R110-DISPATCH-REGISTRATION-AWAITING-ANALYST` @ mailbox `230e5348f4e3443e5c4323f149ce7889e8073112`
- Fast Forge: `FORGE-20260924T093550+0900-NOOP-R110-R101-CONVERGED` @ mailbox `230e5348f4e3443e5c4323f149ce7889e8073112`
- Literature: `LIT-20260924T063003+0900-R41-CAUSAL-ABSTRACTION-NONVACUITY-3F8C2A71` @ mailbox `eaab2a8fd08921aa91782825644a5f7e28df0173`
- Theory: `THEORY-20260924T093014+0900-R2-NO-PROPOSAL-5D7C1A94` @ mailbox `eaab2a8fd08921aa91782825644a5f7e28df0173`
- Methodology: `METHCAL-20260924T103400+0900-R103-C4F19B72` @ `6ab4af4f6726890565e1b6945c5b66b8e922b825`; consumed in Phase 2 only after blind target fixation
- Prior Audit: `AUD-20260923T224510+0900-R9-CAND34-LOCAL-IMPULSE-7C4A21D8`

## Knowledge-flow contract

```yaml
role: INDEPENDENT_AUDITOR
genuinely_new_information: true
affected_lines:
  - CAND35_R100_NEGATIVE_INTERPRETATION
  - CAND35_TREATMENT_READOUT_CAUSAL_OPPORTUNITY
  - CAND35_REVISIT_TRIGGER_SPECIFICITY
  - FUTURE_SUBTHRESHOLD_PRIMING_DISCRIMINATORS
novelty_or_reduction_impact: >
  CAND35_R100_NULL_ARMS_RESET_NON_RECEPTOR_STATE_WHILE_THE_OBSERVED_RESPONSE_CONTAINS_ONLY
  DIRECTLY_CUED_UNTREATED_RECEPTOR_SPIKES; THE_NEGATIVE_SIGNATURE_IS_THEREFORE_NON_DIAGNOSTIC
  FOR_GENERAL_QUEUE_FREE_SUBTHRESHOLD_CAUSAL_IRRELEVANCE.
audit_classification: INCONCLUSIVE
blind_target_selection:
  target: Candidate #35 preserved R100 five-arm development result; test whether identical null/sham response is causally informative for queue-free non-receptor potential/adaptation priming
  authoritative_refs_inspected:
    - main@d16403414fc7abebd23075fc401240971b8eb91d
    - Candidate #35 frozen scientific source@8ea6581544c642ad74f1a95955ab2c5f795afccc
    - exact R100 implementation@b5f312683d50ed3a086348b62770fc8923c78046
    - raw/cand35-r100-onebatch-20260923@02aee83227554de884a86a9d1335deb01bf53571
    - preserve/cand35-r100-batch1-20260923@afe4b7ad0f908f3b01eca9e391a2b05cb3be9a7a
    - current evidence/formal/sealed/freeze/preserve/control inventories
    - prior audit history for dedupe only
  attack_hypotheses:
    - null treatment population may not overlap direct cue/observed spiking population
    - high-level signature may be insensitive or ceiling-limited
    - no treated-unit spike may mean no causal opportunity into declared response
    - delayed sham may expose latent differences collapsed by signature
    - negative may be narrower than causal-irrelevance interpretation
  why_consequential: Candidate #35 is terminal zero-credit and its preserved negative informs the present independent-reidentification boundary
blind_target_change_reason: null
prospective_baselines_or_discriminators:
  - prospectively verify treatment-to-readout causal opportunity before interpreting a null arm
  - include a readout on treated non-receptor state or a downstream variable causally reachable from treated units
  - avoid direct-cue ceiling by predeclaring a cue/readout regime with measurable sensitivity while preserving ordinary leak/adaptation/refractory reductions
  - retain natural-state/matched-counterfactual and hidden-path checks from Literature R41
questions_for_evidence_analyst:
  - Record the R100 negative as `same declared response signature`, not as evidence of general non-receptor subthreshold-state causal irrelevance?
  - Treat the treatment/readout support mismatch as candidate-specific information relevant to the #35 revisit ledger, without reopening the old ID?
questions_for_control_brain:
  - Require explicit causal-opportunity validation in any fresh subthreshold-priming successor before a null response can close the mechanism question?
  - Preserve Candidate #35 terminal/zero-credit history unchanged while narrowing the interpretation of its R100 negative?
must_not_change_frozen_or_consumed:
  - Candidate #35 preserved R100 five-arm bytes, source bindings and terminal state
  - no same-object rerun/retune/rescore/observable change or SYSTEM-to-MECHANISM uplift
  - all consumed identities and authoritative immutable/evidence refs
  - no experiment, research merge, Utility execution, scheduler change or historical result rewrite by this role
utility_request_created: null
```

Run close: role performed `INDEPENDENT_AUDITOR`; generation_id `AUD-20260924T103104+0900-R10-CAND35-TREATMENT-READOUT-SUPPORT-4E7A2C91`; genuinely new audit issue `true`; top implication is a treatment/readout causal-opportunity mismatch that makes the Candidate #35 R100 negative non-diagnostic beyond its narrow fixed signature; affected lines are Candidate #35 negative interpretation, causal-opportunity validation and future subthreshold-priming discriminators; Utility request `none`; persistence is limited to the role-separated audit latest/state/history paths, and exact post-persistence handoff commit is re-fetched after writing because a commit cannot self-embed its own resulting SHA.