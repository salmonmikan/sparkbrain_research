# SparkBrain External Research — Literature Reduction Scout

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
- active MAIN research head `research/main-assembly-cluster-order-supported-reachability-arch-study-20260920@7a8fb2698da33ca07203123d1c5ad7dc510ac8e1`
- active/recent SUB research head `research/exploratory-sub-delayed-action-responsibility-20260920@411913e0b3a0493595969513bf0b7829c49cc248`
- delayed-action prospective contract `c2fed3a55fe3bde9af8245d1a0d0ce66f9b245ab`
- delayed-action outcome-bearing commit `1117b56de8845c3200c1f1acd5f04d999743a4e5`
- stable `src/sparkbrain/v05/action.py` blob `792cba20ec5411633f12478d641adf35dba505e3`
- five authoritative `evidence/*` tags unchanged
- `formal/*=0`, `sealed/*=0`, tag-based `freeze/*=0`; legacy freeze branches and preserve/control refs were rechecked through the current control/evidence handoffs
- H5 STARTED `058e90227cd48e1c10c6ecbaed01efdec1217d0e`; H5 raw preserve `ce5797eb584344db7a512e585506fb6c59ea475b`
- exact-head CI `35508632370` for delayed-action result: completed/success
- exact-head CI `35507809211` for MAIN cluster-order Architecture result: completed/success

Consumed control-plane generations:

- Control Brain: `CTRL-20260920T205000+0900-R16-5E9A71C3` @ `016a248143dc71380fca28128d564d74aeb4c3f3`
- Evidence Analyst: `EVA-20260920T211647+0900-R20-B6B0AAA2` @ `2d7841171377226d2962424b5926ca4c4b68a2e7`
- MAIN report: `MAIN-20260920T211206+0900-PRIMARY-FUNNEL21-FAILCLOSED-R19-7F4A92C1` @ `dab812ab5cc50768b86522c2c5205f40bf691e8b`
- MAIN scientific terminal source: `MAIN-20260920T201624+0900-PRIMARY-FUNNEL21-ARCHSYS-R19-D4E9B731` @ `d779929417663fcd029e6f91742ab73002c41f5e`
- SUB report: `SUB-20260920T204649+0900-THEORY-ACTRESP-B71C4E29` @ `59026d651bb141fbfc8a4e99f4c5826531e2af65`
- prior Literature: `LIT-20260920T184200+0900-R13-CONTEXT-PREDICTIVE-3B7D91E4` @ `4a1dfcaef0dfcdbf132156f7656088f7f90a3c96`

Newest role-suffixed MAIN/SUB histories `2112-main.md` and `2046-sub.md` were read. Recent role-specific Literature history from 2026-09-19 and 2026-09-20 was inspected before external search so the prior H7 provenance/actual-cause, Top-k, temporal batching, refractory, homeostasis, Assembly, receptor-tie, and predictive-state findings were not recycled as new literature.

## Repository result being sharpened

`CAND-V05-DELAYED-ACTION-RESPONSIBILITY-01` is now canonically closed by Evidence Analyst R20 as `REJECT / MECHANISM / preformal_eligible=false / NOT_READY / TERMINAL_FOR_CURRENT_OBJECT / NOT_QUEUED`, terminal `LAST_PENDING_ACTION_REDUCTION`; no cycle-2 rescue.

The stable implementation is especially simple: `AssemblyActionPolicy.choose()` stores exactly one `pending=(assembly_id, action)` pair and each later eligible choice overwrites it; `reward(value)` updates only the score for the current pending pair. In the fixed probe, immediate reward after A changed `assembly-A/action-0` from 0 to 0.30, whereas `choose(A) -> choose(B) -> reward(+1)` left A at 0 and changed only B to 0.30. The prospectively fixed one-slot last-action comparator reproduced the delayed arm exactly.

This result is a clean negative result for current v0.5 action-credit state. The external literature below does not rescue or relabel it; it raises the ordinary-reduction bar for any genuinely fresh future H7/action-credit object.

## High-value external findings

### 1. Per-state/action eligibility traces are the direct established baseline that the one-slot pending register lacks

Singh & Sutton (Machine Learning 22, 1996, `Reinforcement Learning with Replacing Eligibility Traces`, DOI `10.1007/BF00114726`) explicitly describe eligibility traces as a basic mechanism for handling delayed reward. A trace is retained for prior state/action events and decays rather than being overwritten wholesale by the next action. Replacing and accumulating variants differ in repeated-event semantics, but both preserve more than one recent eligible state/action in the ordinary case.

SparkBrain implication: because the native policy already keys scores by `(assembly_id, action)`, a future matched ordinary baseline can keep one scalar trace per `(assembly_id, action)` without task labels, replay, or semantic identity beyond information already available to the native policy. In the A→B→reward construction, such a baseline can retain nonzero eligibility for A while also representing B. Therefore merely making A update after B would be standard temporal-credit functionality, not a new mechanism.

Source: https://link.springer.com/article/10.1007/BF00114726

### 2. Delayed local credit via a third-factor reward/modulatory signal is established in computational neuroscience and biologically supported

Izhikevich (2007) linked STDP-induced synaptic eligibility to delayed dopamine so activity can be reinforced after the original spike interaction has passed. Gerstner et al. (Frontiers in Neural Circuits 2018, DOI `10.3389/fncir.2018.00053`) review experimental support for neo-Hebbian three-factor rules in which local pre/post coactivity sets an eligibility trace and a later reward/punishment/surprise factor converts that trace into plasticity. Shouval & Kirkwood (Current Opinion in Neurobiology 2025, DOI `10.1016/j.conb.2025.102978`) review evidence for slowly decaying synaptic eligibility traces across multiple neural systems. Bellec et al. (Nature Communications 2020, DOI `10.1038/s41467-020-17236-y`) derive e-prop, where local eligibility traces combine with later learning signals for recurrent spiking networks.

SparkBrain implication: a future native mechanism that only stores a fading local eligibility and multiplies it by later scalar reward would sit squarely inside established three-factor/e-prop territory. Novelty would require a sharper residual than delayed reward acting on retained local state.

Sources:
- https://pmc.ncbi.nlm.nih.gov/articles/PMC4437488/
- https://www.frontiersin.org/journals/neural-circuits/articles/10.3389/fncir.2018.00053/full
- https://pubmed.ncbi.nlm.nih.gov/39965463/
- https://www.nature.com/articles/s41467-020-17236-y

### 3. A 2026 result raises the baseline from fading traces to temporally precise delayed-credit memory

Ralambomihanta et al., `Learning From the Past with Cascading Eligibility Traces`, ICLR 2026, directly identifies a weakness of standard exponentially decaying traces: events occurring during a long feedback delay become mixed together. Their cascading/state-space eligibility traces provide temporally precise memory and demonstrate delayed credit over behavioral time-scales from seconds to minutes.

This is especially relevant to SparkBrain's A→B→reward discriminator. Even if a fresh architecture later preserves A across intervening B, that observation can no longer be compared only with a one-slot register or a single exponential trace. If the scientific claim involves selecting an earlier temporally specific event across intervening eligible activity, a temporally structured eligibility-memory baseline is now directly relevant.

Source: https://proceedings.iclr.cc/paper_files/paper/2026/hash/e647dad9086b5a4cc136e1d1926cc172-Abstract-Conference.html

### 4. Temporal eligibility and causal responsibility must remain separate claims

This is a synthesis of the fresh action-credit result with the already-consumed 2026-09-19 Literature finding on provenance versus actual causality, not a claim of new external literature by itself. Eligibility traces answer `which recent events remain updateable when a delayed signal arrives`; they do not by themselves establish `which earlier event was the actual difference-making cause`. The new ICLR 2026 cascading-trace result sharpens this distinction because it improves temporal precision without supplying causal semantics.

SparkBrain implication: a future H7/action-credit claim should include a prospective conflict case in which temporal recency and causal responsibility disagree—for example, an earlier A is causally necessary for the delayed outcome while a later B is eligible/closer in time but interventionally irrelevant. The ordinary reduction ladder should compare one-slot pending state, ordinary per-action eligibility, temporally precise/cascading eligibility, and only then an explicit counterfactual/responsibility baseline. A positive result that merely updates A is insufficient if an ordinary trace does the same; a positive result that updates both A and B is temporal credit, not selective causal responsibility.

## Reduction consequence

The current `LAST_PENDING_ACTION_REDUCTION` is strengthened, not weakened. Current v0.5 exposes no earlier-action eligibility state in this path. For any independently selected fresh successor, the prospective reduction ladder should be:

`one-slot last-action pending register`
→ `per-(Assembly,action) accumulating/replacing eligibility trace`
→ `three-factor / e-prop-style local eligibility × delayed learning signal`
→ `temporally precise state-space/cascading eligibility trace when intervening events matter`
→ `counterfactual/actual-responsibility baseline when the claim is selective causal credit`
→ only then a Spark-specific residual, if any.

The strongest future discriminator is therefore not simply `does A update after B?`; it is whether the mechanism preserves/selects the scientifically correct earlier responsibility under matched information/resource privilege when recency, eligibility, and actual causality are deliberately put in conflict.

No Utility request was created. The current object is terminal and the Analyst has explicitly prohibited same-object cycle-2 rescue. A literature-driven trace implementation or new discriminator would be an outcome-responsive successor unless independently admitted as a fresh object.

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
  - Keep H7 on HOLD until a fresh native object has a discriminator that separates eligibility persistence from selective causal responsibility?
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
