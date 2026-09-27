"""
Utility functions for data processing pipeline
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional


def validate_coordinates(lat: pd.Series, lon: pd.Series) -> pd.Series:
    """
    Validate latitude and longitude coordinates
    
    Args:
        lat: Latitude series
        lon: Longitude series
        
    Returns:
        Boolean series indicating valid coordinates
    """
    return (
        (lat.notna()) & 
        (lon.notna()) &
        (lat >= -90) & 
        (lat <= 90) &
        (lon >= -180) & 
        (lon <= 180)
    )


def standardize_state_code(state: pd.Series) -> pd.Series:
    """
    Standardize US state codes to uppercase
    
    Args:
        state: State code series
        
    Returns:
        Standardized state codes
    """
    return state.astype(str).str.strip().str.upper()


def clean_numeric_column(col: pd.Series, min_val: Optional[float] = None, 
                        max_val: Optional[float] = None) -> pd.Series:
    """
    Clean numeric column by converting to numeric and clipping outliers
    
    Args:
        col: Column to clean
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        
    Returns:
        Cleaned numeric series
    """
    col = pd.to_numeric(col, errors='coerce')
    
    if min_val is not None:
        col = col.clip(lower=min_val)
    if max_val is not None:
        col = col.clip(upper=max_val)
    
    return col


def get_memory_usage(df: pd.DataFrame) -> Dict[str, float]:
    """
    Get memory usage statistics for DataFrame
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        Dictionary with memory usage statistics
    """
    memory_mb = df.memory_usage(deep=True).sum() / (1024 ** 2)
    memory_per_row = memory_mb / len(df) if len(df) > 0 else 0
    
    return {
        'total_mb': memory_mb,
        'mb_per_row': memory_per_row,
        'total_rows': len(df)
    }


def calculate_missing_percentage(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate missing value percentage for each column
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        DataFrame with column names and missing percentages
    """
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    
    return pd.DataFrame({
        'column': missing.index,
        'missing_count': missing.values,
        'missing_percentage': missing_pct.values
    }).sort_values('missing_percentage', ascending=False)


def create_route_column(df: pd.DataFrame, origin_col: str = 'Origin', 
                        dest_col: str = 'Dest') -> pd.Series:
    """
    Create route column from origin and destination
    
    Args:
        df: DataFrame with origin and destination columns
        origin_col: Name of origin column
        dest_col: Name of destination column
        
    Returns:
        Series with route strings
    """
    return df[origin_col].astype(str) + '-' + df[dest_col].astype(str)

