# 💰 Personal Finance Expense Classifier

An intelligent web application built with Python and Streamlit that automatically categorizes financial transactions, visualizes spending patterns, and provides actionable insights into your personal finances.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🌐 Live Demo

**Try it now! No installation required:**

👉 **[Launch App](https://personal-finance-classifier-vnjiqyfkvqxafaerpdfkgj.streamlit.app/)**

Simply upload your bank CSV and get instant financial insights!

---

## 🎯 Project Overview

This application helps users understand their spending habits by:
- Automatically categorizing transactions from bank statements, credit cards, or digital wallets (Venmo, Apple Card, etc.)
- Generating interactive visualizations to identify spending patterns
- Providing key financial metrics and insights
- Exporting cleaned and classified data for further analysis

Perfect for anyone looking to gain control over their personal finances with data-driven insights.

---

## ✨ Features

### 📊 Data Processing
- **CSV Upload**: Support for standard financial transaction formats
- **Data Cleaning**: Automatic normalization and validation of uploaded data
- **Smart Parsing**: Handles various date formats and transaction descriptions

### 🤖 Intelligent Categorization
- **Rule-Based Classifier**: Uses keyword matching to categorize transactions
- **12 Categories**: Food & Dining, Groceries, Transportation, Entertainment, Shopping, Bills & Utilities, Health, Income, Gambling/Sports Betting, Subscriptions, Transfers, and Other
- **Smart Classification**: Recognizes hundreds of merchants and keywords for accurate categorization
- **Extensible Design**: Framework ready for ML-based classification

### 📈 Interactive Visualizations
- **Pie Chart**: Percentage breakdown of spending by category
- **Bar Chart**: Total spending comparison across categories
- **Cumulative Line Chart**: Track your total spending growth over time
- **Heatmap**: Discover spending patterns by day of week and category (e.g., "I always eat out on Fridays")

### 💡 Financial Insights
- **Key Metrics**: Total spending, income, and net cash flow
- **Top Merchants**: Identify where you spend the most
- **Category Analysis**: Detailed breakdown with transaction counts and averages
- **Period Summary**: Analysis date range and duration

### 📥 Export Functionality
- **Customizable Downloads**: Select specific columns to include
- **CSV Format**: Compatible with Excel, Google Sheets, and other tools
- **Preview Before Download**: Verify data before exporting

---

## 🛠️ Technology Stack

- **Frontend Framework**: Streamlit 1.31.0
- **Data Processing**: Pandas 2.2.0, NumPy 1.26.3
- **Interactive Visualizations**: Plotly 5.18.0 (all charts are interactive with hover, zoom, and pan)
- **Machine Learning**: Scikit-learn 1.4.0 (for future enhancements)
- **Language**: Python 3.8+

---

## 💻 For Developers - Local Installation

Want to run the app locally, contribute code, or customize it? Follow these instructions:

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository** (or download the project files)
```bash
cd "Personal Finance Expense Classifier"
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### Running the Application

Start the Streamlit server:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Preparing Your Data

Your CSV file should contain these three columns:
- `date`: Transaction date (various formats supported)
- `description`: Transaction description or merchant name
- `amount`: Transaction amount (negative for expenses, positive for income)

**Example CSV format:**
```csv
date,description,amount
2024-01-15,Starbucks Coffee,-5.75
2024-01-16,Whole Foods Market,-87.32
2024-01-17,Shell Gas Station,-45.00
2024-01-18,Salary Deposit,3000.00
```

### Step-by-Step Guide

1. **Upload CSV**: Use the sidebar to upload your transaction CSV file
2. **Review Data**: Check the automatically categorized transactions in the Overview tab
3. **Explore Visualizations**: View spending patterns through interactive charts
4. **Analyze Insights**: Review key metrics and top spending categories
5. **Download Results**: Export the classified data with custom column selection

---

## 📁 Project Structure

```
Personal Finance Expense Classifier/
│
├── app.py                  # Main Streamlit application
├── classifier.py           # Transaction categorization logic
├── utils.py               # Data cleaning and helper functions
├── requirements.txt       # Project dependencies
└── README.md             # Project documentation
```

### Module Descriptions

#### `app.py`
- Main Streamlit interface and UI components
- Chart rendering and visualization logic
- User interaction handling
- Download functionality

#### `classifier.py`
- `RuleBasedClassifier`: Keyword-based categorization engine
- `MLClassifier`: Placeholder for machine learning implementation
- Category definitions and keyword mappings
- Batch processing capabilities

#### `utils.py`
- CSV validation and cleaning functions
- Data normalization and type conversion
- Date parsing and formatting
- Merchant name extraction

---

## 🎨 Features Breakdown

### Categorization Logic

The rule-based classifier uses an extensive keyword dictionary to match transaction descriptions with categories:

- **Food & Dining**: Restaurants, cafes, delivery services (50+ keywords)
- **Groceries**: Supermarkets, farmers markets (20+ keywords)
- **Transportation**: Gas stations, rideshares, parking (25+ keywords)
- **Entertainment**: Streaming services, gaming, events (30+ keywords)
- **Shopping**: Retail stores, online marketplaces (40+ keywords)
- **Bills & Utilities**: Internet, phone, electricity, insurance (25+ keywords)
- **Health**: Pharmacies, medical services (20+ keywords)
- **Income**: Salary, deposits, refunds
- **Other**: Uncategorized transactions

### Data Processing Pipeline

1. **Upload** → CSV file validation
2. **Clean** → Normalize columns, handle missing data
3. **Enhance** → Add derived columns (transaction type, merchant, month)
4. **Classify** → Apply categorization algorithm
5. **Visualize** → Generate interactive charts
6. **Analyze** → Calculate insights and metrics
7. **Export** → Download processed data

---

## 🔮 Future Enhancements

- [ ] Machine Learning classifier with training interface
- [ ] Budget tracking and alerts
- [ ] Multi-currency support
- [ ] Recurring transaction detection
- [ ] Anomaly detection for unusual spending
- [ ] Historical comparison (month-over-month, year-over-year)
- [ ] Custom category creation
- [ ] Mobile-responsive design improvements
- [ ] Database integration for long-term storage
- [ ] User authentication and profiles

---

## 🤝 Contributing

Contributions are welcome! Here are some ways you can contribute:
- Report bugs and issues
- Suggest new features or improvements
- Improve documentation
- Submit pull requests

---

## 📝 License

This project is licensed under the MIT License - feel free to use it for personal or commercial projects.

---

## 👤 Author

**Ashwin Loganathan**

This project demonstrates proficiency in:
- Python development and data processing
- Web application development with Streamlit
- Data visualization and analytics
- Clean code architecture and modular design
- Machine learning frameworks and algorithms

---

## 📧 Contact & Feedback

For questions, suggestions, or feedback, please open an issue or reach out directly.

---

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) - an amazing framework for data apps
- Visualizations powered by [Plotly](https://plotly.com/)
- Data processing with [Pandas](https://pandas.pydata.org/)

---

## 📸 Screenshots

### Dashboard Overview
The main dashboard provides an intuitive interface for uploading and analyzing transactions.

### Spending Visualizations
Interactive charts help identify spending patterns and trends over time.

### Financial Insights
Key metrics and top merchant analysis provide actionable insights.

### Download Options
Customizable export options for further analysis in Excel or other tools.

---

**Made with ❤️ and Python**

