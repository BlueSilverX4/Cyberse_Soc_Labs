# 05-Cyberse SOC Executive Dashboard

Executive reporting and metrics aggregation engine for the Cyberse SOC framework. This module ingests SOAR execution logs from `04-codetalker-soar-playbooks` to calculate real-time Security Operations metrics, including total threat containment counts, Mean Time to Respond (MTTR), and SOC readiness scores, outputting both JSON metrics and an HTML executive summary.

---

## 📁 Repository Structure

```text
05-cyberse-soc-dashboard/
├── reports/
│   ├── soc_dashboard.html         # Generated HTML visual dashboard
│   ├── soc_dashboard_demo.png     # Dashboard screenshot evidence
│   └── soc_executive_summary.json # Aggregated JSON performance metrics
├── scripts/
│   └── generate_dashboard.sh      # Pipeline execution script
├── src/
│   ├── dashboard_builder.py       # HTML report rendering engine
│   └── metrics_engine.py          # SOAR audit log metric parser
└── templates/
    └── config.json                # Dashboard theme & layout config
📊 Executive Metrics Summary
Mean Time to Respond (MTTR): 0.42 seconds (Automated SOAR baseline)

SOC Readiness Score: 98.5%

Supported Playbooks: PLAYBOOK-DARK, PLAYBOOK-FIRE, PLAYBOOK-WATER, PLAYBOOK-EARTH, PLAYBOOK-LIGHT, PLAYBOOK-WIND

📸 Executive Dashboard Output
🧪 How to Reproduce
Run Full Pipeline:

Bash
./scripts/generate_dashboard.sh
View HTML Dashboard:
Open reports/soc_dashboard.html in any browser.
