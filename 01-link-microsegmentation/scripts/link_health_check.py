#!/usr/bin/env python3
import subprocess
import time
import urllib.request
import sys

TARGET_IP = "172.21.0.20"
TARGET_PORT = "8080"

def check_target_health():
    """Simulates a health/integrity check on Link-2."""
    try:
        url = f"http://{TARGET_IP}:{TARGET_PORT}"
        req = urllib.request.urlopen(url, timeout=2)
        if req.getcode() == 200:
            return True
    except Exception as e:
        print(f"[!] Health check failed: {e}")
        return False
    return True

def sever_link_arrow():
    """Applies iptables rule inside Link-1 to sever network route to Link-2."""
    print(f"[x] THREAT/FAILURE DETECTED! Severing Link Marker to {TARGET_IP}...")
    cmd = f"iptables -A OUTPUT -d {TARGET_IP} -j DROP"
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"[+] Link Arrow severed successfully. {TARGET_IP} is isolated.")
    else:
        print(f"[-] Failed to apply isolation rule: {res.stderr}")

def main():
    print(f"[*] Monitoring Link Marker connection to {TARGET_IP}...")
    while True:
        healthy = check_target_health()
        if not healthy:
            sever_link_arrow()
            break
        else:
            print(f"[+] Link Status: OK (Connection to {TARGET_IP} active)")
        time.sleep(5)

if __name__ == "__main__":
    main()
