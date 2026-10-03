# Disposable-environment recovery

## One-command setup

Keep source, configuration and accepted small records in reviewed Git commits.
Rebuild disposable virtual environments instead of copying them between machines.
From a verified checkout, with **CPython 3.12.14 on Linux x86-64 / glibc 2.17+**:

```bash
python -I -B scripts/recover_environment.py
```

This creates `.venv-recovery` from the 13 exact official wheels in
`environments/tools-linux-cp312.lock.json`. URLs, sizes and SHA-256 hashes are
committed. The set includes pytest, Ruff, jsonschema, their dependency closure and
the pinned pip installer. It is **not** the full optional lab/learned/spiking stack.
Historical release locks are unchanged and not relabeled as cross-platform locks.

For the dependency-free reference package on CPython 3.11+:

```bash
python -I -B scripts/recover_environment.py --core --offline
```

Use a new prefix when changing profile or runtime. Core-only does not install
testing tools or imply full-suite readiness. Neither mode constructs a model,
runs a demo, launches an experiment, loads a checkpoint or changes scheduler or
authority state. Its automatic package check is import/origin/version validation.

## Verified cache and offline restore

```bash
# Use a durable volume only if that destination is already authorized.
python -I -B scripts/recover_environment.py \
  --cache /approved/cache/sparkbrain-wheels --prefix /work/env-a

# A second empty prefix; no downloads or dependency resolution.
python -I -B scripts/recover_environment.py --offline \
  --cache /approved/cache/sparkbrain-wheels --prefix /work/env-b

# Synthetic infrastructure tests, requiring no third-party package.
python -B -m unittest discover -s tests -p test_environment_recovery.py -v
```

The default deadline is 300 seconds (`--seconds 1..900`). Linux acquisition has an
elapsed timer that interrupts even a trickling response, at most a 15-second socket
timeout, and up to three total attempts with 1/2 second backoff for recognized
transient failures. TLS failures, HTTP permissions, redirects, unknown errors and
integrity mismatches stop without retry or alternate transport. The existing
platform proxy and CA are honored; no credential logging, mirror, direct-IP route
or security/network-setting change is attempted. Failure messages retain safe
error classes/status codes instead of raw proxy-bearing exception strings.

Downloads are size/hash checked before atomic cache promotion. Every reused wheel
is checked again. Corrupt entries and partial downloads remain for diagnosis and
are not installed. Keep the cache private to trusted writers during use; this is
not an adversarial filesystem sandbox. Remove obsolete partials only after review.

Only after all wheels are verified is the venv created. The verified pip wheel
runs directly with `--no-index --no-deps --require-hashes --only-binary=:all:`.
Offline children omit inherited Python/pip/proxy configuration. No build backend
runs and no editable-build dependencies are fetched. A plain local path file
attaches the source; the imported package origin must match the requested checkout.

Every repeated restore rebuilds the owned prefix cleanly at its original path.
The old directory is preserved as `.incomplete-<timestamp>` after an interrupted
attempt, or `.previous-<timestamp>` after a ready result. These are diagnostic
snapshots, not relocatable environments. This prevents half-written metadata,
untracked tool modules and startup hooks from surviving reinstall. Review and
remove old snapshots when no longer needed; repeated restores use additional disk.
An unowned existing directory is not overwritten. Prefixes below `src` are rejected
so installed dependencies cannot contaminate the developer-source digest.
All symlinks in `src`, including directory links and the source root itself, are
rejected before setup. The Python-source identity is checked again before the
ready receipt; changes during restoration fail instead of receiving a stale digest.
The dependency lock is parsed and hashed from one byte snapshot, then compared
again before readiness; a changed lock cannot mislabel an installation's receipt.
The recorded runtime fields are also checked again before readiness. These drift
checks do not create an atomic filesystem snapshot or extend the runtime identity
to unrecorded native-library bytes.
Concurrent restores to one prefix are rejected. After a killed process, remove
its `.recovery-lock` directory only after confirming that process has stopped.
Runtime/lock changes require a new prefix. Extra distributions or a shadow package
fail validation. These receipts are developer diagnostics, not experiment authority.

## What is and is not pinned

The tools lock pins the interpreter patch and wheel ABI. Receipts record the
observed interpreter hash, OS/architecture, libc version, lock digest and developer
Python-source digest. Source edits are recorded on later developer restoration.

This does **not** freeze an OS image, kernel, libc bytes, complete stdlib, startup
hooks, every importable file or a full scientific source tree. Matching libc
versions do not prove matching native-library bytes. A new venv on the same host
is not a cold-host/container restore. Docker is optional and no unverified image
digest is introduced by this change.

Before admitting a new experiment that requires exact environment reproduction,
its prospective contract must also pin and retain a runnable base-image/runtime
artifact by immutable digest where supported, full dependencies/inputs/source and
relevant native-library/startup bindings. Test that restoration on a separate
clean host/container. If unavailable, mark that stage unverified and review a new
environment identity. Never relabel changed dependencies/host libraries as an old
freeze or replace system libraries to force a historical fingerprint match.

## Durable preservation before experiment execution

A cache or receipt in the same ephemeral workspace is **not a backup**. A digest
without retained bytes is insufficient. Before relying on recovery, establish:

1. Source/config/protocol and small non-sensitive records are published to the
   approved repository at immutable commit/blob IDs and independently read back
2. Experiment identity, execution/consumption status, source/environment/input
   pins, phase, checkpoint sequence and next permitted action are durably recorded
   before launch and at permitted checkpoint boundaries
3. Checkpoint and raw-result **bytes**, sizes and hashes are copied to an approved
   durable destination and independently read back. Large files, private material,
   external datasets, host details and credentials are not pushed to the public repo
4. A second empty workspace retrieves and verifies those exact bytes without the
   original workspace. Record actual restored stages and times; do not promise an
   assumed instant or byte-identical full-environment recovery

These requirements do not authorize a new data publication, credential, paid
service or storage integration. This bootstrap does not provision a checkpoint
store or automatically write experiment status. Existing role-owned persistence,
scientific ledgers and admission checks remain authoritative. If a required
approved durable destination is missing, that prerequisite remains blocked.

A handoff should bind at least experiment ID, immutable source commit, prospective
environment identity and lock hash, authoritative status-record reference,
execution status (including unknown/consumed), checkpoint sequence, durable object
reference/size/SHA-256, remote-readback result and next permitted action.

Missing local files never prove an identity was unused. Environment restoration
never authorizes replay, restart, fresh observations or reuse of a consumed run.
Inspect the durable ledger and current contract first. Uncertain status fails
closed to inspection. Continuation additionally needs its exact checkpoint
contract and valid current source/environment admission.

## Validation boundary

The new unittest suite uses synthetic sources and mocked network responses. It
covers cold-core creation, moved sources, repeated invocation, interruption,
runtime drift, cache integrity, offline mode, bounded retries/deadlines,
permission/TLS/protocol errors and shadow-package rejection. The dedicated CI
workflow additionally acquires exact wheels without a cache, then restores another
empty prefix offline. All commands also run locally; CI is supplementary.

Actual measured results belong in the PR. Unrun full-host, optional-stack,
full-suite and scientific-admission stages must stay explicit. No scientific
claims, frozen outputs, consumed identities or historical evidence change here.

References: [Python venv lifecycle](https://docs.python.org/3/library/venv.html),
[pip hash-checked installs](https://pip.pypa.io/en/stable/topics/secure-installs/).
