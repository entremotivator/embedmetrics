# advanced_engagement_metrics_app.py
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

@st.cache
def generate_engagement_metrics_data(site_name):
    data = {
        'Date': pd.date_range(start='2023-01-01', periods=30),
        f'Session Duration (minutes) - {site_name}': np.random.randint(1, 60, size=30),
        f'Number of Sessions - {site_name}': np.random.randint(10, 100, size=30),
        f'Click-through Rate (%) - {site_name}': np.random.uniform(1, 10, size=30),
        f'Conversion Rate (%) - {site_name}': np.random.uniform(0, 5, size=30),
        f'Pageviews - {site_name}': np.random.randint(50, 200, size=30),
        f'Error Rates (%) - {site_name}': np.random.uniform(0, 2, size=30),
        f'Social Shares - {site_name}': np.random.randint(5, 50, size=30),
        f'Net Promoter Score (NPS) - {site_name}': np.random.randint(0, 10, size=30),
        f'Referral Sources - {site_name}': np.random.choice(['Google', 'Facebook', 'Twitter', 'LinkedIn'], size=30),
        f'Source-specific Engagement - {site_name}': np.random.uniform(0, 1, size=30),
        f'Content Consumption Metrics - Pageviews - {site_name}': np.random.randint(50, 200, size=30),
        f'Content Consumption Metrics - Content Interaction - {site_name}': np.random.uniform(0, 1, size=30),
        f'Error and Debugging Metrics - Error Rates - {site_name}': np.random.uniform(0, 2, size=30),
        f'Error and Debugging Metrics - Debugging Logs - {site_name}': np.random.randint(0, 5, size=30),
        f'Security Metrics - Security Events - {site_name}': np.random.randint(0, 2, size=30),
        f'Security Metrics - Access Control - {site_name}': np.random.randint(0, 1, size=30),
        f'Social Sharing Metrics - Social Shares - {site_name}': np.random.randint(5, 50, size=30),
        f'Social Sharing Metrics - Viral Reach - {site_name}': np.random.randint(0, 100, size=30),
        f'Monetization Metrics - Revenue per User - {site_name}': np.random.uniform(1, 100, size=30),
        f'Monetization Metrics - Conversion Funnel - {site_name}': np.random.uniform(0, 1, size=30),
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

    # Sidebar for site selection
    site_names = st.sidebar.text_input("Enter Site Names (comma-separated)", "Site 1,Site 2,Site 3")
    site_names = [name.strip() for name in site_names.split(',')]

    # Sidebar for frame selection
    frame_names = st.sidebar.multiselect("Select Frames", ["Frame 1", "Frame 2", "Frame 3"], default=["Frame 1"])
    
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

    # Generate example data for each site
    frames_data = {}
    for frame_name in frame_names:
        frames_data[frame_name] = {}
        for site_name in site_names:
            frames_data[frame_name][site_name] = generate_engagement_metrics_data(site_name)

    # Fill missing dates for each frame and site
    for frame_name in frame_names:
        for site_name in site_names:
            frames_data[frame_name][site_name] = fill_missing_dates(frames_data[frame_name][site_name])

    # Filter data based on selected date range
    filtered_data = pd.concat([frames_data[frame_name][site_name] for frame_name in frame_names for site_name in site_names])
    filtered_data = filtered_data[(filtered_data['Date'] >= date_range[0]) & (filtered_data['Date'] <= date_range[1])]

    # Display the filtered data table
    st.write("## User Engagement Metrics Data (Filtered)")
    st.write(filtered_data)

    # Create line charts using Altair with interactivity
    for frame_name in frame_names:
        st.write(f"## {frame_name}")
        for metric in selected_metrics:
            for site_name in site_names:
                y_title = f"{metric} - {site_name}"
                st.write(f"### {metric} Chart for {site_name}")
                st.altair_chart(plot_metric_chart(frames_data[frame_name][site_name], f'{metric} - {site_name}', 'blue', y_title))

    # Summary Statistics
    st.write("## Summary Statistics")
    st.write(filtered_data.describe())

if __name__ == "__main__":
    main()
