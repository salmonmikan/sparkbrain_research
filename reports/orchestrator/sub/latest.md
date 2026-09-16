# SparkBrain Research Orchestrator — SUB latest

Timestamp: `2026-09-17T02:58:09+09:00`

Evidence Analyst authority: `53a1a3cd9dc8b1c657ff056f517278cf3c0b4d00`.

## MAIN frontier avoided

MAIN remains on C19-v2 readiness at `research/c19-truth-free-symbolic-adapter-v2-20260917@7ede1bfb41285ec0107136b4f6abd5e893adcacf`, with the exact package already at `PRE_START_READY_FOR_ADMISSION`. SUB did not touch the C19 branch, protocol `c19-external-v2`, adapter contract `c19-belief-r-truth-free-symbolic-adapter-v1`, planned official identity `c19-external-v2-official-v1`, official Belief-R data, or any MAIN blocker. The Analyst split remains valid.

## Independent SUB work selected and completed

The reserved lane was the generic terminal-provenance accounting v2 prototype (`independent_of_main_critical_path=true`, `execution_allowed=false`). SUB created `research/methods-terminal-provenance-v2-sub-20260917` from the completed prior SUB audit `e127c3989780ebd5a78b8db914d4d6271920497e` and completed it at exact head `d5317485a591439cb52d52b649b4930964cf2b3a`.

The branch adds only three files relative to that base:

- `src/sparkbrain/evaluation/terminal_provenance.py`
- `tests/test_terminal_provenance.py`
- `docs/TERMINAL_PROVENANCE_ACCOUNTING_V2.md`

The model distinguishes `EXECUTED_PHASE_FAILURE`, `EXECUTED_P5_REDUCTION`, `PRE_START_STATIC_REDUCTION`, and `PRE_START_OTHER_REJECTION`; represents P1-P5 as `PASSED` / `FAILED` / `NOT_ASSESSED`; enforces STARTED/identity-consumption consistency; requires comparator authority for reduction classes; and derives family coverage from actual terminal records rather than a bare family-name list. Duplicate family provenance fails closed.

Synthetic fixtures demonstrate truthful executed-vs-pre-START histories and evidence-backed family coverage. No A01 Family-B/C `CandidateDisposition` was instantiated, the current A01 evaluator was not changed, and the A01 machine verdict remains untouched/withheld.

## CI / implementation fixups

Initial push CI `35129992622` exposed only SUB-owned lint defects (UP035 for the `Iterable` import and I001 import ordering). SUB fixed those on its own branch. Intermediate lint retries remained confined to the same three prototype files. Exact final-head CI `35130731774` at `d5317485a591439cb52d52b649b4930964cf2b3a` completed successfully on Python 3.11 and 3.13 through Install, Lint, Local readiness, Test, and Validate bundle.

No PR or merge was created.

## Scientific / integrity result

New scientific measurement: **none**. New readiness/methods information: **yes** — the prior A/B/C audit gap has a generic, isolated, tested representation that preserves pre-START `NOT_ASSESSED` truth and makes family coverage evidence-backed without retroactively adjudicating A01.

No experiment, STARTED/control creation, one-way workflow dispatch, acquisition, raw/scored output, freeze/seal/formal/evidence mutation, or identity consumption occurred. Immutable and consumed authorities were not modified.

## Completion / stop

The Analyst completion target is reached: standalone generic schema/model/tests/docs exist, synthetic tests are green, and current A01 accounting plus verdict remain unchanged. `sub_fallback=null`; no Analyst lane was rejected for MAIN-critical-path coupling; blockers are none.

Next SUB action is to return this completed prototype to the next Evidence Analyst cycle. Do not promote it to `main`, migrate the current A01 evaluator, alter A01 verdicts, or touch C19 without a fresh reserved lane.
