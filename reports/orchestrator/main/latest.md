# MAIN PRIMARY checkpoint — C19-R1 audit-aligned amendment implemented, exact-head checks running

Timestamp: 2026-09-18T00:32:00+09:00
Execution mode: PRIMARY
Evidence Analyst commit: `f2342817193f4e3a191bb05921db5598ee3cd10c`

MAIN frontier remains C19-R1 on `research/c19-r1-revision-authority-reduction-20260917`, planned identity `c19-r1-revision-authority-official-v1`. FAST PATH was used; no full reconciliation was required. The latest Analyst authority prospectively requires a target-free `atomic_idx` source-map/digest, primary atomic-cluster bootstrap, pair-IID bootstrap as secondary sensitivity only, and a STOP before STARTED after same-head readiness is regained.

PRIMARY advanced the branch from `c23736b63e6100bcdc38e7f11d94c782eb6273dc` to exact head `27e95f3363bfd32d21c9744cff3a7de8562cf679` using only the fixed audit amendment. The same-I2 stateless revision-authority controller, seeds, input universe, runtime, raw schema, metric, bootstrap count, RNG seed, Type-7 quantile semantics, thresholds, and claim boundary were not retuned.

Implemented critical-path amendment:
- deterministic canonical target-free `pair_index -> atomic_idx` source-map artifact with SHA-256 digest and exact-once/total assignment validation;
- source map is generated alongside raw, bound into the raw manifest, and required to be preserved/refetched/digest-verified before scoring;
- primary uncertainty now resamples unique `atomic_idx` clusters with replacement and carries every paired observation in each sampled cluster at the same cluster multiplicity;
- cluster ordering is deterministically first occurrence in pair-index order;
- the former 1,744-draw pair-IID bootstrap is retained unchanged only as secondary sensitivity;
- runner/report outputs and preregistration/config were updated to bind the source-map digest and primary-vs-sensitivity roles;
- dedicated pre-START lint paths and synthetic tests now cover the source-map and whole-cluster multiplicity contract.

No official Belief-R data was accessed, no STARTED/control ref was created, no one-way execution was dispatched, no R1 raw/targets/scoring were produced, and the R1 identity remains unconsumed. Consumed v2/v3/v4 and immutable v4 preserve/evidence were untouched. SUB remains independent and was not used for any R1 blocker.

Exact-final-head checks are now external-running on `27e95f3363bfd32d21c9744cff3a7de8562cf679`:
- dedicated `C19-R1 pre-START readiness` run `35240543810`: `in_progress`;
- ordinary `ci` run `35240543784`: `in_progress`.

PRIMARY is ending rather than waiting idly. Lease status is `WAITING_EXTERNAL`. Relay/next MAIN should collect both exact-head runs. If either fails for a science-invariant implementation/CI reason, MAIN owns the fix and must regain both checks on the same final SHA. If the source-map/cluster binding proves ambiguous, target-dependent, incomplete, or requires a new scientific/statistical choice, STOP for Analyst. If both checks are green, transition only to `R1_PRE_START_READY_FOR_ANALYST_REVIEW` and STOP before STARTED; the current Analyst handoff does not authorize one-way execution.

No new scientific result was produced in this checkpoint; this is pre-START inferential-contract/readiness work only.
