#!/usr/bin/env bash
set -e

echo "=== [Code Talker SOAR Execution Pipeline] ==="
echo "[1] Checking dependencies & threat feed..."
if [ ! -f "../03-ignister-attack-detection/telemetry/ignister_alerts.json" ]; then
    echo "[!] Threat feed missing. Running 03-ignister-attack-detection pipeline..."
    python3 ../03-ignister-attack-detection/simulations/generate_telemetry.py
    python3 ../03-ignister-attack-detection/src/ignister_detector.py
fi

echo "[2] Executing Code Talker SOAR Playbooks..."
python3 src/codetalker_soar.py

echo "[3] Validating audit logs..."
cat reports/soar_execution_audit.json | grep "total_playbooks_executed"
echo "=== [SOAR Pipeline Run Complete] ==="
