# Fast Forge — durable reconciliation inbox focused green

forge_id: FORGE-FLY0-DURABLE-RECONCILIATION-INBOX
status: FORGE_INTERESTING
evidentiary_status: NON_EVIDENTIARY
canonical_status: NONCANONICAL
scientific_credit: 0
recommended_handoff: NONE_PENDING_FRESH_ANALYST_RECONCILIATION

Source: Theory R31 / ID-SB-FLY-DURABLE-RECONCILIATION-INBOX-001.
Branch: forge/20261001-fly0-durable-reconciliation-inbox-a.
Exact green head: 1d2c5edc7db894827108ab3a3ae325dac2da41b4.
Source commit/blob: 8c571c405127b5adb89a481e7500dfafc51acaeb / 185173c404f5d62a4d845a34434ca48989fefc54.
Focused test blob: 0056e912a2a58ae2b5814259aca09041685d8a47.
CI: 36839614462, Python 3.11 and 3.13 fully green through Lint, Local readiness, Test and Validate bundle.

The bounded comparator stores full issue/source and execution provenance in the same SQLite/WAL file as the R30 local WORLD/effect row, reconstructs after process loss, and atomically commits receipt dedup plus a scalar durable frontier.

Focused green coverage:
- true subprocess cold restart for structured / rewired / random-sparse with no phase-A Python objects reused;
- exact replay after a second reopen is a no-op;
- failure after inbox insert or after frontier update rolls back both;
- missing execution, source tamper, missing WORLD effect and cross-wired receipt fail closed;
- unresolved outcome gaps cannot advance the frontier;
- WORLD/frontier lineage divergence fails closed;
- exact duplicate across independently opened store instances does not advance twice.

Ordinary reduction: SQLite/WAL ACID + durable provenance/event state + idempotent inbox + scalar watermark. Scientific novelty is zero.

Remaining boundaries: bounded retention/outside-horizon is not implemented in this narrowed comparator; duplicate handling is not yet tested under a true simultaneous race; stale/future cut/epoch cases are represented only by fail-closed WORLD/frontier divergence; R27 in-memory projection rebuild is not composed here; local ACID does not prove remote or physical exactly-once effects.

Collision check: Control R150, Analyst R177, MAIN M1 PR #164 untouched, SB003 inactive. Analyst R177 predates this result, so there is no SYSTEM_BUILD handoff.

P0 remains OPEN/root cause UNKNOWN. Source publication saw two fresh pre-GitHub refusals before success on attempt 3. Focused-test create succeeded on attempt 1. Lint-only repair saw one pre-GitHub refusal before success on attempt 2. The initial focused head failed only on F401 unused import; the semantic-preserving repair produced exact-head green CI.

No canonical science, consumed FORMAL identity, immutable evidence, MAIN/Relay ownership or scheduler state was changed.
