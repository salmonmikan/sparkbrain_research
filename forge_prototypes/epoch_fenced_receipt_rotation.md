# Epoch-fenced receipt rotation (Forge prototype)

Status: `FORGE_PROTOTYPE` / non-evidentiary / noncanonical.

The bounded receipt prototype uses a fixed conservative identity filter.  It
cannot forget compacted identifiers safely, so false-positive refusal grows as
the stream runs.  This extension adds an explicit transport-only
`stream_epoch` and a compare-and-fence rotation operation.

Within an epoch, exact receipts, compacted-history rejection, POSIX locking and
atomic checkpoint replacement work as before.  Rotation is accepted only when:

- the next epoch is exactly the current epoch plus one; and
- the caller's `expected_next_sequence` matches the current locked checkpoint.

The rotation hashes the complete retired epoch into a rolling chain digest,
preserves the revision coordinator, then starts a fresh delivery namespace at
sequence zero with an empty exact ledger and identity filter.  All earlier
epochs are rejected wholesale.  Reusing an event identifier in a new epoch is
safe only because an old delivery must carry its old epoch and is fenced.

`stream_epoch` is transport metadata.  It must not encode or proxy scope,
regime, episode, target, truth or evaluator identity.

## Ordinary explanation and limits

This is epoch fencing, log rotation, a hash-chain audit summary, advisory
locking and atomic local snapshot replacement.  It is not distributed
consensus, broker fencing, proof that all producers stopped an old epoch, a
learning mechanism, a memory principle, or scientific evidence.

The chain digest is an integrity summary, not an archive or membership proof.
Exact retired receipts cannot be reconstructed.  A producer that lies about
the epoch can still create a logically new delivery.  Rotation coordination,
multi-host leases, network filesystems, non-cooperating writers, process kill,
power loss, checkpoint archives and filter-saturation thresholds remain
unverified.  The prototype bounds current receipt/filter state per epoch, not
the revision coordinator or every possible checkpoint field.
