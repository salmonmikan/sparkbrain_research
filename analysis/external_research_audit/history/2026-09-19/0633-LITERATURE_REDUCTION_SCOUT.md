# SparkBrain External Research — Literature Reduction Scout

Timestamp: `2026-09-19 06:33 JST`
Role: `LITERATURE_REDUCTION_SCOUT`

## Repository / control-plane state consumed

- `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- `research/lp01-actual-lineage-causal-credit-spec-20260918@f6d59a55730c5f99cd7f30470847fc3f175bdf64`
- 5 authoritative annotated `evidence/*` tags; no `formal/*` or `sealed/*` tags.
- Control Brain `10eb4206fb0c998fcdbc40c0e16f38829ea5d41e`
- Evidence Analyst `f2ca44cc99797dd13ddc20947558022c35ab2c60`
- MAIN latest/state through 06:14; SUB latest/state through 06:35, report branch tip observed `b32ac63e6ee4d1fa8bcaf8f13b3c91bc9e42d901`.

Current programme state is `NO_HIGH_VALUE_OBJECT / architecture-testbed mode`. LP01 is closed pre-formal and consumed no formal identity. Its current dev/reference implementation explicitly stores append-only parent relations and includes an ordinary explicit transitive-ancestor comparator. No formal experiment or evidence was produced in this scout run.

## New external findings

1. **Explicit lineage is ordinary provenance.** Buneman–Khanna–Tan why-provenance and Green–Karvounarakis–Tannen provenance semirings already formalize source participation and propagation of derivation tokens. A future lineage claim based only on opaque source IDs / ancestor relations is reducible to provenance bookkeeping unless it demonstrates more.

2. **Provenance/ancestry is not actual causality.** Halpern–Pearl actual causality requires counterfactual/interventional witnesses and contingency reasoning; preemption and overdetermination are decisive cases where ancestry or naive but-for dependence is insufficient. A future SparkBrain lineage object should separate historical participation from actual difference-making responsibility.

3. **Query-answer causality is a direct ordinary comparator.** Database causality identifies an actual cause by deletion, possibly under a contingency set, and causal responsibility by the minimum contingency required. This provides a simple explicit event-DAG counterfactual baseline between provenance and causal credit.

4. **2026 credit-assignment work raises the same bar.** Counterfactual Shapley Credit Assignment and policy-conditioned counterfactual credit explicitly use interventions to separate genuine causal contribution from temporal correlation / environmental stochasticity. They are not direct architectural equivalents, but they make intervention-validated contribution the relevant contemporary comparison.

## Scientific implication

This literature does **not** justify reopening LP01. It strengthens the stop decision. The residual should be narrowed to whether a native, non-privileged mechanism can assign credit to the **actual difference-making historical cause**, not merely preserve/recover an ancestor token, under preemption/overdetermination and matched provenance/counterfactual baselines.

Prospective reduction ladder:

`explicit provenance bookkeeping -> counterfactual actual-cause/responsibility baseline -> matched ordinary recurrent/plastic reductions -> only then a Spark-specific lineage-credit residual`.

## Sources

- Buneman, Khanna & Tan, *Why and Where: A Characterization of Data Provenance*, ICDT 2001, DOI 10.1007/3-540-44503-X_20.
- Green, Karvounarakis & Tannen, *Provenance Semirings*, PODS 2007, DOI 10.1145/1265530.1265535.
- Halpern & Pearl, structural-model actual causality framework.
- Chockler & Halpern, *Responsibility and Blame: A Structural-Model Approach*, JAIR 2004.
- Bertossi et al., *Causes for query answers from databases: Datalog abduction, view-updates, and integrity constraints*, IJAR 2017.
- Li, Lee & Bareinboim, *Counterfactual Shapley Credit Assignment*, RLC 2026 / arXiv:2607.16999.
- Meng, *Policy-Conditioned Counterfactual Credit for Verifiable Reinforcement Learning of Long-Horizon Language Agents*, arXiv:2606.05263.

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
  propagation is ordinary provenance; actual causal credit requires intervention and
  counterfactual responsibility. Current LP01 remains closed. A future lineage object
  must beat provenance-only and actual-cause/responsibility baselines under matched privilege.
audit_classification: null
prospective_baselines_or_discriminators:
  - provenance-only opaque-token / derivation-support propagation baseline
  - explicit event-DAG actual-cause / responsibility baseline
  - preemption and overdetermination cases with matched or near-matched provenance
  - ancestry-preserving but responsibility-changing interventions
  - counterfactual-credit suite separating ancestry, temporal proximity, and difference-making
questions_for_evidence_analyst:
  - Keep LP01 closed; provenance recovery is not actual causal credit.
  - Require an actual-cause/responsibility gate for any future H7/lineage admission?
  - Require provenance-only and counterfactual-responsibility comparators before formal review?
questions_for_control_brain:
  - Narrow the residual to intervention-validated lineage-specific causal responsibility?
  - Add provenance bookkeeping and actual-cause/responsibility to the ordinary-reduction ladder?
  - Retain NO_HIGH_VALUE_OBJECT until a native mechanism independently creates this distinction?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - canonical PD01/NI01/H5 terminal classifications
  - consumed A01/RV01/RV02/CX identities and legacy immutable refs
  - LP01 remains pre-formal and is not upgraded by this literature
  - no outcome-responsive successor, identity, STARTED, official TEST, rerun, retune, or rescore
```
