import streamlit as st

def show_dashboard():

    # page title
    st.title("Dashboard")

    # Create three columns with different widths
    col1, col2 = st.columns([3, 1])

    # Content for the first column
    with col1:
        st.header("Map")
        st.write("text")

    # Content for the second column
    with col2:
        st.header("Alerts")
        st.write("text")

