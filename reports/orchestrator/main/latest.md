# MAIN PRIMARY checkpoint — C19-R1 audit amendment complete, lint blocker fixed, exact-head checks running

Timestamp: 2026-09-18T00:35:00+09:00
Execution mode: PRIMARY
Evidence Analyst commit: `f2342817193f4e3a191bb05921db5598ee3cd10c`

MAIN frontier remains C19-R1 on `research/c19-r1-revision-authority-reduction-20260917`, planned identity `c19-r1-revision-authority-official-v1`. FAST PATH was used throughout; no full reconciliation was required. The Analyst-authorized audit amendment is implemented: deterministic target-free `pair_index -> atomic_idx` source-map/digest, primary atomic-cluster bootstrap with whole-cluster multiplicity, and the former pair-IID bootstrap retained only as secondary sensitivity. The same-I2 stateless controller, seeds, input universe, runtime, metric, bootstrap count, RNG seed, Type-7 quantile semantics, thresholds, and claim boundary were not retuned.

The first amended exact head `27e95f3363bfd32d21c9744cff3a7de8562cf679` reached dedicated pre-START run `35240543810`, which failed only at Ruff lint with one `E501` line-length error in `c19_r1_scoring.py`; install had succeeded and later readiness steps were skipped. This was a science-invariant mechanical blocker, so MAIN fixed only that formatting defect. The branch now points to exact head `7cf849051a68b4227e29fe2f6ee95b2ff277dacd` (`fix(c19-r1): wrap cluster policy for lint`).

Exact-new-head checks are now running on `7cf849051a68b4227e29fe2f6ee95b2ff277dacd`:
- dedicated `C19-R1 pre-START readiness` run `35241040727`: `in_progress`;
- ordinary `ci` run `35241040735`: `in_progress`.

No official Belief-R data was accessed, no STARTED/control ref was created, no one-way execution was dispatched, no R1 raw/targets/scoring were produced, and the R1 identity remains fresh/unSTARTED/unconsumed. Consumed v2/v3/v4 and immutable v4 preserve/evidence were untouched. SUB remains independent and was not used for any R1 blocker.

PRIMARY is ending rather than waiting idly. Lease status is `WAITING_EXTERNAL`. Relay/next MAIN should collect runs `35241040727` and `35241040735` and re-fetch the exact branch head first. If either fails for another science-invariant implementation/CI reason, MAIN owns the fix and must regain both checks on one final SHA. If the atomic source-map/cluster binding proves ambiguous, target-dependent, incomplete, or requires any new scientific/statistical choice, STOP for Analyst. If both exact-head checks are green, transition only to `R1_PRE_START_READY_FOR_ANALYST_REVIEW` and STOP before STARTED; current Analyst authority does not authorize one-way execution.

No new scientific result was produced. This run advanced only the prospectively fixed pre-START inferential contract/readiness boundary.
