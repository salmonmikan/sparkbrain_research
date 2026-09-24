# FAST FORGE latest — TH-002 static addressability probe killed by ordinary key-value reduction

- schema_version: `2`
- worker_role: `FAST_FORGE`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- overall_status: `FORGE_DEAD_END`
- forge_id: `FORGE-20260924T223801+0900-R126-TH002-STATIC-KILL`
- theory_id: `TH-002-ANONYMOUS-LINEAGE-ADDRESSABILITY`
- analyst_probe_spec: `TH002-FORGE-001-STATIC-ADDRESSABILITY-KILL`

## Freshness / ownership
Stable `main` is `d16403414fc7abebd23075fc401240971b8eb91d`. Evidence Analyst R126 at `abb12babbdf1385826029ee39e9fb20c13c42f7d` explicitly authorizes exactly one bounded `THEORY_FORGE_TEST` static falsification for TH-002. MAIN PRIMARY R130 remains `STOPPED_NO_ALLOCATED_CANONICAL_OBJECT`, 35/35 canonical objects terminal, active 0, scientifically queued 0. Theory R4 remains noncanonical and emits no Revisit proposal. Literature R43, Audit R10, Methodology R116 and Utility R125 were re-fetched; Utility remains IDLE/non-authorizing. H7 and Candidate #35 remain terminal and untouched.

## Selected question / prototype
Analyst-approved Theory probe, not independent Forge work and not Revisit work: can a fresh three-lineage permutation-symmetric merged carrier support delayed content-selective historical revision without reducing to ordinary addressable memory?

Isolated branch: `forge/th002-static-addressability-kill-20260924`.

Fresh fixed construction uses three pairwise-orthogonal content-derived physical signatures `k0=(1,1,1,-1)`, `k1=(1,1,-1,1)`, `k2=(1,-1,1,1)`, scalar states `(0.25,-0.50,0.75)`, merge carrier `M=sum(v_i k_i/4)`, delayed physical query `q=k_j`, readout `q·M`, and fixed revision `M'=M+0.20q/4`. The ordinary comparator receives the same content query and stores the same `(key,value)` bindings as an associative key-value table; no evaluator-only target index is supplied.

Prototype script blob `a2b840631a733c0d29948fde4f5da6b57ce1e027`; technical note blob `e4c3639e2c01898cb9ed140e47aefa11f1656e8b`.

## Observation / ordinary reduction
Static checker passes all six lineage-order permutations, all three delayed queries, target-selective revision and exact matched-access key-value equivalence. Carrier `M=(0.125,-0.25,0.375,0.0)` decodes exactly to `(0.25,-0.50,0.75)`.

Strongest ordinary reduction: `ASSOCIATIVE_KEY_VALUE_MEMORY / SEPARABLE_ADDRESS_PLUS_STATE`, with finite-register equivalence on the three-lineage subspace. Since `k_i·k_j=4δ_ij`, the delayed physical signature is exactly a lookup key; the associative comparator reproduces every read/revision relation under matched information access. No reduction-resistant residue remains.

## Disposition
`FORGE_DEAD_END`. Immediate static kill per R126. No dynamic/performance experiment, parameter/resource/architecture/fixture sweep, candidate creation, promotion proposal or Utility request. MAIN collision check `PASS_NO_COLLISION`.

Full record: `reports/orchestrator/sub/history/2026-09-24/2238-r126-th002-static-addressability-kill.md` (create commit `e6c520bc9f2568087868f99f8926d701d9b21150`).

Metrics after run: runs `32`, prototypes `21`, Theory probes/kills/survivors `3/3/0`, Revisit probes/kills/survivors `1/1/0`, dead ends `17`, interesting retained `1`, promotion proposals `1`, later admissions `0`, duplicate/rescue rejects `13`, ownership collisions `0`, ordinary-reduction rejects `17`, idea-to-observation latency `SAME_RUN_STATIC`.

Exact refs: main `d16403414fc7abebd23075fc401240971b8eb91d`; Evidence Analyst R126 `abb12babbdf1385826029ee39e9fb20c13c42f7d` / blob `a1d8fb2f6eab9b275bf4b38e825cb5250fc252d1`; Control R63 `f804b40381cc35493cc12e04a2bc83dbca580c86`; MAIN R130 pre-Forge mailbox `89d3a73da19f515a58999404652658abacbcd3bb` / blob `626cc86f575f8adbe594bf81c47d4c1b96a748fa`; Theory R4 branch `87d206a3f62c70c393531413445703fd0baa108a`; Literature R43 blob `bc346dac47b85fdcdeae49a85f4036f97a0aee91`; Audit R10 blob `a89738c837b2e5bc2eab94adb1722bbb6daeb673`; Methodology R116 `4ba0b61d657bd5ba58df1cb580456c05629a6b7f` / blob `0245f57594ac6d49084d2b9b8867bc65855634ca`; Utility R125 `40143dd0f8b19f5d2c0c557b2574a07cf2815e92`; Repository Steward `3232ec8921a640de7ba4a0e432d2cb647fbfc506`; Forge record commit `7db8abb08e7862e3bb98c985f2e7ec4d81cd9d16`.

Hard-floor actions: none. No PRE_FORMAL/FORMAL identity, STARTED, official TEST/scoring/protected held-out/evidence/formal/sealed/freeze/preserve mutation, terminal rerun/retune/rescore/reopen, consumed evidence mutation or canonical workflow dispatch occurred. Forge branch was not merged.
