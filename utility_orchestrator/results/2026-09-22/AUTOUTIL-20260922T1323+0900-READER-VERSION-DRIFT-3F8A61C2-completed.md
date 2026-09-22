# Utility autonomous task completed — stable-main reader version drift

- schema_version: `2`
- autonomous_task_id: `AUTOUTIL-20260922T1323+0900-READER-VERSION-DRIFT-3F8A61C2`
- assignment_mode: `AUTONOMOUS_IDLE`
- status: `COMPLETED`
- run_count / max_runs: `1 / 1`
- evidentiary_status: `NON_EVIDENTIARY`
- scientific_authority: `NONE`
- outcome_classification: `READER_NAVIGATION_DRIFT_CONFIRMED_ROOT_DISTRIBUTION_VERSION_MIGRATION_UNDERDETERMINED`

## Exact authority / ownership inputs

- assignment pointer: schema-v2 clean `IDLE`, active assignment/generation both null, blob `6fe8c6da7192a3021eea9e2c4a94b1a1251e6da7`.
- Evidence Analyst: `EVA-20260922T130900+0900-R62-D4A7C21F@d93bfe4ac1d4ed752fa8ca1074b1794a69d08682`.
- MAIN/Relay: `MAIN-20260922T125400+0900-RELAY-H7-DEVR1-ARCH-C2-C7F421A9@8d9479100cb0df994efd33ac2d53670b809bf40a`, BLOCKED before the R62 versioned DEV-R2 continuation.
- SUB: `SUB-20260922T125100+0900-QFD-R61-ZERORETAIN-C7F421A9@e56c285996c30888ec7f914efc505974695a6ed0`, zero retained and independent-idle after its bounded scan.
- Control: `CTRL-20260922T124800+0900-R33-E7C421B6@c41db58a5cc87e5460f143ce07c4256d7238d577`.
- Repository Steward: G9 `a3ab4f4f70c4782e7ff916838c33a64eb0a9c2dd`; no fresh review surfaced.
- authoritative stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`.

No ownership generation materially superseded this bounded read-only task. The active H7 scientific path was not touched and Utility did not become a MAIN dependency.

## Reconciliation result

The reader/navigation drift is real, but the package-version interpretation is more nuanced than a simple stale `pyproject.toml`.

Stable main simultaneously contains:

1. Root distribution / legacy-current reader surfaces at `0.3.2.dev0`:
   - `README.md@de76e99c1d9eefae3dc66ae77f46dbea0a11b4f8`
   - `docs/START_HERE.md@706e827b68a4f593024c513349c6809997b98177`
   - `pyproject.toml@49d47f3d65f67f1c0a6b82a3f7fc2d0364e2a88c`
   - root `src/sparkbrain/__init__.py` declares `0.3.2.dev0`
   - `RELEASE_METADATA.json@ad67d280478a57250d26418bd2c24ab7fe85fd21` records package version `0.3.2.dev0`
   - `scripts/local_readiness_check.py@7907c6c8f992d11d40363462dabc919bbc33044c` explicitly requires package version `0.3.2.dev0`.

2. A versioned v0.4 research namespace/spec at `0.4.0.dev0`.

3. A versioned v0.5 research namespace/spec at `0.5.0.dev0`:
   - `docs/THEORY_SPEC_v0.5.md@c1d3dbd041476428a103324b58616d3cc6534885` declares package target `0.5.0.dev0`.
   - `src/sparkbrain/v05/__init__.py@bb45b132bbd4d8ad203911ad46eafffdf63820c4` declares namespace version `0.5.0.dev0`.
   - `configs/v05_reference.json` also declares `0.5.0.dev0`.
   - `docs/V05_MASTER_PLAN.md@0812069c4e19d8a25364ff8476870b770cee15c9` describes the v0.5 research/implementation line.

Therefore:

- `README.md` and `docs/START_HERE.md` are demonstrably stale as current reader/navigation surfaces because they direct a new reader through v0.3 while v0.4/v0.5 research specifications and implementation namespaces coexist on the same authoritative main.
- `pyproject.toml version = 0.3.2.dev0` is not safely classifiable as a one-line stale-value defect. The same root-version assumption is enforced by root `__version__`, local readiness, release metadata/generator semantics, package-content documentation, and existing v0.3 release machinery while v04/v05 expose their own namespace versions.
- An autonomous `0.3.2.dev0 -> 0.5.0.dev0` root bump would therefore collapse two currently distinct concepts — root distribution version and research namespace/spec version — without a reviewed version-semantics decision.

## Smallest safe follow-up boundary

Fresh Repository Steward review should first decide the intended version model:

- If the root distribution intentionally remains `0.3.2.dev0`, perform a small reviewed reader-surface refresh that explicitly distinguishes root distribution version from current v0.4/v0.5 research namespaces/specs and links the newer theory/implementation surfaces.
- If the root distribution is intended to migrate to `0.5.0.dev0`, treat it as a coordinated package/release contract migration covering at minimum `pyproject.toml`, root `sparkbrain.__version__`, local-readiness expected version, release metadata/generator semantics, package-content/reader docs, and their tests. Do not implement it as a single metadata edit.

No new Utility request was appended because Control R33 already marks this issue `PENDING_STEWARD_AUDIT`; duplicating that route would add mailbox churn rather than information gain.

## Integrity / Funnel preservation

- no scientific workflow or experiment
- no outcome-bearing measurement
- no source, docs, package, release, research, or workflow mutation
- no candidate/Funnel typing or readiness change
- no PRE_FORMAL or FORMAL action
- no scheduler mutation
- no protected/frozen/evidence/control/preserve ref mutation
- no research merge or promotion approval
- no consumed identity target
- no theory-backward / Discovery / readiness / promotion credit
- candidate touched: `false`

Stop reason: `COMPLETED_BOUNDED_READER_VERSION_SEMANTICS_RECONCILIATION`.
