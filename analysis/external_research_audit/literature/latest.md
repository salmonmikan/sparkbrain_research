# SparkBrain External Research — Literature Reduction Scout

Timestamp: `2026-09-19 09:32 JST`
Role: `LITERATURE_REDUCTION_SCOUT`

## Repository context

Repository science was re-fetched independently; `ops/*` branches were treated only as designated control-plane mailboxes.

- `main`: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- LP01 research head: `research/lp01-actual-lineage-causal-credit-spec-20260918@f6d59a55730c5f99cd7f30470847fc3f175bdf64`
- Authoritative annotated `evidence/*` tags: 5; legacy `freeze/*` branches: 13.
- Control Brain: `ops/control-brain-handoff@10eb4206fb0c998fcdbc40c0e16f38829ea5d41e`
- Evidence Analyst: `ops/evidence-analyst-handoff@7a2ef7021fdaa3dd701353a18b45b6db4915756c`
- MAIN latest commit consumed: `904e9e041a26d102d87f0a6ac088385619fad363` (09:14 report).
- SUB report stream advanced during this run through `e8ab335ab67a81b9ab2fc299a0266b7b32fd5d6c` (09:35 no-op reconciliation).

Current programme status remains `NO_HIGH_VALUE_OBJECT / experimental cognitive architecture testbed`. LP01 remains closed pre-formal with no formal identity. Its current reference code is still explicit bookkeeping: `ActualLineageIndex` stores append-only parent/child relations, `ExplicitParentTable` stores transitive ancestor sets, and `RecentWindowState` is a bounded comparator. No new formal scientific evidence appeared.

The 06:33 Literature run already covered provenance semirings, ancestry-vs-actual-causality, query-answer causality, and counterfactual credit. Earlier runs covered PSRs, causal states/epsilon-machines, reservoirs/fading memory, local causal states, and automata extraction. Those findings are not repeated here.

## Genuinely new external findings

### 1. Causal-history tokens plus competition/conflict already have an ordinary Petri-net/event-structure reduction

Petri-net causal semantics explicitly represent dependencies between transition occurrences. Under the individual-token interpretation, tokens are distinguished by their causal history; process semantics recover a partial order of causal dependencies. More recent causal-net/event-structure work also represents concurrency and asymmetric conflict explicitly.

This raises the bar beyond the 06:33 provenance finding. A future SparkBrain object that retains opaque token identities, ancestry, concurrent alternatives, or winner/loser history is not yet outside standard formal machinery. In particular, `historical lineage + local competition/conflict` can be represented by occurrence/causal nets and event structures without invoking a novel cognitive credit principle.

Prospective implication: if a native lineage mechanism independently appears, include an **individual-token causal-net/event-structure baseline** that receives the same event envelope and tests whether the claimed causal-history/competition effect is exactly reconstructible as ordinary partial-order/conflict state.

Sources:
- van Glabbeek, Goltz & Schicke, *On Causal Semantics of Petri Nets*, arXiv:2103.00729 (2021).
- Melgratti, Mezzina & Pinna, *Relating Reversible Petri Nets and Reversible Event Structures, categorically*, Logical Methods in Computer Science 21(2:20), published 2025-06-05, DOI 10.46298/lmcs-21(2:20)2025.

### 2. Dynamic slicing is a stronger ordinary baseline than ancestry alone for actual-run influence

Dynamic slicing asks which executed statements/events actually affected a selected outcome in a particular run. Perera, Garg & Cheney extend this to concurrent systems and show a causally consistent slicing relation: causally equivalent executions yield the same slicing structure up to isomorphism.

This fills an important gap in the reduction ladder. Provenance/ancestry records participation; full structural-model actual causality asks counterfactual responsibility. **Causally consistent dynamic slicing** supplies an intermediate ordinary baseline that follows actual execution dependencies while respecting concurrency and causal equivalence, without requiring SparkBrain-style persistent dynamics.

Prospective implication: a future lineage-credit claim should beat three distinct levels rather than only one explicit parent table: provenance/ancestry, actual-run dynamic dependence/slicing, and counterfactual actual-cause/responsibility. A result that exceeds ancestry but is exactly recovered by a dynamic slice is still ordinary trace dependence, not a new causal-credit mechanism.

Source:
- Perera, Garg & Cheney, *Causally Consistent Dynamic Slicing*, CONCUR 2016, DOI 10.4230/LIPIcs.CONCUR.2016.18.

### 3. Local/online/spiking credit assignment is now too well populated to carry novelty by itself

Generalized Latent Equilibrium (GLE) derives fully local spatio-temporal credit assignment for physical dynamical neuronal networks from neuron-local mismatch signals, with phase-free continuous-time local plasticity. Separately, Spike-based Alignment Learning (SAL), published 2026-07-07, provides a synapse-local STDP-compatible mechanism for maintaining effective weight alignment in noisy spiking systems and explicitly frames locality in space and time as the core credit-assignment constraint.

Neither result is an architectural equivalent of SparkBrain's remaining lineage-specific hypothesis, and neither by itself solves preemption/actual-responsibility attribution. But together they make `local`, `online`, `physical`, `spiking`, or `history-sensitive learning` unusable as standalone novelty axes.

Prospective implication: any future Spark-specific causal-credit object must demonstrate **lineage-selective, intervention-validated responsibility under matched local information** beyond ordinary local physical credit rules—not merely that learning occurs without global backpropagation or semantic lookup.

Sources:
- *Backpropagation through space, time and the brain*, Nature Communications 17, Article 66 (2026), DOI 10.1038/s41467-025-66666-z; published 2025-12-26.
- Gierlich et al., *Spike-based alignment learning solves the weight transport problem*, Nature Communications 17, 8699 (2026), DOI 10.1038/s41467-026-74460-8; published 2026-07-07.

## Reduction synthesis

No literature finding justifies reopening LP01. The current close/HOLD decision is strengthened.

The lineage residual should now be evaluated on two orthogonal reduction axes:

1. **History/influence representation:** `provenance -> causal-net/event-structure history + conflict -> causally consistent dynamic slice -> counterfactual actual-cause/responsibility`.
2. **Learning/locality:** `ordinary local eligibility/three-factor/e-prop/GLE/SAL/recurrent-plastic mechanisms -> Spark-specific residual only if intervention-validated lineage selectivity remains under matched privilege/resources`.

A future object is scientifically interesting only if it arises natively and survives both axes. Designing a benchmark solely because these papers suggest one would be rescue-driven and should remain disallowed while `NO_HIGH_VALUE_OBJECT` holds.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - H7_LINEAGE_CAUSAL_CREDIT_RESIDUAL
  - LP01_PREFORMAL_CLOSEOUT
  - PROGRAMME_NOVELTY
  - FUTURE_OBJECT_ADMISSION
  - CAUSAL_CREDIT_REDUCTION_LADDER
novelty_or_reduction_impact: >
  STRONGER_REDUCTION_PRESSURE. Causal-history token identity, concurrency and conflict can be
  represented by causal/occurrence-net and event-structure formalisms; actual-run influence
  has an ordinary causally-consistent dynamic-slicing baseline; and local/online/spiking
  credit assignment is already strongly populated by contemporary physical-learning work.
  LP01 should remain closed. A future Spark-specific residual must demonstrate native,
  intervention-validated lineage responsibility that survives both history/influence and
  local-learning reduction axes under matched privilege/resources.
audit_classification: null
prospective_baselines_or_discriminators:
  - individual-token causal-net / occurrence-net / event-structure baseline
  - causally consistent dynamic-slicing baseline on the same event envelope
  - explicit counterfactual actual-cause / responsibility baseline
  - matched local physical credit comparator family where learning is central
  - preemption/overdetermination cases separating ancestry, trace influence, and responsibility
questions_for_evidence_analyst:
  - Keep LP01 closed; do not count causal-history retention or conflict tracking alone as actual causal credit.
  - Should future lineage admission require survival of provenance, event-structure/dynamic-slice, and actual-cause baselines before formal review?
  - When local learning is claimed, require matched local-information comparators rather than treating locality itself as novelty?
questions_for_control_brain:
  - Organize the residual reduction ladder into separate history/influence and learning/locality axes?
  - Remove local/online/spiking credit assignment as standalone novelty evidence?
  - Retain NO_HIGH_VALUE_OBJECT until a native mechanism independently creates an intervention-validated residual rather than engineering a successor from literature?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - canonical PD01/NI01/H5 terminal classifications
  - all consumed A01/RV01/RV02/CX identities and legacy immutable refs
  - LP01 remains pre-formal and must not be upgraded from this literature alone
  - no outcome-responsive successor, identity, STARTED, official TEST, rerun, retune, or rescore
```
