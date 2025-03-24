# modules/data_extraction.py
import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import os
from dotenv import load_dotenv
# import os

load_dotenv()


host=os.getenv("host")
user=os.getenv("user")
password=os.getenv("password")
database=os.getenv("database")

DB_CONFIG = {
    "host": host,
    "user": user,
    "password": password,
    "database": database
}
engine = create_engine(f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}")

# List of companies
COMPANIES = ["AAPL", "MSFT", "GOOGL"]

def extract_financials(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    
    # Company Data (dim_company)
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
    market_data["report_date"] = market_data["Date"].dt.date

    market_data["ticker"] = ticker

    
    
    dim_market = market_data.rename(columns={"Close": "closing_price", "Volume": "volume"}).drop(columns=["Date"])
    
    # Time Data (dim_time)
    dim_time = pd.DataFrame({"report_date": dim_market["report_date"].unique()})
    
    # Financial Statements (fact_financials)
    income_stmt = stock.financials.T.fillna(0).reset_index()
    fact_financials = pd.DataFrame({
        "report_date": pd.to_datetime(income_stmt["index"]).dt.date,
        "ticker": ticker,
        "revenue": income_stmt.get("Total Revenue", 0),
        "net_income": income_stmt.get("Net Income", 0),
        "eps": income_stmt.get("Diluted EPS", 0)
    })
    
    # Financial Metrics (dim_financial_metrics)
    balance_sheet = stock.balance_sheet.T.fillna(0).reset_index()
    dim_financial_metrics = pd.DataFrame({
        "report_date": pd.to_datetime(balance_sheet["index"]).dt.date,
        "ticker": ticker,
        "total_assets": balance_sheet.get("Total Assets", 0),
        "total_liabilities": balance_sheet.get("Total Liabilities", 0),
        "equity": balance_sheet.get("Ordinary Shares Number", 0)
    })
    
    return dim_company, dim_time, dim_market, fact_financials, dim_financial_metrics

def extract_and_load_data():
    st.sidebar.write("Extracting financial data...")
    dim_company_list, dim_time_list, dim_market_list, fact_financials_list, dim_financial_metrics_list = [], [], [], [], []
    
    for ticker in COMPANIES:
        company, time, market, financials, metrics = extract_financials(ticker)
        dim_company_list.append(company)
        dim_time_list.append(time)
        dim_market_list.append(market)
        fact_financials_list.append(financials)
        dim_financial_metrics_list.append(metrics)
    
    # Concatenate data
    dim_company_df = pd.concat(dim_company_list, ignore_index=True).drop_duplicates()
    dim_time_df = pd.concat(dim_time_list, ignore_index=True).drop_duplicates()
    dim_market_df = pd.concat(dim_market_list, ignore_index=True)
    fact_financials_df = pd.concat(fact_financials_list, ignore_index=True)
    dim_financial_metrics_df = pd.concat(dim_financial_metrics_list, ignore_index=True)
    
    # Insert into MySQL
    with engine.connect() as conn:
        dim_company_df.to_sql("dim_company", conn, if_exists="append", index=False)
        dim_time_df.to_sql("dim_time", conn, if_exists="append", index=False)
        dim_market_df.to_sql("dim_market", conn, if_exists="append", index=False)
        fact_financials_df.to_sql("fact_financials", conn, if_exists="append", index=False)
        dim_financial_metrics_df.to_sql("dim_financial_metrics", conn, if_exists="append", index=False)
    
    st.sidebar.success("Data successfully inserted into MySQL!")