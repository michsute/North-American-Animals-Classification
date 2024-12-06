import streamlit as st"
# page title
st.title("North American Animals Classification")

# Create three columns with different widths
col1, col2, col3 = st.columns([1, 2, 1])

# Content for the first column
with col1:
    st.header("Column 1")
    st.write("text")

# Content for the second column
with col2:
    st.header("Column 2")
    st.write("text")

# Content for the third column
with col3:
    st.header("Column 3")
    st.write("text")