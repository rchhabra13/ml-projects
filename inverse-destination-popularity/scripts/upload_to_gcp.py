"""
Upload cleaned datasets to GCP Cloud Storage
"""

from google.cloud import storage
from pathlib import Path
import os
import sys

# Configuration
BUCKET_NAME = 'bdt_data_raw'
PROJECT_ID = os.environ.get('GOOGLE_CLOUD_PROJECT', 'imanager')

# Files to upload from silver layer
FILES_TO_UPLOAD = {
    'attractions_data_cleaned.parquet': 'silver/attractions_data_cleaned.parquet',
    'flight_data_cleaned.parquet': 'silver/flight_data_cleaned.parquet',
    'poi_data_cleaned.parquet': 'silver/poi_data_cleaned.parquet',
}


def upload_file_to_gcp(local_path: Path, gcp_path: str, bucket):
    """Upload a single file to GCP Cloud Storage"""
    print(f"Uploading: {local_path.name} → gs://{bucket.name}/{gcp_path}")
    
    try:
        blob = bucket.blob(gcp_path)
        
        # Upload with progress indication
        file_size = local_path.stat().st_size
        print(f"  File size: {file_size / 1024 / 1024:.2f} MB")
        
        blob.upload_from_filename(str(local_path))
        
        print(f"  ✓ Upload complete")
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def upload_cleaned_data():
    """Upload all cleaned data from silver layer to GCP"""
    print("="*60)
    print("UPLOADING CLEANED DATA TO GCP CLOUD STORAGE")
    print("="*60)
    print(f"Bucket: {BUCKET_NAME}")
    print(f"Project: {PROJECT_ID}\n")
    
    # Get project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    silver_dir = project_root / 'data' / 'silver'
    
    if not silver_dir.exists():
        print("✗ Silver layer directory not found!")
        print("Run the pipeline first: python scripts/run_local_pipeline.py")
        sys.exit(1)
    
    try:
        # Initialize client
        client = storage.Client(project=PROJECT_ID)
        bucket = client.bucket(BUCKET_NAME)
        
        success_count = 0
        total_count = len(FILES_TO_UPLOAD)
        
        for filename, gcp_path in FILES_TO_UPLOAD.items():
            local_file = silver_dir / filename
            
            if not local_file.exists():
                print(f"\n[{success_count + 1}/{total_count}] {filename}")
                print(f"  ⚠ Warning: File not found locally")
                continue
            
            print(f"\n[{success_count + 1}/{total_count}] {filename}")
            
            if upload_file_to_gcp(local_file, gcp_path, bucket):
                success_count += 1
        
        print("\n" + "="*60)
        print(f"✓ Upload complete: {success_count}/{total_count} files uploaded")
        print("="*60)
        
        if success_count > 0:
            print(f"\n✓ Files uploaded to: gs://{BUCKET_NAME}/silver/")
            print("\nYou can now access them from:")
            for filename, gcp_path in FILES_TO_UPLOAD.items():
                if (silver_dir / filename).exists():
                    print(f"  gs://{BUCKET_NAME}/{gcp_path}")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure you have:")
        print("1. gcloud CLI installed and authenticated")
        print("2. GOOGLE_CLOUD_PROJECT environment variable set")
        print("3. Proper permissions on the bucket")
        sys.exit(1)


if __name__ == "__main__":
    upload_cleaned_data()

