import yfinance as yf
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

# List of companies
COMPANIES = ["AAPL", "MSFT", "GOOGL"]

# Extract data from yfinance
def extract_financials(ticker):
    stock = yf.Ticker(ticker)

    # Company Data (dim_company)
    info = stock.info
    dim_company = pd.DataFrame([{
        "ticker": ticker,
        "name": info.get("longName", ""),
        "sector": info.get("sector", ""),
        "industry": info.get("industry", ""),
        "market_cap": info.get("marketCap", 0),
        "country": info.get("country", "")
    }])

    # Market Data (dim_market)
    market_data = stock.history(period="1y")[["Close", "Volume"]]
    market_data.reset_index(inplace=True)
    market_data["report_date"] = market_data["Date"].dt.date  # Convert to DATE format
    market_data["ticker"] = ticker
    dim_market = market_data.rename(columns={"Close": "closing_price", "Volume": "volume"}).drop(columns=["Date"])

    # Time Data (dim_time)
    dim_time = pd.DataFrame({"report_date": dim_market["report_date"].unique()})

    # Financial Statements (fact_financials)
    income_stmt = stock.financials.T.fillna(0).reset_index()
    fact_financials = income_stmt.rename(columns={"index": "report_date"})[["report_date"]]
    fact_financials["report_date"] = pd.to_datetime(fact_financials["report_date"]).dt.date  # Convert to DATE
    fact_financials["ticker"] = ticker
    fact_financials["revenue"] = income_stmt.get("Total Revenue", 0)
    fact_financials["net_income"] = income_stmt.get("Net Income", 0)
    fact_financials["eps"] = income_stmt.get("Diluted EPS", 0)

    # Financial Metrics (dim_financial_metrics)
    balance_sheet = stock.balance_sheet.T.fillna(0).reset_index()
    dim_financial_metrics = balance_sheet.rename(columns={"index": "report_date"})[["report_date"]]
    dim_financial_metrics["report_date"] = pd.to_datetime(dim_financial_metrics["report_date"]).dt.date  # Convert to DATE
    dim_financial_metrics["ticker"] = ticker
    dim_financial_metrics["total_assets"] = balance_sheet.get("Total Assets", 0)
    dim_financial_metrics["total_liabilities"] = balance_sheet.get("Total Liabilities", 0)
    dim_financial_metrics["equity"] = balance_sheet.get("Ordinary Shares Number", 0)

    return dim_company, dim_time, dim_market, fact_financials, dim_financial_metrics

# Extract and store data for all companies
dim_company_list, dim_time_list, dim_market_list, fact_financials_list, dim_financial_metrics_list = [], [], [], [], []

for ticker in COMPANIES:
    company, time, market, financials, metrics = extract_financials(ticker)
    dim_company_list.append(company)
    dim_time_list.append(time)
    dim_market_list.append(market)
    fact_financials_list.append(financials)
    dim_financial_metrics_list.append(metrics)

# Concatenate data for all companies
dim_company_df = pd.concat(dim_company_list, ignore_index=True).drop_duplicates()
dim_time_df = pd.concat(dim_time_list, ignore_index=True).drop_duplicates()
dim_market_df = pd.concat(dim_market_list, ignore_index=True)
fact_financials_df = pd.concat(fact_financials_list, ignore_index=True)
dim_financial_metrics_df = pd.concat(dim_financial_metrics_list, ignore_index=True)

# Display sample data
print("dim_company:", dim_company_df.head(), "\n")
print("dim_time:", dim_time_df.head(), "\n")
print("dim_market:", dim_market_df.head(), "\n")
print("fact_financials:", fact_financials_df.head(), "\n")
print("dim_financial_metrics:", dim_financial_metrics_df.head(), "\n")

# Pushing data to MySQL

# MySQL connection details
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "financial_db"
}

# Create a database connection
engine = create_engine(f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}")

# Insert data into MySQL tables
def insert_data():
    with engine.connect() as conn:
        # Insert into dim_company
        dim_company_df.to_sql("dim_company", conn, if_exists="append", index=False)

        # Insert into dim_time (avoid duplicates)
        dim_time_df.drop_duplicates(subset=["report_date"]).to_sql("dim_time", conn, if_exists="append", index=False)

        # Insert into dim_market
        dim_market_df.to_sql("dim_market", conn, if_exists="append", index=False)

        # Insert into fact_financials
        fact_financials_df.to_sql("fact_financials", conn, if_exists="append", index=False)

        # Insert into dim_financial_metrics
        dim_financial_metrics_df.to_sql("dim_financial_metrics", conn, if_exists="append", index=False)

    print("Data successfully inserted into MySQL!")

# Run the insertion function
insert_data()
