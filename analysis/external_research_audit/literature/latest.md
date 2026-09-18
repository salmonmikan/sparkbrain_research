# SparkBrain External Research — Literature Reduction Scout

Timestamp: `2026-09-19 06:33 JST`
Role: `LITERATURE_REDUCTION_SCOUT`

## Repository context

Repository science was re-fetched independently; `ops/*` branches were treated only as designated control-plane mailboxes.

- `main`: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- LP01 research head: `research/lp01-actual-lineage-causal-credit-spec-20260918@f6d59a55730c5f99cd7f30470847fc3f175bdf64`
- Authoritative annotated `evidence/*` tags: 5; `formal/*`: 0; `sealed/*`: 0.
- Control Brain: `ops/control-brain-handoff@10eb4206fb0c998fcdbc40c0e16f38829ea5d41e`
- Evidence Analyst: `ops/evidence-analyst-handoff@f2ca44cc99797dd13ddc20947558022c35ab2c60`
- MAIN report stream consumed through its 06:14 latest/state; SUB through 06:35 latest/state on `ops/orchestrator-run-report@b32ac63e6ee4d1fa8bcaf8f13b3c91bc9e42d901`.

Current programme status is `NO_HIGH_VALUE_OBJECT / experimental cognitive architecture testbed`. LP01 is closed pre-formal: no formal identity was consumed. The current LP01 reference implementation is explicitly an append-only parent relation (`ActualLineageIndex`) with opaque IDs and an ordinary explicit transitive-ancestor comparator (`ExplicitParentTable`). This is useful as a dev/reference object, but it does not yet establish an online native causal-credit mechanism.

The prior Literature stream covered PSRs, causal states/epsilon-machines, local causal states, reservoir/fading-memory universality and automata extraction. Those findings are not repeated here.

## Genuinely new external findings

### 1. LP01-like explicit ancestry is already a standard provenance problem

Buneman, Khanna & Tan (ICDT 2001) distinguish **why-provenance**—which source records influenced the existence of an output—from where-provenance. Green, Karvounarakis & Tannen (PODS 2007) go further: provenance semirings attach source variables to derivations and algebraically propagate/combine those annotations.

That is a strong reduction pressure on any future SparkBrain claim that is based only on retaining opaque source IDs and parent/ancestor relations. The present LP01 dev/reference index is structurally much closer to explicit provenance bookkeeping than to a new cognitive credit mechanism.

Prospective implication: if a lineage object is ever reopened for independent reasons, include a **provenance-only baseline** that propagates opaque source tokens/derivation supports with no SparkBrain dynamics or learning. A win over recent-window memory but not over provenance bookkeeping would not support novelty.

Sources:
- Buneman, Khanna & Tan, *Why and Where: A Characterization of Data Provenance*, ICDT 2001, DOI 10.1007/3-540-44503-X_20.
- Green, Karvounarakis & Tannen, *Provenance Semirings*, PODS 2007, DOI 10.1145/1265530.1265535.

### 2. Historical ancestry/provenance is not the same thing as actual causation

Halpern–Pearl structural-model work makes actual causation counterfactual/interventional rather than something that can simply be read from an ancestry graph. Classic **preemption** and **overdetermination** are exactly the cases where naive ancestry or simple but-for dependence is insufficient.

This sharply changes the admission bar for the residual `actual historical lineage` idea. A future object should not merely ask whether a source is an ancestor of an outcome. It should force two candidate lineages to have comparable provenance while differing in **actual causal responsibility under intervention**.

Prospective discriminator: construct redundant/backup/preempted routes. Preserve or closely match the provenance graph, then intervene on a candidate source/edge and ask whether only the actually responsible lineage receives credit. This is much stronger than source-token lookup or ancestor recovery.

Sources:
- Halpern & Pearl, structural-model actual causality framework (2005); modern summaries emphasize that actual causality cannot simply be read off a causal model and requires counterfactual witnesses/contingencies.
- Dyrkolbotn, *On Preemption and Overdetermination in Formal Theories of Causality*, 2017.

### 3. Query-answer causality gives an ordinary interventional comparator between provenance and causal credit

Database causality work operationalizes actual cause for a query answer by deleting a candidate tuple, possibly under a contingency set, and checking whether the answer disappears; causal responsibility increases as the minimum required contingency shrinks. This is important because it bridges exactly the gap relevant to SparkBrain: **provenance says what participated in a derivation; causality asks what was actually difference-making under controlled intervention**.

Prospective implication: before attributing lineage-specific credit to persistent dynamics, compare against an explicit event-DAG deletion/responsibility model under the same observable event envelope. If the ordinary counterfactual model identifies the same responsible source, the result reduces to standard causal attribution rather than a new circulation principle.

Source:
- Bertossi et al., query-answer causality / responsibility work, including *Causes for query answers from databases: Datalog abduction, view-updates, and integrity constraints*, International Journal of Approximate Reasoning, 2017.

### 4. Recent 2026 credit-assignment work independently reinforces the intervention requirement

Counterfactual Shapley Credit Assignment (Li, Lee & Bareinboim, 2026) explicitly targets the credit-assignment problem by separating policy contribution from environmental stochasticity via counterfactual Shapley values; related 2026 agent work estimates step contribution by controlled deletion/substitution interventions rather than temporal correlation alone.

This is not a direct architectural equivalent to SparkBrain, but it raises the contemporary bar: `delayed/history-specific credit` is not enough. A claimed causal-credit mechanism should recover **intervention-validated contribution**, especially when multiple plausible historical contributors or stochastic outcomes exist.

Prospective implication: if a future native lineage mechanism appears, preregister a small counterfactual-credit ground-truth suite where ancestry, temporal proximity and causal responsibility are deliberately dissociated.

Sources:
- Li, Lee & Bareinboim, *Counterfactual Shapley Credit Assignment*, RLC 2026 / arXiv:2607.16999.
- Meng, *Policy-Conditioned Counterfactual Credit for Verifiable Reinforcement Learning of Long-Horizon Language Agents*, arXiv:2606.05263 (2026).

## Reduction synthesis

The new literature does **not** justify reopening LP01. It strengthens the current stop decision. The residual programme question should be narrowed from `historical lineage can be retained/recovered` to:

> can a native, non-privileged mechanism assign credit to the **actual difference-making historical cause**, not merely an ancestor/provenance token, under preemption/overdetermination and matched ordinary provenance/counterfactual baselines?

A future admission ladder should therefore include:

`explicit provenance bookkeeping -> counterfactual actual-cause/responsibility baseline -> matched ordinary recurrent/plastic reductions -> only then a Spark-specific lineage-credit residual`.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - H7_LINEAGE_PROVENANCE_RESIDUAL
  - LP01_PREFORMAL_CLOSEOUT
  - PROGRAMME_NOVELTY
  - FUTURE_OBJECT_ADMISSION
  - CAUSAL_CREDIT_DISCRIMINATORS
novelty_or_reduction_impact: >
  STRONGER_REDUCTION_AND_ADMISSION_PRESSURE. Explicit historical ancestry/source-token
  propagation is well covered by provenance theory, while actual causal credit requires
  counterfactual/interventional distinction, especially under preemption and
  overdetermination. Current LP01 should remain closed; a future lineage object must beat
  both provenance-only and actual-cause/responsibility baselines under matched privilege.
audit_classification: null
prospective_baselines_or_discriminators:
  - provenance-only opaque-token / derivation-support propagation baseline
  - explicit event-DAG query-answer actual-cause / responsibility baseline
  - preemption and overdetermination cases with matched or near-matched provenance
  - ancestry-preserving but responsibility-changing interventions
  - counterfactual-credit ground-truth suite separating ancestry, temporal proximity, and difference-making
questions_for_evidence_analyst:
  - Keep LP01 closed; do not treat provenance recovery as evidence of actual causal credit.
  - Should any future H7/lineage admission require a prospectively fixed actual-cause/responsibility gate, not only ancestry recovery?
  - Should provenance-only and counterfactual-responsibility comparators be mandatory before a lineage object can reach formal review?
questions_for_control_brain:
  - Should the residual theory be renamed/narrowed from lineage provenance to intervention-validated lineage-specific causal responsibility?
  - Add provenance semiring / explicit ancestry bookkeeping and actual-cause responsibility to the ordinary-reduction ladder?
  - Retain NO_HIGH_VALUE_OBJECT until a native mechanism independently creates this distinction rather than engineering a new benchmark to rescue LP01?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - canonical PD01/NI01/H5 terminal classifications
  - all consumed A01/RV01/RV02/CX identities and legacy immutable refs
  - LP01 remains pre-formal and must not be upgraded from this literature alone
  - no outcome-responsive successor, identity, STARTED, official TEST, rerun, retune, or rescore
```
