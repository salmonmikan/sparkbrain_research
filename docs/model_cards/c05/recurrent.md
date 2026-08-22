# GRU and LSTM baselines

- Role: causal recurrent learned competitors with per-episode reset.
- Information: common observation-only encoder; no evaluator target is an input.
- Capacity: architecture-body parameter count is matched within ±2% by performance-blind
  hidden-size search; no padding reserve is counted.
- Training: Adam, deterministic CPU execution, fixed steps and paired episode order.
- Abstention: confidence threshold selected on dev only; coverage is separate from accuracy.
- Limitation: committed acceptance run is deliberately short and quality matching failed.
