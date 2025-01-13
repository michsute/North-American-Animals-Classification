import streamlit as st
import pandas as pd
import altair as alt
from datetime import timedelta
from pathlib import Path


def show_stats_trends():

    # Setze den absoluten Pfad des aktuellen Verzeichnisses
    dir = Path(__file__).resolve().parent

    # Pfad zur CSV-Datei 
    path_to_csv = dir.parent / 'streamlit' / 'test-dataset' / 'df_dashboard-02-time-long-lat.csv'  

    # Load the data
    df = pd.read_csv(path_to_csv, sep=',', encoding='utf-8')
    
    # page title
    st.title("Stat's & Trends")

    # Create three columns with different widths
    #col1, col2 = st.columns([3, 1])

    

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

    st.write('''This chart displays the monthly trend of animal sightings. 
             You can filter the data by the common name of the species, 
             and the chart will show how the number of sightings has changed over time. 
             Each point on the line represents the total number of sightings for that month. 
             over over the chart to view the exact number of sightings for each month. ''')

    st.markdown('#')


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
            #title=f'Most Active Cameras in {', '.join(selected_months)} {selected_year}',
            width=800,
            height=400
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.write(f"No data available for the selected months in {selected_year}.")

    st.write('''This bar chart visualizes the camera activity for the selected year and months. 
             It shows the number of animal captures at each location, with the locations listed 
             on the x-axis and the capture counts on the y-axis. You can filter the data by year 
             and month to see how the activity at each location varies over time. Hover over each 
             bar to view the exact count of captures for each location. ''')

    st.markdown('#')

    st.subheader("species co-occurrence analysis")

    # Load the dataset
    df = pd.read_csv(path_to_csv, sep=',', encoding='utf-8')

    # Ensure the 'timestamp' column is in datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Create a new DataFrame to track species at each location
    df_filtered = df[['location', 'common_name']].drop_duplicates()

    # Create a list of species pairs that occur together at the same location (ignoring timestamp)
    species_pairs = []
    for _, group in df_filtered.groupby('location'):  # Group only by location
        species_list = group['common_name'].tolist()
        for i in range(len(species_list)):
            for j in range(i + 1, len(species_list)):
                species_pairs.append((species_list[i], species_list[j]))

    # Create a DataFrame from the species pairs
    species_pair_df = pd.DataFrame(species_pairs, columns=['Species1', 'Species2'])

    # Count the number of times each pair co-occurs at the same location
    co_occurrence = species_pair_df.groupby(['Species1', 'Species2']).size().reset_index(name='Co-occurrence')


    # Create the Altair heatmap
    heatmap = alt.Chart(co_occurrence).mark_rect().encode(
        x=alt.X('Species1:N', title=None, sort=alt.SortField('Co-occurrence', order='descending')),
        y=alt.Y('Species2:N', title=None, sort=alt.SortField('Co-occurrence', order='descending')),
        color=alt.Color('Co-occurrence:Q', scale=alt.Scale(range=['#f0f0f0', '#44592f'])),  # Custom color scale
        tooltip=['Species1', 'Species2', 'Co-occurrence']
    ).properties(
        width=600,
        height=600,
        title="Species Co-occurrence Heatmap (By Location, Timestamp Ignored)"
    )

    # Display the heatmap
    st.altair_chart(heatmap, use_container_width=True)

    st.markdown('''
                This heatmap visualizes the co-occurrence of species at the same location, 
                without considering the time. Darker cells indicate higher co-occurrence, 
                while lighter cells represent less frequent pairings. Hovering over a cell 
                reveals the exact count of co-occurrences.''')
    
