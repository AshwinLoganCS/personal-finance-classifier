# Personal Finance Expense Classifier

A simple web app that categorizes your bank transactions and shows you where your money is going. Built with Python and Streamlit.

Live demo: https://personal-finance-classifier-vnjiqyfkvqxafaerpdfkgj.streamlit.app/

## What it does

Upload a CSV of your bank transactions and the app will:
- Automatically categorize each transaction (food, groceries, entertainment, etc.)
- Show you charts of your spending patterns
- Calculate total spending, income, and net cashflow
- Let you download the categorized data

I made this because I wanted an easy way to see where I was spending money without manually going through hundreds of transactions or paying for budgeting software.

## Features

- Supports 12 categories: Food & Dining, Groceries, Transportation, Entertainment, Shopping, Bills & Utilities, Health, Income, Gambling/Sports Betting, Subscriptions, Transfers, and Other
- Works with most bank statement formats (as long as you have date, description, and amount columns)
- Interactive charts - pie chart, bar chart, spending over time, and a heatmap showing spending by day of week
- Shows top merchants and spending averages
- Export your categorized data as CSV

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

The categorization uses keyword matching. I've built up a dictionary of keywords for each category - like "starbucks", "chipotle", "ubereats" for Food & Dining, or "shell", "chevron", "uber" for Transportation. When processing transactions, it looks for these keywords in the description.

It's not perfect but works pretty well for my needs. You can easily add more keywords in `classifier.py` if needed.

## Project structure

- `app.py` - main Streamlit app with all the UI and charts
- `classifier.py` - categorization logic
- `utils.py` - data cleaning functions
- `requirements.txt` - dependencies

## Tech stack

- Streamlit for the web interface
- Pandas for data processing
- Plotly for interactive charts
- Python 3.8+

## Future improvements

Some things I might add later:
- Budget tracking
- Month over month comparisons
- Better handling of recurring transactions
- Custom categories
- Multi-currency support

## License

MIT License - use it however you want
