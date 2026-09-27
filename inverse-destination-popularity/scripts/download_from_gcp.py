"""
Download datasets from GCP Cloud Storage with proper naming
"""

import os
import sys
from pathlib import Path
import requests
from urllib.parse import urlparse

# GCP Cloud Storage URLs
GCP_URLS = {
    'attractions_data_USA.csv': 'https://storage.googleapis.com/bdt_data_raw/cleaned_data_USA.csv',
    'poi_data_osm.csv': 'https://storage.googleapis.com/bdt_data_raw/merged_file.csv',
    'flight_data_2018_2024.csv': 'https://storage.googleapis.com/bdt_data_raw/flight_data_2018_2024.csv',
    'flight_data.parquet': 'https://storage.googleapis.com/bdt_data_raw/flight_data.parquet'
}


def download_file(url: str, destination: Path, chunk_size: int = 8192):
    """Download a file from URL with progress indication"""
    print(f"Downloading: {url}")
    
    try:
        # First try public download (works if bucket is public)
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        print(f"\r  Progress: {progress:.1f}% ({downloaded / 1024 / 1024:.1f} MB / {total_size / 1024 / 1024:.1f} MB)", 
                              end='', flush=True)
        
        print(f"\n  ✓ Saved to: {destination}")
        return True
        
    except requests.exceptions.RequestException as e:
        # If public download fails, try authenticated download
        if "403" in str(e) or "401" in str(e):
            print(f"  ⚠ Public access denied, trying authenticated download...")
            try:
                from google.cloud import storage
                import os
                
                # Parse bucket and blob name from URL
                # URL format: https://storage.googleapis.com/BUCKET_NAME/blob_name
                parsed = urlparse(url)
                # Extract bucket name from path (first part after /)
                path_parts = parsed.path.lstrip('/').split('/', 1)
                bucket_name = path_parts[0]
                blob_name = path_parts[1] if len(path_parts) > 1 else ''
                
                # Set project if not already set
                project_id = os.environ.get('GOOGLE_CLOUD_PROJECT', 'imanager')
                
                client = storage.Client(project=project_id)
                bucket = client.bucket(bucket_name)
                blob = bucket.blob(blob_name)
                
                print(f"  Using authenticated download (project: {project_id})...")
                blob.download_to_filename(str(destination))
                print(f"  ✓ Saved to: {destination}")
                return True
            except ImportError:
                print(f"  ✗ google-cloud-storage not installed.")
                print(f"     Install with: pip install google-cloud-storage")
                print(f"     Or run: gcloud auth application-default login")
                return False
            except Exception as auth_error:
                print(f"  ✗ Authentication failed: {auth_error}")
                print(f"  💡 Tip: Run: gcloud auth application-default login")
                return False
        else:
            print(f"\n  ✗ Error downloading: {e}")
            return False
    except Exception as e:
        print(f"\n  ✗ Error: {e}")
        return False


def download_all_datasets(raw_dir: Path):
    """Download all datasets from GCP with proper naming"""
    print("="*60)
    print("DOWNLOADING DATASETS FROM GCP CLOUD STORAGE")
    print("="*60)
    
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    total_count = len(GCP_URLS)
    
    for filename, url in GCP_URLS.items():
        destination = raw_dir / filename
        print(f"\n[{success_count + 1}/{total_count}] {filename}")
        
        if download_file(url, destination):
            success_count += 1
    
    print("\n" + "="*60)
    print(f"✓ Download complete: {success_count}/{total_count} files downloaded")
    print("="*60)
    
    return success_count == total_count


if __name__ == "__main__":
    # Get project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Change to project root
    os.chdir(project_root)
    
    # Download to data/raw
    raw_dir = project_root / 'data' / 'raw'
    success = download_all_datasets(raw_dir)
    
    if success:
        print("\n✓ All datasets downloaded successfully!")
        print("You can now run the pipeline with: python scripts/run_local_pipeline.py")
    else:
        print("\n✗ Some downloads failed. Please check the errors above.")
        sys.exit(1)

