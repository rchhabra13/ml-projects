# Inverse Destination Popularity

A data cleaning and preprocessing pipeline for analyzing flight data, points of interest, and tourist attractions. This project processes large-scale datasets using a Bronze-Silver-Gold data lake architecture.

## Overview

This project cleans and prepares three key datasets:
- **Flight data** - US domestic flights (2018-2024)
- **POI data** - Places of interest from OpenStreetMap
- **Attractions data** - Tourist attractions across the USA

## Quick Start

### 1. Set Up

```bash
# Create a virtual environment
python -m venv bigdata_env
source bigdata_env/bin/activate  # On Windows: bigdata_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Get Your Data

**Option A: Download from GCP Cloud Storage** (Recommended)

```bash
export GOOGLE_CLOUD_PROJECT=imanager
python scripts/download_from_gcp.py
```

**Option B: Use Local Files**

Put your CSV files in `data/raw/`:
- `attractions_data_USA.csv`
- `poi_data_osm.csv`
- `flight_data_2018_2024.csv`

### 3. Run the Pipeline

```bash
python scripts/run_local_pipeline.py
```

This will:
1. Copy all raw files to `data/bronze/` (Bronze Layer)
2. Clean and process data to `data/silver/` (Silver Layer)
3. Generate cleaning reports in `logs/`

## Project Structure

```
inverse-destination-popularity/
├── data/
│   ├── raw/          # Original data files
│   ├── bronze/       # Backup copies (raw data)
│   ├── silver/       # Cleaned data (Parquet format)
│   └── gold/         # Analytics-ready data (future)
├── scripts/
│   ├── bronze_layer.py          # Copy raw data
│   ├── silver_layer.py          # Clean and standardize
│   ├── run_local_pipeline.py    # Run complete pipeline
│   ├── download_from_gcp.py     # Download from GCP
│   ├── upload_to_gcp.py         # Upload to GCP
│   └── utils.py                 # Utility functions
├── notebooks/
│   └── 01_data_exploration.ipynb
├── logs/              # Processing logs and reports
└── requirements.txt   # Python dependencies
```

## Data Pipeline Layers

### Bronze Layer
- **Purpose**: Preserve original data for audit and recovery
- **Action**: Copy raw CSV files without modifications
- **Output**: `data/bronze/*.csv`

### Silver Layer
- **Purpose**: Clean, validate, and standardize data
- **Actions**:
  - Remove duplicates
  - Handle missing values
  - Validate and standardize formats
  - Remove outliers
  - Create derived columns
- **Output**: `data/silver/*.parquet` (compressed, efficient format)

### Gold Layer (Future)
- **Purpose**: Analytics-ready aggregated data
- **Actions**: Feature engineering, aggregations, business logic

## Working with GCP Cloud Storage

All datasets are stored in GCP Cloud Storage (`gs://bdt_data_raw/`). 

### Download Data from GCP

```bash
export GOOGLE_CLOUD_PROJECT=imanager
python scripts/download_from_gcp.py
```

### Upload Cleaned Data to GCP

```bash
export GOOGLE_CLOUD_PROJECT=imanager
python scripts/upload_to_gcp.py
```

### Using GCP Services

Once in GCP Cloud Storage, your data works with:
- Cloud Dataproc (Spark)
- BigQuery
- Cloud Dataflow
- Vertex AI

## Dataset Information

### Flight Data
- **Size**: ~582,425 rows × 120 columns
- **Content**: US domestic flight records (2018-2024)
- **Key Fields**: Flight dates, airlines, routes, delays, cancellations

### POI Data
- **Size**: ~1.6M rows × 160 columns
- **Content**: OpenStreetMap points of interest
- **Key Fields**: Coordinates, amenities, addresses, business info

### Attractions Data
- **Size**: ~3,124 rows × 15 columns
- **Content**: US tourist attractions and points of interest
- **Key Fields**: Names, categories, ratings, reviews, locations

## Key Features

1. **Chunked Processing**: Handles large files without memory issues
2. **Parquet Format**: 50-80% smaller than CSV, faster reads
3. **Comprehensive Logging**: Track all transformations
4. **Modular Design**: Easy to modify individual cleaning steps
5. **GCP-Ready**: Structure matches cloud data lake architecture
6. **Reproducible**: Clear pipeline steps you can run repeatedly

## License

MIT License
