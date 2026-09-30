# Fast Forge — R27 causal frontier focused acceptance publication blocked

- forge_id: `FORGE-FLY0-CAUSAL-FRONTIER-R27-FOCUSED-ACCEPTANCE`
- status: `FORGE_PROTOTYPE`
- evidentiary_status: `NON_EVIDENTIARY / NONCANONICAL`
- source_branch: `forge/20260930-fly0-causal-frontier-a`
- source_head: `2ccb4df11241b8547b69c06c6d8731f245625c27`
- source_path: `forge_prototypes/fly0_causal_frontier.py`
- source_blob: `a60e1de4b4781237c2a7f9dda7b2bcc8e8a10f9e`
- focused_test_path: `tests/test_forge_fly0_causal_frontier.py`
- focused_test_persisted: false
- recommended_handoff: `NONE_UNTIL_FOCUSED_ACCEPTANCE`
- scientific_credit: 0

## Why now

Milestone 1 remains active but PRIMARY MAIN R210 owns M1-002 and SB003 remains
`ALLOCATED_CONDITIONAL_INACTIVE`. This Forge probe does not collide with MAIN.
Theory R27 proposes a session-scoped durable causal frontier above replaceable
bounded-horizon reconciliation; Theory R28 separately fixes issue-time lineage.
Control R138 classifies the causal-frontier source as source-only,
`FORGE_PROTOTYPE_UNVERIFIED_NO_HANDOFF`.

## Fresh authority

- Human Directive index head:
  `8ce979b9ec0bc7eede5225c0403698f8886d3e8d`
- active-index blob:
  `1ba1e173344f36e14d0e21e6f3e823254e031f7d`
- directive delta: none
- Control: R138
- Evidence Analyst: R174
- PRIMARY MAIN: R210
- Relay: unallocated
- Methodology: R153 / WELL_CALIBRATED
- Theory moving pointer: R27
- Theory append-only newest relevant generation: R28
- Literature append-only: R53
- Independent Audit: R14
- M1-002 exact head:
  `2a21d3e879f1db4e81a58273180ad2124e823a5e`
- SB003: `ALLOCATED_CONDITIONAL_INACTIVE`

## Focused acceptance attempted

A new focused test file was prepared to cover:

1. structured / rewired / random-sparse inner-reconciler recreation cannot reset
   the durable outcome watermark;
2. atomic WORLD rebase advances outer cut/recovery epoch and retires older R28
   issue lineage;
3. same-session anchor coverage below the durable watermark is rejected without
   frontier mutation;
4. checkpoint restore rejects an inner reconciler behind the durable frontier
   and rejects a tampered frontier token;
5. repeated rebases keep the outer frontier checkpoint fixed-shape / bounded.

This would test the central R27 claim that replaceable inner horizon/dedupe state
cannot become the authority for global session causal time.

## Publication result

The focused-test create purpose exhausted the repository mutation ceiling:
5 total attempts, each preceded by fresh branch-head and target-path readback.
All five attempts were refused before GitHub mutation execution with:

`This tool call was blocked by OpenAI's safety checks. Please double check what you are sending.`

Final preflight state remained:

- branch head:
  `2ccb4df11241b8547b69c06c6d8731f245625c27`
- focused test path: absent
- source unchanged
- new focused CI evidence: none

Independent current-head checks found no combined commit statuses and no
PR-triggered workflow runs for the source-only head. Therefore no CI-green claim
is made for this causal-frontier generation.

## Disposition

`FORGE_PROTOTYPE / SOURCE_ONLY / FOCUSED_ACCEPTANCE_NOT_PERSISTED /
UNVERIFIED / NON_EVIDENTIARY / NONCANONICAL`.

No SYSTEM_BUILD handoff. R28's separately tested issue-time provenance head is
not downgraded by this result. The causal-frontier source remains ordinary
systems engineering reducible to monotonic state-machine/WAL/fencing patterns;
engineering usefulness, if later verified, would not establish biological
fidelity, fly-topology superiority, efficiency, composition contribution,
whole-system superiority, external validity, or scientific novelty.

P0 `INC-GITHUB-MUTATION-RECURRENCE-20260928-001` remains OPEN / root cause
UNKNOWN. This run adds another focused-test contents-write refusal observation;
it does not establish a repository-wide GitHub outage.

No consumed FORMAL identity, immutable evidence, M1-002, SB003 activation,
MAIN/Relay ownership, canonical science, scheduler state, or Work-backed path
was changed.
