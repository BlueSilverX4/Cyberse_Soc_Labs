#!/usr/bin/env python3
import json
from pathlib import Path

def generate_html_report(json_path="reports/soc_executive_summary.json", output_path="reports/soc_dashboard.html"):
    json_file = Path(json_path)
    if not json_file.exists():
        print(f"[!] Summary JSON {json_path} not found.")
        return

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    playbooks_html = "".join([f"<li><code>{pb}</code> - Executed and Contained</li>" for pb in data.get("playbooks_triggered", [])])

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Cyberse SOC Executive Dashboard</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 40px; }}
        .card {{ background-color: #1e293b; border-radius: 8px; padding: 24px; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5); }}
        h1 {{ color: #38bdf8; border-bottom: 2px solid #334155; padding-bottom: 10px; }}
        .metric-grid {{ display: flex; gap: 20px; }}
        .metric-box {{ background-color: #334155; padding: 15px; border-radius: 6px; flex: 1; text-align: center; }}
        .metric-value {{ font-size: 2em; font-weight: bold; color: #4ade80; }}
        ul {{ line-height: 1.8; }}
    </style>
</head>
<body>
    <h1>🛡️ Cyberse SOC Executive Performance Dashboard</h1>
    <div class="card">
        <div class="metric-grid">
            <div class="metric-box">
                <div>Threats Contained</div>
                <div class="metric-value">{data.get("total_threats_contained")}</div>
            </div>
            <div class="metric-box">
                <div>Mean Time to Respond (MTTR)</div>
                <div class="metric-value">{data.get("mean_time_to_respond_seconds")}s</div>
            </div>
            <div class="metric-box">
                <div>SOC Readiness Score</div>
                <div class="metric-value">{data.get("soc_readiness_score")}</div>
            </div>
        </div>
    </div>
    <div class="card">
        <h3>Triggered Playbook Audit</h3>
        <ul>
            {playbooks_html}
        </ul>
    </div>
</body>
</html>
"""

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as out_f:
        out_f.write(html_content)

    print(f"[+] Executive HTML Dashboard generated at {output_path}")

if __name__ == "__main__":
    generate_html_report()
