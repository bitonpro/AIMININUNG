"""
Talmudic Logic Module
Implements Talmudic reasoning rules and methods
"""

import re
from typing import Dict, List, Optional, Any
from enum import Enum

class TalmudicRule(Enum):
    """Talmudic logical rules"""
    KAL_VACHOMER = "קל וחומר"
    GEZERAH_SHAVAH = "גזירה שווה"
    BINYAN_AV = "בניין אב"
    KLAAL_UFERAT = "כלל ופרט"
    RIBUI_UMIUT = "ריבוי ומיעוט"
    DAVAR_HALAMED = "דבר הלמד"

class TalmudicLogic:
    """Implements Talmudic logical reasoning"""
    
    def __init__(self):
        self.rules = self._initialize_rules()
        self.examples = self._load_examples()
    
    def _initialize_rules(self) -> Dict[TalmudicRule, Dict]:
        """Initialize Talmudic rules with descriptions and examples"""
        return {
            TalmudicRule.KAL_VACHOMER: {
                "description": "Inference from minor to major or vice versa",
                "template": "If {minor_case}, then certainly {major_case}",
                "example": "If one is liable for damage caused by one's property, certainly for damage caused by oneself",
            },
            TalmudicRule.GEZERAH_SHAVAH: {
                "description": "Analogy based on similar words or phrases",
                "template": "{case_a} is analogous to {case_b} because both share {common_term}",
                "example": "The word 'Shabbat' appears in two contexts, creating a legal analogy",
            },
            TalmudicRule.BINYAN_AV: {
                "description": "Constructive analogy from multiple sources",
                "template": "From {sources} we learn that {principle} applies to {target}",
                "example": "From multiple cases of liability, we construct a general principle",
            },
            TalmudicRule.KLAAL_UFERAT: {
                "description": "General principle limited by specifics",
                "template": "The general principle {general} is limited by the specific case {specific}",
                "example": "'All fruits' (general) limited by 'grapes and figs' (specific)",
            },
        }
    
    def apply_kal_vachomer(self, minor_case: str, major_case: str) -> Dict[str, Any]:
        """Apply Kal Vachomer (a fortiori) reasoning"""
        return {
            "rule": TalmudicRule.KAL_VACHOMER,
            "application": self.rules[TalmudicRule.KAL_VACHOMER]["template"].format(
                minor_case=minor_case,
                major_case=major_case
            ),
            "confidence": self._calculate_confidence(minor_case, major_case),
            "conditions": self._check_kal_vachomer_conditions(minor_case, major_case),
        }
    
    def apply_gezerah_shavah(self, case_a: str, case_b: str, common_term: str) -> Dict[str, Any]:
        """Apply Gezerah Shavah (verbal analogy)"""
        return {
            "rule": TalmudicRule.GEZERAH_SHAVAH,
            "application": self.rules[TalmudicRule.GEZERAH_SHAVAH]["template"].format(
                case_a=case_a,
                case_b=case_b,
                common_term=common_term
            ),
            "confidence": self._calculate_verbal_similarity(case_a, case_b),
            "validity_checks": self._validate_gezerah_shavah(case_a, case_b, common_term),
        }
    
    def apply_binyan_av(self, sources: List[str], principle: str, target: str) -> Dict[str, Any]:
        """Apply Binyan Av (constructive analogy)"""
        return {
            "rule": TalmudicRule.BINYAN_AV,
            "application": self.rules[TalmudicRule.BINYAN_AV]["template"].format(
                sources=", ".join(sources),
                principle=principle,
                target=target
            ),
            "confidence": len(sources) / 10.0,  # More sources = higher confidence
            "source_count": len(sources),
            "coherence": self._check_coherence(sources, principle),
        }
    
    def analyze_text(self, text: str) -> List[Dict[str, Any]]:
        """Analyze text for potential Talmudic reasoning patterns"""
        insights = []
        
        # Look for comparative language (Kal Vachomer)
        comparative_patterns = [
            r'if.*then certainly',
            r'certainly.*if',
            r'all the more so',
            r'how much more',
        ]
        
        for pattern in comparative_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                match = re.search(pattern, text, re.IGNORECASE)
                insights.append({
                    "rule": "KAL_VACHOMER",
                    "pattern": pattern,
                    "match": match.group(0) if match else "",
                    "suggestion": "Consider applying קל וחומר reasoning",
                })
        
        # Look for analogical language (Gezerah Shavah)
        analogical_patterns = [
            r'just as.*so too',
            r'analogous to',
            r'similar to',
            r'like.*so',
        ]
        
        for pattern in analogical_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                match = re.search(pattern, text, re.IGNORECASE)
                insights.append({
                    "rule": "GEZERAH_SHAVAH",
                    "pattern": pattern,
                    "match": match.group(0) if match else "",
                    "suggestion": "Consider applying גזירה שווה reasoning",
                })
        
        return insights
    
    def generate_hypothesis(self, premises: List[str]) -> Dict[str, Any]:
        """Generate a Talmudic-style hypothesis from premises"""
        
        if len(premises) == 0:
            return {"error": "No premises provided"}
        
        if len(premises) == 1:
            # Try Kal Vachomer
            return self._generate_kal_vachomer_hypothesis(premises[0])
        
        if len(premises) >= 2:
            # Try Gezerah Shavah or Binyan Av
            if self._have_common_terms(premises):
                return self._generate_gezerah_shavah_hypothesis(premises)
            else:
                return self._generate_binyan_av_hypothesis(premises)
        
        return {"error": "Unable to generate hypothesis"}
    
    def _calculate_confidence(self, minor: str, major: str) -> float:
        """Calculate confidence score for Kal Vachomer"""
        # Simple heuristic: ratio of word lengths
        minor_words = len(minor.split())
        major_words = len(major.split())
        
        if minor_words == 0 or major_words == 0:
            return 0.5
        
        ratio = min(minor_words, major_words) / max(minor_words, major_words)
        return min(ratio * 1.5, 1.0)
    
    def _check_kal_vachomer_conditions(self, minor: str, major: str) -> List[str]:
        """Check conditions for valid Kal Vachomer"""
        conditions = []
        
        # Condition 1: The minor case must be included in the major case
        minor_words = set(minor.lower().split())
        major_words = set(major.lower().split())
        common_words = minor_words.intersection(major_words)
        
        if len(common_words) > 0:
            conditions.append(f"Common terms: {', '.join(common_words)}")
        else:
            conditions.append("Warning: No common terms found")
        
        # Condition 2: The inference should be logical
        if len(minor.split()) < len(major.split()):
            conditions.append("Appears to be minor to major inference")
        else:
            conditions.append("Appears to be major to minor inference")
        
        return conditions
    
    def _calculate_verbal_similarity(self, text1: str, text2: str) -> float:
        """Calculate verbal similarity for Gezerah Shavah"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def _validate_gezerah_shavah(self, case_a: str, case_b: str, common_term: str) -> List[str]:
        """Validate Gezerah Shavah application"""
        validations = []
        
        # Check if common term appears in both cases
        if common_term.lower() in case_a.lower() and common_term.lower() in case_b.lower():
            validations.append(f"Common term '{common_term}' found in both cases")
        else:
            validations.append(f"Warning: Common term '{common_term}' not found in both cases")
        
        # Check for additional similarities
        similarity = self._calculate_verbal_similarity(case_a, case_b)
        if similarity > 0.3:
            validations.append(f"High verbal similarity: {similarity:.2f}")
        else:
            validations.append(f"Low verbal similarity: {similarity:.2f}")
        
        return validations
    
    def _check_coherence(self, sources: List[str], principle: str) -> float:
        """Check coherence of sources with principle"""
        principle_words = set(principle.lower().split())
        total_common = 0
        
        for source in sources:
            source_words = set(source.lower().split())
            common = len(principle_words.intersection(source_words))
            total_common += common
        
        avg_common = total_common / len(sources) if sources else 0
        max_possible = len(principle_words)
        
        if max_possible == 0:
            return 0.5
        
        return min(avg_common / max_possible, 1.0)
    
    def _have_common_terms(self, texts: List[str]) -> bool:
        """Check if texts have common terms"""
        if len(texts) < 2:
            return False
        
        word_sets = [set(text.lower().split()) for text in texts]
        common = set.intersection(*word_sets)
        
        return len(common) > 0
    
    def _generate_kal_vachomer_hypothesis(self, premise: str) -> Dict[str, Any]:
        """Generate Kal Vachomer hypothesis from single premise"""
        words = premise.split()
        if len(words) < 3:
            return {"rule": "KAL_VACHOMER", "hypothesis": f"If {premise}, then certainly..."}
        
        # Split premise and create inference
        midpoint = len(words) // 2
        minor = " ".join(words[:midpoint])
        major = " ".join(words[midpoint:])
        
        return {
            "rule": "KAL_VACHOMER",
            "hypothesis": f"If {minor}, then certainly {major}",
            "confidence": self._calculate_confidence(minor, major),
        }
    
    def _generate_gezerah_shavah_hypothesis(self, premises: List[str]) -> Dict[str, Any]:
        """Generate Gezerah Shavah hypothesis from multiple premises"""
        # Find common terms
        word_sets = [set(premise.lower().split()) for premise in premises]
        common_terms = set.intersection(*word_sets)
        
        if not common_terms:
            return self._generate_binyan_av_hypothesis(premises)
        
        common_term = next(iter(common_terms))
        
        return {
            "rule": "GEZERAH_SHAVAH",
            "hypothesis": f"{premises[0]} is analogous to {premises[1]} because both involve '{common_term}'",
            "common_term": common_term,
            "confidence": self._calculate_verbal_similarity(premises[0], premises[1]),
        }
    
    def _generate_binyan_av_hypothesis(self, premises: List[str]) -> Dict[str, Any]:
        """Generate Binyan Av hypothesis from multiple premises"""
        # Extract key terms from each premise
        key_terms = []
        for premise in premises:
            words = premise.split()
            if words:
                key_terms.append(words[-1])  # Use last word as key term
        
        principle = " and ".join(key_terms)
        
        return {
            "rule": "BINYAN_AV",
            "hypothesis": f"From {len(premises)} cases, we learn the principle of {principle}",
            "principle": principle,
            "confidence": len(premises) / 10.0,
        }
    
    def _load_examples(self) -> Dict[str, List[str]]:
        """Load Talmudic reasoning examples"""
        return {
            "kal_vachomer": [
                "If one is forbidden from working on a minor holiday, certainly on Yom Kippur",
                "If a teacher is responsible for students during class, certainly during dangerous activities",
            ],
            "gezerah_shavah": [
                "The word 'dwelling' in two contexts creates an analogy about sukkah",
                "Similar terminology about 'lighting' connects Shabbat and Hanukkah laws",
            ],
            "binyan_av": [
                "From cases of ox, pit, and fire, we learn principles of property liability",
                "Multiple cases of mistaken identity teach us about witness reliability",
            ],
        }