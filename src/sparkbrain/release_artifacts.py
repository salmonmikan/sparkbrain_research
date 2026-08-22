from __future__ import annotations

import csv
import html
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from .release import (
    _canonical_json,
    declared_project_license,
    project_license_selected,
    sha256_file,
    validate_evidence_map,
)

PRIMARY_INPUTS = (
    "artifacts/benchmarks/benchmark_aggregate.csv",
    "artifacts/phase1/c02-main-1000/aggregate/metrics.json",
    "artifacts/phase2/learned-routing-v1/main/summary.json",
    "artifacts/spiking/c07_comparison.json",
)


def source_revision(root: Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _load_json(root: Path, relative: str) -> Any:
    return json.loads((root / relative).read_text(encoding="utf-8"))


def build_evidence_map(root: Path) -> dict[str, Any]:
    entries = [
        {
            "id": "EV-C01-REFERENCE",
            "status": "accepted",
            "claim_ids": ["CL-001", "CL-002", "CL-005", "CL-011"],
            "run_ids": ["R0003"],
            "artifacts": ["artifacts/demo/trace.json", "artifacts/demo/checkpoint.json"],
            "boundary": "Deterministic implementation and replay evidence only.",
        },
        {
            "id": "EV-C02-CONTROLLED",
            "status": "negative",
            "claim_ids": ["CL-003", "CL-004", "CL-006", "CL-007"],
            "run_ids": ["R0006"],
            "artifacts": [
                "artifacts/phase1/c02-main-1000/run_manifest.json",
                "artifacts/phase1/c02-main-1000/aggregate/metrics.json",
                "artifacts/phase1/c02-main-1000/aggregate/confidence_intervals.json",
            ],
            "boundary": "Controlled synthetic E2 evidence; MultiObjectWorld is a retained failure.",
        },
        {
            "id": "EV-C04-LEARNED",
            "status": "negative",
            "claim_ids": ["CL-004", "CL-007"],
            "run_ids": ["R0008"],
            "artifacts": [
                "artifacts/phase2/learned-routing-v1/main/summary.json",
                "artifacts/phase2/learned-routing-v1/main/manifest-evidence.json",
                "artifacts/phase2/learned-routing-v1/main/negative-findings.json",
            ],
            "boundary": (
                "Controlled held-out result with dead/overloaded modules; no superiority claim."
            ),
        },
        {
            "id": "EV-C05-CHECKPOINT",
            "status": "pending",
            "claim_ids": ["CL-003", "CL-004", "CL-007"],
            "run_ids": [],
            "artifacts": [],
            "boundary": (
                "C05 is not integrated. Public evidence requires a dev-only encoder vocabulary/"
                "feature manifest whose hash and input dimension match every selected checkpoint."
            ),
        },
        {
            "id": "EV-C06-FOUNDATION",
            "status": "pending",
            "claim_ids": ["CL-003", "CL-004", "CL-007"],
            "run_ids": [],
            "artifacts": [
                "configs/external_validation/foundation.json",
                "schemas/external-evaluation-v0.2.schema.json",
            ],
            "boundary": (
                "Foundation only. External model execution and strict C05 encoder-state/hash "
                "validation are pending."
            ),
        },
        {
            "id": "EV-C07-SPIKING",
            "status": "accepted",
            "claim_ids": ["CL-009"],
            "run_ids": ["R0005", "R0007"],
            "artifacts": [
                "artifacts/spiking/c07_comparison.json",
                "artifacts/spiking/rate_trace.json",
                "artifacts/spiking/spike_trace.json",
            ],
            "boundary": "Reduced sensory-LIF hybrid canonical equivalence only.",
        },
        {
            "id": "EV-C08-PLASTICITY",
            "status": "negative",
            "claim_ids": ["CL-008"],
            "run_ids": ["R0010"],
            "artifacts": [
                "artifacts/phase3/structural-plasticity-v1/main/summary.json",
                "artifacts/phase3/structural-plasticity-v1/main/gate-matrix.json",
                "artifacts/phase3/structural-plasticity-v1/main/input-hashes.json",
                "artifacts/phase3/structural-plasticity-v1/main/negative-findings.json",
            ],
            "boundary": (
                "Bounded mechanism acceptance with failed decisiveness, fertility, and "
                "specificity gates; CL-008 remains E0 and no emergent-organ claim is permitted."
            ),
        },
        {
            "id": "EV-C09-PRIOR-ART",
            "status": "accepted",
            "claim_ids": ["CL-001", "CL-002", "CL-003", "CL-005", "CL-009"],
            "run_ids": [],
            "artifacts": [
                "docs/research/literature_matrix.csv",
                "docs/research/claim_challenge_report.md",
            ],
            "boundary": (
                "Bounded search and adversarial audit; absence of a match is not novelty proof."
            ),
        },
    ]
    result = {
        "schema_version": "c10-evidence-map-v1",
        "source_revision": source_revision(root),
        "entries": entries,
    }
    problems = validate_evidence_map(root, result)
    if problems:
        raise ValueError("invalid generated evidence map: " + "; ".join(problems))
    return result


def primary_rows(root: Path) -> list[dict[str, str]]:
    benchmark_path = root / PRIMARY_INPUTS[0]
    with benchmark_path.open(encoding="utf-8", newline="") as handle:
        benchmark = list(csv.DictReader(handle))
    sparkbrain = next(row for row in benchmark if row["model"] == "sparkbrain")
    phase1 = _load_json(root, PRIMARY_INPUTS[1])
    switch = next(
        row
        for row in phase1
        if row["world"] == "switchworld" and row["condition"] == "full"
    )
    multi = next(
        row
        for row in phase1
        if row["world"] == "multi_object_world" and row["condition"] == "full"
    )
    learned = _load_json(root, PRIMARY_INPUTS[2])["held_out"]
    spiking = _load_json(root, PRIMARY_INPUTS[3])
    return [
        {
            "result": "Phase-0 reference",
            "run": "R0001",
            "accuracy": f"{float(sparkbrain['accuracy_all_steps']):.4f}",
            "coverage": f"{float(sparkbrain['coverage']):.4f}",
            "boundary": "hand-authored software validation",
        },
        {
            "result": "C02 SwitchWorld",
            "run": "R0006",
            "accuracy": f"{float(switch['accuracy_all_steps']):.4f}",
            "coverage": f"{float(switch['coverage']):.4f}",
            "boundary": "controlled synthetic E2",
        },
        {
            "result": "C02 MultiObjectWorld",
            "run": "R0006",
            "accuracy": f"{float(multi['accuracy_all_steps']):.4f}",
            "coverage": f"{float(multi['coverage']):.4f}",
            "boundary": "retained negative result",
        },
        {
            "result": "C04 learned held-out",
            "run": "R0008",
            "accuracy": f"{float(learned['accuracy']):.4f}",
            "coverage": f"{float(learned['coverage']):.4f}",
            "boundary": "60 controlled episodes; load collapse retained",
        },
        {
            "result": "C07 hybrid canonical",
            "run": "R0005",
            "accuracy": "1.0000" if all(spiking["checks"].values()) else "0.0000",
            "coverage": "n/a",
            "boundary": "9 frozen behavioral checks, one scenario",
        },
    ]


def render_primary_table(rows: list[dict[str, str]]) -> str:
    lines = [
        "# Frozen primary result subset",
        "",
        "This is the bounded release smoke subset, not the full evaluation suite.",
        "",
        "| Result | Run | Accuracy/check fraction | Coverage | Evidence boundary |",
        "|---|---|---:|---:|---|",
    ]
    lines.extend(
        f"| {row['result']} | {row['run']} | {row['accuracy']} | {row['coverage']} | "
        f"{row['boundary']} |"
        for row in rows
    )
    return "\n".join(lines) + "\n"


def render_primary_figure(rows: list[dict[str, str]]) -> str:
    bars = []
    for index, row in enumerate(rows):
        value = float(row["accuracy"])
        width = round(value * 400, 2)
        y = 35 + index * 42
        bars.append(
            f'<text x="10" y="{y}" font-size="13">{html.escape(row["result"])}</text>'
            f'<rect x="190" y="{y - 15}" width="{width}" height="18" fill="#3569a8" />'
            f'<text x="{195 + width}" y="{y}" font-size="12">{value:.4f}</text>'
        )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="680" height="250" '
        'role="img" aria-labelledby="title desc">\n'
        '<title id="title">Frozen primary release subset</title>\n'
        '<desc id="desc">Accuracy or frozen behavioral-check fraction. Values have different '
        'evidence boundaries and are not a ranking.</desc>\n'
        + "\n".join(bars)
        + "\n</svg>\n"
    )


def render_markdown_html(markdown: str, *, title: str) -> str:
    body: list[str] = []
    in_list = False
    for raw in markdown.splitlines():
        line = raw.rstrip()
        if line.startswith("#"):
            if in_list:
                body.append("</ul>")
                in_list = False
            level = min(len(line) - len(line.lstrip("#")), 6)
            body.append(f"<h{level}>{html.escape(line[level:].strip())}</h{level}>")
        elif line.startswith("- "):
            if not in_list:
                body.append("<ul>")
                in_list = True
            body.append(f"<li>{html.escape(line[2:])}</li>")
        elif not line:
            if in_list:
                body.append("</ul>")
                in_list = False
        else:
            if in_list:
                body.append("</ul>")
                in_list = False
            body.append(f"<p>{html.escape(line)}</p>")
    if in_list:
        body.append("</ul>")
    return (
        "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
        f"<title>{html.escape(title)}</title><style>body{{max-width:900px;margin:2rem auto;"
        "font:16px/1.5 system-ui;color:#17202a}}code{background:#eef;padding:.1rem}</style>"
        "</head><body>\n"
        + "\n".join(body)
        + "\n</body></html>\n"
    )


def build_sbom(root: Path) -> dict[str, Any]:
    package_rows = []
    for raw in (root / "requirements-release.lock").read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "==" not in line:
            continue
        name, version = line.split("==", 1)
        package_rows.append(
            {
                "SPDXID": f"SPDXRef-Package-{re.sub(r'[^A-Za-z0-9.-]', '-', name)}",
                "name": name,
                "versionInfo": version,
                "downloadLocation": "NOASSERTION",
                "licenseConcluded": "NOASSERTION",
                "licenseDeclared": "NOASSERTION",
            }
        )
    selected = project_license_selected(root)
    project_license = declared_project_license(root) if selected else "NOASSERTION"
    project_package = {
        "SPDXID": "SPDXRef-Package-SparkBrain",
        "name": "sparkbrain-research",
        "versionInfo": "0.2.1",
        "downloadLocation": "NOASSERTION",
        "licenseConcluded": project_license,
        "licenseDeclared": project_license,
    }
    if not selected:
        project_package["comment"] = "Project license is intentionally owner-blocked."
    return {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": "sparkbrain-research-v0.2.1-release-candidate",
        "documentNamespace": f"urn:sparkbrain:sbom:{source_revision(root)}",
        "creationInfo": {"creators": ["Tool: scripts/generate_release_artifacts.py"]},
        "packages": [
            project_package,
            *package_rows,
        ],
    }


def build_negative_appendix(root: Path) -> str:
    ledger = (root / "docs/RESULTS_LEDGER.md").read_text(encoding="utf-8")
    run_titles = re.findall(r"^## \d{4}-\d{2}-\d{2} — (R\d{4}) — (.+)$", ledger, re.MULTILINE)
    lines = [
        "# Negative-result appendix",
        "",
        "Generated from the append-only results ledger. This index does not replace the full "
        "entries.",
        "",
        "| Run | Ledger title | Release interpretation |",
        "|---|---|---|",
    ]
    boundaries = {
        "R0001": "Accumulator remained competitive; no general advantage.",
        "R0005": "Single hybrid scenario and parameter-sensitive no-spike failure.",
        "R0006": "MultiObjectWorld coverage was zero; duplicate signals changed activation.",
        "R0008": "Smoke was below chance; dead/overloaded learned modules remained.",
        "R0010": "Structural mechanisms ran, but causal specialization gates failed.",
    }
    for run_id, title in run_titles:
        interpretation = boundaries.get(run_id, "No grade increase inferred.")
        lines.append(f"| {run_id} | {title} | {interpretation} |")
    lines.extend(
        [
            "",
            "## Pending integration",
            "",
            "- C05 matched baselines and checkpoint-matched dev-only encoder manifests are not "
            "present in this candidate.",
            "- C06 external execution remains blocked at the model gate; only foundation code "
            "is present.",
            "- The owner has not selected a project license; public release remains blocked.",
        ]
    )
    return "\n".join(lines) + "\n"


def claim_audit(root: Path, evidence_map: dict[str, Any]) -> dict[str, Any]:
    inspected = [
        "README.md",
        "docs/ARTIFACT_EVALUATION_GUIDE.md",
        "docs/MODEL_CARD.md",
        "docs/NEGATIVE_RESULTS_APPENDIX.md",
        "docs/PROJECT_STATUS.md",
        "docs/SECURITY_PRIVACY_REVIEW.md",
        "docs/SYSTEM_CARD.md",
        "docs/TECHNICAL_REPORT_v0.2.1.md",
        "docs/TECHNICAL_REPORT_v0.2.1.html",
        "artifacts/release/primary_results.md",
        "artifacts/release/primary_results.svg",
    ]
    prohibited = {
        "human brain reproduction": r"\b(reproduces?|reproduced) the human brain\b",
        "consciousness": r"\b(system|sparkbrain) is conscious\b",
        "AGI": r"\b(this|sparkbrain) is (an )?AGI\b",
        "novelty proof": r"\b(completely novel|proved novel|proves novelty)\b",
        "energy gain": r"\b(proves?|demonstrates?) (lower )?energy\b",
    }
    findings = []
    for relative in inspected:
        text = (root / relative).read_text(encoding="utf-8")
        for label, pattern in prohibited.items():
            if re.search(pattern, text, re.IGNORECASE):
                findings.append({"file": relative, "rule": label})
    pending = [entry["id"] for entry in evidence_map["entries"] if entry["status"] == "pending"]
    return {
        "schema_version": "c10-claim-audit-v1",
        "inspected_files": inspected,
        "prohibited_wording_findings": findings,
        "pending_evidence_entries": pending,
        "status": "pass-with-pending-evidence" if not findings else "fail",
    }


def generate_release_artifacts(root: Path, *, output_root: Path | None = None) -> dict[str, str]:
    destination = output_root or root
    release_dir = destination / "artifacts/release"
    release_dir.mkdir(parents=True, exist_ok=True)
    rows = primary_rows(root)
    table = release_dir / "primary_results.md"
    figure = release_dir / "primary_results.svg"
    table.write_text(render_primary_table(rows), encoding="utf-8", newline="\n")
    figure.write_text(render_primary_figure(rows), encoding="utf-8", newline="\n")
    input_hashes = {path: sha256_file(root / path) for path in PRIMARY_INPUTS}
    subset = {
        "schema_version": "c10-primary-subset-v1",
        "selection_status": "immutable-smoke-subset",
        "full_evaluation": False,
        "warning": "This smoke subset must not be described as the full C02-C08 evaluation.",
        "inputs": input_hashes,
        "outputs": {
            "artifacts/release/primary_results.md": sha256_file(table),
            "artifacts/release/primary_results.svg": sha256_file(figure),
        },
    }
    (release_dir / "primary_subset.json").write_text(
        _canonical_json(subset), encoding="utf-8", newline="\n"
    )
    evidence = build_evidence_map(root)
    (release_dir / "evidence_map.json").write_text(
        _canonical_json(evidence), encoding="utf-8", newline="\n"
    )
    (release_dir / "sbom.spdx.json").write_text(
        _canonical_json(build_sbom(root)), encoding="utf-8", newline="\n"
    )
    negative = destination / "docs/NEGATIVE_RESULTS_APPENDIX.md"
    negative.parent.mkdir(parents=True, exist_ok=True)
    negative.write_text(build_negative_appendix(root), encoding="utf-8", newline="\n")
    report_source = root / "docs/TECHNICAL_REPORT_v0.2.1.md"
    report_html = destination / "docs/TECHNICAL_REPORT_v0.2.1.html"
    report_html.write_text(
        render_markdown_html(
            report_source.read_text(encoding="utf-8"), title="SparkBrain v0.2.1 technical report"
        ),
        encoding="utf-8",
        newline="\n",
    )
    audit = claim_audit(destination, evidence)
    (release_dir / "claim_audit.json").write_text(
        _canonical_json(audit), encoding="utf-8", newline="\n"
    )
    provenance = {
        "schema_version": "c10-provenance-v1",
        "generator": "scripts/generate_release_artifacts.py",
        "source_revision": source_revision(root),
        "products": {
            "artifacts/release/primary_results.md": list(PRIMARY_INPUTS),
            "artifacts/release/primary_results.svg": list(PRIMARY_INPUTS),
            "docs/TECHNICAL_REPORT_v0.2.1.html": ["docs/TECHNICAL_REPORT_v0.2.1.md"],
            "docs/NEGATIVE_RESULTS_APPENDIX.md": ["docs/RESULTS_LEDGER.md"],
            "artifacts/release/sbom.spdx.json": [
                "pyproject.toml",
                "requirements-release.lock",
            ],
        },
    }
    (release_dir / "provenance.json").write_text(
        _canonical_json(provenance), encoding="utf-8", newline="\n"
    )
    return {
        relative: sha256_file(destination / relative)
        for relative in (
            "artifacts/release/primary_results.md",
            "artifacts/release/primary_results.svg",
            "artifacts/release/primary_subset.json",
            "artifacts/release/evidence_map.json",
            "artifacts/release/sbom.spdx.json",
            "artifacts/release/claim_audit.json",
            "artifacts/release/provenance.json",
            "docs/NEGATIVE_RESULTS_APPENDIX.md",
            "docs/TECHNICAL_REPORT_v0.2.1.html",
        )
    }
