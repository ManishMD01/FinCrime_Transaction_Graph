"""
BigQuery Configuration Loader
"""

import os
from pathlib import Path


class BigQueryConfig:
    def __init__(self, config_dir=None):
        if config_dir is None:
            config_dir = Path(__file__).parent
        self.config_dir = Path(config_dir)
        self._load_config()
    
    def _load_config(self):
        env_file = self.config_dir / '.env'
        if env_file.exists():
            self._load_env_file(env_file)
        
        self.project_id = os.environ.get('GCP_PROJECT_ID') or os.environ.get('BQ_PROJECT_ID') or 'nalen-458109'
        self.dataset_id = os.environ.get('BQ_DATASET_ID', 'fincrime_er')
        self.location = os.environ.get('BQ_LOCATION', 'US')
        self.credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '')
        self.environment = os.environ.get('ENVIRONMENT', 'dev')
    
    def _load_env_file(self, env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if value.strip():
                        os.environ[key.strip()] = value.strip()
                    elif key.strip() not in os.environ:
                        os.environ[key.strip()] = ''
    
    def get_full_table_id(self, table_name: str) -> str:
        return f"{self.project_id}.{self.dataset_id}.{table_name}"
    
    def get_dataset_ref(self) -> str:
        return f"{self.project_id}.{self.dataset_id}"
    
    def get_config(self):
        return {
            'project_id': self.project_id,
            'dataset_id': self.dataset_id,
            'location': self.location,
            'credentials_path': self.credentials_path,
            'environment': self.environment,
            'dataset_ref': self.get_dataset_ref()
        }
    
    def validate(self):
        errors = []
        if self.project_id == 'your-gcp-project-id':
            errors.append("GCP_PROJECT_ID not set")
        # Don't require credentials in Cloud Shell
        return errors


config = BigQueryConfig()
