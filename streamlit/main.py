import streamlit as st
from streamlit_option_menu import option_menu

from dashboard import show_dashboard

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




