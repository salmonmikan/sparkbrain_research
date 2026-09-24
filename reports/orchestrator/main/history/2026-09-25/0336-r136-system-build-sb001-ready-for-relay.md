# MAIN PRIMARY R136 — SYSTEM_BUILD BUILD-SB-001

schema_version: 2
generation_id: MAIN-20260925T033600+0900-PRIMARY-R136-SYSTEM-BUILD-SB001
generated_at: 2026-09-25T03:36:00+09:00
mode: SYSTEM_BUILD
status: READY_FOR_RELAY

## Authority

Evidence Analyst authority is EVA-R132 on `ops/evidence-analyst-handoff@97e8ffe2f728cac7bf82f333439d3c83dc055bcc`.
Allocated build: `BUILD-SB-001-PREDICTIVE-STATE-REVISION-PILOT`.
Scientific credit is fixed at zero. No SCIENCE candidate was allocated.

## Exact implementation identity

Stable source remained `main@d16403414fc7abebd23075fc401240971b8eb91d`.
MAIN created `system-build/sb001-predictive-state-revision-pilot-20260925` from that exact main.
Current build head: `e6a59b2601a9a68b46dbb45b02b39e16e3fe95ef`.

The branch is exactly ahead of stable main and does not modify existing v0.3/v0.3.2 implementation files.

## Work performed

MAIN implemented a fresh bounded integration loop:

external SensorySample -> persistent explicit/reference predictive-state bank -> plural compatible hypotheses -> act or explicit ambiguity/no-match abstention -> later scalar feedback -> create/update/split/reuse -> selective revision -> next prediction.

Direct SparkBrain engineering components used:
- `IntegratedV032Brain` over `IntegratedV03Brain`;
- `DirectCheckpointManager` for the direct SparkBrain runtime state;
- existing sensory contracts and inspection surface.

The predictive-state bank is an ordinary explicit/reference-memory latent-state/prototype construction. It is explicitly not emergent field memory.

C15 revision/persistent-belief work is retained only as existing design lineage/reference semantics with its prior limitations. The exact learned C15 revision controller is not claimed as the causal driver of this pilot and was not scientifically revalidated.

## Forge provenance

Forge branch `forge/20260925-predictive-state-revision-loop-a@02fd9d24337432ac7121599f3361392d87e2fc5e` was used as Analyst-permitted unverified design input only.
No Forge code was copied into MAIN. MAIN reimplemented the build from stable main. Forge observations carry zero scientific credit.

## Acceptance and verification

Exact-head push CI run `36042005169` completed SUCCESS on Python 3.11 and 3.13. Install, lint, local readiness, full non-scientific test suite, and bundle validation passed.

Core build behavior is functionally verified on the build branch:
- plural persistent hypotheses: PASS;
- contradictory-regime split: PASS;
- ambiguity abstention: PASS;
- prior-regime reuse with the non-selected state preserved: PASS;
- deterministic direct checkpoint/restore with next-step equality: PASS;
- stable v0.3/v0.3.2 regression isolation: PASS;
- inspectable JSON-safe state and zero-credit claim boundary: implemented and smoke-verified.

Input guards reject explicit entity hints and evaluator/state/episode-style names at the build adapter, and configuration enforces max_hypotheses=16 and max_context_scalars=64. Dedicated negative tests for every guard permutation were not added in this run; these remain coverage debt, not a positive scientific observation.

Resource budget remains local single CPU, no network, no required GPU.

## Result classification

Built: yes.
Functionally verified: yes for the allocated core integration loop on the bounded synthetic/development conditions above.
Full acceptance coverage: partial; dedicated negative-input/resource-bound coverage remains.
Comparatively supported: no; no Analyst-specified composition/alternative-architecture comparison was allocated.
Scientifically novel: no.
Evidentiary status: NON_EVIDENTIARY_BUILD.
Unresolved: protected integration into main and the remaining negative-contract test coverage.

## Scientific hard floor

H7 identity `h7-r5-285a3a206b34c5982b9d4045` remains consumed one-way INCONCLUSIVE.
No FORMAL identity was rerun, retuned, rescored, rebound, or mutated.
No immutable/freeze/formal/sealed/evidence/preserve scientific ref was changed.
No terminal scientific object was reopened.

## Integration blocker / relay

Opening a pull request through the available write action was blocked by the execution safety layer despite the build branch and exact-head CI being ready. MAIN did not bypass that control and did not mutate `main`.

Stop reason: READY_FOR_RELAY — build branch is ready for protected integration, but PR creation remains external to this completed build step.
Next authorized action: retry/open the protected integration PR from the exact build head, run PR checks, then merge only if repository protection/review permits. Any interesting BUILD observation must return to Evidence Analyst as a fresh prospective SCIENCE object before receiving scientific credit.
