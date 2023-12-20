# advanced_engagement_metrics_app.py
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

@st.cache
def generate_engagement_metrics_data():
    data = {
        'Date': pd.date_range(start='2023-01-01', periods=30),
        'Session Duration (minutes)': np.random.randint(1, 30, size=30),
        'Number of Sessions': np.random.randint(10, 100, size=30),
        'Click-through Rate (%)': np.random.uniform(1, 10, size=30),
        'Conversion Rate (%)': np.random.uniform(0, 5, size=30),
        'Pageviews': np.random.randint(50, 200, size=30),
        'Error Rates (%)': np.random.uniform(0, 2, size=30),
        'Social Shares': np.random.randint(5, 50, size=30),
    }
    return pd.DataFrame(data)

def plot_metric_chart(data, metric, color, y_title):
    chart = alt.Chart(data).mark_line().encode(
        x='Date:T',
        y=alt.Y(f'{metric}:Q', axis=alt.Axis(title=y_title)),
        color=alt.value(color),
        tooltip=['Date:T', f'{metric}:Q']
    ).properties(width=800, height=300)

    # Add average line
    average_line = alt.Chart(data).mark_rule(color='gray').encode(
        y=f'average({metric}):Q',
        size=alt.value(2)
    )
    
    return chart + average_line

def main():
    st.title("User Engagement Metrics")

    # Sidebar for metric selection and date range
    selected_metrics = st.sidebar.multiselect("Select Metrics", ["Session Duration", "Number of Sessions", "Click-through Rate", "Conversion Rate", "Pageviews", "Error Rates", "Social Shares"], default=["Session Duration", "Number of Sessions"])
    
    date_range = st.sidebar.date_input("Select Date Range:", [pd.to_datetime("2023-01-01"), pd.to_datetime("2023-01-30")], key="date_range")

    # Generate example data
    engagement_metrics_data = generate_engagement_metrics_data()

    # Filter data based on selected date range
    filtered_data = engagement_metrics_data[(engagement_metrics_data['Date'] >= date_range[0]) & (engagement_metrics_data['Date'] <= date_range[1])]

    # Display the filtered data table
    st.write("## User Engagement Metrics Data (Filtered)")
    st.write(filtered_data)

    # Create line charts using Altair with interactivity
    for metric in selected_metrics:
        st.write(f"## {metric} Chart")
        st.altair_chart(plot_metric_chart(filtered_data, metric, 'blue', f'{metric}'))

    # Summary Statistics
    st.write("## Summary Statistics")
    st.write(filtered_data.describe())

if __name__ == "__main__":
    main()
