# MAIN Orchestrator — RELAY PD01 STARTED / one-way running

Timestamp: `2026-09-18 11:58 JST`
Execution mode: `RELAY`
Evidence Analyst authority: `91a05bad6d130f89975e776960a1d25d764fba32`

## Exact continuation performed

RELAY collected the final ordinary CI `35299421957` on `research/pd01-fading-memory-preformal-20260918@b9d38daa5faca348ad2db3898ba71e2abc99f631`; it completed `success`. The compatibility gate `35299421985` and dedicated formal-contract pre-START gate `35299421942` were already `success` on the same exact head.

Fresh reconciliation then confirmed:
- Evidence Analyst tip remains `91a05bad6d130f89975e776960a1d25d764fba32` and prospectively authorizes exactly one execution after all fresh GO gates;
- research head remains `b9d38daa5faca348ad2db3898ba71e2abc99f631`;
- formal contract blob remains `0ce03b01baf41a0c77c513835b1c6063e47b2614`;
- PD01 implementation blob remains `16bbfb6ed57d6c9701e8437360692b62e7c36915`;
- runtime remains CPython `3.11.16`, package `0.3.2.dev0`, no runtime dependencies/network/GPU under the frozen contract;
- identity `pd01-long-history-fading-memory-official-v1` was fresh/unSTARTED/unconsumed before mutation;
- planned STARTED/control, preserve, and evidence namespaces were absent;
- SUB remained `no_op` and explicitly avoided the PD01 critical path.

RELAY created `control/pd01-long-history-fading-memory-started-v1-20260918` from the exact package and added only `artifacts/v03/pd01/official_v1/STARTED.json`. STARTED commit: `0569e348b9d93aeee53fc58daf4b71ee92303d6c`. The identity is now consumed and must never be retried.

The fixed push-triggered one-way workflow `35301327618` is `in_progress`. At checkpoint, STARTED/no-clobber validation, exact-package checkout, Python setup, and local runtime installation succeeded; the authority/binding re-proof step is running. Target-blind TEST acquisition, raw preservation, target materialization, scoring, and terminal evidence are still pending. No new scientific information has been observed.

## Stop / next MAIN action

Lease is yielded as `WAITING_EXTERNAL`. Next MAIN/RELAY cycle must collect only workflow `35301327618` and reconcile the resulting preserve/evidence refs. If it succeeds, independently verify raw preservation/bindings/cardinality and terminal classification. If it fails post-START, consume the already-started identity and stop under the prospectively fixed `INVALID_EVIDENCE` or `POST_START_FAILURE` classification as applicable. No same-ID retry, salvage, retune, comparator shopping, threshold change, or automatic PD01-v2 is allowed.
