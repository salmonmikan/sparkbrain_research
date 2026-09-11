# RV02 RD004 hidden-return gate reachability audit

Date: 2026-09-11  
Status: **POST-HOC OFFLINE AUDIT OF PRESERVED DEVELOPMENT EVIDENCE / NO RERUN / NO RESCORING**

## Evidence identity

This audit reads only the already-consumed RD004 attempt-001 artifact. It does not execute a Field, alter RD004 source, rerun a cell, change a threshold, or rescore the registered behavioral endpoint.

- Protocol: `rv02-rd004-relative-probe-clock-v1`
- Frozen source: `freeze/rv02-rd004-development-source`
- Exact source SHA: `75268dd804f0ef113869be172adf575ac22523a0`
- GitHub Actions run: `34592080367`
- Artifact id: `10196093854`
- Artifact digest: `sha256:1b583bd25587944f96b98d580c99d4215547859df28730e64e454072122a57f0`
- Preserved compressed raw cells SHA-256: `2c553868031848d7d24a9e39ce0f508de99e2b8ea5dfcf3fffe70d7b6215588c`

The existing attempt report remains authoritative for the registered RD004 behavioral interpretation: 15 cells were complete, three `opposing-reversal` cells were incomplete under the native training guard, and no complete cell satisfied the preregistered selective-organization conjunction.

## Audit question

The attempt report also records that several complete cells contained matched E1/ES hidden eligibility activity while the retained causal hidden-return update lists were empty. This audit asks a narrower engineering question:

> In the already-preserved complete-cell trace stream, did any causal hidden eligibility trace ever have a later external teaching observation that could legally commit a `hidden_return_potentiation` update under the frozen adapter contract?

The frozen adapter requires all of the following at one later external observation:

1. the retained trace has not expired;
2. lag is in the inherited `[0.5, 6.5] ms` window;
3. the trace's assigned hidden source is an incoming source to the current visible external target;
4. that existing hidden-to-visible edge is plastic and has non-negative weight.

A same-timestamp external observation has lag `0 ms` and is therefore not an admissible hidden-return gate.

## Preserved complete-cell accounting

Across the 15 complete RD004 cells, six cells contained causal hidden eligibility activity. The audit reconstructed each retained E1 trace against the exact retained external training schedule and initial connection inventory.

| family | scale | E1 traces | created during training | created in final tail | no later external observation within 6.5 ms | later external within 6.5 ms but no eligible assigned-source -> target edge | admissible hidden-return gates | retained hidden-return updates |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| shared-cue | 1 | 4 | 4 | 0 | 4 | 0 | 0 | 0 |
| dense-load | 1 | 28 | 28 | 0 | 28 | 0 | 0 | 0 |
| dense-load | 3 | 16 | 16 | 0 | 16 | 0 | 0 | 0 |
| capacity-pressure | 1 | 28 | 26 | 2 | 22 | 4 | 0 | 0 |
| capacity-pressure | 3 | 20 | 20 | 0 | 20 | 0 | 0 | 0 |
| capacity-pressure | 10 | 8 | 7 | 1 | 7 | 0 | 0 | 0 |
| **total** |  | **104** | **101** | **3** | **97** | **4** | **0** | **0** |

The three final-tail traces occur after the last external training observation, so by construction there is no later external teaching gate before washout. Together with the 101 training-time traces, **none of the 104 retained causal traces in scientifically complete cells had an admissible hidden-return commit opportunity**.

The dominant pattern is temporal: 97 training traces have no later external observation inside the 6.5-ms eligibility lifetime. Four additional traces in `capacity-pressure`, scale 1 do have a later external observation inside the time window, but the assigned hidden source is not an eligible incoming plastic non-negative edge to that later visible target. Thus the frozen commit rule correctly produces zero hidden-return updates in all complete cells.

## Incomplete-cell sanity observation

This audit does not convert incomplete cells into scientific scores. For engineering context only, the consumed `opposing-reversal`, scale 1 partial trace contains one retained `hidden_return_potentiation` update before the native training guard terminated the cell. This shows that the adapter path is not globally incapable of emitting such an update; however, because the cell is incomplete, that observation cannot support the registered RD004 behavioral claim.

## Interpretation

RD004's complete-cell negative result should be narrowed one step further:

- it **does** show that the frozen online training schedule produced hidden runtime eligibility in several complete cells;
- it **does not** provide a complete-cell test of causal-versus-shuffled hidden assignment at the physical update stage, because the frozen external-gated commit opportunity was never reached in those cells;
- consequently, E1/ES behavioral equivalence in the complete cells is expected under the actual retained update ledger and should not be over-interpreted as evidence that causal assignment and shuffled assignment are behaviorally equivalent after successful hidden-return learning.

This does not rescue RD004. Its preregistered conjunction remains unsatisfied, and the attempt remains a negative development diagnosis. The audit only localizes why the physical hidden-return branch was silent in the complete evidence.

## Prospective next-stage constraint

Any future RV02 diagnostic that asks whether causal hidden assignment matters must be a **new protocol identity** fixed before execution. It must prospectively guarantee or explicitly measure gate reachability without using reward, route correctness, future outcome, or post-hoc favorable-case selection. In particular, it must not alter or rerun RD004, increase native guards to rescue `opposing-reversal`, or tune the inherited eligibility window after seeing this result.

A clean next question is whether an outcome-blind, externally generated return event can be scheduled so that both causal E1 and matched shuffled ES consume an identical, preregistered set of *gate-reachable* eligibility events, while the only E1/ES difference remains the hidden source assignment. That question requires a fresh RD005 preregistration before implementation or execution.
