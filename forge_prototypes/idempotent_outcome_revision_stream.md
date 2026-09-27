# Forge prototype: idempotent observed-outcome revision stream

Status: FORGE_PROTOTYPE  
Source design: ID-SB-LATENT-SCOPE-PLURAL-REVISION-001

## Question

Can the one-step transaction coordinator tolerate ordinary at-least-once stream
delivery without applying the same revision twice, silently accepting two
different payloads under one event identifier, or reordering new events?

## Prototype

`IdempotentOutcomeRevisionStream` adds a small delivery ledger around the
transactional coordinator:

- each new event must carry the next contiguous sequence number;
- the event identifier is bound to a SHA-256 digest of every public input;
- exact redelivery returns the stored semantic receipt without re-evaluation;
- same-identifier/different-content delivery fails closed;
- stale or gapped new delivery fails closed;
- no-write outcomes are also ledgered, so later state changes cannot turn a
  replayed omission into a mutation;
- coordinator state, sequence position and the receipt ledger round-trip in one
  deterministic checkpoint.

The candidate coordinator is restored from a checkpoint and evaluated before
live coordinator/ledger state advances. A validation exception consumes neither
the sequence number nor event identifier.

## Ordinary reduction

This is an ordinary ordered idempotent consumer with a content-addressed
deduplication ledger and copy-on-write state transition. It is not distributed
exactly-once processing, event-time inference, a learned memory mechanism or a
scientific result.

## Claim boundary

Passing bounded tests supports only local retry/replay hygiene for this isolated
Forge chain. It does not test a continuous scientific task, long-running storage
retention, distributed crashes, matched comparators, resources, interaction
ablations, composition contribution, SYSTEM_BUILD admission or novelty. It is
not admitted to SB001 or RV02.
