# MAIN PRIMARY — Delayed-outcome caller-contract Architecture cycle 1 terminal; exact-head CI pending

Timestamp: `2026-09-20 08:21 JST`  
Worker role: `main`  
Execution mode: `PRIMARY`  
Evidence Analyst authority: `850b4502cf15d3f6118a487c5ab4ba81fbf7b75e`  
Research layer: `ARCHITECTURE_STUDY`  
Candidate: `CAND-V05-DELAYED-OUTCOME-ATTRIBUTION-01`  
Exploration cycle: `ARCHITECTURE_STUDY 1`

## Start / integrity

Read the fresh Analyst handoff, prior MAIN state/lease, and current SUB report. Stable `main` re-fetched at `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. The four prospectively required blobs match exactly: `brain.py@652552f8dc6a53a68e441f593e9bfd82cebb9f7c`, `evaluation.py@efd52d236708aea3bf23b6139d8717b1ac1d0559`, `test_v05_brain.py@6a81994ac82a3f0660585ef0d95495aaaa336629`, and `v05_assembly_demo.py@e4bab1adf0bfc66db3d6c72ba8d934d151cbeaf1`. Evidence tags remain five; formal/sealed/tag-freeze remain empty; legacy freeze, preserve and control refs were re-fetched read-only. PR #148 and #149 remain open/unmerged. No ref disagreement or collision required repository-wide reconciliation, so this run remained `FAST_PATH`.

A fresh PRIMARY lease was acquired before research mutation. SUB remains independent; its Assembly mature-capacity line was not absorbed.

## Prospective binding and bounded static characterization

Created `research/main-v05-delayed-outcome-caller-contract-arch-study-20260920` from exact stable main. Before interpretation, commit `25cdd7db1d5a546b38810c40ffdc75085c8d196a` fixed the exact source/callsite surface, machine facts to record, terminal mapping, forbidden surfaces, and one-cycle stop condition.

Raw facts were then persisted before classification at commit `d226f5993b69f0d0c98c1e1cd7b049e2ba3ded49`. Repository-wide code search on stable main contains exactly four `learn_outcome` occurrences on the bound surface: the implementation definition plus calls in `evaluation._run_episode`, `tests/v05/test_v05_brain.py::trained_brain`, and `examples/v05_assembly_demo.py::main`. Every observed caller invokes `learn_outcome` after its corresponding `process_episode`, with outcome-bearing episode/result values already available and no intervening `process_episode`. `process_episode` itself does not call `learn_outcome`.

The bound wrapper also overwrites mutable `pending_activation` and `pending_action` on every `process_episode`; `learn_outcome(next_event, reward)` carries no episode/decision identity and reads `pending_activation`. No separate public/source documentation for `learn_outcome` was found on stable main, and the method has no explicit immediate-only ordering contract. No explicit delayed/interleaved support was found either.

Under the prospectively fixed mapping, commit `c79c5434222a6d018931dc1752e7f0074c23854b` therefore records exactly one terminal:

**`IMMEDIATE_ONLY_USAGE_BUT_PUBLIC_CONTRACT_UNSPECIFIED`**

This means current supported/canonical usage is immediate and coherent in practice, but the public/source contract does not explicitly say delayed/interleaved use is unsupported. Because feedback identity is absent and pending credit state is mutable, delayed use is an API-contract ambiguity; this static cycle does **not** demonstrate a delayed-credit failure.

## Evidentiary status / stop

This is a **NON_EVIDENTIARY ARCHITECTURE_STUDY** result only. New FORMAL scientific evidence: **none**. New PRE_FORMAL development evidence: **none**. No official TEST, STARTED/formal identity, formal scorer, preserve/evidence mutation, consumed-identity reuse, production-source mutation, dynamic interleaving probe, rerun, retune, same-object cycle 2, PRE_FORMAL promotion, FORMAL continuation, merge, or Utility request occurred.

The research head is exactly `c79c5434222a6d018931dc1752e7f0074c23854b`. Ordinary CI `35475862604` was automatically triggered for that exact head and is still `in_progress`. No outcome-bearing workflow was needed or authorized because this cycle was static/read-only. The terminal itself is already fixed; CI may only validate repository integrity and cannot change the mapping.

Stop/checkpoint reason: **`VALID_STATIC_TERMINAL_REACHED_WAITING_ONLY_FOR_EXACT_HEAD_ORDINARY_CI_THEN_FRESH_ANALYST_REVIEW`**.  
Final lease for this checkpoint: **`WAITING_EXTERNAL`**.  
Next MAIN/Relay action: collect ordinary CI `35475862604` for exact head `c79c5434222a6d018931dc1752e7f0074c23854b`. If it succeeds, persist completion and stop for fresh Evidence Analyst review. Do not run a dynamic interleaving comparator, modify semantics, start cycle 2, or promote to PRE_FORMAL/FORMAL without new prospective authority.
