import streamlit as st
import pandas as pd

# if "metadata" not in st.session_state:
#   metadata = pd.read_csv("meta.csv").drop(columns=['TABLE_NAME'])
#   st.session_state.metadata = metadata
# metadata = st.session_state.metadata
metadata = pd.read_csv("meta.csv").drop(columns=['TABLE_NAME'])

# Set up the Streamlit app layout
st.title("Chat with Database")
st.subheader("Iowa Liquor Retail Sales Metadata")
st.caption("Liquor sales in Iowa since 2012, by store, by item, and by day")

st.divider()
st.subheader("Table Name: sales")
st.dataframe(metadata, hide_index=True)

st.rerun()