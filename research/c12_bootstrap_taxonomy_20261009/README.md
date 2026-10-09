# C12 bounded mapping taxonomy, isolated source-only candidate r4

Prepared from c12-bootstrap-diagnostic-r3-20261009T1335Z. Existing candidates and
published sources were not modified. The original source candidate was prepared without execution. Independent evidence
now records nine fresh pure/mock tests passing in 0.033 seconds. No collector,
supervisor, target runtime, native or scientific code was executed for this candidate.
No job is allocated; two future CI allowances remain unreserved and unconsumed.

Only capture.py changes operationally. Its original limits, checked_path,
collect(), runtime target, roots, scope arguments, rejection order, file set,
symlink policy and no-retry rule are retained. supervise.py remains byte-identical. This separate publication candidate refreshes
only the workflow identity, source paths, exact capture hash, and branch-only
CI exclusions for one prospective same-scope observation. No trusted runtime
pin is updated. Publication and execution remain held for parent review.
The checkpoint remains a single overwritten latest record.

mapping_taxonomy receives only the existing split(None, 5) maps fields. It adds:
- mapping_namespace: DEVICE_NAMESPACE for exact /dev or descendants;
  SYSTEM_LOCALE_NAMESPACE for exact /usr/lib/locale or descendants;
  NORMAL_ABSOLUTE for all remaining slash-prefixed names. The helper returns
  null for nonabsolute/absent names, which never reach mapped admission.
- mapping_deleted_suffix: true only for the literal terminal ' (deleted)'.
- mapping_inode_zero: boolean for 1..32 ASCII decimal digits, otherwise null.
- mapping_device_zero: boolean for two 1..16 ASCII hexadecimal components and
  one colon (maximum 33 characters total), otherwise null.
- mapping_metadata_valid: boolean conjunction of those metadata validations.

All output is finite; no pathname, basename, address, permission, offset, raw
inode/device identifier or exception payload is added. Bounded strings are
scanned without integer conversion. No target stat/open/read is introduced.
Fields are attached before the original checked_path call. The displayed path
is not stripped, normalized, resolved or altered for admission.

Interpretation: namespace and suffix labels describe text, not kernel file type,
regular-file status, deletion fact, harmlessness or executable significance.
SYSTEM_LOCALE_NAMESPACE is a lexical hypothesis only, never an admitted root.
FILE_BACKED_MAPPING is the inherited role name for absolute-name candidates;
it does not verify regular-file backing. Even /usr/lib/locale/../private is
lexically locale-like, while the unchanged noncanonical check rejects it.
Existing mapped library-name classification is unchanged, including deleted
suffixes. Malformed metadata never repairs or replaces original rejection.

Verification status: source reviewed and nine fresh pure/mock tests passed in a
separate evidence directory. No tests are repeated for publication preparation. The test source extracts only
five reviewed definitions via AST into a synthetic namespace; it does not import
capture.py or call collect()/supervisor. No actual /proc access is allowed.
Full original tests are not invoked. No runtime-admission credit is earned.
