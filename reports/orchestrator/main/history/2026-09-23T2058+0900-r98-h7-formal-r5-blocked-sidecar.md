# MAIN history — R98 H7 FORMAL R5 pre-start fail-closed

- schema_version: `2`
- generation: `MAIN-20260923T205800+0900-PRIMARY-H7-FORMAL-R5-R98-BLOCKED-SIDECAR`
- candidate: `CAND-H7-RESPONSIBILITY`
- layer: `FORMAL`
- phase/revision: `RESULT_EXPOSED_DEVELOPMENT / H7-FORMAL-R5-CONTENT-ADDRESSED-RUNTIME-IDENTITY-AND-PROVISIONING-PROVENANCE-SPLIT`
- cycle: `12`
- Analyst: `EVA-20260923T200231+0900-R98-2B6F91C4`
- scientific source: `research/main-h7-formal-r5-runtime-identity-r88-cycle12@2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`
- repaired controller: `research/main-h7-r5-oneway-controller-r98@f21dc7521af7413adcc46a2561271e0b8852f371`

R98 prospectively authorized exactly one fresh untouched H7 R5 FORMAL identity under unchanged R5 with preserve-raw-before-read/score and pre-start fail-closed requirements.

MAIN applied two controller-only `SCIENCE_INVARIANT_REPAIR`s: first, enabled the NON_RESULT readiness workflow on its canonical controller branch; second, fixed nested-checkout workspace-path plumbing after the first readiness run failed at the exact preidentity validation. No scientific source or contract field changed.

First readiness run `35856825277` was non-result-bearing and failed at preidentity validation. Repaired readiness run `35857110884` passed authority freshness, untouched H7 namespaces, exact R5 contract/component blobs, locked runtime recreation and exact non-result preidentity validation. Generic CI `35857110749` also succeeded on the repaired head.

The repaired readiness run then failed at `Assert protected sidecar handoff capability exists without exposing it`. The prospectively fixed gate requires concealed repository Actions secret `H7_R5_SIDECAR_PASSPHRASE` to be present and at least 32 characters. The connected GitHub capability has no repository Actions secret read/write operation, so MAIN cannot provision or inspect the secret and cannot lawfully bypass the gate.

Scientific/evidentiary status remains `NON_EVIDENTIARY_FORMAL_PREIDENTITY_READINESS_ONLY`: no fresh FORMAL identity, no STARTED, no concealed evaluation access, no official raw output, no scientific preserve, no target-side read, no official scoring and no evidence mutation. Prior results and 7 previously consumed official identities remain unchanged. H7 itself remains unconsumed. Fast Forge code/observations were not reused.

Stop: `FAIL_CLOSED_PRESTART_PROTECTED_SIDECAR_CAPABILITY`.

Next: provision/correct the concealed repository Actions secret `H7_R5_SIDECAR_PASSPHRASE` to satisfy the existing >=32-character gate. Then re-fetch fresh Analyst authority and every H7 one-way namespace and rerun only the NON_RESULT readiness gate. Start exactly one fresh FORMAL identity only after all prospective checks are green and unchanged.
