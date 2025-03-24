# --- SQL Queries for Aggregation & KPIs ---
AGG_QUERIES = [
    """
    CREATE TABLE IF NOT EXISTS agg_revenue_net_income AS
    SELECT 
        YEAR(f.report_date) AS year,
        f.ticker,
        SUM(f.revenue) AS total_revenue,
        SUM(f.net_income) AS total_net_income
    FROM fact_financials f
    GROUP BY year, f.ticker;
    """,
    
    """
    CREATE TABLE IF NOT EXISTS agg_market_performance AS
    SELECT 
        m.ticker,
        YEAR(m.report_date) AS year,
        AVG(m.closing_price) AS avg_closing_price,
        SUM(m.volume) AS total_volume
    FROM dim_market m
    GROUP BY m.ticker, year;
    """,
    
    """
    CREATE TABLE IF NOT EXISTS kpi_metrics AS
    SELECT 
        f.ticker,
        YEAR(f.report_date) AS year,
        CASE 
            WHEN SUM(m.shares_outstanding) = 0 THEN NULL 
            ELSE SUM(f.net_income) / NULLIF(SUM(m.shares_outstanding), 0) 
        END AS earnings_per_share
    FROM fact_financials f
    JOIN dim_financial_metrics m ON f.ticker = m.ticker AND f.report_date = m.report_date
    GROUP BY f.ticker, year;
    """
]

# --- SQL Queries for Data Marts ---
DATA_MART_QUERIES = [
    """
    CREATE TABLE IF NOT EXISTS profitability_mart AS
    SELECT 
        f.ticker,
        YEAR(f.report_date) AS year,
        SUM(f.revenue) AS total_revenue,
        SUM(f.net_income) AS total_net_income,
        CASE 
            WHEN SUM(f.revenue) = 0 THEN NULL 
            ELSE SUM(f.net_income) / NULLIF(SUM(f.revenue), 0) * 100 
        END AS profit_margin,
        CASE 
            WHEN SUM(m.total_assets) = 0 THEN NULL 
            ELSE SUM(f.net_income) / NULLIF(SUM(m.total_assets), 0) * 100 
        END AS return_on_assets
    FROM fact_financials f
    JOIN dim_financial_metrics m ON f.ticker = m.ticker AND f.report_date = m.report_date
    GROUP BY f.ticker, year;
    """,

    """
    CREATE TABLE IF NOT EXISTS market_performance_mart AS
    SELECT 
        m.ticker,
        YEAR(m.report_date) AS year,
        AVG(m.closing_price) AS avg_closing_price,
        MAX(m.closing_price) AS highest_price,
        MIN(m.closing_price) AS lowest_price,
        SUM(m.volume) AS total_trading_volume
    FROM dim_market m
    GROUP BY m.ticker, year;
    """
]