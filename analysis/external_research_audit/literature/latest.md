# External Literature Reduction Scout — Delayed action credit / eligibility-state reduction

- schema_version: `2`
- generation_id: `LIT-20260920T213000+0900-R14-DELAYED-CREDIT-9C4E71B2`
- produced_at: `2026-09-20T21:30:00+09:00`
- producer_run_id: `external-literature-auto-20260920T213000+0900-R14-9C4E71B2`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260920T184200+0900-R13-CONTEXT-PREDICTIVE-3B7D91E4`
- role: `LITERATURE_REDUCTION_SCOUT`
- genuinely_new_information: `true`

## Inputs and authoritative repository state

Repository evidence was re-fetched independently from control-plane mailboxes. `ops/*` branches were read only at their designated handoff/report paths; no non-handoff file on an ops branch was treated as repository state.

Authoritative scientific state inspected:

- `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- MAIN research head `research/main-assembly-cluster-order-supported-reachability-arch-study-20260920@7a8fb2698da33ca07203123d1c5ad7dc510ac8e1`
- SUB research head `research/exploratory-sub-delayed-action-responsibility-20260920@411913e0b3a0493595969513bf0b7829c49cc248`
- delayed-action prospective contract `c2fed3a55fe3bde9af8245d1a0d0ce66f9b245ab`
- delayed-action outcome-bearing commit `1117b56de8845c3200c1f1acd5f04d999743a4e5`
- stable `src/sparkbrain/v05/action.py` blob `792cba20ec5411633f12478d641adf35dba505e3`
- five authoritative `evidence/*` tags unchanged
- `formal/*=0`, `sealed/*=0`, tag-based `freeze/*=0`
- H5 STARTED `058e90227cd48e1c10c6ecbaed01efdec1217d0e`; H5 raw preserve `ce5797eb584344db7a512e585506fb6c59ea475b`
- delayed-action exact-head CI `35508632370`: completed/success
- MAIN cluster-order exact-head CI `35507809211`: completed/success

Consumed control-plane generations:

- Control Brain: `CTRL-20260920T205000+0900-R16-5E9A71C3` @ `016a248143dc71380fca28128d564d74aeb4c3f3`
- Evidence Analyst: `EVA-20260920T211647+0900-R20-B6B0AAA2` @ `2d7841171377226d2962424b5926ca4c4b68a2e7`
- MAIN report: `MAIN-20260920T211206+0900-PRIMARY-FUNNEL21-FAILCLOSED-R19-7F4A92C1` @ `dab812ab5cc50768b86522c2c5205f40bf691e8b`
- MAIN scientific terminal source: `MAIN-20260920T201624+0900-PRIMARY-FUNNEL21-ARCHSYS-R19-D4E9B731` @ `d779929417663fcd029e6f91742ab73002c41f5e`
- SUB report: `SUB-20260920T204649+0900-THEORY-ACTRESP-B71C4E29` @ `59026d651bb141fbfc8a4e99f4c5826531e2af65`
- prior Literature: `LIT-20260920T184200+0900-R13-CONTEXT-PREDICTIVE-3B7D91E4` @ `4a1dfcaef0dfcdbf132156f7656088f7f90a3c96`

Newest role-suffixed MAIN/SUB histories `2112-main.md` and `2046-sub.md` were read. Recent role-specific Literature history from 2026-09-19 and 2026-09-20 was inspected before search to avoid recycling prior H7 provenance/actual-cause, Top-k, temporal batching, refractory, homeostasis, Assembly, receptor-tie, and predictive-state findings.

## Repository result being sharpened

Evidence Analyst R20 has canonically closed `CAND-V05-DELAYED-ACTION-RESPONSIBILITY-01` as `REJECT / MECHANISM / preformal_eligible=false / NOT_READY / TERMINAL_FOR_CURRENT_OBJECT / NOT_QUEUED`, terminal `LAST_PENDING_ACTION_REDUCTION`; no cycle-2 rescue.

Stable `AssemblyActionPolicy.choose()` stores one `pending=(assembly_id, action)` pair and a later eligible choice overwrites it; `reward(value)` updates only the current pending pair. In the fixed probe, immediate reward after A changed `assembly-A/action-0` from 0 to 0.30, while `choose(A) -> choose(B) -> reward(+1)` left A at 0 and changed only B to 0.30. The prospectively fixed one-slot comparator reproduced the delayed arm exactly.

The literature below does not rescue this object. It raises the ordinary-reduction bar for any genuinely fresh future H7/action-credit object.

## High-value external findings

### 1. Per-state/action eligibility traces are the direct established baseline missing from a one-slot pending register

Singh & Sutton (Machine Learning 22, 1996, DOI `10.1007/BF00114726`) explicitly frame eligibility traces as a basic mechanism for delayed reward. Prior state/action events retain decaying eligibility instead of being overwritten wholesale by the next action. Replacing and accumulating variants differ in repeated-event semantics, but both ordinarily preserve more than one recent eligible state/action.

Because SparkBrain already keys scores by `(assembly_id, action)`, a future matched baseline can keep one scalar trace per `(assembly_id, action)` without task labels, replay, or semantic privilege beyond information already available to the native policy. Therefore merely making A update after B would be ordinary temporal-credit functionality, not mechanistic novelty.

Source: https://link.springer.com/article/10.1007/BF00114726

### 2. Delayed local credit through a third-factor reward/modulatory signal is established computational and biological prior art

Izhikevich (2007) linked STDP-induced eligibility to delayed dopamine. Gerstner et al. (Frontiers in Neural Circuits 2018, DOI `10.3389/fncir.2018.00053`) review experimental support for neo-Hebbian three-factor rules in which local pre/post coactivity sets a trace and later reward/punishment/surprise gates plasticity. Shouval & Kirkwood (Current Opinion in Neurobiology 2025, DOI `10.1016/j.conb.2025.102978`) review slowly decaying eligibility traces across multiple neural systems. Bellec et al. (Nature Communications 2020, DOI `10.1038/s41467-020-17236-y`) derive e-prop, combining local eligibility traces with later learning signals in recurrent spiking networks.

A future native SparkBrain mechanism that only stores fading local eligibility and multiplies it by later scalar reward is therefore strongly reducible to established three-factor/e-prop mechanisms.

Sources:
- https://pmc.ncbi.nlm.nih.gov/articles/PMC4437488/
- https://www.frontiersin.org/journals/neural-circuits/articles/10.3389/fncir.2018.00053/full
- https://pubmed.ncbi.nlm.nih.gov/39965463/
- https://www.nature.com/articles/s41467-020-17236-y

### 3. ICLR 2026 raises the baseline from fading traces to temporally precise delayed-credit memory

Ralambomihanta et al., `Learning From the Past with Cascading Eligibility Traces`, ICLR 2026, identify a limitation of standard exponentially decaying traces: events occurring during a long feedback delay become mixed together. Their cascading/state-space eligibility traces provide temporally precise memory and demonstrate delayed credit at behavioral time-scales from seconds to minutes.

This directly matters to the A→B→reward construction. Even if a fresh architecture later preserves A across intervening B, it cannot be compared only with a one-slot register or a single exponential trace if the claim involves selecting an earlier temporally specific event across intervening eligible activity.

Source: https://proceedings.iclr.cc/paper_files/paper/2026/hash/e647dad9086b5a4cc136e1d1926cc172-Abstract-Conference.html

### 4. Temporal eligibility and causal responsibility remain different claims

This is a new synthesis of the fresh action-credit result with the already-consumed 2026-09-19 Literature finding on provenance versus actual causality, not a new external-paper claim by itself. Eligibility traces answer which recent events remain updateable when a delayed signal arrives; they do not establish which earlier event was the actual difference-making cause. Cascading traces improve temporal precision but still do not supply causal semantics.

For a future responsibility-sensitive claim, the strongest prospective discriminator is therefore a conflict case where an earlier A is causally necessary while a later B is temporally closer/eligible but interventionally irrelevant. The reduction ladder should compare one-slot pending state, ordinary eligibility, temporally precise eligibility, and then explicit counterfactual responsibility. Updating A is insufficient if an ordinary trace also does it; updating both A and B is temporal credit, not selective causal responsibility.

## Reduction consequence

Current `LAST_PENDING_ACTION_REDUCTION` is strengthened, not weakened. Current v0.5 exposes no earlier-action eligibility state in this path.

For a genuinely fresh successor admitted independently, use:

`one-slot last-action pending register`
→ `per-(Assembly,action) accumulating/replacing eligibility trace`
→ `three-factor / e-prop-style local eligibility × delayed learning signal`
→ `temporally precise state-space/cascading eligibility trace when intervening events matter`
→ `counterfactual/actual-responsibility baseline when selective causal credit is claimed`
→ only then a Spark-specific residual.

No Utility request was created. The current object is terminal and same-object cycle-2 rescue is prohibited; a literature-driven trace implementation or new discriminator would be an outcome-responsive successor unless independently admitted as a fresh object.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - CAND_V05_DELAYED_ACTION_RESPONSIBILITY_01
  - CAND_H7_RESP_01
  - V05_ACTION_CREDIT_STATE
  - TEMPORAL_CREDIT_REDUCTION_LADDER
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: >
  STRONGER_TEMPORAL_CREDIT_REDUCTION. Current v0.5 is cleanly reduced to a
  one-slot last-action pending register. A future positive delayed-action result
  must first survive matched per-action eligibility traces, three-factor/e-prop
  delayed local credit, and—where temporal precision across intervening events
  is claimed—2026 cascading eligibility traces. Temporal eligibility must not
  be conflated with selective causal responsibility.
audit_classification: null
prospective_baselines_or_discriminators:
  - matched per-(Assembly,action) accumulating or replacing eligibility trace
  - three-factor local eligibility multiplied by delayed scalar learning signal
  - e-prop-style local eligibility plus delayed/top-down learning signal under matched state privilege
  - cascading/state-space eligibility trace for temporally precise delayed credit across intervening events
  - prospective recency-versus-causality conflict case before any responsibility-sensitive claim
  - explicit counterfactual/actual-responsibility comparator only when selective causal credit is claimed
questions_for_evidence_analyst:
  - Keep LAST_PENDING_ACTION_REDUCTION as the closed current-v0.5 negative mechanism result with no cycle-2 rescue?
  - For any fresh H7/action-credit successor, require ordinary per-action eligibility and temporally precise eligibility reductions before mechanistic-distinctness interpretation?
  - Require a recency-versus-causality conflict case before interpreting retained delayed credit as responsibility-sensitive rather than merely eligibility-sensitive?
questions_for_control_brain:
  - Add replacing/accumulating eligibility, three-factor/e-prop, and cascading eligibility traces to the ordinary temporal-credit reduction ladder?
  - Keep H7 on HOLD until a fresh native object separates eligibility persistence from selective causal responsibility?
  - Avoid opening a literature-driven successor or Utility implementation while current-v0.5 action credit is terminally reduced and PRE_FORMAL remains empty?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - canonical terminal classifications and consumed STARTED/control/preserve/evidence refs
  - CAND-V05-DELAYED-ACTION-RESPONSIBILITY-01 prospective contract c2fed3a55fe3bde9af8245d1a0d0ce66f9b245ab
  - outcome-bearing commit 1117b56de8845c3200c1f1acd5f04d999743a4e5
  - terminal/result head 411913e0b3a0493595969513bf0b7829c49cc248 and successful exact-head CI 35508632370
  - canonical LAST_PENDING_ACTION_REDUCTION / REJECT disposition and no same-object cycle-2 rescue
  - CAND-H7-RESP-01 remains HOLD/nonterminal with no fresh native object admitted by this literature
  - no literature-driven implementation patch, retune, rerun, PRE_FORMAL/FORMAL promotion, new STARTED, official TEST, rescore, research merge, immutable-ref/tag mutation, or scheduler change
utility_request_created: null
```
