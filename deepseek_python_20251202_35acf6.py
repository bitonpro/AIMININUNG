#!/usr/bin/env python3
"""
🧠 Resource Manager for Hybrid AI Infrastructure
מנהל משאבים חכם לחלוקת עבודה בין Alibaba Cloud ו-Vast.ai
"""

import json
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkloadType(Enum):
    """סוגי workload אפשריים"""
    AI_TRAINING = "ai_training"
    AI_INFERENCE = "ai_inference"
    MEDIA_RENDER = "media_render"
    MINING = "mining"
    DEVELOPMENT = "development"
    DATABASE = "database"
    MONITORING = "monitoring"

class Provider(Enum):
    """ספקי ענן"""
    ALIBABA = "alibaba"
    VASTAI_RESERVED = "vastai_reserved"
    VASTAI_ONDEMAND = "vastai_ondemand"

@dataclass
class ResourceRequest:
    """בקשת משאבים"""
    workload_type: WorkloadType
    gpu_memory_gb: int
    vcpu_count: int
    ram_gb: int
    storage_gb: int
    duration_hours: float
    budget_usd: float

@dataclass
class ResourceAllocation:
    """הקצאת משאבים"""
    provider: Provider
    instance_id: str
    cost_per_hour: float
    estimated_completion: float
    specs: Dict

class HybridResourceManager:
    """מנהל משאבים היברידי"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.allocations: Dict[str, ResourceAllocation] = {}
        
        # מחירי שעה ממוצעים (בדולרים)
        self.hourly_rates = {
            Provider.ALIBABA: {
                "ecs.g6.large": 0.12,
                "ecs.r6.large": 0.18,
            },
            Provider.VASTAI_RESERVED: {
                "RTX 5090": 0.36,
                "RTX 4090": 0.28,
            },
            Provider.VASTAI_ONDEMAND: {
                "RTX 3090": 0.22,
                "RTX 4060": 0.15,
                "RTX 3060": 0.12,
            }
        }
        
        # תצורה מומלצת לכל workload
        self.workload_configs = {
            WorkloadType.AI_TRAINING: {
                "provider": Provider.VASTAI_RESERVED,
                "gpu": "RTX 5090",
                "min_gpu_memory": 24,
                "template": "au",
                "priority": "high"
            },
            WorkloadType.AI_INFERENCE: {
                "provider": Provider.VASTAI_RESERVED,
                "gpu": "RTX 5090",
                "min_gpu_memory": 16,
                "template": "au",
                "priority": "high"
            },
            WorkloadType.MEDIA_RENDER: {
                "provider": Provider.VASTAI_RESERVED,
                "gpu": "RTX 4090",
                "min_gpu_memory": 12,
                "template": "xurt",
                "priority": "medium"
            },
            WorkloadType.MINING: {
                "provider": Provider.VASTAI_ONDEMAND,
                "gpu": "RTX 3090",
                "min_gpu_memory": 24,
                "template": "mining",
                "priority": "low"
            },
            WorkloadType.DATABASE: {
                "provider": Provider.ALIBABA,
                "instance_type": "ecs.r6.large",
                "priority": "high"
            },
            WorkloadType.MONITORING: {
                "provider": Provider.ALIBABA,
                "instance_type": "ecs.g6.large",
                "priority": "medium"
            }
        }
    
    def _load_config(self, config_path: str) -> Dict:
        """טעינת קובץ קונפיגורציה"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found, using defaults")
            return {
                "alibaba_api_key": "",
                "vastai_api_key": "",
                "budget_limit": 1500,
                "auto_scaling": True
            }
    
    def allocate_resources(self, request: ResourceRequest) -> Optional[ResourceAllocation]:
        """
        הקצאת משאבים חכמה לפי workload type ו-budget
        """
        logger.info(f"Allocating resources for {request.workload_type.value}")
        
        # קבלת קונפיגורציה מומלצת
        config = self.workload_configs.get(request.workload_type)
        if not config:
            logger.error(f"No configuration for workload type: {request.workload_type}")
            return None
        
        provider = config["provider"]
        
        # בדיקת budget
        if not self._check_budget(request, provider):
            logger.warning(f"Budget too low for {provider.value}, trying lower tier")
            provider = self._downgrade_provider(provider)
        
        # יצירת instance
        allocation = self._create_instance(provider, request, config)
        
        if allocation:
            self.allocations[allocation.instance_id] = allocation
            logger.info(f"✅ Allocated {provider.value} instance: {allocation.instance_id}")
            logger.info(f"   Cost: ${allocation.cost_per_hour}/hour")
            
            # רישום בהסטוריה
            self._log_allocation(allocation, request)
        
        return allocation
    
    def _check_budget(self, request: ResourceRequest, provider: Provider) -> bool:
        """בדיקה אם ה-budget מספיק"""
        if provider == Provider.ALIBABA:
            hourly_rate = self.hourly_rates[provider]["ecs.g6.large"]
        else:
            gpu_type = self.workload_configs[request.workload_type]["gpu"]
            hourly_rate = self.hourly_rates[provider][gpu_type]
        
        total_cost = hourly_rate * request.duration_hours
        return total_cost <= request.budget_usd
    
    def _downgrade_provider(self, provider: Provider) -> Provider:
        """הורדת רמת provider ל-budget נמוך יותר"""
        downgrade_map = {
            Provider.VASTAI_RESERVED: Provider.VASTAI_ONDEMAND,
            Provider.VASTAI_ONDEMAND: Provider.ALIBABA,
            Provider.ALIBABA: None
        }
        return downgrade_map.get(provider, provider)
    
    def _create_instance(self, provider: Provider, request: ResourceRequest, config: Dict) -> Optional[ResourceAllocation]:
        """יצירת instance בפועל"""
        
        # הדמיית יצירה - במציאות יתחבר ל-API
        instance_id = f"{provider.value}-{request.workload_type.value}-{hash(str(request))}"
        
        if provider == Provider.ALIBABA:
            cost_per_hour = self.hourly_rates[provider][config["instance_type"]]
            specs = {
                "type": config["instance_type"],
                "vcpu": request.vcpu_count,
                "ram": request.ram_gb,
                "storage": request.storage_gb
            }
        else:
            gpu_type = config["gpu"]
            cost_per_hour = self.hourly_rates[provider][gpu_type]
            specs = {
                "gpu": gpu_type,
                "template": config["template"],
                "storage": request.storage_gb,
                "sireg_enabled": True if provider == Provider.VASTAI_RESERVED else False
            }
        
        return ResourceAllocation(
            provider=provider,
            instance_id=instance_id,
            cost_per_hour=cost_per_hour,
            estimated_completion=request.duration_hours,
            specs=specs
        )
    
    def _log_allocation(self, allocation: ResourceAllocation, request: ResourceRequest):
        """רישום הקצאה לקובץ לוג"""
        log_entry = {
            "timestamp": time.time(),
            "allocation": {
                "instance_id": allocation.instance_id,
                "provider": allocation.provider.value,
                "cost_per_hour": allocation.cost_per_hour,
                "specs": allocation.specs
            },
            "request": {
                "workload_type": request.workload_type.value,
                "duration": request.duration_hours,
                "budget": request.budget_usd
            }
        }
        
        with open("allocations.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def optimize_costs(self):
        """אופטימיזציה של עלויות"""
        logger.info("Running cost optimization...")
        
        total_monthly_cost = sum(
            alloc.cost_per_hour * 24 * 30 
            for alloc in self.allocations.values()
        )
        
        # המלצות לאופטימיזציה
        recommendations = []
        
        if total_monthly_cost > self.config.get("budget_limit", 1500):
            recommendations.append(
                f"⚠️  Monthly cost ${total_monthly_cost:.2f} exceeds budget"
            )
        
        # בדיקה אם כדאי להעביר ל-Reserved
        for instance_id, alloc in self.allocations.items():
            if alloc.provider == Provider.VASTAI_ONDEMAND:
                # אם שימוש מעל 18 שעות ביום - עדיף Reserved
                estimated_daily_hours = alloc.estimated_completion
                if estimated_daily_hours > 18:
                    recommendations.append(
                        f"💡 Convert {instance_id} to Reserved (uses {estimated_daily_hours}h/day)"
                    )
        
        return {
            "total_monthly_cost": total_monthly_cost,
            "recommendations": recommendations
        }

# שימוש לדוגמה
if __name__ == "__main__":
    import time
    
    # יצירת מנהל משאבים
    manager = HybridResourceManager()
    
    # בקשת הדמיית AI Training
    request = ResourceRequest(
        workload_type=WorkloadType.AI_TRAINING,
        gpu_memory_gb=24,
        vcpu_count=8,
        ram_gb=32,
        storage_gb=500,
        duration_hours=48,
        budget_usd=100
    )
    
    # הקצאת משאבים
    allocation = manager.allocate_resources(request)
    
    if allocation:
        print(f"\n🎯 Allocation Result:")
        print(f"   Provider: {allocation.provider.value}")
        print(f"   Instance: {allocation.instance_id}")
        print(f"   Cost: ${allocation.cost_per_hour}/hour")
        print(f"   Estimated: {allocation.estimated_completion} hours")
        print(f"   Specs: {allocation.specs}")
    
    # אופטימיזציה
    optimization = manager.optimize_costs()
    print(f"\n💰 Cost Optimization:")
    print(f"   Monthly Cost: ${optimization['total_monthly_cost']:.2f}")
    for rec in optimization['recommendations']:
        print(f"   {rec}")