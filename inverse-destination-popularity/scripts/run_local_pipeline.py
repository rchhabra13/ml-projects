"""
Run complete local data pipeline
"""

from pathlib import Path
import sys
import os

# Get project root directory (parent of scripts directory)
script_dir = Path(__file__).parent
project_root = script_dir.parent

# Change to project root directory
os.chdir(project_root)

# Add scripts to path
sys.path.insert(0, str(script_dir))

from bronze_layer import BronzeLayer
from silver_layer import SilverLayer


def main():
    print("\n" + "="*60)
    print("STARTING LOCAL DATA PIPELINE")
    print(f"Working directory: {os.getcwd()}")
    print("="*60)
    
    # Step 1: Bronze Layer
    print("\n[1/2] Bronze Layer - Copying raw data...")
    bronze = BronzeLayer()
    bronze.copy_to_bronze()
    
    # Step 2: Silver Layer
    print("\n[2/2] Silver Layer - Cleaning data...")
    silver = SilverLayer()
    silver.run_all()
    
    print("\n" + "="*60)
    print("✓ PIPELINE COMPLETE")
    print("="*60)
    print("\nNext steps:")
    print("1. Review cleaning reports in logs/")
    print("2. Inspect cleaned data in data/silver/")
    print("3. Run feature engineering (Gold layer)")
    print("4. Upload to GCP for distributed processing")


if __name__ == "__main__":
    main()

