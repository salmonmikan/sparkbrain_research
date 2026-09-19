# Utility result — suppression static-detector consistency

assignment_id: `CTRL-20260920-0650-SUPPRESSION-STATIC-DETECTOR-CONSISTENCY`
run_count: `1 / 1`
status: `COMPLETED`
evidentiary_status: `NON_EVIDENTIARY_METHODOLOGY_DIAGNOSTIC`
classification: `STATIC_EXTRACTOR_FALSE_NEGATIVE_CONFIRMED`
recommendation: `DO_NOT_USE_DISPUTED_STATIC_FACTS_AS_SUCCESSOR_SEMANTIC_AUTHORITY`

## Scope and integrity

This run was read-only with respect to all scientific/research refs. It did not dispatch or rerun a workflow, execute pulses/probes/training, modify the completed suppression artifact/contract/harness/research branch, relabel or rescore the completed `AMBIGUOUS_CONTRACT`, access official TEST or consumed/formal raw evidence, change thresholds/comparators/metrics/seeds/candidate status/successors, create PRE_FORMAL/FORMAL authority, or mutate any scheduler.

Only this append-only Utility result and the normal Utility state update are authorized outputs.

## Exact authoritative refs independently re-fetched

- stable source binding in prospective contract: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- completed research head: `2ef4b24f8e7ef8577ebbcb0328e7b3476bc24336`
- workflow run: `35465512928` — `completed/success`
- workflow: `.github/workflows/v05-unit-suppression-transient-semantics-arch-cycle1.yml`
- artifact id: `10591265966`
- artifact archive GitHub digest: `sha256:d4dd67e97132229fc60c1cf13b6dbc9366bfa22a2568aa7de116667b41d33669`
- downloaded archive SHA-256 independently recomputed: `d4dd67e97132229fc60c1cf13b6dbc9366bfa22a2568aa7de116667b41d33669` — exact match
- raw artifact SHA-256 independently recomputed: `220eb06b051273680726b8f0f4ad318a95863fcc1e9909daeb23ffd745ec6805`
- raw SHA-256 carried by summary: `220eb06b051273680726b8f0f4ad318a95863fcc1e9909daeb23ffd745ec6805` — exact match
- contract SHA-256 carried by raw/summary: `4d688d4d6ed4e7998d6e4a14ddb0cb9442474168f22996608acceae60fd8a51a`
- contract blob at completed head: `e45025feb290e0ec6740328323d250d34ada8f5d`
- harness blob at completed head: `fb0fab0e9d53fc9fd1a6d7cb17e9f96bc2bc4aba`
- exact bound source blobs:
  - `src/sparkbrain/v05/brain.py@652552f8dc6a53a68e441f593e9bfd82cebb9f7c`
  - `src/sparkbrain/v05/evaluation.py@efd52d236708aea3bf23b6139d8717b1ac1d0559`
  - `tests/v05/test_v05_brain.py@6a81994ac82a3f0660585ef0d95495aaaa336629`
- completed machine outcome remains exactly: `AMBIGUOUS_CONTRACT`
- artifact scope verification: `PASS`

The exact `brain.py` file re-fetched at the completed head reports blob SHA `652552f8dc6a53a68e441f593e9bfd82cebb9f7c`, matching the prospective contract.

## Static-fact audit

### Mapping-critical / implementation-conjunction fields

| field | artifact | exact bound source semantics | audit |
|---|---:|---:|---|
| `supported_public_suppress_surface` | `true` | `true` — `IntegratedV05Brain.suppress_units(...)` exists | MATCH |
| `supported_public_clear_surface` | `true` | `true` — `IntegratedV05Brain.clear_unit_suppression()` exists | MATCH |
| `suppress_updates_selector` | `true` | `true` — updates `self.suppressed_unit_ids` | MATCH |
| `clear_clears_selector` | `true` | `true` — calls `self.suppressed_unit_ids.clear()` | MATCH |
| `apply_temporarily_raises_base_threshold` | `true` | `true` — stores original threshold then assigns `unit.base_threshold = 1e9` | MATCH |
| `restore_restores_original_base_threshold` | `false` | **`true`** — `_restore_unit_suppression()` assigns the saved `threshold` back to `self.base.field.units[unit_id].base_threshold` | **MISMATCH / FALSE NEGATIVE** |
| `process_applies_suppression_before_base_ingest` | `true` | `true` — `_apply_unit_suppression()` precedes `self.base.ingest_pulses(...)` | MATCH |
| `process_restores_threshold_after_base_ingest` | `true` | `true` — restore occurs in `finally` after the ingest call | MATCH |
| `clear_resets_dynamic_state` | `false` | `false` — clear only mutates the selector set; it does not reset field/membrane/potential/adaptation/receptors | MATCH |
| `implementation_state_preserving` | `false` | **`true` under the harness's own fixed conjunction when the restore fact is evaluated structurally** | **DERIVED MISMATCH** |

The key extractor defect is exact and deterministic. The harness computes:

`restore_restores_threshold = "unit.base_threshold = threshold" in restore_source`

but the exact bound method uses:

`self.base.field.units[unit_id].base_threshold = threshold`

The two are semantically the same restoration operation for the saved threshold, but the literal token `unit.base_threshold = threshold` is absent. Therefore the artifact's `false` is a lexical-shape false negative, not a source-semantic fact.

`implementation_state_preserving` is then computed by `all(...)` over the constituent facts, including this false-negative restore field. All other conjunction inputs observed in the artifact match the exact source; therefore its artifact value `false` is also detector-derived rather than faithful to the bound source semantics.

### Supporting characterization fields

| field | artifact | source/test/callsite audit | audit |
|---|---:|---|---|
| `suppression_test_names` | `['test_unit_suppression_is_reversible']` | exact bound test file contains that suppression test | MATCH |
| `tests_selector_reversibility` | `true` | test suppresses `{0,1}`, verifies selector, clears, then verifies empty selector | MATCH |
| `tests_dynamic_state_semantics` | `false` | suppression test does not run `process_episode` or inspect field/membrane/potential/adaptation state | MATCH |
| `evaluator_suppress_call_count` | `3` | exact bound evaluator has three `.suppress_units(...)` calls in causal ablation setup | MATCH |
| `evaluator_clear_call_count` | `0` | no `.clear_unit_suppression(...)` call in the exact bound evaluator | MATCH |
| `explicit_contract_hits.state_preserving` | `[]` | no explicit supported state-preserving phrase attached to the suppression surface in the fixed three-file scope | MATCH |
| `explicit_contract_hits.state_neutral` | `[]` | no explicit supported state-neutral/reset phrase attached to the suppression surface in the fixed three-file scope | MATCH |
| `explicit_state_preserving_contract` | `false` | consistent with fixed scoped source/tests/callsites | MATCH |
| `explicit_state_neutral_contract` | `false` | consistent with fixed scoped source/tests/callsites | MATCH |

The `method_source_sha256` subobject is provenance metadata generated from the parsed method text; it is not consumed directly by `map_outcome()`. No contradictory source identity was observed: workflow binding passed, the contract/source blob SHAs match, and the archive/raw hashes re-verify exactly.

## Extractor mismatch vs handoff mismatch

This is an **artifact extractor mismatch**, not an artifact-to-handoff transcription mismatch.

The immutable raw artifact itself records `restore_restores_original_base_threshold=false`. The Evidence Analyst 05:02 record faithfully repeats that machine value and separately notes that the exact bound source visibly restores the threshold, explicitly identifying a plausible detector false negative. No reviewed handoff rewrote `false` into a different machine value.

Therefore a handoff-binding guard alone cannot catch this defect: the machine artifact is internally self-consistent but semantically wrong on this detector field. This is exactly an upstream machine-fact validity problem.

## Decision relevance / trust boundary

The disputed restore field is decision-relevant because it feeds the derived `implementation_state_preserving` boolean, which is directly consumed by the fixed `map_outcome()` logic. Thus:

- the completed artifact remains historically preserved and must **not** be repaired, relabeled, rescored, regenerated, or rerun;
- the completed `mapped_outcome=AMBIGUOUS_CONTRACT` remains unchanged as the closed cycle-1 terminal record;
- however, `restore_restores_original_base_threshold=false` and `implementation_state_preserving=false` are **not trustworthy source-semantic facts for future successor design**;
- any future reasoning that depends on those semantics should re-bind a fresh, prospectively authorized structural characterization rather than treating these two machine fields as semantic authority.

This diagnostic deliberately does not assign a replacement terminal class and does not choose a successor.

## Prospective methodology recommendation

For future static source facts of this kind, replace narrow literal substrings with deterministic structural/AST checks bound prospectively to the exact source blob. For this specific pattern, the detector should recognize an assignment whose target resolves to `self.base.field.units[unit_id].base_threshold` and whose value is the saved loop variable `threshold`, rather than requiring a local variable spelling such as `unit.base_threshold`.

A future extractor should also fail closed when its structural pattern cannot be established, and its extractor version/digest plus decision-relevant emitted fields should be included in the normal machine handoff binding. This is a methodology recommendation only; no live workflow or scheduler integration is authorized here.

## Collision / ownership check

Latest Evidence Analyst allocation observed at `ops/evidence-analyst-handoff@7e7d425948a86d0eec306b1a75bfc07165d9afa1` explicitly lists this Utility assignment as READ_ONLY/NONBLOCKING. MAIN currently owns `REFRACTORY_CURRENT_ACCOUNTING_ARCHITECTURE_STUDY_CYCLE1`; its research branch was observed at `4589192d927e40cf7a05cf8a94207efb42ebbc65`. The active MAIN object was not used as a fixture or dependency. SUB is limited to independent bounded Discovery. No collision or ownership takeover occurred.

## Stop

`COMPLETED_ONE_READ_ONLY_CONSISTENCY_RESULT_MAX_RUNS_REACHED`

Follow-up authority: none without a fresh Control Brain decision.
