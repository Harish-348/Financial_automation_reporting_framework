# # module/aggregate_tables.py
# import streamlit as st
# import plotly.express as px
# from modules.db_connection import fetch_data

# def show_aggregate_tables():
#     st.subheader("Aggregated Financial Data")
#     data = fetch_data("SELECT * FROM agg_revenue_net_income")
#     if not data.empty:
#         fig = px.line(data, x="year", y=["total_revenue", "total_net_income"], color="ticker", title="Total Revenue vs Net Income")
#         st.plotly_chart(fig)
#         st.dataframe(data)
#     else:
#         st.warning("No data available.")
import streamlit as st
import plotly.express as px
from modules.db_connection import fetch_data, execute_queries
from modules.queries import AGG_QUERIES

def show_aggregate_tables():
    st.subheader("Aggregated Financial Data")
    
    # Ensure aggregate tables exist
    execute_queries(AGG_QUERIES)
    
    # Define tables with corresponding visualization types
    agg_tables = {
        "Total Revenue vs Net Income": {
            "table": "agg_revenue_net_income",
            "y": ["total_revenue", "total_net_income"],
            "chart_type": "funnel"
        },
        "Market Performance": {
            "table": "agg_market_performance",
            "y": ["avg_closing_price", "total_volume"],
            "chart_type": "line"
        },
        "Earnings Per Share (EPS)": {
            "table": "kpi_metrics",
            "y": "profit_margin",
            "chart_type": "bubble"
        }
    }
    
    for title, config in agg_tables.items():
        st.subheader(f"{title}")
        
        # Fetch data
        data = fetch_data(f"SELECT * FROM {config['table']}")

        if not data.empty:
            # Ensure `year` column is integer to avoid float values
            data["year"] = data["year"].astype(int)

            # Filter for only 2024 and 2025
            data = data[data["year"].isin([2024, 2025])]

            if data.empty:
                st.warning(f"No relevant data for {title} (Only 2024 & 2025 shown).")
                continue

            # Choose appropriate visualization
            if config["chart_type"] == "line":
                fig = px.line(data, x="year", y=config["y"], color="ticker", title=title, markers=True)
            elif config["chart_type"] == "bar":
                fig = px.bar(data, x="year", y=config["y"], color="ticker", barmode="stack", title=title)
            elif config["chart_type"] == "area":
                fig = px.area(data, x="year", y=config["y"], color="ticker", title=title)
            elif config["chart_type"] == "scatter":
                fig = px.scatter(data, x="year", y=config["y"], color="ticker", size=config["y"], title=title)
            elif config["chart_type"] == "bubble":
                # Ensure the `y` column exists in the data and is numeric
                if config["y"] in data.columns and data[config["y"]].dtype in ["int64", "float64"]:
                    fig = px.scatter(
                        data, x="year", y=config["y"], color="ticker",
                        size=data[config["y"]].abs(), size_max=60, 
                        title=title, opacity=0.7
                    )
                else:
                    st.warning(f"Invalid column '{config['y']}' for Bubble Chart in {title}. Skipping visualization.")
                    continue
            elif config["chart_type"] == "funnel":
                fig = px.funnel(data, x="year", y=config["y"], color="ticker", title=title)
            elif config["chart_type"] == "heatmap":
                fig = px.density_heatmap(data, x="year", y=config["y"], z="ticker", title=title)

            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(data)
        else:
            st.warning(f"No data available for {title}.")
