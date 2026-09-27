"""
Bronze Layer: Copy raw data without modifications
Purpose: Preserve original data for audit and recovery
"""

import pandas as pd
import shutil
from pathlib import Path
from datetime import datetime


class BronzeLayer:
    def __init__(self, raw_dir='data/raw', bronze_dir='data/bronze'):
        self.raw_dir = Path(raw_dir)
        self.bronze_dir = Path(bronze_dir)
        self.bronze_dir.mkdir(parents=True, exist_ok=True)
        
        # Create log directory
        self.log_dir = Path('logs')
        self.log_dir.mkdir(exist_ok=True)
        
    def copy_to_bronze(self):
        """Copy all raw files to bronze layer"""
        print("="*60)
        print("BRONZE LAYER: Copying raw data")
        print("="*60)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.log_dir / f'bronze_layer_{timestamp}.log'
        
        with open(log_file, 'w') as log:
            log.write(f"Bronze Layer Processing - {timestamp}\n")
            log.write("="*60 + "\n\n")
            
            for file in self.raw_dir.glob('*.csv'):
                print(f"\nProcessing: {file.name}")
                log.write(f"File: {file.name}\n")
                
                # Get file size
                size_mb = file.stat().st_size / (1024 * 1024)
                print(f"Size: {size_mb:.2f} MB")
                log.write(f"Size: {size_mb:.2f} MB\n")
                
                # Copy file
                dest = self.bronze_dir / file.name
                shutil.copy2(file, dest)
                
                # Verify copy
                if dest.exists():
                    print(f"✓ Successfully copied to {dest}")
                    log.write(f"Status: SUCCESS\n")
                else:
                    print(f"✗ Failed to copy {file.name}")
                    log.write(f"Status: FAILED\n")
                
                log.write("\n")
        
        print(f"\n✓ Bronze layer complete. Log saved to {log_file}")


if __name__ == "__main__":
    bronze = BronzeLayer()
    bronze.copy_to_bronze()

