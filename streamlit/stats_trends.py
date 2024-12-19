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

    with col1:

        st.subheader("trends over time")

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
            tooltip=['Month', 'number of sightings'],
            color=alt.value("#44592f"),
        ).properties(
            width=700,
            height=400,
            title=f"Monthly Trend of Sightings ({common_name_filter})"
        )

        # Display the chart
        st.altair_chart(chart, use_container_width=True)

        
        st.subheader("camera activity / location")

        # Convert 'timestamp' to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Extract year and month
        df['year'] = df['timestamp'].dt.year
        df['month'] = df['timestamp'].dt.month

        # Year filter
        years = sorted(df['year'].unique())
        selected_year = st.selectbox("Select Year", years, index=len(years) - 1)

        # Month filter
        months = {
            1: "January", 2: "February", 3: "March", 4: "April", 
            5: "May", 6: "June", 7: "July", 8: "August", 
            9: "September", 10: "October", 11: "November", 12: "December"
        }
        month_options = sorted(months.items())
        selected_months = st.multiselect(
        "Select Months", 
        [name for _, name in month_options],
        default=[name for _, name in month_options]  # Select all months by default
    )
        # Map selected month names back to numbers
        selected_month_numbers = [num for num, name in month_options if name in selected_months]


        # Filter the DataFrame based on selections
        filtered_df = df[(df['year'] == selected_year) & (df['month'].isin(selected_month_numbers))]



        # Preprocessing: Count the number of captures per camera ID
        camera_activity = filtered_df['location'].value_counts().reset_index()
        camera_activity.columns = ['Location', 'Activity Count']

        # Create a bar chart using Altair
        if not camera_activity.empty:
            chart = alt.Chart(camera_activity).mark_bar().encode(
                x=alt.X('Location:O', sort='-y', title='Location'),
                y=alt.Y('Activity Count:Q', title='Number of Captures'),
                tooltip=['Location', 'Activity Count'],
                color=alt.value("#44592f")
            ).properties(
                title=f'Most Active Cameras in {', '.join(selected_months)} {selected_year}',
                width=800,
                height=400
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.write(f"No data available for the selected months in {selected_year}.")
