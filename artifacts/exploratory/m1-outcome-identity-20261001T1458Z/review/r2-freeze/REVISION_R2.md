# R2 tooling correction, frozen before corrected execution

This is a fresh exploratory attempt following an environment-packaging failure, not a
FORMAL rerun or concealed budget reset. The first frozen attempt and every raw/checkpoint
byte remain unchanged in ../freeze and ../run1. Original freeze SHA-256:
c7f81d594765d93949730fa188335d84f4f3133d90773b2f676453ab510c80b8.

The original source archive omitted the repository-relative schemas required by v03
trace validation. Consequently every observation failed before successful processing,
all outcomes lacked a pending observation, and zero outcomes committed. Its fixed
budget was 32 observations plus 32 outcome deliveries. No primary identity-boundary
result was exposed. The original verifier failed when dereferencing the absent probe
action. These failures remain reportable; the corrected attempt does not replace them.

Corrections only:
- Include unchanged schemas from source commit 3cb955cd42474b36d2d37617e5390d08656c06f1
- Make the read-only verifier handle failed probe observations without dereferencing None
- Add a regression test for the retained failed attempt and static schema dependency checks
- Correct environment metadata to record jsonschema and its installed dependency versions
- Use fresh task-local r2 event and receipt IDs; all scalar/time/arm/default parameters stay fixed

The parent explicitly authorized this science-invariant correction on 2026-10-01 UTC.
No scientific identity, runtime implementation, threshold or outcome-dependent choice changes.
Development repair is consistent with the active non-evidentiary development/integrity policy.

Prospective corrected budget: one eight-case primary process, followed by one fresh-process
reproduction with PYTHONHASHSEED=37, 32 observations and 32 outcome deliveries in each.
Including the preserved first packaging attempt, the total budget is therefore 96 observation
attempts plus 96 outcome-delivery attempts. Count committed work separately. Do not execute
the missing original reproduction. No Session.cycle execution or expanded matrix is added.

All prior interpretation and no-publication/no-runtime-edit boundaries remain in force.
