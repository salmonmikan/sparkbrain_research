# SparkBrain Evidence Analyst handoff — 2026-09-15 19:09 JST

## Orchestrator report consumed

Read `ops/orchestrator-run-report@406821a3d9c8506a34927d902af9a1481e622eb3` (`reports/orchestrator/latest.md` and `state.json`) before choosing work. Its authoritative branch heads and consumed-identity inventory were re-fetched and remained current: main `ba16bf10535141c2edb29bbe3439ba0a38e71179`, A01 `8044b25f3a7b7767bf1262ea6a99cd6b795e3e8d`, RV01 `02b3d80744d0eb10cb0d90fc38d3c55729d7ab99`, RV02 `c60b7fd8d3889ee969f505d921e7d31c990871e6`. The report is broadly consistent, but its RV01 mechanistic interpretation is superseded by the numerical-validity audit below.

## Evidence inspected

- Open PR #133, exact head `78790d08b1da9c7efcb397203ca77cce34a7a487`, base `research/rv01-endogenous-transition@02b3d80744d0eb10cb0d90fc38d3c55729d7ab99`; CI run `34951827861` is green.
- PR #133 review state and comments: unresolved P1 requires a canonical `docs/RESULTS_LEDGER.md` entry. The attempted `@codex address that feedback` remediation did not run because Codex replied that an environment must be created for the repository.
- Immutable RV01 capability preserve `preserve/rv01-r01-16-capability-20260915@0a25eac227d7ac0e8dbd5532d450ed2d50efa105`, STARTED/control `control/rv01-r01-16-capability-started-7761c1f7-20260915`, source freeze `freeze/rv01-r01-16-capability-source-20260915`, workflow `34903089159`, Actions artifact `10370968354`.
- Immutable capability raw/result bundle plus source code at `02b3d80744d0eb10cb0d90fc38d3c55729d7ab99`: `rv01_r01_16_capability.py`, `rv01_r01_16_factorization.py`, `rv01_r01_16_worlds.py`, `rv01/interference_runner.py`, `rv01/direct_field_plasticity.py`.
- A01 P2 freeze/control/preserve refs, RV02 RD005 D1 freeze/control/preserve refs, and CX01 candidate-002 source/package/control/preserve refs were re-fetched unchanged.
- No `r01-17`, `rd006`, or `cx01-candidate-003` branch exists. Only PR #133 is open.

## Genuinely new evidence since the previous analyst run

### RV01 R01-16 numerical-validity audit

The frozen R01-16 classification remains exactly what the immutable scorer recorded: Weight=`WEIGHT_SUPPORTED` (100/100), Delay=`DELAY_MIXED` (46 discordant, 54 negative), Combined=`COMBINED_SUPPORTED` (100/100). Do not rewrite those historical labels.

However, the immutable raw capability artifact shows that the purported learned-delay intervention is effectively zero at scientific scale:

- all 290 physical edges have a nonzero delay difference only under exact floating-point inequality;
- maximum absolute pre/post delay change: `1.0325962307433656e-11 ms`;
- mean absolute delay change: `1.3210275785146725e-12 ms`;
- median nonzero absolute delay change: `6.954437026251981e-13 ms`;
- maximum relative change: about `2.05e-12` of the nominal lag;
- by contrast, absolute weight changes range from about `0.6368` to `1.2` from initial weight `0.05`.

This follows directly from the frozen implementation: each world initializes connection delay to `world.lag_ms`; training pulses are also spaced by `world.lag_ms`; the plasticity rule moves delay toward the observed pulse lag; and `delay_changed_edges` uses exact `pre.delay_ms != post.delay_ms` without a numerical or mechanistic magnitude floor. Therefore there is no prospectively intended nonzero delay-learning signal in R01-16; tiny timestamp arithmetic differences are promoted into a delay contrast.

The 46/100 `F0_vs_FD` sequence differences are also consistent with numerical tie/order sensitivity rather than meaningful learned-delay expression. Across all 46 differing probes, F0 and FD contain the same unique generated-unit set. In 42/46 they contain the same multiset and the same length, with only ordering differing; the remaining four are edge-reversal cyclic probes with the same unique set but repeat-count/order differences inside the fixed horizon. The 46 cells occur only in competing/cyclic families: shared-cue 12/15, shared-prefix 12/15, edge-reversal 6/15, dense-route-load 16/40, and disjoint-routes 0/15.

**Scientific interpretation:** R01-16 robustly supports a learned-weight contribution at development level. It does **not** provide credible evidence for a scientifically meaningful learned-delay mechanism, because the delay intervention amplitude is roundoff-scale. The immutable `DELAY_MIXED` label should be retained as the historical scorer output, but interpreted as a numerical/order-sensitive measurement outcome rather than evidence of a weight-conditioned biological/mechanistic delay contribution. Combined support is at least inseparable from, and plausibly dominated by, the strong weight effect.

### PR #133 provenance issue

PR #133 currently labels `b1b4d555d30630d1051482563696981261619143099216ab893bbea481d69392d` as the “Capability suite hash”. That is not the immutable suite hash declared by both preserved `COMPLETE.json` and the raw capability result. The authoritative suite hash is `c5c5e32160b634680ff5cad726365c38ec3d06c266cc453fcf349d604ee48ffc`.

Therefore PR #133 must **not** be merged as-is. Adding only the missing results-ledger entry is insufficient; the mechanistic interpretation and suite-hash provenance also require correction. This is a genuine scientific/provenance blocker, not optional polish.

## Interpretation by active line

### A01 MD-002

P2 candidate-002 remains consumed and development-positive: `SUPPORTED_SELECTIVE_CIRCULATION`. This is useful development evidence for selective post-attribution circulation, not held-out/formal confirmation. The old-confirmatory P4 route remains STOP because no complete pre-P2 executable scoring/replay/decision contract has been established. A future P4 designed now must be a distinct exploratory/development candidate with fresh prospective identity and contract.

### RV01 R01-16 / successor

Weight mechanism: **SUPPORTED at exposed-development level** by a large, robust intervention. Delay mechanism: **UNRESOLVED / not credibly supported by R01-16**, because the realized delay contrast is numerical-jitter scale. The previous “asymmetric weight-conditioned delay expression” interpretation is too strong and should be superseded by the numerical-validity audit. R01-16 itself is consumed and must not be rerun or retuned.

The shortest clean next science is a distinct exploratory successor that creates a prospectively meaningful nonzero delay-learning signal on fresh worlds/seeds/identity. Initial physical delay and training inter-pulse lag must be deliberately separated by a preregistered magnitude far above numerical tolerance, and delay eligibility must use a meaningful magnitude floor rather than exact float inequality. Preserve both the existing route/behavior endpoint and an orthogonal timing/trajectory endpoint; do not make exact same-time event order alone a positive mechanism endpoint.

### RV02 RD005 / successor

D1 remains consumed terminal `D1_ZERO_READY_STOP`; blind result remains unopened. No new successor exists. Shortest valid next move remains a fresh blind-preserving construction diagnostic that distinguishes why no row became ready, without repairing or rerunning D1.

### CX/CX01

Candidate-002 remains immutable formal NEGATIVE. Source `freeze/cx01-002-source@e8483968ce43076b4c3fd04c76e62106e2031769`, package `freeze/cx01-002-package@c104be281285d52a732d5366fe36209d5688d973`, STARTED `control/cx01-candidate-002-started-20260913@8216d41a57e6933443d38dfc8d93f9188e423d0c`, preserve `preserve/cx01-candidate-002-formal-34742073336@6d45928827209cd763a2879494d85838df38b96f`. No candidate-003 branch exists. Do not rerun or retune candidate-002.

## Consumed identities / no-rerun set referenced

- A01 MD-001 (`preserve/v061-a01-md-001`).
- A01 MD-002 P2 candidate-002: `a01-md002-p2-candidate-002-ef73823f4c667aee2655d0e2`; source/control at `8044b25f3a7b7767bf1262ea6a99cd6b795e3e8d`, preserve `d7d48a8ad482acdb18de783c9506c32377530e1e`.
- RV01 R01-16 construction census (preserved workflow `34881254582`) and capability `rv01-r01-16-capability-02b3d80744d0eb10-65ebe33d70af`; capability preserve `0a25eac227d7ac0e8dbd5532d450ed2d50efa105`; same-identity retry false.
- RV02 RD005 D1 construction identity `96634541dc29b00be9f19b5819d45f541af69348ab6c1b0da6b48e943221700a`; source `c60b7fd8d3889ee969f505d921e7d31c990871e6`, STARTED `2535b6312a091f7da4efa10c064c285bdeda7eaf`, preserve `d1fdd67ea197b879c52942c4a34e7d39a0a40698`.
- CX01 candidate-002 formal identity and associated immutable refs above.

## Genuine blockers vs optional work

**Genuine blockers**
1. PR #133 cannot merge as-is: unresolved canonical-ledger P1, incorrect suite-hash provenance, and an over-strong mechanism interpretation that ignores roundoff-scale delay amplitude.
2. A valid RV01 delay successor must prospectively create a substantive delay contrast and define a magnitude-aware/tie-robust scorer before any output is observed.
3. A01 P4 cannot be called the old confirmatory P4 unless a complete pre-P2 frozen executable contract is actually found; otherwise it is a new exploratory identity.

**Optional / defer**
- Generic cleanup, main integration, broad registry work, historical branch deletion, and unrelated documentation polish.

## Ranked next actions

1. **RV01 real-delay successor, preceded by the minimum correction of PR #133 — HIGH information / MODERATE distance.** Correct the durable R01-16 interpretation/provenance first, then prospectively define and, if integrity-ready, execute a fresh exploratory successor with a deliberately nonzero delay-learning signal and a magnitude-aware/tie-robust endpoint.
2. **A01 P4 as a distinct exploratory continuing-vs-reset discriminator — HIGH / MODERATE.** Proceed only under a newly prospective contract unless a complete pre-P2 frozen executable P4 contract is found.
3. **RV02 blind-preserving zero-ready successor diagnostic — HIGH / MODERATE.** Fresh identity only; preserve D1 blind and terminal evidence.

## GO / STOP criteria for #1

### GO

- Re-fetch PR #133 and RV01 authoritative/preserve refs; if the head moved, re-audit the new head.
- Preserve the historical frozen labels exactly, but correct the interpretation to state that R01-16’s realized delay deltas are roundoff-scale and cannot establish meaningful delay plasticity.
- Correct the suite-hash provenance to authoritative `c5c5e32160b634680ff5cad726365c38ec3d06c266cc453fcf349d604ee48ffc` and add the required canonical results-ledger entry. Re-review and merge only an exact green reviewed head.
- For the successor, use new seed/world/experiment identities and a prospectively fixed separation between initial physical delay and training inter-pulse lag/desired delay that is scientifically material and many orders above numerical jitter.
- Pre-register a minimum realized delay-change eligibility threshold; never use exact float inequality as sufficient evidence of a delay intervention.
- Pre-register both route/behavior and timing/trajectory endpoints. Treat near-simultaneous event ordering robustly so a permutation caused only by sub-tolerance timestamps cannot count as mechanism support by itself.
- Bind exact source/runtime/package/input, no-clobber/STARTED, review/override, and raw-before-score preservation before one-way execution.

### STOP

- PR #133 still claims weight-conditioned delay expression without acknowledging the roundoff-scale intervention, still contains the wrong suite hash, or lacks durable ledger preservation.
- The proposed successor sets initial delay equal to training lag/desired delay or otherwise produces only machine-precision-scale delay changes.
- Delay eligibility still depends on exact `!=` rather than a preregistered meaningful magnitude floor.
- Same-time/tiny-jitter event ordering alone can satisfy the primary support criterion.
- Any R01-16 consumed identity/world/seed is reused as the new one-way identity, or any frozen/preserved R01-16 evidence is modified.
- Another worker has already STARTED the same proposed successor identity.

## Exact refs the orchestrator must re-check

- `ops/orchestrator-run-report@406821a3d9c8506a34927d902af9a1481e622eb3`
- PR #133 / `review/rv01-r01-16-delay-interaction-diagnostic-20260915@78790d08b1da9c7efcb397203ca77cce34a7a487`
- `research/rv01-endogenous-transition@02b3d80744d0eb10cb0d90fc38d3c55729d7ab99`
- `freeze/rv01-r01-16-capability-source-20260915@02b3d80744d0eb10cb0d90fc38d3c55729d7ab99`
- `control/rv01-r01-16-capability-started-7761c1f7-20260915@02b3d80744d0eb10cb0d90fc38d3c55729d7ab99`
- `preserve/rv01-r01-16-capability-20260915@0a25eac227d7ac0e8dbd5532d450ed2d50efa105`
- workflow `34903089159`, artifact `10370968354`
- A01 `research/v061-a01-n3-adapter@8044b25f3a7b7767bf1262ea6a99cd6b795e3e8d` and P2 preserve `d7d48a8ad482acdb18de783c9506c32377530e1e`
- RV02 source/preserve/control refs listed above
- CX01 source/package/control/preserve refs listed above

## Concurrency / staleness findings

No authoritative research head or immutable evidence ref moved during this analysis. PR #133 remains at the same exact head. The attempted Codex remediation is stale/unavailable because no Codex environment is configured, so the next orchestrator should not wait for that path; it should make a clean review-branch correction itself or supersede PR #133 prospectively while preserving its history.

## ORCHESTRATOR HANDOFF

Do **not** merge PR #133 merely after adding the ledger entry. First re-audit it against the immutable R01-16 capability bundle: correct the suite hash to `c5c5e321...`, replace the weight-conditioned-delay mechanism claim with the numerical-validity finding (max realized delay change only `1.03e-11 ms`, while weight changes are ~`0.64–1.2`), and preserve that negative/measurement-validity result in the canonical ledger. Once the exact corrected head is green/reviewed, merge it. Then prioritize a fresh RV01 exploratory successor that deliberately generates a real nonzero delay-learning contrast and uses magnitude-aware/tie-robust timing plus route endpoints. If that successor cannot be made prospective and integrity-ready in the run, pivot to a new exploratory A01 P4; never rerun R01-16, A01 P2, RD005 D1, or CX01 candidate-002.
