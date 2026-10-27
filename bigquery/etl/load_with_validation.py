#!/usr/bin/env python3
"""
ETL Data Loader with Validation and File Tracking
Prevents duplicate loads and tracks loaded/unloaded files
"""

import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
import pandas as pd
from validate_data import DataValidator
from load_new_data import NewDataLoader

class ValidatedETLLoader:
    def __init__(self):
        self.validator = DataValidator()
        self.loader = NewDataLoader()
        self.incoming_dir = Path('data/incoming')
        self.loaded_dir = Path('data/loaded')
        self.unloaded_dir = Path('data/unloaded')
        self.rejected_dir = Path('data/rejected')
        
        # Create directories
        for d in [self.incoming_dir, self.loaded_dir, self.unloaded_dir, self.rejected_dir]:
            d.mkdir(parents=True, exist_ok=True)
    
    def process_file(self, filepath, file_type):
        """Process a single file with validation"""
        filepath = Path(filepath)
        print(f"\n{'='*60}")
        print(f"Processing: {filepath.name}")
        print(f"{'='*60}")
        
        # Check if already loaded
        already_loaded, reason = self.validator.is_file_already_loaded(filepath)
        if already_loaded:
            print(f"⚠️  SKIPPED: {reason}")
            dest = self.loaded_dir / filepath.name
            if not dest.exists():
                shutil.copy(filepath, dest)
                print(f"   Moved to: {dest}")
            return False
        
        # Track file
        batch_id = f"ETL_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        file_id = self.validator.track_file(filepath, file_type, batch_id, 'LOADING')
        
        try:
            # Load and validate
            df = pd.read_csv(filepath)
            print(f"✓ Read {len(df)} rows")
            
            if file_type == 'customers':
                valid, errors = self.validator.validate_customers(df)
            elif file_type == 'transactions':
                valid, errors = self.validator.validate_transactions(df)
            else:
                valid, errors = False, ["Unknown file type"]
            
            if not valid:
                print(f"✗ Validation FAILED:")
                for err in errors:
                    print(f"   - {err}")
                dest = self.rejected_dir / filepath.name
                shutil.move(filepath, dest)
                # Update tracking
                print(f"   Moved to rejected: {dest}")
                return False
            
            print(f"✓ Validation PASSED")
            
            # Load to BigQuery
            if file_type == 'customers':
                self.loader.load_new_customers(df, source_system='FILE_ETL')
            elif file_type == 'transactions':
                self.loader.load_new_transactions(df, source_system='FILE_ETL')
            
            # Move to loaded
            dest = self.loaded_dir / filepath.name
            shutil.move(filepath, dest)
            print(f"✓ Successfully loaded and moved to: {dest}")
            
            # Update tracking status
            return True
            
        except Exception as e:
            print(f"✗ ERROR: {e}")
            dest = self.rejected_dir / filepath.name
            if filepath.exists():
                shutil.move(filepath, dest)
            print(f"   Moved to rejected: {dest}")
            return False
    
    def process_incoming(self):
        """Process all files in incoming directory"""
        print("\n" + "="*60)
        print("ETL File Processor - Checking for new files")
        print("="*60)
        
        incoming_files = list(self.incoming_dir.glob('*.csv'))
        if not incoming_files:
            print("\nNo files found in data/incoming/")
            print(f"Place CSV files in: {self.incoming_dir}")
            return
        
        print(f"\nFound {len(incoming_files)} file(s) in incoming/")
        
        for f in incoming_files:
            name = f.name.lower()
            if 'customer' in name:
                self.process_file(f, 'customers')
            elif 'transaction' in name:
                self.process_file(f, 'transactions')
            else:
                print(f"\n⚠️  Skipping {f.name} - cannot determine type (need 'customer' or 'transaction' in filename)")
                dest = self.unloaded_dir / f.name
                shutil.move(f, dest)
        
        print("\n" + "="*60)
        print("Processing Complete")
        print("="*60)
        print(f"Loaded: {len(list(self.loaded_dir.glob('*.csv')))} files")
        print(f"Rejected: {len(list(self.rejected_dir.glob('*.csv')))} files")
        print(f"Unloaded: {len(list(self.unloaded_dir.glob('*.csv')))} files")
        print("="*60)

if __name__ == '__main__':
    processor = ValidatedETLLoader()
    processor.process_incoming()
