#!/usr/bin/env python3
import time

class FirewallIntegration:
    @staticmethod
    def block_ip(ip):
        rule = f"iptables -A INPUT -s {ip} -j DROP"
        return {"status": "SUCCESS", "command": rule}

class IdentityIntegration:
    @staticmethod
    def revoke_user_sessions(ip):
        return {"status": "SUCCESS", "revoked_ip": ip, "timestamp": time.time()}

class ITSMIntegration:
    @staticmethod
    def open_ticket(event_id, priority="CRITICAL"):
        ticket_id = f"INC-{int(time.time())}-{event_id}"
        return {"status": "OPEN", "ticket_id": ticket_id, "priority": priority}
