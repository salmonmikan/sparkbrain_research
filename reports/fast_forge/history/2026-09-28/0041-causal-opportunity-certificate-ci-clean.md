# Fast Forge history — causal-opportunity certificate

- generation_id: `FORGE-20260928T004156+0900-CAUSAL-OPPORTUNITY-CERTIFICATE-CI-CLEAN`
- produced_at: `2026-09-28T00:41:56+09:00`
- role: `FAST_FORGE`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- new_scientific_result: false

## 今回試したこと

Independent Audit R10 identified a general failure mode in intervention tests: the treated population can be distinct from the directly cued population that produces the declared readout, leaving a null result without demonstrated treatment-to-observable opportunity.

This isolated Forge prototype accepts only caller-supplied events, direct influence edges, intervention targets and declared readouts. It checks event IDs, requires influence edges to move forward in `(time, sequence)` order, identifies post-intervention state-bearing events on treated actors, and returns a deterministic shortest path only when those events can reach a declared readout.

The work is generic synthetic tooling. It does not read preserved Candidate #35 output, execute any candidate, modify any result or propose a successor.

## 結果

- A treated hidden event connected through a relay to a visible return produced a three-event witness certificate.
- A complete direct-cue path containing only untreated receptor events returned `NO_TREATED_ACTIVITY` and did not count as opportunity.
- Treated activity disconnected from readout returned `NO_PATH_TO_READOUT`.
- An incomplete trace returned `INCOMPLETE_TRACE` rather than a negative certificate.
- Unknown edge endpoints and backward event edges returned `INVALID_TRACE`.
- Same-time events can form a valid path only through an increasing deterministic sequence number.
- Pre-intervention activity and non-state-bearing target logs cannot seed a certificate.
- Witness selection remained deterministic under event/edge input reordering.
- Focused tests: 10/10 PASS.
- Full local selected suite: 587/587 PASS; 392 scientific/reproduction/external tests remained excluded by the repository's default marker contract.
- Ruff, compileall, local readiness and bundle validation: PASS.
- Exact prototype head: `c8280a8aaebc29881c07369680777633aa5f7ac7`.
- GitHub CI run `36330332740`: Python 3.11 and 3.13 SUCCESS.

## 単純な説明で足りるか

Yes. The behavior is ordinary directed-graph reachability with temporal-order validation and fail-closed input checking. It does not require a new causal-inference, learning, memory or cognitive mechanism.

## 統合部品として使えるか

Potentially, as a precondition diagnostic for future intervention or ablation tooling. It can prevent a missing treatment-to-readout path from being silently interpreted as evidence that the treated state is irrelevant.

Its usefulness is conditional: the caller must justify `trace_complete=True` through an independent trace contract. A certified path still needs an appropriate counterfactual or intervention comparison before any causal effect can be claimed.

## 扱い

`FORGE_INTERESTING`; `recommended_handoff=SYSTEM_BUILD_INPUT`; scientific credit 0. The prototype remains isolated, noncanonical and non-evidentiary. It does not reopen Candidate #35 and is not admitted to SB002, RD006, SB001 or canonical science.

## 注意

- Reachability is only a necessary opportunity check, not causal attribution.
- The analyzer trusts caller-supplied direct influence edges and trace completeness; it does not discover hidden edges.
- It does not detect readout ceiling/saturation or quantify sensitivity.
- It does not prove that the intervention changed any event on a witness path.
- It provides no matched counterfactual, effect size, comparator, resource study or external validation.
- MAIN owns allocated SB002. This prototype implements no online scope router, route-local revision, checkpoint/replay, atomic rollback or scope-token semantics.
- RD005 remains consumed; RD006 v1-v4 remain closed; all terminal, FORMAL, evidence and preserved refs are unchanged.
- No scheduler, Analyst, MAIN, Relay, Control, Theory, Methodology or Utility state was changed.

## Authority and collision readback

- `main@cf0bc45262824f1fe282ccd7b785b3ea50be2099`
- `ops/human-directives@3f8bc8d387ad6c8333c43c90b81a80dc3241f0f7`
- Evidence Analyst `EVA-20260928T000605+0900-R158-RD006-V4-AUDIT-CLOSURE-SB002-ALLOCATION` at `7e1942e8dfe5fa5333d956ab717e041f79206075`
- MAIN `MAIN-20260927T233306+0900-PRIMARY-R163-RD006-V4-RETURN-ALIGNMENT-AUDIT` at `5568912a42644582d9fd763bd05fc94a17ecf233`
- Control `CTRL-20260927T235243+0900-R98-RD006-V4-AUDIT-RECONCILIATION` at `57fe5474dea444fe21cd4e1be9b4c81be8cd582a`
- Methodology `METHCAL-20260928T002022+0900-R135-SB002-ALLOCATION-CALIBRATION` at `70ec61002581d55ebb29b01fc5f240b7aca4b467`
- Theory `THEORY-20260927T213213+0900-R11-NO-PROPOSAL-ROUTER-RESOLUTION-BOUNDARY-5A8C31D4` at `c4066afb33fdb6a67d53fa1dc9eaabfc78d211a3`
- Utility `UTILITY-20260927T233140+0900-R157-BRIDGE-HANDOFF-RECONCILIATION` at `f196d437c28fa377f925c832c3e1df6ba1fd2ecb`
- SB002 target branch absent at final collision readback; allocation remains MAIN-owned.

新しい科学結果: なし

