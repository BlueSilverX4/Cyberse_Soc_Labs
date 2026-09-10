#!/usr/bin/env python3
import json
import os
import time
import statistics
from pathlib import Path

class IgnisterAttackDetector:
    """
    @Ignister Multi-Attribute Threat Classification Engine.
    Maps raw telemetry events into 6 Cyberse Attack Attributes:
      - DARK  : Credential Dumping / Auth Abuse
      - FIRE  : High-Volume Exfiltration / Network Spikes
      - WATER : SQLi / Web Application Injection
      - EARTH : Port Scanning / Reconnaissance
      - WIND  : DDoS / Rapid Session Flooding
      - LIGHT : Malware Dropper / Command & Control Execution
    """

    ATTRIBUTE_MAP = {
        "AUTH_FAILURE": ("DARK", "Credential/Auth Abuse"),
        "EXFIL": ("FIRE", "High-Volume Data Exfiltration"),
        "INJECTION": ("WATER", "SQLi/Command Injection"),
        "SCAN": ("EARTH", "Port Scan/Reconnaissance"),
        "FLOOD": ("WIND", "DDoS/Session Flood"),
        "MALWARE": ("LIGHT", "Malware Dropper/C2 Execution")
    }

    def __init__(self, ingest_dir="telemetry/ingest"):
        self.ingest_dir = Path(ingest_dir)
        self.events = []
        self.detected_threats = []
        self.attribute_counts = {attr: 0 for attr, _ in self.ATTRIBUTE_MAP.values()}

    def load_telemetry(self):
        """Ingests mock log stream from telemetry/ingest/."""
        self.ingest_dir.mkdir(parents=True, exist_ok=True)
        mock_file = self.ingest_dir / "ignister_stream.json"

        if not mock_file.exists():
            mock_stream = [
                {"event_id": "IGN-01", "timestamp": time.time(), "src_ip": "192.168.1.50", "type": "AUTH_FAILURE", "details": "10 failed SSH logins"},
                {"event_id": "IGN-02", "timestamp": time.time()+1, "src_ip": "10.0.4.12", "type": "EXFIL", "bytes": 250000000},
                {"event_id": "IGN-03", "timestamp": time.time()+2, "src_ip": "172.16.0.88", "type": "INJECTION", "details": "' OR 1=1 --"},
                {"event_id": "IGN-04", "timestamp": time.time()+3, "src_ip": "192.168.1.50", "type": "SCAN", "details": "SYN scan on 1000 ports"},
                {"event_id": "IGN-05", "timestamp": time.time()+4, "src_ip": "10.0.4.15", "type": "MALWARE", "details": "Exec: reverse_shell.elf"},
            ]
            with open(mock_file, "w", encoding="utf-8") as f:
                json.dump(mock_stream, f, indent=2)

        with open(mock_file, "r", encoding="utf-8") as f:
            self.events = json.load(f)
        print(f"[+] Successfully loaded {len(self.events)} events from {mock_file}")

    def analyze_attributes(self):
        """Evaluates and tags incoming events with @Ignister Cyberse Attributes."""
        print("\n--- [@Ignister Threat Attribute Analysis] ---")
        for evt in self.events:
            evt_type = evt.get("type", "UNKNOWN")
            if evt_type in self.ATTRIBUTE_MAP:
                attr_code, description = self.ATTRIBUTE_MAP[evt_type]
                self.attribute_counts[attr_code] += 1
                
                threat = {
                    "event_id": evt["event_id"],
                    "src_ip": evt["src_ip"],
                    "ignister_attribute": attr_code,
                    "classification": description,
                    "raw_event": evt
                }
                self.detected_threats.append(threat)
                print(f"[!] Threat Detected | Attribute: [{attr_code}] | Src: {evt['src_ip']} | Type: {description}")

    def export_results(self, output_path="telemetry/ignister_alerts.json"):
        """Outputs classified threats and attribute breakdown to JSON."""
        out_file = Path(output_path)
        out_file.parent.mkdir(parents=True, exist_ok=True)

        payload = {
            "timestamp": time.time(),
            "total_threats": len(self.detected_threats),
            "attribute_summary": self.attribute_counts,
            "threats": self.detected_threats
        }

        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

        print(f"\n[+] Exported @Ignister threat report to {output_path}")


if __name__ == "__main__":
    detector = IgnisterAttackDetector()
    detector.load_telemetry()
    detector.analyze_attributes()
    detector.export_results()
