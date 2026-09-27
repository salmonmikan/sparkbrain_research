# Bounded receipt retention (Forge prototype)

Status: `FORGE_PROTOTYPE` / non-evidentiary / noncanonical.

This extension puts an optional positive `receipt_capacity` on the local
idempotent outcome stream. Once the capacity is exceeded, the oldest exact
receipts are removed while three pieces of conservative metadata remain:

- `retained_from_sequence`, the first sequence with an exact receipt;
- a rolling SHA-256 digest of the compacted receipt prefix, for checkpoint
  integrity and audit comparison rather than membership proofs;
- a fixed 2,048-bit, four-position event-identity filter.

Within the retained window, exact replay still returns the stored receipt. A
replay older than the window raises `CompactedReceiptUnavailableError` and is
never re-applied. Reuse of an event identifier that the fixed filter marks as
possibly compacted raises `CompactedEventIdentityError`. The filter is
deliberately fail-closed: it has no false negatives for inserted identifiers,
but false positives rise as history grows and may reject a genuinely new
identifier. This preserves safety at the cost of eventual liveness; operators
must rotate or archive streams before the filter saturates.

The capacity and compaction metadata are checkpointed under the same atomic
replace, directory flush, and cooperating-process lock as the prior prototype.
Reopening an existing bounded checkpoint with a different explicit capacity is
rejected. Version-1 unbounded stream snapshots are accepted and migrate in
memory without implicit compaction.

## Ordinary explanation and limits

This is log retention plus a conservative duplicate filter. It does not prove
distributed exactly-once delivery, preserve exact old receipts, make a remote
transaction, supply a learning rule, or add scientific evidence. It bounds the
exact receipt ledger, not the coordinator state or the total checkpoint size.
It also inherits every prior local-store limit: advisory-lock bypass,
non-POSIX/network filesystem behavior, post-replace uncertain commits,
power-loss and filesystem faults not exercised here, and no fairness or remote
storage guarantee.
