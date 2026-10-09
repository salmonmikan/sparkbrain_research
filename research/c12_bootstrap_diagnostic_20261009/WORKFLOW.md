# One prospective same-environment diagnostic

Repository salmonmikan/sparkbrain_research; branch probe/c12-bootstrap-diagnostic-20261009T1335Z.
Commit message: probe: c12-bootstrap-diagnostic-20261009T1335Z ONE_SHOT OBSERVATION_ONLY
Source payload: research/c12_bootstrap_diagnostic_20261009; new workflow .github/workflows/c12_bootstrap_diagnostic_20261009.yml.

Identical runtime/provisioning boundaries to the approved initial observation:
official pinned checkout/setup-python, exact ordinary CPython 3.14.8 x64,
ubuntu-24.04, one-minute whole-job timeout, one supervised -I -S -B target child,
15s CPU, 512MiB address space, 30s stream deadline, outer timeout 35s + 2s grace,
64MiB explicit collector reads/32MiB file cap and 4MiB combined target/log receipt
cap. Runtime loader and setup I/O are outside collector read bounds; queue and
provisioning precede or consume job budget. No OS network/fork containment claim.
Only bound prefix/lib LD_LIBRARY_PATH reaches target; no runner environment.
Bounded public stdout, zero artifacts. No package installs beyond official setup;
no retries, reruns, repairs, alternate runtime, science, owner construction,
native queries, Phase B or old trusted-pin changes.

Create the new branch directly at one complete reviewed commit containing source,
workflow and two exact branch-only exclusions. Do not expose a temporary main-head
branch. No PR/merge. Recheck main and workflow directory/blobs immediately before
publication; saved originals are pinned to main 3313974cf0cf7389d7bf1e3f714eb55e0721c0dd,
independently read by the previous publisher at 13:31 UTC. Preparation is offline.
The parent must explicitly allocate one of the newly approved three jobs before
publication. This candidate itself has consumed no job allowance.
An INCOMPLETE result is terminal and preserves the redacted checkpoint; it does
not authorize broader roots or another run. Diagnose from that result first.
