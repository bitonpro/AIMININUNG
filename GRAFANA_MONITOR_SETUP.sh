#!/bin/bash
# ============================================
# 🧩 GRAFANA_MONITOR_SETUP.sh
# Version: 1.0 | Date: 2-Dec-2025
# Author: X-GPT GUIDES™
# Purpose: Setup Grafana & Prometheus dashboard
# ============================================

echo "🚀 Setting up Grafana Monitoring for ALL BITON..."

sudo apt update -y
sudo apt install -y docker.io docker-compose

cat <<EOF > docker-compose.yml
version: '3'
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=biton2025
    depends_on:
      - prometheus
EOF

docker-compose up -d
echo "✅ Grafana running on port 3000 (login: admin / biton2025)"
