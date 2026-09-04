# PR #18 Diagnostic Handoff

Current scope: candidate-003 failure diagnostics D1-D12, P1-P5 falsification protocols, strengthened
P5 dynamic/state equivalence, pre-mechanism admission, prospective negative-completion rules, and A01
v2 preregistration.

Formal candidate-003 result remains unchanged:

```text
Primary supported: false
G3 supported:      true
G4 supported:      true
G5 supported:      true
```

A01 v2:

```text
proposal SHA-256:
c31e7c4148a2940e09c65960b8f208242e9e1d4c19f01929fcdc81b7b7379147

protocol/null source:
92c2ead081844861847d679315639da6de401e1b

status:
PREREGISTERED_NOT_IMPLEMENTED
```

Validated code/evaluator head:

```text
44798cbfc85cce3239d490bf37bfd4a9ca1f4b58
GitHub Actions run 33926818301
Python 3.11: Ruff / readiness / full pytest / bundle PASS
Python 3.13: Ruff / readiness / full pytest / bundle PASS
```

Later commits in this handoff are documentation-only status synchronization.

Cross-line status at 2026-09-05:

```text
CX01: corrected pre-formal review merged; source-freeze candidate f2c5ead5...; formal unopened
RV01: R01-12E freeze review closed; 50 held-out worlds sealed-not-executed
```

Neither line contributes a new formal outcome to candidate-003/A01.

Next mechanism implementation belongs on a separate prospective A01 branch. It must not modify or
rerun candidate-003.
