"""
BigQuery-integrated Entity Resolution Pipeline
"""

from datetime import datetime
from .bq_client import BigQueryClient
from ..er.pipeline import EntityResolutionPipeline


class BigQueryERPipeline:
    """ER Pipeline that reads from and writes to BigQuery"""
    
    def __init__(self, match_threshold=0.75):
        self.bq_client = BigQueryClient()
        self.pipeline = EntityResolutionPipeline(match_threshold=match_threshold)
    
    def run_with_historical_data(self, days_back=365):
        """Run ER on historical data from BigQuery"""
        print(f"Loading historical data (last {days_back} days)...")
        customers_df = self.bq_client.get_historical_customers(days_back)
        transactions_df = self.bq_client.get_historical_transactions(days_back)
        
        print(f"Loaded {len(customers_df)} customers, {len(transactions_df)} transactions")
        
        # Run ER pipeline
        resolved_customers, golden_entities = self.pipeline.resolve(customers_df, transactions_df)
        
        if resolved_customers is None or len(resolved_customers) == 0:
            import pandas as pd
            return pd.DataFrame(), pd.DataFrame()
        
        # Add metadata
        try:
            resolved_customers['resolution_date'] = datetime.now()
            resolved_customers['batch_id'] = f"ER_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            if golden_entities is not None and len(golden_entities) > 0:
                golden_entities['created_date'] = datetime.now()
                golden_entities['last_updated'] = datetime.now()
                golden_entities['batch_id'] = resolved_customers['batch_id'].iloc[0]
        except:
            pass
        
        # Write to BigQuery
        print("Writing results to BigQuery...")
        self.bq_client.dataframe_to_table(resolved_customers, 'resolved_customers', if_exists='append')
        self.bq_client.dataframe_to_table(golden_entities, 'golden_entities', if_exists='append')
        
        return resolved_customers, golden_entities
    
    def run_with_new_data(self, since_date):
        """Run ER on new data loaded since specific date"""
        print(f"Loading new data since {since_date}...")
        customers_df = self.bq_client.get_new_customers_since(since_date)
        transactions_df = self.bq_client.get_new_transactions_since(since_date)
        
        print(f"Loaded {len(customers_df)} new customers, {len(transactions_df)} new transactions")
        
        resolved_customers, golden_entities = self.pipeline.resolve(customers_df, transactions_df)
        
        resolved_customers['resolution_date'] = datetime.now()
        golden_entities['created_date'] = datetime.now()
        golden_entities['last_updated'] = datetime.now()
        
        self.bq_client.dataframe_to_table(resolved_customers, 'resolved_customers', if_exists='append')
        self.bq_client.dataframe_to_table(golden_entities, 'golden_entities', if_exists='append')
        
        return resolved_customers, golden_entities
