"""
BigQuery Configuration Loader
Centralized configuration management for BigQuery integration
"""

import os
import json
from pathlib import Path
from typing import Dict, Any

class BigQueryConfig:
    """Load and manage BigQuery configuration from environment variables"""
    
    def __init__(self, config_dir=None):
        if config_dir is None:
            config_dir = Path(__file__).parent
        self.config_dir = Path(config_dir)
        self._load_config()
    
    def _load_config(self):
        """Load configuration from environment variables and config files"""
        # Load from .env if exists
        env_file = self.config_dir / '.env'
        if env_file.exists():
            self._load_env_file(env_file)
        
        # Core configuration
        self.project_id = os.environ.get('GCP_PROJECT_ID') or os.environ.get('BQ_PROJECT_ID') or 'your-gcp-project-id'
        self.dataset_id = os.environ.get('BQ_DATASET_ID', 'fincrime_er')
        self.location = os.environ.get('BQ_LOCATION', 'US')
        self.credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '')
        self.environment = os.environ.get('ENVIRONMENT', 'dev')
        
        # Load JSON config for additional settings
        json_config_path = self.config_dir / 'bq_config.json'
        if json_config_path.exists():
            with open(json_config_path) as f:
                self.json_config = json.load(f)
        else:
            self.json_config = {}
    
    def _load_env_file(self, env_file):
        """Simple .env file loader"""
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
    
    def get_full_table_id(self, table_name: str) -> str:
        """Get fully qualified table ID"""
        return f"{self.project_id}.{self.dataset_id}.{table_name}"
    
    def get_dataset_ref(self) -> str:
        """Get dataset reference"""
        return f"{self.project_id}.{self.dataset_id}"
    
    def get_config(self) -> Dict[str, Any]:
        """Get all configuration as dict"""
        return {
            'project_id': self.project_id,
            'dataset_id': self.dataset_id,
            'location': self.location,
            'credentials_path': self.credentials_path,
            'environment': self.environment,
            'dataset_ref': self.get_dataset_ref()
        }
    
    def validate(self):
        """Validate required configuration"""
        errors = []
        if self.project_id == 'your-gcp-project-id':
            errors.append("GCP_PROJECT_ID not set")
        if not self.credentials_path and self.environment != 'local':
            errors.append("GOOGLE_APPLICATION_CREDENTIALS not set")
        return errors

# Global config instance
config = BigQueryConfig()
