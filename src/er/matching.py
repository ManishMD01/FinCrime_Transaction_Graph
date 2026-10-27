"""
Record Linkage / Fuzzy Matching Module
Implements deterministic and probabilistic matching logic.
"""

from typing import Dict, Tuple
import pandas as pd
import Levenshtein
from difflib import SequenceMatcher
import jellyfish


class FuzzyMatcher:
    """Implements fuzzy matching for entity resolution."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def jaro_winkler_similarity(self, s1: str, s2: str) -> float:
        """Calculate Jaro-Winkler similarity for names."""
        if pd.isna(s1) or pd.isna(s2) or s1 == '' or s2 == '':
            return 0.0
        try:
            return jellyfish.jaro_winkler_similarity(str(s1), str(s2))
        except:
            return 0.0
    
    def levenshtein_similarity(self, s1: str, s2: str) -> float:
        """Calculate normalized Levenshtein similarity for addresses."""
        if pd.isna(s1) or pd.isna(s2) or s1 == '' or s2 == '':
            return 0.0
        s1, s2 = str(s1), str(s2)
        if s1 == s2:
            return 1.0
        distance = Levenshtein.distance(s1, s2)
        max_len = max(len(s1), len(s2))
        if max_len == 0:
            return 1.0
        return 1.0 - (distance / max_len)
    
    def jaccard_similarity(self, set1: set, set2: set) -> float:
        """Calculate Jaccard similarity for shared attributes."""
        if not set1 or not set2:
            return 0.0
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        if union == 0:
            return 0.0
        return intersection / union
    
    def exact_match(self, val1, val2) -> bool:
        """Check for exact match."""
        if pd.isna(val1) or pd.isna(val2):
            return False
        return str(val1).strip() == str(val2).strip()
    
    def calculate_match_score(self, idx1: int, idx2: int) -> Dict[str, float]:
        """
        Calculate probabilistic match score between two records.
        Uses weighted combination of different similarity metrics.
        """
        row1 = self.df.iloc[idx1]
        row2 = self.df.iloc[idx2]
        
        scores = {}
        
        # Deterministic matches (high weight)
        if self.exact_match(row1.get('ssn_std'), row2.get('ssn_std')) and row1.get('ssn_std'):
            scores['ssn_match'] = 1.0
        else:
            scores['ssn_match'] = 0.0
        
        # Name similarity (Jaro-Winkler)
        scores['name_jw'] = self.jaro_winkler_similarity(
            row1.get('full_name_clean', ''), 
            row2.get('full_name_clean', '')
        )
        
        # Address similarity (Levenshtein)
        scores['address_lev'] = self.levenshtein_similarity(
            row1.get('address_clean', ''),
            row2.get('address_clean', '')
        )
        
        # Phone match
        scores['phone_match'] = 1.0 if self.exact_match(row1.get('phone_std'), row2.get('phone_std')) and row1.get('phone_std') else 0.0
        
        # Email match
        scores['email_match'] = 1.0 if self.exact_match(row1.get('email_std'), row2.get('email_std')) and row1.get('email_std') else 0.0
        
        # DOB match
        scores['dob_match'] = 1.0 if self.exact_match(row1.get('dob'), row2.get('dob')) and row1.get('dob') else 0.0
        
        # Zip match
        scores['zip_match'] = 1.0 if self.exact_match(row1.get('zip_std'), row2.get('zip_std')) and row1.get('zip_std') else 0.0
        
        # Device match
        scores['device_match'] = 1.0 if self.exact_match(row1.get('device_id'), row2.get('device_id')) and row1.get('device_id') else 0.0
        
        # IP match
        scores['ip_match'] = 1.0 if self.exact_match(row1.get('ip_address'), row2.get('ip_address')) and row1.get('ip_address') else 0.0
        
        # Calculate weighted score
        weights = {
            'ssn_match': 0.30,
            'name_jw': 0.20,
            'phone_match': 0.15,
            'email_match': 0.12,
            'dob_match': 0.10,
            'address_lev': 0.08,
            'zip_match': 0.03,
            'device_match': 0.02,
        }
        
        weighted_score = sum(scores.get(k, 0) * weights.get(k, 0) for k in weights)
        
        # Boost score if strong indicators match
        if scores['ssn_match'] == 1.0 and scores['name_jw'] > 0.8:
            weighted_score = max(weighted_score, 0.95)
        if scores['phone_match'] == 1.0 and scores['name_jw'] > 0.7:
            weighted_score = min(1.0, weighted_score + 0.1)
        if scores['device_match'] == 1.0 and (scores['name_jw'] > 0.6 or scores['phone_match'] == 1.0):
            weighted_score = min(1.0, weighted_score + 0.05)
        
        scores['weighted_score'] = weighted_score
        
        return scores
    
    def is_match(self, idx1: int, idx2: int, threshold: float = 0.75) -> Tuple[bool, float, Dict]:
        """Determine if two records match based on threshold."""
        scores = self.calculate_match_score(idx1, idx2)
        weighted_score = scores['weighted_score']
        is_match_result = weighted_score >= threshold
        return is_match_result, weighted_score, scores
