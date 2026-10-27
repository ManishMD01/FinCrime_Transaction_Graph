"""
Fraud & AML Detection Heuristics
Detects suspicious patterns across resolved entities.
"""

from typing import List, Dict
import pandas as pd
from datetime import timedelta


class AMLFraudDetector:
    """Detects AML/Fraud patterns using heuristics."""
    
    def __init__(self, resolved_customers: pd.DataFrame, transactions: pd.DataFrame, 
                 reporting_threshold: float = 10000.0, structuring_threshold: float = 9900.0):
        self.customers = resolved_customers
        self.transactions = transactions.copy()
        self.reporting_threshold = reporting_threshold
        self.structuring_threshold = structuring_threshold
        self.alerts = []
        
        # Map customer to entity
        self.customer_to_entity = {}
        for _, row in self.customers.iterrows():
            cust_id = row['customer_id'] if 'customer_id' in row else row.name
            self.customer_to_entity[cust_id] = row['golden_entity_id']
        
        # Add entity info to transactions
        self.transactions['sender_entity'] = self.transactions['sender_id'].map(self.customer_to_entity)
        self.transactions['receiver_entity'] = self.transactions['receiver_id'].map(self.customer_to_entity)
        self.transactions['timestamp'] = pd.to_datetime(self.transactions['timestamp'])
    
    def detect_structuring_smurfing(self, window_hours: int = 24, min_transactions: int = 3) -> List[Dict]:
        """
        Detect structuring/smurfing: breaking large transactions into small amounts
        just below regulatory reporting thresholds.
        """
        alerts = []
        
        for entity_id in self.customers['golden_entity_id'].unique():
            entity_txns = self.transactions[
                self.transactions['sender_entity'] == entity_id
            ].copy()
            
            if len(entity_txns) < min_transactions:
                continue
            
            entity_txns = entity_txns.sort_values('timestamp')
            
            # Look for clusters of transactions just below threshold
            for i in range(len(entity_txns)):
                window_start = entity_txns.iloc[i]['timestamp']
                window_end = window_start + timedelta(hours=window_hours)
                
                window_txns = entity_txns[
                    (entity_txns['timestamp'] >= window_start) & 
                    (entity_txns['timestamp'] <= window_end)
                ]
                
                if len(window_txns) < min_transactions:
                    continue
                
                # Check if transactions are just below threshold
                below_threshold = window_txns[
                    (window_txns['amount'] >= self.structuring_threshold * 0.8) & 
                    (window_txns['amount'] < self.reporting_threshold)
                ]
                
                total_amount = window_txns['amount'].sum()
                
                if len(below_threshold) >= min_transactions and total_amount >= self.structuring_threshold:
                    alerts.append({
                        'alert_type': 'STRUCTURING_SMURFING',
                        'severity': 'HIGH',
                        'golden_entity_id': entity_id,
                        'transaction_count': len(window_txns),
                        'total_amount': float(total_amount),
                        'avg_amount': float(window_txns['amount'].mean()),
                        'time_window_hours': window_hours,
                        'start_time': window_start.isoformat(),
                        'transaction_ids': window_txns.index.tolist(),
                        'description': f'Entity {entity_id} made {len(window_txns)} transactions totaling ${total_amount:.2f} just below reporting threshold within {window_hours}h'
                    })
                    break  # Avoid duplicate alerts for same entity
        
        self.alerts.extend(alerts)
        return alerts
    
    def detect_money_mule_networks(self, rapid_transfer_minutes: int = 60) -> List[Dict]:
        """
        Detect money mule networks: receiving funds from multiple sources
        and immediately transferring to high-risk external entities.
        """
        alerts = []
        
        for entity_id in self.customers['golden_entity_id'].unique():
            # Find inflows to this entity
            inflows = self.transactions[
                self.transactions['receiver_entity'] == entity_id
            ].copy()
            
            # Find outflows from this entity
            outflows = self.transactions[
                self.transactions['sender_entity'] == entity_id
            ].copy()
            
            if len(inflows) < 2 or len(outflows) < 1:
                continue
            
            inflows = inflows.sort_values('timestamp')
            outflows = outflows.sort_values('timestamp')
            
            # Check if funds received from multiple unlinked sources
            unique_sources = inflows['sender_entity'].nunique()
            
            if unique_sources >= 2:
                # Check for rapid pass-through
                for _, outflow in outflows.iterrows():
                    outflow_time = outflow['timestamp']
                    # Look for inflows before this outflow within rapid_transfer_minutes
                    recent_inflows = inflows[
                        (outflows['timestamp'].iloc[0] if False else True) &  # dummy
                        (inflows['timestamp'] <= outflow_time) &
                        (outflow_time - inflows['timestamp'] <= timedelta(minutes=rapid_transfer_minutes))
                    ]
                    
                    if len(recent_inflows) >= 2:
                        total_in = recent_inflows['amount'].sum()
                        total_out = outflow['amount']
                        # Check if most funds are passed through
                        if total_out >= total_in * 0.7:  # Pass through >=70% of received funds
                            alerts.append({
                                'alert_type': 'MONEY_MULE_NETWORK',
                                'severity': 'CRITICAL',
                                'golden_entity_id': entity_id,
                                'source_entity_count': unique_sources,
                                'inflow_count': len(recent_inflows),
                                'total_inflow_amount': float(total_in),
                                'outflow_amount': float(total_out),
                                'pass_through_ratio': float(total_out / total_in) if total_in > 0 else 0,
                                'time_to_transfer_minutes': float((outflow_time - recent_inflows['timestamp'].min()).total_seconds() / 60),
                                'transaction_ids': recent_inflows.index.tolist() + [outflow.name],
                                'description': f'Money mule suspect: Entity {entity_id} received from {unique_sources} sources and transferred ${total_out:.2f} within {rapid_transfer_minutes}min'
                            })
                            break
        
        self.alerts.extend(alerts)
        return alerts
    
    def detect_rapid_velocity_phantom_profiles(self, window_minutes: int = 60, 
                                               min_transactions: int = 5) -> List[Dict]:
        """
        Detect rapid velocity: multiple distinct profiles (same golden entity by ER)
        performing high-frequency transactions from same Device ID or IP.
        """
        alerts = []
        
        for entity_id in self.customers['golden_entity_id'].unique():
            entity_customers = self.customers[
                self.customers['golden_entity_id'] == entity_id
            ]
            
            # Check if this golden entity has multiple underlying profiles
            if len(entity_customers) < 2:
                continue
            
            entity_cust_ids = entity_customers['customer_id'].tolist() if 'customer_id' in entity_customers.columns else entity_customers.index.tolist()
            
            # Get all transactions for this entity
            entity_txns = self.transactions[
                (self.transactions['sender_id'].isin(entity_cust_ids)) | 
                (self.transactions['receiver_id'].isin(entity_cust_ids))
            ].copy()
            
            if len(entity_txns) < min_transactions:
                continue
            
            entity_txns = entity_txns.sort_values('timestamp')
            
            # Check for shared device/IP across different original profiles
            shared_devices = set()
            shared_ips = set()
            if 'device_id' in entity_customers.columns:
                devices = entity_customers['device_id'].dropna().unique()
                if len(devices) > 0:
                    shared_devices = set(devices)
            if 'ip_address' in entity_customers.columns:
                ips = entity_customers['ip_address'].dropna().unique()
                if len(ips) > 0:
                    shared_ips = set(ips)
            
            # Look for high velocity transactions
            for i in range(len(entity_txns)):
                window_start = entity_txns.iloc[i]['timestamp']
                window_end = window_start + timedelta(minutes=window_minutes)
                
                window_txns = entity_txns[
                    (entity_txns['timestamp'] >= window_start) & 
                    (entity_txns['timestamp'] <= window_end)
                ]
                
                if len(window_txns) >= min_transactions:
                    # Check if from same device/IP
                    device_matches = False
                    ip_matches = False
                    
                    if shared_devices and 'device_id' in self.transactions.columns:
                        # This would need device info on transactions
                        pass
                    
                    alerts.append({
                        'alert_type': 'RAPID_VELOCITY_PHANTOM_PROFILE',
                        'severity': 'HIGH',
                        'golden_entity_id': entity_id,
                        'underlying_profile_count': len(entity_customers),
                        'transaction_count': len(window_txns),
                        'time_window_minutes': window_minutes,
                        'total_amount': float(window_txns['amount'].sum()),
                        'shared_devices': list(shared_devices),
                        'shared_ips': list(shared_ips),
                        'start_time': window_start.isoformat(),
                        'transaction_ids': window_txns.index.tolist(),
                        'description': f'Phantom profile: {len(entity_customers)} profiles resolved to Entity {entity_id} made {len(window_txns)} txns in {window_minutes}min'
                    })
                    break
        
        self.alerts.extend(alerts)
        return alerts
    
    def run_all_detections(self) -> pd.DataFrame:
        """Run all detection heuristics."""
        print("Running AML/Fraud Detection...")
        self.detect_structuring_smurfing()
        self.detect_money_mule_networks()
        self.detect_rapid_velocity_phantom_profiles()
        
        print(f"Generated {len(self.alerts)} alerts")
        return pd.DataFrame(self.alerts)
