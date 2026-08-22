# RIM-like modular recurrent baseline

- Architecture: four GRUCell modules; the top two input gates update per step.
- Claim boundary: a small modular recurrent equivalent inspired by RIMs, not an exact
  reproduction of the paper's attention, communication, or training recipe.
- Reset/context: module state resets per episode and processing is causal.
- Limitation: reduced CPU integration run; dev quality matching was not achieved.
