# CX01 Branch Policy

Architecture branches are forked from the same common-contract checkpoint.

```text
research/cx01-comparator-extension
  ├─ research/cx01-g6-vomm
  ├─ research/cx01-g7-htm
  └─ research/cx01-g8-stm
```

Rules:

- comparator branches may add architecture-specific model code and fidelity tests;
- they may not alter shared world/scoring semantics to improve their own result;
- any necessary shared-contract correction must be proposed on the parent branch and applied symmetrically;
- formal held-out candidate generation happens only after integration and cross-architecture review.
