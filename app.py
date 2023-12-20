# advanced_engagement_metrics_app.py
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

@st.cache
def generate_engagement_metrics_data():
    data = {
        'Date': pd.date_range(start='2023-01-01', periods=30),
        'Session Duration (minutes)': np.random.randint(1, 60, size=30),
        'Number of Sessions': np.random.randint(10, 100, size=30),
        'Click-through Rate (%)': np.random.uniform(1, 10, size=30),
        'Conversion Rate (%)': np.random.uniform(0, 5, size=30),
        'Pageviews': np.random.randint(50, 200, size=30),
        'Error Rates (%)': np.random.uniform(0, 2, size=30),
        'Social Shares': np.random.randint(5, 50, size=30),
        'Net Promoter Score (NPS)': np.random.randint(0, 10, size=30),
        'Referral Sources': np.random.choice(['Google', 'Facebook', 'Twitter', 'LinkedIn'], size=30),
        'Source-specific Engagement': np.random.uniform(0, 1, size=30),
        'Content Consumption Metrics - Pageviews': np.random.randint(50, 200, size=30),
        'Content Consumption Metrics - Content Interaction': np.random.uniform(0, 1, size=30),
        'Error and Debugging Metrics - Error Rates': np.random.uniform(0, 2, size=30),
        'Error and Debugging Metrics - Debugging Logs': np.random.randint(0, 5, size=30),
        'Security Metrics - Security Events': np.random.randint(0, 2, size=30),
        'Security Metrics - Access Control': np.random.randint(0, 1, size=30),
        'Social Sharing Metrics - Social Shares': np.random.randint(5, 50, size=30),
        'Social Sharing Metrics - Viral Reach': np.random.randint(0, 100, size=30),
        'Monetization Metrics - Revenue per User': np.random.uniform(1, 100, size=30),
        'Monetization Metrics - Conversion Funnel': np.random.uniform(0, 1, size=30),
    }
    return pd.DataFrame(data)

def fill_missing_dates(data, date_col='Date'):
    all_dates = pd.date_range(start=data[date_col].min(), end=data[date_col].max())
    return pd.DataFrame(all_dates, columns=[date_col]).merge(data, on=date_col, how='left')

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
    selected_metrics = st.sidebar.multiselect("Select Metrics", [
        "Session Duration (minutes)",
        "Number of Sessions",
        "Click-through Rate (%)",
        "Conversion Rate (%)",
        "Pageviews",
        "Error Rates (%)",
        "Social Shares",
        "Net Promoter Score (NPS)",
        "Referral Sources",
        "Source-specific Engagement",
        "Content Consumption Metrics - Pageviews",
        "Content Consumption Metrics - Content Interaction",
        "Error and Debugging Metrics - Error Rates",
        "Error and Debugging Metrics - Debugging Logs",
        "Security Metrics - Security Events",
        "Security Metrics - Access Control",
        "Social Sharing Metrics - Social Shares",
        "Social Sharing Metrics - Viral Reach",
        "Monetization Metrics - Revenue per User",
        "Monetization Metrics - Conversion Funnel",
    ], default=[
        "Session Duration (minutes)",
        "Number of Sessions",
        "Click-through Rate (%)",
        "Conversion Rate (%)",
        "Pageviews",
        "Error Rates (%)",
        "Social Shares",
    ])
    
    date_range = st.sidebar.date_input("Select Date Range:", [pd.to_datetime("2023-01-01"), pd.to_datetime("2023-01-30")], key="date_range")

    # Convert date range values to numpy.datetime64
    date_range = [np.datetime64(date) for date in date_range]

    # Generate example data
    engagement_metrics_data = generate_engagement_metrics_data()

    # Fill missing dates for each metric
    filled_data = fill_missing_dates(engagement_metrics_data)

    # Filter data based on selected date range
    filtered_data = filled_data[(filled_data['Date'] >= date_range[0]) & (filled_data['Date'] <= date_range[1])]

    # Display the filtered data table
    st.write("## User Engagement Metrics Data (Filtered)")
    st.write(filtered_data)

    # Create line charts using Altair with interactivity
    for metric in selected_metrics:
        st.write(f"## {metric} Chart")
        y_title = metric.split(" - ")[-1] if " - " in metric else metric
        st.altair_chart(plot_metric_chart(filtered_data, metric, 'blue', y_title))

    # Summary Statistics
    st.write("## Summary Statistics")
    st.write(filtered_data.describe())

if __name__ == "__main__":
    main()

