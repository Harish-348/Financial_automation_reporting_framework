# module/data_marts.py
import streamlit as st
import plotly.express as px
from modules.db_connection import fetch_data

def show_data_marts():
    st.subheader("Data Marts")

    # --- Profitability Data Mart ---
    st.subheader("Profitability Metrics")
    profitability_data = fetch_data("SELECT * FROM profitability_mart")
    
    if not profitability_data.empty:
        profitability_data["year"] = profitability_data["year"].astype(int)

        # Line chart for profit margin
        fig_profit_margin = px.line(
            profitability_data[profitability_data['year'].between(2021, 2024)], x="year", y="profit_margin", color="ticker",
            title="Profit Margin Over Time", markers=True
        )
        st.plotly_chart(fig_profit_margin, use_container_width=True)

        # Bar chart for return on assets
        fig_return_on_assets = px.bar(
            profitability_data[profitability_data['year'].between(2021, 2024)], x="year", y="return_on_assets", color="ticker",
            title="Return on Assets Over Time", barmode="group"
        )
        st.plotly_chart(fig_return_on_assets, use_container_width=True)

        # Display profitability data
        st.dataframe(profitability_data)
    else:
        st.warning("No data available for Profitability Metrics.")

    # --- Market Performance Data Mart ---
    st.subheader("Market Performance Metrics")
    market_data = fetch_data("SELECT * FROM market_performance_mart")
    
    if not market_data.empty:
        market_data["year"] = market_data["year"].astype(int)

        # Line chart for avg closing price
        fig_avg_price = px.line(
            market_data, x="year", y="avg_closing_price", color="ticker",
            title="Average Closing Price Over Time", markers=True
        )
        st.plotly_chart(fig_avg_price, use_container_width=True)

        # Bar chart for total trading volume
        fig_trading_volume = px.bar(
            market_data[market_data['year'].between(2024, 2025)], x="year", y="total_trading_volume", color="ticker",
            title="Total Trading Volume Over Time", barmode="stack"
        )
        st.plotly_chart(fig_trading_volume, use_container_width=True)

        # Display market performance data
        st.dataframe(market_data)
    else:
        st.warning("No data available for Market Performance Metrics.")
