import streamlit as st
import pandas as pd

# Set up the Streamlit app layout
chat_page = st.Page("page_chat.py", title="Chatbot")
meta_page = st.Page("page_meta.py", title="Metadata")
simple_page = st.Page("page_simple.py", title="Simple Question")

pg = st.navigation({"Page Menu":[chat_page, meta_page, simple_page]})
st.set_page_config(page_title="Chat with Data")
pg.run()