# SparkBrain Repository Steward — Latest

- schema_version: `2`
- generation_id: `STEWARD-20260922T135014+0900-G10-4D8C21A7`
- produced_at: `2026-09-22T13:50:14+09:00`
- producer_run_id: `repository-steward-auto-20260922T135014+0900-G10-4D8C21A7`
- authority_scope: `REPOSITORY_GOVERNANCE_ONLY_NO_SCIENTIFIC_AUTHORITY`
- supersedes_generation_id: `STEWARD-20260922T075212+0900-G9-8C4E21D3`

Independent repository refresh keeps the authoritative substrate stable. `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d` is unchanged and unprotected; repository rulesets remain `0`; the five authoritative `evidence/*` refs remain annotated-tag objects at the same tag-object SHAs; thirteen legacy `freeze/*` branches remain present; tag-form `freeze/*`, `formal/*`, and `sealed/*` remain absent. The five evidence-family raw preserve branches were independently re-read at the same heads: H5 `ce5797eb584344db7a512e585506fb6c59ea475b`, NI01 `8a39cf70e397bb7588f948910f01ec58672ac814`, C19-v4 `d8fcc5216ff24940836972816cb0ec8f11e4ba06`, C19-R2 `3628694294a6eb33b18a0b42a56bb5ad77fe7b94`, and PD01 `65ae7a50ee2279ab5edc3ca43ea3bf69daecb881`. No immutable-ref incident is observed.

Fresh governance context is Control `CTRL-20260922T124800+0900-R33-E7C421B6`, Evidence Analyst `EVA-20260922T130900+0900-R62-D4A7C21F`, MAIN `MAIN-20260922T125400+0900-RELAY-H7-DEVR1-ARCH-C2-C7F421A9`, SUB `SUB-20260922T133738+0900-PRENOOP-R62-NOFRESHDELTA-6C8A21F4`, and Utility `UTILITY-20260922T133300+0900-AUTO-READER-VERSION-DRIFT-COMPLETED-3F8A61C2`.

Main/research/evidence separation remains healthy. Active H7 development is still isolated from `main` on `research/main-h7-dev-r1-claim-scoped-causal-contract-r60-cycle1`; compared with `main`, that branch is five commits ahead and zero behind and contains only H7 development contract/preflight/source/test additions. Exact research commit `c97af135742a7cd3af94c857f4d5b83d7707075d` records the cycle-2 preflight and explicitly stops on two science-affecting comparator-protocol gaps without result exposure or identity consumption. Analyst R62 has prospectively versioned the next scientific work as H7 DEV-R2, but no DEV-R2 research branch was present in the fresh SUB scan. H7 therefore is not a main-promotion candidate.

## HUMAN-20260922-006 reader/version audit

The reader-facing drift is real, but a root package-version bump is not governance-safe from present evidence. `pyproject.toml`, README, START_HERE, and RELEASE_METADATA all describe the root distribution as `0.3.2.dev0`. In the same stable `main`, `sparkbrain.v04` declares `0.4.0.dev0` and is explicitly documented as a development engineering layer rather than a public release, while `sparkbrain.v05` declares `0.5.0.dev0` and the v0.5 theory specification names `0.5.0.dev0` as its package target. This establishes additive v04/v05 development namespaces, but does not by itself establish that the root distribution/release contract has already migrated from 0.3.2 to 0.5.

The safe governance conclusion is therefore: do **not** change `pyproject.toml` or `RELEASE_METADATA.json` as an isolated fix. A small documentation-only main-promotion candidate is appropriate: refresh README and START_HERE navigation so they acknowledge the existing v0.4/v0.5 development research surfaces, clearly distinguish root distribution version from namespace/research-spec versions, and retain all existing scientific caveats. If project owners intend `0.5.0.dev0` to become the root distribution version, that should be a coordinated reviewed package/release-contract migration rather than a one-line version bump.

## Generic equivalence verifier review

Utility branch `utility/equivalence-certificate-v0-1-A42D7C19` is three commits ahead of `main`, zero behind, and changes only `src/sparkbrain/equivalence_certificate.py` and `tests/test_equivalence_certificate.py`. Exact head `9f9d18065b481d8597236b0b682f0574c251b319` has successful GitHub Actions checks on Python 3.11 and 3.13. The implementation is candidate-independent, fail-closed on schema/binding/envelope drift, and explicitly disclaims scientific authority.

However, direct main promotion is **deferred pending trust-boundary clarification**. The verifier checks equality of declared trajectory/checkpoint digests and rejects duplicate self-declared producer IDs/process IDs/nonces/PIDs, but it does not independently establish producer provenance, raw-to-digest derivation, or process isolation. In particular, `VALID_EQUIVALENT` and reason `EXACT_SEMANTIC_DIGEST_MATCH` could be misread as stronger than the code can establish. This branch is a valid reusable tooling candidate only if reviewed integration makes the boundary explicit (for example, certificate-internal exact declared-digest equivalence, not independent scientific/semantic equivalence) and does not let MAIN or Evidence Analyst treat it as trusted producer evidence without a separately authenticated producer/raw chain.

## Canonical governance tracking

Issue #139 remains the sole non-PR open Issue and correctly tracks the still-open authoritative-tag protection gap: canonical docs require server-side protection while repository rulesets remain zero. The prior legacy CX01 write-capable self-trigger pattern also remains because authoritative `main` is unchanged; it remains governance-only and currently self-disarmed by existing historical control/preserve refs.

PR #148 remains open/unmerged at `14ba187bb13705bc306baabe310d5364cf1b60fb` with three current unresolved review threads. PR #149 remains open/unmerged at `01ef8c3a54ff20403aba2fab9996dbda5552dd4d` with one current unresolved non-outdated thread plus one outdated unresolved thread. Both remain deferred; no merge is performed.

Main-promotion review now has two bounded governance/tooling candidates and zero active scientific candidates: (1) a documentation-only reader-navigation refresh for v0.4/v0.5 visibility, eligible for normal reviewed integration without changing package/release versions; and (2) the generic equivalence verifier, deferred until its trust boundary/naming is made unambiguous. Active H7 development remains research-only.

No experiment, research workflow dispatch, identity consumption, outcome reinterpretation, scientific lifecycle change, scientific freeze decision, research PR merge, scheduler mutation, ruleset/protection mutation, Issue mutation, workflow/main mutation, preserve/evidence mapping mutation, immutable-ref mutation, or main promotion was performed. Only designated Steward history/latest/state persistence is authorized for this run.
