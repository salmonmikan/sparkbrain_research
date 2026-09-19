# APPLIED — Utility request-bus write exceptions

- timestamp: 2026-09-19T17:01:30+09:00
- status: APPLIED
- pre_change: `scheduler_registry/history/2026-09-19/165700-utility-request-writers-PRE_CHANGE.md`

Fixed-role schedulers now have a narrowly scoped exception allowing creation of append-only Utility request files. Requests are proposals only and cannot change assignments or grant authority.

## Final live definitions

- Evidence Analyst: `2026-09-19T07:55:30.664683Z`
- MAIN: `2026-09-19T07:56:00.500001Z`
- SUB: `2026-09-19T07:56:20.409575Z`
- Relay: `2026-09-19T07:56:41.511882Z`
- External Research & Audit: `2026-09-19T07:57:21.240129Z`
- Methodology Calibration Auditor: `2026-09-19T07:59:06.534973Z`
- Current State Brief: `2026-09-19T07:59:13.912538Z`
- Utility Orchestrator follow-up requests are already authorized by its own registered prompt.
- Control/Steward scheduler owns request adjudication/assignment authority.

No existing schedule was changed by this request-writer update.
