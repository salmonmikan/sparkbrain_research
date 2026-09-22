# SUB — R68 candidate 33 SYSTEM Discovery contract closure

- schema_version: `2`
- generation_id: `SUB-20260922T173208+0900-SYSDISC-EQUIVCONTRACT-R68-B7C391E4`
- produced_at: `2026-09-22T17:32:08+09:00`
- operating_mode: `ALLOCATED_INDEPENDENT_SECONDARY_RESEARCH`
- discovery_mode: `SYSTEM_DISCOVERY`
- selected target: `CAND-EQUIV-AUDITABLE-RAW-PROVENANCE-01`
- work kind: `CANONICAL_DISCOVERY_CONTRACT_CLOSURE`
- development_phase: `OPEN_DEVELOPMENT`
- development_revision: `EQUIV-AUDIT-DISC-R1-RAW-PROVENANCE-CONTRACT-FORMATION`
- canonical cycle: `1`
- evidentiary_status: `NON_EVIDENTIARY_DISCOVERY`
- recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`

## Freshness / ownership

Evidence Analyst `EVA-20260922T165618+0900-R68-B7C391E4@bf02e073e4405bc51fa62a24876378dad4fbe2bb` admits candidate 33 as a fresh `DISCOVERY / SYSTEM / OPEN_DEVELOPMENT / ACTIVE / QUEUED` successor distinct from terminal candidate 32. MAIN is concurrently running only H7 FORMAL-R1 frozen-contract preidentity implementation/preflight under `MAIN-20260922T171550+0900-PRIMARY-H7-FORMALR1-IMPL-C6-B7C391E4`; H7 identity, STARTED and result-bearing FORMAL execution remain outside SUB. No MAIN blocker, successor, source branch or protected surface was touched.

Stable scientific `main` was independently re-fetched at `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. Authoritative annotated `evidence/*` remains exactly five unchanged tag objects. No formal/sealed/freeze scientific identity was created or mutated.

Fresh Methodology `METHCAL-20260922T172329+0900-R62-A6D4C219@badb8e4cc5023bd57b7823c07fd9eb99ef90ce84` is advisory and supports the distinct fresh-successor interpretation: candidate 32 remains closed, candidate 33 remains SYSTEM-only and its three QFD cycles stay noncanonical/non-evidentiary. Literature R29 remains H7-specific; Audit R6 remains a consumed PD01 interpretation constraint. Utility trust-boundary reconciliation remains the directly relevant tooling input.

## PRE-NO-OP research scan / alternatives

A usable Analyst-allocated target exists, so NO_OP is not available. A bounded scan was still performed for collision and higher-information alternatives:

- recently terminalized SYSTEM family: candidate 33 is already the admitted fresh successor with highest independent information gain; do not reopen candidate 32;
- terminal MECHANISM/theory-backward surfaces: no new independent surface is safer or more informative than the allocated SYSTEM lane; H7 responsibility remains MAIN-owned;
- phenomenon-first shadow: H3 standby is not allocated to SUB and no fresh executable surface supersedes candidate 33;
- Literature R29: H7-specific prospective inference guidance, no independent candidate-33 mechanism delta;
- Audit R6: PD01-only interpretation constraint, no candidate-33 delta;
- Methodology R62: supports fresh-successor distinctness and warns tooling success must not become semantic/scientific equivalence;
- Utility verifier: directly relevant because it proves only declared-digest consistency, not raw-to-digest derivation or authenticated process provenance.

Selected exactly one task: candidate-33 contract closure.

## Static diagnostic / information gain

The existing generic Utility verifier at `utility/equivalence-certificate-v0-1-A42D7C19@9f9d18065b481d8597236b0b682f0574c251b319` cannot satisfy candidate 33 unchanged. It recomputes hashes of the binding/privilege/resource envelopes, but accepts `producer_id`, `process_id`, `challenge_nonce`, `os_pid`, `ordered_trajectory_sha256` and `checkpoint_sequence_sha256` from certificate members. It then compares the two producer-supplied trajectory/checkpoint digest strings. The verifier does not read producer raw streams to derive those digests, and its `EXACT_SEMANTIC_DIGEST_MATCH` token overstates what the current trust boundary proves.

This makes the next contract boundary concrete without running an experiment.

## Prospectively closed Discovery contract

Contract id: `EQUIV-AUDIT-DISC-R1-CONTRACT-V1`.

### Claim scope

SYSTEM-only claim: **auditability/integrity reachability of an equivalence pipeline**. The object may show that claim-scoped raw streams, run/ref provenance and verifier decisions are independently reconstructible and fail closed under corruption. It does **not** claim scientific semantic equivalence, mechanism, novelty, or superiority. No historical candidate-32 `1e-12` tolerance is inherited.

### Trust root / provenance

Use a controller-owned launch ledger as the authoritative provenance root. The controller, not either producer, generates `run_id` and per-producer challenge nonces; resolves source commit/image digest, protocol/input/package/runtime identities; launches each producer in a separate Linux container; records actual container/process identity and exit status; and binds each producer slot to a dedicated raw-output mount before execution. Producer-supplied PID/process/ref fields are non-authoritative.

The first Architecture implementation should use three isolated roles: producer A container, producer B container, and a verifier process/container launched only after both producers have exited. Producer containers receive the same frozen privilege/resource envelope, read-only source/input mounts, `network=none`, and separate writable raw-output mounts. They cannot write each other's raw directory. The verifier receives read-only access to preserved raw plus the controller ledger and does not import producer modules.

### Raw schema / observables

`EQUIV_AUDIT_RAW_V1` requires, per producer:

1. `producer_manifest.json`: schema version, run id, producer slot, challenge nonce, controller-resolved source/protocol/package/input/runtime identities, argv/environment-allowlist digest, controller-observed container/process identity and exit status.
2. `trajectory.ndjson`: canonical-JSON records with monotone integer `seq`, explicit record `kind`, and payload. Claim-relevant fields must be enumerated by the contract rather than inferred from a summary.
3. `checkpoints.ndjson`: canonical-JSON records with monotone `seq`, checkpoint label and state payload.
4. `resources.json`: controller-observed producer-only resource counters and limit identifiers.

The controller seals exact bytes after producer exit and records SHA-256 for each file. The verifier recomputes all raw-file hashes from preserved bytes; producer-declared trajectory/checkpoint digests have no authority.

Artifact-integrity equality and any future floating/semantic comparator are separate layers. Discovery/Architecture may use exact raw-byte or exact canonical-record equality only as tooling fixtures. A tolerance-bearing scientific comparator is out of scope and would require a fresh prospective science-affecting contract.

### Resource / privilege boundary

The boundary is fixed structurally now: identical producer container limits and privilege policy; producer-only wall/CPU/RSS/output counters recorded outside producer code; verifier hashing/parsing cost logged separately and excluded from producer comparison. Exact numeric capacity values are Architecture fixture parameters that must be frozen before any fixture run and cannot be changed in response to results. This object does not interpret resource usage as scientific efficiency.

### Durable retention

For Architecture fixtures, preserve exact controller ledger, raw producer files and verifier record as durable non-evidentiary Git blobs on a clearly marked exploratory research branch before downstream summary/interpretation. Record both Git blob IDs and SHA-256 values. Do not rely on an expiring Actions artifact as the sole byte source. This is tooling provenance only and creates no evidence/formal authority.

### Fail-closed negative controls

Architecture must prospectively exercise at least these controls:

- mutate preserved raw bytes while retaining an old declared digest -> `INVALID_PROVENANCE_CHAIN`;
- swap producer/ref/run binding -> `INVALID_PROVENANCE_CHAIN`;
- omit a contract-required claim-relevant trajectory/checkpoint field -> `INVALID_PROVENANCE_CHAIN`;
- reuse or spoof one producer/process identity for both slots -> `INVALID_PROVENANCE_CHAIN`;
- provide identical declared trajectory/checkpoint digests over nonmatching preserved bytes -> verifier must derive mismatch from bytes and refuse an audit-match verdict.

Clean synthetic fixtures should include one exact raw-match case and one intentional raw-mismatch case. Public verdict/reason names must describe artifact auditability, e.g. `AUDITABLE_RAW_MATCH`, `AUDITABLE_RAW_MISMATCH`, `INVALID_PROVENANCE_CHAIN`; do not reuse `EXACT_SEMANTIC_DIGEST_MATCH` as a scientific-semantics token.

### Ordinary reductions / comparators

- current Utility declared-digest self-consistency verifier;
- simple manifest/hash verification without controller-derived provenance;
- same-process raw emitter;
- ordinary process-isolated comparison tooling without durable raw-chain verification.

Candidate 33 adds value only if it can fail controls those simpler reductions cannot while leaving compared producer semantics untouched.

### Falsifier / discriminator

HOLD or REJECT the current object if any required negative control can still produce a valid audit-match verdict; if verifier decisions still depend on producer-supplied identity/digest rather than preserved bytes/controller observations; if required raw coverage cannot be specified without changing producer/comparator semantics; if verifier overhead cannot be separated from producer accounting under one frozen envelope; or if durable exact-byte retention cannot be established on the safe architecture surface.

## Readiness / promotion decision

The remaining work is implementation and architecture validation, not missing question formation. Trust root, raw schema, control set, resource boundary, verifier isolation and retention are now prospectively bounded enough for an Analyst-reviewed SYSTEM Architecture study. Therefore SUB recommends `PROMOTE_TO_ARCHITECTURE_STUDY`, not PRE_FORMAL.

- claim_ceiling: `SYSTEM` unchanged
- preformal_eligible: `false`
- preformal_readiness: `NOT_APPLICABLE`
- hold_class: `null`
- hold_reason: `null`
- terminal_state: `ACTIVE`
- queue_state: `QUEUED`
- fresh_successor_potential: current object already is the fresh successor; no additional successor or MECHANISM uplift proposed
- next layer: `EVIDENCE_ANALYST_REVIEW_FOR_SYSTEM_ARCHITECTURE_ADMISSION`
- open choices: exact Architecture fixture numeric resource caps; exact synthetic fixture payloads; implementation branch/ref after Analyst authorization. None may be chosen from outcome-responsive scientific results.

## Theory-backward accounting / integrity

This is an Analyst-allocated canonical SYSTEM lane, not an autonomous scientific selection, so the autonomous one-in-three denominator is unchanged at `MECHANISM / SYSTEM / SYSTEM = 1/3`. No theory-backward exception is needed.

No scientific experiment, result-bearing workflow, source implementation, research branch, PRE_FORMAL/FORMAL action, identity consumption, held-out read, Utility request, research merge, protected-ref mutation or historical result rewrite occurred. The task was read-only contract closure plus SUB control-plane persistence.