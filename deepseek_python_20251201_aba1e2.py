"""
Abraham-AI Core Engine
Main AI engine for Jewish-Chinese wisdom fusion
"""

__version__ = "1.0.0"
__author__ = "Abraham-AI Community"
__email__ = "community@abraham-ai.org"

from .abraham_ai_engine import AbrahamAIEngine
from .response_models import (
    WisdomResponse,
    JewishAnalysis,
    ChineseAnalysis,
    FusionResult
)

__all__ = [
    "AbrahamAIEngine",
    "WisdomResponse",
    "JewishAnalysis", 
    "ChineseAnalysis",
    "FusionResult"
]