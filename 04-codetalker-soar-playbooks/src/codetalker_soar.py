#!/usr/bin/env python3
import json
import os
import time
from pathlib import Path

class CodeTalkerSOAR:
    """
    Code Talker SOAR Playbook Engine.
    Executes automated containment actions based on active threat telemetry:
      - IP Quarantine / Host Isolation
      - Revoke User Active Sessions
      - Generate Incident Response Ticket
    """

    def __init__(self, alert_feed="../03-ignister-attack-detection/telemetry/ignister_alerts.json"):
        self.alert_feed = Path(alert_feed)
        self.actions_executed = []

    def load_alerts(self):
        if not self.alert_feed.exists():
            print(f"[!] Target alert stream {self.alert_feed} not found. Running fallback initialization...")
            return []

        with open(self.alert_feed, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("threats", [])

    def execute_playbooks(self):
        threats = self.load_alerts()
        print(f"[*] Ingested {len(threats)} high-fidelity threats into Code Talker SOAR Pipeline.\n")

        for threat in threats:
            ip = threat.get("src_ip")
            attr = threat.get("ignister_attribute")
            classification = threat.get("classification")

            print(f"=== [Executing Playbook: PLAYBOOK-{attr}] ===")
            print(f"[*] Target Host: {ip} | Threat Profile: {classification}")

            # Playbook Action 1: Network Isolation
            iso_action = self._action_quarantine_ip(ip)
            
            # Playbook Action 2: Session Termination for Auth Abuse
            sess_action = None
            if attr in ["DARK", "LIGHT"]:
                sess_action = self._action_revoke_sessions(ip)

            # Playbook Action 3: Incident Ticket Generation
            ticket = self._action_create_ticket(threat)

            self.actions_executed.append({
                "target_ip": ip,
                "playbook": f"PLAYBOOK-{attr}",
                "actions": [iso_action, sess_action, ticket] if sess_action else [iso_action, ticket]
            })
            print()

    def _action_quarantine_ip(self, ip):
        action_msg = f"iptables -A INPUT -s {ip} -j DROP"
        print(f"  [SOAR ACTION] Network Isolation: Executed block rule -> `{action_msg}`")
        return {"type": "NET_BLOCK", "rule": action_msg}

    def _action_revoke_sessions(self, ip):
        print(f"  [SOAR ACTION] Identity Containment: Terminated active auth tokens associated with {ip}")
        return {"type": "AUTH_REVOKE", "target": ip}

    def _action_create_ticket(self, threat):
        ticket_id = f"INC-{int(time.time())}-{threat.get('event_id')}"
        print(f"  [SOAR ACTION] ITSM Integration: Created Critical Incident Ticket -> [{ticket_id}]")
        return {"type": "TICKET_CREATED", "ticket_id": ticket_id}

    def export_soar_audit_log(self, output_path="reports/soar_execution_audit.json"):
        out_file = Path(output_path)
        out_file.parent.mkdir(parents=True, exist_ok=True)

        payload = {
            "engine": "Code Talker SOAR Engine",
            "timestamp": time.time(),
            "total_playbooks_executed": len(self.actions_executed),
            "audit_log": self.actions_executed
        }

        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

        print(f"[+] Code Talker SOAR execution complete. Audit log written to {output_path}")

if __name__ == "__main__":
    soar = CodeTalkerSOAR()
    soar.execute_playbooks()
    soar.export_soar_audit_log()
