# Durable observed-outcome revision store

This Forge-only adapter persists an `IdempotentOutcomeRevisionStream` as a
single local checkpoint. It evaluates each event on a copy, writes a complete
same-directory temporary snapshot, flushes it, atomically replaces the prior
checkpoint and then installs the candidate as live memory.

The checkpoint contains a canonical SHA-256 digest. A writer also remembers the
digest it opened and refuses to overwrite a newer checkpoint produced by a
second local writer.

## Bounded behavior

- failure before atomic replace leaves disk and live memory unchanged;
- a crash after replace is recovered by reopening the checkpoint;
- redelivery after an uncertain commit is safe through the existing receipt
  ledger;
- stale local writers fail closed;
- malformed, torn or digest-mismatched checkpoints fail closed;
- checkpoint and stream state remain local and offline-capable.

## Reduction and limitations

This is ordinary atomic-file replacement, optimistic digest comparison and an
idempotent consumer. It is not distributed exactly-once processing, consensus,
event-time inference, a learned memory mechanism or scientific evidence.

The prototype does not provide multi-process locking, remote storage, broker
integration, receipt compaction, backup rotation or proof against filesystem or
hardware failure. Directory `fsync` support is platform-dependent. A real
exception after replacement is an uncertain commit and requires reopen plus
idempotent redelivery.
