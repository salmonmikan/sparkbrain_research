# Bounded function-reference observation, source-only successor

This collector records the first encountered exact Python function reference without
calling it, then returns INCOMPLETE / FUNCTION_REFERENCES_UNRESOLVED with exit 2.
It preserves the containing partial function record and a finite diagnostic path.
Identity, bounded name/module/qualname, code identity, globals identity, process-local
reference ordinal, and structural code hash are observation metadata, never complete
callable-state provenance. Referenced defaults, closure and globals are not traversed.
Names outside 256 ASCII characters are marked redacted and not exact. Nested paths
contain only finite code-field names and container ordinals; depth is capped at 64.

Strong references prevent identity recycling. Only exact FunctionType is recognized.
A separate structural-code encoder rejects functions and shares the original 100000
node / 4096 code budgets. Partial reference metadata is published before hashing.
No function invocation, annotation evaluation, repr, eval, descriptor expansion,
new preload, module discovery, filesystem root or environment-variable capture is added.
The output-limit fallback retains the finite diagnostic and first partial reference.
No graph-completeness or stable-fingerprint equivalence claim is made.

The prior exact two locale files remain the only special candidates, and only when
already mapped: /usr/lib/locale/locale-archive and /usr/lib/locale/C.utf8/LC_CTYPE.
All original roots and checks remain. Limits remain 32 MiB per file, 64 MiB explicit
reads, 4 MiB combined output, 512 MiB address space, CPU 15 seconds, phase 30 seconds,
wrapper 35 seconds plus 2-second kill grace, and a single one-minute CI job.
Official CPython 3.14.8 x64 / Ubuntu 24.04 and supervisor bytes are unchanged.
Loader/setup I/O are outside explicit collector read accounting. No OS network
isolation or guaranteed kernel-level termination claim is made.

This preparation ran no tests, mocks, imports, collector, supervisor or native code.
The one separately approved CI allowance is controlled by the root coordinator.
There is no retry, rerun, second branch launch or automatic continuation.
No native admission, trusted pins, research execution or scientific credit follows.
Prior commit 3486ee6073cbd40301edf057edac619c4c3b7a1c and run 37965212437 remain
immutable failure evidence. Main 3313974cf0cf7389d7bf1e3f714eb55e0721c0dd is unchanged.
