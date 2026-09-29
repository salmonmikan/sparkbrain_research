# Evidence Analyst R170 — FLY-0 narrow observer admission + P0 R123 reconciliation

generation_id: EVA-20260929T175854+0900-R170-FLY0-NARROW-OBSERVER-P0-R123
generated_at: 2026-09-29T17:58:54+09:00
role: EVIDENCE_ANALYST
mode: READ_ONLY_ADJUDICATION
new_scientific_result: false
scientific_execution_authorized: false

## Freshness and persistence reconciliation

Main policy was re-fetched explicitly from `main@59fc994b39d0ba02682e972161bb46801592d25b`. Human Directive freshness is unchanged at `ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d` / active-index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`; there is no directive delta from durable R169.

Applicable directives re-read for this decision are HUMAN-20260925-002, HUMAN-20260926-003, HUMAN-20260926-004, HUMAN-20260927-002, HUMAN-20260928-001 and HUMAN-20260928-002.

Durable Analyst authority before this generation is R169 at `ops/evidence-analyst-handoff@95972cb31cb26d5994e506bfa46e6a11dc786a15`, with verified complete receipt `EA-R169-20260929T050453JST`. The request mailbox remains at `1deab7b4cc250e216b65831cb06c6b45b6421be2`; no newer Analyst request is durable.

Current append-only Control authority is R123 on `ops/control-brain-handoff@ccd58081057a94908d2775f45ca22bcc0fbeb0d6`. PRIMARY MAIN is R192; Methodology is R150; Theory is R22. Relay remains unallocated.

## Canonical science

Canonical science is unchanged: 35/35 terminal, 0 active, 0 queued and 8 consumed FORMAL identities. No FORMAL execution, rerun, retune, rescore, redispatch, immutable-evidence mutation or terminal reopen is authorized.

## M1 critical path

`BUILD-SB-M1-002-INTEGRATED-ROBUSTNESS-HARNESS` remains exact head `2a21d3e879f1db4e81a58273180ad2124e823a5e` over `main@59fc994b39d0ba02682e972161bb46801592d25b`, freshly compared 1 ahead / 0 behind. Exact-head CI run `36361950457` remains completed/success. Fresh PR search found no matching open PR.

Retain exact-head PR/conditional-merge authority. MAIN R192 exhausted its five-count PR-creation ceiling without a PR: counted attempt 1 reached the Code Mode orchestration tool-call ceiling with no PR on readback, and attempts 2-5 were explicit pre-GitHub platform refusals. No merge was attempted.

M1-002 remains built=true, bounded-functionally-verified=true, comparatively-supported=false, composition-contribution=NOT_ESTABLISHED, scientifically-novel=false and scientific-credit=0. The blocker remains the required PR-create path, not a new engineering defect or review gate.

## SB003 / FLY-0 engineering adjudication

`BUILD-SB-003-FLYLIKE-SENSORIMOTOR-PILOT` remains PRIMARY_MAIN / ALLOCATED_CONDITIONAL_INACTIVE under R169's unchanged activation conditions and rolling A/B/C contract. This generation does not bypass M1-002 integration or post-merge acceptance.

The FLY-0 intent-supersession guard is admitted as OPTIONAL preauthorized SYSTEM_BUILD hardening for SB003 A/B:
- exact source `8452bff9e1d0dc91c47c1d968f5ddcddd5335a22`;
- CI `36487505532` completed/success at that exact head;
- stale authority epoch/token frames fail closed before local execution without false local/bridge advance;
- mandatory gate=false; activation condition=false; scientific credit=0.

The FLY-0 observed-state summary is admitted only at its tested NARROW_OBSERVER scope as OPTIONAL preauthorized SYSTEM_BUILD input for SB003 B/C:
- validated exact head `1acc34b2a0bbfc623561dac114111b66a6b383a7`;
- CI `36503631615` completed/success at that exact head;
- realized local/WORLD outcome reporting rather than command echo;
- superseded-frame no-false-advance;
- one descending-cut command/outcome mismatch path;
- exact checkpoint/restore replay;
- common observer surface across structured, rewired, random-sparse and reactive variants.

This narrow admission reconciles Independent Audit R12's `SYNTHESIS_OK` classification for the current tested Forge scope. It does not establish the fuller Theory R22 outcome-receipt contract.

Theory R22 separates causal/transaction validity of a committed outcome from whether its source authority remains current for future control. If MAIN elects to rely on fuller receipt semantics, scoped engineering acceptance must cover commit-before-supersede, supersede-before-execution, exact source-frame/transaction/checkpoint binding, duplicate/out-of-order idempotence, feedback freshness/mask/delay provenance, ascending cut, replay and the common four-way interface. These requirements apply only to that fuller adopted scope; they are not M1 gates and do not change SB003 activation conditions.

The newer outcome-receipt-correlation prototype remains FORGE_PROTOTYPE_UNVERIFIED / NO_HANDOFF. Current Forge branch head is `3610032e897f70b0fc2b0e9ee9158fea88537c07`; its 17:35 append-only report records another five fresh-state attempts to land the R22 dual-validity source repair, all refused before GitHub. The source blob remains `ab83eae491145bb08447d2b9d0c61766c88aa24f`; no focused test or CI validates the fuller semantics.

## P0 reconciliation

P0 `INC-GITHUB-MUTATION-RECURRENCE-20260928-001` remains OPEN / root cause UNKNOWN.

Control R123 adds useful nonuniformity evidence. Utility demonstrated a STARTED create-file mutation succeeding on attempt 5 after four pre-GitHub refusals and a state update succeeding on attempt 4 after three refusals, both independently read back. In the same period, MAIN PR creation remained blocked and Forge's R22 source-update repair again failed 5/5 before GitHub.

Repository-wide write loss and a generic scheduled Contents-write outage remain unsupported. The best bounded classification is `NONUNIFORM_INTERMITTENT_PRE_GITHUB_MUTATION_REFUSAL_ACTION_PATH_PURPOSE_EXECUTION_CONTEXT_TIMING_SENSITIVE`. `create_pull_request` remains the strongest recurrent surface. Root cause remains UNKNOWN.

Moving-cache debt must not override append-only authority: Control append-only/latest are R123 while state is still R122; MAIN append-only/latest/state are R192 while lease remains R191. These cache lags do not change current M1/SB003 allocation.

## Methodology / claim boundary

Methodology R150 remains WELL_CALIBRATED. Mandatory SYSTEM_BUILD review remains a non-gate. The narrow observer admission is engineering reuse only; fuller R22 receipt hardening remains scoped if adopted.

All FLY-0 / SYSTEM_BUILD observations remain NON_EVIDENTIARY/NONCANONICAL with scientific credit 0. No biological fidelity/equivalence, topology necessity/superiority, compute/energy efficiency, composition contribution, whole-system superiority, external validity, rich goal-conditioned behavior or scientific novelty is established. No Revisit object is required.

## Disposition

- M1-002: GO under retained exact-head PR/conditional-merge authority.
- SB003: ALLOCATED_CONDITIONAL_INACTIVE; owner PRIMARY MAIN after unchanged activation conditions pass.
- FLY-0 intent-supersession guard: OPTIONAL_PREAUTHORIZED_SYSTEM_BUILD_HARDENING for A/B.
- FLY-0 observed-state: OPTIONAL_PREAUTHORIZED_NARROW_OBSERVER_SYSTEM_BUILD_INPUT for B/C.
- Full R22 receipt semantics: HOLD_FOR_SCOPED_ENGINEERING_ACCEPTANCE if adopted.
- Outcome-receipt-correlation prototype: UNVERIFIED / NO_HANDOFF.
- Relay: no allocation.
- Result-bearing science: STOP / no authority.
- Revisit: no new object.
