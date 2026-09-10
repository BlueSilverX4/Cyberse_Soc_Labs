#!/usr/bin/env bash
set -e

echo "=== [Cyberse SOC Dashboard Generator] ==="
echo "[1] Aggregating SOAR metrics..."
python3 src/metrics_engine.py

echo "[2] Building Executive HTML Dashboard..."
python3 src/dashboard_builder.py

echo "=== [Dashboard Build Complete] ==="
