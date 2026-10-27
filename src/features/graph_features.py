"""
Transactional Feature Engineering & Graph Analytics
Builds unified Customer-Transaction Graph and extracts features.
"""

from typing import Dict, List
import pandas as pd
import networkx as nx
from datetime import timedelta


class TransactionGraphBuilder:
    """Builds and analyzes the Customer-Transaction Graph."""
    
    def __init__(self, resolved_customers: pd.DataFrame, transactions: pd.DataFrame):
        self.customers = resolved_customers
        self.transactions = transactions
        self.graph = nx.DiGraph()
        self.customer_to_entity = {}
    
    def build_graph(self) -> nx.DiGraph:
        """Construct unified Customer-Transaction Graph."""
        # Map customer IDs to golden entity IDs
        for _, row in self.customers.iterrows():
            cust_id = row['customer_id'] if 'customer_id' in row else row.name
            self.customer_to_entity[cust_id] = row['golden_entity_id']
        
        # Add nodes for golden entities
        entity_ids = self.customers['golden_entity_id'].unique()
        for entity_id in entity_ids:
            self.graph.add_node(f"ENTITY_{entity_id}", type='entity')
        
        # Add transaction edges between entities
        for _, txn in self.transactions.iterrows():
            sender = txn['sender_id']
            receiver = txn['receiver_id']
            
            sender_entity = self.customer_to_entity.get(sender)
            receiver_entity = self.customer_to_entity.get(receiver)
            
            if sender_entity is not None and receiver_entity is not None:
                sender_node = f"ENTITY_{sender_entity}"
                receiver_node = f"ENTITY_{receiver_entity}"
                
                # Add edge with transaction details
                if self.graph.has_edge(sender_node, receiver_node):
                    self.graph[sender_node][receiver_node]['weight'] += txn['amount']
                    self.graph[sender_node][receiver_node]['count'] += 1
                    self.graph[sender_node][receiver_node]['transactions'].append(txn.name)
                else:
                    self.graph.add_edge(
                        sender_node, 
                        receiver_node,
                        weight=txn['amount'],
                        count=1,
                        transactions=[txn.name],
                        first_seen=txn['timestamp'],
                        last_seen=txn['timestamp'],
                        channels=[txn.get('channel')],
                        locations=[txn.get('location')]
                    )
        
        return self.graph
    
    def extract_node_features(self) -> pd.DataFrame:
        """Extract node features for golden entities."""
        features = []
        
        # Aggregate transactions by entity
        self.transactions['sender_entity'] = self.transactions['sender_id'].map(self.customer_to_entity)
        self.transactions['receiver_entity'] = self.transactions['receiver_id'].map(self.customer_to_entity)
        
        for entity_id in self.customers['golden_entity_id'].unique():
            entity_txns_out = self.transactions[self.transactions['sender_entity'] == entity_id]
            entity_txns_in = self.transactions[self.transactions['receiver_entity'] == entity_id]
            
            all_txns = pd.concat([entity_txns_out, entity_txns_in])
            
            # Calculate features
            total_outflow = entity_txns_out['amount'].sum()
            total_inflow = entity_txns_in['amount'].sum()
            total_volume = total_outflow + total_inflow
            
            freq_out = len(entity_txns_out)
            freq_in = len(entity_txns_in)
            total_freq = freq_out + freq_in
            
            # Velocity features
            if not all_txns.empty and 'timestamp' in all_txns.columns:
                all_txns['timestamp'] = pd.to_datetime(all_txns['timestamp'])
                time_span = (all_txns['timestamp'].max() - all_txns['timestamp'].min()).total_seconds() / 3600  # hours
                velocity = total_freq / max(time_span, 1)
            else:
                velocity = 0
            
            features.append({
                'golden_entity_id': entity_id,
                'total_volume': total_volume,
                'total_inflow': total_inflow,
                'total_outflow': total_outflow,
                'transaction_frequency': total_freq,
                'outflow_frequency': freq_out,
                'inflow_frequency': freq_in,
                'net_flow': total_inflow - total_outflow,
                'avg_transaction_amount': all_txns['amount'].mean() if not all_txns.empty else 0,
                'max_transaction_amount': all_txns['amount'].max() if not all_txns.empty else 0,
                'velocity_txns_per_hour': velocity,
                'unique_counterparties': len(set(entity_txns_out['receiver_entity'].dropna()) | set(entity_txns_in['sender_entity'].dropna())),
                'member_count': len(self.customers[self.customers['golden_entity_id'] == entity_id])
            })
        
        return pd.DataFrame(features)
    
    def extract_edge_features(self) -> pd.DataFrame:
        """Extract edge features for relationships between entities."""
        edge_features = []
        
        for sender_node, receiver_node, edge_data in self.graph.edges(data=True):
            sender_id = int(sender_node.replace('ENTITY_', ''))
            receiver_id = int(receiver_node.replace('ENTITY_', ''))
            
            # Check if cross-border
            sender_locs = self.customers[self.customers['golden_entity_id'] == sender_id]['location'] if 'location' in self.customers.columns else []
            receiver_locs = self.customers[self.customers['golden_entity_id'] == receiver_id]['location'] if 'location' in self.customers.columns else []
            
            cross_border = False
            if len(sender_locs) > 0 and len(receiver_locs) > 0:
                cross_border = sender_locs.iloc[0] != receiver_locs.iloc[0]
            
            edge_features.append({
                'sender_entity': sender_id,
                'receiver_entity': receiver_id,
                'total_amount': edge_data.get('weight', 0),
                'transaction_count': edge_data.get('count', 0),
                'avg_amount': edge_data.get('weight', 0) / max(edge_data.get('count', 1), 1),
                'cross_border': cross_border,
                'channels': edge_data.get('channels', []),
                'shared_accounts': False,  # Would need additional data
            })
        
        return pd.DataFrame(edge_features)
    
    def find_hidden_networks(self, min_connections: int = 3) -> List[Dict]:
        """Find hidden networks between seemingly unrelated entities."""
        networks = []
        
        # Find strongly connected components
        try:
            sccs = list(nx.strongly_connected_components(self.graph))
            for scc in sccs:
                if len(scc) >= min_connections:
                    networks.append({
                        'type': 'strongly_connected',
                        'entities': [int(n.replace('ENTITY_', '')) for n in scc],
                        'size': len(scc)
                    })
        except:
            pass
        
        # Find cliques (highly interconnected)
        try:
            undirected = self.graph.to_undirected()
            for clique in nx.find_cliques(undirected):
                if len(clique) >= min_connections:
                    networks.append({
                        'type': 'clique',
                        'entities': [int(n.replace('ENTITY_', '')) for n in clique],
                        'size': len(clique)
                    })
        except:
            pass
        
        return networks
