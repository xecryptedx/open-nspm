from __future__ import annotations

from datetime import datetime
from typing import Any


def render_html_report(
    snapshot: dict[str, Any], findings: list[dict[str, Any]], diff: dict[str, Any] | None = None
) -> str:
    device = snapshot.get("device", {})
    policies = snapshot.get("normalized_json", {}).get("policies", [])
    diff_summary = diff.get("summary", {}).get("policies", {}) if diff else {}
    generated_at = datetime.utcnow().isoformat()

    rows = "".join(
        f"<tr><td class='border px-2 py-1'>{f.get('type')}</td>"
        f"<td class='border px-2 py-1'>{f.get('severity')}</td>"
        f"<td class='border px-2 py-1'>{f.get('summary')}</td></tr>"
        for f in findings
    ) or "<tr><td colspan='3' class='border px-2 py-2 text-center text-gray-500'>No findings</td></tr>"

    return f"""
<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <title>OpenNSPM Snapshot Report</title>
  <script src=\"https://cdn.tailwindcss.com\"></script>
</head>
<body class=\"bg-slate-100 text-slate-900\">
  <main class=\"max-w-4xl mx-auto py-10\">
    <header class=\"mb-6\">
      <h1 class=\"text-3xl font-semibold\">Snapshot Report</h1>
      <p class=\"text-sm text-slate-600\">Generated at {generated_at}Z</p>
      <div class=\"mt-2 rounded bg-white p-4 shadow\">
        <p><strong>Device:</strong> {device.get('hostname', 'Unknown')}</p>
        <p><strong>Snapshot ID:</strong> {snapshot.get('id')}</p>
        <p><strong>Policy Count:</strong> {len(policies)}</p>
        <p><strong>Diff:</strong> Added {diff_summary.get('added', 0)}, Removed {diff_summary.get('removed', 0)}, Modified {diff_summary.get('modified', 0)}</p>
      </div>
    </header>
    <section class=\"rounded bg-white shadow\">
      <h2 class=\"border-b px-4 py-2 text-xl font-semibold\">Findings</h2>
      <table class=\"w-full border-collapse\">
        <thead>
          <tr class=\"bg-slate-200\"><th class=\"border px-2 py-1 text-left\">Type</th><th class=\"border px-2 py-1 text-left\">Severity</th><th class=\"border px-2 py-1 text-left\">Summary</th></tr>
        </thead>
        <tbody>{rows}</tbody>
      </table>
    </section>
  </main>
</body>
</html>
"""
