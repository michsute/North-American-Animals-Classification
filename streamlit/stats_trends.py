import streamlit as st
import pandas as pd
import altair as alt


def show_stats_trends():

    #read data
    df = pd.read_csv('./test-dataset/df_dashboard-02-time-long-lat.csv', sep=',', encoding='utf-8')
    
    # page title
    st.title("Stat's & Trends")

    # Create three columns with different widths
    col1, col2 = st.columns([3, 1])

    # Ensure the 'timestamp' column is in datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Common Name Filter
    common_name_filter = st.selectbox("Filter by Common Name:", options=["All"] + df['common_name'].dropna().unique().tolist())

    # Filter data by the selected common name
    if common_name_filter != "All":
        filtered_df = df[df['common_name'] == common_name_filter]
    else:
        filtered_df = df

    # Group data by month and year
    trend_df = (
        filtered_df
        .groupby(filtered_df['timestamp'].dt.to_period('M'))  # Group by month
        .size()  # Count occurrences
        .reset_index(name='number of sightings')  # Rename column
        .rename(columns={'timestamp': 'Month'})  # Rename timestamp to Month
    )

    # Convert 'Month' back to datetime for plotting
    trend_df['Month'] = trend_df['Month'].dt.to_timestamp()


    # Create the Altair chart (more costumizable than st.line_chart)
    chart = alt.Chart(trend_df).mark_line(point=True).encode(
        x=alt.X('Month:T', title='Month'),
        y=alt.Y('number of sightings:Q', title='number of sightings', scale=alt.Scale(domainMin=0), axis=alt.Axis(tickMinStep=1)),
        tooltip=['Month', 'number of sightings']
    ).properties(
        width=700,
        height=400,
        title=f"Monthly Trend of Sightings ({common_name_filter})"
    )

    # Display the chart
    st.altair_chart(chart, use_container_width=True)
