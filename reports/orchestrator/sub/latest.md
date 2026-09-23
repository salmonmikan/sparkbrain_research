# FAST FORGE latest — v0.5 reward/credit locality dead end

- schema_version: `2`
- generation_id: `FORGE-20260923T233625+0900-V05-CREDIT-LOCALITY-R100`
- produced_at: `2026-09-23T23:36:25+09:00`
- worker_role: `FAST_FORGE`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- overall_status: `FORGE_DEAD_END`
- selection_outcome: `BOUNDED_PROTOTYPES_COMPLETED`

## Freshness / independence

Stable main remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. Evidence Analyst R100 is current and conditionally assigns Candidate #35's fixed five-arm result-bearing Architecture batch to MAIN; H7 remains held at the protected-sidecar capability gate. Methodology R92 keeps those boundaries and leaves independent mechanism discovery open. Literature R39 is Candidate #35 intervention-realism/reachable-state guidance and was excluded. Audit R9 reduces terminal Candidate #34 to ordinary local edge impulse physics and provides no rescue. Utility R100 is clean IDLE.

Forge selected a separate stable-main v0.5 field-plasticity credit-assignment question not present in prior Forge history.

## Probes

Question: does optional v0.5 reward-modulated field plasticity provide native local responsibility/delayed credit to the episode whose outcome arrives later, or ordinary global reward-modulated STDP/eligibility gating?

Two read-only exact-source/formula-equivalent diagnostics were performed without a Forge branch:

1. `process_episode()` applies plasticity before `learn_outcome()` sets reward. For a causal 5 ms pair, eligibility is `exp(-5/18)=0.7574651283969664`. After the neutral apply, setting reward `-1` and calling an empty-spike apply decays eligibility to `0.6817186155572699` but leaves the weight unchanged at `0.5007574651283969`; reward trace itself relaxes to `-0.7`. Stored eligibility is therefore not consumed by reward alone.
2. `reward(value)` stores one global scalar. Two independent plastic edges with identical 5 ms causal timing under `reward(+2)` receive identical eligibility `0.7574651283969664`, identical weight `0.501514930256794`, and identical delay `2.012`. The update path receives no action/Assembly/responsibility identifier or local reward vector.

Default `V05BrainConfig.enable_reward_modulation` is `false`; the field reward track is opt-in.

## Reduction / disposition

The behavior is fully explained by ordinary globally neuromodulated STDP with a per-edge eligibility accumulator. Old eligibility can amplify the next qualifying local coactivation, but there is no standalone retrospective reward-only update and no native local responsibility signal. The v0.4 predecessor explicitly describes the closely related baseline as a bounded STDP-like engineering rule with optional reward modulation.

Disposition: `FORGE_DEAD_END`. No Evidence Analyst promotion proposal. No Utility request. No code branch or repository science mutation.

MAIN collision check passed. Candidate #35 response/successors, H7, terminal Candidate #34 rescue, and all consumed/protected/evidence/formal/preserve surfaces were avoided. No hard-floor action occurred.

Cumulative metrics: runs `12`, prototypes attempted `16`, dead ends `12`, interesting retained `0`, promotion proposals `0`, later admissions `0`, duplicate/rescue rejects `9`, ownership collisions `0`, ordinary-reduction rejects `12`.
