# Dependency and License Record

## C04 optional learned stack — verified 2026-08-23

PyTorch and NumPy are isolated in the `learned` optional extra and are not core runtime
dependencies. The offline CPU smoke and main profiles ran locally with PyTorch 2.13.0+cpu and
NumPy 2.5.2. C04 adds no PyTorch Geometric, remote tracker, hosted storage, or model API.

| Package | Local role | License boundary |
|---|---|---|
| PyTorch 2.13.0+cpu | encoder, router, recurrent selected-subgraph update, training/checkpoint | upstream BSD-3-Clause plus bundled component notices |
| NumPy 2.5.2 | optional learned-stack compatibility; no core import | upstream BSD-3-Clause |

The repository does not redistribute either wheel. Exact release packaging/notices remain a
C10 responsibility.

## C05 optional learned stack — reviewed 2026-08-23

PyTorch `2.13.0` is pinned in `requirements-learned.lock` and isolated in the `learned`
optional extra. The tested local build was `2.13.0+cpu` on Python 3.13.3. PyTorch's
upstream v2.13.0 license permits redistribution under three conditions and includes
component copyright notices; it is recorded as BSD-style/3-clause in this project.
Official source: <https://github.com/pytorch/pytorch/blob/v2.13.0/LICENSE>.

The baseline runtime performs no network access and uses one CPU thread in committed
profiles. Core `[project].dependencies` remains empty.

## C07 optional spiking stack — reviewed 2026-08-23

Core SparkBrain remains dependency-light. These packages are isolated in the `spiking`
optional extra and are not imported until the C07 backend is instantiated.

| Package | Status | Official compatibility evidence | License | Local verification |
|---|---|---|---|---|
| snnTorch 1.0.0 | selected | Official docs describe PyTorch integration, LIF recurrent units, CPU operation, and installation after PyTorch. They do not publish a bounded Python/PyTorch version matrix, so broader compatibility is not inferred. | MIT source; docs CC BY-SA 3.0 | Python 3.13.3, PyTorch 2.13.0+cpu, NumPy 2.5.2, snnTorch 1.0.0 import and LIF step passed |
| Norse | considered | Current official metadata requires Python >=3.10, torch >=2.2.0, torchvision >=0.15.0 and classifies Python 3.10–3.13. | LGPL-3.0 | not installed or executed for C07 |
| PyTorch 2.13.0+cpu | selected substrate | Current upstream metadata requires Python >=3.10. | main project BSD-3-Clause; bundled components have an upstream SPDX expression | CPU tensor and snnTorch LIF execution passed |

Official references:

- https://snntorch.readthedocs.io/en/latest/
- https://github.com/jeshraghian/snntorch
- https://github.com/jeshraghian/snntorch/blob/master/LICENSE
- https://norse.github.io/norse/pages/installing.html
- https://github.com/norse/norse/blob/main/pyproject.toml
- https://github.com/norse/norse/blob/main/LICENSE

snnTorch was selected because its exact local CPU/PyTorch combination was import-tested
and its source license is MIT. Norse remains an optional alternative.

## Implementation deviation

C07 implements an snnTorch LIF sensory encoder but retains the evidence graph,
hypothesis dynamics, Coalition, ignition, broadcast, and Workspace as rate/algorithmic
components. It is explicitly hybrid. A fully spiking recurrent mapping and
surrogate-gradient or local-plasticity comparison were not implemented.
