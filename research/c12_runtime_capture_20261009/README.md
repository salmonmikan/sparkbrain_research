# C12 Phase A prospective runtime observation, revision 2

SOURCE ONLY. No new test, target capture, native/C11 import, owner, query, science,
CI, publication, installer or local-PC work was executed for this revision. All
historic trusted pins remain unchanged. r1 and its test receipts are preserved.

## Usable first observation without prior trusted runtime pins

`capture.py` retains its strict explicit manifest API. Its new
prepare_observation_manifest function, in the SAME supervised target process,
can first derive that finite manifest from preapproved public runtime metadata.
It is not a second capture or a trust/admission step. Ordinary exact
CPython (3,14,8,'final',0), -I -S -B, a bound official setup-python prefix under
/opt/hostedtoolcache/Python/3.14.8/, and the exact executable/source hash are required.

Discovery is only currently loaded/preloaded stdlib ModuleSpec origins under
that prefix, the exact executable/collector, and file-backed /proc/self/maps
images under that prefix or canonical /usr/lib/x86_64-linux-gnu. There is no
recursive directory walk, all-filesystem scan, environment-variable read,
credential/user-file read, site-package import or SparkBrain/C11/native import.
Source-root access admits only the explicit collector file. Module closure is
capped at 256, file closure 192, proc metadata 1 MiB/4096 lines. Every path is
admitted before it is opened. Noncanonical/symlink/unexpected roots or loaders
stop. Bootstrap metadata reads join the same 64 MiB explicit read budget.

The collector captures executable/version/build/ABI/flags/pointer-width/import
configuration, observed file hashes, mapped-image metadata, bounded direct
function/class-method code fingerprints, defaults/closures and globals ownership.
Opaque/cyclic closure values terminate INCOMPLETE while preserving bounded partial
evidence. No annotations/properties/repr/default factory/native method are evaluated.
All hashes/fingerprints are observations. They do not prove executed-code provenance
or source equivalence. Frozen, extension and builtin evidence is distinct.

native_admission=false; scientific_execution=false; trusted_pins_approved=false.
No result chains into Phase B, installs trusted pins or changes historical pins.

## Enforcement and limits

The Linux wrapper installs child-only 15s CPU, 512MiB address-space, core/file-size
rlimits before target exec; monitors target streams against one 30s deadline;
limits combined target streams plus public log receipt/framing to 4MiB; kills the process group
on terminal paths; reserves an exclusive output directory. One target, no retries.
64MiB counts explicit collector reads (32MiB per file), including bootstrap metadata;
interpreter startup/import/pyc loader I/O and wrapper input/source reads are excluded.
-B suppresses pyc writes, not reads. No network operations occur in the collector,
but no OS network isolation or fork containment is claimed. Trusted quiescent roots
are required; ancestor path races and hostile interpreter containment remain outside
this source-observation contract.

Blocking Popen/preexec and wrapper filesystem I/O cannot be interrupted by its
stream deadline. The prospective workflow adds GNU timeout 35s + 2s kill grace and
an outer 1-minute GitHub job timeout. This is not a strict 30s whole-job promise.
Queue/provisioning precede the job, and checkout/setup can consume the job ceiling.
Job cancellation/kernel uninterruptibility may prevent receipt preservation.
Workflow setup/action diagnostics are outside the 4MiB observation log cap.
The bootstrap workflow emits bounded stdout logs only, with zero evidence artifacts
and no duplicate local evidence files (only the exclusive attempt directory). setup-python may acquire the exact official runtime; that new setup/network
scope requires fresh explicit user approval. If unavailable or over any bound, stop;
no fallback version, retries, repair, budget increase or Phase B.

## Validation

Revision 2 has had source-only preparation and read-only independent review only.
No r2 test or runtime execution was authorized. r1's 10-pass/one-fixture-error suite
and separately approved corrected-one-test pass are historical helper evidence,
not a test pass for this added bootstrap/workflow. See WORKFLOW.md and public plan.

Provisioning scope: pinned setup-python itself resolves python-versions release
metadata and can download/run its setup script on cache miss. Its action pin does
not freeze every runtime release asset. Provisioning may invoke Python outside the
supervised capture; one-attempt means one supervised capture child, not one Python
invocation across the whole job. Network/installer/setup effects and their I/O/CPU
are outside capture limits, but within the job timeout. Future approval must cover
these explicitly. The target gets only LD_LIBRARY_PATH set to the bound official
prefix/lib; no runner environment, token or secret is inherited.
