# SparkBrain Research Orchestrator run report — 2026-09-15 22:59 JST

## Control-plane input and reconciliation

- Evidence Analyst handoff consumed first: `ops/evidence-analyst-handoff@e8f6551a178eed234cbc0e7f7e8f566fafc67df1`.
- The handoff's top recommendation was followed: correct/retire the R01-16 delay-validity issue, then prioritize a fresh prospective RV01 real-delay successor if the exact source was reviewed, green, frozen, collision-free, and raw-before-score safe.
- Current remote superseded part of the handoff's readiness picture before this worker acted: PR #133 had already been exact-head merged into RV01, authoritative RV01 had advanced from `02b3d80744d0eb10cb0d90fc38d3c55729d7ab99` to `f72d840da0b3602971635698b4a15bf8f12585c4`, and a distinct R01-17 successor PR #134 plus source freeze already existed. This run reconciled that concurrent work and did not recreate it.

## Authoritative refs re-fetched

- `main`: `ba16bf10535141c2edb29bbe3439ba0a38e71179`.
- A01 authoritative `research/v061-a01-n3-adapter`: `8044b25f3a7b7767bf1262ea6a99cd6b795e3e8d`.
- RV01 authoritative at start of active work: `f72d840da0b3602971635698b4a15bf8f12585c4`; after exact-head PR #134 merge: `98be60268845487ce51e76b8a7687552a5dbc51f`.
- RV02 authoritative/source-binding `research/rv02-rd005-source-binding-20260913`: `c60b7fd8d3889ee969f505d921e7d31c990871e6`.
- CX01 immutable refs rechecked unchanged: source `e8483968ce43076b4c3fd04c76e62106e2031769`, package `c104be281285d52a732d5366fe36209d5688d973`, STARTED `8216d41a57e6933443d38dfc8d93f9188e423d0c`, preserve `6d45928827209cd763a2879494d85838df38b96f`.

## RV01 R01-16 correction status

PR #133 is no longer open. Its measurement-validity correction and canonical `docs/RESULTS_LEDGER.md` entry are present in RV01 via merge commit `f72d840da0b3602971635698b4a15bf8f12585c4`. Historical frozen labels remain unchanged: Weight `WEIGHT_SUPPORTED`, Delay `DELAY_MIXED`, Combined `COMBINED_SUPPORTED`; the durable interpretation now correctly states that the realized R01-16 delay displacement was roundoff-scale and does not support a substantive learned-delay mechanism.

## RV01 R01-17 prospective readiness audited

Open PR #134 was re-fetched and audited at exact head `5ecb459b609b393ff837f57cc138f1eb44c1b255`, base `research/rv01-endogenous-transition@f72d840da0b3602971635698b4a15bf8f12585c4`.

Prospective fixed contract before any R01-17 output:
- protocol `rv01-r01-17-real-delay-causal-timing-v1`;
- fresh development seeds `141800..141804`;
- initial physical delay deliberately exceeds training lag by `1.5–2.25 ms`;
- minimum learned-delay displacement `0.5 ms`;
- minimum downstream causal first-arrival shift `0.5 ms`;
- timing/tie tolerance `0.05 ms`;
- F0 learned-delay vs FD reset-delay with weights held matched, plus deterministic SHAM;
- complete per-exposure raw learner observations/hashes retained;
- synthetic scorer tests cover support, negative, mixed, ineligible, and exact 0.5 ms boundaries without invoking real acquisition;
- raw preservation precedes scoring;
- exposed-development only, no held-out/formal authority.

Exact-head CI run `34976949639` was green. Latest Codex review on exact head `5ecb459...` reported no major issues. Earlier P1 comments were addressed by the current head; freeze-readiness record explicitly preserves the user-authorized human-review waiver without bypassing real integrity gates.

Source freeze existed before execution and was re-fetched unchanged: `freeze/rv01-r01-17-real-delay-source-20260915@5ecb459b609b393ff837f57cc138f1eb44c1b255`. Immediately before one-way execution there was no R01-17 STARTED/control ref and no raw/scored preserve ref.

## Exact-head merge

PR #134 was re-fetched for head/diff/mergeability/checks immediately before merge and merged only with expected head SHA `5ecb459b609b393ff837f57cc138f1eb44c1b255`.

- PR: #134 `RV01 R01-17: preregister real-delay causal timing development`
- merge result: success
- merge commit / new RV01 authoritative head: `98be60268845487ce51e76b8a7687552a5dbc51f`
- merge method: merge commit

No frozen or preserved evidence was imported or modified by the merge.

## One-way execution under global authorization

After a final freeze/preserve/collision audit, this run atomically created:

- `control/rv01-r01-17-real-delay-started-20260915@5ecb459b609b393ff837f57cc138f1eb44c1b255`

That push legitimately triggered exactly-once workflow run `34978554838`, attempt 1, on the exact frozen source. The workflow completed successfully. All scientific one-way steps succeeded in order:

1. exact STARTED/freeze/no-preserve verification;
2. exact Python 3.11.16/runtime and source manifest binding;
3. raw acquisition exactly once;
4. raw preservation before scoring;
5. preserved raw-byte verification;
6. scoring only the already-preserved raw;
7. scored evidence preservation.

Immutable evidence refs created by the workflow:
- raw preserve `preserve/rv01-r01-17-real-delay-raw-20260915@fceb3663c7a880d82593e6c1efe52fcd1ad0c00a`;
- scored preserve `preserve/rv01-r01-17-real-delay-scored-20260915@d4737d52ecbb2306d9f00f99366f0ad6424327be`.

Execution metadata binds frozen source `5ecb459b609b393ff837f57cc138f1eb44c1b255`, workflow `34978554838`, attempt 1, Python 3.11.16, same-identity rerun false, held-out false, formal false.

## New scientific result

**New scientific information was produced in this run.** Frozen scorer classification:

`SUPPORTED_REAL_DELAY_CAUSAL_TIMING`

All five prospectively fixed development cells were `REAL_DELAY_SUPPORT_CELL`; all were delay-eligible, route-preserved, arm-binding-valid, and SHAM-exact.

Per-cell learned-delay displacement / first downstream timing shift:
- seed 141800: delay displacement ~`1.817788 ms`; unit-1 shift `1.817788 ms`, accumulating to unit-3 `5.453365 ms`;
- seed 141801: ~`2.060727 ms`; unit-1 `2.060727 ms`, unit-3 `6.182181 ms`;
- seed 141802: ~`2.195000 ms`; unit-1 `2.195000 ms`, unit-3 `6.584999 ms`;
- seed 141803: ~`1.780925 ms`; unit-1 `1.780925 ms`, unit-3 `5.342776 ms`;
- seed 141804: ~`1.512860 ms`; unit-1 `1.512860 ms`, unit-3 `4.538581 ms`.

All effects are far above the preregistered `0.5 ms` minimum and `0.05 ms` numerical/tie tolerance. Raw suite SHA-256: `7d6642bf16364c2a67acdf979324d0da59dcd7bbdc508c5f8773b6c654803dc2`; score SHA-256: `b76f3c7b3ec29f97ea69de30c6fb0e3c171c1eaa0e80699bf8055c3586ded76e`.

Scientific interpretation is intentionally narrow: on the fixed exposed-development chain, the ordinary physical learner can create a nontrivial learned-delay state, and resetting that learned delay while holding learned weights matched causally delays downstream first-arrival timing while preserving the route. This resolves the specific R01-16 measurement-validity ambiguity for capability, but does not establish generality, interference retention, weight×delay interaction, held-out confirmation, biological fidelity, or a formal SparkBrain claim.

R01-17 is now consumed and must never be rerun or retuned.

## Other active lines

### A01 MD-002
P2 candidate-002 remains consumed with development result `SUPPORTED_SELECTIVE_CIRCULATION`; no rerun. Old-confirmatory P4 remains invalid absent a complete pre-P2 executable contract; any new P4 is distinct exploratory/development work.

### RV02 RD005
D1 identity `96634541dc29b00be9f19b5819d45f541af69348ab6c1b0da6b48e943221700a` remains consumed terminal `D1_ZERO_READY_STOP`; blind result remains unopened. No rerun or repair.

### CX/CX01
Candidate-002 remains immutable formal NEGATIVE and consumed. Source/package/control/preserve refs remained unchanged; no rerun or retune.

## Repository hygiene / concurrency / main

- Concurrent work was reconciled rather than overwritten: PR #133 and R01-17 branch/freeze creation had already occurred before this worker acted.
- Open PRs after PR #134 merge: **0**.
- Obsolete PRs newly closed as obsolete: **0**; #133 and #134 are merged, not archived/abandoned.
- Branch deletion: **0**.
- `main` integration: **0**. No current change on this run required main integration to obtain the scientific result.
- Historical/freeze/preserve/control refs remain evidence-bearing and are not cleanup candidates.
- Review/research branches for already merged #133/#134 may be classified for manual cleanup only after confirming they are not referenced by any process; no deletion performed.

## Human-review override

`USER_AUTHORIZED_REVIEW_GATE_OVERRIDE / HUMAN_REVIEW_WAIVED_BY_USER` was already recorded prospectively in the R01-17 freeze-readiness review and applied only to the literal independent-human-only gate. Exact-source review, CI, freeze, no-collision, STARTED, and raw-before-score gates were all independently satisfied.

## Consumed identities / no-rerun additions

Existing consumed identities remain no-rerun/no-retune: A01 MD-001, A01 MD-002 P2 candidate-002, RV01 R01-16 construction/capability, RV02 RD005 D1, CX01 candidate-002, and other immutable consumed identities represented by retained control/preserve refs.

Newly consumed in this run:
- RV01 R01-17 `rv01-r01-17-real-delay-causal-timing-v1` at frozen source `5ecb459b609b393ff837f57cc138f1eb44c1b255`, STARTED `control/rv01-r01-17-real-delay-started-20260915`, workflow `34978554838`, raw preserve `fceb3663c7a880d82593e6c1efe52fcd1ad0c00a`, scored preserve `d4737d52ecbb2306d9f00f99366f0ad6424327be`.

## Blockers and next-ready frontier

No integrity blocker remains for the already-completed R01-17 identity; it is consumed and immutable.

Highest-information next scientific move should be chosen by the Evidence Analyst using this new result. The natural RV01 successor question is now whether a real, demonstrated learned-delay signal changes route competition/interference independently of or jointly with learned weight on a **new** prospective identity. Do not automatically execute such a successor before prospective contract/scoring is fixed. A01 P4 and RV02 blind-preserving successor remain valid alternative frontiers.

## Run result

This run produced a new positive exposed-development measurement, exact-head merged the reviewed R01-17 prospective tooling into the active RV01 research line, consumed exactly one new one-way identity under global authorization, and preserved both raw and scored evidence immutably. No formal or held-out claim was made.
