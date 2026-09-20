# APPLIED — generation/freshness contract v1 + Utility lifecycle v1

- timestamp_jst: 2026-09-20T10:34:00+09:00
- status: APPLIED
- pre_change_commit: `336c23f1b296bbe48e7b60323c475feccca4fbaa`
- before_snapshot_commit: `edc480e26ee55f6b305228eaae38107f7851e07d`
- utility_lifecycle_repo_commit: `d4d0f75f1a57df1298e49e67448158ab12a2754f`
- manifest_commit: `5829ca58819f05649a3d15a67911539f4adc8994`
- live_tasks_updated: 9
- schedules_changed: false
- enabled_states_changed: false
- scientific_authority_change: false
- formal_integrity_change: false

All nine active SparkBrain scheduler prompts now use role-appropriate generation/freshness v1 semantics. Control and Utility also use Utility assignment lifecycle v1 with Control-owned assignment generations and compare-and-swap terminal closure.

Post-change live verification confirmed the nine requested schedules and enabled states remained unchanged. Registry drift now ignores volatile execution timestamps and keys off stable-definition fields only. The current-definition files and manifest contain the applied prompts and stable-definition fingerprints.

Utility's prior terminal assignment `CTRL-20260920-0650-SUPPRESSION-STATIC-DETECTOR-CONSISTENCY` was archived under lifecycle v1 and `assignment/current.md` was migrated to a schema-v2 IDLE pointer using the explicit legacy-terminal bootstrap path. No scientific result or immutable evidence was changed.
