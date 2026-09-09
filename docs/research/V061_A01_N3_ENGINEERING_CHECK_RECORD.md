# N3 engineering check execution record

Status: **ADAPTER_AND_BUDGET_UNBOUND**. Engineering-only; no A01/MD-001/MD-002 or world capability execution.

Source-only check script commit: `87d7771b338af37fff89a5153bc8675b39f4b90d`.
Recurrent-family source checkout: `2f2aae612ee6e0f08453c855a9910d965fa89bec`.
The script checks the actual imported recurrent module Git blob before execution.
It does not run training or any experiment runner.

Command from this branch, supplying the existing pinned source checkout:

```bash
python scripts/check_a01_n3_family_engineering.py --source-root /path/to/checkout-at-2f2aae612ee6e0f08453c855a9910d965fa89bec
```

Exact stdout (one compact JSON line followed by LF):

```json
{"capability_run":false,"engineering_only":true,"hidden_state_scalars":2,"persistent_nonmutation":true,"persistent_scalars":4,"persistent_serialized_bytes":444,"persistent_state_sha256":"6da2ae15a27f5f08b32ca4c653cae2bda2df12071ec28859df18450a8f80d3bf","recurrence_dependence":true,"source_blob":"b703a326bbeae1dabc5b8a50055aaeb1a3ae310d","status":"ADAPTER_AND_BUDGET_UNBOUND"}
```

Stdout SHA-256 including final LF:
`73248cba132def1e8dbba1cdd202838ba174958d887b06babbab846b47b2c917`.

The script was executed successfully; a second execution piped to sha256sum
verified the displayed stdout hash. Both are engineering-only recurrence
primitive calls, not capability trials.

## Accounting categories and unresolved comparability

| Category | Existing A01 MD-001 figure | Existing sparse-family check | Matching requirement |
|---|---|---|---|
| Incremental learned support/readout | 4 path-support counters at peak | 2 readout weights | Count actual encoded values |
| Fixed recurrent weights | Not present in incremental support payload | 2 weights | Count them even when deterministically generated |
| Hidden dynamic state | Not included in 155-byte support-only figure | 2 scalars, caller-owned and excluded from persistent_state_dict | Transient only under explicitly reset lifecycle; otherwise persistent |
| Topology/configuration/identifiers | Support payload includes path keys, not all base runtime metadata | 444-byte payload includes topology, config, seed, unit/output counts | Align categories before comparing totals |
| Base local temporal state | Outside reported incremental support payload | Not supplied as a common adapter in this primitive check | Declare genuine common infrastructure, not an assumed free component |
| Exact-parent router/C relation evidence | Shared infrastructure in N1-scoped design | Not implemented in this primitive | Charge shared components symmetrically once adapter exists |
| Per-step operations, lookups and peak occupancy | Not independently measured by original MD-001 P5 fields | Not yet instrumented by this check | Must be measured before resource-matched claim |

**444 versus 155 is not a fair whole-system ratio.** The two figures describe
different serialization scopes. It proves that simply equating four scalar
entries does not establish the original byte-budget claim; it does not prove
the recurrent family is 2.86 times larger as a complete system.

No accounting scheme or MD-001 interpretation has been changed here. A future
MD-002 budget contract must be frozen before outcomes, include equivalent
categories, and fail closed if the comparator exceeds it. No unbudgeted causal
adapter has been implemented. See V061_A01_N3_FAMILY_FEASIBILITY.md for the
source-backed family selection and remaining adapter contract.
