import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np



def show_dashboard():

    df = pd.read_csv('./test-dataset/df_dashboard-02-time-long-lat.csv', sep=',', encoding='utf-8')
    
    # Konvertiere die Zeitspalte in ein Datum-Zeit-Format
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # page title
    st.title("Dashboard")

    # Create three columns with different widths
    col1, col2 = st.columns([3, 1])

    # Content for the second column
    with col2:
        st.header("Alerts")
        st.write("text")


    # Content for the first column
    with col1:
        st.header("Map")


        # Filter für die Tierarten
        species_options = df['common_name'].unique()
        selected_animals = st.multiselect("Choose species:", species_options)
        

        # Wenn keine Tiere ausgewählt sind, zeige eine Fehlermeldung
        if not selected_animals:
            st.error("Please choose at least one species")
            return
        
        # Filtere die Daten nach den ausgewählten Tieren
        filtered_animal_data = df[df['common_name'].isin(selected_animals)]

        min_date = df['timestamp'].min().date()
        max_date = df['timestamp'].max().date() 

        selected_time = st.slider(
            "Choose a time:",
            min_value=min_date,
            max_value=max_date,
            value=min_date,
            format="YYYY-MM-DD"
            )

        # Convert selected_time to datetime if it's a pandas Timestamp
        selected_time = selected_time.to_pydatetime() if isinstance(selected_time, pd.Timestamp) else selected_time

        # Filter data based on the selected time
        filtered_data = filtered_animal_data[filtered_animal_data['timestamp'].dt.date <= selected_time]

        # Farbcodierung für jede Spezies
        spezies_colors = {animal: [int(np.random.randint(0, 255)), int(np.random.randint(0, 255)), int(np.random.randint(0, 255)), 255] for animal in selected_animals}



        # Pydeck-Karte erstellen
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=35.0,
                longitude=-110.0,
                zoom=5,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=filtered_data,
                    get_position='[longitude, latitude]',
                    get_color=spezies_colors,
                    get_radius=40000,
                    pickable=True,
                ),
            ],
        ))


        st.write("text")

        st.write(df)

   

