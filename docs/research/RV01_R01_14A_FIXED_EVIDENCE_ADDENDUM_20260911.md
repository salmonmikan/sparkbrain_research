# RV01 R01-14A fixed-evidence addendum — 2026-09-11

Status: **APPEND_ONLY_PRESERVATION / REGISTERED-AUC INVALID / NO RERUN**

The original development artifact is retained byte-for-byte from workflow run `34308089316` at `artifacts/research/rv01/r01_14/development_result.json` with SHA-256 `4a214059cacc66d473776de7b46455c959ce0ac5c7089c6acfafbc9e0ef91e25`. The artifact ZIP hash remains `fb9e4f6ee01bb41ca0a733480683fafdf3f1d5d1b7e1d141681d241191d50bdd`. No science was rerun while preserving it.

Independent review found a preregistration mismatch in the historical `normalized_discovery_auc`: the implementation divided cumulative discovery by the ideal discovery curve, while the registered endpoint divides the mean cumulative distinct count by final distinct count, equivalently `sum(cumulative_distinct) / (events * final_distinct_count)`. Historical AUC values are therefore not accepted evidence for that registered endpoint. The code is corrected prospectively, but the fixed artifact is not regenerated.

The fixed evidence is runtime-bound to CPython 3.11.15 and makes no byte/semantic-hash portability claim across other supported interpreters.

The retained negative conclusion does not depend on the invalid AUC field: the traversal/event signature was not interference-specific and was strongest in the disjoint reference family. Held-out R01-14 capability remains closed and unexecuted.
