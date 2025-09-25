from app.reports.html import render_html_report


def test_html_report_renders_findings():
    snapshot = {
        "id": 1,
        "normalized_json": {"policies": [{}]},
        "device": {"hostname": "edge-fw-01"},
    }
    findings = [
        {"type": "any_any", "severity": "high", "summary": "Rule allows any"}
    ]

    html = render_html_report(snapshot, findings)
    assert "Snapshot Report" in html
    assert "Rule allows any" in html
