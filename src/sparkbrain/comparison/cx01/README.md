# CX01 common comparator contract

This directory is the shared, architecture-neutral CX01 comparison layer.

The checkpoint before G6/G7/G8 implementation freezes the following development contracts:

- anonymous external event + timestamp input;
- no evaluator context ID, target, semantic label, or reward leakage;
- balanced chronological exposure scheduling;
- six world families: high-order, timing, cycle, branch, selectivity, and loop;
- non-compensatory family scoring;
- descriptive-only resource accounting;
- explicit comparator privilege disclosure;
- historical G3 preserved as a first-order transition anchor.

G6/G7/G8 implementations may consume these contracts but must not modify them from architecture-specific branches merely to improve outcomes.
