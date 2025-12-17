#!/usr/bin/env bash
set -euo pipefail

echo "[post-install] Checking Docker & Compose..."
if ! command -v docker >/dev/null 2>&1; then
  echo "Docker not found. Please install Docker first."; exit 1
fi

# vm.max_map_count for Elasticsearch
echo "[post-install] Setting vm.max_map_count=262144"
sudo sysctl -w vm.max_map_count=262144 || true
if [ -d /etc/sysctl.d ]; then
  echo "vm.max_map_count=262144" | sudo tee /etc/sysctl.d/99-elastic.conf >/dev/null || true
  sudo sysctl --system || true
fi

echo "[post-install] Ensuring local folders exist"
mkdir -p logs/app volumes/esdata volumes/grafana volumes/postgres

echo "[post-install] Done."
