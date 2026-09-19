# MAIN RELAY — Refractory current accounting Architecture cycle 1 terminal

Timestamp: `2026-09-20 07:44 JST`  
Worker role: `main`  
Execution mode: `RELAY`  
Fresh Evidence Analyst continuation authority: `7e7d425948a86d0eec306b1a75bfc07165d9afa1`  
Prospective contract authority embedded in the unchanged contract/artifact: `eb1c305017d32c8c3efb0794e547b889e5a80461`  
Research layer: `ARCHITECTURE_STUDY`  
Candidate: `CAND-REFRACTORY-CURRENT-ACCOUNTING-01`

## Lease / collision reconciliation

Inherited MAIN lease was `WAITING_EXTERNAL` from the prior RELAY checkpoint with heartbeat `2026-09-20T07:17:00+09:00`; it was not a fresh PRIMARY `RUNNING` collision. Fresh Evidence Analyst tip remained `7e7d425948a86d0eec306b1a75bfc07165d9afa1`. Stable `main` remained `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`, and the active research branch remained exactly `research/main-refractory-current-accounting-arch-study-20260920@4589192d927e40cf7a05cf8a94207efb42ebbc65`. SUB remained on its independent delayed-outcome Discovery object and did not collide with this MAIN object.

RELAY acquired lease `sparkbrain-main-relay-20260920T0742JST` before durable MAIN persistence.

## Exact-head workflow result

- ordinary CI `35472786733`: `completed/success` on exact head `4589192d927e40cf7a05cf8a94207efb42ebbc65`.
- Refractory Architecture workflow `35472786687`: `completed/success` on the same exact head.
- Both exact-head CI jobs passed `Verify prospective binding only`.
- The outcome-bearing `architecture-study` job passed preflight, executed exactly one NON_EVIDENTIARY Architecture cycle, and uploaded raw-before-summary artifacts.

Artifact: `10593866036` (`refractory-current-accounting-cycle1-4589192d927e40cf7a05cf8a94207efb42ebbc65`). GitHub archive digest: `sha256:b4dfbf04ab2f1dbb69fcee3833890ce6ad30d85a0c095a4699cde356c43e9115`.

RELAY downloaded the artifact and read `raw.json` before `summary.json`. Local archive SHA-256 matched the GitHub artifact digest. `summary.json.raw_sha256` matched the independently computed `raw.json` SHA-256 `4587b7e0ee1404f3f78f8a0c83c8224fea3d632e8a25162cb0ae586dc4a5712e`. Artifact `git_head`, workflow id, source bindings, source-blob verification, comparator, observables, input-family digest, and contract digest were internally consistent with the fixed cycle. The prospective contract blob remained `957b8ad5c22e3485dfedf8cf9052a234a63102aa`; no contract or production source mutation occurred after outcome visibility.

## Fixed terminal mapping

The raw artifact reports all required machine/source checks true, supported same-time mixed-sign runtime condition true, outside-refractory controls matching, simple refractory controls valid, and zero treatment spikes in every refractory arm. There is no explicit supported canonical netting contract hit.

For the prospectively fixed `balanced_same_time` refractory arm:

- production `potential_after_treatment = 0.4729797344533827`, shadow `-0.027020265546617295` -> fixed `state_effect = true`;
- production `post_refractory_probe_spike_count = 1`, shadow `0` -> fixed `functional_effect = true`.

The already-fixed precedence therefore maps exactly once to:

**`FUNCTIONAL_REFRACTORY_ACCOUNTING_EFFECT`**

This is a valid **NON_EVIDENTIARY Architecture/API semantics result**: under the fixed synthetic DEV probe, production's same-time signed-current netting before refractory clamp changes retained state and the single fixed post-refractory spike observable relative to the prospectively bound positive-ignore shadow. It is not FORMAL or PRE_FORMAL evidence and does not establish biological novelty or broader prevalence.

## Integrity / stop

No formal identity, STARTED/control authority, official TEST, formal preserve/scorer/evidence, consumed-identity retry, immutable evidence mutation, production-source mutation, post-outcome repair, result-dependent retuning, cycle 2, PRE_FORMAL promotion, FORMAL continuation, or SUB/Utility mutation occurred.

Fresh Analyst contingency for `FUNCTIONAL_REFRACTORY_ACCOUNTING_EFFECT` is `STOP_FRESH_ARCHITECTURE_REVIEW_NO_AUTO_PRE_FORMAL`. The current MAIN cycle is therefore terminal and stops here for fresh Evidence Analyst review.

Stop reason: **`VALID_FUNCTIONAL_REFRACTORY_ACCOUNTING_EFFECT_STOP_FOR_FRESH_ANALYST_REVIEW`**.  
Final lease: **`COMPLETED`**.  
Next MAIN action: fresh Evidence Analyst review only. Do not automatically start cycle 2, implementation repair, PRE_FORMAL, FORMAL, or the queued delayed-outcome Architecture object without new prospective authority.
