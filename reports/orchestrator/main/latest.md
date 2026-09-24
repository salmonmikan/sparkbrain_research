# MAIN PRIMARY R137

schema_version: 2
generation_id: MAIN-20260925T061700+0900-PRIMARY-R137-SB001-ENTITY-BOUNDARY-WAITING-CI
generated_at: 2026-09-25T06:17:00+09:00
mode: SYSTEM_BUILD
status: WAITING_EXTERNAL

Evidence Analyst R133 explicitly continues `BUILD-SB-001-PREDICTIVE-STATE-REVISION-PILOT` for acceptance closure only. Stable source remains `main@d16403414fc7abebd23075fc401240971b8eb91d`.

MAIN closed the remaining generic entity-style privileged-input gap by rejecting `entity`, `entity_id`, `entity_key`, and `entity_slot` in observation channels and recursively nested metadata, while preserving the existing explicit `entity_hint` rejection. Dedicated negative tests were expanded accordingly.

Build branch: `system-build/sb001-predictive-state-revision-pilot-20260925@5b86dfa6cad634312c81e579e5339b3b47cef6e0`.
Exact-head CI: run `36060329063`, currently in progress.

No protected integration PR was opened because acceptance closure is not claimed before exact-head CI. No Forge code was reused; delayed-action-credit remains deferred/not admitted. No scientific execution, rerun, retune, rescore, scoring, protected target access, or scientific-ref mutation occurred.

Built: yes. Prior bounded core functionally verified: yes. New entity-boundary hardening exact-head verified: pending CI. Comparatively supported: no. Scientifically novel: no.

Next: recheck CI run 36060329063. On success, re-audit R133 acceptance closure and only then proceed to the protected integration PR path. On failure, repair science-invariantly only.

Full record: `reports/orchestrator/main/history/2026-09-25/0617-r137-sb001-entity-boundary-waiting-ci.md`.
