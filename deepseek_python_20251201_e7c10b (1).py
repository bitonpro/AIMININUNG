"""
Response models for Abraham-AI
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime

class YinYangBalance(Enum):
    """Yin-Yang balance states"""
    YIN_DOMINANT = "yin_dominant"
    YANG_DOMINANT = "yang_dominant"
    BALANCED = "balanced"
    HARMONIOUS = "harmonious"

class WisdomLayer(Enum):
    """Four levels of interpretation"""
    PSHAT = "pshat"
    REMEZ = "remez"
    DRASH = "drash"
    SOD = "sod"

@dataclass
class TalmudicInsight:
    """Insight from Talmudic analysis"""
    rule: str
    application: str
    conclusion: str
    confidence: float = 0.0
    sources: List[str] = field(default_factory=list)

@dataclass
class JewishAnalysis:
    """Jewish wisdom analysis results"""
    talmudic_insights: List[TalmudicInsight] = field(default_factory=list)
    midrashic_insights: List[Dict[str, Any]] = field(default_factory=list)
    kabbalistic_insights: List[Dict[str, Any]] = field(default_factory=list)
    ethical_insights: List[Dict[str, Any]] = field(default_factory=list)
    summary: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TaoistInsight:
    """Insight from Taoist analysis"""
    principle: str
    application: str
    interpretation: str
    wu_wei_score: float = 0.0  # Score for Wu Wei (effortless action)

@dataclass
class FiveElementsAnalysis:
    """Five Elements analysis"""
    dominant_element: str
    generating_element: str
    controlling_element: str
    harmony_score: float = 0.0
    recommendations: List[str] = field(default_factory=list)

@dataclass
class ChineseAnalysis:
    """Chinese wisdom analysis results"""
    taoist_insights: List[TaoistInsight] = field(default_factory=list)
    confucian_insights: List[Dict[str, Any]] = field(default_factory=list)
    five_elements_analysis: Optional[FiveElementsAnalysis] = None
    i_ching_insights: List[Dict[str, Any]] = field(default_factory=list)
    yin_yang_analysis: Dict[str, float] = field(default_factory=dict)
    summary: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FusionInsight:
    """Fusion of Jewish and Chinese insights"""
    jewish_source: str
    chinese_source: str
    fusion_result: str
    complementarity_score: float = 0.0
    novelty_score: float = 0.0

@dataclass
class WisdomResponse:
    """Complete wisdom response from Abraham-AI"""
    
    # Original query
    question: str
    question_analysis: Dict[str, Any]
    
    # Wisdom analyses
    jewish_analysis: Optional[JewishAnalysis] = None
    chinese_analysis: Optional[ChineseAnalysis] = None
    fusion_result: Dict[str, Any] = field(default_factory=dict)
    
    # Interpretations
    wisdom_layers: Dict[WisdomLayer, str] = field(default_factory=dict)
    
    # Balance metrics
    balance_score: float = 0.5
    yin_yang_balance: YinYangBalance = YinYangBalance.BALANCED
    
    # Final answer
    integrated_answer: str = ""
    
    # Metadata
    timestamp: datetime = field(default_factory=datetime.now)
    processing_id: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "question": self.question,
            "question_analysis": self.question_analysis,
            "jewish_analysis": self._convert_jewish_analysis(),
            "chinese_analysis": self._convert_chinese_analysis(),
            "fusion_result": self.fusion_result,
            "wisdom_layers": {k.value: v for k, v in self.wisdom_layers.items()},
            "balance_score": self.balance_score,
            "yin_yang_balance": self.yin_yang_balance.value,
            "integrated_answer": self.integrated_answer,
            "timestamp": self.timestamp.isoformat(),
            "processing_id": self.processing_id,
            "metadata": self.metadata,
        }
    
    def _convert_jewish_analysis(self) -> Optional[Dict[str, Any]]:
        """Convert JewishAnalysis to dict"""
        if not self.jewish_analysis:
            return None
        
        return {
            "talmudic_insights": [
                {
                    "rule": insight.rule,
                    "application": insight.application,
                    "conclusion": insight.conclusion,
                    "confidence": insight.confidence,
                    "sources": insight.sources,
                }
                for insight in self.jewish_analysis.talmudic_insights
            ],
            "midrashic_insights": self.jewish_analysis.midrashic_insights,
            "kabbalistic_insights": self.jewish_analysis.kabbalistic_insights,
            "ethical_insights": self.jewish_analysis.ethical_insights,
            "summary": self.jewish_analysis.summary,
            "metadata": self.jewish_analysis.metadata,
        }
    
    def _convert_chinese_analysis(self) -> Optional[Dict[str, Any]]:
        """Convert ChineseAnalysis to dict"""
        if not self.chinese_analysis:
            return None
        
        return {
            "taoist_insights": [
                {
                    "principle": insight.principle,
                    "application": insight.application,
                    "interpretation": insight.interpretation,
                    "wu_wei_score": insight.wu_wei_score,
                }
                for insight in self.chinese_analysis.taoist_insights
            ],
            "confucian_insights": self.chinese_analysis.confucian_insights,
            "five_elements_analysis": (
                {
                    "dominant_element": self.chinese_analysis.five_elements_analysis.dominant_element,
                    "generating_element": self.chinese_analysis.five_elements_analysis.generating_element,
                    "controlling_element": self.chinese_analysis.five_elements_analysis.controlling_element,
                    "harmony_score": self.chinese_analysis.five_elements_analysis.harmony_score,
                    "recommendations": self.chinese_analysis.five_elements_analysis.recommendations,
                }
                if self.chinese_analysis.five_elements_analysis
                else None
            ),
            "i_ching_insights": self.chinese_analysis.i_ching_insights,
            "yin_yang_analysis": self.chinese_analysis.yin_yang_analysis,
            "summary": self.chinese_analysis.summary,
            "metadata": self.chinese_analysis.metadata,
        }