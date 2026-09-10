#!/usr/bin/env python3
import json
import time
from pathlib import Path

def generate_simulation_data(output_path="telemetry/ingest/ignister_stream.json"):
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    simulated_events = [
        {"event_id": "IGN-01", "timestamp": time.time(), "src_ip": "192.168.1.50", "type": "AUTH_FAILURE", "details": "10 failed SSH logins"},
        {"event_id": "IGN-02", "timestamp": time.time()+1, "src_ip": "10.0.4.12", "type": "EXFIL", "bytes": 250000000},
        {"event_id": "IGN-03", "timestamp": time.time()+2, "src_ip": "172.16.0.88", "type": "INJECTION", "details": "' OR 1=1 --"},
        {"event_id": "IGN-04", "timestamp": time.time()+3, "src_ip": "192.168.1.50", "type": "SCAN", "details": "SYN scan on 1000 ports"},
        {"event_id": "IGN-05", "timestamp": time.time()+4, "src_ip": "10.0.4.15", "type": "MALWARE", "details": "Exec: reverse_shell.elf"},
        {"event_id": "IGN-06", "timestamp": time.time()+5, "src_ip": "10.0.4.200", "type": "FLOOD", "details": "5000 SYN packets/sec"}
    ]

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(simulated_events, f, indent=2)

    print(f"[+] Simulation completed. Generated {len(simulated_events)} events -> {output_path}")

if __name__ == "__main__":
    generate_simulation_data()
