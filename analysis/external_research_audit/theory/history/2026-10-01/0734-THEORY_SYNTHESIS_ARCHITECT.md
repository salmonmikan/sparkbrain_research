# Theory R30 — local atomic WORLD effect journal

schema_version: `2`
generation_id: `THEORY-20261001T073425+0900-R30-LOCAL-ATOMIC-WORLD-EFFECT-JOURNAL`
produced_at: `2026-10-01T07:34:25+09:00`
producer_run_id: `EXTERNAL_SCIENCE_TRIROLE-20261001T073425+0900`
authority_scope: `NON_EVIDENTIARY_NONCANONICAL_THEORY_SYNTHESIS_ZERO_EXECUTION_AUTHORITY`
supersedes_generation_id: `THEORY-20260930T193342+0900-R29-WORLD-COMMIT-LINEAGE-JOIN`
status: `INTEGRATION_DESIGN_PROPOSAL`
design_id: `ID-SB-FLY-LOCAL-ATOMIC-WORLD-EFFECT-JOURNAL-001`
genuinely_new_information: `true`
new_sparkbrain_scientific_result: `false`
scientific_credit: `0`

Directive index `8ce979b9ec0bc7eede5225c0403698f8886d3e8d` / `1ba1e173344f36e14d0e21e6f3e823254e031f7d`, unchanged. Inputs: Control R143, Analyst R176, Theory R29, Literature R53 plus durable-partial R54 guidance, Audit R15. Refs inspected: main `59fc994b39d0ba02682e972161bb46801592d25b`, control `2b13447570e203b3efccdc5ded9ecd5bd0503d05`, analyst `acf01924d3db1fef0cbba3565db8aba2433ab642`, external-before `fbe44c805bed0eff8b76b9ae19bcccfb5de1bc57`.

## Proposal
For the local deterministic synthetic WORLD, refine R29 by making the authoritative WORLD mutation and its unique issue/action-bound `world_effect` row one ACID transaction. R28 supplies immutable issue/session/cut/recovery identity; journal and typed receipt must reference the exact effect token; R27 advances the causal frontier only after exact issue/effect/journal/receipt agreement.

When action leaves the local atomic domain, keep a separate established state machine: `INTENT -> DISPATCHED -> ACKNOWLEDGED | UNCERTAIN | COMPENSATED`. A local commit row proves local bookkeeping only, not remote or physical actuation.

Known reductions: SQLite/WAL or equivalent ACID transaction, transactional outbox, idempotency key, unique constraint, epoch fencing, Saga-style compensation. Prefer these established primitives over a bespoke certificate layer unless the latter passes an acceptance requirement the ACID baseline cannot.

## Acceptance
- skip WORLD transaction despite valid issue/journal/signal -> fail closed and no frontier advance;
- Issue A + Effect B -> reject;
- crash before atomic commit -> neither WORLD mutation nor effect row survives;
- crash after atomic commit before receipt -> both survive and only matching receipt reconciles;
- exact replay is idempotent with no second WORLD mutation;
- same identity with changed payload/digest -> conflict;
- old epoch/cut issue cannot create current effect;
- R14/R27 monotonicity survives restore/rebuild;
- retention expiry -> outside-horizon/unresolved;
- remote dispatch without acknowledgement -> external-effect UNCERTAIN.

Replacement test: R29 bespoke certificate vs SQLite/WAL single writer under the same suite. Ablate issue->effect identity, effect->receipt binding, frontier gating and external acknowledgement independently.

Alternative established architecture: event-sourced append-only WORLD log with replay/snapshot, likely more complex for the bounded local WORLD.

## Claim boundary / scope
This design is not scientific evidence. No biological fidelity/equivalence, fly-topology superiority, novelty, composition contribution, whole-system superiority, emergence, external validity, compute or energy efficiency is claimed. Scientific credit 0.

Suggested scope is bounded Forge acceptance refining R29/R30 after fresh Analyst reconciliation of the engineering-green R27 head. No M1 stop, no SB003 activation change, no mandatory review gate, no dispatch. P0 remains OPEN/root cause UNKNOWN. Literature R54 pointer debt and Control latest/state mismatch are observed but not mutated by this Theory role.
