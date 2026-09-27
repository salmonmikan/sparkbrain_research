# Continuous scope-revision interaction ablation

This Forge-only harness compares two arms over the same ordered synthetic stream.

- Connected arm: internally routed scope receives the observed-outcome evidence.
- Connection-cut arm: the same router, allocator, coverage guard and transaction
  boundary execute, but scope-local evidence strength is zero and the original
  evidence goes to one Assembly-wide overlay.

The fixture asks whether two observation clusters with contradictory outcomes can
retain separate late-evidence support and recover it when each cluster returns.
It also includes a cue-rich single-cluster negative control where both arms should
behave the same.

The harness accepts no caller scope, regime, episode, truth or evaluator identity.
Observation vectors and exposed outcome values are ordinary task inputs. Queries
run against reconstructed checkpoints so inspection cannot create live caches.

This is a narrow interaction diagnostic, not a benchmark. A difference between
arms supports dependence on the connection only inside this constructed fixture.
It does not establish system superiority, general composition contribution,
scientific novelty, calibrated latent causes or a production SYSTEM_BUILD.

