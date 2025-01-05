import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np



def show_dashboard():

    df = pd.read_csv('./test-dataset/df_dashboard-02-time-long-lat.csv', sep=',', encoding='utf-8')
    
    # Konvertiere die Zeitspalte in ein Datum-Zeit-Format
    df['timestamp'] = pd.to_datetime(df['timestamp'])


    spezies_colors = {
        "american black bear": [0, 0, 0, 255],               # Schwarz
        "coyote": [255, 140, 0, 255],                        # Leuchtendes Orange
        "gray fox": [128, 128, 128, 255],                    # Mittelgrau
        "striped skunk": [255, 255, 0, 255],                 # Leuchtendes Gelb
        "bobcat": [139, 69, 19, 255],                        # Dunkelbraun
        "elk": [34, 139, 34, 255],                           # Dunkelgrün
        "mule deer": [255, 165, 0, 255],                     # Helles Orange
        "unidentified deer": [0, 191, 255, 255],             # Helles Blau
        "california ground squirrel": [75, 0, 130, 255],     # Indigo
        "empty": [255, 0, 0, 255],                           # Rot
        "red deer": [255, 69, 0, 255],                       # Rot-orange
        "wild boar": [139, 0, 0, 255],                       # Dunkelrot
    }

    # page title
    st.title("Dashboard")

    # Create three columns with different widths
    col1, col2 = st.columns([3, 1])

    # Content for the second column
    with col2:
        st.header("Alerts")
        st.write("No unusual incidents at present")


    # Content for the first column
    with col1:
        st.header("Map")


        # Filter for species
        species_options = df['common_name'].unique()
        selected_animals = st.multiselect("Choose species:", species_options)
        

        # if no species is selected show error
        if not selected_animals:
            st.error("Please choose at least one species")
            return
        
        # filter the data for selected species
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

        # Add slight random offsets to the latitude and longitude for each species
        offset_magnitude = 0.01  # Adjust this value for more/less separation
        filtered_data['latitude'] = filtered_data['latitude'] + np.random.uniform(-offset_magnitude, offset_magnitude, size=len(filtered_data))
        filtered_data['longitude'] = filtered_data['longitude'] + np.random.uniform(-offset_magnitude, offset_magnitude, size=len(filtered_data))

        # Feste Farben zuweisen
        filtered_data['color'] = filtered_data['common_name'].map(spezies_colors)

        # convert `timestamp` for tooltip
        filtered_data['formatted_time'] = filtered_data['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

        # Tooltip configuration
        tooltip = {
            "html": "<b>Species:</b> {common_name}<br>"
                    "<b>Timestamp:</b> {formatted_time}<br>",
            "style": {
                "backgroundColor": "steelblue",
                "color": "white",
                "fontSize": "12px",
                "borderRadius": "5px",
                "padding": "10px"
            }
        }

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
                    get_color='color',
                    get_radius=6000,
                    radius_min_pixels=1,  # Minimum pixel size
                    radius_max_pixels=15,  # Maximum pixel size when zoomed out 
                    pickable=True,
                ),
            ],
            tooltip=tooltip  # Add the tooltip
        ))

        st.write(''' This map visualizes the distribution of selected animal species 
                 across different locations. Choose your species and time range to filter 
                 the data. Hover over a location to see more details about the animal sightings at that point.
                 ''')
   

