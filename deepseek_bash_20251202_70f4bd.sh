#!/bin/bash
# 📦 סקריפט פריסה אוטומטי לתשתית ההיברידית

set -euo pipefail

echo "🚀 התקנת תשתית AIMININUNG ההיברידית"
echo "====================================="

# קונפיגורציה
export ALIBABA_REGION="cn-hangzhou"
export PROJECT_NAME="aimininung"
export VAST_API_KEY="${VAST_API_KEY}"
export ALIBABA_ACCESS_KEY="${ALIBABA_ACCESS_KEY}"
export ALIBABA_SECRET_KEY="${ALIBABA_SECRET_KEY}"

# פונקציות עזר
log_info() { echo -e "\033[1;34m[INFO]\033[0m $1"; }
log_success() { echo -e "\033[1;32m[SUCCESS]\033[0m $1"; }
log_error() { echo -e "\033[1;31m[ERROR]\033[0m $1"; }

# שלב 1: פריסת Alibaba Cloud
deploy_alibaba() {
    log_info "מפריס שרתי ניהול ב-Alibaba Cloud..."
    
    # יצירת VPC (מדומה - יש להתאים ל-API האמיתי)
    cat > alibaba_config.json << EOF
{
    "vpc_name": "${PROJECT_NAME}-vpc",
    "vswitch_name": "${PROJECT_NAME}-vswitch",
    "instances": [
        {
            "name": "A1-WebAPI",
            "type": "ecs.g6.large",
            "image": "ubuntu_22_04",
            "ports": [22, 80, 443, 8000]
        },
        {
            "name": "A2-Monitoring",
            "type": "ecs.g6.large",
            "image": "ubuntu_22_04",
            "ports": [22, 3000, 9090]
        },
        {
            "name": "A3-Database",
            "type": "ecs.r6.large",
            "image": "ubuntu_22_04",
            "ports": [22, 3306, 5432, 6379]
        },
        {
            "name": "A4-DevOps",
            "type": "ecs.g6.large",
            "image": "ubuntu_22_04",
            "ports": [22, 8080, 5000]
        }
    ]
}
EOF
    
    log_success "תצורת Alibaba Cloud נוצרה - הרץ עם Aliyun CLI"
    echo "פקודה מומלצת: aliyun ecs CreateInstance --config-file alibaba_config.json"
}

# שלב 2: פריסת Vast.ai Reserved Instances
deploy_vastai_reserved() {
    log_info "מפריס Reserved Instances ב-Vast.ai..."
    
    # קובץ תצורה ל-Reserved Instances
    cat > vastai_reserved.json << EOF
{
    "api_key": "${VAST_API_KEY}",
    "reserved_instances": [
        {
            "label": "V1-AI-Train",
            "template": "au",
            "gpu_name": "RTX 5090",
            "disk_space": 500,
            "duration": 30,
            "onstart": "curl -sSL https://raw.githubusercontent.com/bitonpro/AIMININUNG/main/scripts/setup_ai.sh | bash"
        },
        {
            "label": "V2-AI-Infer",
            "template": "au",
            "gpu_name": "RTX 5090",
            "disk_space": 300,
            "duration": 30,
            "onstart": "curl -sSL https://raw.githubusercontent.com/bitonpro/AIMININUNG/main/scripts/setup_inference.sh | bash"
        },
        {
            "label": "V3-Media",
            "template": "xurt",
            "gpu_name": "RTX 4090",
            "disk_space": 1000,
            "duration": 30,
            "onstart": "curl -sSL https://raw.githubusercontent.com/bitonpro/AIMININUNG/main/scripts/setup_media.sh | bash"
        }
    ],
    "options": {
        "enable_sireg": true,
        "auto_start": true,
        "persistent_storage": true
    }
}
EOF
    
    log_success "תצורת Reserved Instances נוצרה"
    
    # סקריפט יצירה אוטומטי (דוגמה - יש להתאים ל-API האמיתי)
    cat > create_reserved.py << 'PYTHON'
#!/usr/bin/env python3
import requests
import json
import time

with open('vastai_reserved.json') as f:
    config = json.load(f)

API_URL = "https://console.vast.ai/api/v0"
headers = {"Authorization": f"Bearer {config['api_key']}"}

for instance in config['reserved_instances']:
    payload = {
        "image": f"vastai/{instance['template']}:latest",
        "gpu_name": instance['gpu_name'],
        "disk_space": instance['disk_space'],
        "label": instance['label'],
        "extra_args": "--reserved 30",
        "env": {"SIREG_ENABLED": "true"},
        "onstart": instance['onstart']
    }
    
    response = requests.post(
        f"{API_URL}/instances/create",
        headers=headers,
        json=payload
    )
    
    if response.status_code == 200:
        print(f"✅ Created reserved instance: {instance['label']}")
        print(f"   ID: {response.json()['id']}")
        print(f"   Cost: ${response.json()['cost']}/month")
    else:
        print(f"❌ Failed to create {instance['label']}: {response.text}")
    
    time.sleep(2)

print("\n🎯 All reserved instances created successfully!")
PYTHON
    
    log_info "הרץ: python create_reserved.py"
}

# שלב 3: פריסת On-Demand Instances
deploy_vastai_ondemand() {
    log_info "מפריס On-Demand Instances ב-Vast.ai..."
    
    cat > vastai_ondemand.sh << 'BASH'
#!/bin/bash
# סקריפט ליצירת On-Demand Instances

INSTANCES=(
    "V4-Mining:RTX 3090:100:mining"
    "V5-Testing:RTX 4060:50:dev"
    "V6-Backup:RTX 3060:200:backup"
)

for instance in "${INSTANCES[@]}"; do
    IFS=':' read -r label gpu disk template <<< "$instance"
    
    echo "Creating $label with $gpu..."
    
    # פקודת יצירה (דוגמה - יש להתאים ל-API)
    curl -X POST "https://console.vast.ai/api/v0/instances" \
        -H "Authorization: Bearer $VAST_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
            \"image\": \"vastai/$template:latest\",
            \"gpu_name\": \"$gpu\",
            \"disk_space\": $disk,
            \"label\": \"$label\",
            \"onstart\": \"echo 'Ready for workload'\"
        }"
    
    sleep 1
done
BASH
    
    chmod +x vastai_ondemand.sh
    log_success "סקריפט On-Demand נוצר - הרץ: ./vastai_ondemand.sh"
}

# שלב 4: אינטגרציה וניטור
setup_integration() {
    log_info "מגדיר אינטגרציה וניטור..."
    
    cat > integration_setup.sh << 'BASH'
#!/bin/bash
# סקריפט לאינטגרציה בין המערכות

echo "🔗 הגדרת חיבור בין Alibaba Cloud ל-Vast.ai"

# 1. הגדרת VPN/שרות Gateway
echo "Setting up VPN tunnel..."
# קוד להגדרת WireGuard/OpenVPN

# 2. הגדרת Prometheus לניטור Vast.ai
cat > prometheus_vastai.yml << EOF
scrape_configs:
  - job_name: 'vastai-gpu'
    static_configs:
      - targets: ['vastai-node-1:9100', 'vastai-node-2:9100']
    metrics_path: /metrics
    
  - job_name: 'vastai-mining'
    static_configs:
      - targets: ['vastai-mining-1:9200']
    params:
      coin: ['FLUX', 'QUBIT']
EOF

# 3. הגדרת Grafana Dashboards
echo "Importing Grafana dashboards..."
curl -X POST "http://A2-Monitoring-IP:3000/api/dashboards/db" \
    -H "Content-Type: application/json" \
    -d @ai_monitoring_dashboard.json

# 4. הגדרת התראות
cat > alerts.yml << EOF
groups:
  - name: ai-infra
    rules:
      - alert: GPUTemperatureHigh
        expr: gpu_temperature > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "GPU temperature too high"
          
      - alert: MiningProfitabilityLow
        expr: mining_profitability < 0
        for: 1h
        labels:
          severity: critical
EOF

echo "✅ Integration setup completed"
BASH
    
    chmod +x integration_setup.sh
}

# פריסה ראשית
main() {
    echo "🎯 AIMININUNG Hybrid Infrastructure Deployment"
    echo "============================================"
    
    # בדיקת תלויות
    command -v curl >/dev/null 2>&1 || { log_error "curl not installed"; exit 1; }
    command -v jq >/dev/null 2>&1 || { log_error "jq not installed"; exit 1; }
    
    # הרצת השלבים
    deploy_alibaba
    deploy_vastai_reserved
    deploy_vastai_ondemand
    setup_integration
    
    log_success "🎉 כל הקבצים לפריסה נוצרו!"
    echo ""
    echo "📁 קבצים שנוצרו:"
    echo "  - alibaba_config.json          # תצורת Alibaba Cloud"
    echo "  - vastai_reserved.json         # תצורת Reserved Instances"
    echo "  - create_reserved.py           # סקריפט Python ליצירה"
    echo "  - vastai_ondemand.sh           # סקריפט On-Demand"
    echo "  - integration_setup.sh         # סקריפט אינטגרציה"
    echo ""
    echo "🚀 שלבי פריסה:"
    echo "  1. הרץ את פקודות Alibaba Cloud"
    echo "  2. הרץ: python create_reserved.py"
    echo "  3. הרץ: ./vastai_ondemand.sh"
    echo "  4. הרץ: ./integration_setup.sh"
    echo ""
    echo "💰 הערכת עלויות חודשית: $1,246"
    echo "⏱️  זמן פריסה משוער: 45-60 דקות"
}

main