import streamlit as st
from modules.aggregate_tables import show_aggregate_tables
from modules.data_marts import show_data_marts
from modules.kpi_dashboard import show_kpi_dashboard  # Import the new KPI module

def main():
    st.sidebar.title("Navigation")

    selected_option = st.sidebar.radio(
        "Choose a section:", 
        ["Home", "Schema Overview", "KPI Overview", "Aggregate Tables", "Data Marts"]
    )

    st.title("Financial Reporting Automation Framework")

    if selected_option == "Home":
        st.subheader("Project Overview")
        st.markdown(
            """
            This **Financial Reporting Automation Framework** streamlines financial analysis by automating data extraction, transformation, and visualization.  
            
            🔹 **Key Features:**
            - **KPI Dashboard**: Track key financial ratios and performance metrics.
            - **Aggregated Financial Data**: Summarized revenue, net income, and market performance trends.
            - **Data Marts**: Structured insights for profitability and market performance.
            - **Dynamic Visualizations**: Interactive charts for better financial decision-making.
            
            Navigate through the sidebar to explore different sections.
            """
        )

    elif selected_option == "Schema Overview":
        st.subheader("Database Schema & Star Schema Design")
        st.image("star_schema.jpg", caption="Star Schema Diagram", use_container_width=True)
        st.markdown(
            """
            The project follows a **Star Schema** to efficiently organize financial data. This structure allows for optimized querying, aggregation, and reporting.

            ### 🔹 **Fact Table:**
            The central **fact_financials** table contains key financial metrics like:
            - **Revenue**
            - **Net Income**
            - **Earnings Per Share (EPS)**

            ### 🔹 **Dimension Tables:**
            The supporting dimension tables provide context:
            - **dim_company**: Company metadata (name, sector, industry, market cap, country).
            - **dim_time**: Time-related attributes for period-based analysis.
            - **dim_market**: Market performance data (closing price, volume).
            - **dim_financial_metrics**: Assets, liabilities, and equity details.

            ### **Why Use a Star Schema?**
            - **Faster Query Performance**: Simplifies joins and improves aggregation speed.
            - **Scalability**: Well-structured for large financial datasets.
            - **Better Data Integrity**: Ensures consistency in financial reporting.

            This schema enables seamless financial reporting and KPI tracking.
            """
        )

    elif selected_option == "KPI Overview":
        show_kpi_dashboard()  # Call the KPI Dashboard module

    elif selected_option == "Aggregate Tables":
        show_aggregate_tables()

    elif selected_option == "Data Marts":
        show_data_marts()

if __name__ == '__main__':
    main()
