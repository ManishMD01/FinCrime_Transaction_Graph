"""
Entity Resolution Pipeline
Orchestrates the full ER process.
"""

from typing import Tuple, List
import pandas as pd
from .standardize import DataStandardizer
from .blocking import BlockingEngine
from .matching import FuzzyMatcher
from .clustering import EntityClusterer


class EntityResolutionPipeline:
    """Complete Entity Resolution pipeline."""
    
    def __init__(self, match_threshold: float = 0.75):
        self.match_threshold = match_threshold
        self.standardizer = DataStandardizer()
        self.blocker = None
        self.matcher = None
        self.clusterer = EntityClusterer()
        self.matches = []
    
    def resolve(self, customers_df: pd.DataFrame, transactions_df: pd.DataFrame = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Run full ER pipeline on customer data.
        Returns (resolved_customers_df, golden_entities_df)
        """
        print("Step 1: Data Standardization...")
        customers_std = self.standardizer.standardize_all(customers_df)
        
        print("Step 2: Blocking/Indexing...")
        self.blocker = BlockingEngine(customers_std)
        candidate_pairs = self.blocker.get_candidate_pairs()
        blocking_stats = self.blocker.get_blocking_statistics()
        print(f"  - Reduced from {blocking_stats['total_possible_pairs']} to {blocking_stats['candidate_pairs']} pairs ({blocking_stats['reduction_percentage']} reduction)")
        
        print("Step 3: Record Linkage (Fuzzy Matching)...")
        self.matcher = FuzzyMatcher(customers_std)
        self.matches = []
        for idx1, idx2 in candidate_pairs:
            is_match, score, scores_detail = self.matcher.is_match(idx1, idx2, self.match_threshold)
            if is_match:
                self.matches.append((idx1, idx2, score))
        print(f"  - Found {len(self.matches)} matching pairs")
        
        print("Step 4: Graph Clustering...")
        self.clusterer.build_match_graph(customers_std, self.matches)
        self.clusterer.find_connected_components()
        resolved_customers = self.clusterer.create_golden_entities(customers_std)
        clustering_stats = self.clusterer.get_cluster_statistics()
        print(f"  - Created {clustering_stats['total_clusters']} golden entities ({clustering_stats['clusters_with_matches']} with multiple records)")
        
        if self.clusterer.golden_df is None or len(self.clusterer.golden_df) == 0:
            self.clusterer.golden_df = pd.DataFrame(columns=['golden_entity_id', 'member_count'])
        return resolved_customers, self.clusterer.golden_df
