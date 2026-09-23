# Utility terminal result — PF-R1 exact-byte development provenance preservation

schema_version: 2
generation_id: UTILITY-20260923T184052+0900-PFR1-PRESERVE-COMPLETED-R96-D7A19C4E
produced_at: 2026-09-23T18:40:52+09:00
completed_at: 2026-09-23T18:40:52+09:00
producer_run_id: utility-auto-20260923T1827+0900-pfr1-preserve
assignment_mode: ASSIGNMENT
status: COMPLETED
assignment_id: UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE
assignment_generation_id: UASSIGN-20260923T155800+0900-PFR1-7B1D4E92
run_count: 1
max_runs: 1
evidentiary_status: NON_EVIDENTIARY_PROVENANCE_ONLY
scientific_authority: NONE
fast_forge_support: false
completion_requires_control_ack: true
control_acknowledged: false

## Objective

Preserve the exact original PF-R1 development `raw.json` and `summary.json` bytes with verified hashes and durable non-evidentiary provenance, without rerun, reconstruction, regeneration, retune, rescore, or scientific reinterpretation.

## Fresh authority and ownership checks

- Utility `assignment/current.md` was re-read immediately before mutation and remained ACTIVE with the exact matching assignment ID and generation.
- Control decision remained `CTRL-DEC-20260923-1558-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE`.
- Latest Evidence Analyst at final pre-mutation check: `EVA-20260923T180248+0900-R96-3F7C92A1` / commit `df97c2c8830c7d50d23d13c43091866ad5d23c77`.
- Latest MAIN/Relay + Fast Forge control-plane branch at final pre-mutation check: `ops/orchestrator-run-report@ebde477bd697f4f99565062fb8ada9c40dbc331a`.
- Fresh MAIN owns Candidate #35 Architecture R2; Utility did not touch that object/runtime.
- Fresh Fast Forge R96 is NO_OP under the Candidate #35 R2 ownership shadow; Utility did not perform Forge work.
- Stable `main` independently re-fetched unchanged at `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`.
- PF-R1 frozen source branch independently re-fetched unchanged at `research/main-h7-pf-r1-frozen-panel-r64-cycle4@8681dcbbe2fff986c28a79057f557b35f3f0f752`.

## Exact source

- repository: `salmonmikan/sparkbrain_research`
- workflow run: `35695286240`
- artifact ID: `10680620448`
- artifact name: `h7-pf-r1-cycle4-8681dcbbe2fff986c28a79057f557b35f3f0f752`
- artifact expired: `false`
- artifact expires at: `2026-12-21T06:32:24Z`
- workflow path: `.github/workflows/h7-pf-r1-cycle4.yml`
- PF-R1 contract path: `artifacts/preformal_h7_pf_r1/contract.json`
- source contract path: `artifacts/architecture_h7_dev_r2/contract.json`

## Hash verification before persistence

- original artifact ZIP SHA-256: `db43c7557b55760ddd182afe836405c2e2f261c60261504723182ef9240e908d` — MATCHES Actions artifact digest and prior provenance
- exact `raw.json` SHA-256: `695261aeadab1ab311b60787f1b6a9023c29e24009c6f173c1a660469a6906db` — MATCHES prior provenance
- exact `summary.json` SHA-256: `6202ee328f20b637ec32258b9764b6c521900d87ad84bd5b77f7074cad05e237`
- sizes: ZIP `100325` bytes; raw `807932` bytes; summary `2172` bytes

No scientific fields were interpreted in order to establish these hashes.

## Durable create-only destination

Storage surface: persistent ChatGPT Library, explicitly NON_EVIDENTIARY development provenance.

Folder:
`/SparkBrain/Non-Evidentiary Development Provenance/PF-R1/artifact-10680620448/`

Create-only uploads (`overwrite=false`):
- `source-artifact.zip` — library_file_id `libfile_6bea74e45e80819181c0a83a747eb1ea`
- `raw.json` — library_file_id `libfile_5a28497fec488191aad90afba6a0a65a`
- `summary.json` — library_file_id `libfile_315d4c6697088191bf7debb5da9fae6d`
- `provenance-manifest.json` — library_file_id `libfile_4a06e944fbe08191b1aa3760b22e0ff4`

The original ZIP is retained as an additional byte-exact container for the two source files. The manifest is classified `NON_EVIDENTIARY_DEVELOPMENT_PROVENANCE_ONLY` and grants no scientific authority.

## Post-persistence byte verification

Each persisted Library object was materialized back from its exact returned file ID and SHA-256 re-computed:

- persisted ZIP: `db43c7557b55760ddd182afe836405c2e2f261c60261504723182ef9240e908d` — MATCH
- persisted raw: `695261aeadab1ab311b60787f1b6a9023c29e24009c6f173c1a660469a6906db` — MATCH
- persisted summary: `6202ee328f20b637ec32258b9764b6c521900d87ad84bd5b77f7074cad05e237` — MATCH
- persisted manifest: `6818d3bf02d5c35cc9b19284fea55e461144766e437d4c31b5e5c19a0487f970` — MATCH

Availability status: `DURABLY_AVAILABLE_EXACT_BYTES_VERIFIED`.

## Integrity / hard-floor checks

- PF-R1 rerun: NONE
- reconstruction/regeneration: NONE
- retune/rescore: NONE
- scientific interpretation: NONE
- Candidate #34 D34-Q002 raw/result access: NONE
- Candidate #35 runtime mutation: NONE
- FORMAL identity / STARTED creation: NONE
- consumed/formal/sealed/evidence/preserve mutation: NONE
- protected outcome access/scoring: NONE
- result-bearing workflow dispatch: NONE
- scheduler mutation: NONE
- research PR merge: NONE
- research branch mutation: NONE
- Fast Forge work: NONE
- hard-floor actions: NONE

## Stop reason / follow-up

stop_reason: COMPLETED_EXACT_BYTES_PRESERVED_AND_REVERIFIED
follow_up_recommendation: Control should acknowledge this terminal result, re-read the still-matching current assignment generation, close/archive the assignment via its compare-and-swap lifecycle, and return the Utility pointer to IDLE. Evidence Analyst may then independently re-fetch unchanged H7 R5 and decide any later H7 authority; Utility grants none.
