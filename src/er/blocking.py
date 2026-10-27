"""
Blocking / Indexing Module
Prevents combinatorial explosion using smart blocking strategies.
"""

from typing import List, Set, Tuple
import pandas as pd
from itertools import combinations


class BlockingEngine:
    """Implements various blocking strategies for entity resolution."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.blocks = {}
    
    def create_soundex_blocks(self) -> dict:
        """Block by Soundex code of names."""
        blocks = {}
        for idx, row in self.df.iterrows():
            if row.get('soundex'):
                key = row['soundex']
                if key not in blocks:
                    blocks[key] = []
                blocks[key].append(idx)
        self.blocks['soundex'] = blocks
        return blocks
    
    def create_metaphone_blocks(self) -> dict:
        """Block by Metaphone code of names."""
        blocks = {}
        for idx, row in self.df.iterrows():
            if row.get('metaphone'):
                key = row['metaphone']
                if key not in blocks:
                    blocks[key] = []
                blocks[key].append(idx)
        self.blocks['metaphone'] = blocks
        return blocks
    
    def create_zip_blocks(self) -> dict:
        """Block by ZIP code."""
        blocks = {}
        for idx, row in self.df.iterrows():
            if row.get('zip_std'):
                key = row['zip_std']
                if key not in blocks:
                    blocks[key] = []
                blocks[key].append(idx)
        self.blocks['zip'] = blocks
        return blocks
    
    def create_phone_blocks(self) -> dict:
        """Block by phone number."""
        blocks = {}
        for idx, row in self.df.iterrows():
            if row.get('phone_std'):
                key = row['phone_std']
                if key not in blocks:
                    blocks[key] = []
                blocks[key].append(idx)
        self.blocks['phone'] = blocks
        return blocks
    
    def create_dob_blocks(self) -> dict:
        """Block by Date of Birth."""
        blocks = {}
        for idx, row in self.df.iterrows():
            if row.get('dob'):
                key = str(row['dob'])
                if key not in blocks:
                    blocks[key] = []
                blocks[key].append(idx)
        self.blocks['dob'] = blocks
        return blocks
    
    def create_device_blocks(self) -> dict:
        """Block by Device ID."""
        blocks = {}
        for idx, row in self.df.iterrows():
            if row.get('device_id'):
                key = str(row['device_id'])
                if key not in blocks:
                    blocks[key] = []
                blocks[key].append(idx)
        self.blocks['device'] = blocks
        return blocks
    
    def get_candidate_pairs(self, min_block_size: int = 2, max_block_size: int = 100) -> Set[Tuple[int, int]]:
        """
        Generate candidate pairs from all blocking strategies.
        Combines multiple blocking keys for better coverage.
        """
        candidate_pairs = set()
        
        # Create all blocks
        self.create_soundex_blocks()
        self.create_metaphone_blocks()
        self.create_zip_blocks()
        self.create_phone_blocks()
        self.create_dob_blocks()
        self.create_device_blocks()
        
        # Generate pairs from each block
        for block_type, blocks in self.blocks.items():
            for key, indices in blocks.items():
                if min_block_size <= len(indices) <= max_block_size:
                    # Generate all pairs in this block
                    for pair in combinations(sorted(indices), 2):
                        candidate_pairs.add(pair)
        
        return candidate_pairs
    
    def get_blocking_statistics(self) -> dict:
        """Get statistics about blocking efficiency."""
        candidate_pairs = self.get_candidate_pairs()
        total_possible = (len(self.df) * (len(self.df) - 1)) // 2
        
        return {
            'total_records': len(self.df),
            'total_possible_pairs': total_possible,
            'candidate_pairs': len(candidate_pairs),
            'reduction_ratio': 1 - (len(candidate_pairs) / total_possible) if total_possible > 0 else 0,
            'reduction_percentage': f"{(1 - len(candidate_pairs) / total_possible) * 100:.2f}%" if total_possible > 0 else "0%"
        }
