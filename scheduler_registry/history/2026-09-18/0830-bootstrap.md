# SparkBrain scheduler registry bootstrap

- registry boundary: 2026-09-18 JST
- event: `BOOTSTRAP`
- fleet size: 7 enabled SparkBrain schedulers
- source of truth inspected: live ChatGPT automation definitions
- historical limitation: prior scheduler-definition versions are not exposed by the currently available ChatGPT scheduler interface and are therefore not reconstructed.

## Current fleet captured

| Task | Task ID | Current snapshot commit |
|---|---|---|
| SparkBrain Control & Repository Steward | `6aa9184960d4819192c8de1d9b22c1d9` | `ffddf0edb4b4761831355a4e4a2337602140f9b3` |
| SparkBrain Evidence Analyst | `6aa893eab4748191bd98de5e490739ce` | `78bffcb1c7537d6ef9658d9b26e76c1ba13deeff` |
| SparkBrain Research Orchestrator | `6aa35e5370bc8191888926c2457a2b7f` | `03e34a6ec1c2a23d77d25bfc83a3b7679b7c7364` |
| SparkBrain Research Orchestrator Relay | `6aaba7c85034819198e3b91eb58556d0` | `a7921fa0e8c72fd0139690db5cd47d07baba41cf` |
| SparkBrain Research Orchestrator Sub | `6aaa08248794819180e6627ef2a9b5fc` | `bd8a5f5abe98a3051593ce1f4be596d4bac62604` |
| SparkBrain External Research & Audit | `6aa9b43ec5288191bc12c59cb5ae1e99` | `d66b1ca2a2036364e1f6daff9efc0d1d1c3a8815` |
| SparkBrain 現在状態ブリーフ | `6aa9543b594c8191b44e2356a34719c1` | `e3c4a43259f6714ec2392dfb847f44c431f39715` |

The exact current title, enabled state, timing mode, timezone, iCal schedule, and prompt are stored under `scheduler_registry/current/<task-id>.md`.

## Existing history that is *not* scheduler-definition history

The programme already preserves substantial run/output history under control-plane branches such as:

- `ops/control-brain-handoff`
- `ops/evidence-analyst-handoff`
- `ops/orchestrator-run-report`
- `ops/external-research-audit-handoff`
- `ops/repository-steward`

Those records describe what scheduled workers did. They do not form a reliable version ledger of the ChatGPT task prompt/schedule definitions themselves.

## Partial legacy clues

Disabled one-time scheduler-sync automations and past conversations contain partial evidence of older scheduler changes. They are intentionally not promoted to a complete reconstructed history because they do not provide a guaranteed exact before/after definition for every mutation.

From this bootstrap onward, scheduler mutations must be recorded transactionally.
