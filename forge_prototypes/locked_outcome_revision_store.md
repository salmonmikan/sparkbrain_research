# Locked local observed-outcome revision store

This Forge-only adapter adds a stable POSIX advisory lock around the durable
outcome-revision checkpoint. Every cooperating writer takes the same exclusive
lock and then reopens the checkpoint inside the critical section before it
evaluates one event.

The in-lock reload closes the prior optimistic-check gap: two processes may be
created from the same checkpoint, but the second process observes the first
process's committed receipt and sequence before processing. Exact concurrent
redelivery therefore becomes one processed event plus one duplicate replay,
not two state transitions or a last-writer-wins overwrite.

## Bounded behavior

- cooperating processes serialize through a stable sidecar lock file;
- every operation reloads the latest digest-verified checkpoint under lock;
- distinct contiguous events from previously opened instances both commit in
  order without stale-writer overwrite;
- exact concurrent redelivery applies once and returns one duplicate receipt;
- lock acquisition has a bounded timeout and leaves checkpoint state unchanged
  on timeout;
- the existing atomic replace, directory flush, digest check and uncertain
  commit recovery remain in force.

## Reduction and limitations

This is ordinary POSIX `flock` serialization around atomic snapshot replace and
an idempotent consumer. It is not lock-free compare-and-swap, distributed
consensus, remote-store exactly-once processing, a cognitive mechanism or
scientific evidence.

The lock is advisory and only protects cooperating writers that use the same
filesystem and lock path. POSIX `flock` availability and network-filesystem
semantics are platform-dependent. Process-kill, power-loss, filesystem-fault,
receipt-compaction, backup and migration tests remain unresolved.
