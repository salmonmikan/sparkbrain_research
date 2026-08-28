# Spark Dynamic Cognition — Theory Specification v0.3

> **Status:** working, falsifiable engineering specification
>
> **Package boundary:** the checked-in package is `0.3.0`; `v0.3.1` is corrective work until
> versioned implementation and release evidence are complete.
>
> **Compatibility boundary:** persisted v0.2 config/state/trace payloads remain schema `0.2`.
> This specification adds explicit v0.3 contracts; it never silently upgrades a v0.2 payload.

## 0. Scope and non-claims

This document is the v0.3 normative specification. `THEORY_SPEC_v0.2.1.md` remains the normative
legacy-reference specification for the accepted v0.2 engine. Where a v0.3 contract is absent or
not yet integrated, this document records that absence rather than inventing behavior.

SparkBrain is a local, inspectable research system. It is not a reproduction of a human brain,
a conscious system, AGI, a biologically equivalent model, or evidence of hardware energy
efficiency. A passed engineering gate is not scientific support beyond its registered boundary.

## 1. Versioned state domains

A v0.3 run is an explicit state tuple:

```text
BrainState = (sensory, entities, evidence, coalition, beliefs, workspace,
              concept_observer, organ_observer, action, world_feedback,
              trace_lineage, rng, configuration)
```

Every field must be either serializable, reconstructible from a recorded trace, or explicitly
reported as `not_implemented`. A future integrated runtime may not claim this tuple is complete
until all of its named components are live, checkpointed, and tested.

## 2. Raw and local sensory samples

A `SensorySample` is a local, finite observation with a sample ID, non-negative time, source ID,
modality, and value mapping. It is input data, not a conclusion. The reference path must not read
an evaluator answer key, official test label, remote API, or cloud service to construct a local
sample.

Input modes remain distinguishable:

| Mode | Meaning | Claim boundary |
|---|---|---|
| I0 | whole-string/hash diagnostic | information-loss control, not semantics |
| I1 | local compositional diagnostic | local structure retention, not semantic understanding |
| I2 | symbolic oracle diagnostic | upper-bound condition, excluded from autonomous claims |
| I3 | truth-free local adapter | not accepted until separately implemented and audited |

## 3. Sensory Field and Perceptual Sparks

The `AdaptiveSensoryField` inspects a local sample and records channel-local terms for
habituation, novelty, prediction error, and bounded goal bias. It emits `PerceptualSpark` records
only when the registered salience condition accepts the channel. Suppression is also an observable
outcome, not missing data.

All channels may still be inspected and scored. Therefore a reduction in emitted Sparks or
downstream active work does not establish reduced dense input work, wall-clock cost, or energy use.

## 4. Evidence identity, provenance, and lineage

An `EvidenceRecord` has a stable identity and records source, polarity, support/contradiction,
time, correlation group, lineage, and entity scope. Repeated propagation of one evidence ID is not
independent support. A correlated copy is not independent support merely because its ID differs.
Evidence mutations must preserve the audit path needed to identify active, removed, and restored
records.

## 5. Entity scope

Evidence may be evaluated under distinct entity modes:

| Mode | Definition | Boundary |
|---|---|---|
| E0 | no explicit entity scope | diagnostic control |
| E1 | oracle entity binding | not autonomous entity discovery |
| E2 | learned/autonomous slots | `not_implemented` unless a dedicated implementation and evidence exist |

An aggregate must not mix Oracle and autonomous rows. Entity cross-talk, evidence assignment, and
unavailable bindings must remain visible in the raw output.

## 6. Coalition state and ignition

A Coalition evaluates attributable active evidence for one `(entity, belief)` candidate. Its score
uses registered support, contradiction, source diversity, stability, and correlation-aware terms.
The C14 bounded Coalition score must be consumed by the declared ignition decision path, not merely
displayed beside a fixed decision.

Ignition requires the declared threshold, competitor margin, stability, and source conditions.
No-Ignition is a first-class result. Its reason taxonomy includes, at minimum, insufficient support,
insufficient independent sources, contradiction, below-threshold score, and insufficient margin;
unsupported reasons must fail closed rather than being inferred by a UI.

## 7. Persistent belief and revision outcomes

Persistent belief state represents competing candidates and may retain residual losers. A transition
is classified as `maintain`, `revise`, `recover`, or `no_ignition` only from recorded state and
registered conditions. Attribution identifies stored evidence; it does not manufacture a causal
explanation.

C15 established engineering behavior at its protocol boundary but did not support residual
superiority. An integrated runtime must retain that counterevidence and may not promote residual
retention to a general advantage without a new preregistered evaluation.

## 8. Workspace, action, and world feedback

A Workspace broadcast is an explicit post-ignition state transition. Action is distinct from a
belief: the minimum action vocabulary is `observe`, `withhold`, `inspect`, `commit_belief`,
`revise`, and a task-specific action. World feedback, when implemented, must return as a new local
sensory/evidence event rather than silently changing belief state.

At this revision, action selection and world feedback are not integrated v0.3 runtime evidence.
They are required future contracts, not implied by a final classification output.

## 9. Proto-concept candidates

`OnlineConceptFormer` may observe recurring label-free local patterns and expose proto-concept
candidates. Candidate observation is not semantic concept formation, functional utility, causal
necessity, or biological concept formation. A candidate may affect an experiment only after a
separate registered protocol defines held-out utility, matched controls, ablation, collateral
effects, and multiple-seed criteria.

## 10. Functional-organ candidates

A functional-organ candidate is a proposed structural group, not an accepted organ. Acceptance
requires the registered conjunction of structural cohesion, selective activation, held-out reuse,
targeted impairment, matched-control excess, bounded collateral damage, and seed consistency.
C17 is an engineering-complete scientific negative: no functional-organ claim is supported.

In a first integrated runtime, concept and organ components are observer-only and cannot alter
Coalition, belief, action, or scoring decisions.

## 11. Trace, checkpoint, replay, and fork

The additive `sparkbrain.v03_integration` contract uses schema `0.3`. A trace event has a branch,
sequence, parent hash, state hashes before/after, event kind, and explicit payload. Cited evidence
must already be active before the event. Inspection is pure and cannot advance dynamics or work
counters.

A checkpoint retains explicit state, configuration hash, trace hash chain, and parent lineage.
Replay validates the chain and terminal state hash before restoring stored state. A fork records
its parent checkpoint, parent state, fork point, and intervention. v0.2 payloads are never
implicitly interpreted as v0.3.

The C18 artifact validates this contract with a manually constructed trace. It does not establish
that a live integrated brain emitted that trace.

## 12. Integrated runtime contract

The future stable entrypoint is:

```python
from sparkbrain.v03 import IntegratedV03Brain, SensorySample, V03BrainConfig, V03StepResult
```

`IntegratedV03Brain` must be stateful and own an explicit configuration, local input interpreter,
entity mode, Sensory Field, Evidence Ledger, Coalition Gate, persistent belief state, workspace,
trace session, checkpoint state, and RNG state. The initial live reference path connects C12--C14.
C15 controller integration, action/world feedback, and learned modes require their own accepted
contracts. Legacy `SparkBrain` remains the v0.2-compatible root API.

## 13. Brain Lab boundary

Legacy `sparkbrain.lab` and `/api/runs*` remain the v0.2 reference UI. The live v0.3 runtime must
use `sparkbrain.v03` and `/api/v03/*`, with explicit schema `0.3` payloads. It must show stored
raw/local input, accepted/suppressed Sparks, entity assignment, evidence IDs and correlations,
Coalition decomposition, no-ignition reason, belief transition, observer-only candidates, action
when implemented, feedback when implemented, checkpoint lineage, and fork comparison.

The UI must not infer hidden state or turn a missing trace field into a positive attribution.

## 14. Scientific falsification conditions

- I1 failing to improve its registered input diagnostic remains a negative input result.
- E1 oracle binding does not falsify or establish autonomous E2 binding.
- Coalition must change the actual declared gate under causal removal/restoration tests.
- Equal full and no-residual outcomes do not support residual superiority.
- Candidate recurrence without held-out causal utility does not support concept formation.
- Candidate absence or failed causal controls does not support organ formation.
- A blocked C19 preflight supplies no external score, attribution, winner, or generalization claim.

## 15. Claim and release boundaries

C06 remains the recorded negative external result. C15 and C17 remain scientifically
`not_supported`; C16 is candidate-level; C18 is observability/replay engineering evidence only;
C19 is `blocked` / `not_evaluated`. CL-007 and CL-008 remain E0.

v0.3.1 evidence must be generated in a new versioned release directory from its own clean source
pin. It must not rewrite the v0.3.0 release layer or turn packaging, documentation, or integration
work into a scientific claim-grade upgrade. Public tag, archive, and release remain blocked until
the repository owner selects a project license.
