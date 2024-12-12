import streamlit as st
from streamlit_option_menu import option_menu

from dashboard import show_dashboard
from stats_trends import show_stats_trends
from cameras_numbers import show_cameras_numbers


#use wide mode
st.set_page_config(layout="wide")

st.sidebar.title("North American Animals Classification")

with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Stat's & Trends", "Cameras & Numbers", "Settings"],
        icons=["house", "graph-up",  "clipboard-data", "gear"]
    )



if selected == "Dashboard":
    show_dashboard()

if selected == "Stat's & Trends":
    show_stats_trends()

if selected == "Cameras & Numbers":
    show_cameras_numbers()

    



