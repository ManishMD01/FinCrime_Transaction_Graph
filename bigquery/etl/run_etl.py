#!/usr/bin/env python3
"""
Main ETL Orchestrator for FinCrime Entity Resolution Engine
Run this from project root to execute ETL jobs
"""

import os
import sys
from pathlib import Path

# Ensure we're running from project root
PROJECT_ROOT = Path(__file__).parent.parent.parent
os.chdir(PROJECT_ROOT)
sys.path.insert(0, str(PROJECT_ROOT))

from bigquery.etl.load_with_validation import ValidatedETLLoader

def main():
    print("="*60)
    print("FinCrime ETL Job Runner")
    print("="*60)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Working Dir: {os.getcwd()}")
    print("="*60)
    
    # Process incoming files with validation
    processor = ValidatedETLLoader()
    processor.process_incoming()

if __name__ == '__main__':
    main()
