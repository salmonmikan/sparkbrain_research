# Frozen execution contract

Diagnostic ID: `exploratory-m1-outcome-identity-20261001T1458Z`

Status: EXPLORATORY / NONCANONICAL / NON_EVIDENTIARY. Scientific credit: 0.
This is a task-local diagnostic, not an Analyst build allocation or scientific identity.

The reviewed protocol is retained byte-for-byte in PROTOCOL_REVIEWED.md, SHA-256
af5738a963eb441c71802b306c8f85e296d517225fda0800d85845181e0d9752.
Runtime source is a local git archive of main 3cb955cd42474b36d2d37617e5390d08656c06f1.
No source, thresholds, defaults, production tests, working branch, scheduler, canonical
authority, scientific result, or remote repository will be modified by this diagnostic.

## Prospectively fixed execution

Execute exactly the eight cases in matrix.json. Fresh default IntegratedM1Pilot per case.
Bootstrap 0.0 / +0.8, then 0.45 / -0.8 at times 0 and 1. At time 2, probe each
of 0.0 and 0.45 in the original, exact-reversal, near-alias-reversal and null arms.
Routing-only offset is exactly 0.000001; sensory signal stays at exact target.
All receipt magnitudes are 0.8. Use unique event/receipt IDs within and across cases.
Re-deliver the probe receipt once, then attempt one fresh time-3 observation at the
exact target sensory/routing vector, with no fourth fresh outcome.

Budget per primary process: 32 observation attempts and 32 outcome-delivery attempts.
Each case therefore has four observation IDs, three receipt IDs and four deliveries.
The fourth outcome delivery is duplicate committed delivery or retry of an uncommitted
receipt according to the first delivery result. It is never relabeled new evidence.

One second fresh process uses PYTHONHASHSEED=37 instead of 1 with the same frozen
logical case/event/receipt identities and source. It is solely a reproducibility check,
not independent evidence, and not repetition of any formal or consumed identity.
No further matrix, outcome-responsive repair, threshold/offset change or rescue is allowed.

## Recording and comparisons

Before and after every call retain inspection, inspection state hash, and all three
supported canonical checkpoint JSON payloads from PilotCheckpointManager.save and
ScopeRevisionCheckpointManager.save, including reference-brain.json. Record action,
revision, exact exception type/message/traceback, call input and sequencing.
Use no-clobber output paths. At every capture save twice into separate new directories,
read back every JSON payload and compare every field, and verify inspection/state hash
remain unchanged. Do not discard metadata or hidden serializer fields for rollback claims.
Compare full serialized components and all compositor inspection fields before/after
rejection. Record sequence deltas to distinguish new commit from idempotent old revision.

Driver unit tests cover successful calls, failure preservation and serialization mismatch
using fakes only before the freeze. No SparkBrain observation/outcome is executed by them.

Stop immediately if an exact reversal commits, any rejected call mutates complete
serialized state, or repeated serialization is not state-neutral. Preserve partial outputs.
Unexpected near-alias routing/failure is retained and reported without adjusting input.

## Interpretation limits

SB002 identical-observation candidate consistency is an intentional documented contract.
Confirming it is not discovering a bug. A near-alias commit does not mean successful
adaptation: record scope support tie and the fourth prediction/action reason.

The Session.cycle whole-cycle rollback distinction is SOURCE-BACKED ONLY. This driver
does not execute Session.cycle or a modified world. Direct-pilot pending rejection must
not be presented as demonstrated session deadlock or system-wide liveness failure.

No whole-repository test suite, benchmark, formal run or PR #164 acceptance run is part
of this fixed diagnostic. Validation covers this driver and its records. Existing runtime
source is unmodified, and broader project acceptance is neither repeated nor claimed.

## Fresh collision preflight

AGENTS and current scheduler policy were fetched from main before the active index.
Authoritative index: ops/human-directives, head 8ce979b9ec0bc7eede5225c0403698f8886d3e8d,
blob 1ba1e173344f36e14d0e21e6f3e823254e031f7d. No delta from reviewed source protocol.
HUMAN-20260928-001 permits non-colliding causal integration diagnostics with zero credit.
Analyst durable authority remains R177. Control R153 and MAIN R222 retain PR #164 ownership
and HOLD MERGE; R178 request is not durable authority. This task changes none of them.
The task is an explicit independent user-approved cloud diagnostic, not a scheduled MAIN,
Control, Analyst, Forge or Utility invocation and claims none of those roles' write authority.

Artifacts remain local to the dot cloud workspace. No remote publication is authorized here.
