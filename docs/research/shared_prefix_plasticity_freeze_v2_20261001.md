# Prospective source-freeze v2 corrections (2026-10-01)

Status: **SOURCE FIXES FOR REVIEW / UNEXECUTED / ZERO SCIENTIFIC CREDIT**.

The first package remains at published commit
`8a7cd002d7b3242b3f022d7c4be69044b8899632` (PR173). Its `freeze/` and
`preparation-validation.json` files are preserved unchanged. These corrections
address two pre-execution P1 comments:

- https://github.com/salmonmikan/sparkbrain_research/pull/173#discussion_r4159897207
- https://github.com/salmonmikan/sparkbrain_research/pull/173#discussion_r4159897217

No model construction, prefix, suffix, baseline or smoke trajectory has occurred.
Seeds, input-generation rules, four suffix branches, configurations, endpoint
definitions and the 768-pair maximum remain unchanged. A separately reviewed
`freeze-v2/` will be generated later. The published v1 freeze is not overwritten.

## Dependency-byte coverage

`-B` only disables bytecode writes. The inventory now includes every `.pyc` under
the configured stdlib, including `__pycache__` and standalone bytecode, alongside
`.py` and native-extension files. Site/dist packages remain excluded and forbidden
on the execution import path. Existing system files are neither removed nor
rewritten. The verifier rejects changed, added or removed inventoried bytecode.
This is a machine-specific file inventory, not a cryptographic full-machine
attestation. Kernel and transitive system shared-library coverage remain outside
its scope; it cannot retroactively authenticate interpreter/bootstrap code that
already executed before verification.

## Mandatory live-driver worker envelope

A direct worker command now fails without an inherited anonymous supervisor pipe.
The driver emits one bounded envelope binding the exact job digest, worker path,
output root, parent PID/start identity and CPU/wall allowances. The worker requires:

1. Both `SHARED_PREFIX_OUTPUT_ROOT` and `SPARK_PROBE_OUTPUT_ROOT` resolve to the
   frozen output root before any worker write, source gate or model construction
2. An inherited FIFO descriptor and a complete, bounded, one-shot envelope
3. The real OS parent process uses the same Python executable and this runner's
   `run` entry point with `-S -P -B`, targeting the frozen output root
4. The live parent PID/start identity matches the envelope and the real parent
   holds the write side of the same pipe
5. Linux parent-death SIGKILL is installed, followed by a race-closing identity
   recheck. The worker checks parent identity and pipe liveness before transitions
   and writes. The driver retains wait4 accounting and global supervision

The driver holds the pipe writer open until the worker has terminated. Missing,
closed, substituted or extra-data supervision channels fail closed. This is
process/liveness enforcement inside the local Linux harness, not protection
against a malicious OS or arbitrary same-account process memory modification.

Workers no longer accept a job-supplied absolute wall deadline. Their allowance
comes from the inherited supervisor envelope, must match the bounded job values,
and is independently clipped to at most119 CPU/179 wall seconds, with startup
CPU subtracted and remaining supervisor wall time applied. The inherited outer
120/180-second inclusive trajectory budget retains its existing one-second
headroom; prefix costs further reduce suffix allowance. Arbitrary future job
deadlines, nonfinite numbers, overlarge limits and expired supervisor windows are
rejected before dynamics. The driver still owns the global timer, output-byte
accounting, exact reservation order, prefix eligibility gates and terminal-attempt
policy. No unsupervised worker can make the two output-bound helpers optional.

The driver initializes absent cap-root variables but rejects conflicting ones;
workers require them already present and correct. Pure/synthetic tests cover
bytecode inventory/tampering, missing/mismatched roots, missing/dead supervision,
wrong parent commands, envelope/job substitutions and inflated deadlines without
constructing any model or running any trajectory. OS signal installation is
mocked in the synthetic tests; no prospective runtime smoke test is added.

The optional `pythonXY.zip` entry already permitted on the import path is now
bound explicitly: the dependency inventory records its path, absence/presence
and content hash when present. Creation of a previously absent zip, removal or
byte changes invalidate verification; a non-file zip path is rejected.

Before production imports, execution rejects non-null `sys.pycache_prefix`, any
`sys._xoptions`, optimized interpreter mode, `ignore_environment` and `isolated`
flags. In particular `-E`/`-I` cannot pass merely because the environment still
contains `PYTHONHASHSEED=0`; these flags ignore that setting. No alternate cache
root or unbound `-X` mode is accepted. Pure tests cover each rejected setting and
the ordinary unoptimized invocation. These checks do not broaden the inventory
into full-machine attestation.
