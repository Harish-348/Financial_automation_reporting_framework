import streamlit as st
import plotly.express as px
from modules.db_connection import fetch_data

# KPI Query to extract financial metrics
KPI_QUERY = """
SELECT 
    f.ticker,
    YEAR(f.report_date) AS year,
    SUM(f.revenue) AS total_revenue,
    SUM(f.net_income) AS total_net_income,
    AVG(f.eps) AS avg_eps,
    CASE 
        WHEN SUM(f.revenue) = 0 THEN NULL 
        ELSE SUM(f.net_income) / NULLIF(SUM(f.revenue), 0) * 100 
    END AS profit_margin,
    CASE 
        WHEN SUM(m.total_assets) = 0 THEN NULL 
        ELSE SUM(f.net_income) / NULLIF(SUM(m.total_assets), 0) * 100 
    END AS return_on_assets
FROM fact_financials f
JOIN dim_financial_metrics m 
    ON f.ticker = m.ticker AND f.report_date = m.report_date
GROUP BY f.ticker, year;
"""

def show_kpi_dashboard():
    st.subheader("Key Performance Indicators (KPIs)")

    # Fetch KPI data
    data = fetch_data(KPI_QUERY)

    if not data.empty:
        # Display KPI Table
        st.write("### KPI Summary Table")
        st.dataframe(data)
        
        data_filtered = data[data["year"].between(2021, 2024)]

        # Create a Profit Margin Trend Chart
        st.write("### Profit Margin Over Time")
        fig = px.line(data_filtered, x="year", y="profit_margin", color="ticker", 
                      title="Profit Margin Trends", markers=True)
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No KPI data available.")
