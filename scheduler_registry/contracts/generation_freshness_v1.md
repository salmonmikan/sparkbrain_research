# SparkBrain Control-Plane Generation / Freshness Contract v1

## Principle

Scheduler time is a polling opportunity, not proof that upstream work completed. Durable generations and authoritative refs determine whether work may proceed.

## Producer envelope

Every durable state/handoff producer records:

- `schema_version: 2`
- `generation_id`: role-scoped unique ID generated before persistence; MUST NOT depend on the producer's own resulting Git commit SHA
- `produced_at`
- `producer_run_id`
- `authority_scope`
- `supersedes_generation_id` (nullable for bootstrap)
- `input_generations`: map of consumed streams to generation ID, handoff commit when known, and observed timestamp
- authoritative refs relevant to the role

The resulting Git commit remains separate provenance and is recorded by consumers as `consumed_*_commit`.

## Consumer rules

1. Re-fetch the controlling handoff/state and authoritative repository refs at run start.
2. Record the exact generation ID and Git commit consumed.
3. Do not infer ordering from scheduled clock slots.
4. Immediately before a critical mutation, workflow dispatch, STARTED transition, merge, preserve/score action, or other role-specific irreversible step, re-read the controlling generation.
5. If a newer generation materially changes allocation, authority, bindings, stop conditions, or ownership, stop/reconcile before mutation.
6. If a newer generation is semantically equivalent for the current object and bindings, the worker may refresh authority and continue, recording the refreshed generation.
7. If no new relevant generation exists, do not manufacture work. A role with prospectively authorized autonomous bounded progress may continue only within that explicit authority and must record why same-generation progress was valid.

## Freshness

Freshness = generation dependency + authoritative refs + age signal.

- Old age alone does not invalidate an unchanged generation.
- Recent timestamp alone does not validate a generation whose dependency/ref has advanced.
- A stale dependency is a knowledge-flow condition, not permission to guess.
- Consumers should expose `last_consumed_generation` / `input_generations` so lag can be audited.

## MAIN / Relay

MAIN lease/state records the consumed Analyst generation and commit. Relay must match the current Analyst authority plus MAIN run/generation, branch/head, workflow and continuation state. A stale/missing lease never grants authority.

## SUB

SUB records Analyst generation. Same Analyst generation can still permit a new bounded independent Discovery only when the standing Analyst allocation explicitly allows autonomous Discovery and all exclusions/cycle budgets remain valid.

## External / Methodology

These roles may produce a new generation from genuinely new independent literature/audit/calibration work even when research allocation is unchanged.

## Control / Utility

Control records generation deltas across the fleet. Utility assignment and state use assignment generation/identity. Utility never self-approves, self-extends, or closes Control-owned assignment pointers.

## Compatibility

Existing state files lacking generation fields are `LEGACY_GENERATION_UNKNOWN`, not invalid evidence. Consumers bootstrap prospectively and do not rewrite historical scientific results.
