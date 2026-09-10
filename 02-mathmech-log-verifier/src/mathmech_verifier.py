#!/usr/bin/env python3
import hashlib
import json
import os
import time
import statistics
from pathlib import Path

class MathmechLogVerifier:
    def __init__(self):
        self.log_chain = []
        self.merkle_tree = []
        self.network_bytes_history = []

    def compute_hash(self, log_entry):
        """Computes SHA-256 hash of a log entry string."""
        return hashlib.sha256(log_entry.encode('utf-8')).hexdigest()

    def add_log(self, log_dict):
        """Appends log, tracks byte metrics, and builds Merkle leaf node."""
        log_str = json.dumps(log_dict, sort_keys=True)
        log_hash = self.compute_hash(log_str)
        
        self.log_chain.append({"log": log_dict, "hash": log_hash})
        self.network_bytes_history.append(log_dict.get("bytes_sent", 0))
        print(f"[+] Log Added | Hash: {log_hash[:16]}... | Bytes: {log_dict.get('bytes_sent')}")

    def build_merkle_root(self):
        """Computes Merkle Root across all current log hashes (Merkle Tree)."""
        if not self.log_chain:
            return None
        
        current_level = [item["hash"] for item in self.log_chain]
        
        while len(current_level) > 1:
            if len(current_level) % 2 != 0:
                current_level.append(current_level[-1]) # Duplicate last hash if odd
            
            next_level = []
            for i in range(0, len(current_level), 2):
                combined = current_level[i] + current_level[i+1]
                next_level.append(self.compute_hash(combined))
            current_level = next_level

        return current_level[0]

    def detect_statistical_anomaly(self, new_bytes, threshold_z=2.0):
        """Mathmech Addition/Division: Uses Z-score to detect traffic spikes."""
        if len(self.network_bytes_history) < 3:
            return False, 0.0 # Need baseline data first
        
        mean = statistics.mean(self.network_bytes_history)
        stdev = statistics.stdev(self.network_bytes_history)
        if stdev == 0:
            return False, 0.0
        
        z_score = (new_bytes - mean) / stdev
        is_anomaly = z_score > threshold_z
        return is_anomaly, z_score

    def verify_log_integrity(self, original_root):
        """Mathmech Subtraction/Multiplication: Verifies hash tree integrity."""
        current_root = self.build_merkle_root()
        if current_root == original_root:
            print(f"[✔] INTEGRITY VERIFIED | Merkle Root: {current_root[:16]}...")
            return True
        else:
            print(f"[x] TAMPER ALERT! Merkle Root Mismatch!")
            print(f"    Expected: {original_root[:16]}...")
            print(f"    Calculated: {current_root[:16]}...")
            return False

    def export_audit_trail(self, baseline_root, output_path="telemetry/verification_audit.json"):
        """Outputs the Merkle root audit trail and log chain to JSON."""
        out_file = Path(output_path)
        out_file.parent.mkdir(parents=True, exist_ok=True)

        payload = {
            "timestamp": time.time(),
            "baseline_merkle_root": baseline_root,
            "calculated_merkle_root": self.build_merkle_root(),
            "integrity_status": self.build_merkle_root() == baseline_root,
            "total_logs": len(self.log_chain),
            "log_chain": self.log_chain
        }

        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        print(f"[+] Audit trail successfully written to {output_path}")


if __name__ == "__main__":
    verifier = MathmechLogVerifier()
    
    print("--- [1] Ingesting Normal System Telemetry ---")
    sample_logs = [
        {"timestamp": time.time(), "src_ip": "10.0.0.5", "action": "LOGIN", "bytes_sent": 512},
        {"timestamp": time.time()+1, "src_ip": "10.0.0.5", "action": "GET_FILE", "bytes_sent": 480},
        {"timestamp": time.time()+2, "src_ip": "10.0.0.12", "action": "LOGIN", "bytes_sent": 530},
        {"timestamp": time.time()+3, "src_ip": "10.0.0.5", "action": "GET_FILE", "bytes_sent": 505},
    ]
    
    for log in sample_logs:
        verifier.add_log(log)

    print("\n--- [2] Mathmech Statistical Anomaly Check ---")
    exfiltration_log = {"timestamp": time.time()+4, "src_ip": "10.0.0.5", "action": "EXFIL", "bytes_sent": 85000}
    is_anomaly, z_score = verifier.detect_statistical_anomaly(exfiltration_log["bytes_sent"])
    
    print(f"[!] Analyzing outbound transfer: {exfiltration_log['bytes_sent']} bytes")
    print(f"[!] Calculated Z-Score: {z_score:.2f}")
    if is_anomaly:
        print(f"[ALERT] High-volume data exfiltration detected! (Z-Score > 2.0 threshold)")
    verifier.add_log(exfiltration_log)

    # Baseline Merkle root
    baseline_root = verifier.build_merkle_root()
    print(f"\n[*] Sealed Merkle Tree Root (5 Logs): {baseline_root}\n")

    print("--- [3] Verifying Log Chain Integrity ---")
    verifier.verify_log_integrity(baseline_root)

    print("\n--- [4] Exporting Baseline Audit Trail ---")
    verifier.export_audit_trail(baseline_root)

    print("\n--- [5] Simulating Log Tampering (Attacker Modifying Past Log) ---")
    print("[!] Attacker modifies log #2 to alter bytes_sent from 480 to 0...")
    verifier.log_chain[1]["log"]["bytes_sent"] = 0
    verifier.log_chain[1]["hash"] = verifier.compute_hash(json.dumps(verifier.log_chain[1]["log"], sort_keys=True))

    print("\n--- [6] Re-checking Integrity Post-Tamper ---")
    verifier.verify_log_integrity(baseline_root)
