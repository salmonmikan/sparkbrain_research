# G0 v3 external prelaunch materialization verifier

**NEW SOURCE-ONLY IMPLEMENTATION, NOT RECOVERED CODE. UNAPPROVED.**

This is model-free preparation for `assembly-m1-g0-v3-20261003`. It does not import
SparkBrain, run a candidate interpreter, acquire a package, reserve an identity,
issue an approval, issue the legacy `g0-prelaunch-materialization-attestation-v1`,
or launch a target. No real final binding/observation/overlay is included.

The published v2 baseline remains an immutable reference, not v3 execution
source. A final v3 source commit/tree and environment freeze do not yet exist.

## Files and checks completed

- `materialization_verifier.py`: stdlib-only checker and future authority-facing API
- `published_baseline_inventory.json`: exact **source inventory**, not an attestation
- `test_materialization_verifier.py`: 48 inert synthetic filesystem tests
- `test_results.txt`: focused test output only
- `format_validation.json`: lint/AST-change accounting
- `_prepare_inventory.py`: reproducible read-only baseline-inventory reconstruction

The source-only check read all 1,323 baseline files, totaling 165,996,693 bytes,
compared Git blob SHA-1 and exact Git/POSIX file modes, computed every SHA-256,
and independently reconstructed the Git tree:

- Published commit: `16dba8f28a88134c57603d4f0c90d2edc39e4e49`
- Published tree: `cbb897ed74a1f0b9f40c77e534c794dc82c7a962`
- Raw bundled inventory SHA-256: `1dbe162e7b015193c9de9f8c25b1363b889feb9e1fb6d7f5b5e28f9289ee343f`
- Canonical `files` array SHA-256: `c2f0fb45c5a956e6fe9f5e56d61b750d9e84deb945d3d75e40030f185b52ce75`

The commit-to-tree publication provenance comes from the independently supplied
published GitHub tree, not local Git metadata. Git-tree reconstruction authenticates
bytes/modes against that fixed tree; it does not query GitHub or prove publication.

Run from any working directory, using a separately trusted verifier interpreter:

```sh
python -I -S -B /absolute/path/prelaunch/test_materialization_verifier.py
python -I -S -B /absolute/path/prelaunch/materialization_verifier.py check-source \
  --root /absolute/path/to/exact/published-baseline
```

`check-source` is hard-wired to the archived v2 commit/tree and inventory digest.
It cannot bless a changed v3 tree. Its JSON says `environment_verified: false`
and `execution_authorized: false`. A copied inventory must stay adjacent to the
checker, or integration must deliberately adjust its fixed resource location.

## Future independently trusted binding

`verify_final(binding_path, externally_trusted_sha256, request)` is the complete
validation entrypoint. `check-final --binding PATH --binding-sha256 DIGEST
--launch-request PATH` exposes it as a CLI. The digest is of the **raw binding
file**, including whitespace, authenticated through a separate trusted authority
channel. Deriving it from the candidate binding and calling that “external proof”
is invalid. The verifier reads and hashes the exact buffer it then parses, rejects
duplicate keys and nonfinite JSON (including finite-looking float overflow such
as `1e400`, `-1e400`, and `1e999`), and never fetches or executes referenced content.

The binding schema is `g0-external-prelaunch-binding-v3` with exactly:

- `source`: canonical absolute root, published commit/tree, independently verified
  publication reference, complete file records, explicit dynamic-data exceptions
- `runtime`: interpreter and timeout paths, ordered import-root inventories,
  repository import roots, trusted native/startup files, startup absence checks,
  absent import archives, exact startup search-path order, independently reviewed
  native/startup closure reference and digest, complete replacement environment
- `bindings`: the final execution-object digest, existing source-inventory digest,
  environment-freeze digest, and runtime-origin commit
- `target_arguments`: the fixed arguments from `expected_arguments(binding)`

Each file record contains `path`, `mode` (`100644` or `100755`), byte `size`,
`sha256`, and `git_blob_sha1`. Inventories contain **every file**, including JSON
schemas, package data, dependency metadata, and native extensions. Import-root
inventories are closed; extra files, packages, namespace directories (including
empty ones), symlinks, hardlinks, special files, executable-bit drift, and writable
group/world modes fail. Repository bytecode always rejects, even if declared.
Existing runtime bytecode is allowed only as an exactly inventoried file; changing
or adding cache bytes fails. This authenticates the reviewed cache bytes; it does
not independently prove source-to-pyc equivalence or regenerate bytecode. Root ancestors cannot be symlinks.
All declared top-level import names are compared across ordered roots, including
namespace directories and ABI-tagged extension modules. Collisions reject rather
than silently accepting path shadowing. Conservative checks can reject legitimate
multi-root namespace packages: no such exception is silently invented.

Each `import_roots` entry has exactly `path`, `files`, and `excluded_subtrees`.
`import_roots` may include both a stdlib root and nested `lib-dynload`; each must
have an exact inventory, and duplicate import names still reject. The standard
pinned `__pycache__` directories may coexist across runtime roots, containing only
bytecode; repository cache directories remain prohibited. Resource files
under nested roots are intentionally checked more than once. Zip import archives
are unsupported unless explicitly declared **absent**, with their path/order
bound. An expected-but-absent path becoming a file, directory, or symlink fails.

A stdlib inventory containing `site.py` and `runpy.py` may explicitly exclude only
its top-level `site-packages` and/or `dist-packages` directories. These must be real,
non-writable directories. Such an exclusion requires the target interpreter's
exactly pinned `../pyvenv.cfg`, with `include-system-site-packages = false`. No
excluded directory or any descendant may simultaneously be a declared active
import root. This avoids scanning globally installed, inactive base packages;
the independent startup review must establish their inactivity. Exclusions never
apply to arbitrary subdirectories or to source roots. Nested stdlib directories
which really occur on `sys.path`, including `lib-dynload`, remain inventoried.

No `.pth`, `._pth`, `.egg-link`, `sitecustomize` or `usercustomize` hook is permitted
inside any source/import tree, even if included in the binding. Declared
`pyvenv.cfg` outside the import roots is hash-checked and parsed from the same
buffer, requires a canonical `home`, and requires
`include-system-site-packages = false`. Its exact bytes remain authority-pinned.
Unlisted adjacent venv configuration and `/etc/ld.so.preload` must be absent.
Additional relevant build-specific startup paths belong in the trusted authority's
`startup_absent_paths` and native/startup closure review.

Native libraries, interpreter, GNU timeout, and loader configuration are exact
regular files in `trusted_files`. Required roles include one interpreter and one
timeout. Native-extension package bytes are already included in import roots.
The checker does not run `ldd`, import an extension, or execute the candidate to
learn its search path. Completeness of the native catalog (including possible
later `libgcc_s` mappings), loader configuration and interpreter startup path is
an **independently reviewed input**, not a deduction from a current `/proc` map.
Current-mappings subset validation and later runtime enforcement remain separate.

## Preserved command profile and acyclic approval graph

The fixed target command remains:

```text
<timeout> --signal=KILL 900s <interpreter> -B -s -m scripts.launch_g0_v3_eligibility
  --run-reviewed --root <exact-root>
  --approval-sha256 <typed raw-approval digest slot>
  --approval-object-sha256 <typed canonical-approval digest slot>
  --published-commit <externally bound final commit>
  --source-inventory-sha256 <externally bound final source inventory>
```

The exact cwd is the source root. The complete replacement environment requires
`PYTHONPATH=src` and `PYTHONDONTWRITEBYTECODE=1`; only `LANG`, `LC_ALL`, `TZ` are
additional allowed variables. `PYTHONHOME`, `PYTHONSTARTUP`, preload/loader variables,
extra path roots and inherited environment are not allowed by this profile.
There is no new `-I -S` target bootstrap. `-I -S -B` applies to the **external
verifier's trusted interpreter**, not the scientific target.

The authority must independently establish that the pinned interpreter/site
configuration produces the recorded startup path: cwd, `src`, then the ordered
trusted roots, with absent archives at their pinned positions. Merely asserting
this in a self-created binding is insufficient. `-s` disables the user site;
known system/venv startup hooks and resources are covered by the closed inventory.

1. `make_launch_request(binding)` creates a typed **non-executable** template with
   two digest slots; `verify_final` compares the whole template exactly
2. `verify_final` returns `g0-prelaunch-observation-v3`, marked
   `checked-not-authorized`, with hashes of the raw authority binding, full source
   inventory, and command template. It contains no approval bytes/digests and makes
   no claim that target startup has already been externally sequenced
3. The independent authority reviews/checks the exact frozen source/environment
   while holding it quiescent, establishes that the target has not started, and
   can later issue its own proof/approval under the separate execution policy.
   The new observation is **not** a drop-in legacy-v1 attestation or authorization
4. Only after genuine external approval exists,
   `verify_approval_overlay(observation, template, binding, approval_path,
   externally_trusted_raw_sha256, externally_trusted_canonical_sha256)` checks
   the single exact approval byte buffer, substitutes only the typed hash slots,
   and returns a detached `g0-prelaunch-overlay-observation-v3`. This receipt
   references both the closure observation and approval hashes and final argv.
   Its digest is not fed back into the proof or approval. It never executes argv

Approval-object hashing uses `target_approval_canonical`: sorted, compact,
ASCII-escaped JSON **plus one final LF**, matching published `support.canonical`.
Internal observation/binding-template canonicalization deliberately has no LF;
the two formats must not be mixed. A literal cross-contract test covers this.

The overlay is a mechanical binding receipt, **not an approval validator**. It
explicitly reports `approval_semantics_verified: false`. Approval content, scope,
nonce, source/environment identity, proof linkage, reservation, limits, and execution
eligibility still require the parent/target's independently reviewed gates.

There is only one optional dynamic exception: the exact path
`artifacts/research/assembly_m1_g0_v3_20261003/independent-execution-approval.json`.
It is JSON-only, maximum 64 KiB, under existing published directories, with purpose
`independently-pinned-approval-data`. It may be absent or contain one JSON object;
no new package/namespace directory or executable mode is permitted. Its mode may
be private `0600` or ordinary `0644`. Approval overlays and authority/request JSON
likewise accept `0600`; published source/runtime files retain their exact Git modes. Their mutable
bytes are excluded from the closure observation to avoid circular hashes. Their
exact bytes must be pinned through the detached approval overlay/target gates.
Create the actual authority files outside the source tree when possible. If
materializing an allowed file after initial checking, rerun the same prestart check
and hold the final state quiescent before launch.

## Trust boundary and explicit limits

This is a bounded static materialization checker for a trusted, quiescent POSIX
filesystem/environment. The independent authority controls the verifier binary and
stdlib, verified binding digest, complete native/startup review, source/environment
freeze, process ordering, and final command/env execution. It must keep them fixed
from checking through target completion, except declared approval-data delivery
before the last check. There is no hostile-filesystem sandbox, malicious-kernel or
concurrent-writer defense, inferred resource budget authority, or guarantee against
arbitrary later dynamic loading outside the independently reviewed catalog.

A stdlib Python checker cannot bootstrap trust in its own interpreter/stdlib or
prove that another process has not started. It must run under a separately trusted
supervisor before the target, outside target-controlled import paths. Production
use must not accept an observation produced by an untrusted checker. Neither a
local commit label nor a caller-calculated digest authenticates publication.

The `bindings` digest fields are format-checked and recorded, not reconstructed
from the scientific descriptor/freeze by this standalone checker. Independent
review must establish their exact relations to the final source, object, origin,
and environment artifacts. Likewise `native_closure_review` is an authenticated
reference/digest in the external binding, not an artifact this checker opens or
verifies semantically. `startup_search_path` is cross-checked against inventoried
roots and explicit absence/exclusion rules, not discovered by executing the target.
A self-sufficient “complete closure independently proven” claim would overstate
this implementation. Final proof issuance must discharge these obligations.

Bounds: 64 MiB JSON, 200,000 files aggregate, 4 GiB aggregate bytes, 512 MiB per file,
64 relative path components, 16 runtime import roots, 4,096 separately cataloged
native/startup files. Bounds reject; they never silently truncate or skip entries.

The full SparkBrain test/readiness/demo/benchmark sequence was **not** run. These
focused, synthetic tests support the new checker only and make no scientific,
G0-success, approval, reservation, or integrated-environment claim. Publication,
final freeze construction, independent review and genuine prestart proof issuance
remain blocked on the final source/environment and separate execution authority.

## Repository integration paths

The intended public location is `scripts/g0_prelaunch/materialization_verifier.py`,
with the inventory and this README adjacent. Copy the test to
`tests/test_g0_prelaunch_verifier.py` and change its `BASE` definition to
`Path(__file__).absolute().parents[1] / "scripts" / "g0_prelaunch"`.
The standalone test here uses its adjacent checker. All synthetic fixture
files are created in `tempfile.TemporaryDirectory` under the system's temporary
directory (honoring a configured validation TMPDIR), never under published source.
They are cleaned up after each test. No verifier behavior changes are needed.
