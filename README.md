# Financial Reporting Automation Framework

## Overview
The **Financial Reporting Automation Framework** automates the extraction, transformation, and loading (ETL) of financial data, performs financial analysis, and generates customizable financial reports using **Streamlit**.

## Features
- **Automated ETL Pipeline**: Fetches financial data from multiple sources (Yahoo Finance API, Kaggle dataset, MySQL, BigQuery).
- **Financial Data Normalization**: Standardizes financial statements across different reporting standards.
- **KPI Calculations**: Computes financial ratios like **P/E Ratio, ROI, Profit Margin, ROA, and EPS**.
- **Time-Series Analysis**: Generates historical financial insights for better decision-making.
- **Streamlit Dashboard**: Interactive visualization of financial reports with dynamic charts and tables.

## Project Structure
```
financial_reporting_automation/
│-- modules/
│   ├── data_extraction.py
│   ├── data_transformation.py
│   ├── kpi_calculations.py
│   ├── db_connection.py
│   ├── visualization.py
│-- dashboards/
│   ├── main.py (Streamlit Dashboard)
│-- data/
│   ├── raw_data/
│   ├── processed_data/
│-- README.md
```

## Installation
### 1. Clone the repository
```bash
git clone https://github.com/your-repo/financial_reporting_automation.git
cd financial_reporting_automation
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file and add:
```env
DB_HOST=your_database_host
DB_USER=your_database_user
DB_PASSWORD=your_database_password
API_KEY=your_yahoo_finance_api_key
```

## Usage
### 1. Run the ETL Pipeline
```bash
python modules/main.py
```
### 2. Launch the Streamlit Dashboard
```bash
streamlit run dashboards/main.py
```

## Data Sources
- **Yahoo Finance API**: Retrieves financial metrics.
- **Kaggle Dataset**: Provides historical financial data.
- **MySQL/BigQuery**: Stores and queries structured financial data.

## Key Metrics
- **Revenue Trends**
- **Net Income Analysis**
- **Profit Margin Over Time**
- **Return on Assets (ROA)**
- **Earnings Per Share (EPS)**

## Visualizations
- **Line Charts**: Time-series analysis of financial KPIs.
- **Bar Charts**: Comparison of financial metrics across years.
- **Data Tables**: Interactive financial statements.

## Contributions
Feel free to fork the repo, create issues, or submit pull requests!

## License
This project is licensed under the MIT License.
