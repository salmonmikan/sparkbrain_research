# One-shot closure-cell diagnostic

This environment-only successor preserves a closure cell's process-local identity,
ordinal, and INCOMPLETE record status before reading or encoding its contents.
Empty cells and successfully encoded values receive OBSERVED_FIELDS status.
The first exact function reference still stops with FUNCTION_REFERENCES_UNRESOLVED
and exit 2. A retained cell does not resolve callable semantics or permit science.

Source predecessor: e7392e10b44f69c03fe7ea48fe27631e546b4694.
Prior failed run 38008062465 remains immutable and must not be rerun.

The collector change is limited to append-before-encode bookkeeping. No function
invocation, annotation evaluation, recursive reference worklist, extra imports,
new discovery root, environment-variable capture, or raw referenced value is added.
Public output remains the GitHub Actions log for this repository. New metadata is
only cell identity, ordinal, and status; existing hosted runtime paths, module and
mapping metadata, file/code hashes, finite function names, and receipt remain.
No artifact uploads are used.

Budgets unchanged: 32 MiB per file, 64 MiB explicit reads, 4 MiB combined output,
512 MiB address space, 15 CPU seconds, 30 wall seconds, 35-second wrapper plus
2-second kill grace, one one-minute CI job, and exactly one target capture.
CPython 3.14.8 x64 / Ubuntu 24.04 and supervisor source remain unchanged.
Loader/setup I/O are excluded from explicit read accounting; no OS network
isolation or guaranteed kernel-level termination claim is made.

The only authorized runtime action is one fresh environment-only CI run. No retry,
rerun, PR, merge, dispatch, second launch, trusted-pin approval, native admission,
research-body execution, or scientific credit follows from any result.
