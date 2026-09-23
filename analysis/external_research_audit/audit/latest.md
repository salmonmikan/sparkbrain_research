# INDEPENDENT_AUDITOR — candidate #34 D34-Q002 preserved-result reduction audit

- schema_version: `2`
- generation_id: `AUD-20260923T224510+0900-R9-CAND34-LOCAL-IMPULSE-7C4A21D8`
- produced_at: `2026-09-23T22:45:10+09:00`
- producer_run_id: `external-audit-20260923T2230JST-R9-CAND34-LOCAL-IMPULSE`
- authority_scope: `INDEPENDENT_AUDITOR_READ_ONLY_REPOSITORY_EVIDENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `AUD-20260923T103000+0900-R8-CAND34-OPPORTUNITY-7D4A21C8`
- role: `INDEPENDENT_AUDITOR`
- schedule_slot: `22:30 JST`
- schedule_inference: `false`
- audit_classification: `REDUCIBLE`

## Phase 1 — blind target selection

Before reading current Control Brain, Evidence Analyst, MAIN/Fast Forge, or Literature summaries, this run re-fetched repository evidence and fixed the newly preserved Candidate #34 D34-Q002 PRE_FORMAL development result as the blind target.

Target: determine whether the preserved primary observation is mechanistically diagnostic of an Assembly temporal route, or whether it is fully explained by ordinary local edge transmission and membrane decay that also occurs on matched non-target edges.

Repository-only attack hypotheses fixed before summaries:
1. destination membrane response may be determined directly by configured edge weight and delay;
2. matched non-target edges may show the same response, defeating Assembly specificity;
3. destination units may never spike, leaving no downstream state transition;
4. secondary Assembly response may be only passive membrane tails;
5. the result may therefore support only narrow physical edge influence and be reducible as a mechanism claim.

Why consequential: D34-Q002 is a newly preserved response-bearing result from a MECHANISM-track candidate and could otherwise be overinterpreted as evidence for an Assembly-specific temporal-route mechanism.

Authoritative repository evidence inspected before strategy summaries included `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`, closed R2 source `43d0f25541a3c447d4c7156303647ae94f3119f4`, response branch `8ce961dc88fb52afa6399093fce1e3de7e982f2b`, preserve ref `preserve/cand34-d34-q002-r94-raw-20260923@4d45f1135bcb607f1e663648cd8335333eb98de4`, current evidence refs/tags, formal/sealed/freeze inventory, and prior audit history for dedupe only. The blind target did not change.

## Read-only recomputation from preserved raw

The preserved raw explicitly remains `PREFORMAL_DEVELOPMENT_ONLY_ZERO_CONFIRMATORY_CREDIT`; no FORMAL action, official scoring, or confirmatory credit exists.

For all four target edges, the sham destination potential at nominal arrival equals the configured edge weight exactly. One millisecond later it equals the same weight multiplied by the frozen 18ms membrane decay:

- `-0.4 * exp(-1/18) = -0.3783837875627062`
- `+0.2 * exp(-1/18) = +0.1891918937813531`
- `+0.9 * exp(-1/18) = +0.8513635220160889`
- `+0.8 * exp(-1/18) = +0.7567675751254124`

These values match the preserved raw at floating-point precision. The `+1ms` arm does not expose an extra residual: it simply moves the unchanged edge amplitude one millisecond later. The transmission-null arm is exactly zero at both sampled times.

Matched non-target controls show the same local pattern with their own near-matched weights/delays: null gives zero and `+1ms` exposes the control edge weight at the shifted arrival. Thus this immediate destination response is not specific to Assembly-internal edges.

No tested target destination unit spikes within the 64ms measurement window in the preserved target rows. The secondary Assembly export therefore does not demonstrate a downstream target-unit spike/state transition; where a tail remains, it is consistent with passive decay of the local edge impulse.

## Phase 2 — interpretation comparison

Only after blind target fixation and the read-only recomputation, current control-plane streams were read.

Control Brain R43 records D34-Q002 as preserved-before-interpretation, development-only, zero confirmatory credit, with repeat response prohibited and scientific interpretation deferred. Evidence Analyst R99 treats Candidate #34 as a historical preserved PRE_FORMAL-development result rather than current FORMAL evidence. Current MAIN is working Candidate #35 non-result preservation; current Fast Forge is an unrelated non-evidentiary homeostasis dead end. Literature R39 concerns Candidate #35 off-manifold null interventions and does not alter this audit target.

There is therefore no conflict between the independent reduction and current control-plane governance. The new point is mechanistic: the preserved D34-Q002 primary response itself contains no demonstrated Assembly-specific residual beyond ordinary local edge physics.

## Classification

`REDUCIBLE`.

The narrow statement **"the configured source-only cue causes the tested edge to physically alter its destination membrane potential with the configured weight/delay"** is robust so far. The broader interpretation **"D34-Q002 demonstrates an Assembly-specific temporal-route mechanism"** is not supported by this result because the primary measurement is exactly predicted by local edge weight, delay, and 18ms membrane decay; matched non-target edges exhibit the same immediate behavior; and no target destination spike/downstream transition is observed.

This does not invalidate any existing FORMAL or confirmatory evidence. D34-Q002 remains a preserved PRE_FORMAL development result with zero confirmatory credit.

No Utility request was created. The reduction is already computable from immutable preserved raw and frozen source; no new execution is needed.

## Prospective implication

Do not modify, rerun, rescore, or rescue D34-Q002. If a fresh successor later seeks Assembly-route mechanism uplift, prospectively require:
- an exact local impulse-response baseline using edge weight, delay, membrane time constant, and local state;
- target-internal versus matched-non-target residual comparison after that local baseline is removed;
- a downstream spike/state transition or Assembly-level effect that cannot be algebraically predicted from the immediate local membrane impulse.

## Knowledge-flow contract

```yaml
role: INDEPENDENT_AUDITOR
genuinely_new_information: true
affected_lines:
  - CAND34_D34_Q002_PREFORMAL_INTERPRETATION
  - CAND34_ASSEMBLY_TEMPORAL_ROUTE_SPECIFICITY
  - CAND34_LOCAL_IMPULSE_RESPONSE_REDUCTION
  - CAND34_FUTURE_MECHANISM_ADMISSION
novelty_or_reduction_impact: D34_Q002_PRIMARY_RESPONSE_IS_EXACTLY_REDUCIBLE_TO_LOCAL_EDGE_WEIGHT_DELAY_AND_18MS_MEMBRANE_DECAY; NO_ASSEMBLY_SPECIFIC_MECHANISM_UPLIFT
audit_classification: REDUCIBLE
blind_target_selection:
  target: newly preserved Candidate #34 D34-Q002 PRE_FORMAL result, audited for Assembly-specific temporal-route content versus ordinary local impulse response
  authoritative_refs_inspected:
    - main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d
    - research/main-cand34-assembly-route-preformal-r92-cycle4@43d0f25541a3c447d4c7156303647ae94f3119f4
    - research/main-cand34-assembly-route-preformal-r93-response@8ce961dc88fb52afa6399093fce1e3de7e982f2b
    - preserve/cand34-d34-q002-r94-raw-20260923@4d45f1135bcb607f1e663648cd8335333eb98de4
    - current evidence/formal/sealed/freeze and legacy preserve/control inventories
  attack_hypotheses:
    - primary membrane response may be ordinary weight/delay physics
    - matched non-target controls may reproduce it
    - no destination spike may occur
    - secondary Assembly response may be passive tail only
    - broader mechanism interpretation may reduce to ordinary local dynamics
  why_consequential: first newly preserved response-bearing result on this MECHANISM-track Candidate #34 surface
blind_target_change_reason: null
prospective_baselines_or_discriminators:
  - exact local impulse-response baseline from weight, delay, 18ms membrane decay and local state
  - Assembly-internal versus matched-non-target residual after local-kernel normalization
  - downstream target spike/state-transition/Assembly effect beyond immediate membrane response
questions_for_evidence_analyst:
  - Cap D34-Q002 at the narrow local physical-edge influence supported by the preserved raw?
  - Treat broader Assembly temporal-route mechanism interpretation as reduced absent a residual beyond the local impulse model?
questions_for_control_brain:
  - Require a prospectively frozen local-impulse residual discriminator in any fresh successor before mechanism uplift?
  - Keep D34-Q002 preserved, development-only, zero-credit, and non-rescuable in place?
must_not_change_frozen_or_consumed:
  - preserve/cand34-d34-q002-r94-raw-20260923 exact bytes and provenance
  - frozen Candidate #34 R2 contract/source and response branch
  - all consumed identities and immutable evidence
  - no D34-Q002 rerun/rescore/retune or outcome-responsive reinterpretation
  - no FORMAL action, research merge, immutable-ref mutation, Utility execution, or scheduler change
utility_request_created: null
```

Durable persistence limitation: a Git commit cannot contain its own final SHA without changing itself. The append-only history object records the generation and consumed commits; the exact post-persistence branch tip is verified after writing and reported by the run, rather than self-embedded in its own commit.