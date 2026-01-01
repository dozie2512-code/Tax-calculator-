"""Utility functions for validation and helpers."""
import re
from datetime import datetime
from fastapi import HTTPException


def validate_period_format(period: str) -> tuple[int, int]:
    """
    Validate period format and return year and month.
    
    Args:
        period: Period string in YYYY-MM format
        
    Returns:
        Tuple of (year, month)
        
    Raises:
        HTTPException: If period format is invalid
    """
    if not period or not isinstance(period, str):
        raise HTTPException(status_code=400, detail="Period must be a non-empty string")
    
    # Validate format using regex
    pattern = r'^\d{4}-(0[1-9]|1[0-2])$'
    if not re.match(pattern, period):
        raise HTTPException(
            status_code=400, 
            detail="Period must be in YYYY-MM format (e.g., '2026-01')"
        )
    
    try:
        year, month = period.split("-")
        year_int = int(year)
        month_int = int(month)
        
        # Additional validation
        if year_int < 1900 or year_int > 2100:
            raise HTTPException(status_code=400, detail="Year must be between 1900 and 2100")
        
        if month_int < 1 or month_int > 12:
            raise HTTPException(status_code=400, detail="Month must be between 01 and 12")
        
        return year_int, month_int
    except (ValueError, AttributeError) as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid period format: {str(e)}"
        )


def get_period_date_range(period: str) -> tuple[datetime, datetime]:
    """
    Get start and end datetime for a period.
    
    Args:
        period: Period string in YYYY-MM format
        
    Returns:
        Tuple of (start_datetime, end_datetime)
    """
    year, month = validate_period_format(period)
    
    start_date = datetime(year, month, 1)
    
    # Calculate end date (start of next month)
    if month < 12:
        end_date = datetime(year, month + 1, 1)
    else:
        end_date = datetime(year + 1, 1, 1)
    
    return start_date, end_date
