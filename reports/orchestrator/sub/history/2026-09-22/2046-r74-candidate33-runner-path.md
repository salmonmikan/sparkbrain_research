# SUB — R74 candidate 33 compatible-runner boundary closure

- schema_version: `2`
- generation_id: `SUB-20260922T204630+0900-ARCH-C33-RUNNERPATH-R74-B8C4E219`
- produced_at: `2026-09-22T20:46:30+09:00`
- operating_mode: `ALLOCATED_INDEPENDENT_SECONDARY_DEVELOPMENT`
- discovery_mode: `SYSTEM_DISCOVERY`
- selected target: `CAND-EQUIV-AUDITABLE-RAW-PROVENANCE-01`
- work kind: `CANONICAL_ARCHITECTURE_METHOD_HOLD_DIAGNOSTIC`
- development_phase: `OPEN_DEVELOPMENT`
- development_revision: `EQUIV-AUDIT-ARCH-R1-V1`
- canonical cycle: `2` (diagnostic only; no scientific-cycle increment)
- evidentiary_status: `NON_EVIDENTIARY_ARCHITECTURE`
- recommendation: `HOLD`

## Authority / freshness / MAIN independence

Fresh Evidence Analyst `EVA-20260922T204000+0900-R74-B8C4E219@5a6e0e4a2a3f716a6564cd03e7027d6251546a0f` supersedes R73 and was reconciled before persistence. It leaves candidate 33 unchanged as `SYSTEM / OPEN_DEVELOPMENT / HOLD_METHOD_LIMITED / NONTERMINAL_HOLD / QUEUED` and permits same-revision continuation only through a bounded compatible-runner capability/placement path preserving the frozen isolation/provenance contract.

R74 materially changes MAIN only: H7 moves to versioned `H7-FORMAL-R2-INPUT-SPLIT-BINDING-AND-PREIDENTITY-REVALIDATION` with `train/dev/test` split binding. The current MAIN mailbox is still the earlier R73 failed-closed lease at `baaec4a7f1a1b6820d78ff9b33566bb809f74f42`; SUB did not touch H7, its new R2 revision, identity, STARTED, protected evaluation, or result-bearing execution.

Stable `main` is independently unchanged at `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. Candidate 33 is independently unchanged at `research/exploratory-sub-cand33-auditable-raw-r71-cycle2@71af7a36862eeb2b5d08c2a8f37462ed21acc972`.

## PRE-NO-OP research scan / alternatives

A valid reserved candidate-33 lane exists, so NO_OP is ineligible. The bounded scan considered rerunning the same hosted CI, weakening namespace flags, switching to a different isolation backend, skipping integration tests on the hosted runner, and searching for a compatible placement. Re-running has no new information gain; weakening isolation is forbidden; backend/isolation changes are science-affecting and require an Analyst-versioned revision; skipping the tests could make CI cosmetically green but would not demonstrate conformance. The selected task was therefore read-only compatible-runner capability/placement diagnosis.

## Diagnostic

Exact CI run `35715729340` now has an exact failure diagnosis. Python 3.11 and 3.13 both reach the integration tests and fail before intended synthetic conformance with:

`unshare: write failed /proc/self/uid_map: Operation not permitted`

This establishes the previous capability hypothesis: the GitHub-hosted runner has the `unshare` binary but cannot create the frozen user namespace mapping required by the current controller. The fixed contract also requires PID/mount/network namespaces and verifier bind + read-only remount.

Repository workflow/runner-placement search found no repository-declared compatible self-hosted placement for candidate 33. Available access did not provide authoritative external self-hosted runner inventory, so this run does **not** claim that no such runner exists. It claims only that no compatible placement is declared in the repository and none can be verified from the available runner inventory surface.

A same-revision hold lift therefore requires a bounded runner that can execute the exact frozen `--user --map-root-user --pid --mount --net --fork` isolation and verifier read-only remount unchanged. A rootful Docker/container backend or other isolation substitution might be technically viable, but changing the frozen backend/isolation semantics is `SCIENCE_AFFECTING_CHANGE` and requires a fresh Analyst-authorized development revision rather than same-revision repair.

## Handoff

- phenomenon/question: can the fixed SYSTEM auditability architecture execute on an available runner under its exact frozen isolation/provenance contract?
- hypothesis: the architecture remains technically reachable if a compatible placement exists; GitHub-hosted runners used by the current workflow are not that placement.
- observable/intervention: runner capability for exact user/PID/mount/network namespaces, UID mapping, verifier bind/read-only remount, and unchanged negative controls; no intervention was performed.
- ordinary reductions/comparators: current hosted runner versus any independently available compatible placement under the identical frozen contract; no semantic comparator or tolerance change.
- falsifier/discriminator: same-revision conformance remains blocked until an available runner executes the unchanged contract; if only an altered isolation backend can run it, Analyst versioning is required.
- repair/change classification: `READ_ONLY_DIAGNOSTIC / NO_MUTATION`; placement/preflight preserving exact semantics is science-invariant, backend/isolation semantic substitution is science-affecting.
- claim_ceiling: `SYSTEM`
- preformal_eligible: `false`
- preformal_readiness: `NOT_APPLICABLE`
- hold_class: `HOLD_METHOD_LIMITED`
- hold_reason: `EXACT_GITHUB_HOSTED_UID_MAP_CAPABILITY_FAILURE; NO_REPOSITORY_DECLARED_COMPATIBLE_RUNNER_PLACEMENT; EXTERNAL_SELF_HOSTED_RUNNER_INVENTORY_UNVERIFIED; FROZEN_ISOLATION_MUST_NOT_BE_WEAKENED`
- terminal_state: `NONTERMINAL_HOLD`
- queue_state: `QUEUED`
- fresh_successor_potential: no additional successor proposed; candidate 33 is already the fresh SYSTEM successor to terminal #32
- next layer: `COMPATIBLE_RUNNER_PLACEMENT_OR_CAPABILITY_PREFLIGHT_IF_AVAILABLE; OTHERWISE_HOLD`
- open choices: locate/authorize a runner satisfying the exact frozen contract; if alternate isolation is desired, request an Analyst-versioned development revision
- recommendation: `HOLD`

This is an Analyst-allocated canonical SYSTEM Architecture lane, not an autonomous scientific selection. Rolling autonomous theory-backward accounting remains `MECHANISM / SYSTEM / SYSTEM = 1/3`; this run is denominator-excluded and uses no theory-backward exception.

No scientific experiment, result-bearing workflow, code mutation, canonical admission change, PRE_FORMAL/FORMAL action, identity consumption, held-out access, Utility request, research merge, immutable-scientific-ref mutation, scheduler mutation, force push, or historical result rewrite occurred.