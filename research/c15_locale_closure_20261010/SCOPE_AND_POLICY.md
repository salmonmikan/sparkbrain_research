# Finite model-free dependency verification proposal

Prepared source only. No target process, tests, CI publication or execution yet.
Five environment-check CI slots remain available.

## Exact next check

One process, Python 3.14.8 at the existing official hosted-toolcache path, isolated/no-site/no-bytecode, explicit UTF-8 mode, and inherited environment limited to LD_LIBRARY_PATH, LC_ALL=C and LANG=C. No model imports, model construction, native queries or scientific operations. An early audit hook rejects imports outside the prior 86-name diagnostic census and rejects socket/subprocess/fork/spawn/exec events. This name allowlist bounds the check only; it is not an approved module-provenance manifest. Exact CPython ABI/GIL, executable/base-prefix and three-entry import search path are checked.

Read and compare exactly the 53 known official artifact paths against independently acquired package bytes. Retain file identities, then inspect bounded /proc/self/maps snapshots after support imports and after fixed preloads copy/copyreg/dataclasses/random/inspect. Reject generated locale-archive, unknown mapped files, deleted mappings and writable-executable mappings. Accept no new file through observation. Anonymous mappings are allowed only when nonexecutable; the known kernel vdso (r-xp) and x86-64 vsyscall (--xp at ffffffffff600000-ffffffffff601000) are explicit executable pseudo-map exceptions. Neither is artifact-attested; this narrow classification is grounded in the prior C12 snapshot.

Resolve and retain the already identified BuiltinImporter.get_code wrapper closure edge in that same process, without invoking it. This is an explicit finite structural check, not recursive discovery or a blanket callable admission.

Inherited supervisor: exactly one target process, 30s wall, 15s CPU, 512MiB address space, 4MiB combined output. Collector explicit reads: 64MiB total, 32MiB/file, 1MiB maps each, <=4096 mappings/checkpoint, <=256 loaded modules, 1MiB JSON. Loader reads remain outside the explicit counter. No child process is created by the collector. Existing process-group timeout limitations remain unchanged.

Public logs are restricted to existing approved diagnostic categories: fixed runtime paths, module/function names, byte-comparison outcome, resource counters, mapping classes, explicit incomplete reason and false authority/science flags. No inherited environment dump or secrets. Exact source/ref hashes, independent review, fresh branch and duplicate-trigger gates are prerequisites for a single launch.

## Prospective trust policy, separate from the check result

The existing repository contract already assumes trusted source/environment bytes in a dedicated quiescent process. The narrow concrete proposal is to use:

- actions/python-versions asset python-3.14.8-linux-24.04-x64.tar.gz, 110382248 bytes, SHA256 fa74abc70a55c10f6631967784878704eef81bbde9b8ec27469534f6ba997cb3; independent reference is GitHub release asset API, release 3.14.8-36806082737, asset 602296995.
- Ubuntu libc6_2.39-0ubuntu8.9_amd64.deb, SHA256 ff5557d99b51f761c4b7c92368b9cc45565eda17df9bf9eb4b134d09825008be.
- Ubuntu libc-bin_2.39-0ubuntu8.9_amd64.deb, SHA256 066398a06ef1a218d4109461d4c636eafe83322ad19b179de9ef7af42b3fec58.
- Ubuntu libssl3t64_3.0.13-0ubuntu3.16_amd64.deb, SHA256 219f43b1cd836a4da550938db5fda93160d269d39a4edcf1f1ce698a470db797.

Exact reference URLs and per-file hashes are in REFERENCE.json. Published HTTPS distribution metadata supplies independent expected digests; no detached signature chain, reproducible source build or source-version equivalence is claimed. This proposal selects precise official binary distributions under the existing trusted-environment assumption. It does not strengthen that assumption into hostile-process attestation and does not relax it to trust arbitrary measured files.

For this environment-only check no trust promotion is needed: expected bytes are comparison references only. A later runtime-admission implementation must explicitly adopt a reviewed policy artifact under the existing contract and bind the full needed same-process stdlib closure before C7's native seam. Native/scientific execution still needs its separate authorization. If the existing authority does not cover adopting these official artifacts as the runtime reference, the only user decision needed is whether to use these exact four pinned official distributions under that existing dedicated/quiescent-process contract. No measured-snapshot exception is proposed.

## Remaining gaps even if this check passes

A pass establishes only the finite comparisons and the locale-dependency hypothesis for this process. It does not establish complete module/source/pyc/frozen selection, arbitrary function globals/defaults/annotation semantics, mutable dispatch behavior, full same-process live admission or scientific validity. Serialized output cannot carry a live admission token into another process.
