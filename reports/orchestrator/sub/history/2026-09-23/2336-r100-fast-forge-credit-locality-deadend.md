# FAST FORGE history — v0.5 reward/credit locality dead end

- schema_version: `2`
- generation_id: `FORGE-20260923T233625+0900-V05-CREDIT-LOCALITY-R100`
- produced_at: `2026-09-23T23:36:25+09:00`
- worker_role: `FAST_FORGE`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- overall_status: `FORGE_DEAD_END`
- selection_outcome: `BOUNDED_PROTOTYPES_COMPLETED`

## Freshness / ownership

Stable scientific `main` was re-fetched at `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. Evidence Analyst R100 (`EVA-20260923T225720+0900-R100-C6A2F18D@a32494246245a559ad4e1f8543a1f252b03ef2e7`) is current. It conditionally assigns Candidate #35's one fixed five-arm result-bearing Architecture batch to MAIN after exact R100 repin/preflight/preserve-before-read and keeps H7 at the protected-sidecar capability gate. Direct Candidate #35 branch re-fetch still shows implementation head `5bc64fbd8fd2f3e8d804d18e0a0ad0d58b5a3e4c`, so Forge did not enter Candidate #35 response, reachable-state/off-manifold successor work, or H7.

Methodology R92 (`METHCAL-20260923T232021+0900-R92-5C91E7A4@8b92f841227988c1ac7c4faea7d8d95d2517ad55`) tightens the same boundaries and explicitly keeps independent mechanism discovery open while forbidding manufactured immediate same-family rescue. Literature R39 is Candidate #35 intervention-realism/reachable-state guidance and was excluded. Independent Audit R9 classifies Candidate #34's preserved route response as ordinary local impulse physics and provides no rescue basis. Utility is clean IDLE at `UTILITY-20260923T232600+0900-IDLE-ACK-RECONCILE-R100-6C2A91F4@c231c2652f1c824a276649a7b9b6d752c2b729ae`.

Current Forge history/state was re-read first. Prior Forge work covers receptor traces/suppression, Assembly realization/completion/order/capacity/coactivation, action-context blindness, concept closure, and homeostasis windowing, but not v0.5 field-plasticity reward/eligibility locality. This run therefore selected one independent stable-main credit-assignment surface.

## Forge object

- forge_id: `FORGE-V05-CREDIT-LOCALITY-01`
- question: Does the optional v0.5 reward-modulated field-plasticity track provide native local responsibility/delayed credit to the synapses active in the episode whose outcome is learned, or is it ordinary global reward-modulated STDP/eligibility gating?
- why_now: Native local responsibility/credit is theory-central, independently reachable on stable main, absent from prior Forge history, and does not depend on Candidate #35/H7 outcomes.
- branch: `null` (read-only exact-source/synthetic diagnostics only)

### Prototype A — outcome-after-episode delayed-credit ordering

Exact stable-main source shows `IntegratedV05Brain.process_episode()` calls `plasticity.apply(...)` before action/outcome learning. `learn_outcome()` later calls `plasticity.reward(reward)` only when `enable_reward_modulation=true`; that config is `false` by default. `V05PlasticityController.apply()` first decays stored eligibility but skips an edge entirely unless the *current* spike batch contains both pre- and post-synaptic spikes. Therefore a reward arriving after an episode cannot by itself update the stored eligibility from that episode.

Formula-equivalent synthetic diagnostic using one plastic edge (`weight=0.5`) and one causal pair at lag 5 ms:
- causal STDP increment: `exp(-5/18) = 0.7574651283969664`;
- neutral first apply changes weight to `0.5007574651283969` and stores eligibility `0.7574651283969664`;
- then `reward(-1)` followed by an empty-spike apply decays eligibility to `0.6817186155572699`, leaves weight exactly `0.5007574651283969`, and relaxes reward trace from `-1` to `-0.7`.

Observation: persistent eligibility is not consumed by a reward-only event. Outcome reward affects a later `apply()` only if a later batch again contains a qualifying current pre/post pair.

### Prototype B — global scalar reward versus local responsibility

`reward(value)` stores one scalar `reward_trace`. `apply(field, spikes)` receives no action id, Assembly id, behavioral responsibility id, target synapse, or local reward vector. Every currently qualifying plastic edge multiplies its accumulated eligibility by the same scalar reward trace.

Formula-equivalent two-edge diagnostic with two independent plastic edges, identical 5 ms causal timing, initial weight `0.5`, delay `2.0`, and `reward(+2)` before apply:
- both edges store identical eligibility `0.7574651283969664`;
- both weights become exactly `0.501514930256794`;
- both delays become exactly `2.012` ms.

No representation of which edge caused a later action/outcome exists in this update path, so coincident qualifying edges with the same timing receive the same reward modulation.

## Ordinary reductions

Strongest reduction: ordinary globally neuromodulated STDP with a per-edge eligibility accumulator. The v0.4 predecessor explicitly describes its closely related rule as a bounded STDP-like engineering rule with optional reward modulation; v0.5 adds eligibility persistence but retains the same global scalar reward semantics.

The apparently delayed component is also ordinary: old eligibility is decayed and added to the next qualifying local STDP event. It does not constitute standalone retrospective credit assignment, and the implementation has no native local responsibility signal. On the default v0.5 configuration, field reward modulation is disabled entirely.

## Disposition

Status: `FORGE_DEAD_END`.

Dead-end reason: `GLOBAL_REWARD_MODULATED_STDP_PLUS_ELIGIBILITY_TRACE_FULLY_EXPLAINS_THE_REACHABLE_BEHAVIOR; NO_NATIVE_LOCAL_RESPONSIBILITY_OR_REWARD_ONLY_RETROSPECTIVE_UPDATE_PATH_EXISTS`.

No Evidence Analyst promotion proposal. No Utility request. No Forge branch was needed because exact-source ordering/function signatures plus bounded formula-equivalent synthetic probes resolved the question without repository code changes.

## MAIN collision / hard floor

MAIN work explicitly avoided:
- Candidate #35 exact scientific source, response producer, fixed five-arm response execution, preserve-before-read runtime/preserver, reachable-state/off-manifold/on-manifold successor surfaces;
- H7 R5 controller/sidecar remediation, FORMAL identity/STARTED/protected evaluation/scorer/preserver;
- terminal Candidate #34 and same-family rescue;
- all consumed/frozen/evidence/formal/sealed/freeze/preserve identities.

Hard-floor action occurred: **no**. No PRE_FORMAL/FORMAL identity, STARTED, official TEST/scoring, protected/held-out target, consumed identity rerun/retune/rescore, scientific preserve/evidence mutation, result-bearing workflow dispatch, scientific branch mutation, or research merge occurred.

## Exact refs

- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- Evidence Analyst R100 state commit: `a32494246245a559ad4e1f8543a1f252b03ef2e7`
- Candidate #35 implementation head: `5bc64fbd8fd2f3e8d804d18e0a0ad0d58b5a3e4c`
- Methodology R92: `8b92f841227988c1ac7c4faea7d8d95d2517ad55`
- Literature/Audit branch head: `e8e527e1ed399bb26f926237931618d9b93056e0`
- Literature R39 latest blob: `9a1e0138ed31f9626c1c269bf2e4a42dba65c56a`
- Audit R9 latest blob: `e0c838636dfb36708df8d86dd9165a2a0acedada`
- Utility R100 idle commit: `c231c2652f1c824a276649a7b9b6d752c2b729ae`
- v0.5 plasticity source/blob: `src/sparkbrain/v05/plasticity.py@bb04eaac527aaa6343018ffb49347d087c6a29e5`
- v0.5 brain source/blob: `src/sparkbrain/v05/brain.py@652552f8dc6a53a68e441f593e9bfd82cebb9f7c`
- v0.4 ordinary-baseline plasticity/blob: `src/sparkbrain/v04/plasticity.py@25b965107b903d7634674e24a44afe561aeee518`

## Metrics

Cumulative FAST FORGE metrics after this run:
- runs: `12`
- prototypes attempted: `16`
- dead ends: `12`
- interesting observations retained: `0`
- promotion proposals: `0`
- later admissions: `0`
- duplicate/rescue rejects: `9`
- ownership collisions: `0`
- ordinary-reduction rejects: `12`
- idea-to-observation latency: `SAME_RUN`
