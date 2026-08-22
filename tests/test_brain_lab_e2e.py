from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from sparkbrain.lab.app import create_app

STATIC = Path(__file__).parents[1] / "src" / "sparkbrain" / "lab" / "static"


def test_canonical_ui_flow_reaches_cat_toy_cat_and_exposes_evidence(tmp_path) -> None:
    with TestClient(create_app(artifact_root=tmp_path)) as api:
        page = api.get("/")
        assert page.status_code == 200
        run = api.post("/api/runs", json={"seed": 7}).json()
        predictions = []
        for _ in range(7):
            run = api.post(f"/api/runs/{run['run_id']}/step").json()
            predictions.append(run["prediction"])
        assert predictions[1] == "cat"
        assert predictions[4] == "toy"
        assert predictions[6] == "cat"
        cat = run["spark_details"]["hypothesis:cat"]
        assert "event:6:purr" in cat["supports"]


def test_frontend_contains_all_screens_accessibility_and_offline_assets() -> None:
    html = (STATIC / "index.html").read_text(encoding="utf-8")
    js = (STATIC / "app.js").read_text(encoding="utf-8")
    css = (STATIC / "styles.css").read_text(encoding="utf-8")
    for identifier in (
        "brain-field",
        "timeline",
        "belief-panel",
        "workspace",
        "inspector",
        "controls",
        "intervention",
        "comparison",
        "export",
    ):
        assert f'id="{identifier}"' in html
    assert 'aria-label="Functional Spark graph' in html
    assert 'role="status"' in html
    assert "focus-visible" in css
    assert "keydown" in js
    assert "requestAnimationFrame" in js
    combined = html + js + css
    assert 'src="http' not in combined
    assert 'href="http' not in combined
    assert 'fetch("http' not in combined
    assert "fetch(" in js
    assert "innerHTML=`<td>" in js
