"""
Silver Layer: Data Cleaning and Standardization
Purpose: Clean, validate, and standardize data
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class SilverLayer:
    def __init__(self, bronze_dir='data/bronze', silver_dir='data/silver'):
        self.bronze_dir = Path(bronze_dir)
        self.silver_dir = Path(silver_dir)
        self.silver_dir.mkdir(parents=True, exist_ok=True)
        
        self.log_dir = Path('logs')
        self.log_dir.mkdir(exist_ok=True)
        
        # Initialize cleaning stats
        self.stats = {}
        
    def clean_flight_data(self, chunk_size=100000):
        """Clean flight data with chunked processing for large files"""
        print("\n" + "="*60)
        print("CLEANING: Flight Data")
        print("="*60)
        
        input_file = self.bronze_dir / 'flight_data_2018_2024.csv'
        output_file = self.silver_dir / 'flight_data_cleaned.parquet'
        
        stats = {
            'original_rows': 0,
            'rows_after_cleaning': 0,
            'duplicates_removed': 0,
            'nulls_handled': 0,
            'outliers_removed': 0
        }
        
        # Process in chunks
        chunks = []
        for chunk in pd.read_csv(input_file, chunksize=chunk_size):
            stats['original_rows'] += len(chunk)
            cleaned_chunk = self._clean_flight_chunk(chunk, stats)
            chunks.append(cleaned_chunk)
        
        # Combine chunks
        df_clean = pd.concat(chunks, ignore_index=True)
        stats['rows_after_cleaning'] = len(df_clean)
        
        # Save as parquet (more efficient than CSV)
        df_clean.to_parquet(output_file, index=False, compression='snappy')
        
        print(f"\n✓ Cleaned flight data saved: {output_file}")
        print(f"  Original rows: {stats['original_rows']:,}")
        print(f"  Final rows: {stats['rows_after_cleaning']:,}")
        print(f"  Rows removed: {stats['original_rows'] - stats['rows_after_cleaning']:,}")
        
        self.stats['flight'] = stats
        return df_clean
    
    def _clean_flight_chunk(self, df, stats):
        """Clean individual flight data chunk"""
        
        # 1. Handle duplicates
        before = len(df)
        df = df.drop_duplicates()
        stats['duplicates_removed'] += (before - len(df))
        
        # 2. Standardize date columns
        date_columns = ['FlightDate']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # 3. Standardize airport codes (uppercase, trim)
        airport_cols = ['Origin', 'Dest', 'OriginCityName', 'DestCityName']
        for col in airport_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().str.upper()
        
        # 4. Handle numeric columns
        numeric_cols = ['DepDelay', 'ArrDelay', 'Distance', 'AirTime']
        for col in numeric_cols:
            if col in df.columns:
                # Convert to numeric
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # Cap extreme outliers (beyond 3 std devs)
                if col in ['DepDelay', 'ArrDelay']:
                    mean = df[col].mean()
                    std = df[col].std()
                    if not pd.isna(std) and std > 0:
                        df[col] = df[col].clip(lower=mean - 3*std, upper=mean + 3*std)
        
        # 5. Handle categorical columns
        if 'Cancelled' in df.columns:
            df['Cancelled'] = df['Cancelled'].fillna(0).astype(int)
        
        if 'Diverted' in df.columns:
            df['Diverted'] = df['Diverted'].fillna(0).astype(int)
        
        # 6. Create derived columns
        if 'DepDelay' in df.columns:
            df['IsDelayed'] = (df['DepDelay'] > 15).astype(int)
        
        if 'Origin' in df.columns and 'Dest' in df.columns:
            df['Route'] = df['Origin'] + '-' + df['Dest']
        
        # 7. Remove rows with critical missing values
        critical_cols = ['FlightDate', 'Origin', 'Dest']
        before = len(df)
        df = df.dropna(subset=[col for col in critical_cols if col in df.columns])
        stats['nulls_handled'] += (before - len(df))
        
        return df
    
    def clean_poi_data(self, chunk_size=50000):
        """Clean POI data"""
        print("\n" + "="*60)
        print("CLEANING: POI Data")
        print("="*60)
        
        input_file = self.bronze_dir / 'poi_data_osm.csv'
        output_file = self.silver_dir / 'poi_data_cleaned.parquet'
        
        stats = {
            'original_rows': 0,
            'rows_after_cleaning': 0,
            'duplicates_removed': 0,
            'invalid_coords_removed': 0
        }
        
        # Process in chunks
        chunks = []
        for chunk in pd.read_csv(input_file, chunksize=chunk_size, low_memory=False):
            stats['original_rows'] += len(chunk)
            cleaned_chunk = self._clean_poi_chunk(chunk, stats)
            if len(cleaned_chunk) > 0:
                chunks.append(cleaned_chunk)
        
        # Combine chunks
        df_clean = pd.concat(chunks, ignore_index=True)
        stats['rows_after_cleaning'] = len(df_clean)
        
        # Save as parquet
        df_clean.to_parquet(output_file, index=False, compression='snappy')
        
        print(f"\n✓ Cleaned POI data saved: {output_file}")
        print(f"  Original rows: {stats['original_rows']:,}")
        print(f"  Final rows: {stats['rows_after_cleaning']:,}")
        print(f"  Rows removed: {stats['original_rows'] - stats['rows_after_cleaning']:,}")
        
        self.stats['poi'] = stats
        return df_clean
    
    def _clean_poi_chunk(self, df, stats):
        """Clean individual POI data chunk"""
        
        # 1. Handle duplicates
        before = len(df)
        df = df.drop_duplicates()
        stats['duplicates_removed'] += (before - len(df))
        
        # 2. Standardize coordinate columns
        coord_cols = {
            'latitude': 'latitude',
            'longitude': 'longitude',
            'lat': 'latitude',
            'lon': 'longitude'
        }
        
        # Rename coordinate columns if needed
        for old_col, new_col in coord_cols.items():
            if old_col in df.columns and new_col not in df.columns:
                df = df.rename(columns={old_col: new_col})
        
        # 3. Validate coordinates
        if 'latitude' in df.columns and 'longitude' in df.columns:
            before = len(df)
            
            # Convert to numeric
            df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
            df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
            
            # Remove invalid coordinates
            df = df[
                (df['latitude'].notna()) & 
                (df['longitude'].notna()) &
                (df['latitude'] >= -90) & 
                (df['latitude'] <= 90) &
                (df['longitude'] >= -180) & 
                (df['longitude'] <= 180)
            ]
            
            # Round to 6 decimal places (~11cm precision)
            df['latitude'] = df['latitude'].round(6)
            df['longitude'] = df['longitude'].round(6)
            
            stats['invalid_coords_removed'] += (before - len(df))
        
        # 4. Standardize address columns
        address_cols = ['addr:city', 'addr:state', 'addr:street', 'addr:postcode']
        for col in address_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().str.title()
        
        # 5. Standardize state codes (if present)
        if 'addr:state' in df.columns:
            df['addr:state'] = df['addr:state'].str.upper()
        
        # 6. Clean name column
        if 'name' in df.columns:
            df['name'] = df['name'].astype(str).str.strip()
            df['name'] = df['name'].replace(['nan', 'None', ''], np.nan)
        
        # 7. Standardize categorical columns
        category_cols = ['amenity', 'tourism', 'shop', 'cuisine']
        for col in category_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().str.lower()
                df[col] = df[col].replace(['nan', 'none', ''], np.nan)
        
        # 8. Keep only essential columns to reduce size
        essential_cols = [
            'latitude', 'longitude', 'name', 
            'amenity', 'tourism', 'shop', 'cuisine',
            'addr:city', 'addr:state', 'addr:street', 'addr:postcode',
            'phone', 'website', 'opening_hours'
        ]
        
        available_cols = [col for col in essential_cols if col in df.columns]
        df = df[available_cols]
        
        return df
    
    def clean_attractions_data(self):
        """Clean attractions data"""
        print("\n" + "="*60)
        print("CLEANING: Attractions Data")
        print("="*60)
        
        input_file = self.bronze_dir / 'attractions_data_USA.csv'
        output_file = self.silver_dir / 'attractions_data_cleaned.parquet'
        
        df = pd.read_csv(input_file)
        
        stats = {
            'original_rows': len(df),
            'duplicates_removed': 0,
            'rows_after_cleaning': 0
        }
        
        # 1. Handle duplicates
        before = len(df)
        df = df.drop_duplicates()
        stats['duplicates_removed'] = before - len(df)
        
        # 2. Standardize text columns
        text_cols = ['name', 'city', 'state', 'address']
        for col in text_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        
        # 3. Standardize state codes
        if 'state' in df.columns:
            df['state'] = df['state'].str.upper()
        
        # 4. Clean numeric columns
        if 'rating' in df.columns:
            df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
            df['rating'] = df['rating'].clip(lower=0, upper=5)
        
        if 'reviews' in df.columns:
            df['reviews'] = pd.to_numeric(df['reviews'], errors='coerce')
            df['reviews'] = df['reviews'].fillna(0).astype(int)
        
        # 5. Standardize categories
        if 'main_category' in df.columns:
            df['main_category'] = df['main_category'].str.strip().str.title()
        
        # 6. Clean zipcode
        if 'zipcode' in df.columns:
            df['zipcode'] = df['zipcode'].astype(str).str.extract(r'(\d{5})')[0]
        
        # 7. Create category flags
        if 'categories' in df.columns:
            df['is_museum'] = df['categories'].str.contains('Museum', case=False, na=False).astype(int)
            df['is_park'] = df['categories'].str.contains('Park', case=False, na=False).astype(int)
            df['is_historical'] = df['categories'].str.contains('Historical', case=False, na=False).astype(int)
        
        stats['rows_after_cleaning'] = len(df)
        
        # Save as parquet
        df.to_parquet(output_file, index=False, compression='snappy')
        
        print(f"\n✓ Cleaned attractions data saved: {output_file}")
        print(f"  Original rows: {stats['original_rows']:,}")
        print(f"  Final rows: {stats['rows_after_cleaning']:,}")
        print(f"  Duplicates removed: {stats['duplicates_removed']:,}")
        
        self.stats['attractions'] = stats
        return df
    
    def generate_cleaning_report(self):
        """Generate comprehensive cleaning report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.log_dir / f'silver_layer_report_{timestamp}.txt'
        
        with open(report_file, 'w') as f:
            f.write("="*60 + "\n")
            f.write("SILVER LAYER CLEANING REPORT\n")
            f.write("="*60 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for dataset, stats in self.stats.items():
                f.write(f"\n{dataset.upper()} DATA:\n")
                f.write("-" * 60 + "\n")
                for key, value in stats.items():
                    f.write(f"  {key}: {value:,}\n")
        
        print(f"\n✓ Cleaning report saved: {report_file}")
    
    def run_all(self):
        """Run all cleaning tasks"""
        print("\n" + "="*60)
        print("STARTING SILVER LAYER PROCESSING")
        print("="*60)
        
        # Clean each dataset
        self.clean_flight_data()
        self.clean_poi_data()
        self.clean_attractions_data()
        
        # Generate report
        self.generate_cleaning_report()
        
        print("\n" + "="*60)
        print("✓ SILVER LAYER PROCESSING COMPLETE")
        print("="*60)


if __name__ == "__main__":
    silver = SilverLayer()
    silver.run_all()

