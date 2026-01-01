"""
Utility functions for the Autonomous Month-End Close Process
Provides helper functions for CSV reading, date parsing, and formatting
"""

import csv
from datetime import datetime
from typing import List, Dict, Any


def read_csv_file(filepath: str) -> List[Dict[str, Any]]:
    """
    Read a CSV file and return a list of dictionaries.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        List of dictionaries where keys are column headers
    """
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    
    return data


def write_csv_file(filepath: str, data: List[Dict[str, Any]], fieldnames: List[str]):
    """
    Write data to a CSV file.
    
    Args:
        filepath: Path to the output CSV file
        data: List of dictionaries to write
        fieldnames: List of column headers
    """
    try:
        with open(filepath, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Data successfully written to {filepath}")
    except Exception as e:
        print(f"Error writing CSV file: {e}")


def parse_date(date_str: str, format: str = '%Y-%m-%d') -> datetime:
    """
    Parse a date string into a datetime object.
    
    Args:
        date_str: Date string to parse
        format: Expected date format (default: '%Y-%m-%d')
        
    Returns:
        datetime object
    """
    try:
        return datetime.strptime(date_str, format)
    except ValueError:
        # Try alternative formats
        for fmt in ['%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d']:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"Unable to parse date: {date_str}")


def format_currency(amount: float) -> str:
    """
    Format a number as currency (GBP).
    
    Args:
        amount: Numerical amount
        
    Returns:
        Formatted currency string
    """
    return f"£{amount:,.2f}"


def safe_float(value: Any, default: float = 0.0) -> float:
    """
    Safely convert a value to float.
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        Float value or default
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def safe_int(value: Any, default: int = 0) -> int:
    """
    Safely convert a value to int.
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        Int value or default
    """
    try:
        if isinstance(value, str) and not value.strip():
            return default
        return int(value)
    except (ValueError, TypeError):
        return default
