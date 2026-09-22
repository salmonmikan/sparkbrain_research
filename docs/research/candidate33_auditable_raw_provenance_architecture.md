# Candidate 33 — auditable raw provenance architecture (NON-EVIDENTIARY)

This is an **Architecture Study / SYSTEM** implementation for `CAND-EQUIV-AUDITABLE-RAW-PROVENANCE-01` under `EQUIV-AUDIT-ARCH-R1-V1`.
It is not PRE_FORMAL or FORMAL evidence, does not establish semantic equivalence, and does not alter terminal candidate 32.

## Boundary

The controller owns the run/ref bindings, challenge nonces, launch ledger, runtime lock, resource caps and process launch recipes. Producer A and B execute as separate Linux user/PID/mount/network namespaces and write to separate raw directories. The verifier starts only after both producers exit and receives the run root through a read-only bind mount. The verifier recomputes SHA-256 from preserved raw bytes; producer-declared trajectory/checkpoint digests are not authoritative.

The implementation refuses ambient-thread execution by requiring producer and verifier PID 1 inside their PID namespaces. Runtime lock fields include Python patch/implementation, OS and architecture, clock implementations, timezone, locale, shell, PATH digest, CPU count, RSS source, hash algorithm, fixed resource caps, and role recipe hashes.

## Raw schema

Each producer emits:

- `producer_manifest.json`
- `trajectory.ndjson`
- `checkpoints.ndjson`
- `resources.json`
- `declared_digests.json` (non-authoritative self-report retained only to test stale-digest behavior)

Public SYSTEM verdict vocabulary is deliberately limited to:

- `AUDITABLE_RAW_MATCH`
- `AUDITABLE_RAW_MISMATCH`
- `INVALID_PROVENANCE_CHAIN`

No scientific tolerance is inherited from candidate 32/R50.

## Prospective architecture controls

The fixed synthetic fixture has a clean match pair and a one-field raw mismatch pair. Resource caps are frozen in source before execution: producer wall time <= 5000 ms, producer `ru_maxrss` <= 262144 KiB, and controller-wrapper RSS overhead <= 65536 KiB.

Fail-closed controls include at minimum:

1. mutate preserved trajectory bytes after the producer-declared digest is written; verifier-side recomputation must no longer produce a raw match;
2. swap the controller ledger's producer/ref binding; verifier must emit `INVALID_PROVENANCE_CHAIN`;
3. missing required raw files, reused producer/challenge/host identity, reused PID/mount/network namespace, or runtime-lock mismatch must fail closed.

This study tests auditability reachability only. A future semantic comparator or floating-point tolerance would require a separate prospectively fixed science-affecting contract.
