# Personal Finance Expense Classifier

A web application that automatically categorizes bank transactions and visualizes spending patterns. Built with Python and Streamlit.

Live demo: https://personal-finance-classifier-vnjiqyfkvqxafaerpdfkgj.streamlit.app/

## Overview

This tool processes CSV exports from bank statements and credit cards, automatically categorizing transactions and generating insights about spending behavior. It's designed to give you a clear picture of where your money goes without manual data entry or subscription fees.

## Features

- Automatic categorization across 12 categories: Food & Dining, Groceries, Transportation, Entertainment, Shopping, Bills & Utilities, Health, Income, Gambling/Sports Betting, Subscriptions, Transfers, and Other
- Support for standard bank statement CSV formats (requires date, description, and amount columns)
- Interactive visualizations: pie charts, bar charts, spending timelines, and day-of-week heatmaps
- Financial metrics including total spending, income, net cashflow, and top merchants
- CSV export of categorized data for further analysis

## Running locally

1. Clone this repo
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

## CSV format

Your file needs three columns:
- `date` - transaction date
- `description` - what the transaction was
- `amount` - negative for expenses, positive for income

Example:
```csv
date,description,amount
2024-01-15,Starbucks Coffee,-5.75
2024-01-16,Whole Foods Market,-87.32
2024-01-18,Salary Deposit,3000.00
```

## How it works

The categorization engine uses keyword matching against a curated dictionary of merchant names and transaction descriptors. Each category contains dozens of keywords that are matched against transaction descriptions. For example, Food & Dining includes keywords like "starbucks", "chipotle", and "ubereats", while Transportation covers "shell", "chevron", and ride-sharing services.

The keyword dictionary can be extended in `classifier.py` to improve accuracy for specific use cases.

## Project structure

- `app.py` - main Streamlit app with UI and visualization logic
- `classifier.py` - transaction categorization engine
- `utils.py` - data cleaning and processing utilities
- `requirements.txt` - project dependencies

## Tech stack

- Streamlit for the web interface
- Pandas for data processing
- Plotly for interactive charts
- Python 3.8+

## Future improvements

Potential enhancements:
- Budget tracking and threshold alerts
- Month-over-month comparison analysis
- Recurring transaction detection
- User-defined custom categories
- Multi-currency support

## License

MIT License - use it however you want
