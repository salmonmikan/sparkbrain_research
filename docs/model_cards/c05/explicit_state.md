# Explicit-state memory baseline

- Architecture: learned additive log-belief update over a visible state vector.
- Inspection: the current belief state is exposed by the module and probability trace.
- Reset: belief vector resets per episode; no test state crosses episode boundaries.
- Limitation: this is a compact explicit-memory comparator, not an external differentiable
  memory reproduction; the reduced run showed unstable/high loss on some seeds.
