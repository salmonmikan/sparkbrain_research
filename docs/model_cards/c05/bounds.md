# Oracle and chance bounds

- Oracle: evaluator-only truth upper bound. Calling the observation `step` API is rejected,
  so truth cannot enter ordinary baseline inference accidentally.
- Chance: uniform label distribution and deterministic tie choice.
- Both are bounds, have no learned parameters, and are excluded from matched rankings.
