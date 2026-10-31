"""
Graph Clustering Module
Merges resolved records into golden entities using connected components.
"""

from typing import Dict, List, Set, Tuple
import pandas as pd
import networkx as nx


class EntityClusterer:
    """Clusters matching records into golden entities."""
    
    def __init__(self):
        self.graph = nx.Graph()
        self.clusters = {}
        self.golden_entities = {}
        self.golden_df = None
    
    def build_match_graph(self, df: pd.DataFrame, matches: List[Tuple[int, int, float]]) -> nx.Graph:
        """Build undirected graph where edges represent matches."""
        self.graph = nx.Graph()
        
        # Add all nodes
        for idx in df.index:
            self.graph.add_node(idx)
        
        # Add edges for matches
        for idx1, idx2, score in matches:
            if score >= 0.75:  # Match threshold
                self.graph.add_edge(idx1, idx2, weight=score)
        
        return self.graph
    
    def find_connected_components(self) -> Dict[int, int]:
        """Find connected components using NetworkX."""
        components = list(nx.connected_components(self.graph))
        
        # Assign cluster IDs
        self.clusters = {}
        for cluster_id, component in enumerate(components):
            for node in component:
                self.clusters[node] = cluster_id
        
        return self.clusters
    
    def create_golden_entities(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create golden entity records by merging cluster members."""
        if len(df) == 0:
            df_result = df.copy()
            df_result['cluster_id'] = []
            df_result['golden_entity_id'] = []
            self.golden_df = pd.DataFrame()
            return df_result
        if not self.clusters:
            self.find_connected_components()
        
        df_result = df.copy()
        df_result['cluster_id'] = df_result.index.map(self.clusters)
        df_result['golden_entity_id'] = df_result['cluster_id']
        
        # Create golden entity summary
        golden_list = []
        for cluster_id, group in df_result.groupby('cluster_id'):
            # Create a consolidated golden entity
            golden = {
                'golden_entity_id': cluster_id,
                'member_count': len(group),
                'member_ids': group['customer_id'].tolist() if 'customer_id' in group.columns else group.index.tolist(),
                # Golden attributes - prefer non-null, most complete
                'primary_name': group['full_name_clean'].dropna().iloc[0] if not group['full_name_clean'].dropna().empty else '',
                'primary_phone': group['phone_std'].dropna().iloc[0] if not group['phone_std'].dropna().empty else '',
                'primary_email': group['email_std'].dropna().iloc[0] if not group['email_std'].dropna().empty else '',
                'primary_address': group['address_clean'].dropna().iloc[0] if not group['address_clean'].dropna().empty else '',
                'all_ssns': group['ssn_std'].dropna().unique().tolist(),
                'all_devices': group['device_id'].dropna().unique().tolist() if 'device_id' in group.columns else [],
                'all_ips': group['ip_address'].dropna().unique().tolist() if 'ip_address' in group.columns else [],
                'all_emails': group['email_std'].dropna().unique().tolist(),
                'all_phones': group['phone_std'].dropna().unique().tolist(),
            }
            golden_list.append(golden)
            self.golden_entities[cluster_id] = golden
        
        self.golden_df = pd.DataFrame(golden_list)
        return df_result
    
    def get_cluster_statistics(self) -> Dict:
        """Get clustering statistics."""
        if not self.clusters:
            return {
                'total_clusters': 0,
                'total_nodes': 0,
                'singletons': 0,
                'clusters_with_matches': 0,
                'largest_cluster_size': 0,
                'average_cluster_size': 0,
            }

