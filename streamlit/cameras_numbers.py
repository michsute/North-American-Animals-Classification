import streamlit as st
import pandas as pd

def show_cameras_numbers():
    
    # page title
    st.title("Cameras & Numbers")

    df = pd.read_csv('./test-dataset/df_dashboard-02-time-long-lat.csv', sep=',', encoding='utf-8')

    # Sicherstellen, dass die 'timestamp'-Spalte als Datetime interpretiert wird
    df['timestamp'] = pd.to_datetime(df['timestamp'])


    st.subheader("Filter Options")

    # Multi-Select-Filter für 'location'
    location_filter = st.multiselect(
        "Filter by Location:", 
        options=df['location'].dropna().unique().tolist(),
        default=[]
    )

    # Multi-Select-Filter für 'common_name'
    common_name_filter = st.multiselect(
        "Filter by Common Name:", 
        options=df['common_name'].dropna().unique().tolist(),
        default=[]
    )

    # Zeitraum auswählen
    col1, col2 = st.columns(2)
    start_date = col1.date_input("Start Date", value=df['timestamp'].min().date())
    end_date = col2.date_input("End Date", value=df['timestamp'].max().date())


    # Filtern der Tabelle
    filtered_df = df.copy()

    # Zeitraumfilter anwenden
    filtered_df = filtered_df[(filtered_df['timestamp'] >= pd.Timestamp(start_date)) & (filtered_df['timestamp'] <= pd.Timestamp(end_date))]

    # Location-Filter anwenden
    if location_filter:
        filtered_df = filtered_df[filtered_df['location'].isin(location_filter)]    

    # Common Name-Filter anwenden
    if common_name_filter:
        filtered_df = filtered_df[filtered_df['common_name'].isin(common_name_filter)]


    st.subheader("Sightings")

    # Gefilterte Tabelle anzeigen
    st.dataframe(filtered_df, column_order=("timestamp", "common_name", "name", "location", "id"), hide_index=True)

