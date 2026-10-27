#!/usr/bin/env python3
"""
Setup BigQuery - Create dataset and tables
"""

import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from bigquery.config.config import config
from google.cloud import bigquery

class BigQuerySetup:
    def __init__(self):
        self.config = config
        self.client = bigquery.Client(project=self.config.project_id, location=self.config.location)
        
        errors = self.config.validate()
        if errors:
            print("Configuration errors:")
            for e in errors:
                print(f"  - {e}")
            print("\nPlease set up bigquery/config/.env with your values")
            sys.exit(1)
    
    def create_dataset(self):
        """Create BigQuery dataset if not exists"""
        dataset_id = f"{self.config.project_id}.{self.config.dataset_id}"
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = self.config.location
        dataset.description = "FinCrime Entity Resolution and AML Detection"
        dataset.labels = {"domain": "fincrime", "env": self.config.environment}
        
        try:
            dataset = self.client.create_dataset(dataset, exists_ok=True)
            print(f"Dataset {dataset_id} created/exists")
        except Exception as e:
            print(f"Error creating dataset: {e}")
            raise
    
    def run_ddl_scripts(self):
        """Run all DDL scripts with project ID substitution"""
        ddl_dir = Path(__file__).parent.parent / 'ddl'
        ddl_files = sorted(ddl_dir.glob('*.sql'))
        
        for ddl_file in ddl_files:
            print(f"Running {ddl_file.name}...")
            with open(ddl_file) as f:
                sql = f.read()
            
            # Replace placeholder with actual project ID
            sql = sql.replace('your-project-id', self.config.project_id)
            
            try:
                job = self.client.query(sql)
                job.result()
                print(f"  ✓ {ddl_file.name} completed")
            except Exception as e:
                print(f"  ✗ Error in {ddl_file.name}: {e}")
    
    def setup_all(self):
        """Run complete setup"""
        print(f"Setting up BigQuery for project: {self.config.project_id}")
        print(f"Dataset: {self.config.dataset_id}")
        print(f"Location: {self.config.location}")
        print("-" * 50)
        
        self.create_dataset()
        self.run_ddl_scripts()
        
        print("-" * 50)
        print("Setup complete!")

if __name__ == '__main__':
    setup = BigQuerySetup()
    setup.setup_all()
