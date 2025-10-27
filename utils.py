"""
Utility functions for cleaning and normalizing financial transaction data.
"""

import pandas as pd
from datetime import datetime
import io


def clean_csv_data(df):
    """
    Clean and normalize the uploaded CSV data.
    
    Args:
        df (pd.DataFrame): Raw DataFrame with columns: date, description, amount
        
    Returns:
        tuple: (cleaned_df, removed_rows_info)
            - cleaned_df: Cleaned DataFrame with standardized columns
            - removed_rows_info: List of dicts with info about removed rows
    """
    removed_rows = []
    # Create a copy to avoid modifying the original
    df_clean = df.copy()
    
    # Standardize column names (case-insensitive)
    df_clean.columns = df_clean.columns.str.lower().str.strip()
    
    # Check for required columns
    required_cols = ['date', 'description', 'amount']
    missing_cols = [col for col in required_cols if col not in df_clean.columns]
    
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Keep only the required columns (drop extra columns like running balance, etc.)
    # First check for duplicate columns
    if df_clean.columns.duplicated().any():
        # Keep only first occurrence of each column
        df_clean = df_clean.loc[:, ~df_clean.columns.duplicated()]
    
    df_clean = df_clean[required_cols].copy()
    
    # Clean description column
    df_clean.loc[:, 'description'] = df_clean['description'].astype(str).str.strip()
    df_clean.loc[:, 'description'] = df_clean['description'].replace(['nan', 'None', ''], 'Unknown')
    
    # Clean amount column - handle currency symbols and commas
    # Always convert to string first, clean, then convert to numeric
    amount_series = df_clean['amount'].squeeze()  # Ensure it's a Series
    if isinstance(amount_series, pd.DataFrame):
        amount_series = amount_series.iloc[:, 0]  # Take first column if DataFrame
    
    amount_clean = amount_series.astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False).str.strip()
    df_clean.loc[:, 'amount'] = amount_clean
    
    # Convert to numeric
    df_clean.loc[:, 'amount'] = pd.to_numeric(df_clean['amount'], errors='coerce')
    
    # Track rows with invalid amounts
    invalid_amounts = df_clean[df_clean['amount'].isna()]
    for idx, row in invalid_amounts.iterrows():
        removed_rows.append({
            'index': idx,
            'date': row['date'],
            'description': row['description'],
            'amount': 'Invalid',
            'reason': 'Invalid amount (could not convert to number)'
        })
    
    # Remove rows with invalid amounts
    df_clean = df_clean.dropna(subset=['amount'])
    
    # Clean and parse date column
    df_clean['date'] = pd.to_datetime(df_clean['date'], errors='coerce')
    
    # Track rows with invalid dates
    invalid_dates = df_clean[df_clean['date'].isna()]
    for idx, row in invalid_dates.iterrows():
        removed_rows.append({
            'index': idx,
            'date': 'Invalid',
            'description': row['description'],
            'amount': row['amount'],
            'reason': 'Invalid date (could not parse)'
        })
    
    # Remove rows with invalid dates
    df_clean = df_clean.dropna(subset=['date'])
    
    # Sort by date
    df_clean = df_clean.sort_values('date').reset_index(drop=True)
    
    return df_clean, removed_rows


def categorize_transaction_type(amount):
    """
    Categorize transaction as income or expense based on amount.
    
    Args:
        amount (float): Transaction amount
        
    Returns:
        str: 'Income' or 'Expense'
    """
    return 'Income' if amount > 0 else 'Expense'


def get_absolute_amount(amount):
    """
    Get the absolute value of the transaction amount.
    
    Args:
        amount (float): Transaction amount
        
    Returns:
        float: Absolute value of amount
    """
    return abs(amount)


def add_derived_columns(df):
    """
    Add derived columns for better analysis.
    
    Args:
        df (pd.DataFrame): Cleaned DataFrame
        
    Returns:
        pd.DataFrame: DataFrame with additional columns
    """
    df_enhanced = df.copy()
    
    # Add transaction type
    df_enhanced['transaction_type'] = df_enhanced['amount'].apply(categorize_transaction_type)
    
    # Add absolute amount for easier analysis
    df_enhanced['abs_amount'] = df_enhanced['amount'].apply(get_absolute_amount)
    
    # Add month and year for time-based analysis
    df_enhanced['month'] = df_enhanced['date'].dt.to_period('M')
    df_enhanced['year'] = df_enhanced['date'].dt.year
    df_enhanced['month_year'] = df_enhanced['date'].dt.strftime('%Y-%m')
    
    return df_enhanced


def extract_merchant_name(description):
    """
    Extract merchant name from transaction description.
    Simplified extraction - takes first significant word/phrase.
    
    Args:
        description (str): Transaction description
        
    Returns:
        str: Extracted merchant name
    """
    # Remove common prefixes and clean up
    description = str(description).upper().strip()
    
    # Remove common payment indicators
    prefixes_to_remove = [
        'DEBIT CARD PURCHASE - ',
        'PURCHASE AUTHORIZED ON ',
        'CARD PURCHASE - ',
        'PAYMENT TO ',
        'TRANSFER TO ',
        'TRANSFER FROM ',
    ]
    
    for prefix in prefixes_to_remove:
        if description.startswith(prefix):
            description = description[len(prefix):]
    
    # Take first 30 characters or up to first special pattern
    description = description[:50].strip()
    
    return description if description else 'Unknown'


def smart_read_csv(uploaded_file, skip_rows=0):
    """
    Intelligently read CSV files from banks that may have messy formats.
    
    Args:
        uploaded_file: Uploaded file object
        skip_rows (int): Number of rows to skip from the top
        
    Returns:
        pd.DataFrame: Parsed DataFrame or None if parsing fails
    """
    try:
        # Reset file pointer
        uploaded_file.seek(0)
        
        # Try reading with different parameters
        try:
            # Standard read
            df = pd.read_csv(uploaded_file, skiprows=skip_rows)
        except:
            # Try with different error handling
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, skiprows=skip_rows, on_bad_lines='skip')
        
        return df
    except Exception as e:
        return None


def detect_header_row(uploaded_file):
    """
    Detect which row contains the actual headers (date, description, amount).
    
    Args:
        uploaded_file: Uploaded file object
        
    Returns:
        int: Row number to skip (0-indexed) or 0 if headers are in first row
    """
    uploaded_file.seek(0)
    
    # Read first 20 rows as raw text to analyze
    try:
        import csv
        uploaded_file.seek(0)
        reader = csv.reader(uploaded_file.read().decode('utf-8').splitlines())
        rows = []
        for i, row in enumerate(reader):
            if i >= 20:
                break
            rows.append(row)
    except:
        uploaded_file.seek(0)
        return 0
    
    uploaded_file.seek(0)
    
    # Look for rows containing all three required keywords
    required_keywords = ['date', 'description', 'amount']
    
    for idx, row in enumerate(rows):
        # Convert all cells to lowercase for matching
        row_lower = [str(cell).lower().strip() for cell in row]
        
        # Check if this row contains all three keywords (case-insensitive)
        matches = 0
        for keyword in required_keywords:
            # Check if keyword appears in any cell
            if any(keyword in cell for cell in row_lower):
                matches += 1
        
        # If we found all 3 keywords in this row, it's our header
        if matches == 3:
            return idx
    
    return 0


def normalize_column_names(df):
    """
    Normalize column names to standard format: date, description, amount.
    Handles various naming conventions from different banks.
    
    Args:
        df (pd.DataFrame): Raw DataFrame with any column names
        
    Returns:
        pd.DataFrame: DataFrame with normalized column names
    """
    df_normalized = df.copy()
    
    # Define common column name variations
    date_variations = [
        'date', 'posted date', 'transaction date', 'post date', 'trans date',
        'posting date', 'trans_date', 'posted_date', 'transaction_date'
    ]
    
    description_variations = [
        'description', 'desc', 'merchant', 'transaction description',
        'trans description', 'details', 'memo', 'payee', 'name',
        'transaction_description', 'trans_description'
    ]
    
    amount_variations = [
        'amount', 'amt', 'transaction amount', 'trans amount', 'value',
        'debit', 'credit', 'transaction_amount', 'trans_amount'
    ]
    
    # Create mapping dictionary
    column_mapping = {}
    
    for col in df_normalized.columns:
        col_lower = col.lower().strip()
        
        # Check for date column
        if col_lower in date_variations or 'date' in col_lower:
            if 'date' not in column_mapping:  # Take first match
                column_mapping[col] = 'date'
        
        # Check for description column
        elif col_lower in description_variations or 'description' in col_lower or 'merchant' in col_lower:
            if 'description' not in column_mapping:
                column_mapping[col] = 'description'
        
        # Check for amount column
        elif col_lower in amount_variations or 'amount' in col_lower:
            if 'amount' not in column_mapping:
                column_mapping[col] = 'amount'
    
    # Rename columns
    if column_mapping:
        df_normalized = df_normalized.rename(columns=column_mapping)
    
    return df_normalized


def validate_csv_structure(df):
    """
    Validate that the uploaded CSV has the correct structure.
    
    Args:
        df (pd.DataFrame): Raw uploaded DataFrame
        
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if df is None or df.empty:
        return False, "CSV file is empty"
    
    # Check for required columns (case-insensitive)
    columns_lower = [col.lower().strip() for col in df.columns]
    required = ['date', 'description', 'amount']
    
    missing = [col for col in required if col not in columns_lower]
    
    if missing:
        return False, f"Missing required columns: {', '.join(missing)}. Expected columns: date, description, amount"
    
    return True, None

