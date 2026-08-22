# Third-party notices for optional Brain Lab tooling

C03 does not add a mandatory runtime dependency to the SparkBrain reference engine. The following direct dependencies are confined to optional `lab` or `dev` extras. Tested versions are recorded in `requirements-lab.lock`.

| Package | C03 role | Tested version | Upstream license | Official source |
|---|---|---:|---|---|
| FastAPI | localhost REST/SSE application | 0.141.1 | MIT | <https://github.com/fastapi/fastapi/blob/master/LICENSE> |
| Uvicorn | loopback ASGI server | 0.52.4 | BSD 3-Clause | <https://github.com/Kludex/uvicorn/blob/main/LICENSE.md> |
| HTTPX | API tests only | 0.28.1 | BSD 3-Clause | <https://github.com/encode/httpx/blob/master/LICENSE.md> |

The bundled Brain Lab frontend uses native HTML, CSS, JavaScript, and SVG. It contains no third-party graph library, CDN asset, hosted font, analytics SDK, or copied browser-side package.

This notice records direct project choices. Installed transitive packages remain governed by their own upstream license files and package metadata.

## Direct development and research dependencies

The release-candidate environment is pinned in `requirements-release.lock`; wheels are not
redistributed. The SPDX-like SBOM records the complete tested snapshot with `NOASSERTION` where
license metadata has not been independently reconciled. Direct project choices are:

| Package | Role | Tested version | Upstream license | Official source |
|---|---|---:|---|---|
| pytest | tests | 9.1.1 | MIT | <https://github.com/pytest-dev/pytest/blob/main/LICENSE> |
| Ruff | lint | 0.16.4 | MIT | <https://github.com/astral-sh/ruff/blob/main/LICENSE> |
| jsonschema | artifact schemas | 4.26.0 | MIT | <https://github.com/python-jsonschema/jsonschema/blob/main/COPYING> |
| NumPy | learned optional stack | 2.5.2 | BSD-3-Clause plus bundled notices | <https://github.com/numpy/numpy/blob/main/LICENSE.txt> |
| PyTorch | learned/spiking optional stack | 2.13.0+cpu | BSD-3-Clause plus bundled component notices | <https://github.com/pytorch/pytorch/blob/main/LICENSE> |
| snnTorch | reduced hybrid backend | 1.0.0 | MIT | <https://github.com/jeshraghian/snntorch/blob/master/LICENSE> |

The project package itself remains `NOASSERTION` because the repository owner has not selected
a license. Third-party licenses do not supply or imply a license for SparkBrain source.

## C06 external evaluation data

| Dataset | C06 role | Pinned revision | Declared license | Official source |
|---|---|---|---|---|
| Belief-R (`CAiRE/belief_r`) | official test-only external evaluation | `3719f5804c63318037465fecf298a7fd78d99121` | CC BY-SA 4.0 on the Hugging Face dataset card | <https://huggingface.co/datasets/CAiRE/belief_r> |

Belief-R text is acquired into a gitignored local cache and is not redistributed in this
repository. The separate `HLTCHKUST/belief-revision` GitHub repository did not display a
repository license when checked on 2026-08-23. Its code is not cloned, imported, executed,
copied, or treated as covered by the dataset-card license.

## Optional C05 learned baseline tooling

| Package | C05 role | Tested version | Upstream license | Official source |
|---|---|---:|---|---|
| PyTorch | CPU GRU/LSTM/Transformer/modular/explicit-state models and profiler substrate | 2.13.0+cpu | BSD-style 3-clause plus bundled component notices | <https://github.com/pytorch/pytorch/blob/v2.13.0/LICENSE> |

PyTorch is not a core runtime dependency and is installed only through the `learned` or
existing optional `spiking` extra.
