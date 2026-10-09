# C12 Phase A bootstrap diagnostic, revision 3

Prepared offline. No publication, CI, native capture, Phase B, scientific execution,
or trusted-pin change has occurred for this candidate. The failed first source and
run 37937365823 at commit 746c88a75dc8725429514d210c753d5ee456d897 remain untouched.
Its OUTSIDE_APPROVED_ROOT result does not identify which path was rejected.

The only collector change is a single bounded latest bootstrap checkpoint before
existing path checks: finite stage, zero-based entry ordinal, finite role, lexical
approved-root category, and (for mappings) lexical library-name category. No raw
candidate path, filename, module name, contents, exception payload, environment or
secret is added to the diagnostic. Successful existing observations may still
include already admitted public runtime paths under the original contract.

Stages are executable, collector, sys_path, module_origin, and mapped_file.
Ordinals index executable/collector singleton 0, sys.path, the snapshotted module
sequence, or /proc/self/maps lines respectively. The exact collector exemption
already existed and is preserved; other source-root module origins stay rejected.
Root categories are INVALID_ABSOLUTE_PATH, NONCANONICAL_PATH, EXACT_COLLECTOR,
APPROVED_RUNTIME_PREFIX, APPROVED_SYSTEM_LIBRARY_ROOT,
SOURCE_ROOT_OTHER_NOT_BOOTSTRAP_ADMITTED, and OUTSIDE_APPROVED_ROOTS.
Categories are lexical descriptions, never admission: an approved-root category
can still fail a narrower per-role scope or the unchanged symlink checks.
Mapping names ending .so or .so.NUMERIC[.NUMERIC...] are SHARED_LIBRARY_NAME;
other names are OTHER_FILE_NAME. This is a filename convention, not file-type
verification; no off-root target is opened or probed for this classification.

All original scopes, checks, failure outcomes, read/stream/process bounds and
no-retry rules remain. Root scopes: exact official bound runtime prefix,
exact collector file within its source root, and canonical system mapped files
under /usr/lib/x86_64-linux-gnu. No extra locale/shared-data root is added.
The single checkpoint is overwritten rather than accumulating per-entry records.

Fresh synthetic-only test_bootstrap_diagnostic.py covers each of four off-root
failpoints, collector exemption, runtime/system prefix boundaries, a symlink,
source-root noncollector denial, mapped library/nonlibrary and finite malformed
path classifications. Tests mock metadata and proc I/O, do not run original 10+1
helper tests, supervisor, native capture, target Python or scientific code.
Execution is held until independent source preflight. Test evidence is separate
from frozen candidate files and supplies zero runtime-admission credit.
